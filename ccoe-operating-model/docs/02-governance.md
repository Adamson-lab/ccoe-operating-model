# Governance

Diagrams: [03 Forums and cadence](../diagrams/svg/03-governance-forums-decision-cadence.svg), [08 ADR lifecycle](../diagrams/svg/08-adr-lifecycle-state-machine.svg), [14 Exception workflow](../diagrams/svg/14-exception-waiver-workflow.svg).

| Forum | Cadence | Chair | Decides |
|---|---|---|---|
| Cloud Council | Quarterly | CIO | Strategy, funding, risk appetite, charter |
| Risk and Investment Committee | Quarterly | CFO + CISO | Exposure, spend trajectory |
| ARB | Weekly | Chief cloud architect | ADRs, standards, reference architectures |
| Exception Board | Weekly | Cloud security lead | Waivers |
| FinOps Board | Monthly | FinOps lead | Budgets, commitments, chargeback |
| Security Guild | Fortnightly | Security lead | Guardrail backlog, threat review |

## Decision flow
Anyone proposes by pull request. CODEOWNERS routes to the right forum. Decisions are merged into the repository, which is the single source of truth. CI (`make validate`) blocks malformed ADRs, RACI rows without exactly one Accountable, and invalid exceptions.

## Escalation
Operational forum, then tactical forum, then Cloud Council. Unresolved after two cycles escalates automatically.
