# {{Flow/change}} verification

Date: {{date/time and timezone}}

Owner: {{responsible verifier}}

Scope: {{behavior and entry points}}
Status: {{verified within stated scope / pending / failed}}

## Revision and environment

{{Source revision/artifact hash, local changes, runtime identity, relevant versions, production-equivalent properties and known differences. No credentials or private endpoints.}}

## Synthetic setup and ownership

{{Clearly synthetic identities/data, isolated providers, run identifier and ownership method.}}

| Resource type | Non-sensitive identifier/reference | Owner/run | Cleanup method |
|---|---|---|---|
| {{process/schema/file/account/etc.}} | {{reference}} | {{run}} | {{method}} |

## Reproduction or baseline

{{Expected vs observed before the change; exact safe steps; regression failing for the original defect. If unavailable, explain rather than invent.}}

## Replay after change

| Case/entry point | Steps and input | Expected | Observed and durable state | Status |
|---|---|---|---|---|
| {{case}} | {{synthetic steps}} | {{expected}} | {{result/effects}} | {{status}} |

## Failure, isolation and retry

{{Applicable cases: denied/revoked permission, another tenant, input error, duplicate, concurrency, dependency failure, accepted effect with lost response, retry, recovery and no duplicate effects.}}

## Automated checks

| Actual command/check | Environment | Result/counts | Scope/limits |
|---|---|---|---|
| {{command}} | {{environment}} | {{actual}} | {{limits}} |

## External execution versus simulation

{{Separate real sandbox exercises from deterministic simulations. List limitations of provider/device/environment access.}}

## Cleanup verification

| Owned resource | Removal outcome | Independent absence check | Remaining action |
|---|---|---|---|
| {{resource}} | {{outcome}} | {{check}} | {{none or action}} |

{{Do not delete resources with unproven ownership. Cleanup failures remain visible.}}

## Remaining gaps

| Unexecuted/blocked/failed case | Impact | Owner | Next evidence required |
|---|---|---|---|
| {{gap or none}} | {{impact}} | {{owner}} | {{closure}} |

## Evidence handling

{{Sanitized summaries/references only. No raw logs, tokens, cookies, environment files, database dumps or private captures. Conclusions apply only to the revision, environment and cases above.}}
