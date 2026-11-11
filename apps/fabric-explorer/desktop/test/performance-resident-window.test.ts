// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Deterministic coverage and threshold boundaries; no real-time sleeps are used. */
import { describe, expect, it } from 'vitest';
import { ResidentTree } from './performance-process.js';
import { assessResidentWindow } from './performance-resident-window.js';
import { MEMORY_BUDGET_BYTES } from './performance-metrics.js';
const window = { startedMs: 0, endedMs: 200, budgetBytes: 1000, maximumGapMs: 100 };
function sample(startedMs: number, endedMs = startedMs + 1, residentBytes = 1000) {
  return { startedMs, endedMs, selected: new ResidentTree(10).select({ processes: [{ pid: 10, parentPid: 1, startTicks: '1', cpuTicks: '0', residentBytes }], errors: [], vanished: 0, vanishedPids: [] }) };
}
describe('coverage-aware app resident assessment', () => {
  it.each(['M', 'L'] as const)('enforces the approved %s gross budget inclusively while preserving partial coverage', tier => {
    const budgetBytes = MEMORY_BUDGET_BYTES[tier];
    expect(budgetBytes).toBe((tier === 'M' ? 2 : 4) * 1024 ** 3);
    expect(assessResidentWindow([sample(0, 1, budgetBytes), sample(100, 101, budgetBytes)], { ...window, budgetBytes }).status).toBe('pass');
    expect(assessResidentWindow([sample(0, 1, budgetBytes + 1), sample(100)], { ...window, budgetBytes }).status).toBe('fail');
    expect(assessResidentWindow([], { ...window, budgetBytes }).status).toBe('partial');
  });
  it('passes exactly at the gross RSS and sample-gap boundaries without baseline subtraction', () => {
    const result = assessResidentWindow([sample(0), sample(100)], window);
    expect(result.status).toBe('pass'); expect(result.peakBytes).toBe(1000); expect(result.maximumGapMs).toBe(100);
    expect(assessResidentWindow([sample(0, 100), sample(100, 200)], window).maximumCollectionMs).toBe(100);
    expect(assessResidentWindow([sample(0), sample(100, 101, 1001)], window).status).toBe('fail');
  });
  it('marks actual long sampling gaps, incomplete lifetimes and vanished processes as partial', () => {
    expect(assessResidentWindow([], window)).toMatchObject({ status: 'partial', peakBytes: null });
    expect(assessResidentWindow([sample(101)], window).reasons).toContain('sample-gap');
    expect(assessResidentWindow([sample(0)], window).reasons).toContain('sample-gap');
    expect(assessResidentWindow([sample(0, 101), sample(101)], window).reasons).toContain('collection-duration');
    for (const changed of [{ rootPresent: false }, { rootObserved: false }, { rootPidReused: true }, { ownershipComplete: false }, { collectionErrors: [{ pid: 10, code: 'EACCES' }] }]) {
      const first = sample(0); const result = assessResidentWindow([{ ...first, selected: { ...first.selected, ...changed } }, sample(100)], window);
      expect(result.status).toBe('partial'); expect(result.incompleteSamples).toBe(1);
    }
    const first = sample(0); first.selected.vanishedDuringCollection = 1; first.selected.attributedVanishedPids.push(20);
    expect(assessResidentWindow([first, sample(100)], window).reasons).toContain('app-processes-vanished-during-collection');
    expect(assessResidentWindow([{ ...first, selected: { ...first.selected, residentBytes: 1001 } }, sample(100)], window).status).toBe('fail');
  });
  it('rejects invalid or reordered evidence rather than sorting away timing defects', () => {
    for (const invalid of [{ ...window, budgetBytes: 0 }, { ...window, endedMs: 0 }, { ...window, maximumGapMs: NaN }]) expect(() => assessResidentWindow([], invalid)).toThrow();
    for (const samples of [[sample(-1)], [sample(200, 201)], [sample(100), sample(0)], [sample(0, 100), sample(99)]]) expect(() => assessResidentWindow(samples, window)).toThrow();
  });
  it('reports unrelated host churn without treating it as a missing app-process observation', () => {
    const first = sample(0); first.selected.vanishedDuringCollection = 1;
    expect(assessResidentWindow([first, sample(100)], window)).toMatchObject({ status: 'pass', vanishedDuringCollection: 1 });
  });
});
