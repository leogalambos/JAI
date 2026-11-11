// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Application-owned end-to-end canonical helper/worker/archive import using synthetic files only. */
import { afterEach, describe, expect, it } from 'vitest';
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';
import { mkdtemp, mkdir, readFile, writeFile, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { ReadBroker } from '../src/broker/read-broker.js';
import { ImportSession } from '../src/import/session.js';
import { NativeImportWorker } from '../src/import/worker-client.js';
const repo = resolve(dirname(fileURLToPath(import.meta.url)), '../../../..');
const python = join(repo, 'build/fabric-explorer/helper-venv', process.platform === 'win32' ? 'Scripts/python.exe' : 'bin/python');
const workerEntry = join(repo, 'apps/fabric-explorer/desktop/dist/import-worker.cjs');
const execute = promisify(execFile);
const cleanups: (() => Promise<unknown>)[] = [];
afterEach(async () => { for (const cleanup of cleanups.splice(0).reverse()) await cleanup(); });
describe('canonical application import', () => {
  it('imports fabric and findings, retains exact captured pages after failed refresh, and never changes source bytes', async () => {
    const base = await mkdtemp(join(tmpdir(), 'jai-import-integration-')); cleanups.push(() => rm(base, { recursive: true, force: true }));
    const app = join(base, 'app'); const project = join(base, 'project'); await mkdir(app, { mode: 0o700 }); await mkdir(project, { mode: 0o700 });
    const generated = await execute(python, ['-I', '-B', join(repo, 'apps/fabric-explorer/reader/test/make_fabric_fixture.py'), project], { maxBuffer: 1024 * 1024 });
    const metadata = JSON.parse(generated.stdout) as { filename: string; head: string; versions: number; uses: number; sequence: number };
    const expected = { ...metadata, path: join(project, metadata.filename), sequence: String(metadata.sequence) };
    const findingsPath = join(project, 'review.jsonl'); const findingsBytes = await readFile(join(repo, 'apps/fabric-explorer/test/fixtures/findings-review.jsonl')); await writeFile(findingsPath, findingsBytes);
    const fabricBytes = await readFile(expected.path); const registry = new Map<string, string>();
    const broker = new ReadBroker({ executable: python, script: join(repo, 'apps/fabric-explorer/reader/raw_reader.py'), coreTools: join(repo, '.ai/runtime/tools'), cwd: app, writeRoots: [app], registry: { getOrCreate: async (kind, key) => { const name = `${kind}:${key}`; if (!registry.has(name)) registry.set(name, `${kind}-${registry.size}`); return registry.get(name)!; } } });
    cleanups.push(() => broker.disposeSession('integration'));
    const opened = await broker.open('integration', [{ projectPath: project, path: expected.path, family: 'fabric' }, { projectPath: project, path: findingsPath, family: 'findings' }]);
    const progress: import('../src/import/progress.js').ImportProgress[] = [];
    const session = new ImportSession({ sessionId: 'integration', capability: opened.capability, sources: opened.sources, broker, archiveDirectory: join(app, 'captures'), workerFactory: () => { const worker = new NativeImportWorker(workerEntry); const direct = worker.importDirect.bind(worker); worker.importDirect = (input, material, signal, observe) => direct(input, material, signal, value => { progress.push(value); observe?.(value); }); return worker; } }); cleanups.push(() => session.dispose());
    const descriptor = await session.import(opened.sources.map(source => source.sourceId), null);
    expect(progress[0]).toMatchObject({ phase: 'processing', bytesRead: 0, records: 0 }); expect(progress.at(-1)).toMatchObject({ phase: 'complete', bytesRead: fabricBytes.length + findingsBytes.length, sourcesCompleted: 2 }); expect(progress.some(value => value.phase === 'indexing')).toBe(true);
    expect(descriptor.counts.findings).toBe('6'); expect(BigInt(descriptor.counts.vertices)).toBeGreaterThanOrEqual(BigInt(expected.versions + expected.uses + 6));
    expect(descriptor.sources.find(source => source.family === 'fabric')).toMatchObject({ head: expected.head, sequence: expected.sequence });
    expect(session.state().report?.supportedVersions.map(item => item.family).sort()).toEqual(['fabric', 'findings']); expect(session.state().report?.observation).toBe('observed-revision-set');
    const source = descriptor.sources.find(item => item.family === 'fabric')!;
    const first = await session.sourcePage({ sourceId: source.sourceId, pointer: '', sequence: null, offset: '0', length: 256 * 1024 }, '1'); expect(Buffer.from(first.bytesBase64, 'base64')).toEqual(fabricBytes.subarray(0, 256 * 1024));
    expect(await readFile(expected.path)).toEqual(fabricBytes); expect(await readFile(findingsPath)).toEqual(findingsBytes);
    await writeFile(expected.path, fabricBytes.subarray(0, fabricBytes.length - 2));
    await expect(session.refresh('1')).rejects.toThrow(); expect(session.state().snapshot).toEqual(descriptor); expect(session.state().stale).toBe(true);
    const retained = await session.sourcePage({ sourceId: source.sourceId, pointer: '', sequence: null, offset: '0', length: 256 * 1024 }, '1'); expect(retained.bytesBase64).toBe(first.bytesBase64);
  });
});
