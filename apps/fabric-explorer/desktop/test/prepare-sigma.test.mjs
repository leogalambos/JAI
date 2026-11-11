/** Actual prepared-cache API and isolated offline failure behavior; no product source mutation. */
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtemp, mkdir, copyFile, writeFile, readFile, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { resolve, join } from 'node:path';
import { spawnSync } from 'node:child_process';
import { prepareSigma } from '../tools/prepare-sigma.mjs';
const desktop = resolve(import.meta.dirname, '..');
test('prepareSigma reuses the established same-pin cache with and without explicit offline mode', async () => {
  const a = await prepareSigma({ offline: true }); const before = await readFile(join(a, '.jai-prepared.json'));
  assert.equal(await prepareSigma(), a); assert.deepEqual(await readFile(join(a, '.jai-prepared.json')), before);
});
test('offline preparation rejects missing and mismatched caches without modifying them', async () => {
  const fixture = await mkdtemp(join(tmpdir(), 'jai-sdk-prepare-')); const tools = join(fixture, 'tools'); const recipe = join(fixture, 'vendor/sigma');
  try {
    await mkdir(tools); await mkdir(recipe, { recursive: true });
    await copyFile(join(desktop, 'tools/prepare-sigma.mjs'), join(tools, 'prepare-sigma.mjs'));
    for (const name of ['provenance.json', 'label-programs.patch']) await copyFile(join(desktop, 'vendor/sigma', name), join(recipe, name));
    const missing = spawnSync(process.execPath, [join(tools, 'prepare-sigma.mjs'), '--offline'], { encoding: 'utf8' });
    assert.notEqual(missing.status, 0); assert.match(missing.stderr, /source cache is missing/);
    await mkdir(join(recipe, '.cache/upstream'), { recursive: true }); const marker = '{"format":"jai.sigma-prepared/1","pin":"wrong"}\n'; await writeFile(join(recipe, '.cache/upstream/.jai-prepared.json'), marker);
    const mismatched = spawnSync(process.execPath, [join(tools, 'prepare-sigma.mjs'), '--offline'], { encoding: 'utf8' });
    assert.notEqual(mismatched.status, 0); assert.match(mismatched.stderr, /cache differs/); assert.equal(await readFile(join(recipe, '.cache/upstream/.jai-prepared.json'), 'utf8'), marker);
  } finally { await rm(fixture, { recursive: true, force: true }); }
});
