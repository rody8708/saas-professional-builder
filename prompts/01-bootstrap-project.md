# 01 · Bootstrap a professional SaaS

## Request
Create the authorized foundation for {{product, users, first valuable workflow}} in {{target directory/repository}}.

## Read and decide
Read existing project rules and [project adaptation](../core/project-adaptation.md). Select the agreed technical profile through the [profile registry](../profiles/registry.json); use its real framework conventions and tooling. Reuse confirmed requirements.

Record the relevant decisions with [the project profile](../templates/project-profile.template.md): stack, persistence, tenancy, identity, permissions, languages, clients, optional billing, data policy, CI, ownership and operational objectives. Ask only about unresolved choices that materially affect behavior or risk; continue independent authorized work.

## Implement
1. Preserve existing code and conventions. For a new product, choose the simplest deployment shape that meets the requirements; separate services only for a demonstrated need.
2. Add project governance and discoverable build/test commands from the selected profile. Do not invent or merely name checks that do not exist.
3. Implement one complete initial workflow with actual entry point, application rules, persistence, authentication/authorization where needed, and usable UI/API.
4. Enforce tenant boundaries in reads/writes and any jobs, caches or files used by that workflow.
5. Add meaningful unit/integration tests, synthetic infrastructure and ownership-based cleanup. Add architecture/dependency controls with explicitly bounded coverage.
6. Prepare a representative isolated acceptance environment and exercise success, denial, another tenant and relevant retry/failure cases.
7. Document setup, contracts, operations, evidence and next milestones. Billing, native clients and assistants are included only if requested.

## Deliver
Profile and decisions, implemented workflow, files changed, checks actually run, sanitized acceptance evidence, cleanup result and remaining milestones. Distinguish the delivered foundation from a complete production product. Publishing and deployment follow the user's authorization.
