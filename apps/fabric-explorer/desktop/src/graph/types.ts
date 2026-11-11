// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Worker-local graph/query ports; public results keep the existing read-only S04 contract. */
import type { Binding, Edge, GraphProjection, Request, ResponsePayloads, SnapshotDescriptor, Vertex } from '@jai/fabric-explorer-contracts';
import type { SealedGraphStore } from '../import/compact-store.js';

/** One sealed graph; production shares its store, while direct fixtures are compact-admitted once. */
export type GraphData = { readonly snapshot: SnapshotDescriptor; readonly store: SealedGraphStore } | { readonly snapshot: SnapshotDescriptor; readonly records: Iterable<Vertex | Edge> };
/** Read-only operations whose data comes from the accepted graph, not live sources. */
export type GraphRequest = Extract<Request, { readonly operation: 'element.lookup' | 'element.details' | 'search.page' | 'graph.counts' | 'graph.neighbours' | 'graph.path' }>;
/** Optional cancellation observation, supplied by the worker from main-owned atomic state. */
export interface QueryControl {
  /** Return true after cancellation; implementations must be synchronous and side-effect free. */
  cancelled(): boolean;
}
/** Numeric projection edge; the original parallel edge identity remains resolvable by handle. */
export interface HandleEdge { readonly handle: number; readonly from: number; readonly to: number }
/** Bounded projection for worker-local layout; handles are canonical-ID-sorted generation-local ordinals. */
export interface HandleProjection { readonly vertices: readonly number[]; readonly edges: readonly HandleEdge[] }
/** Exact indexed membership of a retained bounded projection; masks use little-endian bits per byte. */
export interface FilteredHandles { readonly handles: HandleProjection; readonly vertexMask: string; readonly edgeMask: string; readonly hiddenVertices: string; readonly hiddenEdges: string; readonly filtered: boolean }
/** Actual bounded traversal work, independent of visible output capacity. */
export interface QueryWork { readonly visitedVertices: number; readonly scannedEdges: number }
/** Internal graph result; parent transport emits only the existing S04 payload. */
export interface ProjectionResult { readonly projection: GraphProjection; readonly handles: HandleProjection; readonly work: QueryWork }
/** Numeric-only projection selection; complete public records are reconstructed only for bounded output. */
export interface ProjectionSelection { readonly projection: Omit<GraphProjection, 'vertices' | 'edges'>; readonly handles: HandleProjection; readonly work: QueryWork }
/** Existing query payload plus compact layout view for projection-producing operations. */
export type GraphReply =
  | { readonly operation: 'element.lookup'; readonly value: ResponsePayloads['element.lookup'] }
  | { readonly operation: 'element.details'; readonly value: ResponsePayloads['element.details'] }
  | { readonly operation: 'search.page'; readonly value: ResponsePayloads['search.page'] }
  | { readonly operation: 'graph.counts'; readonly value: ResponsePayloads['graph.counts'] }
  | ({ readonly operation: 'graph.neighbours'; readonly value: ResponsePayloads['graph.neighbours'] } & Omit<ProjectionResult, 'projection'>)
  | ({ readonly operation: 'graph.path'; readonly value: ResponsePayloads['graph.path'] } & Omit<ProjectionResult, 'projection'>);
/** Worker-local lazy query result; no whole expanded result is retained by production transport. */
export type GraphSelection =
  | { readonly operation: 'element.lookup'; readonly handle: number | null }
  | { readonly operation: 'element.details'; readonly handle: number; readonly identity: ResponsePayloads['element.details']['identity'] }
  | { readonly operation: 'graph.counts'; readonly value: ResponsePayloads['graph.counts'] }
  | { readonly operation: 'search.page'; readonly vertices: readonly number[]; readonly terminal: Omit<ResponsePayloads['search.page'], 'items'> }
  | ({ readonly operation: 'graph.neighbours' } & ProjectionSelection)
  | ({ readonly operation: 'graph.path'; readonly found: boolean | null } & ProjectionSelection);
/** Deterministic internal grouping dimensions; no new public operation is introduced. */
export type GroupAxis = 'project' | 'kind' | 'family' | 'finding-state';
/** Stable facet group address and exact internal counts; no element is merged or rewritten. */
export interface GraphGroup { readonly id: string; readonly by: GroupAxis; readonly value: string; readonly vertices: string; readonly edges: string; readonly findings: string }
/** Group counts disclose nonapplicable vertices and edges crossing group boundaries. */
export interface GraphGroups { readonly by: GroupAxis; readonly groups: readonly GraphGroup[]; readonly ungroupedVertices: string; readonly ungroupedEdges: string; readonly crossGroupEdges: string }
/** Exact accepted work binding used by graph and layout consumers. */
export type GraphBinding = Binding & { readonly capability: string; readonly generation: string };
