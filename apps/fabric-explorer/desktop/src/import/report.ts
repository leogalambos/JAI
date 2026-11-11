// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Bounded import outcomes preserve diagnostic totals without exposing native helper exceptions. */
import { assertSnapshot, encodeWire } from '@jai/fabric-explorer-contracts';
import type { Binding, Diagnostic, SourceLocator } from '@jai/fabric-explorer-contracts';
import type { SemanticLease, ReaderDiagnostic } from '../broker/semantic-types.js';
import { ImportError } from './types.js';
import type { DiagnosticContext, ImportLimits, ImportReport } from './types.js';
import { unsigned } from './facts.js';
/**
 * Validate captured lease metadata and map reader diagnostics to consumer diagnostics.
 * @param lease Candidate captured source metadata, not yet a published snapshot.
 * @param binding Exact current prior-generation context.
 * @param selected Exact requested admitted source IDs.
 * @param limits Trusted diagnostic display bound.
 * @returns Detached provisional report; no graph is accepted by this operation.
 * @throws {ImportError} For partial/unsupported/duplicate capture metadata or invalid counts.
 */
export function captureReport(lease: Pick<SemanticLease, 'sources' | 'compatibility' | 'report'>, binding: Binding, selected: readonly string[], limits: ImportLimits): ImportReport {
  encodeWire({ sources: lease.sources, compatibility: lease.compatibility, report: lease.report });
  assertSnapshot({ format: 'jai.fabric-explorer.snapshot/1', sessionId: binding.sessionId, generation: String(BigInt(binding.generation ?? '0') + 1n), sources: lease.sources, counts: { vertices: '0', edges: '0', findings: '0' }, authorityGranted: false, freshAssessment: false });
  const sourceMap = new Map(lease.sources.map(source => [source.sourceId, source]));
  if (sourceMap.size !== selected.length || selected.some(sourceId => !sourceMap.has(sourceId))) throw new ImportError('invalid-model', 'Captured revision set differs from the requested sources.');
  for (const source of lease.sources) {
    const evidence = source.verification;
    const recorded = evidence.mode === 'recorded' && evidence.decoded === 'decoded' && evidence.chain === 'unknown' && evidence.replay === 'recorded';
    const verified = evidence.mode === 'canonical' && evidence.decoded === 'decoded' && evidence.chain === 'verified' && (source.family !== 'fabric' || evidence.replay === 'verified');
    if (!recorded && !verified) throw new ImportError('read-failed', 'A required source could not be decoded for display.');
  }
  const report = lease.report;
  if (!report || Object.keys(report).sort().join() !== 'accepted,diagnosticTotal,diagnostics,rejected,selected,skipped' || unsigned(report.selected) !== BigInt(selected.length) || unsigned(report.accepted) !== BigInt(selected.length) || unsigned(report.rejected) !== 0n || unsigned(report.skipped) !== 0n || !Array.isArray(report.diagnostics) || report.diagnostics.length > 1000 || unsigned(report.diagnosticTotal) < BigInt(report.diagnostics.length)) throw new ImportError('invalid-model', 'Capture did not produce a complete source set.');
  if (lease.compatibility.length !== selected.length || new Set(lease.compatibility.map(item => item.sourceId)).size !== selected.length) throw new ImportError('invalid-model', 'Incomplete source compatibility report.');
  let hasUndeclaredEmptyFabric = false;
  for (const item of lease.compatibility) {
    if (Object.keys(item).sort().join() !== 'adapterVersion,declaredFormat,declaredProtocol,family,sourceId,supported') throw new ImportError('invalid-model', 'Malformed source compatibility report.');
    const source = sourceMap.get(item.sourceId);
    if (!source || source.family !== item.family || source.adapterVersion !== item.adapterVersion || typeof item.supported !== 'boolean') throw new ImportError('invalid-model', 'Source compatibility namespace differs.');
    const emptyFabric = item.family === 'fabric' && source.sequence === '0' && source.head === '0'.repeat(64);
    const fabricDeclaration = emptyFabric ? item.declaredFormat === null && item.declaredProtocol === null : item.declaredFormat === '9' && item.declaredProtocol === 'jai.governed-delivery/1';
    const adapterSupported = item.adapterVersion === `jai.fabric-explorer.${item.family}/1` || source.verification.mode === 'recorded' && item.adapterVersion === `jai.fabric-explorer.${item.family}/2`;
    if (!item.supported || !adapterSupported || item.family === 'audit' || item.family === 'fabric' && !fabricDeclaration || item.family === 'findings' && (item.declaredFormat !== null || item.declaredProtocol !== null)) throw new ImportError('incompatible-source', 'The selected source format or adapter version is unsupported.');
    hasUndeclaredEmptyFabric ||= emptyFabric;
  }
  const diagnostics = report.diagnostics.map((item: ReaderDiagnostic): Diagnostic => {
    if (!item || Object.keys(item).sort().join() !== 'code,message,pointer,sequence,sourceId' || !['incompatible-source', 'read-failed', 'resource-limit', 'cancelled', 'missing-public-trust', 'missing-material', 'source-changed', 'helper-failed'].includes(item.code) || typeof item.message !== 'string' || item.message.length > 4096 || typeof item.pointer !== 'string' || item.pointer.length > 4096 || (item.sequence !== null && unsigned(item.sequence) < 0n)) throw new ImportError('invalid-model', 'Malformed reader diagnostic.');
    if (item.code !== 'missing-material') throw new ImportError(item.code === 'resource-limit' || item.code === 'incompatible-source' || item.code === 'cancelled' ? item.code : 'read-failed', 'A required source reported an import failure.');
    const revision = item.sourceId === null ? null : sourceMap.get(item.sourceId);
    if (item.sourceId !== null && !revision) throw new ImportError('invalid-model', 'Diagnostic names an unselected source.');
    const source: SourceLocator | null = revision ? { projectId: revision.projectId, rootId: revision.rootId, sourceId: revision.sourceId, family: revision.family, relativePath: revision.relativePath, pointer: item.pointer, sequence: item.sequence, revisionId: revision.revisionId, adapterVersion: revision.adapterVersion } : null;
    const code: Diagnostic['code'] = item.code === 'missing-material' ? 'not-found' : item.code === 'missing-public-trust' || item.code === 'source-changed' ? 'read-failed' : item.code === 'helper-failed' ? 'worker-failed' : item.code;
    return { code, message: item.message, source, severity: 'warning' };
  });
  return { status: 'ready', selectedSources: report.selected, acceptedSources: report.accepted, rejectedSources: report.rejected, vertices: '0', edges: '0', unresolvedVertices: '0', skippedItems: report.skipped, diagnosticTotal: report.diagnosticTotal, diagnostics: diagnostics.slice(0, limits.diagnostics), supportedVersions: structuredClone(lease.compatibility), observation: 'observed-revision-set', limitation: [hasUndeclaredEmptyFabric ? 'Empty Fabric journal: no format or protocol has been declared; future records must use a supported format.' : null, lease.sources.some(source => source.verification.mode === 'recorded') ? 'Recorded source content is displayed; chain, signature and lifecycle verification was not performed.' : null].filter(Boolean).join(' ') || null };
}
/**
 * Build a value-redacted failed outcome while preserving the previous published model separately.
 * @param selected Number of deliberately selected sources.
 * @param error Typed application failure.
 * @returns Bounded failed/cancelled report with no partial accepted-source claim.
 */
export function failedReport(selected: number, error: ImportError): ImportReport {
  if (error.report) return structuredClone(error.report);
  return { status: error.code === 'cancelled' ? 'cancelled' : 'failed', selectedSources: String(selected), acceptedSources: '0', rejectedSources: String(selected), vertices: '0', edges: '0', unresolvedVertices: '0', skippedItems: '0', diagnosticTotal: '1', diagnostics: [{ code: error.code, message: error.message, source: null, severity: 'error' }], supportedVersions: [], observation: 'observed-revision-set', limitation: error.code === 'resource-limit' ? 'Import resource limit reached; previous snapshot retained.' : null };
}

/**
 * Preserve a failed helper's observed formats and counts without accepting its partial model.
 * @param value Closed reader failure report.
 * @param compatibility Observed selected-source versions, possibly a proper subset on early failure.
 * @param selected Exact admitted source IDs requested for this attempt.
 * @param limits Trusted diagnostic display bound.
 * @returns A bounded failed report with no snapshot publication.
 * @throws {ImportError} For malformed/unbound diagnostic metadata.
 */
export function readerFailureReport(value: import('../broker/semantic-types.js').ImportReport, compatibility: readonly import('../broker/semantic-types.js').SourceCompatibility[], selected: readonly string[], limits: ImportLimits): ImportReport {
  encodeWire({ value, compatibility });
  if (!value || Object.keys(value).sort().join() !== 'accepted,diagnosticTotal,diagnostics,rejected,selected,skipped' || unsigned(value.selected) !== BigInt(selected.length) || unsigned(value.accepted) + unsigned(value.rejected) > BigInt(selected.length) || unsigned(value.skipped) > BigInt(selected.length) || !Array.isArray(value.diagnostics) || value.diagnostics.length > 1000 || unsigned(value.diagnosticTotal) < BigInt(value.diagnostics.length)) throw new ImportError('invalid-model', 'Invalid failed source report.');
  const seen = new Set<string>();
  for (const item of compatibility) {
    if (!item || Object.keys(item).sort().join() !== 'adapterVersion,declaredFormat,declaredProtocol,family,sourceId,supported' || !selected.includes(item.sourceId) || seen.has(item.sourceId) || !['fabric', 'findings', 'audit'].includes(item.family) || typeof item.supported !== 'boolean' || typeof item.adapterVersion !== 'string' || item.adapterVersion.length > 4096 || (item.declaredFormat !== null && (typeof item.declaredFormat !== 'string' || item.declaredFormat.length > 4096)) || (item.declaredProtocol !== null && (typeof item.declaredProtocol !== 'string' || item.declaredProtocol.length > 4096))) throw new ImportError('invalid-model', 'Invalid failed compatibility report.'); seen.add(item.sourceId);
  }
  const diagnostics: Diagnostic[] = []; const diagnosticContexts: DiagnosticContext[] = [];
  for (const item of value.diagnostics) {
    if (!item || Object.keys(item).sort().join() !== 'code,message,pointer,sequence,sourceId' || !['incompatible-source', 'read-failed', 'resource-limit', 'cancelled', 'missing-public-trust', 'missing-material', 'source-changed', 'helper-failed'].includes(item.code) || (item.sourceId !== null && !selected.includes(item.sourceId)) || typeof item.message !== 'string' || item.message.length > 4096 || typeof item.pointer !== 'string' || item.pointer.length > 4096 || (item.sequence !== null && unsigned(item.sequence) < 0n)) throw new ImportError('invalid-model', 'Invalid failed reader diagnostic.');
    if (diagnostics.length < limits.diagnostics) {
      diagnostics.push({ code: item.code === 'helper-failed' ? 'worker-failed' : ['missing-public-trust', 'missing-material', 'source-changed'].includes(item.code) ? 'read-failed' : item.code as Diagnostic['code'], message: item.code === 'source-changed' ? 'Selected file was replaced; reopen sources to admit the new file.' : item.message, source: null, severity: 'error' });
      diagnosticContexts.push({ sourceId: item.sourceId, pointer: item.pointer, sequence: item.sequence });
    }
  }
  return { status: value.diagnostics.some(item => item.code === 'cancelled') ? 'cancelled' : 'failed', selectedSources: value.selected, acceptedSources: value.accepted, rejectedSources: value.rejected, vertices: '0', edges: '0', unresolvedVertices: '0', skippedItems: value.skipped, diagnosticTotal: value.diagnosticTotal, diagnostics, diagnosticContexts, supportedVersions: structuredClone(compatibility), observation: 'observed-revision-set', limitation: value.diagnostics.some(item => item.code === 'source-changed') ? 'Selected file was replaced; reopen sources to admit the new file.' : null };
}
