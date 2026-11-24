"""Policy-as-code engine: evaluates Terraform plan JSON against the guardrail catalogue."""
import datetime
import json

MAX_EXCEPTION_DAYS = 180
OPEN = ("0.0.0.0/0", "::/0")


def load_json(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def get_path(obj, path):
    cur = obj
    for part in path.split("."):
        if isinstance(cur, list):
            try:
                cur = cur[int(part)]
            except (ValueError, IndexError):
                return None
        elif isinstance(cur, dict):
            cur = cur.get(part)
        else:
            return None
        if cur is None:
            return None
    return cur


def _resources(plan, types):
    for rc in plan.get("resource_changes", []):
        actions = rc.get("change", {}).get("actions", [])
        if actions in (["no-op"], ["delete"], ["read"]):
            continue
        after = rc.get("change", {}).get("after") or {}
        if types is None or rc.get("type") in types:
            yield rc["address"], rc["type"], after


def _tags(after):
    t = after.get("tags_all")
    if not isinstance(t, dict):
        t = after.get("tags")
    return t if isinstance(t, dict) else {}


def _port_hit(frm, to, proto, ports):
    if proto in ("-1", "all"):
        return True
    if frm is None or to is None:
        return False
    return any(frm <= p <= to for p in ports)


def _wildcard_admin(policy_json):
    try:
        doc = json.loads(policy_json) if isinstance(policy_json, str) else policy_json
    except ValueError:
        return False
    stmts = doc.get("Statement", [])
    stmts = [stmts] if isinstance(stmts, dict) else stmts
    for s in stmts:
        if s.get("Effect") != "Allow":
            continue
        acts = s.get("Action", [])
        res = s.get("Resource", [])
        acts = [acts] if isinstance(acts, str) else acts
        res = [res] if isinstance(res, str) else res
        if "*" in acts and "*" in res:
            return True
    return False


def evaluate_rule(g, plan):
    """Yield (address, message) for each violation of guardrail g."""
    chk = g.get("check")
    if not chk:
        return
    t = chk["type"]
    types = set(chk["resource_types"]) if "resource_types" in chk else None
    if t == "attrs_true":
        for addr, _, after in _resources(plan, types):
            for attr in chk["attrs"]:
                if after.get(attr) is not True:
                    yield addr, f"{attr} must be true"
    elif t == "attr_eq":
        for addr, _, after in _resources(plan, types):
            v = get_path(after, chk["path"])
            if v != chk["value"]:
                yield addr, f"{chk['path']} must equal {chk['value']!r} (found {v!r})"
    elif t == "attr_not_eq":
        for addr, _, after in _resources(plan, types):
            if get_path(after, chk["path"]) == chk["value"]:
                yield addr, f"{chk['path']} must not equal {chk['value']!r}"
    elif t == "required_tags":
        for addr, _, after in _resources(plan, types):
            missing = [k for k in chk["tags"] if k not in _tags(after)]
            if missing:
                yield addr, "missing tags: " + ", ".join(missing)
    elif t == "no_open_ingress":
        ports = chk["ports"]
        for addr, rtype, after in _resources(plan, {"aws_security_group", "aws_security_group_rule", "aws_vpc_security_group_ingress_rule"}):
            rules = []
            if rtype == "aws_security_group":
                for r in after.get("ingress") or []:
                    rules.append((r.get("cidr_blocks", []) + r.get("ipv6_cidr_blocks", []), r.get("from_port"), r.get("to_port"), str(r.get("protocol"))))
            elif rtype == "aws_security_group_rule" and after.get("type") == "ingress":
                rules.append(((after.get("cidr_blocks") or []) + (after.get("ipv6_cidr_blocks") or []), after.get("from_port"), after.get("to_port"), str(after.get("protocol"))))
            elif rtype == "aws_vpc_security_group_ingress_rule":
                rules.append(([c for c in (after.get("cidr_ipv4"), after.get("cidr_ipv6")) if c], after.get("from_port"), after.get("to_port"), str(after.get("ip_protocol"))))
            for cidrs, frm, to, proto in rules:
                if any(c in OPEN for c in cidrs) and _port_hit(frm, to, proto, ports):
                    yield addr, f"open ingress to admin ports {ports} from the internet"
    elif t == "allowed_regions":
        for name, cfg in (plan.get("configuration", {}).get("provider_config", {}) or {}).items():
            if cfg.get("name") == "aws":
                region = get_path(cfg, "expressions.region.constant_value")
                if region and region not in chk["regions"]:
                    yield f"provider.{name}", f"region {region} is not in the approved list"
    elif t == "iam_no_wildcard_admin":
        for addr, _, after in _resources(plan, {"aws_iam_policy", "aws_iam_role_policy", "aws_iam_user_policy", "aws_iam_group_policy"}):
            if _wildcard_admin(after.get("policy")):
                yield addr, "policy allows Action * on Resource *"
    else:
        raise ValueError(f"unknown rule type {t}")


def validate_exceptions(exc_data, catalogue_ids):
    errors, seen = [], set()
    for e in exc_data.get("exceptions", []):
        eid = e.get("id", "?")
        for f in ("id", "guardrail", "resource", "created", "expires", "approver", "ticket", "justification", "compensating_controls"):
            if not e.get(f):
                errors.append(f"{eid}: missing field '{f}'")
        if eid in seen:
            errors.append(f"{eid}: duplicate id")
        seen.add(eid)
        if e.get("guardrail") not in catalogue_ids:
            errors.append(f"{eid}: unknown guardrail {e.get('guardrail')}")
        try:
            c = datetime.date.fromisoformat(e["created"])
            x = datetime.date.fromisoformat(e["expires"])
            if (x - c).days > MAX_EXCEPTION_DAYS:
                errors.append(f"{eid}: duration {(x - c).days}d exceeds the {MAX_EXCEPTION_DAYS}d maximum")
            if x < c:
                errors.append(f"{eid}: expires before created")
        except (KeyError, ValueError):
            errors.append(f"{eid}: created/expires must be ISO dates")
    return errors


def check_plan(plan, catalogue, exceptions=None, today=None):
    """Evaluate plan. Returns a list of finding dicts with status violation|waived|expired-waiver."""
    today = today or datetime.date.today()
    waivers = {(e["guardrail"], e["resource"]): e for e in (exceptions or {}).get("exceptions", [])}
    findings = []
    for g in catalogue["guardrails"]:
        for addr, msg in evaluate_rule(g, plan):
            w = waivers.get((g["id"], addr))
            status = "violation"
            note = ""
            if w:
                if datetime.date.fromisoformat(w["expires"]) >= today:
                    status, note = "waived", f"{w['id']} until {w['expires']} ({w['ticket']})"
                else:
                    status, note = "violation", f"{w['id']} expired on {w['expires']}"
            findings.append({"guardrail": g["id"], "severity": g["severity"], "resource": addr, "message": msg,
                             "status": status, "note": note, "remediation": g.get("remediation", "")})
    return findings


def blocking(findings):
    return [f for f in findings if f["status"] == "violation" and f["severity"] == "mandatory"]


def render(findings, fmt="text"):
    if fmt == "json":
        return json.dumps(findings, indent=2)
    if not findings:
        return "All guardrails passed.\n"
    if fmt == "markdown":
        out = ["| Status | Guardrail | Resource | Finding |", "|---|---|---|---|"]
        for f in findings:
            out.append(f"| {f['status']} | {f['guardrail']} ({f['severity']}) | `{f['resource']}` | {f['message']} {f['note']} |")
        return "\n".join(out) + "\n"
    lines = []
    for f in findings:
        mark = {"violation": "FAIL", "waived": "WAIVED"}.get(f["status"], f["status"].upper())
        if f["severity"] == "advisory" and f["status"] == "violation":
            mark = "WARN"
        lines.append(f"[{mark}] {f['guardrail']} {f['resource']}: {f['message']}" + (f"  <{f['note']}>" if f["note"] else ""))
    return "\n".join(lines) + "\n"
