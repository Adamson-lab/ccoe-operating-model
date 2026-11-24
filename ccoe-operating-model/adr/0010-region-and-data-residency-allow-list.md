# ADR-0010: Region and data-residency allow-list
- Status: Accepted
- Date: 2026-08-11
- Deciders: ARB
- Domain: security
- Related: 0004
- Supersedes: -

## Context
Regulation and contracts constrain where data may be stored and processed.

## Decision
Only an approved list of regions is permitted, enforced by an SCP (preventive) and check-plan (proactive, G-REG-001). Additions require an ADR.

## Consequences
Residency is demonstrable. Some global services need explicit carve-outs.

## Alternatives considered
- Policy documents only: rejected, not enforceable.
