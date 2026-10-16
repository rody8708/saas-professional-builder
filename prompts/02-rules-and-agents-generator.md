# 02 · Generate project governance

## Request
Create or update governance for {{project and scope}} using confirmed requirements.

## Procedure
1. Read existing rules and the project profile; select the technical profile through the [registry](../profiles/registry.json). Preserve established conventions and user instructions.
2. Use [RULES.template.md](../templates/RULES.template.md) and [AGENTS.template.md](../templates/AGENTS.template.md) as starting points, not files to overwrite blindly.
3. Define the project's actual architecture, ownership, tenant model, authentication modes, authorization, data handling, test levels, documentation duties and delivery gates.
4. List only real commands, paths and checks. Mark an unimplemented control pending with an owner instead of claiming it is enforced.
5. Keep stack commands in the project/profile-specific sections; shared rules describe guarantees.
6. Distinguish mandatory controls from recommendations. Every exception names reason, owner, scope, expiry/review condition and compensating verification.
7. Include scope discipline: review-only remains read-only; implementation does not imply deployment; respect permissions already granted.
8. Validate links, commands and consistency against the actual repository without modifying unrelated code.

## Deliver
Governance diff, decisions retained/changed, enforcement map and unresolved gates. Do not install dependencies, publish or implement features merely because the generated rules mention them.
