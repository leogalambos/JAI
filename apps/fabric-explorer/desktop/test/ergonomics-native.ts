// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Six finite native-keyboard observations of the current development UI; no release or speech qualification. */
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { mkdirSync, readFileSync, readdirSync, writeFileSync } from 'node:fs';
import { isAbsolute, join } from 'node:path';
import { app, BrowserWindow } from 'electron';
import { accessibilityFixture, accessibilityHost } from './accessibility-host.js';
import { NativeInput } from './native-input.js';
import type { InputOwnership } from './native-input.js';
import { nativeKeyEvents } from './native-key.js';
import { installKeyCounter } from './ergonomics-key-counter.js';
import { NativeExit } from './native-exit.js';
const destination = process.argv.at(-1);
assert(destination && isAbsolute(destination) && !destination.endsWith('.cjs'), 'Absolute private evidence directory required');
const output = destination; mkdirSync(output, { recursive: true, mode: 0o700 });
const termination = new NativeExit(code => app.exit(code));
const observations: { id: string; title: string; status: 'pass' | 'fail'; detail: unknown }[] = [];
const audit: unknown[] = []; const rendererErrors: string[] = []; let sourceIntegrity: unknown = null; let window: BrowserWindow | null = null; let status = 'in-progress'; let failure: string | null = null;
const digest = (bytes: Buffer) => createHash('sha256').update(bytes).digest('hex');
const assets = ['main.cjs', 'preload.cjs', 'import-worker.cjs', 'renderer/index.html', 'renderer/renderer.js', 'renderer/renderer.css', 'ergonomics-native.cjs'].map(path => ({ path, sha256: digest(readFileSync(join(__dirname, path))) }));
const save = () => writeFileSync(join(output, 'observations.json'), JSON.stringify({ format: 'jai.fabric-explorer.ergonomics-keyboard/1', status, failure, expectedCases: 6, observations, audit, assets, rendererErrors, sourceIntegrity, environment: { platform: process.platform, electron: process.versions.electron, chromium: process.versions.chrome, node: process.versions.node, desktop: process.env.XDG_CURRENT_DESKTOP ?? null, sessionType: process.env.XDG_SESSION_TYPE ?? null }, scope: 'One development composition with synthetic automatic picker; actual native keyboard ownership and trusted DOM key events. Not packaged startup, OS-picker, performance, speech, reference-host, foreign-platform or five-user study evidence.' }, null, 2) + '\n');
const abort = (reason: string, code: 1 | 2 | 130) => { if (termination.finished) return; status = code === 130 ? 'interrupted' : 'failed'; failure = reason; save(); termination.finish(code); };
process.once('SIGINT', () => abort('Ctrl+C', 130)); process.once('SIGTERM', () => abort('Parent termination', 130));
const watchdog = setTimeout(() => abort('60-second automated observation watchdog expired', 2), 60000);
async function evaluate<T>(body: string): Promise<T> { assert(window && !window.isDestroyed()); return window.webContents.executeJavaScript(`(async()=>{${body}})()`); }
async function paint(): Promise<void> { await evaluate('await new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)));'); }
async function wait(expression: string, label: string): Promise<void> { assert(await evaluate<boolean>(`const end=performance.now()+10000;while(performance.now()<end){if(${expression})return true;await new Promise(resolve=>requestAnimationFrame(resolve));}return false;`), label); }
const input = new NativeInput({
  acquire: () => { assert(window); window.focus(); window.webContents.focus(); }, paint,
  focus: async expression => { await evaluate(`const item=(${expression});if(!(item instanceof HTMLElement))throw new Error('Native target missing');item.scrollIntoView({block:'nearest'});item.focus();globalThis.__ergonomicTarget=item;`); },
  ownership: async () => { assert(window); const dom = await evaluate<Omit<InputOwnership, 'windowFocused' | 'contentsFocused'>>("const item=globalThis.__ergonomicTarget;return{documentFocused:document.hasFocus(),targetActive:item===document.activeElement,targetVisible:item instanceof HTMLElement&&!!item.getClientRects().length&&getComputedStyle(item).visibility!=='hidden',targetEnabled:item instanceof HTMLElement&&!item.matches(':disabled')&&item.getAttribute('aria-disabled')!=='true'};"); return { ...dom, windowFocused: window.isFocused(), contentsFocused: window.webContents.isFocused() }; },
  send: (key, modifiers, character) => { assert(window); for (const event of nativeKeyEvents(key, modifiers, character)) window.webContents.sendInputEvent({ ...event, modifiers: [...event.modifiers] as ('control' | 'shift' | 'alt')[] }); audit.push({ key, modifiers }); },
  acceptActive: async () => { await evaluate('globalThis.__ergonomicTarget=document.activeElement;'); },
  insert: async value => { assert(window); await window.webContents.insertText(value); },
});
const key = (name: string, modifiers: readonly string[] = []) => input.key(name, modifiers);
const focus = (selector: string) => input.focus(`document.querySelector(${JSON.stringify(selector)})`);
async function activate(selector: string): Promise<void> { await focus(selector); await key('Enter'); }
async function active(id: string): Promise<void> { assert.equal(await evaluate('return document.activeElement?.id;'), id, `Native focus: ${id}`); }
async function openPreferences(): Promise<void> { await focus('#menu-file'); await key('Down'); await key('End'); await active('preferences-open'); await key('Enter'); await wait("document.querySelector('.preferences-dialog')?.open", 'Preferences opened'); await active('theme'); }
async function darkDraft(): Promise<void> { await input.choice("document.querySelector('#theme')", 2, 3, () => evaluate("return document.querySelector('#theme').value==='dark'&&document.activeElement!==document.querySelector('#theme');")); }
function preferenceBytes(root: string): Record<string, string> {
  const result: Record<string, string> = {};
  const walk = (directory: string) => { for (const row of readdirSync(directory, { withFileTypes: true })) { const path = join(directory, row.name); if (row.isDirectory()) walk(path); else if (row.isFile() && row.name === 'preferences.json') result[path] = digest(readFileSync(path)); } };
  walk(root); return result;
}
async function observe(id: string, title: string, action: () => Promise<unknown>): Promise<void> {
  console.log(`${id}/6: ${title}`); const before = await evaluate<{ trusted: number; untrusted: number }>('return {...globalThis.__ergonomicKeys};');
  try { const detail = await action(); const after = await evaluate<{ trusted: number; untrusted: number }>('return {...globalThis.__ergonomicKeys};'); assert(after.trusted > before.trusted, 'Actual trusted native key delivery'); assert.equal(after.untrusted, before.untrusted, 'No synthetic DOM key delivery'); observations.push({ id, title, status: 'pass', detail: { result: detail, trustedKeys: after.trusted - before.trusted } }); save(); }
  catch (error) { observations.push({ id, title, status: 'fail', detail: error instanceof Error ? error.message : String(error) }); throw error; }
}
async function run(): Promise<void> {
  save(); const fixture = accessibilityFixture(__dirname, output); window = await accessibilityHost(__dirname, fixture, false);
  // Wider native geometry keeps both real separators available; no device-support claim is inferred.
  window.setSize(1600, 1000); window.webContents.on('console-message', event => { if (event.level === 'error') rendererErrors.push(event.message); }); window.once('closed', () => abort('Window closed', 130));
  await wait("document.querySelector('#open')&&!document.querySelector('#open').disabled", 'Initial Open control');
  await evaluate("document.querySelector('#open').click();");
  await wait("document.querySelector('#cancel')?.disabled&&(await window.fabricExplorer.getState()).snapshot?.counts.findings==='6'", 'Synthetic import');
  await evaluate(`globalThis.__ergonomicKeys=(${installKeyCounter.toString()})(document);`);
  const initial = await evaluate('return (await window.fabricExplorer.getState()).preferences;'); const beforePreferences = preferenceBytes(join(output, 'application'));
  await observe('1', 'File menu native arrows and Preferences initial focus', async () => { await focus('#menu-file'); await key('Right'); await active('menu-view'); await key('Left'); await active('menu-file'); await openPreferences(); return { initialFocus: 'theme', route: 'File / Down / End / Enter' }; });
  await observe('2', 'Draft, native modal containment and Escape discard', async () => { await darkDraft(); await focus('#theme'); await key('Tab', ['shift']); await active('save'); await key('Escape'); await wait("!document.querySelector('.preferences-dialog')?.open", 'Escape closes modal'); await active('menu-file'); assert.deepEqual(await evaluate('return (await window.fabricExplorer.getState()).preferences;'), initial); assert.deepEqual(preferenceBytes(join(output, 'application')), beforePreferences, 'Escape performs no preference write'); return { draft: 'dark', cancelled: true, focusRestored: 'menu-file' }; });
  await observe('3', 'Real preference Save and native focus restoration', async () => { await openPreferences(); await darkDraft(); await activate('#save'); await wait("!document.querySelector('.preferences-dialog')?.open&&(await window.fabricExplorer.getState()).preferences.theme==='dark'&&document.documentElement.dataset.theme==='dark'", 'Saved theme applied'); await active('menu-file'); assert.notDeepEqual(preferenceBytes(join(output, 'application')), beforePreferences, 'Actual preference file changed'); return { savedTheme: 'dark' }; });
  await observe('4', 'Navigation tab arrows expose the selected real panel', async () => { await activate('#tab-sources'); await key('Right'); await active('tab-search'); assert(await evaluate("return !document.querySelector('#search-content').hidden;")); await key('End'); await active('show-elements'); assert(await evaluate("return !document.querySelector('#elements-content').hidden;")); await key('Home'); await active('tab-sources'); return { selectedTab: 'sources' }; });
  // Owned setup chooses a fixed existing finding through its normal production DOM callback.
  await activate('#tab-findings'); await evaluate("const item=[...document.querySelectorAll('#findings-content .results button')].find(item=>item.textContent.startsWith('F-0001'));if(!item||!item.getClientRects().length)throw new Error('Fixed finding unavailable');item.click();");
  await wait("document.querySelector('[data-testid=selected-label]')?.textContent.startsWith('F-0001')", 'Finding selection');
  const selected = await evaluate<string>("return document.querySelector('[data-testid=selected-id]').textContent;");
  await observe('5', 'Inspector native tab arrows preserve exact selected identity', async () => { await activate('#inspector-tab-overview'); await key('Right'); await active('inspector-tab-relations'); assert(await evaluate("return !document.querySelector('#inspector-relations').hidden;")); await key('End'); await active('inspector-tab-raw'); assert(await evaluate("return !document.querySelector('#inspector-raw').hidden;")); await key('Home'); await active('inspector-tab-overview'); assert.equal(await evaluate("return document.querySelector('[data-testid=selected-id]').textContent;"), selected); return { selected }; });
  await observe('6', 'Both splitter keyboard bounds and reset retain selection', async () => { const widths = []; for (const side of ['navigation', 'inspector']) { await focus(`#${side}-splitter`); const bounds = await evaluate<{ minimum: number; maximum: number }>('return{minimum:Number(document.activeElement.getAttribute("aria-valuemin")),maximum:Number(document.activeElement.getAttribute("aria-valuemax"))};'); const before = await evaluate<number>('return Number(document.activeElement.getAttribute("aria-valuenow"));'); await key('Right'); const after = await evaluate<number>('return Number(document.activeElement.getAttribute("aria-valuenow"));'); assert.equal(after, Math.max(bounds.minimum, Math.min(bounds.maximum, before + (side === 'navigation' ? 8 : -8))), 'Actual 8px step respects the observed geometry bounds'); await key('Home'); assert(await evaluate('return document.activeElement.getAttribute("aria-valuenow")===document.activeElement.getAttribute("aria-valuemin");')); await key('End'); assert(await evaluate('return document.activeElement.getAttribute("aria-valuenow")===document.activeElement.getAttribute("aria-valuemax");')); const resetBounds = await evaluate<{ minimum: number; maximum: number }>('return{minimum:Number(document.activeElement.getAttribute("aria-valuemin")),maximum:Number(document.activeElement.getAttribute("aria-valuemax"))};'); await key('Enter'); assert.equal(await evaluate('return Number(document.activeElement.getAttribute("aria-valuenow"));'), Math.max(resetBounds.minimum, Math.min(resetBounds.maximum, side === 'navigation' ? 276 : 340)), 'Reset default respects the observed geometry bounds'); widths.push({ side, before, after }); } assert.equal(await evaluate("return document.querySelector('[data-testid=selected-id]').textContent;"), selected); return widths; });
  sourceIntegrity = { fabric: { before: digest(fixture.originalFabric), after: digest(readFileSync(fixture.fabric)) }, findings: { before: digest(fixture.originalFindings), after: digest(readFileSync(fixture.findings)) } };
  assert.deepEqual(readFileSync(fixture.fabric), fixture.originalFabric); assert.deepEqual(readFileSync(fixture.findings), fixture.originalFindings); assert.equal(observations.length, 6); assert.deepEqual(rendererErrors, [], 'No unexpected renderer errors');
  status = 'passed'; save(); console.log('6/6 keyboard observations passed; synthetic source bytes unchanged.'); termination.finish(0);
}
void run().catch(error => abort(error instanceof Error ? error.message : String(error), 1)).finally(() => clearTimeout(watchdog));
