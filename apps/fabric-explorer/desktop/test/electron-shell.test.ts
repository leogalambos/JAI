/** Owned Electron fake verifies startup ordering and actual wrapper policy wiring. */
import { afterEach, describe, expect, it, vi } from 'vitest';
import { mkdirSync, mkdtempSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { PROTOCOL, decodeResponseFrame, encodeFrame } from '@jai/fabric-explorer-contracts';
const fake = vi.hoisted(() => ({ base: '', calls: [] as string[], options: null as Record<string, unknown> | null, handlers: new Map<string, (...args: any[]) => any>(), appEvents: new Map<string, (...args: any[]) => any>(), windowEvents: new Map<string, (...args: any[]) => any>(), quitCalls: 0, onQuit: null as (() => void) | null, fail: false, sender: null as any, dialog: vi.fn() }));
vi.mock('electron', () => ({
  app: { getPath: () => fake.base, setPath: (name: string) => fake.calls.push(name), setAppLogsPath: () => fake.calls.push('logs'), commandLine: { appendSwitch: () => fake.calls.push('cache') }, whenReady: async () => { fake.calls.push('ready'); if (fake.fail) throw new Error('Native initialization unavailable'); }, on: (name: string, callback: (...args: any[]) => any) => fake.appEvents.set(name, callback), quit: () => { fake.quitCalls++; fake.onQuit?.(); } },
  session: { fromPartition: () => { fake.calls.push('session'); return { webRequest: { onBeforeRequest: vi.fn(), onHeadersReceived: vi.fn() }, setSpellCheckerLanguages: (languages: string[]) => fake.calls.push(`spellcheck-languages:${JSON.stringify(languages)}`), setSpellCheckerEnabled: (enabled: boolean) => fake.calls.push(`spellcheck:${enabled}`), setPermissionCheckHandler: vi.fn(), setPermissionRequestHandler: vi.fn(), on: vi.fn() }; } },
  BrowserWindow: class { webContents: any; constructor(options: Record<string, unknown>) { this.webContents = { session: (options.webPreferences as any).session, mainFrame: { url: '' }, isDestroyed: () => false, setWindowOpenHandler: vi.fn(), on: vi.fn() }; fake.sender = this.webContents; fake.options = options; fake.calls.push('window'); } removeMenu() { fake.calls.push('remove-menu'); } on(name: string, callback: (...args: any[]) => any) { fake.windowEvents.set(name, callback); } async loadURL(url: string) { this.webContents.mainFrame.url = url; fake.calls.push('load'); } isDestroyed() { return false; } show() { fake.calls.push('show'); } },
  ipcMain: { handle: (name: string, handler: (...args: any[]) => any) => fake.handlers.set(name, handler) }, dialog: { showOpenDialog: fake.dialog },
}));
import { startDesktop } from '../src/shell/electron-shell.js';
const originalTemporaryEnvironment = { TMPDIR: process.env.TMPDIR, TEMP: process.env.TEMP, TMP: process.env.TMP };
const fixedTemporaryBase = tmpdir();
const dirs: string[] = [];
afterEach(() => { for (const [key, value] of Object.entries(originalTemporaryEnvironment)) { if (value === undefined) delete process.env[key]; else process.env[key] = value; } for (const dir of dirs.splice(0)) rmSync(dir, { recursive: true, force: true }); fake.calls = []; fake.handlers.clear(); fake.appEvents.clear(); fake.windowEvents.clear(); fake.quitCalls = 0; fake.onQuit = null; fake.fail = false; fake.sender = null; fake.dialog.mockReset(); vi.restoreAllMocks(); });
function dependencies() { fake.base = mkdtempSync(join(fixedTemporaryBase, 'jai-electron-test-')); dirs.push(fake.base); return { createBroker: () => ({ open: vi.fn(), close: vi.fn(), disposeSession: vi.fn() }), picker: { project: async () => null, files: async () => null } }; }
describe('Electron wrapper', () => {
  it('uses canonical project ledgers through the production picker without extra native dialogs', async () => {
    const ports = dependencies(); const project = mkdtempSync(join(fixedTemporaryBase, 'jai-native-project-')); dirs.push(project);
    mkdirSync(join(project, '.fabric')); mkdirSync(join(project, '.findings'));
    const fabric = join(project, '.fabric/engagement.jsonl'); const findings = join(project, '.findings/review.jsonl');
    writeFileSync(fabric, 'not parsed during selection'); writeFileSync(findings, 'not parsed during selection');
    const open = vi.fn(async () => ({ capability: 'cap', sources: [{ projectId: 'project', rootId: 'fabric-root', sourceId: 'fabric-source', family: 'fabric' as const, relativePath: 'engagement.jsonl', readHandle: 'fabric-handle' }, { projectId: 'project', rootId: 'findings-root', sourceId: 'findings-source', family: 'findings' as const, relativePath: 'review.jsonl', readHandle: 'findings-handle' }] }));
    ports.createBroker = () => ({ open, close: vi.fn(), disposeSession: vi.fn() });
    fake.dialog.mockResolvedValueOnce({ canceled: false, filePaths: [project] });
    await startDesktop({ createBroker: ports.createBroker }, '/fixed/dist');
    const event = { sender: fake.sender, senderFrame: fake.sender.mainFrame }; const state = fake.handlers.get('jai:state')!(event);
    const response = await fake.handlers.get('jai:request')!(event, encodeFrame({ protocol: PROTOCOL, kind: 'request', operation: 'roots.pick', requestId: 'native-automatic', binding: { sessionId: state.sessionId, capability: null, generation: null }, payload: { families: ['fabric', 'findings'] } }));
    expect(decodeResponseFrame(response).status).toBe('ok');
    expect(fake.dialog).toHaveBeenCalledOnce();
    expect(open).toHaveBeenCalledExactlyOnceWith(state.sessionId, [{ projectPath: project, path: fabric, family: 'fabric' }, { projectPath: project, path: findings, family: 'findings' }], expect.any(AbortSignal));
  });
  it('opens production manual source selection in the chosen project instead of cwd', async () => {
    const ports = dependencies(); const project = join(fake.base, 'chosen-project');
    fake.dialog.mockResolvedValueOnce({ canceled: false, filePaths: [project] }).mockResolvedValueOnce({ canceled: true, filePaths: [] });
    await startDesktop({ createBroker: ports.createBroker }, '/fixed/dist');
    const event = { sender: fake.sender, senderFrame: fake.sender.mainFrame };
    const state = fake.handlers.get('jai:state')!(event);
    const frame = encodeFrame({ protocol: PROTOCOL, kind: 'request', operation: 'roots.pick', requestId: 'native-default', binding: { sessionId: state.sessionId, capability: null, generation: null }, payload: { families: ['fabric'] } });
    await fake.handlers.get('jai:request')!(event, frame);
    expect(fake.dialog).toHaveBeenCalledTimes(2);
    expect(fake.dialog.mock.calls[1]?.[1]).toMatchObject({ defaultPath: project, properties: ['openFile', 'multiSelections', 'dontAddToRecent'] });
  });

  it('fixes all write locations before readiness/session/window and applies hardened window options', async () => {
    await startDesktop(dependencies(), '/fixed/dist');
    expect(fake.calls).toEqual(['userData', 'sessionData', 'crashDumps', 'temp', 'logs', 'cache', 'ready', 'session', 'spellcheck-languages:[]', 'spellcheck:false', 'window', 'remove-menu', 'load', 'show']);
    expect(fake.options?.webPreferences).toMatchObject({ sandbox: true, contextIsolation: true, nodeIntegration: false, webSecurity: true, devTools: false, spellcheck: false });
    for (const name of ['jai:state', 'jai:query-start', 'jai:search-findings', 'jai:filter-projection', 'jai:query-next', 'jai:query-drop', 'jai:layout', 'jai:groups']) expect(() => fake.handlers.get(name)!({ sender: {}, senderFrame: {} })).toThrow();
  });
  it('does not create a browser session or window when native readiness fails', async () => {
    const ports = dependencies(); fake.fail = true; await expect(startDesktop(ports, '/fixed/dist')).rejects.toThrow('Native initialization'); expect(fake.calls).not.toContain('session'); expect(fake.calls).not.toContain('window');
  });
  it.each([false, true])('waits for owned cleanup before quit even after controller is cleared: %s', async closed => {
    let finish!: () => void; let entered!: () => void;
    const waiting = new Promise<void>(resolve => { finish = resolve; });
    const started = new Promise<void>(resolve => { entered = resolve; });
    const ports = dependencies(); const dispose = vi.fn(async () => { entered(); await waiting; });
    ports.createBroker = () => ({ open: vi.fn(), close: vi.fn(), disposeSession: dispose });
    await startDesktop(ports, '/fixed/dist');
    if (closed) { fake.windowEvents.get('closed')!(); fake.appEvents.get('window-all-closed')!(); }
    const previousQuitCalls = fake.quitCalls; const event = { preventDefault: vi.fn() };
    fake.appEvents.get('before-quit')!(event); expect(event.preventDefault).toHaveBeenCalledOnce();
    fake.appEvents.get('activate')!(); expect(fake.calls.filter(call => call === 'window')).toHaveLength(1);
    await started; expect(fake.quitCalls).toBe(previousQuitCalls);
    const complete = new Promise<void>(resolve => { fake.onQuit = resolve; }); finish(); await complete;
    expect(dispose).toHaveBeenCalledOnce(); expect(fake.quitCalls).toBe(previousQuitCalls + 1);
    const allowed = { preventDefault: vi.fn() }; fake.appEvents.get('before-quit')!(allowed); expect(allowed.preventDefault).not.toHaveBeenCalled();
  });
  it('reports a fixed cleanup failure and still completes the exit attempt', async () => {
    const error = vi.spyOn(console, 'error').mockImplementation(() => {});
    const ports = dependencies(); ports.createBroker = () => ({ open: vi.fn(), close: vi.fn(), disposeSession: vi.fn(async () => { throw new Error('/private/source/path'); }) });
    await startDesktop(ports, '/fixed/dist');
    const complete = new Promise<void>(resolve => { fake.onQuit = resolve; });
    fake.appEvents.get('before-quit')!({ preventDefault: vi.fn() }); await complete;
    expect(error).toHaveBeenCalledExactlyOnceWith('Fabric Explorer cleanup failed.');
  });
});
