/** Bounded fixed-name application state; selected source trees are never write destinations. */
import { closeSync, constants, fstatSync, fsyncSync, lstatSync, openSync, readSync, realpathSync, renameSync, unlinkSync, writeFileSync } from 'node:fs';
import { randomUUID } from 'node:crypto';
import { join } from 'node:path';
import { APP_NOFOLLOW, StorageError } from './paths.js';
import type { DesktopPaths } from './paths.js';

/** Only these maintainer-owned files may be accessed through the state store. */
export type StateName = 'preferences.json' | 'namespaces.json';
const limits: Readonly<Record<StateName, number>> = { 'preferences.json': 4096, 'namespaces.json': 4 * 1024 * 1024 };

/** Fixed-directory atomic JSON store; validation does not grant filesystem authority. */
export class AppStateFile<T> {
  private readonly directories: readonly { path: string; dev: number; ino: number }[];
  private readonly path: string;

  /**
   * Bind a fixed app-owned state file to initialized physical directory identities.
   * @param paths Private destinations initialized before Electron windows/sessions.
   * @param name Exact maintained filename, never a renderer-selected path.
   * @param validate Closed validator returning a detached state value.
   * @throws {StorageError} For an unsafe directory or unsupported filename.
   */
  constructor(private readonly paths: DesktopPaths, private readonly name: StateName, private readonly validate: (value: unknown) => T) {
    if (!Object.hasOwn(limits, name)) throw new StorageError('unsafe-storage');
    this.path = join(paths.userData, name);
    this.directories = [paths.root, paths.userData].map(path => {
      const info = lstatSync(path);
      if (!info.isDirectory() || info.isSymbolicLink() || realpathSync.native(path) !== path) throw new StorageError('unsafe-storage');
      return { path, dev: info.dev, ino: info.ino };
    });
    this.checkDirectories();
  }

  private checkDirectories(): void {
    for (const directory of this.directories) {
      const info = lstatSync(directory.path);
      if (!info.isDirectory() || info.isSymbolicLink() || info.dev !== directory.dev || info.ino !== directory.ino || realpathSync.native(directory.path) !== directory.path) throw new StorageError('unsafe-storage');
      if (process.platform !== 'win32' && ((info.mode & 0o077) !== 0 || (process.getuid && info.uid !== process.getuid()))) throw new StorageError('unsafe-storage');
    }
  }

  private target(): void {
    try {
      const info = lstatSync(this.path);
      if (!info.isFile() || info.isSymbolicLink() || info.nlink !== 1) throw new StorageError('unsafe-storage');
      if (process.platform !== 'win32' && ((info.mode & 0o077) !== 0 || (process.getuid && info.uid !== process.getuid()))) throw new StorageError('unsafe-storage');
      if (info.size > limits[this.name]) throw new StorageError('state-limit');
    } catch (error) { if ((error as NodeJS.ErrnoException).code !== 'ENOENT') throw error; }
  }

  /**
   * Read one finite validated JSON state snapshot without creating a missing file.
   * @returns Detached validated state, or null for first-run absence.
   * @throws {StorageError} For unsafe links/identity changes, excessive bytes or malformed state.
   */
  read(): T | null {
    let handle: number | undefined;
    try {
      this.checkDirectories(); this.target();
      try { handle = openSync(this.path, constants.O_RDONLY | APP_NOFOLLOW); }
      catch (error) { if ((error as NodeJS.ErrnoException).code === 'ENOENT') return null; throw error; }
      const before = fstatSync(handle, { bigint: true });
      if (!before.isFile() || before.nlink !== 1n || before.size > BigInt(limits[this.name])) throw new StorageError('unsafe-storage');
      const bytes = Buffer.alloc(Number(before.size)); let offset = 0;
      while (offset < bytes.length) {
        const count = readSync(handle, bytes, offset, bytes.length - offset, offset);
        if (!count) throw new StorageError('invalid-state'); offset += count;
      }
      const after = fstatSync(handle, { bigint: true });
      if (before.dev !== after.dev || before.ino !== after.ino || before.size !== after.size || before.mtimeNs !== after.mtimeNs || before.ctimeNs !== after.ctimeNs) throw new StorageError('invalid-state');
      this.checkDirectories();
      return this.validate(JSON.parse(new TextDecoder('utf-8', { fatal: true }).decode(bytes)) as unknown);
    } catch (error) {
      if (error instanceof StorageError) throw error;
      throw new StorageError('invalid-state');
    } finally { if (handle !== undefined) closeSync(handle); }
  }

  /**
   * Atomically replace one bounded app-only file after closed validation.
   * @param value Candidate preference or namespace data; paths and arbitrary filenames are not accepted.
   * @returns Detached validated state written to the fixed destination.
   * @throws {StorageError} For invalid state, unsafe storage, oversized bytes or failed replacement.
   */
  write(value: unknown): T {
    let temporary: string | undefined; let handle: number | undefined;
    try {
      const state = this.validate(value); const bytes = Buffer.from(JSON.stringify(state) + '\n', 'utf8');
      if (bytes.length > limits[this.name]) throw new StorageError('state-limit');
      this.checkDirectories(); this.target();
      temporary = join(this.paths.userData, `.${this.name}-${randomUUID()}.tmp`);
      handle = openSync(temporary, constants.O_CREAT | constants.O_EXCL | constants.O_WRONLY | APP_NOFOLLOW, 0o600);
      writeFileSync(handle, bytes); fsyncSync(handle); closeSync(handle); handle = undefined;
      this.checkDirectories(); this.target(); renameSync(temporary, this.path); temporary = undefined;
      if (process.platform !== 'win32') { const directory = openSync(this.paths.userData, constants.O_RDONLY | APP_NOFOLLOW); try { fsyncSync(directory); } finally { closeSync(directory); } }
      return state;
    } catch (error) {
      if (error instanceof StorageError) throw error;
      throw new StorageError('storage-unavailable');
    } finally {
      if (handle !== undefined) closeSync(handle);
      if (temporary !== undefined) { try { unlinkSync(temporary); } catch { /* A failed private temporary cleanup must not redirect a write. */ } }
    }
  }
}
