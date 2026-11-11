/** Source flow tests use owned bridge callbacks and explicit deferred phase barriers, without timers. */
import { expect, it, vi } from 'vitest';
import { openAndLoadSources } from '../src/renderer/source-flow.js';
import type { OpenSourcesOptions, SourceWork } from '../src/renderer/source-flow.js';
import type { ShellState } from '../src/shell/controller.js';
import { DEFAULT_PREFERENCES } from '../src/shell/preferences.js';

function fixture() {
  const initial: ShellState = { sessionId: 'initial-session', capability: null, sources: [], preferences: DEFAULT_PREFERENCES, warning: null, snapshot: null, report: null, stale: false };
  const admitted: ShellState = { ...initial, sessionId: 'fresh-session', capability: 'fresh-capability', sources: [{ projectId: 'p', rootId: 'r', sourceId: 'fresh-source', family: 'fabric', relativePath: 'project.jsonl', readHandle: 'opaque' }] };
  const api = { pickRoots: vi.fn(async () => ({ status: 'ok' })), importSnapshot: vi.fn(async () => ({ status: 'ok' })) };
  const abort = new AbortController(); const phases: SourceWork[] = [];
  const refresh = vi.fn(async () => admitted);
  const options: OpenSourcesOptions = { api, initial, families: ['fabric'], selectionId: 'select', importId: 'load', signal: abort.signal, refresh, onImport: work => phases.push(work) };
  return { initial, admitted, api, abort, phases, refresh, options };
}
it('opens once and immediately imports exactly the fresh main-owned session, capability and source IDs', async () => {
  const f = fixture(); expect(await openAndLoadSources(f.options)).toBe('ready');
  expect(f.api.pickRoots).toHaveBeenCalledExactlyOnceWith({ sessionId: 'initial-session', capability: null, generation: null }, 'select', ['fabric']);
  expect(f.api.importSnapshot).toHaveBeenCalledExactlyOnceWith({ sessionId: 'fresh-session', capability: 'fresh-capability', generation: null }, 'load', ['fresh-source']);
  expect(f.phases).toEqual([{ id: 'load', kind: 'import', binding: { sessionId: 'fresh-session', capability: 'fresh-capability', generation: null } }]);
  expect(f.refresh).toHaveBeenCalledTimes(2);
});
it.each(['rejected', 'throw', 'empty', 'missing-capability'] as const)('does not import a %s selection', async variant => {
  const f = fixture();
  if (variant === 'rejected') f.api.pickRoots.mockResolvedValueOnce({ status: 'error' });
  if (variant === 'throw') f.api.pickRoots.mockRejectedValueOnce(new Error('Selection unavailable'));
  if (variant === 'empty') f.refresh.mockResolvedValueOnce({ ...f.admitted, sources: [] });
  if (variant === 'missing-capability') f.refresh.mockResolvedValueOnce({ ...f.admitted, capability: null });
  expect(await openAndLoadSources(f.options)).not.toBe('ready'); expect(f.api.importSnapshot).not.toHaveBeenCalled(); expect(f.phases).toEqual([]);
});
it('does not cross the admission/import boundary after cancellation during a pending fresh-state read', async () => {
  const f = fixture(); let finish!: (state: ShellState) => void; let entered!: () => void;
  const started = new Promise<void>(resolve => { entered = resolve; }); const read = new Promise<ShellState>(resolve => { finish = resolve; });
  f.refresh.mockImplementationOnce(() => { entered(); return read; });
  const work = openAndLoadSources(f.options); await started; f.abort.abort(); finish(f.admitted);
  expect(await work).toBe('cancelled'); expect(f.api.importSnapshot).not.toHaveBeenCalled();
});
it('does not start selection or import when its renderer lifetime is already cancelled', async () => {
  const f = fixture(); f.abort.abort(); expect(await openAndLoadSources(f.options)).toBe('cancelled'); expect(f.api.pickRoots).not.toHaveBeenCalled(); expect(f.api.importSnapshot).not.toHaveBeenCalled();
});
it.each(['rejected', 'throw'] as const)('publishes retained state after a %s import', async variant => {
  const f = fixture();
  if (variant === 'rejected') f.api.importSnapshot.mockResolvedValueOnce({ status: 'error' }); else f.api.importSnapshot.mockRejectedValueOnce(new Error('Import unavailable'));
  expect(await openAndLoadSources(f.options)).toBe(variant === 'rejected' ? 'import-rejected' : 'import-failed');
  expect(f.refresh).toHaveBeenCalledTimes(2); expect(f.api.importSnapshot).toHaveBeenCalledOnce();
});
it('uses the import phase context before dispatch and stops when cancellation wins that exact handoff', async () => {
  const f = fixture();
  expect(await openAndLoadSources({ ...f.options, onImport: work => { f.phases.push(work); f.abort.abort(); } })).toBe('cancelled');
  expect(f.phases[0]?.binding.capability).toBe('fresh-capability'); expect(f.api.importSnapshot).not.toHaveBeenCalled(); expect(f.refresh).toHaveBeenCalledOnce();
});
it('reports a failed fresh-state read without importing or retrying the read automatically', async () => {
  const f = fixture(); f.refresh.mockRejectedValueOnce(new Error('State unavailable'));
  expect(await openAndLoadSources(f.options)).toBe('selection-failed'); expect(f.api.importSnapshot).not.toHaveBeenCalled(); expect(f.refresh).toHaveBeenCalledOnce();
});
it('marks each actual main request settled before its following state refresh', async () => {
  const f = fixture(); const events: string[] = [];
  f.refresh.mockImplementation(async () => { events.push('refresh'); return f.admitted; });
  expect(await openAndLoadSources({ ...f.options, onRequestSettled: () => events.push('settled') })).toBe('ready');
  expect(events).toEqual(['settled', 'refresh', 'settled', 'refresh']);
});
