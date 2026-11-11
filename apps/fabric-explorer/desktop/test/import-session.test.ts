// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Atomic publication tests use independent owned candidate model ports and immutable archive doubles. */
import { describe, expect, it } from 'vitest';
import { ImportModel } from '../src/import/model.js';
import type { ModelInput } from '../src/import/model.js';
import { ImportSession } from '../src/import/session.js';
import type { ImportWorkerPort } from '../src/import/worker-client.js';
import type { SemanticLease } from '../src/broker/semantic-types.js';
import { captureReport } from '../src/import/report.js';
import { DEFAULT_IMPORT_LIMITS } from '../src/import/types.js';
import { lease, revision } from './import-fixtures.js';
class OwnedWorker implements ImportWorkerPort {
  model: ImportModel | null = null; stopped = false;
  async initialize(input: ModelInput) { this.model = new ImportModel(input); }
  async consume(chunk: unknown) { if (this.stopped) throw new Error('Worker stopped'); this.model!.consume(chunk); }
  async finish() { return this.model!.finish(); }
  async span(sourceId: string, pointer: string, sequence: string | null) { if (this.stopped) throw new Error('Worker stopped'); return this.model!.span(sourceId, pointer, sequence); }
  async terminate() { this.stopped = true; }
}
function fixture(capture: () => Promise<SemanticLease> = async () => lease()) {
  const workers: OwnedWorker[] = []; const source = revision();
  const session = new ImportSession({ sessionId: 'session', capability: 'capability', sources: [{ projectId: source.projectId, rootId: source.rootId, sourceId: source.sourceId, family: source.family, relativePath: source.relativePath, readHandle: 'handle' }], broker: { capture }, workerFactory: () => { const worker = new OwnedWorker(); workers.push(worker); return worker; } });
  return { session, workers };
}
describe('atomic import session', () => {
  it('publishes only metadata, refreshes generation and releases the old worker after replacement', async () => {
    const { session, workers } = fixture(); expect(session.state().snapshot).toBeNull();
    const first = await session.import(['fabric'], null); expect(first.generation).toBe('1'); expect(workers[0]?.stopped).toBe(false); expect(session.state()).not.toHaveProperty('vertices');
    const second = await session.refresh('1'); expect(second.generation).toBe('2'); expect(workers[0]?.stopped).toBe(true); expect(workers[1]?.stopped).toBe(false);
    await expect(session.refresh('1')).rejects.toMatchObject({ code: 'stale-generation' }); await session.dispose(); await session.dispose(); expect(workers[1]?.stopped).toBe(true);
  });
  it('preserves exact previous model and frozen pages after a failed refresh/helper crash', async () => {
    let attempts = 0; const { session, workers } = fixture(async () => { if (++attempts > 1) throw new Error('SECRET native path'); return lease(); });
    const first = await session.import(['fabric'], null); await expect(session.refresh('1')).rejects.toThrow('could not be imported');
    expect(session.state().snapshot).toEqual(first); expect(session.state().stale).toBe(true); expect(workers[0]?.stopped).toBe(false);
    const page = await session.sourcePage({ sourceId: 'fabric', pointer: '/operations/0/data/effects/0/manifest', sequence: '1', offset: '95', length: 10 }, '1'); expect(page.byteLength).toBe(5); expect(page.eof).toBe(true); expect(page.pointer).toBe('/operations/0/data/effects/0/manifest'); expect(page.offset).toBe('95');
    await expect(session.sourcePage({ sourceId: 'fabric', pointer: '/invented', sequence: '1', offset: '0', length: 1 }, '1')).rejects.toMatchObject({ code: 'not-found' });
    await expect(session.sourcePage({ sourceId: 'fabric', pointer: '', sequence: null, offset: '0', length: 262145 }, '1')).rejects.toThrow('bounds');
    expect(JSON.stringify(session.state())).not.toContain('SECRET'); await session.dispose();
  });
  it('discards late cancelled candidates without stopping the separate accepted worker', async () => {
    let attempts = 0; let complete!: (value: SemanticLease) => void;
    const deferred = new Promise<SemanticLease>(resolve => { complete = resolve; });
    const { session, workers } = fixture(async () => ++attempts === 1 ? lease() : deferred);
    await session.import(['fabric'], null); const abort = new AbortController(); const work = session.refresh('1', abort.signal); abort.abort();
    await expect(session.refresh('1')).rejects.toMatchObject({ code: 'resource-limit' }); complete(lease()); await expect(work).rejects.toMatchObject({ code: 'cancelled' });
    expect(session.state().snapshot?.generation).toBe('1'); expect(workers[0]?.stopped).toBe(false); await session.dispose();
  });
  it('rejects failed persistence and corrupt worker candidates without partial publication', async () => {
    const bad = lease(); const { session, workers } = fixture(async () => ({ ...bad, persist: async () => { throw new Error('Disk unavailable'); } }));
    await expect(session.import(['fabric'], null)).rejects.toMatchObject({ code: 'read-failed' }); expect(session.state().snapshot).toBeNull(); expect(workers[0]?.stopped).toBe(true);
    await expect(session.import(['fabric', 'fabric'], null)).rejects.toMatchObject({ code: 'capability-mismatch' }); await expect(session.import(['foreign'], null)).rejects.toThrow('unadmitted'); await session.dispose();
  });
  it('validates compatibility and caps diagnostics without changing their exact total', () => {
    const input = lease(); const diagnostic = { code: 'missing-material' as const, message: 'Material unavailable.', sourceId: 'fabric', pointer: '', sequence: null };
    const reported = { ...input, report: { ...input.report, diagnosticTotal: '1001', diagnostics: Array.from({ length: 1000 }, () => diagnostic) } };
    const report = captureReport(reported, { sessionId: 'session', capability: 'capability', generation: null }, ['fabric'], { ...DEFAULT_IMPORT_LIMITS, diagnostics: 2 }); expect(report.diagnostics).toHaveLength(2); expect(report.diagnosticTotal).toBe('1001');
    expect(() => captureReport({ ...input, compatibility: [{ ...input.compatibility[0]!, declaredFormat: '10' }] }, { sessionId: 'session', capability: 'capability', generation: null }, ['fabric'], DEFAULT_IMPORT_LIMITS)).toThrow('unsupported');
    expect(() => captureReport({ ...input, report: { ...input.report, skipped: '1' } }, { sessionId: 'session', capability: 'capability', generation: null }, ['fabric'], DEFAULT_IMPORT_LIMITS)).toThrow('complete');
  });
});

it('preserves explicit unknown-version failures and verifies no late candidate after close', async () => {
  const { SemanticError } = await import('../src/broker/semantic-broker.js');
  const unknown = lease(); const failure = new SemanticError('incompatible-source', { ...unknown.report, accepted: '0', rejected: '1', diagnosticTotal: '1', diagnostics: [{ code: 'incompatible-source', message: 'Unsupported source version.', sourceId: 'fabric', pointer: '', sequence: null }] }, [{ ...unknown.compatibility[0]!, declaredFormat: '99', supported: false }]);
  const { session } = fixture(async () => { throw failure; }); await expect(session.import(['fabric'], null)).rejects.toMatchObject({ code: 'incompatible-source' });
  expect(session.state().report).toMatchObject({ status: 'failed', supportedVersions: [{ declaredFormat: '99', supported: false }] }); await session.dispose();
  let finish!: (value: SemanticLease) => void; const waiting = new Promise<SemanticLease>(resolve => { finish = resolve; }); const late = fixture(() => waiting);
  const work = late.session.import(['fabric'], null); const closed = late.session.dispose(); finish(lease()); await expect(work).rejects.toMatchObject({ code: 'cancelled' }); await closed; expect(late.session.state().snapshot).toBeNull();
});

it('retains accepted state and fixed recovery for an actual stale viewer capture marker only', async () => {
  const { mkdtemp, mkdir, writeFile, rm } = await import('node:fs/promises'); const { tmpdir } = await import('node:os'); const { join } = await import('node:path');
  const { CaptureArchiveStore } = await import('../src/broker/capture-archive.js');
  const base = await mkdtemp(join(tmpdir(), 'jai-import-cache-')); const cache = join(base, 'captures'); await mkdir(cache, { mode: 0o700 }); await writeFile(join(cache, '.active'), 'synthetic stale marker', { mode: 0o600 });
  const recovery = 'Capture cache is in use or stale; close other viewer instances and clear only the viewer temporary capture cache.';
  const store = new CaptureArchiveStore(cache); let attempts = 0;
  const setup = fixture(async () => {
    const captured = lease();
    if (++attempts === 1) return captured;
    return { ...captured, persist: () => store.persist(captured.sources, async () => { throw new Error('Unexpected source page request'); }) };
  });
  try {
    const first = await setup.session.import(['fabric'], null);
    await expect(setup.session.refresh('1')).rejects.toThrow(recovery); expect(setup.session.state().snapshot).toEqual(first); expect(setup.workers[0]?.stopped).toBe(false);
    expect(setup.session.state().report).toMatchObject({ status: 'failed', limitation: recovery, diagnostics: [{ code: 'read-failed', message: recovery }] });
    const bytes = await setup.session.sourcePage({ sourceId: 'fabric', pointer: '', sequence: null, offset: '0', length: 1 }, '1'); expect(bytes.byteLength).toBe(1);
  } finally { await setup.session.dispose(); await rm(base, { recursive: true, force: true }); }
  const generic = fixture(async () => { throw new Error(recovery); });
  await expect(generic.session.import(['fabric'], null)).rejects.toThrow('could not be imported'); expect(generic.session.state().report?.limitation).toBeNull(); await generic.session.dispose();
});
