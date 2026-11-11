// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Named bridge methods retain exact request correlation across asynchronous replies. */
import { describe, expect, it } from 'vitest';
import { decodeRequestFrame, encodeFrame } from '@jai/fabric-explorer-contracts';
import type { Response } from '@jai/fabric-explorer-contracts';
import { CHANNELS, createBridge } from '../src/shell/bridge.js';

describe('import preload methods', () => {
  it('exposes immutable named operations and forwards only bounded consumer frames', async () => {
    const operations: string[] = [];
    const api = createBridge({ invoke: async (channel, value) => {
      expect(channel).toBe(CHANNELS.request); const request = decodeRequestFrame(value as string); operations.push(request.operation);
      return encodeFrame({ protocol: request.protocol, requestId: request.requestId, operation: request.operation, binding: request.binding, kind: 'response', status: 'error', error: { code: 'cancelled', message: 'Fixture cancellation.', source: null, severity: 'error' } } as Response);
    } });
    expect(Object.isFrozen(api)).toBe(true);
    expect(Object.keys(api).sort()).toEqual(['cancelRequest', 'cancelSelection', 'closeRoots', 'counts', 'details', 'dropQuery', 'filterProjection', 'getState', 'groups', 'importSnapshot', 'layout', 'lookup', 'neighbours', 'pageSource', 'path', 'pickRoots', 'refreshSnapshot', 'search', 'searchFindings', 'updatePreferences']);
    await api.importSnapshot({ sessionId: 'session', capability: 'cap', generation: null }, 'import', ['source']);
    await api.refreshSnapshot({ sessionId: 'session', capability: 'cap', generation: '1' }, 'refresh');
    await api.pageSource({ sessionId: 'session', capability: 'cap', generation: '1' }, 'page', { sourceId: 'source', pointer: '', sequence: null, offset: '0', length: 3 });
    expect(operations).toEqual(['snapshot.import', 'snapshot.refresh', 'source.page']);
  });
  it('rejects a well-shaped page belonging to a different requested source', async () => {
    const api = createBridge({ invoke: async (_channel, value) => {
      const request = decodeRequestFrame(value as string);
      return encodeFrame({ ...request, kind: 'response', operation: 'source.page', status: 'ok', payload: { sourceId: 'other', pointer: '', sequence: null, offset: '0', byteLength: 3, bytesBase64: 'YWJj', eof: true } } as Response);
    } });
    await expect(api.pageSource({ sessionId: 'session', capability: 'cap', generation: '1' }, 'page', { sourceId: 'source', pointer: '', sequence: null, offset: '0', length: 3 })).rejects.toThrow();
    await expect(api.importSnapshot({ sessionId: 'session', capability: null, generation: null }, 'bad', ['source'])).rejects.toThrow();
  });
});

it('discards and drops filtered projection output delivered across a controlled generation replacement', async () => {
  const binding = { sessionId: 'session', capability: 'capability', generation: '1' };
  const calls: unknown[] = [];
  const result = { binding, requestId: 'filter', baseProjectionToken: 'base', projectionToken: 'filtered', handles: [], vertexMask: 'AA==', edgeMask: '', hiddenVertices: '1', hiddenEdges: '0', complete: true, omissions: ['filter'] };
  const api = createBridge({ invoke: async (channel, value) => {
    if (channel === CHANNELS.filterProjection) return result;
    if (channel === CHANNELS.state) return { sessionId: binding.sessionId, capability: binding.capability, snapshot: { generation: '2' } };
    if (channel === CHANNELS.queryDrop) { calls.push(value); return; }
    throw new Error('Unexpected channel');
  } });
  await expect(api.filterProjection(binding, 'filter', 'base', { projectIds: [], families: [], findingStates: [], relations: [] })).rejects.toThrow();
  expect(calls).toEqual([{ binding, requestId: 'filter', continuationToken: null, projectionToken: 'filtered' }]);
});
