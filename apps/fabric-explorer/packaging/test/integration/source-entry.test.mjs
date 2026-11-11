/** Opt-in real existing-package delegation; never builds, starts a GUI or writes actual user state. */
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, mkdirSync, existsSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { resolve, join } from 'node:path';
import { spawnSync } from 'node:child_process';
const packages = process.env.JAI_VIEWER_TEST_PACKAGE_DIR;
test('clone entry installs and uninstalls the real local package through its existing verified bootstrap', { skip: !packages || process.platform !== 'linux' }, () => {
  const root = resolve(import.meta.dirname, '../../../../..'); const owned = mkdtempSync(join(tmpdir(), 'jai-viewer-entry-integration-'));
  try {
    const data = join(owned, 'data'); const config = join(owned, 'config'); const temporary = join(owned, 'tmp'); for (const path of [data, config, temporary]) mkdirSync(path);
    const env = { ...process.env, XDG_DATA_HOME: data, XDG_CONFIG_HOME: config, TMPDIR: temporary, JAI_VIEWER_NODE: '/intentionally-unavailable-node' };
    const args = [join(root, 'install-viewer.sh'), '--package-dir', resolve(packages), '--allow-development'];
    const installed = spawnSync('/bin/sh', args, { env, encoding: 'utf8', timeout: 60000 }); assert.equal(installed.status, 0, installed.stderr); const installation = join(data, 'jai-fabric-explorer/install'); assert(existsSync(join(installation, 'active'))); assert(existsSync(join(installation, 'launch-viewer')));
    const removed = spawnSync('/bin/sh', [...args, '--uninstall'], { env, encoding: 'utf8', timeout: 60000 }); assert.equal(removed.status, 0, removed.stderr); assert(!existsSync(join(installation, 'active'))); assert(!existsSync(join(installation, 'launch-viewer')));
  } finally { rmSync(owned, { recursive: true, force: true }); }
});
