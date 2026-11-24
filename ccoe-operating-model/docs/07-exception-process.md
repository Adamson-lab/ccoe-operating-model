# Exception and Waiver Process

Diagram: [14 Exception workflow](../diagrams/svg/14-exception-waiver-workflow.svg).

1. Requester opens a PR adding an entry to `data/exceptions.json` (fields: id, guardrail, resource, created, expires, approver, ticket, justification, compensating_controls).
2. CCoE triages within 2 days; Security and Risk assesses within 3 days.
3. Exception Board decides weekly. Maximum duration is **180 days**; renewals need a new PR.
4. On merge, `ccoe check-plan` downgrades the matching violation to *waived* until expiry. After expiry the violation blocks again automatically.

Try it: `make demo` shows EXC-001 waiving the legacy volume; `--today 2027-02-01` shows it expiring.
