// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Finite development-only production journey over externally ACL-sealed synthetic sources; no fixture writes. */
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { existsSync, lstatSync, readdirSync, readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { isAbsolute, join, relative, sep } from 'node:path';
import { pathToFileURL } from 'node:url';
import { app, BrowserWindow, ipcMain } from 'electron';
import { startDesktop } from '../src/shell/electron-shell.js';
import { ReadBroker } from '../src/broker/read-broker.js';
import { ImportSession } from '../src/import/session.js';
import { NativeImportWorker } from '../src/import/worker-client.js';
import { assertNativeIsolation } from './native-isolation.js';
interface Entry { readonly path: string; readonly kind: 'directory' | 'file'; readonly device: string; readonly inode: string; readonly mode: string; readonly size: string; readonly sha256?: string }
interface Manifest { readonly format: string; readonly sourceRoot: string; readonly projectRoot: string; readonly fabric: string; readonly findings: string; readonly appRoot: string; readonly initialCwd: string; readonly trustedExecutables: readonly string[]; readonly sourceSnapshotBefore: readonly Entry[]; readonly negativeWriteProbes: readonly { readonly denied: boolean }[] }
const destination = process.argv.at(-2); const input = process.argv.at(-1);
assert(destination && input && isAbsolute(destination) && isAbsolute(input), 'Absolute evidence directory and manifest required');
const manifest = JSON.parse(readFileSync(input, 'utf8')) as Manifest;
assert.equal(manifest.format, 'jai.fabric-explorer.security-input/1'); assert.equal(manifest.sourceRoot, join(destination, 'synthetic-source')); assert.equal(manifest.appRoot, join(destination, 'application')); assert.equal(manifest.projectRoot, manifest.sourceRoot);
assert([manifest.fabric, manifest.findings].every(path => isAbsolute(path) && relative(manifest.sourceRoot, path).split(sep).length === 1), 'Fixed journal children required');
assert(manifest.negativeWriteProbes.length === 4 && manifest.negativeWriteProbes.every(probe => probe.denied), 'Actual prior OS-denied probes required');
app.setPath('appData', manifest.appRoot);
const observations: { id: number; title: string; status: 'pass'; detail?: unknown }[] = [];
const capturedErrors: { contentsId: number; message: string }[] = [];
let rendererContentsId: number | null = null;
const consoleErrors = () => capturedErrors.filter(item => item.contentsId === rendererContentsId).map(item => item.message);
let window: BrowserWindow | null = null; let outcome = 'in-progress'; let failure: string | null = null; let step = 0;
let integrity: unknown = null; let nativeIsolation: unknown = null; let spellCheckerEnabled: boolean | null = null;
let spellCheckerLanguages: string[] | null = null; const dictionaryDownloads: string[] = []; let dictionaryFiles: string[] | null = null;
const report = () => ({ format: 'jai.fabric-explorer.security-native/1', status: outcome, completedCases: observations.length, totalCases: 8, step, observations, consoleErrors: consoleErrors(), failure, integrity, nativeIsolation, runtimePolicy: { spellCheckerEnabled, spellCheckerLanguages, dictionaryDownloads, dictionaryFiles }, environment: { platform: process.platform, electron: process.versions.electron, chromium: process.versions.chrome, node: process.versions.node, uid: process.getuid?.(), display: !!(process.env.DISPLAY || process.env.WAYLAND_DISPLAY) }, method: 'Actual fixed production composition and byte-identical renderer with production preload plus test-only native isolation observation; explicitly synthetic picker. All source creation and denied write probes precede tracing. No HTTP endpoint or source mutation is part of this journey.' });
const save = () => writeFileSync(join(destination, 'security-native.json'), JSON.stringify(report(), null, 2) + '\n');
function snapshot(root: string): Entry[] {
  const entries: Entry[] = []; const pending = [root];
  while (pending.length) {
    const path = pending.pop()!; const info = lstatSync(path, { bigint: true }); const directory = info.isDirectory();
    assert(directory || info.isFile() && info.nlink === 1n, 'Only nonlinked regular fixture entries');
    const entry = { path: relative(root, path).split(sep).join('/') || '.', kind: directory ? 'directory' as const : 'file' as const, device: String(info.dev), inode: String(info.ino), mode: String(info.mode & 0o7777n), size: String(info.size) };
    if (directory) { entries.push(entry); pending.push(...readdirSync(path).map(name => join(path, name))); }
    else entries.push({ ...entry, sha256: createHash('sha256').update(readFileSync(path)).digest('hex') });
  }
  return entries.sort((left, right) => left.path < right.path ? -1 : left.path > right.path ? 1 : 0);
}
async function evaluate<T>(body: string): Promise<T> { assert(window && !window.isDestroyed()); return window.webContents.executeJavaScript(`(async()=>{${body}})()`); }
async function wait(expression: string, label: string): Promise<void> {
  assert(await evaluate<boolean>(`const end=performance.now()+20000;while(performance.now()<end){if(${expression})return true;await new Promise(resolve=>requestAnimationFrame(resolve));}return false;`), label);
}
async function click(selector: string): Promise<void> { if (['#tab-sources', '#tab-search', '#tab-findings', '#show-elements'].includes(selector) && await evaluate<boolean>("return !!document.querySelector('.navigation-pane')?.hidden;")) await click('#show-navigation'); if (selector.startsWith('#inspector-tab-') && await evaluate<boolean>("return !!document.querySelector('.inspector')?.hidden;")) await click('#show-inspector'); await evaluate(`const element=document.querySelector(${JSON.stringify(selector)});if(!(element instanceof HTMLButtonElement)||element.disabled||!element.getClientRects().length)throw new Error('Named control unavailable');element.click();`); }
function begin(title: string): void { step++; console.log(`Krok ${step}/8: ${title}`); save(); }
function passed(title: string, detail?: unknown): void { observations.push({ id: step, title, status: 'pass', ...(detail === undefined ? {} : { detail }) }); save(); }
async function run(): Promise<void> {
  console.log('Bezpečnostní zkouška: 8 konečných kroků; žádné ruční hodnocení. Okno nebo Ctrl+C ukončí běh.');
  assert.deepEqual(snapshot(manifest.sourceRoot), manifest.sourceSnapshotBefore, 'Source baseline before launch');
  begin('Spuštění skutečné aplikace nad chráněnými syntetickými daty.');
  const isolationObservation = new Promise<{ event: Electron.IpcMainEvent; value: unknown }>(resolve => {
    ipcMain.once('jai:native-smoke:isolation', (event, value: unknown) => resolve({ event, value }));
  });
  const assets = join(__dirname, 'security-assets');
  const observe = (_event: Electron.Event, contents: Electron.WebContents) => {
    contents.on('console-message', event => { if (event.level === 'error') capturedErrors.push({ contentsId: contents.id, message: event.message }); });
  };
  const observeSession = (current: Electron.Session) => {
    current.on('spellcheck-dictionary-download-begin', (_event, language) => dictionaryDownloads.push(language));
  };
  app.on('web-contents-created', observe);
  app.on('session-created', observeSession);
  await startDesktop({ picker: { project: async () => manifest.projectRoot, files: async family => [family === 'findings' ? manifest.findings : manifest.fabric] },
    createBroker: (_paths, registry, writeRoots) => new ReadBroker({ registry, writeRoots }),
    createImport: (selection, broker, paths) => { assert(broker instanceof ReadBroker); return new ImportSession({ ...selection, broker, archiveDirectory: join(paths.temp, 'captures'), workerFactory: () => new NativeImportWorker(join(__dirname, 'import-worker.cjs')) }); },
  }, assets);
  app.off('web-contents-created', observe);
  app.off('session-created', observeSession);
  window = BrowserWindow.getAllWindows()[0] ?? null; assert(window); rendererContentsId = window.webContents.id; window.setSize(1440, 1000);
  window.once('closed', () => { if (outcome === 'in-progress') { outcome = 'interrupted'; save(); app.exit(130); } });
  await wait("document.querySelector('#open')&&!document.querySelector('#open').disabled", 'Initial production controls');
  passed('Production shell loaded');

  begin('Ověření oddělení rendereru a otevření pouze vybraných vstupů.');
  const isolation = await evaluate<{ require: string; process: string; frozen: boolean; names: string[] }>("return{require:typeof require,process:typeof process,frozen:Object.isFrozen(window.fabricExplorer),names:Object.keys(window.fabricExplorer).sort()};");
  assert.equal(isolation.require, 'undefined'); assert.equal(isolation.process, 'undefined'); assert(isolation.frozen);
  const observed = await isolationObservation;
  assert.equal(observed.event.sender, window.webContents); assert.equal(observed.event.senderFrame, window.webContents.mainFrame);
  assert.equal(observed.event.sender.session, window.webContents.session);
  assert.equal(observed.event.senderFrame?.url, pathToFileURL(join(assets, 'renderer/index.html')).href);
  assertNativeIsolation(observed.value); nativeIsolation = observed.value;
  spellCheckerEnabled = window.webContents.session.isSpellCheckerEnabled();
  assert.equal(spellCheckerEnabled, false, 'Automatic spellchecker dictionary downloads must be disabled');
  spellCheckerLanguages = window.webContents.session.getSpellCheckerLanguages();
  assert.deepEqual(spellCheckerLanguages, [], 'Queued dictionaries must be cleared, not only renderer spellchecking disabled');
  assert.deepEqual(isolation.names, ['cancelRequest', 'cancelSelection', 'closeRoots', 'counts', 'details', 'dropQuery', 'filterProjection', 'getState', 'groups', 'importSnapshot', 'layout', 'lookup', 'neighbours', 'pageSource', 'path', 'pickRoots', 'refreshSnapshot', 'search', 'searchFindings', 'updatePreferences']);
  passed('Actual renderer boundary before source selection', isolation);

  begin('Import a čtení materiálů při zákazu zápisu operačním systémem.');
  await click('#open'); await wait("document.querySelector('.semantic-panel tbody button')&&document.querySelector('#cancel').disabled&&document.querySelector('[data-testid=count-findings]')?.textContent==='6'", 'Imported read-only snapshot');
  const state = await evaluate<{ sessionId: string; capability: string; snapshot: { generation: string; counts: unknown } }>('return window.fabricExplorer.getState();'); assert(state.snapshot);
  passed('ACL-protected actual import', state.snapshot);

  begin('Přesná identita, odmítnutí cizí relace a příliš velkého dotazu.');
  const identity = await evaluate<unknown>("const binding=await window.fabricExplorer.getState();const page=await window.fabricExplorer.search({sessionId:binding.sessionId,capability:binding.capability,generation:binding.snapshot.generation},'security-seed',{text:'',filter:{projectIds:[],families:[],findingStates:[],relations:[]},order:'identity',limit:1,cursor:null});return page.response.payload.items[0].identity;");
  console.log('Očekávaná negativní zkouška: následující session-mismatch je záměrné odmítnutí cizí session, nikoli závada aplikace.');
  const forged = await evaluate<boolean>(`try{await window.fabricExplorer.lookup({sessionId:'foreign-session',capability:${JSON.stringify(state.capability)},generation:${JSON.stringify(state.snapshot.generation)}},'security-forged',{identity:${JSON.stringify(identity)}});return false;}catch{return true;}`); assert(forged);
  console.log('Očekávané odmítnutí cizí session bylo ověřeno; test pokračuje.');
  const oversized = await evaluate<boolean>("const current=await window.fabricExplorer.getState();try{await window.fabricExplorer.search({sessionId:current.sessionId,capability:current.capability,generation:current.snapshot.generation},'security-oversized',{text:'x'.repeat(9*1024*1024),filter:{projectIds:[],families:[],findingStates:[],relations:[]},order:'identity',limit:1,cursor:null});return false;}catch{return true;}"); assert(oversized);
  passed('Forged and oversized named requests rejected');

  begin('Zobrazení škodlivě vypadajícího popisku jako neaktivního textu.');
  await click('#tab-findings'); await evaluate("const item=document.querySelector('#finding-text').closest('section').querySelector('.results button');if(!item)throw new Error('Finding unavailable');item.click();");
  await wait("document.querySelector('[data-testid=selected-id]')", 'Finding inspector');
  const inert = await evaluate<{ marker: string; activeNodes: number; text: string }>("return{marker:typeof globalThis.__sourceExecuted,activeNodes:document.querySelectorAll('.inspector img,.inspector script,#search-content .results img,#search-content .results script').length,text:document.querySelector('.inspector').textContent};");
  assert.equal(inert.marker, 'undefined'); assert.equal(inert.activeNodes, 0); assert(inert.text.includes('<img'), 'Prepared hostile label is actually present'); passed('Hostile source label remains inert', { marker: inert.marker, activeNodes: inert.activeNodes });

  begin('Stránka zachyceného zdroje bez změny původních souborů.');
  await click('#inspector-tab-evidence'); await click('#read-source'); await wait("document.querySelector('#source-text')?.textContent.length>0", 'Archived source page');
  assert.deepEqual(snapshot(manifest.sourceRoot), manifest.sourceSnapshotBefore); passed('Archived page and unchanged protected source tree');

  begin('Obnovení stejné revize a zavření oprávnění ke zdrojům.');
  await click('#refresh'); await wait(`document.querySelector('#cancel').disabled&&(await window.fabricExplorer.getState()).snapshot?.generation!==${JSON.stringify(state.snapshot.generation)}`, 'Unchanged-source refresh');
  await click('#close'); await wait("(await window.fabricExplorer.getState()).capability===null", 'Source capabilities closed'); passed('Unchanged protected refresh and close');

  begin('Závěrečná kontrola bajtů, položek adresářů a fyzických identit.');
  const after = snapshot(manifest.sourceRoot); integrity = { unchanged: JSON.stringify(after) === JSON.stringify(manifest.sourceSnapshotBefore), before: manifest.sourceSnapshotBefore, after };
  assert.deepEqual(after, manifest.sourceSnapshotBefore); assert.equal(consoleErrors().length, 0, 'Unexpected renderer errors');
  assert.equal(existsSync(join(manifest.appRoot, 'project-code-executed')), false, 'Project-controlled Python startup code must not execute');
  const dictionaries = join(manifest.appRoot, 'JAI Fabric Explorer', 'session-data', 'Dictionaries');
  dictionaryFiles = existsSync(dictionaries) ? readdirSync(dictionaries).filter(name => name.toLowerCase().endsWith('.bdic')) : [];
  assert.deepEqual(dictionaryDownloads, [], 'No dictionary download may start during the native session');
  assert.deepEqual(dictionaryFiles, [], 'No downloaded dictionary may appear in the fresh application state');
  passed('Complete source tree unchanged; project startup sentinel absent'); outcome = 'passed'; save();
  window.close(); app.quit();
}
const watchdog = setTimeout(() => { if (outcome === 'in-progress') { outcome = 'blocked'; failure = '150-second native watchdog expired'; save(); app.exit(2); } }, 150000);
void run().then(() => clearTimeout(watchdog)).catch(error => { clearTimeout(watchdog); outcome = 'failed'; failure = error instanceof Error ? error.message : 'Security journey failed'; save(); console.error(failure); app.exit(1); });
