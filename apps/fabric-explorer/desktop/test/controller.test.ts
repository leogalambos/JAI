/** Root lifecycle tests use owned broker/dialog ports; no production test backdoor exists. */
import { describe, expect, it, vi } from 'vitest';
import { PROTOCOL, encodeFrame, decodeResponseFrame } from '@jai/fabric-explorer-contracts';
import type { Request } from '@jai/fabric-explorer-contracts';
import type { BrokerPort } from '../src/broker/types.js';
import { ShellController } from '../src/shell/controller.js';
import type { PickerPort } from '../src/shell/controller.js';
import { DEFAULT_PREFERENCES } from '../src/shell/preferences.js';
import type { PreferenceStore } from '../src/shell/preferences.js';
function fixture(project: () => Promise<string | null> = async () => '/project', files: PickerPort['files'] = async () => ['/external/nodes.jsonl']) {
  const calls: unknown[] = [];
  const broker: BrokerPort = { open: async (...args) => { calls.push(['open', ...args]); return { capability: 'cap', sources: [{ projectId: 'project', rootId: 'root', sourceId: 'source', family: 'fabric', relativePath: 'nodes.jsonl', readHandle: 'handle' }] }; }, close: async (...args) => { calls.push(['close', ...args]); }, disposeSession: async (...args) => { calls.push(['dispose', ...args]); } };
  const store = { load: () => ({ preferences: DEFAULT_PREFERENCES, warning: null }), save: () => DEFAULT_PREFERENCES } as unknown as PreferenceStore;
  const controller = new ShellController(broker, { project, files }, store);
  const request = (operation: 'roots.pick' | 'roots.close' | 'snapshot.import' | 'request.cancel', requestId: string, payload: unknown = {}) => encodeFrame({ protocol: PROTOCOL, kind: 'request', operation, requestId, binding: { sessionId: controller.sessionId, capability: operation === 'roots.pick' ? null : controller.state().capability, generation: null }, payload } as Request);
  return { controller, calls, request };
}
describe('desktop controller', () => {
  it('passes the selected project and remaining capacity to each family picker', async () => {
    const files = vi.fn(async () => ['/external/nodes.jsonl']);
    const { controller, request } = fixture(async () => '/chosen/project', files);
    expect(decodeResponseFrame(await controller.request(request('roots.pick', 'pick', { families: ['fabric', 'findings'] }))).status).toBe('ok');
    expect(files).toHaveBeenNthCalledWith(1, 'fabric', '/chosen/project', 128, expect.any(AbortSignal));
    expect(files).toHaveBeenNthCalledWith(2, 'findings', '/chosen/project', 127, expect.any(AbortSignal));
  });

  it('admits deliberate external files with the project anchor and closes handles', async () => {
    const { controller, calls, request } = fixture();
    expect(decodeResponseFrame(await controller.request(request('roots.pick', 'pick', { families: ['fabric'] }))).status).toBe('ok');
    expect(calls[0]).toEqual(['open', controller.sessionId, [{ projectPath: '/project', path: '/external/nodes.jsonl', family: 'fabric' }], expect.any(AbortSignal)]);
    expect(controller.state().capability).toBe('cap'); await controller.request(request('roots.close', 'close')); expect(controller.state().sources).toEqual([]); expect(calls.at(-1)).toEqual(['close', controller.sessionId, 'cap']);
  });
  it('reports unavailable interpretation explicitly without fabricating a snapshot', async () => {
    const { controller, request } = fixture(); await controller.request(request('roots.pick', 'pick', { families: ['fabric'] })); const response = decodeResponseFrame(await controller.request(request('snapshot.import', 'refresh', { sourceIds: ['source'] })));
    expect(response.status).toBe('error'); expect(response).not.toHaveProperty('payload');
  });
  it('rejects malformed/foreign envelopes and cancelled native selection never calls broker', async () => {
    const { controller, calls, request } = fixture(async () => null);
    await expect(controller.request('{}')).rejects.toThrow();
    await expect(controller.request(request('roots.pick', 'pick', { families: ['fabric'] }).replace(controller.sessionId, 'foreign'))).rejects.toThrow();
    expect(decodeResponseFrame(await controller.request(request('roots.pick', 'pick', { families: ['fabric'] }))).status).toBe('error'); expect(calls).toEqual([]);
  });
  it('cancels a pending native dialog and rejects duplicate request identifiers', async () => {
    let finish!: (path: string) => void; const waiting = new Promise<string>(resolve => { finish = resolve; }); const { controller, calls, request } = fixture(() => waiting);
    const frame = request('roots.pick', 'pick', { families: ['fabric'] }); const work = controller.request(frame);
    await expect(controller.request(frame)).rejects.toThrow('Request limit');
    expect(controller.cancelSelection('pick')).toBe(true); expect(() => controller.cancelSelection('../bad')).toThrow();
    expect(decodeResponseFrame(await controller.request(request('roots.pick', 'queued', { families: ['fabric'] }))).status).toBe('error');
    finish('/project'); expect(decodeResponseFrame(await work).status).toBe('error'); expect(calls).toEqual([]);
  });
  it('suppresses a late dialog reply after session disposal', async () => {
    let finish!: (path: string) => void; const waiting = new Promise<string>(resolve => { finish = resolve; }); const { controller, calls, request } = fixture(() => waiting);
    const work = controller.request(request('roots.pick', 'pick', { families: ['fabric'] })); await controller.dispose(); finish('/project');
    expect(decodeResponseFrame(await work).status).toBe('error'); expect(calls).toEqual([['dispose', controller.sessionId]]);
  });
  it.each(['cancel', 'dispose'])('does not admit files from a late family picker after %s', async action => {
    let finish!: (paths: string[]) => void; let entered!: () => void;
    const waiting = new Promise<string[]>(resolve => { finish = resolve; });
    const started = new Promise<void>(resolve => { entered = resolve; });
    const { controller, calls, request } = fixture(async () => '/project', async (_family, _project, _capacity, signal) => { expect(signal.aborted).toBe(false); entered(); return waiting; });
    const work = controller.request(request('roots.pick', 'pick', { families: ['fabric'] })); await started;
    if (action === 'cancel') controller.cancelSelection('pick'); else await controller.dispose();
    finish(['/external/late.jsonl']); expect(decodeResponseFrame(await work).status).toBe('error');
    expect(calls.some(call => Array.isArray(call) && call[0] === 'open')).toBe(false);
  });
});
