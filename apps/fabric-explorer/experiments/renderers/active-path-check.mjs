/** Actual pinned SDK grouping/style/spread/path-selection regression; no GPU/paint or timing qualification. */
import assert from 'node:assert/strict';
import { stripTypeScriptTypes } from 'node:module';
import { readFileSync, readdirSync } from 'node:fs';
import { MultiDirectedGraph } from 'graphology';
import { createCorpus, visibleProjection } from './src/corpus.ts';
const previous = globalThis.WebGL2RenderingContext;
globalThis.WebGL2RenderingContext = { FLOAT: 0x1406 };
try {
  const directory = new URL('./node_modules/sigma/dist/', import.meta.url);
  const names = readdirSync(directory);
  const module = prefix => import(new URL(names.find(name => name.startsWith(prefix) && name.endsWith('.esm.js')), directory));
  const loop = await module('loop-'); const colors = await module('colors-'); const types = await module('types-');
  const sdk = readFileSync(new URL('sigma.esm.js', directory), 'utf8');
  const factory = readFileSync(new URL(names.find(name => name.startsWith('factory-') && name.endsWith('.esm.js')), directory), 'utf8');
  const extract = (text, head) => { const start = text.indexOf(head); assert.ok(start >= 0, head); let index = text.indexOf('{', start), depth = 1, end = index + 1; for (; depth; end++) { if (text[end] === '{') depth++; if (text[end] === '}') depth--; } return text.slice(start, end); };
  const groupSource = sdk.slice(sdk.indexOf('function groupKey('), sdk.indexOf('/**\n * Sigma.js Label Events'));
  const Index = new Function('_classCallCheck', '_defineProperty', '_createClass', '_createForOfIteratorHelper', '_slicedToArray', `${groupSource};return EdgeGroupIndex;`)(loop.c, loop.e, loop.a, colors.a, colors._);
  const setGraph = new Function('cancelAnimationFrame', `return ${extract(sdk, 'function setGraph(graph)')}`)(() => {});
  const spread = new Function(`return ${extract(sdk, 'function applyEdgeSpread(edge, data, edgeState)')}`)();
  const bind = new Function('_toConsumableArray', '_createForOfIteratorHelper', '_slicedToArray', `return ${extract(sdk, 'function bindGraphHandlers(ctx, activeListeners)')}`)(loop.f, colors.a, colors._);
  const { sigmaOptions } = await import('./src/sigma-options.ts');
  const adapterSource = stripTypeScriptTypes(readFileSync(new URL('./src/sigma-adapter.ts', import.meta.url), 'utf8')).replace(/^import .*;\s*$/gm, '').replace('export function createSigmaAdapter', 'function createSigmaAdapter');
  const createSigmaAdapter = new Function('Sigma', 'MultiDirectedGraph', 'sigmaOptions', adapterSource + '; return createSigmaAdapter;')(null, MultiDirectedGraph, sigmaOptions);
  let instance; let created = 0; let killed = 0;
  class ControlledSdk {
    constructor(graph, _container, options) {
      instance = this; created++; this.originalGraph = graph; this.internals = { graph }; this.options = options;
      this.events = new Map(); this.nodeStates = new Map(); this.edgeStates = new Map(); this.scheduled = 0; this.explicit = 0;
      this.cameraState = { x: .5, y: .5, ratio: 1, angle: 0 }; this.autoRescaleFrozen = true; this.checkEdgesEventsFrame = null;
      this.stateManager = { getEdgeState: id => this.getEdgeState(id), pruneNodes: predicate => { for (const id of this.nodeStates.keys()) if (!predicate(id)) this.nodeStates.delete(id); }, pruneEdges: predicate => { for (const id of this.edgeStates.keys()) if (!predicate(id)) this.edgeStates.delete(id); } };
      this.edgeGroups = new Index(graph, (ids, count) => ids.forEach((id, index) => Object.assign(this.getEdgeState(id), { parallelIndex: index, parallelCount: count })));
      this.edgePathsByName = new Map(options.primitives.edges.paths.map(path => [path.name, path]));
      this.context = { get graph() { return instance.internals.graph; }, edgeGroups: this.edgeGroups, markNodesDirty() {}, clearNodeState: () => { this.nodeStates.clear(); this.autoRescaleFrozen = false; }, clearEdgeState: () => this.edgeStates.clear(), clearNodeIndices() {}, clearEdgeIndices: () => this.edgeGroups.clear(), refresh: options => this.refresh(options) };
      this.bindGraphHandlers(); this.refresh();
    }
    bindGraphHandlers() { this.listeners = {}; bind(this.context, this.listeners); }
    unbindGraphHandlers() { for (const [name, handler] of Object.entries(this.listeners)) this.internals.graph.off(name, handler); }
    refresh(options) { if (options?.schedule) this.scheduled++; else { this.explicit++; this.edgeGroups.rebuild(); } }
    setGraph(graph) { return setGraph.call(this, graph); }
    getNodeState(id) { if (!this.nodeStates.has(id)) this.nodeStates.set(id, types.c()); return this.nodeStates.get(id); }
    getEdgeState(id) { if (!this.edgeStates.has(id)) this.edgeStates.set(id, types.a()); return this.edgeStates.get(id); }
    setNodeState(id, value) { Object.assign(this.getNodeState(id), value); }
    setEdgeState(id, value) { Object.assign(this.getEdgeState(id), value); }
    getCamera() { return { getState: () => ({ ...this.cameraState }), setState: value => Object.assign(this.cameraState, value) }; }
    graphToViewport(value) { return value; }
    on(name, callback) { this.events.set(name, callback); }
    kill() { killed++; }
    active(id) {
      const graph = this.internals.graph; const state = this.getEdgeState(id);
      const data = types.d(this.options.styles.edges, graph.getEdgeAttributes(id), state, types.b(), graph);
      spread.call(this, id, data, state);
      const paths = this.options.primitives.edges.paths; const ids = Object.fromEntries(paths.map((path, index) => [path.name, index]));
      const resolve = new Function('defaultHeadIndex', 'defaultTailIndex', 'pathNameToIndex', 'extremityNameToIndex', 'extremities', 'isAttributeSource', `return ${extract(factory, 'function resolveEdgeIds(data, isSelfLoop, isParallel)')}`)(0, 0, ids, {}, [{ length: 0 }], value => typeof value === 'object' && value !== null);
      const loopEdge = graph.source(id) === graph.target(id);
      return { data, state, path: paths[resolve(data, loopEdge, !loopEdge && state.parallelCount > 1).pathId].name };
    }
  }
  const source = createCorpus('M'); const empty = { nodes: [], edges: [] };
  const feature = { nodes: source.nodes.slice(0, 2), edges: source.edges.slice(0, 4) };
  const selections = [];
  const adapter = createSigmaAdapter(empty, { querySelector: () => null }, (id, method) => selections.push({ id, method }), ControlledSdk);
  for (const view of [visibleProjection(source), visibleProjection(source, 5000, 20000), visibleProjection(source, 5000, 20000, 0), visibleProjection(source), feature]) {
    adapter.panZoom(1);
    for (const key of instance.internals.graph.nodes()) instance.setNodeState(key, { isHighlighted: true, isHovered: true, isLabelHovered: true, isDragged: true });
    for (const key of instance.internals.graph.edges()) instance.setEdgeState(key, { isHighlighted: true, isHovered: true, isLabelHovered: true });
    adapter.replace(view);
    for (const state of [...instance.nodeStates.values(), ...instance.edgeStates.values()]) for (const key of ['isHighlighted', 'isHovered', 'isLabelHovered', 'isDragged']) assert.ok(!state[key], `Transient ${key} must not survive replacement`);
    for (const edge of view.edges.filter(edge => ['e0', 'e1', 'e2', 'e3'].includes(edge.id))) {
      const actual = instance.active(edge.id);
      assert.equal(actual.data.label, edge.label);
      assert.equal(actual.path, edge.source === edge.target ? 'loop' : 'curved', `${edge.id}: active SDK path must respect real sibling grouping`);
    }
    assert.equal(instance.edgeGroups.graph, instance.internals.graph, 'The actual SDK index must retain the rendered graph identity');
    assert.equal(instance.internals.graph, instance.originalGraph);
    assert.deepEqual(instance.cameraState, { x: .5, y: .5, ratio: 1, angle: 0 });
    assert.equal(instance.autoRescaleFrozen, false);
  }
  const forward = ['e0', 'e1', 'e3'].map(id => { const value = instance.active(id); assert.equal(value.state.parallelCount, 3); return value.data.curvature * (instance.internals.graph.source(id) < instance.internals.graph.target(id) ? 1 : -1); });
  assert.equal(new Set(forward).size, 3, 'Canonical-orientation curves must separate the parallel/reverse relation paths');
  adapter.inspect('e1'); instance.events.get('clickEdge')({ edge: 'e3' });
  assert.deepEqual(selections.at(-1), { id: 'e3', method: 'edge-pointer' });
  assert.equal(created, 1); assert.ok(instance.scheduled > 0); assert.equal(killed, 0); adapter.destroy(); assert.equal(killed, 1);
  console.log('PASS: actual SDK group/style/spread/path chain across empty/default/expanded/group/reset/feature and public stable-graph events.');
} finally { globalThis.WebGL2RenderingContext = previous; }
