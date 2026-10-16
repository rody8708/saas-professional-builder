# 11 · Synchronize documentation and prepare review

## Request
Prepare {{change}} for review/publication within the user's authorization.

## Documentation
From the final diff, identify changes to behavior, setup, architecture, APIs, modules, privacy, testing, operations and user workflows. Update the owning documentation in the project's agreed languages. Describe implemented behavior; label proposals and pending controls.

Use [verification-record.template.md](../templates/verification-record.template.md) for meaningful functional evidence. Include revision/environment, commands actually run, real counts, acceptance results and explicit gaps. Explain when documentation is unaffected.

## Hygiene
Inspect the exact file list and complete staged diff before commit/push. Run the project's secret/private-data checks; confirm operational configuration, customer data, logs, databases and backups are excluded. Verify cleanup of owned test resources, including ignored/external ones.

Validate the intended repository, visibility, base branch and coherent scope before publication. Preserve unrelated work and follow the project's branch policy. If publication is already authorized, complete it after the concrete reviewable work and checks; do not add a redundant approval request.

## Review description
Use [PULL_REQUEST_TEMPLATE.md](../templates/PULL_REQUEST_TEMPLATE.md): problem and resulting behavior, scope, verification, migration/compatibility, deployment/recovery, privacy/security impact and material gaps. Check boxes only with evidence; no universal production-readiness claim.

## Deliver
Docs/hygiene summary and the final review description. Report publication outcome only if it actually happened; otherwise state the prepared artifact and any required unresolved gate.
