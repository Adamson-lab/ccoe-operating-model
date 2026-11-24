# ADR-0008: Time-boxed exceptions with compensating controls
- Status: Accepted
- Date: 2026-07-18
- Deciders: ARB
- Domain: governance
- Related: 0004, 0007
- Supersedes: -

## Context
Rigid rules get bypassed informally; permanent exceptions erode the control set.

## Decision
Exceptions are requested by pull request to data/exceptions.json, approved by the Exception Board, limited to 180 days, require compensating controls and expire automatically in CI.

## Consequences
Deviation is visible and temporary. The registry needs regular review and the board needs SLAs.

## Alternatives considered
- No exceptions: rejected, drives shadow IT.
- Permanent waivers: rejected, controls decay.
