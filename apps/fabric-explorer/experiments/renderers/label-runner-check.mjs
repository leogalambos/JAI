/** Actual standalone runner cancellation/cleanup through browser doubles; never native visual qualification. */
import assert from 'node:assert/strict';
import { chromium } from '@playwright/test';
import { mkdtemp, readFile, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { PassThrough } from 'node:stream';
import { createCorpus } from './src/corpus.ts';
const s = createCorpus('S'), m = createCorpus('M');
assert.deepEqual(s.nodes.slice(0, 2), m.nodes.slice(0, 2)); assert.deepEqual(s.edges.slice(0, 4), m.edges.slice(0, 4));
const scratch = await mkdtemp(join(tmpdir(), 'jai-label-runner-'));
const launch = chromium.launch, argumentsBefore = process.argv, exitBefore = process.exitCode, stdinBefore = Object.getOwnPropertyDescriptor(process, 'stdin');
const scenarios = ['complete', 'button', 'escape', 'window', 'SIGINT', 'SIGTERM', 'EOF', 'wrong-bounds', 'context-cleanup', 'browser-cleanup', 'late-context-cleanup'];
try {
  for (const scenario of scenarios) {
    let closed = 0, tiny = 0, empty = 0, created = 0, stopBinding, closeHandler;
    const input = new PassThrough(); input.isTTY = true;
    Object.defineProperty(process, 'stdin', { configurable: true, value: input });
    const output = join(scratch, scenario);
    const closeContext = async () => { if (['context-cleanup', 'late-context-cleanup'].includes(scenario)) throw new Error('Controlled context disposal failed'); };
    chromium.launch = async options => {
      assert.equal(options.headless, false); assert.equal(options.chromiumSandbox, true); assert.equal(options.args, undefined);
      return { on() {}, version: () => 'controlled-not-native', close: async () => { closed++; if (scenario === 'browser-cleanup') throw new Error('Controlled browser disposal failed'); }, newContext: async () => {
        created++;
        if (scenario === 'late-context-cleanup') { process.emit('SIGINT'); return { close: closeContext }; }
        return { close: closeContext, newPage: async () => ({ on(event, handler) { if (event === 'close') closeHandler = handler; }, route: async () => {}, exposeBinding: async (_name, binding) => { stopBinding = binding; }, setContent: async () => {}, addStyleTag: async () => {}, addScriptTag: async () => {}, waitForFunction: async () => {}, screenshot: async () => {}, evaluate: async (fn, value) => {
          const source = String(fn);
          assert.ok(!source.includes('.loadGraph(') && !source.includes('.animate(') && !source.includes('.expand('), 'No dense/animation actions');
          if (source.includes('.emptyRenderer(')) { empty++; return { visibleVertices: 0, visibleEdges: 0 }; }
          if (source.includes('.loadFeature(')) { tiny++; return { visibleVertices: scenario === 'wrong-bounds' ? 2000 : 2, visibleEdges: 4 }; }
          if (source.includes('resolveAnswer')) {
            if (scenario === 'button' || scenario === 'escape') stopBinding({}, scenario === 'escape' ? 'browser-escape' : 'browser-stop-button');
            if (scenario === 'window') closeHandler();
            if (scenario === 'SIGINT' || scenario === 'SIGTERM') process.emit(scenario);
            if (scenario === 'EOF') input.emit('end');
            return {};
          }
          if (source.includes('.pointerEvents')) return [];
          if (source.includes('setProgress')) assert.equal(value.stageCount, 4);
        } }) };
      } };
    };
    process.argv = [process.execPath, 'run-label-check.mjs', `--output=${output}`, '--scales=1,1.5,2'];
    await import(`./run-label-check.mjs?scenario=${scenario}`);
    const report = JSON.parse(await readFile(join(output, 'observations.json'), 'utf8'));
    assert.equal(report.totalSteps, 12); assert.ok(closed); assert.equal(report.mode, 'labels-only');
    assert.equal(report.memory, undefined); assert.equal(report.performance, undefined);
    for (const result of report.results) { assert.equal(result.observation.pathSeparation, 'unknown'); assert.equal(result.observation.canvasLabelReadability, 'unknown'); }
    if (scenario === 'complete') { assert.equal(report.completedSteps, 12); assert.equal(created, 3); assert.equal(tiny, 3); assert.equal(empty, 3); assert.equal(report.status, 'completed'); assert.equal(report.failures.length, 0); assert.equal(process.exitCode, 0); }
    else if (['wrong-bounds', 'context-cleanup', 'browser-cleanup', 'late-context-cleanup'].includes(scenario)) { assert.equal(report.status, 'failed'); assert.ok(report.failures.length); assert.equal(process.exitCode, 2); if (scenario === 'late-context-cleanup') { assert.ok(report.failures.some(value => value.includes('Create context'))); assert.equal(report.results[0].status, 'interrupted'); } }
    else { assert.equal(created, 1); assert.equal(report.status, 'interrupted'); assert.equal(report.failures.length, 0); assert.equal(process.exitCode, 130); assert.equal(report.completedCases, 0); assert.equal(report.results[0].status, 'interrupted'); assert.equal(report.completedSteps, 2); }
    input.destroy(); process.exitCode = exitBefore;
  }
  console.log(`PASS: ${scenarios.length} actual labels-only runner scenarios: finite12steps, unknown, bounds, Stop/Escape/window/signals/EOF and late/ordinary cleanup failures; double only.`);
} finally { chromium.launch = launch; process.argv = argumentsBefore; process.exitCode = exitBefore; Object.defineProperty(process, 'stdin', stdinBefore); await rm(scratch, { recursive: true, force: true }); }
