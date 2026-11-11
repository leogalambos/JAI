// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Separate synthetic engine measurement; not a browser/GPU or product-RSS qualification. */
import assert from 'node:assert/strict';
import { performance } from 'node:perf_hooks';
import { cpus, totalmem } from 'node:os';
import { elementKey, edgeKey, PROTOCOL, RELATION_DIRECTIONS } from '@jai/fabric-explorer-contracts';
import { QueryIndex, DEFAULT_QUERY_LIMITS } from '../src/graph/query-index.ts';
import { layoutProjection } from '../src/layout/engine.ts';

const binding = { sessionId: 'synthetic-smoke', capability: 'synthetic-capability', generation: '1' };
const relations = Object.keys(RELATION_DIRECTIONS);
const attributes = { kind: 'inline', value: { type: 'null' } };
const source = { projectId: 'synthetic', rootId: 'synthetic-root', sourceId: 'synthetic-source', family: 'fabric', relativePath: 'synthetic.jsonl', pointer: '', sequence: '1', revisionId: 'synthetic-revision', adapterVersion: 'synthetic-graph/1' };
const observed = '2026-11-10T00:00:00Z';

/** Build deterministic skewed cyclic/parallel synthetic records; no canonical input is read. */
function _corpus(vertices, edges) {
  const nodes = Array.from({ length: vertices }, (_, i) => {
    const identity = { kind: 'participant', projectId: 'synthetic', participant: { kind: 'controller', id: `node-${i}` } };
    return { id: elementKey(identity), identity, kind: 'participant', label: `Node ${String(i).padStart(6, '0')}`, source, attributes };
  });
  const links = Array.from({ length: edges }, (_, i) => {
    const from = i % 19 === 0 ? 0 : Math.floor(i * vertices / edges);
    const to = i % 23 === 0 ? from : (from + [1, 1, 7, 113][i % 4]) % vertices;
    const identity = { kind: 'explicit', projectId: 'synthetic', origin: nodes[from].identity, sourceEdgeId: `edge-${i}`, from: nodes[from].identity, to: nodes[to].identity };
    return { id: edgeKey(identity), identity, from: nodes[from].id, to: nodes[to].id, relation: 'other-reference', label: 'Synthetic association', source, basis: 'exact-reference', causal: false, attributes };
  });
  const snapshot = { format: 'jai.fabric-explorer.snapshot/1', sessionId: binding.sessionId, generation: '1', sources: [{ ...source, byteLength: '1', digest: '0'.repeat(64), head: null, observedAt: observed, verification: { mode: 'diagnostic', decoded: 'decoded', chain: 'unknown', replay: 'unknown', publicTrust: 'unknown', material: 'not-observed', recordedApplicability: null, authorityGranted: false, freshAssessment: false } }], counts: { vertices: String(vertices), edges: String(edges), findings: '0' }, authorityGranted: false, freshAssessment: false };
  // SourceRevision excludes record-local pointer and sequence comes from the source.
  delete snapshot.sources[0].pointer;
  return { nodes, links, snapshot };
}

/** Run the finite engine cases; a failed assertion exits unsuccessfully. */
async function _run() {
const measurements = [];
for (const [tier, vertexCount, edgeCount] of [['S', 1000, 3000], ['M', 25000, 100000]]) {
  const corpus = _corpus(vertexCount, edgeCount);
  const started = performance.now();
  const index = new QueryIndex({ snapshot: corpus.snapshot, records: [...corpus.nodes, ...corpus.links] }, binding);
  const indexMs = performance.now() - started;
  const lookup = [];
  for (let i = 0; i < 100; i++) {
    const before = performance.now();
    const reply = index.execute({ protocol: PROTOCOL, kind: 'request', binding, requestId: `lookup-${i}`, operation: 'element.lookup', payload: { identity: corpus.nodes[(i * 251) % vertexCount].identity } });
    assert(reply.value.vertex); lookup.push(performance.now() - before);
  }
  const beforeQuery = performance.now();
  const reply = index.execute({ protocol: PROTOCOL, kind: 'request', binding, requestId: `neighbours-${tier}`, operation: 'graph.neighbours', payload: { identity: corpus.nodes[0].identity, direction: 'both', relations, causalOnly: false, limits: DEFAULT_QUERY_LIMITS } });
  const queryMs = performance.now() - beforeQuery;
  assert(reply.operation === 'graph.neighbours');
  assert(reply.value.projection.vertices.length <= DEFAULT_QUERY_LIMITS.maxVertices);
  assert(reply.value.projection.edges.length <= DEFAULT_QUERY_LIMITS.maxEdges);
  assert(reply.work.visitedVertices <= DEFAULT_QUERY_LIMITS.maxVisitedVertices);
  assert(reply.work.scannedEdges <= DEFAULT_QUERY_LIMITS.maxScannedEdges);
  const beforeLayout = performance.now();
  const layout = await layoutProjection({ binding: { ...binding, requestId: `layout-${tier}`, projectionId: `projection-${tier}` }, graph: reply.handles }, { yieldControl: () => new Promise(resolve => setImmediate(resolve)) });
  const layoutMs = performance.now() - beforeLayout;
  assert.equal(layout.positions.length, reply.handles.vertices.length);
  assert(layout.positions.every(position => Number.isFinite(position.x) && Number.isFinite(position.y)));
  let cancellationChecks = 0;
  const beforeCancel = performance.now();
  assert.throws(() => index.execute({ protocol: PROTOCOL, kind: 'request', binding, requestId: `cancel-${tier}`, operation: 'graph.neighbours', payload: { identity: corpus.nodes[0].identity, direction: 'both', relations, causalOnly: false, limits: DEFAULT_QUERY_LIMITS } }, { cancelled: () => ++cancellationChecks >= 8 }), error => error.code === 'cancelled');
  const cancelMs = performance.now() - beforeCancel;
  let yielded = false;
  await assert.rejects(layoutProjection({ binding: { ...binding, requestId: `cancel-layout-${tier}`, projectionId: `projection-${tier}` }, graph: reply.handles }, { cancelled: () => yielded, yieldControl: async () => { yielded = true; } }), error => error.code === 'cancelled');
  lookup.sort((a, b) => a - b);
  measurements.push({ tier, indexedVertices: vertexCount, indexedEdges: edgeCount, indexMs, lookupSamples: lookup.length, lookupP95Ms: lookup[94], queryMs, visitedVertices: reply.work.visitedVertices, scannedEdges: reply.work.scannedEdges, visibleVertices: reply.handles.vertices.length, visibleEdges: reply.handles.edges.length, algorithm: layout.algorithm, seed: 1, iterations: layout.iterations, layoutMs, layoutWork: layout.work, cancellationChecks, cancelMs, layoutCancelledAtYield: yielded, residentBytes: process.memoryUsage().rss });
  index.dispose();
}
console.log(JSON.stringify({ format: 'jai.fabric-explorer.graph-smoke/1', scope: 'synthetic Node engine only; no GPU/product RSS qualification', node: process.version, platform: process.platform, hardware: { cpuModel: cpus()[0]?.model, logicalCpus: cpus().length, totalMemoryBytes: totalmem() }, visibleBudgets: { vertices: DEFAULT_QUERY_LIMITS.maxVertices, edges: DEFAULT_QUERY_LIMITS.maxEdges }, measurements }, null, 2));
}
_run().catch(error => { console.error(error); process.exitCode = 1; });
