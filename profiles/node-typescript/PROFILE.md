# Node.js / TypeScript profile

Status: **profile controls validated**. This profile supplies a bounded dependency checker and its regression tests. It does not supply a SaaS application, authentication, migrations, an ORM, deployment, or a certified TypeScript architecture.

## Structure and framework adaptation

Use `src/domain` for entities, value objects and ports, and `src/application` for use cases and orchestration through those ports. Keep SQL clients, payment SDKs, queues and persistence adapters in `src/infrastructure`. Put HTTP handlers, framework request types and serializers in `src/presentation`. Wire concrete dependencies in a composition root outside the inner layers.

For Express or Fastify, handlers adapt HTTP to application DTOs. For NestJS, keep framework decorators and injectable adapter wiring outside the pure domain/application packages. For Next.js, route handlers and server actions are entry-point adapters; a server-only file is not automatically authorized or tenant-isolated. UI JSX/TSX belongs outside the two guarded roots. Choose and lock the framework and package versions in the actual project; none is installed by this profile.

## Executable controls supplied

- `templates/architecture-guard.mjs`: standard-library CLI that reads source text without executing or importing the application.
- `templates/architecture-policy.json`: explicit roots, import aliases, forbidden internal paths, and forbidden persistence/transport packages for both inner layers. Adapt aliases to the project's real module resolution and review policy changes.
- `tests/architecture-guard.test.mjs`: subprocess tests against temporary synthetic projects. No network, database, application bootstrap or `.env` access. Teardown removes each owned fixture in `finally`.

The checker requires both roots to exist and contain supported source files. It rejects source symlinks and malformed policy paths. It inspects static ES imports, type-only imports/reexports, side-effect imports, literal `require`, `module.require`, `require.resolve`, and dynamic `import` calls. Recognized loaders with nonliteral targets fail closed. Relative paths and explicitly configured aliases are checked against forbidden paths. Alias keys are prefixes without trailing `/` or `*` (for example `@domain`, not `@domain/*`). Absolute path and URL imports fail closed; configured `node:` builtins are checked as packages. Package prefixes are matched at `/` boundaries. Comments, quoted strings, template text and ordinary regex literals are ignored; code inside template interpolations is visited. JSX in inner layers fails with an explicit unsupported-syntax error.

The lexer supports `.ts`, `.mts`, `.cts`, `.js`, `.mjs` and `.cjs`; it excludes `node_modules`, `vendor`, `.git`, `dist` and `build`. Exit codes are `0` for the configured lexical checks passing, `1` for a dependency violation, and `2` when inspection cannot complete. A zero result is not a type check or runtime acceptance result.

## Reproduce the profile validation

From this repository root, with Node.js 24 available:

```sh
node --test profiles/node-typescript/tests/architecture-guard.test.mjs
```

Validated on Windows with Node.js v24.16.0: **28 tests passed, zero failures/skips**. The tests exercise successful imports and real rejected CLI executions: missing/empty roots, forbidden cross-layer imports, aliases, package subpaths, type-only dependencies, dynamic loaders, escaped module names, comments/strings, template interpolation, malformed policies and unsupported JSX. All fixtures are removed after each test.

To adopt, copy the two template files into the project's `tools/` and root policy location, adapt the policy, and run:

```sh
node tools/architecture-guard.mjs --project-root . --config architecture-policy.json
```

The checked roots must contain real source files. Do not weaken the policy or add empty placeholders merely to make a new project green.

## Required TypeScript and dependency gates

This lexer is not a TypeScript parser or resolver. Regex-versus-division classification is contextual and incomplete; loader shadowing may produce false positives. It does not resolve aliases absent from the policy, package `exports`, transitive dependencies, arbitrary loader aliases, computed module access, `eval`, generated code, or architecture violations without imports. The configured forbidden-package list is finite; an unknown package is not automatically safe. These limitations must remain visible in project evidence.

Every adopting TypeScript project must separately configure and pass the compiler, plus a resolver-aware dependency rule using the actual `tsconfig` aliases and package boundaries. For a locked, locally installed TypeScript dependency, the compiler command is:

```sh
node node_modules/typescript/bin/tsc --noEmit --project tsconfig.json
```

This profile does not supply or claim to have run that project's `tsconfig`, framework build, lint configuration or dependency-rule configuration. JavaScript-only adoption still needs a parser/resolver-aware lint or dependency check. Do not replace those gates with the supplied lexer.

## Project acceptance gates

| Gate | Evidence required from the adopting SaaS |
| --- | --- |
| Architecture | Configured guard, real compiler/build and resolver-aware dependency checks; port/adaptor boundaries reviewed. |
| Tenant isolation | Cross-tenant negative tests through routes/jobs and persisted-state assertions against the chosen production database engine. |
| Authorization | Denied actions, membership changes/revocation, object-level ownership and authenticated entry-point tests. |
| Data integrity | Actual migrations, rollback or documented irreversibility, constraints, transaction boundaries and concurrent writes. |
| Retry safety | Duplicate submissions/webhooks, idempotency keys, dependency failures and retry races without duplicate effects. |
| Real entry point | HTTP/browser/worker replay in the required environment, checked outcome and stored state; provider sandbox for payments. |
| Operations | Validated config, secret isolation, scheduler/queue recovery, alerts, backup restore drill and cleanup evidence. |

Use unit tests for business behavior, database integration tests with isolated synthetic data, and real entry-point acceptance independently of the controls here. Payment/authentication flows require their own implemented providers, negative tests and sandbox evidence. Set project-specific coverage thresholds and obtain coverage from the project's actual test runner; this profile ships no coverage-report parser or threshold gate and makes no product coverage claim. No active CI workflow is included: integrate the commands only after dependencies, policy and the remaining gates exist, with sanitized evidence for every unexecuted check.
