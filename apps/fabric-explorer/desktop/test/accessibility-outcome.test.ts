// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Automatic unexpected-error gate preserves all twelve keyboard and six visual context observations. */
import { expect, it } from 'vitest';
import { automaticOutcome } from './accessibility-outcome.js';
it('rejects an error-bearing execution without rewriting its eighteen passing observations', () => {
  const observations = Object.freeze(Array.from({ length: 18 }, () => Object.freeze({ status: 'pass' as const })));
  expect(automaticOutcome(observations, [])).toBe('passed'); expect(automaticOutcome(observations, ['Unexpected renderer error'])).toBe('failed'); expect(observations).toHaveLength(18); expect(observations.every(item => item.status === 'pass')).toBe(true);
});
it('retains unknown/skipped evidence and gives actual failures precedence', () => {
  expect(automaticOutcome([{ status: 'unknown' }], [])).toBe('unknown'); expect(automaticOutcome([{ status: 'skipped' }], [])).toBe('unknown'); expect(automaticOutcome([{ status: 'unknown' }, { status: 'fail' }], [])).toBe('failed');
});
