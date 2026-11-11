// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Real nonroot ACL and direct TypeScript import/archive qualification on synthetic owned inputs only. */
import { afterEach, beforeEach, describe, expect, it } from 'vitest';
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';
import { mkdtemp, readFile, rm, access } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { ReadBroker } from '../src/broker/read-broker.js';
import { CaptureArchiveStore } from '../src/broker/capture-archive.js';
import { draftDirectRevision } from '../src/broker/direct-types.js';
import { buildDirectModel } from '../src/import/direct-import.js';
import { importLimits } from '../src/import/types.js';
import type { CapturedSources } from '../src/broker/semantic-types.js';
const run = promisify(execFile); const repository = resolve(dirname(fileURLToPath(import.meta.url)), '../../../..');
const python = join(repository, 'build/fabric-explorer/helper-venv/bin/python');
const fixtureScript = join(repository, 'apps/fabric-explorer/qualification/fixtures.py');
let directory: string; let manifest: { sourceRoot: string; projectRoot: string; fabric: string; findings: string; appRoot: string; negativeWriteProbes: { denied: boolean; errno: number }[] };
let broker: ReadBroker; let archive: CapturedSources | null;
async function fixture(...args: string[]) { return run(python, ['-I', '-B', fixtureScript, ...args], { cwd: repository, env: { LANG: 'C.UTF-8', PATH: '' }, maxBuffer: 4 * 1024 * 1024 }); }
async function captureRecorded(capability: string, sourceIds: readonly string[]) {
  const capture = await broker.captureDirect('security-owner', capability, sourceIds);
  let stage: Awaited<ReturnType<CaptureArchiveStore['stageDirect']>> | null = null; let adopted = false;
  try {
    stage = await new CaptureArchiveStore(join(manifest.appRoot, 'captures')).stageDirect(capture.files);
    const { ready } = await buildDirectModel({ binding: { sessionId: 'security-owner', capability, generation: null }, generation: '1', limits: importLimits(),
      files: capture.files.map(file => ({ revision: draftDirectRevision(file), stamp: file.stamp, sourceHandle: file.handle, archiveHandle: stage!.outputs.get(file.admitted.sourceId)! })) },
    { cancelled: () => false, materialAvailable: capture.materialAvailable });
    await capture.validate(); archive = await stage.adopt(ready.descriptor.sources); adopted = true; return ready;
  } finally { await capture.dispose(); if (!adopted) await stage?.dispose(); }
}

describe.skipIf(process.platform !== 'linux')('actual protected-source qualification', () => {
  beforeEach(async () => {
    expect(process.getuid?.()).not.toBe(0); directory = await mkdtemp(join(tmpdir(), 'jai-security-readonly-')); archive = null;
    await fixture('prepare', '--directory', directory, '--python', python, '--electron', '/usr/bin/true', '--initial-cwd', join(repository, 'apps/fabric-explorer/desktop'));
    manifest = JSON.parse(await readFile(join(directory, 'security-input.json'), 'utf8'));
    const entries = new Map<string, string>();
    broker = new ReadBroker({ writeRoots: [manifest.appRoot], registry: { getOrCreate: async (kind, key) => { const address = `${kind}:${key}`; if (!entries.has(address)) entries.set(address, `${kind}-${entries.size}`); return entries.get(address)!; } } });
  });
  afterEach(async () => {
    await archive?.dispose(); await broker?.disposeSession('security-owner');
    if (directory) { await fixture('restore', '--manifest', join(directory, 'security-input.json')); await rm(directory, { recursive: true, force: true }); }
  });
  it('imports journals/material and archives bytes under proven OS write denial without changing entries or identities', async () => {
    expect(manifest.negativeWriteProbes).toHaveLength(4); expect(manifest.negativeWriteProbes.every(probe => probe.denied && probe.errno === 13)).toBe(true);
    const before = await readFile(manifest.findings);
    const opened = await broker.open('security-owner', [{ projectPath: manifest.projectRoot, path: manifest.fabric, family: 'fabric' }, { projectPath: manifest.projectRoot, path: manifest.findings, family: 'findings' }]);
    const ready = await captureRecorded(opened.capability, opened.sources.map(source => source.sourceId));
    expect(BigInt(ready.descriptor.counts.vertices)).toBeGreaterThan(0n); expect(ready.report.acceptedSources).toBe('2');
    const source = opened.sources.find(item => item.family === 'findings')!; const page = await archive!.page(source.sourceId, '0', 262144); expect(Buffer.from(page.bytesBase64, 'base64')).toEqual(before);
    await fixture('check', '--manifest', join(directory, 'security-input.json'), '--output', join(directory, 'integrity.json'));
    expect(JSON.parse(await readFile(join(directory, 'integrity.json'), 'utf8')).unchanged).toBe(true);
    await expect(access(join(manifest.appRoot, 'project-code-executed'))).rejects.toThrow();
  });
  it('rejects a new live read after a controlled permission change while retaining its accepted archived bytes', async () => {
    const before = await readFile(manifest.findings); const opened = await broker.open('security-owner', [{ projectPath: manifest.projectRoot, path: manifest.findings, family: 'findings' }]);
    const source = opened.sources[0]!; await captureRecorded(opened.capability, [source.sourceId]);
    // Explicit test-driver mutation after admission, before the next action; no timing sleeps.
    await run('/usr/bin/setfacl', ['-m', 'u::---', manifest.findings]);
    await expect(broker.readPage('security-owner', opened.capability, source.sourceId, { offset: '0', length: 10 })).rejects.toThrow();
    await expect(broker.captureDirect('security-owner', opened.capability, [source.sourceId])).rejects.toThrow();
    expect(Buffer.from((await archive!.page(source.sourceId, '0', 262144)).bytesBase64, 'base64')).toEqual(before);
    await run('/usr/bin/setfacl', ['-m', 'u::r--', manifest.findings]);
    await fixture('check', '--manifest', join(directory, 'security-input.json'), '--output', join(directory, 'integrity.json'));
    expect(JSON.parse(await readFile(join(directory, 'integrity.json'), 'utf8')).unchanged).toBe(true);
  });
});
