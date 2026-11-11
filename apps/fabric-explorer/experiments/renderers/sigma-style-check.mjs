/** Disposable failed-first audit of actual Sigma display-data bindings, not an inspector or GPU mock. */
import assert from 'node:assert/strict';
import { MultiDirectedGraph } from 'graphology';
import { createCorpus } from './src/corpus.ts';
const previous = globalThis.WebGL2RenderingContext;
// The installed path factories require this enum at module load. No WebGL
// context, paint, font or native picking verdict is created by this SDK audit.
globalThis.WebGL2RenderingContext = { FLOAT: 0x1406 };
try {
  const { evaluateEdgeStyle, evaluateNodeStyle, DEFAULT_STYLES } = await import('sigma/types');
  const { sigmaOptions } = await import('./src/sigma-options.ts');
  const options = sigmaOptions();
  const source = createCorpus('S');
  const graph = new MultiDirectedGraph();
  for (const node of source.nodes.slice(0, 2)) graph.addNode(node.id, { ...node, size: 7, color: '#315779' });
  for (const [index, edge] of source.edges.slice(0, 4).entries()) graph.addDirectedEdgeWithKey(edge.id, edge.source, edge.target, { ...edge, size: 3 + index, color: '#9a316f' });
  const graphState = { isIdle: true, isPanning: false, isZooming: false, isDragging: false, hasHovered: false, hasHighlighted: false };
  const edgeState = { isHovered: false, isLabelHovered: false, isHidden: false, isHighlighted: false, parallelIndex: 0, parallelCount: 3 };
  for (const id of ['e0', 'e1', 'e2', 'e3']) for (const state of [edgeState, { ...edgeState, isHighlighted: true }, { ...edgeState, isHidden: true }, { ...edgeState, isHighlighted: true, isHovered: true }]) {
    const attributes = graph.getEdgeAttributes(id);
    const displayed = evaluateEdgeStyle(options.styles.edges, attributes, state, graphState, graph);
    assert.equal(displayed.label, attributes.label, `${id}: graph label must survive the actual SDK evaluator`);
    assert.equal(displayed.size, attributes.size, `${id}: graph size binding must survive`);
    assert.equal(displayed.color, attributes.color, `${id}: graph colour binding must survive`);
    assert.equal(displayed.visibility, state.isHidden ? 'hidden' : 'visible');
    const baseline = evaluateEdgeStyle(DEFAULT_STYLES.edges, attributes, state, graphState, graph);
    assert.equal(displayed.depth, baseline.depth, 'Preserve the actual SDK default depth predicate rather than inventing a selection rule');
    assert.equal(displayed.labelVisibility, state.isHighlighted ? 'visible' : 'auto');
    assert.equal(displayed.head, 'arrow');
    assert.equal(displayed.parallelPath, 'curved');
    assert.equal(displayed.selfLoopPath, 'loop');
  }
  const nodeState = { isHovered: false, isLabelHovered: false, isHidden: false, isHighlighted: false, isDragged: false };
  // Match the real constructor's branch fallback, since this adapter intentionally
  // customizes only edges; a missing node branch retains DEFAULT_STYLES.nodes.
  const nodeStyles = options.styles.nodes ?? DEFAULT_STYLES.nodes;
  for (const id of ['v0', 'v1']) for (const state of [nodeState, { ...nodeState, isHovered: true }, { ...nodeState, isHidden: true }]) {
    const attributes = graph.getNodeAttributes(id);
    const displayed = evaluateNodeStyle(nodeStyles, attributes, state, graphState, graph);
    for (const field of ['label', 'size', 'color', 'x', 'y']) assert.equal(displayed[field], attributes[field], `${id}: node ${field} binding`);
    assert.equal(displayed.visibility, state.isHidden ? 'hidden' : 'visible');
    assert.equal(displayed.depth, state.isHovered ? 'topNodes' : 'nodes');
  }
  assert.equal(options.settings.renderEdgeLabels, true);
  assert.equal(options.settings.enableEdgeEvents, true);
  console.log('PASS: real SDK edge normal/selected/hidden label-size-colour-depth-visibility bindings, directional primitives and node fallback.');
} finally { globalThis.WebGL2RenderingContext = previous; }
