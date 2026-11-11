// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Import controller binding and ownership tests use the owned importer port. */
import { describe, expect, it, vi } from 'vitest';
import { PROTOCOL, decodeResponseFrame, encodeFrame } from '@jai/fabric-explorer-contracts';
import type { Request, SnapshotDescriptor } from '@jai/fabric-explorer-contracts';
import { ShellController } from '../src/shell/controller.js';
import type { ImportSessionFactory } from '../src/shell/controller.js';
import type { ImportState } from '../src/import/types.js';
import { ImportError } from '../src/import/types.js';
import { DEFAULT_PREFERENCES } from '../src/shell/preferences.js';
import type { PreferenceStore } from '../src/shell/preferences.js';

function fixture(factoryFailure = false) {
  let state: ImportState = { snapshot: null, report: null, stale: false };
  let failRefresh = false;
  const dispose = vi.fn(async () => {}); const close = vi.fn(async () => {});
  const page = vi.fn(async (payload: { sourceId: string; pointer: string; sequence: string | null; offset: string; length: number }, generation: string) => {
    expect(generation).toBe(state.snapshot?.generation);
    return { sourceId: payload.sourceId, pointer: payload.pointer, sequence: payload.sequence, offset: payload.offset, byteLength: 3, bytesBase64: 'YWJj', eof: true };
  });
  const createImport: ImportSessionFactory = input => {
    if (factoryFailure) throw new Error('Owned worker unavailable');
    const advance = () => {
      const snapshot: SnapshotDescriptor = {
        format: 'jai.fabric-explorer.snapshot/1', sessionId: input.sessionId,
        generation: String(BigInt(state.snapshot?.generation ?? '0') + 1n),
        sources: [{ projectId: 'project', rootId: 'root', sourceId: 'source', family: 'fabric', relativePath: 'data.jsonl', revisionId: 'revision', adapterVersion: 'test/1', digest: 'a'.repeat(64), byteLength: '3', head: null, sequence: null, observedAt: '2026-11-10T00:00:00Z', verification: { mode: 'canonical', decoded: 'decoded', chain: 'verified', replay: 'verified', publicTrust: 'not-required', material: 'not-observed', recordedApplicability: null, authorityGranted: false, freshAssessment: false } }],
        counts: { vertices: '0', edges: '0', findings: '0' }, authorityGranted: false, freshAssessment: false,
      };
      state = { snapshot, report: null, stale: false }; return snapshot;
    };
    return {
      state: () => state, dispose,
      import: async (ids, expected) => { expect(ids).toEqual(['source']); expect(expected).toBe(state.snapshot?.generation ?? null); return advance(); },
      refresh: async expected => { expect(expected).toBe(state.snapshot?.generation); if (failRefresh) { state = { ...state, stale: true }; throw new ImportError('incompatible-source', 'Fixture import rejected.'); } return advance(); },
      sourcePage: page,
    };
  };
  const store = { load: () => ({ preferences: DEFAULT_PREFERENCES, warning: null }) } as unknown as PreferenceStore;
  const controller = new ShellController({ open: async () => ({ capability: 'cap', sources: [{ projectId: 'project', rootId: 'root', sourceId: 'source', family: 'fabric', relativePath: 'data.jsonl', readHandle: 'read' }] }), close, disposeSession: async () => {} }, { project: async () => '/project', files: async () => ['/source/data.jsonl'] }, store, createImport);
  const request = (operation: Request['operation'], requestId: string, payload: unknown = {}, generation: string | null = controller.state().snapshot?.generation ?? null) => encodeFrame({ protocol: PROTOCOL, kind: 'request', operation, requestId, binding: { sessionId: controller.sessionId, capability: operation === 'roots.pick' ? null : controller.state().capability, generation }, payload } as Request);
  const open = () => controller.request(request('roots.pick', 'open', { families: ['fabric'] }));
  return { controller, request, open, dispose, close, page, fail: () => { failRefresh = true; } };
}

describe('import controller composition', () => {
  it('publishes import and refresh replies against their retained prior generation', async () => {
    const f = fixture(); await f.open();
    const imported = decodeResponseFrame(await f.controller.request(f.request('snapshot.import', 'import', { sourceIds: ['source'] })));
    expect(imported.status).toBe('ok'); expect(imported.binding.generation).toBeNull();
    expect(f.controller.state().snapshot?.generation).toBe('1');
    const refreshed = decodeResponseFrame(await f.controller.request(f.request('snapshot.refresh', 'refresh')));
    expect(refreshed.status).toBe('ok'); expect(refreshed.binding.generation).toBe('1'); expect(f.controller.state().snapshot?.generation).toBe('2');
    await expect(f.controller.request(f.request('snapshot.refresh', 'stale', {}, '1'))).rejects.toThrow('context');
    const detached = f.controller.state(); (detached.snapshot as { generation: string }).generation = '99'; expect(f.controller.state().snapshot?.generation).toBe('2');
  });
  it('keeps the published snapshot after a failed refresh and routes only bound captured pages', async () => {
    const f = fixture(); await f.open(); await f.controller.request(f.request('snapshot.import', 'import', { sourceIds: ['source'] }));
    f.fail(); const failed = decodeResponseFrame(await f.controller.request(f.request('snapshot.refresh', 'failed')));
    expect(failed.status).toBe('error'); expect(f.controller.state().snapshot?.generation).toBe('1'); expect(f.controller.state().stale).toBe(true);
    const response = decodeResponseFrame(await f.controller.request(f.request('source.page', 'page', { sourceId: 'source', pointer: '/0', sequence: '1', offset: '0', length: 3 })));
    expect(response.status).toBe('ok'); expect(f.page).toHaveBeenCalledOnce();
    await f.controller.request(f.request('roots.close', 'close')); expect(f.dispose).toHaveBeenCalledOnce(); expect(f.close).toHaveBeenCalledOnce(); expect(f.controller.state().snapshot).toBeNull();
  });
  it('releases admission when importer construction fails and never publishes a partial root', async () => {
    const f = fixture(true); expect(decodeResponseFrame(await f.open()).status).toBe('error');
    expect(f.close).toHaveBeenCalledOnce(); expect(f.controller.state().capability).toBeNull();
  });
});
