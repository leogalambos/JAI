/** Real source compiler/public-export bootstrap and a disposable compiler-error negative. */
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtemp, mkdir, copyFile, writeFile, readFile, rm, symlink } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { resolve, join } from 'node:path';
import { spawnSync } from 'node:child_process';
import { buildSigma } from '../tools/build-sigma.mjs';
const desktop = resolve(import.meta.dirname, '..');
test('buildSigma compiles the prepared source into every declared JS and type entry', async () => {
  await buildSigma({ offline: true }); const manifest = JSON.parse(await readFile(join(desktop, 'vendor/sigma/package.json'), 'utf8'));
  for (const [name, entry] of Object.entries(manifest.exports)) if (name !== './package.json') for (const field of ['import', 'require', 'types']) assert.ok((await readFile(join(desktop, 'vendor/sigma', entry[field]))).length > 0);
});
test('a real compiler error rejects a disposable build instead of leaving a successful result', async () => {
  const fixture = await mkdtemp(join(tmpdir(), 'jai-sdk-type-error-')); const recipe = join(fixture, 'vendor/sigma');
  try {
    await mkdir(join(fixture, 'tools')); await mkdir(join(recipe, '.cache/upstream/src'), { recursive: true });
    await symlink(join(desktop, 'node_modules'), join(fixture, 'node_modules'), process.platform === 'win32' ? 'junction' : 'dir');
    for (const name of ['build-sigma.mjs', 'prepare-sigma.mjs']) await copyFile(join(desktop, 'tools', name), join(fixture, 'tools', name));
    for (const name of ['provenance.json', 'label-programs.patch', 'package.json', 'tsconfig.json']) await copyFile(join(desktop, 'vendor/sigma', name), join(recipe, name));
    await copyFile(join(desktop, 'vendor/sigma/.cache/upstream/.jai-prepared.json'), join(recipe, '.cache/upstream/.jai-prepared.json'));
    await writeFile(join(recipe, '.cache/upstream/package.json'), '{"type":"module"}\n'); await writeFile(join(recipe, '.cache/upstream/tsconfig.json'), '{}\n');
    await writeFile(join(recipe, '.cache/upstream/src/index.ts'), 'const invalid: number = "deliberate type error";\n');
    const result = spawnSync(process.execPath, [join(fixture, 'tools/build-sigma.mjs'), '--offline'], { encoding: 'utf8' });
    assert.notEqual(result.status, 0); assert.match(result.stdout, /TS2322/); assert.match(result.stderr, /declaration\/type build failed/);
  } finally { await rm(fixture, { recursive: true, force: true }); }
});
