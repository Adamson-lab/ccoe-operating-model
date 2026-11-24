# RACI Matrix

_Generated from `data/raci.json` by `ccoe raci-md`. Do not edit by hand._

| Group | Activity | Exec Sponsor | Cloud Council | CCoE Core | ARB | Security & Risk | FinOps | Platform Eng | BU / Product | Internal Audit |
|---|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| Strategy | A01 Define cloud strategy and principles | **A** | R | C | C | C | C | I | I | I |
| Strategy | A02 Approve funding and chargeback model | **A** | C | C |  |  | R |  | I | I |
| Strategy | A03 Set risk appetite and data classification | C | **A** | C | C | R | I | I | I | C |
| Architecture | A04 Maintain reference architectures |  | I | R | **A** | C | I | R | C |  |
| Architecture | A05 Review and approve ADRs |  | I | R | **A** | C |  | C | C | I |
| Platform | A06 Operate landing zone and account vending |  |  | **A** | C | C | I | R | I |  |
| Platform | A07 Maintain golden-path IaC modules |  |  | R | I | C |  | **A** | C |  |
| Security | A08 Author and maintain guardrail policies |  | I | R | C | **A** |  | R | C | I |
| Security | A09 Approve exceptions and waivers |  | I | R | C | **A** |  |  | R | I |
| Security | A10 Monitor continuous compliance and drift |  |  | C |  | **A** |  | R | R | I |
| Security | A11 Cloud incident response | I | I | C |  | **A** |  | R | R |  |
| Security | A12 Independent control assurance | I | I | C |  | C |  |  |  | **A/R** |
| FinOps | A13 Enforce tagging and cost allocation |  |  | R |  | I | **A** | R | R | I |
| FinOps | A14 Manage commitments and rightsizing | I |  | C |  |  | **A** | R | C |  |
| FinOps | A15 Publish showback and chargeback | I | I | C |  |  | **A/R** |  | I |  |
| People | A16 Run cloud skills and certification program | I | C | **A/R** |  |  | I |  | R |  |
| People | A17 Run cloud champions network | I | I | **A/R** |  |  |  |  | R |  |
| Delivery | A18 Onboard and migrate workloads |  |  | C | C | C | C | R | **A/R** |  |

**Legend:** R = Responsible; A = Accountable; AR = Accountable and Responsible; C = Consulted; I = Informed

## Load per role

| Role | Accountable | Responsible |
|---|:-:|:-:|
| Executive Sponsor (CIO/CTO) | 2 | 0 |
| Cloud Council | 1 | 1 |
| CCoE Core Team | 3 | 8 |
| Architecture Review Board | 2 | 0 |
| Security & Risk | 4 | 1 |
| FinOps | 3 | 2 |
| Platform Engineering | 1 | 8 |
| BU Cloud Champions & Product Teams | 1 | 7 |
| Internal Audit | 1 | 1 |
