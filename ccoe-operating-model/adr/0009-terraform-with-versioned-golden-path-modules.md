# ADR-0009: Terraform with versioned golden-path modules
- Status: Accepted
- Date: 2026-08-10
- Deciders: ARB
- Domain: platform
- Related: 0002, 0004
- Supersedes: -

## Context
Teams reinvent infrastructure patterns inconsistently and bypass guardrails.

## Decision
Terraform is the standard IaC tool. The CCoE publishes semver-versioned modules (network-spoke, secure-bucket, iam-role and others) with guardrails baked in; teams consume them from the registry.

## Consequences
Faster delivery and built-in compliance. Module maintenance becomes a platform responsibility.

## Alternatives considered
- Native CloudFormation only: rejected, weaker multi-cloud story.
- Free-form IaC: rejected, no paved road.
