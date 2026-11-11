// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Finite development-only DOM journeys through the production shell, preload, reader and graph workers. */
import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { readFileSync, writeFileSync, mkdtempSync, mkdirSync } from 'node:fs';
import { join, resolve, isAbsolute } from 'node:path';
import { app, BrowserWindow } from 'electron';
import { startDesktop } from '../src/shell/electron-shell.js';
import { ReadBroker } from '../src/broker/read-broker.js';
import { ImportSession } from '../src/import/session.js';
import { NativeImportWorker } from '../src/import/worker-client.js';
import { NativeExit } from './native-exit.js';
import { assertCanvasReport } from './canvas-report.js';
const termination = new NativeExit(code => app.exit(code));
const directory = __dirname;
const presentationReady = "document.querySelector('.graph-canvas')?.getAttribute('data-canvas-ready') === 'true' && !!document.querySelector('#fit-graph') && !document.querySelector('#fit-graph').disabled";
const focused = process.argv.includes('--focused');
const destination = process.argv.at(-1);
if (!destination || !isAbsolute(destination) || destination.endsWith('.cjs')) { console.error('One absolute evidence directory is required'); termination.finish(2); }
const output = mkdtempSync(join(destination!, 'viewer-'));
const repository = resolve(directory, '../../../..');
// Python is used only by the synthetic fixture writer before import.
const configuration = { executable: join(repository, 'build/fabric-explorer/helper-venv', process.platform === 'win32' ? 'Scripts/python.exe' : 'bin/python'), coreTools: join(repository, '.ai/runtime/tools') };
const sourceDirectory = join(output, 'synthetic-source'); mkdirSync(sourceDirectory, { mode: 0o700 });
const created = JSON.parse(execFileSync(configuration.executable, ['-I', '-B', join(repository, 'apps/fabric-explorer/reader/test/make_fabric_fixture.py'), sourceDirectory], { timeout: 20000, maxBuffer: 1024 * 1024, encoding: 'utf8' })) as { filename: string };
const fabric = join(sourceDirectory, created.filename); const findings = join(sourceDirectory, 'review.jsonl');
writeFileSync(findings, readFileSync(join(repository, 'apps/fabric-explorer/test/fixtures/findings-review.jsonl')), { mode: 0o600 });
const originalFabric = readFileSync(fabric); const originalFindings = readFileSync(findings);
const applicationData = join(output, 'application'); mkdirSync(applicationData, { mode: 0o700 }); app.setPath('appData', applicationData);
const observations: { step: number; title: string; status: 'pass'; detail?: unknown }[] = [];
let canvasReport: unknown = null;
const errors: string[] = []; let window: BrowserWindow; let step = 0; const total = focused ? 7 : 15;
const watchdog = setTimeout(() => { console.error(`Viewer failed at ${step}/${total}: 150-second total watchdog expired.`); termination.finish(2); }, 150000);
const progress = (title: string) => { step++; console.log(`Step ${step}/${total}: ${title}`); };
const done = (title: string, detail?: unknown) => observations.push({ step, title, status: 'pass', ...(detail === undefined ? {} : { detail }) });
async function evaluate<T>(body: string): Promise<T> { return window.webContents.executeJavaScript(`(async () => { ${body} })()`); }
async function wait(expression: string, label: string, timeout = 12000): Promise<void> {
  assert.equal(await evaluate<boolean>(`const end = performance.now() + ${timeout}; while (performance.now() < end) { if (${expression}) return true; await new Promise(resolve => requestAnimationFrame(resolve)); } return false;`), true, label);
}
async function click(selector: string): Promise<void> { if (['#tab-sources', '#tab-search', '#tab-findings', '#show-elements'].includes(selector) && await evaluate<boolean>("return !!document.querySelector('.navigation-pane')?.hidden;")) await click('#show-navigation'); if (selector.startsWith('#inspector-tab-') && await evaluate<boolean>("return !!document.querySelector('.inspector')?.hidden;")) await click('#show-inspector'); await evaluate(`const control = document.querySelector(${JSON.stringify(selector)}); if (!control || control.disabled || !control.getClientRects().length) throw new Error('Required enabled control unavailable'); control.click();`); }
async function value(selector: string, next: string): Promise<void> { await evaluate(`const control = document.querySelector(${JSON.stringify(selector)}); if (!control || !control.getClientRects().length) throw new Error('Required input unavailable'); const setter = Object.getOwnPropertyDescriptor(control.tagName === 'SELECT' ? HTMLSelectElement.prototype : HTMLInputElement.prototype, 'value').set; setter.call(control, ${JSON.stringify(next)}); control.dispatchEvent(new Event(control.tagName === 'SELECT' ? 'change' : 'input', {bubbles:true}));`); }
async function capture(name: string, graphExpected = true): Promise<void> {
  if (graphExpected) await wait(presentationReady, 'Current graph committed before capture');
  await evaluate("await new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve))); ");
  writeFileSync(join(output, `${name}.png`), (await window.webContents.capturePage()).toPNG());
}
async function run(): Promise<void> {
  progress('Start isolated production shell and local synthetic source picker');
  await startDesktop({ picker: { project: async () => sourceDirectory, files: async family => [family === 'findings' ? findings : fabric] },
    createBroker: (_paths, registry, writeRoots) => new ReadBroker({ registry, writeRoots }),
    createImport: (input, broker, paths) => { assert(broker instanceof ReadBroker); return new ImportSession({ ...input, broker, archiveDirectory: join(paths.temp, 'captures'), workerFactory: () => new NativeImportWorker(join(directory, 'import-worker.cjs')) }); },
  }, directory);
  window = BrowserWindow.getAllWindows()[0]!; assert(window); window.setSize(1440, 1100);
  window.once('closed', () => { if (!termination.finished) { console.error(`Stopped at ${step}/${total}; remaining steps will not run.`); termination.finish(130); } });
  window.webContents.on('console-message', event => { if (event.level === 'error') errors.push(event.message); if (event.message.startsWith('Canvas check ')) console.log(event.message); });
  await wait("document.querySelector('#open') && !document.querySelector('#open').disabled", 'initial source control'); done('Production shell ready');
  progress('U01: open explicit sources and import one observed revision set');
  await click('#open');
  await wait("document.querySelector('[data-testid=count-findings]')?.textContent === '6' && document.querySelector('#cancel').disabled && document.querySelector('.semantic-panel tbody button') && (" + presentationReady + ")", 'recorded graph and current display ready', 30000);
  assert(await evaluate<boolean>("return document.querySelector('#snapshot-provenance')?.textContent.includes('recorded') && document.querySelector('#snapshot-provenance')?.textContent.includes('Replay');")); done('Fabric and findings imported');
  if (!focused) {
  progress('U02: search an exact visible identity and inspect that same element');
  await click('#show-elements'); const identity = await evaluate<string>("return document.querySelector('.semantic-panel tbody button').dataset.elementId;"); await click('#tab-search'); await value('#search-text', identity);
  await evaluate("document.querySelector('#search-text').form.requestSubmit();"); await wait("document.querySelector('#search-content .results button')?.title === " + JSON.stringify(identity), 'exact identity search'); await click('#search-content .results button'); await wait("document.querySelector('[data-testid=selected-id]')?.textContent === " + JSON.stringify(identity), 'exact inspector selection'); await click('#inspector-tab-raw'); done('Exact-ID selection', { identity });
  progress('U03: select a recorded relation and expose endpoints, arrow and evidence');
  await click('#show-elements'); await value('#element-kind', 'edges'); await wait("document.querySelector('.semantic-panel tbody button')", 'relation list'); await click('.semantic-panel tbody button'); await wait("document.querySelector('#inspector-heading')?.textContent === 'Relation inspector'", 'relation inspector');
  await click('#inspector-tab-relations'); const relation = await evaluate<string>("return document.querySelector('.inspector').textContent;"); assert(relation.includes('From → To, as recorded')); assert(relation.includes('Recorded relation basis')); assert(relation.includes('Source evidence'));
  await capture('relation-100'); await click('#inspector-tab-evidence'); await capture('relation-evidence-100'); done('Inspectable recorded relation', { inspectorText: relation });
  progress('U04: select a finding and expose subject candidates or unresolved evidence');
  await click('#tab-findings'); await wait("document.querySelector('#finding-text').form.parentElement.querySelector('.results button')", 'findings list'); await evaluate("document.querySelector('#finding-text').form.parentElement.querySelector('.results button').click();");
  await wait("document.querySelector('[aria-label=\"Finding subjects\"]')", 'finding subjects'); await click('#inspector-tab-relations'); await capture('finding-100'); const subjectEvidence = await evaluate<string>("return document.querySelector('[aria-label=\"Finding subjects\"]').textContent;");
  const subject = await evaluate<string>("return document.querySelector('[aria-label=\"Finding subjects\"] li code').textContent;"); await evaluate("document.querySelector('[aria-label=\"Finding subjects\"] li button').click();"); await wait("document.querySelector('[data-testid=selected-id]')?.textContent === " + JSON.stringify(subject), 'exact finding subject navigation'); await click('#inspector-tab-raw'); done('Finding subject evidence and exact navigation', { subjects: subjectEvidence, selected: subject });
  progress('U05: exercise camera controls and bounded visible element navigation');
  await wait(presentationReady, 'Current graph committed before camera input');
  await click('#zoom-in'); await click('#zoom-out'); await click('#fit-graph');
  assert(await evaluate<boolean>("return document.querySelector('.visible-graph-counts').textContent.includes('Hidden globally:');")); done('Bounded graph and camera controls');
  progress('Apply an exact filter, then reset without changing source or generation');
  await click('#tab-search'); await click('#search-filters'); await value('#filter-state', 'open'); await wait("document.querySelector('[data-testid=count-findings]')?.textContent === '1' && !document.querySelector('#status').textContent.includes('Working:')", 'filter work quiescence'); await click('#reset-filters'); await wait("document.querySelector('[data-testid=count-findings]')?.textContent === '6' && !document.querySelector('#status').textContent.includes('Working:')", 'filter reset'); done('Reversible filters');
  progress('Read captured source bytes through the selected record locator');
  await click('#inspector-tab-evidence'); await click('#read-source'); await wait("document.querySelector('#source-text')?.textContent.length > 0", 'captured source'); done('Captured byte page', await evaluate("return document.querySelector('#source-text').textContent.slice(0,200);"));
  progress('Verify keyboard search focus and reversible navigation controls');
  await click('#back'); await wait("document.querySelector('[data-testid=count-findings]')?.textContent === '1'", 'history restores filtered intent'); await click('#forward'); await wait("document.querySelector('[data-testid=count-findings]')?.textContent === '6'", 'forward restores reset filters');
  window.webContents.sendInputEvent({ type: 'keyDown', keyCode: 'Escape' }); window.webContents.sendInputEvent({ type: 'keyUp', keyCode: 'Escape' });
  await evaluate("document.activeElement?.blur();"); window.webContents.sendInputEvent({ type: 'keyDown', keyCode: 'K', modifiers: ['control'] }); window.webContents.sendInputEvent({ type: 'keyUp', keyCode: 'K', modifiers: ['control'] }); await wait("document.activeElement?.id === 'search-text'", 'keyboard search focus');
  window.webContents.sendInputEvent({ type: 'keyDown', keyCode: 'Tab' }); window.webContents.sendInputEvent({ type: 'keyUp', keyCode: 'Tab' }); await wait("document.activeElement?.tagName === 'BUTTON' && document.activeElement?.textContent === 'Search'", 'native forward tab order');
  window.webContents.sendInputEvent({ type: 'keyDown', keyCode: 'Tab', modifiers: ['shift'] }); window.webContents.sendInputEvent({ type: 'keyUp', keyCode: 'Tab', modifiers: ['shift'] }); await wait("document.activeElement?.id === 'search-text'", 'native reverse tab order'); done('Keyboard search focus and native tab order');
  progress('Capture actual production presentation at 150% and 200% scale');
  window.webContents.setZoomFactor(1.5); await evaluate("await new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)));"); await capture('viewer-150');
  window.webContents.setZoomFactor(2); await evaluate("await new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)));"); await capture('viewer-200'); window.webContents.setZoomFactor(1); done('Scaled production captures');
  }
  progress('U06: verify source integrity and successful coherent refresh');
  assert.deepEqual(readFileSync(fabric), originalFabric); assert.deepEqual(readFileSync(findings), originalFindings);
  const priorGeneration = await evaluate<string>("return document.querySelector('#snapshot-state').textContent;");
  // Only the test driver writes this synthetic fixture, through its maintained canonical writer.
  execFileSync(configuration.executable, ['-I', '-B', '-c', "import os,sys; os.environ['FINDINGS_HOME']=sys.argv[2]; sys.dont_write_bytecode=True; sys.path.insert(0,sys.argv[1]); import findings; events=findings.load('review'); findings.append('review',events,[{'op':'resolve','id':'F-0001','by':'synthetic-viewer-author','note':'Synthetic successful refresh','ref':None}])", configuration.coreTools, sourceDirectory], { timeout: 10000 });
  const updatedFindings = readFileSync(findings); assert(updatedFindings.length > originalFindings.length); await click('#refresh');
  await wait("document.querySelector('#snapshot-state').textContent !== " + JSON.stringify(priorGeneration) + " && !document.querySelector('#status').textContent.includes('Working:') && document.querySelector('[data-testid=count-findings]')?.textContent === '6' && (" + presentationReady + ")", 'successful coherent generation and display replacement', 30000);
  assert.deepEqual(readFileSync(findings), updatedFindings); assert.equal(await evaluate("return document.querySelector('#source-text');"), null); done('Source integrity and successful generation replacement');
  progress('U06/U07: malformed refresh retains the accepted snapshot and diagnostic');
  const generation = await evaluate<string>("return document.querySelector('#snapshot-state').textContent;"); const malformed = originalFabric.subarray(0, originalFabric.length - 2); writeFileSync(fabric, malformed);
  await click('#refresh'); await wait("document.querySelector('.warning')?.textContent.includes('Previous snapshot retained')", 'failed refresh retains accepted view', 30000);
  assert.equal(await evaluate("return document.querySelector('#snapshot-state').textContent;"), generation); assert.deepEqual(readFileSync(fabric), malformed); done('Failed refresh preserves accepted snapshot');
  progress('Compare two actual SDK program configurations, then run eleven finite production canvas checks');
  await window.webContents.executeJavaScript(readFileSync(join(directory, 'canvas-native.js'), 'utf8'));
  const sdkPrograms = await evaluate<{ status: string }>("return CanvasNative.runSdkNativeComparison(document.body);");
  writeFileSync(join(output, 'sdk-program-observations.json'), JSON.stringify(sdkPrograms, null, 2) + '\n');
  assert.equal(sdkPrograms.status, 'pass', 'Actual SDK program comparison; counts retained in sdk-program-observations.json');
  canvasReport = await evaluate("return CanvasNative.runCanvasNativeChecks(document.body);");
  writeFileSync(join(output, 'canvas-observations.json'), JSON.stringify(canvasReport, null, 2) + '\n');
  assertCanvasReport(canvasReport); done('Actual canvas checks', canvasReport);
  progress('Close sources and verify no semantic graph remains visible');
  await click('#close'); await wait("document.querySelector('#snapshot-state')?.textContent === 'No snapshot imported.' && document.querySelectorAll('.graph-canvas canvas').length === 0", 'close clears canvas'); done('Closed source and canvas ownership');
  progress('Save exact observations and release the native window');
  assert.equal(step, total); writeFileSync(fabric, originalFabric); writeFileSync(findings, originalFindings); await capture('closed-100', false); done('Saved observations and closed sources');
  const report = { format: 'jai.fabric-explorer.viewer-journeys/1', mode: focused ? 'focused-native-recheck' : 'full', platform: process.platform, electron: process.versions.electron, observations, consoleErrors: errors, scope: 'actual Linux production DOM/preload/direct worker; synthetic inputs only; no GPU performance or cross-platform qualification' };
  writeFileSync(join(output, 'observations.json'), JSON.stringify(report, null, 2) + '\n'); clearTimeout(watchdog);
  console.log(`Viewer journeys PASS: ${step}/${total}; evidence=${output}`); termination.finish(0);
}
void run().catch(error => { clearTimeout(watchdog); writeFileSync(join(output, 'failure.json'), JSON.stringify({ step, total, error: error instanceof Error ? error.message : 'Unknown native failure', observations, canvas: canvasReport, consoleErrors: errors }, null, 2)); console.error(`Viewer journeys FAIL at ${step}/${total}: ${error instanceof Error ? error.message : 'Unknown failure'}; evidence=${output}`); termination.finish(1); });
