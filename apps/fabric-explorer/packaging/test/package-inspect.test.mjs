/** Real temporary filesystem inspection of the fixed compiled application boundary. */
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtemp, mkdir, writeFile, rm, symlink, chmod } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join, dirname } from 'node:path';
import { APPLICATION_FILES, collectEntries, hashFile, inspectPackage } from '../inspect.mjs';
import { applicationPrefix } from '../manifest.ts';

async function fixture(run) {
  const root = await mkdtemp(join(tmpdir(), 'jai-package-inspect-'));
  try { await run(root); } finally { await rm(root, { recursive: true, force: true }); }
}
async function file(root, name, data = 'compiled fixture') {
  const path = join(root, name); await mkdir(dirname(path), { recursive: true }); await writeFile(path, data, { mode: 0o644 });
}
async function payload(root) {
  await file(root, 'runtime/electron'); await chmod(join(root, 'runtime/electron'), 0o755);
  const runtimeEntries = await collectEntries(join(root, 'runtime'));
  for (const name of [...APPLICATION_FILES, 'package.json']) await file(root, `${applicationPrefix('linux-x64')}/${name}`);
  await file(root, 'installer.cjs'); await file(root, 'notices/sbom.json', '{}'); await file(root, 'notices/third-party.txt');
  return { target: 'linux-x64', version: '0.1.0-test', runtimeEntries, noticePaths: ['notices/sbom.json', 'notices/third-party.txt'] };
}

test('hashFile records exact bytes including the empty boundary and rejects absent input', async () => fixture(async root => {
  await file(root, 'empty', '');
  assert.equal(await hashFile(join(root, 'empty')), 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855');
  await file(root, 'other', 'different'); assert.notEqual(await hashFile(join(root, 'empty')), await hashFile(join(root, 'other')));
  await assert.rejects(hashFile(join(root, 'absent')));
}));
test('collectEntries observes empty roots and preserves confined framework-style links', async () => fixture(async root => {
  assert.deepEqual(await collectEntries(root), []);
  await file(root, 'Framework/Versions/A/Resources/data');
  await symlink('A', join(root, 'Framework/Versions/Current'));
  await symlink('Versions/Current/Resources', join(root, 'Framework/Resources'));
  const entries = await collectEntries(root);
  assert.deepEqual(entries.find(entry => entry.path === 'Framework/Resources'), { path: 'Framework/Resources', kind: 'symlink', target: 'Versions/Current/Resources' });
}));
test('collectEntries rejects lexical escape, linked roots and special entries', async () => fixture(async root => {
  await symlink('../outside', join(root, 'escape'));
  await assert.rejects(collectEntries(root), /Invalid package metadata/);
  await rm(join(root, 'escape')); await symlink(root, join(root, 'alias'));
  await assert.rejects(collectEntries(join(root, 'alias')), /real directory/);
}));
test('inspectPackage admits only selected compiled assets and verified runtime bytes', async () => fixture(async root => {
  const options = await payload(root); const inventory = await inspectPackage(root, options);
  assert.equal(inventory.target, 'linux-x64');
  assert.equal(inventory.entries.filter(entry => entry.kind === 'file').length, 11);
  await file(root, `${applicationPrefix('linux-x64')}/source.ts`);
  await assert.rejects(inspectPackage(root, options), /Unselected package entry/);
}));
test('inspectPackage rejects missing outputs and post-verification runtime changes', async () => fixture(async root => {
  const options = await payload(root);
  await rm(join(root, 'installer.cjs')); await assert.rejects(inspectPackage(root, options), /Missing selected/);
  await file(root, 'installer.cjs'); await file(root, 'runtime/electron', 'modified');
  await assert.rejects(inspectPackage(root, options), /Runtime entry differs/);
}));
