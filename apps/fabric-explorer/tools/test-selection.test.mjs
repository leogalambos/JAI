// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Selection contract tests use the real maintained manifest and local dependency graph. */
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { inventory, selectTests, preparationCommands } from './test-selection.mjs';
const prefix = 'apps/fabric-explorer/';
test('all maintained native tests have explicit levels and full selection preserves every entry', () => {
  const rows = inventory(); assert.ok(rows.length > 100); assert.deepEqual(selectTests(), rows);
  assert.ok(rows.some(row => row.path.endsWith('test/integration/prepare-sigma.test.mjs')));
  assert.ok(rows.some(row => row.path.endsWith('test/manifest.test.ts')));
});
test('control selects contracts and collaboration without e2e qualification', () => {
  const rows = selectTests({ profile: 'control' }); assert.ok(rows.length > 5);
  assert.ok(rows.every(row => row.tags.includes('control') && !row.tags.includes('e2e')));
  for (const name of ['desktop', 'contracts', 'packaging']) assert.ok(rows.some(row => row.package === name));
});
test('category union is intersected with a package filter', () => {
  const rows = selectTests({ category: ['contract', 'security'], package: 'packaging' });
  assert.ok(rows.length); assert.ok(rows.every(row => row.package === 'packaging' && row.tags.some(tag => ['contract', 'security'].includes(tag))));
});
test('development uses transitive dependencies, direct tests and contract consumers', () => {
  const rows = selectTests({ profile: 'development', changed: [`${prefix}desktop/src/layout/wire.ts`] });
  assert.ok(rows.some(row => row.path.endsWith('layout-wire.test.ts')));
  assert.ok(rows.length < inventory().length);
  const direct = `${prefix}desktop/test/theme.test.ts`;
  assert.deepEqual(selectTests({ profile: 'development', changed: [direct] }).map(row => row.path), [direct]);
  assert.ok(selectTests({ profile: 'development', changed: [`${prefix}packages/contracts/src/index.ts`] }).some(row => row.package === 'desktop'));
});
test('deleted inputs and package configuration conservatively select a package', () => {
  for (const path of [`${prefix}desktop/src/deleted.ts`, `${prefix}desktop/package.json`]) {
    assert.deepEqual(selectTests({ profile: 'development', changed: [path] }), inventory().filter(row => row.package === 'desktop'));
  }
});
test('known unrelated inputs select nothing; unknown inputs broaden verification', () => {
  assert.deepEqual(selectTests({ profile: 'development', changed: ['tests/test_repository.py'] }), []);
  assert.deepEqual(selectTests({ profile: 'development', changed: ['unknown/resource'] }), inventory());
  assert.deepEqual(selectTests({ profile: 'development', changed: [`${prefix}tools/test-selection.mjs`] }), inventory());
});
test('invalid and empty development requests fail instead of claiming success', () => {
  for (const options of [{ profile: 'development' }, { profile: 'typo' }, { category: ['typo'] }, { package: 'typo' }]) assert.throws(() => selectTests(options));
  const child = spawnSync(process.execPath, [new URL('./test-selection.mjs', import.meta.url).pathname, '--category', 'typo'], { encoding: 'utf8' });
  assert.equal(child.status, 2); assert.match(child.stderr, /Unknown native/);
});
test('unmapped scripts, documentation and Python runtime changes broaden native coverage', () => {
  for (const path of ['scripts/new_generator.py', 'docs/unknown.md', '.ai/runtime/tools/findings.py']) assert.deepEqual(selectTests({ profile: 'development', changed: [path] }), inventory());
});

test('a valid but empty category intersection fails explicitly', () => {
  assert.throws(() => selectTests({ package: 'contracts', category: ['e2e'] }), /No native tests/);
});
test('compiled worker consumers are additive to static source dependencies', () => {
  for (const name of ['direct-import', 'model']) {
    const rows = selectTests({ profile: 'development', changed: [`${prefix}desktop/src/import/${name}.ts`] });
    for (const consumer of ['explore-integration', 'import-worker-ownership']) assert.ok(rows.some(row => row.path.endsWith(`${consumer}.test.ts`)), `${name} must select ${consumer}`);
  }
});

test('compiled consumers rebuild current contracts and exact bundles without cleaning other assets', () => {
  const rows = inventory(); const worker = rows.filter(row => row.path.endsWith('explore-integration.test.ts'));
  assert.deepEqual(preparationCommands('desktop', worker), [['npm', 'run', 'build:contracts'], [process.execPath, 'tools/build.mjs', '--test-assets']]);
  assert.equal(preparationCommands('desktop', rows)[1][2], '--test-performance-assets');
  assert.deepEqual(preparationCommands('desktop', rows.filter(row => !row.assets?.length)), [['npm', 'run', 'build:contracts'], ['npm', 'run', 'build:sdk']]);
  assert.deepEqual(preparationCommands('contracts', rows), [['npm', 'run', 'generate']]);
  assert.deepEqual(preparationCommands('packaging', rows), []);
});
