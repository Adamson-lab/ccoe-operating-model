# ADR-0002: Multi-account landing zone with automated account vending
- Status: Accepted
- Date: 2026-04-12
- Deciders: ARB
- Domain: platform
- Related: 0003, 0005, 0006, 0009
- Supersedes: -

## Context
Shared accounts blur blast radius, billing and ownership. Manual account creation takes weeks.

## Decision
Adopt an AWS Organizations multi-account structure (Security, Infrastructure, Sandbox, Workloads, Policy Staging, Suspended OUs) and vend accounts through an automated factory driven by pull requests.

## Consequences
Strong isolation and per-account cost attribution. Requires an account factory pipeline and baseline stacks to be maintained as a product.

## Alternatives considered
- Single account per environment: rejected, large blast radius.
- Manual ticket-driven creation: rejected, slow and inconsistent.
