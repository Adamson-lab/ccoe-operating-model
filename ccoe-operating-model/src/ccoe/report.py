"""KPI scorecard and guardrail catalogue rendering."""


def rag(k):
    cur, tgt, better = k["current"], k["target"], k["better"]
    met = cur >= tgt if better == "higher" else cur <= tgt
    if met:
        return "green"
    gap = abs(cur - tgt) / (abs(tgt) if tgt else 1)
    return "amber" if gap <= 0.15 else "red"


def scorecard_markdown(data):
    icon = {"green": "🟢", "amber": "🟠", "red": "🔴"}
    out = ["# CCoE KPI Scorecard", "", f"_As of {data['as_of']}. Generated from `data/kpis.json` by `ccoe scorecard`._", "",
           "| Category | KPI | Current | Target | Status |", "|---|---|--:|--:|:-:|"]
    counts = {"green": 0, "amber": 0, "red": 0}
    for k in data["kpis"]:
        r = rag(k)
        counts[r] += 1
        out.append(f"| {k['category']} | {k['name']} | {k['current']} {k['unit']} | {k['target']} {k['unit']} | {icon[r]} |")
    out += ["", f"**Summary:** {counts['green']} green, {counts['amber']} amber, {counts['red']} red of {len(data['kpis'])} KPIs."]
    return "\n".join(out) + "\n"


def catalog_markdown(cat):
    out = ["# Guardrail Catalogue", "", "_Generated from `data/guardrails.json` by `ccoe catalog`._", "",
           "| ID | Guardrail | Domain | Layer | Severity | Controls | Automated check |", "|---|---|---|---|---|---|:-:|"]
    for g in cat["guardrails"]:
        out.append(f"| {g['id']} | {g['title']} | {g['domain']} | {g['layer']} | {g['severity']} | {', '.join(g['controls'])} | {'yes' if g.get('check') else 'org/runtime'} |")
    return "\n".join(out) + "\n"
