# 04 · Implement one feature end to end

## Request
{{User story, acceptance criteria, allowed actors, affected data and surfaces}}

## Procedure
1. Read project rules, selected profile and affected contracts. Identify unresolved permission, tenancy, commercial or destructive-data decisions before implementing them.
2. Describe the operation: input, output, failures, authority, invariants, transaction and external effects. Use the framework's established composition and structure.
3. Define a meaningful test matrix: success, validation, denial, other tenant and relevant concurrency/retry/dependency failures.
4. Implement at the appropriate boundary. Keep protocol details in adapters and business decisions testable; use abstractions where they protect a real boundary.
5. For effects that cannot be lost, persist intent with outbox or an equivalent guarantee; make delivery idempotent.
6. Apply authentication-specific protection: CSRF for ambient credentials, strict Bearer-only isolation or signed webhook verification. Encode output for its actual context.
7. Implement designed UI states and agreed localization/accessibility, if visible.
8. Run focused and required project checks, then exercise the affected real entry point in the lab. Inspect persisted state and side effects.
9. Synchronize contracts and documentation; record gaps and cleanup.

## Deliver
Behavior changed and why, files, meaningful tests, acceptance evidence and remaining risks. Refer to [testing guidance](../core/testing-verification.md); do not claim an unexecuted check passed.
