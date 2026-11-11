// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Development-only automatic execution verdict; individual observations remain immutable evidence. */
/** Minimal completed automatic observation state, independent of keyboard/context denominators. */
export interface AutomaticObservationStatus { readonly status: 'pass' | 'fail' | 'unknown' | 'skipped' }
/**
 * Classify execution errors separately from the retained individual observations.
 * @param observations Completed keyboard and context states, kept unchanged.
 * @param consoleErrors Unexpected renderer errors captured during this execution.
 * @returns Failed for any execution/observation error, unknown for incomplete evidence, otherwise passed.
 */
export function automaticOutcome(observations: readonly AutomaticObservationStatus[], consoleErrors: readonly string[]): 'failed' | 'unknown' | 'passed' {
  if (consoleErrors.length || observations.some(item => item.status === 'fail')) return 'failed';
  return observations.some(item => item.status === 'unknown' || item.status === 'skipped') ? 'unknown' : 'passed';
}
