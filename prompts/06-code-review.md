# 06 · Review concrete defects

## Scope
Review {{diff, pull request, branch or artifact}} against the project rules/profile. This is read-only unless fixes were separately authorized.

## Inspect
- Correctness: invariants, transactions, concurrency, precision, timezone, partial failure and retries.
- Architecture: declared boundaries, ownership, inappropriate coupling and controls that scan no code or overstate their coverage.
- Security: actual authentication mode, explicit/revalidated permission, cross-tenant access in reads/writes/jobs/cache/files, contextual CSRF/XSS, injection, egress and safe errors.
- Billing if present: stable idempotency keys during unknown outcomes, provider confirmation, event ordering, reconciliation and durable delivery.
- Privacy: chosen data lifecycle, minimized logs, shared ownership, export/suppression/retention and restoration.
- Tests: credible regression, production-engine semantics, synthetic isolation, meaningful assertions and verified cleanup.
- UX: agreed locales, formats, accessibility, states and actual visual verification.
- Delivery: contracts/docs, migration compatibility/recovery, operational ownership and truthful evidence.

## Method
Read the relevant diff and callers. For every finding, establish a concrete input/state and wrong outcome, with exact path/line evidence. Separate demonstrated defects from unanswered decisions and unexecuted checks. Do not invent runtime evidence or execute mutating acceptance flows during a read-only review.

## Output
Rank actionable findings by severity with location, failing scenario, impact and remedy. Then state the inspected scope and material verification gaps. If no actionable defect was found, say so without implying complete safety or production certification.
