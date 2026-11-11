// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Indexed read-only queries over one sealed worker-local observed graph. */
import { createHmac, randomBytes, timingSafeEqual } from 'node:crypto';
import { isDeepStrictEqual } from 'node:util';
import { assertBinding, assertRequest, assertSnapshot, ContractError, elementKey, LIMITS, PROTOCOL, queryKey, RELATION_DIRECTIONS } from '@jai/fabric-explorer-contracts';
import type { Attributes, Binding, Counts, Edge, Filter, GraphProjection, OmissionReason, QueryLimits, RelationClass, RequestPayloads, SnapshotDescriptor, Vertex } from '@jai/fabric-explorer-contracts';
import { CompactGraphStore } from '../import/compact-store.js';
import type { SealedGraphStore } from '../import/compact-store.js';
import { EXPLORE_LIMITS } from '../explore/types.js';
import type { GraphSelection, ProjectionSelection, FilteredHandles, GraphBinding, GraphData, GraphGroup, GraphGroups, GraphReply, GraphRequest, GroupAxis, HandleProjection, QueryControl } from './types.js';

/** Fixed query failure whose category/message never embeds source content. */
export class GraphQueryError extends Error {
  /**
   * Construct a cancelled or missing-element result.
   * @param code Safe worker-boundary category.
   */
  constructor(readonly code: 'cancelled' | 'not-found') {
    super(code === 'cancelled' ? 'Graph query cancelled.' : 'Element is absent from this captured graph.'); this.name = 'GraphQueryError';
  }
}
/** Public visible defaults; requests still carry explicit S04 work/visible ceilings. */
export const DEFAULT_QUERY_LIMITS: QueryLimits = Object.freeze({ maxVertices: LIMITS.defaultVertices, maxEdges: LIMITS.defaultEdges, maxVisitedVertices: LIMITS.visitedVertices, maxScannedEdges: LIMITS.scannedEdges, maxHops: LIMITS.hops });
/** Explicit all-relation traversal selector; S04 traversal requests require at least one relation. */
export const DEFAULT_RELATIONS: readonly RelationClass[] = Object.freeze(Object.keys(RELATION_DIRECTIONS) as RelationClass[]);
const compare = (left: string, right: string): number => left < right ? -1 : left > right ? 1 : 0;
const check = (control?: QueryControl): void => { if (control?.cancelled()) throw new GraphQueryError('cancelled'); };
type FilterView = { vertices: Uint8Array; edges: Uint8Array; counts: Counts };
type Walk = { visited: number[]; eligible: number[]; seen: Uint8Array; predecessor: Int32Array; predecessorEdge: Int32Array; scanned: number; limited: boolean; filtered: boolean; found: boolean };

/** One immutable-generation index; numeric handles never replace public stable element identities. */
export class QueryIndex {
  private store: SealedGraphStore | null;
  private cache: { key: string; value: FilterView } | null = null;
  private readonly secret = randomBytes(32);
  private readonly binding: GraphBinding;
  private readonly snapshot: SnapshotDescriptor;
  private closed = false;

  /**
   * Borrow the sealed worker store; fixture records are packed into the same representation once.
   * @param data Exact descriptor and shared store, or trusted direct-fixture record iterable.
   * @param binding Accepted session/capability/generation; never renderer-selected authority.
   * @throws {ContractError} For mismatched binding, snapshot or cardinality.
   */
  constructor(data: GraphData, binding: Binding) {
    assertSnapshot(data.snapshot); assertBinding(binding, binding);
    if (!binding.capability || !binding.generation || data.snapshot.sessionId !== binding.sessionId || data.snapshot.generation !== binding.generation) throw new ContractError('stale-generation', 'Graph binding differs from its sealed snapshot.');
    this.binding = Object.freeze({ ...binding }) as GraphBinding; this.snapshot = structuredClone(data.snapshot);
    this.store = 'store' in data ? data.store : CompactGraphStore.fromRecords(data.snapshot, data.records);
    if (!isDeepStrictEqual(this.store.snapshot, data.snapshot) || String(this.store.vertexCount) !== data.snapshot.counts.vertices || String(this.store.edgeCount) !== data.snapshot.counts.edges) throw new ContractError('invalid-model', 'Indexed store differs from its sealed descriptor.');
  }
  private get graph(): SealedGraphStore { this.active(); return this.store!; }

  private active(): void { if (this.closed) throw new ContractError('stale-generation', 'Graph work generation is no longer active.'); }

  /**
   * Resolve one numeric layout handle inside the exact owning work generation.
   * @param handle Canonical-ID-sorted vertex ordinal.
   * @returns Detached complete vertex; caller mutation cannot affect the store.
   * @throws {ContractError} For a disposed index or invalid ordinal.
   */
  vertex(handle: number): Vertex { return this.graph.vertex(handle); }

  /**
   * Reconstruct an original parallel or self relation from its accepted numeric handle.
   * @param handle Canonical-ID-sorted relation ordinal.
   * @returns Detached complete edge; no expanded edge cache is retained.
   * @throws {ContractError} For disposed work or an invalid ordinal.
   */
  edge(handle: number): Edge { return this.graph.edge(handle); }

  /**
   * Read a validated record's encoded size before reconstructing output.
   * @param kind Vertex or edge table selected by the owned transport.
   * @param handle Canonical-ID-sorted ordinal in that table.
   * @returns UTF-8 JSON bytes, excluding the surrounding frame delimiter.
   * @throws {ContractError} For disposed work or an invalid ordinal.
   */
  wireBytes(kind: 'vertex' | 'edge', handle: number): number { return kind === 'vertex' ? this.graph.vertexWireBytes(handle) : this.graph.edgeWireBytes(handle); }

  /**
   * Read attribute size independently of label, identity and other vertex fields.
   * @param handle Exact vertex ordinal.
   * @returns UTF-8 JSON bytes for the complete Attributes value.
   * @throws {ContractError} For disposed work or an invalid handle.
   */
  attributeWireBytes(handle: number): number { return this.graph.vertexAttributesWireBytes(handle); }

  /**
   * Decode only the attributes requested by the inspector.
   * @param handle Exact vertex ordinal whose output size has already been checked.
   * @returns Detached complete attributes without reconstructing the vertex.
   * @throws {ContractError} For disposed work or an invalid handle.
   */
  attributes(handle: number): Attributes { return this.graph.vertexAttributes(handle); }


  private filter(filter: Filter, control?: QueryControl): FilterView {
    check(control);
    const projects = new Set(filter.projectIds); const families = new Set(filter.families); const states = new Set(filter.findingStates); const relations = new Set(filter.relations);
    const key = JSON.stringify([[...projects].sort(), [...families].sort(), [...states].sort(), [...relations].sort()]);
    if (this.cache?.key === key) return this.cache.value;
    const base = new Uint8Array(this.graph.vertexCount); const vertices = new Uint8Array(this.graph.vertexCount); const edges = new Uint8Array(this.graph.edgeCount);
    for (let handle = 0; handle < this.graph.vertexCount; handle++) {
      check(control);
      const family = this.graph.vertexFamily(handle);
      base[handle] = Number((!projects.size || projects.has(this.graph.vertexProject(handle))) && (!families.size || !this.graph.vertexFamilyApplicable(handle) || family !== null && families.has(family)) && (!states.size || this.graph.vertexKind(handle) !== 'finding' || states.has(this.graph.vertexFindingState(handle)!)));
      if (!relations.size) vertices[handle] = base[handle]!;
    }
    let edgeCount = 0;
    for (let handle = 0; handle < this.graph.edgeCount; handle++) {
      check(control);
      if (base[this.graph.edgeFrom(handle)] && base[this.graph.edgeTo(handle)] && (!projects.size || projects.has(this.graph.edgeProject(handle))) && (!relations.size || relations.has(this.graph.edgeRelation(handle)))) {
        edges[handle] = 1; edgeCount++;
        if (relations.size) { vertices[this.graph.edgeFrom(handle)] = 1; vertices[this.graph.edgeTo(handle)] = 1; }
      }
    }
    let vertexCount = 0; let findings = 0;
    for (let handle = 0; handle < vertices.length; handle++) { check(control); if (vertices[handle]) { vertexCount++; if (this.graph.vertexKind(handle) === 'finding') findings++; } }
    const value = { vertices, edges, counts: { vertices: String(vertexCount), edges: String(edgeCount), findings: String(findings) } };
    this.cache = { key, value }; return value;
  }

  private signature(key: string, offset: string, domain: 'all' | 'findings'): string { return createHmac('sha256', this.secret).update(JSON.stringify([this.binding, domain, key, offset])).digest('hex'); }

  private search(request: Extract<GraphRequest, { operation: 'search.page' }>, control?: QueryControl, domain: 'all' | 'findings' = 'all'): Extract<GraphSelection, { operation: 'search.page' }> {
    const payload = request.payload; const key = queryKey(request); let offset = 0;
    if (payload.cursor) {
      const token = payload.cursor.token; const expected = this.signature(key, payload.cursor.offset, domain);
      if (!/^[0-9a-f]{64}$/.test(token) || !timingSafeEqual(Buffer.from(token, 'hex'), Buffer.from(expected, 'hex')) || BigInt(payload.cursor.offset) > BigInt(this.graph.vertexCount)) throw new ContractError('cursor-mismatch', 'Search cursor is not authentic for this work generation.');
      offset = Number(payload.cursor.offset);
    }
    const view = this.filter(payload.filter, control); const text = payload.text.toLowerCase(); const vertices: number[] = []; let matched = 0;
    const scan = (handle: number): void => {
      check(control);
      if (view.vertices[handle] && (domain === 'all' || this.graph.vertexKind(handle) === 'finding') && (this.graph.vertexLabelFolded(handle).includes(text) || this.graph.vertexIdFolded(handle).includes(text))) {
        if (matched >= offset && vertices.length < payload.limit) vertices.push(handle); matched++;
      }
    };
    if (payload.order === 'label') { for (let position = 0; position < this.graph.vertexCount; position++) scan(this.graph.labelHandle(position)); }
    else { for (let handle = 0; handle < this.graph.vertexCount; handle++) scan(handle); }
    if (offset > matched) throw new ContractError('cursor-mismatch', 'Search cursor exceeds its immutable result set.');
    const next = offset + vertices.length; const hidden = matched - next;
    return { operation: 'search.page', vertices, terminal: { hidden: String(hidden), complete: hidden === 0, nextCursor: hidden === 0 ? null : { binding: { ...this.binding }, operation: 'search.page', queryKey: key, offset: String(next), token: this.signature(key, String(next), domain) } } };
  }

  /**
   * Search only canonical finding vertices without changing the public search wire contract.
   * @param request Existing validated search request; its queryKey remains unchanged.
   * @param control Optional live cancellation observation.
   * @returns A finding-only page with a domain-authenticated cursor.
   * @throws {ContractError} For invalid requests, stale binding or cross-domain cursors.
   */
  searchFindings(request: Extract<GraphRequest, { operation: 'search.page' }>, control?: QueryControl): Extract<GraphReply, { operation: 'search.page' }> {
    this.active(); check(control); assertRequest(request); assertBinding(request.binding, this.binding);
    if (request.operation !== 'search.page') throw new ContractError('unknown-operation', 'Finding search requires a search request.');
    const selection = this.search(request, control, 'findings');
    this.checkTransfer(selection.vertices, [], control);
    return { operation: 'search.page', value: { ...selection.terminal, items: selection.vertices.map(handle => { check(control); return this.vertex(handle); }) } };
  }

  /**
   * Filter only an already retained bounded projection using whole-index exact membership.
   * @param base Trusted generation-local handles, in original displayed record order.
   * @param filter Existing conditional project/family/finding/relation selectors.
   * @param control Optional live cancellation observation.
   * @returns Exact aligned masks, layout handles and global snapshot hidden counts.
   * @throws {ContractError} For invalid handles, endpoint mismatch or excessive visible size.
   */
  filterProjection(base: HandleProjection, filter: Filter, control?: QueryControl): FilteredHandles {
    this.active(); check(control);
    assertRequest({ protocol: PROTOCOL, kind: 'request', requestId: 'projection-filter', binding: this.binding, operation: 'graph.counts', payload: { filter } });
    if (base.vertices.length > LIMITS.visibleVertices || base.edges.length > LIMITS.visibleEdges) throw new ContractError('resource-limit', 'Projection exceeds the visible limit.');
    const view = this.filter(filter, control); const vertices: number[] = []; const edges: HandleProjection['edges'][number][] = [];
    const vertexMask = Buffer.alloc(Math.ceil(base.vertices.length / 8)); const edgeMask = Buffer.alloc(Math.ceil(base.edges.length / 8));
    const present = new Set<number>(); const all = new Set<number>(); const edgeIds = new Set<number>();
    for (const [position, handle] of base.vertices.entries()) {
      check(control); this.graph.vertexKind(handle);
      if (all.has(handle)) throw new ContractError('invalid-message', 'Duplicate projection handle.'); all.add(handle);
      if (view.vertices[handle]) { vertexMask[position >> 3]! |= 1 << (position & 7); vertices.push(handle); present.add(handle); }
    }
    for (const [position, edge] of base.edges.entries()) {
      check(control); this.graph.edgeRelation(edge.handle);
      if (edgeIds.has(edge.handle) || edge.from !== this.graph.edgeFrom(edge.handle) || edge.to !== this.graph.edgeTo(edge.handle) || !all.has(edge.from) || !all.has(edge.to)) throw new ContractError('invalid-message', 'Invalid projection edge handles.'); edgeIds.add(edge.handle);
      if (view.edges[edge.handle] && present.has(edge.from) && present.has(edge.to)) { edgeMask[position >> 3]! |= 1 << (position & 7); edges.push(edge); }
    }
    return { handles: { vertices, edges }, vertexMask: vertexMask.toString('base64'), edgeMask: edgeMask.toString('base64'), hiddenVertices: String(this.graph.vertexCount - vertices.length), hiddenEdges: String(this.graph.edgeCount - edges.length), filtered: vertices.length !== base.vertices.length || edges.length !== base.edges.length };
  }

  private *adjacent(vertex: number, direction: 'forward' | 'reverse' | 'both'): IterableIterator<number> {
    let outgoing = this.graph.outBegin(vertex); let incoming = this.graph.inBegin(vertex);
    const outEnd = this.graph.outEnd(vertex); const inEnd = this.graph.inEnd(vertex);
    while ((direction !== 'reverse' && outgoing < outEnd) || (direction !== 'forward' && incoming < inEnd)) {
      const left = direction === 'reverse' || outgoing >= outEnd ? Infinity : this.graph.outEdge(outgoing);
      const right = direction === 'forward' || incoming >= inEnd ? Infinity : this.graph.inEdge(incoming);
      if (left <= right) { yield left; outgoing++; if (left === right) incoming++; }
      else { yield right; incoming++; }
    }
  }

  private walk(start: number, goal: number | null, payload: RequestPayloads['graph.neighbours'] | RequestPayloads['graph.path'], control?: QueryControl): Walk {
    const limits = payload.limits; const seen = new Uint8Array(this.graph.vertexCount); const considered = new Uint8Array(this.graph.edgeCount); const depth = new Uint8Array(this.graph.vertexCount);
    const predecessor = new Int32Array(this.graph.vertexCount).fill(-1); const predecessorEdge = new Int32Array(this.graph.vertexCount).fill(-1);
    const visited = [start]; const eligible: number[] = []; seen[start] = 1; let scanned = 0; let limited = false; let filtered = false; let found = goal === start;
    const relations = new Set(payload.relations);
    outer: for (let position = 0; position < visited.length && !found; position++) {
      check(control); const current = visited[position]!;
      for (const handle of this.adjacent(current, payload.direction)) {
        check(control); if (considered[handle]) continue;
        if (scanned >= limits.maxScannedEdges) { limited = true; break outer; }
        // Work is charged before predicates, so filtered high-degree hubs cannot
        // bypass the scan ceiling by making every considered edge ineligible.
        considered[handle] = 1; scanned++;
        if (relations.size && !relations.has(this.graph.edgeRelation(handle)) || payload.causalOnly && !this.graph.edgeCausal(handle)) { filtered = true; continue; }
        eligible.push(handle);
        const other = this.graph.edgeFrom(handle) === current ? this.graph.edgeTo(handle) : this.graph.edgeFrom(handle);
        if (seen[other]) continue;
        if (depth[current]! >= limits.maxHops || visited.length >= limits.maxVisitedVertices) { limited = true; continue; }
        seen[other] = 1; depth[other] = depth[current]! + 1; predecessor[other] = current; predecessorEdge[other] = handle; visited.push(other);
        if (other === goal) { found = true; break outer; }
      }
    }
    return { visited, eligible, seen, predecessor, predecessorEdge, scanned, limited, filtered, found };
  }

  private sorted(handles: readonly number[], control?: QueryControl): number[] {
    check(control); let comparisons = 0;
    const sorted = [...handles].sort((left, right) => { if ((++comparisons & 255) === 0) check(control); return left - right; });
    check(control); return sorted;
  }

  private projection(vertices: readonly number[], edges: readonly number[], reasons: Set<OmissionReason>, work: { visitedVertices: number; scannedEdges: number }, control?: QueryControl): ProjectionSelection {
    const selected = this.sorted(vertices, control); const links = this.sorted(edges, control);
    for (const handle of selected) { check(control); if (this.graph.vertexKind(handle) === 'unresolved') reasons.add('unresolved'); }
    const omissions: OmissionReason[] = ['filter', 'visible-limit', 'work-limit', 'unresolved', 'unavailable'].filter(reason => reasons.has(reason as OmissionReason)) as OmissionReason[];
    const handles: HandleProjection = { vertices: selected, edges: links.map(handle => { check(control); return { handle, from: this.graph.edgeFrom(handle), to: this.graph.edgeTo(handle) }; }) };
    return { projection: { format: 'jai.fabric-explorer.projection/1', snapshot: structuredClone(this.snapshot), hiddenVertices: String(this.graph.vertexCount - selected.length), hiddenEdges: String(this.graph.edgeCount - links.length), complete: omissions.every(reason => reason === 'filter'), omissions }, handles, work };
  }

  private frontier(walk: Walk, limits: QueryLimits, control?: QueryControl): ProjectionSelection {
    const reasons = new Set<OmissionReason>(); if (walk.limited) reasons.add('work-limit');
    const vertices = walk.visited.slice(0, limits.maxVertices); const visible = new Set(vertices); const edges: number[] = []; let reachableEdges = 0;
    if (vertices.length < walk.visited.length) reasons.add('visible-limit');
    for (const handle of this.sorted(walk.eligible, control)) {
      check(control);
      const from = this.graph.edgeFrom(handle); const to = this.graph.edgeTo(handle);
      if (!walk.seen[from] || !walk.seen[to]) continue;
      reachableEdges++;
      if (!visible.has(from) || !visible.has(to) || edges.length >= limits.maxEdges) { reasons.add('visible-limit'); continue; }
      edges.push(handle);
    }
    if (walk.filtered || !walk.limited && (walk.visited.length < this.graph.vertexCount || reachableEdges < this.graph.edgeCount)) reasons.add('filter');
    return this.projection(vertices, edges, reasons, { visitedVertices: walk.visited.length, scannedEdges: walk.scanned }, control);
  }

  private neighbours(request: Extract<GraphRequest, { operation: 'graph.neighbours' }>, control?: QueryControl): ProjectionSelection {
    const start = this.graph.findVertex(elementKey(request.payload.identity));
    if (start === undefined) return this.projection([], [], new Set(['unavailable']), { visitedVertices: 0, scannedEdges: 0 });
    return this.frontier(this.walk(start, null, request.payload, control), request.payload.limits, control);
  }

  private path(request: Extract<GraphRequest, { operation: 'graph.path' }>, control?: QueryControl): ProjectionSelection & { found: boolean | null } {
    const start = this.graph.findVertex(elementKey(request.payload.from)); const goal = this.graph.findVertex(elementKey(request.payload.to));
    const filtered = (): Set<OmissionReason> => new Set(this.graph.vertexCount || this.graph.edgeCount ? ['filter'] : []);
    if (start === undefined || goal === undefined) return { ...this.projection([], [], filtered(), { visitedVertices: 0, scannedEdges: 0 }), found: false };
    const walk = this.walk(start, goal, request.payload, control); const work = { visitedVertices: walk.visited.length, scannedEdges: walk.scanned };
    if (!walk.found) {
      const unknown = walk.limited || walk.visited.some(handle => { check(control); return this.graph.vertexKind(handle) === 'unresolved'; });
      if (!unknown) return { ...this.projection([], [], filtered(), work), found: false };
      const result = this.frontier(walk, request.payload.limits, control);
      if (walk.visited.some(handle => { check(control); return this.graph.vertexKind(handle) === 'unresolved'; }) && !result.projection.omissions.includes('unresolved')) return { ...this.projection(result.handles.vertices, result.handles.edges.map(edge => edge.handle), new Set([...result.projection.omissions, 'unresolved']), work, control), found: null };
      return { ...result, found: null };
    }
    const pathVertices = [goal]; const pathEdges: number[] = [];
    for (let current = goal; current !== start;) { check(control); pathEdges.push(walk.predecessorEdge[current]!); current = walk.predecessor[current]!; pathVertices.push(current); }
    pathVertices.reverse(); pathEdges.reverse();
    const vertices = pathVertices.slice(0, request.payload.limits.maxVertices); const visible = new Set(vertices); const edges = pathEdges.filter(handle => { check(control); return visible.has(this.graph.edgeFrom(handle)) && visible.has(this.graph.edgeTo(handle)); }).slice(0, request.payload.limits.maxEdges);
    const reasons = filtered(); if (pathVertices.length === this.graph.vertexCount && pathEdges.length === this.graph.edgeCount) reasons.delete('filter');
    if (vertices.length < pathVertices.length || edges.length < pathEdges.length) reasons.add('visible-limit'); if (walk.limited) reasons.add('work-limit');
    return { ...this.projection(vertices, edges, reasons, work, control), found: true };
  }

  /**
   * Select exact numeric records without reconstructing full DTOs during scans or traversal.
   * @param request Closed S04 request against this accepted generation.
   * @param control Main-owned atomic cancellation observer.
   * @param mode Application-owned findings selector; valid only for search.
   * @returns Bounded numeric selection and unchanged terminal semantics.
   * @throws {ContractError} For malformed, stale, unsupported or unauthentic requests.
   * @throws {GraphQueryError} For cancellation or absent details.
   */
  select(request: GraphRequest, control?: QueryControl, mode: 'all' | 'findings' = 'all'): GraphSelection {
    this.active(); check(control); assertRequest(request); assertBinding(request.binding, this.binding);
    if (mode === 'findings' && request.operation !== 'search.page') throw new ContractError('unknown-operation', 'Finding search requires a search request.');
    switch (request.operation) {
      case 'element.lookup': return { operation: request.operation, handle: this.graph.findVertex(elementKey(request.payload.identity)) ?? null };
      case 'element.details': { const handle = this.graph.findVertex(elementKey(request.payload.identity)); if (handle === undefined) throw new GraphQueryError('not-found'); return { operation: request.operation, handle, identity: request.payload.identity }; }
      case 'graph.counts': return { operation: request.operation, value: { ...this.filter(request.payload.filter, control).counts } };
      case 'search.page': return this.search(request, control, mode);
      case 'graph.neighbours': return { operation: request.operation, ...this.neighbours(request, control) };
      case 'graph.path': return { operation: request.operation, ...this.path(request, control) };
      default: throw new ContractError('unknown-operation', 'Operation does not read the graph index.');
    }
  }

  /**
   * Materialize a bounded logical response for direct in-worker consumers.
   * @param request Valid S04 request; production pull transport instead uses select().
   * @param control Optional cancellation observation checked before each reconstruction.
   * @returns Detached public records and the same numeric projection/work metadata.
   * @throws {ContractError} For invalid context or transfer bounds.
   * @throws {GraphQueryError} For cancellation or absent details.
   */
  execute(request: GraphRequest, control?: QueryControl): GraphReply {
    const selection = this.select(request, control);
    switch (selection.operation) {
      case 'element.lookup': return { operation: selection.operation, value: { vertex: selection.handle === null ? null : this.vertex(selection.handle) } };
      case 'element.details': return { operation: selection.operation, value: { identity: selection.identity, attributes: this.attributes(selection.handle) } };
      case 'graph.counts': return selection;
      case 'search.page': {
        this.checkTransfer(selection.vertices, [], control);
        return { operation: selection.operation, value: { ...selection.terminal, items: selection.vertices.map(handle => { check(control); return this.vertex(handle); }) } };
      }
      case 'graph.neighbours': case 'graph.path': {
        this.checkTransfer(selection.handles.vertices, selection.handles.edges.map(edge => edge.handle), control);
        const projection: GraphProjection = { ...selection.projection,
          vertices: selection.handles.vertices.map(handle => { check(control); return this.vertex(handle); }),
          edges: selection.handles.edges.map(edge => { check(control); return this.edge(edge.handle); }) };
        return selection.operation === 'graph.neighbours'
          ? { operation: selection.operation, value: { projection }, handles: selection.handles, work: selection.work }
          : { operation: selection.operation, value: { projection, found: selection.found, complete: projection.complete }, handles: selection.handles, work: selection.work };
      }
    }
  }
  private checkTransfer(vertices: readonly number[], edges: readonly number[], control?: QueryControl): void {
    let bytes = 0;
    for (const handle of vertices) { check(control); bytes += this.wireBytes('vertex', handle); }
    for (const handle of edges) { check(control); bytes += this.wireBytes('edge', handle); }
    if (bytes > EXPLORE_LIMITS.transferBytes) throw new ContractError('resource-limit', 'Logical query exceeds the transfer limit.');
  }

  /**
   * Return exact deterministic facet counts without merging or changing graph records.
   * @param filter Existing S04 conditional vertex/relation selectors.
   * @param by Internal grouping dimension; nonapplicable vertices remain explicitly ungrouped.
   * @param control Optional atomic cancellation observer.
   * @returns Stable group tuples and exact ungrouped/cross-group counts.
   * @throws {ContractError} For disposed work or unsupported grouping dimension.
   * @throws {GraphQueryError} For cancellation.
   */
  groups(filter: Filter, by: GroupAxis, control?: QueryControl): GraphGroups {
    this.active(); check(control);
    assertRequest({ protocol: PROTOCOL, kind: 'request', requestId: 'group-filter', binding: this.binding, operation: 'graph.counts', payload: { filter } });
    if (!['project', 'kind', 'family', 'finding-state'].includes(by)) throw new ContractError('invalid-message', 'Unknown grouping dimension.');
    const view = this.filter(filter, control); const membership: (string | null)[] = Array(this.graph.vertexCount).fill(null);
    const groups = new Map<string, { value: string; vertices: number; edges: number; findings: number }>(); let ungroupedVertices = 0; let ungroupedEdges = 0; let crossGroupEdges = 0;
    for (let handle = 0; handle < this.graph.vertexCount; handle++) {
      check(control); if (!view.vertices[handle]) continue;
      const value = by === 'project' ? this.graph.vertexProject(handle) : by === 'kind' ? this.graph.vertexKind(handle) : by === 'family' ? this.graph.vertexFamily(handle) : this.graph.vertexFindingState(handle);
      if (value === null) { ungroupedVertices++; continue; }
      const id = JSON.stringify(['jai.fabric-explorer.group/1', by, value]); membership[handle] = id;
      const group = groups.get(id) ?? { value, vertices: 0, edges: 0, findings: 0 }; group.vertices++; if (this.graph.vertexKind(handle) === 'finding') group.findings++; groups.set(id, group);
    }
    for (let handle = 0; handle < this.graph.edgeCount; handle++) {
      check(control); if (!view.edges[handle]) continue;
      const from = membership[this.graph.edgeFrom(handle)]!; const to = membership[this.graph.edgeTo(handle)]!;
      if (from === null || to === null) ungroupedEdges++; else if (from !== to) crossGroupEdges++; else groups.get(from)!.edges++;
    }
    const values: GraphGroup[] = [...groups.entries()].sort(([left], [right]) => compare(left, right)).map(([id, group]) => ({ id, by, value: group.value, vertices: String(group.vertices), edges: String(group.edges), findings: String(group.findings) }));
    return { by, groups: values, ungroupedVertices: String(ungroupedVertices), ungroupedEdges: String(ungroupedEdges), crossGroupEdges: String(crossGroupEdges) };
  }

  /** Release worker-local index references and revoke its stateless cursor secret idempotently. */
  dispose(): void {
    if (this.closed) return; this.closed = true; this.secret.fill(0); this.cache = null; this.store = null;
  }
}
