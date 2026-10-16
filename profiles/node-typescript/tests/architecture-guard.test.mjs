import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import test from 'node:test';

const profile = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const guard = path.join(profile, 'templates/architecture-guard.mjs');
const policyFile = path.join(profile, 'templates/architecture-policy.json');

function runGuard(files = {}, options = {}) {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'saas-node-guard-'));
  try {
    const fixtures = {
      'src/domain/entity.ts': 'export interface Entity { readonly id: string; }\n',
      'src/application/use-case.ts': 'import type { Entity } from "../domain/entity.js";\nexport type Result = Entity;\n',
      ...files,
    };
    for (const [relative, source] of Object.entries(fixtures)) {
      if (options.missing && relative.startsWith(options.missing)) continue;
      const file = path.join(root, relative);
      fs.mkdirSync(path.dirname(file), { recursive: true });
      fs.writeFileSync(file, source);
    }
    const policy = JSON.parse(fs.readFileSync(policyFile, 'utf8'));
    options.mutate?.(policy, root);
    const config = path.join(root, 'architecture-policy.json');
    fs.writeFileSync(config, JSON.stringify(policy));
    const result = spawnSync(process.execPath, [guard, '--project-root', root, '--config', config], { cwd: root, encoding: 'utf8', timeout: 20_000 });
    assert.equal(result.error, undefined, result.error?.message);
    return result;
  } finally {
    const owned = path.resolve(root);
    assert.equal(path.dirname(owned), path.resolve(os.tmpdir()));
    assert.ok(path.basename(owned).startsWith('saas-node-guard-'));
    fs.rmSync(owned, { recursive: true, force: true });
    assert.equal(fs.existsSync(owned), false, 'Synthetic fixture must be removed');
  }
}

function rejected(files, expected, code = 1) {
  const result = runGuard(files);
  assert.equal(result.status, code, result.stdout + result.stderr);
  assert.ok(result.stderr.includes(expected), result.stderr);
}

test('allowed relative and configured alias imports pass', () => {
  const result = runGuard({ 'src/application/alias.ts': 'import type { Entity } from "@domain/entity";\n' });
  assert.equal(result.status, 0, result.stderr);
  assert.match(result.stdout, /3 source files inspected/);
});

test('missing domain root fails closed', () => {
  const result = runGuard({}, { missing: 'src/domain/' });
  assert.equal(result.status, 2);
  assert.match(result.stderr, /required layer root is missing: domain/);
});

test('missing application root fails closed', () => {
  const result = runGuard({}, { missing: 'src/application/' });
  assert.equal(result.status, 2);
  assert.match(result.stderr, /required layer root is missing: application/);
});

test('empty source root fails closed', () => {
  const result = runGuard({}, { mutate: (policy, root) => fs.unlinkSync(path.join(root, 'src/domain/entity.ts')) });
  assert.equal(result.status, 2);
  assert.match(result.stderr, /no source files inspected/);
});

test('domain cannot import application', () => {
  rejected({ 'src/domain/bad.ts': 'import { run } from "../application/use-case.js";\n' }, '../application/use-case.js');
});

test('application cannot import infrastructure by relative path', () => {
  rejected({ 'src/application/bad.ts': 'import { Repo } from "../infrastructure/repo.js";\n' }, '../infrastructure/repo.js');
});

test('configured infrastructure alias cannot bypass the boundary', () => {
  rejected({ 'src/application/bad.ts': 'import type { Repo } from "@infrastructure/repo";\n' }, '@infrastructure/repo');
});

test('database package subpath imports fail', () => {
  rejected({ 'src/application/bad.ts': 'import { Client } from "pg/lib/client";\n' }, 'pg/lib/client');
});

test('transport package imports fail', () => {
  rejected({ 'src/domain/bad.ts': 'import { Request } from "express";\n' }, 'express');
});

test('type-only reexports cannot bypass the boundary', () => {
  rejected({ 'src/application/bad.ts': 'export type { PrismaClient } from "@prisma/client";\n' }, '@prisma/client');
});

test('side-effect imports fail', () => {
  rejected({ 'src/application/bad.ts': 'import "node:http";\n' }, 'node:http');
});

test('literal require imports fail', () => {
  rejected({ 'src/application/bad.cts': 'const client = require("mysql2");\n' }, 'mysql2');
});

test('literal dynamic imports fail', () => {
  rejected({ 'src/application/bad.ts': 'const client = import("pg");\n' }, 'pg');
});

test('unresolved dynamic loaders fail closed', () => {
  rejected({ 'src/application/bad.ts': 'const client = import(configuredName);\n' }, 'unresolved-dynamic-import');
});

test('escaped package name cannot bypass package policy', () => {
  rejected({ 'src/application/bad.ts': 'import "\\u0070g";\n' }, 'pg');
});

test('comments strings template text and ordinary regex are not imports', () => {
  const source = '// import { Client } from "pg";\n/* require("mysql2"); */\n'
    + 'const example = "import(\\"pg\\")";\nconst text = `require("pg")`;\n'
    + 'const matcher = /import.*from "pg"/;\n';
  const result = runGuard({ 'src/domain/example.ts': source });
  assert.equal(result.status, 0, result.stderr);
});

test('real import inside template interpolation is inspected', () => {
  rejected({ 'src/application/bad.ts': 'const text = `${import("pg")}`;\n' }, 'pg');
});

test('no-interpolation template loader is resolved', () => {
  rejected({ 'src/application/bad.ts': 'const client = import(`mysql2`);\n' }, 'mysql2');
});

test('unterminated source comment fails closed', () => {
  rejected({ 'src/application/bad.ts': '/* unfinished\n' }, 'unterminated comment', 2);
});

test('incomplete policy fails closed', () => {
  const result = runGuard({}, { mutate: policy => delete policy.layers.domain });
  assert.equal(result.status, 2);
  assert.match(result.stderr, /must configure domain and application/);
});

test('policy root cannot escape the project', () => {
  const result = runGuard({}, { mutate: policy => { policy.roots.domain = '../outside'; } });
  assert.equal(result.status, 2);
  assert.match(result.stderr, /relative path/);
});

test('relative dependency cannot escape the project', () => {
  rejected({ 'src/application/bad.ts': 'import "../../../outside.js";\n' }, '../../../outside.js');
});

test('absolute path dependency cannot bypass configured relative roots', () => {
  rejected({ 'src/application/bad.ts': 'import "/outside/infrastructure/repository.js";\n' }, '/outside/infrastructure');
});

test('URL loader cannot bypass dependency policy', () => {
  rejected({ 'src/application/bad.ts': 'import("file:///outside/infrastructure/repository.js");\n' }, 'file:///');
});

test('wildcard alias configuration is rejected instead of silently ignored', () => {
  const result = runGuard({}, { mutate: policy => { policy.aliases['@/*'] = 'src'; } });
  assert.equal(result.status, 2);
  assert.match(result.stderr, /alias prefixes/);
});

test('package prefix does not match an unrelated package', () => {
  const result = runGuard({ 'src/domain/example.ts': 'import "pg-format-pure";\n' });
  assert.equal(result.status, 0, result.stderr);
});

test('third-party source directories are excluded', () => {
  const result = runGuard({ 'src/domain/node_modules/package/index.js': 'import "pg";\n' });
  assert.equal(result.status, 0, result.stderr);
  assert.match(result.stdout, /2 source files inspected/);
});

test('JSX in guarded inner layers requires moving it or a real parser', () => {
  rejected({ 'src/domain/view.tsx': 'export const view = <p>hello</p>;\n' }, 'JSX is not supported', 2);
});
