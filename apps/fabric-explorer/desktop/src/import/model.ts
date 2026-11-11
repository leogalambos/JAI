// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Worker-local graph mapping of canonical facts; no lifecycle replay or scope resolution lives here. */
import { assertAdapterChunk, assertSnapshot, encodeSemantic } from '@jai/fabric-explorer-contracts';
import { encodeElementKey, encodeEdgeKey, encodeStableLocator } from '@jai/fabric-explorer-contracts/internal/identity-codec';
import type { Attributes, Binding, Edge, ElementIdentity, RelationClass, SnapshotDescriptor, SourceLocator, SourceReference, SourceRevision, Vertex } from '@jai/fabric-explorer-contracts';
import type { CanonicalFact, CanonicalPoint } from '../broker/semantic-types.js';
import { factChunk, projectedFactOrigin } from './facts.js';
import { ImportError, importLimits } from './types.js';
import type { ImportLimits, ImportReport } from './types.js';
import { CompactGraphStore } from './compact-store.js';
import type { CompactUsage, SealedGraphStore, CompactImportWriter } from './compact-store.js';
/** Worker initialization contains only immutable captured metadata and the expected next generation. */
export interface ModelInput { readonly binding: Binding; readonly generation: string; readonly sources: readonly SourceRevision[]; readonly report: ImportReport; readonly limits: ImportLimits }
/** Ready metadata sent to main; graph arrays stay in the worker. */
export interface ModelReady { readonly descriptor: SnapshotDescriptor; readonly report: ImportReport }
/** Captured byte span resolved only for an exact source locator in the accepted model. */
export interface SourceSpan { readonly offset: string; readonly length: string }
const empty: Attributes = { kind: 'inline', value: { type: 'null' } };
const familyRelation = (pointer: string, causal: boolean): RelationClass => {
  if (pointer === '/origin/ref') return 'assignment';
  const first = pointer.split('/')[1];
  const relation: Partial<Record<string, RelationClass>> = { profile: 'profile', criteria: 'criteria', inherited: 'inheritance', assignment: 'assignment', inputs: 'input-binding', subject: 'assessed-subject', assessed_closure: 'assessed-subject' };
  return (first && relation[first]) || (causal ? 'causal-dependency' : 'other-reference');
};
/** Immutable candidate builder; one instance belongs to one candidate worker lifetime. */
export class ImportModel {
  private readonly sources: Map<string, SourceRevision>;
  private readonly store: CompactGraphStore;
  private readonly writer: CompactImportWriter;
  private readonly checkedText = new Set<string>();
  private readonly checkedDigests = new Set<string>();
  private findingCount = 0;
  private failed = false;
  private readonly limits: ImportLimits;
  private factBytes = 0;
  private readonly directSourceSequences = new Map<string, bigint>();
  private readonly directFactSources = new Set<string>();
  private nextSequence = 0n;
  private ended = false;
  private ready: ModelReady | null = null;
  /**
   * Bind a candidate to exact prior context and captured source revisions.
   * @param input Trusted candidate generation/configuration and validated acquisition metadata.
   * @throws {ImportError} For invalid generation, empty/repeated sources or resource bounds.
   */
  constructor(private input: ModelInput) {
    this.limits = importLimits(input.limits);
    if (!input.binding.capability || !/^(?:0|[1-9][0-9]*)$/.test(input.generation) || BigInt(input.generation) !== BigInt(input.binding.generation ?? '0') + 1n || !input.sources.length) throw new ImportError('invalid-model', 'Invalid candidate generation.');
    assertSnapshot(this.descriptor()); const candidate = CompactGraphStore.candidate(this.descriptor(), this.limits.encodedGraphBytes); this.store = candidate.store; this.writer = candidate.writer; this.sources = new Map(input.sources.map(source => [source.sourceId, source]));
    if (this.sources.size !== input.sources.length) throw new ImportError('invalid-model', 'Repeated captured source.');
  }
  // Only input-derived public identity strings are checked, once per distinct immutable string.
  // Tagged attribute payloads are not identity data and deliberately retain isolated surrogates.
  private text(value: string, required = false): void {
    if (typeof value !== 'string' || required && !value.length) throw new ImportError('invalid-model', 'Invalid recorded identity text.');
    if (!this.checkedText.has(value)) { if (/[\uD800-\uDBFF](?![\uDC00-\uDFFF])|(?<![\uD800-\uDBFF])[\uDC00-\uDFFF]/u.test(value)) throw new ImportError('invalid-model', 'Invalid Unicode in recorded identity text.'); this.checkedText.add(value); }
  }
  private reference(ref: SourceReference): void {
    this.text(ref.engagement, true); this.text(ref.scope, true); this.text(ref.logical_id, true);
    if (!this.checkedDigests.has(ref.version_id)) { if (typeof ref.version_id !== 'string' || !/^[0-9a-f]{64}$/.test(ref.version_id)) throw new ImportError('invalid-model', 'Invalid recorded version identity.'); this.checkedDigests.add(ref.version_id); }
  }
  private identity(value: ElementIdentity): void {
    switch (value.kind) {
      case 'version': this.reference(value.ref); break;
      case 'use': this.reference(value.ref); this.text(value.useScope, true); if (value.useScope.length > 128 && [...value.useScope].length > 128) throw new ImportError('invalid-model', 'Recorded use scope exceeds its identity bound.'); break;
      case 'finding': this.text(value.findingId, true); break;
      case 'participant': if (value.participant.kind === 'assignment') this.reference(value.participant.ref); else { if (!['authority', 'controller'].includes(value.participant.kind)) throw new ImportError('invalid-model', 'Invalid recorded participant kind.'); this.text(value.participant.id, true); } break;
      case 'ownership': { const owner = value.owner; if (!Number.isInteger(owner.layer) || owner.layer < 1 || owner.layer > 6 || !['question', 'integration', 'handoff', 'measurement'].includes(owner.work_kind)) throw new ImportError('invalid-model', 'Invalid recorded owner.'); if (owner.work_kind === 'question' ? !['what', 'why', 'how', 'who', 'where', 'when'].includes(owner.question ?? '') : owner.question !== null) throw new ImportError('invalid-model', 'Invalid recorded owner question.'); this.text(owner.work_item, true); break; }
      case 'location': this.text(value.text, true); break;
      case 'blob': if (!/^[0-9a-f]{64}$/.test(value.blobId)) throw new ImportError('invalid-model', 'Invalid recorded material identity.'); break;
    }
  }
  private key(value: ElementIdentity): string { this.identity(value); return encodeElementKey(value); }
  private descriptor(): SnapshotDescriptor { return { format: 'jai.fabric-explorer.snapshot/1', sessionId: this.input.binding.sessionId, generation: this.input.generation, sources: this.input.sources, counts: { vertices: String(this.store?.vertexCount ?? 0), edges: String(this.store?.edgeCount ?? 0), findings: String(this.findingCount) }, authorityGranted: false, freshAssessment: false }; }
  private node(vertex: Vertex, primary = false): void {
    this.text(vertex.label);
    const exists = this.store.hasVertex(vertex.id);
    if (!exists && this.store.vertexCount >= this.limits.vertices) throw new ImportError('resource-limit', 'Candidate vertex limit exceeded.');
    this.writer.vertex(vertex, primary); if (!exists && vertex.kind === 'finding') this.findingCount++;
  }
  private ensure(identity: ElementIdentity, source: SourceLocator): void {
    const id = this.key(identity); if (this.store.hasVertex(id)) return;
    if (identity.kind !== 'version' && identity.kind !== 'use' && identity.kind !== 'location') throw new ImportError('invalid-model', 'Unknown exact endpoint.');
    this.node({ kind: 'unresolved', id, identity, label: identity.kind === 'location' ? identity.text : identity.ref.logical_id, reason: identity.kind === 'location' ? 'textual-location' : 'missing-reference', source, attributes: empty });
  }
  private edge(origin: ElementIdentity, from: ElementIdentity, to: ElementIdentity, source: SourceLocator, pointer: string, occurrence: number, relation: RelationClass, basis: Edge['basis'], label: string, extensions?: Edge['extensions'], attributes: Attributes = empty): void {
    this.identity(origin); this.text(pointer); this.text(label); this.ensure(from, source); this.ensure(to, source);
    const identity = { kind: 'occurrence' as const, projectId: source.projectId, origin, pointer, occurrence, from, to };
    const edge: Edge = { id: encodeEdgeKey(identity), identity, from: this.key(from), to: this.key(to), relation, label, source, basis, causal: basis === 'canonical-dependency', attributes, ...(extensions ? { extensions } : {}) };
    if (this.store.edgeCount >= this.limits.edges) throw new ImportError('resource-limit', 'Candidate edge limit exceeded.');
    this.writer.edge(edge);
  }
  /**
   * Consume exactly one bounded pull chunk before the main requests the next.
   * @param value Untrusted semantic helper chunk.
   * @throws {ImportError} For invalid order, malformed facts, duplicate elements or exhausted limits.
   */
  consume(value: unknown): void {
    if (this.failed) throw new ImportError('invalid-model', 'Import candidate is unavailable.');
    if (this.ended || this.ready) throw new ImportError('invalid-model', 'Records arrived after the terminal chunk.');
    try {
      const chunk = factChunk(value, this.sources, this.nextSequence);
      if (chunk.next !== null && chunk.facts.length === 0) throw new ImportError('invalid-model', 'A nonterminal helper chunk made no progress.');
      const bytes = Buffer.byteLength(JSON.stringify(chunk));
      if (this.factBytes + bytes > this.limits.encodedGraphBytes) throw new ImportError('resource-limit', 'Candidate semantic fact stream exceeds its byte limit.');
      for (const fact of chunk.facts) this.map(fact);
      this.factBytes += bytes; this.store.setFactBytes(this.factBytes); this.nextSequence++;
      this.ended = chunk.next === null;
    } catch (error) { this.failed = true; this.store.poison(); throw error; }
  }

  /**
   * Map one trusted parser fact directly within this worker, without a wire or retained fact list.
   * @param fact Exact lossless fact emitted by the app-owned recorded parser.
   * @throws {ImportError} For malformed fact, terminal state or existing logical semantic limits.
   */
  consumeDirect(fact: CanonicalFact): void {
    if (this.failed || this.ended || this.ready) throw new ImportError('invalid-model', 'Import candidate is unavailable.');
    try {
      const bytes = Buffer.byteLength(JSON.stringify(fact));
      if (bytes > 1024 * 1024 || this.factBytes + bytes > this.limits.encodedGraphBytes) throw new ImportError('resource-limit', 'Candidate semantic fact stream exceeds its byte limit.');
      projectedFactOrigin(fact, this.sources, 2);
      if (fact.origin.sequence !== null) { const sequence = BigInt(fact.origin.sequence); if (sequence > (this.directSourceSequences.get(fact.sourceId) ?? 0n)) this.directSourceSequences.set(fact.sourceId, sequence); }
      this.directFactSources.add(fact.sourceId); this.map(fact); this.factBytes += bytes; this.store.setFactBytes(this.factBytes);
    } catch (error) { this.failed = true; this.store.poison(); throw error; }
  }
  /**
   * Bind final source content observations only after direct streams are complete.
   * @param sources Complete revisions retaining every admitted identity and capture byte length.
   * @param report Validated recorded-source import outcome.
   * @throws {ImportError} For changed binding, malformed revisions or already published state.
   */
  finalizeSources(sources: readonly SourceRevision[], report: ImportReport): void {
    if (this.failed || this.ended || this.ready || sources.length !== this.sources.size) throw new ImportError('invalid-model', 'Invalid direct source finalization.');
    for (const source of sources) {
      const prior = this.sources.get(source.sourceId);
      const sequence = this.directSourceSequences.get(source.sourceId);
      if (source.sequence === '0' && this.directFactSources.has(source.sourceId) || sequence !== undefined && source.sequence !== null && sequence > BigInt(source.sequence)) throw new ImportError('invalid-model', 'Direct fact sequence exceeds captured source.');
      if (!prior || (['revisionId', 'projectId', 'rootId', 'sourceId', 'family', 'relativePath', 'byteLength', 'adapterVersion'] as const).some(key => source[key] !== prior[key])) throw new ImportError('invalid-model', 'Direct source binding changed.');
    }
    this.input = { ...this.input, sources: structuredClone(sources), report: structuredClone(report) }; assertSnapshot(this.descriptor());
    this.sources.clear(); for (const source of this.input.sources) this.sources.set(source.sourceId, source);
    this.store.finalizeSources(this.input.sources); this.ended = true;
  }

  private map(fact: CanonicalFact): void {
    this.text(fact.origin.pointer);
    const revision = this.sources.get(fact.sourceId)!;
    const source: SourceLocator = { projectId: revision.projectId, rootId: revision.rootId, sourceId: revision.sourceId, family: revision.family, relativePath: revision.relativePath, pointer: fact.origin.pointer, sequence: fact.origin.sequence, revisionId: revision.revisionId, adapterVersion: revision.adapterVersion };
    this.store.putSpan(fact.sourceId, fact.origin.pointer, fact.origin.sequence, fact.origin.byteOffset, fact.origin.byteLength);
    const version = (ref: SourceReference): ElementIdentity => ({ kind: 'version', projectId: source.projectId, ref });
    const use = (point: CanonicalPoint): ElementIdentity => ({ kind: 'use', projectId: source.projectId, ref: point.ref, useScope: point.use_scope });
    const fields = (value: Extract<CanonicalFact, { kind: 'version' | 'finding' }>['attributes']): Attributes => value.kind === 'inline' ? value : { kind: 'paged', source, byteLength: value.byteLength, mediaType: value.mediaType };
    switch (fact.kind) {
      case 'version': {
        const identity = { kind: 'version' as const, projectId: source.projectId, ref: fact.ref };
        this.node({ kind: 'version', identity, id: this.key(identity), label: fact.label, family: fact.family, source, attributes: fields(fact.attributes) }, true); break;
      }
      case 'use': {
        const identity = { kind: 'use' as const, projectId: source.projectId, ref: fact.point.ref, useScope: fact.point.use_scope };
        this.node({ kind: 'use', identity, id: this.key(identity), label: `${fact.point.ref.logical_id} @ ${fact.point.use_scope}`, source, attributes: { kind: 'inline', value: fact.state } }, true); break;
      }
      case 'reference': {
        const origin = fact.originUseScope === null ? version(fact.originRef) : use({ ref: fact.originRef, use_scope: fact.originUseScope });
        const target = fact.targetUseScope === null ? version(fact.targetRef) : use({ ref: fact.targetRef, use_scope: fact.targetUseScope });
        const relation = familyRelation(fact.fieldPointer, fact.historicalCausal);
        const reverse = fact.historicalCausal || ['profile', 'criteria', 'inheritance', 'assignment', 'input-binding', 'assessed-subject'].includes(relation);
        this.edge(origin, reverse ? target : origin, reverse ? origin : target, source, fact.fieldPointer, fact.occurrence, relation, fact.historicalCausal ? 'canonical-dependency' : 'exact-reference', fact.fieldPointer, { 'jai.dependency-basis': encodeSemantic(fact.dependencyBasis), 'jai.governing': encodeSemantic(fact.governing), 'jai.historical-causal': encodeSemantic(fact.historicalCausal) }); break;
      }
      case 'governing-dependency': {
        const origin = use(fact.originPoint); this.edge(origin, use(fact.prerequisitePoint), origin, source, '/@canonical/governing-dependencies', fact.occurrence, 'causal-dependency', 'canonical-dependency', 'Scoped governing dependency', { 'jai.dependency-basis': encodeSemantic('governing'), 'jai.derived': encodeSemantic(true) }); break;
      }
      case 'participant': {
        const identity = { kind: 'participant' as const, projectId: source.projectId, participant: fact.participant }; this.node({ kind: 'participant', identity, id: this.key(identity), label: fact.participant.kind === 'assignment' ? fact.participant.ref.logical_id : fact.participant.id, source, attributes: { kind: 'inline', value: encodeSemantic(fact.participant) } });
        this.edge(version(fact.originRef), version(fact.originRef), identity, source, fact.fieldPointer, 0, 'participant', 'exact-reference', fact.fieldPointer); break;
      }
      case 'ownership': {
        const identity = { kind: 'ownership' as const, projectId: source.projectId, owner: fact.owner }; this.node({ kind: 'ownership', identity, id: this.key(identity), label: `${fact.owner.layer}: ${fact.owner.work_item}`, source, attributes: { kind: 'inline', value: encodeSemantic(fact.owner) } });
        this.edge(version(fact.originRef), version(fact.originRef), identity, source, '/owner', 0, 'ownership', 'exact-reference', 'Owner'); break;
      }
      case 'material': {
        const identity = { kind: 'blob' as const, projectId: source.projectId, rootId: source.rootId, blobId: fact.blobId }; this.node({ kind: 'blob', identity, id: this.key(identity), label: fact.blobId, availability: fact.availability, source, attributes: empty });
        this.edge(version(fact.originRef), version(fact.originRef), identity, source, fact.fieldPointer, 0, 'material-attachment', 'exact-reference', fact.fieldPointer, { 'jai.material-availability': encodeSemantic(fact.availability) }); break;
      }
      case 'decision-effect': {
        if (fact.targetPoint !== null) this.edge(version(fact.decisionRef), version(fact.decisionRef), use(fact.targetPoint), source, '/@canonical/decision-effects', fact.occurrence, 'decision-effect', 'recorded-effect', fact.effectKind, { 'jai.derived': encodeSemantic(true) }, { kind: 'inline', value: fact.effect }); break;
      }
      case 'finding': {
        if (!['open', 'resolved', 'verified', 'stuck', 'withdrawn', 'accepted'].includes(fact.state) || !['critical', 'high', 'medium', 'low'].includes(fact.severity) || !['defect', 'gap', 'risk', 'inconsistency', 'suggestion'].includes(fact.findingKind)) throw new ImportError('invalid-model', 'Invalid recorded finding classification.');
        if (fact.recordedExpiry !== null) this.text(fact.recordedExpiry);
        const identity = { kind: 'finding' as const, projectId: source.projectId, ledgerId: source.sourceId, findingId: fact.findingId };
        this.node({ kind: 'finding', identity, id: this.key(identity), label: fact.label, state: fact.state, severity: fact.severity, findingKind: fact.findingKind, rounds: fact.rounds, recordedExpiry: fact.recordedExpiry, source, attributes: fields(fact.attributes), extensions: { 'jai.effective-max-rounds': encodeSemantic(fact.effectiveMaxRounds), 'jai.historical-max-rounds-known': encodeSemantic(false) } }, true);
        for (const [pointer, text] of [['/target', fact.target], ['/location', fact.location]] as const) if (text !== null && text !== '') {
          const location: ElementIdentity = { kind: 'location', projectId: source.projectId, origin: encodeStableLocator(source), text };
          this.edge(identity, identity, location, source, pointer, 0, 'location-association', 'textual-location', pointer);
        }
        break;
      }
      case 'audit': throw new ImportError('incompatible-source', 'The optional audit adapter is unavailable in this build.');
    }
  }
  /**
   * Seal a complete model and expose metadata only after all fact chunks have arrived.
   * @returns Validated descriptor and bounded import report; arrays remain worker-local.
   * @throws {ImportError} For premature EOF, missing endpoints or inconsistent metadata.
   */
  finish(): ModelReady {
    if (this.ready) throw new ImportError('invalid-model', 'Import did not have exactly one terminal chunk.');
    try {
      if (this.failed || !this.ended) throw new ImportError('invalid-model', 'Import did not have exactly one terminal chunk.');
      this.store.seal(this.descriptor()); const descriptor = this.store.snapshot;
      assertAdapterChunk({ kind: 'complete', binding: this.input.binding, snapshot: descriptor, checkpointToken: null });
      let unresolved = 0; for (let handle = 0; handle < this.store.vertexCount; handle++) if (this.store.vertexKind(handle) === 'unresolved') unresolved++;
      this.ready = { descriptor, report: { ...this.input.report, status: 'ready', vertices: descriptor.counts.vertices, edges: descriptor.counts.edges, unresolvedVertices: String(unresolved) } };
      return structuredClone(this.ready);
    } catch (error) { this.failed = true; this.store.poison(); throw error; }
  }

  /**
   * Iterate the sealed immutable model inside its owning worker for downstream handoff.
   * @returns Vertex records followed by relation records; no main-process transfer occurs.
   * @throws {ImportError} Before the model has been sealed.
   */
  *records(): IterableIterator<Vertex | Edge> { if (!this.ready || this.failed) throw new ImportError('invalid-model', 'Snapshot is not ready.'); yield* this.store.records(); }
  /**
   * Resolve an accepted model locator to its immutable captured byte span.
   * @param sourceId Exact captured source ID.
   * @param pointer Exact emitted record pointer, or empty for the whole captured source.
   * @param sequence Exact local row sequence, or null with an empty pointer.
   * @returns Detached span or null for a locator not represented in this model.
   * @throws {ImportError} If the model has not been sealed.
   */
  span(sourceId: string, pointer: string, sequence: string | null): SourceSpan | null {
    if (!this.ready || this.failed) throw new ImportError('invalid-model', 'Snapshot is not ready.');
    return this.store.span(sourceId, pointer, sequence);
  }
  /** Return the shared sealed worker store; no full DTO graph is copied. */
  graph(): SealedGraphStore { if (!this.ready || this.failed) throw new ImportError('invalid-model', 'Snapshot is not ready.'); return this.store; }
  /** Return exact private codec bytes for a successfully sealed model. */
  compactBytes(): number { return this.graph().compactBytes(); }
  /** Return exact compact/fact accounting without an expanded graph serialization. */
  usage(): CompactUsage { return this.graph().usage(); }

}
