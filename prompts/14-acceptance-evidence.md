# 14 · Prove a flow through its real entry point

## Target
{{Feature, defect or release}} at revision {{revision/artifact identifier}}.

## Setup
Read the project profile and [testing guidance](../core/testing-verification.md). Confirm the isolated runtime matches the intended source/artifact. Reproduce relevant production properties and use only synthetic identities/data and sandbox providers.

Register every resource created with a run identifier and owner: processes, ports, schemas, files, volumes, accounts, queues and mail. Never edit a generated release or disrupt another workload.

## Execute
1. Reproduce the defect if applicable; otherwise record that it could not be reproduced.
2. Run the actual entry point: browser/client, API, scheduler, queue consumer or signed provider delivery.
3. Compare expected/observed UI or protocol result and inspect persisted state, audit and external effects.
4. Test relevant invalid input, denied/revoked authority, other tenant, duplicate, dependency outage, timeout, retry and partial failure.
5. Verify mode-appropriate auth/CSRF/signatures, safe errors and data isolation.
6. Confirm recovery does not duplicate effects; distinguish actual external execution from controlled simulation.

## Record and clean up
Use [verification-record.template.md](../templates/verification-record.template.md). Include real commands/results/counts, environment/revision, limits, blocked checks and what closes each gap. Do not save raw credentials, logs, dumps or private captures.

Teardown owned resources even on failure and independently verify absence. Unclear ownership means do not delete; report the specific unresolved cleanup.

## Deliver
Acceptance status per case, sanitized evidence, cleanup and remaining gates. No check is passed unless executed and observed; a healthy endpoint or green suite does not replace the flow.
