# Cloud Center of Excellence: Operating Model Repository

A working CCoE operating model: RACI, ADRs and guardrails are **data and code**, validated and enforced in CI, with 20 architecture diagrams generated from the same sources.

## What is inside
| Path | Purpose |
|---|---|
| `data/raci.json` | RACI matrix (18 activities x 9 roles); validator enforces exactly one Accountable |
| `adr/` | 10 Architecture Decision Records, linted and indexed ([index](adr/README.md)) |
| `data/guardrails.json` | 16-guardrail catalogue mapped to NIST, ISO 27001, SOC 2, CIS, PCI, NDPA |
| `data/exceptions.json` | Time-boxed waiver registry (180-day cap, auto-expiry) |
| `data/kpis.json` | 15 KPIs feeding the [scorecard](docs/08-scorecard.md) |
| `src/ccoe/` | Python 3.9+ toolkit, standard library only |
| `policies/` | AWS SCPs, Azure Policy, Rego mirror for Conftest |
| `terraform/aws-scp-baseline/` | Deploys the SCP baseline to your org |
| `diagrams/` | 20 SVG diagrams plus `index.html` gallery |
| `docs/` | Charter, operating model, governance, maturity, FinOps, exceptions |

## Quick start
```bash
make all        # validate, test, build diagrams, regenerate docs
make demo       # good plan passes; bad plan is blocked with exit code 1
python3 -m ccoe check-plan plan.json --format markdown   # use in any Terraform repo (PYTHONPATH=src)
```
Open `diagrams/index.html` in a browser for the gallery, or see [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## How the guardrail engine works
`terraform show -json` output is evaluated against `data/guardrails.json`. Rule types: `attrs_true`, `attr_eq`, `attr_not_eq`, `required_tags`, `no_open_ingress`, `allowed_regions`, `iam_no_wildcard_admin`. Mandatory failures exit 1 and block the merge; advisory ones warn. Waivers from the exception registry are honoured until expiry.

## Diagram index
1 Operating model on a page · 2 Organisation · 3 Governance forums · 4 RACI heatmap (live) · 5 Landing zone OUs · 6 Guardrail defence in depth · 7 Policy-as-code pipeline · 8 ADR lifecycle · 9 ADR dependency graph (live) · 10 Adoption roadmap · 11 Service catalogue · 12 FinOps · 13 Control traceability (live) · 14 Exception workflow · 15 Account vending sequence · 16 Identity and access · 17 Network topology · 18 Observability · 19 KPI architecture (live) · 20 End-to-end control plane

## Notes on scope
The Rego files mirror a subset of guardrails and are provided for teams standardised on OPA; the Python engine is the tested reference implementation. Terraform and SCP files are provided as deployable baselines and should be reviewed in a non-production organisation first. Sample figures in `data/kpis.json` are illustrative.

MIT licensed.
