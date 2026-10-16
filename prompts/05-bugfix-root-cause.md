# 05 · Fix a demonstrated root cause

## Bug
{{Observed behavior, expected behavior, affected users/surfaces, sanitized evidence}}

## Preconditions
Read rules/profile, relevant callers and existing evidence. Use the project's branch/base policy; preserve unrelated work. Operate only on synthetic, isolated resources and never read operational credentials or customer data for fixtures.

## Procedure
1. Map the symptom, candidate cause and every entry point reaching the affected logic.
2. Reproduce with synthetic input or controlled fault injection. If reproduction is unavailable, report the limitation without calling the cause demonstrated.
3. Add a regression and run it on the unfixed version; it must fail because of the original defect.
4. Correct the cause at the responsible boundary. Inspect sibling paths for the same defect and handle them within scope or report them.
5. Run the focused regression and mandatory checks; broaden according to impact, not repetition for its own sake.
6. Replay the affected flow through its real lab entry point, including relevant denial, timeout, retry, duplicate and partial-failure paths. Verify observable result, durable state and side effects.
7. Record revision, setup, expected/actual results, tests and pending evidence using [the verification template](../templates/verification-record.template.md).
8. Teardown only owned resources and verify their absence.

## Deliver
Cause, fix, fail-before/pass-after evidence, real-flow replay, cleanup and gaps. A healthy endpoint or green suite alone does not close the defect. Do not weaken assertions, suppress failures as success or hide violations in exclusions.
