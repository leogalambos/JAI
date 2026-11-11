/** Explicit first-use integration against the real pinned upstream archive; run separately from offline tests. */
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtemp, mkdir, copyFile, readFile, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { resolve, join } from 'node:path';
import { spawnSync } from 'node:child_process';
const desktop = resolve(import.meta.dirname, '../..');
test('real pinned archive download applies the patch and creates a reusable offline source cache', async () => {
  const fixture = await mkdtemp(join(tmpdir(), 'jai-sdk-download-')); const recipe = join(fixture, 'vendor/sigma');
  try {
    await mkdir(join(fixture, 'tools')); await mkdir(recipe, { recursive: true });
    await copyFile(join(desktop, 'tools/prepare-sigma.mjs'), join(fixture, 'tools/prepare-sigma.mjs'));
    for (const name of ['provenance.json', 'label-programs.patch']) await copyFile(join(desktop, 'vendor/sigma', name), join(recipe, name));
    const prepared = spawnSync(process.execPath, [join(fixture, 'tools/prepare-sigma.mjs')], { encoding: 'utf8', timeout: 65000 });
    assert.equal(prepared.status, 0, prepared.stderr); assert.match(prepared.stdout, /source hashes verified/);
    const marker = await readFile(join(recipe, '.cache/upstream/.jai-prepared.json'), 'utf8');
    const cached = spawnSync(process.execPath, [join(fixture, 'tools/prepare-sigma.mjs'), '--offline'], { encoding: 'utf8' });
    assert.equal(cached.status, 0, cached.stderr); assert.match(cached.stdout, /reusing prepared source cache/); assert.equal(await readFile(join(recipe, '.cache/upstream/.jai-prepared.json'), 'utf8'), marker);
  } finally { await rm(fixture, { recursive: true, force: true }); }
});
