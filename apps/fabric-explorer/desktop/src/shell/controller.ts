/** Authenticated desktop coordination; source semantics remain outside the S05 shell. */
import { randomUUID } from 'node:crypto';
import { PROTOCOL, decodeRequestFrame, encodeFrame, assertBinding, encodeWire } from '@jai/fabric-explorer-contracts';
import type { AdmittedSource, Diagnostic, Request, Response, SourceFamily } from '@jai/fabric-explorer-contracts';
import type { BrokerPort, SourceSelection } from '../broker/types.js';
import type { PreferenceStore, Preferences } from './preferences.js';
import type { ImportSessionPort } from '../import/session.js';
import { queryPage, QueryTransfer, projectionFilterView } from '../explore/transport.js';
import type { GraphRequest } from '../graph/types.js';
import type { QueryPage, QueryContinuation, QueryDrop, LayoutSelection, GroupSelection, ProjectionFilterSelection, ProjectionFilterView } from '../explore/types.js';
import { ImportError } from '../import/types.js';
import type { ImportState } from '../import/types.js';

/**
 * Main-only composition of an import lifetime.
 * @param input Admitted session/capability/catalog, never renderer-native paths.
 * @returns Owned import service without eagerly reading source data.
 * @throws {Error} When trusted composition is unavailable.
 */
export interface ImportSessionFactory { (input: { readonly sessionId: string; readonly capability: string; readonly sources: readonly AdmittedSource[] }): ImportSessionPort }

/** Trusted native dialogs; returned paths never cross the renderer boundary. */
export interface PickerPort {
  /** Choose an association anchor; cancellation returns null. */
  project(): Promise<string | null>;
  /**
   * Discover project sources or choose explicit files in a project-relative native dialog.
   * @param family Requested source family.
   * @param projectPath Explicitly selected association directory; paths stay main-only.
   * @param maximumFiles Remaining capacity from the existing 128-source admission bound.
   * @param signal Existing selection lifetime; no late fallback dialog opens after cancellation.
   * @returns Complete candidate list, explicit manual selection, or null for cancellation.
   * @throws {Error} Native selection failures propagate to the shell error response.
   */
  files(family: SourceFamily, projectPath: string, maximumFiles: number, signal: AbortSignal): Promise<readonly string[] | null>;
}
/** Small application-only state; no imported graph or source pathname is included. */
export interface ShellState extends ImportState { readonly sessionId: string; readonly capability: string | null; readonly sources: readonly AdmittedSource[]; readonly preferences: Preferences; readonly warning: string | null }
/** Serial root lifecycle with cancellable native selection and late-reply suppression. */
export class ShellController {
  readonly sessionId = randomUUID();
  private capability: string | null = null;
  private sources: readonly AdmittedSource[] = [];
  private alive = true;
  private selectionRequestId: string | null = null;
  private epoch = 0;
  private readonly active = new Map<string, AbortController>();
  private readonly queries = new Map<string, { request: GraphRequest; transfer: QueryTransfer; page: QueryPage }>();
  private preferences: Preferences;
  private readonly warning: string | null;
  private importer: ImportSessionPort | null = null;
  /**
   * Bind trusted dependencies for one renderer lifetime.
   * @param broker Main-owned native read capability owner.
   * @param picker Native source selection adapter.
   * @param store Fixed presentation preference store.
   * @param createImport Optional app-owned import factory invoked after admission.
   * @throws {Error} If trusted preference initialization fails.
   */
  constructor(private readonly broker: BrokerPort, private readonly picker: PickerPort, private readonly store: PreferenceStore, private readonly createImport?: ImportSessionFactory) {
    const loaded = store.load(); this.preferences = loaded.preferences; this.warning = loaded.warning;
  }
  /** Obtain detached app state after sender authentication by the transport. */
  state(): ShellState { if (!this.alive) throw new Error('Session unavailable'); return { sessionId: this.sessionId, capability: this.capability, sources: this.sources.map(source => ({ ...source })), preferences: { ...this.preferences }, warning: this.warning, ...structuredClone(this.importer?.state() ?? { snapshot: null, report: null, stale: false }) }; }
  /** Validate and save presentation preferences after sender authentication. */
  savePreferences(value: unknown): Preferences { if (!this.alive) throw new Error('Session unavailable'); this.preferences = this.store.save(value); return { ...this.preferences }; }
  /** Cancel only a pending native selection in this authenticated shell session. */
  cancelSelection(requestId: unknown): boolean {
    if (!this.alive || typeof requestId !== 'string' || !/^[A-Za-z0-9._:-]{1,128}$/.test(requestId)) throw new Error('Invalid selection identifier');
    const work = this.selectionRequestId === requestId ? this.active.get(requestId) : undefined; work?.abort(); return !!work;
  }
  /** Revoke requests and handles when the renderer lifetime ends. */
  async dispose(): Promise<void> { if (!this.alive) return; this.alive = false; this.epoch++; for (const work of this.active.values()) work.abort(); this.active.clear(); this.queries.clear(); this.capability = null; this.sources = []; const importer = this.importer; this.importer = null; try { await importer?.dispose(); } finally { await this.broker.disposeSession(this.sessionId); } }
  private explorationContext(binding: Request['binding']): void {
    if (!this.alive || !this.importer?.state().snapshot) throw new Error('Snapshot unavailable');
    assertBinding(binding, { sessionId: this.sessionId, capability: this.capability, generation: this.importer.state().snapshot!.generation });
  }
  /**
   * Start one authenticated bounded graph query; its active cancellation entry survives chunk pulls.
   * @param frame Original bounded S04 graph request frame from the current renderer.
   * @returns One validated private page, never a whole snapshot clone.
   * @throws {Error} For stale context, duplicate request IDs, limits or malformed worker replies.
   */
  async queryStart(frame: unknown, mode: 'all' | 'findings' = 'all'): Promise<QueryPage> {
    if (typeof frame !== 'string') throw new Error('Invalid graph request');
    const request = decodeRequestFrame(frame);
    if (!['element.lookup', 'element.details', 'search.page', 'graph.counts', 'graph.neighbours', 'graph.path'].includes(request.operation)) throw new Error('Invalid graph operation');
    if (mode === 'findings' && request.operation !== 'search.page') throw new Error('Invalid findings operation');
    this.explorationContext(request.binding);
    if (this.active.has(request.requestId) || this.active.size >= 16 || !this.importer?.queryStart) throw new Error('Query unavailable');
    const abort = new AbortController(); this.active.set(request.requestId, abort);
    let page: QueryPage | null = null;
    try {
      const run = mode === 'findings' ? this.importer.searchFindings : this.importer.queryStart;
      if (!run) throw new Error('Findings search unavailable');
      page = queryPage(await run.call(this.importer, request as Extract<GraphRequest, { operation: 'search.page' }>, abort.signal)); this.explorationContext(request.binding);
      if (abort.signal.aborted) throw new Error('Query cancelled');
      const transfer = new QueryTransfer(request, false); transfer.accept(page, request.binding);
      if (page.continuationToken !== null) this.queries.set(request.requestId, { request: request as GraphRequest, transfer, page });
      else this.active.delete(request.requestId);
      return page;
    } catch (error) {
      this.active.delete(request.requestId);
      if (page) await this.importer?.queryDrop?.({ binding: request.binding, requestId: request.requestId, continuationToken: page.continuationToken, projectionToken: page.projectionToken }).catch(() => {});
      throw error;
    }
  }
  /**
   * Pull only the next owned token from the retained original query.
   * @param input Bound request ID and current opaque continuation.
   * @returns One correlated finite-progress page.
   * @throws {Error} For stale/replayed tokens, cancellation or inconsistent chunks.
   */
  async queryNext(input: QueryContinuation): Promise<QueryPage> {
    encodeWire(input); this.explorationContext(input.binding);
    const job = this.queries.get(input.requestId); const abort = this.active.get(input.requestId);
    if (!job || !abort || abort.signal.aborted || job.page.continuationToken !== input.continuationToken || !this.importer?.queryNext) throw new Error('Query continuation unavailable');
    // Consume the continuation before yielding; concurrent replay cannot race the worker.
    this.queries.delete(input.requestId);
    let page = job.page;
    try {
      page = queryPage(await this.importer.queryNext(input, abort.signal)); this.explorationContext(input.binding);
      if (abort.signal.aborted) throw new Error('Query cancelled');
      job.transfer.accept(page, input.binding);
      if (page.continuationToken !== null) this.queries.set(input.requestId, { ...job, page }); else this.active.delete(input.requestId);
      return page;
    } catch (error) { this.active.delete(input.requestId); await this.importer?.queryDrop?.({ binding: input.binding, requestId: input.requestId, continuationToken: page.continuationToken, projectionToken: page.projectionToken }).catch(() => {}); throw error; }
  }
  /**
   * Release owned ephemeral jobs/projections without changing source data.
   * @param input Current binding, owner request and tokens to release.
   * @returns Nothing after worker release.
   * @throws {Error} For stale/cross-request selections.
   */
  async queryDrop(input: QueryDrop): Promise<void> {
    encodeWire(input); this.explorationContext(input.binding);
    if (!this.importer?.queryDrop) throw new Error('Exploration unavailable');
    await this.importer.queryDrop(input); this.active.get(input.requestId)?.abort(); this.active.delete(input.requestId); this.queries.delete(input.requestId);
  }
  private async derived<T>(input: LayoutSelection | GroupSelection | ProjectionFilterSelection, run: (signal: AbortSignal) => Promise<T>): Promise<T> {
    encodeWire(input); this.explorationContext(input.binding);
    if (!/^[A-Za-z0-9._:-]{1,128}$/.test(input.requestId) || this.active.has(input.requestId) || this.active.size >= 16) throw new Error('Derived request limit');
    const abort = new AbortController(); this.active.set(input.requestId, abort);
    try { const result = await run(abort.signal); this.explorationContext(input.binding); if (abort.signal.aborted) throw new Error('Derived request cancelled'); encodeWire(result); return result; }
    finally { this.active.delete(input.requestId); }
  }
  /** Start only finding search through the same retained S04 query transfer. */
  async searchFindings(frame: unknown): Promise<QueryPage> { return this.queryStart(frame, 'findings'); }
  /** Filter a current bounded projection and revoke output if cancellation wins delivery. */
  async filterProjection(input: ProjectionFilterSelection): Promise<ProjectionFilterView> {
    const output: { result: ProjectionFilterView | null } = { result: null };
    const importer = this.importer;
    try { return await this.derived(input, async signal => { if (!importer?.filterProjection) throw new Error('Projection filtering unavailable'); output.result = projectionFilterView(await importer.filterProjection(input, signal), input); return output.result; }); }
    catch (error) { if (output.result) await importer?.queryDrop?.({ binding: input.binding, requestId: input.requestId, continuationToken: null, projectionToken: output.result.projectionToken }).catch(() => {}); throw error; }
  }
  /** Layout an owned current-generation projection after native sender authentication. */
  async layout(input: LayoutSelection) { return this.derived(input, signal => { if (!this.importer?.layout) throw new Error('Layout unavailable'); return this.importer.layout(input, signal); }); }
  /** Group accepted records after native sender authentication; no new public operation is created. */
  async groups(input: GroupSelection) { return this.derived(input, signal => { if (!this.importer?.groups) throw new Error('Grouping unavailable'); return this.importer.groups(input, signal); }); }
  /** Decode one bounded authenticated frame and return a validated bounded response. */
  async request(frame: unknown): Promise<string> {
    if (!this.alive || typeof frame !== 'string') throw new Error('Request rejected');
    const request = decodeRequestFrame(frame);
    const generation = request.operation === 'roots.pick' ? null : this.importer?.state().snapshot?.generation ?? null;
    if (request.binding.sessionId !== this.sessionId || request.binding.generation !== generation || request.binding.capability !== (request.operation === 'roots.pick' ? null : this.capability)) throw new Error('Request context rejected');
    if (this.active.has(request.requestId) || this.active.size >= 16) throw new Error('Request limit');
    const abort = new AbortController(); this.active.set(request.requestId, abort);
    const epoch = this.epoch;
    const valid = () => this.alive && !abort.signal.aborted && this.epoch === epoch;
    const base = { protocol: PROTOCOL, kind: 'response' as const, requestId: request.requestId, binding: request.binding, operation: request.operation };
    const failure = (code: Diagnostic['code'], message: string) => encodeFrame({ ...base, status: 'error', error: { code, message, source: null, severity: 'error' } } as Response);
    try {
      if (request.operation === 'request.cancel') {
        const target = this.active.get(request.payload.targetRequestId); if (target !== abort) target?.abort();
        const query = this.queries.get(request.payload.targetRequestId);
        if (query) { this.queries.delete(request.payload.targetRequestId); this.active.delete(request.payload.targetRequestId); await this.importer?.queryDrop?.({ binding: query.request.binding, requestId: query.request.requestId, continuationToken: query.page.continuationToken, projectionToken: query.page.projectionToken }); }
        return encodeFrame({ ...base, operation: 'request.cancel', status: 'ok', payload: { targetRequestId: request.payload.targetRequestId, acknowledgement: target && target !== abort ? 'accepted' : 'not-active' } });
      }
      if (request.operation === 'roots.close') {
        this.epoch++; this.queries.clear(); for (const [id, work] of this.active) if (id !== request.requestId) work.abort();
        const capability = this.capability; const importer = this.importer; this.importer = null; this.capability = null; this.sources = [];
        try { await importer?.dispose(); } finally { if (capability) await this.broker.close(this.sessionId, capability); }
        return encodeFrame({ ...base, operation: 'roots.close', status: 'ok', payload: { closed: true } });
      }
      if (request.operation === 'snapshot.import' || request.operation === 'snapshot.refresh') {
        if (!this.importer) return failure('unknown-operation', 'Source interpretation is unavailable in this build.');
        const snapshot = request.operation === 'snapshot.import'
          ? await this.importer.import(request.payload.sourceIds, request.binding.generation, abort.signal)
          : await this.importer.refresh(request.binding.generation!, abort.signal);
        if (!valid()) return failure('cancelled', 'Import result discarded after cancellation or source closure.');
        return encodeFrame({ ...base, operation: request.operation, status: 'ok', payload: { snapshot } } as Response);
      }
      if (request.operation === 'source.page') {
        if (!this.importer) return failure('unknown-operation', 'Source interpretation is unavailable in this build.');
        const page = await this.importer.sourcePage(request.payload, request.binding.generation!, abort.signal);
        if (!valid()) return failure('cancelled', 'Source page discarded after cancellation or source closure.');
        return encodeFrame({ ...base, operation: 'source.page', status: 'ok', payload: page });
      }
      if (request.operation !== 'roots.pick') return failure('unknown-operation', 'Graph queries are unavailable in this build.');
      if (this.capability || [...this.active.keys()].some(id => id !== request.requestId)) return failure('read-failed', 'Close the current selection before opening another.');
      this.selectionRequestId = request.requestId;
      const projectPath = await this.picker.project();
      if (!projectPath || !valid()) return failure('cancelled', 'Selection cancelled.');
      const selections: SourceSelection[] = [];
      for (const family of request.payload.families) {
        const paths = await this.picker.files(family, projectPath, 128 - selections.length, abort.signal);
        if (!paths || !valid()) return failure('cancelled', 'Selection cancelled.');
        if (paths.length > 128 || selections.length + paths.length > 128) return failure('read-failed', 'Too many selected files.');
        for (const path of paths) selections.push({ projectPath, path, family });
      }
      if (!selections.length) return failure('cancelled', 'Selection cancelled.');
      const opened = await this.broker.open(this.sessionId, selections, abort.signal);
      if (!valid()) { await this.broker.close(this.sessionId, opened.capability); return failure('cancelled', 'Selection cancelled.'); }
      let response: string; let importer: ImportSessionPort | null = null;
      try { importer = this.createImport?.({ sessionId: this.sessionId, capability: opened.capability, sources: opened.sources }) ?? null; response = encodeFrame({ ...base, operation: 'roots.pick', status: 'ok', payload: opened }); }
      catch { try { await importer?.dispose(); } finally { await this.broker.close(this.sessionId, opened.capability); } throw new Error('Invalid broker response'); }
      this.capability = opened.capability; this.sources = opened.sources; this.importer = importer;
      return response;
    } catch (error) { return failure(abort.signal.aborted ? 'cancelled' : error instanceof ImportError ? error.code : 'read-failed', abort.signal.aborted ? 'Request cancelled.' : 'The operation could not be completed.'); }
    finally { if (this.selectionRequestId === request.requestId) this.selectionRequestId = null; this.active.delete(request.requestId); }
  }
}
