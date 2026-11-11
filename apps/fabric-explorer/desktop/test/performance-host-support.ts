// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Bounded source-integrity and native-event helpers for the external Linux performance observer. */
import { constants } from 'node:fs';
import { lstat, open, readdir } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import { basename, dirname } from 'node:path';
import type { PerformanceSourceSet } from './performance-corpus.js';
import type { ResidentSample } from './performance-resident-window.js';
import { assessCloseRetention, measurementSummary } from './performance-metrics.js';

/** Physical source entry; access timestamps are omitted because verification itself reads source bytes. */
export interface PerformanceSourceEntry { readonly path: string; readonly device: string; readonly inode: string; readonly mode: string; readonly size: string; readonly digest: string | null; readonly names: readonly string[] | null }
/** Native progress is data, not an instruction to execute code or launch another process. */
export interface PerformanceEvent { readonly name: string; readonly monotonicNs: string; readonly value: unknown }
/** Narrow owned event adapter; root exit and inherited stdio closure are deliberately separate. */
export interface PerformanceProcessEvents {
  /** Register the actual root-process exit event. */
  exit(callback: (code: number | null, signal: NodeJS.Signals | null) => void): void;
  /** Register a launch error, which need not emit an exit event. */
  error(callback: (error: Error) => void): void;
  /** Register closure of all child stdio streams, which an orphan may delay indefinitely. */
  closed(callback: () => void): void;
}
/**
 * Observe root exit independently from inherited pipe closure.
 * @param port Owned adapter over the launched child's events.
 * @returns Root completion promise and separately observable stdio closure.
 * @remarks A remaining inherited pipe must never defer the start of the bounded descendant drain.
 */
export function performanceProcessExit(port: PerformanceProcessEvents) {
  let closed = false;
  const exited = new Promise<{ code: number | null; signal: NodeJS.Signals | null; launchError: string | null }>(resolve => {
    port.exit((code, signal) => resolve({ code, signal, launchError: null }));
    port.error(error => resolve({ code: null, signal: null, launchError: error.message }));
  });
  port.closed(() => { closed = true; });
  return { exited, stdioClosed: () => closed };
}

/**
 * Parse a bounded complete native event line while leaving ordinary runtime output untouched.
 * @param line Complete stdout line from the fixed native child.
 * @returns Closed progress event, or null for a non-event line.
 * @throws {Error} For malformed, oversized or non-monotonic-clock event envelopes.
 */
export function performanceEvent(line: string): PerformanceEvent | null {
  if (!line.startsWith('JAI_PERF_EVENT ')) return null;
  if (Buffer.byteLength(line) > 65536) throw new Error('Native progress event exceeds its bound.');
  const value = JSON.parse(line.slice('JAI_PERF_EVENT '.length)) as Record<string, unknown>;
  if (!value || typeof value !== 'object' || Array.isArray(value) || Object.keys(value).sort().join() !== 'monotonicNs,name,value' || typeof value.name !== 'string' || !/^[a-z-]{1,64}$/.test(value.name) || typeof value.monotonicNs !== 'string' || !/^(0|[1-9][0-9]*)$/.test(value.monotonicNs)) throw new Error('Invalid native event envelope.');
  return value as unknown as PerformanceEvent;
}

/**
 * Hash explicit selected journals and canonical companion files using one bounded read buffer.
 * @param selected Maintainer-generated selection; no project-wide filesystem traversal occurs.
 * @returns Sorted source bytes/physical identities and selected-parent/companion directory entries.
 * @throws {Error} For links, unsupported source names, changed reads or unexpected companion names.
 * @remarks Run once per distinct corpus before/after the population, outside measured app lifetimes.
 */
export async function performanceSourceSnapshot(selected: PerformanceSourceSet): Promise<readonly PerformanceSourceEntry[]> {
  const files = new Set<string>(); const directories = new Set<string>();
  for (const source of selected.sources) {
    if (!basename(source.path).endsWith('.jsonl')) throw new Error('Generated JSON Lines source required.');
    files.add(source.path); directories.add(dirname(source.path));
    if (source.family === 'fabric') {
      const companion = source.path + '.blobs';
      try {
        const info = await lstat(companion); if (!info.isDirectory() || info.isSymbolicLink()) throw new Error('Regular companion directory required.');
        directories.add(companion);
        for (const name of await readdir(companion)) { if (!/^[0-9a-f]{64}$/.test(name)) throw new Error('Unexpected canonical companion name.'); files.add(companion + '/' + name); }
      } catch (error) { if ((error as NodeJS.ErrnoException).code !== 'ENOENT') throw error; }
    }
  }
  const result: PerformanceSourceEntry[] = [];
  for (const path of [...directories].sort()) {
    const info = await lstat(path, { bigint: true }); if (!info.isDirectory() || info.isSymbolicLink()) throw new Error('Nonlinked selected directory required.');
    result.push({ path, device: String(info.dev), inode: String(info.ino), mode: String(info.mode & 0o7777n), size: String(info.size), digest: null, names: (await readdir(path)).sort() });
  }
  const buffer = Buffer.alloc(65536);
  for (const path of [...files].sort()) {
    const before = await lstat(path, { bigint: true }); if (!before.isFile() || before.isSymbolicLink()) throw new Error('Nonlinked source file required.');
    const file = await open(path, constants.O_RDONLY | (constants.O_NOFOLLOW ?? 0)); const digest = createHash('sha256');
    try {
      const admitted = await file.stat({ bigint: true }); if (admitted.dev !== before.dev || admitted.ino !== before.ino) throw new Error('Source replaced before integrity read.');
      for (;;) { const { bytesRead } = await file.read(buffer, 0, buffer.length, null); if (!bytesRead) break; digest.update(buffer.subarray(0, bytesRead)); }
      const after = await file.stat({ bigint: true });
      if (admitted.dev !== after.dev || admitted.ino !== after.ino || admitted.size !== after.size || admitted.mtimeNs !== after.mtimeNs || admitted.ctimeNs !== after.ctimeNs) throw new Error('Source changed during integrity read.');
      result.push({ path, device: String(after.dev), inode: String(after.ino), mode: String(after.mode & 0o7777n), size: String(after.size), digest: digest.digest('hex'), names: null });
    } finally { await file.close(); }
  }
  return result.sort((left, right) => left.path < right.path ? -1 : left.path > right.path ? 1 : 0);
}

/**
 * Assess the last second of each fixed five-second close observation, retaining absent windows as partial.
 * @param samples Actual host-relative gross RSS samples.
 * @param windows Explicit native settle intervals converted to the same host clock.
 * @returns Natural settled medians, ten-cycle assessment and missing-window coverage.
 * @throws {Error} For malformed settle timing.
 */
export function settledCloseRetention(samples: readonly ResidentSample[], windows: readonly { readonly cycle: number; readonly startedMs: number; readonly endedMs: number }[]) {
  const settled: { cycle: number; rssBytes: number | null }[] = []; const coverage: { cycle: number; status: 'complete' | 'partial'; sampleCount: number; maximumGapMs: number }[] = [];
  for (const window of windows) {
    if (!Number.isInteger(window.cycle) || window.cycle < 1 || window.cycle > 10 || window.cycle <= (coverage.at(-1)?.cycle ?? 0) || !Number.isFinite(window.startedMs) || !Number.isFinite(window.endedMs) || window.endedMs - window.startedMs < 5000) throw new Error('Ordered fixed five-second settle windows required.');
    const start = window.endedMs - 1000; const rows = samples.filter(row => row.startedMs >= start && row.endedMs <= window.endedMs);
    let prior = start; let maximumGapMs = 0;
    for (const row of rows) { maximumGapMs = Math.max(maximumGapMs, row.startedMs - prior); prior = row.startedMs; }
    maximumGapMs = Math.max(maximumGapMs, window.endedMs - prior);
    const complete = rows.length >= 2 && maximumGapMs <= 100 && rows.every(row => row.selected.rootPresent && row.selected.ownershipComplete && !row.selected.rootPidReused && !row.selected.attributedVanishedPids.length);
    coverage.push({ cycle: window.cycle, status: complete ? 'complete' : 'partial', sampleCount: rows.length, maximumGapMs });
    settled.push({ cycle: window.cycle, rssBytes: complete ? measurementSummary(rows.map(row => row.selected.residentBytes)).median : null });
  }
  const assessment = assessCloseRetention(settled.flatMap(row => row.rssBytes === null ? [] : [row.rssBytes]));
  const complete = coverage.length === 10 && coverage.every(row => row.status === 'complete');
  const baselineBytes = settled.find(row => row.cycle === 1)?.rssBytes ?? null; const finalBytes = settled.find(row => row.cycle === 10)?.rssBytes ?? null;
  const endpointFailure = baselineBytes !== null && baselineBytes > 0 && finalBytes !== null && BigInt(finalBytes) * 100n > BigInt(baselineBytes) * 115n;
  return { settledCycles: settled, coverage, assessment: { ...assessment, status: endpointFailure ? 'fail' as const : complete ? assessment.status : 'partial' as const, complete,
    baselineBytes, finalBytes, percentageChange: baselineBytes && finalBytes !== null ? (finalBytes - baselineBytes) * 100 / baselineBytes : null } };
}
