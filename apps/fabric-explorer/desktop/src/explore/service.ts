// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Accepted-worker query ownership, finite pull delivery and numeric layout selection. */
import { randomUUID } from 'node:crypto';
import { PROTOCOL, assertBinding, assertRequest, encodeFrame, encodeChunkFrame, encodeWire } from '@jai/fabric-explorer-contracts';
import type { Binding, Edge, Request, Response, ResponseChunk, Vertex, GraphProjection } from '@jai/fabric-explorer-contracts';
import { QueryIndex } from '../graph/query-index.js';
import type { GraphRequest, HandleProjection, QueryControl } from '../graph/types.js';
import { layoutProjection } from '../layout/engine.js';
import type { LayoutResult } from '../layout/types.js';
import { ImportError } from '../import/types.js';
import { graphGroups } from './transport.js';
import { EXPLORE_LIMITS } from './types.js';
import type { GroupSelection, LayoutSelection, QueryContinuation, QueryDrop, QueryPage, ProjectionFilterSelection, ProjectionFilterView } from './types.js';
interface Projection { readonly requestId: string; readonly handles: HandleProjection; readonly complete: boolean; readonly omissions: GraphProjection['omissions'] }
interface Job { readonly request: GraphRequest; readonly operation: 'search.page' | 'graph.neighbours' | 'graph.path'; readonly vertices: readonly number[]; readonly edges: readonly number[]; readonly terminal: unknown; readonly projectionToken: string | null; readonly handles: readonly number[] | null; vertex: number; edge: number; sequence: number; transferred: number }
const bytes = (text: string) => Buffer.byteLength(text, 'utf8');
function closed(input: unknown, names: string): void { if (!input || typeof input !== 'object' || Array.isArray(input) || Object.keys(input).sort().join() !== names) throw new ImportError('invalid-message', 'Invalid exploration selection.'); }
/** One accepted-generation owner; jobs retain numeric selections and reconstruct records one frame at a time. */
export class ExploreService {
  private readonly jobs = new Map<string, Job>();
  private readonly projections = new Map<string, Projection>();
  private running = 0;
  /**
   * Bind the already sealed index to its accepted generation.
   * @param index Worker-local immutable record index owned by this service.
   * @param binding Current descriptor generation and exact source capability.
   */
  constructor(private readonly index: QueryIndex, private readonly binding: Binding) {}
  private context(binding: Binding, requestId: string): void { assertBinding(binding, this.binding); if (typeof requestId !== 'string' || !/^[A-Za-z0-9._:-]{1,128}$/.test(requestId)) throw new ImportError('invalid-message', 'Invalid exploration request.'); }
  private check(control?: QueryControl): void { if (control?.cancelled()) throw new ImportError('cancelled', 'Exploration cancelled.'); }
  /**
   * Execute a validated read-only query and stage at most one bounded result.
   * @param request Original operation-specific S04 request.
   * @param control Synchronous main-owned atomic cancellation observation.
   * @param mode Fixed application entry selects ordinary records or findings only.
   * @returns First bounded frame plus opaque owned continuation/projection tokens.
   * @throws {ImportError} For cancellation, stale binding or byte/job bounds.
   */
  start(request: GraphRequest, control?: QueryControl, mode: 'all' | 'findings' = 'all'): QueryPage {
    assertRequest(request); this.context(request.binding, request.requestId); this.check(control);
    if (this.jobs.size + this.running >= EXPLORE_LIMITS.jobs) throw new ImportError('resource-limit', 'Exploration job limit exceeded.');
    if (mode === 'findings' && request.operation !== 'search.page') throw new ImportError('invalid-message', 'Invalid findings operation.');
    const reply = this.index.select(request, control, mode); this.check(control);
    let projectionToken: string | null = null; let handles: readonly number[] | null = null;
    if ('handles' in reply) {
      if (this.projections.size >= EXPLORE_LIMITS.projections) throw new ImportError('resource-limit', 'Projection limit exceeded; release an existing projection.');
      projectionToken = randomUUID(); handles = reply.handles.vertices;
      this.projections.set(projectionToken, { requestId: request.requestId, handles: reply.handles, complete: reply.projection.complete, omissions: reply.projection.omissions });
    }
    try {
      if (reply.operation === 'element.lookup' || reply.operation === 'element.details' || reply.operation === 'graph.counts') {
        if (reply.operation === 'element.lookup' && reply.handle !== null || reply.operation === 'element.details') {
          const placeholder = reply.operation === 'element.lookup' ? { vertex: null } : { identity: reply.identity, attributes: null };
          const envelope = bytes(encodeWire({ protocol: PROTOCOL, kind: 'response', requestId: request.requestId, binding: request.binding, operation: reply.operation, status: 'ok', payload: placeholder })) - 4;
          const recordBytes = reply.operation === 'element.lookup' ? this.index.wireBytes('vertex', reply.handle!) : this.index.attributeWireBytes(reply.handle);
          if (envelope + recordBytes > EXPLORE_LIMITS.frameBytes) throw new ImportError('resource-limit', 'Query record exceeds the frame limit.');
        }
        const payload = reply.operation === 'element.lookup' ? { vertex: reply.handle === null ? null : this.index.vertex(reply.handle) }
          : reply.operation === 'element.details' ? { identity: reply.identity, attributes: this.index.attributes(reply.handle) } : reply.value;
        const frame = encodeFrame({ protocol: PROTOCOL, kind: 'response', requestId: request.requestId, binding: request.binding, operation: reply.operation, status: 'ok', payload } as Response);
        if (bytes(frame) > EXPLORE_LIMITS.frameBytes) throw new ImportError('resource-limit', 'Query record exceeds the frame limit.');
        return { frame, continuationToken: null, projectionToken, handles };
      }
      const vertices = reply.operation === 'search.page' ? reply.vertices : reply.handles.vertices;
      const edges = reply.operation === 'search.page' ? [] : reply.handles.edges.map(edge => edge.handle);
      let terminal: unknown;
      if (reply.operation === 'search.page') terminal = reply.terminal;
      else { const { format: _format, ...rest } = reply.projection; terminal = reply.operation === 'graph.path' ? { ...rest, found: reply.found } : rest; }
      let recordBytes = 0;
      for (const handle of vertices) { this.check(control); recordBytes += this.index.wireBytes('vertex', handle); }
      for (const handle of edges) { this.check(control); recordBytes += this.index.wireBytes('edge', handle); }
      if (recordBytes > EXPLORE_LIMITS.transferBytes) throw new ImportError('resource-limit', 'Query transfer exceeds its byte limit.');
      return this.page({ request, operation: reply.operation, vertices, edges, terminal, projectionToken, handles, vertex: 0, edge: 0, sequence: 0, transferred: 0 }, control);
    } catch (error) { if (projectionToken) this.projections.delete(projectionToken); throw error; }
  }

  private page(job: Job, control?: QueryControl): QueryPage {
    this.check(control);
    const base = { protocol: PROTOCOL, kind: 'response-chunk' as const, requestId: job.request.requestId, binding: job.request.binding, operation: job.operation, sequence: String(job.sequence) };
    const vertices: Vertex[] = []; const edges: Edge[] = [];
    let size = bytes(encodeWire({ ...base, vertices: [], edges: [], terminal: job.terminal })) + 128;
    if (size > EXPLORE_LIMITS.frameBytes) throw new ImportError('resource-limit', 'Query metadata exceeds the frame limit.');
    while (job.vertex < job.vertices.length || job.edge < job.edges.length) {
      this.check(control); const vertex = job.vertex < job.vertices.length;
      const handle = vertex ? job.vertices[job.vertex]! : job.edges[job.edge]!;
      const length = this.index.wireBytes(vertex ? 'vertex' : 'edge', handle) + 1;
      if (size + length > EXPLORE_LIMITS.frameBytes) {
        if (!vertices.length && !edges.length) throw new ImportError('resource-limit', 'Query record exceeds the frame limit.');
        break;
      }
      size += length;
      if (vertex) { vertices.push(this.index.vertex(handle)); job.vertex++; } else { edges.push(this.index.edge(handle)); job.edge++; }
    }
    const done = job.vertex === job.vertices.length && job.edge === job.edges.length;
    const frame = encodeChunkFrame({ ...base, vertices, edges, terminal: done ? job.terminal : null } as ResponseChunk);
    if (bytes(frame) > EXPLORE_LIMITS.frameBytes) throw new ImportError('resource-limit', 'Query frame exceeds the frame limit.');
    job.transferred += bytes(frame);
    if (job.transferred > EXPLORE_LIMITS.transferBytes) throw new ImportError('resource-limit', 'Query transfer exceeds its byte limit.');
    this.check(control); job.sequence++;
    const continuationToken = done ? null : randomUUID(); if (continuationToken) this.jobs.set(continuationToken, job);
    return { frame, continuationToken, projectionToken: job.projectionToken, handles: job.handles };
  }
  /**
   * Consume one continuation exactly once, retaining request/generation correlation.
   * @param input Closed current-binding continuation selection.
   * @param control Optional atomic cancellation observation.
   * @returns Next finite-progress frame.
   * @throws {ImportError} For unknown/replayed tokens, stale context or resource bounds.
   */
  next(input: QueryContinuation, control?: QueryControl): QueryPage {
    closed(input, 'binding,continuationToken,requestId'); this.context(input.binding, input.requestId);
    const job = this.jobs.get(input.continuationToken);
    if (!job || job.request.requestId !== input.requestId) throw new ImportError('not-found', 'Query continuation is unavailable.');
    this.jobs.delete(input.continuationToken);
    try { return this.page(job, control); } catch (error) { if (job.projectionToken) this.projections.delete(job.projectionToken); throw error; }
  }
  /**
   * Release only tokens owned by the supplied current request; repeated release is safe.
   * @param input Exact context and optional job/projection tokens.
   * @returns Nothing; canonical source data is unchanged.
   * @throws {ImportError} For malformed/stale/cross-request token selection.
   */
  drop(input: QueryDrop): void {
    closed(input, 'binding,continuationToken,projectionToken,requestId'); this.context(input.binding, input.requestId);
    const job = input.continuationToken === null ? undefined : this.jobs.get(input.continuationToken);
    const projection = input.projectionToken === null ? undefined : this.projections.get(input.projectionToken);
    if ((job && job.request.requestId !== input.requestId) || (projection && projection.requestId !== input.requestId)) throw new ImportError('capability-mismatch', 'Exploration token belongs to another request.');
    if (input.continuationToken !== null) this.jobs.delete(input.continuationToken);
    if (input.projectionToken !== null) this.projections.delete(input.projectionToken);
  }
  /**
   * Layout an existing bounded projection without cloning records or original edge IDs.
   * @param input Current generation, owned projection token and finite layout options.
   * @param control Main-owned cancellation observation.
   * @returns Numeric positions and derived SCC groups bound to this exact layout request.
   * @throws {ImportError} For unknown tokens, stale generation, cancellation or concurrent work bounds.
   */
  async layout(input: LayoutSelection, control?: QueryControl): Promise<LayoutResult> {
    closed(input, 'binding,options,projectionToken,requestId'); this.context(input.binding, input.requestId); this.check(control);
    const projection = this.projections.get(input.projectionToken);
    if (!projection) throw new ImportError('not-found', 'Projection is unavailable.');
    if (this.running + this.jobs.size >= EXPLORE_LIMITS.jobs) throw new ImportError('resource-limit', 'Exploration job limit exceeded.');
    this.running++;
    try { return await layoutProjection({ binding: { sessionId: this.binding.sessionId, capability: this.binding.capability!, generation: this.binding.generation!, requestId: input.requestId, projectionId: input.projectionToken }, graph: projection.handles, options: input.options }, { cancelled: () => !!control?.cancelled() || !this.projections.has(input.projectionToken) }); }
    finally { this.running--; }
  }
  /**
   * Filter a retained bounded projection without copying semantic attributes.
   * @param input Current generation, original projection token and existing S04 filter.
   * @param control Optional atomic cancellation observation.
   * @returns Masks aligned to the original projection plus a separately owned layout token.
   * @throws {ImportError} For stale context, unknown base token, cancellation or projection bounds.
   */
  filterProjection(input: ProjectionFilterSelection, control?: QueryControl): ProjectionFilterView {
    closed(input, 'baseProjectionToken,binding,filter,requestId'); this.context(input.binding, input.requestId); this.check(control);
    const base = this.projections.get(input.baseProjectionToken);
    if (!base) throw new ImportError('not-found', 'Projection is unavailable.');
    if (this.projections.size >= EXPLORE_LIMITS.projections) throw new ImportError('resource-limit', 'Projection limit exceeded; release an existing projection.');
    const filtered = this.index.filterProjection(base.handles, input.filter, control); this.check(control);
    const projectionToken = randomUUID();
    const omissions = filtered.filtered ? [...new Set([...base.omissions, 'filter' as const])] : base.omissions;
    const result: ProjectionFilterView = { binding: this.binding, requestId: input.requestId, baseProjectionToken: input.baseProjectionToken, projectionToken, handles: filtered.handles.vertices, vertexMask: filtered.vertexMask, edgeMask: filtered.edgeMask, hiddenVertices: filtered.hiddenVertices, hiddenEdges: filtered.hiddenEdges, complete: base.complete, omissions };
    if (bytes(encodeWire(result)) > EXPLORE_LIMITS.frameBytes) throw new ImportError('resource-limit', 'Projection filter frame limit exceeded.');
    this.projections.set(projectionToken, { requestId: input.requestId, handles: filtered.handles, complete: base.complete, omissions });
    return result;
  }
  /**
   * Group current indexed records using the existing filter without mutating the graph.
   * @param input Closed bound facet selection.
   * @param control Main-owned cancellation observation.
   * @returns Exact deterministic group counts with omission metadata.
   * @throws {Error} For invalid filters/axis, stale context or cancellation.
   */
  groups(input: GroupSelection, control?: QueryControl) { closed(input, 'binding,by,filter,requestId'); this.context(input.binding, input.requestId); this.check(control); return graphGroups(this.index.groups(input.filter, input.by, control), input.by); }
  /** Revoke ephemeral query/projection state when this accepted worker is replaced. */
  dispose(): void { this.jobs.clear(); this.projections.clear(); this.index.dispose(); }
}
