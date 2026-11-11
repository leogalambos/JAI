import { describe, expect, it } from 'vitest';
import fixture from './fixtures/projection.json' with { type: 'json' };
import { assertBinding, assertCancellationTarget, assertRequest, assertResponse, assertResponseForRequest, decodeBytePage, decodeRequestFrame, decodeResponseFrame, encodeFrame, queryKey } from '../src/consumer.js';
import type { Request, Response } from '../src/protocol.js';
import { PROTOCOL } from '../src/protocol.js';
import { LIMITS } from '../src/model.js';

const binding = { sessionId: 'synthetic-session', capability: 'opaque-capability', generation: '1' };
const filter = { projectIds: [], families: [], findingStates: [], relations: [] };
const request = (operation: string, payload: unknown): Request => ({ protocol: PROTOCOL, kind: 'request', requestId: 'query-one', binding, operation, payload }) as Request;
const response = (input: Request, payload: unknown): Response => ({ protocol: PROTOCOL, kind: 'response', requestId: input.requestId, binding: input.binding, operation: input.operation, status: 'ok', payload }) as Response;

describe('read-only versioned consumer protocol', () => {
  it('accepts actual closed request/response contracts for every maintained operation', () => {
    const identity = fixture.vertices[0]!.identity;
    const limits = { maxVertices: 5000, maxEdges: 20000, maxVisitedVertices: 10000, maxScannedEdges: 50000, maxHops: 32 };
    const cases: [string, unknown, unknown][] = [
      ['roots.pick', { families: ['fabric'] }, { capability: 'new-capability', sources: [{ projectId: 'synthetic-project-A', rootId: 'synthetic-root', sourceId: 'synthetic-fabric', family: 'fabric', relativePath: 'fabric.jsonl', readHandle: 'opaque-read' }] }],
      ['roots.close', {}, { closed: true }],
      ['snapshot.import', { sourceIds: ['synthetic-fabric'] }, { snapshot: fixture.snapshot }],
      ['snapshot.refresh', {}, { snapshot: { ...fixture.snapshot, generation: '2' } }],
      ['request.cancel', { targetRequestId: 'another-request' }, { targetRequestId: 'another-request', acknowledgement: 'not-active' }],
      ['element.lookup', { identity }, { vertex: null }],
      ['search.page', { text: '', filter, order: 'identity', limit: 5000, cursor: null }, { items: [], hidden: '0', complete: true, nextCursor: null }],
      ['graph.counts', { filter }, fixture.snapshot.counts],
      ['graph.neighbours', { identity, direction: 'both', relations: ['other-reference'], causalOnly: false, limits }, { projection: fixture }],
      ['graph.path', { from: identity, to: fixture.vertices[1]!.identity, direction: 'forward', relations: ['other-reference'], causalOnly: false, limits }, { projection: fixture, complete: true, found: true }],
      ['element.details', { identity }, { identity, attributes: fixture.vertices[0]!.attributes }],
      ['source.page', { sourceId: 'synthetic-fabric', pointer: '', sequence: null, offset: '0', length: 1 }, { sourceId: 'synthetic-fabric', pointer: '', sequence: null, offset: '0', byteLength: 0, bytesBase64: '', eof: true }],
    ];
    for (const [operation, payload, result] of cases) {
      let input = request(operation, payload);
      if (operation === 'roots.pick') input = { ...input, binding: { ...binding, capability: null, generation: null } };
      if (operation === 'snapshot.import') input = { ...input, binding: { ...binding, generation: null } };
      const output = response(input, result);
      expect(() => assertRequest(input), operation).not.toThrow();
      expect(() => assertResponseForRequest(output, input, input.binding), operation).not.toThrow();
      expect(() => assertResponse({ ...output, payload: { unboundedUnknownPayload: true } }), operation).toThrow();
    }
  });

  it('round trips a real operation-specific frame and rejects writes/versions/extra authority fields', () => {
    const input = request('element.lookup', { identity: fixture.vertices[0]!.identity });
    assertRequest(input);
    expect(decodeRequestFrame(encodeFrame(input))).toEqual(input);
    for (const operation of ['note.add', 'approval.grant', 'shell', 'source.write']) expect(() => assertRequest({ ...input, operation })).toThrow();
    expect(() => assertRequest({ ...input, protocol: 'jai.fabric-explorer.consumer/2' })).toThrow();
    expect(() => decodeRequestFrame(JSON.stringify({ ...input, payload: { ...input.payload, authorityGranted: true } }))).toThrow();
  });

  it('requires picker admission without accepting paths or a fabricated existing capability', () => {
    const pick = { ...request('roots.pick', { families: ['fabric', 'findings'] }), binding: { ...binding, capability: null, generation: null } };
    expect(() => assertRequest(pick)).not.toThrow();
    expect(() => assertRequest({ ...pick, payload: { families: ['fabric'], path: '/private/source' } })).toThrow();
    expect(() => assertRequest({ ...pick, binding })).toThrow();
    expect(() => assertRequest({ ...request('graph.counts', { filter }), binding: { ...binding, generation: null } })).toThrow();
  });

  it('rejects ambiguous source IDs returned by one native picker admission', () => {
    const pick = { ...request('roots.pick', { families: ['fabric'] }), binding: { ...binding, capability: null, generation: null } };
    const source = { projectId: 'one', rootId: 'one', sourceId: 'ambiguous', family: 'fabric', relativePath: 'fabric.jsonl', readHandle: 'one' };
    expect(() => assertResponse(response(pick, { capability: 'admitted', sources: [source, { ...source, projectId: 'two', rootId: 'two', readHandle: 'two' }] }))).toThrow();
  });

  it('correlates admitted picker source families with the retained request', () => {
    const pick = { ...request('roots.pick', { families: ['fabric'] }), binding: { ...binding, capability: null, generation: null } };
    const source = { projectId: 'project', rootId: 'root', sourceId: 'source', family: 'findings', relativePath: 'findings.jsonl', readHandle: 'opaque' };
    expect(() => assertResponseForRequest(response(pick, { capability: 'admitted', sources: [source] }), pick, pick.binding)).toThrow();
  });

  it('does not publish an import that omitted a selected source ID', () => {
    const input = { ...request('snapshot.import', { sourceIds: ['selected-source'] }), binding: { ...binding, generation: null } };
    expect(() => assertResponseForRequest(response(input, { snapshot: fixture.snapshot }), input, input.binding)).toThrow();
  });

  it('rejects stale/misdirected replies before publishing, even if they echo their old request', () => {
    const input = request('element.lookup', { identity: fixture.vertices[0]!.identity });
    const output = response(input, { vertex: fixture.vertices[0] });
    assertResponse(output); assertResponseForRequest(output, input, binding);
    expect(decodeResponseFrame(encodeFrame(output))).toEqual(output);
    expect(() => assertResponseForRequest(output, input, { ...binding, generation: '2' })).toThrow();
    expect(() => assertBinding(binding, { ...binding, sessionId: 'another' })).toThrow();
    expect(() => assertBinding(binding, { ...binding, capability: 'another' })).toThrow();
    expect(() => assertResponseForRequest(response(input, { vertex: fixture.vertices[1] }), input, binding)).toThrow();
  });

  it('echoes the original generation while admitting a newer candidate inside a snapshot result', () => {
    const input = request('snapshot.refresh', {});
    const output = response(input, { snapshot: { ...fixture.snapshot, generation: '2' } });
    expect(() => assertResponseForRequest(output, input, binding)).not.toThrow();
    expect(() => assertResponse(response(input, { snapshot: fixture.snapshot }))).toThrow();
    expect(() => assertResponse({ ...output, binding: { ...binding, generation: '2' } })).toThrow();
  });

  it('binds cursors to query/filter/order/session and preserves opaque source strings', () => {
    const input = request('search.page', { text: 'café', filter, order: 'identity', limit: 2, cursor: null }) as Extract<Request, { operation: 'search.page' }>;
    const next = { binding, operation: 'search.page', queryKey: queryKey(input), offset: '1', token: 'opaque-server-cursor' };
    const output = response(input, { items: [fixture.vertices[0]], hidden: '100', complete: false, nextCursor: next });
    expect(() => assertResponseForRequest(output, input, binding)).not.toThrow();
    const continued = { ...input, payload: { ...input.payload, cursor: next } };
    expect(() => assertRequest(continued)).not.toThrow();
    expect(() => assertRequest({ ...continued, payload: { ...continued.payload, text: 'cafe\u0301' } })).toThrow();
    expect(() => assertRequest({ ...continued, binding: { ...binding, generation: '2' } })).toThrow();
    expect(() => assertResponseForRequest(response(input, { items: [], hidden: '1', complete: false, nextCursor: next }), input, binding)).toThrow();
  });

  it('binds cancellation to the retained target and does not treat acknowledgement as quiescence', () => {
    const target = request('graph.counts', { filter });
    const cancel = { ...request('request.cancel', { targetRequestId: target.requestId }), requestId: 'cancel-one' };
    expect(() => assertCancellationTarget(cancel, target)).not.toThrow();
    expect(() => assertCancellationTarget(cancel, { ...target, binding: { ...binding, generation: '2' } })).toThrow();
    expect(() => assertRequest({ ...cancel, requestId: target.requestId })).toThrow();
    expect(() => assertResponseForRequest(response(cancel, { targetRequestId: target.requestId, acknowledgement: 'accepted' }), cancel, binding)).not.toThrow();
  });

  it('enforces traversal work limits and never claims no path after exhaustion', () => {
    const limits = { maxVertices: 5000, maxEdges: 20000, maxVisitedVertices: 10000, maxScannedEdges: 50000, maxHops: 32 };
    const input = request('graph.path', { from: fixture.vertices[0]!.identity, to: fixture.vertices[1]!.identity, direction: 'forward', relations: ['other-reference'], causalOnly: false, limits });
    expect(() => assertRequest(input)).not.toThrow();
    expect(() => assertRequest({ ...input, payload: { ...input.payload, limits: { ...limits, maxHops: 33 } } })).toThrow();
    const incomplete = { ...fixture, complete: false, omissions: ['work-limit'] };
    expect(() => assertResponse(response(input, { projection: incomplete, complete: false, found: null }))).not.toThrow();
    expect(() => assertResponse(response(input, { projection: incomplete, complete: false, found: false }))).toThrow();
  });

  it('preserves exact raw bytes, bounds pages at256KiB and rejects nonprogress/mismatched ranges', () => {
    const bytes = new Uint8Array([0, 13, 10, 255]);
    const page = { sourceId: 'synthetic-fabric', pointer: '/record', sequence: '1', offset: '0', byteLength: bytes.length, bytesBase64: btoa(String.fromCharCode(...bytes)), eof: false };
    expect(decodeBytePage(page)).toEqual(bytes);
    const input = request('source.page', { sourceId: page.sourceId, pointer: page.pointer, sequence: page.sequence, offset: page.offset, length: LIMITS.rawPageBytes });
    expect(() => assertResponseForRequest(response(input, page), input, binding)).not.toThrow();
    const boundary = { ...page, byteLength: LIMITS.rawPageBytes, bytesBase64: 'AA=='.replace('AA==', btoa('\0'.repeat(LIMITS.rawPageBytes))), eof: true };
    expect(decodeBytePage(boundary)).toHaveLength(LIMITS.rawPageBytes);
    expect(() => assertRequest({ ...input, payload: { ...input.payload, length: LIMITS.rawPageBytes + 1 } })).toThrow();
    expect(() => decodeBytePage({ ...page, bytesBase64: 'AA== ' })).toThrow();
    expect(() => decodeBytePage({ ...page, bytesBase64: '', byteLength: 0 })).toThrow();
    expect(() => assertResponseForRequest(response(input, { ...page, offset: '1' }), input, binding)).toThrow();
  });
});
