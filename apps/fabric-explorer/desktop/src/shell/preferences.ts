/** Closed view preferences and stable opaque namespaces live only in private application state. */
import { randomUUID } from 'node:crypto';
import { AppStateFile } from './app-state.js';
import { StorageError } from './paths.js';
import type { DesktopPaths } from './paths.js';
import type { NamespaceRegistry } from '../broker/types.js';

/** Local presentation preferences; no source paths, content, notes or authority fields are accepted. */
export interface Preferences { readonly version: 1; readonly theme: 'system' | 'light' | 'dark'; readonly reducedMotion: boolean }
/** First-run presentation defaults, detached from all selected source inputs. */
export const DEFAULT_PREFERENCES: Preferences = Object.freeze({ version: 1, theme: 'system', reducedMotion: false });

function plain(value: unknown): asserts value is Record<string, unknown> {
  if (!value || typeof value !== 'object' || Array.isArray(value) || ![null, Object.prototype].includes(Object.getPrototypeOf(value))) throw new StorageError('invalid-state');
  for (const key of Reflect.ownKeys(value)) {
    const item = Object.getOwnPropertyDescriptor(value, key);
    if (typeof key !== 'string' || !item || !('value' in item) || !item.enumerable) throw new StorageError('invalid-state');
  }
}

/**
 * Validate fixed view preferences without invoking accessors or retaining arbitrary fields.
 * @param value Candidate application-only preference record.
 * @returns Frozen detached preferences.
 * @throws {StorageError} For unknown fields/version, wrong types or executable object structure.
 */
export function assertPreferences(value: unknown): Preferences {
  plain(value);
  if (Object.keys(value).sort().join() !== 'reducedMotion,theme,version' || value.version !== 1 || !['system', 'light', 'dark'].includes(value.theme as string) || typeof value.reducedMotion !== 'boolean') throw new StorageError('invalid-state');
  return Object.freeze({ version: 1, theme: value.theme as Preferences['theme'], reducedMotion: value.reducedMotion });
}

/** App-only preference facade; malformed existing preferences are visible rather than silently rewritten. */
export class PreferenceStore {
  private readonly file: AppStateFile<Preferences>;
  /**
   * Bind the fixed preference file to the initialized private app directory.
   * @param paths Physical write destinations; no selected input path is accepted.
   */
  constructor(paths: DesktopPaths) { this.file = new AppStateFile(paths, 'preferences.json', assertPreferences); }
  /**
   * Load preferences without writing missing or malformed state.
   * @returns Preferences and an explicit bounded warning for malformed/unreadable state.
   * @throws {StorageError} For an unsafe application directory or linked target.
   */
  load(): { readonly preferences: Preferences; readonly warning: 'preferences-unavailable' | null } {
    try { return { preferences: this.file.read() ?? DEFAULT_PREFERENCES, warning: null }; }
    catch (error) {
      if (error instanceof StorageError && (error.code === 'invalid-state' || error.code === 'state-limit')) return { preferences: DEFAULT_PREFERENCES, warning: 'preferences-unavailable' };
      throw error;
    }
  }
  /**
   * Replace only the fixed presentation preference file.
   * @param value Closed preference record; no arbitrary file/path is accepted.
   * @returns Validated persisted preferences.
   * @throws {StorageError} For invalid data or unsafe/unavailable application storage.
   */
  save(value: unknown): Preferences { return this.file.write(value); }
}

interface NamespaceState { readonly version: 1; readonly entries: Readonly<Record<string, string>> }
function namespaceState(value: unknown): NamespaceState {
  plain(value);
  if (Object.keys(value).sort().join() !== 'entries,version' || value.version !== 1) throw new StorageError('invalid-state');
  plain(value.entries);
  const entries = Object.create(null) as Record<string, string>;
  if (Object.keys(value.entries).length > 20000) throw new StorageError('state-limit');
  for (const [key, id] of Object.entries(value.entries)) {
    if (!/^(project|root|source):[a-f0-9]{64}$/.test(key) || typeof id !== 'string' || !/^(project|root|source)-[a-f0-9-]{36}$/.test(id) || id.split('-')[0] !== key.split(':')[0]) throw new StorageError('invalid-state');
    entries[key] = id;
  }
  if (new Set(Object.values(entries)).size !== Object.keys(entries).length) throw new StorageError('invalid-state');
  return { version: 1, entries };
}

/** Persistent application-assigned namespaces; corruption never silently rebinds a project or source. */
export class PersistentNamespaceRegistry implements NamespaceRegistry {
  private readonly file: AppStateFile<NamespaceState>;
  private state: NamespaceState | undefined;
  /**
   * Bind opaque namespace persistence without storing raw paths or labels.
   * @param paths Initialized private application state locations.
   */
  constructor(paths: DesktopPaths) { this.file = new AppStateFile(paths, 'namespaces.json', namespaceState); }
  /**
   * Resolve or atomically persist one typed physical-identity namespace.
   * @param kind App-owned namespace class, not a canonical ledger identifier.
   * @param identityKey Exactly 64 lowercase SHA-256 hexadecimal digits computed by the broker.
   * @returns Stable opaque identifier across re-admissions and application sessions.
   * @throws {StorageError} For malformed/corrupt/excessive state or unavailable app storage.
   */
  async getOrCreate(kind: 'project' | 'root' | 'source', identityKey: string): Promise<string> {
    if (!['project', 'root', 'source'].includes(kind) || !/^[a-f0-9]{64}$/.test(identityKey)) throw new StorageError('invalid-state');
    this.state ??= this.file.read() ?? { version: 1, entries: Object.create(null) as Record<string, string> };
    const key = `${kind}:${identityKey}`; const existing = this.state.entries[key];
    if (existing) return existing;
    if (Object.keys(this.state.entries).length >= 20000) throw new StorageError('state-limit');
    const next = { version: 1 as const, entries: { ...this.state.entries, [key]: `${kind}-${randomUUID()}` } };
    this.state = this.file.write(next); return this.state.entries[key]!;
  }
}
