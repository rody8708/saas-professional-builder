# 08 · Add a client feature with a backend contract

## Feature
{{Client platforms, workflow, roles, offline needs and acceptance criteria}}

## Procedure
1. Read rules, project/client profile and [API/client guidance](../core/api-and-native-clients.md). Use the chosen client framework and its existing conventions.
2. Define or extend the actual API contract: authentication, permission, data, errors, compatibility, pagination and idempotency where relevant. Proposed fields/endpoints are documented before use.
3. Implement backend authorization and live tenant membership. For Bearer-only routes, reject cookie fallback and do not change browser sessions; do not require browser CSRF. Cookie-authenticated routes keep their declared CSRF protection.
4. Implement client state, navigation, transport and secure credential storage through the established architecture. The backend remains authoritative for commercial and security decisions.
5. If offline applies, scope caches/queues by environment+user+tenant, mark pending writes, define conflicts, cursor expiry, deletion and resync. Clear/re-scope data on logout/revocation/context change.
6. Render text as text; rich content or embedded browsing requires contextual sanitization and URL policy.
7. Verify agreed layouts, accessibility, languages and all reachable states. Apply the client's actual version/release policy.
8. Run profile-specific checks and exercise the real client against the isolated lab: login, stronger-auth, tenant switch, denial, revocation, retry and offline recovery where applicable.

## Deliver
Contract and implementation, checks, device/client/version matrix, persisted-state evidence, cleanup and unexecuted cases. Do not impose a native app on a product whose requested client is web-only.
