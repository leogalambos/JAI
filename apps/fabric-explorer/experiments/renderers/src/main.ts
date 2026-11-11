/** Disposable dual-renderer probe; synthetic projection only, never canonical import or product code. */
import cytoscape from 'cytoscape';
import type { Core } from 'cytoscape';
import { createSigmaAdapter } from './sigma-adapter';
import { createViewController } from './view-controller';
import type { CorpusSize } from './corpus';
import type { CorpusReply, CorpusRequest } from './corpus-service';
import CorpusWorker from './corpus.worker?worker&inline';
import { installProbeControls } from './probe-controls';
import type { ProbeProgress } from './probe-controls';
import { animateProjection } from './animation';
import './style.css';

type Kind = 'sigma' | 'cytoscape';
type View = CorpusReply['view'];
type Adapter = { gpuInfo?(): Record<string, unknown>; replace?(data: View): void; destroy(): void; panZoom(t: number): void; inspect(id: string): void; nodePoint(id: string): { x: number; y: number }; loseContext(): string; };
const parameters = new URLSearchParams((window as Window & { rendererProbeParameters?: string }).rendererProbeParameters ?? location.search);
const kind: Kind = parameters.get('renderer') === 'cytoscape' ? 'cytoscape' : 'sigma';
const size: CorpusSize = parameters.get('size') === 'L' ? 'L' : parameters.get('size') === 'S' ? 'S' : 'M';
const graphElement = document.querySelector<HTMLElement>('#graph')!;
const statusElement = document.querySelector<HTMLElement>('#status')!;
const detailsElement = document.querySelector<HTMLElement>('#details')!;
const controls = installProbeControls(document, window, parameters.get('review') ?? 'all');
Object.assign(window, { rendererProbeControls: controls });
const initialProgress = (window as Window & { rendererProbeProgress?: ProbeProgress }).rendererProbeProgress;
if (initialProgress) controls.setProgress(initialProgress);
const longTasks: number[] = [];
let lastPick: { kind: string; id: string } | null = null;
const pointerEvents: { kind: string; id: string; atMs: number }[] = [];
let metadata: CorpusReply['metadata'];
let initialized = false;
let view: View;
let adapter: Adapter;
let generation = 0;
let generationMs = 0;
let projectionMs = 0;
let buildMs = 0;
let longTaskObserverAvailable = false;
try { new PerformanceObserver(list => list.getEntries().forEach(entry => longTasks.push(entry.duration))).observe({ type: 'longtask', buffered: true }); longTaskObserverAvailable = true; } catch { /* An unsupported observer is recorded below, never a pass. */ }

function detail(id: string, clickedKind = 'programmatic') {
  const value = view.nodes.find(node => node.id === id) ?? view.edges.find(edge => edge.id === id);
  document.querySelector<HTMLElement>('#selected-identity')!.textContent = value ? `${'source' in value ? 'Relation' : 'Vertex'} ${value.id}` : 'No selected element';
  document.querySelector<HTMLElement>('#selected-label')!.textContent = value?.label ?? '';
  detailsElement.textContent = JSON.stringify({ selectionMethod: clickedKind, element: value ?? null }, null, 2);
  if (clickedKind !== 'programmatic') {
    lastPick = { kind: clickedKind, id };
    if (pointerEvents.length < 1000) pointerEvents.push({ ...lastPick, atMs: performance.now() });
  }
}

function cytoscapeAdapter(data: View): Adapter {
  const cy: Core = cytoscape({
    container: graphElement,
    elements: [
      ...data.nodes.map(node => ({ data: { ...node }, position: { x: node.x * 4, y: node.y * 4 } })),
      ...data.edges.map(edge => ({ data: { ...edge } })),
    ],
    layout: { name: 'preset', fit: true, padding: 30 },
    style: [
      { selector: 'node', style: { label: 'data(label)', width: 8, height: 8, 'background-color': '#365e94', 'font-size': 10, 'min-zoomed-font-size': 8 } },
      { selector: 'edge', style: { label: 'data(label)', width: 1, 'line-color': '#a1b2c4', 'target-arrow-color': '#a1b2c4', 'target-arrow-shape': 'triangle', 'curve-style': 'bezier', 'font-size': 9, 'min-zoomed-font-size': 10, 'text-rotation': 'autorotate', 'loop-direction': '-45deg', 'loop-sweep': '70deg' } },
      { selector: '.inspected', style: { 'background-color': '#ba365e', 'line-color': '#ba365e', 'target-arrow-color': '#ba365e', 'font-size': 12, 'min-zoomed-font-size': 0, 'text-background-color': '#ffffff', 'text-background-opacity': 1 } },
    ],
    hideEdgesOnViewport: false, textureOnViewport: false, pixelRatio: 'auto',
  });
  const select = (id: string, method = 'programmatic') => { cy.elements().removeClass('inspected'); cy.getElementById(id).addClass('inspected'); detail(id, method); };
  cy.on('tap', 'node', event => select(event.target.id(), 'vertex-pointer'));
  cy.on('tap', 'edge', event => select(event.target.id(), 'edge-pointer'));
  const pan = cy.pan(); const zoom = cy.zoom();
  return {
    destroy: () => cy.destroy(),
    panZoom: t => cy.viewport({ zoom: zoom * (0.85 + Math.sin(t) * 0.1), pan: { x: pan.x + Math.sin(t * 2) * 40, y: pan.y + Math.cos(t * 2) * 40 } }),
    inspect: id => select(id),
    nodePoint: id => cy.getElementById(id).renderedPosition(),
    loseContext: () => 'not-applicable-canvas-renderer',
  };
}

type Phases = { mark(name: string): void; snapshot(): Record<string, unknown> };
const phaseApi = () => (window as Window & { rendererProbePhases?: Phases }).rendererProbePhases;
const phase = (name: string) => phaseApi()?.mark(name);
const worker = new CorpusWorker();
let sequence = 0;
const pending = new Map<number, { resolve(reply: CorpusReply): void; reject(error: Error): void }>();
worker.onmessage = (event: MessageEvent<CorpusReply & { error?: string }>) => {
  const callback = pending.get(event.data.requestId); if (!callback) return;
  pending.delete(event.data.requestId);
  if (event.data.error) callback.reject(new Error(event.data.error)); else callback.resolve(event.data);
};
worker.onerror = event => { for (const callback of pending.values()) callback.reject(new Error(event.message)); pending.clear(); };
function requestView(request: Omit<CorpusRequest, 'requestId'>): Promise<CorpusReply> {
  const requestId = ++sequence;
  return new Promise((resolve, reject) => { pending.set(requestId, { resolve, reject }); worker.postMessage({ ...request, requestId }); });
}
const views = createViewController<View, Adapter>(data => kind === 'sigma' ? createSigmaAdapter(data, graphElement, detail) : cytoscapeAdapter(data));
function mount(data: View, label = 'graph-build') {
  generation++; view = data; phase(label);
  const started = performance.now(); adapter = views.set(view); buildMs = performance.now() - started;
  statusElement.textContent = `${kind} / ${size}: ${view.nodes.length} vertices, ${view.edges.length} edges; hidden ${view.hiddenVertices}/${view.hiddenEdges}; exploratory only`;
  if (view.nodes.length) adapter.inspect(view.nodes[0].id);
}
async function rebuild(vertexLimit = 2000, edgeLimit = 8000, group?: number) {
  phase(initialized ? 'projection-request' : 'corpus-generation-and-bounded-transfer');
  const reply = await requestView(initialized ? { type: 'project', vertexLimit, edgeLimit, group } : { type: 'initialize', size, vertexLimit, edgeLimit, group });
  initialized = true; metadata = reply.metadata; generationMs = reply.generationMs; projectionMs = reply.projectionMs;
  mount(reply.view);
}
window.addEventListener('pagehide', () => { views.dispose(); worker.terminate(); });

function gpuInfo() {
  return adapter?.gpuInfo?.() ?? { webgl2: false, renderer: 'not-applicable-canvas-renderer', softwareLikely: null, source: 'renderer-has-no-webgl-diagnostic' };
}

const api = {
  ready: false,
  error: null as string | null,
  inspect: (id: string) => adapter.inspect(id),
  details: () => detailsElement.textContent,
  nodePoint: (id: string) => adapter.nodePoint(id),
  bootstrapped: true,
  loadFeature: async () => { await rebuild(2, 4); api.ready = true; return api.summary(); },
  loadGraph: async () => { await rebuild(); api.ready = true; return api.summary(); },
  emptyRenderer: () => { mount({ nodes: [], edges: [], hiddenVertices: 0, hiddenEdges: 0 }, 'empty-renderer-first-construction-this-page'); return { visibleVertices: 0, visibleEdges: 0 }; },
  expand: async () => { await rebuild(5000, 20000); return api.summary(); },
  reset: async () => { await rebuild(); return api.summary(); },
  featureView: async () => {
    const reply = await requestView({ type: 'feature' });
    mount(reply.view, 'manual-feature-build');
    statusElement.textContent = `${kind}: manual feature fixture only — two vertices, parallel e0/e1, self-loop e2, reverse e3; not a performance sample`;
    return api.summary();
  },
  group: async (group: number) => { if (!Number.isInteger(group) || group < 0 || group > 9) throw new Error('Group must be 0..9'); await rebuild(5000, 20000, group); return api.summary(); },
  loseContext: () => adapter.loseContext(),
  summary: () => ({ kind, size, seed: metadata.seed, corpusVertices: metadata.vertices, corpusEdges: metadata.edges, findingsMetadataCount: metadata.findings, workerOwnsFullCorpus: true,
    visibleVertices: view.nodes.length, visibleEdges: view.edges.length, hiddenVertices: view.hiddenVertices, hiddenEdges: view.hiddenEdges, generation,
    generationMs, projectionMs, buildMs, gpu: gpuInfo(), deviceScale: devicePixelRatio, viewport: { width: innerWidth, height: innerHeight }, graphViewport: { width: graphElement.clientWidth, height: graphElement.clientHeight }, lastPick, pointerEvents: [...pointerEvents],
    labelReadability: 'manual-review-required', directedParallelAndLoopPicking: 'manual-pointer-review-required',
    inputSemantics: 'synthetic-projection-not-canonical-journal', qualification: 'exploratory-only' }),
  animate: (durationMs = 20000) => animateProjection({
    now: () => performance.now(), requestFrame: callback => requestAnimationFrame(callback),
    generation: () => generation, panZoom: seconds => adapter.panZoom(seconds),
  }, durationMs).then(result => ({ ...result, phaseEvidence: phaseApi()?.snapshot() ?? null, longTasksMs: [...longTasks], longTaskObserverAvailable,
    noTaskOver200ms: longTaskObserverAvailable ? longTasks.every(value => value <= 200) : null, qualification: 'exploratory-only' })),
  cancel: () => { generation++; return { generation, acknowledgedAt: performance.now() }; },
};
Object.assign(window, { rendererProbe: api });
if (parameters.get('mode') !== 'labels-only' && parameters.get('diagnostics') !== 'memory-phases') {
  void api.loadGraph().catch(error => { api.error = String(error); statusElement.textContent = api.error; });
} else statusElement.textContent = 'Harness loaded with no renderer or corpus; controlled memory baselines precede graph loading.';
