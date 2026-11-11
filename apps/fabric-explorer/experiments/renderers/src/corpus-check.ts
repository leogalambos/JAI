/** Disposable corpus invariants; run without browser or renderer qualification. */
import assert from 'node:assert/strict';
import { createCorpus, visibleProjection, dimensions } from './corpus.ts';
import type { CorpusSize } from './corpus.ts';
for (const size of ['S', 'M', 'L'] as CorpusSize[]) {
  const graph = createCorpus(size);
  assert.equal(graph.nodes.length, dimensions[size].vertices);
  assert.equal(graph.edges.length, dimensions[size].edges);
  assert.equal(new Set(graph.edges.map(edge => edge.id)).size, graph.edges.length);
  assert.equal(graph.edges[0].source, graph.edges[1].source);
  assert.equal(graph.edges[0].target, graph.edges[1].target);
  assert.equal(graph.edges[2].source, graph.edges[2].target);
  const view = visibleProjection(graph);
  assert.equal(view.nodes.length, Math.min(2000, graph.nodes.length));
  assert.equal(view.edges.length, Math.min(8000, graph.edges.length));
  const expanded = visibleProjection(graph, 5000, 20000);
  assert.equal(expanded.nodes.length, Math.min(5000, graph.nodes.length));
  assert.equal(expanded.edges.length, Math.min(20000, graph.edges.length));
  const group = visibleProjection(graph, 5000, 20000, 0);
  assert.ok(group.nodes.every(node => node.group === 0));
  const groupIds = new Set(group.nodes.map(node => node.id));
  assert.ok(group.edges.every(edge => groupIds.has(edge.source) && groupIds.has(edge.target)));
  const repeat = createCorpus(size);
  assert.deepEqual(graph.edges.slice(-100), repeat.edges.slice(-100));
  console.log(JSON.stringify({ size, vertices: graph.nodes.length, edges: graph.edges.length, visibleVertices: view.nodes.length, visibleEdges: view.edges.length, deterministicTail: true }));
}
