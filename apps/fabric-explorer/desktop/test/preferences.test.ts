/** Preference and namespace persistence use real private temporary directories. */
import { afterEach, describe, expect, it } from 'vitest';
import { mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { assertPreferences, DEFAULT_PREFERENCES, PersistentNamespaceRegistry, PreferenceStore } from '../src/shell/preferences.js';
import { initializeApplicationPaths, StorageError } from '../src/shell/paths.js';
const roots: string[] = [];
afterEach(() => { for (const path of roots.splice(0)) rmSync(path, { recursive: true, force: true }); });
function fixture() {
  const base = mkdtempSync(join(tmpdir(), 'jai-prefs-')); roots.push(base);
  return initializeApplicationPaths({ appData: () => base, setPath() {}, setLogsPath() {}, setCachePath() {}, setTemporaryEnvironment() {} });
}
describe('closed local preferences', () => {
  it('preserves defaults and validates each declared preference', () => {
    expect(assertPreferences(DEFAULT_PREFERENCES)).toEqual(DEFAULT_PREFERENCES);
    for (const theme of ['system', 'light', 'dark']) expect(assertPreferences({ version: 1, theme, reducedMotion: true }).theme).toBe(theme);
    for (const value of [{ ...DEFAULT_PREFERENCES, path: '/untrusted' }, { ...DEFAULT_PREFERENCES, version: 2 }, { ...DEFAULT_PREFERENCES, theme: 'remote' }]) expect(() => assertPreferences(value)).toThrowError(StorageError);
    let invoked = false; const getter = Object.defineProperty({}, 'version', { enumerable: true, get() { invoked = true; return 1; } });
    expect(() => assertPreferences(getter)).toThrowError(StorageError); expect(invoked).toBe(false);
  });
  it('reports malformed state without silently overwriting it', () => {
    const paths = fixture(); const store = new PreferenceStore(paths);
    expect(store.load()).toEqual({ preferences: DEFAULT_PREFERENCES, warning: null });
    writeFileSync(join(paths.userData, 'preferences.json'), '{', { mode: 0o600 });
    expect(store.load().warning).toBe('preferences-unavailable'); expect(readFileSync(join(paths.userData, 'preferences.json'), 'utf8')).toBe('{');
    store.save({ version: 1, theme: 'dark', reducedMotion: true });
    expect(new PreferenceStore(paths).load().preferences.theme).toBe('dark');
  });
  it('persists opaque namespace identities separately from source labels and paths', async () => {
    const paths = fixture(); const registry = new PersistentNamespaceRegistry(paths); const digest = 'a'.repeat(64);
    const id = await registry.getOrCreate('project', digest);
    expect(await registry.getOrCreate('project', digest)).toBe(id);
    expect(await new PersistentNamespaceRegistry(paths).getOrCreate('project', digest)).toBe(id);
    expect(await registry.getOrCreate('root', digest)).not.toBe(id);
    await expect(registry.getOrCreate('project', '../path')).rejects.toBeInstanceOf(StorageError);
    expect(readFileSync(join(paths.userData, 'namespaces.json'), 'utf8')).not.toContain(paths.root);
  });
  it('fails closed on a corrupt identity registry instead of generating replacement IDs', async () => {
    const paths = fixture(); writeFileSync(join(paths.userData, 'namespaces.json'), '{', { mode: 0o600 });
    await expect(new PersistentNamespaceRegistry(paths).getOrCreate('project', 'b'.repeat(64))).rejects.toBeInstanceOf(StorageError);
    expect(readFileSync(join(paths.userData, 'namespaces.json'), 'utf8')).toBe('{');
  });
});
