# .NET / C# profile

This profile supplies an executable architecture source guard and isolated regression tests. It is a starting point for an agreed ASP.NET Core architecture, not a SaaS application, authentication implementation, compliance certification or proof that a destination project's gates pass.

Read the shared product rules first. Retain the destination's framework, database, locales, account lifecycle and existing architectural decisions. The example configuration uses separate `Domain` and `Application` projects; adapt its paths and forbidden namespace/project names before adopting it. An existing single-project application needs an adapted control or a documented gap, not an automatic architectural rewrite.

## Supported tools and runtime

- The supplied control builds and runs on **.NET SDK/runtime 8**, with PowerShell 7 for the wrapper. [global.json](global.json) selects the latest installed .NET 8 feature band at or above 8.0.100. A machine with only SDK 9/10 must also install SDK 8 to reproduce this profile as supplied.
- Roslyn comes from the selected SDK's `Roslyn/bincore` directory. There are no NuGet package dependencies. [NuGet.Offline.Config](tools/NuGet.Offline.Config) clears package sources for this control only; no user/global configuration is changed.
- The destination SaaS may use another supported .NET version. Its real build, analyzers and tests must use its chosen SDK. The guard's syntax parser supports the C# syntax understood by the selected SDK 8 Roslyn; it does not certify newer language features.
- The package regression harness is a standalone executable, so `dotnet test` would not execute it. Use the commands below. Application tests should use an explicitly selected framework such as xUnit, NUnit or MSTest and their real test adapter; record the chosen versions and run the destination's `dotnet test` command.

## Run the supplied regression tests

From `profiles/dotnet`:

```powershell
pwsh -NoProfile -File ./tools/Invoke-Profile.ps1 -Mode Test
```

The wrapper builds [the control](tools/ArchitectureGuard/ArchitectureGuard.csproj) and [the regression executable](tests/ArchitectureGuard.Regression.csproj), then runs the latter. Build output, restore metadata, package cache and CLI home are placed in an owned system-temporary directory. Compiler/build-server reuse is disabled. The wrapper restores its process environment, checks the cleanup target and removes that temporary directory in `finally`.

Each scenario creates synthetic `.cs`, `.csproj` and JSON files under a distinct temporary directory and removes it in `finally`. No application is bootstrapped, no real `.env` or database is loaded, and no provider or network service is contacted. The CLI scenarios invoke the actual guard entry point and check its exit code.

## Apply the control to a project

1. Copy [architecture-guard.example.json](templates/architecture-guard.example.json) to the target repository root as `architecture-guard.json`.
2. Set the two source roots to the real Domain/Application project directories. Each requires C# source containing declarations/statements and at least one `.csproj`. Replace `Example.*` with actual namespace prefixes and review the forbidden project-name fragments and persistence libraries. An empty forbidden list is rejected. Configuration changes belong in code review; this control does not prevent someone from deliberately weakening its configuration.
3. Run the guard from the profile directory, supplying an absolute destination path:

```powershell
pwsh -NoProfile -File ./tools/Invoke-Profile.ps1 -Mode Check -ProjectRoot '/absolute/path/to/target-repository'
```

On Windows, pass a quoted path such as `D:\Projects\Example`. The guard reads configuration and C#/project source only and does not build or execute the destination application. It returns **0** for no findings, **1** for architecture/configuration findings, and **2** for invalid CLI usage or an inspection I/O failure. A wrapper build/prerequisite failure also produces a nonzero exit.

In CI, install/select the required .NET 8 SDK and PowerShell 7, then invoke the same wrapper command. Commit the reviewed destination configuration and preserve the command's exit code. This profile does not activate a workflow or configure required branch checks. Provider action versions and runner provisioning belong to the destination's delivery policy.

## What the supplied guard checks

- Missing/malformed configuration, missing source roots, no C# files, empty/comment-only source and missing layer project files fail closed. Source outside the declared repository and linked source/project paths are rejected.
- Roslyn parses source names and member expressions. Configured namespace prefixes are rejected in Domain/Application imports, type references, qualified expressions, namespace aliases, global aliases and relevant enclosing namespace contexts. Comments and string contents are not treated as dependency code; expressions inside interpolated strings are inspected.
- Literal `ProjectReference` edges are inspected transitively. Forbidden project-name fragments and assembly/root-namespace identities produce findings. Literal `PackageReference`, `FrameworkReference` and assembly `Reference` identifiers are checked against the namespace-prefix rules.
- Missing project references, dynamic/wildcard identifiers, malformed project XML and XML DTDs fail closed. Project conditions are conservatively inspected regardless of whether a particular build would activate them.
- `bin`, `obj` and `.git` directories are excluded. Syntax errors and inactive conditional source are explicit findings, not silently accepted source.

The implementation is in [ArchitectureScanner.cs](tools/ArchitectureGuard/ArchitectureScanner.cs); [regressions](tests/Program.cs) cover permitted and forbidden cases, CLI behavior and cleanup.

## Limits of this control

This is **syntax and literal project-reference inspection**, not a Roslyn semantic analyzer or an evaluated MSBuild dependency graph. Namespace/type ambiguity can produce findings requiring review. It does not resolve reflection, dynamic dispatch, runtime service registration, generated code, dependencies introduced by imported `.props`/`.targets`, transitive NuGet packages, or global usings declared outside the configured layer roots. Full build/type-aware architecture analysis and review are still required. A zero exit code proves only the configured checks over the inspected source.

The guard intentionally reports inactive preprocessor code as unresolved; it cannot certify every symbol/build configuration. Projects using conditional implementations need an additional build-aware control before treating that architecture coverage as complete. Do not suppress the finding and claim the omitted code was checked.

It does not inspect tenant ownership, authorization, transactions, retry behavior, SQL correctness, authentication security or legal policies. The matrix below remains mandatory project verification; listing a gate does not implement it.

## ASP.NET Core implementation guidance

Use ASP.NET Core's real routing, dependency injection, configuration, logging and authorization mechanisms. ASP.NET endpoints/controllers and EF Core `DbContext`, mappings and migrations belong in outer API/Infrastructure/Persistence projects. Application coordinates use cases through agreed ports; Domain stays independent of transport and persistence. Using EF Core outside Domain/Application is permitted by the supplied control. Avoid loading an implicit tenant into a singleton or static mutable field.

Use maintained identity components or the chosen identity provider, for example ASP.NET Core Identity and established OpenID Connect/OAuth middleware. Do not invent password hashing, token formats, session handling or cryptography. Define cookie/CSRF versus Bearer-only authentication per route, validate provider callbacks and test the actual account lifecycle. An identity library does not replace business authorization or tenant membership checks.

Use the production database engine for transactional, constraint, migration and concurrency integration tests. EF Core's in-memory provider or SQLite cannot establish another engine's locking/DDL behavior. Query filters can add defense but are not sufficient authorization: validate membership and resource ownership, cover raw SQL/filter bypasses, and enforce appropriate database keys/constraints. Use isolated temporary databases/containers with synthetic identities and verified teardown.

## Required destination project gates

| Gate | Required evidence | Supplied here |
|---|---|---|
| `architecture` | Build/analyzers plus agreed dependency boundaries across the actual source and build configurations | Bounded syntax/literal-reference guard and its regressions only |
| `tenant-isolation` | Two-tenant negative reads/writes, exports/jobs, stale membership, cache/context switching and database constraints | Guidance; destination tests required |
| `authorization` | Resource/capability decisions at the use-case boundary, denied operations and actual route authentication/CSRF modes | Guidance; destination tests required |
| `data-integrity` | Real-engine migrations, rollback/recovery, transactions, optimistic/row concurrency and constraint failures | Guidance; destination tests required |
| `retry-safety` | Durable operation identity, stable payload/key, duplicate delivery, unknown outcomes and outbox/reconciliation behavior where needed | Guidance; destination tests required |
| `real-entrypoint` | Actual HTTPS/API/worker flow with synthetic inputs; verify response, persisted state and relevant failure/retry results | Guidance; destination functional evidence required |
| `operations` | Production configuration validation, safe telemetry, readiness, scheduler/workers, backup restore and recovery objectives | Guidance; destination operational evidence required |

For payments, preserve a durable operation and its idempotency key across unknown provider outcomes; retry policies such as transient HTTP/EF retries must not silently duplicate side effects. Use a provider adapter and test sandbox/reconciliation flows in the destination. For operation, redact sensitive data, propagate cancellation appropriately, and verify recovery rather than inferring it from a healthy endpoint.

## Validation record

The profile manifest records the actual local execution and its limits in [profile.json](profile.json). `controls-validated` describes these supplied controls only; it is not a destination SaaS approval. GitHub CI, Linux execution and application/domain flows require separate evidence.
