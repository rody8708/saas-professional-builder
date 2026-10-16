# Project profile: {{project name}}

Status: {{draft / accepted / partially decided}}

Owner: {{owner}}

Updated: {{date}}

Technical profile: {{id and path from the profile registry}}
Decision references: {{accepted decisions and requirements}}

Complete what affects the current task. Mark unknowns pending with impact/owner; do not silently replace them with defaults. The profile selects mechanisms while core guidance defines guarantees.

## Product and scope

| Field | Decision |
|---|---|
| Users and valuable workflows | {{actors and jobs}} |
| Current milestone and acceptance | {{bounded deliverable}} |
| Explicitly excluded capabilities | {{scope}} |
| Data sensitivity and deployment constraints | {{constraints}} |
| Product/engineering/security decision owners | {{roles}} |

## Stack and repository

| Field | Decision |
|---|---|
| Language/runtime and supported versions | {{decision}} |
| Framework and conventions | {{decision}} |
| Package manager and dependency lock strategy | {{decision}} |
| Client surfaces/frameworks | {{decision}} |
| Architecture/deployment shape and reason | {{decision}} |
| Module boundaries and owners | {{decision}} |
| Repository/visibility and integration branch | {{decision; no remote if absent}} |
| Base/branch/change policy | {{decision}} |
| Publication, merge and deployment authority | {{roles and existing authorization}} |

Use framework facilities where suitable; custom infrastructure needs a concrete reason.

## Persistence and tenancy

| Field | Decision |
|---|---|
| Production engine/version and other supported engines | {{decision}} |
| Tenant model and effective-context resolution | {{row/schema/database/other}} |
| Relationship constraints and shared-data ownership | {{decision}} |
| Reads/writes/search/export isolation | {{mechanisms}} |
| Job/queue/cache/file isolation | {{mechanisms}} |
| Transactions, concurrency and exact numeric representation | {{decision}} |
| Migration/backfill/expand-contract/recovery | {{mechanism and owners}} |
| Durable events, outbox and reconciliation | {{required effects and mechanism}} |

## Identity and authority

| Field | Decision |
|---|---|
| Identity provider/credential mechanism | {{decision}} |
| Enrollment, recovery and abuse controls | {{decision}} |
| Stronger-auth requirements and surface parity | {{decision}} |
| Session/token lifetime, revocation and secure storage | {{decision}} |
| Cookie, Bearer-only and webhook route contracts | {{decision}} |
| Roles/capabilities and composite permissions | {{decision}} |
| Membership changes and revalidation | {{decision}} |
| Platform authority/impersonation if needed | {{decision or not applicable}} |

## Commercial capability

| Field | Decision |
|---|---|
| Billing needed | {{yes/no and scope}} |
| Provider, account model and API lifecycle | {{decision or not applicable}} |
| Plans/entitlements/quotas and source of truth | {{decision}} |
| Money, currencies, tax and rounding | {{decision}} |
| Cancellation, refunds, disputes and retry policy | {{decision}} |
| Idempotency window, unknown outcomes and reconciliation | {{decision}} |
| Commercial-to-privacy interaction | {{explicit policy, not inferred}} |

## Data lifecycle

| Category/finality | Owner/scope | Export | Suppression/conservation | Retention/start | Restore treatment |
|---|---|---|---|---|---|
| {{category}} | {{owner}} | {{contract}} | {{policy}} | {{duration/event}} | {{method}} |

{{Include logs, uploads, backups, visitors without accounts and any external processing. State applicable policy/jurisdiction review, exceptions, shared ownership, request handling and grace only if chosen. No universal legal claims or fixed time defaults.}}

## Experience and language

| Field | Decision |
|---|---|
| Product locales and engineering/documentation languages | {{decision}} |
| Fallback, timezone, currency and formats | {{decision}} |
| Accessibility target and verification | {{decision}} |
| Devices, viewports, themes and design system | {{decision}} |
| Offline/client compatibility and release policy | {{decision or not applicable}} |
| Help/assistant capability and authority | {{decision or not applicable}} |

## Build, checks and CI

List commands verified in the actual project; placeholders are not executable instructions.

| Purpose | Actual command/tool | Required environment | Evidence/status |
|---|---|---|---|
| Install/build | {{command}} | {{environment}} | {{status}} |
| Format/lint/type or static analysis | {{command}} | {{environment}} | {{status}} |
| Unit/contract tests | {{command}} | {{environment}} | {{status}} |
| Integration/production-engine tests | {{command}} | {{environment}} | {{status}} |
| UI/client/acceptance | {{command or flow}} | {{environment}} | {{status}} |
| Architecture and dependency controls | {{command}} | {{environment}} | {{scope/limits}} |
| Secret/private-data scan | {{command}} | {{environment}} | {{status}} |

CI provider/runners, trust boundaries, permissions, required checks, artifact retention and owner: {{decisions}}. Test resource ownership and teardown/absence verification: {{mechanisms}}.

## Operations and gates

| Field | Decision |
|---|---|
| Environments and production-shaped acceptance lab | {{decision}} |
| SLO/SLI, budget of error and monitoring owner | {{decision}} |
| RPO/RTO, backup coverage and restore cadence | {{decision}} |
| Jobs/queue/retention health and escalation | {{decision}} |
| Configuration/secrets management and rotation | {{decision}} |
| Rollout, abort, rollback/forward recovery | {{decision}} |
| Incident runbooks and responsible roles | {{decision}} |

| Gate | Required evidence | Owner | Current status |
|---|---|---|---|
| {{capability/release gate}} | {{evidence}} | {{owner}} | {{verified/pending/not applicable with reason}} |

## Outstanding decisions

| Decision | Affected work | Owner | Next action |
|---|---|---|---|
| {{unknown or none}} | {{impact}} | {{owner}} | {{resolution}} |
