/** Development-only finite native smoke of the production shell and retained-source broker. */
import assert from 'node:assert/strict';
import { mkdtempSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { pathToFileURL } from 'node:url';
import { createServer } from 'node:http';
import { app, BrowserWindow, ipcMain } from 'electron';
import { startDesktop } from '../src/shell/electron-shell.js';
import { ReadBroker } from '../src/broker/read-broker.js';
import type { DesktopBridge } from '../src/shell/bridge.js';
import { assertNativeIsolation } from './native-isolation.js';
import type { Binding, Response } from '@jai/fabric-explorer-contracts';

const directory = __dirname;
const workspace = mkdtempSync(join(tmpdir(), 'jai-desktop-native-'));
const project = join(workspace, 'source'); mkdirSync(project, { mode: 0o700 });
const source = join(project, 'selected.jsonl'); const original = '{"synthetic":true}\n'; writeFileSync(source, original, { mode: 0o600 });
const state = join(workspace, 'application'); mkdirSync(state, { mode: 0o700 });
app.setPath('appData', state);
let broker: ReadBroker;
let window: BrowserWindow;
let step = 0;
const total = 9;
const progress = (label: string): void => { console.log(`Step ${++step}/${total}: ${label}`); };
const watchdog = setTimeout(() => { console.error('Native smoke failed: 60-second total watchdog expired.'); app.exit(2); }, 60_000);
/** Evaluate only fixed maintainer-authored probes through the actual isolated preload. */
async function evaluate<T>(body: string): Promise<T> { return window.webContents.executeJavaScript(`(async () => { ${body} })()`); }

async function run(): Promise<void> {
  progress('Start production shell with isolated app data and trusted synthetic picker');
  const observation = new Promise<{ event: Electron.IpcMainEvent; value: unknown }>(resolve => {
    ipcMain.once('jai:native-smoke:isolation', (event, value: unknown) => resolve({ event, value }));
  });
  await startDesktop({
    picker: { project: async () => project, files: async () => [source] },
    createBroker: (paths, registry, writeRoots) => {
      broker = new ReadBroker({ registry, writeRoots }); return broker;
    },
  }, join(directory, 'native-smoke-assets'));
  window = BrowserWindow.getAllWindows()[0]!; assert(window);
  progress('Verify actual renderer isolation and frozen named bridge');
  const observed = await observation;
  assert.equal(observed.event.sender, window.webContents, 'Native observation must belong to the actual window');
  assert.equal(observed.event.senderFrame, window.webContents.mainFrame, 'Native observation must originate in the main frame');
  assert.equal(observed.event.senderFrame?.url, pathToFileURL(join(directory, 'native-smoke-assets/renderer/index.html')).href, 'Native observation must come from the fixed local document');
  assert.equal(observed.event.sender.session, window.webContents.session, 'Native observation must use the actual local session');
  assertNativeIsolation(observed.value);
  await window.webContents.executeJavaScriptInIsolatedWorld(999, [{ code: 'window.__isolatedProbe = true' }]);
  assert.equal(await evaluate<string>('return typeof window.__isolatedProbe;'), 'undefined');
  const isolation = await evaluate<{ require: string; process: string; names: string[]; frozen: boolean }>("return {require: typeof require, process: typeof process, names: Object.keys(window.fabricExplorer).sort(), frozen: Object.isFrozen(window.fabricExplorer)};");
  assert.equal(isolation.require, 'undefined'); assert.equal(isolation.process, 'undefined'); assert.equal(isolation.frozen, true);
  assert.deepEqual(isolation.names, ['cancelRequest', 'cancelSelection', 'closeRoots', 'counts', 'details', 'dropQuery', 'filterProjection', 'getState', 'groups', 'importSnapshot', 'layout', 'lookup', 'neighbours', 'pageSource', 'path', 'pickRoots', 'refreshSnapshot', 'search', 'searchFindings', 'updatePreferences']);
  progress('Admit one explicit source through real preload, IPC and read-only file broker');
  const selected = await evaluate<Response>("const state = await window.fabricExplorer.getState(); return window.fabricExplorer.pickRoots({sessionId: state.sessionId, capability: null, generation: null}, 'native-pick', ['fabric']);");
  assert.equal(selected.status, 'ok'); assert.equal(selected.operation, 'roots.pick');
  if (selected.status !== 'ok' || selected.operation !== 'roots.pick') throw new Error('Admission failed');
  const shell = await evaluate<Awaited<ReturnType<DesktopBridge['getState']>>>('return window.fabricExplorer.getState();');
  assert(shell.capability); assert.equal(shell.sources.length, 1);
  assert(!JSON.stringify(shell).includes(project), 'Native source paths must not enter renderer state');
  progress('Read bounded bytes with opaque capability; reject foreign owner and invented source');
  const page = await broker!.readPage(shell.sessionId, shell.capability, shell.sources[0]!.sourceId, { offset: '0', length: 256 });
  assert.equal(Buffer.from(page.bytesBase64, 'base64').toString('utf8'), original);
  await assert.rejects(broker!.readPage('foreign', shell.capability, shell.sources[0]!.sourceId, { offset: '0', length: 1 }));
  await assert.rejects(broker!.readPage(shell.sessionId, shell.capability, '../outside', { offset: '0', length: 1 }));
  progress('Reject malformed and foreign-session renderer calls');
  assert.equal(await evaluate<boolean>("try { await window.fabricExplorer.updatePreferences({version:1,theme:'system',reducedMotion:false,path:'/outside'}); return false; } catch { return true; }"), true);
  assert.equal(await evaluate<boolean>("try { await window.fabricExplorer.closeRoots({sessionId:'foreign',capability:'foreign',generation:null}, 'foreign-close'); return false; } catch { return true; }"), true);
  progress('Deny a controlled reachable endpoint, inline scripts and new windows');
  let received = 0;
  const endpoint = createServer((_request, response) => { received++; response.setHeader('Access-Control-Allow-Origin', '*'); response.end('reachable'); });
  await new Promise<void>((resolve, reject) => { endpoint.once('error', reject); endpoint.listen(0, '127.0.0.1', resolve); });
  const address = endpoint.address(); assert(address && typeof address !== 'string');
  const url = `http://127.0.0.1:${address.port}/`;
  // Prove endpoint reachability in the trusted main before using its request count.
  assert.equal(await (await fetch(url)).text(), 'reachable'); assert.equal(received, 1); received = 0;
  assert.equal(await evaluate<boolean>(`try { await fetch(${JSON.stringify(url)}); return false; } catch { return true; }`), true);
  assert.equal(received, 0, 'Forbidden renderer fetch must not reach the controlled endpoint');
  await new Promise<void>((resolve, reject) => endpoint.close(error => error ? reject(error) : resolve()));
  assert.equal(await evaluate<boolean>("window.__inlineProbe = false; const script = document.createElement('script'); script.textContent = 'window.__inlineProbe = true'; document.head.append(script); const denied = window.__inlineProbe === false; script.remove(); delete window.__inlineProbe; return denied;"), true);
  assert.equal(await evaluate<boolean>("return window.open('https://example.invalid/') === null;"), true);
  assert.equal(BrowserWindow.getAllWindows().length, 1);
  progress('Persist only schema-valid presentation preferences');
  await evaluate("return window.fabricExplorer.updatePreferences({version:1,theme:'dark',reducedMotion:true});");
  const prefs = await evaluate<Awaited<ReturnType<DesktopBridge['getState']>>>('return window.fabricExplorer.getState();');
  assert.equal(prefs.preferences.theme, 'dark');
  progress('Close source capability and reject subsequent access');
  const binding: Binding = { sessionId: shell.sessionId, capability: shell.capability, generation: null };
  const closed = await evaluate<Response>(`return window.fabricExplorer.closeRoots(${JSON.stringify(binding)}, 'native-close');`);
  assert.equal(closed.status, 'ok');
  await assert.rejects(broker!.readPage(shell.sessionId, shell.capability, shell.sources[0]!.sourceId, { offset: '0', length: 1 }));
  progress('Verify source bytes unchanged and release the native window');
  assert.equal(readFileSync(source, 'utf8'), original);
  await broker!.disposeSession(shell.sessionId);
  clearTimeout(watchdog);
  console.log(`Native smoke PASS: ${step}/${total}; platform=${process.platform}; Electron=${process.versions.electron}. OS dialog interaction and process-tree network qualification are separate checks.`);
  window.destroy(); app.exit(0);
}
void run().catch((error: unknown) => {
  clearTimeout(watchdog);
  ipcMain.removeAllListeners('jai:native-smoke:isolation');
  const detail = error instanceof Error ? `${error.name}: ${error.message}`.slice(0, 500) : 'Unknown native failure';
  console.error(`Native smoke FAIL at step ${step}/${total}: ${detail}. Synthetic evidence remains in the operating-system temporary directory.`);
  app.exit(1);
});
