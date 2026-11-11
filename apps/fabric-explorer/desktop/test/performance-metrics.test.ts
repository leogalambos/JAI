// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Frozen rank, population and lifecycle boundaries; slow/missing samples cannot become passes. */
import { describe, expect, it } from 'vitest';
import { activeFrameIntervals, assessCloseRetention, assessMeasurements, measurementSummary, nearestRank, UI_TASK_BUDGET_MS } from './performance-metrics.js';
describe('qualification arithmetic', () => {
  it('applies the owner-adopted inclusive UI task budget without discarding slower observations', () => {
    expect(assessMeasurements([227], 1, UI_TASK_BUDGET_MS, 'maximum').status).toBe('pass');
    expect(assessMeasurements([250], 1, UI_TASK_BUDGET_MS, 'maximum').status).toBe('pass');
    expect(assessMeasurements([250.1], 1, UI_TASK_BUDGET_MS, 'maximum').status).toBe('fail');
    expect(assessMeasurements([], 1, UI_TASK_BUDGET_MS, 'maximum').status).toBe('partial');
  });
  it('uses sample29 of30 for p95 and preserves the original unsorted population', () => {
    const values = Array.from({ length: 30 }, (_, i) => 30 - i);
    expect(nearestRank(values)).toBe(29); expect(values[0]).toBe(30);
    expect(nearestRank([0])).toBe(0); expect(nearestRank([4, 2], 1)).toBe(4);
    expect(measurementSummary([4, 1, 3, 2])).toEqual({ count: 4, minimum: 1, median: 2.5, p95: 4, maximum: 4 });
    expect(measurementSummary([0])).toEqual({ count: 1, minimum: 0, median: 0, p95: 0, maximum: 0 });
  });
  it('rejects invalid units/populations instead of dropping bad samples', () => {
    for (const values of [[], [-1], [Infinity], [NaN]]) expect(() => nearestRank(values)).toThrow();
    for (const fraction of [0, -0.1, 1.1, NaN]) expect(() => nearestRank([1], fraction)).toThrow();
    expect(() => measurementSummary([])).toThrow();
    for (const n of [0, 1.5, Infinity]) expect(() => assessMeasurements([1], n, 10, 'p95')).toThrow();
    expect(() => assessMeasurements([1], 1, 0, 'maximum')).toThrow();
  });
  it('accepts inclusive thresholds and keeps missing samples or outliers visible', () => {
    expect(assessMeasurements([100], 1, 100, 'p95').status).toBe('pass');
    expect(assessMeasurements([], 30, 100, 'p95')).toMatchObject({ status: 'partial', complete: false, summary: null });
    expect(assessMeasurements([1], 30, 100, 'p95').status).toBe('partial');
    expect(assessMeasurements([200], 30, 100, 'p95').status).toBe('partial');
    expect(assessMeasurements([1, 200], 30, 100, 'maximum')).toMatchObject({ status: 'fail', complete: false, measured: 200 });
    expect(assessMeasurements([1, 1, 1, 1000], 4, 100, 'p95').status).toBe('fail');
    expect(assessMeasurements([1, 1], 1, 100, 'maximum').status).toBe('partial');
  });
  it('requires all ten settled cycles and treats zero baseline as unknown', () => {
    expect(assessCloseRetention([1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1150]).status).toBe('pass');
    expect(assessCloseRetention([1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1151]).status).toBe('fail');
    expect(assessCloseRetention([1000, 1200]).status).toBe('partial');
    expect(assessCloseRetention(Array(10).fill(0)).status).toBe('partial');
    expect(assessCloseRetention([]).percentageChange).toBeNull();
    for (const values of [[-1], [1.5], [Number.MAX_SAFE_INTEGER + 1]]) expect(() => assessCloseRetention(values)).toThrow();
  });
  it('retains a long frame rather than filtering stalls or sorting clock errors', () => {
    expect(activeFrameIntervals([0, 16, 400, 416])).toEqual([16, 384, 16]);
    expect(activeFrameIntervals([])).toEqual([]); expect(activeFrameIntervals([4])).toEqual([]);
    expect(() => activeFrameIntervals([10, 9])).toThrow(); expect(() => activeFrameIntervals([10, 10])).toThrow();
    expect(() => activeFrameIntervals([NaN])).toThrow();
  });
});
