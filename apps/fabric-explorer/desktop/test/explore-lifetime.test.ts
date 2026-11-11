// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Controlled late-delivery regression: cancellation releases staged tokens without stopping accepted work. */
import { expect, it } from 'vitest';
import { PROTOCOL } from '@jai/fabric-explorer-contracts';
import { ImportModel } from '../src/import/model.js';
import type { ModelInput } from '../src/import/model.js';
import { ImportSession } from '../src/import/session.js';
import type { ImportWorkerPort } from '../src/import/worker-client.js';
import { ExploreService } from '../src/explore/service.js';
import type { QueryDrop } from '../src/explore/types.js';
import { QueryIndex, DEFAULT_QUERY_LIMITS, DEFAULT_RELATIONS } from '../src/graph/query-index.js';
import type { GraphRequest } from '../src/graph/types.js';
import { lease, revision, ref } from './import-fixtures.js';
it('releases every successful late cancelled query page and preserves accepted worker capacity', async () => {
  let model!: ImportModel; let input!: ModelInput; let service!: ExploreService; let stopped = false;
  const drops: QueryDrop[] = []; let enter!: () => void; let release!: () => void;
  let gate: Promise<void>;
  let lateFilter = false;
  const worker: ImportWorkerPort = {
    initialize: async value => { input = value; model = new ImportModel(value); }, consume: async value => model.consume(value),
    finish: async () => { const ready = model.finish(); const binding = { ...input.binding, generation: ready.descriptor.generation }; service = new ExploreService(new QueryIndex({ snapshot: ready.descriptor, records: model.records() }, binding), binding); return ready; },
    span: async () => null,
    queryStart: async request => { const page = service.start(request); enter(); await gate; return page; },
    filterProjection: async selection => { const view = service.filterProjection(selection); if (lateFilter) { enter(); await gate; } return view; },
    queryDrop: async drop => { drops.push(drop); service.drop(drop); },
    terminate: async () => { stopped = true; service.dispose(); },
  };
  const source = revision(); const session = new ImportSession({ sessionId: 'session', capability: 'capability', sources: [{ projectId: source.projectId, rootId: source.rootId, sourceId: source.sourceId, family: source.family, relativePath: source.relativePath, readHandle: 'read' }], broker: { capture: async () => lease() }, workerFactory: () => worker });
  const binding = { sessionId: 'session', capability: 'capability', generation: '1' };
  try {
    await session.import(['fabric'], null);
    for (let i = 0; i < 9; i++) {
      gate = new Promise<void>(resolve => { release = resolve; }); const entered = new Promise<void>(resolve => { enter = resolve; });
      const request: GraphRequest = { protocol: PROTOCOL, kind: 'request', requestId: `late-${i}`, binding, operation: 'graph.neighbours', payload: { identity: { kind: 'version', projectId: 'project', ref }, direction: 'both', relations: DEFAULT_RELATIONS, causalOnly: false, limits: DEFAULT_QUERY_LIMITS } };
      const abort = new AbortController(); const work = session.queryStart(request, abort.signal); const rejected = expect(work).rejects.toMatchObject({ code: 'cancelled' });
      await entered; abort.abort(); release(); await rejected;
      expect(drops).toHaveLength(i + 1); expect(drops[i]).toMatchObject({ binding, requestId: request.requestId, continuationToken: null, projectionToken: expect.any(String) });
      expect(stopped).toBe(false);
    }
    const baseRequest: GraphRequest = { protocol: PROTOCOL, kind: 'request', requestId: 'base', binding, operation: 'graph.neighbours', payload: { identity: { kind: 'version', projectId: 'project', ref }, direction: 'both', relations: DEFAULT_RELATIONS, causalOnly: false, limits: DEFAULT_QUERY_LIMITS } };
    const base = service.start(baseRequest); lateFilter = true;
    for (let i = 0; i < 9; i++) {
      gate = new Promise<void>(resolve => { release = resolve; }); const entered = new Promise<void>(resolve => { enter = resolve; });
      const abort = new AbortController();
      const work = session.filterProjection({ binding, requestId: `filter-${i}`, baseProjectionToken: base.projectionToken!, filter: { projectIds: [], families: [], findingStates: [], relations: [] } }, abort.signal);
      const rejected = expect(work).rejects.toMatchObject({ code: 'cancelled' }); await entered; abort.abort(); release(); await rejected;
      expect(drops).toHaveLength(10 + i); expect(drops.at(-1)).toMatchObject({ requestId: `filter-${i}`, continuationToken: null, projectionToken: expect.any(String) });
    }
  } finally { await session.dispose(); }
});
