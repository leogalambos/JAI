/** Application-owned write destinations are initialized before Electron sessions or windows. */
import { constants, lstatSync, mkdirSync, realpathSync } from 'node:fs';
import { join, resolve } from 'node:path';

/** Exact private destinations; source roots are checked against all of them by the broker. */
export interface DesktopPaths {
  readonly root: string;
  readonly userData: string;
  readonly sessionData: string;
  readonly logs: string;
  readonly crashDumps: string;
  readonly temp: string;
  readonly cache: string;
}

/** Owned startup adapter; Electron-specific objects never enter the renderer API. */
export interface PathSettingsPort {
  /** Return the platform's trusted application-data base directory. */
  appData(): string;
  /** Override one Electron write destination before a session/window exists. */
  setPath(name: 'userData' | 'sessionData' | 'crashDumps' | 'temp', value: string): void;
  /** Override Electron's log location without enabling persistent source diagnostics. */
  setLogsPath(value: string): void;
  /** Set the fixed Chromium cache directory before runtime child creation. */
  setCachePath(value: string): void;
  /** Set inherited temporary locations for intrinsic children to the app-owned tree. */
  setTemporaryEnvironment(value: string): void;
}

/** Value-redacted app-state rejection; no selected path or source content is included. */
export class StorageError extends Error {
  /**
   * Construct a bounded storage failure.
   * @param code Maintainer-owned category, never an untrusted filename.
   * @returns A typed storage error.
   */
  constructor(readonly code: 'storage-unavailable' | 'unsafe-storage' | 'invalid-state' | 'state-limit') {
    super(code); this.name = 'StorageError';
  }
}

function privateDirectory(path: string): void {
  try { mkdirSync(path, { mode: 0o700 }); }
  catch (error) { if ((error as NodeJS.ErrnoException).code !== 'EEXIST') throw error; }
  const info = lstatSync(path);
  if (info.isSymbolicLink() || !info.isDirectory()) throw new StorageError('unsafe-storage');
  if (process.platform !== 'win32' && ((info.mode & 0o077) !== 0 || (process.getuid && info.uid !== process.getuid()))) throw new StorageError('unsafe-storage');
}

/**
 * Establish private fixed directories and configure every application write destination synchronously.
 * @param port Startup-only platform adapter; no window/session may have been created yet.
 * @returns Frozen absolute physical destinations for broker exclusion and app-only stores.
 * @throws {StorageError} For inaccessible, linked, nonprivate or non-directory application state.
 */
export function initializeApplicationPaths(port: PathSettingsPort): DesktopPaths {
  try {
    const requested = resolve(port.appData());
    mkdirSync(requested, { recursive: true, mode: 0o700 });
    const base = realpathSync.native(requested);
    const root = join(base, 'JAI Fabric Explorer'); privateDirectory(root);
    const paths: DesktopPaths = Object.freeze({ root, userData: join(root, 'user-data'), sessionData: join(root, 'session-data'), logs: join(root, 'logs'), crashDumps: join(root, 'crash-dumps'), temp: join(root, 'temp'), cache: join(root, 'cache') });
    for (const path of Object.values(paths)) if (path !== root) privateDirectory(path);
    port.setPath('userData', paths.userData); port.setPath('sessionData', paths.sessionData);
    port.setPath('crashDumps', paths.crashDumps); port.setPath('temp', paths.temp);
    port.setLogsPath(paths.logs); port.setCachePath(paths.cache); port.setTemporaryEnvironment(paths.temp);
    return paths;
  } catch (error) {
    if (error instanceof StorageError) throw error;
    throw new StorageError('storage-unavailable');
  }
}

/**
 * List every fixed write tree for source-root overlap rejection.
 * @param paths Initialized physical application destinations.
 * @returns Detached destination array; callers cannot expand the app's write surface.
 */
export function applicationWriteLocations(paths: DesktopPaths): readonly string[] { return Object.values(paths); }

/** Native final-component no-follow flag, or zero where the platform requires separate handle checks. */
export const APP_NOFOLLOW = constants.O_NOFOLLOW ?? 0;
