/** Disposable tiny-scene visual check only: no dense graph, animation, or performance qualification. */
import { chromium } from '@playwright/test';
import { mkdir, readFile, writeFile, rename, readdir } from 'node:fs/promises';
import { createHash, randomUUID } from 'node:crypto';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { admitOutput } from './output-path.mjs';
import { createPlan, createRunControl, executePlan } from './runner-control.mjs';
import { labelCriteria, parseLabelObservation, unknownLabelObservation } from './label-observation.mjs';
const directory = dirname(fileURLToPath(import.meta.url));
const options = {};
for (const argument of process.argv.slice(2)) {
  const match = /^--(output|browser|scales)=(.+)$/.exec(argument);
  if (!match || options[match[1]] !== undefined) throw new Error('Use distinct --output= --browser= --scales= arguments');
  options[match[1]] = match[2];
}
if (!options.output) throw new Error('Explicit fresh private/scratch --output is required');
const output = admitOutput(options.output, directory);
const scales = (options.scales ?? '1,1.5,2').split(',').map(Number);
if (!scales.every(value => [1, 1.5, 2].includes(value))) throw new Error('Display scales must be 1,1.5,2');
const plan = createPlan(scales, 'sigma');
await mkdir(output, { recursive: true });
if ((await readdir(output)).length) throw new Error('Output must be new or empty; historical observations are immutable');
const report = { format: 'jai.renderer-probe.labels-only/1', mode: 'labels-only', qualification: 'operator-visual-only-not-performance-qualification',
  startedAt: new Date().toISOString(), node: process.version, browserVersion: null, browserExecutable: options.browser ?? '/usr/bin/chromium-browser',
  headful: true, chromiumSandbox: true, transport: 'playwright-pipe-no-listener', browserLifetime: 'one-browser-reused-across-cases',
  fixture: { size: 'S', backgroundCorpusVertices: 1000, backgroundCorpusEdges: 3000, mountedVertexLimit: 2, mountedEdgeLimit: 4, seed: 20261109 },
  caseCount: plan.length, stagesPerCase: 4, totalSteps: plan.length * 4, completedCases: 0, completedSteps: 0, results: [], failures: [] };
let browser; let expectedClose = false; let queue = Promise.resolve(); let stopCleanup = Promise.resolve();
const control = createRunControl({ onStop: () => { stopCleanup = Promise.resolve(browser?.close()).catch(error => { report.failures.push(`Stop cleanup: ${error}`); }); } });
const interrupt = () => control.stop('terminal-interrupt');
const terminate = () => control.stop('terminal-termination');
const inputClosed = () => control.stop('terminal-input-closed');
process.once('SIGINT', interrupt); process.once('SIGTERM', terminate);
const terminal = Boolean(process.stdin.isTTY);
if (terminal) { process.stdin.resume(); process.stdin.once('end', inputClosed); process.stdin.once('close', inputClosed); }
const checkpoint = () => {
  const content = JSON.stringify({ ...report, stopReason: control.reason, remainingSteps: report.totalSteps - report.completedSteps }, null, 2) + '\n';
  queue = queue.then(async () => { const temporary = resolve(admitOutput(output, directory), `.labels-${randomUUID()}.tmp`); await writeFile(temporary, content, { flag: 'wx' }); await rename(temporary, resolve(output, 'observations.json')); });
  return queue;
};
console.log(`Labels-only check: ${plan.length} cases × 4 steps = ${report.totalSteps}. Only two vertices/four edges are mounted. No performance measurements.`);
console.log('Stop with Stop, Escape, closing the window, or Ctrl+C. Unanswered/Skip remains unknown.');
await checkpoint();
try {
  browser = await control.operation('Browser launch', () => chromium.launch({ executablePath: report.browserExecutable, headless: false, chromiumSandbox: true, handleSIGINT: false, handleSIGTERM: false, handleSIGHUP: false, timeout: 20000 }), 20000, value => value.close());
  browser.on('disconnected', () => { if (!expectedClose) control.stop('browser-disconnected'); });
  report.browserVersion = browser.version();
  const html = (await readFile(resolve(directory, 'index.html'), 'utf8')).replace(/<script[^>]*src="[^"]*"[^>]*><\/script>/, '');
  const script = await readFile(resolve(directory, 'dist/probe.js'), 'utf8');
  const css = await readFile(resolve(directory, 'dist/probe.css'), 'utf8');
  report.assetDigests = Object.fromEntries([['probe.js', script], ['probe.css', css]].map(([name, value]) => [name, createHash('sha256').update(value).digest('hex')]));
  await executePlan(plan, control, async ({ scale }, caseIndex, caseCount) => {
    let context; let page; let closing = false;
    const result = { scale, observation: unknownLabelObservation(), status: 'incomplete' }; report.results.push(result);
    const operation = (label, action) => control.operation(label, action, 15000);
    const stage = async (stageIndex, title, instructions, mode = 'automatic') => {
      console.log(`Step ${(caseIndex - 1) * 4 + stageIndex}/${report.totalSteps}: ${scale * 100}% ${title}`);
      await operation('Update progress', () => page.evaluate(value => window.rendererProbeControls.setProgress(value), { caseIndex, caseCount, stageIndex, stageCount: 4, renderer: 'sigma', scale, title, instructions, mode }));
    };
    try {
      context = await control.operation('Create context', () => browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: scale }), 15000, value => value.close());
      page = await operation('Create page', () => context.newPage());
      page.on('close', () => { if (!closing) control.stop('browser-window-closed'); });
      await page.exposeBinding('requestProbeStop', (_source, reason) => control.stop(typeof reason === 'string' ? reason : 'browser-stop-button'));
      await page.route('**/*', route => route.abort());
      await operation('Load offline page', () => page.setContent(html));
      await operation('Load offline style', () => page.addStyleTag({ content: css }));
      await operation('Configure tiny scene', () => page.evaluate(() => { window.rendererProbeParameters = '?renderer=sigma&size=S&mode=labels-only'; }));
      await operation('Load offline script', () => page.addScriptTag({ content: script }));
      await operation('Wait for harness', () => page.waitForFunction(() => window.rendererProbe?.bootstrapped));
      await stage(1, 'Create empty renderer', 'One empty Sigma renderer; no dense graph or animation will run.');
      const empty = await operation('Empty renderer', () => page.evaluate(() => window.rendererProbe.emptyRenderer()));
      if (empty.visibleVertices !== 0 || empty.visibleEdges !== 0) throw new Error('Expected empty renderer');
      report.completedSteps++; await checkpoint();
      await stage(2, 'Load tiny fixture', 'Two vertices and four relations only; S background corpus is generated in a worker, not mounted.');
      const scene = await operation('Tiny fixture', () => page.evaluate(() => window.rendererProbe.loadFeature()));
      result.scene = Object.fromEntries(['visibleVertices', 'visibleEdges', 'seed', 'size', 'gpu', 'deviceScale', 'viewport', 'graphViewport'].map(key => [key, scene[key]]));
      if (result.scene.visibleVertices !== 2 || result.scene.visibleEdges !== 4) throw new Error('Tiny fixture bounds violated');
      report.completedSteps++; await checkpoint();
      await stage(3, 'Review paths and labels', 'Select e0/e1/e3 and loop e2 by clicking their paths. Pan/zoom as needed. Record geometry separately from text readability.', 'manual');
      const answer = await control.operation('Manual label review', () => page.evaluate(criteria => new Promise(resolveAnswer => {
        const form = document.createElement('form'); form.id = 'label-only-review';
        const title = document.createElement('h2'); title.textContent = 'Review separate paths and graph labels'; form.append(title);
        for (const [key, prompt] of Object.entries(criteria)) {
          const label = document.createElement('label'); label.textContent = prompt;
          const select = document.createElement('select'); select.name = key;
          for (const value of ['unknown', 'pass', 'fail']) { const option = document.createElement('option'); option.value = value; option.textContent = value; select.append(option); }
          label.append(select); form.append(label);
        }
        const note = document.createElement('textarea'); note.maxLength = 2000; note.placeholder = 'Optional observation'; form.append(note);
        const save = document.createElement('button'); save.type = 'submit'; save.textContent = 'Save observations and continue'; form.append(save);
        const skip = document.createElement('button'); skip.type = 'button'; skip.textContent = 'Skip and continue'; form.append(skip);
        const finish = skipped => { const value = { note: skipped ? '' : note.value }; for (const key of Object.keys(criteria)) value[key] = skipped ? 'unknown' : form.elements.namedItem(key).value; form.remove(); resolveAnswer(value); };
        form.addEventListener('submit', event => { event.preventDefault(); finish(false); }); skip.addEventListener('click', () => finish(true));
        document.querySelector('aside').append(form); title.tabIndex = -1; title.focus();
      }), labelCriteria));
      result.observation = parseLabelObservation(answer);
      result.pointerEvidence = await operation('Pointer evidence', () => page.evaluate(() => window.rendererProbe.summary().pointerEvents));
      report.completedSteps++; await checkpoint();
      await stage(4, 'Save case', 'Saving visual observations; no performance verdict is produced.');
      await operation('Save screenshot', () => page.screenshot({ path: resolve(output, `sigma-${scale}-labels.png`) }));
      result.status = 'completed'; report.completedSteps++; report.completedCases++; await checkpoint();
    } finally {
      closing = true;
      await context?.close().catch(error => { report.failures.push(`Context cleanup: ${error}`); control.stop('context-cleanup-failure', true); });
      if (result.status !== 'completed') result.status = control.failed || report.failures.length ? 'failed' : 'interrupted';
    }
  });
} catch (error) {
  if (!control.stopped || control.failed) report.failures.push(String(error));
  if (!control.stopped) control.stop('execution-failure', true);
} finally {
  expectedClose = true; await stopCleanup;
  await browser?.close().catch(error => report.failures.push(`Browser cleanup: ${error}`));
  await control.settleResources();
  report.failures.push(...control.cleanupErrors);
  process.off('SIGINT', interrupt); process.off('SIGTERM', terminate);
  if (terminal) { process.stdin.off('end', inputClosed); process.stdin.off('close', inputClosed); process.stdin.pause(); }
  report.finishedAt = new Date().toISOString(); report.status = report.failures.length || control.failed ? 'failed' : control.stopped ? 'interrupted' : 'completed'; await checkpoint();
}
process.exitCode = report.status === 'failed' ? 2 : report.status === 'interrupted' ? 130 : 0;
