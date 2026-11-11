/** Real filesystem state-store integration; source-like targets are never rewritten. */
import { afterEach, describe, expect, it } from 'vitest';
import { linkSync, mkdtempSync, readFileSync, readdirSync, renameSync, rmSync, symlinkSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { initializeApplicationPaths, StorageError } from '../src/shell/paths.js';
import { AppStateFile } from '../src/shell/app-state.js';
const roots: string[] = [];
afterEach(() => { for (const path of roots.splice(0)) rmSync(path, { recursive: true, force: true }); });
function fixture() {
  const base = mkdtempSync(join(tmpdir(), 'jai-app-state-')); roots.push(base);
  const paths = initializeApplicationPaths({ appData: () => base, setPath() {}, setLogsPath() {}, setCachePath() {}, setTemporaryEnvironment() {} });
  const validate = (value: unknown) => { if (!value || typeof value !== 'object' || Object.keys(value).join() !== 'value' || typeof (value as { value?: unknown }).value !== 'string') throw new StorageError('invalid-state'); return { value: (value as { value: string }).value }; };
  return { paths, store: new AppStateFile(paths, 'preferences.json', validate) };
}
describe('fixed app state filesystem integration', () => {
  it('does not create absent state and atomically replaces validated data', () => {
    const { paths, store } = fixture(); expect(store.read()).toBeNull(); expect(readdirSync(paths.userData)).toEqual([]);
    expect(store.write({ value: 'first' })).toEqual({ value: 'first' });
    store.write({ value: 'café' }); expect(store.read()).toEqual({ value: 'café' });
    expect(readdirSync(paths.userData)).toEqual(['preferences.json']);
    expect(() => store.write({ value: 'x'.repeat(4096) })).toThrowError(StorageError);
    expect(store.read()).toEqual({ value: 'café' });
  });
  it('rejects symlink and hardlink targets without modifying their bytes', () => {
    const { paths, store } = fixture(); const external = join(paths.root, 'source-like.json'); writeFileSync(external, 'source bytes');
    symlinkSync(external, join(paths.userData, 'preferences.json'));
    expect(() => store.write({ value: 'bad' })).toThrowError(StorageError); expect(() => store.read()).toThrowError(StorageError);
    rmSync(join(paths.userData, 'preferences.json')); linkSync(external, join(paths.userData, 'preferences.json'));
    expect(() => store.write({ value: 'bad' })).toThrowError(StorageError);
    expect(readFileSync(external, 'utf8')).toBe('source bytes');
  });
  it('rejects directory identity replacement and malformed JSON', () => {
    const first = fixture(); writeFileSync(join(first.paths.userData, 'preferences.json'), '{', { mode: 0o600 });
    expect(() => first.store.read()).toThrowError(StorageError);
    const second = fixture(); renameSync(second.paths.userData, second.paths.userData + '-old');
    symlinkSync(second.paths.userData + '-old', second.paths.userData, 'dir');
    expect(() => second.store.write({ value: 'bad' })).toThrowError(StorageError);
  });
});
