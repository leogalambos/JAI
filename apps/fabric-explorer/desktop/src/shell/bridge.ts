/** Fixed renderer-facing application methods; no generic IPC, filesystem or process primitive is exposed. */
import { PROTOCOL, encodeFrame, decodeRequestFrame, decodeResponseFrame, assertResponseForRequest, assertBinding } from '@jai/fabric-explorer-contracts';
import type { Binding, RequestPayloads, SourceFamily } from '@jai/fabric-explorer-contracts';
import { decodeLayout } from '../explore/layout-wire.js';
import type { LayoutWireResult } from '../explore/layout-wire.js';
import { queryPage, QueryTransfer, graphGroups, projectionFilterView } from '../explore/transport.js';
import type { GraphRequest, GraphGroups, GroupAxis } from '../graph/types.js';
import type { QueryView, QueryDrop, ProjectionFilterView } from '../explore/types.js';
import type { LayoutOptions, LayoutResult } from '../layout/types.js';
import type { ShellState } from './controller.js';
import type { Preferences } from './preferences.js';
/** Private fixed channels shared only by preload and authenticated main handlers. */
export const CHANNELS = Object.freeze({ state: 'jai:state', request: 'jai:request', preferences: 'jai:preferences', cancelSelection: 'jai:cancel-selection', queryStart: 'jai:query-start', searchFindings: 'jai:search-findings', filterProjection: 'jai:filter-projection', queryNext: 'jai:query-next', queryDrop: 'jai:query-drop', layout: 'jai:layout', groups: 'jai:groups' });
/** Owned invocation adapter, with no renderer-selectable channel. */
export interface InvokePort { invoke(channel: string, value?: unknown): Promise<unknown> }
/** Narrow application bridge; source bindings are opaque values, never native paths. */
export interface DesktopBridge {
  /** Obtain the current shell session and presentation preferences. */
  getState(): Promise<ShellState>;
  /** Invoke native project/file dialogs for explicitly selected source families. */
  pickRoots(binding: Binding, requestId: string, families: readonly SourceFamily[]): Promise<unknown>;
  /** Release the active root capability. */
  closeRoots(binding: Binding, requestId: string): Promise<unknown>;
  /**
   * Import explicit admitted source IDs into an atomic candidate snapshot.
   * @param binding Current session/capability and prior generation.
   * @param requestId Unique invocation identifier.
   * @param sourceIds Explicit admitted catalog IDs, never native paths.
   * @returns Validated correlated consumer response.
   * @throws {Error} For invalid input, unavailable transport or a mismatched reply.
   */
  importSnapshot(binding: Binding, requestId: string, sourceIds: readonly string[]): Promise<unknown>;
  /**
   * Refresh the accepted source subset against its exact current generation.
   * @param binding Current session/capability/generation.
   * @param requestId Unique invocation identifier.
   * @returns Validated correlated consumer response.
   * @throws {Error} For invalid input, unavailable transport or a mismatched reply.
   */
  refreshSnapshot(binding: Binding, requestId: string): Promise<unknown>;
  /**
   * Read one bounded original-revision source page; no native path is accepted.
   * @param binding Current session/capability/generation.
   * @param requestId Unique invocation identifier.
   * @param payload Exact source locator and bounded byte range.
   * @returns Validated response matching the requested source and byte range.
   * @throws {Error} For invalid input, unavailable transport or a mismatched reply.
   */
  pageSource(binding: Binding, requestId: string, payload: RequestPayloads['source.page']): Promise<unknown>;
  /** Look up an exact stable identity in the accepted graph. */
  lookup(binding: Binding, requestId: string, payload: RequestPayloads['element.lookup']): Promise<QueryView>;
  /** Read complete inline attributes or the existing lossless paged descriptor. */
  details(binding: Binding, requestId: string, payload: RequestPayloads['element.details']): Promise<QueryView>;
  /** Search a bounded current-generation page with validated cursor continuity. */
  search(binding: Binding, requestId: string, payload: RequestPayloads['search.page']): Promise<QueryView>;
  /** Search finding records through the existing staged S04 search contract. */
  searchFindings(binding: Binding, requestId: string, payload: RequestPayloads['search.page']): Promise<QueryView>;
  /** Filter a bounded existing projection; returned masks preserve original array alignment. */
  filterProjection(binding: Binding, requestId: string, baseProjectionToken: string, filter: RequestPayloads['graph.counts']['filter']): Promise<ProjectionFilterView>;
  /** Count records under the current shared indexed filter. */
  counts(binding: Binding, requestId: string, payload: RequestPayloads['graph.counts']): Promise<QueryView>;
  /** Build a bounded directed neighbourhood and retain its numeric layout projection. */
  neighbours(binding: Binding, requestId: string, payload: RequestPayloads['graph.neighbours']): Promise<QueryView>;
  /** Find one bounded directed path without asserting absence after exhausted work. */
  path(binding: Binding, requestId: string, payload: RequestPayloads['graph.path']): Promise<QueryView>;
  /** Release only this consumer's retained projection/job tokens. */
  dropQuery(input: QueryDrop): Promise<void>;
  /** Compute ephemeral coordinates from an existing current-generation projection token. */
  layout(binding: Binding, requestId: string, projectionToken: string, options: Partial<LayoutOptions>): Promise<LayoutResult>;
  /** Obtain current indexed facets without creating a new S04 operation. */
  groups(binding: Binding, requestId: string, filter: RequestPayloads['graph.counts']['filter'], by: GroupAxis): Promise<GraphGroups>;
  /** Cancel one active operation without changing source data. */
  cancelRequest(binding: Binding, requestId: string, targetRequestId: string): Promise<unknown>;
  /** Cancel a first native picker before any source capability exists. */
  cancelSelection(requestId: string): Promise<boolean>;
  /** Persist only the fixed presentation preference schema. */
  updatePreferences(preferences: Preferences): Promise<Preferences>;
}
/**
 * Construct immutable named methods over a trusted preload invocation adapter.
 * @param port Trusted preload-only invocation adapter.
 * @returns Frozen named application methods.
 */
export function createBridge(port: InvokePort): DesktopBridge {
  const send = async (binding: Binding, requestId: string, operation: 'roots.pick' | 'roots.close' | 'request.cancel' | 'snapshot.import' | 'snapshot.refresh' | 'source.page', payload: unknown) => {
    const frame = encodeFrame({ protocol: PROTOCOL, kind: 'request', binding, requestId, operation, payload } as Parameters<typeof encodeFrame>[0]);
    const request = decodeRequestFrame(frame);
    const result = await port.invoke(CHANNELS.request, frame);
    if (typeof result !== 'string') throw new Error('Invalid application response');
    const response = decodeResponseFrame(result); assertResponseForRequest(response, request, request.binding); return response;
  };
  const current = async (): Promise<Binding> => { const state = await port.invoke(CHANNELS.state) as ShellState; return { sessionId: state.sessionId, capability: state.capability, generation: state.snapshot?.generation ?? null }; };
  const query = async (binding: Binding, requestId: string, operation: GraphRequest['operation'], payload: unknown, mode: 'all' | 'findings' = 'all'): Promise<QueryView> => {
    const frame = encodeFrame({ protocol: PROTOCOL, kind: 'request', binding, requestId, operation, payload } as GraphRequest);
    const request = decodeRequestFrame(frame); const transfer = new QueryTransfer(request, true);
    let page: ReturnType<typeof queryPage> | null = null;
    try {
      page = queryPage(await port.invoke(mode === 'findings' ? CHANNELS.searchFindings : CHANNELS.queryStart, frame));
      for (;;) {
        const result = transfer.accept(page, await current());
        if (result) return result;
        if (!page.continuationToken) throw new Error('Incomplete query response');
        page = queryPage(await port.invoke(CHANNELS.queryNext, { binding, requestId, continuationToken: page.continuationToken }));
      }
    } catch (error) {
      if (page) await port.invoke(CHANNELS.queryDrop, { binding, requestId, continuationToken: page.continuationToken, projectionToken: page.projectionToken }).catch(() => {});
      throw error;
    }
  };
  return Object.freeze({
    getState: async () => await port.invoke(CHANNELS.state) as ShellState,
    pickRoots: (binding: Binding, requestId: string, families: readonly SourceFamily[]) => send(binding, requestId, 'roots.pick', { families }),
    closeRoots: (binding: Binding, requestId: string) => send(binding, requestId, 'roots.close', {}),
    importSnapshot: (binding: Binding, requestId: string, sourceIds: readonly string[]) => send(binding, requestId, 'snapshot.import', { sourceIds }),
    refreshSnapshot: (binding: Binding, requestId: string) => send(binding, requestId, 'snapshot.refresh', {}),
    pageSource: (binding: Binding, requestId: string, payload: RequestPayloads['source.page']) => send(binding, requestId, 'source.page', payload),
    lookup: (binding: Binding, requestId: string, payload: RequestPayloads['element.lookup']) => query(binding, requestId, 'element.lookup', payload),
    details: (binding: Binding, requestId: string, payload: RequestPayloads['element.details']) => query(binding, requestId, 'element.details', payload),
    search: (binding: Binding, requestId: string, payload: RequestPayloads['search.page']) => query(binding, requestId, 'search.page', payload),
    searchFindings: (binding: Binding, requestId: string, payload: RequestPayloads['search.page']) => query(binding, requestId, 'search.page', payload, 'findings'),
    filterProjection: async (binding: Binding, requestId: string, baseProjectionToken: string, filter: RequestPayloads['graph.counts']['filter']) => {
      const selection = { binding, requestId, baseProjectionToken, filter }; let result: ProjectionFilterView | null = null;
      try { result = projectionFilterView(await port.invoke(CHANNELS.filterProjection, selection), selection); assertBinding(binding, await current()); return result; }
      catch (error) { if (result) await port.invoke(CHANNELS.queryDrop, { binding, requestId, continuationToken: null, projectionToken: result.projectionToken }).catch(() => {}); throw error; }
    },
    counts: (binding: Binding, requestId: string, payload: RequestPayloads['graph.counts']) => query(binding, requestId, 'graph.counts', payload),
    neighbours: (binding: Binding, requestId: string, payload: RequestPayloads['graph.neighbours']) => query(binding, requestId, 'graph.neighbours', payload),
    path: (binding: Binding, requestId: string, payload: RequestPayloads['graph.path']) => query(binding, requestId, 'graph.path', payload),
    dropQuery: async (input: QueryDrop) => { await port.invoke(CHANNELS.queryDrop, input); },
    layout: async (binding: Binding, requestId: string, projectionToken: string, options: Partial<LayoutOptions>) => { const result = decodeLayout(await port.invoke(CHANNELS.layout, { binding, requestId, projectionToken, options }) as LayoutWireResult); const now = await current(); if (result.binding.sessionId !== now.sessionId || result.binding.capability !== now.capability || result.binding.generation !== now.generation || result.binding.requestId !== requestId || result.binding.projectionId !== projectionToken) throw new Error('Stale layout response'); return result; },
    groups: async (binding: Binding, requestId: string, filter: RequestPayloads['graph.counts']['filter'], by: GroupAxis) => { const result = graphGroups(await port.invoke(CHANNELS.groups, { binding, requestId, filter, by }), by); assertBinding(binding, await current()); return result; },
    cancelRequest: (binding: Binding, requestId: string, targetRequestId: string) => send(binding, requestId, 'request.cancel', { targetRequestId }),
    cancelSelection: async (requestId: string) => await port.invoke(CHANNELS.cancelSelection, requestId) as boolean,
    updatePreferences: async (preferences: Preferences) => await port.invoke(CHANNELS.preferences, preferences) as Preferences,
  });
}
