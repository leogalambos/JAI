import { ContractError } from './errors.js';
import { elementKey } from './identity.js';
import type { Attributes, ElementIdentity } from './model.js';
import { LIMITS } from './model.js';
import { PROTOCOL } from './protocol.js';
import type { Binding, BytePage, Cursor, Operation, RejectionNotice, Request, Response } from './protocol.js';
import { assertShape } from './schema-validation.js';
import { assertProjection, assertSnapshot, assertVertex } from './validation.js';
import { assertSemantic } from './semantic.js';
import { encodeWire, parseWire } from './wire.js';

const operations: readonly Operation[] = ['roots.pick', 'roots.close', 'snapshot.import', 'snapshot.refresh', 'request.cancel', 'element.lookup', 'search.page', 'graph.counts', 'graph.neighbours', 'graph.path', 'element.details', 'source.page'];
const queryOperations: readonly Operation[] = ['snapshot.refresh', 'element.lookup', 'search.page', 'graph.counts', 'graph.neighbours', 'graph.path', 'element.details', 'source.page'];

function envelope(value: unknown): Record<string, unknown> {
  if (!value || typeof value !== 'object' || Array.isArray(value)) throw new ContractError('invalid-message', 'Consumer envelope must be an object');
  const result = value as Record<string, unknown>;
  if (result.protocol !== PROTOCOL) throw new ContractError('unsupported-protocol', 'Unsupported consumer protocol version');
  if (!operations.includes(result.operation as Operation)) throw new ContractError('unknown-operation', 'Operation is not in the read-only allowlist');
  return result;
}

function operationBinding(operation: Operation, binding: Binding): void {
  if (operation === 'roots.pick') {
    if (binding.capability !== null || binding.generation !== null) throw new ContractError('invalid-message', 'Root admission has no existing root capability/generation');
  } else {
    if (binding.capability === null) throw new ContractError('capability-mismatch', 'An admitted root capability is required');
    if (queryOperations.includes(operation) && binding.generation === null) throw new ContractError('stale-generation', 'Operation requires an existing snapshot generation');
  }
}

function searchKey(request: Extract<Request, { operation: 'search.page' }>): string {
  const query = request.payload; const filter = query.filter;
  return JSON.stringify(['jai.fabric-explorer.query/1', request.operation, query.text, [...filter.projectIds].sort(), [...filter.families].sort(), [...filter.findingStates].sort(), [...filter.relations].sort(), query.order, query.limit]);
}

function cursorFor(cursor: Cursor, request: Extract<Request, { operation: 'search.page' }>): void {
  assertBinding(cursor.binding, request.binding);
  if (cursor.operation !== request.operation || cursor.queryKey !== searchKey(request)) throw new ContractError('cursor-mismatch', 'Cursor belongs to another query');
}

function detailAttributes(attributes: Attributes, identity: ElementIdentity): void {
  if (attributes.kind === 'inline') {
    const findingDomain = identity.kind === 'finding' || (identity.kind === 'location' && identity.origin.family === 'findings');
    assertSemantic(attributes.value, findingDomain ? 'findings' : 'lifecycle');
  } else if (BigInt(attributes.byteLength) > 100n * 1024n * 1024n) throw new ContractError('resource-limit', 'Decoded record limit exceeded');
}

/**
 * Validate operation-specific request shape and its locally checkable binding rules.
 * @param value Untrusted DTO; capability authenticity and source access remain broker-owned.
 * @returns Nothing for a closed, read-only request with consistent cursor/cancellation fields.
 * @throws {ContractError} For unsupported versions/operations, extra fields or inconsistent binding.
 */
export function assertRequest(value: unknown): asserts value is Request {
  envelope(value); assertShape('request', value);
  const request = value as Request;
  operationBinding(request.operation, request.binding);
  if (request.operation === 'request.cancel' && request.payload.targetRequestId === request.requestId) throw new ContractError('invalid-message', 'Cancellation cannot target itself');
  if (request.operation === 'search.page' && request.payload.cursor !== null) cursorFor(request.payload.cursor, request);
}

/**
 * Compare a message or cursor context to trusted currently active broker state.
 * @param actual Context from a validated or untrusted message.
 * @param expected Trusted active session/capability/generation; never supplied by the same message.
 * @returns Nothing when all three exact fields match.
 * @throws {ContractError} With session/capability/stale-generation category on mismatch.
 */
export function assertBinding(actual: Binding, expected: Binding): void {
  assertShape('binding', actual);
  if (actual.sessionId !== expected.sessionId) throw new ContractError('session-mismatch', 'Message belongs to another session');
  if (actual.capability !== expected.capability) throw new ContractError('capability-mismatch', 'Message belongs to another root capability');
  if (actual.generation !== expected.generation) throw new ContractError('stale-generation', 'Message belongs to another snapshot generation');
}

/**
 * Encode the identity of a viewer search without source hashing or string normalization.
 * @param request Closed search-page request; set filters are sorted without mutating the input.
 * @returns Deterministic query key excluding its current cursor/offset/token.
 * @throws {ContractError} For an invalid request shape or unsupported operation.
 */
export function queryKey(request: Extract<Request, { operation: 'search.page' }>): string {
  assertShape('request', request);
  if (request.operation !== 'search.page') throw new ContractError('unknown-operation', 'Only paginated search has this query key');
  return searchKey(request);
}

/**
 * Validate a bound response and operation-specific result, without authenticating source claims.
 * @param value Candidate read-only response with the original request binding.
 * @returns Nothing when result DTOs and local consistency rules hold.
 * @throws {ContractError} For invalid envelopes/results, false path absence or malformed exact bytes.
 */
export function assertResponse(value: unknown): asserts value is Response {
  envelope(value); assertShape('response', value);
  const response = value as Response;
  operationBinding(response.operation, response.binding);
  if (response.status === 'error') return;
  switch (response.operation) {
    case 'roots.pick':
      if (new Set(response.payload.sources.map(source => source.sourceId)).size !== response.payload.sources.length) throw new ContractError('invalid-message', 'Admitted source IDs must be unambiguous within the catalog');
      break;
    case 'snapshot.import': case 'snapshot.refresh': {
      const snapshot = response.payload.snapshot; assertSnapshot(snapshot);
      if (snapshot.sessionId !== response.binding.sessionId || (response.binding.generation !== null && BigInt(snapshot.generation) <= BigInt(response.binding.generation))) throw new ContractError('stale-generation', 'Candidate snapshot must advance the original session generation');
      break;
    }
    case 'element.lookup': if (response.payload.vertex !== null) assertVertex(response.payload.vertex); break;
    case 'search.page': {
      response.payload.items.forEach(assertVertex);
      if (new Set(response.payload.items.map(item => item.id)).size !== response.payload.items.length) throw new ContractError('invalid-message', 'Search page repeats an element identity');
      if (response.payload.nextCursor !== null) {
        if (response.payload.items.length === 0 || response.payload.complete) throw new ContractError('invalid-message', 'Search cursor must make progress and not follow a complete result');
        assertBinding(response.payload.nextCursor.binding, response.binding);
      }
      break;
    }
    case 'graph.neighbours': assertProjection(response.payload.projection); break;
    case 'graph.path':
      assertProjection(response.payload.projection);
      if (response.payload.complete !== response.payload.projection.complete || (!response.payload.complete && response.payload.found === false) || (response.payload.complete && response.payload.found === null)) throw new ContractError('invalid-message', 'Incomplete search cannot assert path absence');
      break;
    case 'element.details': elementKey(response.payload.identity); detailAttributes(response.payload.attributes, response.payload.identity); break;
    case 'source.page': decodeBytePage(response.payload); break;
  }
  if ((response.operation === 'graph.neighbours' || response.operation === 'graph.path') && (response.payload.projection.snapshot.sessionId !== response.binding.sessionId || response.payload.projection.snapshot.generation !== response.binding.generation)) throw new ContractError('stale-generation', 'Graph result snapshot differs from response binding');
}

/**
 * Reject stale/misdirected successes before a client publishes their result.
 * @param value Response from the peer.
 * @param request Original request retained by the receiver, not reconstructed from the response.
 * @param current Trusted active context at publication time.
 * @returns Nothing when request/response correlation and operation-specific echoes match current state.
 * @throws {ContractError} For stale context, wrong request/operation/query or wrong source/element reply.
 */
export function assertResponseForRequest(value: unknown, request: Request, current: Binding): asserts value is Response {
  assertRequest(request); assertResponse(value); const response = value;
  assertBinding(request.binding, current); assertBinding(response.binding, current);
  if (response.requestId !== request.requestId || response.operation !== request.operation) throw new ContractError('invalid-message', 'Response does not correlate with its retained request');
  if (response.status === 'error') return;
  if (request.operation === 'roots.pick' && response.operation === 'roots.pick' && response.payload.sources.some(source => !request.payload.families.includes(source.family))) throw new ContractError('invalid-message', 'Picker returned a source outside the requested families');
  if (request.operation === 'snapshot.import' && response.operation === 'snapshot.import') {
    const captured = new Set(response.payload.snapshot.sources.map(source => source.sourceId));
    if (request.payload.sourceIds.some(sourceId => !captured.has(sourceId))) throw new ContractError('invalid-message', 'Import omitted a selected admitted source');
  }
  if (request.operation === 'element.lookup' && response.operation === 'element.lookup' && response.payload.vertex !== null && response.payload.vertex.id !== elementKey(request.payload.identity)) throw new ContractError('invalid-message', 'Lookup returned another identity');
  if (request.operation === 'element.details' && response.operation === 'element.details' && elementKey(request.payload.identity) !== elementKey(response.payload.identity)) throw new ContractError('invalid-message', 'Details returned another identity');
  if (request.operation === 'request.cancel' && response.operation === 'request.cancel' && response.payload.targetRequestId !== request.payload.targetRequestId) throw new ContractError('invalid-message', 'Cancellation acknowledged another request');
  if (request.operation === 'source.page' && response.operation === 'source.page') {
    const page = response.payload; const wanted = request.payload;
    if (page.sourceId !== wanted.sourceId || page.pointer !== wanted.pointer || page.sequence !== wanted.sequence || page.offset !== wanted.offset || page.byteLength > wanted.length) throw new ContractError('invalid-message', 'Raw page does not match the requested source/range');
  }
  if (request.operation === 'search.page' && response.operation === 'search.page') {
    if (response.payload.items.length > request.payload.limit) throw new ContractError('resource-limit', 'Search page exceeds the requested result bound');
    const next = response.payload.nextCursor;
    if (next !== null) {
      cursorFor(next, request);
      const previousOffset = BigInt(request.payload.cursor?.offset ?? '0');
      if (BigInt(next.offset) !== previousOffset + BigInt(response.payload.items.length)) throw new ContractError('cursor-mismatch', 'Search cursor has an inconsistent next offset');
    }
  }
  if ((request.operation === 'graph.neighbours' || request.operation === 'graph.path') && (response.operation === 'graph.neighbours' || response.operation === 'graph.path')) {
    if (response.payload.projection.vertices.length > request.payload.limits.maxVertices || response.payload.projection.edges.length > request.payload.limits.maxEdges) throw new ContractError('resource-limit', 'Graph reply exceeds requested visible limits');
  }
}

/**
 * Bind cancellation to the exact active request rather than only its display ID.
 * @param cancellation Valid cancellation request from the current peer.
 * @param target Retained active target request from the receiver's request table.
 * @returns Nothing when target ID and session/capability/generation all match.
 * @throws {ContractError} For non-cancellation input or a different/self-targeted context.
 */
export function assertCancellationTarget(cancellation: Request, target: Request): void {
  assertRequest(cancellation); assertRequest(target);
  if (cancellation.operation !== 'request.cancel' || cancellation.payload.targetRequestId !== target.requestId) throw new ContractError('invalid-message', 'Cancellation does not address the active request');
  assertBinding(cancellation.binding, target.binding);
}

/**
 * Decode an exact bounded raw source page without text/newline normalization.
 * @param page Base64 page and its declared decoded length.
 * @returns New bytes exactly matching the page; no source hashing or execution occurs.
 * @throws {ContractError} For noncanonical base64, excess length or empty nonterminal pages.
 */
export function decodeBytePage(page: BytePage): Uint8Array {
  assertShape('bytePage', page);
  let decoded: string;
  try { decoded = atob(page.bytesBase64); } catch { throw new ContractError('invalid-message', 'Malformed base64 source page'); }
  if (btoa(decoded) !== page.bytesBase64 || decoded.length !== page.byteLength || decoded.length > LIMITS.rawPageBytes || (decoded.length === 0 && !page.eof)) throw new ContractError('invalid-message', 'Source page length/encoding/progress mismatch');
  return Uint8Array.from(decoded, character => character.charCodeAt(0));
}

/**
 * Validate and serialize one bounded consumer envelope without source canonicalization.
 * @param value Closed request/response/rejection DTO.
 * @returns UTF-8-budgeted JSON frame text; arbitrary-precision values remain tagged strings.
 * @throws {ContractError} For invalid structure, unsupported operations or wire resource exhaustion.
 */
export function encodeFrame(value: Request | Response | RejectionNotice): string {
  if (value.kind === 'request') assertRequest(value);
  else if (value.kind === 'response') assertResponse(value);
  else assertShape('rejection', value);
  return encodeWire(value);
}

/**
 * Parse one request frame after preflight byte/depth/duplicate-key enforcement.
 * @param text Raw JSON consumer frame, never raw canonical source JSON.
 * @returns Validated request DTO with no coercion/defaults or source interpretation.
 * @throws {ContractError} For syntax, bounds, unsupported versions/operations or invalid shape.
 */
export function decodeRequestFrame(text: string): Request {
  const value = parseWire(text); assertRequest(value); return value;
}

/**
 * Parse one response frame without publishing it or accepting stale generations.
 * @param text Raw JSON response frame.
 * @returns Structurally validated response; callers still use assertResponseForRequest before publication.
 * @throws {ContractError} For malformed/bounded wire input or invalid response structure.
 */
export function decodeResponseFrame(text: string): Response {
  const value = parseWire(text); assertResponse(value); return value;
}
