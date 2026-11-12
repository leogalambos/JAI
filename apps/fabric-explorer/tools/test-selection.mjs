// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Select maintained native tests by semantic category and source dependency impact.
 * Paths are repository relative. Unknown inputs conservatively select every native test.
 * Vendored SDK tests retain their separate explicit qualification command.
 */
import { existsSync, readFileSync, readdirSync } from 'node:fs';
import { dirname, resolve, relative, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '../../..');
const prefix = 'apps/fabric-explorer/';
const packages = { desktop: `${prefix}desktop`, contracts: `${prefix}packages/contracts`, packaging: `${prefix}packaging`, selection: `${prefix}tools` };
const assets = JSON.parse(readFileSync(resolve(root, prefix, 'test-categories.json'), 'utf8')).assets;
const categories = new Set(['unit', 'integration', 'contract', 'e2e', 'slow', 'security', 'performance', 'control']);

/** Read and validate the explicit file tags; reject missing, duplicate or unclassified tests.
 * @returns {Array<object>} Manifest entries with repository-relative paths and tags.
 * @throws {Error} When maintained test discovery and the manifest disagree.
 */
export function inventory() {
  const rows = JSON.parse(readFileSync(resolve(root, prefix, 'test-categories.json'), 'utf8')).tests;
  const paths = new Set();
  for (const row of rows) {
    if (paths.has(row.path) || !existsSync(resolve(root, row.path)) || !packages[row.package] || !['node', 'vitest'].includes(row.runner) || !row.tags?.length || row.tags.some(tag => !categories.has(tag)) || (row.assets || []).some(asset => !assets[asset])) throw new Error(`Invalid native classification: ${row.path}`);
    if (row.tags.filter(tag => ['unit', 'integration', 'contract', 'e2e'].includes(tag)).length !== 1) throw new Error(`Expected one test level: ${row.path}`);
    paths.add(row.path);
  }
  const walk = directory => readdirSync(directory, { withFileTypes: true }).flatMap(entry => entry.isDirectory() ? walk(join(directory, entry.name)) : [join(directory, entry.name)]);
  for (const [name, directory] of Object.entries(packages)) {
    const base = resolve(root, directory, name === 'selection' ? '.' : 'test');
    for (const file of walk(base).filter(path => /\.test\.(?:tsx?|mjs)$/.test(path))) {
      const path = relative(root, file).replaceAll('\\', '/');
      if (!paths.has(path)) throw new Error(`Unclassified native test: ${path}`);
    }
  }
  return rows;
}

function dependencies(path, seen = new Set()) {
  if (seen.has(path)) return seen;
  seen.add(path);
  const absolute = resolve(root, path);
  if (!existsSync(absolute)) return seen;
  const source = readFileSync(absolute, 'utf8');
  for (const asset of Object.values(assets)) {
    if (source.includes(asset.output)) dependencies(asset.source, seen);
  }
  for (const match of source.matchAll(/(?:from\s*|import\s*\(\s*|import\s*)['"](\.[^'"]+)['"]/g)) {
    const imported = resolve(dirname(absolute), match[1]);
    const candidates = [imported, imported.replace(/\.js$/, '.ts'), imported.replace(/\.js$/, '.tsx'), `${imported}.ts`, `${imported}.tsx`, join(imported, 'index.ts')];
    const found = candidates.find(candidate => existsSync(candidate) && /\.(?:tsx?|mjs|js|json)$/.test(candidate));
    if (found) dependencies(relative(root, found).replaceAll('\\', '/'), seen);
  }
  return seen;
}

/** Choose tests with OR category matching, then intersect an optional changed-input scope.
 * @param {object} options Profile, optional package, categories and repository-relative changed paths.
 * @param {string} options.profile Selection profile: full, control or development.
 * @param {string[]} options.category Optional categories combined with OR matching.
 * @param {string[]} options.changed Repository-relative changed input paths.
 * @param {string} options.package Optional package name limiting the selection.
 * @returns {Array<object>} Deterministically ordered selected manifest entries.
 * @throws {Error} For unknown filters or development selection without changed inputs.
 */
export function selectTests(options = {}) {
  const { profile = 'full', category = [], changed = [], package: packageName } = options;
  if (!['full', 'control', 'development'].includes(profile) || category.some(tag => !categories.has(tag)) || (packageName && !packages[packageName])) throw new Error('Unknown native test filter');
  if (profile === 'development' && !changed.length) throw new Error('Development selection requires --changed');
  let rows = inventory().filter(row => (!packageName || row.package === packageName) && (profile !== 'control' || row.tags.includes('control')) && (!category.length || category.some(tag => row.tags.includes(tag))));
  if (!rows.length) throw new Error('No native tests match the requested filters');
  if (!changed.length) return rows;
  const paths = changed.map(path => relative(root, resolve(root, path)).replaceAll('\\', '/'));
  const knownUnrelated = new Set(['tests/test_repository.py']);
  const unknown = paths.some(path => !path.startsWith(prefix) && !knownUnrelated.has(path));
  if (unknown || paths.some(path => path.startsWith(`${prefix}tools/`) || path === `${prefix}test-categories.json`)) return rows;
  const consumers = new Map();
  for (const path of paths.filter(path => /\.(?:tsx?|mjs|js)$/.test(path))) {
    consumers.set(path, new Set(inventory().filter(row => dependencies(row.path).has(path)).map(row => row.path)));
  }
  return rows.filter(row => paths.some(path => {
    if (path === row.path) return true;
    if (!path.startsWith(prefix)) return false;
    if (path.startsWith(`${prefix}packages/contracts/`) && row.package === 'desktop') return true;
    const base = packages[row.package];
    if (path.startsWith(`${base}/`)) {
      if (/\.(?:tsx?|mjs|js)$/.test(path) && existsSync(resolve(root, path)) && !path.includes('/tools/')) return consumers.get(path).size === 0 || consumers.get(path).has(row.path);
      return true;
    }
    // Reader, fixtures, shared selectors and qualification data cross package boundaries.
    return !Object.values(packages).some(directory => path.startsWith(`${directory}/`));
  }));
}

/** Return required package-local preparation commands for current selected source assets.
 * @param {string} packageName Native package being tested.
 * @param {Array<object>} rows Selected tests, including declared compiled-asset consumers.
 * @returns {Array<string[]>} Command and arguments in execution order; no commands are run here.
 */
export function preparationCommands(packageName, rows) {
  if (packageName === 'contracts') return [['npm', 'run', 'generate']];
  if (packageName !== 'desktop') return [];
  if (rows.some(row => row.assets?.length)) return [
    ['npm', 'run', 'build:contracts'],
    [process.execPath, 'tools/build.mjs', rows.some(row => row.assets?.includes('performance-native')) ? '--test-performance-assets' : '--test-assets'],
  ];
  return [['npm', 'run', 'build:contracts'], ['npm', 'run', 'build:sdk']];
}

function main(args) {
  const options = { category: [], changed: [] }; let list = false;
  for (let i = 0; i < args.length; i++) {
    const key = args[i];
    if (key === '--list') { list = true; continue; }
    if (!['--profile', '--category', '--changed', '--package'].includes(key) || !args[i + 1] || args[i + 1].startsWith('--')) throw new Error(`Invalid native test argument: ${key}`);
    const value = args[++i];
    if (key === '--category' || key === '--changed') options[key.slice(2)].push(value); else options[key.slice(2)] = value;
  }
  const rows = selectTests(options);
  if (!rows.length && !options.changed.length) throw new Error('No native tests match the requested filters');
  if (options.changed.length) {
    const unknown = options.changed.some(path => !path.startsWith(prefix) && path !== 'tests/test_repository.py');
    console.log(unknown ? 'Native impact: unknown input; conservative full native fallback within filters' : rows.length ? 'Native impact: dependency consumers and conservative package fallback' : 'Native impact: known unrelated inputs; no native tests required');
  }
  if (list) { for (const row of rows) console.log(`${row.path} [${row.tags.join(',')}]`); return; }
  console.log(`Native test selection: ${rows.length} files`);
  for (const packageName of Object.keys(packages)) {
    const selected = rows.filter(row => row.package === packageName);
    if (!selected.length) continue;
    const cwd = resolve(root, packages[packageName]);
    const run = (command, argv, directory = cwd) => {
      const result = spawnSync(command, argv, { cwd: directory, stdio: 'inherit' });
      if (result.error) throw result.error;
      if (result.status !== 0) process.exit(result.status || 1);
    };
    const vitest = selected.filter(row => row.runner === 'vitest');
    if (vitest.length) {
      for (const [command, ...argv] of preparationCommands(packageName, selected)) run(command, argv);
      run(process.execPath, [resolve(cwd, 'node_modules/vitest/vitest.mjs'), 'run', ...vitest.map(row => relative(cwd, resolve(root, row.path)))]);
    }
    const native = selected.filter(row => row.runner === 'node');
    if (native.length) run(process.execPath, ['--test', '--test-concurrency=1', ...native.map(row => resolve(root, row.path))], root);
  }
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  try { main(process.argv.slice(2)); } catch (error) { console.error(error.message); process.exitCode = 2; }
}
