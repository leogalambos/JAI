import { ContractError } from './errors.js';
import { assertBinding, assertRequest, queryKey } from './consumer.js';
import { LIMITS } from './model.js';
import { PROTOCOL } from './protocol.js';
import type { Binding, ChunkOperation, ChunkState, Request, ResponseChunk } from './protocol.js';
import { assertShape } from './schema-validation.js';
import { assertEdge, assertSnapshot, assertVertex } from './validation.js';
import { encodeWire, parseWire } from './wire.js';

function chunkOperation(operation: string): operation is ChunkOperation { return ['search.page', 'graph.neighbours', 'graph.path'].includes(operation); }

/**
 * Validate one query-result chunk without pretending that its partial graph is publishable.
 * @param value One operation-specific chunk; complete endpoints are checked only after assembly.
 * @returns Nothing for valid records, bindings and terminal metadata.
 * @throws {ContractError} For invalid records, empty nonterminal progress or inconsistent terminal claims.
 */
export function assertResponseChunk(value: unknown): asserts value is ResponseChunk {
  assertShape('responseChunk', value); const chunk = value as ResponseChunk;
  if (chunk.binding.capability === null || chunk.binding.generation === null) throw new ContractError('invalid-message', 'Query chunks require a bound snapshot');
  chunk.vertices.forEach(assertVertex); chunk.edges.forEach(assertEdge);
  if (new Set(chunk.vertices.map(item => item.id)).size !== chunk.vertices.length || new Set(chunk.edges.map(item => item.id)).size !== chunk.edges.length) throw new ContractError('invalid-message', 'Chunk repeats a local element identity');
  if (chunk.terminal === null && chunk.vertices.length + chunk.edges.length === 0) throw new ContractError('invalid-message', 'Nonterminal chunks must make bounded progress');
  if (chunk.operation === 'search.page') {
    if (chunk.edges.length) throw new ContractError('invalid-message', 'Search chunks cannot carry edges');
    if (chunk.terminal?.nextCursor) {
      if (chunk.terminal.complete) throw new ContractError('invalid-message', 'Complete search cannot return another cursor');
      assertBinding(chunk.terminal.nextCursor.binding, chunk.binding);
    }
  } else if (chunk.terminal !== null) {
    const terminal = chunk.terminal; assertSnapshot(terminal.snapshot);
    if (terminal.snapshot.sessionId !== chunk.binding.sessionId || terminal.snapshot.generation !== chunk.binding.generation) throw new ContractError('stale-generation', 'Chunk terminal belongs to another snapshot');
    if ((terminal.complete && terminal.omissions.some(reason => reason !== 'filter')) || (!terminal.complete && terminal.omissions.length === 0)) throw new ContractError('invalid-message', 'Chunk terminal completeness is inconsistent');
    if (chunk.operation === 'graph.path' && ((!chunk.terminal.complete && chunk.terminal.found === false) || (chunk.terminal.complete && chunk.terminal.found === null))) throw new ContractError('invalid-message', 'Incomplete path stream cannot assert absence');
  }
}

/**
 * Start receiver-owned progress for a supported retained query request.
 * @param request Original validated request, retained independently of peer replies.
 * @returns Frozen zero-based state with no records or authority grant.
 * @throws {ContractError} For an invalid request or an operation without chunked results.
 */
export function startChunks(request: Request): ChunkState {
  assertRequest(request);
  if (!chunkOperation(request.operation)) throw new ContractError('unknown-operation', 'This operation has no chunked result');
  return Object.freeze({ requestId: request.requestId, operation: request.operation, binding: Object.freeze({ ...request.binding }), nextSequence: '0', vertices: 0, edges: 0, ended: false });
}

/**
 * Enforce contiguous finite delivery before an owning consumer stages records.
 * @param state Receiver-owned state from startChunks or the preceding successful transition.
 * @param value Next validated or untrusted chunk; this method never assembles/publishes its graph.
 * @param request Original retained query request.
 * @param current Trusted current session/capability/generation at reception time.
 * @returns New frozen progress with bounded cumulative counts and terminal status.
 * @throws {ContractError} For stale/cross-request data, duplicate/out-of-order/postterminal delivery or excess results.
 */
export function advanceChunks(state: ChunkState, value: unknown, request: Request, current: Binding): ChunkState {
  assertRequest(request); assertResponseChunk(value); const chunk = value;
  assertBinding(request.binding, current); assertBinding(chunk.binding, current); assertBinding(state.binding, current);
  if (state.ended || state.requestId !== request.requestId || chunk.requestId !== request.requestId || state.operation !== request.operation || chunk.operation !== request.operation || chunk.sequence !== state.nextSequence) throw new ContractError('invalid-message', 'Chunk sequence/request/terminal state mismatch');
  const vertices = state.vertices + chunk.vertices.length; const edges = state.edges + chunk.edges.length;
  const vertexLimit = request.operation === 'search.page' ? request.payload.limit : request.operation === 'graph.neighbours' || request.operation === 'graph.path' ? request.payload.limits.maxVertices : 0;
  const edgeLimit = request.operation === 'search.page' ? 0 : request.operation === 'graph.neighbours' || request.operation === 'graph.path' ? request.payload.limits.maxEdges : 0;
  if (!Number.isSafeInteger(vertices) || !Number.isSafeInteger(edges) || vertices > vertexLimit || edges > edgeLimit || vertices > LIMITS.visibleVertices || edges > LIMITS.visibleEdges) throw new ContractError('resource-limit', 'Chunked result exceeds cumulative requested bounds');
  if (chunk.operation === 'search.page' && request.operation === 'search.page' && chunk.terminal?.nextCursor) {
    const cursor = chunk.terminal.nextCursor;
    if (vertices === 0 || cursor.queryKey !== queryKey(request) || BigInt(cursor.offset) !== BigInt(request.payload.cursor?.offset ?? '0') + BigInt(vertices)) throw new ContractError('cursor-mismatch', 'Stream terminal cursor does not match its query/progress');
  }
  if (chunk.operation !== 'search.page' && chunk.terminal && (BigInt(chunk.terminal.snapshot.counts.vertices) < BigInt(vertices) || BigInt(chunk.terminal.snapshot.counts.edges) < BigInt(edges))) throw new ContractError('invalid-message', 'Stream exceeds its final indexed graph counts');
  const next = Number(state.nextSequence) + 1;
  if (!Number.isSafeInteger(next) || next > LIMITS.visibleVertices + LIMITS.visibleEdges + 1) throw new ContractError('resource-limit', 'Chunk sequence exceeds finite result bounds');
  return Object.freeze({ ...state, nextSequence: String(next), vertices, edges, ended: chunk.terminal !== null });
}

/**
 * Encode one chunk while retaining the ordinary 8 MiB physical-frame limit.
 * @param value Structurally consistent query chunk.
 * @returns Bounded JSON frame; oversized logical results require additional smaller chunks.
 * @throws {ContractError} For invalid chunks or frame budget exhaustion.
 */
export function encodeChunkFrame(value: ResponseChunk): string { assertResponseChunk(value); return encodeWire(value); }

/**
 * Decode one bounded query chunk without updating any snapshot or stream state.
 * @param text Raw transport JSON, never canonical source JSON.
 * @returns Validated chunk; advanceChunks still binds it to retained receiver state.
 * @throws {ContractError} For invalid wire data, versions, operations or chunk fields.
 */
export function decodeChunkFrame(text: string): ResponseChunk {
  const value = parseWire(text);
  if ((value as { protocol?: unknown } | null)?.protocol !== PROTOCOL) throw new ContractError('unsupported-protocol', 'Unsupported consumer protocol version');
  assertResponseChunk(value); return value;
}
