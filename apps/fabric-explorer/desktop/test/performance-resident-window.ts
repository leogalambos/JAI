// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Coverage-aware RSS assessment over actual externally sampled app descendants. */
import type { ResidentTree } from './performance-process.js';

/** Collection interval and actual attribution; all times use the same host monotonic clock. */
export interface ResidentSample {
  readonly startedMs: number;
  readonly endedMs: number;
  readonly selected: ReturnType<ResidentTree['select']>;
}
/** Coverage gaps cannot manufacture a memory pass; observed over-budget RSS is still a failure. */
export interface ResidentAssessment {
  readonly status: 'pass' | 'fail' | 'partial';
  readonly peakBytes: number | null;
  readonly sampleCount: number;
  readonly maximumGapMs: number;
  readonly maximumCollectionMs: number;
  readonly incompleteSamples: number;
  readonly vanishedDuringCollection: number;
  readonly attributedDisappearances: number;
  readonly reasons: readonly string[];
}

/**
 * Assess a bounded measurement interval without subtracting browser baseline or hiding missing samples.
 * @param samples Actual monotonically collected host observations in collection order.
 * @param window Measurement start/end on the host monotonic clock, byte budget and maximum sample gap.
 * @returns Gross peak, coverage diagnostics and a conservative sampled-memory verdict.
 * @throws {Error} For invalid budgets/times, overlapping collection or samples outside the window.
 * @remarks Sampling cannot observe processes born and exited wholly between observations.
 */
export function assessResidentWindow(samples: readonly ResidentSample[], window: { readonly startedMs: number; readonly endedMs: number; readonly budgetBytes: number; readonly maximumGapMs: number }): ResidentAssessment {
  if (![window.startedMs, window.endedMs, window.maximumGapMs].every(Number.isFinite) || window.startedMs < 0 || window.endedMs <= window.startedMs || window.maximumGapMs <= 0 || !Number.isSafeInteger(window.budgetBytes) || window.budgetBytes < 1) throw new Error('Valid monotonic window and positive RSS budget required.');
  let previousStart = window.startedMs; let previousEnd = window.startedMs; let peakBytes: number | null = null;
  let maximumGapMs = 0; let maximumCollectionMs = 0; let incompleteSamples = 0; let vanishedDuringCollection = 0; let attributedDisappearances = 0;
  for (const sample of samples) {
    if (![sample.startedMs, sample.endedMs].every(Number.isFinite) || sample.startedMs < previousEnd || sample.endedMs < sample.startedMs || sample.endedMs > window.endedMs || !Number.isSafeInteger(sample.selected.residentBytes) || sample.selected.residentBytes < 0 || !Number.isSafeInteger(sample.selected.vanishedDuringCollection) || sample.selected.vanishedDuringCollection < 0) throw new Error('Invalid or overlapping resident sample.');
    maximumGapMs = Math.max(maximumGapMs, sample.startedMs - previousStart);
    maximumCollectionMs = Math.max(maximumCollectionMs, sample.endedMs - sample.startedMs);
    previousStart = sample.startedMs; previousEnd = sample.endedMs;
    if (!sample.selected.rootPresent || !sample.selected.rootObserved || sample.selected.rootPidReused || !sample.selected.ownershipComplete || sample.selected.collectionErrors.length) incompleteSamples++;
    vanishedDuringCollection += sample.selected.vanishedDuringCollection;
    attributedDisappearances += sample.selected.attributedVanishedPids.length;
    if (sample.selected.processes.length) peakBytes = Math.max(peakBytes ?? 0, sample.selected.residentBytes);
  }
  maximumGapMs = Math.max(maximumGapMs, window.endedMs - previousStart);
  const reasons: string[] = [];
  if (!samples.length || peakBytes === null) reasons.push('missing-samples');
  if (maximumGapMs > window.maximumGapMs) reasons.push('sample-gap');
  if (maximumCollectionMs > window.maximumGapMs) reasons.push('collection-duration');
  if (incompleteSamples) reasons.push('incomplete-attribution');
  if (attributedDisappearances) reasons.push('app-processes-vanished-during-collection');
  if (peakBytes !== null && peakBytes > window.budgetBytes) reasons.push('rss-budget');
  return { status: reasons.includes('rss-budget') ? 'fail' : reasons.length ? 'partial' : 'pass', peakBytes, sampleCount: samples.length, maximumGapMs, maximumCollectionMs, incompleteSamples, vanishedDuringCollection, attributedDisappearances, reasons };
}
