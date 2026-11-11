// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Report boundaries retain exact failures/version observations rather than manufacturing partial success. */
import { expect, it } from 'vitest';
import { captureReport, failedReport, readerFailureReport } from '../src/import/report.js';
import { DEFAULT_IMPORT_LIMITS, ImportError } from '../src/import/types.js';
import { lease } from './import-fixtures.js';
it('records cancellation/limits and keeps explicit source-replacement recovery in a failed report', () => {
  expect(failedReport(1, new ImportError('cancelled', 'Cancelled.')).status).toBe('cancelled'); expect(failedReport(1, new ImportError('resource-limit', 'Limit.')).limitation).toContain('resource limit');
  const input = lease(); const report = readerFailureReport({ ...input.report, accepted: '0', rejected: '1', diagnosticTotal: '1', diagnostics: [{ code: 'source-changed', message: 'Changed.', sourceId: 'fabric', pointer: '', sequence: null }] }, input.compatibility, ['fabric'], DEFAULT_IMPORT_LIMITS);
  expect(report.status).toBe('failed');
  expect(readerFailureReport({ ...input.report, diagnosticTotal: '1', diagnostics: [{ code: 'cancelled', message: 'Cancelled.', sourceId: null, pointer: '', sequence: null }] }, [], ['fabric'], DEFAULT_IMPORT_LIMITS).status).toBe('cancelled'); expect(report.diagnostics[0]?.code).toBe('read-failed'); expect(report.diagnostics[0]?.message).toBe('Selected file was replaced; reopen sources to admit the new file.'); expect(report.limitation).toContain('reopen sources'); expect(failedReport(1, new ImportError('read-failed', 'Changed.', report))).toEqual(report);
});
it('rejects malformed counts, unknown-source compatibility/diagnostics and invalid verification', () => {
  const input = lease(); const limits = DEFAULT_IMPORT_LIMITS;
  expect(() => readerFailureReport({ ...input.report, selected: '2' }, input.compatibility, ['fabric'], limits)).toThrow();
  expect(() => readerFailureReport(input.report, [{ ...input.compatibility[0]!, sourceId: 'other' }], ['fabric'], limits)).toThrow();
  expect(() => readerFailureReport({ ...input.report, diagnosticTotal: '1', diagnostics: [{ code: 'read-failed', message: 'Failure.', sourceId: 'other', pointer: '', sequence: null }] }, [], ['fabric'], limits)).toThrow();
  expect(() => captureReport({ ...input, report: { ...input.report, diagnosticTotal: '1', diagnostics: [{ code: 'resource-limit', message: 'Limit.', sourceId: 'fabric', pointer: '', sequence: null }] } }, { sessionId: 'session', capability: 'capability', generation: null }, ['fabric'], limits)).toThrow('reported an import failure');
  expect(() => captureReport({ ...input, sources: [{ ...input.sources[0]!, verification: { ...input.sources[0]!.verification, replay: 'unknown' } }] }, { sessionId: 'session', capability: 'capability', generation: null }, ['fabric'], limits)).toThrow('decoded for display');
});

it('reports no invented format for canonically empty Fabric and rejects unknown nonempty versions', () => {
  const input = lease(); const binding = { sessionId: 'session', capability: 'capability', generation: null };
  const empty = { ...input, sources: [{ ...input.sources[0]!, sequence: '0', head: '0'.repeat(64), byteLength: '0' }], compatibility: [{ ...input.compatibility[0]!, declaredFormat: null, declaredProtocol: null }] };
  expect(captureReport(empty, binding, ['fabric'], DEFAULT_IMPORT_LIMITS).supportedVersions[0]).toMatchObject({ declaredFormat: null, declaredProtocol: null, supported: true });
  expect(captureReport(empty, binding, ['fabric'], DEFAULT_IMPORT_LIMITS).limitation).toContain('no format or protocol');
  expect(captureReport({ ...empty, sources: [{ ...empty.sources[0]!, byteLength: '1' }] }, binding, ['fabric'], DEFAULT_IMPORT_LIMITS).supportedVersions[0]?.declaredFormat).toBeNull();
  expect(() => captureReport({ ...empty, compatibility: input.compatibility }, binding, ['fabric'], DEFAULT_IMPORT_LIMITS)).toThrow('unsupported');
  expect(() => captureReport({ ...empty, sources: input.sources }, binding, ['fabric'], DEFAULT_IMPORT_LIMITS)).toThrow('unsupported');
  expect(() => captureReport({ ...empty, sources: [{ ...empty.sources[0]!, head: 'c'.repeat(64) }] }, binding, ['fabric'], DEFAULT_IMPORT_LIMITS)).toThrow('unsupported');
  expect(() => captureReport({ ...empty, compatibility: [{ ...empty.compatibility[0]!, declaredFormat: '10' }] }, binding, ['fabric'], DEFAULT_IMPORT_LIMITS)).toThrow('unsupported');
});

it('retains known admitted prelease failure context without fabricating a verified revision', () => {
  const input = lease(); const value = { ...input.report, accepted: '0', rejected: '1', diagnosticTotal: '2', diagnostics: [
    { code: 'read-failed' as const, message: 'Record failed.', sourceId: 'fabric', pointer: '/operations/0', sequence: '7' },
    { code: 'incompatible-source' as const, message: 'Version failed.', sourceId: null, pointer: '', sequence: null },
  ] };
  const report = readerFailureReport(value, input.compatibility, ['fabric'], { ...DEFAULT_IMPORT_LIMITS, diagnostics: 1 });
  expect(report.diagnostics[0]?.source).toBeNull(); expect(report.diagnostics).toHaveLength(1); expect(report.diagnosticTotal).toBe('2');
  expect(report).toHaveProperty('diagnosticContexts', [{ sourceId: 'fabric', pointer: '/operations/0', sequence: '7' }]);
});

it('admits recorded sources honestly without requiring duplicate canonical verification', () => {
  const input = lease();
  const recorded = { ...input, sources: input.sources.map(source => ({ ...source, verification: { ...source.verification, mode: 'recorded' as const, decoded: 'decoded' as const, chain: 'unknown' as const, replay: 'recorded' as const, publicTrust: 'unknown' as const, material: 'not-observed' as const, recordedApplicability: null } })) };
  const result = captureReport(recorded, { sessionId: 'session', capability: 'capability', generation: null }, ['fabric'], DEFAULT_IMPORT_LIMITS);
  expect(result.status).toBe('ready'); expect(result.limitation).toContain('verification was not performed');
  expect(recorded.sources[0]!.verification.chain).toBe('unknown');
});
