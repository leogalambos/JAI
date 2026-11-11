/** Explicit build-input integration: actual official download/cache, extraction and inventory. */
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { resolve, join } from 'node:path';
import { prepareRuntime, runtimePin } from '../../package.mjs';
import { hashFile } from '../../inspect.mjs';

test('actual pinned Linux runtime download produces a reusable offline cache without executing Electron', async () => {
  const cacheRoot = resolve('build/fabric-explorer/runtime-cache');
  const runtime = await prepareRuntime({ target: 'linux-x64', cacheRoot });
  assert.ok(runtime.entries.some(entry => entry.path === 'electron' && entry.kind === 'file'));
  assert.ok(!runtime.entries.some(entry => entry.path.endsWith('default_app.asar')));
  assert.equal(await hashFile(join(cacheRoot, 'electron-45.2.3-linux-x64', runtimePin('linux-x64').fileName)), runtimePin('linux-x64').sha256);
  const offline = await prepareRuntime({ target: 'linux-x64', cacheRoot, offline: true });
  assert.deepEqual(offline.entries, runtime.entries); assert.match((await readFile(join(runtime.root, 'version'), 'utf8')).trim(), /^45\.2\.3$/);
});
