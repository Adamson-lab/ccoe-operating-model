# ADR-0006: Mandatory tagging and cost allocation standard
- Status: Accepted
- Date: 2026-06-16
- Deciders: ARB
- Domain: finops
- Related: 0002
- Supersedes: -

## Context
Without ownership and cost-centre tags, showback and chargeback are unreliable.

## Decision
Four mandatory tags (owner, cost-center, environment, data-classification) are enforced by G-TAG-001 and inherited via provider default_tags.

## Consequences
Allocation accuracy improves and orphaned spend is traceable. Teams must adopt tagging in modules.

## Alternatives considered
- Account-only allocation: rejected, cannot split shared accounts.
