/** Real filesystem startup checks; unit ports only record calls to the owned platform boundary. */
import { afterEach, describe, expect, it } from 'vitest';
import { chmodSync, lstatSync, mkdtempSync, mkdirSync, rmSync, symlinkSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { applicationWriteLocations, initializeApplicationPaths, StorageError } from '../src/shell/paths.js';
import type { PathSettingsPort } from '../src/shell/paths.js';

const roots: string[] = [];
afterEach(() => { for (const path of roots.splice(0)) rmSync(path, { recursive: true, force: true }); });
function fixture() {
  const base = mkdtempSync(join(tmpdir(), 'jai-desktop-paths-')); roots.push(base);
  const events: string[] = [];
  const port: PathSettingsPort = { appData: () => base, setPath: name => { events.push(name); }, setLogsPath: () => { events.push('logs'); }, setCachePath: () => { events.push('cache'); }, setTemporaryEnvironment: () => { events.push('environment'); } };
  return { base, port, events };
}

describe('application paths filesystem integration', () => {
  it('creates only fixed private trees before returning startup settings', () => {
    const { base, port, events } = fixture(); const paths = initializeApplicationPaths(port);
    expect(paths.root).toBe(join(base, 'JAI Fabric Explorer'));
    expect(Object.isFrozen(paths)).toBe(true);
    expect(applicationWriteLocations(paths)).toHaveLength(7);
    for (const path of applicationWriteLocations(paths)) {
      expect(lstatSync(path).isDirectory()).toBe(true);
      if (process.platform !== 'win32') expect(lstatSync(path).mode & 0o077).toBe(0);
    }
    expect(events).toEqual(['userData', 'sessionData', 'crashDumps', 'temp', 'logs', 'cache', 'environment']);
    expect(initializeApplicationPaths(port)).toEqual(paths);
  });

  it('rejects an app root file or symlink without writing through it', () => {
    const fileCase = fixture(); writeFileSync(join(fileCase.base, 'JAI Fabric Explorer'), 'unchanged');
    expect(() => initializeApplicationPaths(fileCase.port)).toThrowError(StorageError);
    const linkCase = fixture(); const target = join(linkCase.base, 'target'); mkdirSync(target);
    symlinkSync(target, join(linkCase.base, 'JAI Fabric Explorer'), 'dir');
    expect(() => initializeApplicationPaths(linkCase.port)).toThrowError(StorageError);
    expect(linkCase.events).toHaveLength(0);
  });

  it('rejects nonprivate existing app state instead of changing its permissions', () => {
    if (process.platform === 'win32') return;
    const { base, port } = fixture(); const root = join(base, 'JAI Fabric Explorer'); mkdirSync(root); chmodSync(root, 0o755);
    expect(() => initializeApplicationPaths(port)).toThrowError(StorageError);
    expect(lstatSync(root).mode & 0o777).toBe(0o755);
  });

  it('keeps storage failures value-redacted', () => {
    const error = new StorageError('unsafe-storage');
    expect(error.message).toBe('unsafe-storage'); expect(error.name).toBe('StorageError');
  });
});
