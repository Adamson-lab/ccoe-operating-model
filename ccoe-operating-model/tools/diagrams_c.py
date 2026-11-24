import os, sys
from diagramlib import *
from diagrams_a import ROOT, J
sys.path.insert(0, os.path.join(ROOT, "src"))
from ccoe import adr as adrmod
from ccoe import report


def d15():
    d = Dia(15, "Account Vending Sequence", "From request to a fully baselined, tagged and inventoried account in under four hours, with no tickets", 1600, 1000, "Platform")
    P = ["Requester", "Dev portal", "Git repo", "CI/CD", "Account factory", "AWS Organizations", "Baseline stacks", "Inventory / CMDB", "Slack / ITSM"]
    cx = [100 + 175 * i for i in range(9)]
    M = [(0, 1, "1 · request account", 0), (1, 2, "2 · open PR (tfvars)", 0), (2, 3, "3 · trigger pipeline", 0), (3, 3, "4 · check-plan + validate", 0),
         (3, 4, "5 · invoke vending API", 0), (4, 5, "6 · CreateAccount in OU", 0), (5, 4, "7 · account id", 1), (4, 6, "8 · apply baseline", 0),
         (6, 6, "9 · SCPs, logging, SSO, VPC", 0), (6, 7, "10 · register + tag", 0), (4, 3, "11 · status: ready", 1), (3, 2, "12 · report status", 1),
         (2, 8, "13 · notify requester and owner", 0), (8, 0, "14 · account ready in under 4h", 1)]
    y0, st = 190, 50
    ys = [y0 + i * st for i in range(len(M))]
    bands = [(0, 2, "Request", "blue"), (3, 3, "Validate", "amber"), (4, 8, "Provision", "purple"), (9, 9, "Register", "teal"), (10, 13, "Notify", "green")]
    for a, b, t, k in bands:
        ya, yb = ys[a] - 28, ys[b] + (34 if M[b][0] == M[b][1] else 22)
        d.add(f'<rect x="25" y="{ya}" width="1550" height="{yb-ya}" rx="10" fill="{PAL[k][1]}" fill-opacity="0.07" stroke="{PAL[k][1]}" stroke-opacity="0.3" stroke-dasharray="4 4"/>')
        d.text(1562, ya + 15, t.upper(), 10, True, PAL[k][1], "end", ls="1")
    for x, n in zip(cx, P):
        d.box(x - 75, 84, 150, 54, n, None, "navy", 12)
        d.add(f'<line x1="{x}" y1="138" x2="{x}" y2="{d.h-42}" stroke="#94A3B8" stroke-width="1.2" stroke-dasharray="5 5"/>')
    for (a, b, lab, dash), y in zip(M, ys):
        k = "gray" if dash else "blue"
        if a == b:
            d.arrow([(cx[a], y), (cx[a] + 34, y), (cx[a] + 34, y + 22), (cx[a], y + 22)], "amber")
            d.text(cx[a] + 44, y + 15, lab, 11, True, "#3D2300", halo=True)
        else:
            if tw(lab, 11) > abs(cx[a] - cx[b]) - 16:
                d.warn.append(f"[15] message label too long: {lab}")
            d.arrow([(cx[a], y), (cx[b], y)], k, dash=bool(dash))
            d.text((cx[a] + cx[b]) / 2, y - 7, lab, 11, True, "#0F172A", "middle", halo=True)
    d.legend = [("blue", "Call"), ("gray", "Return (dashed)"), ("amber", "Internal step")]
    return d


def d16():
    d = Dia(16, "Identity & Access Architecture", "One workforce identity source, federated into every cloud, with just-in-time elevation and no long-lived keys", 1600, 930, "Security")
    G = [(25, 290, "Identity sources", "navy", "navy", [("HR system", "Joiner-mover-leaver is the source of truth"), ("Partner directory", "B2B guests, sponsor required, auto-expiry"), ("Service account registry", "Mandatory owner and rotation policy"), ("Customer identities", "Separate CIAM trust zone, never federated to cloud")]),
         (375, 310, "Workforce IdP", "blue", "blue", [("Workforce IdP", "SSO, MFA, conditional access"), ("Group & role sync", "SCIM provisioning from HR attributes"), ("PAM / JIT broker", "Time-boxed elevation with approval"), ("Access reviews", "Quarterly recertification by managers")]),
         (745, 380, "Cloud access federation", "purple", "purple", [("AWS IAM Identity Center", "Permission sets: ReadOnly, Developer, PlatformAdmin, SecurityAudit"), ("Azure Entra ID + PIM", "Eligible RBAC assignments with activation logs"), ("GCP Cloud Identity + IAM", "IAM conditions, workforce identity federation"), ("Session logging", "Every role assumption lands in the Log Archive")]),
         (1185, 390, "Target accounts", "green", "green", [("Production accounts", "Read-only by default; elevation via JIT"), ("Non-production accounts", "Developer access by group"), ("Security & log archive", "Audit role only; no human write access"), ("Break-glass", "Offline credentials, sealed, tested twice a year")])]
    for x, w, lab, gk, bk, boxes in G:
        d.group(x, 80, w, 500, lab, gk)
        for j, (t, s) in enumerate(boxes):
            d.box(x + 20, 120 + j * 116, w - 40, 96, t, s, bk, 12)
    for x0, x1, lab in [(315, 375, "sync"), (685, 745, "SSO"), (1125, 1185, "STS")]:
        d.arrow([(x0, 330), (x1, 330)], "navy", label=lab, lp=((x0 + x1) / 2, 330))
    d.group(25, 620, 1550, 250, "Workload identity: no long-lived keys", "teal")
    xs, w = cols(45, 1510, 5, 16)
    for x, (t, s) in zip(xs, [("GitHub Actions OIDC", "Short-lived role per repository and branch"), ("Kubernetes workloads", "IRSA / workload identity per service account"), ("Dynamic secrets", "Vault or Secrets Manager with lease and rotation"), ("KMS grants", "Key policies scoped per workload role"), ("Machine identity CA", "Private CA issuing short-lived certificates")]):
        d.box(x, 664, w, 170, t, s, "teal")
    d.arrow([(1380, 620), (1380, 580)], "teal", label="OIDC federation", lp=(1380, 600))
    d.legend = [("navy", "Source"), ("blue", "IdP"), ("purple", "Federation"), ("green", "Targets")]
    return d


def d17():
    d = Dia(17, "Network Reference Topology: Hub-and-Spoke with Central Inspection", "All north-south and east-west traffic traverses the hub; spokes have no internet gateways", 1600, 1000, "Platform")
    d.box(700, 84, 200, 56, "Internet & users", None, "navy")
    d.arrow([(800, 140), (800, 170)], "navy")
    d.group(500, 170, 600, 130, "Edge account (ingress)", "amber")
    d.box(520, 206, 270, 80, "CloudFront + WAF", "Edge caching, bot and OWASP rules", "amber")
    d.box(810, 206, 270, 80, "Public ALB + Shield", "Only entry for inbound HTTP(S)", "amber")
    d.arrow([(800, 300), (800, 340)], "amber", label="ingress", lp=(800, 320))
    d.group(400, 340, 800, 300, "Network hub account (primary region)", "purple")
    xs, w = cols(420, 760, 3, 20)
    ins = d.box(xs[0], 382, w, 100, "Inspection VPC", "Network Firewall / GWLB, IDS and TLS policy", "red")
    tgw = d.box(xs[1], 382, w, 100, "Transit Gateway", "Route tables per tier: prod, non-prod, shared", "navy")
    egr = d.box(xs[2], 382, w, 100, "Egress VPC", "NAT and proxy with domain allow-list", "amber")
    d.box(xs[0], 510, w, 100, "DNS & endpoints", "Route 53 Resolver, shared PrivateLink endpoints", "teal")
    d.box(xs[1], 510, w, 100, "Flow logs", "VPC flow logs and traffic mirroring to SIEM", "teal")
    d.box(xs[2], 510, w, 100, "Network Manager", "Topology view and route analyser", "teal")
    d.arrow([(xs[0] + w, 432), (xs[1], 432)], "purple", both=True)
    d.arrow([(xs[1] + w, 432), (xs[2], 432)], "purple", both=True)
    d.group(25, 340, 290, 300, "On-premises", "gray")
    d.box(45, 382, 250, 100, "Data centres", "Dual Direct Connect / ExpressRoute plus VPN backup", "gray")
    d.box(45, 510, 250, 100, "Branches & partners", "SD-WAN and IPsec attachments", "gray")
    d.arrow([(315, 490), (400, 490)], "gray", both=True, label="DX / VPN", lp=(357, 490))
    d.group(1285, 340, 290, 300, "DR region hub", "gray")
    d.box(1305, 382, 250, 100, "DR Transit Gateway", "Peered; warm standby routes", "gray")
    d.box(1305, 510, 250, 100, "DR inspection", "Mirror of primary policy", "gray")
    d.arrow([(1200, 490), (1285, 490)], "gray", both=True, dash=True, label="peering", lp=(1242, 490))
    d.group(25, 700, 1550, 240, "Spoke VPCs (no internet gateway, tiered subnets)", "green")
    xs5, w5 = cols(45, 1510, 5, 16)
    for x, (t, s, k) in zip(xs5, [("Prod VPC A", "10.10.0.0/16 · public / app / data tiers", "green"), ("Prod VPC B", "10.11.0.0/16 · public / app / data tiers", "green"), ("Non-prod VPC", "10.20.0.0/16 · isolated from prod routes", "blue"), ("Data & analytics VPC", "10.30.0.0/16 · private endpoints only", "purple"), ("Shared services VPC", "10.40.0.0/16 · CI runners, registry", "teal")]):
        d.box(x, 742, w5, 170, t, s, k)
    d.arrow([(800, 640), (800, 700)], "purple", label="TGW attachments · route table per tier", lp=(800, 670))
    d.legend = [("purple", "Hub"), ("red", "Inspection"), ("green", "Spokes"), ("gray", "External / DR")]
    return d


def d18():
    d = Dia(18, "Observability & Operations Model", "A single telemetry pipeline feeds SLOs and incident response; incident learnings flow back into guardrails and ADRs", 1600, 950, "Operations")
    d.group(25, 80, 290, 620, "Telemetry sources", "gray")
    for i, (t, s) in enumerate([("Applications", "Traces, metrics, structured logs"), ("Containers & serverless", "Runtime metrics and platform events"), ("Control-plane audit", "CloudTrail, Activity Log, Audit Logs"), ("Network & DNS", "VPC flow logs, resolver query logs"), ("Security findings", "GuardDuty, Defender, SCC")]):
        d.box(45, 116 + i * 112, 250, 92, t, s, "gray")
    d.group(375, 80, 360, 620, "Collection & processing", "blue")
    for i, (t, s) in enumerate([("OpenTelemetry collectors", "Agents and sidecars, tail sampling"), ("Streaming backbone", "Kinesis / Event Hubs / Pub/Sub, 24h replay"), ("Enrichment & scrubbing", "Account-to-product tags, PII redaction"), ("Routing by classification", "Restricted data stays in region")]):
        d.box(395, 116 + i * 146, 320, 110, t, s, "blue")
    d.group(795, 80, 330, 620, "Storage & analytics", "teal")
    for i, (t, s) in enumerate([("Metrics store", "Prometheus / CloudWatch, 13 months"), ("Log store", "OpenSearch / Log Analytics, 30 days hot"), ("Trace store", "Tempo / X-Ray, 7 days"), ("Immutable audit archive", "S3 Object Lock, 7 years")]):
        d.cyl(815, 116 + i * 146, 290, 120, t, s, "teal", 12)
    d.group(1185, 80, 390, 620, "Action", "red")
    for i, (t, s) in enumerate([("SLO engine", "Burn-rate alerts per service"), ("Alert router", "Paging policy by severity"), ("Incident management", "Sev 1-4, commander role, status page"), ("Automation & runbooks", "SSM, functions, safe auto-remediation")]):
        d.box(1205, 116 + i * 146, 350, 110, t, s, "red")
    for x0, x1, lab in [(315, 375, "OTLP"), (735, 795, "stream"), (1125, 1185, "query")]:
        d.arrow([(x0, 390), (x1, 390)], "navy", label=lab, lp=((x0 + x1) / 2, 390))
    d.group(25, 740, 1550, 170, "Ownership model", "navy")
    xs, w = cols(45, 1510, 3, 20)
    for x, (t, s, k) in zip(xs, [("Product teams", "Instrument code, own SLOs and on-call: you build it, you run it", "green"), ("Platform team", "Run the telemetry pipeline, golden dashboards and paging policy", "purple"), ("CCoE", "SLO templates, post-incident reviews; feed learnings into guardrails and ADRs", "blue")]):
        d.box(x, 780, w, 110, t, s, k)
    d.arrow([(1380, 740), (1380, 700)], "amber", dash=True, label="PIR → backlog", lp=(1380, 720))
    d.legend = [("gray", "Source"), ("blue", "Pipeline"), ("teal", "Store"), ("red", "Action")]
    return d


def d19():
    kp = J("data/kpis.json")
    d = Dia(19, "KPI Scorecard Architecture & Live Catalogue", f"From source systems to executive dashboards; the bottom catalogue is rendered from data/kpis.json (as of {kp['as_of']})", 1600, 960, "Operations")
    d.group(25, 80, 280, 440, "Sources", "gray")
    for i, t in enumerate(["Git: ADRs, RACI, exceptions", "Cloud config & findings", "Billing exports", "CI/CD run history", "ITSM tickets & incidents", "Learning platform (LMS)"]):
        d.box(45, 116 + i * 66, 240, 56, t, None, "gray")
    d.group(365, 80, 260, 440, "Ingestion", "blue")
    for y, (t, s) in zip((140, 270, 400), [("Collectors", "API pollers and event hooks, hourly and on change"), ("Schema validation", "JSON Schema contract per source"), ("Data quality gate", "Dead-letter queue, freshness alarms")]):
        d.box(385, y, 220, 90, t, s, "blue")
    d.group(685, 80, 300, 440, "Store & definitions", "teal")
    d.cyl(705, 150, 260, 130, "Metrics warehouse", "Time series, daily grain, 13-month retention", "teal", 12)
    d.box(705, 330, 260, 110, "KPI definitions as code", "data/kpis.json: target, direction, owner", "teal")
    d.group(1045, 80, 260, 440, "Compute", "purple")
    d.box(1065, 140, 220, 120, "Scorecard engine", "ccoe scorecard computes RAG status and trend", "purple")
    d.box(1065, 300, 220, 110, "Alert rules", "Page the owner when a KPI is red for two periods", "purple")
    d.group(1365, 80, 210, 440, "Outputs", "green")
    for i, t in enumerate(["Exec dashboard", "Ops dashboard", "FinOps view", "Slack alerts"]):
        d.box(1385, 116 + i * 100, 170, 84, t, None, "green")
    for x0, x1, lab in [(305, 365, "pull"), (625, 685, "load"), (985, 1045, "calc"), (1305, 1365, "send")]:
        d.arrow([(x0, 300), (x1, 300)], "navy", label=lab, lp=((x0 + x1) / 2, 300))
    cats = ["Governance", "Platform", "Security", "FinOps", "People"]
    xs, w = cols(25, 1550, 5, 14)
    ck = {"green": "green", "amber": "amber", "red": "red"}
    for x, c in zip(xs, cats):
        d.group(x, 560, w, 355, c + " KPIs", "navy")
        for j, k in enumerate([k for k in kp["kpis"] if k["category"] == c]):
            r = report.rag(k)
            d.box(x + 10, 592 + j * 104, w - 20, 92, k["name"], f"{k['current']} {k['unit']} now · target {k['target']} {k['unit']}", ck[r], 11)
    d.legend = [("green", "Target met"), ("amber", "Within 15%"), ("red", "Off target")]
    return d


def d20():
    ad = adrmod.load_all(os.path.join(ROOT, "adr"))
    ra = J("data/raci.json")
    gr = J("data/guardrails.json")["guardrails"]
    kp = J("data/kpis.json")["kpis"]
    d = Dia(20, "Enterprise Cloud Control Plane: End-to-End Reference Architecture", "Governance artifacts in Git are compiled into enforcement on every cloud, with telemetry and findings flowing back", 1600, 1130, "Architecture")
    d.group(25, 80, 1510, 110, "Stakeholders", "navy")
    xs, w = cols(45, 1470, 4, 20)
    for x, (t, s) in zip(xs, [("Board & executives", "Strategy, funding, risk appetite"), ("Product teams", "Consume the platform"), ("Auditors & regulators", "Independent assurance"), ("Cloud providers", "TAMs, roadmaps, support")]):
        d.box(x, 112, w, 64, t, s, "navy")
    d.arrow([(300, 190), (300, 230)], "navy", label="mandate · funding", lp=(300, 210))
    d.arrow([(1200, 230), (1200, 190)], "amber", dash=True, label="assurance reports", lp=(1200, 210))
    d.group(25, 230, 1510, 330, "CCoE control plane (this repository)", "blue")
    xs5, w5 = cols(45, 1470, 5, 16)
    for x, (t, s, k) in zip(xs5, [("ADR registry", f"adr/ · {len(ad)} decisions", "blue"), ("RACI matrix", f"{len(ra['activities'])} activities, validated", "blue"), ("Guardrail catalogue", f"{len(gr)} guardrails, 4 layers", "red"), ("Exceptions registry", "Time-boxed, auto-expiring", "red"), ("KPI definitions", f"{len(kp)} KPIs, 5 categories", "amber")]):
        d.box(x, 270, w5, 90, t, s, k)
    d.arrow([(800, 360), (800, 400)], "blue", label="versioned releases", lp=(800, 380))
    xs4, w4 = cols(45, 1470, 4, 16)
    for x, (t, s, k) in zip(xs4, [("ccoe policy engine", "validate · check-plan · catalog · scorecard", "purple"), ("CI/CD pipelines", "GitHub Actions with OIDC; policy gate on every plan", "purple"), ("Service catalogue & vending", "Account factory and golden-path modules", "teal"), ("Scorecard & dashboards", "KPI RAG status for executives and auditors", "amber")]):
        d.box(x, 400, w4, 130, t, s, k)
    CL = [(25, "AWS organisation", "SCPs + baselines", [("Preventive", "SCPs per OU"), ("Landing zone", "Account factory with baseline stacks"), ("Security tooling", "GuardDuty, Security Hub, Config"), ("Workload accounts", "Prod and non-prod per app")]),
          (537, "Azure tenant", "Azure Policy + landing zone", [("Preventive", "Azure Policy deny on MG hierarchy"), ("Landing zone", "Subscription vending, ALZ"), ("Security tooling", "Defender for Cloud, Sentinel"), ("Workload subscriptions", "Per app and environment")]),
          (1049, "GCP organisation", "Org Policy + folders", [("Preventive", "Org Policy constraints"), ("Landing zone", "Folders and project factory"), ("Security tooling", "Security Command Center"), ("Workload projects", "Per app and environment")])]
    for gx, lab, al, bx in CL:
        d.group(gx, 620, 486, 250, lab, "green")
        d.arrow([(gx + 243, 560), (gx + 243, 620)], "blue", label=al, lp=(gx + 243, 590))
        for i, (t, s) in enumerate(bx):
            d.box(gx + 15 + (i % 2) * 234, 660 + (i // 2) * 105, 222, 88, t, s, "green", 12)
    d.group(25, 910, 1510, 190, "Shared enterprise services", "teal")
    for x, (t, s) in zip(xs5, [("SIEM & SOAR", "Detection and response automation"), ("Observability", "Metrics, logs, traces, SLOs"), ("FinOps data lake", "Allocation and unit economics"), ("ITSM & CMDB", "Changes, incidents, ownership"), ("Identity provider", "Workforce SSO, MFA, PAM")]):
        d.box(x, 950, w5, 120, t, s, "teal")
    d.arrow([(780, 910), (780, 870)], "teal", label="telemetry · findings · cost", lp=(780, 890))
    d.arrow([(1535, 1000), (1568, 1000), (1568, 420), (1535, 420)], "amber", dash=True)
    d.legend = [("blue", "Governance as code"), ("purple", "Enforcement"), ("green", "Cloud estate"), ("teal", "Shared services")]
    return d


ALL = [d15, d16, d17, d18, d19, d20]
