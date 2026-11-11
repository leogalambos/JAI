// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Development-only aggregate validation; collected native failures must never become a passing run. */
/** One numbered result from the fixed eleven-check native canvas helper. */
export interface NativeCanvasCheck {
  readonly step: number;
  readonly title: string;
  readonly status: 'pass' | 'fail' | 'unknown' | 'skipped';
}
/** Minimum report contract used by the trusted native runner; diagnostics remain attached separately. */
export interface NativeCanvasReport { readonly steps: readonly NativeCanvasCheck[] }
/**
 * Require every mandatory native check to pass after all available evidence has been saved.
 * @param report Actual helper result; only check ten may report an unsupported context-loss observation.
 * @returns Nothing for an acceptable complete report.
 * @throws {Error} For missing/out-of-order checks, failed/skipped checks or unexpected unknown outcomes.
 */
export function assertCanvasReport(report: unknown): asserts report is NativeCanvasReport {
  if (!report || typeof report !== 'object' || !('steps' in report) || !Array.isArray(report.steps) || report.steps.length !== 11) throw new Error('Canvas report must contain all 11 numbered checks');
  const failures: string[] = [];
  report.steps.forEach((step: unknown, index: number) => {
    if (!step || typeof step !== 'object' || !('step' in step) || step.step !== index + 1 || !('title' in step) || typeof step.title !== 'string' || !step.title || !('status' in step) || !['pass', 'fail', 'unknown', 'skipped'].includes(String(step.status))) throw new Error('Canvas report has malformed or unordered checks');
    if (step.status !== 'pass' && !(index === 9 && step.status === 'unknown')) failures.push(`${index + 1}: ${step.title} (${String(step.status)})`);
  });
  if (failures.length) throw new Error(`Canvas checks failed: ${failures.join('; ')}`);
}
