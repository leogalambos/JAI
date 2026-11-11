/** Disposable Sigma adapter; graph replacement reuses native contexts without asserting native cost. */
import Sigma from 'sigma';
import { MultiDirectedGraph } from 'graphology';
import { sigmaOptions } from './sigma-options';
import type { Vertex, Relation } from './corpus';
/** Bounded graph data consumed by the renderer only. */
export type SigmaView = { nodes: Vertex[]; edges: Relation[] };
/**
 * Construct one Sigma instance and retain it across graph-only changes.
 * @param data Bounded initial view, including an optional empty baseline.
 * @param container Owned graph canvas container.
 * @param selected Receives selected IDs and input method.
 * @param Constructor Actual SDK constructor, injectable only by controlled tests.
 * @returns Adapter with current-graph selection, replacement and final cleanup.
 */
export function createSigmaAdapter(data: SigmaView, container: HTMLElement, selected: (id: string, method?: string) => void, Constructor = Sigma) {
  const build = (value: SigmaView) => {
    const next = new MultiDirectedGraph();
    for (const node of value.nodes) next.addNode(node.id, { ...node, size: 4, color: node.id === 'v0' ? '#ba365e' : '#365e94' });
    for (const edge of value.edges) next.addDirectedEdgeWithKey(edge.id, edge.source, edge.target, { ...edge, size: 1, color: edge.ordinal < 4 ? '#ba365e' : '#a1b2c4' });
    return next;
  };
  const graph = build(data);
  const renderer = new Constructor(graph, container, sigmaOptions());
  let cachedGpuInfo: { webgl2: boolean; renderer: string; softwareLikely: boolean | null; source: string } | undefined;
  const freshCamera = { ...renderer.getCamera().getState() };
  let initial = { ...freshCamera };
  const select = (id: string, method = 'programmatic') => {
    for (const key of graph.nodes()) if (renderer.getNodeState(key).isHighlighted) renderer.setNodeState(key, { isHighlighted: false });
    for (const key of graph.edges()) if (renderer.getEdgeState(key).isHighlighted) renderer.setEdgeState(key, { isHighlighted: false });
    if (graph.hasEdge(id)) renderer.setEdgeState(id, { isHighlighted: true });
    else if (graph.hasNode(id)) renderer.setNodeState(id, { isHighlighted: true });
    selected(id, method);
  };
  renderer.on('clickNode', event => select(event.node, 'vertex-pointer'));
  renderer.on('clickEdge', event => select(event.edge, 'edge-pointer'));
  return {
    destroy: () => renderer.kill(),
    gpuInfo() {
      if (cachedGpuInfo) return cachedGpuInfo;
      // Borrow the already initialized public stage canvas; never create or lose
      // a diagnostic context, and never lose this renderer-owned context.
      const gl = renderer.getStageCanvas().getContext('webgl2');
      const extension = gl?.getExtension('WEBGL_debug_renderer_info');
      const name = extension && gl ? String(gl.getParameter(extension.UNMASKED_RENDERER_WEBGL)) : 'unavailable';
      cachedGpuInfo = { webgl2: Boolean(gl), renderer: name, softwareLikely: name === 'unavailable' ? null : /swiftshader|llvmpipe|software/i.test(name), source: 'existing-renderer-stage-context' };
      return cachedGpuInfo;
    },
    replace(value: SigmaView) {
      const next = build(value);
      for (const key of graph.nodes()) {
        const state = renderer.getNodeState(key);
        if (state.isHighlighted || state.isHovered || state.isLabelHovered || state.isDragged) renderer.setNodeState(key, { isHighlighted: false, isHovered: false, isLabelHovered: false, isDragged: false });
      }
      for (const key of graph.edges()) {
        const state = renderer.getEdgeState(key);
        if (state.isHighlighted || state.isHovered || state.isLabelHovered) renderer.setEdgeState(key, { isHighlighted: false, isHovered: false, isLabelHovered: false });
      }
      renderer.getCamera().setState(freshCamera);
      // Sigma 4.0.5's group index retains the constructor graph. Mutate that
      // public Graphology instance so actual SDK mutation handlers update it.
      graph.clear();
      next.forEachNode((key, attributes) => graph.addNode(key, attributes));
      next.forEachEdge((key, attributes, source, target) => graph.addDirectedEdgeWithKey(key, source, target, attributes));
      renderer.refresh();
      initial = { ...renderer.getCamera().getState() };
    },
    panZoom: (t: number) => renderer.getCamera().setState({ x: initial.x + Math.sin(t * 2) * 0.06, y: initial.y + Math.cos(t * 2) * 0.06, ratio: initial.ratio * (0.85 + Math.sin(t) * 0.1) }),
    inspect: (id: string) => select(id),
    nodePoint: (id: string) => renderer.graphToViewport(graph.getNodeAttributes(id) as { x: number; y: number }),
    loseContext: () => {
      const gl = container.querySelector('canvas')?.getContext('webgl2');
      const extension = gl?.getExtension('WEBGL_lose_context');
      if (!extension) return 'extension-unavailable'; extension.loseContext(); return 'loss-requested';
    },
  };
}
