/** Native selected-file capabilities; no Python, canonical runtime or executable source configuration. */
import { open, lstat, realpath, stat, type FileHandle } from 'node:fs/promises';
import { constants, type BigIntStats } from 'node:fs';
import { createHash, randomUUID } from 'node:crypto';
import { basename, dirname, isAbsolute, parse, relative, resolve, sep } from 'node:path';
import type { AdmittedSource, BytePage } from '@jai/fabric-explorer-contracts';
import type { NamespaceRegistry, OpenedSources, PageBrokerPort, SourceSelection } from './types.js';
import { EXCERPT_LIMIT, IMPORT_EXCERPT_LIMIT, type CompanionObservation, type DirectCapture, type ExcerptRequest, type ExcerptResult, type DirectSourceFile, type NativeFileStamp } from './direct-types.js';
import { parseRecordedJSON } from '../import/recorded-json.js';
import { recordedVersionId } from '../import/recorded-projection.js';

/** Fixed application storage and stable namespace owner. Legacy launcher fields are ignored. */
export interface ReadBrokerOptions {
  readonly writeRoots: readonly string[]; readonly registry: NamespaceRegistry;
  readonly cwd?: string; readonly executable?: string; readonly script?: string; readonly coreTools?: string; readonly verifierDirectory?: string;
  readonly onHelperClose?: (observation: HelperCloseObservation) => void;
}
/** Historical evidence shape; direct imports do not launch a helper. */
export interface HelperCloseObservation { readonly lifetime: number; readonly exitCode: number | null; readonly signal: string | null }
/** Fixed redacted source-admission failure. */
export class BrokerError extends Error {
  constructor(readonly code: 'cancelled' | 'read-failed' | 'resource-limit' | 'stale-binding' | 'source-changed', message: string) { super(message); this.name = 'BrokerError'; }
}
const TOTAL = 1024n * 1024n * 1024n;
const failure = () => new BrokerError('read-failed', 'Selected source is unavailable or unsafe.');
const changed = () => new BrokerError('source-changed', 'Selected file changed or was replaced; reopen sources to admit the new file.');
const hash = (value: unknown) => createHash('sha256').update(JSON.stringify(value)).digest('hex');
const identity = (info: BigIntStats) => [process.platform === 'win32' ? 'node-windows' : 'posix', String(info.dev), String(info.ino)];
/** Capture lossless identity, size and mutable content markers from a native handle.
 * @param info Native bigint file metadata.
 */
export function nativeFileStamp(info: BigIntStats): NativeFileStamp { return { device: String(info.dev), inode: String(info.ino), size: String(info.size), modified: String(info.mtimeNs), changed: String(info.ctimeNs) }; }
/** Compare exact stable source observation without converting native integers to Number.
 * @param a Earlier captured observation.
 * @param b Later captured observation.
 */
export function sameFileStamp(a: NativeFileStamp, b: NativeFileStamp): boolean { return a.device === b.device && a.inode === b.inode && a.size === b.size && a.modified === b.modified && a.changed === b.changed; }
const sameIdentity = (a: NativeFileStamp, b: NativeFileStamp) => a.device === b.device && a.inode === b.inode;
const within = (child: string, parent: string) => { const value = relative(parent, child); return value === '' || value !== '..' && !value.startsWith('..' + sep) && !isAbsolute(value); };
const cancelled = (signal?: AbortSignal) => { if (signal?.aborted) throw new BrokerError('cancelled', 'Source request cancelled.'); };
async function matchesRecordedCompanion(file: FileHandle, stamp: NativeFileStamp, request: ExcerptRequest): Promise<boolean> {
  const { rowOffset, rowLength, effectIndex } = request;
  const prefix = rowOffset > 0 ? 1 : 0;
  const bytes = Buffer.alloc(rowLength + prefix);
  let offset = 0;
  while (offset < bytes.length) {
    const { bytesRead } = await file.read(bytes, offset, bytes.length - offset, rowOffset - prefix + offset);
    if (!bytesRead) return false;
    offset += bytesRead;
  }
  if (!sameFileStamp(nativeFileStamp(await file.stat({ bigint: true })), stamp)) return false;
  if (prefix && bytes[0] !== 10 && bytes[0] !== 13) return false;
  const body = new TextDecoder('utf-8', { fatal: true, ignoreBOM: true }).decode(bytes.subarray(prefix));
  if (BigInt(rowOffset + rowLength) < BigInt(stamp.size) && !/[\r\n]$/.test(body)) return false;
  const line = body.replace(/(?:\r\n|\r|\n)$/, '');
  if (/[\r\n]/.test(line)) return false;
  const row = parseRecordedJSON(line, 'fabric') as Record<string, any>;
  const operation = row?.operations?.[0];
  if (row?.format !== 9n || row.protocol !== 'jai.governed-delivery/1'
      || !Array.isArray(row.operations) || row.operations.length !== 1 || operation?.op !== 'governed') return false;
  const { effects, message } = operation.data ?? {};
  const effect = Array.isArray(effects) ? effects[effectIndex] : undefined;
  if (!effect || !['register', 'decision-record'].includes(effect.op)
      || effect.manifest?.schema !== 'jai.lifecycle.manifest/2'
      || recordedVersionId(effect.manifest) !== request.versionId) return false;
  const material = effect.manifest.content?.record?.material;
  if (!Array.isArray(material) || material.filter(id => id === request.blobId).length !== 1
      || !Array.isArray(message?.attachments)) return false;
  const declarations = message.attachments.filter((item: Record<string, unknown> | null) => item?.blob_id === request.blobId);
  const eligible = message.attachments.filter((item: Record<string, unknown> | null) => item && material.includes(item.blob_id)
    && ['text/plain', 'text/markdown'].some(media => media === item.media_type));
  const declaration = declarations[0];
  return !!declaration && declarations.length === 1 && eligible.length === 1 && declaration === eligible[0]
    && declaration.media_type === request.media && declaration.byte_length === BigInt(request.byteLength)
    && ['public', 'internal', 'confidential', 'restricted'].some(kind => kind === declaration.classification)
    && typeof declaration.access_handle === 'string' && declaration.access_handle.length > 0;
}

interface Entry { readonly path: string; readonly projectPath: string; readonly file: FileHandle; readonly admitted: AdmittedSource; readonly initial: NativeFileStamp }
interface Group { readonly owner: string; readonly entries: readonly Entry[] }
/** Source handles establish authority after explicit selection; pathname observations grant no recursive read access. */
export class ReadBroker implements PageBrokerPort {
  private readonly groups = new Map<string, Group>(); private readonly closed = new Map<string, string>(); private readonly epochs = new Map<string, number>(); private operations = 0;
  constructor(private readonly options: ReadBrokerOptions) { if (!Array.isArray(options.writeRoots) || !options.writeRoots.length || options.writeRoots.some(path => !isAbsolute(path)) || typeof options.registry?.getOrCreate !== 'function') throw failure(); }
  private async work<T>(signal: AbortSignal | undefined, action: () => Promise<T>): Promise<T> {
    cancelled(signal); if (this.operations >= 2) throw new BrokerError('resource-limit', 'Reader work limit reached.'); this.operations++;
    try { return await action(); } catch (error) { if (error instanceof BrokerError) throw error; throw failure(); } finally { this.operations--; }
  }
  private owned(owner: string, capability: string): Group { const group = this.groups.get(capability); if (!group || group.owner !== owner) throw new BrokerError('stale-binding', 'Source capability is unavailable.'); return group; }
  private async observePath(path: string): Promise<void> {
    if (!isAbsolute(path) || path.split(/[\\/]/).includes('..')) throw failure();
    const root = parse(path).root; let current = root;
    for (const part of path.slice(root.length).split(sep).filter(Boolean)) { current = resolve(current, part); if ((await lstat(current)).isSymbolicLink()) throw failure(); }
  }
  private async overlap(path: string): Promise<void> {
    const parent = await realpath(dirname(path));
    for (const write of this.options.writeRoots) {
      const destination = await realpath(write);
      if (within(parent, destination) || within(destination, parent)) throw failure();
      const [a, b] = await Promise.all([stat(parent, { bigint: true }), stat(destination, { bigint: true })]);
      if (a.dev === b.dev && a.ino === b.ino) throw failure();
    }
  }
  private async acquire(path: string, expected?: NativeFileStamp, signal?: AbortSignal): Promise<{ file: FileHandle; stamp: NativeFileStamp }> {
    cancelled(signal); await this.observePath(path); await this.overlap(path);
    const before = await lstat(path, { bigint: true });
    const file = await open(path, constants.O_RDONLY | (constants.O_NOFOLLOW ?? 0) | (constants.O_NONBLOCK ?? 0));
    try {
      const info = await file.stat({ bigint: true }); const after = await lstat(path, { bigint: true }); const stamp = nativeFileStamp(info);
      if (!info.isFile() || info.nlink !== 1n || info.size > TOTAL || !before.isFile() || !after.isFile() || before.dev !== info.dev || before.ino !== info.ino || after.dev !== info.dev || after.ino !== info.ino) throw failure();
      if (expected && !sameIdentity(stamp, expected)) throw changed();
      cancelled(signal); return { file, stamp };
    } catch (error) { await file.close(); throw error; }
  }
  /** Admit explicit picker files and stable physical namespace associations, without reading content. */
  async open(owner: string, selections: readonly SourceSelection[], signal?: AbortSignal): Promise<OpenedSources> {
    const epoch = this.epochs.get(owner) ?? 0;
    return this.work(signal, async () => {
      if (!owner || !Array.isArray(selections) || selections.length < 1 || selections.length > 128 || this.groups.size >= 128) throw failure();
      const entries: Entry[] = []; let total = 0n;
      try {
        for (const selection of selections) {
          if (!['fabric', 'findings', 'audit'].includes(selection.family) || !isAbsolute(selection.projectPath)) throw failure();
          await this.observePath(selection.projectPath); const project = await stat(selection.projectPath, { bigint: true }); const parent = await stat(dirname(selection.path), { bigint: true });
          if (!project.isDirectory() || !parent.isDirectory()) throw failure();
          const acquired = await this.acquire(selection.path, undefined, signal);
          try {
            total += BigInt(acquired.stamp.size); if (total > TOTAL || selection.family === 'audit' && BigInt(acquired.stamp.size) > 100n * 1024n * 1024n) throw new BrokerError('resource-limit', 'Selected source byte limit exceeded.');
            const projectKey = identity(project), rootKey = identity(parent), name = basename(selection.path);
            const projectId = await this.options.registry.getOrCreate('project', hash(projectKey)); const rootId = await this.options.registry.getOrCreate('root', hash(rootKey)); const sourceId = await this.options.registry.getOrCreate('source', hash([projectKey, rootKey, name, selection.family]));
            if (entries.some(entry => entry.admitted.sourceId === sourceId)) throw failure();
            entries.push({ path: resolve(selection.path), projectPath: selection.projectPath, file: acquired.file, initial: acquired.stamp, admitted: { projectId, rootId, sourceId, family: selection.family, relativePath: name, readHandle: randomUUID() } });
          } catch (error) { await acquired.file.close(); throw error; }
        }
        cancelled(signal); if ((this.epochs.get(owner) ?? 0) !== epoch) throw new BrokerError('cancelled', 'Source request cancelled.');
        const capability = randomUUID(); this.groups.set(capability, { owner, entries }); return { capability, sources: entries.map(entry => ({ ...entry.admitted })) };
      } catch (error) { await Promise.all(entries.map(entry => entry.file.close())); throw error; }
    });
  }
  /** Return detached public descriptors only; paths and native handles remain main-owned. */
  catalog(owner: string, capability: string): readonly AdmittedSource[] { return this.owned(owner, capability).entries.map(entry => ({ ...entry.admitted })); }
  /** Open candidate source handles whose admitted leaf identities are checked before any bytes. */
  async captureDirect(owner: string, capability: string, sourceIds: readonly string[], signal?: AbortSignal): Promise<DirectCapture> {
    return this.work(signal, async () => {
      const group = this.owned(owner, capability); if (!sourceIds.length || sourceIds.length > 128 || new Set(sourceIds).size !== sourceIds.length) throw failure();
      const files: DirectSourceFile[] = []; let total = 0n; let excerptRemaining = IMPORT_EXCERPT_LIMIT;
      const companions = new Map<string, CompanionObservation>();
      let companionChanged = false;
      const dispose = async () => { await Promise.all(files.map(file => file.handle.close().catch(() => undefined))); };
      try {
        for (const sourceId of sourceIds) {
          const entry = group.entries.find(item => item.admitted.sourceId === sourceId); if (!entry) throw new BrokerError('stale-binding', 'Source capability is unavailable.');
          const acquired = await this.acquire(entry.path, entry.initial, signal);
          if (this.groups.get(capability) !== group) { await acquired.file.close(); throw new BrokerError('cancelled', 'Source capability was revoked.'); }
          total += BigInt(acquired.stamp.size);
          if (total > TOTAL) { await acquired.file.close(); throw new BrokerError('resource-limit', 'Selected source byte limit exceeded.'); }
          files.push({ admitted: { ...entry.admitted }, revisionId: randomUUID(), observedAt: new Date().toISOString(), stamp: acquired.stamp, handle: acquired.file });
        }
        this.owned(owner, capability); cancelled(signal);
        const companionKey = (sourceId: string, blobId: string) => JSON.stringify([sourceId, blobId]);
        const companionFailure = (error: unknown) => (error as NodeJS.ErrnoException)?.code === 'ENOENT' ? 'missing' as const : 'read-denied' as const;
        const sameCompanion = (a: CompanionObservation['state'], b: CompanionObservation['state']) =>
          typeof a === 'string' || typeof b === 'string' ? a === b : sameFileStamp(a, b);
        const observeCompanion = (sourceId: string, blobId: string, state: CompanionObservation['state']) => {
          const key = companionKey(sourceId, blobId);
          const prior = companions.get(key)?.state;
          if (prior !== undefined && !sameCompanion(prior, state)) companionChanged = true;
          companions.set(key, { sourceId, blobId, state });
        };
        const companionsUnchanged = async (previous: readonly CompanionObservation[]): Promise<boolean> => {
          this.owned(owner, capability); cancelled(signal);
          if (companionChanged) return false;
          for (const { sourceId, blobId, state } of previous) {
            const entry = group.entries.find(item => item.admitted.sourceId === sourceId);
            if (!entry || !sourceIds.includes(sourceId) || !/^[0-9a-f]{64}$/.test(blobId)) return false;
            let current: CompanionObservation['state'];
            try {
              const material = await this.acquire(entry.path + '.blobs/' + blobId, undefined, signal);
              try { current = material.stamp; } finally { await material.file.close(); }
            } catch (error) {
              cancelled(signal);
              current = companionFailure(error);
            }
            if (!sameCompanion(state, current)) return false;
          }
          this.owned(owner, capability); cancelled(signal);
          return true;
        };
        return { files, dispose, companionsUnchanged, companionObservations: () => [...companions.values()], validate: async () => {
          this.owned(owner, capability); cancelled(signal);
          for (const captured of files) { const entry = group.entries.find(item => item.admitted.sourceId === captured.admitted.sourceId)!; const current = await this.acquire(entry.path, entry.initial, signal); try { if (!sameFileStamp(current.stamp, captured.stamp)) throw changed(); } finally { await current.file.close(); } }
          this.owned(owner, capability); cancelled(signal);
        }, materialExcerpt: async request => {
          this.owned(owner, capability); cancelled(signal);
          const entry = group.entries.find(item => item.admitted.sourceId === request.sourceId && item.admitted.family === 'fabric');
          const captured = files.find(file => file.admitted.sourceId === request.sourceId);
          if (!entry || !captured || typeof request.blobId !== 'string' || !/^[0-9a-f]{64}$/.test(request.blobId)
              || typeof request.versionId !== 'string' || !/^[0-9a-f]{64}$/.test(request.versionId) || !Number.isSafeInteger(request.byteLength)
              || request.byteLength < 0 || !['text/plain', 'text/markdown'].includes(request.media)
              || !Number.isSafeInteger(request.rowOffset) || request.rowOffset < 0
              || !Number.isSafeInteger(request.rowLength) || request.rowLength < 1
              || !Number.isSafeInteger(request.effectIndex) || request.effectIndex < 0
              || BigInt(request.rowOffset) + BigInt(request.rowLength) > BigInt(captured.stamp.size)) return { kind: 'read-denied' };
          if (request.byteLength > EXCERPT_LIMIT) return { kind: 'oversized' };
          const proofBytes = request.rowLength + Number(request.rowOffset > 0);
          if (proofBytes + request.byteLength > excerptRemaining) return { kind: 'import-budget-exhausted' };
          excerptRemaining -= proofBytes;
          return this.work<ExcerptResult>(signal, async () => {
            let companionOpened = false;
            try {
              if (!await matchesRecordedCompanion(entry.file, captured.stamp, request)) return { kind: 'read-denied' };
              this.owned(owner, capability); cancelled(signal);
              if (request.byteLength > excerptRemaining) return { kind: 'import-budget-exhausted' };
              let material;
              try { material = await this.acquire(entry.path + '.blobs/' + request.blobId, undefined, signal); }
              catch (error) {
                cancelled(signal);
                const state = companionFailure(error);
                observeCompanion(request.sourceId, request.blobId, state);
                return { kind: state };
              }
              companionOpened = true;
              try {
                observeCompanion(request.sourceId, request.blobId, material.stamp);
                const size = BigInt(material.stamp.size);
                if (size > BigInt(EXCERPT_LIMIT)) return { kind: 'oversized' };
                if (size !== BigInt(request.byteLength)) return { kind: 'digest-mismatch' };
                if (request.byteLength > excerptRemaining) return { kind: 'import-budget-exhausted' };
                excerptRemaining -= request.byteLength;
                const bytes = Buffer.alloc(request.byteLength);
                let offset = 0;
                while (offset < bytes.length) {
                  cancelled(signal);
                  const { bytesRead } = await material.file.read(bytes, offset, bytes.length - offset, offset);
                  if (!bytesRead) return { kind: 'digest-mismatch' };
                  offset += bytesRead;
                }
                this.owned(owner, capability); cancelled(signal);
                if (!sameFileStamp(nativeFileStamp(await material.file.stat({ bigint: true })), material.stamp)
                    || createHash('sha256').update('jai.lifecycle.blob.v2\0').update(bytes).digest('hex') !== request.blobId) return { kind: 'digest-mismatch' };
                try { return { kind: 'text', text: new TextDecoder('utf-8', { fatal: true, ignoreBOM: true }).decode(bytes) }; }
                catch { return { kind: 'invalid-utf8' }; }
              } finally { await material.file.close(); }
            } catch (error) {
              if (companionOpened) companionChanged = true;
              if (signal?.aborted) throw error;
              return { kind: 'read-denied' };
            }
          }).catch(error => {
            companionChanged = true;
            throw error;
          });
        }, materialAvailable: async (sourceId, blobId) => {
          this.owned(owner, capability); cancelled(signal);
          const entry = group.entries.find(item => item.admitted.sourceId === sourceId);
          if (!entry || !sourceIds.includes(sourceId) || !/^[0-9a-f]{64}$/.test(blobId)) throw failure();
          let state = companions.get(companionKey(sourceId, blobId))?.state;
          if (state === undefined) {
            try {
              const material = await this.acquire(entry.path + '.blobs/' + blobId, undefined, signal);
              try { state = material.stamp; } finally { await material.file.close(); }
            } catch (error) {
              cancelled(signal);
              state = companionFailure(error);
            }
            observeCompanion(sourceId, blobId, state);
          }
          return typeof state !== 'string' && BigInt(state.size) <= 32n * 1024n * 1024n ? 'available' : 'missing';
        } };
      } catch (error) { await dispose(); throw error; }
    });
  }
  /** Read a bounded live page for trusted diagnostics; accepted source pages use the immutable archive. */
  async readPage(owner: string, capability: string, sourceId: string, page: { offset: string; length: number }, signal?: AbortSignal): Promise<BytePage> {
    if (!/^(?:0|[1-9][0-9]*)$/.test(page.offset) || !Number.isInteger(page.length) || page.length < 1 || page.length > 262144) throw failure();
    const capture = await this.captureDirect(owner, capability, [sourceId], signal);
    try { const source = capture.files[0]!; const offset = BigInt(page.offset); const size = BigInt(source.stamp.size); if (offset > size) throw failure(); const bytes = Buffer.alloc(Number(size - offset < BigInt(page.length) ? size - offset : BigInt(page.length))); let read = 0; while (read < bytes.length) { const result = await source.handle.read(bytes, read, bytes.length - read, Number(offset) + read); if (!result.bytesRead) throw changed(); read += result.bytesRead; } await capture.validate(); return { sourceId, offset: page.offset, pointer: '', sequence: null, byteLength: bytes.length, bytesBase64: bytes.toString('base64'), eof: offset + BigInt(bytes.length) === size }; } finally { await capture.dispose(); }
  }
  /** Close an owned admission; old immutable snapshots are independently owned by their session. */
  async close(owner: string, capability: string): Promise<void> { const group = this.groups.get(capability); if (!group) { if (this.closed.get(capability) === owner) return; throw new BrokerError('stale-binding', 'Source capability is unavailable.'); } if (group.owner !== owner) throw new BrokerError('stale-binding', 'Source capability is unavailable.'); this.groups.delete(capability); this.closed.set(capability, owner); if (this.closed.size > 4096) this.closed.delete(this.closed.keys().next().value!); await Promise.all(group.entries.map(entry => entry.file.close())); }
  /** Revoke late admissions and close every source capability owned by one renderer session. */
  async disposeSession(owner: string): Promise<void> { this.epochs.set(owner, (this.epochs.get(owner) ?? 0) + 1); for (const [key, group] of this.groups) if (group.owner === owner) await this.close(owner, key); }
}
