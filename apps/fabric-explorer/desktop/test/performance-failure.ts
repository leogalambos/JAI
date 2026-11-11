// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Private development failure summaries; arbitrary exception properties never enter evidence. */
import { SemanticError } from '../src/broker/semantic-broker.js';
import { ImportError } from '../src/import/types.js';

/**
 * Preserve typed import categories without native paths, arbitrary messages or unbounded error objects.
 * @param error Actual error from the main-owned canonical acquisition or import boundary.
 * @returns A bounded value-only summary, or null for an unknown exception type.
 */
export function performanceFailure(error: unknown) {
  if (!(error instanceof SemanticError) && !(error instanceof ImportError)) return null;
  const report = error.report;
  const diagnostics = report?.diagnostics.slice(0, 64).map(item => ({ code: item.code }));
  return { type: error instanceof SemanticError ? 'SemanticError' : 'ImportError', code: error.code,
    diagnosticTotal: report?.diagnosticTotal ?? null, diagnostics: diagnostics ?? [] };
}
