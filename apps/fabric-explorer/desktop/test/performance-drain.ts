// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Strict terminal evidence for the external observer's existing two-second descendant drain. */
import type { ResidentSample } from './performance-resident-window.js';
/** Existing shutdown observation budget; this does not grant another collection or retry window. */
export const PERFORMANCE_DRAIN_MS = 2000;
/** Host-clock acceptance context sampled after the raw observation was appended successfully. */
export interface PerformanceDrainContext {
  readonly rootExitObservedMs: number; readonly checkedMs: number; readonly stdioClosed: boolean; readonly samplerError: string | null;
}
/** Exact accepted sample; later observations cannot replace its terminal evidence. */
export interface PerformanceDrainWitness { readonly sample: ResidentSample; readonly checkedMs: number }
/**
 * Apply the same bounded certainty requirements to stopping and final completion.
 * @param sample Actual serialized collection, possibly absent before the first sample.
 * @param context Root exit, actual check time, inherited-pipe closure and sampler error.
 * @returns True only for a fully attributed empty population accepted within the original window.
 */
export function performanceDrainComplete(sample: ResidentSample | undefined, context: PerformanceDrainContext): boolean {
  return !!sample && sample.startedMs >= context.rootExitObservedMs && sample.endedMs <= context.checkedMs
    && context.checkedMs >= context.rootExitObservedMs && context.checkedMs <= context.rootExitObservedMs + PERFORMANCE_DRAIN_MS
    && context.stdioClosed && !context.samplerError && sample.selected.rootObserved && !sample.selected.rootPidReused
    && !sample.selected.processes.length && !sample.selected.collectionErrors.length && !sample.selected.attributedVanishedPids.length;
}
/**
 * Capture the first strict witness after successful raw append; preserve an already terminal sample unchanged.
 * @param current Previously accepted witness, or null while drain evidence remains incomplete.
 * @param sample Current append-only raw sample.
 * @param context Actual sampler acceptance context, with no synthetic deadline extension.
 * @returns Existing witness, a newly accepted exact sample, or null when collection must continue within its bound.
 */
export function performanceDrainWitness(current: PerformanceDrainWitness | null, sample: ResidentSample, context: PerformanceDrainContext): PerformanceDrainWitness | null {
  return current ?? (performanceDrainComplete(sample, context) ? { sample, checkedMs: context.checkedMs } : null);
}
