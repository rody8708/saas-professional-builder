# 16 · Record an architecture decision

## Decision
{{Problem, constraints, alternatives and decision owner}}

## Procedure
1. Read the existing decision record and project profile. Separate facts, constraints, assumptions and preferences.
2. Use [ADR.template.md](../templates/ADR.template.md) in the project's actual decision directory and naming convention.
3. Record the concrete choice, affected ownership/contracts, alternatives and why they were rejected.
4. Include benefits, costs, operational/security/data consequences, compatibility/migration and recovery.
5. Specify evidence or an experiment that validates the decision, and guards/tests that can enforce its boundary.
6. State status and authority: proposed does not mean approved or implemented. Link the implementation/evidence when available.
7. Link from affected documentation. Supersede accepted decisions transparently rather than silently rewriting their history.

## Deliver
A concise decision record, connected docs and explicit follow-ups with owners. Do not implement a proposed choice merely because the ADR describes it.
