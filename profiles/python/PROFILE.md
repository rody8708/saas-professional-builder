# Python profile

Status: **profile controls validated**. This profile supplies an AST dependency checker and isolated regression tests. It does not supply a SaaS application, framework configuration, authentication, migrations, production database integration or deployment.

## Structure and framework adaptation

The starter policy assumes a package at `src/example_saas`, with `domain`, `application`, `infrastructure` and `presentation` subpackages. Configure the real package name and source root before adoption. Domain contains entities, value objects and port contracts; application coordinates use cases through those ports. Persistence implementations, provider clients and task adapters belong in infrastructure; HTTP/request/response integration belongs in presentation. A composition root wires concrete dependencies.

For FastAPI or Flask, handlers and framework request/schema conversion stay outside domain/application. SQLAlchemy sessions and repositories belong in infrastructure; pass an application-owned transaction port into use cases. For Django, keep ORM models, views, management commands and framework-specific signals in outer adapters, with explicit mapping to domain models. This profile does not presume that a Django model is a domain entity. Configure the project's real migrations and transaction strategy instead of inferring correctness from package layout.

Choose locked project dependencies and a project-local environment. The profile scripts and tests themselves need only Python's standard library; they do not install frameworks or packages.

## Executable controls supplied

- `templates/architecture_guard.py`: parses Python source with `ast` without importing or executing application modules.
- `templates/architecture-policy.json`: required package/root, domain/application policies, forbidden internal layers and known persistence/transport import prefixes.
- `tests/test_architecture_guard.py`: `unittest` subprocess regressions in synthetic temporary projects; `TemporaryDirectory` teardown is checked after each run. No network, database or `.env` access.

Both guarded layer directories must exist and contain `.py` files. Invalid policy paths, source symlinks, empty scans, encoding errors and syntax errors fail closed. Static imports, `from` imports, nested relative imports and package `__init__` imports are checked. Known literal `__import__` and `importlib.import_module` calls are inspected, including common import aliases. Nonliteral targets and relative dynamic imports through those recognized loaders are rejected as unresolved. Python comments and string contents do not become import nodes.

The scanner excludes `__pycache__`, `.venv`, `venv`, `.git` and `vendor`. Exit codes are `0` for configured checks passing, `1` for forbidden/unresolved imports, and `2` when inspection cannot complete. It reads policy JSON and source text only; deployment configuration is not part of this control.

## Reproduce the profile validation

From this repository root:

```sh
python -B -m unittest discover -s profiles/python/tests -p "test_*.py" -v
```

Validated on Windows with Python 3.13.6: **18 tests passed, zero failures/skips**. Tests verify positive and negative subprocess exit codes, missing/empty roots, malformed policy, cross-layer persistence/transport dependencies, relative imports from nested modules and `__init__`, loader aliases, unresolved dynamic targets, syntax errors and comment/string handling. `-B` prevents bytecode artifacts in the source tree; temporary synthetic projects are removed.

To adopt, copy the guard to `tools/`, copy and adapt the policy at the project root, then run:

```sh
python -B tools/architecture_guard.py --project-root . --config architecture-policy.json
```

The package and directories must match the real project. Do not add empty placeholder source merely to satisfy a nonempty scan.

## Required companion checks and limits

This is AST syntax and configured direct-dependency analysis, not whole-program architecture enforcement. It does not resolve arbitrary reassignment of loader functions, `getattr`/`eval`/`exec`, import hooks, indirect façade/reexport dependencies, generated modules or monkey-patching. Common loader aliases are identified syntactically; shadowed names can require review. The forbidden external-module list is finite. Unknown libraries, custom persistence wrappers and unconfigured package boundaries require review and policy updates. `TYPE_CHECKING` imports are still architecture dependencies and are inspected.

Configure the actual project's linter, type checker and dependency-boundary tool with its Python version, source paths and supported frameworks. Run those tools against locked local dependencies. Syntax parsing by this script does not replace application tests, type checking, a build/package check, or a complete dependency graph. This profile does not claim those project tools have run.

## Project acceptance gates

| Gate | Evidence required from the adopting SaaS |
| --- | --- |
| Architecture | Configured AST guard, real project typing/lint/dependency checks and review of contracts/adapters. |
| Tenant isolation | Cross-tenant API/job/repository negative cases and stored-state checks on the selected production database engine. |
| Authorization | Unauthorized/forbidden operations, membership revocation, ownership and authentication flow tests. |
| Data integrity | Real migrations, rollback strategy, constraints, transaction handling and concurrency tests. |
| Retry safety | Duplicate webhooks/jobs/submissions, idempotency, partial failure and safe retries without duplicate effects. |
| Real entry point | Actual browser/HTTPS/worker replay, observable output and persisted state, synthetic data and payment-provider sandbox. |
| Operations | Configuration validation, scheduler recovery, alert delivery, secret boundaries, restored backups and verified cleanup. |

Business behavior belongs in unit tests; repositories/migrations require isolated integration tests against the supported engines; authentication and payments require their own provider and negative-flow evidence. Choose project-specific test coverage thresholds and the actual runner/report format. This profile ships no coverage parser and does not assert product coverage. No active CI is supplied: wire these controls and the required project gates only after their configurations and dependencies exist, and report unexecuted checks explicitly.
