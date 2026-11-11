// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Framework-independent observable presentation state; canonical semantics remain worker-owned. */
import { LIMITS, RELATION_DIRECTIONS, decodeBytePage } from '@jai/fabric-explorer-contracts';
import type { Binding, Edge, ElementIdentity, Filter, GraphProjection, RequestPayloads, ResponsePayloads, Vertex } from '@jai/fabric-explorer-contracts';
import type { QueryView } from '../../explore/types.js';
import type { GroupAxis } from '../../graph/types.js';
import type { DesktopBridge } from '../../shell/bridge.js';
import type { ShellState } from '../../shell/controller.js';
import type { ExploreLane, ExplorePage, ExploreState, NeighbourOptions, PathOptions } from './types.js';

const empty: Filter = { projectIds: [], families: [], findingStates: [], relations: [] };
const limits = { maxVertices: LIMITS.defaultVertices, maxEdges: LIMITS.defaultEdges, maxVisitedVertices: LIMITS.visitedVertices, maxScannedEdges: LIMITS.scannedEdges, maxHops: LIMITS.hops };
const relations = Object.keys(RELATION_DIRECTIONS) as RequestPayloads['graph.neighbours']['relations'];
type Job = { lane: ExploreLane; epoch: number; navigation: number | null; binding: Binding; cancelled: boolean; ids: Set<string>; tokens: Set<string> };
type Token = { binding: Binding; requestId: string; token: string };
type GraphIntent = { kind: 'neighbours'; options: NeighbourOptions } | { kind: 'path'; from: ElementIdentity; to: ElementIdentity; options: PathOptions };
type SelectionIntent = { kind: 'select'; identity: ElementIdentity } | { kind: 'edge'; id: string; context: GraphIntent };
type Intent = { graph: GraphIntent | null; selection: SelectionIntent | null; filter: Filter; search: { text: string; order: 'identity' | 'label' }; findings: string; groupAxis: GroupAxis };
type Base = { projection: GraphProjection; handles: readonly number[]; token: Token; intent: GraphIntent; published: boolean };
class Superseded extends Error {}
function payload<K extends QueryView['response']['operation']>(view: QueryView, operation: K): ResponsePayloads[K] {
  const response = view.response;
  if (response.operation !== operation || response.status !== 'ok') throw new Error('Presentation query failed.');
  return response.payload as ResponsePayloads[K];
}
function mask(value: string, length: number): readonly boolean[] {
  const decoded = atob(value);
  if (decoded.length !== Math.ceil(length / 8) || btoa(decoded) !== value || length % 8 && decoded.length && decoded.charCodeAt(decoded.length - 1) >> (length % 8)) throw new Error('Invalid projection membership.');
  return Array.from({ length }, (_, position) => !!(decoded.charCodeAt(position >> 3) & (1 << (position & 7))));
}

/** Observable immutable UI state with generation-bound request and projection ownership. */
export class ExploreController {
  private value: ExploreState = { shell: null, binding: null, busy: [], error: null, message: null, filter: empty, search: null, findings: null, counts: null, groups: null, groupAxis: 'kind', projection: null, handles: [], layout: null, selection: null, sourcePage: null, history: { canBack: false, canForward: false } };
  private readonly listeners = new Set<() => void>();
  private readonly frozen = new WeakSet<object>();
  private readonly jobs = new Map<ExploreLane, Job>();
  private readonly tokens = new Map<string, Token>();
  private base: Base | null = null;
  private committedBase: Base | null = null;
  private display: Token | null = null;
  private epoch = 0;
  private counter = 0;
  private closed = false;
  private history: Intent[] = [];
  private position = -1;
  private graphIntent: GraphIntent | null = null;
  private selectionIntent: SelectionIntent | null = null;
  private navigationVersion = 0;
  private replayVersion: number | null = null;

  /**
   * Bind a trusted named desktop bridge without introducing DOM or framework dependencies.
   * @param bridge Existing read-only application methods.
   */
  constructor(private readonly bridge: DesktopBridge) { this.freeze(this.value); }
  /** Return the same immutable snapshot until a state transition is published. */
  getSnapshot = (): ExploreState => this.value;
  /**
   * Subscribe to publications without polling or retaining prior DTOs.
   * @param listener Callback invoked after the next immutable state is installed.
   * @returns Idempotent unsubscribe function.
   */
  subscribe = (listener: () => void): (() => void) => { if (this.closed) return () => undefined; this.listeners.add(listener); return () => { this.listeners.delete(listener); }; };
  private freeze<T>(value: T): T {
    if (value && typeof value === 'object' && !this.frozen.has(value)) { this.frozen.add(value); for (const item of Object.values(value)) this.freeze(item); Object.freeze(value); }
    return value;
  }
  private publish(update: Partial<ExploreState>): void { if (this.closed) return; this.value = this.freeze({ ...this.value, ...update }); for (const listener of this.listeners) listener(); }
  private id(): string { return `presentation-${++this.counter}`; }
  private valid(job: Job): boolean { return !this.closed && !job.cancelled && this.epoch === job.epoch && this.jobs.get(job.lane) === job && (job.navigation === null || job.navigation === this.navigationVersion); }
  private beginAction(): void {
    this.navigationVersion++; this.replayVersion = null;
    for (const job of this.jobs.values()) if (job.navigation !== null) { this.jobs.delete(job.lane); void this.abort(job); }
  }
  private guard(job: Job): void { if (!this.valid(job)) throw new Superseded(); }
  private busy(): void { this.publish({ busy: [...this.jobs.keys()] }); }
  private currentBinding(binding: Binding): boolean { const current = this.value.binding; return !!current && binding.sessionId === current.sessionId && binding.capability === current.capability && binding.generation === current.generation; }
  private async abort(job: Job): Promise<void> { job.cancelled = true; if (!this.currentBinding(job.binding)) return; await Promise.all([...job.ids].map(id => this.bridge.cancelRequest(job.binding, this.id(), id).catch(() => undefined))); }
  private async release(token: Token | null): Promise<void> { if (!token || !this.tokens.delete(token.token) || !this.currentBinding(token.binding)) return; await this.bridge.dropQuery({ binding: token.binding, requestId: token.requestId, continuationToken: null, projectionToken: token.token }).catch(() => undefined); }
  private async call<T>(job: Job, invoke: (id: string) => Promise<T>): Promise<T> {
    this.guard(job); const requestId = this.id(); job.ids.add(requestId);
    try {
      const result = await invoke(requestId);
      if (result && typeof result === 'object' && 'projectionToken' in result && typeof result.projectionToken === 'string') {
        const token = { binding: job.binding, requestId, token: result.projectionToken }; this.tokens.set(token.token, token); job.tokens.add(token.token);
        if (!this.valid(job)) await this.release(token);
      }
      this.guard(job); return result;
    } finally { job.ids.delete(requestId); }
  }
  private async run(lane: ExploreLane, action: (job: Job) => Promise<void>): Promise<void> {
    if (this.closed || !this.value.binding?.generation || !this.value.binding.capability) return;
    const prior = this.jobs.get(lane); if (prior) void this.abort(prior);
    const job: Job = { lane, epoch: this.epoch, navigation: this.replayVersion, binding: this.value.binding, cancelled: false, ids: new Set(), tokens: new Set() }; this.jobs.set(lane, job); this.publish({ error: null }); this.busy();
    try { await action(job); }
    catch (error) { if (this.valid(job) && !(error instanceof Superseded)) this.publish({ error: 'The requested view could not be loaded. The previous view remains available.' }); }
    finally { await Promise.all([...job.tokens].filter(token => token !== this.base?.token.token && token !== this.committedBase?.token.token && token !== this.display?.token).map(token => this.release(this.tokens.get(token) ?? null))); if (this.jobs.get(lane) === job) { this.jobs.delete(lane); this.busy(); } }
  }
  private remember(): void {
    const intent: Intent = { graph: this.graphIntent, selection: this.selectionIntent, filter: this.value.filter, search: { text: this.value.search?.text ?? '', order: this.value.search?.order ?? 'identity' }, findings: this.value.findings?.text ?? '', groupAxis: this.value.groupAxis };
    this.history = this.history.slice(0, this.position + 1); this.history.push(structuredClone(intent)); if (this.history.length > 50) this.history.shift(); this.position = this.history.length - 1; this.historyState();
  }
  private historyState(): void { this.publish({ history: { canBack: this.position > 0, canForward: this.position >= 0 && this.position + 1 < this.history.length } }); }

  /**
   * Observe shell state; a new accepted generation initializes one overview automatically.
   * @param shell Current main-owned state, including failed-refresh diagnostics.
   * @returns Completion of any automatic overview; unchanged generations retain their view.
   */
  async setShell(shell: ShellState): Promise<void> {
    if (this.closed) return;
    const binding: Binding = { sessionId: shell.sessionId, capability: shell.capability, generation: shell.snapshot?.generation ?? null };
    const changed = JSON.stringify(binding) !== JSON.stringify(this.value.binding);
    if (!changed) { this.publish({ shell: structuredClone(shell) }); return; }
    this.epoch++; this.navigationVersion++; this.replayVersion = null; const jobs = [...this.jobs.values()]; this.jobs.clear();
    const tokens = [...this.tokens.values()]; this.base = null; this.committedBase = null; this.graphIntent = null; this.selectionIntent = null; this.display = null; this.history = []; this.position = -1;
    this.publish({ shell: structuredClone(shell), binding, busy: [], error: null, message: null, search: null, findings: null, counts: null, groups: null, projection: null, handles: [], layout: null, selection: null, sourcePage: null, history: { canBack: false, canForward: false } });
    // Main has already retired the previous worker before publishing this binding.
    // Forget its local ownership without sending obsolete cancellation/drop IPC.
    for (const job of jobs) void this.abort(job);
    await Promise.all(tokens.map(token => this.release(token))); if (binding.generation) await this.loadOverview();
  }
  /** Load bounded search/finding pages, global facets/counts and a small initial neighbourhood. */
  async loadOverview(): Promise<void> {
    await this.run('overview', async job => {
      const filter = this.value.filter;
      const [search, findings, counts, groups] = await Promise.all([
        this.call(job, id => this.bridge.search(job.binding, id, { text: '', filter, order: 'identity', limit: 50, cursor: null })),
        this.call(job, id => this.bridge.searchFindings(job.binding, id, { text: '', filter, order: 'identity', limit: 50, cursor: null })),
        this.call(job, id => this.bridge.counts(job.binding, id, { filter })),
        this.call(job, id => this.bridge.groups(job.binding, id, filter, this.value.groupAxis)),
      ]);
      this.guard(job); const found = payload(search, 'search.page');
      this.publish({ search: { ...found, text: '', order: 'identity' }, findings: { ...payload(findings, 'search.page'), text: '', order: 'identity' }, counts: payload(counts, 'graph.counts'), groups });
      if (found.items[0]) await this.showNeighbours({ identity: found.items[0].identity, limits: { ...limits, maxVertices: 100, maxEdges: 300, maxHops: 1 } }, false);
      this.guard(job); this.remember();
    });
  }
  private async searchPage(lane: 'search' | 'findings', text: string, order: 'identity' | 'label', append: boolean, recordHistory = true): Promise<void> {
    await this.run(lane, async job => {
      const previous = this.value[lane]; const continuing = append && previous?.text === text && previous.order === order;
      if (continuing && !previous.nextCursor) return;
      const input = { text, filter: this.value.filter, order, limit: 50, cursor: continuing ? previous.nextCursor : null };
      const result = await this.call(job, id => lane === 'findings' ? this.bridge.searchFindings(job.binding, id, input) : this.bridge.search(job.binding, id, input));
      const page = payload(result, 'search.page');
      // Pagination advances the displayed page rather than retaining an unbounded list of DTOs.
      this.publish({ [lane]: { ...page, text, order } as ExplorePage });
      if (recordHistory && !append) this.remember();
    });
  }
  /**
   * Search a finite literal/identity page with the worker's exact indexed filter.
   * @param text Literal query text.
   * @param order Deterministic identity or label order.
   * @param append Follow only the current matching page cursor.
   */
  async search(text: string, order: 'identity' | 'label' = 'identity', append = false): Promise<void> { this.beginAction(); await this.searchPage('search', text, order, append); }
  /**
   * Search only findings, preserving explicit remaining counts and separate cursor authentication.
   * @param text Literal query text.
   * @param append Follow the current finding cursor.
   */
  async findings(text: string, append = false): Promise<void> { this.beginAction(); await this.searchPage('findings', text, 'identity', append); }
  /**
   * Resolve an exact canonical identity and load its immutable inspector record.
   * @param identity Full version/use-point identity, never a label guess.
   */
  async select(identity: ElementIdentity): Promise<void> {
    this.beginAction(); await this.selectIdentity(identity, true);
  }
  private async selectIdentity(identity: ElementIdentity, recordHistory: boolean): Promise<void> {
    await this.run('selection', async job => {
      const found = payload(await this.call(job, id => this.bridge.lookup(job.binding, id, { identity })), 'element.lookup').vertex;
      if (!found) { this.publish({ message: 'The exact element is absent from this captured snapshot.' }); return; }
      await this.inspect(job, found); this.guard(job); this.selectionIntent = { kind: 'select', identity }; if (recordHistory) this.remember();
    });
  }
  /**
   * Select an exact node or parallel relation already present in the displayed projection.
   * @param id Canonical element or edge key supplied by the canvas/list.
   */
  async selectElement(id: string): Promise<void> {
    this.beginAction(); await this.selectKey(id, true);
  }
  private async selectKey(id: string, recordHistory: boolean): Promise<void> {
    const projection = this.value.projection; const record = projection?.vertices.find(item => item.id === id) ?? projection?.edges.find(item => item.id === id);
    if (!record) { this.publish({ message: 'The selected element is outside this displayed projection.' }); return; }
    if ('kind' in record) { await this.selectIdentity(record.identity, recordHistory); return; }
    const context = this.graphIntent; if (!context) return;
    await this.run('selection', async job => { await this.inspect(job, record); this.guard(job); this.selectionIntent = { kind: 'edge', id, context }; if (recordHistory) this.remember(); });
  }
  private async restoreSelection(selection: SelectionIntent): Promise<void> {
    if (selection.kind === 'select') { await this.selectIdentity(selection.identity, false); return; }
    if (this.value.projection?.edges.some(edge => edge.id === selection.id)) { await this.selectKey(selection.id, false); return; }
    // An inspector may legitimately refer to a relation outside the current graph.
    // Re-execute its original bounded query without publishing or laying out that temporary graph.
    await this.run('selection', async job => {
      const context = selection.context;
      const view = context.kind === 'neighbours'
        ? await this.call(job, id => this.bridge.neighbours(job.binding, id, { direction: 'both', relations, causalOnly: false, limits, ...context.options, identity: context.options.identity! }))
        : await this.call(job, id => this.bridge.path(job.binding, id, { from: context.from, to: context.to, direction: 'forward', relations, causalOnly: false, limits, ...context.options }));
      const graph = context.kind === 'neighbours' ? payload(view, 'graph.neighbours').projection : payload(view, 'graph.path').projection;
      const edge = graph.edges.find(edge => edge.id === selection.id); if (!edge) throw new Error('Historical relation is unavailable.');
      await this.inspect(job, edge); this.guard(job); this.selectionIntent = selection;
    });
  }
  private async inspect(job: Job, record: Vertex | Edge): Promise<void> {
    const endpoints: Vertex[] = []; const subjects: Vertex[] = []; let subjectComplete = true;
    if (!('kind' in record)) {
      for (const identity of [record.identity.from, record.identity.to]) { const endpoint = payload(await this.call(job, id => this.bridge.lookup(job.binding, id, { identity })), 'element.lookup').vertex; if (endpoint) endpoints.push(endpoint); }
    } else if (record.kind === 'finding') {
      const result = await this.call(job, id => this.bridge.neighbours(job.binding, id, { identity: record.identity, direction: 'forward', relations: ['finding-subject', 'location-association'], causalOnly: false, limits: { ...limits, maxHops: 1 } }));
      const graph = payload(result, 'graph.neighbours').projection; subjectComplete = graph.complete;
      const ids = new Set(graph.edges.filter(edge => edge.from === record.id && (edge.relation === 'finding-subject' || edge.relation === 'location-association')).map(edge => edge.to));
      subjects.push(...graph.vertices.filter(vertex => ids.has(vertex.id)));
      if (result.projectionToken) await this.release(this.tokens.get(result.projectionToken) ?? null);
    }
    this.guard(job); const sourceJob = this.jobs.get('source'); if (sourceJob) { this.jobs.delete('source'); void this.abort(sourceJob); this.busy(); }
    this.publish({ selection: { element: record, attributes: record.attributes, endpoints, subjectCandidates: subjects, subjectComplete }, sourcePage: null, message: 'kind' in record && record.kind === 'finding' && subjects.length !== 1 ? 'The finding has no single unambiguous displayed subject. Inspect the explicit candidates.' : null });
  }
  /**
   * Replace the bounded graph with a directed neighbourhood of the selected or explicit identity.
   * @param options Finite traversal controls; directions retain canonical meaning.
   */
  async neighbours(options: NeighbourOptions = {}): Promise<void> {
    this.beginAction(); await this.showNeighbours(options, true);
  }
  private async showNeighbours(options: NeighbourOptions, recordHistory: boolean): Promise<void> {
    const selected = this.value.selection?.element; const identity = options.identity ?? (selected && 'kind' in selected ? selected.identity : undefined);
    if (!identity) return;
    await this.run('graph', async job => { const result = await this.call(job, id => this.bridge.neighbours(job.binding, id, { identity, direction: 'both', relations, causalOnly: false, limits, ...options })); await this.install(job, result, payload(result, 'graph.neighbours').projection, { kind: 'neighbours', options: { ...options, identity } }); this.guard(job); if (recordHistory) this.remember(); });
  }
  /**
   * Display one bounded directed path; an inconclusive work limit is never reported as absence.
   * @param from Exact start identity.
   * @param to Exact destination identity.
   * @param options Finite path controls.
   */
  async path(from: ElementIdentity, to: ElementIdentity, options: PathOptions = {}): Promise<void> {
    this.beginAction(); await this.showPath(from, to, options, true);
  }
  private async showPath(from: ElementIdentity, to: ElementIdentity, options: PathOptions, recordHistory: boolean): Promise<void> {
    await this.run('graph', async job => { const result = await this.call(job, id => this.bridge.path(job.binding, id, { from, to, direction: 'forward', relations, causalOnly: false, limits, ...options })); const found = payload(result, 'graph.path'); await this.install(job, result, found.projection, { kind: 'path', from, to, options }); this.guard(job); this.publish({ message: found.found === null ? 'Path search is inconclusive within the reported bounds.' : found.found ? 'A path was found in this captured graph.' : 'No path exists within the selected indexed relation scope.' }); if (recordHistory) this.remember(); });
  }
  private async install(job: Job, result: QueryView, projection: GraphProjection, intent: GraphIntent): Promise<void> {
    if (!result.projectionToken || !result.handles) throw new Error('Missing projection ownership.');
    const token = this.tokens.get(result.projectionToken)!; const old = this.committedBase; const oldDisplay = this.display;
    const candidate: Base = { projection, handles: result.handles, token, intent, published: false }; this.base = candidate;
    try { await this.applyFilter(job); }
    catch (error) { if (this.base === candidate && !candidate.published) this.base = this.committedBase; throw error; }
    finally { if (candidate.published) await Promise.all([this.release(old?.token ?? null), this.release(oldDisplay)]); }
  }
  private async applyFilter(job: Job): Promise<void> {
    const base = this.base; if (!base) return;
    const filter = this.value.filter; const result = await this.call(job, id => this.bridge.filterProjection(job.binding, id, base.token.token, filter));
    const verticesMask = mask(result.vertexMask, base.projection.vertices.length); const edgesMask = mask(result.edgeMask, base.projection.edges.length);
    const vertices = base.projection.vertices.filter((_, index) => verticesMask[index]); const edges = base.projection.edges.filter((_, index) => edgesMask[index]);
    const ids = new Set(vertices.map(vertex => vertex.id));
    const handles = base.handles.filter((_, index) => verticesMask[index]);
    const removed = vertices.length !== base.projection.vertices.length || edges.length !== base.projection.edges.length;
    const omissions = [...new Set([...base.projection.omissions, ...(removed ? ['filter' as const] : [])])];
    if (edges.some(edge => !ids.has(edge.from) || !ids.has(edge.to)) || JSON.stringify(handles) !== JSON.stringify(result.handles)
      || result.complete !== base.projection.complete || result.hiddenVertices !== String(BigInt(base.projection.snapshot.counts.vertices) - BigInt(vertices.length)) || result.hiddenEdges !== String(BigInt(base.projection.snapshot.counts.edges) - BigInt(edges.length))
      || omissions.length !== result.omissions.length || omissions.some(reason => !result.omissions.includes(reason))) throw new Error('Invalid filtered projection closure.');
    this.guard(job); if (this.base !== base || this.value.filter !== filter) throw new Superseded(); const old = this.display; this.display = this.tokens.get(result.projectionToken)!;
    base.published = true; this.committedBase = base; this.graphIntent = base.intent;
    this.publish({ projection: { ...base.projection, vertices, edges, hiddenVertices: result.hiddenVertices, hiddenEdges: result.hiddenEdges, complete: result.complete, omissions: result.omissions }, handles, layout: null });
    await this.release(old);
    try { const layout = await this.call(job, id => this.bridge.layout(job.binding, id, result.projectionToken, {})); if (this.display?.token !== result.projectionToken) throw new Superseded(); this.publish({ layout }); }
    catch (error) { if (error instanceof Superseded) throw error; this.guard(job); this.publish({ message: 'The graph is available, but its layout could not be computed.' }); }
  }
  /**
   * Apply exact worker membership to the original retained graph, making filters reversible.
   * @param filter Shared S04 conditional filter; empty selectors admit all applicable records.
   */
  async setFilter(filter: Filter): Promise<void> {
    this.beginAction(); await this.changeFilter(filter, true);
  }
  private async changeFilter(filter: Filter, recordHistory: boolean): Promise<void> {
    const previous = this.value; const next = structuredClone(filter); let applied = false;
    for (const lane of ['search', 'findings', 'groups', 'overview'] as const) { const job = this.jobs.get(lane); if (job) { this.jobs.delete(lane); void this.abort(job); } }
    this.publish({ filter: next, search: null, findings: null });
    await this.run('filter', async job => { await this.applyFilter(job); applied = true; });
    if (!applied) { if (this.value.filter === next) this.publish({ filter: previous.filter, search: previous.search, findings: previous.findings }); return; }
    await Promise.all([this.searchPage('search', previous.search?.text ?? '', previous.search?.order ?? 'identity', false, false), this.searchPage('findings', previous.findings?.text ?? '', 'identity', false, false), this.loadGroups(this.value.groupAxis), this.loadCounts()]);
    if (recordHistory && this.value.filter === next) this.remember();
  }
  /**
   * Load deterministic full-index facets without merging graph elements.
   * @param axis Maintained grouping dimension.
   */
  async setGroupAxis(axis: GroupAxis): Promise<void> { this.beginAction(); await this.loadGroups(axis); this.remember(); }
  private async loadGroups(axis: GroupAxis): Promise<void> { this.publish({ groupAxis: axis }); await this.run('groups', async job => { const groups = await this.call(job, id => this.bridge.groups(job.binding, id, this.value.filter, axis)); this.publish({ groups }); }); }
  private async loadCounts(): Promise<void> { await this.run('overview', async job => { const result = await this.call(job, id => this.bridge.counts(job.binding, id, { filter: this.value.filter })); this.publish({ counts: payload(result, 'graph.counts') }); }); }
  /**
   * Read exact archived source bytes for the selected record or its explicit paged attributes.
   * @param offset Decimal byte offset, independent of UTF-8 character count.
   * @param length Bounded requested byte count, at most256KiB.
   */
  async pageSource(offset = '0', length = 4096): Promise<void> {
    this.beginAction();
    const selection = this.value.selection; if (!selection) return;
    const source = selection.attributes.kind === 'paged' ? selection.attributes.source : selection.element.source;
    await this.run('source', async job => {
      const response = await this.call(job, id => this.bridge.pageSource(job.binding, id, { sourceId: source.sourceId, pointer: source.pointer, sequence: source.sequence, offset, length }));
      if (!response || typeof response !== 'object' || !('status' in response) || response.status !== 'ok' || !('operation' in response) || response.operation !== 'source.page' || !('payload' in response)) throw new Error('Source page unavailable.');
      if (this.value.selection !== selection) throw new Superseded();
      const page = response.payload as ResponsePayloads['source.page']; const bytes = decodeBytePage(page); this.publish({ sourcePage: { page, text: new TextDecoder('utf-8', { fatal: false }).decode(bytes) } });
    });
  }
  private async navigate(position: number): Promise<void> {
    const intent = this.history[position]; if (!intent) return; const version = ++this.navigationVersion; this.replayVersion = version; this.position = position;
    const current = () => { if (version !== this.navigationVersion || this.closed) throw new Superseded(); };
    try {
      await this.cancelWork(); current();
      const filterChanged = JSON.stringify(this.value.filter) !== JSON.stringify(intent.filter);
      const graphChanged = JSON.stringify(this.graphIntent) !== JSON.stringify(intent.graph);
      this.publish({ filter: structuredClone(intent.filter), selection: null, sourcePage: null }); this.selectionIntent = null;
      if (graphChanged && intent.graph) { if (intent.graph.kind === 'neighbours') await this.showNeighbours(intent.graph.options, false); else await this.showPath(intent.graph.from, intent.graph.to, intent.graph.options, false); }
      else if (filterChanged) await this.run('filter', job => this.applyFilter(job));
      current(); await Promise.all([
        filterChanged || this.value.search?.text !== intent.search.text || this.value.search?.order !== intent.search.order ? this.searchPage('search', intent.search.text, intent.search.order, false, false) : undefined,
        filterChanged || this.value.findings?.text !== intent.findings ? this.searchPage('findings', intent.findings, 'identity', false, false) : undefined,
        filterChanged || this.value.groupAxis !== intent.groupAxis ? this.loadGroups(intent.groupAxis) : undefined,
        filterChanged ? this.loadCounts() : undefined,
      ]); current();
      if (intent.selection) await this.restoreSelection(intent.selection);
    } catch (error) { if (!(error instanceof Superseded)) this.publish({ error: 'The previous navigation intent could not be restored.' }); }
    finally { if (this.replayVersion === version) this.replayVersion = null; this.historyState(); }
  }
  /** Re-execute the previous bounded intent in the current generation. */
  async back(): Promise<void> { if (this.position > 0) await this.navigate(this.position - 1); }
  /** Re-execute the next bounded intent in the current generation. */
  async forward(): Promise<void> { if (this.position + 1 < this.history.length) await this.navigate(this.position + 1); }
  /** Cancel only this controller's active requests, retaining the accepted graph and sources. */
  async cancel(): Promise<void> { this.beginAction(); await this.cancelWork(); }
  private async cancelWork(): Promise<void> { const jobs = [...this.jobs.values()]; this.jobs.clear(); await Promise.all(jobs.map(job => this.abort(job))); this.busy(); }
  /** Release all owned view tokens and subscriptions; repeated disposal is safe. */
  async dispose(): Promise<void> { if (this.closed) return; this.closed = true; this.epoch++; await this.cancel(); await Promise.all([...this.tokens.values()].map(token => this.release(token))); this.base = null; this.committedBase = null; this.display = null; this.listeners.clear(); }
}
