/** Disposable guided-controls regressions; deterministic clocks, no native browser qualification. */
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { createProbeControls, progressText } from './src/probe-controls.ts';

const progress = { caseIndex: 1, caseCount: 6, stageIndex: 3, stageCount: 8, renderer: 'sigma', scale: 1, title: 'Automatic load test', instructions: 'Wait for measurement.', mode: 'automatic', remainingMs: 20000 };
let now = 1000;
let timer;
let clears = 0;
let stopped = 0;
let handlers;
const rendered = { countdown: '', progress: null, reviewVisible: false, disabled: false, instructions: '' };
let answers = {};
const view = {
  renderProgress: value => { rendered.progress = value; },
  renderCountdown: value => { rendered.countdown = value; },
  showReview: value => { rendered.reviewVisible = value; },
  readReview: () => ({ answers, note: 'Observed only this fixture.' }),
  resetReview: () => { answers = {}; },
  disableReview: value => { rendered.disabled = value; },
  showStopping: reason => { rendered.instructions = reason; },
  showReviewError: message => { throw new Error(message); },
  bind: value => { handlers = value; },
};
const controls = createProbeControls(view, {
  now: () => now, timestamp: () => '2030-01-01T00:00:00Z',
  setInterval: callback => { timer = callback; return 1; },
  clearInterval: () => { clears++; },
  requestStop: () => { stopped++; },
});
assert.equal(progressText(progress).overall, 'Overall step 3 of 48');
assert.equal(progressText({ ...progress, caseIndex: 6, stageIndex: 8 }).overall, 'Overall step 48 of 48');
assert.throws(() => progressText({ ...progress, caseIndex: 7 }));
controls.setProgress(progress);
assert.equal(rendered.countdown, '20 s remaining');
now += 7000; timer();
assert.equal(rendered.countdown, '13 s remaining');
now += 25000; timer();
assert.equal(rendered.countdown, '0 s — finishing measurement');
assert.ok(clears >= 1);

controls.setProgress({ ...progress, stageIndex: 6, mode: 'manual', remainingMs: undefined });
let review = controls.review();
assert.equal(rendered.reviewVisible, true);
answers = { parallelEdgePicking: 'pass', selfLoopPicking: 'fail', edgeLabelReadability: 'pass', edgeCanvasLabelReadability: 'fail' };
handlers.save();
let result = await review;
assert.equal(result.criteria.parallelEdgePicking, 'pass');
assert.equal(result.criteria.selfLoopPicking, 'fail');
assert.equal(result.format, 'jai.renderer-probe.operator-observation/2');
assert.equal(result.criteria.edgeLabelReadability, 'pass');
assert.equal(result.criteria.edgeCanvasLabelReadability, 'fail');
assert.equal(result.criteria.arrowDirection, 'unknown');
assert.equal(rendered.reviewVisible, false);

review = controls.review();
answers = { arrowDirection: 'pass' };
handlers.skip();
result = await review;
assert.ok(Object.values(result.criteria).every(value => value === 'unknown'));
assert.equal(result.method, 'operator-skipped');

review = controls.review();
const rejected = assert.rejects(review, { name: 'AbortError' });
handlers.stop('escape'); handlers.stop('stop-button');
await rejected;
assert.equal(stopped, 1);
assert.equal(rendered.disabled, true);
await assert.rejects(controls.review(), { name: 'AbortError' });

const html = await readFile(new URL('./index.html', import.meta.url), 'utf8');
for (const id of ['probe-case', 'probe-stage', 'probe-overall', 'probe-countdown', 'probe-stop', 'probe-review', 'probe-save', 'probe-skip']) {
  assert.ok(html.includes(`id="${id}"`), `Missing visible ${id} control`);
}
assert.ok(html.includes('Automatic load test'));
assert.ok(html.indexOf('id="details"') < html.indexOf('id="probe-review"'), 'Selected element must precede the scrollable manual questionnaire');
console.log('PASS: finite progress, controlled countdown, unknown-safe in-browser review and idempotent Stop/Escape.');
