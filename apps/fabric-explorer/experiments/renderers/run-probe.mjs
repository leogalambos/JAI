/** Disposable finite renderer observation runner. No release/GPU qualification is granted. */
import { chromium } from '@playwright/test';
import { execFileSync } from 'node:child_process';
import { mkdir, readFile, writeFile, rename, readdir } from 'node:fs/promises';
import { randomUUID, createHash } from 'node:crypto';
import { captureMemorySample } from './memory-accounting.mjs';
import { resolve, dirname } from 'node:path';
import { admitOutput } from './output-path.mjs';
import { fileURLToPath } from 'node:url';
import os from 'node:os';
import { parseOperatorObservation, unknownObservation } from './operator-observation.mjs';
import { stages, createPlan, createRunControl, executePlan } from './runner-control.mjs';

const directory = dirname(fileURLToPath(import.meta.url));
const argumentsMap = Object.fromEntries(process.argv.slice(2).map(argument => {
  const separator = argument.indexOf('=');
  if (!argument.startsWith('--') || separator === -1) throw new Error('Arguments use --name=value');
  return [argument.slice(2, separator), argument.slice(separator + 1)];
}));
if (!argumentsMap.output) throw new Error('An explicit --output=/absolute/private-or-scratch/directory is required');
const output = admitOutput(argumentsMap.output, directory);
const size = argumentsMap.size ?? 'M';
if (!['S', 'M', 'L'].includes(size)) throw new Error('Unknown corpus size');
const scales = (argumentsMap.scales ?? '1,1.5,2').split(',').map(Number);
if (!scales.every(scale => [1, 1.5, 2].includes(scale))) throw new Error('Only registered display scales 1/1.5/2 are accepted');
if (argumentsMap.manual !== undefined && !['true', 'false'].includes(argumentsMap.manual)) throw new Error('--manual must be true or false');
const manual = argumentsMap.manual === 'true';
const diagnostics = argumentsMap.diagnostics ?? 'none';
if (!['none', 'memory-phases'].includes(diagnostics)) throw new Error('Diagnostics must be none or memory-phases');
const reviewScope = argumentsMap.review ?? 'all';
if (!['all', 'labels'].includes(reviewScope)) throw new Error('Review must be all or labels');
const rendererSelection = argumentsMap.renderer ?? 'both';
const plan = createPlan(scales, rendererSelection);
const executablePath = argumentsMap.browser ?? '/usr/bin/chromium-browser';
await mkdir(output, { recursive: true });
if ((await readdir(output)).length) throw new Error('A new or empty observation directory is required; previous run files are never overwritten');
const observations = {
  format: 'jai.renderer-probe.observations/4', qualification: 'exploratory-only',
  inputSemantics: 'synthetic-projection-not-canonical-journal', startedAt: new Date().toISOString(),
  host: { os: os.platform(), release: os.release(), architecture: os.arch(), cpu: os.cpus()[0]?.model, logicalCpus: os.cpus().length, memoryBytes: os.totalmem(), node: process.version },
  browserExecutable: executablePath, browserVersion: null, browserSandboxRequested: true, manualMode: manual, headful: manual, interrupted: false, transport: 'playwright-pipe-no-listener', results: [], failures: [],
  diagnostics, reviewScope, browserLifetime: 'one-browser-reused-across-cases; first-case-startup-not-purged; later-cases-warm', rendererSelection, caseCount: plan.length, stagesPerCase: stages.length, totalSteps: plan.length * stages.length, completedCases: 0, completedSteps: 0, activeCase: null,
  decision: 'hold-pending-native-reference-host-and-manual-feature-evidence',
};
let browser;
let memorySession;
let memorySessionError = null;
let expectedBrowserClose = false;
let checkpointQueue = Promise.resolve();
const control = createRunControl({ onStop: reason => {
  console.log(`Stopping the entire test: ${reason}. No further case will start.`);
  void browser?.close().catch(() => {});
} });
const onInterrupt = () => control.stop('terminal-interrupt');
const onTermination = () => control.stop('terminal-termination');
const onInputClosed = () => control.stop('terminal-input-closed');
process.once('SIGINT', onInterrupt);
process.once('SIGTERM', onTermination);
const watchTerminal = Boolean(process.stdin.isTTY);
if (watchTerminal) { process.stdin.once('end', onInputClosed); process.stdin.once('close', onInputClosed); process.stdin.resume(); }
const checkpoint = () => {
  observations.remainingCases = plan.length - observations.completedCases;
  observations.remainingSteps = observations.totalSteps - observations.completedSteps;
  const content = JSON.stringify(observations, null, 2) + '\n';
  checkpointQueue = checkpointQueue.then(async () => {
    const admitted = admitOutput(output, directory);
    const temporary = resolve(admitted, `.observations-${randomUUID()}.tmp`);
    await writeFile(temporary, content, { flag: 'wx' });
    await rename(temporary, resolve(admitted, 'observations.json'));
  });
  return checkpointQueue;
};
function treeRss(rootIds) {
  try {
    if (process.platform === 'win32') return null;
    const listing = execFileSync('ps', ['-axo', 'pid=,ppid=,rss='], { encoding: 'utf8', timeout: 2000 });
    const rows = listing.trim().split('\n').map(line => line.trim().split(/\s+/).map(Number));
    const admitted = new Set(rootIds);
    let grew = true;
    while (grew) { grew = false; for (const [pid, parent] of rows) if (admitted.has(parent) && !admitted.has(pid)) { admitted.add(pid); grew = true; } }
    return rows.filter(([pid]) => admitted.has(pid)).reduce((sum, row) => sum + row[2] * 1024, 0);
  } catch { return null; }
}
console.log(`Renderer test: ${plan.length} cases, ${stages.length} stages per case, ${observations.totalSteps} numbered steps.`);
console.log(`Automatic pan/zoom sampling totals ${plan.length * 20} seconds, plus graph loading and your manual reviews. Dense graphs are automatic load tests, not reading tasks.`);
console.log('Stop with the browser Stop button, Escape, window close or terminal Ctrl+C. Enter manual answers in the browser; no terminal JSON is required.');
await checkpoint();
try {
  console.log(`Opening Chromium. Case 1 of ${plan.length} starts after launch (20-second launch watchdog).`);
  browser = await control.operation('Browser launch', () => chromium.launch({ executablePath, headless: !manual, chromiumSandbox: true, handleSIGINT: false, handleSIGTERM: false, handleSIGHUP: false, timeout: 20000 }), 20000, resource => resource.close());
  browser.on('disconnected', () => { if (!expectedBrowserClose) control.stop('browser-disconnected'); });
  observations.browserVersion = browser.version();
  const html = (await readFile(resolve(directory, 'index.html'), 'utf8')).replace(/<script[^>]*src="[^"]*"[^>]*><\/script>/, '');
  const script = await readFile(resolve(directory, 'dist/probe.js'), 'utf8');
  const style = await readFile(resolve(directory, 'dist/probe.css'), 'utf8');
  const phaseScript = await readFile(resolve(directory, 'dist/phase-bootstrap.js'), 'utf8');
  observations.assetDigests = Object.fromEntries([['probe.js', script], ['probe.css', style], ['phase-bootstrap.js', phaseScript]].map(([name, bytes]) => [name, createHash('sha256').update(bytes).digest('hex')]));
  observations.runtimeFlags = { headless: !manual, chromiumSandbox: true, transport: 'pipe', graphDurationMs: 20000, diagnostics, reviewScope };
  if (diagnostics === 'memory-phases') {
    try { memorySession = await control.operation('Browser memory inventory session', () => browser.newBrowserCDPSession(), 15000); }
    catch (error) { memorySessionError = String(error); }
  }
  await executePlan(plan, control, async ({ renderer, scale }, caseIndex, caseCount) => {
    control.check();
    let context;
    let page;
    let expectedPageClose = false;
    let timer;
    let countdown;
    let currentProgress;
    const errors = [];
    const result = { renderer, size, scale, caseIndex, caseStatus: 'running', stageIndex: 0, stageTitle: '', errors,
      peakRssBytes: null, rssSamplesBytes: [], memoryScope: 'probe-runner-browser-performance-phase-no-canonical-helper-or-manual-feature-phase',
      rssMeasurement: process.platform === 'win32' ? 'unavailable-not-a-pass' : 'sum-ps-rss-conservative', qualification: 'exploratory-only', contextRecovery: 'unknown-not-tested', browserProcessReuse: caseIndex === 1 ? 'first-case-process-startup; no-cache-purge' : 'same-browser-warm-after-prior-cases', reviewScope };
    const memorySamples = [];
    let memoryPhase = 'browser-page-creation';
    let pendingMemory; let previousSampleStart; let skippedSamples = 0;
    result.memory = { scope: 'browser-application-tree through reset/cancellation only; manual/context excluded; Node-driver-separate; helper-not-present; not-whole-product', samples: memorySamples, baselines: [], sessionError: memorySessionError, productMemoryStatus: 'not-proven-canonical-helper-not-present' };
    const sampleMemory = async (kind = 'periodic') => {
      if (pendingMemory) { if (kind === 'periodic') { skippedSamples++; return; } await pendingMemory; }
      if (control.stopped) return null;
      const phaseAtStart = memoryPhase; const started = performance.now();
      const spacing = previousSampleStart === undefined ? null : started - previousSampleStart; previousSampleStart = started;
      pendingMemory = (async () => {
        let sample;
        try {
          sample = memorySession ? await control.operation('Browser process memory snapshot', () => captureMemorySample(memorySession, process.pid), 15000)
            : { complete: false, browserRssBytes: null, observedBrowserRssBytes: null, driverRssBytes: null, combinedRssBytes: null, browserPssBytes: null, errors: [memorySessionError ?? 'Memory inventory unavailable'] };
        } catch (error) { sample = { complete: false, browserRssBytes: null, observedBrowserRssBytes: null, errors: [String(error)] }; }
        const index = memorySamples.length;
        memorySamples.push({ index, phaseAtStart, phaseAtEnd: memoryPhase, kind, actualStartSpacingMs: spacing, collectionMs: performance.now() - started, ...sample });
        return index;
      })();
      try { return await pendingMemory; } finally { pendingMemory = undefined; }
    };
    const markPhase = async name => { memoryPhase = name; if (page) await operation('Mark measurement phase', () => page.evaluate(value => window.rendererProbePhases?.mark(value), name)); };
    const baseline = async (name, action) => {
      await markPhase(name);
      if (action) await action();
      await operation('Two natural baseline frames', () => page.evaluate(() => new Promise(resolve => {
        requestAnimationFrame(() => requestAnimationFrame(() => resolve(null)));
      })));
      const indices = []; let next = performance.now();
      for (let index = 0; index < 5; index++) {
        const delay = next - performance.now(); if (delay > 0) await new Promise(resolve => setTimeout(resolve, delay));
        const sampleIndex = await sampleMemory('baseline'); indices.push(sampleIndex ?? null); next += 100;
      }
      result.memory.baselines.push({ name, sampleIndices: indices, complete: indices.length === 5 && indices.every(index => index !== null && memorySamples[index]?.kind === 'baseline' && memorySamples[index]?.phaseAtStart === name && memorySamples[index]?.phaseAtEnd === name && memorySamples[index]?.complete), settling: 'two-natural-frames; five-scheduled-100ms-samples; no-quiescence-claim' });
    };
    const finishMemory = () => {
      const known = memorySamples.filter(sample => sample.complete && Number.isFinite(sample.browserRssBytes));
      const observed = memorySamples.map(sample => sample.browserRssBytes ?? sample.observedBrowserRssBytes).filter(Number.isFinite);
      result.memory.completeSampleCount = known.length; result.memory.skippedPeriodicSamples = skippedSamples;
      result.memory.peakBrowserRssBytes = known.length ? Math.max(...known.map(sample => sample.browserRssBytes)) : null;
      result.memory.peakObservedBrowserRssBytes = observed.length ? Math.max(...observed) : null;
      result.memory.absoluteBrowserRssBudgetBytes = size === 'L' ? 2 * 1024 ** 3 : 1024 ** 3;
      const intervals = memorySamples.map(sample => sample.actualStartSpacingMs).filter(Number.isFinite);
      result.memory.sampling = { nominalIntervalMs: 100, maximumActualStartSpacingMs: intervals.length ? Math.max(...intervals) : null, overrunCount: intervals.filter(value => value > 100).length, skippedPeriodicSamples: skippedSamples, continuousPeakObserved: false, warning: 'Discrete samples and missing/overrun/transition windows cannot prove the continuous peak stayed below budget.' };
      result.memory.absoluteRssStatus = observed.some(value => value > result.memory.absoluteBrowserRssBudgetBytes) ? 'fail' : known.length === memorySamples.length && known.length ? (skippedSamples || intervals.some(value => value > 100) ? 'not-proven-sampling-gaps' : 'no-sampled-exceedance-not-product-pass') : 'unknown-incomplete';
      result.memory.diagnosticPhaseMedians = result.memory.baselines.map(phase => { const values = phase.sampleIndices.map(index => memorySamples[index]).filter(sample => sample?.complete && sample.kind === 'baseline' && sample.phaseAtStart === phase.name && sample.phaseAtEnd === phase.name).map(sample => sample.browserRssBytes).sort((a, b) => a - b); return { name: phase.name, medianBrowserRssBytes: values.length ? values[Math.floor(values.length / 2)] : null, completeSamples: values.length }; });
      const values = result.memory.diagnosticPhaseMedians; const graph = values.find(phase => phase.name === 'bounded-graph');
      result.memory.diagnosticDeltaBytes = values.map(phase => ({ baseline: phase.name, graphMinusPhaseMedian: graph?.medianBrowserRssBytes != null && phase.medianBrowserRssBytes != null ? graph.medianBrowserRssBytes - phase.medianBrowserRssBytes : null, meaning: 'difference-of-paired-phase-medians; non-additive; not-a-physical-allocation-or-budget-subtraction' }));
    };
    observations.activeCase = result;
    const operation = (label, action, timeout = 15000) => control.operation(label, action, timeout);
    const stage = async (stageIndex, remainingMs) => {
      control.check();
      const [title, instructions] = stages[stageIndex - 1];
      result.stageIndex = stageIndex; result.stageTitle = title;
      const progress = { caseIndex, caseCount, stageIndex, stageCount: stages.length, renderer, scale, title, instructions,
        mode: stageIndex === 6 && manual ? 'manual' : 'automatic', ...(remainingMs === undefined ? {} : { remainingMs }) };
      currentProgress = progress;
      console.log(`Case ${caseIndex}/${caseCount} · ${renderer} ${scale * 100}% · Step ${(caseIndex - 1) * stages.length + stageIndex}/${observations.totalSteps} · ${title}. ${instructions}`);
      if (page) await operation('Update progress', () => page.evaluate(value => { window.rendererProbeProgress = value; window.rendererProbeControls?.setProgress(value); }, progress));
      await checkpoint();
    };
    try {
      await stage(1);
      context = await control.operation('Create browser context', () => browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: scale }), 15000, resource => resource.close());
      page = await operation('Create browser page', () => context.newPage());
      page.setDefaultTimeout(15000);
      page.on('pageerror', error => errors.push(String(error)));
      page.on('close', () => { if (!expectedPageClose) control.stop('browser-window-closed'); });
      await page.exposeBinding('requestProbeStop', (_source, reason) => { control.stop(typeof reason === 'string' ? reason : 'browser-stop-button'); });
      await page.route('**/*', route => route.abort('blockedbyclient'));
      timer = setInterval(() => {
        if (diagnostics === 'memory-phases') { void sampleMemory(); return; }
        const value = treeRss([process.pid]);
        if (value !== null) { result.rssSamplesBytes.push(value); result.peakRssBytes = Math.max(result.peakRssBytes ?? 0, value); }
      }, 100);
      await operation('Install early task observer', () => page.addScriptTag({ content: phaseScript }));
      if (diagnostics === 'memory-phases') { console.log(`Case ${caseIndex}/${caseCount}: paired browser-blank baseline (same reused-browser lifetime as reported).`); await baseline('browser-blank'); }
      await markPhase('harness-html-and-module-bootstrap');
      await operation('Load local page', () => page.setContent(html));
      await operation('Load local stylesheet', () => page.addStyleTag({ content: style }));
      await operation('Set probe parameters', () => page.evaluate(parameters => { window.rendererProbeParameters = parameters; }, `?renderer=${renderer}&size=${size}&diagnostics=${diagnostics}&review=${reviewScope}`));
      await operation('Set initial progress', () => page.evaluate(value => { window.rendererProbeProgress = value; }, currentProgress));
      await operation('Load graph', async () => {
        await page.addScriptTag({ content: script });
        if (diagnostics === 'memory-phases') {
          await page.waitForFunction(() => window.rendererProbe?.bootstrapped, undefined, { timeout: 60000 });
          console.log(`Case ${caseIndex}/${caseCount}: harness-only baseline; no renderer/corpus initialized.`);
          await baseline('harness-unloaded-renderer');
          console.log(`Case ${caseIndex}/${caseCount}: empty renderer baseline; first construction in this page remains in overall task evidence (browser lifetime is recorded).`);
          await baseline('empty-renderer', () => operation('Construct empty renderer', () => page.evaluate(() => window.rendererProbe.emptyRenderer())));
          await markPhase('corpus-generation-and-bounded-transfer');
          await page.evaluate(() => window.rendererProbe.loadGraph());
          await baseline('bounded-graph');
        }
        await page.waitForFunction(() => window.rendererProbe?.ready || window.rendererProbe?.error, undefined, { timeout: 60000 });
        const failure = await page.evaluate(() => window.rendererProbe.error);
        if (failure) throw new Error(failure);
      }, 60000);
      result.initial = await operation('Read initial graph', () => page.evaluate(() => window.rendererProbe.summary()));
      observations.completedSteps = (caseIndex - 1) * stages.length + 1;
      await stage(2);
      result.featureSelections = [];
      for (const id of ['v0', 'e0', 'e1', 'e2', 'e3']) {
        await operation('Select element', () => page.evaluate(id => window.rendererProbe.inspect(id), id));
        result.featureSelections.push({ id, inspector: await operation('Read inspector', () => page.evaluate(() => window.rendererProbe.details())), method: 'programmatic-not-pointer-proof' });
      }
      await operation('Capture selected element', () => page.screenshot({ path: resolve(output, `${renderer}-${size}-${scale}-selected.png`) }));
      const point = await operation('Locate vertex', () => page.evaluate(() => window.rendererProbe.nodePoint('v0')));
      const box = await operation('Locate graph bounds', () => page.locator('#graph').boundingBox());
      if (box && Number.isFinite(point.x) && Number.isFinite(point.y)) await operation('Click vertex', () => page.mouse.click(box.x + point.x, box.y + point.y));
      result.afterPointer = await operation('Read pointer selection', () => page.evaluate(() => window.rendererProbe.summary()));
      observations.completedSteps = (caseIndex - 1) * stages.length + 2;
      await stage(3, 20000);
      await markPhase('active-animation');
      const started = Date.now();
      countdown = setInterval(() => console.log(`Case ${caseIndex}/${caseCount} · automatic measurement: ${Math.max(0, Math.ceil((20000 - (Date.now() - started)) / 1000))} seconds remaining; do not inspect this dense graph.`), 1000);
      try { result.animation = await operation('20-second pan/zoom measurement', () => page.evaluate(() => window.rendererProbe.animate(20000)), 30000); }
      finally { clearInterval(countdown); }
      observations.completedSteps = (caseIndex - 1) * stages.length + 3;
      await stage(4);
      await markPhase('expansion-and-grouping');
      result.expanded = await operation('Expand graph', () => page.evaluate(() => window.rendererProbe.expand()));
      result.groupExpansion = await operation('Expand group', () => page.evaluate(() => window.rendererProbe.group(0)));
      await operation('Capture expansion', () => page.screenshot({ path: resolve(output, `${renderer}-${size}-${scale}-expanded.png`) }));
      observations.completedSteps = (caseIndex - 1) * stages.length + 4;
      await stage(5);
      await markPhase('reset-and-cancellation');
      await operation('Reset graph', () => page.evaluate(() => window.rendererProbe.reset()));
      result.cancellation = await operation('Check animation cancellation', () => page.evaluate(async () => {
        const start = performance.now(); const active = window.rendererProbe.animate(20000); const acknowledgement = window.rendererProbe.cancel(); const value = await active;
        return { acknowledgementMs: acknowledgement.acknowledgedAt - start, result: value, quiescenceMs: performance.now() - start };
      }));
      clearInterval(timer); if (pendingMemory) await pendingMemory; finishMemory();
      result.phaseEvidenceCapturedThroughStage = 5;
      result.phaseEvidence = await operation('Read pre-manual task phase evidence', () => page.evaluate(() => window.rendererProbePhases?.snapshot() ?? null));
      observations.completedSteps = (caseIndex - 1) * stages.length + 5;
      await stage(6);
      if (manual) {
        await markPhase('manual-selected-label-review');
        result.manualFeatureFixture = await operation('Show readable review example', () => page.evaluate(() => window.rendererProbe.featureView()));
        console.log(`Case ${caseIndex}/${caseCount}: waiting for your browser review. Use Save, Skip or Stop. There is no terminal JSON prompt.`);
        const answer = await operation('Browser manual review', () => page.evaluate(() => window.rendererProbeControls.review()), null);
        result.operatorReview = parseOperatorObservation(JSON.stringify({ ...answer.criteria, note: answer.note ?? '' }), new Date().toISOString());
        result.operatorReview.method = answer.method === 'operator-skipped' ? 'operator-skipped' : 'explicit-browser-observation';
        result.afterManual = await operation('Read manual selection history', () => page.evaluate(() => window.rendererProbe.summary()));
        await operation('Capture manual feature example', () => page.screenshot({ path: resolve(output, `${renderer}-${size}-${scale}-manual-features.png`) }));
      } else result.operatorReview = unknownObservation('not-requested');
      observations.completedSteps = (caseIndex - 1) * stages.length + 6;
      await stage(7);
      await markPhase('context-loss-observation');
      result.contextLoss = await operation('Observe context loss', () => page.evaluate(() => window.rendererProbe.loseContext()));
      observations.completedSteps = (caseIndex - 1) * stages.length + 7;
      await stage(8);
      await markPhase('final-case-checkpoint');
      result.phaseEvidence = await operation('Read final task phase evidence', () => page.evaluate(() => window.rendererProbePhases?.snapshot() ?? null));
      result.phaseEvidenceCapturedThroughStage = 8;
      result.caseStatus = 'complete'; observations.completedCases++;
      observations.completedSteps = caseIndex * stages.length;
    } catch (error) {
      if (error?.name === 'AbortError') control.stop('operation-cancelled');
      else if (!control.stopped) control.stop(`failed: ${result.stageTitle || 'case setup'}`, true);
      result.caseStatus = control.failed ? 'failed' : 'interrupted';
      result.stopReason = control.reason; result.error = String(error);
      observations.failures.push({ renderer, size, scale, caseIndex, stageIndex: result.stageIndex, error: String(error), errors, peakRssBytes: result.peakRssBytes });
    } finally {
      clearInterval(timer); clearInterval(countdown); if (pendingMemory) await pendingMemory; finishMemory();
      observations.results.push(result); observations.activeCase = null;
      await checkpoint(); expectedPageClose = true;
      if (context) await context.close().catch(() => {});
    }
  });
} catch (error) {
  if (error?.name === 'AbortError') control.stop('operation-cancelled');
  else if (!control.stopped) control.stop('launch-or-inline-load-failure', true);
  observations.failures.push({ scope: 'launch-or-inline-load', error: String(error) });
} finally {
  expectedBrowserClose = true;
  if (browser) await browser.close().catch(() => {});
  await control.settleResources();
  observations.resourceCleanupErrors = control.cleanupErrors;
  observations.finishedAt = new Date().toISOString(); observations.interrupted = control.stopped && !control.failed;
  observations.status = control.failed || control.cleanupErrors.length ? 'failed' : control.stopped ? 'interrupted' : 'completed'; observations.stopReason = control.reason;
  await checkpoint(); process.removeListener('SIGINT', onInterrupt); process.removeListener('SIGTERM', onTermination);
  if (watchTerminal) { process.stdin.removeListener('end', onInputClosed); process.stdin.removeListener('close', onInputClosed); process.stdin.pause(); }
}
console.log(`Test ${observations.status}: ${observations.completedCases}/${plan.length} cases and ${observations.completedSteps}/${observations.totalSteps} steps completed. Results: ${resolve(output, 'observations.json')}`);
console.log(JSON.stringify({ output, runs: observations.results.length, completedCases: observations.completedCases, failures: observations.failures.length, decision: observations.decision }));
if (control.cleanupErrors.length) process.exitCode = 2;
else if (control.stopped) process.exitCode = control.failed ? 2 : 130;
