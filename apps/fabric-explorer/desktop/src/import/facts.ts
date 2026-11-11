// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Closed helper-fact boundary; canonical truth is supplied, never rederived from labels or hashes. */
import { assertSemantic, elementKey, encodeWire } from '@jai/fabric-explorer-contracts';
import type { ElementIdentity, SourceRevision } from '@jai/fabric-explorer-contracts';
import type { CanonicalFact, SemanticFactChunk } from '../broker/semantic-types.js';
import { ImportError } from './types.js';
const fields: Readonly<Record<CanonicalFact['kind'], readonly string[]>> = {
  version: ['ref', 'family', 'label', 'attributes'], use: ['point', 'state'],
  reference: ['originRef', 'originUseScope', 'fieldPointer', 'occurrence', 'targetRef', 'targetUseScope', 'historicalCausal', 'governing', 'dependencyBasis'],
  'governing-dependency': ['originPoint', 'prerequisitePoint', 'occurrence', 'dependencyBasis'],
  participant: ['originRef', 'participant', 'fieldPointer'], ownership: ['originRef', 'owner'], material: ['originRef', 'blobId', 'availability', 'fieldPointer'],
  'decision-effect': ['decisionRef', 'effectKind', 'targetPoint', 'effect', 'occurrence'],
  finding: ['findingId', 'state', 'severity', 'findingKind', 'rounds', 'recordedExpiry', 'label', 'target', 'location', 'attributes', 'effectiveMaxRounds', 'historicalMaxRoundsKnown'], audit: ['attributes'],
};
/**
 * Require a canonical unsigned decimal without lossy number coercion.
 * @param value Potential source integer.
 * @returns Exact bigint for bounded arithmetic only.
 * @throws {ImportError} For malformed integers.
 */
export function unsigned(value: unknown): bigint { if (typeof value !== 'string' || !/^(?:0|[1-9][0-9]*)$/.test(value) || value.length > 128) throw new ImportError('invalid-model', 'Invalid helper integer.'); return BigInt(value); }
function object(value: unknown): Record<string, unknown> { if (!value || typeof value !== 'object' || Array.isArray(value)) throw new ImportError('invalid-model', 'Invalid helper record.'); return value as Record<string, unknown>; }
function exact(value: Record<string, unknown>, expected: readonly string[]): void { if (Object.keys(value).sort().join() !== [...expected].sort().join()) throw new ImportError('invalid-model', 'Unknown or missing helper field.'); }
function text(value: unknown, nullable = false): void { if (!(nullable && value === null) && (typeof value !== 'string' || value.length > 1024 * 1024)) throw new ImportError('invalid-model', 'Invalid helper text.'); }
function pointer(value: unknown): void { text(value); if (typeof value !== 'string' || (value !== '' && !/^(?:\/(?:[^~]|~[01])*)+$/.test(value))) throw new ImportError('invalid-model', 'Invalid helper pointer.'); }
function occurrence(value: unknown): void { if (!Number.isSafeInteger(value) || (value as number) < 0) throw new ImportError('invalid-model', 'Invalid relation occurrence.'); }
function reference(value: unknown, projectId: string): void { elementKey({ kind: 'version', projectId, ref: value } as ElementIdentity); }
function point(value: unknown, projectId: string): void { const item = object(value); exact(item, ['ref', 'use_scope']); elementKey({ kind: 'use', projectId, ref: item.ref, useScope: item.use_scope } as ElementIdentity); }
/**
 * Validate one closed bounded pull chunk at the worker acceptance boundary.
 * @param value Raw helper chunk from the trusted transport, still untrusted semantic data.
 * @param sources Exact selected captured revision set.
 * @param expectedSequence Contiguous zero-based chunk sequence.
 * @returns The same validated typed chunk; callers retain no authority from validation alone.
 * @throws {ImportError} For unknown fields, invalid provenance, order, types or resource exhaustion.
 */
export function factChunk(value: unknown, sources: ReadonlyMap<string, SourceRevision>, expectedSequence: bigint): SemanticFactChunk {
  encodeWire(value);
  const chunk = object(value); exact(chunk, ['sequence', 'facts', 'next']);
  if (unsigned(chunk.sequence) !== expectedSequence || !Array.isArray(chunk.facts)) throw new ImportError('invalid-model', 'Out-of-order helper chunk.');
  text(chunk.next, true); if (chunk.next === '') throw new ImportError('invalid-model', 'Invalid continuation token.');
  for (const input of chunk.facts) recordedFact(input, sources);
  return value as SemanticFactChunk;
}

/**
 * Check source-bound typed record structure without encoding a transport envelope.
 * @param input One worker-local parser fact, with no executable source objects.
 * @param sources Exact private draft or final source bindings.
 * @param recordTerminatorAllowance Zero for legacy frames, or two bytes for direct LF/CRLF physical spans.
 * @returns The same validated fact without a JSON wire roundtrip.
 * @throws {ImportError} For malformed fields, incompatible source or out-of-range locators.
 */
export function recordedFact(input: unknown, sources: ReadonlyMap<string, SourceRevision>, recordTerminatorAllowance: 0 | 2 = 0): CanonicalFact {
  const item = object(input); const kind = item.kind as CanonicalFact['kind'];
  if (!Object.hasOwn(fields, kind)) throw new ImportError('invalid-model', 'Unknown helper fact.');
  exact(item, ['kind', 'sourceId', 'origin', ...fields[kind]]);
  const source = sources.get(item.sourceId as string); if (!source) throw new ImportError('invalid-model', 'Helper fact names an unselected source.');
  const origin = object(item.origin); exact(origin, ['pointer', 'sequence', 'byteOffset', 'byteLength']);
  projectedFactOrigin(input as CanonicalFact, sources, recordTerminatorAllowance);
  const length = unsigned(origin.byteLength);
  for (const name of ['ref', 'originRef', 'targetRef', 'decisionRef']) if (Object.hasOwn(item, name)) reference(item[name], source.projectId);
  for (const name of ['point', 'originPoint', 'prerequisitePoint']) if (Object.hasOwn(item, name)) point(item[name], source.projectId);
  if (Object.hasOwn(item, 'targetPoint') && item.targetPoint !== null) point(item.targetPoint, source.projectId);
  if (Object.hasOwn(item, 'occurrence')) occurrence(item.occurrence);
  if (Object.hasOwn(item, 'fieldPointer')) pointer(item.fieldPointer);
  if (Object.hasOwn(item, 'attributes')) {
    const attributes = object(item.attributes);
    if (attributes.kind === 'inline') { exact(attributes, ['kind', 'value']); assertSemantic(attributes.value, source.family === 'findings' ? 'findings' : 'lifecycle'); }
    else if (attributes.kind === 'paged') { exact(attributes, ['kind', 'byteLength', 'mediaType']); if (unsigned(attributes.byteLength) !== length) throw new ImportError('invalid-model', 'Paged attributes do not match captured span.'); text(attributes.mediaType); }
    else throw new ImportError('invalid-model', 'Invalid helper attributes.');
  }
  if (kind === 'use') assertSemantic(item.state);
  if (kind === 'reference') {
    text(item.originUseScope, true); text(item.targetUseScope, true);
    if (typeof item.historicalCausal !== 'boolean' || typeof item.governing !== 'boolean' || (item.governing && !item.historicalCausal) || item.dependencyBasis !== (item.historicalCausal ? 'historical' : 'association') || (item.historicalCausal && (item.originUseScope === null || item.targetUseScope === null))) throw new ImportError('invalid-model', 'Invalid canonical dependency facts.');
  }
  if (kind === 'governing-dependency' && item.dependencyBasis !== 'governing') throw new ImportError('invalid-model', 'Invalid governing dependency basis.');
  if (kind === 'version') { if (!['source', 'profile', 'assignment', 'context', 'product', 'assessment', 'decision'].includes(item.family as string)) throw new ImportError('invalid-model', 'Unknown record family.'); text(item.label); }
  if (kind === 'participant') elementKey({ kind: 'participant', projectId: source.projectId, participant: item.participant } as ElementIdentity);
  if (kind === 'ownership') elementKey({ kind: 'ownership', projectId: source.projectId, owner: item.owner } as ElementIdentity);
  if (kind === 'material') { elementKey({ kind: 'blob', projectId: source.projectId, rootId: source.rootId, blobId: item.blobId } as ElementIdentity); if (!['available', 'missing', 'unknown'].includes(item.availability as string)) throw new ImportError('invalid-model', 'Invalid material availability.'); }
  if (kind === 'decision-effect') { text(item.effectKind); assertSemantic(item.effect); }
  if (kind === 'finding') {
    text(item.findingId); text(item.label); text(item.target, true); text(item.location, true); text(item.recordedExpiry, true); unsigned(item.rounds);
    if (!['open', 'resolved', 'verified', 'stuck', 'withdrawn', 'accepted'].includes(item.state as string) || !['critical', 'high', 'medium', 'low'].includes(item.severity as string) || !['defect', 'gap', 'risk', 'inconsistency', 'suggestion'].includes(item.findingKind as string) || !Number.isSafeInteger(item.effectiveMaxRounds) || (item.effectiveMaxRounds as number) < 1 || item.historicalMaxRoundsKnown !== false) throw new ImportError('invalid-model', 'Invalid findings reducer facts.');
  }
  return input as CanonicalFact;
}

/**
 * Enforce typed projected fact ownership and physical source bounds, without revalidating its semantic tree.
 * @param fact Worker-local fact constructed by the recorded projector.
 * @param sources Exact admitted source revisions.
 * @param recordTerminatorAllowance Physical LF/CRLF allowance beyond the unchanged body cap.
 * @throws {ImportError} For foreign source, incompatible family or an out-of-capture span.
 */
export function projectedFactOrigin(fact: CanonicalFact, sources: ReadonlyMap<string, SourceRevision>, recordTerminatorAllowance: 0 | 2 = 2): void {
  const source = sources.get(fact.sourceId as string); if (!source) throw new ImportError('invalid-model', 'Helper fact names an unselected source.');
  if (source.sequence === '0') throw new ImportError('invalid-model', 'A canonically empty source cannot emit record facts.');
  const origin = fact.origin; pointer(origin.pointer);
  if (origin.sequence !== null && (unsigned(origin.sequence) === 0n || (source.sequence !== null && unsigned(origin.sequence) > unsigned(source.sequence)))) throw new ImportError('invalid-model', 'Helper sequence exceeds captured source.');
  const offset = unsigned(origin.byteOffset); const length = unsigned(origin.byteLength);
  if (length > 100n * 1024n * 1024n + BigInt(recordTerminatorAllowance)) throw new ImportError('resource-limit', 'Source record exceeds 100 MiB.');
  if (offset + length > unsigned(source.byteLength)) throw new ImportError('invalid-model', 'Helper span exceeds captured source.');
  if (fact.kind !== 'finding' && fact.kind !== 'audit' && source.family !== 'fabric') throw new ImportError('invalid-model', 'Canonical record has incompatible source family.');
  if (fact.kind === 'finding' && source.family !== 'findings') throw new ImportError('invalid-model', 'Finding has incompatible source family.');
  if (fact.kind === 'audit') throw new ImportError('incompatible-source', 'The optional audit adapter is unavailable in this build.');
}
