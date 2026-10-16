# 15 · Refactor a declared boundary without changing behavior

## Target
{{Boundary violation or debt item, current exception, responsible module}}

## Procedure
1. Read project rules/profile and [architecture guidance](../core/architecture.md). Confirm the rule protects a real boundary rather than a stylistic preference.
2. Characterize behavior and relevant failures before moving code; add meaningful missing coverage.
3. Refactor using the framework's native composition and conventions. Add interfaces/adapters only where they improve isolation or replaceability.
4. Preserve transaction, authorization, tenancy and side-effect semantics. A new abstraction must not hide changes to retry or durability.
5. Remove the resolved exception in the same change. Run the guard and compare its scope/thresholds with the base so coverage was not silently reduced.
6. Run affected tests and required checks; replay the significant real entry point when behavior could be disturbed.
7. Update architectural documentation and debt status; clean owned resources.

## Constraints
Do not mix unrelated behavior changes. If a newly discovered bug requires different behavior, give it an explicit decision, regression and coherent change. Do not grow exclusions to make the refactor green; an intentional rule change requires a documented architecture decision.

## Deliver
Boundary/debt change, before/after behavior evidence, checks, exceptions removed and remaining risk. Do not replace the agreed framework with custom infrastructure as a refactor.
