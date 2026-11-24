import json, os
from diagramlib import *

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
def J(p):
    with open(os.path.join(ROOT, p), encoding="utf-8") as f:
        return json.load(f)


def d01():
    d = Dia(1, "CCoE Operating Model on a Page", "Strategic intent flows down through five capability pillars to product teams; demand and feedback flow back up", 1600, 1060, "Operating model")
    d.group(25, 80, 1550, 160, "Business & enterprise context", "navy")
    xs, w = cols(45, 1510, 4, 20)
    for x, (t, s) in zip(xs, [("Business strategy & outcomes", "Growth, resilience and speed-to-market targets"), ("Enterprise architecture principles", "Cloud-first, secure-by-default, buy before build"), ("Risk appetite & regulation", "Data residency, sector regulators, internal policy"), ("Funding & chargeback model", "Product-aligned budgets, showback to chargeback")]):
        d.box(x, 114, w, 104, t, s, "navy")
    d.arrow([(800, 242), (800, 308)], "navy", label="policy intent · funding · priorities")
    d.group(25, 310, 1550, 450, "CCoE capability pillars", "blue")
    xs, w = cols(45, 1510, 5, 18)
    P = [("Govern", "blue", ["Cloud Council & charter", "Architecture Review Board", "ADR registry", "Exception & waiver board"]),
         ("Enable", "teal", ["Training & certification", "Cloud champions network", "Reference architectures", "Office hours & community"]),
         ("Platform", "purple", ["Landing zone factory", "Golden-path IaC modules", "Service catalog", "Shared network & identity"]),
         ("Secure & comply", "red", ["Guardrails as code", "Control mapping to frameworks", "Continuous compliance", "Threat & incident response"]),
         ("Optimize", "amber", ["Cost allocation & showback", "Rightsizing & commitments", "Unit economics", "Sustainability (GreenOps)"])]
    for x, (h, k, caps) in zip(xs, P):
        d.box(x, 346, w, 56, h, None, "navy", 14)
        for i, c in enumerate(caps):
            d.box(x, 416 + i * 82, w, 70, c, None, k)
    d.group(25, 830, 1550, 120, "Consumers of the platform", "green")
    xs, w = cols(45, 1510, 4, 20)
    for x, t in zip(xs, ["Product teams (spokes)", "Data & AI platforms", "Migration factories", "Regulated & third-party workloads"]):
        d.box(x, 864, w, 64, t, None, "green")
    d.arrow([(560, 828), (560, 762)], "teal", label="paved roads · guardrails · training", lp=(560, 795))
    d.arrow([(1040, 762), (1040, 828)], "amber", dash=True, label="demand · incidents · feedback", lp=(1040, 795))
    d.box(25, 968, 1550, 52, "Foundation: AWS · Azure · GCP  |  Shared services: identity · network · observability · security tooling", None, "gray")
    d.legend = [("navy", "Context"), ("blue", "Pillar capability"), ("green", "Consumer")]
    return d


def d02():
    d = Dia(2, "CCoE Organisation: Federated Hub-and-Spoke", "A small central core owns the platform and standards; BU champions own adoption and feed demand back", 1600, 920, "Operating model")
    d.group(25, 80, 1550, 130, "Executive sponsorship", "navy")
    xs, w = cols(45, 1510, 3, 20)
    for x, (t, s) in zip(xs, [("Executive sponsor (CIO / CTO)", "Chairs Cloud Council, owns funding"), ("CISO", "Owns cyber risk appetite and guardrail mandate"), ("CFO / Finance partner", "Co-owns FinOps and chargeback model")]):
        d.box(x, 112, w, 80, t, s, "navy")
    d.arrow([(800, 210), (800, 262)], "navy", label="mandate · funding", lp=(800, 236))
    d.group(340, 262, 920, 300, "CCoE core team (hub)", "blue", False)
    xs, w = cols(360, 880, 3, 20)
    R = [("Head of CCoE", "Product owner of the cloud platform"), ("Chief cloud architect", "Chairs ARB, owns reference architectures"), ("Platform engineering lead", "Landing zone, modules, catalog"), ("Cloud security lead", "Guardrails, exceptions, compliance"), ("FinOps lead", "Allocation, commitments, unit cost"), ("Enablement & community lead", "Academy, champions, office hours")]
    for i, (t, s) in enumerate(R):
        d.box(xs[i % 3], 300 + (i // 3) * 124, w, 104, t, s, ["blue", "purple", "teal", "red", "amber", "green"][i])
    d.group(25, 262, 290, 300, "External ecosystem", "gray")
    for i, t in enumerate(["Cloud providers (TAMs, specialists)", "Systems integrators & MSPs", "Standards bodies & communities"]):
        d.box(45, 298 + i * 86, 250, 70, t, None, "gray")
    d.group(1285, 262, 290, 300, "Assurance & oversight", "amber")
    for i, t in enumerate(["Internal audit", "Risk & compliance", "Regulators & external auditors"]):
        d.box(1305, 298 + i * 86, 250, 70, t, None, "amber")
    d.arrow([(315, 412), (340, 412)], "gray", both=True)
    d.arrow([(1260, 412), (1285, 412)], "amber", dash=True, both=True)
    d.group(25, 640, 1550, 230, "Federated spokes: business-unit cloud champions", "green")
    xs, w = cols(45, 1510, 5, 18)
    for x, (t, s) in zip(xs, [("BU: Retail", "Cloud champion + 12 product squads"), ("BU: Banking", "Cloud champion + 9 product squads"), ("BU: Operations", "Cloud champion + 7 product squads"), ("BU: Data & AI", "Cloud champion + 6 product squads"), ("BU: Digital", "Cloud champion + 14 product squads")]):
        d.box(x, 680, w, 160, t, s, "green")
    d.arrow([(560, 562), (560, 640)], "teal", label="paved roads · guardrails · training", lp=(560, 600))
    d.arrow([(1040, 640), (1040, 562)], "amber", dash=True, label="backlog · feedback · demand", lp=(1040, 600))
    d.legend = [("blue", "CCoE core"), ("green", "Spokes"), ("amber", "Oversight (dashed)")]
    return d


def d03():
    d = Dia(3, "Governance Forums & Decision Cadence", "Three tiers of forums with explicit escalation paths; every decision lands as an artifact in this repository", 1600, 930, "Governance")
    d.group(25, 80, 1100, 200, "Tier 1 · Strategic", "navy")
    xs, w = cols(45, 1060, 2, 20)
    for x, (t, s) in zip(xs, [("Cloud Council", "Quarterly · Chair: CIO · Sets strategy, funding and risk appetite; approves charter changes"), ("Risk & Investment Committee", "Quarterly · Chair: CFO + CISO · Reviews exposure, spend trajectory and major commitments")]):
        d.box(x, 116, w, 140, t, s, "navy")
    d.group(25, 330, 1100, 290, "Tier 2 · Tactical", "blue")
    xs, w = cols(45, 1060, 4, 16)
    T = [("Architecture Review Board", "Weekly · Chair: chief cloud architect · Decides ADRs, standards, reference architectures", "blue"), ("Exception Board", "Weekly · Chair: cloud security lead · Approves time-boxed waivers with compensating controls", "red"), ("FinOps Board", "Monthly · Chair: FinOps lead · Budgets, commitments, anomalies, chargeback", "amber"), ("Security Guild", "Fortnightly · Chair: security lead · Threat review, guardrail backlog, incident learnings", "purple")]
    for x, (t, s, k) in zip(xs, T):
        d.box(x, 366, w, 220, t, s, k)
    d.group(25, 670, 1100, 200, "Tier 3 · Operational", "teal")
    xs, w = cols(45, 1060, 3, 20)
    for x, (t, s) in zip(xs, [("Platform daily stand-up", "Daily · Platform backlog, incidents, vending queue"), ("Cloud champions sync", "Fortnightly · BU demand, adoption blockers, roadmap input"), ("Incident & problem review", "Weekly · Post-incident reviews feed guardrail backlog")]):
        d.box(x, 706, w, 130, t, s, "teal")
    d.arrow([(300, 330), (300, 280)], "amber", dash=True, label="escalations · funding asks", lp=(300, 305))
    d.arrow([(800, 280), (800, 330)], "navy", label="mandates · priorities", lp=(800, 305))
    d.arrow([(300, 670), (300, 620)], "amber", dash=True, label="findings · proposals", lp=(300, 645))
    d.arrow([(800, 620), (800, 670)], "blue", label="standards · backlog", lp=(800, 645))
    d.group(1160, 80, 415, 790, "Decision artifacts (this repo)", "green")
    A = [("ADR registry", "adr/ · numbered, linted, immutable once accepted"), ("RACI matrix", "data/raci.json · one Accountable per activity"), ("Guardrail catalogue", "data/guardrails.json · versioned policy"), ("Exception registry", "data/exceptions.json · 180-day maximum"), ("KPI definitions", "data/kpis.json · scorecard inputs"), ("Charter & policies", "docs/ · operating model documents")]
    for i, (t, s) in enumerate(A):
        d.box(1180, 116 + i * 124, 375, 100, t, s, "green")
    for y in (180, 475, 770):
        d.arrow([(1125, y), (1160, y)], "green")
    d.legend = [("navy", "Strategic"), ("blue", "Tactical"), ("teal", "Operational"), ("green", "Artifact")]
    return d


def d04():
    data = J("data/raci.json")
    roles, acts = data["roles"], data["activities"]
    labw, cw, rh, gh = 430, 120, 36, 26
    groups = []
    for a in acts:
        if a["group"] not in groups:
            groups.append(a["group"])
    H = 150 + len(acts) * rh + len(groups) * gh + 200
    W = 25 + labw + cw * len(roles) + 25
    d = Dia(4, "RACI Heatmap: Who Decides, Who Delivers", "Rendered live from data/raci.json · exactly one Accountable per activity is enforced by ccoe validate", W, H, "Governance")
    x0 = 25 + labw
    for i, r in enumerate(roles):
        d.box(x0 + i * cw + 3, 80, cw - 6, 56, r["short"], None, "navy", 11)
    C = {"A": "navy", "AR": "navy", "R": "teal", "C": "amber", "I": "gray"}
    y = 148
    cur = None
    for a in acts:
        if a["group"] != cur:
            cur = a["group"]
            d.text(30, y + 17, cur.upper(), 11, True, "#2563EB", ls="1")
            d.add(f'<line x1="{30+tw(cur.upper(),11,True)+14:.0f}" y1="{y+13}" x2="{W-25}" y2="{y+13}" stroke="#CBD5E1"/>')
            y += gh
        if acts.index(a) % 2 == 0:
            d.add(f'<rect x="25" y="{y}" width="{W-50}" height="{rh}" fill="#FFFFFF" fill-opacity="0.7"/>')
        d.text(34, y + 23, f"{a['id']}  {a['name']}", 12, False, "#0F172A")
        if tw(f"{a['id']}  {a['name']}", 12) > labw - 20:
            d.warn.append("raci label overflow " + a["name"])
        for i, r in enumerate(roles):
            v = a["raci"].get(r["id"])
            if v:
                f, st, tx = PAL[C[v]]
                fill, tc = (st, "#FFFFFF") if v in ("A", "AR", "R") else (f, tx)
                d.add(f'<rect x="{x0+i*cw+16}" y="{y+4}" width="{cw-32}" height="{rh-8}" rx="7" fill="{fill}" stroke="{st}" stroke-width="1.3"/>')
                d.text(x0 + i * cw + cw / 2, y + 23, "A/R" if v == "AR" else v, 12, True, tc, "middle")
        y += rh
    y += 14
    stats = {r["id"]: {"A": 0, "R": 0} for r in roles}
    for a in acts:
        for rid, v in a["raci"].items():
            stats[rid]["A"] += v in ("A", "AR")
            stats[rid]["R"] += v in ("R", "AR")
    d.group(25, y, W - 50, 112, "Load analysis (activities per role)", "blue")
    d.text(40, y + 62, "Accountable", 12, True, "#0B1F3A")
    d.text(40, y + 90, "Responsible", 12, True, "#0B1F3A")
    for i, r in enumerate(roles):
        cx = x0 + i * cw + cw / 2
        d.text(cx, y + 62, str(stats[r["id"]]["A"]), 14, True, "#0B1F3A", "middle")
        d.text(cx, y + 90, str(stats[r["id"]]["R"]), 14, True, "#0D9488", "middle")
    y += 128
    lx = 40
    for k, lab in [("AR", "A/R Accountable & Responsible"), ("A", "A Accountable"), ("R", "R Responsible"), ("C", "C Consulted"), ("I", "I Informed")]:
        f, st, tx = PAL[C[k]]
        d.add(f'<rect x="{lx}" y="{y}" width="26" height="20" rx="6" fill="{st if k in ("A","AR","R") else f}" stroke="{st}"/>')
        d.text(lx + 36, y + 15, lab, 12, False, "#334155")
        lx += 56 + tw(lab, 12)
    return d


def d05():
    d = Dia(5, "Multi-Account Landing Zone: Organisation & OU Design", "Account boundaries are the primary blast-radius control; SCPs attached at OU level are the preventive baseline", 1600, 1000, "Platform")
    d.box(600, 84, 400, 70, "Management account (organisation root)", "Billing, SCP authoring, no workloads, 2 break-glass admins", "navy")
    xs, w = cols(25, 1550, 7, 14)
    OU = [("Security OU", "red", [("Log archive", "Immutable CloudTrail/Config logs"), ("Security tooling", "GuardDuty, Security Hub admin"), ("Break-glass", "Sealed emergency access")]),
          ("Infrastructure OU", "purple", [("Network hub", "TGW, inspection, DNS"), ("Shared services", "CI/CD runners, registry"), ("Identity", "IdP federation, SSO")]),
          ("Policy staging OU", "amber", [("Policy canary", "Test SCPs before rollout")]),
          ("Sandbox OU", "teal", [("Sandbox accounts", "Per-engineer, budget cap, auto-clean")]),
          ("Workloads: non-prod", "blue", [("Dev accounts", "One per app and team"), ("Test / QA accounts", "Pre-production parity")]),
          ("Workloads: prod", "green", [("Prod accounts", "One per application"), ("Regulated prod", "PCI / personal data")]),
          ("Suspended OU", "gray", [("Quarantine", "Deny-all SCP, decommission queue")])]
    hdr = []
    for x, (t, k, accts) in zip(xs, OU):
        hb = d.box(x, 200, w, 58, t, None, k, 12)
        hdr.append(hb)
        for i, (n, s) in enumerate(accts):
            d.box(x, 276 + i * 94, w, 82, n, s, k, 11)
    mg = B(600, 84, 400, 70)
    for hb in hdr:
        d.conn(mg, hb, "b", "t", m=178, kind="navy", w=1.6)
    d.group(25, 610, 1550, 220, "Preventive baseline: service control policies attached per OU (policies/aws-scp)", "red")
    S = ["Deny delete of log buckets, KMS keys and trails", "Deny leaving org, deny root user, protect tooling", "Staged: new SCP versions soak here for 7 days", "Deny costly services; deny non-approved regions", "Deny public S3, IMDSv1, unencrypted volumes", "Same as non-prod + deny console write access", "Deny all actions except account closure"]
    for x, s, (t, k, _) in zip(xs, S, OU):
        d.box(x, 650, w, 150, "SCP set", s, "red", 11)
    d.box(25, 856, 1550, 70, "Inherited by every account: deny leave-org · deny root user · protect CloudTrail, Config, GuardDuty · region allow-list (G-ORG-001/002/003, G-REG-001)", None, "navy")
    d.arrow([(800, 856), (800, 830)], "navy", label="inherited", lp=(900, 843))
    d.legend = [("navy", "Org root / baseline"), ("red", "Preventive control")]
    return d


def d06():
    d = Dia(6, "Guardrail Defence in Depth Across the Delivery Lifecycle", "Four guardrail layers act on six lifecycle stages; every incident feeds a new guardrail or ADR", 1600, 980, "Security")
    xs, w = cols(205, 1370, 6, 0)
    st = ["Design", "Code", "Build / CI", "Deploy", "Run", "Respond"]
    kk = ["blue", "teal", "purple", "amber", "red", "green"]
    for i, (x, t) in enumerate(zip(xs, st)):
        d.chevron(x, 84, w, 54, t, kk[i], first=(i == 0), fs=13)
    rows = [("Preventive", "Block it at the API", "red"), ("Proactive", "Stop it before merge", "amber"), ("Detective", "Find it fast", "blue"), ("Responsive", "Fix it automatically", "green")]
    for r, (t, s, k) in enumerate(rows):
        y = 158 + r * 150
        d.box(25, y, 170, 130, t, s, "navy", 14)
        d.add(f'<rect x="205" y="{y}" width="1370" height="130" rx="10" fill="{PAL[k][1]}" fill-opacity="0.06" stroke="{PAL[k][1]}" stroke-opacity="0.35" stroke-dasharray="5 4"/>')
    def cell(row, c0, c1, t, s, k):
        y = 158 + row * 150
        d.box(xs[c0] + 8, y + 12, xs[c1] + w - xs[c0] - 16, 106, t, s, k)
    cell(0, 0, 0, "Approved patterns", "Reference architectures and accepted ADRs", "red")
    cell(0, 3, 4, "SCP · Azure Policy deny · GCP Org Policy", "API-level hard stop applied to every account, subscription and project", "red")
    cell(1, 1, 1, "Pre-commit & IDE", "tflint, secrets scan, fmt", "amber")
    cell(1, 2, 2, "ccoe check-plan", "Plan JSON vs 16 guardrails; PR blocked on mandatory failure", "amber")
    cell(1, 3, 3, "Deployment gates", "CloudFormation Hooks, Azure deployment stacks", "amber")
    cell(2, 3, 3, "Drift scan", "Scheduled refresh-only plan", "blue")
    cell(2, 4, 4, "Config · Security Hub · Defender · SCC", "Continuous posture evaluation", "blue")
    cell(2, 5, 5, "Findings pipeline", "SIEM correlation, ticket with owner tag", "blue")
    cell(3, 4, 4, "Auto-remediation", "SSM, Lambda, Azure Automation", "green")
    cell(3, 5, 5, "SOAR playbooks", "Quarantine, account suspension", "green")
    d.arrow([(xs[5] + w / 2, 738), (xs[5] + w / 2, 764), (xs[0] + w / 2, 764), (xs[0] + w / 2, 738)], "navy", dash=True, label="feedback loop: every incident yields a guardrail or an ADR", lp=(800, 764))
    d.group(25, 800, 1550, 130, "Severity model applied to every guardrail", "gray")
    xs3, w3 = cols(45, 1510, 3, 20)
    for x, (t, s, k) in zip(xs3, [("Mandatory", "Blocks merge or deploy; waivable only via Exception Board", "red"), ("Advisory", "Warns in PR, tracked on scorecard, never blocks", "amber"), ("Informational", "Logged for trend analysis and future promotion", "blue")]):
        d.box(x, 836, w3, 80, t, s, k)
    d.legend = [("red", "Preventive"), ("amber", "Proactive"), ("blue", "Detective"), ("green", "Responsive")]
    return d


def d07():
    d = Dia(7, "Policy-as-Code Delivery Pipeline", "Every infrastructure change is evaluated against the guardrail catalogue before apply, and evidence is retained", 1600, 960, "Security")
    xs, w = cols(40, 1520, 5, 80)
    r1 = []
    items = [("Engineer", "Platform or product team", "gray"), ("Pull request", "CODEOWNERS routes review", "blue"), ("Static checks", "fmt, validate, tflint, secrets scan", "blue"), ("terraform plan", "plan -out, show -json", "purple"), ("plan.json artifact", "Immutable CI artifact", "purple")]
    for i, (x, (t, s, k)) in enumerate(zip(xs, items)):
        r1.append(d.pill(x, 110, w, 90, t, s, k) if i == 0 else d.box(x, 110, w, 90, t, s, k))
        d.badge(x + 2, 110, i + 1)
    for a, b in zip(r1, r1[1:]):
        d.conn(a, b, "r", "l")
    eng = d.box(1320, 330, 240, 120, "ccoe check-plan", "Evaluates all guardrails, applies waivers, checks region allow-list", "red")
    d.badge(1322, 330, 6, "red")
    dia = d.diamond(1100, 390, 240, 130, "Mandatory violations?", "amber")
    appr = d.box(660, 335, 240, 110, "Approval gate", "CODEOWNERS + environment protection", "blue")
    app = d.box(340, 335, 240, 110, "terraform apply", "OIDC short-lived role, no static keys", "green")
    scan = d.box(40, 335, 240, 110, "Post-deploy scan", "Config, Security Hub, drift detection", "teal")
    for n, bx in zip((8, 9, 10), (appr, app, scan)):
        d.badge(bx["x"] + 2, 335, n, "navy")
    d.arrow([(1440, 200), (1440, 330)], "purple")
    d.arrow([(1320, 390), (1220, 390)], "red")
    d.badge(1100, 325, 7, "amber")
    d.arrow([(980, 390), (900, 390)], "green", label="no", lp=(940, 390))
    d.arrow([(660, 390), (580, 390)], "green")
    d.arrow([(340, 390), (280, 390)], "green")
    d.arrow([(1100, 325), (1100, 262), (480, 262), (480, 200)], "red", dash=True, label="yes: PR check fails, fix or request exception", lp=(790, 262))
    d.group(900, 500, 660, 190, "Policy inputs (versioned in this repo)", "red")
    for x, (t, s) in zip((920, 1135, 1350), [("Guardrail catalogue", "data/guardrails.json"), ("Exceptions registry", "data/exceptions.json"), ("Rego mirror", "policies/rego")]):
        d.cyl(x, 540, 190, 130, t, s, "red", 11)
    d.arrow([(1440, 500), (1440, 450)], "red", label="load policy + waivers", lp=(1440, 475))
    d.group(25, 500, 840, 190, "Assurance & evidence", "teal")
    d.cyl(45, 540, 240, 130, "Evidence store", "S3 Object Lock, 7-year retention", "teal", 11)
    d.box(330, 545, 250, 120, "Drift detector", "Scheduled refresh-only plans raise tickets", "teal")
    d.box(610, 545, 235, 120, "Auditor view", "Scorecard and attestation pack", "teal")
    d.arrow([(160, 445), (160, 540)], "teal", label="evidence", lp=(160, 492))
    d.box(25, 740, 1550, 100, "Continuous improvement loop", "Violations and drift → guardrail backlog → Security Guild review → semver policy release → all pipelines pick up the new catalogue on next run", "navy")
    d.arrow([(1130, 740), (1130, 690)], "navy", label="policy release", lp=(1130, 715))
    d.legend = [("red", "Policy decision point"), ("green", "Deploy path"), ("teal", "Assurance")]
    return d


ALL = [d01, d02, d03, d04, d05, d06, d07]
