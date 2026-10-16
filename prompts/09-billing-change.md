# 09 · Change billing safely

## Change
{{Commercial rule, affected scopes, provider and acceptance criteria}}
Read project rules/profile and [billing guidance](../core/billing-entitlements.md). Billing is in scope only when requested.

## Design before effects
- Define the authoritative catalog, entitlement, permission and quota separately.
- Describe durable transition/operation/attempt, frozen payload, exact amounts/currency and uniqueness boundary.
- Reuse one idempotency key for transport retry, timeout, lost response or local failure after remote success. A new payment attempt requires a confirmed prior outcome and an explicit policy.
- Define provider confirmation, account/scope/object binding, idempotency window, unknown-outcome reconciliation and manual escalation.
- Specify cancellation, reversal, suspension and retry timing; email availability does not drive the payment clock.
- Keep privacy requests and service cancellation separate according to the chosen policy.

## Implement
Use the selected provider's adapter and actual supported APIs. Verify incoming signatures over raw body with timestamp/replay controls, without browser session/CSRF. Claims, leases and fencing protect concurrent processing. Durable downstream effects need outbox or equivalent delivery. Preserve immutable financial facts and model later adjustments explicitly.

## Verify
Use synthetic sandbox data. Test success, rejection, accepted request with lost response, local persistence failure, concurrent retry, duplicate/out-of-order event, invalid signature, expired key window, cancellation/reversal and outage recovery. Inspect one charge, correct entitlement and durable state. Never rotate a key merely to escape an unknown result.

Distinguish deterministic simulation from actual sandbox evidence; list unsupported/unexecuted scenarios. Use only test credentials and valid TLS, and remove owned resources.

## Deliver
Rule/contract changes, implementation, meaningful automated and real-flow evidence, reconciliation/runbook updates, cleanup and remaining gates.
