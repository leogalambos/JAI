/** Local dependency provenance: maintained source, reviewed patch, directory link and lock must agree. */
import { createHash } from 'node:crypto';
import { readFileSync, existsSync } from 'node:fs';
import { spawnSync } from 'node:child_process';
import { resolve } from 'node:path';
import { expect, it } from 'vitest';
const base = resolve(import.meta.dirname, '..');
const bytes = (file: string) => readFileSync(resolve(base, file));
const provenance = JSON.parse(bytes('vendor/sigma/provenance.json').toString());
it('binds the integration recipe to its upstream commit and reviewable patch', () => {
  expect(provenance.upstream.commit).toBe('617afb0508fc0fd8b60b208a04a83c49edf05a9f');
  expect(createHash('sha256').update(bytes('vendor/sigma/label-programs.patch')).digest('hex')).toBe(provenance.patchSha256);
});
it('uses a source-directory dependency and locked link without a generated archive', () => {
  const manifest = JSON.parse(bytes('vendor/sigma/package.json').toString());
  const desktop = JSON.parse(bytes('package.json').toString()); const lock = JSON.parse(bytes('package-lock.json').toString());
  expect(existsSync(resolve(base, 'vendor/sigma/src'))).toBe(false);
  expect(desktop.dependencies.sigma).toBe('file:vendor/sigma');
  expect(lock.packages['node_modules/sigma']).toMatchObject({ resolved: 'vendor/sigma', link: true });
  expect(lock.packages['vendor/sigma']).toMatchObject({ version: manifest.version, dependencies: manifest.dependencies });
  expect(lock.packages['node_modules/sigma']).not.toHaveProperty('integrity');
  expect(Object.keys(manifest.exports).sort()).toEqual(['.', './package.json', './primitives', './rendering', './settings', './types', './utils']);
  expect(manifest.files).not.toContain('src');
  for (const [name, entry] of Object.entries(manifest.exports)) {
    if (name === './package.json') continue;
    const exports = entry as { import: string; require: string; types: string };
    for (const file of [exports.import, exports.require, exports.types]) expect(bytes(`node_modules/sigma/${file}`).length).toBeGreaterThan(0);
  }
});


it('exports only integration metadata through the actual Git-independent release file selector', () => {
  const script = "import sys,json;from pathlib import Path;sys.path.insert(0,sys.argv[1]);import release_bundle;root=Path(sys.argv[2]);print(json.dumps(sorted(str(p.relative_to(root)) for p in release_bundle.files(root))))";
  const result = spawnSync(process.platform === 'win32' ? 'python' : 'python3', ['-I', '-B', '-c', script, resolve(base, '../../../.ai/runtime/tools'), resolve(base, 'vendor/sigma')], { encoding: 'utf8' });
  expect(result.status, result.stderr).toBe(0);
  expect(JSON.parse(result.stdout)).toEqual(['LICENSE.txt', 'README.md', 'label-programs.patch', 'package.json', 'provenance.json', 'tsconfig.json']);
});
