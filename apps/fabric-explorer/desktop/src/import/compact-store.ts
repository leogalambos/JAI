// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Schema-specific worker storage; public graph DTOs are reconstructed only for bounded consumers. */
import { createHash } from 'node:crypto';
import { assertEdge, assertSnapshot, assertVertex } from '@jai/fabric-explorer-contracts';
import { encodeElementKey as elementKey, encodeEdgeKey as edgeKey } from '@jai/fabric-explorer-contracts/internal/identity-codec';
import type { Attributes, Edge, ElementIdentity, FindingState, RecordFamily, RelationClass, SnapshotDescriptor, SourceLocator, SourceReference, StableLocator, Vertex } from '@jai/fabric-explorer-contracts';
import { DEFAULT_IMPORT_LIMITS, ImportError } from './types.js';

/** Exact private codec payload accounting; process RSS remains a separate qualification metric. */
export interface CompactUsage {
  readonly codec: 'jai.fabric-explorer.compact-graph/1'; readonly compactGraphBytes: number;
  readonly semanticFactBytes: number; readonly headerBytes: number; readonly dictionaryBytes: number;
  readonly rowBytes: number; readonly indexBytes: number; readonly sealScratchBytes: number;
  readonly vertices: number; readonly edges: number; readonly spans: number;
}
/** Exact immutable byte range for one admitted source locator. */
export interface CompactSpan { readonly offset: string; readonly length: string }
/** Shared accepted-worker data; scalar methods never reconstruct full graph records. */
export interface SealedGraphStore {
  readonly snapshot: SnapshotDescriptor; readonly vertexCount: number; readonly edgeCount: number;
  /** Return exact compact codec bytes. */ compactBytes(): number;
  /** Return detached accounting counters. */ usage(): CompactUsage;
  /** Find a canonical vertex ordinal, or undefined. */ findVertex(id: string): number | undefined;
  /** Read an exact public vertex key. */ vertexId(handle: number): string;
  /** Read vertex kind. */ vertexKind(handle: number): Vertex['kind'];
  /** Read complete source label. */ vertexLabel(handle: number): string;
  /** Read cached lowercase label. */ vertexLabelFolded(handle: number): string;
  /** Read cached lowercase identity. */ vertexIdFolded(handle: number): string;
  /** Read exact project identity. */ vertexProject(handle: number): string;
  /** Read exact version/use family, or null. */ vertexFamily(handle: number): RecordFamily | null;
  /** Distinguish nonapplicable family from an unresolved applicable family. */ vertexFamilyApplicable(handle: number): boolean;
  /** Read a finding state, or null. */ vertexFindingState(handle: number): FindingState | null;
  /** Resolve a label-sorted position to a canonical vertex ordinal. */ labelHandle(position: number): number;
  /** Resolve the canonical from-vertex ordinal. */ edgeFrom(handle: number): number;
  /** Resolve the canonical to-vertex ordinal. */ edgeTo(handle: number): number;
  /** Read relation class. */ edgeRelation(handle: number): RelationClass;
  /** Read canonical causal classification. */ edgeCausal(handle: number): boolean;
  /** Read source project identity. */ edgeProject(handle: number): string;
  /** Read outgoing CSR start. */ outBegin(vertex: number): number;
  /** Read outgoing CSR exclusive end. */ outEnd(vertex: number): number;
  /** Read canonical outgoing edge ordinal. */ outEdge(position: number): number;
  /** Read incoming CSR start. */ inBegin(vertex: number): number;
  /** Read incoming CSR exclusive end. */ inEnd(vertex: number): number;
  /** Read canonical incoming edge ordinal. */ inEdge(position: number): number;
  /** Decode only detached attributes, without identity or label materialization. */ vertexAttributes(handle: number): Attributes;
  /** Read exact attribute JSON bytes before attribute-only materialization. */ vertexAttributesWireBytes(handle: number): number;
  /** Read exact expanded JSON byte length before materialization. */ vertexWireBytes(handle: number): number;
  /** Read exact expanded JSON byte length before materialization. */ edgeWireBytes(handle: number): number;
  /** Reconstruct one detached vertex. */ vertex(handle: number): Vertex;
  /** Reconstruct one detached edge. */ edge(handle: number): Edge;
  /** Resolve an exact immutable captured range, or null. */ span(sourceId: string, pointer: string, sequence: string | null): CompactSpan | null;
}
const PAGE = 1024;
const HEADER = 32;
const SECTION_HEADERS = 11 * 8;
const KINDS = ['version', 'use', 'blob', 'participant', 'ownership', 'finding', 'unresolved'] as const;
const IDENTITIES = ['version', 'use', 'finding', 'blob', 'participant', 'ownership', 'location'] as const;
const FAMILIES: readonly RecordFamily[] = ['source', 'profile', 'assignment', 'context', 'product', 'assessment', 'decision'];
const STATES: readonly FindingState[] = ['open', 'resolved', 'verified', 'stuck', 'accepted', 'withdrawn'];
const cmp = (a: string, b: string): number => a < b ? -1 : a > b ? 1 : 0;
const fail = (message: string): never => { throw new ImportError('invalid-model', message); };

class Rows {
  count = 0; readonly pages: Buffer[] = []; readonly keys = new Map<string, number>();
  constructor(readonly width: number, private readonly reserve: (extra: number) => void, private readonly indexDelta = 0) {}
  get capacity(): number { return this.pages.length * PAGE; }
  get bytes(): number { return 8 + this.capacity * this.width * 4; }
  get(id: number, field: number): number {
    if (!Number.isInteger(id) || id < 1 || id > this.count || field < 0 || field >= this.width) return fail('Invalid compact row.');
    const row = id - 1; return this.pages[Math.floor(row / PAGE)]!.readUInt32LE(((row % PAGE) * this.width + field) * 4);
  }
  set(id: number, field: number, value: number): void {
    const row = id - 1; this.pages[Math.floor(row / PAGE)]!.writeUInt32LE(value, ((row % PAGE) * this.width + field) * 4);
  }
  add(fields: readonly number[], intern = false): number {
    if (fields.length !== this.width || fields.some(value => !Number.isSafeInteger(value) || value < 0 || value > 0xffffffff)) return fail('Invalid compact numeric fields.');
    const key = intern ? fields.join(',') : '';
    if (intern && this.keys.has(key)) return this.keys.get(key)!;
    this.reserve((this.count === this.capacity ? PAGE * this.width * 4 : 0) + this.indexDelta);
    if (this.count === this.capacity) this.pages.push(Buffer.alloc(PAGE * this.width * 4));
    const id = ++this.count; fields.forEach((value, field) => this.set(id, field, value));
    if (intern) this.keys.set(key, id); return id;
  }
  clearKeys(): void { this.keys.clear(); }
}
class Strings {
  readonly values: string[] = []; readonly ids = new Map<string, number>(); bytes = 4;
  constructor(private readonly reserve: (extra: number) => void) {}
  put(value: string): number {
    const existing = this.ids.get(value); if (existing !== undefined) return existing;
    const bytes = 4 + Buffer.byteLength(value); this.reserve(bytes);
    const id = this.values.push(value); this.ids.set(value, id); this.bytes += bytes; return id;
  }
  get(id: number): string { if (!id || id > this.values.length) return fail('Invalid compact string.'); return this.values[id - 1]!; }
}
class Blobs {
  readonly values: Buffer[] = []; readonly hashes = new Map<string, number[]>(); bytes = 4;
  constructor(private readonly reserve: (extra: number) => void) {}
  put(value: unknown): number {
    const text = JSON.stringify(value); const length = Buffer.byteLength(text); const hash = createHash('sha256').update(text).digest('hex');
    for (const id of this.hashes.get(hash) ?? []) if (this.values[id - 1]!.length === length && this.values[id - 1]!.toString('utf8') === text) return id;
    this.reserve(4 + length); const bytes = Buffer.from(text);
    const id = this.values.push(bytes); const ids = this.hashes.get(hash) ?? []; ids.push(id); this.hashes.set(hash, ids); this.bytes += 4 + length; return id;
  }
  get(id: number): any { if (!id || id > this.values.length) return fail('Invalid compact value.'); return JSON.parse(this.values[id - 1]!.toString('utf8')); }
}
/** App-internal generated record sink; never a renderer admission operation. */
export interface CompactImportWriter {
  /** Pack a worker-generated vertex. */ vertex(value: Vertex, primary?: boolean): void;
  /** Pack a worker-generated relation. */ edge(value: Edge): void;
}
/** Candidate builder and sealed shared store; any failed mutation makes this instance unusable. */
export class CompactGraphStore implements SealedGraphStore {
  /**
   * Bind a typed construction writer to one candidate lifetime.
   * @param snapshot Private admitted source metadata.
   * @param limitBytes Exact compact payload budget.
   * @returns Store plus mapper-only writer.
   */
  static candidate(snapshot: SnapshotDescriptor, limitBytes: number): { store: CompactGraphStore; writer: CompactImportWriter } {
    const store = new CompactGraphStore(snapshot, limitBytes);
    return { store, writer: { vertex: (value, primary = false) => store.packVertex(value, primary), edge: value => store.packEdge(value) } };
  }
  /**
   * Validate external/fixture vertex admission before packing.
   * @param value Untrusted public graph record.
   * @param primary Whether this is a source-defined primary.
   */
  putVertex(value: Vertex, primary = false): void { this.mutate(() => { assertVertex(value); this.packVertex(value, primary); }); }
  /**
   * Validate external/fixture edge admission before packing.
   * @param value Untrusted public graph relation.
   */
  putEdge(value: Edge): void { this.mutate(() => { assertEdge(value); this.packEdge(value); }); }

  private readonly strings: Strings; private readonly blobs: Blobs;
  private readonly refs: Rows; private readonly stable: Rows; private readonly locators: Rows; private readonly identities: Rows;
  private readonly attributes: Rows; private readonly vertices: Rows; private readonly edges: Rows; private readonly spans: Rows;
  private readonly vertexIds = new Map<string, number>(); private readonly edgeIds = new Set<string>(); private readonly spanIds = new Map<string, number>();
  private readonly identityVertices = new Map<number, number>();
  private readonly session: number; private readonly generation: number; private sourceBlob: number;
  private ready = false; private failed = false; private factBytes = 0; private scratchBytes = 0;
  private descriptor: SnapshotDescriptor | null = null;
  private vertexOrder = new Uint32Array(0); private vertexRank = new Uint32Array(0); private edgeOrder = new Uint32Array(0); private labelOrder = new Uint32Array(0);
  private families = new Uint8Array(0); private applicable = new Uint8Array(0); private states = new Uint8Array(0);
  private outgoing = new Uint32Array(0); private incoming = new Uint32Array(0); private outgoingEdges = new Uint32Array(0); private incomingEdges = new Uint32Array(0); private spanOrder = new Uint32Array(0);
  /**
   * Bind a fresh candidate to captured metadata and an explicit compact byte envelope.
   * @param snapshot Valid descriptor supplying immutable session/generation/source metadata.
   * @param limitBytes Maximum compact and separate seal scratch payload bytes.
   * @throws {ImportError} For an invalid envelope or metadata exceeding it.
   */
  constructor(snapshot: SnapshotDescriptor, private readonly limitBytes = DEFAULT_IMPORT_LIMITS.encodedGraphBytes) {
    assertSnapshot(snapshot);
    if (!Number.isSafeInteger(limitBytes) || limitBytes < 1 || limitBytes > DEFAULT_IMPORT_LIMITS.encodedGraphBytes) throw new ImportError('resource-limit', 'Invalid compact byte limit.');
    const reserve = (extra: number) => this.reserve(extra);
    this.strings = new Strings(reserve); this.blobs = new Blobs(reserve);
    this.refs = new Rows(4, reserve); this.stable = new Rows(7, reserve); this.locators = new Rows(9, reserve); this.identities = new Rows(8, reserve);
    this.attributes = new Rows(5, reserve); this.vertices = new Rows(12, reserve, 23); this.edges = new Rows(15, reserve, 12); this.spans = new Rows(5, reserve, 4);
    this.session = this.strings.put(snapshot.sessionId); this.generation = this.strings.put(snapshot.generation); this.sourceBlob = this.blobs.put(snapshot.sources);
    this.reserve(0);
  }
  private tables(): Rows[] { return [this.refs, this.stable, this.locators, this.identities, this.attributes, this.vertices, this.edges, this.spans].filter(Boolean); }
  private indexBytes(): number { return 23 * (this.vertices?.count ?? 0) + 12 * (this.edges?.count ?? 0) + 4 * (this.spans?.count ?? 0) + 8; }
  private reserve(extra: number): void {
    const bytes = HEADER + SECTION_HEADERS + (this.strings?.bytes ?? 4) + (this.blobs?.bytes ?? 4) + this.tables().reduce((sum, table) => sum + table.bytes, 0) + this.indexBytes();
    if (!Number.isSafeInteger(extra) || bytes + extra > this.limitBytes) throw new ImportError('resource-limit', 'Candidate compact graph byte limit exceeded.');
  }
  private active(sealed = false): void { if (this.failed || sealed && !this.ready) fail('Compact graph is unavailable.'); }
  private mutate(action: () => void): void { this.active(); if (this.ready) fail('Compact graph is already sealed.'); try { action(); } catch (error) { this.failed = true; throw error; } }
  /** Irreversibly reject a candidate; accepted stores are never mutated. */
  poison(): void { if (!this.ready) this.failed = true; }
  /** Record the independently enforced semantic stream metric without changing its envelope. */
  setFactBytes(bytes: number): void { this.mutate(() => { if (!Number.isSafeInteger(bytes) || bytes < 0 || bytes > this.limitBytes) throw new ImportError('resource-limit', 'Candidate semantic fact stream exceeds its byte limit.'); this.factBytes = bytes; }); }
  private putRef(ref: SourceReference): number { return this.refs.add([ref.engagement, ref.scope, ref.logical_id, ref.version_id].map(value => this.strings.put(value)), true); }
  private getRef(id: number): SourceReference { return { engagement: this.strings.get(this.refs.get(id, 0)), scope: this.strings.get(this.refs.get(id, 1)), logical_id: this.strings.get(this.refs.get(id, 2)), version_id: this.strings.get(this.refs.get(id, 3)) }; }
  private putLocator(source: StableLocator | SourceLocator, full: boolean): number {
    const values = [source.projectId, source.rootId, source.sourceId, source.family, source.relativePath, source.pointer].map(value => this.strings.put(value)); values.push(source.sequence === null ? 0 : this.strings.put(source.sequence));
    if (full) { const value = source as SourceLocator; values.push(this.strings.put(value.revisionId), this.strings.put(value.adapterVersion)); }
    return (full ? this.locators : this.stable).add(values, true);
  }
  private getLocator(id: number, full: boolean): any {
    const table = full ? this.locators : this.stable; const value: any = {};
    ['projectId', 'rootId', 'sourceId', 'family', 'relativePath', 'pointer'].forEach((key, index) => { value[key] = this.strings.get(table.get(id, index)); });
    value.sequence = table.get(id, 6) ? this.strings.get(table.get(id, 6)) : null;
    if (full) { value.revisionId = this.strings.get(table.get(id, 7)); value.adapterVersion = this.strings.get(table.get(id, 8)); } return value;
  }
  private putIdentity(value: ElementIdentity): number {
    const row = Array<number>(8).fill(0); row[0] = IDENTITIES.indexOf(value.kind) + 1; row[1] = this.strings.put(value.projectId); row[7] = this.strings.put(elementKey(value));
    switch (value.kind) {
      case 'version': row[2] = this.putRef(value.ref); break;
      case 'use': row[2] = this.putRef(value.ref); row[3] = this.strings.put(value.useScope); break;
      case 'finding': row[2] = this.strings.put(value.ledgerId); row[3] = this.strings.put(value.findingId); break;
      case 'blob': row[2] = this.strings.put(value.rootId); row[3] = this.strings.put(value.blobId); break;
      case 'participant': row[2] = this.strings.put(value.participant.kind); row[3] = value.participant.kind === 'assignment' ? this.putRef(value.participant.ref) : this.strings.put(value.participant.id); break;
      case 'ownership': row[2] = value.owner.layer; row[3] = this.strings.put(value.owner.work_kind); row[4] = value.owner.question === null ? 0 : this.strings.put(value.owner.question); row[5] = this.strings.put(value.owner.work_item); break;
      case 'location': row[2] = this.putLocator(value.origin, false); row[3] = this.strings.put(value.text); break;
    }
    return this.identities.add(row, true);
  }
  private getIdentity(id: number): ElementIdentity {
    const kind = IDENTITIES[this.identities.get(id, 0) - 1]!; const projectId = this.strings.get(this.identities.get(id, 1)); const a = this.identities.get(id, 2); const b = this.identities.get(id, 3);
    switch (kind) {
      case 'version': return { kind, projectId, ref: this.getRef(a) };
      case 'use': return { kind, projectId, ref: this.getRef(a), useScope: this.strings.get(b) };
      case 'finding': return { kind, projectId, ledgerId: this.strings.get(a), findingId: this.strings.get(b) };
      case 'blob': return { kind, projectId, rootId: this.strings.get(a), blobId: this.strings.get(b) };
      case 'participant': { const type = this.strings.get(a); return { kind, projectId, participant: type === 'assignment' ? { kind: 'assignment', ref: this.getRef(b) } : { kind: type as 'authority' | 'controller', id: this.strings.get(b) } }; }
      case 'ownership': return { kind, projectId, owner: { layer: a as 0 | 1 | 2 | 3 | 4 | 5 | 6, work_kind: this.strings.get(b) as 'question' | 'integration', question: this.identities.get(id, 4) ? this.strings.get(this.identities.get(id, 4)) as any : null, work_item: this.strings.get(this.identities.get(id, 5)) } };
      case 'location': return { kind, projectId, origin: this.getLocator(a, false), text: this.strings.get(b) };
    }
  }
  private putAttributes(value: Attributes): number { const bytes = Buffer.byteLength(JSON.stringify(value)); return value.kind === 'inline' ? this.attributes.add([1, this.blobs.put(value.value), 0, 0, bytes], true) : this.attributes.add([2, this.putLocator(value.source, true), this.strings.put(value.byteLength), this.strings.put(value.mediaType), bytes], true); }
  private getAttributes(id: number): Attributes { return this.attributes.get(id, 0) === 1 ? { kind: 'inline', value: this.blobs.get(this.attributes.get(id, 1)) } : { kind: 'paged', source: this.getLocator(this.attributes.get(id, 1), true), byteLength: this.strings.get(this.attributes.get(id, 2)), mediaType: this.strings.get(this.attributes.get(id, 3)) }; }
  /** Test exact candidate membership without decoding attributes. */
  hasVertex(id: string): boolean { this.active(); return this.vertexIds.has(id); }
  /**
   * Pack one validated vertex, preserving primary/placeholder/blob preference behavior.
   * @param value Detached public record to pack; it is not retained.
   * @param primary Whether this record is a unique source-defined primary.
   * @throws {ImportError} For duplicate primaries or exhausted storage/cardinality bounds.
   */
  private packVertex(value: Vertex, primary = false): void { this.mutate(() => { const previous = this.vertexIds.get(value.id);
    if (previous !== undefined) {
      if (primary && this.vertices.get(previous, 8)) fail('Duplicate source element identity.');
      const kind = KINDS[this.vertices.get(previous, 0) - 1];
      if (kind !== 'unresolved') {
        if (primary) fail('Conflicting source element identity.');
        if (kind !== 'blob' || value.kind !== 'blob') return;
        const old = this.blobs.get(this.vertices.get(previous, 7)); const rank = { missing: 0, unknown: 1, available: 2 };
        const source = this.getLocator(this.vertices.get(previous, 4), true); const left = [value.source.sourceId, value.source.pointer, value.source.sequence ?? '']; const right = [source.sourceId, source.pointer, source.sequence ?? '']; const different = left.findIndex((item, i) => item !== right[i]);
        if (!(rank[value.availability] > rank[old.availability as keyof typeof rank] || rank[value.availability] === rank[old.availability as keyof typeof rank] && different !== -1 && left[different]! < right[different]!)) return;
      }
    }
    if (!previous && this.vertices.count >= DEFAULT_IMPORT_LIMITS.vertices) throw new ImportError('resource-limit', 'Candidate vertex limit exceeded.');
    const { kind, identity, id, label, source, attributes, extensions, ...payload } = value;
    const ident = this.putIdentity(identity); const row = [KINDS.indexOf(kind) + 1, ident, this.strings.put(id), this.strings.put(label), this.putLocator(source, true), this.putAttributes(attributes), extensions === undefined ? 0 : this.blobs.put(extensions), this.blobs.put(payload), Number(primary), this.strings.put(label.toLowerCase()), this.strings.put(id.toLowerCase()), Buffer.byteLength(JSON.stringify(value))];
    if (previous) row.forEach((field, column) => this.vertices.set(previous, column, field));
    else { const handle = this.vertices.add(row); this.vertexIds.set(id, handle); this.identityVertices.set(ident, handle); }
  }); }
  /**
   * Pack an exact relation occurrence, without retaining its expanded public key.
   * @param value Valid public edge with possibly forward-declared endpoints.
   * @throws {ImportError} For duplicate identity or compact/cardinality exhaustion.
   */
  private packEdge(value: Edge): void { this.mutate(() => { if (this.edges.count >= DEFAULT_IMPORT_LIMITS.edges) throw new ImportError('resource-limit', 'Candidate edge limit exceeded.');
    const identity = value.identity; const occurrence = identity.kind === 'occurrence' ? identity.occurrence : 0;
    const low = occurrence >>> 0; const high = Math.floor(occurrence / 0x100000000);
    const row = [identity.kind === 'explicit' ? 1 : 2, this.strings.put(identity.kind === 'explicit' ? identity.sourceEdgeId : identity.pointer), low, high, this.putIdentity(identity.origin), this.putIdentity(identity.from), this.putIdentity(identity.to), this.putLocator(value.source, true), this.strings.put(value.relation), this.strings.put(value.label), this.strings.put(value.basis), Number(value.causal), this.putAttributes(value.attributes), value.extensions === undefined ? 0 : this.blobs.put(value.extensions), Buffer.byteLength(JSON.stringify(value))];
    const key = row.slice(0, 7).join(','); if (this.edgeIds.has(key)) fail('Duplicate source relation identity.'); this.edges.add(row); this.edgeIds.add(key);
  }); }
  /**
   * Retain an exact captured span, refusing contradictory reuse of its address.
   * @param sourceId Opaque captured source identity.
   * @param pointer Exact record pointer.
   * @param sequence Exact sequence or null.
   * @param offset Unsigned decimal byte offset.
   * @param length Unsigned decimal byte length.
   * @throws {ImportError} For a conflicting span or exhausted compact storage.
   */
  putSpan(sourceId: string, pointer: string, sequence: string | null, offset: string, length: string): void { this.mutate(() => {
    const row = [this.strings.put(sourceId), this.strings.put(pointer), sequence === null ? 0 : this.strings.put(sequence), this.strings.put(offset), this.strings.put(length)]; const key = row.slice(0, 3).join(','); const previous = this.spanIds.get(key);
    if (previous) { if (this.spans.get(previous, 3) !== row[3] || this.spans.get(previous, 4) !== row[4]) fail('Conflicting source record span.'); }
    else this.spanIds.set(key, this.spans.add(row));
  }); }
  /**
   * Validate endpoints, sort exact public identities and build one shared numeric index.
   * @param expected Optional complete cardinality oracle for fixture admission.
   * @returns This immutable shared store after successful publication.
   * @throws {ImportError} For missing endpoints, count mismatch or bounded scratch exhaustion.
   */
  /** Replace private draft source observations before sealing; allocated metadata remains budgeted. */
  finalizeSources(sources: SnapshotDescriptor['sources']): void {
    this.active(false); if (this.descriptor) throw new ImportError('invalid-model', 'Graph is already sealed.');
    this.sourceBlob = this.blobs.put(sources);
  }

  seal(expected?: SnapshotDescriptor): SealedGraphStore {
    this.active(); if (this.ready) return fail('Compact graph is already sealed.');
    try {
      const V = this.vertices.count; const E = this.edges.count; const I = this.identities.count; const P = this.spans.count;
      let units = 0; let largest = 0;
      for (let id = 1; id <= I; id++) { const quoted = JSON.stringify(this.strings.get(this.identities.get(id, 7))); units += quoted.length; largest = Math.max(largest, quoted.length); }
      // Address strings are also quoted scalar comparator inputs; they can be
      // larger than element IDs for the explicit-identity compatibility port.
      for (let id = 1; id <= E; id++) largest = Math.max(largest, JSON.stringify(this.strings.get(this.edges.get(id, 1))).length);
      const scratch = 2 * units + 4 * (I + 1) + 8 * I + 4 * Math.max(I, V, E, P) + 8 * (V + 1) + 4 * largest;
      if (!Number.isSafeInteger(scratch) || scratch > this.limitBytes) throw new ImportError('resource-limit', 'Compact seal scratch byte limit exceeded.');
      this.scratchBytes = scratch; this.reserve(0);
      const quotes = new Uint16Array(units); const offsets = new Uint32Array(I + 1); const quoteOrder = new Uint32Array(I); const quoteRanks = new Uint32Array(I);
      const temporary = new Uint32Array(Math.max(I, V, E, P)); let position = 0;
      for (let id = 1; id <= I; id++) { offsets[id - 1] = position; const text = JSON.stringify(this.strings.get(this.identities.get(id, 7))); for (let n = 0; n < text.length; n++) quotes[position++] = text.charCodeAt(n); quoteOrder[id - 1] = id; } offsets[I] = position;
      const quotedCompare = (left: number, right: number): number => { let a = offsets[left - 1]!; let b = offsets[right - 1]!; const ae = offsets[left]!; const be = offsets[right]!; while (a < ae && b < be) { const delta = quotes[a++]! - quotes[b++]!; if (delta) return delta; } return (ae - a) - (be - b); };
      this.sort(quoteOrder, temporary, quotedCompare); for (let n = 0; n < I; n++) quoteRanks[quoteOrder[n]! - 1] = n;
      this.vertexOrder = Uint32Array.from({ length: V }, (_, n) => n + 1); this.vertexRank = new Uint32Array(V);
      this.sort(this.vertexOrder, temporary, (a, b) => cmp(this.strings.get(this.vertices.get(a, 2)), this.strings.get(this.vertices.get(b, 2))));
      for (let n = 0; n < V; n++) this.vertexRank[this.vertexOrder[n]! - 1] = n;
      const quoteString = (left: number, right: number): number => left === right ? 0 : cmp(JSON.stringify(this.strings.get(left)), JSON.stringify(this.strings.get(right)));
      this.edgeOrder = Uint32Array.from({ length: E }, (_, n) => n + 1);
      this.sort(this.edgeOrder, temporary, (a, b) => {
        const kindA = this.edges.get(a, 0); const kindB = this.edges.get(b, 0); if (kindA !== kindB) return kindA - kindB;
        const originA = this.edges.get(a, 4); const originB = this.edges.get(b, 4);
        let value = quoteString(this.identities.get(originA, 1), this.identities.get(originB, 1)); if (value) return value;
        value = quoteRanks[originA - 1]! - quoteRanks[originB - 1]!; if (value) return value;
        value = quoteString(this.edges.get(a, 1), this.edges.get(b, 1)); if (value) return value;
        if (kindA === 2) { value = cmp(String(this.occurrence(a)), String(this.occurrence(b))); if (value) return value; }
        value = quoteRanks[this.edges.get(a, 5) - 1]! - quoteRanks[this.edges.get(b, 5) - 1]!; if (value) return value;
        return quoteRanks[this.edges.get(a, 6) - 1]! - quoteRanks[this.edges.get(b, 6) - 1]!;
      });
      for (let id = 1; id <= E; id++) for (const column of [5, 6]) { const vertex = this.identityVertices.get(this.edges.get(id, column)); if (vertex === undefined) fail('Indexed relation endpoint is absent.'); this.edges.set(id, column, vertex!); }
      this.labelOrder = this.vertexOrder.slice(); this.sort(this.labelOrder, temporary, (a, b) => cmp(this.strings.get(this.vertices.get(a, 9)), this.strings.get(this.vertices.get(b, 9))) || this.vertexRank[a - 1]! - this.vertexRank[b - 1]!);
      for (let n = 0; n < V; n++) this.labelOrder[n] = this.vertexRank[this.labelOrder[n]! - 1]!;
      this.families = new Uint8Array(V); this.applicable = new Uint8Array(V); this.states = new Uint8Array(V);
      for (let handle = 0; handle < V; handle++) {
        const row = this.vertexOrder[handle]!; const kind = this.vertices.get(row, 0); const identity = this.vertices.get(row, 1); const identityKind = this.identities.get(identity, 0);
        if (kind === 1 || kind === 2 || kind === 7 && (identityKind === 1 || identityKind === 2)) { this.applicable[handle] = 1; const key = elementKey({ kind: 'version', projectId: this.strings.get(this.identities.get(identity, 1)), ref: this.getRef(this.identities.get(identity, 2)) }); const version = this.vertexIds.get(key); this.families[handle] = version && this.vertices.get(version, 0) === 1 ? FAMILIES.indexOf(this.blobs.get(this.vertices.get(version, 7)).family) + 1 : 0; }
        if (kind === 6) this.states[handle] = STATES.indexOf(this.blobs.get(this.vertices.get(row, 7)).state) + 1;
      }
      this.outgoing = new Uint32Array(V + 1); this.incoming = new Uint32Array(V + 1); this.outgoingEdges = new Uint32Array(E); this.incomingEdges = new Uint32Array(E);
      for (let id = 1; id <= E; id++) { this.outgoing[this.vertexRank[this.edges.get(id, 5) - 1]! + 1]!++; this.incoming[this.vertexRank[this.edges.get(id, 6) - 1]! + 1]!++; }
      for (let n = 1; n <= V; n++) { this.outgoing[n]! += this.outgoing[n - 1]!; this.incoming[n]! += this.incoming[n - 1]!; }
      const out = this.outgoing.slice(); const incoming = this.incoming.slice();
      for (let handle = 0; handle < E; handle++) { const row = this.edgeOrder[handle]!; this.outgoingEdges[out[this.vertexRank[this.edges.get(row, 5) - 1]!]!++] = handle; this.incomingEdges[incoming[this.vertexRank[this.edges.get(row, 6) - 1]!]!++] = handle; }
      this.spanOrder = Uint32Array.from({ length: P }, (_, n) => n + 1); this.sort(this.spanOrder, temporary, (a, b) => { for (let field = 0; field < 3; field++) { const x = this.spans.get(a, field); const y = this.spans.get(b, field); const value = cmp(x ? this.strings.get(x) : '', y ? this.strings.get(y) : ''); if (value) return value; } return 0; });
      let findings = 0; for (let row = 1; row <= V; row++) if (this.vertices.get(row, 0) === 6) findings++;
      this.descriptor = { format: 'jai.fabric-explorer.snapshot/1', sessionId: this.strings.get(this.session), generation: this.strings.get(this.generation), sources: this.blobs.get(this.sourceBlob), counts: { vertices: String(V), edges: String(E), findings: String(findings) }, authorityGranted: false, freshAssessment: false };
      assertSnapshot(this.descriptor); if (expected && (expected.counts.vertices !== String(V) || expected.counts.edges !== String(E) || expected.counts.findings !== String(findings))) fail('Indexed cardinality differs from its sealed descriptor.');
      this.vertexIds.clear(); this.edgeIds.clear(); this.spanIds.clear(); this.identityVertices.clear(); this.tables().forEach(table => table.clearKeys()); this.strings.ids.clear(); this.blobs.hashes.clear(); this.ready = true;
      return this;
    } catch (error) { this.failed = true; throw error; }
  }
  private sort(values: Uint32Array, temporary: Uint32Array, compare: (a: number, b: number) => number): void {
    for (let width = 1; width < values.length; width *= 2) {
      for (let start = 0; start < values.length; start += width * 2) { const middle = Math.min(start + width, values.length); const end = Math.min(start + width * 2, values.length); let a = start; let b = middle;
        for (let n = start; n < end; n++) temporary[n] = b >= end || a < middle && compare(values[a]!, values[b]!) <= 0 ? values[a++]! : values[b++]!;
      }
      values.set(temporary.subarray(0, values.length));
    }
  }
  private occurrence(row: number): number { return this.edges.get(row, 2) + this.edges.get(row, 3) * 0x100000000; }
  private v(handle: number): number { this.active(true); if (!Number.isInteger(handle) || handle < 0 || handle >= this.vertexOrder.length) return fail('Invalid vertex handle.'); return this.vertexOrder[handle]!; }
  private e(handle: number): number { this.active(true); if (!Number.isInteger(handle) || handle < 0 || handle >= this.edgeOrder.length) return fail('Invalid edge handle.'); return this.edgeOrder[handle]!; }
  /** @inheritdoc */ get snapshot(): SnapshotDescriptor { this.active(true); return structuredClone(this.descriptor!); }
  /** @inheritdoc */ get vertexCount(): number { this.active(); return this.vertices.count; }
  /** @inheritdoc */ get edgeCount(): number { this.active(); return this.edges.count; }
  /** @inheritdoc */ compactBytes(): number { return this.usage().compactGraphBytes; }
  /** @inheritdoc */ usage(): CompactUsage {
    this.active(); const dictionaryBytes = this.strings.bytes + this.blobs.bytes + this.tables().slice(0, 5).reduce((sum, table) => sum + table.bytes, 0) + 7 * 8;
    const rowBytes = this.vertices.bytes + this.edges.bytes + this.spans.bytes + 3 * 8; const indexBytes = this.indexBytes() + 8;
    return { codec: 'jai.fabric-explorer.compact-graph/1', compactGraphBytes: HEADER + dictionaryBytes + rowBytes + indexBytes, semanticFactBytes: this.factBytes, headerBytes: HEADER, dictionaryBytes, rowBytes, indexBytes, sealScratchBytes: this.scratchBytes, vertices: this.vertices.count, edges: this.edges.count, spans: this.spans.count };
  }
  /** @inheritdoc */ findVertex(id: string): number | undefined { this.active(true); let low = 0; let high = this.vertexOrder.length; while (low < high) { const middle = (low + high) >>> 1; const value = cmp(this.vertexId(middle), id); if (value < 0) low = middle + 1; else high = middle; } return low < this.vertexOrder.length && this.vertexId(low) === id ? low : undefined; }
  /** @inheritdoc */ vertexId(handle: number): string { return this.strings.get(this.vertices.get(this.v(handle), 2)); }
  /** @inheritdoc */ vertexKind(handle: number): Vertex['kind'] { return KINDS[this.vertices.get(this.v(handle), 0) - 1]!; }
  /** @inheritdoc */ vertexLabel(handle: number): string { return this.strings.get(this.vertices.get(this.v(handle), 3)); }
  /** @inheritdoc */ vertexLabelFolded(handle: number): string { return this.strings.get(this.vertices.get(this.v(handle), 9)); }
  /** @inheritdoc */ vertexIdFolded(handle: number): string { return this.strings.get(this.vertices.get(this.v(handle), 10)); }
  /** @inheritdoc */ vertexProject(handle: number): string { return this.strings.get(this.identities.get(this.vertices.get(this.v(handle), 1), 1)); }
  /** @inheritdoc */ vertexFamily(handle: number): RecordFamily | null { this.v(handle); return this.families[handle] ? FAMILIES[this.families[handle]! - 1]! : null; }
  /** @inheritdoc */ vertexFamilyApplicable(handle: number): boolean { this.v(handle); return this.applicable[handle] !== 0; }
  /** @inheritdoc */ vertexFindingState(handle: number): FindingState | null { this.v(handle); return this.states[handle] ? STATES[this.states[handle]! - 1]! : null; }
  /** @inheritdoc */ labelHandle(position: number): number { this.v(position); return this.labelOrder[position]!; }
  /** @inheritdoc */ edgeFrom(handle: number): number { return this.vertexRank[this.edges.get(this.e(handle), 5) - 1]!; }
  /** @inheritdoc */ edgeTo(handle: number): number { return this.vertexRank[this.edges.get(this.e(handle), 6) - 1]!; }
  /** @inheritdoc */ edgeRelation(handle: number): RelationClass { return this.strings.get(this.edges.get(this.e(handle), 8)) as RelationClass; }
  /** @inheritdoc */ edgeCausal(handle: number): boolean { return this.edges.get(this.e(handle), 11) !== 0; }
  /** @inheritdoc */ edgeProject(handle: number): string { return this.strings.get(this.locators.get(this.edges.get(this.e(handle), 7), 0)); }
  /** @inheritdoc */ outBegin(vertex: number): number { this.v(vertex); return this.outgoing[vertex]!; }
  /** @inheritdoc */ outEnd(vertex: number): number { this.v(vertex); return this.outgoing[vertex + 1]!; }
  /** @inheritdoc */ outEdge(position: number): number { this.active(true); if (!Number.isInteger(position) || position < 0 || position >= this.outgoingEdges.length) return fail('Invalid adjacency position.'); return this.outgoingEdges[position]!; }
  /** @inheritdoc */ inBegin(vertex: number): number { this.v(vertex); return this.incoming[vertex]!; }
  /** @inheritdoc */ inEnd(vertex: number): number { this.v(vertex); return this.incoming[vertex + 1]!; }
  /** @inheritdoc */ inEdge(position: number): number { this.active(true); if (!Number.isInteger(position) || position < 0 || position >= this.incomingEdges.length) return fail('Invalid adjacency position.'); return this.incomingEdges[position]!; }
  /** @inheritdoc */ vertexAttributes(handle: number): Attributes { return this.getAttributes(this.vertices.get(this.v(handle), 5)); }
  /** @inheritdoc */ vertexAttributesWireBytes(handle: number): number { return this.attributes.get(this.vertices.get(this.v(handle), 5), 4); }
  /** @inheritdoc */ vertexWireBytes(handle: number): number { return this.vertices.get(this.v(handle), 11); }
  /** @inheritdoc */ edgeWireBytes(handle: number): number { return this.edges.get(this.e(handle), 14); }
  private decodeVertex(row: number): Vertex { const value: any = { kind: KINDS[this.vertices.get(row, 0) - 1]!, identity: this.getIdentity(this.vertices.get(row, 1)), id: this.strings.get(this.vertices.get(row, 2)), label: this.strings.get(this.vertices.get(row, 3)), source: this.getLocator(this.vertices.get(row, 4), true), attributes: this.getAttributes(this.vertices.get(row, 5)), ...this.blobs.get(this.vertices.get(row, 7)) }; if (this.vertices.get(row, 6)) value.extensions = this.blobs.get(this.vertices.get(row, 6)); return value; }
  private decodeEdge(row: number): Edge {
    const origin = this.getIdentity(this.edges.get(row, 4)); const from = this.getIdentity(this.vertices.get(this.edges.get(row, 5), 1)); const to = this.getIdentity(this.vertices.get(this.edges.get(row, 6), 1));
    const common = { projectId: origin.projectId, origin, from, to }; const identity: Edge['identity'] = this.edges.get(row, 0) === 1 ? { kind: 'explicit', ...common, sourceEdgeId: this.strings.get(this.edges.get(row, 1)) } : { kind: 'occurrence', ...common, pointer: this.strings.get(this.edges.get(row, 1)), occurrence: this.occurrence(row) };
    const edge: Edge = { id: edgeKey(identity), identity, from: elementKey(from), to: elementKey(to), source: this.getLocator(this.edges.get(row, 7), true), relation: this.strings.get(this.edges.get(row, 8)) as RelationClass, label: this.strings.get(this.edges.get(row, 9)), basis: this.strings.get(this.edges.get(row, 10)) as Edge['basis'], causal: this.edges.get(row, 11) !== 0, attributes: this.getAttributes(this.edges.get(row, 12)) };
    if (this.edges.get(row, 13)) return { ...edge, extensions: this.blobs.get(this.edges.get(row, 13)) }; return edge;
  }
  /** @inheritdoc */ vertex(handle: number): Vertex { return this.decodeVertex(this.v(handle)); }
  /** @inheritdoc */ edge(handle: number): Edge { return this.decodeEdge(this.e(handle)); }
  /** @inheritdoc */ span(sourceId: string, pointer: string, sequence: string | null): CompactSpan | null {
    this.active(true); if (pointer === '' && sequence === null) { const source = this.snapshot.sources.find(value => value.sourceId === sourceId); return source ? { offset: '0', length: source.byteLength } : null; }
    const desired = [sourceId, pointer, sequence ?? '']; const compare = (row: number): number => { for (let n = 0; n < 3; n++) { const id = this.spans.get(row, n); const value = cmp(id ? this.strings.get(id) : '', desired[n]!); if (value) return value; } return 0; };
    let low = 0; let high = this.spanOrder.length; while (low < high) { const middle = (low + high) >>> 1; if (compare(this.spanOrder[middle]!) < 0) low = middle + 1; else high = middle; }
    if (low === this.spanOrder.length || compare(this.spanOrder[low]!) !== 0) return null; const row = this.spanOrder[low]!; return { offset: this.strings.get(this.spans.get(row, 3)), length: this.strings.get(this.spans.get(row, 4)) };
  }
  /** Iterate detached DTOs in original admission order for diagnostic compatibility. */
  *records(): IterableIterator<Vertex | Edge> { this.active(true); for (let n = 1; n <= this.vertices.count; n++) yield this.decodeVertex(n); for (let n = 1; n <= this.edges.count; n++) yield this.decodeEdge(n); }
  /**
   * Emit the actual private codec image incrementally, without retaining a second graph image.
   * @returns Header/section/payload chunks whose total length equals compactBytes().
   * @throws {ImportError} Before successful sealing or after candidate rejection.
   */
  *encodedChunks(): IterableIterator<Buffer> {
    this.active(true); const header = Buffer.alloc(HEADER); header.write('JAI.GS01'); [1, 11, this.session, this.generation, this.sourceBlob, 0].forEach((value, n) => header.writeUInt32LE(value, 8 + n * 4)); yield header;
    const word = (value: number): Buffer => { const data = Buffer.alloc(4); data.writeUInt32LE(value); return data; };
    const section = (tag: number, size: number): Buffer => { const data = Buffer.alloc(8); data.writeUInt32LE(tag); data.writeUInt32LE(size, 4); return data; };
    yield section(1, this.strings.bytes); yield word(this.strings.values.length); for (const text of this.strings.values) { const data = Buffer.from(text); yield word(data.length); yield data; }
    yield section(2, this.blobs.bytes); yield word(this.blobs.values.length); for (const data of this.blobs.values) { yield word(data.length); yield Buffer.from(data); }
    let tag = 3; for (const table of this.tables()) { yield section(tag++, table.bytes); yield word(table.count); yield word(table.capacity); for (const page of table.pages) yield Buffer.from(page); }
    yield section(11, this.indexBytes());
    for (const array of [this.vertexOrder, this.vertexRank, this.labelOrder, this.families, this.applicable, this.states, this.edgeOrder, this.outgoing, this.incoming, this.outgoingEdges, this.incomingEdges, this.spanOrder]) {
      if (array instanceof Uint32Array) { const data = Buffer.alloc(array.byteLength); array.forEach((value, n) => data.writeUInt32LE(value, n * 4)); yield data; } else yield Buffer.from(array);
    }
  }
  /**
   * Compact-admit trusted record fixtures in arbitrary order, preserving independent edge origins.
   * @param snapshot Expected complete descriptor.
   * @param records One-pass iterable of public records; edges may precede their vertices.
   * @param limitBytes Trusted compact/scratch envelope, no larger than the maintained ceiling.
   * @returns One sealed compact store, without retaining the input DTOs.
   * @throws {ImportError} For duplicate records, absent endpoints or exhausted resources.
   */
  static fromRecords(snapshot: SnapshotDescriptor, records: Iterable<Vertex | Edge>, limitBytes = DEFAULT_IMPORT_LIMITS.encodedGraphBytes): SealedGraphStore {
    const store = new CompactGraphStore(snapshot, limitBytes); for (const record of records) { if ('kind' in record) store.putVertex(record, true); else store.putEdge(record); } return store.seal(snapshot);
  }
}
