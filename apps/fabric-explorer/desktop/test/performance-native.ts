// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Development-only finite performance observations of the actual sandboxed production composition. */
import assert from 'node:assert/strict';
import { appendFileSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { isAbsolute, join } from 'node:path';
import { monitorEventLoopDelay, performance } from 'node:perf_hooks';
import { app, BrowserWindow, screen, session } from 'electron';
import type { Counts, SourceRevision } from '@jai/fabric-explorer-contracts';
import { startDesktop } from '../src/shell/electron-shell.js';
import { initializeApplicationPaths } from '../src/shell/paths.js';
import { ReadBroker } from '../src/broker/read-broker.js';
import { importProgressText } from '../src/import/progress.js';
import { ImportSession } from '../src/import/session.js';
import { NativeImportWorker } from '../src/import/worker-client.js';
import type { ImportWorkerPort } from '../src/import/worker-client.js';
import { assertPerformanceRevisions, loadPerformanceSourceSet } from './performance-corpus.js';
import type { PerformanceSourceSet } from './performance-corpus.js';
import { activeFrameIntervals, assessMeasurements } from './performance-metrics.js';
import { animationCoverage, importOverviewReady, PERFORMANCE_POPULATIONS, remainingLImportWait, L_IMPORT_TAIL_MS } from './performance-plan.js';
import { fitCommittedOverview, prepareNativeFocus, performObservedDrag } from './performance-activity.js';
import type { NativePerformanceInput } from './performance-plan.js';
import { performanceLookupSeeds } from './performance-seeds.js';
import type { PerformanceIdentitySeed } from './performance-seeds.js';
import { rendererCpuProfileEnabled, RendererCpuProfiler } from './renderer-cpu-profile.js';

const [inputPath, outputArgument] = process.argv.slice(2);
assert(inputPath && outputArgument && isAbsolute(inputPath) && isAbsolute(outputArgument), 'Absolute case input and evidence directory required.');
const output = outputArgument;
const input = JSON.parse(readFileSync(inputPath, 'utf8')) as NativePerformanceInput;
assert.equal(input.format, 'jai.fabric-explorer.performance-case/1');
assert(Number.isSafeInteger(input.ordinal) && input.ordinal >= 1 && input.ordinal <= input.total);
assert(input.definition.watchdogMs > 0 && input.definition.watchdogMs <= 3600000);
assert(['blank', 'shell', 'import', 'queries', 'animation', 'retention', 'faults', 'endurance'].includes(input.definition.kind));
const kind = input.definition.kind;
const rendererProfileDiagnostic = rendererCpuProfileEnabled(input.mode, input.rendererCpuProfile);
assert(!rendererProfileDiagnostic || kind === 'import' && input.definition.tier === 'S' && input.total === 1 && input.ordinal === 1, 'CPU profiling is limited to the single S smoke case.');
const stages = { blank: 3, shell: 3, import: 6, queries: 10, animation: 6, retention: 32, faults: 8, endurance: 6 }[kind];
const stateRoot = join(output, 'application'); mkdirSync(stateRoot, { mode: 0o700, recursive: true }); app.setPath('appData', stateRoot);
const loopDelay = monitorEventLoopDelay({ resolution: 10 }); loopDelay.enable();
const observations: { stage: number; title: string; value: unknown }[] = [];
const errors: string[] = []; let errorCount = 0; let stage = 0; let finished = false; let failure: string | null = null;
let window: BrowserWindow | null = null; let selected: PerformanceSourceSet | null = null;
let importMs: number | null = null; let observedSnapshot: { counts: Counts; sources: SourceRevision[]; generation: string } | null = null;
let metadata: unknown = null; let animation: unknown = null; let rendererTasks: unknown = null;
let rendererCpuDiagnostic: Record<string, unknown> | null = null; let activeRendererProfiler: RendererCpuProfiler | null = null;
let importStartedMs: number | null = null;
let profileRoi: { startedMs: number; endedMs: number | null; timeOriginMs: number } | null = null;
let enduranceWatchdog: ReturnType<typeof setTimeout> | null = null;
let pendingWorkerCalls = 0; let createdWorkers = 0; let terminatedWorkers = 0; let killNextCandidate = false; let workerFaultTriggered = false;
const ownedWorkers = new Set<ImportWorkerPort>();
const event = (name: string, value: unknown) => console.log('JAI_PERF_EVENT ' + JSON.stringify({ name, monotonicNs: String(process.hrtime.bigint()), value }));
const counters = () => ({ ownedWorkers: ownedWorkers.size, pendingWorkerCalls, createdWorkers, terminatedWorkers });
const report = () => ({ format: 'jai.fabric-explorer.performance-native/1', case: input, status: finished ? failure ? 'failed' : 'collected' : 'in-progress', stage, stages, observations, failure, errors, errorCount, metadata, importMs, snapshot: observedSnapshot, animation, rendererTasks, counters: counters(),
  importTimingMethod: 'Main ImportSession.import entry to usable renderer overview, including layout; Open admission excluded. Automatic Open/import flow.',
  measurementPurpose: rendererProfileDiagnostic ? 'renderer-cpu-diagnostic-only-not-timing-or-RSS-qualification' : 'performance-observation', rendererCpuDiagnostic,
  inspectorTimingMethod: 'Real semantic-row selection through exact ID displayed in expanded Raw identity details; tab and details activation are included when needed.',
  overviewReadinessMethod: 'Committed visible graph plus indexed semantic table availability; Elements tab may be inactive until selection observations explicitly reveal it.',
  mainLoopGap: { method: 'monitorEventLoopDelay polling delay, not individual task duration', coverage: 'partial-for-strict-main-UI-task-gate', resolutionMs: 10, count: loopDelay.count, maximumMs: loopDelay.count ? loopDelay.max / 1000000 : null },
  limits: ['Current-host development composition only; no packaged or minimum-reference-host qualification.', 'No append/malformed source mutation is performed; prior matching functional evidence is separate.', 'Worker ownership counters do not establish OS-thread or strict main-task coverage.'] });
const save = () => writeFileSync(join(output, 'native-observations.json'), JSON.stringify(report(), null, 2) + '\n', { mode: 0o600 });
function begin(title: string): void { assert(stage < stages); stage++; console.log(`Případ ${input.ordinal}/${input.total} · ${input.definition.id} · krok ${stage}/${stages}: ${title}`); event('stage', { stage, stages, title }); save(); }
function observed(title: string, value: unknown): void { observations.push({ stage, title, value }); save(); }
function stop(reason: string, code = 130): void { if (finished) return; failure = reason; finished = true; try { activeRendererProfiler?.abort(); if (rendererCpuDiagnostic && activeRendererProfiler) rendererCpuDiagnostic.cleanupErrors = activeRendererProfiler.cleanupErrors(); save(); event('stopped', { reason, code }); console.error(`Test ukončen: ${reason}. Další kroky tohoto případu se nespustí.`); } finally { app.exit(code); } }
const caseStartedMs = performance.now();
const watchdog = setTimeout(() => stop('Vypršel pevný diagnostický limit případu.', 2), input.definition.watchdogMs);
process.once('SIGTERM', () => stop('Zastavení nadřazeným testem.')); process.once('SIGINT', () => stop('Ctrl+C.'));
async function evaluate<T>(body: string): Promise<T> { assert(window && !window.isDestroyed()); return window.webContents.executeJavaScript(`(async()=>{${body}})()`); }
async function wait(expression: string, title: string, milliseconds = 15000, failureExpression = 'false'): Promise<void> {
  const ok = await evaluate<boolean>(`const end=performance.now()+${milliseconds};while(performance.now()<=end){if(${expression})return true;if(${failureExpression})throw new Error('Observed operation rejection before watchdog');await new Promise(resolve=>requestAnimationFrame(resolve));}return false;`);
  assert(ok, title);
}
async function click(selector: string): Promise<void> { if (['#tab-sources', '#tab-search', '#tab-findings', '#show-elements'].includes(selector) && await evaluate<boolean>("return !!document.querySelector('.navigation-pane')?.hidden;")) await click('#show-navigation'); if (selector.startsWith('#inspector-tab-') && await evaluate<boolean>("return !!document.querySelector('.inspector')?.hidden;")) await click('#show-inspector'); await evaluate(`const item=document.querySelector(${JSON.stringify(selector)});if(!(item instanceof HTMLButtonElement)||item.disabled||!item.getClientRects().length)throw new Error('Required enabled control unavailable: '+${JSON.stringify(selector)});item.click();`); }
async function setValue(selector: string, value: string): Promise<void> { await evaluate(`const item=document.querySelector(${JSON.stringify(selector)});if(!item||!item.getClientRects().length)throw new Error('Required input unavailable');Object.getOwnPropertyDescriptor(item.tagName==='SELECT'?HTMLSelectElement.prototype:HTMLInputElement.prototype,'value').set.call(item,${JSON.stringify(value)});item.dispatchEvent(new Event(item.tagName==='SELECT'?'change':'input',{bubbles:true}));`); }
async function idle(milliseconds: number): Promise<void> { const until = performance.now() + milliseconds; while (performance.now() < until) await new Promise<void>(resolve => setTimeout(resolve, Math.max(1, Math.ceil(until - performance.now())))); }
const quiet = "!document.querySelector('#status')?.textContent.includes('Working:') && document.querySelector('#cancel')?.disabled";

function worker(): ImportWorkerPort {
  const native = new NativeImportWorker(join(__dirname, 'import-worker.cjs')); createdWorkers++;
  const track = async <T>(work: () => Promise<T>): Promise<T> => { pendingWorkerCalls++; try { return await work(); } finally { pendingWorkerCalls--; } };
  let stopped = false;
  const port: ImportWorkerPort = {
    initialize: value => track(() => native.initialize(value)),
    consume: value => track(() => native.consume(value)),
    importDirect: (input, materialAvailable, signal, progress) => track(async () => {
      const pending = native.importDirect(input, materialAvailable, signal, value => { progress?.(value); console.log(`Import progress: ${importProgressText(value)}`); });
      if (killNextCandidate) { killNextCandidate = false; workerFaultTriggered = true; await Promise.all([pending, port.terminate()]); }
      return await pending;
    }),
    finish: () => track(() => native.finish()), span: (source, pointer, sequence) => track(() => native.span(source, pointer, sequence)),
    queryStart: (value, signal) => track(() => native.queryStart(value, signal)), searchFindings: (value, signal) => track(() => native.searchFindings(value, signal)),
    filterProjection: (value, signal) => track(() => native.filterProjection(value, signal)), queryNext: (value, signal) => track(() => native.queryNext(value, signal)), queryDrop: value => track(() => native.queryDrop(value)),
    layout: (value, signal) => track(() => native.layout(value, signal)), groups: (value, signal) => track(() => native.groups(value, signal)),
    terminate: async () => { try { await native.terminate(); } finally { if (!stopped) { stopped = true; terminatedWorkers++; ownedWorkers.delete(port); } } },
  };
  ownedWorkers.add(port); return port;
}

async function instrument(): Promise<void> {
  await evaluate(`const state={tasks:[],dropped:0,startedMs:performance.now(),observer:null};if(PerformanceObserver.supportedEntryTypes.includes('longtask')){state.observer=new PerformanceObserver(list=>{for(const item of list.getEntries()){if(state.tasks.length<10000)state.tasks.push({startTime:item.startTime,duration:item.duration});else state.dropped++;}});state.observer.observe({type:'longtask',buffered:false});}window.__jaiPerformance=state;
    const button=document.createElement('button');button.textContent='Zastavit celý test';button.id='jai-performance-stop';button.style.cssText='position:fixed;right:8px;top:4px;z-index:2147483647';button.addEventListener('click',()=>console.log('JAI_PERF_STOP'));document.body.append(button);window.addEventListener('keydown',e=>{if(e.key==='Escape'){e.preventDefault();e.stopImmediatePropagation();console.log('JAI_PERF_STOP');}},true);`);
}
async function start(): Promise<void> {
  begin('Spuštění pevné aplikace se zapnutým sandboxem.');
  const observeConsole = (_event: Electron.Event, contents: Electron.WebContents) => contents.on('console-message', item => { if (item.message === 'JAI_PERF_STOP') stop('Tlačítko Zastavit nebo Escape.'); if (item.level === 'error') { errorCount++; if (errors.length < 100) errors.push(item.message); } });
  app.on('web-contents-created', observeConsole);
  if (kind === 'blank') {
    initializeApplicationPaths({ appData: () => stateRoot, setPath: (name, value) => app.setPath(name, value), setLogsPath: value => app.setAppLogsPath(value), setCachePath: value => app.commandLine.appendSwitch('disk-cache-dir', value), setTemporaryEnvironment: value => { process.env.TMPDIR = value; process.env.TEMP = value; process.env.TMP = value; } });
    await app.whenReady(); const local = session.fromPartition('fabric-explorer-performance-blank', { cache: false }); local.setSpellCheckerLanguages([]); local.setSpellCheckerEnabled(false);
    window = new BrowserWindow({ width: 1920, height: 1080, webPreferences: { sandbox: true, contextIsolation: true, nodeIntegration: false, spellcheck: false, session: local } }); await window.loadURL('about:blank');
  } else {
    if (input.manifest) selected = await loadPerformanceSourceSet(input.manifest, 'base');
    await startDesktop({ picker: { project: async () => selected?.sources[0]?.projectPath ?? null, files: async family => selected?.sources.filter(source => source.family === family).map(source => source.path) ?? [] },
      createBroker: (_paths, registry, writeRoots) => new ReadBroker({ registry, writeRoots }),
      createImport: (selection, broker, paths) => {
        assert(broker instanceof ReadBroker);
        const importer = new ImportSession({ ...selection, broker, archiveDirectory: join(paths.temp, 'captures'), workerFactory: worker });
        const original = importer.import.bind(importer);
        // Observe the real service entry after admission; preserve its receiver and arguments.
        importer.import = (...args) => { importStartedMs = performance.now(); return original(...args); };
        return importer;
      },
    }, __dirname);
    window = BrowserWindow.getAllWindows()[0] ?? null; assert(window);
    await wait("document.querySelector('#open')&&!document.querySelector('#open').disabled", 'Production shell ready', 12000);
  }
  window.setContentSize(1920, 1080); window.webContents.setZoomFactor(1); window.focus();
  app.off('web-contents-created', observeConsole);
  window.on('closed', () => { if (!finished) stop('Testovací okno bylo zavřeno.'); });
  event('shell-ready', { kind });
  metadata = { platform: process.platform, architecture: process.arch, electron: process.versions.electron, chromium: process.versions.chrome, node: process.versions.node,
    gpu: await app.getGPUInfo('complete'), gpuFeatures: app.getGPUFeatureStatus(), display: screen.getDisplayMatching(window.getBounds()), viewport: await evaluate('return {width:innerWidth,height:innerHeight,scale:devicePixelRatio,visibility:document.visibilityState};'), focused: window.isFocused(), processRoles: app.getAppMetrics().map(row => ({ pid: row.pid, type: row.type, name: row.name ?? null })),
    cachePolicy: { mesaShaderCacheDisabled: process.env.MESA_SHADER_CACHE_DISABLE === 'true', xdgCacheHome: process.env.XDG_CACHE_HOME, settingsBackend: process.env.GSETTINGS_BACKEND }, artifact: 'compiled-development-composition', referenceHostEnrolled: false };
  if (kind !== 'blank') await instrument(); observed('Initial native environment', metadata);
}
/** Start the actual Open-to-import UI flow; profiling begins before any import work. */
async function open(): Promise<void> {
  assert(selected); importStartedMs = null; profileRoi = null;
  if (rendererProfileDiagnostic) {
    assert(window && !window.isDestroyed()); const target = window.webContents;
    activeRendererProfiler = new RendererCpuProfiler({ attach: () => target.debugger.attach('1.3'), command: (method, parameters) => target.debugger.sendCommand(method, parameters), detach: () => target.debugger.detach() });
    rendererCpuDiagnostic = { purpose: 'diagnostic-only', status: 'starting', samplingIntervalUs: 1000 };
    await activeRendererProfiler.start();
    profileRoi = await evaluate('return {startedMs:performance.now(),endedMs:null,timeOriginMs:performance.timeOrigin};');
  }
  await click('#open');
}
function usableOverviewExpression(): string { return `(()=>{const stage=document.querySelector('.graph-canvas');const canvas=stage?.querySelector('canvas.sigma-stage');const bounds=canvas?.getBoundingClientRect();const style=stage?getComputedStyle(stage):null;return (${importOverviewReady.toString()})({quiet:!!(${quiet}),canvasPresent:!!canvas,tablePresent:!!document.querySelector('.semantic-panel tbody button'),fitEnabled:!!document.querySelector('#fit-graph')&&!document.querySelector('#fit-graph').disabled,visible:!!stage&&stage.getAttribute('aria-hidden')!=='true'&&style?.visibility==='visible'&&style?.display!=='none',width:bounds?.width??0,height:bounds?.height??0});})()`; }
async function importSources(): Promise<void> {
  const importWaitMs = input.definition.tier === 'L' ? remainingLImportWait(caseStartedMs, performance.now(), input.definition.watchdogMs) : 120000;
  if (importWaitMs <= 0) throw new Error('Existing case diagnostic window exhausted before Import.');
  if (input.definition.tier === 'L') observed('Remaining L diagnostic window', { importWaitMs, totalCaseMs: input.definition.watchdogMs, reservedTailMs: L_IMPORT_TAIL_MS, acceptanceBudgetMs: 45000, acceptanceUnchanged: true });
  const profiler = activeRendererProfiler; const roi = profileRoi;
  let importFailed = false; let usable = false;
  try {
    await wait(usableOverviewExpression(), 'Usable indexed overview and layout', importWaitMs, "document.querySelector('#cancel')?.disabled&&/Import (?:failed|rejected)/.test(document.querySelector('#status')?.textContent??'')");
    const endedMs = await evaluate<number>('await new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)));return performance.now();');
    if (roi) roi.endedMs = endedMs;
    assert(importStartedMs !== null, 'Automatic import reached the real service entry');
    usable = true; importMs = performance.now() - importStartedMs; event('import-ready', { importMs });
  } catch (error) {
    importFailed = true; if (rendererCpuDiagnostic) { rendererCpuDiagnostic.status = 'failed'; rendererCpuDiagnostic.error = error instanceof Error ? error.message : 'Import/profile failure'; }
    throw error;
  } finally {
    if (profiler) {
      try {
        const profile = await profiler.stop(); const { json, ...profileMetadata } = profile;
        writeFileSync(join(output, 'renderer-cpu.cpuprofile'), json, { mode: 0o600, flag: 'wx' });
        rendererCpuDiagnostic = { purpose: 'diagnostic-only-not-timing-or-RSS-qualification', status: usable ? 'collected' : 'partial-import-not-usable', file: 'renderer-cpu.cpuprofile', browserOpenToReadyRoi: roi, importEntryEpochMs: importStartedMs === null ? null : performance.timeOrigin + importStartedMs, clockMapping: 'Node performance.timeOrigin + import entry performance.now; browser ROI uses its own timeOrigin.', ...profileMetadata };
      } catch (error) {
        if (rendererCpuDiagnostic) { rendererCpuDiagnostic.status = 'failed'; rendererCpuDiagnostic.profileError = error instanceof Error ? error.message : 'Profile capture failure'; }
        if (!importFailed) throw error;
      } finally {
        await profiler.dispose(); if (rendererCpuDiagnostic) rendererCpuDiagnostic.cleanupErrors = profiler.cleanupErrors(); activeRendererProfiler = null;
      }
    }
  }
}
async function verify(): Promise<void> {
  assert(selected);
  const state = await evaluate<{ snapshot: { counts: Counts; sources: SourceRevision[]; generation: string } }>('return window.fabricExplorer.getState();'); assert(state.snapshot);
  assertPerformanceRevisions(selected, state.snapshot.sources);
  for (const key of ['vertices', 'edges', 'findings'] as const) if (selected.expected[key] !== null) assert.equal(state.snapshot.counts[key], selected.expected[key], `Actual ${key}`);
  observedSnapshot = state.snapshot; observed('Actual captured revisions and counts', state.snapshot);
}
async function close(): Promise<void> {
  await click('#close'); await wait("document.querySelector('#snapshot-state')?.textContent==='No snapshot imported.'&&document.querySelectorAll('.graph-canvas canvas').length===0", 'Source closure clears graph');
  assert.equal(ownedWorkers.size, 0, 'No retained graph workers after close'); assert.equal(pendingWorkerCalls, 0, 'No pending observed worker calls after close');
}
async function selectTable(kindValue: 'vertices' | 'edges', ordinal: number): Promise<{ id: string; durationMs: number }> {
  await click('#show-elements');
  await setValue('#element-kind', kindValue); await wait("document.querySelector('.semantic-panel caption')?.textContent.includes(" + JSON.stringify(kindValue === 'vertices' ? 'Visible vertices' : 'Visible relations') + ")&&document.querySelector('.semantic-panel tbody button')", 'Current semantic table');
  return evaluate(`const buttons=[...document.querySelectorAll('.semantic-panel tbody button')];const button=buttons[${ordinal}%buttons.length];if(!button)throw new Error('No selection candidate');const id=button.dataset.elementId;if(document.querySelector('[data-testid=selected-id]')?.textContent===id)throw new Error('Selection must change identity for timing');const start=performance.now();button.click();while(performance.now()-start<15000){if(document.querySelector('[data-testid=selected-id]')?.textContent===id&&!document.querySelector('#status')?.textContent.includes('Working:')){const raw=document.querySelector('#inspector-tab-raw');if(raw?.getAttribute('aria-selected')!=='true')raw?.click();else{const exact=document.querySelector('[data-testid=selected-id]')?.closest('details');if(exact&&!exact.open)exact.querySelector('summary')?.click();else if(document.querySelector('[data-testid=selected-id]')?.getClientRects().length)return{id,durationMs:performance.now()-start};}}await new Promise(resolve=>requestAnimationFrame(resolve));}throw new Error('Inspector diagnostic watchdog');`);
}
async function series(name: string, budget: number, operation: (ordinal: number) => Promise<number>, coverageComplete = true): Promise<void> {
  const samples: number[] = []; const warmups: number[] = [];
  for (let ordinal = 0; ordinal < 35; ordinal++) {
    console.log(`${name}: ${ordinal < 5 ? `zahřátí ${ordinal + 1}/5` : `měření ${ordinal - 4}/30`}.`);
    let timer: ReturnType<typeof setTimeout> | null = null;
    const timeout = new Promise<never>((_resolve, reject) => { timer = setTimeout(() => reject(new Error('Per-operation 15-second diagnostic watchdog')), 15000); });
    let duration: number;
    try { duration = await Promise.race([operation(ordinal), timeout]); } finally { if (timer) clearTimeout(timer); }
    (ordinal < 5 ? warmups : samples).push(duration);
    appendFileSync(join(output, 'timed-operations.jsonl'), JSON.stringify({ metric: name, ordinal: ordinal + 1, warmup: ordinal < 5, durationMs: duration }) + '\n');
  }
  const observedAssessment = assessMeasurements(samples, 30, budget, 'p95');
  observed(name, { warmups, samples, coverageComplete, observedAssessment, assessment: coverageComplete ? observedAssessment : { ...observedAssessment, status: 'partial' } });
}
async function queries(): Promise<void> {
  begin('Přesné identity: 5 zahřívacích a 30 měřených dotazů.');
  const seedRows = await evaluate<PerformanceIdentitySeed[]>(`const state=await window.fabricExplorer.getState();const binding={sessionId:state.sessionId,capability:state.capability,generation:state.snapshot.generation};const result=await window.fabricExplorer.search(binding,'perf-seed',{text:'input-A',filter:{projectIds:[],families:[],findingStates:[],relations:[]},order:'identity',limit:25,cursor:null});if(result.response.status!=='ok')throw new Error('Seed search failed');return result.response.payload.items.map(row=>({kind:row.kind,id:row.id,identity:row.identity}));`);
  const seed = performanceLookupSeeds(seedRows);
  await series('ID lookup', 100, async ordinal => {
    const absent = ordinal % 3 === 2; const second = ordinal % 3 === 1 && seed.second !== null;
    const identity = absent ? seed.absent : second ? seed.second : seed.present; const expectedId = second ? seed.secondId : seed.presentId;
    return evaluate(`const state=await window.fabricExplorer.getState();const binding={sessionId:state.sessionId,capability:state.capability,generation:state.snapshot.generation};const identity=${JSON.stringify(identity)};const started=performance.now();const result=await window.fabricExplorer.lookup(binding,'perf-id-${ordinal}',{identity});const duration=performance.now()-started;if(result.response.status!=='ok'||(${absent}?result.response.payload.vertex!==null:result.response.payload.vertex?.id!==${JSON.stringify(expectedId)}))throw new Error('Exact lookup oracle');return duration;`);
  }, seed.coverage === 'paired-versions');
  observed('ID population coverage', { presentAndAbsent: true, multipleVersionsSameLogicalIdentity: seed.coverage, present: seed.present, second: seed.second, negativeCandidate: seed.absent });
  begin('Text: 5 zahřívacích a 30 měřených dotazů.');
  await series('Text search', 300, async ordinal => evaluate(`const state=await window.fabricExplorer.getState();const binding={sessionId:state.sessionId,capability:state.capability,generation:state.snapshot.generation};const text=${JSON.stringify(['synthetic', 'synthetic-source-0000', 'absent-performance-probe-20261109'][ordinal % 3])};const payload={text,filter:{projectIds:[],families:[],findingStates:[],relations:[]},order:'identity',limit:25,cursor:null};const started=performance.now();const result=await window.fabricExplorer.search(binding,'perf-text-${ordinal}',payload);const duration=performance.now()-started;if(result.response.status!=='ok')throw new Error('Text search failed');const page=result.response.payload;if(page.items.some(row=>!row.label.toLowerCase().includes(text)&&!row.id.toLowerCase().includes(text)))throw new Error('Literal text mismatch');if(text.startsWith('absent-')&&page.items.length)throw new Error('Absent text oracle');if(page.nextCursor){const next=await window.fabricExplorer.search(binding,'perf-text-next-${ordinal}',{...payload,cursor:page.nextCursor});if(next.response.status!=='ok'||next.response.payload.items.some(row=>page.items.some(prior=>row.id===prior.id)))throw new Error('Pagination oracle');}return duration;`));
  begin('Detail uzlu/vztahu: 5 zahřívacích a 30 měřených výběrů.');
  await series('Cached inspector', 100, async ordinal => (await selectTable(ordinal % 2 ? 'edges' : 'vertices', Math.floor(ordinal / 2) % 2)).durationMs);
  begin('Zachycený zdroj: 5 zahřívacích a 30 měřených stránek.');
  await series('Visible raw page', 500, async ordinal => {
    await selectTable(ordinal % 2 ? 'vertices' : 'edges', Math.floor(ordinal / 2) % 2);
    await click('#inspector-tab-evidence');
    return evaluate(`if(document.querySelector('#source-text'))throw new Error('Prior source page was not cleared');const start=performance.now();document.querySelector('#read-source').click();while(performance.now()-start<15000){const page=document.querySelector('#source-text');if(page&&!document.querySelector('#status')?.textContent.includes('Working:')){if(page.childElementCount!==0||page.textContent.length>8192)throw new Error('Escaped bounded source page oracle');return performance.now()-start;}await new Promise(resolve=>requestAnimationFrame(resolve));}throw new Error('Raw page diagnostic watchdog');`);
  });
  await animationCase();
}
async function animationCase(): Promise<void> {
  begin('Automatický pohyb a zoom po dobu 20 sekund; graf není určen k ručnímu čtení.');
  const bulkSeedId = await evaluate<string>(`const state=await window.fabricExplorer.getState();const binding={sessionId:state.sessionId,capability:state.capability,generation:state.snapshot.generation};const result=await window.fabricExplorer.search(binding,'perf-bulk-seed',{text:'synthetic-source-0000',filter:{projectIds:[],families:[],findingStates:[],relations:[]},order:'identity',limit:1,cursor:null});const row=result.response.status==='ok'?result.response.payload.items[0]:null;if(!row||!['version','use'].includes(row.identity.kind))throw new Error('Source-derived bulk seed absent');return row.id;`);
  await animate(bulkSeedId);
}
async function animate(seedId: string): Promise<void> {
  await click('#tab-search');
  await setValue('#search-text', seedId); await evaluate("document.querySelector('#search-text').form.requestSubmit();");
  await wait("document.querySelector('#search-text').closest('section').querySelector('.results button')?.title===" + JSON.stringify(seedId), 'Exact bulk-source search');
  await evaluate("document.querySelector('#search-text').closest('section').querySelector('.results button').click();");
  await wait("document.querySelector('[data-testid=selected-id]')?.textContent===" + JSON.stringify(seedId), 'Exact bulk-source selection');
  await wait("!document.querySelector('#expand').disabled", 'Neighbourhood control'); await click('#expand'); await wait(usableOverviewExpression(), 'Default-budget visible neighbourhood');
  await evaluate('await new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)));');
  const bounds = await evaluate<{ x: number; y: number; width: number; height: number }>("const rect=document.querySelector('canvas.sigma-stage').getBoundingClientRect();return{x:rect.x,y:rect.y,width:rect.width,height:rect.height};"); assert(bounds.width > 0 && bounds.height > 0);
  await prepareNativeFocus({ requestFocus: () => window!.focus(), waitForFocus: () => wait('document.hasFocus()', 'Actual test window foreground'), isFocused: () => window!.isFocused() });
  await evaluate(`const state={startedMs:performance.now(),endedMs:null,timestamps:[],inputs:{pointerdown:0,pointermove:0,pointerup:0,wheel:0,trusted:0,trustedHeldMoves:0},listeners:[]};window.__jaiFrameSample=state;for(const type of ['pointerdown','pointermove','pointerup','wheel']){const listener=event=>{if(event.target instanceof Element&&event.target.closest('.graph-canvas')){state.inputs[type]++;if(event.isTrusted){state.inputs.trusted++;if(type==='pointermove'&&(event.buttons&1))state.inputs.trustedHeldMoves++;}}};document.addEventListener(type,listener,true);state.listeners.push([type,listener]);}const frame=time=>{state.timestamps.push(time);if(performance.now()-state.startedMs<20000)requestAnimationFrame(frame);else state.endedMs=performance.now();};requestAnimationFrame(frame);`);
  const started = performance.now(); let gesture = 0; let completedGestures = 0; let nextProgress = 0;
  while (performance.now() - started < 20000) {
    const elapsed = performance.now() - started;
    if (elapsed >= nextProgress) { console.log(`Animace: zbývá ${Math.max(0, Math.ceil((20000 - elapsed) / 1000))} sekund z 20.`); nextProgress += 1000; }
    const x = Math.round(bounds.x + bounds.width * 0.8); const y = Math.round(bounds.y + bounds.height * 0.8);
    assert(window!.isFocused(), 'Native input requires the actual test window in foreground.');
    const contents = window!.webContents;
    contents.sendInputEvent({ type: 'mouseMove', x, y }); contents.sendInputEvent({ type: 'mouseDown', x, y, button: 'left', clickCount: 1 });
    let lastX = x, lastY = y; gesture++;
    // Native queues may coalesce a synchronous burst. Observe each held trusted receipt before submitting the next move.
    const received = await performObservedDrag({
      move: async move => {
        if (performance.now() - started >= 20000) return false;
        assert(window!.isFocused(), 'Native input requires the actual test window in foreground.');
        const prior = await evaluate<number>('return window.__jaiFrameSample.inputs.trustedHeldMoves;');
        lastX = Math.round(x + (gesture % 2 ? -25 : 25) * move / 8); lastY = Math.round(y + 12 * move / 8);
        contents.sendInputEvent({ type: 'mouseMove', x: lastX, y: lastY, modifiers: ['leftbuttondown'] });
        return evaluate<boolean>(`const state=window.__jaiFrameSample;while(state.endedMs===null&&performance.now()-state.startedMs<20000){if(state.inputs.trustedHeldMoves>${prior})return true;await new Promise(resolve=>requestAnimationFrame(resolve));}return false;`);
      },
      release: () => contents.sendInputEvent({ type: 'mouseUp', x: lastX, y: lastY, button: 'left', clickCount: 1 }),
    });
    if (!received) break;
    completedGestures++;
    contents.sendInputEvent({ type: 'mouseWheel', x, y, deltaY: gesture % 2 ? -12 : 12, deltaX: 0 });
  }
  await wait('window.__jaiFrameSample.endedMs!==null', 'Animation boundary completes', 15000);
  const value = await evaluate<{ startedMs: number; endedMs: number; timestamps: number[]; inputs: { pointerdown: number; pointermove: number; pointerup: number; wheel: number; trusted: number; trustedHeldMoves: number } }>("const state=window.__jaiFrameSample;for(const [type,listener] of state.listeners)document.removeEventListener(type,listener,true);const {listeners,...result}=state;delete window.__jaiFrameSample;return result;");
  const intervals = activeFrameIntervals(value.timestamps); const coverage = animationCoverage(value);
  const inputCoverage = completedGestures > 0 && value.inputs.trustedHeldMoves >= completedGestures * 8 && value.inputs.pointerdown > 0 && value.inputs.pointerup > 0 && value.inputs.pointermove > value.inputs.pointerdown * 3 && value.inputs.wheel > 0 && value.inputs.trusted > 0;
  animation = { ...value, coverage, inputCoverage, intervals, assessment: coverage.complete && inputCoverage && intervals.length ? assessMeasurements(intervals, intervals.length, 33, 'p95') : { status: 'partial' }, attemptedNativeGestures: gesture, completedNativeGestures: completedGestures, moveEventsPerGesture: 8,
    visible: await evaluate("return [...document.querySelectorAll('.graph-header p')].map(row=>row.textContent).find(text=>text.startsWith('Visible graph'));"), method: 'Actual native mouse/wheel input and production renderer requestAnimationFrame timestamps; full twenty-second boundary is checked separately.' };
  observed('Active frame observation', animation);
}
async function faults(): Promise<void> {
  begin('Obnovení nezměněné revize se zachováním přesných zdrojů.');
  const prior = observedSnapshot!.generation; await click('#refresh'); await wait(`${quiet}&&document.querySelector('#snapshot-state')?.textContent.includes('Snapshot ')`, 'Unchanged refresh', 120000); await verify(); assert.equal(observedSnapshot!.generation, prior, 'Unchanged refresh retains the accepted generation');
  begin('Skutečné ukončení nového kandidátního workeru při jeho spuštění.');
  const generation = observedSnapshot!.generation; killNextCandidate = true;
  const rejected = await evaluate<{ status: string }>("const state=await window.fabricExplorer.getState();return window.fabricExplorer.importSnapshot({sessionId:state.sessionId,capability:state.capability,generation:state.snapshot.generation},'performance-fault-candidate',state.sources.map(source=>source.sourceId));");
  assert.equal(rejected.status, 'error', 'Actual bridge candidate import rejects the terminated worker'); assert(workerFaultTriggered);
  const retained = await evaluate<{ snapshot: { generation: string } }>('return window.fabricExplorer.getState();'); assert.equal(retained.snapshot.generation, generation); observed('Bridge-driven candidate worker termination retains accepted generation; no UI-warning assertion', { generation, workerFaultTriggered, counters: counters() });
  begin('Skutečná ztráta WebGL kontextu, pokud ji ovladač podporuje.');
  const triggered = await evaluate<boolean>("const canvas=document.querySelector('canvas.sigma-stage');const gl=canvas?.getContext('webgl2');const extension=gl?.getExtension('WEBGL_lose_context');if(!extension)return false;extension.loseContext();return true;");
  if (triggered) { await wait("document.querySelector('.graph-empty h2')?.textContent==='Graph unavailable'", 'Production context-loss fallback'); observed('GPU loss', { status: 'pass', trigger: 'WEBGL_lose_context', boundedFallback: true }); }
  else observed('GPU loss', { status: 'blocked', reason: 'Actual WebGL context-loss extension unavailable.' });
}
async function endurance(): Promise<void> {
  begin('Jediný 30minutový aktivní běh M; průběh je hlášen každou minutu.');
  const started = performance.now(); const activeEnd = started + PERFORMANCE_POPULATIONS.enduranceMs; let ordinal = 0; let nextMinute = 0; let nextRefresh = 60000; let nextCycle = 300000;
  enduranceWatchdog = setTimeout(() => stop('Vypršel limit 1800 sekund aktivity, 120 sekund dokončení a 30 sekund ukončení.', 2), 1950000);
  event('endurance-started', { activeMs: 1800000, drainMs: 120000, shutdownMs: 30000 });
  const activeCounters: unknown[] = [];
  while (performance.now() - started < PERFORMANCE_POPULATIONS.enduranceMs) {
    const elapsed = performance.now() - started;
    if (elapsed >= nextMinute) { console.log(`Výdrž M: minuta ${Math.min(30, Math.floor(elapsed / 60000) + 1)}/30; zbývá ${Math.max(0, Math.ceil((1800000 - elapsed) / 1000))} sekund.`); activeCounters.push({ elapsedMs: elapsed, ...counters() }); event('endurance-progress', activeCounters.at(-1)); nextMinute += 60000; }
    await selectTable(ordinal % 2 ? 'vertices' : 'edges', Math.floor(ordinal / 2) % 2);
    if (performance.now() >= activeEnd) break;
    await fitCommittedOverview({ waitForOverview: () => wait(usableOverviewExpression(), 'Endurance current graph commit'), clickFit: () => click('#fit-graph') }); await click('#tab-search'); if (await evaluate("return document.querySelector('#search-filters').getAttribute('aria-expanded')!=='true';")) await click('#search-filters'); await setValue('#filter-state', ordinal % 2 ? 'open' : ''); await wait(quiet, 'Endurance filter quiescence'); await click('#reset-filters'); await wait(quiet, 'Endurance reset quiescence');
    if (performance.now() >= activeEnd) break;
    if (elapsed >= nextCycle) { await close(); if (performance.now() >= activeEnd) break; await open(); await importSources(); await verify(); nextCycle += 300000; }
    else if (elapsed >= nextRefresh) { await click('#refresh'); await wait(quiet, 'Endurance refresh quiescence', 120000); await verify(); nextRefresh += 60000; }
    ordinal++; if (performance.now() < activeEnd) await idle(Math.min(1000, activeEnd - performance.now()));
  }
  observed('Active endurance window', { elapsedMs: performance.now() - started, activeScheduledMs: 1800000, completionOverrunMs: Math.max(0, performance.now() - activeEnd), iterations: ordinal, counters: activeCounters });
}
async function finish(): Promise<void> {
  begin('Uložení výsledků a uvolnění zdrojů.');
  if (kind !== 'blank' && kind !== 'shell' && kind !== 'retention' && await evaluate<boolean>("return !!document.querySelector('#close')&&!document.querySelector('#close').disabled;")) await close();
  if (kind !== 'blank') rendererTasks = await evaluate(`const state=window.__jaiPerformance;const remaining=state.observer?.takeRecords()??[];for(const item of remaining){if(state.tasks.length<10000)state.tasks.push({startTime:item.startTime,duration:item.duration});else state.dropped++;}state.observer?.disconnect();return{supported:!!state.observer,startedMs:state.startedMs,endedMs:performance.now(),tasks:state.tasks,dropped:state.dropped,maximumMs:Math.max(0,...state.tasks.map(item=>item.duration))};`);
  observed('Final ownership', counters()); finished = true; loopDelay.disable(); save(); clearTimeout(watchdog); if (enduranceWatchdog) clearTimeout(enduranceWatchdog); event('collected', { stage, stages, counters: counters() }); assert.equal(stage, stages); app.quit();
}
async function run(): Promise<void> {
  await start();
  if (kind === 'blank' || kind === 'shell') { begin('Pětisekundové měření prázdného okna; žádné zdroje nejsou načtené.'); event('settle-start', { cycle: null }); await idle(5000); event('settle-end', { cycle: null }); await finish(); return; }
  if (kind === 'retention') {
    for (let cycle = 1; cycle <= 10; cycle++) {
      begin(`Cyklus ${cycle}/10: otevření stejných neměnných zdrojů.`); await open();
      begin(`Cyklus ${cycle}/10: import a ověření přesných počtů.`); await importSources(); await verify();
      begin(`Cyklus ${cycle}/10: zavření a pevné pětisekundové ustálení.`); await close(); event('settle-start', { cycle }); await idle(5000); event('settle-end', { cycle, ...counters() }); observed('Closed cycle', { cycle, ...counters() });
    }
    await finish(); return;
  }
  begin('Otevření pouze připravených neměnných zdrojů.'); await open();
  begin('Import do použitelného indexu a skutečného grafu.'); await importSources();
  begin('Porovnání skutečně zachycených revizí a počtů s manifestem.'); await verify();
  if (kind === 'import') { begin('Pětisekundové měření načteného grafu.'); await idle(5000); }
  else if (kind === 'queries') await queries(); else if (kind === 'animation') await animationCase(); else if (kind === 'faults') await faults(); else await endurance();
  await finish();
}
void run().catch(error => { failure = error instanceof Error ? error.message : 'Unknown native observation failure'; finished = true; loopDelay.disable(); clearTimeout(watchdog); try { save(); event('failed', { failure, stage, stages }); console.error(`Pozorování selhalo v kroku ${stage}/${stages}: ${failure}`); } finally { app.exit(1); } });
