// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Application-private bounded query transport; public S04 semantics remain unchanged. */
import type { Binding, Filter, Response, GraphProjection } from '@jai/fabric-explorer-contracts';
import type { GroupAxis } from '../graph/types.js';
import type { LayoutOptions } from '../layout/types.js';
/** Logical query frames and whole staged transfer bounds, in UTF8 bytes. */
export const EXPLORE_LIMITS = Object.freeze({ frameBytes: 2 * 1024 * 1024, transferBytes: 1024 * 1024 * 1024, jobs: 8, projections: 8 });
/** One pull reply; compact vertex handles align exactly with projection vertex order. */
export interface QueryPage { readonly frame: string; readonly continuationToken: string | null; readonly projectionToken: string | null; readonly handles: readonly number[] | null }
/** Private token lookup always retains the original request and current generation. */
export interface QueryContinuation { readonly binding: Binding; readonly requestId: string; readonly continuationToken: string }
/** Explicit release names only the owned tokens; no graph data or native path is accepted. */
export interface QueryDrop { readonly binding: Binding; readonly requestId: string; readonly continuationToken: string | null; readonly projectionToken: string | null }
/** Layout selects an existing worker-owned visible projection, never a renderer graph. */
export interface LayoutSelection { readonly binding: Binding; readonly requestId: string; readonly projectionToken: string; readonly options: Partial<LayoutOptions> }
/** Facet grouping over the same indexed filter semantics as counts/search. */
export interface GroupSelection { readonly binding: Binding; readonly requestId: string; readonly filter: Filter; readonly by: GroupAxis }
/** Fully validated staged result; numeric handles are ephemeral and cannot grant authority. */
export interface QueryView { readonly response: Response; readonly projectionToken: string | null; readonly handles: readonly number[] | null }

/** Filter an existing bounded projection; only its opaque token crosses the channel. */
export interface ProjectionFilterSelection { readonly binding: Binding; readonly requestId: string; readonly baseProjectionToken: string; readonly filter: Filter }
/** Closed bounded filtered view; masks align with the original projection, using low bits first. */
export interface ProjectionFilterView { readonly binding: Binding; readonly requestId: string; readonly baseProjectionToken: string; readonly projectionToken: string; readonly handles: readonly number[]; readonly vertexMask: string; readonly edgeMask: string; readonly hiddenVertices: string; readonly hiddenEdges: string; readonly complete: boolean; readonly omissions: GraphProjection['omissions'] }
