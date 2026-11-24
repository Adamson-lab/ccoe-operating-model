# ADR-0005: Federated identity with no long-lived human credentials
- Status: Accepted
- Date: 2026-06-15
- Deciders: ARB
- Domain: security
- Related: 0002
- Supersedes: -

## Context
Static access keys leak and are hard to rotate or attribute.

## Decision
Humans authenticate through the central IdP with MFA and assume time-boxed roles; pipelines use OIDC federation. IAM users with access keys are prohibited (G-IAM-001).

## Consequences
Stronger attribution and less secret sprawl. Break-glass access must be rigorously controlled and tested.

## Alternatives considered
- IAM users with key rotation: rejected, operational burden and leak risk.
