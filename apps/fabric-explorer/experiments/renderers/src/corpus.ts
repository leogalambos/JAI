/** Disposable deterministic synthetic projection generator; no canonical journal semantics. */
export type CorpusSize = 'S' | 'M' | 'L';
export type Vertex = { id: string; label: string; x: number; y: number; group: number };
export type Relation = { id: string; source: string; target: string; label: string; ordinal: number };
export type Corpus = { seed: number; size: CorpusSize; nodes: Vertex[]; edges: Relation[]; findings: number };
export const dimensions: Record<CorpusSize, { vertices: number; edges: number; findings: number }> = {
  S: { vertices: 1000, edges: 3000, findings: 100 },
  M: { vertices: 25000, edges: 100000, findings: 5000 },
  L: { vertices: 100000, edges: 500000, findings: 20000 },
};

export function createCorpus(size: CorpusSize, seed = 20261109): Corpus {
  const count = dimensions[size];
  let state = seed >>> 0;
  const random = () => { state = (Math.imul(state, 1664525) + 1013904223) >>> 0; return state / 4294967296; };
  const nodes = Array.from({ length: count.vertices }, (_, i) => {
    const group = i % 10;
    const angle = (i / 10) * 2.399963229728653;
    const radius = 2 + Math.sqrt(i / 10) * 0.4;
    return {
      id: `v${i}`, group,
      label: i === 0 ? 'Selected requirement — café ∑ synthetic version A' : `Synthetic entity ${i} · group ${group}`,
      x: (group % 5) * 45 + Math.cos(angle) * radius,
      y: Math.floor(group / 5) * 90 + Math.sin(angle) * radius,
    };
  });
  const edges = Array.from({ length: count.edges }, (_, i) => {
    const pool = Math.min(count.vertices, i < 8000 ? 2000 : i < 20000 ? 5000 : count.vertices);
    const source = i % 17 === 0 ? 0 : Math.floor(random() * pool);
    const target = Math.floor(random() * pool);
    return { id: `e${i}`, source: `v${source}`, target: `v${target}`, label: `depends on · synthetic relation ${i}`, ordinal: i };
  });
  edges[0] = { id: 'e0', source: 'v0', target: 'v1', label: 'Parallel relation α — exact version A', ordinal: 0 };
  edges[1] = { id: 'e1', source: 'v0', target: 'v1', label: 'Parallel relation β — exact version B', ordinal: 1 };
  edges[2] = { id: 'e2', source: 'v0', target: 'v0', label: 'Self-loop, association only', ordinal: 2 };
  edges[3] = { id: 'e3', source: 'v1', target: 'v0', label: 'Reverse association', ordinal: 3 };
  return { seed, size, nodes, edges, findings: count.findings };
}

export function visibleProjection(corpus: Corpus, vertexLimit = 2000, edgeLimit = 8000, group?: number) {
  const candidates = group === undefined ? corpus.nodes : corpus.nodes.filter(node => node.group === group);
  const nodes = candidates.slice(0, Math.min(vertexLimit, 5000));
  const admitted = new Set(nodes.map(node => node.id));
  const edges: Relation[] = [];
  const limit = Math.min(edgeLimit, 20000);
  if (limit > 0 && nodes.length) for (const edge of corpus.edges) {
    if (admitted.has(edge.source) && admitted.has(edge.target)) edges.push(edge);
    if (edges.length === limit) break;
  }
  return { nodes, edges, hiddenVertices: corpus.nodes.length - nodes.length, hiddenEdges: corpus.edges.length - edges.length };
}
