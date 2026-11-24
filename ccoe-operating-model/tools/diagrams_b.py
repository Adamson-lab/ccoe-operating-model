import os, sys
from diagramlib import *
from diagrams_a import ROOT, J
sys.path.insert(0, os.path.join(ROOT, "src"))
from ccoe import adr as adrmod
from ccoe import report


def d08():
    d = Dia(8, "ADR Lifecycle State Machine", "Every architecture decision moves through the same reviewed, linted and auditable path", 1600, 860, "Governance")
    dr = d.pill(40, 300, 190, 64, "Draft", "Author writes in a branch", "gray")
    pr = d.pill(300, 300, 190, 64, "Proposed", "PR open, 3-day comment window", "blue")
    rv = d.box(560, 285, 220, 94, "ARB review", "Weekly, quorum 3 of 5, outcome recorded in the PR", "purple")
    dm = d.diamond(930, 332, 190, 130, "Consensus reached?", "amber")
    ac = d.box(1100, 170, 200, 80, "Accepted", "Immutable; only status may change", "green")
    rj = d.box(1100, 430, 200, 80, "Rejected", "Kept as a record of the path not taken", "red")
    dp = d.box(1360, 150, 210, 80, "Deprecated", "Retired with no replacement", "gray")
    sp = d.box(1360, 260, 210, 80, "Superseded", "Replaced by a newer ADR, cross-linked", "purple")
    d.arrow([(230, 332), (300, 332)], "gray", label="open PR", lp=(265, 332))
    d.arrow([(490, 332), (560, 332)], "blue", label="queue", lp=(525, 332))
    d.arrow([(780, 332), (835, 332)], "purple")
    d.arrow([(930, 267), (930, 210), (1100, 210)], "green", label="consensus", lp=(1015, 210))
    d.arrow([(1025, 332), (1062, 332), (1062, 470), (1100, 470)], "red", label="declined", lp=(1062, 400))
    d.arrow([(930, 397), (930, 560), (135, 560), (135, 364)], "amber", dash=True, label="needs changes: author revises", lp=(530, 560))
    d.conn(ac, dp, "r", "l", kind="gray")
    d.conn(ac, sp, "r", "l", kind="purple")
    d.badge(1100, 170, 1, "green")
    d.group(25, 620, 1550, 190, "Rules enforced by ccoe lint-adr in CI", "teal")
    xs, w = cols(45, 1510, 4, 20)
    for x, (t, s) in zip(xs, [("Mandatory sections", "Context, Decision, Consequences, Alternatives considered"), ("Valid metadata", "Status, ISO date, domain, related and supersedes IDs resolve"), ("Sequential numbering", "No gaps; filename matches heading number"), ("Supersession integrity", "Superseding an ADR requires the old one marked Superseded")]):
        d.box(x, 660, w, 110, t, s, "teal")
    d.legend = [("blue", "Active"), ("green", "Decided"), ("purple", "Review / replaced"), ("red", "Rejected")]
    return d


def d09():
    adrs = {int(a["number"]): a for a in adrmod.load_all(os.path.join(ROOT, "adr"))}
    order = ["governance", "security", "platform", "finops"]
    kinds = {"governance": "blue", "security": "red", "platform": "purple", "finops": "amber"}
    POS = {1: (0, 0), 7: (0, 1), 8: (0, 2), 10: (1, 0), 4: (1, 1), 5: (1, 2), 3: (2, 0), 2: (2, 1), 9: (2, 2), 6: (3, 1)}
    d = Dia(9, "ADR Dependency Graph", "Rendered live from adr/*.md; arrows point from a decision to the earlier decision it builds upon", 1600, 940, "Governance")
    xs, w = cols(45, 1510, 4, 50)
    for i, dom in enumerate(order):
        d.group(xs[i] - 15, 84, w + 30, 548, dom + " decisions", kinds[dom])
    box = {}
    for n, (c, r) in POS.items():
        a = adrs[n]
        if order[c] != a["domain"]:
            d.warn.append(f"ADR {n} domain {a['domain']} != column {order[c]}")
        box[n] = d.box(xs[c], 128 + r * 170, w, 120, f"ADR-{n:04d}", f"{a['title']}\n{a['status']} · {a['date']}", kinds[a["domain"]], 13)
    seen = set()
    for n, a in adrs.items():
        for ref in a["related"]:
            r = int(ref)
            key = tuple(sorted((n, r)))
            if key in seen:
                continue
            seen.add(key)
            hi, lo = max(n, r), min(n, r)
            bh, bl = box[hi], box[lo]
            ch, cl = POS[hi][0], POS[lo][0]
            if ch == cl:
                if bh["y"] < bl["y"]:
                    d.arrow([anchor(bh, "b"), anchor(bl, "t")], "navy")
                else:
                    d.arrow([anchor(bh, "t"), anchor(bl, "b")], "navy")
            elif ch < cl:
                d.curve(anchor(bh, "r"), anchor(bl, "l"), "navy", 1.8)
            else:
                d.curve(anchor(bh, "l"), anchor(bl, "r"), "navy", 1.8)
    st = {}
    dm = {}
    for a in adrs.values():
        st[a["status"]] = st.get(a["status"], 0) + 1
        dm[a["domain"]] = dm.get(a["domain"], 0) + 1
    d.group(25, 670, 1550, 220, "Portfolio view", "gray")
    xs3, w3 = cols(45, 1510, 3, 20)
    d.box(xs3[0], 710, w3, 150, "Status mix", " · ".join(f"{v} {k}" for k, v in sorted(st.items())) + f"\n{len(adrs)} decisions in total", "green")
    d.box(xs3[1], 710, w3, 150, "Domain mix", " · ".join(f"{dm.get(k,0)} {k}" for k in order), "blue")
    d.box(xs3[2], 710, w3, 150, "How to read", "Add a Related: line to an ADR and regenerate; the graph, the index and CI lint all derive from the same files.", "teal")
    d.legend = [("blue", "Governance"), ("red", "Security"), ("purple", "Platform"), ("amber", "FinOps")]
    return d


def d10():
    d = Dia(10, "Cloud Adoption Roadmap & Maturity Gates", "Five waves across five capability lanes; each wave exits through an explicit, measurable gate", 1600, 990, "Operating model")
    xs, w = cols(180, 1395, 5, 15)
    wk = ["navy", "blue", "teal", "purple", "green"]
    for i, (x, t) in enumerate(zip(xs, ["Wave 0 · Foundation", "Wave 1 · Pilot", "Wave 2 · Scale", "Wave 3 · Optimize", "Wave 4 · Innovate"])):
        d.chevron(x, 84, w, 58, t, wk[i], first=(i == 0), fs=12)
    L = [("Governance", "blue", [("Charter & Council", "Sponsor, scope, RACI v1"), ("ARB + ADR registry", "First 10 ADRs accepted"), ("Federated champions", "A champion in every BU"), ("Policy lifecycle", "Quarterly guardrail review"), ("Adaptive governance", "Data-driven standards")]),
         ("Platform", "purple", [("Landing zone MVP", "Org, OUs, logging, SSO"), ("Account vending", "Self-service in under a day"), ("Golden paths", "Catalogue of 8 templates"), ("Multi-region & DR", "Tier-1 reference patterns"), ("Multi-cloud control plane", "AWS, Azure, GCP parity")]),
         ("Security", "red", [("Baseline SCPs", "Preventive org guardrails"), ("Policy-as-code in CI", "check-plan on all repos"), ("Continuous compliance", "Config + Security Hub"), ("Auto-remediation", "Top 10 findings fixed by bots"), ("Zero standing privilege", "Just-in-time access everywhere")]),
         ("FinOps", "amber", [("Tagging standard", "Four mandatory tags"), ("Showback", "Per-account dashboards"), ("Chargeback", "Product-aligned billing"), ("Commitments", "70% coverage target"), ("Unit economics", "Cost per transaction")]),
         ("People", "teal", [("Skills baseline", "Assess and plan"), ("Cloud academy", "Role-based learning paths"), ("Certification drive", "60% of engineers certified"), ("Guilds", "Communities of practice"), ("Innovation labs", "Emerging tech runway")])]
    for r, (lane, k, cells) in enumerate(L):
        y = 160 + r * 124
        d.box(25, y, 140, 108, lane, None, "navy", 13)
        for x, (t, s) in zip(xs, cells):
            d.box(x, y, w, 108, t, s, k)
    d.box(25, 788, 140, 80, "Exit gate", None, "navy", 13)
    for x, (t, s) in zip(xs, [("Gate 0", "Charter signed, funding approved, sponsor named"), ("Gate 1", "10 ADRs accepted; check-plan live on pilot repos"), ("Gate 2", "60% on golden paths; tag compliance ≥ 95%"), ("Gate 3", "Guardrail coverage ≥ 95%; waste under 10%"), ("Gate 4", "Platform NPS ≥ 50; unit costs reported")]):
        d.box(x, 788, w, 80, t, s, "amber")
    d.box(25, 888, 140, 56, "Maturity", None, "navy", 13)
    for x, t in zip(xs, ["L1 · Ad hoc", "L2 · Repeatable", "L3 · Defined", "L4 · Managed", "L5 · Optimising"]):
        d.pill(x, 888, w, 56, t, None, "gray")
    d.legend = [("amber", "Exit gate"), ("gray", "Maturity level")]
    return d


def d11():
    d = Dia(11, "Service Catalogue & Paved-Road Platform", "Product teams self-serve through the portal; every layer below inherits guardrails and day-2 services", 1600, 1000, "Platform")
    gx, gw = 25, 1225
    d.group(gx, 80, gw, 130, "Experience layer", "blue")
    xs, w = cols(45, 1185, 3, 20)
    for x, (t, s) in zip(xs, [("Developer portal", "Backstage-style catalogue, docs and scorecards"), ("CLI & ChatOps", "Request, status and approvals from the terminal or chat"), ("Git templates", "Repository scaffolds with CI and policy wired in")]):
        d.box(x, 114, w, 80, t, s, "blue")
    d.group(gx, 250, gw, 160, "Service catalogue (versioned products)", "teal")
    xs, w = cols(45, 1185, 6, 12)
    for x, (t, s) in zip(xs, [("Web app", "Container + CDN + WAF"), ("Serverless API", "Gateway, functions, auth"), ("Kubernetes namespace", "Quota, mesh, policies"), ("Data lake", "Ingest, catalogue, lineage"), ("Managed database", "Encrypted, backed up"), ("Event streaming", "Topics, schemas, DLQ")]):
        d.box(x, 288, w, 100, t, s, "teal", 11)
    d.group(gx, 450, gw, 140, "Golden-path IaC modules (semver registry)", "purple")
    for x, (t, s) in zip(xs, [("network-spoke", "VPC, subnets, TGW attach"), ("iam-role", "Least-privilege roles"), ("secure-bucket", "Encrypted, no public access"), ("kms-key", "Rotation, grants"), ("observability", "Dashboards, alarms, SLOs"), ("tagging", "default_tags enforced")]):
        d.box(x, 488, w, 80, t, s, "purple", 11)
    d.group(gx, 630, gw, 130, "Guardrails (policy-as-code)", "red")
    xs4, w4 = cols(45, 1185, 4, 16)
    for x, (t, s, k) in zip(xs4, [("Preventive", "SCP / Azure Policy / Org Policy", "red"), ("Proactive", "check-plan in CI", "amber"), ("Detective", "Config / Defender / SCC", "blue"), ("Responsive", "Auto-remediation, SOAR", "green")]):
        d.box(x, 666, w4, 76, t, s, k)
    d.group(gx, 800, gw, 120, "Cloud platforms", "navy")
    for x, t in zip(xs4, ["AWS Organizations", "Azure management groups", "GCP organisation", "Shared services accounts"]):
        d.box(x, 836, w4, 68, t, None, "navy")
    for y0, y1, lab in [(210, 250, "scaffold"), (410, 450, "compose"), (590, 630, "enforced by"), (760, 800, "deploy to")]:
        d.arrow([(640, y0), (640, y1)], "gray", label=lab, lp=(640, (y0 + y1) / 2))
    d.group(1275, 80, 300, 840, "Day-2 platform services", "green")
    for i, (t, s) in enumerate([("Observability", "Golden dashboards"), ("Backup & DR", "Tiered RPO / RTO"), ("Patching", "Image pipeline, SSM"), ("Secrets & certs", "Vault, rotation"), ("Cost & usage", "Showback per product"), ("Support & SLOs", "On-call, runbooks")]):
        d.box(1295, 116 + i * 130, 260, 110, t, s, "green")
    d.arrow([(1250, 500), (1275, 500)], "green", both=True)
    d.legend = [("blue", "Experience"), ("teal", "Catalogue"), ("purple", "Modules"), ("green", "Day-2")]
    return d


def d12():
    d = Dia(12, "FinOps Operating Loop & Cost Allocation Pipeline", "Inform, optimise and operate on a continuous cycle, fed by a normalised and allocated cost data pipeline", 1600, 980, "FinOps")
    d.group(25, 80, 775, 470, "FinOps operating loop", "amber")
    inf = d.box(260, 115, 300, 130, "Inform", "Visibility, allocation, forecasting and benchmarking", "blue", 14)
    opt = d.box(470, 400, 300, 130, "Optimise", "Rightsizing, commitments, waste elimination, architecture", "amber", 14)
    ope = d.box(50, 400, 300, 130, "Operate", "Budgets, governance, anomaly response and culture", "green", 14)
    d.curve((560, 180), (620, 400), "blue", 2.4, c1=(690, 180), c2=(620, 310))
    d.arrow([(470, 465), (350, 465)], "amber", label="decisions", lp=(410, 465))
    d.curve((200, 400), (260, 180), "green", 2.4, c1=(200, 300), c2=(190, 180))
    d.chip(310, 300, "Crawl → Walk → Run", "gray")
    d.group(25, 570, 775, 360, "Commitment strategy waterfall", "teal")
    for i, (t, s) in enumerate([("Rightsize first", "Match size to measured utilisation"), ("Eliminate waste", "Idle, orphaned and over-provisioned resources"), ("Commit on steady state", "Savings Plans / RIs targeting 70% coverage"), ("Use spot for fault-tolerant work", "Batch, CI runners, stateless tiers"), ("Modernise architecture", "Serverless, ARM, managed services")]):
        y = 610 + i * 60
        d.badge(52, y + 25, i + 1, "teal")
        d.box(75, y, 705, 50, f"{t}: {s}", None, "teal", 11)
    d.group(840, 80, 735, 850, "Cost allocation data pipeline", "blue")
    d.cyl(1010, 120, 380, 100, "Provider billing exports", "AWS CUR · Azure Cost Export · GCP billing in BigQuery", "blue", 11)
    nb = d.box(1010, 270, 380, 76, "Normalise to FOCUS schema", "One cost model across clouds", "purple")
    al = d.box(1010, 396, 380, 96, "Allocation engine", "Account-to-product map, tag inheritance, shared-cost split rules", "purple")
    lk = d.cyl(1010, 542, 380, 100, "Cost lake", "13 months, daily grain, per product and environment", "teal", 11)
    d.arrow([(1200, 220), (1200, 270)], "blue", label="export", lp=(1200, 245))
    d.arrow([(1200, 346), (1200, 396)], "purple")
    d.arrow([(1200, 492), (1200, 542)], "purple", label="allocated", lp=(1200, 517))
    xs3, w3 = cols(865, 685, 3, 20)
    outs = []
    for x, (t, s, k) in zip(xs3, [("Showback dashboards", "Per product, weekly", "green"), ("Chargeback to GL", "Monthly journals", "amber"), ("Anomaly alerts", "Slack and ITSM", "red")]):
        outs.append(d.box(x, 700, w3, 100, t, s, k))
    for o in outs:
        d.conn(lk, o, "b", "t", m=672, kind="teal")
    d.box(865, 842, 685, 70, "Budgets: alert at 80%, escalate to CCoE at 100%, throttle sandbox on breach", None, "navy", 11)
    d.arrow([(outs[1]["x"] + w3 / 2, 800), (outs[1]["x"] + w3 / 2, 842)], "navy")
    d.legend = [("blue", "Inform"), ("amber", "Optimise"), ("green", "Operate"), ("purple", "Data processing")]
    return d


def d13():
    cat = J("data/guardrails.json")["guardrails"]
    doms = [("Identity", "purple"), ("Data Protection", "blue"), ("Network", "teal"), ("Logging", "amber"), ("Platform Hardening", "gray"), ("Governance & Org", "red"), ("Cost & Tagging", "green")]
    d = Dia(13, "Control Framework Traceability: Frameworks to Evidence", "Guardrail IDs are read live from data/guardrails.json; each guardrail maps to framework controls and to audit evidence", 1600, 960, "Security")
    d.group(25, 80, 250, 800, "Frameworks", "navy")
    d.group(420, 80, 300, 800, "Control domains", "blue")
    d.group(860, 80, 330, 800, "Guardrails (live)", "red")
    d.group(1330, 80, 245, 800, "Evidence", "teal")
    F = [("NIST 800-53 / CSF", "purple", [0, 1, 2, 3, 4]), ("ISO/IEC 27001", "blue", [0, 1, 3, 5]), ("SOC 2 (TSC)", "teal", [0, 3, 5, 6]), ("CIS Benchmarks", "amber", [0, 2, 3, 4]), ("PCI DSS v4", "red", [1, 2, 3]), ("NDPA 2023 / sector rules", "green", [1, 5])]
    dy = lambda i: 116 + i * 108
    for i, (dom, k) in enumerate(doms):
        ids = [g["id"][2:] for g in cat if g["domain"] == dom]
        lay = sorted({g["layer"] for g in cat if g["domain"] == dom})
        d.box(440, dy(i), 260, 88, dom, f"{len(ids)} guardrails · {', '.join(lay)}", k)
        d.box(880, dy(i), 290, 88, f"{len(ids)} guardrail{'s' if len(ids)!=1 else ''}", ", ".join(ids), k, 11)
        d.arrow([(700, dy(i) + 44), (880, dy(i) + 44)], k)
    for i, (t, k, tgt) in enumerate(F):
        y = 116 + i * 130
        fb = d.box(45, y, 210, 100, t, None, k)
        for j in tgt:
            p1, p2 = (255, y + 50 + (j - 3) * 2), (440, dy(j) + 44 + (i - 2) * 3)
            d.curve(p1, p2, k, 1.4, 0.55, head=False)
            d.add(f'<circle cx="{p2[0]}" cy="{p2[1]:.1f}" r="3.2" fill="{PAL[k][1]}"/>')
    E = [("Plan check log", "CI artifact per pull request"), ("Posture findings", "Config, Security Hub, Defender"), ("Exception approvals", "Registry with approver and expiry"), ("Attestation pack", "Quarterly sign-off for auditors")]
    ey = lambda i: 116 + i * 190
    for i, (t, s) in enumerate(E):
        d.box(1350, ey(i), 205, 130, t, s, "teal")
    M = {0: [1], 1: [0, 1], 2: [0, 1], 3: [1], 4: [0], 5: [2, 3], 6: [0, 3]}
    for i, tg in M.items():
        for j in tg:
            d.curve((1170, dy(i) + 44), (1350, ey(j) + 65), doms[i][1], 1.4, 0.7)
    d.legend = [("navy", "Framework"), ("blue", "Domain"), ("red", "Guardrail"), ("teal", "Evidence")]
    return d


def d14():
    d = Dia(14, "Exception & Waiver Workflow", "Deviation is requested in Git, decided by the Exception Board, time-boxed to 180 days and enforced by CI", 1600, 950, "Governance")
    L = [("Requester (BU)", "Product team", "green"), ("CCoE triage", "Platform engineering", "blue"), ("Security & Risk", "Risk assessor", "red"), ("Exception Board", "Weekly forum", "purple"), ("Automation", "CI and scheduler", "teal")]
    for i, (t, s, k) in enumerate(L):
        y = 84 + i * 164
        d.add(f'<rect x="185" y="{y}" width="1390" height="156" rx="12" fill="#FFFFFF" fill-opacity="0.75" stroke="{PAL[k][1]}" stroke-opacity="0.45"/>')
        d.box(25, y, 150, 156, t, s, k, 13)
    X = lambda k: 205 + k * 235
    Y = lambda l: 84 + l * 164 + 34
    bw, bh = 185, 88
    b1 = d.box(X(0), Y(0), bw, bh, "Raise exception PR", "Edit data/exceptions.json with justification and expiry", "green")
    b2 = d.box(X(1), Y(1), bw, bh, "Triage (2 days)", "Completeness, duplicates, alternatives explored", "blue")
    b3 = d.box(X(2), Y(2), bw, bh, "Risk assessment", "3 days · impact, likelihood, compensating controls", "red")
    dm = d.diamond(X(3) + 92, 84 + 3 * 164 + 78, 170, 120, "Board decision", "purple")
    ap = d.box(X(4), Y(3), bw, bh, "Approve", "Expiry ≤ 180 days; compensating controls recorded", "purple")
    rj = d.box(X(4), Y(0), bw, bh, "Rejected", "Remediate, redesign or appeal to Cloud Council", "gray")
    mg = d.box(X(4), Y(4), bw, bh, "Merge & register", "CI honours the waiver in check-plan from next run", "teal")
    ex = d.box(X(5), Y(4), bw, bh, "Expiry watch", "T-30 reminder; waiver stops applying at expiry", "teal")
    rn = d.box(X(5), Y(0), bw, bh, "Renew or remediate", "New PR required; no silent extension", "green")
    for n, b, k in [(1, b1, "green"), (2, b2, "blue"), (3, b3, "red"), (4, dm, "purple"), (5, ap, "purple"), (6, mg, "teal"), (7, ex, "teal")]:
        d.badge(b["x"] + 4, b["y"] + 2, n, k)
    d.conn(b1, b2, "r", "t", kind="green")
    d.conn(b2, b3, "r", "t", kind="blue")
    d.conn(b3, dm, "r", "l", kind="red")
    d.arrow([(X(3) + 177, 84 + 3 * 164 + 78), (X(4), 84 + 3 * 164 + 78)], "green", label="yes", lp=(X(3) + 213, 84 + 3 * 164 + 78))
    d.arrow([(X(3) + 92, 84 + 3 * 164 + 18), (X(3) + 92, Y(0) + 44), (X(4), Y(0) + 44)], "red", label="no", lp=(X(3) + 92, 400))
    d.conn(ap, mg, "b", "t", kind="teal")
    d.conn(mg, ex, "r", "l", kind="teal")
    d.arrow([(X(5) + bw / 2, Y(4)), (X(5) + bw / 2, Y(0) + bh)], "green", dash=True, label="renew or remediate", lp=(X(5) + bw / 2, 400))
    d.legend = [("green", "Requester"), ("red", "Risk"), ("purple", "Board"), ("teal", "Automation")]
    return d


ALL = [d08, d09, d10, d11, d12, d13, d14]
