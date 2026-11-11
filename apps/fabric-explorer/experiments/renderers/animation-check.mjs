/** Disposable failed-first regressions for frame-start versus callback-time measurement ordering. */
import assert from 'node:assert/strict';
import { animateProjection } from './src/animation.ts';
function harness() {
  let now = 1000;
  let generation = 0;
  const callbacks = [];
  const panTimes = [];
  const result = animateProjection({ now: () => now, generation: () => generation, requestFrame: callback => callbacks.push(callback), panZoom: seconds => panTimes.push(seconds) });
  return { result, panTimes, cancel: () => generation++, frame: (timestamp, callbackNow) => { now = callbackNow; assert.ok(callbacks.length); callbacks.shift()(timestamp); } };
}
const cancelled = harness();
cancelled.cancel(); cancelled.frame(992, 1001);
const cancellation = await cancelled.result;
assert.equal(cancellation.durationMs, 1, 'Cancellation uses callback wall time, never an earlier frame-start instant');
assert.deepEqual(cancellation.samplesMs, []);
assert.equal(cancellation.cancelled, true);
for (const offset of [0.1, 2.9, 5.3, 8, 11.7]) {
  const early = harness(); early.cancel(); early.frame(1000 - offset, 1001);
  assert.equal((await early.result).durationMs, 1);
  assert.deepEqual(early.panTimes, []);
}
const active = harness();
active.frame(992, 1001); active.frame(1008, 1009); active.frame(1024, 1025); active.frame(21001, 21002);
const observed = await active.result;
assert.deepEqual(observed.samplesMs, [16, 16, 19977], 'Only successive frame timestamps form samples, including the final slow interval');
assert.equal(observed.durationMs, 20002);
assert.equal(observed.cancelled, false);
assert.equal(observed.p95Ms, 19977, 'Slow frames are retained rather than filtered to meet a budget');
assert.equal(observed.frameBudgetMet, false);
assert.ok(active.panTimes.every(time => time >= 0));
const afterFrames = harness();
afterFrames.frame(992, 1001); afterFrames.frame(1008, 1009); afterFrames.cancel(); afterFrames.frame(1024, 1025);
assert.deepEqual((await afterFrames.result).samplesMs, [16], 'Cancellation preserves already recorded active intervals');
const backwardsWall = harness(); backwardsWall.frame(992, 999);
await assert.rejects(backwardsWall.result, /Monotonic callback clock/);
const backwardsFrame = harness(); backwardsFrame.frame(1008, 1009); backwardsFrame.frame(992, 1025);
await assert.rejects(backwardsFrame.result, /Nondecreasing frame timestamps/);
await assert.rejects(animateProjection({ now: () => 0, generation: () => 0, requestFrame: () => {}, panZoom: () => {} }, 30000));
console.log('PASS: injected callback time, successive rAF samples, early cancellation and registered 20-second duration.');
