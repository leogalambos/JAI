// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Typed failure evidence must retain categories while excluding uncontrolled error payloads. */
import { expect, it } from 'vitest';
import { SemanticError } from '../src/broker/semantic-broker.js';
import { ImportError } from '../src/import/types.js';
import { performanceFailure } from './performance-failure.js';

it('retains the semantic cap rejection and bounds diagnostics without copying messages', () => {
  const error = new SemanticError('resource-limit', { selected: '1', accepted: '0', rejected: '1', skipped: '0', diagnosticTotal: '65', diagnostics: Array.from({ length: 65 }, () => ({ code: 'resource-limit' as const, message: '/private/native/path', sourceId: null, pointer: '', sequence: null })) }, []);
  const result = performanceFailure(error);
  expect(result).toMatchObject({ type: 'SemanticError', code: 'resource-limit', diagnosticTotal: '65' });
  expect(result?.diagnostics).toHaveLength(64); expect(JSON.stringify(result)).not.toContain('private');
});
it('distinguishes import categories and excludes arbitrary native errors', () => {
  expect(performanceFailure(new ImportError('cancelled', 'private'))).toEqual({ type: 'ImportError', code: 'cancelled', diagnosticTotal: null, diagnostics: [] });
  expect(performanceFailure(Object.assign(new Error('/private'), { code: 'resource-limit', report: { diagnostics: [] } }))).toBeNull();
  expect(performanceFailure(null)).toBeNull();
});
