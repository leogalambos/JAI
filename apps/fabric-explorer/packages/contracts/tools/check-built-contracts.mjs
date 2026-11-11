/**
 * Build/consumer integration check, not application runtime code.
 * Inputs: compiled package, public schema and locally installed pinned Vite.
 * Output: a success line, or a nonzero process status with assertion diagnostics.
 * Bundling stays in memory; a child verifies both targets with string code generation disabled.
 */
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';
import { build } from 'vite';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
await readFile(resolve(root, 'dist/src/index.d.ts'));
const types = spawnSync(process.execPath, [
  resolve(root, 'node_modules/typescript/bin/tsc'), '--ignoreConfig', '--noEmit', '--strict',
  '--module', 'NodeNext', '--moduleResolution', 'NodeNext', '--target', 'ES2023',
  '--skipLibCheck', 'test/built-consumer.types.ts',
], { cwd: root, encoding: 'utf8', timeout: 30000, maxBuffer: 1024 * 1024 });
assert.ifError(types.error);
assert.equal(types.status, 0, types.stderr || types.stdout);
const projection = JSON.parse(await readFile(resolve(root, 'test/fixtures/projection.json'), 'utf8'));
const result = await build({
  configFile: false, envFile: false, publicDir: false, root, logLevel: 'silent',
  build: {
    target: 'es2023', write: false, minify: false,
    lib: { entry: resolve(root, 'dist/src/index.js'), formats: ['es'], fileName: 'contracts-browser' },
  },
});
const outputs = Array.isArray(result) ? result : [result];
assert.equal(outputs.length, 1);
const chunks = outputs[0].output.filter(item => item.type === 'chunk');
assert.equal(chunks.length, 1, 'Browser consumer must be a standalone module');
const chunk = chunks[0];
assert.equal(chunk.imports.length, 0, 'No external runtime imports may remain in the browser consumer');
assert.equal(chunk.dynamicImports.length, 0);
assert.doesNotMatch(chunk.code, /__vite-browser-external|\bnew\s+Function\s*\(|\beval\s*\(/);
const browser = `data:text/javascript;base64,${Buffer.from(chunk.code).toString('base64')}`;
const script = `
import assert from 'node:assert/strict';
const native = await import('@jai/fabric-explorer-contracts');
const schema = await import('@jai/fabric-explorer-contracts/schema', { with: { type: 'json' } });
assert.equal(schema.default.$id, 'https://jai.local/fabric-explorer/contracts/1');
const browser = await import(${JSON.stringify(browser)});
for (const api of [native, browser]) {
  assert.equal(api.PROTOCOL, 'jai.fabric-explorer.consumer/1');
  const integer = 90071992547409931234567890n;
  assert.equal(api.decodeSemantic(api.encodeSemantic({ count: integer })).count, integer);
  const numeric = api.decodeSemantic(api.encodeSemantic({ fraction: 1.5, signedZero: -0 }, 'findings'), 'findings');
  assert.equal(numeric.fraction, 1.5);
  assert.equal(Object.is(numeric.signedZero, -0), true);
  assert.throws(() => api.encodeSemantic(1.5), error => error.code === 'invalid-model');
  const identity = { kind: 'finding', projectId: 'synthetic-project', ledgerId: 'synthetic-review', findingId: 'F-0001' };
  assert.notEqual(api.elementKey(identity), api.elementKey({ ...identity, projectId: 'another-project' }));
  api.assertProjection(${JSON.stringify(projection)});
  const invalidProjection = ${JSON.stringify(projection)};
  invalidProjection.authorityGranted = true;
  assert.throws(() => api.assertProjection(invalidProjection));
  assert.deepEqual(api.parseWire(api.encodeWire({ type: 'integer', value: integer.toString() })), { type: 'integer', value: integer.toString() });
}
console.log('PASS: actual package/schema exports and browser bundle run with runtime string code generation disabled.');
`;
const child = spawnSync(process.execPath, ['--disallow-code-generation-from-strings', '--input-type=module'], {
  cwd: root, input: script, encoding: 'utf8', timeout: 30000, maxBuffer: 1024 * 1024,
});
assert.ifError(child.error);
assert.equal(child.status, 0, child.stderr || child.stdout);
process.stdout.write(child.stdout);
