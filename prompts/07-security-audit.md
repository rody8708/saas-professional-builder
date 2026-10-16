# 07 · Audit security, tenancy and privacy

## Scope
{{Areas, environments and authorized mode: read-only review or isolated active testing}}
Read project rules/profile and [security guidance](../core/security-privacy.md). Default to read-only if active testing or fixes were not requested.

## Map and assess
1. Identity: supported auth mechanisms, credential lifecycle, recovery, stronger-auth parity, session fixation, revocation and abuse limits.
2. Authority: explicit permission at each operation; current membership/role/tenant state; composite actions; impersonation if present.
3. Tenancy: reads, writes, aggregates, search, jobs, caches, files, exports and events; tenant-safe relationships.
4. Route modes: CSRF with ambient credentials; Bearer-only without cookie fallback; signed raw-body webhooks with timestamp/replay controls.
5. Input/output: contextual encoding/sanitization, URL schemes, parameterized queries, uploads, redirects and egress.
6. Privacy: explicit data matrix, export/suppression/retention, shared ownership, backup restoration, minimized logs and external processing.
7. Payments if present: durable intent, stable keys for unknown outcomes, confirmation, claims/fencing and reconciliation.

## Verify within authorization
For active testing, use only isolated synthetic resources. Include missing/invalid CSRF, valid cookie with absent/invalid Bearer, conflicting cookie/token tenants, revoked memberships, direct file access and queued jobs. For webhooks test invalid/expired signatures and duplicates; for rendered content test each executable context. Inject failures only in owned resources.

Read-only analysis must not create accounts, send messages, mutate records or run destructive probes. When fixes are authorized, demonstrate the defect, add a failing regression, fix and replay the affected real entry point. Cleanup and verify all owned resources.

## Output
Finding, severity, evidence, root cause, remedy and status; separate policy decisions from defects. Include tested scope, tests not executed, cleanup and exact evidence needed to close each gap. No legal-compliance or universal security certification.
