# ADR-0003: Hub-and-spoke network with central inspection
- Status: Accepted
- Date: 2026-05-13
- Deciders: ARB
- Domain: platform
- Related: 0002
- Supersedes: -

## Context
Workloads need private connectivity to on-premises and controlled egress without mesh peering sprawl.

## Decision
Use a network hub account with Transit Gateway, centralised inspection and egress, shared DNS resolvers and no internet gateways in spoke VPCs.

## Consequences
Consistent traffic inspection and simpler routing. Hub is a critical shared service requiring multi-AZ and a DR peer.

## Alternatives considered
- Full-mesh VPC peering: rejected, does not scale.
- Per-VPC firewalls: rejected, duplicated cost and policy drift.
