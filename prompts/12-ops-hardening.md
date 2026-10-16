# 12 · Make operations recoverable

## Scope
{{Jobs, queues, backups, configuration, monitoring, retention or defined service}}
Read project rules/profile and [operations guidance](../core/operations.md). Confirm operational owners, environments, SLO, RPO and RTO.

## Assess and implement within scope
1. Configuration: validated prerequisites, secrets management, safe examples, least privilege and reproducible artifacts.
2. Jobs/queues: atomic claims, lease/fencing where needed, timeout, interruption recovery, bounded retry, backlog visibility and idempotent effects.
3. Durability: outbox or equivalent when event/delivery loss violates the contract; retention and replay boundaries.
4. Backups: coverage/cadence tied to RPO, encrypted copies outside the failure domain, separate recoverable keys and approved retention.
5. Restore: isolated rehearsal including data/files/dependencies, application invariants, resumed jobs and already-suppressed data. Measure elapsed time and recovery point.
6. Observability: relevant service/flow signals, external detection, safe correlated logs, actionable alert routing and escalation.
7. Runbooks: owner, signals, preconditions, steps, checks, abort/recovery and evidence.

## Verify
Inject faults only in owned synthetic lab resources: worker interruption, stale lease/heartbeat, provider outage, quota exhaustion, failed backup and restore. Confirm alerts, controlled errors, recovery and no duplicated effects. Remove and verify owned resources.

## Deliver
Controls verified vs pending, measured objectives, fault/recovery evidence, runbooks and residual risk. Do not claim RTO/RPO met from a backup file or health response alone.
