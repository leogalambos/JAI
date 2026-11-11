/** Test-only native observation must retain the real preload and report exact sandbox state. */
import { afterEach, expect, it, vi } from 'vitest';
const fake = vi.hoisted(() => ({ send: vi.fn(), expose: vi.fn() }));
vi.mock('electron', () => ({ contextBridge: { exposeInMainWorld: fake.expose }, ipcRenderer: { invoke: vi.fn(), send: fake.send } }));
import { assertNativeIsolation } from './native-isolation.js';
const originalSandbox = Object.getOwnPropertyDescriptor(process, 'sandboxed');
const originalIsolation = Object.getOwnPropertyDescriptor(process, 'contextIsolated');
afterEach(() => {
  for (const [name, descriptor] of [['sandboxed', originalSandbox], ['contextIsolated', originalIsolation]] as const) { if (descriptor) Object.defineProperty(process, name, descriptor); else Reflect.deleteProperty(process, name); }
  fake.send.mockClear(); fake.expose.mockClear(); vi.resetModules();
});
it('emits exact native observation once without replacing the production bridge', async () => {
  Object.defineProperty(process, 'sandboxed', { value: true, configurable: true }); Object.defineProperty(process, 'contextIsolated', { value: true, configurable: true });
  await import('./native-preload.js');
  expect(fake.expose).toHaveBeenCalledExactlyOnceWith('fabricExplorer', expect.objectContaining({ getState: expect.any(Function), pickRoots: expect.any(Function) }));
  expect(fake.send).toHaveBeenCalledExactlyOnceWith('jai:native-smoke:isolation', { sandboxed: true, contextIsolated: true });
});
it('preserves false and absent observations rather than inferring success', async () => {
  Object.defineProperty(process, 'sandboxed', { value: false, configurable: true }); Reflect.deleteProperty(process, 'contextIsolated');
  await import('./native-preload.js');
  expect(fake.send).toHaveBeenCalledExactlyOnceWith('jai:native-smoke:isolation', { sandboxed: false, contextIsolated: undefined });
});

it('rejects absent, false and malformed native attestations', () => {
  expect(() => assertNativeIsolation({ sandboxed: true, contextIsolated: true })).not.toThrow();
  for (const value of [undefined, null, {}, { sandboxed: false, contextIsolated: true }, { sandboxed: true }, { sandboxed: true, contextIsolated: false }, { sandboxed: true, contextIsolated: true, extra: true }]) expect(() => assertNativeIsolation(value)).toThrow();
});
