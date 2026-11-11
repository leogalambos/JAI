// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Failure collection preserves mandatory assertions and complete numbered evidence. */
import { expect, it } from 'vitest';
import { assertCanvasReport } from './canvas-report.js';
function report() { return { steps: Array.from({ length: 11 }, (_, index) => ({ step: index + 1, title: `Check ${index + 1}`, status: 'pass' })) }; }
it('accepts a complete passing report and the one explicitly optional context-loss observation', () => {
  const current = report(); expect(() => assertCanvasReport(current)).not.toThrow(); current.steps[9]!.status = 'unknown'; expect(() => assertCanvasReport(current)).not.toThrow();
});
it.each(['fail', 'skipped', 'unknown'])('rejects collected mandatory result %s even when later checks pass', status => {
  const current = report(); current.steps[3]!.status = status; expect(() => assertCanvasReport(current)).toThrow(`4: Check 4 (${status})`);
});
it('rejects incomplete, unordered or malformed reports instead of inferring success', () => {
  expect(() => assertCanvasReport(null)).toThrow(); const missing = report(); missing.steps.pop(); expect(() => assertCanvasReport(missing)).toThrow();
  const unordered = report(); unordered.steps.reverse(); expect(() => assertCanvasReport(unordered)).toThrow(); const malformed = report(); malformed.steps[0]!.status = 'accepted'; expect(() => assertCanvasReport(malformed)).toThrow();
});
