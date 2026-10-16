# 03 · Add a coherent module

## Request
Implement {{capability, workflows, actors, data, acceptance criteria}}.

## Design
Read the project rules/profile and [module guidance](../core/modules-and-apps.md). Define module ownership, public contracts, dependencies, data lifecycle, permissions and entry points. Choose an internal module or separate deployment from actual requirements; commercial packaging is optional.

Use native framework conventions. Design schema and tenant-safe relationships, transaction boundaries, idempotency, failure categories and any durable deliveries. Other modules access owned data through declared contracts.

## Implement and verify
- Revalidate permissions and tenant membership in operations; test cross-tenant reads, writes, aggregates and applicable jobs/caches/files.
- Implement migrations, configuration examples without secrets, setup and recovery.
- If personal data is stored, implement the selected export/suppression/retention policy.
- If billing applies, resolve entitlement and quota in the backend; no invented plans.
- Build the necessary UI/API/jobs with designed states and the agreed locales/accessibility.
- Test business invariants, adapters on the supported production engine, concurrency and duplicate/retry cases where relevant.
- Exercise the main flows through their real entry points in an isolated representative lab; inspect state and effects.
- Remove owned test resources and verify absence.

## Deliver
Module contracts, implemented flows, data/permission model, tests and evidence, operator/developer docs and explicit gaps. A module is not complete merely because its first happy path works.
