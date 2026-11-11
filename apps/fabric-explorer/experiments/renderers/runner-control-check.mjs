/** Disposable runner regressions: a cancellation must end the finite plan immediately. */
import assert from 'node:assert/strict';
import { mkdtempSync, readFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { spawnSync } from 'node:child_process';
import { createRunControl, createPlan, stages } from './runner-control.mjs';

const scratch = mkdtempSync(join(tmpdir(), 'renderer-runner-regression-'));
try {
  for (const scenario of ['abort', 'button', 'signal', 'eof', 'window-close', 'manual-signal', 'manual-button', 'failure-after-measurement', 'launch-stop', 'context-stop', 'non-tty', 'success', 'focused-sigma', 'diagnostic-labels']) {
    const output = join(scratch, scenario);
    const run = spawnSync(process.execPath, [new URL('./runner-regression-driver.mjs', import.meta.url).pathname, scenario, output], { encoding: 'utf8', timeout: 10000 });
    assert.equal(run.status, 0, `${scenario}: ${run.stderr}`);
    const state = JSON.parse(readFileSync(join(output, 'driver.json'), 'utf8'));
    const report = JSON.parse(readFileSync(join(output, 'observations.json'), 'utf8'));
    assert.equal(report.format, 'jai.renderer-probe.observations/4');
    const success = ['success', 'non-tty', 'focused-sigma', 'diagnostic-labels'].includes(scenario);
    const cases = ['focused-sigma', 'diagnostic-labels'].includes(scenario) ? 3 : 6;
    assert.equal(state.createdCases, success ? cases : scenario === 'launch-stop' ? 0 : 1, `${scenario}: a cancelled/failed case must not launch another graph`);
    assert.equal(state.exitCode, success ? 0 : scenario === 'failure-after-measurement' ? 2 : 130, scenario);
    assert.equal(state.closed, true, scenario);
    assert.equal(report.completedCases, success ? cases : 0, scenario);
    assert.equal(report.totalSteps, cases * stages.length);
    if (scenario !== 'launch-stop') {
      assert.match(run.stdout, new RegExp(`Case 1/${cases}.*Step 1/${cases * stages.length}`));
      assert.equal(report.results[0].caseStatus, success ? 'complete' : scenario === 'failure-after-measurement' ? 'failed' : 'interrupted', scenario);
    }
    if (scenario === 'diagnostic-labels') {
      assert.equal(report.diagnostics, 'memory-phases'); assert.equal(report.reviewScope, 'labels');
      assert.ok(state.events.indexOf('early-observer') < state.events.indexOf('html'));
      assert.equal(report.results[0].browserProcessReuse.startsWith('first-case'), true);
      assert.equal(report.results[1].browserProcessReuse.startsWith('same-browser-warm'), true);
      for (const entry of report.results) {
        assert.deepEqual(entry.memory.baselines.map(phase => phase.name), ['browser-blank', 'harness-unloaded-renderer', 'empty-renderer', 'bounded-graph']);
        assert.equal(entry.memory.peakBrowserRssBytes, null); assert.equal(entry.memory.absoluteRssStatus, 'unknown-incomplete');
        assert.ok(entry.memory.samples.every(sample => sample.browserRssBytes === null));
        assert.ok(entry.memory.baselines.every(phase => phase.sampleIndices.length === 5 && phase.complete === false));
        assert.equal(entry.phaseEvidenceCapturedThroughStage, 8); assert.equal(entry.phaseEvidence.overallMaxTaskMs, 942);
        assert.equal(entry.phaseEvidence.noObservedTaskOver200ms, false);
      }
    }
    if (scenario === 'context-stop') assert.equal(state.closedContexts, 1, 'A late-created context must be disposed exactly once');
    if (scenario === 'failure-after-measurement' || scenario.startsWith('manual-')) assert.equal(report.results[0].animation.p95Ms, 16, 'Interrupted reports must retain completed measurement evidence');
  }
} finally {
  rmSync(scratch, { recursive: true, force: true });
}
assert.equal(createPlan([1, 1.5, 2]).length * stages.length, 48);
assert.throws(() => createPlan([]));
assert.throws(() => createPlan([1, 1]));
assert.deepEqual(createPlan([1, 1.5, 2], 'sigma').map(item => item.renderer), ['sigma', 'sigma', 'sigma']);
assert.deepEqual(createPlan([2], 'cytoscape'), [{ renderer: 'cytoscape', scale: 2 }]);
assert.throws(() => createPlan([1], 'unknown'));
assert.throws(() => createPlan([1], 'cyto'));
let stopCalls = 0;
const scheduled = new Map();
let next = 0;
const control = createRunControl({ onStop: () => stopCalls++, setTimer: callback => { scheduled.set(++next, callback); return next; }, clearTimer: id => scheduled.delete(id) });
const blocked = control.operation('Controlled frozen animation', () => new Promise(() => {}), 30000);
await Promise.resolve();
assert.equal(control.stopped, false);
assert.equal(scheduled.size, 1);
scheduled.values().next().value();
await assert.rejects(blocked, { name: 'ProbeTimeoutError' });
assert.equal(control.failed, true);
assert.equal(control.stop('second-stop'), false);
assert.equal(stopCalls, 1);
assert.equal(scheduled.size, 0);
const human = createRunControl({ setTimer: () => { throw new Error('Human review must not get an inactivity timeout'); } });
const waiting = human.operation('Human review', () => new Promise(() => {}));
human.stop('operator-stop');
await assert.rejects(waiting, { name: 'AbortError' });
for (const label of ['Browser launch', 'Create browser context']) {
  let admit;
  let disposed = 0;
  const resourceControl = createRunControl();
  const acquisition = resourceControl.operation(label, () => new Promise(resolve => { admit = resolve; }), null, resource => resource.close());
  await Promise.resolve();
  resourceControl.stop('operator-stop-before-resource-resolution');
  await assert.rejects(acquisition, { name: 'AbortError' });
  admit({ close: async () => { disposed++; } });
  await resourceControl.settleResources();
  assert.equal(disposed, 1, label);
}
console.log('PASS: fourteen real-runner double scenarios including diagnostic baseline/labels mode including focused selection, finite progress, partial checkpoints, controlled watchdog, human-wait cancellation and late-resource disposal.');
