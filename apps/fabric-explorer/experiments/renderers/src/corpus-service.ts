/** Disposable worker-owned corpus service; only bounded projections cross the UI boundary. */
import { createCorpus, visibleProjection } from './corpus.ts';
import type { Corpus, CorpusSize } from './corpus.ts';
/** Immutable dimensional metadata; no complete graph arrays are included. */
export type CorpusMetadata = { seed: number; size: CorpusSize; vertices: number; edges: number; findings: number };
/** Internal experiment request, separate from any future product IPC schema. */
export type CorpusRequest = { requestId: number; type: 'initialize' | 'project' | 'feature'; size?: CorpusSize; vertexLimit?: number; edgeLimit?: number; group?: number };
/** Bounded view and source dimensions returned by the worker. */
export type CorpusReply = { requestId: number; view: ReturnType<typeof visibleProjection>; metadata: CorpusMetadata; generationMs: number; projectionMs: number };
/**
 * Retain one full synthetic corpus on the worker side.
 * @returns A handler that returns only bounded projection data and dimensions.
 * @throws {Error} Handler rejects invalid requests or project-before-initialize.
 */
export function createCorpusService() {
  let corpus: Corpus | undefined;
  let generationMs = 0;
  return (request: CorpusRequest): CorpusReply => {
    if (!Number.isSafeInteger(request.requestId) || request.requestId < 1) throw new Error('Positive request identity required');
    if (request.type === 'initialize') {
      if (!request.size || !['S', 'M', 'L'].includes(request.size)) throw new Error('Known corpus size required');
      const started = performance.now(); corpus = createCorpus(request.size); generationMs = performance.now() - started;
    }
    if (!corpus) throw new Error('Initialize the worker corpus first');
    const started = performance.now();
    const vertices = request.vertexLimit ?? 2000; const edges = request.edgeLimit ?? 8000;
    if (!Number.isInteger(vertices) || vertices < 0 || vertices > 5000 || !Number.isInteger(edges) || edges < 0 || edges > 20000) throw new Error('Bounded projection counts required');
    if (request.group !== undefined && (!Number.isInteger(request.group) || request.group < 0 || request.group > 9)) throw new Error('Known group required');
    let view;
    if (request.type === 'feature') view = { nodes: corpus.nodes.slice(0, 2), edges: corpus.edges.slice(0, 4), hiddenVertices: corpus.nodes.length - 2, hiddenEdges: corpus.edges.length - 4 };
    else if (request.type === 'initialize' || request.type === 'project') view = visibleProjection(corpus, vertices, edges, request.group);
    else throw new Error('Known corpus operation required');
    return { requestId: request.requestId, view, metadata: { seed: corpus.seed, size: corpus.size, vertices: corpus.nodes.length, edges: corpus.edges.length, findings: corpus.findings }, generationMs, projectionMs: performance.now() - started };
  };
}
