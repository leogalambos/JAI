/** Project lookup integration tests use real directories; only native dialogs are owned edge ports. */
import { afterEach, describe, expect, it, vi } from 'vitest';
import { chmod, mkdir, mkdtemp, rm, symlink, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { createSourcePicker } from '../src/shell/source-picker.js';
import type { SourceFamily } from '@jai/fabric-explorer-contracts';
const temporary: string[] = [];
afterEach(async () => { await Promise.all(temporary.splice(0).map(path => rm(path, { recursive: true, force: true }))); });
async function fixture() {
  const project = await mkdtemp(join(tmpdir(), 'jai-source-picker-')); temporary.push(project);
  const dialogs = { project: vi.fn(async (): Promise<string | null> => project), files: vi.fn(async (_family: SourceFamily, _defaultPath: string): Promise<readonly string[] | null> => ['/manual/selected.jsonl']) };
  const picker = createSourcePicker(dialogs);
  const select = (family: SourceFamily = 'fabric', maximum = 128, signal = new AbortController().signal) => picker.files(family, project, maximum, signal);
  const put = async (relative: string) => { const path = join(project, relative); await writeFile(path, 'not parsed or validated'); return path; };
  return { project, dialogs, picker, select, put };
}
describe('project source picker', () => {
  it.each([-1, 129, 1.5, NaN])('rejects invalid source capacity %s before opening dialogs', async capacity => {
    const f = await fixture(); await expect(f.select('fabric', capacity)).rejects.toThrow('capacity'); expect(f.dialogs.files).not.toHaveBeenCalled();
  });
  it('propagates native dialog failure rather than presenting lookup as completed', async () => {
    const f = await fixture(); f.dialogs.files.mockRejectedValueOnce(new Error('Native selection unavailable'));
    await expect(f.select()).rejects.toThrow('Native selection unavailable');
  });
  it('returns all sorted direct canonical ledgers without parsing their contents or opening file dialogs', async () => {
    const f = await fixture(); await mkdir(join(f.project, '.fabric')); await mkdir(join(f.project, '.findings'));
    const b = await f.put('.fabric/b.jsonl'); const a = await f.put('.fabric/a.jsonl'); const finding = await f.put('.findings/review.jsonl');
    expect(await f.picker.project()).toBe(f.project);
    expect(await f.select()).toEqual([a, b]); expect(await f.select('findings')).toEqual([finding]); expect(f.dialogs.files).not.toHaveBeenCalled();
  });
  it('falls back only for the missing family and starts its dialog at the selected project', async () => {
    const f = await fixture(); await mkdir(join(f.project, '.fabric')); const fabric = await f.put('.fabric/one.jsonl');
    expect(await f.select()).toEqual([fabric]); expect(await f.select('findings')).toEqual(['/manual/selected.jsonl']);
    expect(f.dialogs.files).toHaveBeenCalledExactlyOnceWith('findings', f.project);
  });
  it('uses the available conventional directory for an empty or noncanonical manual fallback', async () => {
    const f = await fixture(); const family = join(f.project, '.fabric'); await mkdir(family); await f.put('.fabric/material.json'); await f.put('.fabric/notes.ndjson'); await mkdir(join(family, 'nested')); await f.put('.fabric/nested/hidden.jsonl');
    expect(await f.select()).toEqual(['/manual/selected.jsonl']); expect(f.dialogs.files).toHaveBeenCalledExactlyOnceWith('fabric', family);
  });
  it('never follows linked family directories or linked candidate files', async () => {
    const f = await fixture(); const outside = await mkdtemp(join(tmpdir(), 'jai-source-picker-outside-')); temporary.push(outside);
    await writeFile(join(outside, 'outside.jsonl'), '{}'); await symlink(outside, join(f.project, '.fabric'), 'dir');
    expect(await f.select()).toEqual(['/manual/selected.jsonl']); expect(f.dialogs.files).toHaveBeenLastCalledWith('fabric', f.project);
    await mkdir(join(f.project, '.findings')); await symlink(join(outside, 'outside.jsonl'), join(f.project, '.findings/link.jsonl'));
    expect(await f.select('findings')).toEqual(['/manual/selected.jsonl']); expect(f.dialogs.files).toHaveBeenLastCalledWith('findings', join(f.project, '.findings'));
  });
  it('falls back rather than truncating matching files beyond remaining source capacity', async () => {
    const f = await fixture(); const family = join(f.project, '.fabric'); await mkdir(family);
    const a = await f.put('.fabric/a.jsonl'); const b = await f.put('.fabric/b.jsonl');
    expect(await f.select('fabric', 2)).toEqual([a, b]); expect(await f.select('fabric', 1)).toEqual(['/manual/selected.jsonl']);
    expect(f.dialogs.files).toHaveBeenCalledExactlyOnceWith('fabric', family);
    expect(await f.select('fabric', 0)).toEqual(['/manual/selected.jsonl']);
  });
  it('uses all 128 eligible sources at the admission boundary and falls back at 129', async () => {
    const f = await fixture(); const family = join(f.project, '.fabric'); await mkdir(family);
    const sources = await Promise.all(Array.from({ length: 129 }, (_, index) => f.put(`.fabric/source-${index}.jsonl`)));
    expect(await f.select()).toEqual(['/manual/selected.jsonl']);
    await rm(sources.pop()!); expect(await f.select()).toEqual(sources.sort()); expect(f.dialogs.files).toHaveBeenCalledOnce();
  });
  it('does not use a partial list when directory enumeration exceeds its finite entry bound', async () => {
    const f = await fixture(); const family = join(f.project, '.fabric'); await mkdir(family);
    const source = await f.put('.fabric/real.jsonl');
    for (let offset = 0; offset < 4096; offset += 64) await Promise.all(Array.from({ length: 64 }, (_, index) => f.put(`.fabric/unrelated-${offset + index}.txt`)));
    expect(await f.select()).toEqual(['/manual/selected.jsonl']); expect(f.dialogs.files).toHaveBeenCalledExactlyOnceWith('fabric', family);
    await rm(join(family, 'unrelated-0.txt'));
    expect(await f.select()).toEqual([source]); expect(f.dialogs.files).toHaveBeenCalledOnce();
  });
  it('keeps audit explicit even when ordinary family ledgers are discoverable', async () => {
    const f = await fixture(); await mkdir(join(f.project, '.fabric')); await f.put('.fabric/audit.jsonl');
    expect(await f.select('audit')).toEqual(['/manual/selected.jsonl']); expect(f.dialogs.files).toHaveBeenCalledExactlyOnceWith('audit', f.project);
  });
  it('preserves manual cancellation and does not open fallback after selection cancellation', async () => {
    const f = await fixture(); f.dialogs.files.mockResolvedValueOnce(null);
    expect(await f.select()).toBeNull();
    const abort = new AbortController(); abort.abort(); expect(await f.select('findings', 128, abort.signal)).toBeNull(); expect(f.dialogs.files).toHaveBeenCalledOnce();
    const inFlight = new AbortController(); const selection = f.select('fabric', 128, inFlight.signal); inFlight.abort(); expect(await selection).toBeNull(); expect(f.dialogs.files).toHaveBeenCalledOnce();
  });
  it('treats a non-directory conventional path as lookup failure and retains the project default', async () => {
    const f = await fixture(); await f.put('.fabric');
    expect(await f.select()).toEqual(['/manual/selected.jsonl']); expect(f.dialogs.files).toHaveBeenCalledExactlyOnceWith('fabric', f.project);
  });
  it.skipIf(process.platform === 'win32' || process.getuid?.() === 0)('falls back after an actual denied directory read without changing source contents', async () => {
    const f = await fixture(); const family = join(f.project, '.fabric'); await mkdir(family); await f.put('.fabric/one.jsonl'); await chmod(family, 0o000);
    try { expect(await f.select()).toEqual(['/manual/selected.jsonl']); expect(f.dialogs.files).toHaveBeenCalledExactlyOnceWith('fabric', f.project); }
    finally { await chmod(family, 0o700); }
  });
});
