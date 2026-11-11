/** Deterministic binary-only package construction with real local archive tools. */
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtemp, mkdir, writeFile, readFile, rm, chmod, lstat, symlink } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join, dirname } from 'node:path';
import { execFileSync } from 'node:child_process';
import { runtimePin, inspectZip, prepareRuntime, publicSourceRevision, packageTarget } from '../package.mjs';
import { APPLICATION_FILES, collectEntries } from '../inspect.mjs';
import { parseManifest, sha256 } from '../manifest.ts';

async function fixture(run) {
  const root = await mkdtemp(join(tmpdir(), 'jai-package-build-'));
  try { await run(root); } finally { await rm(root, { recursive: true, force: true }); }
}
async function file(root, name, bytes = 'synthetic fixture') {
  const path = join(root, name); await mkdir(dirname(path), { recursive: true }); await writeFile(path, bytes, { mode: 0o644 }); return path;
}
async function inputs(root) {
  const runtimeRoot = join(root, 'runtime');
  await file(runtimeRoot, 'electron', 'synthetic executable fixture'); await chmod(join(runtimeRoot, 'electron'), 0o755);
  await file(runtimeRoot, 'Framework/Versions/A/data', 'framework fixture'); await symlink('A', join(runtimeRoot, 'Framework/Versions/Current'));
  await file(runtimeRoot, 'LICENSE', 'Synthetic runtime license fixture');
  await file(runtimeRoot, 'LICENSES.chromium.html', '<p>Synthetic runtime notices fixture</p>');
  const appRoot = join(root, 'compiled-app'); for (const name of APPLICATION_FILES) await file(appRoot, name, '// synthetic compiled fixture\n');
  const installerFile = await file(root, 'compiled-installer.cjs', '// synthetic compiled installer\n');
  return { target: 'linux-x64', version: '0.1.0-test', cacheRoot: join(root, 'cache'), appRoot, installerFile, development: true, preparedRuntime: { root: runtimeRoot, entries: await collectEntries(runtimeRoot), pin: runtimePin('linux-x64') }, sourceRevision: { commit: 'a'.repeat(40), dirty: true, closureSha256: 'b'.repeat(64) } };
}

test('runtimePin selects each exact target and rejects latest/prototype targets', () => {
  for (const target of ['linux-x64', 'linux-arm64', 'win32-x64', 'darwin-x64', 'darwin-arm64']) {
    const pin = runtimePin(target); assert.match(pin.sha256, /^[a-f0-9]{64}$/); assert.equal(pin.url, `https://github.com/electron/electron/releases/download/v45.2.3/electron-v45.2.3-${target}.zip`);
  }
  for (const target of ['', 'latest', '__proto__', 'linux-ia32']) assert.throws(() => runtimePin(target));
});
test('inspectZip accepts an empty boundary and real file archive; rejects unsafe member names', async () => fixture(async root => {
  const empty = Buffer.alloc(22); empty.writeUInt32LE(0x06054b50); assert.deepEqual(inspectZip(empty), []);
  const data = join(root, 'data'); await file(data, 'good.txt');
  execFileSync('zip', ['-q', join(root, 'good.zip'), 'good.txt'], { cwd: data });
  const archive = await readFile(join(root, 'good.zip')); assert.equal(inspectZip(archive)[0].path, 'good.txt');
  const unsafe = Buffer.from(archive); for (let at = 0; at < unsafe.length - 7; at++) if (unsafe.subarray(at, at + 8).toString() === 'good.txt') unsafe.write('../e.txt', at);
  assert.throws(() => inspectZip(unsafe), /Invalid package metadata/);
  assert.throws(() => inspectZip(Buffer.alloc(0)), /Unsupported ZIP/);
}));
test('prepareRuntime offline miss has no writes; a prepared cache must match its pin', async () => fixture(async root => {
  const cacheRoot = join(root, 'absent'); await assert.rejects(prepareRuntime({ target: 'linux-x64', cacheRoot, offline: true }), /cache missing/);
  await assert.rejects(lstat(cacheRoot), { code: 'ENOENT' });
  const destination = join(cacheRoot, 'electron-45.2.3-linux-x64'); await mkdir(join(destination, 'tree'), { recursive: true });
  const inventory = { format: 'jai.fabric-explorer.inventory/1', productVersion: '45.2.3', target: 'linux-x64', entries: [{path:'electron',kind:'file',size:1,sha256:'a'.repeat(64),mode:493}] };
  await writeFile(join(destination, 'prepared.json'), JSON.stringify({ target: 'linux-x64', archiveSha256: runtimePin('linux-x64').sha256, inventory }));
  assert.equal((await prepareRuntime({ target: 'linux-x64', cacheRoot, offline: true })).root, join(destination, 'tree'));
  await rm(join(destination, 'tree'), {recursive:true});
  await assert.rejects(prepareRuntime({ target: 'linux-x64', cacheRoot, offline: true }), /Incomplete runtime cache/);
  await mkdir(join(destination, 'tree'));
  await writeFile(join(destination, 'prepared.json'), JSON.stringify({ target: 'linux-x64', archiveSha256: '0'.repeat(64), inventory }));
  await assert.rejects(prepareRuntime({ target: 'linux-x64', cacheRoot, offline: true }), /pin mismatch/);
}));
test('publicSourceRevision hashes public inputs only and fails outside a worktree', async () => fixture(async root => {
  const source = publicSourceRevision(); assert.match(source.commit, /^[a-f0-9]{40,64}$/); assert.match(source.closureSha256, /^[a-f0-9]{64}$/); assert.equal(typeof source.dirty, 'boolean');
  assert.throws(() => publicSourceRevision(root));
}));
test('packageTarget deterministically emits compiled-only archives and detached exact metadata', async () => fixture(async root => {
  const options = await inputs(root);
  const first = await packageTarget({ ...options, outputRoot: join(root, 'one') });
  const second = await packageTarget({ ...options, outputRoot: join(root, 'two') });
  assert.equal(sha256(await readFile(first.assetPath)), sha256(await readFile(second.assetPath)));
  assert.deepEqual(await readFile(first.manifestPath), await readFile(second.manifestPath));
  const manifest = parseManifest(await readFile(first.manifestPath)); assert.equal(manifest.status, 'development'); assert.equal(manifest.signatureKeyId, null);
  const inventory = JSON.parse(await readFile(first.inventoryPath));
  assert.deepEqual(inventory.entries.find(entry => entry.path === 'runtime/Framework/Versions/Current'), {path:'runtime/Framework/Versions/Current',kind:'symlink',target:'A'});
  assert.equal(manifest.asset.sha256, sha256(await readFile(first.assetPath)));
  const sbom = JSON.parse(execFileSync('tar', ['-xOzf', first.assetPath, './notices/sbom.json'], {encoding:'utf8'}));
  assert.equal(sbom.packages[0].name, 'jai-fabric-explorer'); assert.equal(sbom.packages[1].checksums[0].checksumValue, runtimePin('linux-x64').sha256);
  assert.equal(sbom.packages[1].licenseConcluded, 'NOASSERTION');
  const names = execFileSync('tar', ['-tzf', first.assetPath], { encoding: 'utf8' });
  assert.match(names, /runtime\/resources\/app\/main.cjs/); assert.doesNotMatch(names, /source\.ts|performance-native|node_modules|INBOX/);
  const before = await readFile(first.assetPath); await assert.rejects(packageTarget({ ...options, outputRoot: join(root, 'one') }), /already exists/); assert.deepEqual(await readFile(first.assetPath), before);
}));
test('packageTarget rejects authored missing/linked inputs, invalid versions and release labeling', async () => fixture(async root => {
  const options = await inputs(root); const outputRoot = join(root, 'out');
  await assert.rejects(packageTarget({ ...options, outputRoot, development: false }), /development-only/);
  await assert.rejects(packageTarget({ ...options, outputRoot, version: '../escape' }), /development-only/);
  await rm(join(options.appRoot, 'main.cjs')); await assert.rejects(packageTarget({ ...options, outputRoot }), { code: 'ENOENT' });
}));
