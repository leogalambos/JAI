// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Fixed, finite native qualification populations; watchdogs are not acceptance budgets. */
import { assessMeasurements, measurementSummary } from './performance-metrics.js';

/** Prepared canonical corpus tier; none may be replaced with a projection-only fixture. */
export type PerformanceTier = 'S' | 'M' | 'L';
/** Each native case runs in a fresh app process; retention/endurance deliberately reuse that process internally. */
export type PerformanceCaseKind = 'blank' | 'shell' | 'import' | 'queries' | 'animation' | 'retention' | 'faults' | 'endurance';
/** Explicit operator run selection, permitting a short smoke before the expensive population. */
export type PerformanceMode = 'smoke' | 'qualification' | 'endurance' | 'activity' | 'animation' | 'imports' | 'all';
/** One immutable case definition, including its total diagnostic lifetime. */
export interface PerformanceCase { readonly id: string; readonly kind: PerformanceCaseKind; readonly tier: PerformanceTier | null; readonly watchdogMs: number }
/** Host-created native input; executable paths are fixed by the compiled composition, never by a selected source. */
export interface NativePerformanceInput {
  readonly format: 'jai.fabric-explorer.performance-case/1';
  readonly definition: PerformanceCase;
  readonly ordinal: number;
  readonly total: number;
  readonly manifest: string | null;
  readonly mode?: 'smoke';
  readonly rendererCpuProfile?: true;
}
/** Warmups and timed sample counts are fixed independently for every query metric. */
export const PERFORMANCE_POPULATIONS = Object.freeze({ warmups: 5, samples: 30, shell: 10, imports: 10, retention: 10, settleMs: 5000, animationMs: 20000, enduranceMs: 1800000, queryWatchdogMs: 15000 });

/** Owner-amended cold shell ceiling; original three-second observations remain historical evidence. */
export const SHELL_READY_BUDGET_MS = 3500;

/**
 * Assess actual spawn-to-ready observations under the owner-adopted ceiling.
 * @param values Original unmodified elapsed milliseconds.
 * @param expected Required fresh-launch population size.
 * @returns Existing finite measurement assessment; missing observations remain partial.
 */
export function assessShellReadiness(values: readonly number[], expected: number) { return assessMeasurements(values, expected, SHELL_READY_BUDGET_MS, 'maximum'); }

/** Fixed tail inside the existing L case envelope for settle, verification, close and report. */
export const L_IMPORT_TAIL_MS = 15000;
/**
 * Use the remaining existing L diagnostic case window without resetting its clock or acceptance budget.
 * @param caseStartedMs Monotonic time when the native case watchdog was armed.
 * @param nowMs Current monotonic time immediately before Import.
 * @param watchdogMs Existing declared total case envelope, unchanged by this calculation.
 * @returns Nonnegative remaining diagnostic import wait after the fixed tail reserve.
 * @throws {Error} For invalid clocks or case bounds.
 */
export function remainingLImportWait(caseStartedMs: number, nowMs: number, watchdogMs: number): number {
  if (![caseStartedMs, nowMs, watchdogMs].every(Number.isFinite) || caseStartedMs < 0 || nowMs < caseStartedMs || watchdogMs <= 0) throw new Error('Valid monotonic case clocks and envelope required.');
  return Math.max(0, watchdogMs - (nowMs - caseStartedMs) - L_IMPORT_TAIL_MS);
}

/**
 * Produce an ordered finite run without retries or implicit repeat populations.
 * @param mode Explicit smoke, ordinary qualification, endurance-only, activity/import comparison or complete selection.
 * @returns Fixed case IDs, required tiers and diagnostic lifetime upper bounds.
 * @throws {Error} For an unknown mode.
 */
export function performanceCases(mode: PerformanceMode): readonly PerformanceCase[] {
  if (!['smoke', 'qualification', 'endurance', 'activity', 'animation', 'imports', 'all'].includes(mode)) throw new Error('Unknown performance run mode.');
  if (mode === 'imports') return [{ id: 'S-import', kind: 'import', tier: 'S', watchdogMs: 180000 }, { id: 'M-import-1', kind: 'import', tier: 'M', watchdogMs: 180000 }, { id: 'L-import-1', kind: 'import', tier: 'L', watchdogMs: 240000 }];
  if (mode === 'smoke') return [{ id: 'S-smoke', kind: 'import', tier: 'S', watchdogMs: 180000 }];
  if (mode === 'endurance') return [{ id: 'M-endurance', kind: 'endurance', tier: 'M', watchdogMs: 2100000 }];
  if (mode === 'animation') return [{ id: 'M-animation', kind: 'animation', tier: 'M', watchdogMs: 240000 }];
  if (mode === 'activity') return [...performanceCases('animation'), ...performanceCases('endurance')];
  const cases: PerformanceCase[] = [{ id: 'blank-runtime', kind: 'blank', tier: null, watchdogMs: 30000 }];
  for (let i = 1; i <= 10; i++) cases.push({ id: `empty-shell-${i}`, kind: 'shell', tier: null, watchdogMs: 30000 });
  cases.push({ id: 'S-import', kind: 'import', tier: 'S', watchdogMs: 180000 });
  for (const tier of ['M', 'L'] as const) for (let i = 1; i <= 10; i++) cases.push({ id: `${tier}-import-${i}`, kind: 'import', tier, watchdogMs: tier === 'M' ? 180000 : 240000 });
  cases.push({ id: 'M-queries', kind: 'queries', tier: 'M', watchdogMs: 2340000 });
  cases.push({ id: 'M-retention', kind: 'retention', tier: 'M', watchdogMs: 1500000 });
  cases.push({ id: 'M-faults', kind: 'faults', tier: 'M', watchdogMs: 600000 });
  if (mode === 'all') cases.push(...performanceCases('endurance'));
  return cases;
}

/**
 * Assess the complete active animation boundary independently of the number of frames that arrived.
 * @param observation Actual start/end and ordered animation-frame timestamps in milliseconds.
 * @returns Complete duration coverage, preserving empty/short/interrupted observations as incomplete.
 * @throws {Error} For invalid clocks or timestamps outside the observation boundary.
 */
export function animationCoverage(observation: { readonly startedMs: number; readonly endedMs: number; readonly timestamps: readonly number[] }) {
  if (![observation.startedMs, observation.endedMs, ...observation.timestamps].every(value => Number.isFinite(value) && value >= 0) || observation.endedMs < observation.startedMs || observation.timestamps.some((value, index) => value < observation.startedMs || value > observation.endedMs || index > 0 && value <= observation.timestamps[index - 1]!)) throw new Error('Invalid active animation clock evidence.');
  const durationMs = observation.endedMs - observation.startedMs;
  const firstGapMs = observation.timestamps.length ? observation.timestamps[0]! - observation.startedMs : durationMs;
  const lastGapMs = observation.timestamps.length ? observation.endedMs - observation.timestamps.at(-1)! : durationMs;
  return { complete: durationMs >= PERFORMANCE_POPULATIONS.animationMs && observation.timestamps.length >= 2 && firstGapMs <= 100 && lastGapMs <= 100,
    durationMs, firstGapMs, lastGapMs, frameCount: observation.timestamps.length };
}

/** One attempted or explicitly unexecuted cold-import observation. */
export interface ColdImportObservation { readonly status: 'collected' | 'failed' | 'interrupted' | 'blocked'; readonly durationMs: number | null }
/** Observable production DOM facts collected before declaring the current overview usable. */
export interface ImportOverviewObservation { readonly quiet: boolean; readonly canvasPresent: boolean; readonly tablePresent: boolean; readonly fitEnabled: boolean; readonly visible: boolean; readonly width: number; readonly height: number }
/**
 * Decide readiness from actual production controls and canvas geometry.
 * @param view Current DOM observations, not inferred SDK state.
 * @returns Whether import may be timed as a usable visible indexed overview.
 */
export function importOverviewReady(view: ImportOverviewObservation): boolean { return view.quiet && view.canvasPresent && view.tablePresent && view.fitEnabled && view.visible && Number.isFinite(view.width) && view.width > 0 && Number.isFinite(view.height) && view.height > 0; }
/**
 * Decide whether the next isolated case may launch after its predecessor exited.
 * @param observedDrainComplete True only when the sampled owned descendant drain completed.
 * @returns Permission to start another case; false preserves isolation failure evidence.
 */
export function nextPerformanceCaseAllowed(observedDrainComplete: boolean): boolean { return observedDrainComplete === true; }
/**
 * Preserve ten-run denominators while stopping an already failed each-run cohort without retries.
 * @param tier Actual medium or large canonical tier.
 * @param observations Prefix including completed, failed and explicitly unexecuted cases.
 * @returns Observed-only statistics, exact population counts and separate cold-skip/dependent-block decisions.
 * @throws {Error} For invalid durations or more than the frozen ten observations.
 */
export function coldImportCohort(tier: 'M' | 'L', observations: readonly ColdImportObservation[]) {
  if (!['M', 'L'].includes(tier) || observations.length > 10 || observations.some(row => !['collected', 'failed', 'interrupted', 'blocked'].includes(row.status) || row.durationMs !== null && (!Number.isFinite(row.durationMs) || row.durationMs < 0))) throw new Error('Valid frozen cold-import population required.');
  const budgetMs = tier === 'M' ? 10000 : 45000;
  const durations = observations.filter(row => row.status === 'collected' && row.durationMs !== null).map(row => row.durationMs!);
  const attempted = observations.filter(row => row.status !== 'blocked').length;
  const budgetFailures = durations.filter(value => value > budgetMs).length;
  const structuralFailures = observations.filter(row => row.status === 'failed' || row.status === 'interrupted' || row.status === 'collected' && row.durationMs === null).length;
  const assessed = assessMeasurements(durations, 10, budgetMs, 'maximum');
  return { tier, planned: 10, attempted, completed: durations.length, failed: budgetFailures + structuralFailures, unexecuted: 10 - attempted, budgetMs,
    status: structuralFailures ? 'fail' as const : assessed.status, complete: assessed.complete && !structuralFailures,
    observedOnly: !assessed.complete, observedStatistics: durations.length ? measurementSummary(durations) : null,
    skipRemainingColdImports: budgetFailures > 0, blockDependentCases: structuralFailures > 0 };
}
