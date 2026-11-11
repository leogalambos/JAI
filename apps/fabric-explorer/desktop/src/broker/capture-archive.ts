/** Main-owned immutable source cache; source pathnames never enter this module. */
import { constants, lstatSync, unlinkSync } from 'node:fs';
import { lstat, mkdir, mkdtemp, open, readdir, realpath, rmdir, unlink, type FileHandle } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import { isAbsolute, join } from 'node:path';
import type { BytePage, SourceRevision } from '@jai/fabric-explorer-contracts';
import type { CapturedSources } from './semantic-types.js';
import type { DirectArchiveStage, DirectSourceFile } from './direct-types.js';

const TOTAL = 1024n * 1024n * 1024n;
const PAGE = 256 * 1024;
const decimal = /^(0|[1-9][0-9]{0,19})$/;
function cancelled(signal?: AbortSignal): void { if (signal?.aborted) throw new Error('Candidate capture cancelled.'); }
type BaseIdentity = { device: bigint; inode: bigint; claimDevice: bigint; claimInode: bigint };
type ArchiveState = { active: number; initialized?: Promise<BaseIdentity>; claim?: BaseIdentity };
const destinations = new Map<string, ArchiveState>();
process.once('exit', () => {
  for (const [base, state] of destinations) if (state.active === 0 && state.claim) {
    try {
      const marker = join(base, '.active'); const info = lstatSync(marker, { bigint: true });
      if (info.isFile() && !info.isSymbolicLink() && info.nlink === 1n && info.dev === state.claim.claimDevice && info.ino === state.claim.claimInode) unlinkSync(marker);
    } catch { /* A stale/foreign marker is never removed as crash recovery. */ }
  }
});
type Cached = { file: FileHandle; size: bigint; modified: bigint; device: bigint; inode: bigint; path: string };

/** Known stale/in-use app cache condition with fixed recovery text and no native path values. */
export class CacheUnavailableError extends Error {
  /** Construct the one safe recovery diagnostic; arbitrary native failures never use this type. */
  constructor() {
    super('Capture cache is in use or stale; close other viewer instances and clear only the viewer temporary capture cache.');
    this.name = 'CacheUnavailableError';
  }
}

/** At most two independently owned source sets, each bounded to 1 GiB on private disk. */
export class CaptureArchiveStore {
  private readonly state: ArchiveState;

  /**
   * Allocate bounded private output descriptors for the single source-stream copy.
   * @param sources Admitted captures supplying exact IDs and captured lengths.
   * @param signal Optional cancellation before descriptor transfer.
   * @returns Owned staging set; adopt only after the worker has closed its writers.
   */
  async stageDirect(sources: readonly DirectSourceFile[], signal?: AbortSignal): Promise<DirectArchiveStage> {
    if (!sources.length || sources.length > 128 || this.state.active >= 2 || new Set(sources.map(source => source.admitted.sourceId)).size !== sources.length || sources.reduce((sum, source) => sum + BigInt(source.stamp.size), 0n) > TOTAL) throw new Error('Capture archive slot/source limit reached.');
    ++this.state.active; let directory: string | undefined; let disposed = false; let adopted = false;
    const outputs = new Map<string, FileHandle>(); const names: string[] = []; const identities = new Map<string, { path: string; device: bigint; inode: bigint; size: bigint }>(); const files = new Map<string, Cached>();
    const cleanup = async () => {
      if (disposed) return; disposed = true; let failure: unknown;
      for (const file of [...outputs.values(), ...Array.from(files.values(), entry => entry.file)]) try { await file.close(); } catch { /* transferred writer handles are detached */ }
      for (const name of names) try { await unlink(name); } catch (error) { if ((error as NodeJS.ErrnoException).code !== 'ENOENT') failure ??= error; }
      if (directory) try { await rmdir(directory); } catch (error) { failure ??= error; }
      --this.state.active; if (failure) throw failure;
    };
    try {
      const base = await this.initialize(); await this.verifyBase(base); cancelled(signal); directory = await mkdtemp(join(this.base, 'set-'));
      for (const source of sources) {
        cancelled(signal); await this.verifyBase(base); const name = join(directory, `source-${names.length}`); const file = await open(name, constants.O_CREAT | constants.O_EXCL | constants.O_RDWR | (constants.O_NOFOLLOW ?? 0), 0o600); names.push(name); outputs.set(source.admitted.sourceId, file);
        const info = await file.stat({ bigint: true }); identities.set(source.admitted.sourceId, { path: name, device: info.dev, inode: info.ino, size: BigInt(source.stamp.size) });
      }
      return { outputs, dispose: cleanup, adopt: async revisions => {
        if (disposed || adopted || revisions.length !== identities.size || new Set(revisions.map(source => source.sourceId)).size !== identities.size) throw new Error('Invalid archive adoption.');
        await this.verifyBase(base);
        try {
          for (const revision of revisions) {
            const expected = identities.get(revision.sourceId); if (!expected || BigInt(revision.byteLength) !== expected.size || !/^[0-9a-f]{64}$/.test(revision.digest)) throw new Error('Invalid captured revision.');
            const file = await open(expected.path, constants.O_RDONLY | (constants.O_NOFOLLOW ?? 0));
            try { const info = await file.stat({ bigint: true }); if (!info.isFile() || info.nlink !== 1n || info.dev !== expected.device || info.ino !== expected.inode || info.size !== expected.size) throw new Error('Archive identity changed.'); files.set(revision.sourceId, { file, path: expected.path, device: info.dev, inode: info.ino, size: info.size, modified: info.mtimeNs }); } catch (error) { await file.close(); throw error; }
          }
          adopted = true;
          return { dispose: cleanup, page: async (sourceId, offset, length) => {
            if (disposed || !decimal.test(offset) || !Number.isInteger(length) || length < 1 || length > PAGE) throw new Error('Invalid captured page request.');
            const cached = files.get(sourceId); if (!cached || BigInt(offset) > cached.size) throw new Error('Unknown captured source/range.'); await this.verifyBase(base);
            const verify = async () => { const info = await cached.file.stat({ bigint: true }); if (!info.isFile() || info.nlink !== 1n || info.dev !== cached.device || info.ino !== cached.inode || info.size !== cached.size || info.mtimeNs !== cached.modified) throw new Error('Immutable captured bytes changed.'); };
            await verify(); const count = Number(cached.size - BigInt(offset) < BigInt(length) ? cached.size - BigInt(offset) : BigInt(length)); const bytes = Buffer.alloc(count); let consumed = 0;
            while (consumed < count) { const read = await cached.file.read(bytes, consumed, count - consumed, Number(offset) + consumed); if (!read.bytesRead) throw new Error('Short immutable capture read.'); consumed += read.bytesRead; }
            await verify(); return { sourceId, pointer: '', sequence: null, offset, byteLength: bytes.length, bytesBase64: bytes.toString('base64'), eof: BigInt(offset) + BigInt(bytes.length) === cached.size };
          } };
        } catch (error) { await cleanup(); throw error; }
      } };
    } catch (error) { await cleanup(); throw error; }
  }

  /**
   * Bind an app-owned private cache destination; no source path is accepted.
   * @param base Absolute destination beneath main's declared app-owned storage tree.
   * @throws {Error} If the fixed application destination is relative.
   */
  constructor(private readonly base: string) {
    if (!isAbsolute(base)) throw new Error('Absolute app-owned capture destination required.');
    let state = destinations.get(base);
    if (!state) { state = { active: 0 }; destinations.set(base, state); }
    this.state = state;
  }

  private async initialize(): Promise<BaseIdentity> {
    if (!this.state.initialized) this.state.initialized = (async () => {
      await mkdir(this.base, { mode: 0o700 }).catch(error => { if ((error as NodeJS.ErrnoException).code !== 'EEXIST') throw error; });
      const info = await lstat(this.base, { bigint: true });
      if (!info.isDirectory() || info.isSymbolicLink() || (process.platform !== 'win32' && ((info.mode & 0o077n) !== 0n || info.uid !== BigInt(process.getuid!())))) throw new Error('Private app-owned capture directory required.');
      // The base is main-created storage, not a user-granted source root. This
      // check rejects replaced/linked app cache destinations before publication.
      if (await realpath(this.base) !== this.base) throw new Error('Linked capture destination denied.');
      const marker = join(this.base, '.active');
      const claim = await open(marker, constants.O_CREAT | constants.O_EXCL | constants.O_WRONLY | (constants.O_NOFOLLOW ?? 0), 0o600).catch(error => {
        if ((error as NodeJS.ErrnoException).code === 'EEXIST') throw new CacheUnavailableError();
        throw error;
      });
      try {
        const claimInfo = await claim.stat({ bigint: true });
        if ((await readdir(this.base)).some(name => name !== '.active')) throw new CacheUnavailableError();
        const identity = { device: info.dev, inode: info.ino, claimDevice: claimInfo.dev, claimInode: claimInfo.ino };
        this.state.claim = identity; return identity;
      } catch (error) { await unlink(marker); throw error; }
      finally { await claim.close(); }
    })();
    return this.state.initialized;
  }

  private async verifyBase(expected: BaseIdentity): Promise<void> {
    const current = await lstat(this.base, { bigint: true });
    if (!current.isDirectory() || current.isSymbolicLink() || current.dev !== expected.device || current.ino !== expected.inode) throw new Error('Capture cache identity changed.');
    const claim = await lstat(join(this.base, '.active'), { bigint: true });
    if (!claim.isFile() || claim.isSymbolicLink() || claim.nlink !== 1n || claim.dev !== expected.claimDevice || claim.ino !== expected.claimInode) throw new Error('Capture cache ownership changed.');
  }

  /**
   * Persist an entire candidate's immutable raw sources without whole-file heap copies.
   * @param sources Captured revisions declaring exact lengths and SHA256 digests.
   * @param page Helper-owned bounded page callback, never a live pathname reader.
   * @param signal Optional cancellation; only newly owned files are removed on failure.
   * @returns Independent archive whose owner must dispose it after its generation retires.
   * @throws {Error} For slot/size limits, cancellation, bytes/digest mismatch or disk failure.
   */
  async persist(sources: readonly SourceRevision[], page: (sourceId: string, offset: string, length: number, signal?: AbortSignal) => Promise<BytePage>, signal?: AbortSignal): Promise<CapturedSources> {
    cancelled(signal);
    if (this.state.active >= 2 || sources.length < 1 || sources.length > 128 || new Set(sources.map(source => source.sourceId)).size !== sources.length) throw new Error('Capture archive slot/source limit reached.');
    let total = 0n;
    for (const source of sources) {
      if (!decimal.test(source.byteLength) || !/^[0-9a-f]{64}$/.test(source.digest)) throw new Error('Invalid captured source metadata.');
      total += BigInt(source.byteLength);
    }
    if (total > TOTAL) throw new Error('Capture archive byte limit reached.');
    ++this.state.active;
    let directory: string | undefined;
    const owned: string[] = []; const files = new Map<string, Cached>(); const writing = new Set<FileHandle>();
    let disposed = false;
    const cleanup = async (): Promise<void> => {
      if (disposed) return; disposed = true;
      let first: unknown;
      for (const handle of [...writing, ...Array.from(files.values(), value => value.file)]) {
        try { await handle.close(); } catch (error) { first ??= error; }
      }
      for (const path of owned) { try { await unlink(path); } catch (error) { if ((error as NodeJS.ErrnoException).code !== 'ENOENT') first ??= error; } }
      if (directory) { try { await rmdir(directory); } catch (error) { first ??= error; } }
      --this.state.active;
      if (first) throw first;
    };
    try {
      const base = await this.initialize(); await this.verifyBase(base); cancelled(signal);
      directory = await mkdtemp(join(this.base, 'set-'));
      for (const source of sources) {
        cancelled(signal); await this.verifyBase(base);
        const path = join(directory, `source-${owned.length}`);
        const writer = await open(path, constants.O_CREAT | constants.O_EXCL | constants.O_RDWR | (constants.O_NOFOLLOW ?? 0), 0o600);
        writing.add(writer); owned.push(path);
        const digest = createHash('sha256'); const expected = BigInt(source.byteLength); let offset = 0n;
        do {
          cancelled(signal);
          const result = await page(source.sourceId, offset.toString(), PAGE, signal);
          const bytes = Buffer.from(result.bytesBase64, 'base64');
          if (result.sourceId !== source.sourceId || result.offset !== offset.toString() || bytes.toString('base64') !== result.bytesBase64 || bytes.length !== result.byteLength || bytes.length > PAGE || (bytes.length === 0 && !result.eof) || offset + BigInt(bytes.length) > expected || result.eof !== (offset + BigInt(bytes.length) === expected)) throw new Error('Captured source page mismatch.');
          digest.update(bytes);
          let written = 0;
          while (written < bytes.length) {
            const result = await writer.write(bytes, written, bytes.length - written, Number(offset) + written);
            if (result.bytesWritten <= 0) throw new Error('Capture cache write made no progress.');
            written += result.bytesWritten;
          }
          offset += BigInt(bytes.length);
        } while (offset < expected);
        if (digest.digest('hex') !== source.digest) throw new Error('Captured source digest mismatch.');
        const before = await writer.stat({ bigint: true });
        if (!before.isFile() || before.nlink !== 1n || before.size !== expected) throw new Error('Capture cache file mismatch.');
        await writer.close(); writing.delete(writer);
        const file = await open(path, constants.O_RDONLY | (constants.O_NOFOLLOW ?? 0)); writing.add(file);
        const info = await file.stat({ bigint: true });
        if (!info.isFile() || info.nlink !== 1n || info.size !== expected || info.dev !== before.dev || info.ino !== before.ino || info.mtimeNs !== before.mtimeNs) throw new Error('Capture cache identity changed.');
        files.set(source.sourceId, { file, size: info.size, modified: info.mtimeNs, device: info.dev, inode: info.ino, path }); writing.delete(file);
      }
      await this.verifyBase(base); cancelled(signal);
      return {
        page: async (sourceId, offset, length) => {
          if (disposed || !decimal.test(offset) || !Number.isInteger(length) || length < 1 || length > PAGE) throw new Error('Invalid captured page request.');
          const cached = files.get(sourceId); if (!cached || BigInt(offset) > cached.size) throw new Error('Unknown captured source/range.');
          await this.verifyBase(base);
          const check = async (): Promise<void> => {
            const info = await cached.file.stat({ bigint: true });
            if (!info.isFile() || info.nlink !== 1n || info.dev !== cached.device || info.ino !== cached.inode || info.size !== cached.size || info.mtimeNs !== cached.modified) throw new Error('Immutable captured bytes changed.');
          };
          await check(); const count = Number(cached.size - BigInt(offset) < BigInt(length) ? cached.size - BigInt(offset) : BigInt(length));
          const bytes = Buffer.alloc(count); let consumed = 0;
          while (consumed < count) {
            const result = await cached.file.read(bytes, consumed, count - consumed, Number(offset) + consumed);
            if (result.bytesRead <= 0) throw new Error('Short immutable capture read.'); consumed += result.bytesRead;
          }
          await check(); await this.verifyBase(base);
          return { sourceId, pointer: '', sequence: null, offset, bytesBase64: bytes.toString('base64'), byteLength: bytes.length, eof: BigInt(offset) + BigInt(bytes.length) === cached.size };
        },
        dispose: cleanup,
      };
    } catch (error) { await cleanup(); throw error; }
  }
}
