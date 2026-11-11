// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Host PID lifetimes and gross RSS boundaries, including reparenting and missing observations. */
import { describe, expect, it } from 'vitest';
import { mkdtemp, mkdir, rm, writeFile, readFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { parseResidentProcess, readResidentPopulation, ResidentTree } from './performance-process.js';
function stat(pid = 10, parent = 1, start = '123', pages = 2) { const values = Array(22).fill('0'); values[0] = 'S'; values[1] = String(parent); values[11] = '5'; values[12] = '3'; values[19] = start; values[21] = String(pages); return `${pid} (command with ) parentheses) ${values.join(' ')}\n`; }
const row = (pid: number, parentPid: number, startTicks = '1', residentBytes = 4096) => ({ pid, parentPid, startTicks, residentBytes, cpuTicks: '0' });
const population = (...processes: ReturnType<typeof row>[]) => ({ processes, vanished: 0, vanishedPids: [], errors: [] });
describe('sampled Linux app memory', () => {
  it('decodes positional fields with command spaces and closing parentheses', () => {
    expect(parseResidentProcess(stat(), 4096)).toEqual({ pid: 10, parentPid: 1, startTicks: '123', cpuTicks: '8', residentBytes: 8192 });
    expect(parseResidentProcess(stat(10, 1, '123', 0), 65536).residentBytes).toBe(0);
    for (const value of ['invalid', stat().replace('123', '-1'), stat(10, -1), stat(10, 1, '123', -1)]) expect(() => parseResidentProcess(value, 4096)).toThrow();
    expect(() => parseResidentProcess(stat(), 0)).toThrow();
  });
  it('sums descendants rather than subtracting the Chromium baseline or counting its parent harness', () => {
    const tree = new ResidentTree(10); const result = tree.select(population(row(1, 0, '1', 1_000_000), row(20, 10), row(10, 1), row(30, 20), row(40, 1)));
    expect(result.residentBytes).toBe(12288); expect(result.processes.map(value => value.pid)).toEqual([20, 10, 30]);
    expect(result.ownershipComplete).toBe(true); expect(result.rootPresent).toBe(true);
  });
  it('retains an observed orphan and its children but excludes unrelated reused PID lifetimes', () => {
    const tree = new ResidentTree(10); tree.select(population(row(10, 1), row(20, 10)));
    const orphan = tree.select(population(row(20, 1), row(30, 20), row(10, 1, 'new-root')));
    expect(orphan.processes.map(value => value.pid)).toEqual([20, 30]); expect(orphan.observedOrphans).toEqual([20]); expect(orphan.rootPidReused).toBe(true);
    expect(tree.select(population(row(20, 1, 'unrelated'))).residentBytes).toBe(0);
  });
  it('does not manufacture a zero-memory pass when the root or population is unknown', () => {
    const tree = new ResidentTree(10);
    expect(tree.select(population()).ownershipComplete).toBe(false);
    const result = tree.select({ ...population(row(10, 1)), errors: [{ pid: 99, code: 'EACCES' }] });
    expect(result.ownershipComplete).toBe(false); expect(result.collectionErrors).toHaveLength(1);
    expect(() => tree.select(population(row(10, 1), row(10, 1)))).toThrow('Duplicate');
    expect(() => new ResidentTree(0)).toThrow();
  });
  it('reads actual filesystem stat fixtures and retains malformed/missing entries', async () => {
    const root = await mkdtemp(join(tmpdir(), 'jai-process-population-'));
    try {
      for (const name of ['10', '20', '30', 'self']) await mkdir(join(root, name));
      await writeFile(join(root, '10/stat'), stat()); await writeFile(join(root, '20/stat'), 'broken');
      const result = await readResidentPopulation(4096, root);
      expect(result.processes).toHaveLength(1); expect(result.vanished).toBe(1); expect(result.vanishedPids).toEqual([30]); expect(result.errors).toEqual([{ pid: 20, code: 'invalid-stat' }]);
      await expect(readResidentPopulation(4096, join(root, 'absent'))).rejects.toThrow();
    } finally { await rm(root, { recursive: true, force: true }); }
  });
  it('distinguishes observed app PID disappearance from unrelated host PID churn', () => {
    const tree = new ResidentTree(10); tree.select(population(row(10, 1), row(20, 10)));
    const result = tree.select({ ...population(row(10, 1)), vanished: 2, vanishedPids: [20, 99] });
    expect(result.vanishedDuringCollection).toBe(2); expect(result.attributedVanishedPids).toEqual([20]);
  });
  it.skipIf(process.platform !== 'linux')('correlates the actual current host process with its kernel lifetime', async () => {
    const actual = parseResidentProcess(await readFile('/proc/self/stat', 'utf8'), 4096);
    expect(actual.pid).toBe(process.pid); expect(BigInt(actual.startTicks)).toBeGreaterThan(0n);
    // The real test verifies field identity only; actual host page size is required for benchmark bytes.
    expect(actual.residentBytes).toBeGreaterThan(0);
  });
});
