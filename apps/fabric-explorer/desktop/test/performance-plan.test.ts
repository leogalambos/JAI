// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Deterministic population and active-frame boundary tests; no real-clock waits. */
import { describe, expect, it } from 'vitest';
import { assessShellReadiness, SHELL_READY_BUDGET_MS, animationCoverage, coldImportCohort, importOverviewReady, nextPerformanceCaseAllowed, performanceCases, PERFORMANCE_POPULATIONS, remainingLImportWait } from './performance-plan.js';
describe('finite performance populations', () => {
  it('reserves cleanup inside the original L envelope without restarting time at Import', () => {
    expect(remainingLImportWait(100, 100, 240000)).toBe(225000);
    expect(remainingLImportWait(100, 10100, 240000)).toBe(215000);
    expect(remainingLImportWait(100, 225100, 240000)).toBe(0);
    expect(remainingLImportWait(100, 240100, 240000)).toBe(0);
    expect(() => remainingLImportWait(100, 99, 240000)).toThrow('monotonic');
    expect(() => remainingLImportWait(0, 0, Number.NaN)).toThrow('monotonic');
  });
  it('has fixed independent cold populations and exactly one optional endurance run', () => {
    const ordinary = performanceCases('qualification');
    expect(ordinary).toHaveLength(35); expect(new Set(ordinary.map(row => row.id)).size).toBe(35);
    expect(ordinary.filter(row => row.kind === 'shell')).toHaveLength(10);
    for (const tier of ['M', 'L']) expect(ordinary.filter(row => row.kind === 'import' && row.tier === tier)).toHaveLength(10);
    expect(performanceCases('all')).toHaveLength(36); expect(performanceCases('all').filter(row => row.kind === 'endurance')).toHaveLength(1);
    expect(performanceCases('smoke')).toMatchObject([{ kind: 'import', tier: 'S' }]);
    expect(performanceCases('endurance')).toHaveLength(1);
    expect(PERFORMANCE_POPULATIONS).toMatchObject({ warmups: 5, samples: 30, retention: 10, enduranceMs: 1800000 });
    expect(ordinary.every(row => row.watchdogMs > 0 && Number.isSafeInteger(row.watchdogMs))).toBe(true);
    expect(() => performanceCases('unknown' as never)).toThrow();
  });
  it('continues only unobserved animation and endurance without repeating completed populations', () => {
    expect(performanceCases('activity')).toEqual([
      { id: 'M-animation', kind: 'animation', tier: 'M', watchdogMs: 240000 },
      { id: 'M-endurance', kind: 'endurance', tier: 'M', watchdogMs: 2100000 },
    ]);
    expect(performanceCases('animation')).toEqual([{ id: 'M-animation', kind: 'animation', tier: 'M', watchdogMs: 240000 }]);
  });
  it('requires actual twenty-second boundary coverage rather than an invented expected frame count', () => {
    expect(animationCoverage({ startedMs: 100, endedMs: 20100, timestamps: [100, 20000, 20100] }).complete).toBe(true);
    expect(animationCoverage({ startedMs: 100, endedMs: 20099, timestamps: [100, 20099] }).complete).toBe(false);
    expect(animationCoverage({ startedMs: 100, endedMs: 20100, timestamps: [] }).complete).toBe(false);
    expect(animationCoverage({ startedMs: 100, endedMs: 20100, timestamps: [201, 20100] }).complete).toBe(false);
    expect(animationCoverage({ startedMs: 100, endedMs: 20100, timestamps: [100, 19999] }).complete).toBe(false);
    for (const timestamps of [[99, 20100], [100, 100], [200, 100], [NaN]]) expect(() => animationCoverage({ startedMs: 100, endedMs: 20100, timestamps })).toThrow();
  });
  it('requires ten successful cold samples for pass and skips only the already failed cold cohort', () => {
    const good = { status: 'collected' as const, durationMs: 10000 };
    expect(coldImportCohort('M', Array(10).fill(good))).toMatchObject({ status: 'pass', complete: true, attempted: 10, completed: 10, failed: 0, unexecuted: 0, skipRemainingColdImports: false, blockDependentCases: false });
    const failed = coldImportCohort('M', [{ ...good, durationMs: 10001 }, ...Array(9).fill({ status: 'blocked', durationMs: null })]);
    expect(failed).toMatchObject({ status: 'fail', complete: false, observedOnly: true, attempted: 1, completed: 1, failed: 1, unexecuted: 9, skipRemainingColdImports: true, blockDependentCases: false });
    expect(failed.observedStatistics?.count).toBe(1);
    expect(coldImportCohort('L', [{ ...good, durationMs: 45000 }]).skipRemainingColdImports).toBe(false);
    expect(coldImportCohort('L', [{ ...good, durationMs: 45001 }]).skipRemainingColdImports).toBe(true);
    expect(coldImportCohort('L', []).status).toBe('partial');
    for (const status of ['failed', 'interrupted'] as const) expect(coldImportCohort('M', [{ status, durationMs: null }])).toMatchObject({ status: 'fail', complete: false, blockDependentCases: true });
    expect(() => coldImportCohort('M', Array(11).fill(good))).toThrow();
  });
  it('does not launch a new case while an observed descendant drain is incomplete', () => {
    expect(nextPerformanceCaseAllowed(true)).toBe(true);
    expect(nextPerformanceCaseAllowed(false)).toBe(false);
  });
  it('requires the current visible layout and enabled Fit control rather than a residual canvas', () => {
    const ready = { quiet: true, canvasPresent: true, tablePresent: true, fitEnabled: true, visible: true, width: 800, height: 600 };
    expect(importOverviewReady(ready)).toBe(true);
    for (const changed of [{ quiet: false }, { canvasPresent: false }, { tablePresent: false }, { fitEnabled: false }, { visible: false }, { width: 0 }, { height: 0 }, { width: NaN }]) expect(importOverviewReady({ ...ready, ...changed })).toBe(false);
  });
});

it('compares exactly one S/M/L import without repeating boot, query or endurance populations', () => {
  const cases = performanceCases('imports');
  expect(cases).toEqual([
    { id: 'S-import', kind: 'import', tier: 'S', watchdogMs: 180000 },
    { id: 'M-import-1', kind: 'import', tier: 'M', watchdogMs: 180000 },
    { id: 'L-import-1', kind: 'import', tier: 'L', watchdogMs: 240000 },
  ]);
  expect(Math.ceil(cases.reduce((sum, row) => sum + row.watchdogMs + 2000, 0) / 1000) + 400).toBe(1006);
});

it('uses the owner-amended 3.5-second startup ceiling without changing observed samples or population completeness', () => {
  expect(SHELL_READY_BUDGET_MS).toBe(3500);
  expect(assessShellReadiness([3500], 1).status).toBe('pass');
  expect(assessShellReadiness([3500.001], 1).status).toBe('fail');
  expect(assessShellReadiness([3100], 10).status).toBe('partial');
});
