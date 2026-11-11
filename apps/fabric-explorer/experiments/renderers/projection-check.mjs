/** Failed-first actual projection equivalence/visit-count regression, not a native timing claim. */
import assert from 'node:assert/strict';
import { createCorpus, visibleProjection } from './src/corpus.ts';
function originalContract(corpus, vertices, edges, group) {
  const nodes = (group === undefined ? corpus.nodes : corpus.nodes.filter(node => node.group === group)).slice(0, Math.min(vertices, 5000));
  const ids = new Set(nodes.map(node => node.id));
  const selected = corpus.edges.filter(edge => ids.has(edge.source) && ids.has(edge.target)).slice(0, Math.min(edges, 20000));
  return { nodes, edges: selected, hiddenVertices: corpus.nodes.length - nodes.length, hiddenEdges: corpus.edges.length - selected.length };
}
for (const size of ['S', 'M', 'L']) {
  const source = createCorpus(size);
  for (const [vertices, edges, group] of [[2000, 8000], [5000, 20000], [5000, 20000, 0], [2000, 0], [3, 2, 9]]) {
    assert.deepEqual(visibleProjection(source, vertices, edges, group), originalContract(source, vertices, edges, group));
  }
}
const corpus = createCorpus('M');
let visits = 0;
corpus.edges = new Proxy(corpus.edges, { get(target, key, receiver) { if (typeof key === 'string' && /^\d+$/.test(key)) visits++; return Reflect.get(target, key, receiver); } });
visibleProjection(corpus);
assert.equal(visits, 8000, 'Default projection must stop after its first 8000 admitted relations');
visits = 0; visibleProjection(corpus, 2000, 0);
assert.equal(visits, 0, 'Zero-edge projection must not scan relations');
console.log('PASS: 15 output-equivalence cases; bounded default scan8000 and zero-edge scan0.');
