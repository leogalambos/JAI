/** Real native selected-file/filesystem integration; namespace persistence is an owned application port. */
import { afterEach, beforeEach, describe, expect, it } from 'vitest';
import { mkdtemp, mkdir, readFile, writeFile, rename, rm, symlink, link } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { nativeFileStamp, sameFileStamp, ReadBroker } from '../src/broker/read-broker.js';
import type { NamespaceRegistry, SourceSelection } from '../src/broker/types.js';

const repo = resolve(dirname(fileURLToPath(import.meta.url)), '../../../..');
const executable = join(repo, 'build/fabric-explorer/helper-venv', process.platform === 'win32' ? 'Scripts/python.exe' : 'bin/python');
const script = join(repo, 'apps/fabric-explorer/reader/raw_reader.py');
const coreTools = join(repo, '.ai/runtime/tools');
let base: string;
let brokers: ReadBroker[];
let selection: SourceSelection;
let app: string;
function registry(): NamespaceRegistry {
  const entries = new Map<string, string>();
  return { getOrCreate: async (kind, key) => {
    expect(key).toMatch(/^[a-f0-9]{64}$/);
    const combined = `${kind}:${key}`;
    if (!entries.has(combined)) entries.set(combined, `${kind}-${entries.size}`);
    return entries.get(combined)!;
  } };
}
function broker(namespaces = registry()): ReadBroker {
  const result = new ReadBroker({ writeRoots: [app], registry: namespaces });
  brokers.push(result); return result;
}
beforeEach(async () => {
  base = await mkdtemp(join(tmpdir(), 'jai-reader-')); brokers = [];
  app = join(base, 'app'); const project = join(base, 'project'); const external = join(base, 'external');
  await Promise.all([mkdir(app), mkdir(project), mkdir(external)]);
  selection = { projectPath: project, path: join(external, 'engagement.jsonl'), family: 'fabric' };
  await writeFile(selection.path, 'first\nsecond\n');
});
afterEach(async () => {
  for (const item of brokers) await item.disposeSession('owner');
  await rm(base, { recursive: true, force: true });
});

describe('fixed retained-root read broker', () => {
  it('does not launch legacy executables or invoke obsolete helper observers', async () => {
    const observations: unknown[] = [];
    const reader = new ReadBroker({ executable: '/not-an-executable', script: '/not-a-script', coreTools: '/not-an-import-root', cwd: app, writeRoots: [app], registry: registry(), onHelperClose: value => observations.push(value) }); brokers.push(reader);
    const opened = await reader.open('owner', [selection]); expect(opened.sources).toHaveLength(1); expect(observations).toEqual([]);
    await reader.disposeSession('owner'); expect(observations).toEqual([]);
  });
  it('reads exact bounded bytes, permits append and preserves namespaces across reopen', async () => {
    const reader = broker(); const before = await readFile(selection.path);
    const first = await reader.open('owner', [selection]); const source = first.sources[0]!;
    expect(source).toMatchObject({ family: 'fabric', relativePath: 'engagement.jsonl' });
    expect(JSON.stringify(first)).not.toContain(base);
    const page = await reader.readPage('owner', first.capability, source.sourceId, { offset: '2', length: 4 });
    expect(Buffer.from(page.bytesBase64, 'base64')).toEqual(before.subarray(2, 6));
    await writeFile(selection.path, Buffer.concat([before, Buffer.from('new\n')]));
    expect((await reader.readPage('owner', first.capability, source.sourceId, { offset: String(before.length), length: 10 })).eof).toBe(true);
    await reader.close('owner', first.capability); await reader.close('owner', first.capability);
    const second = await reader.open('owner', [selection]);
    expect(second.capability).not.toBe(first.capability);
    expect(second.sources[0]!.sourceId).toBe(source.sourceId);
    expect(second.sources[0]!.readHandle).not.toBe(source.readHandle);
  });
  it('denies foreign sessions, foreign source IDs, closed handles and oversized pages', async () => {
    const reader = broker(); const opened = await reader.open('owner', [selection]); const source = opened.sources[0]!;
    await expect(reader.close('foreign', opened.capability)).rejects.toMatchObject({ code: 'stale-binding' });
    await expect(reader.readPage('foreign', opened.capability, source.sourceId, { offset: '0', length: 2 })).rejects.toMatchObject({ code: 'stale-binding' });
    await expect(reader.readPage('owner', opened.capability, 'other', { offset: '0', length: 2 })).rejects.toThrow();
    await expect(reader.readPage('owner', opened.capability, source.sourceId, { offset: '0', length: 262145 })).rejects.toThrow();
    await reader.close('owner', opened.capability);
    await expect(reader.readPage('owner', opened.capability, source.sourceId, { offset: '0', length: 2 })).rejects.toMatchObject({ code: 'stale-binding' });
  });
  it('rejects replacement, links and overlapping app storage without input mutation', async () => {
    const reader = broker(); const before = await readFile(selection.path);
    const opened = await reader.open('owner', [selection]);
    await writeFile(join(base, 'new'), 'replacement'); await rename(join(base, 'new'), selection.path);
    await expect(reader.readPage('owner', opened.capability, opened.sources[0]!.sourceId, { offset: '0', length: 4 })).rejects.toMatchObject({ code: 'source-changed' });
    const alias = join(dirname(selection.path), 'alias.jsonl'); await symlink(selection.path, alias);
    await expect(reader.open('owner', [{ ...selection, path: alias }])).rejects.toThrow();
    await rm(alias); await link(selection.path, alias);
    await expect(reader.open('owner', [selection])).rejects.toThrow();
    const own = join(app, 'own.jsonl'); await writeFile(own, before);
    await expect(reader.open('owner', [{ ...selection, path: own }])).rejects.toThrow();
    expect(await readFile(own)).toEqual(before);
  });
  it('rejects cancellation before launch and cancellation while persisting namespaces', async () => {
    const early = new AbortController(); early.abort();
    await expect(broker().open('owner', [selection], early.signal)).rejects.toMatchObject({ code: 'cancelled' });
    let entered!: () => void; let finish!: () => void;
    const atRegistry = new Promise<void>(resolve => { entered = resolve; });
    const gate = new Promise<void>(resolve => { finish = resolve; });
    const normal = registry();
    const reader = broker({ getOrCreate: async (kind, key) => { entered(); await gate; return normal.getOrCreate(kind, key); } });
    const cancel = new AbortController(); const opening = reader.open('owner', [selection], cancel.signal);
    await atRegistry; cancel.abort(); finish();
    await expect(opening).rejects.toMatchObject({ code: 'cancelled' });
    expect((await reader.open('owner', [selection])).sources).toHaveLength(1);
  });
  it('bounds simultaneous work and suppresses an admission completed after disposal', async () => {
    let entered!: () => void; let finish!: () => void;
    const atRegistry = new Promise<void>(resolve => { entered = resolve; });
    const gate = new Promise<void>(resolve => { finish = resolve; }); const normal = registry();
    const reader = broker({ getOrCreate: async (kind, key) => { entered(); await gate; return normal.getOrCreate(kind, key); } });
    const first = reader.open('owner', [selection]); await atRegistry;
    const second = reader.open('owner', [selection]);
    await expect(reader.open('owner', [selection])).rejects.toMatchObject({ code: 'resource-limit' });
    const firstResult = expect(first).rejects.toMatchObject({ code: 'cancelled' });
    const secondResult = expect(second).rejects.toThrow();
    await reader.disposeSession('owner'); finish(); await Promise.all([firstResult, secondResult]);
  });
  it('suppresses admission disposed before native acquisition completes', async () => {
    const reader = broker();
    const opening = reader.open('owner', [selection]);
    const rejection = expect(opening).rejects.toMatchObject({ code: 'cancelled' });
    await reader.disposeSession('owner'); await rejection;
  });
  it('denies relative application storage while ignoring obsolete launcher configuration', () => {
    expect(() => new ReadBroker({ writeRoots: ['relative'], registry: registry() })).toThrow();
    expect(() => new ReadBroker({ executable: 'not-used', writeRoots: [app], registry: registry() })).not.toThrow();
  });
});

it('keeps native bigint stamps exact and detects content and identity changes', () => {
 const stamp = nativeFileStamp({ dev: 1n, ino: 9007199254740993n, size: 0n, mtimeNs: 0n, ctimeNs: 0n } as import('node:fs').BigIntStats);
 expect(stamp.inode).toBe('9007199254740993'); expect(sameFileStamp(stamp, { ...stamp })).toBe(true);
 expect(sameFileStamp(stamp, { ...stamp, inode: '9007199254740992' })).toBe(false);
 expect(sameFileStamp(stamp, { ...stamp, size: '1' })).toBe(false);
});
