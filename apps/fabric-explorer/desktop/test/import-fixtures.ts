// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Synthetic owned importer collaborators; canonical reader parity is tested separately against the real helper. */
import type { SourceRevision, SourceReference } from '@jai/fabric-explorer-contracts';
import type { CanonicalFact, SemanticLease } from '../src/broker/semantic-types.js';
import { DEFAULT_IMPORT_LIMITS } from '../src/import/types.js';
import type { ImportReport } from '../src/import/types.js';
import type { ModelInput } from '../src/import/model.js';
/** Exact synthetic source reference with independently variable origin scope. */
export const ref: SourceReference = { engagement: 'engagement', scope: 'origin', logical_id: 'record', version_id: 'a'.repeat(64) };
/** Captured synthetic source metadata used only in application unit tests. */
export function revision(family: 'fabric' | 'findings' = 'fabric'): SourceRevision { return { revisionId: `revision-${family}`, projectId: 'project', rootId: `root-${family}`, sourceId: family, family, relativePath: `${family}.jsonl`, adapterVersion: `jai.fabric-explorer.${family}/1`, byteLength: '1000', digest: 'b'.repeat(64), head: 'c'.repeat(64), sequence: '1', observedAt: '2026-11-10T00:00:00Z', verification: { mode: 'canonical', decoded: 'decoded', chain: 'verified', replay: family === 'fabric' ? 'verified' : 'unknown', publicTrust: 'not-required', material: 'not-observed', recordedApplicability: null, authorityGranted: false, freshAssessment: false } }; }
/** A complete synthetic tagged version fact with an exact raw row span. */
export function versionFact(): CanonicalFact { return { kind: 'version', sourceId: 'fabric', origin: { pointer: '/operations/0/data/effects/0/manifest', sequence: '1', byteOffset: '0', byteLength: '100' }, ref, family: 'source', label: 'Record', attributes: { kind: 'inline', value: { type: 'integer', value: '9007199254740993' } } }; }
/** Minimal bounded successful report before graph mapping. */
export function report(): ImportReport { return { status: 'ready', selectedSources: '1', acceptedSources: '1', rejectedSources: '0', vertices: '0', edges: '0', unresolvedVertices: '0', skippedItems: '0', diagnosticTotal: '0', diagnostics: [], supportedVersions: [{ sourceId: 'fabric', family: 'fabric', declaredFormat: '9', declaredProtocol: 'jai.governed-delivery/1', supported: true, adapterVersion: 'jai.fabric-explorer.fabric/1' }], observation: 'observed-revision-set', limitation: null }; }
/** Candidate metadata with source-bound prior and next generation. */
export function modelInput(): ModelInput { return { binding: { sessionId: 'session', capability: 'capability', generation: null }, generation: '1', sources: [revision()], report: report(), limits: DEFAULT_IMPORT_LIMITS }; }
/** A synthetic helper lease with explicit owned persistence and release. */
export function lease(facts: readonly CanonicalFact[] = [versionFact()]): SemanticLease { return { leaseId: 'lease', sources: [revision()], compatibility: report().supportedVersions as SemanticLease['compatibility'], report: { selected: '1', accepted: '1', rejected: '0', skipped: '0', diagnostics: [], diagnosticTotal: '0' }, chunk: async () => ({ sequence: '0', facts, next: null }), persist: async () => ({ page: async (sourceId, offset, length) => ({ sourceId, pointer: '', sequence: null, offset, byteLength: length, bytesBase64: Buffer.alloc(length, 120).toString('base64'), eof: false }), dispose: async () => undefined }), release: async () => undefined }; }
