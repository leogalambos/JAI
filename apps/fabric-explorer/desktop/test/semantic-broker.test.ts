/** Real native source streams and private immutable archive integration; no runtime helper. */
import { afterEach, beforeEach, describe, expect, it } from 'vitest';
import { createHash } from 'node:crypto';
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';
import { copyFile, mkdtemp, mkdir, readFile, readdir, realpath, rm, writeFile } from 'node:fs/promises';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { tmpdir } from 'node:os';
import { decodeSemantic } from '@jai/fabric-explorer-contracts';
import type { BytePage, SourceRevision, Vertex } from '@jai/fabric-explorer-contracts';
import { ReadBroker } from '../src/broker/read-broker.js';
import { CaptureArchiveStore } from '../src/broker/capture-archive.js';
import { draftDirectRevision } from '../src/broker/direct-types.js';
import { buildDirectModel } from '../src/import/direct-import.js';
import { importLimits } from '../src/import/types.js';
import type { CapturedSources } from '../src/broker/semantic-types.js';
type VersionVertex = Extract<Vertex, { kind: 'version' }>;
type UseVertex = Extract<Vertex, { kind: 'use' }>;
type FindingVertex = Extract<Vertex, { kind: 'finding' }>;
const repo = resolve(dirname(fileURLToPath(import.meta.url)), '../../../..');
const executable = join(repo, 'build/fabric-explorer/helper-venv', process.platform === 'win32' ? 'Scripts/python.exe' : 'bin/python');
let base: string; let app: string; let data: string; let raw: ReadBroker; const archives: CapturedSources[] = [];
beforeEach(async () => {
  base = await realpath(await mkdtemp(join(tmpdir(), 'jai-semantic-'))); app = join(base, 'app'); data = join(base, 'data'); await Promise.all([mkdir(app), mkdir(data)]);
  const registry = new Map<string, string>(); raw = new ReadBroker({ writeRoots: [app], registry: { getOrCreate: async (kind, key) => { const id = `${kind}:${key}`; if (!registry.has(id)) registry.set(id, `${kind}-${registry.size}`); return registry.get(id)!; } } });
});
afterEach(async () => { for (const archive of archives.splice(0)) await archive.dispose(); await raw.disposeSession('owner'); await rm(base, { recursive: true, force: true }); });
async function findings() {
  const path = join(data, 'review.jsonl'); await copyFile(join(repo, 'apps/fabric-explorer/test/fixtures/findings-review.jsonl'), path);
  const opened = await raw.open('owner', [{ projectPath: data, path, family: 'findings' }]); return { opened, path };
}
async function imported(opened: Awaited<ReturnType<ReadBroker['open']>>) {
  const capture = await raw.captureDirect('owner', opened.capability, opened.sources.map(source => source.sourceId));
  const stage = await new CaptureArchiveStore(join(app, 'captures')).stageDirect(capture.files);
  try {
    const result = await buildDirectModel({ binding: { sessionId: 'owner', capability: opened.capability, generation: null }, generation: '1', limits: importLimits(), files: capture.files.map(file => ({ revision: draftDirectRevision(file), stamp: file.stamp, sourceHandle: file.handle, archiveHandle: stage.outputs.get(file.admitted.sourceId)! })) }, { cancelled: () => false, materialAvailable: capture.materialAvailable });
    await capture.validate(); const archive = await stage.adopt(result.ready.descriptor.sources); archives.push(archive); return { ...result, archive };
  } catch (error) { await stage.dispose(); throw error; } finally { await capture.dispose(); }
}
describe('direct recorded import and disk archive', () => {
  it('retains exact old source bytes after source capability closure and failed live import', async () => {
    const { opened, path } = await findings(); const before = await readFile(path); const result = await imported(opened);
    expect(result.ready.report.supportedVersions[0]).toMatchObject({ family: 'findings', declaredFormat: null, supported: true }); expect(result.ready.descriptor.counts.findings).toBe('6');
    await writeFile(path, 'new corrupt live source'); await expect(imported(opened)).rejects.toThrow(); await raw.disposeSession('owner');
    const page = await result.archive.page(opened.sources[0]!.sourceId, '0', 262144); expect(Buffer.from(page.bytesBase64, 'base64')).toEqual(before); expect(page.eof).toBe(true);
  });
  it('maps actual seven-family recorded identities, use scopes and relation provenance', async () => {
    const generated = await promisify(execFile)(executable, ['-I', '-B', join(repo, 'apps/fabric-explorer/reader/test/make_fabric_fixture.py'), data], { cwd: app, env: { LANG: 'C.UTF-8', PATH: '' } });
    const expected = JSON.parse(generated.stdout) as { filename: string; versions: number; uses: number; head: string; versionRefs: unknown[]; usePoints: unknown[] };
    const path = join(data, expected.filename); const before = await readFile(path); const opened = await raw.open('owner', [{ projectPath: data, path, family: 'fabric' }]); const result = await imported(opened); const records = [...result.model.records()];
    const versions = records.filter(record => 'kind' in record && record.kind === 'version') as VersionVertex[]; const uses = records.filter(record => 'kind' in record && record.kind === 'use') as UseVertex[];
    expect(versions.map(vertex => vertex.identity.ref)).toEqual(expected.versionRefs);
    const order = (a: unknown, b: unknown) => JSON.stringify(a).localeCompare(JSON.stringify(b));
    expect(uses.map(vertex => ({ ref: vertex.identity.ref, use_scope: vertex.identity.useScope })).sort(order)).toEqual(expected.usePoints.sort(order));
    expect(new Set(versions.map(vertex => vertex.family))).toEqual(new Set(['source', 'profile', 'assignment', 'context', 'product', 'assessment', 'decision']));
    for (const vertex of versions) expect(result.model.span(vertex.source.sourceId, vertex.source.pointer, vertex.source.sequence)).not.toBeNull();
    const productIds = new Set(versions.filter(vertex => vertex.family === 'product').map(vertex => vertex.identity.ref.version_id));
    expect(records.some(record => !('kind' in record) && record.identity.kind === 'occurrence' && record.identity.origin.kind === 'use' && productIds.has(record.identity.origin.ref.version_id) && record.identity.pointer === '/assignment' && record.causal && record.extensions?.['jai.governing']?.type === 'boolean' && record.extensions['jai.governing'].value === false)).toBe(true);
    expect(BigInt(result.ready.descriptor.counts.vertices)).toBeGreaterThanOrEqual(BigInt(expected.versions + expected.uses)); expect(BigInt(result.ready.descriptor.counts.edges)).toBeGreaterThan(0n); expect(result.ready.descriptor.sources[0]!.head).toBe(expected.head); expect(await readFile(path)).toEqual(before);
  });
  it.each(['float', 'nan', 'object', 'unicode'])('retains nontext finding targets through direct parsing and the model: %s', async kind => {
    const path = join(data, `${kind}.jsonl`); await promisify(execFile)(executable, ['-I', '-B', join(repo, 'apps/fabric-explorer/reader/test/make_findings_fixture.py'), path, kind], { cwd: app, env: { LANG: 'C.UTF-8', PATH: '' } });
    const before = await readFile(path); const opened = await raw.open('owner', [{ projectPath: data, path, family: 'findings' }]); const result = await imported(opened);
    for (const vertex of [...result.model.records()].filter(record => 'kind' in record && record.kind === 'finding') as FindingVertex[]) {
      expect(vertex.attributes.kind).toBe('inline'); if (vertex.attributes.kind === 'inline') {
        const value = decodeSemantic(vertex.attributes.value, 'findings') as { record: { target: unknown } };
        if (kind === 'object') expect(value.record.target).toEqual({ counter: 9007199254740993n }); else if (kind === 'unicode') expect(value.record.target).toEqual({ text: 'Ωλ東京'.repeat(20), symbol: '😀' }); else if (kind === 'nan') expect(Number.isNaN(value.record.target)).toBe(true); else expect(value.record.target).toBe(1.5);
      }
    }
    expect(result.ready.descriptor.counts.findings).toBe('6'); expect(result.ready.descriptor.sources[0]!.digest).toBe(createHash('sha256').update(before).digest('hex'));
    const page = await result.archive.page(opened.sources[0]!.sourceId, '0', 262144); expect(Buffer.from(page.bytesBase64, 'base64')).toEqual(before); expect(await readFile(path)).toEqual(before);
  });
  it('rejects foreign owners and cancellation without changing source bytes', async () => {
    const { opened, path } = await findings(); const before = await readFile(path);
    await expect(raw.captureDirect('foreign', opened.capability, [opened.sources[0]!.sourceId])).rejects.toMatchObject({ code: 'stale-binding' });
    const cancel = new AbortController(); cancel.abort(); await expect(raw.captureDirect('owner', opened.capability, [opened.sources[0]!.sourceId], cancel.signal)).rejects.toMatchObject({ code: 'cancelled' }); expect(await readFile(path)).toEqual(before);
  });
  it('bounds accepted and candidate sets and removes only owned archive entries', async () => {
    const { opened } = await findings(); await imported(opened); await imported(opened); await expect(imported(opened)).rejects.toThrow('slot');
    await archives.shift()!.dispose(); await imported(opened);
  });
  it('fails closed on stale or in-use cache and never deletes unknown files', async () => {
    const bytes = Buffer.from('cache bytes'); const source = { sourceId: 'synthetic', byteLength: String(bytes.length), digest: createHash('sha256').update(bytes).digest('hex') } as SourceRevision;
    const page = async (_source: string, offset: string): Promise<BytePage> => ({ sourceId: source.sourceId, pointer: '', sequence: null, offset, bytesBase64: bytes.toString('base64'), byteLength: bytes.length, eof: true });
    const stale = join(app, 'stale'); await mkdir(stale, { mode: 0o700 }); await writeFile(join(stale, 'unknown'), 'preserve');
    await expect(new CaptureArchiveStore(stale).persist([source], page)).rejects.toMatchObject({ name: 'CacheUnavailableError', message: 'Capture cache is in use or stale; close other viewer instances and clear only the viewer temporary capture cache.' }); expect(await readFile(join(stale, 'unknown'), 'utf8')).toBe('preserve'); expect(await readdir(stale)).toEqual(['unknown']);
    const occupied = join(app, 'occupied'); await mkdir(occupied, { mode: 0o700 }); await writeFile(join(occupied, '.active'), 'foreign-owner');
    await expect(new CaptureArchiveStore(occupied).persist([source], page)).rejects.toMatchObject({ name: 'CacheUnavailableError', message: 'Capture cache is in use or stale; close other viewer instances and clear only the viewer temporary capture cache.' }); expect(await readFile(join(occupied, '.active'), 'utf8')).toBe('foreign-owner');
  });
  it('rejects digest corruption and cancellation at controlled copy boundaries', async () => {
    const root = join(app, 'owned-archive'); const store = new CaptureArchiveStore(root); const bytes = Buffer.from('exact bytes');
    const revision = { sourceId: 'synthetic-source', byteLength: String(bytes.length), digest: createHash('sha256').update(bytes).digest('hex') } as SourceRevision;
    const page = async (_source: string, offset: string): Promise<BytePage> => ({ sourceId: revision.sourceId, pointer: '', sequence: null, offset, bytesBase64: bytes.toString('base64'), byteLength: bytes.length, eof: true });
    await expect(store.persist([{ ...revision, digest: '0'.repeat(64) }], page)).rejects.toThrow('digest'); expect(await readdir(root)).toEqual(['.active']);
    const cancel = new AbortController(); await expect(store.persist([revision], async (...args) => { const result = await page(args[0], args[1]); cancel.abort(); return result; }, cancel.signal)).rejects.toThrow('cancelled'); expect(await readdir(root)).toEqual(['.active']);
    const archived = await store.persist([revision], page); archives.push(archived); await expect(archived.page('foreign', '0', 2)).rejects.toThrow(); await expect(archived.page(revision.sourceId, '01', 2)).rejects.toThrow(); await expect(archived.page(revision.sourceId, '0', 262145)).rejects.toThrow();
  });
});

it('retains typed source-scoped format failure metadata without native paths', async () => {
  const path = join(data, 'unsupported.jsonl'); await writeFile(path, '{"format":99,"protocol":"unsupported-recorded-protocol"}\n');
  const opened = await raw.open('owner', [{ projectPath: data, path, family: 'fabric' }]);
  try { await imported(opened); throw Error('Expected rejection'); }
  catch (error) {
    const failure = error as import('../src/import/types.js').ImportError;
    expect(failure.code).toBe('incompatible-source'); expect(failure.report?.rejectedSources).toBe('1');
    expect(failure.report?.supportedVersions[0]).toMatchObject({ sourceId: opened.sources[0]!.sourceId, family: 'fabric', declaredFormat: '99', supported: false });
    expect(JSON.stringify(failure.report)).not.toContain(base);
  }
});
