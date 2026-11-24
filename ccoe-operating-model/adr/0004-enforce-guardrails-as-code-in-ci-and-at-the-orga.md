# ADR-0004: Enforce guardrails as code in CI and at the organisation layer
- Status: Accepted
- Date: 2026-05-14
- Deciders: ARB
- Domain: security
- Related: 0008, 0009, 0010
- Supersedes: -

## Context
Manual security review does not scale and finds issues after deployment.

## Decision
Express guardrails as versioned data (data/guardrails.json) evaluated against Terraform plan JSON by ccoe check-plan, backed by preventive SCPs and detective controls. Mandatory failures block merges.

## Consequences
Fast feedback and one auditable catalogue. Policies are code and need owners, tests and releases.

## Alternatives considered
- Review boards only: rejected, slow and non-repeatable.
- Detective controls only: rejected, issues reach production first.
