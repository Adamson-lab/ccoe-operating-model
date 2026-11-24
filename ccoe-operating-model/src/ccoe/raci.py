"""RACI matrix loading, validation and rendering."""
import json

VALID = {"R", "A", "AR", "C", "I"}


def load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def validate(data):
    """Return a list of error strings. Rules: exactly one Accountable per
    activity, at least one Responsible, known roles, valid letters, unique ids."""
    errors, seen = [], set()
    roles = {r["id"] for r in data["roles"]}
    for a in data["activities"]:
        aid = a["id"]
        if aid in seen:
            errors.append(f"{aid}: duplicate activity id")
        seen.add(aid)
        m = a["raci"]
        for role, letter in m.items():
            if role not in roles:
                errors.append(f"{aid}: unknown role '{role}'")
            if letter not in VALID:
                errors.append(f"{aid}: invalid letter '{letter}' for {role}")
        accountable = [r for r, v in m.items() if v in ("A", "AR")]
        if len(accountable) != 1:
            errors.append(f"{aid} ({a['name']}): needs exactly one Accountable, found {len(accountable)}")
        if not any(v in ("R", "AR") for v in m.values()):
            errors.append(f"{aid} ({a['name']}): needs at least one Responsible")
    return errors


def load_stats(data):
    """Accountable / Responsible counts per role."""
    stats = {r["id"]: {"A": 0, "R": 0} for r in data["roles"]}
    for a in data["activities"]:
        for role, v in a["raci"].items():
            if v in ("A", "AR"):
                stats[role]["A"] += 1
            if v in ("R", "AR"):
                stats[role]["R"] += 1
    return stats


def to_markdown(data):
    roles = data["roles"]
    out = ["# RACI Matrix", "", "_Generated from `data/raci.json` by `ccoe raci-md`. Do not edit by hand._", ""]
    out.append("| Group | Activity | " + " | ".join(r["short"] for r in roles) + " |")
    out.append("|---|---|" + "|".join([":-:"] * len(roles)) + "|")
    for a in data["activities"]:
        cells = [{"AR": "**A/R**", "A": "**A**"}.get(a["raci"].get(r["id"], ""), a["raci"].get(r["id"], "")) for r in roles]
        out.append(f"| {a['group']} | {a['id']} {a['name']} | " + " | ".join(cells) + " |")
    out += ["", "**Legend:** " + "; ".join(f"{k} = {v}" for k, v in data["legend"].items()), "", "## Load per role", "",
            "| Role | Accountable | Responsible |", "|---|:-:|:-:|"]
    for r in roles:
        s = load_stats(data)[r["id"]]
        out.append(f"| {r['name']} | {s['A']} | {s['R']} |")
    return "\n".join(out) + "\n"
