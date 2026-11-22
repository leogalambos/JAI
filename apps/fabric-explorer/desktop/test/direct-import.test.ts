/** Direct native descriptors, streaming archive and atomic refresh integration; Python only builds a test fixture. */
import { afterEach, beforeEach, expect, it, vi } from 'vitest';
import { mkdtemp, mkdir, readFile, writeFile, rm, appendFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join, resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';
import { createHash } from 'node:crypto';
import { PROTOCOL } from '@jai/fabric-explorer-contracts';
import { ReadBroker } from '../src/broker/read-broker.js';
import { CaptureArchiveStore } from '../src/broker/capture-archive.js';
import { draftDirectRevision, type DirectWorkerInput, type MaterialAvailability } from '../src/broker/direct-types.js';
import { buildDirectModel } from '../src/import/direct-import.js';
import { ImportSession } from '../src/import/session.js';
import { importLimits } from '../src/import/types.js';
import { NativeImportWorker, type ImportWorkerPort } from '../src/import/worker-client.js';
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
it('refreshes exact version and use labels and material observations through the actual import worker', async () => {
  const fixture = JSON.parse(await readFile(join(repository,
    'apps/fabric-explorer/packages/contracts/test/fixtures/recorded-labels.json'), 'utf8'));
  const testCase = fixture.cases.find((item: any) => item.case === 'legacy-companion');
  const blobId = testCase.expected.source.blobId;
  const companion = fixture.companions[blobId];
  const structuredMaterial = Buffer.from('Supporting notes that do not supply the label.');
  const structuredBlobId = createHash('sha256').update('jai.lifecycle.blob.v2\0').update(structuredMaterial).digest('hex');
  const structuredManifest = structuredClone(testCase.manifest);
  structuredManifest.content.record.display_summary = 'A structured label.';
  structuredManifest.content.record.material = [structuredBlobId];
  const sourcePath = join(data, 'label-source.jsonl');
  const row = { format: 9, protocol: 'jai.governed-delivery/1', sequence: 1, hash: 'a'.repeat(64),
    operations: [{ op: 'governed', data: { message: { scope: 'default',
      attachments: [{ blob_id: blobId, byte_length: companion.byteLength, media_type: companion.media,
        classification: 'internal', access_handle: 'synthetic-admitted-companion' }] },
      effects: [{ op: 'register', manifest: testCase.manifest,
        origin: { kind: 'controller', id: 'fixture' }, context: null, dependencies: [] },
      { op: 'register', manifest: structuredManifest,
        origin: { kind: 'controller', id: 'fixture' }, context: null, dependencies: [] }] } }] };
  await writeFile(sourcePath, JSON.stringify(row) + '\n');
  await mkdir(sourcePath + '.blobs');
  await writeFile(join(sourcePath + '.blobs', blobId), Buffer.from(companion.contentBase64, 'base64'));
  const selected = await broker.open('owner', [{ projectPath: data, path: sourcePath, family: 'fabric' }]);
  const source = selected.sources[0]!;
  const workerEntry = join(repository, 'apps/fabric-explorer/desktop/dist/import-worker.cjs');
  const session = new ImportSession({ sessionId: 'owner', capability: selected.capability, sources: selected.sources,
    broker, archiveDirectory: join(app, 'captures'), workerFactory: () => new NativeImportWorker(workerEntry) });
  cleanup.push(() => session.dispose());
  const snapshot = await session.import([source.sourceId], null);
  const ref = { engagement: testCase.manifest.content.engagement, scope: testCase.manifest.content.scope,
    logical_id: testCase.manifest.logical_id, version_id: testCase.versionId };
  const lookup = (generation: string, kind: 'version' | 'use') => session.queryStart({
    protocol: PROTOCOL, kind: 'request', requestId: 'lookup-' + kind,
    binding: { sessionId: 'owner', capability: selected.capability, generation },
    operation: 'element.lookup', payload: { identity: kind === 'version' ? { kind, projectId: source.projectId, ref }
      : { kind, projectId: source.projectId, ref, useScope: 'default' } },
  });
  for (const kind of ['version', 'use'] as const) {
    const page = await lookup(snapshot.generation, kind);
    expect(page.frame).toContain(testCase.expected.text);
    expect(page.frame).toContain('jai.recorded-label');
    expect(page.frame).toContain(blobId);
    expect(page.frame).not.toContain(sourcePath);
  }
  expect((await session.refresh(snapshot.generation)).generation).toBe(snapshot.generation);
  const companionPath = join(sourcePath + '.blobs', blobId);
  const original = Buffer.from(companion.contentBase64, 'base64');
  await writeFile(companionPath, Buffer.alloc(original.length, 65));
  const changed = await session.refresh(snapshot.generation);
  expect(changed.generation).toBe('2');
  expect(changed.sources[0]?.digest).toBe(snapshot.sources[0]?.digest);
  expect((await lookup(changed.generation, 'use')).frame).toContain('digest-mismatch');
  await rm(companionPath);
  const missing = await session.refresh(changed.generation);
  expect(missing.generation).toBe('3');
  expect((await lookup(missing.generation, 'version')).frame).toContain('missing');
  expect((await session.refresh(missing.generation)).generation).toBe(missing.generation);
  await writeFile(companionPath, original);
  const restored = await session.refresh(missing.generation);
  expect(restored.generation).toBe('4');
  expect((await lookup(restored.generation, 'use')).frame).toContain(testCase.expected.text);
  const lookupMaterial = (generation: string) => session.queryStart({
    protocol: PROTOCOL, kind: 'request', requestId: 'lookup-material',
    binding: { sessionId: 'owner', capability: selected.capability, generation },
    operation: 'element.lookup', payload: { identity: { kind: 'blob', projectId: source.projectId, rootId: source.rootId, blobId: structuredBlobId } },
  });
  expect((await lookupMaterial(restored.generation)).frame).toContain('"availability":"missing"');
  await writeFile(join(sourcePath + '.blobs', structuredBlobId), structuredMaterial);
  const materialAdded = await session.refresh(restored.generation);
  expect(materialAdded.generation).toBe('5');
  expect((await lookupMaterial(materialAdded.generation)).frame).toContain('"availability":"available"');

  const originalCapture = broker.captureDirect.bind(broker);
  broker.captureDirect = async (...args) => {
    const capture = await originalCapture(...args);
    return { ...capture, companionsUnchanged: async observations => {
      const unchanged = await capture.companionsUnchanged(observations);
      await appendFile(sourcePath, '\n');
      return unchanged;
    } };
  };
  await expect(session.import([source.sourceId], materialAdded.generation)).rejects.toMatchObject({ code: 'read-failed' });
  expect((await lookup(materialAdded.generation, 'use')).frame).toContain(testCase.expected.text);
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
