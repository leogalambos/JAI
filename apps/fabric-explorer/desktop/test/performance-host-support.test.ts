// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Actual filesystem integrity plus controlled native-event and settle-window boundary tests. */
import { describe, expect, it } from 'vitest';
import { mkdtemp, mkdir, rm, symlink, writeFile } from 'node:fs/promises';
import { join } from 'node:path';
import { tmpdir } from 'node:os';
import { performanceEvent, performanceProcessExit, performanceSourceSnapshot, settledCloseRetention } from './performance-host-support.js';
import { ResidentTree } from './performance-process.js';
describe('external performance observer support', () => {
  it('parses only bounded closed data events without treating ordinary output as control', () => {
    expect(performanceEvent('ordinary runtime output')).toBeNull();
    expect(performanceEvent('JAI_PERF_EVENT {"name":"collected","monotonicNs":"123","value":null}')).toEqual({ name: 'collected', monotonicNs: '123', value: null });
    for (const body of ['{}', '{', '{"name":"bad name","monotonicNs":"1","value":null}', '{"name":"valid","monotonicNs":"-1","value":null}', '{"name":"valid","monotonicNs":"1","value":null,"extra":1}', ' '.repeat(65536)]) expect(() => performanceEvent('JAI_PERF_EVENT ' + body)).toThrow();
  });
  it('streams actual selected bytes and companion objects, detects mutation, and refuses linked data', async () => {
    const root = await mkdtemp(join(tmpdir(), 'jai-performance-source-'));
    try {
      const path = join(root, 'source.jsonl'); const companion = path + '.blobs'; await writeFile(path, '{}\n'); await mkdir(companion); const material = join(companion, 'a'.repeat(64)); await writeFile(material, Buffer.alloc(150000, 7));
      const selected = { sources: [{ family: 'fabric' as const, path, projectPath: root }], expected: { vertices: null, edges: null, findings: null }, revisions: [] };
      const before = await performanceSourceSnapshot(selected); expect(before.filter(row => row.digest)).toHaveLength(2);
      expect(await performanceSourceSnapshot(selected)).toEqual(before);
      await writeFile(material, 'changed'); expect(await performanceSourceSnapshot(selected)).not.toEqual(before);
      await rm(material); await symlink(path, material); await expect(performanceSourceSnapshot(selected)).rejects.toThrow('Nonlinked');
      await rm(material); await writeFile(join(companion, 'unexpected'), 'x'); await expect(performanceSourceSnapshot(selected)).rejects.toThrow('Unexpected');
      await expect(performanceSourceSnapshot({ ...selected, sources: [{ ...selected.sources[0]!, path: join(root, '.env') }] })).rejects.toThrow('JSON Lines');
    } finally { await rm(root, { recursive: true, force: true }); }
  });
  it('requires ten fully observed natural settle windows and keeps missing coverage partial', () => {
    const tree = new ResidentTree(10); const windows = Array.from({ length: 10 }, (_, i) => ({ cycle: i + 1, startedMs: i * 6000, endedMs: i * 6000 + 5000 }));
    const samples = windows.flatMap(window => Array.from({ length: 20 }, (_, i) => ({ startedMs: window.endedMs - 1000 + i * 50, endedMs: window.endedMs - 999 + i * 50, selected: tree.select({ processes: [{ pid: 10, parentPid: 1, startTicks: '1', cpuTicks: '0', residentBytes: window.cycle === 10 ? 1150 : 1000 }], vanished: 0, vanishedPids: [], errors: [] }) })));
    expect(settledCloseRetention(samples, windows).assessment.status).toBe('pass');
    expect(settledCloseRetention(samples.filter(row => row.startedMs < windows[9]!.startedMs), windows).assessment.status).toBe('partial');
    expect(settledCloseRetention(samples, windows.slice(1)).assessment).toMatchObject({ status: 'partial', baselineBytes: null, finalBytes: 1150 });
    const failed = samples.map(row => ({ ...row, selected: { ...row.selected, residentBytes: row.startedMs >= windows[9]!.startedMs ? 1151 : row.selected.residentBytes } }));
    expect(settledCloseRetention(failed, windows.filter(row => row.cycle !== 5)).assessment).toMatchObject({ status: 'fail', complete: false, baselineBytes: 1000, finalBytes: 1151 });
    expect(() => settledCloseRetention(samples, [{ cycle: 1, startedMs: 0, endedMs: 4999 }])).toThrow();
  });
  it('observes root exit without waiting indefinitely for an orphan-held stdio pipe', async () => {
    let exit: (code: number | null, signal: NodeJS.Signals | null) => void = () => {}; let closed: () => void = () => {};
    const observation = performanceProcessExit({ exit: callback => { exit = callback; }, error: () => {}, closed: callback => { closed = callback; } });
    let completed = false; void observation.exited.then(() => { completed = true; });
    exit(0, null); await Promise.resolve();
    expect(completed).toBe(true); expect(observation.stdioClosed()).toBe(false);
    closed(); expect(observation.stdioClosed()).toBe(true);
  });
  it('completes launch-error evidence without requiring a root exit event that may never occur', async () => {
    let error: (value: Error) => void = () => {};
    const observation = performanceProcessExit({ exit: () => {}, error: callback => { error = callback; }, closed: () => {} });
    error(new Error('launch rejected'));
    await expect(observation.exited).resolves.toEqual({ code: null, signal: null, launchError: 'launch rejected' });
    expect(observation.stdioClosed()).toBe(false);
  });
});
