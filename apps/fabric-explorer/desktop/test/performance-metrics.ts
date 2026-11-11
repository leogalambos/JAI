// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Qualification arithmetic preserves incomplete populations and all slow observations. */

/** Owner-adopted S11 upper UI-task budget; the original optimization target remains separate. */
export const UI_TASK_BUDGET_MS = 250;
/** Preferred UI-task target, retained without treating it as the adopted acceptance threshold. */
export const UI_TASK_TARGET_MS = 200;

/** Owner-approved gross process-tree RSS ceilings; input and compact-storage limits remain separate. */
export const MEMORY_BUDGET_BYTES = Object.freeze({ M: 2 * 1024 ** 3, L: 4 * 1024 ** 3 });

/** Numeric observation summary; every value uses the caller's declared unit. */
export interface MeasurementSummary { readonly count: number; readonly minimum: number; readonly median: number; readonly p95: number; readonly maximum: number }
/** A measured threshold result is separate from complete sample coverage. */
export interface MeasurementVerdict { readonly status: 'pass' | 'fail' | 'partial'; readonly complete: boolean; readonly expectedSamples: number; readonly summary: MeasurementSummary | null; readonly budget: number; readonly measured: number | null }

function validate(values: readonly number[]): void {
  if (values.some(value => !Number.isFinite(value) || value < 0)) throw new Error('Measurements must be finite nonnegative values.');
}

/**
 * Calculate nearest-rank quantile without filtering observations or mutating input.
 * @param values Nonempty real samples in one declared unit.
 * @param fraction Quantile strictly above zero and at most one.
 * @returns Sorted sample at one-based rank ceil(fraction * count).
 * @throws {Error} For empty, negative/nonfinite samples or an invalid fraction.
 */
export function nearestRank(values: readonly number[], fraction = 0.95): number {
  validate(values);
  if (!values.length || !Number.isFinite(fraction) || fraction <= 0 || fraction > 1) throw new Error('Nonempty population and a valid quantile required.');
  return [...values].sort((a, b) => a - b)[Math.ceil(fraction * values.length) - 1]!;
}

/**
 * Summarize all recorded samples, preserving nearest-rank p95 and conventional median.
 * @param values Nonempty finite nonnegative samples, including slow or failed-budget observations.
 * @returns Count, minimum, median, p95 and maximum in the original unit.
 * @throws {Error} For invalid or empty input.
 */
export function measurementSummary(values: readonly number[]): MeasurementSummary {
  validate(values); if (!values.length) throw new Error('No observed samples.');
  const sorted = [...values].sort((a, b) => a - b); const middle = Math.floor(sorted.length / 2);
  return { count: sorted.length, minimum: sorted[0]!, median: sorted.length % 2 ? sorted[middle]! : (sorted[middle - 1]! + sorted[middle]!) / 2,
    p95: nearestRank(sorted), maximum: sorted.at(-1)! };
}

/**
 * Assess an upper budget while retaining missing samples as incomplete coverage.
 * @param values Observed samples only; no invented values for blocked operations.
 * @param expectedSamples Frozen population size after warmups.
 * @param budget Inclusive positive upper threshold in the same unit.
 * @param statistic Maximum for each-run budgets, or p95 for query/frame budgets.
 * @returns Explicit coverage; each-run violations fail immediately, while p95 requires its complete population.
 * @throws {Error} For invalid samples, population, threshold or statistic.
 */
export function assessMeasurements(values: readonly number[], expectedSamples: number, budget: number, statistic: 'maximum' | 'p95'): MeasurementVerdict {
  validate(values);
  if (!Number.isSafeInteger(expectedSamples) || expectedSamples < 1 || !Number.isFinite(budget) || budget <= 0 || !['maximum', 'p95'].includes(statistic)) throw new Error('Frozen positive sample count, budget and statistic required.');
  const summary = values.length ? measurementSummary(values) : null; const complete = values.length === expectedSamples;
  const measured = summary?.[statistic] ?? null;
  return { status: measured !== null && measured > budget && (complete || statistic === 'maximum') ? 'fail' : complete ? 'pass' : 'partial', complete, expectedSamples, summary, budget, measured };
}

/**
 * Assess the fixed ten-cycle close-retention boundary using gross resident bytes.
 * @param settledRss Exactly ten settled cycle samples for a complete result; first is the post-first-close baseline.
 * @returns Explicit coverage, baseline/final bytes and percentage change; zero baseline is unqualified.
 * @throws {Error} For negative, fractional, unsafe or nonfinite resident-byte samples.
 */
export function assessCloseRetention(settledRss: readonly number[]) {
  if (settledRss.some(value => !Number.isSafeInteger(value) || value < 0)) throw new Error('Resident byte samples must be nonnegative safe integers.');
  const baseline = settledRss[0] ?? null; const final = settledRss.at(-1) ?? null;
  const complete = settledRss.length === 10 && baseline !== null && baseline > 0;
  return { status: !complete ? 'partial' as const : BigInt(final!) * 100n <= BigInt(baseline!) * 115n ? 'pass' as const : 'fail' as const,
    complete, baselineBytes: baseline, finalBytes: final, percentageChange: baseline && final !== null ? (final - baseline) * 100 / baseline : null };
}

/**
 * Preserve every active-frame interval, including stalls, in observed order.
 * @param timestamps Ordered monotonic requestAnimationFrame timestamps in milliseconds.
 * @returns Adjacent intervals; fewer than two timestamps yields no measured interval.
 * @throws {Error} For nonfinite/negative values or repeated/backwards timestamps.
 */
export function activeFrameIntervals(timestamps: readonly number[]): number[] {
  validate(timestamps); const result: number[] = [];
  for (let index = 1; index < timestamps.length; index++) {
    const interval = timestamps[index]! - timestamps[index - 1]!;
    if (interval <= 0) throw new Error('Frame timestamps must advance monotonically.');
    result.push(interval);
  }
  return result;
}
