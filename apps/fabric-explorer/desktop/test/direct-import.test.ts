/** Direct native descriptors, streaming archive and atomic refresh integration; Python only builds a test fixture. */
import { afterEach, beforeEach, expect, it, vi } from 'vitest';
import { mkdtemp, mkdir, readFile, writeFile, rm, appendFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join, resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';
import { createHash } from 'node:crypto';
import { ReadBroker } from '../src/broker/read-broker.js';
import { CaptureArchiveStore } from '../src/broker/capture-archive.js';
import { draftDirectRevision, type DirectWorkerInput, type MaterialAvailability } from '../src/broker/direct-types.js';
import { buildDirectModel } from '../src/import/direct-import.js';
import { ImportSession } from '../src/import/session.js';
import { importLimits } from '../src/import/types.js';
import type { ImportWorkerPort } from '../src/import/worker-client.js';
const repository = resolve(dirname(fileURLToPath(import.meta.url)), '../../../..');
let base: string, app: string, data: string, path: string, broker: ReadBroker;
const cleanup: (() => Promise<unknown>)[] = [];
beforeEach(async () => {
  base = await mkdtemp(join(tmpdir(), 'jai-direct-')); app = join(base, 'app'); data = join(base, 'data'); await mkdir(app); await mkdir(data); path = join(data, 'findings.jsonl');
  await writeFile(path, await readFile(join(repository, 'apps/fabric-explorer/test/fixtures/findings-review.jsonl')));
  const names = new Map<string, string>(); broker = new ReadBroker({ writeRoots: [app], registry: { getOrCreate: async (kind, key) => { const address = kind + key; if (!names.has(address)) names.set(address, `${kind}-${names.size}`); return names.get(address)!; } } });
});
afterEach(async () => { for (const action of cleanup.splice(0).reverse()) await action(); await broker.disposeSession('owner'); await rm(base, { recursive: true, force: true }); });
async function opened(fabric = false) {
  const selections = [{ projectPath: data, path, family: 'findings' as const }];
  if (fabric) {
    const directory = join(data, 'fabric'); await mkdir(directory);
    const executable = join(repository, 'build/fabric-explorer/helper-venv', process.platform === 'win32' ? 'Scripts/python.exe' : 'bin/python');
    const result = await promisify(execFile)(executable, ['-I', '-B', join(repository, 'apps/fabric-explorer/reader/test/make_fabric_fixture.py'), directory], { env: { LANG: 'C.UTF-8', PATH: '' } });
    const source = JSON.parse(result.stdout) as { filename: string }; return broker.open('owner', [...selections, { projectPath: data, path: join(directory, source.filename), family: 'fabric' }]);
  }
  return broker.open('owner', selections);
}
function localWorker(counter: { created: number; imports: number; stopped: number }): ImportWorkerPort {
  counter.created++; let model: Awaited<ReturnType<typeof buildDirectModel>>['model'] | null = null;
  return { importDirect: async (input: DirectWorkerInput, material: MaterialAvailability) => { counter.imports++; const result = await buildDirectModel(input, { cancelled: () => false, materialAvailable: material }); model = result.model; return result.ready; }, initialize: async () => { throw Error('Legacy initialize not used'); }, consume: async () => { throw Error('Legacy consume not used'); }, finish: async () => { throw Error('Legacy finish not used'); }, span: async (...args) => model!.span(...args), terminate: async () => { counter.stopped++; } };
}
it('streams actual Fabric and Findings into the compact graph with exact immutable archive pages', async () => {
  const selected = await opened(true); const ids = selected.sources.map(source => source.sourceId); const capture = await broker.captureDirect('owner', selected.capability, ids); cleanup.push(() => capture.dispose());
  const stage = await new CaptureArchiveStore(join(app, 'captures')).stageDirect(capture.files); cleanup.push(() => stage.dispose());
  const input: DirectWorkerInput = { binding: { sessionId: 'owner', capability: selected.capability, generation: null }, generation: '1', limits: importLimits(), files: capture.files.map(file => ({ revision: draftDirectRevision(file), stamp: file.stamp, sourceHandle: file.handle, archiveHandle: stage.outputs.get(file.admitted.sourceId)! })) };
  const { model, ready } = await buildDirectModel(input, { cancelled: () => false, materialAvailable: capture.materialAvailable }); await capture.validate();
  expect(ready.descriptor.counts.findings).toBe('6'); expect(BigInt(ready.descriptor.counts.vertices)).toBeGreaterThan(100n); expect(ready.descriptor.sources.every(source => source.verification.mode === 'recorded')).toBe(true);
  const archive = await stage.adopt(ready.descriptor.sources); const source = ready.descriptor.sources.find(source => source.family === 'findings')!; const original = await readFile(path);
  expect(source.digest).toBe(createHash('sha256').update(original).digest('hex')); expect(model.span(source.sourceId, '', null)).toEqual({ offset: '0', length: String(original.length) });
  await writeFile(path, 'changed live bytes'); const page = await archive.page(source.sourceId, '0', 262144); expect(Buffer.from(page.bytesBase64, 'base64')).toEqual(original);
});
it('refreshes unchanged sources without another worker and uses explicit Import as a deliberate candidate', async () => {
  const selected = await opened(); const counter = { created: 0, imports: 0, stopped: 0 }; const session = new ImportSession({ sessionId: 'owner', capability: selected.capability, sources: selected.sources, broker, archiveDirectory: join(app, 'captures'), workerFactory: () => localWorker(counter) }); cleanup.push(() => session.dispose());
  const ids = selected.sources.map(source => source.sourceId); const first = await session.import(ids, null); const same = await session.refresh(first.generation);
  expect(same).toEqual(first); expect(counter).toMatchObject({ created: 1, imports: 1 });
  const second = await session.import(ids, first.generation); expect(second.generation).toBe('2'); expect(counter).toMatchObject({ created: 2, imports: 2, stopped: 1 });
  const original = await readFile(path); await appendFile(path, '{malformed}\n'); await expect(session.refresh(second.generation)).rejects.toThrow(); expect(session.state().snapshot?.generation).toBe('2');
  const page = await session.sourcePage({ sourceId: ids[0]!, pointer: '', sequence: null, offset: '0', length: 262144 }, second.generation); expect(Buffer.from(page.bytesBase64, 'base64')).toEqual(original);
});
it('does not publish a candidate changed after capture and cleans private output descriptors', async () => {
  const selected = await opened(); const capture = await broker.captureDirect('owner', selected.capability, selected.sources.map(source => source.sourceId)); cleanup.push(() => capture.dispose());
  const stage = await new CaptureArchiveStore(join(app, 'captures')).stageDirect(capture.files); cleanup.push(() => stage.dispose()); await appendFile(path, '\n');
  await expect(buildDirectModel({ binding: { sessionId: 'owner', capability: selected.capability, generation: null }, generation: '1', limits: importLimits(), files: capture.files.map(file => ({ revision: draftDirectRevision(file), stamp: file.stamp, sourceHandle: file.handle, archiveHandle: stage.outputs.get(file.admitted.sourceId)! })) }, { cancelled: () => false })).rejects.toMatchObject({ code: 'read-failed' });
  expect(capture.files[0]!.handle.fd).toBe(-1);
});

it('closes independent capture handles when worker termination fails and preserves the unconfirmed writer stage', async () => {
  const outputs: import('node:fs/promises').FileHandle[] = []; const stageMethod = CaptureArchiveStore.prototype.stageDirect;
  const stageSpy = vi.spyOn(CaptureArchiveStore.prototype, 'stageDirect').mockImplementation(async function (this: CaptureArchiveStore, ...args) { const stage = await stageMethod.apply(this, args); outputs.push(...stage.outputs.values()); return stage; }); cleanup.push(async () => { stageSpy.mockRestore(); await Promise.all(outputs.map(file => file.close())); });
  const selected = await opened(); let captured: Awaited<ReturnType<ReadBroker['captureDirect']>> | null = null;
  const original = broker.captureDirect.bind(broker); broker.captureDirect = async (...args) => { captured = await original(...args); return captured; };
  const session = new ImportSession({ sessionId: 'owner', capability: selected.capability, sources: selected.sources, broker, archiveDirectory: join(app, 'captures'), workerFactory: () => ({
    importDirect: async () => { throw Error('Candidate failed'); }, initialize: async () => {}, consume: async () => {}, finish: async () => { throw Error('unused'); }, span: async () => null, terminate: async () => { throw Error('Stop not confirmed'); },
  }) }); cleanup.push(() => session.dispose());
  await expect(session.import(selected.sources.map(source => source.sourceId), null)).rejects.toThrow();
  expect(captured!.files[0]!.handle.fd).toBe(-1); expect(outputs).toHaveLength(1); expect(outputs[0]!.fd).toBe(-1);
  const { readdir } = await import('node:fs/promises'); const sets = (await readdir(join(app, 'captures'))).filter(name => name.startsWith('set-'));
  expect(sets).toHaveLength(1); expect(await readdir(join(app, 'captures', sets[0]!))).toHaveLength(1);
});

it('transfers candidate ownership before awaiting old-worker cleanup so late cancellation preserves the published worker', async () => {
  const selected = await opened(); const counter = { created: 0, imports: 0, stopped: 0 }; const stopped: number[] = [];
  let release!: () => void; const held = new Promise<void>(resolve => { release = resolve; });
  let started!: () => void; const barrier = new Promise<void>(resolve => { started = resolve; });
  const session = new ImportSession({ sessionId: 'owner', capability: selected.capability, sources: selected.sources, broker, archiveDirectory: join(app, 'captures'), workerFactory: () => {
    const worker = localWorker(counter); const id = counter.created; const terminate = worker.terminate;
    return { ...worker, terminate: async () => { stopped.push(id); if (id === 1) { started(); await held; } await terminate(); } };
  } }); cleanup.push(() => session.dispose());
  try {
    const ids = selected.sources.map(source => source.sourceId); const first = await session.import(ids, null); const abort = new AbortController();
    const pending = session.import(ids, first.generation, abort.signal); await barrier;
    expect(session.state().snapshot?.generation).toBe('2'); abort.abort(); release(); await pending;
    expect(stopped).not.toContain(2); expect(await session.sourcePage({ sourceId: ids[0]!, pointer: '', sequence: null, offset: '0', length: 100 }, '2')).toMatchObject({ byteLength: 100 });
  } finally { release(); }
});

it('drops cancelled and stale candidate progress while preserving session ownership', async () => {
  const selected = await opened(); const counter = { created: 0, imports: 0, stopped: 0 }; let notify: ((value: import('../src/import/progress.js').ImportProgress) => void) | undefined;
  let release!: () => void; const held = new Promise<void>(resolve => { release = resolve; }); let started!: () => void; const barrier = new Promise<void>(resolve => { started = resolve; });
  const session = new ImportSession({ sessionId: 'owner', capability: selected.capability, sources: selected.sources, broker, archiveDirectory: join(app, 'captures'), workerFactory: () => {
    const worker = localWorker(counter); return { ...worker, importDirect: async (input, material, signal, progress) => { notify = progress; started(); await held; if (signal?.aborted) throw Error('Cancelled candidate'); return worker.importDirect!(input, material, signal, progress); } };
  } }); cleanup.push(() => session.dispose()); const abort = new AbortController();
  const pending = session.import(selected.sources.map(source => source.sourceId), null, abort.signal); await barrier;
  const progress = { phase: 'processing' as const, bytesRead: 1, totalBytes: 10, records: 1, factsProcessed: 0, sourcesCompleted: 0, totalSources: 1 }; notify!(progress); expect(session.state().progress).toEqual(progress);
  abort.abort(); notify!({ ...progress, bytesRead: 2 }); expect(session.state().progress?.bytesRead).toBe(1); release(); await expect(pending).rejects.toThrow();
  notify!({ ...progress, bytesRead: 3 }); expect(session.state().progress).toBeUndefined();
  await session.import(selected.sources.map(source => source.sourceId), null); notify!({ ...progress, bytesRead: 4 }); expect(session.state().progress).toBeUndefined();
});
