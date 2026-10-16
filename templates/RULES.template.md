# Project rules

Status: {{draft/accepted}}

Owner: {{owner}}

Profile: {{project profile path and revision}}
Architecture: {{architecture/decision references}}

Adapt this template to the product. MUST denotes a required invariant; SHOULD permits a documented exception. An exception records owner, reason, scope, mitigation and review condition. Requirements apply to capabilities actually present.

## Product and architecture

- MUST preserve declared module/data ownership and compatibility contracts.
- MUST keep authority and business invariants enforceable independently of UI behavior.
- SHOULD use the selected framework's maintained mechanisms and the simplest deployment shape that meets requirements.
- SHOULD add abstractions for actual boundaries/variation, not one interface or service per class by default.
- MUST document effects that cross transaction boundaries and provide recovery when loss or duplication violates the contract.
- Architecture checks: {{actual checks, scope and known limitations}}.

## Identity and tenancy

- MUST authenticate through maintained mechanisms and validate credential/user state.
- MUST revalidate permissions, active membership and tenant status at protected operations, including alternative entry points.
- MUST enforce the chosen tenant model in reads, writes, relationships, jobs, caches, files, search and exports.
- MUST test cross-tenant denial and absence of indirect leakage.
- Authentication modes and stronger-auth policy: {{references}}.
- Tenant model and data owners: {{references}}.

## Security and privacy

- MUST protect mutations using ambient credentials against CSRF; Bearer-only routes reject cookie fallback; webhooks verify raw-body signatures and replay controls.
- MUST encode/sanitize output by context, validate URL schemes and use safe query APIs with parameterized values.
- MUST bound external calls, uploads and public-endpoint cost; enforce the agreed egress/TLS policy.
- MUST keep public errors safe and logs minimized/redacted with controlled access.
- MUST keep secrets and operational/customer data out of source control and fixtures.
- MUST define export, suppression, retention, shared ownership and restore behavior before implementing destructive data policy.
- Data policy: {{reference}}. No universal retention, grace or subscription-blocking rule is implied.

## Consistency and commercial operations

- MUST define transaction and concurrency boundaries for invariant-changing operations.
- MUST preserve a stable idempotency key/payload for retries of the same external operation.
- MUST reconcile unknown outcomes before starting another effect that could duplicate a charge or mutation.
- MUST use outbox or an equivalent durable mechanism when lost delivery violates the contract.
- Billing/entitlement policy, if applicable: {{reference or not applicable}}.

## Verification and cleanup

- MUST use synthetic identities and isolated infrastructure; tests cannot read operational environment files/databases.
- MUST register owned resources, teardown on failure/success and verify absence.
- MUST test database semantics on the supported production engine and any other promised engines.
- MUST demonstrate bug regressions before/after and replay affected significant flows through their real entry points.
- MUST record actual results and explicit gaps; health, coverage and review alone do not prove functional acceptance.
- Test commands, matrix and thresholds: {{real project profile references}}.

## Experience and documentation

- MUST meet agreed accessibility, locales, formats, supported devices/themes and workflow states.
- MUST update affected contracts, user/developer guidance and operation with behavior changes.
- SHOULD keep user copy clear and dynamic limits/plan names tied to their source.
- Experience/release standards: {{references}}.

## Delivery and operations

- MUST inspect the final diff, scan for private data and verify cleanup before publication.
- MUST use versioned migrations and document compatibility, rollout and rollback/forward recovery.
- MUST define operational owners, alert routing, SLO and recovery objectives; only measured evidence demonstrates them.
- MUST follow the user's authorization and the repository's actual branch/CI/publication policy.
- Delivery, CI, restore and incident references: {{paths}}.
