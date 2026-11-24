# ADR-0001: Record architecture decisions as ADRs in Git
- Status: Accepted
- Date: 2026-04-11
- Deciders: ARB
- Domain: governance
- Related: 0007
- Supersedes: -

## Context
Decisions made in meetings and chat are lost, and new teams repeat old debates.

## Decision
Every significant cloud architecture decision is recorded as a Markdown ADR in /adr, reviewed by pull request, numbered sequentially and linted in CI.

## Consequences
Decisions are discoverable, reviewable and auditable. Authors pay a small writing cost; the ARB must keep cycle time low.

## Alternatives considered
- Wiki pages: rejected, no review trail or immutability.
- Slide decks: rejected, not versioned or searchable.
