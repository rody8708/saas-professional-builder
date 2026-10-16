# 10 · Migrate data with compatibility and recovery

## Change
{{Schema/data change, owning module, supported engines and deployment shape}}

## Procedure
1. Read rules/profile and [delivery guidance](../core/delivery-workflow.md). Use the framework's versioned migration mechanism.
2. Describe current/target schema, data ownership, tenant-safe relationships, indexes, invariants and impact on old callers.
3. Plan expand-contract where versions coexist: compatible expansion, compatible code, idempotent batched backfill, validation, retirement and separately controlled contraction.
4. Define transaction/DDL limits, privileges, locks, duration, interruption and resumability for every supported engine.
5. Provide a safe rollback where possible; otherwise label the step irreversible and define recovery/forward repair. Do not pretend data loss is reversed by restoring a column name.
6. Test empty and populated synthetic databases on all supported engines, including production's engine. Exercise interruption/retry, concurrency and constraints.
7. Run rollback/up cycles for reversible changes; rehearse the actual recovery plan for irreversible changes.
8. Document deployment order, observability, abort criteria and owner. Destructive production execution requires the user's applicable authorization and is not implied by writing a migration.

## Deliver
Migration and backfill, compatibility matrix, measured test results, recovery evidence and remaining risks. Tests use isolated data and verified cleanup, never copies of customer databases.
