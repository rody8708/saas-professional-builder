## Problem and resulting behavior

{{Concrete trigger and before/after behavior; scope useful to a reviewer without conversation history.}}

## Verification

| Check or flow | Environment/revision | Actual result | Evidence |
|---|---|---|---|
| {{check}} | {{environment}} | {{passed/failed/blocked/not run; real counts}} | {{sanitized reference}} |

{{For a fix: reproduction, failing regression before, passing after and affected real-entry-point replay. For documents only: state the documentary checks and absence of runtime claims.}}

## Applicable controls

Check only with supporting evidence. Mark non-applicable items explicitly with a reason.

- [ ] Permissions and current membership/tenant context validated.
- [ ] Cross-tenant reads/writes and affected jobs/caches/files checked.
- [ ] Protection matches authentication mode; contextual output handling checked.
- [ ] Idempotency, concurrency, partial failure and durable delivery covered where relevant.
- [ ] Data lifecycle and shared ownership follow explicit policy.
- [ ] Required UX, accessibility, locales and client surfaces verified.
- [ ] Documentation and contracts reflect implemented behavior.
- [ ] Complete diff inspected; secrets/private data excluded.
- [ ] Owned temporary resources removed and absence verified.

## Data, compatibility and deployment

{{Migration/backfill; coexistence with old code/clients; rollout order; abort criteria; rollback/forward recovery; owner. State not applicable with reason when appropriate.}}

## Operational impact

{{Configuration changes without secrets; capacity/cost, monitoring, alerts, runbooks and recovery impact.}}

## Remaining gaps and exceptions

| Gap/exception | Impact | Owner | Evidence needed to close |
|---|---|---|---|
| {{item or none}} | {{impact}} | {{owner}} | {{closure}} |

{{Do not call an unexecuted check passed, an unresolved evidence gap fixed, or a subset of tests production certification.}}
