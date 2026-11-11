/** Source-entry planning and fail-fast contracts; no dependency installation or product compilation. */
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, mkdirSync, writeFileSync, existsSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { resolve, join } from 'node:path';
import { spawnSync } from 'node:child_process';
import { currentTarget, sourceOptions, sourcePlan, installFromSource, npmCli } from '../install-from-source.mjs';
const root = resolve(import.meta.dirname, '../../../..');
const ports = overrides => ({ root, node: '/host path/node', npm: '/host path/npm/bin/npm-cli.js', nodeVersion: '24.22.2', npmVersion: '11.21.2', output: join(tmpdir(), `source-viewer-unwritten-${process.pid}`), log() {}, ...overrides });
test('all five exact targets retain arguments with spaces and only package the current combination', () => {
  for (const [platform, architecture] of [['linux','x64'],['linux','arm64'],['darwin','x64'],['darwin','arm64'],['win32','x64']]) {
    const target = currentTarget(platform, architecture); const plan = sourcePlan(ports({ target }));
    const packaging = plan.find(row => row.args[0].endsWith('/package.mjs')); assert.equal(packaging.args[1], target); assert(!packaging.args.includes('all'));
    assert(plan.some(row => row.args[0].endsWith('/check-built-contracts.mjs'))); assert(!plan.some(row => row.args[0].endsWith('/prepare-sigma.mjs'))); assert.equal(plan[0].program, '/host path/node'); assert.equal(plan[0].args[0], '/host path/npm/bin/npm-cli.js'); assert(plan[0].args.includes('--ignore-scripts'));
    assert.equal(plan.at(-1).program, platform === 'win32' ? 'powershell.exe' : 'sh'); assert(plan.at(-1).args.some(arg => arg.includes('.install.')));
  }
});
test('unsupported targets and missing explicit flags stop before execution', () => {
  for (const pair of [['win32','arm64'],['freebsd','x64'],['linux','ia32']]) assert.throws(() => currentTarget(...pair), /Unsupported/);
  for (const args of [[],['--build'],['--allow-development'],['--build','--allow-development','--uninstall'],['--build','--allow-development','--build']]) assert.throws(() => sourceOptions(args));
});
test('dry run writes nothing and invokes neither build commands nor prerequisite probes', () => {
  let called = 0; const host = ports({ platform: 'linux', architecture: 'x64', run() { called++; }, probe() { called++; } });
  const result = installFromSource(['--build','--allow-development','--dry-run'], host);
  assert.equal(result.dryRun, true); assert.equal(called, 0); assert.equal(existsSync(host.output), false);
});
test('wrong host versions and missing prerequisites reject before the first build write', () => {
  for (const versions of [{ nodeVersion: '24.18.0' }, { npmVersion: '11.16.0' }]) assert.throws(() => installFromSource(['--build','--allow-development'], ports(versions)), /requires/);
  let ran = 0; assert.throws(() => installFromSource(['--build','--allow-development'], ports({ platform: 'darwin', architecture: 'arm64', probe: program => program === 'tar' ? 'bsdtar' : 'available', run() { ran++; } })), /GNU tar/); assert.equal(ran, 0);
  assert.throws(() => installFromSource(['--build','--allow-development'], ports({ probe() { throw new Error('missing tool'); }, run() { ran++; } })), /missing tool/); assert.equal(ran, 0);
});
test('the first failed build command stops all later packaging and installation commands', () => {
  const calls = []; assert.throws(() => installFromSource(['--build','--allow-development'], ports({ probe: () => 'GNU tar available', run(program,args) { calls.push({program,args}); throw new Error('npm rejected lockfile'); } })), /npm rejected/); assert.equal(calls.length, 1); assert.equal(calls[0].args[1], 'ci');
});
test('host npm override resolves an existing JavaScript CLI without shell quoting', () => {
  const directory = mkdtempSync(join(tmpdir(), 'viewer npm & path-')); try { const cli = join(directory, 'npm-cli.js'); writeFileSync(cli, ''); assert.equal(npmCli({ env: { JAI_VIEWER_NPM_CLI: cli }, node: '/unused/node' }), cli); assert.throws(() => npmCli({ env: { JAI_VIEWER_NPM_CLI: join(directory, 'missing.js') } }), /missing/); } finally { rmSync(directory, { recursive: true }); }
});
test('POSIX prebuilt route is Node-free, preserves path metacharacters and dry-run never executes the sidecar', { skip: process.platform === 'win32' }, () => {
  const base = mkdtempSync(join(tmpdir(), 'viewer-entry-')); try {
    const packages = join(base, 'packages & literal'); mkdirSync(packages); const marker = join(base, 'called');
    const sidecar = join(packages, `jai-fabric-explorer-test-${process.platform}-${process.arch}.tar.gz.install.sh`); writeFileSync(sidecar, `#!/bin/sh\nprintf '%s\\n' "$@" > '${marker}'\n`);
    const args = [join(root, 'install-viewer.sh'), '--package-dir', packages, '--allow-development'];
    const dry = spawnSync('/bin/sh', [...args, '--dry-run'], { encoding: 'utf8', env: { ...process.env, JAI_VIEWER_NODE: '/missing/node' } }); assert.equal(dry.status, 0, dry.stderr); assert(!existsSync(marker));
    const install = spawnSync('/bin/sh', args, { encoding: 'utf8', env: { ...process.env, JAI_VIEWER_NODE: '/missing/node' } }); assert.equal(install.status, 0, install.stderr); assert(existsSync(marker));
    const missing = spawnSync('/bin/sh', [join(root, 'install-viewer.sh')], { encoding: 'utf8' }); assert.equal(missing.status, 2); assert.match(missing.stderr, /--build/);
  } finally { rmSync(base, { recursive: true }); }
});
