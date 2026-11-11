// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Browser-safe closed envelope and finite staged query transfer validation. */
import { advanceChunks, assertResponseForRequest, decodeChunkFrame, decodeResponseFrame, startChunks, PROTOCOL, encodeWire, ContractError, assertBinding } from '@jai/fabric-explorer-contracts';
import type { Binding, ChunkState, Edge, Request, Response, ResponseChunk, Vertex } from '@jai/fabric-explorer-contracts';
import type { GraphGroups, GroupAxis } from '../graph/types.js';
import { EXPLORE_LIMITS } from './types.js';
import type { QueryPage, QueryView, ProjectionFilterView, ProjectionFilterSelection } from './types.js';
/**
 * Reject extra private authority fields and oversized logical query frames.
 * @param input Untrusted structured-clone response from the owned channel.
 * @returns Closed bounded query page with only opaque tokens and numeric vertex handles.
 * @throws {Error} For malformed values or logical frame bounds.
 */
export function queryPage(input: unknown): QueryPage {
  if (!input || typeof input !== 'object' || Array.isArray(input) || Object.keys(input).sort().join() !== 'continuationToken,frame,handles,projectionToken') throw new Error('Invalid query envelope');
  const page = input as QueryPage;
  const token = (value: unknown) => value === null || (typeof value === 'string' && /^[A-Za-z0-9-]{1,128}$/.test(value));
  if (typeof page.frame !== 'string' || new TextEncoder().encode(page.frame).length > EXPLORE_LIMITS.frameBytes || !token(page.continuationToken) || !token(page.projectionToken) || (page.handles !== null && (!Array.isArray(page.handles) || page.handles.length > 5000 || page.handles.some(value => !Number.isInteger(value) || value < 0 || value > 0xffffffff) || new Set(page.handles).size !== page.handles.length))) throw new Error('Invalid query envelope');
  if ((page.projectionToken === null) !== (page.handles === null)) throw new Error('Invalid projection envelope');
  return page;
}
/** Bounded receiver state; full records are assembled only in the preload consumer, never main. */
export class QueryTransfer {
  private state: ChunkState | null = null;
  private readonly vertices: Vertex[] = [];
  private readonly edges: Edge[] = [];
  private total = 0;
  private ended = false;
  private projection: string | null | undefined;
  private handles: readonly number[] | null = null;
  /**
   * Retain a validated original request and choose whether this receiver stages full records.
   * @param request Original S04 query context, not a peer-returned request.
   * @param assemble False for main's metadata-only validation; true for preload assembly.
   */
  constructor(private readonly request: Request, private readonly assemble: boolean) {}
  /**
   * Accept one correlated page and optionally finish a validated logical response.
   * @param input Untrusted private envelope.
   * @param current Trusted current session/capability/generation.
   * @returns Completed assembled view or null while progress remains (also null for main chunk terminals).
   * @throws {Error} For stale, out-of-order, excessive, inconsistent or postterminal data.
   */
  accept(input: unknown, current: Binding): QueryView | null {
    if (this.ended) throw new Error('Query already ended');
    const page = queryPage(input); this.total += new TextEncoder().encode(page.frame).length;
    if (this.total > EXPLORE_LIMITS.transferBytes) throw new Error('Query transfer byte limit');
    if (this.projection === undefined) { this.projection = page.projectionToken; this.handles = page.handles; }
    else if (page.projectionToken !== this.projection || JSON.stringify(page.handles) !== JSON.stringify(this.handles)) throw new Error('Projection changed during query');
    let chunk: ResponseChunk;
    // The discriminant is checked by the maintained contract decoders; it selects no executable operation.
    if (JSON.parse(page.frame).kind === 'response') {
      if (this.state || page.continuationToken !== null) throw new Error('Unexpected scalar reply');
      const response = decodeResponseFrame(page.frame); assertResponseForRequest(response, this.request, current); this.ended = true;
      if (page.projectionToken !== null) throw new Error('Scalar projection is invalid');
      return { response, projectionToken: null, handles: null };
    }
    chunk = decodeChunkFrame(page.frame);
    this.state = advanceChunks(this.state ?? startChunks(this.request), chunk, this.request, current);
    if (this.state.ended !== (page.continuationToken === null)) throw new Error('Query terminal/token mismatch');
    if (this.assemble) { this.vertices.push(...chunk.vertices); this.edges.push(...chunk.edges); }
    if (!this.state.ended) return null;
    this.ended = true;
    if (page.handles !== null && page.handles.length !== this.state.vertices) throw new Error('Projection handles do not match vertices');
    if (!this.assemble) return null;
    const base = { protocol: PROTOCOL, kind: 'response' as const, requestId: this.request.requestId, operation: chunk.operation, binding: this.request.binding, status: 'ok' as const };
    let response: Response;
    if (chunk.operation === 'search.page') response = { ...base, operation: 'search.page', payload: { ...chunk.terminal!, items: this.vertices } };
    else {
      const terminal = chunk.terminal!;
      const { found: _found, ...graph } = terminal as typeof terminal & { found?: boolean | null };
      const projection = { ...graph, format: 'jai.fabric-explorer.projection/1' as const, vertices: this.vertices, edges: this.edges };
      response = chunk.operation === 'graph.path' ? { ...base, operation: 'graph.path', payload: { projection, found: chunk.terminal!.found, complete: terminal.complete } } : { ...base, operation: 'graph.neighbours', payload: { projection } };
    }
    assertResponseForRequest(response, this.request, current);
    return { response, projectionToken: page.projectionToken, handles: page.handles };
  }
}

/**
 * Validate a bounded app-private grouping result against its retained requested axis.
 * @param input Untrusted group metadata; no complete source records are permitted.
 * @param by Retained requested grouping dimension.
 * @returns Closed deterministic count metadata after byte/count checks.
 * @throws {Error} For unknown fields, mismatched dimensions or excessive/invalid counts.
 */
export function graphGroups(input: unknown, by: GroupAxis): GraphGroups {
  if (!input || typeof input !== 'object' || Array.isArray(input) || Object.keys(input).sort().join() !== 'by,crossGroupEdges,groups,ungroupedEdges,ungroupedVertices') throw new Error('Invalid groups result');
  const value = input as GraphGroups;
  const count = (item: unknown, max: bigint) => typeof item === 'string' && /^(?:0|[1-9][0-9]{0,6})$/.test(item) && BigInt(item) <= max;
  if (!['project', 'kind', 'family', 'finding-state'].includes(by) || value.by !== by || !Array.isArray(value.groups) || value.groups.length > 100000 || !count(value.crossGroupEdges, 500000n) || !count(value.ungroupedEdges, 500000n) || !count(value.ungroupedVertices, 100000n)) throw new Error('Invalid groups result');
  const ids = new Set<string>();
  for (const group of value.groups) {
    if (!group || Object.keys(group).sort().join() !== 'by,edges,findings,id,value,vertices' || group.by !== by || typeof group.id !== 'string' || typeof group.value !== 'string' || ids.has(group.id) || !count(group.vertices, 100000n) || !count(group.edges, 500000n) || !count(group.findings, 100000n) || BigInt(group.findings) > BigInt(group.vertices) || BigInt(group.vertices) === 0n) throw new Error('Invalid group metadata');
    ids.add(group.id);
  }
  if (new TextEncoder().encode(encodeWire(value)).length > EXPLORE_LIMITS.frameBytes) throw new ContractError('resource-limit', 'Groups frame limit exceeded'); return value;
}

/**
 * Validate a closed bounded filtered projection reply and exact retained correlation.
 * @param input Untrusted worker or authenticated channel result.
 * @param selection Original requested filter context, never peer-returned authority.
 * @returns Validated masks and new ephemeral projection ownership.
 * @throws {Error} For unknown fields, malformed masks/counts or mismatched context.
 */
export function projectionFilterView(input: unknown, selection: ProjectionFilterSelection): ProjectionFilterView {
  if (!input || typeof input !== 'object' || Array.isArray(input) || Object.keys(input).sort().join() !== 'baseProjectionToken,binding,complete,edgeMask,handles,hiddenEdges,hiddenVertices,omissions,projectionToken,requestId,vertexMask') throw new Error('Invalid projection filter envelope');
  const value = input as ProjectionFilterView;
  assertBinding(value.binding, selection.binding);
  const count = (item: unknown) => typeof item === 'string' && /^(?:0|[1-9][0-9]*)$/.test(item) && item.length <= 16;
  const mask = (item: unknown, max: number) => typeof item === 'string' && item.length <= Math.ceil(Math.ceil(max / 8) / 3) * 4 && /^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$/.test(item) && btoa(atob(item)) === item;
  if (value.requestId !== selection.requestId || value.baseProjectionToken !== selection.baseProjectionToken || typeof value.projectionToken !== 'string' || !/^[A-Za-z0-9-]{1,128}$/.test(value.projectionToken) || value.projectionToken === value.baseProjectionToken || !Array.isArray(value.handles) || value.handles.length > 5000 || value.handles.some(handle => !Number.isInteger(handle) || handle < 0 || handle > 0xffffffff) || new Set(value.handles).size !== value.handles.length || !mask(value.vertexMask, 5000) || !mask(value.edgeMask, 20000) || !count(value.hiddenVertices) || !count(value.hiddenEdges) || typeof value.complete !== 'boolean' || !Array.isArray(value.omissions) || new Set(value.omissions).size !== value.omissions.length || value.omissions.some(reason => !['filter', 'visible-limit', 'work-limit', 'unresolved', 'unavailable'].includes(reason)) || (value.complete && value.omissions.some(reason => reason !== 'filter')) || (!value.complete && !value.omissions.length) || new TextEncoder().encode(encodeWire(value)).length > EXPLORE_LIMITS.frameBytes) throw new Error('Invalid projection filter metadata');
  let visible = 0; for (const byte of atob(value.vertexMask)) { let bits = byte.charCodeAt(0); while (bits) { visible += bits & 1; bits >>>= 1; } }
  if (visible !== value.handles.length) throw new Error('Projection mask/handle mismatch');
  return value;
}
