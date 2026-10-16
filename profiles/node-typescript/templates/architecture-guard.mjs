#!/usr/bin/env node
/** Bounded lexical dependency checks. Never imports or executes project modules. */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const extensions = new Set(['.ts', '.mts', '.cts', '.js', '.mjs', '.cjs']);
const excluded = new Set(['node_modules', 'vendor', '.git', 'dist', 'build']);

function fail(message) { throw new Error(message); }
function strings(value, name) {
  if (!Array.isArray(value) || value.some(item => typeof item !== 'string' || !item)) fail(`${name} must be a string array`);
  return value;
}
function within(root, candidate) {
  const relative = path.relative(root, candidate);
  return relative === '' || (!relative.startsWith(`..${path.sep}`) && relative !== '..' && !path.isAbsolute(relative));
}
function projectPath(root, relative, name) {
  if (typeof relative !== 'string' || !relative || path.isAbsolute(relative) || relative.split(/[\\/]/).includes('..')) fail(`${name} must be a relative path without '..'`);
  const result = path.resolve(root, relative);
  if (!within(root, result)) fail(`${name} escapes the project root`);
  let current = root;
  for (const part of relative.split(/[\\/]/)) {
    current = path.join(current, part);
    if (fs.existsSync(current) && fs.lstatSync(current).isSymbolicLink()) fail(`${name} traverses a symlink`);
  }
  return result;
}
function filesIn(directory) {
  const files = [];
  for (const entry of fs.readdirSync(directory, { withFileTypes: true }).sort((a, b) => a.name.localeCompare(b.name))) {
    if (excluded.has(entry.name)) continue;
    const file = path.join(directory, entry.name);
    if (entry.isSymbolicLink()) fail(`source symlink is not inspected: ${entry.name}`);
    if (entry.isDirectory()) files.push(...filesIn(file));
    else if (extensions.has(path.extname(entry.name))) files.push(file);
    else if (/\.[jt]sx$/.test(entry.name)) fail(`JSX is not supported in guarded inner layers: ${entry.name}`);
  }
  return files;
}

function decodeEscape(source, index) {
  const character = source[index];
  const simple = { n: '\n', r: '\r', t: '\t', b: '\b', f: '\f', v: '\v', '0': '\0' };
  if (character === '\n') return ['', index + 1];
  if (character === '\r') return ['', index + (source[index + 1] === '\n' ? 2 : 1)];
  if (character === 'u' || character === 'x') {
    const braced = character === 'u' && source[index + 1] === '{';
    const start = index + (braced ? 2 : 1);
    const end = braced ? source.indexOf('}', start) : start + (character === 'u' ? 4 : 2);
    const digits = source.slice(start, end);
    if (end < start || !/^[0-9a-f]+$/i.test(digits) || (!braced && digits.length !== (character === 'u' ? 4 : 2))) fail('invalid string escape');
    return [String.fromCodePoint(Number.parseInt(digits, 16)), end + (braced ? 1 : 0)];
  }
  if (/[1-9]/.test(character ?? '')) fail('legacy numeric string escapes require a parser');
  if (character === undefined) fail('unterminated string escape');
  return [simple[character] ?? character, index + 1];
}

/**
 * A lexer, not the TypeScript compiler. Skips comments, strings and ordinary
 * regex literals; visits template interpolations. Regex-vs-division classification
 * is contextual and incomplete. Use tsc and a resolver-aware dependency rule too.
 */
export function dependencies(source) {
  const tokens = [];
  let index = 0;
  let line = 1;
  function advance(end) { line += (source.slice(index, end).match(/\n/g) ?? []).length; index = end; }
  function token(kind, value, startLine = line) { tokens.push({ kind, value, line: startLine }); }
  function quoted(quote) {
    const startLine = line;
    advance(index + 1);
    let value = '';
    while (index < source.length) {
      if (source[index] === quote) { advance(index + 1); token('string', value, startLine); return; }
      if (source[index] === '\\') {
        const [decoded, end] = decodeEscape(source, index + 1);
        value += decoded; advance(end);
      } else {
        if (/\r|\n/.test(source[index])) fail('unescaped newline in quoted string');
        value += source[index]; advance(index + 1);
      }
    }
    fail('unterminated quoted string');
  }
  function template() {
    const startLine = line;
    const position = tokens.length;
    token('template', null, startLine);
    advance(index + 1);
    let value = '';
    let interpolated = false;
    while (index < source.length) {
      if (source[index] === '`') {
        advance(index + 1);
        if (!interpolated) tokens[position] = { kind: 'string', value, line: startLine };
        return;
      }
      if (source.startsWith('${', index)) { interpolated = true; advance(index + 2); segment(true); }
      else if (source[index] === '\\') { const [decoded, end] = decodeEscape(source, index + 1); value += decoded; advance(end); }
      else { value += source[index]; advance(index + 1); }
    }
    fail('unterminated template literal');
  }
  function regex() {
    advance(index + 1);
    let bracket = false;
    while (index < source.length) {
      if (source[index] === '\\') { advance(index + 2); continue; }
      if (/\r|\n/.test(source[index])) fail('unterminated regex literal');
      if (source[index] === '[') bracket = true;
      if (source[index] === ']') bracket = false;
      if (source[index] === '/' && !bracket) {
        advance(index + 1);
        while (/[a-z]/i.test(source[index] ?? '')) advance(index + 1);
        token('regex', null); return;
      }
      advance(index + 1);
    }
    fail('unterminated regex literal');
  }
  function segment(interpolation = false) {
    let braces = 0;
    while (index < source.length) {
      const character = source[index];
      if (/\s/.test(character)) { advance(index + 1); continue; }
      if (source.startsWith('//', index)) { const end = source.indexOf('\n', index); advance(end < 0 ? source.length : end); continue; }
      if (source.startsWith('/*', index)) { const end = source.indexOf('*/', index + 2); if (end < 0) fail('unterminated comment'); advance(end + 2); continue; }
      if (character === '"' || character === "'") { quoted(character); continue; }
      if (character === '`') { template(); continue; }
      if (interpolation && character === '}' && braces === 0) { advance(index + 1); return; }
      if (character === '{') braces++;
      if (character === '}') braces--;
      const previous = tokens.at(-1)?.value;
      if (character === '/' && (previous === undefined || ['=', '(', '[', '{', ',', ':', ';', '!', '?', 'return', 'throw', 'case', '=>'].includes(previous))) { regex(); continue; }
      if (/[A-Za-z_$]/.test(character)) {
        const start = index;
        const startLine = line;
        while (/[A-Za-z0-9_$]/.test(source[index] ?? '')) advance(index + 1);
        token('word', source.slice(start, index), startLine); continue;
      }
      const operator = ['=>', '?.'].find(value => source.startsWith(value, index));
      token('punctuation', operator ?? character); advance(index + (operator?.length ?? 1));
    }
    if (interpolation) fail('unterminated template interpolation');
  }
  segment();
  const found = [];
  function add(argument, at) {
    const next = tokens[argument + 1]?.value;
    const value = tokens[argument];
    found.push({ line: at.line, specifier: value?.kind === 'string' && [')', ','].includes(next) ? value.value : null });
  }
  for (let i = 0; i < tokens.length; i++) {
    const current = tokens[i];
    if (current.kind !== 'word') continue;
    const previous = tokens[i - 1]?.value;
    if (current.value === 'require' && (previous !== '.' || tokens[i - 2]?.value === 'module')) {
      if (tokens[i + 1]?.value === '(') add(i + 2, current);
      else if (tokens[i + 1]?.value === '.' && tokens[i + 2]?.value === 'resolve' && tokens[i + 3]?.value === '(') add(i + 4, current);
    }
    if (!['import', 'export'].includes(current.value) || ['.', '?.'].includes(previous)) continue;
    if (tokens[i + 1]?.value === '(') { if (current.value === 'import') add(i + 2, current); continue; }
    if (tokens[i + 1]?.value === '.') continue; // import.meta
    if (current.value === 'import' && tokens[i + 1]?.kind === 'string') {
      found.push({ line: current.line, specifier: tokens[i + 1].value }); continue;
    }
    for (let cursor = i + 1; cursor < tokens.length; cursor++) {
      if ([';', 'import', 'export', '='].includes(tokens[cursor].value)) break;
      if (tokens[cursor].value === 'from' && tokens[cursor + 1]?.kind === 'string') {
        found.push({ line: current.line, specifier: tokens[cursor + 1].value }); break;
      }
    }
  }
  return found;
}

export function inspect(root, policy) {
  if (!policy || typeof policy !== 'object' || !policy.roots || !policy.layers || !policy.aliases) fail('policy must configure roots, layers, aliases');
  if (Object.keys(policy.roots).sort().join(',') !== 'application,domain' || Object.keys(policy.layers).sort().join(',') !== 'application,domain') fail('roots and layers must configure domain and application');
  if (typeof policy.aliases !== 'object' || Array.isArray(policy.aliases)) fail('aliases must be an object');
  const aliases = Object.entries(policy.aliases).map(([alias, target]) => {
    if (!alias || alias.endsWith('/') || alias.includes('*')) fail('alias prefixes must be nonempty without trailing slash or wildcard');
    return [alias, projectPath(root, target, 'alias')];
  }).sort((a, b) => b[0].length - a[0].length);
  const violations = [];
  let inspected = 0;
  for (const layer of ['domain', 'application']) {
    const directory = projectPath(root, policy.roots[layer], `${layer} root`);
    if (!fs.existsSync(directory) || !fs.statSync(directory).isDirectory()) fail(`required layer root is missing: ${layer}`);
    const files = filesIn(directory);
    if (!files.length) fail(`no source files inspected in required layer: ${layer}`);
    const rules = policy.layers[layer];
    if (!rules || typeof rules !== 'object') fail(`invalid ${layer} policy`);
    const forbiddenPaths = strings(rules.forbidden_paths, `${layer}.forbidden_paths`).map(value => projectPath(root, value, 'forbidden path'));
    const forbiddenPackages = strings(rules.forbidden_packages, `${layer}.forbidden_packages`);
    for (const file of files) {
      inspected++;
      for (const dependency of dependencies(fs.readFileSync(file, 'utf8'))) {
        const specifier = dependency.specifier;
        let forbidden = specifier === null;
        if (specifier !== null) {
          // Absolute paths and URL loaders do not use this policy's relative /
          // package resolution. Reject them rather than treating them as packages.
          const unsupportedLocation = path.isAbsolute(specifier) || /^[a-z][a-z0-9+.-]*:/i.test(specifier) && !specifier.startsWith('node:');
          let resolved = specifier.startsWith('.') ? path.resolve(path.dirname(file), specifier) : null;
          for (const [alias, target] of aliases) {
            if (specifier === alias || specifier.startsWith(`${alias}/`)) { resolved = path.resolve(target, `.${specifier.slice(alias.length)}`); break; }
          }
          if (resolved) forbidden = unsupportedLocation || !within(root, resolved) || forbiddenPaths.some(boundary => within(boundary, resolved));
          else forbidden = unsupportedLocation || forbiddenPackages.some(prefix => specifier === prefix || specifier.startsWith(`${prefix}/`));
        }
        if (forbidden) violations.push(`${path.relative(root, file).split(path.sep).join('/')}:${dependency.line}: ${layer} imports forbidden/unresolved dependency ${specifier ?? '<unresolved-dynamic-import>'}`);
      }
    }
  }
  return { inspected, violations: [...new Set(violations)].sort() };
}

function main() {
  try {
    const args = process.argv.slice(2);
    if (args.length !== 4 || args[0] !== '--project-root' || args[2] !== '--config') fail('usage: node architecture-guard.mjs --project-root <directory> --config <policy.json>');
    const root = fs.realpathSync(args[1]);
    if (!fs.statSync(root).isDirectory()) fail('project-root must be a directory');
    const result = inspect(root, JSON.parse(fs.readFileSync(args[3], 'utf8')));
    if (result.violations.length) { console.error(result.violations.join('\n')); return 1; }
    console.log(`Architecture controls passed: ${result.inspected} source files inspected; configured lexical imports only.`);
    return 0;
  } catch (error) { console.error(`Architecture inspection failed: ${error.message}`); return 2; }
}
if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) process.exitCode = main();
