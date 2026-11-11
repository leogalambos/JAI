// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Immutable external-store contracts for the read-only exploration interface. */
import type { Attributes, Binding, BytePage, Counts, Edge, ElementIdentity, Filter, GraphProjection, RequestPayloads, ResponsePayloads, Vertex } from '@jai/fabric-explorer-contracts';
import type { GraphGroups, GroupAxis } from '../../graph/types.js';
import type { LayoutResult } from '../../layout/types.js';
import type { ShellState } from '../../shell/controller.js';

/** Independently superseded groups of asynchronous presentation work. */
export type ExploreLane = 'overview' | 'search' | 'findings' | 'selection' | 'graph' | 'filter' | 'source' | 'groups';
/** A finite server page; append combines only explicitly requested pages. */
export type ExplorePage = ResponsePayloads['search.page'] & { readonly text: string; readonly order: 'identity' | 'label' };
/** Exact selected records; unresolved or ambiguous finding subjects remain explicit candidates. */
export interface ExploreSelection { readonly element: Vertex | Edge; readonly attributes: Attributes; readonly endpoints: readonly Vertex[]; readonly subjectCandidates: readonly Vertex[]; readonly subjectComplete: boolean }
/** Original raw bytes with a display-only UTF-8 interpretation; offsets always count bytes. */
export interface ExploreSourcePage { readonly page: BytePage; readonly text: string }
/** One stable publication consumed through subscribe/getSnapshot, including by useSyncExternalStore. */
export interface ExploreState {
  readonly shell: ShellState | null;
  readonly binding: Binding | null;
  readonly busy: readonly ExploreLane[];
  readonly error: string | null;
  readonly message: string | null;
  readonly filter: Filter;
  readonly search: ExplorePage | null;
  readonly findings: ExplorePage | null;
  readonly counts: Counts | null;
  readonly groups: GraphGroups | null;
  readonly groupAxis: GroupAxis;
  readonly projection: GraphProjection | null;
  readonly handles: readonly number[];
  readonly layout: LayoutResult | null;
  readonly selection: ExploreSelection | null;
  readonly sourcePage: ExploreSourcePage | null;
  readonly history: { readonly canBack: boolean; readonly canForward: boolean };
}
/** Optional traversal changes; absence retains finite application defaults. */
export type NeighbourOptions = Partial<Omit<RequestPayloads['graph.neighbours'], 'identity'>> & { readonly identity?: ElementIdentity };
/** Directed path controls never derive direction from visual placement. */
export type PathOptions = Partial<Omit<RequestPayloads['graph.path'], 'from' | 'to'>>;
