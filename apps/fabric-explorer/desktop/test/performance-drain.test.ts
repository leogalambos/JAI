/** Controlled sample ordering and clock boundaries; no process launch, sleep or PID manipulation. */
import { expect, it } from 'vitest';
import { performanceDrainComplete, performanceDrainWitness } from './performance-drain.js';
import type { ResidentSample } from './performance-resident-window.js';
const context = { rootExitObservedMs: 100, checkedMs: 160, stdioClosed: true, samplerError: null };
const sample = (changes: Partial<ResidentSample['selected']> = {}, startedMs = 120, endedMs = 140): ResidentSample => ({ startedMs, endedMs,
  selected: { residentBytes: 0, processes: [], observedOrphans: [], rootPresent: false, rootObserved: true, rootPidReused: false, ownershipComplete: true, collectionErrors: [], vanishedDuringCollection: 0, attributedVanishedPids: [], ...changes } });
it('continues past the actual empty-but-attributed-disappearance shape and accepts a later clean sample', () => {
  const uncertain = sample({ attributedVanishedPids: [415524, 415525] });
  expect(performanceDrainComplete(uncertain, context)).toBe(false);
  expect(performanceDrainWitness(null, uncertain, context)).toBeNull();
  const clean = sample({}, 170, 180); const witness = performanceDrainWitness(null, clean, { ...context, checkedMs: 190 });
  expect(witness?.sample).toBe(clean); expect(performanceDrainComplete(witness!.sample, { ...context, checkedMs: witness!.checkedMs })).toBe(true);
});
it.each([
  sample({ rootObserved: false }), sample({ rootPidReused: true }), sample({ collectionErrors: [{ pid: 42, code: 'EACCES' }] }),
  sample({ processes: [{ pid: 42, parentPid: 1, startTicks: '7', cpuTicks: '1', residentBytes: 1 }] }),
  sample({ attributedVanishedPids: [42] }), sample({}, 90, 140),
])('rejects uncertainty or remaining owned lifetimes without treating empty RSS as absence', candidate => {
  expect(performanceDrainComplete(candidate, context)).toBe(false); expect(performanceDrainWitness(null, candidate, context)).toBeNull();
});
it('requires inherited stdio closure and preserves sampler errors', () => {
  expect(performanceDrainComplete(sample(), { ...context, stdioClosed: false })).toBe(false);
  expect(performanceDrainComplete(sample(), { ...context, samplerError: 'failed append' })).toBe(false);
});
it('never accepts a witness after the original two-second window, even if collection began earlier', () => {
  expect(performanceDrainWitness(null, sample({}, 2050, 2090), { ...context, checkedMs: 2100 })).not.toBeNull();
  expect(performanceDrainWitness(null, sample({}, 2050, 2090), { ...context, checkedMs: 2100.01 })).toBeNull();
  expect(performanceDrainWitness(null, sample({}, 2050, 2110), { ...context, checkedMs: 2110 })).toBeNull();
});
it('keeps the exact terminal witness despite a later uncertain append or late collection', () => {
  const clean = sample(); const witness = performanceDrainWitness(null, clean, context)!;
  const late = sample({ attributedVanishedPids: [42] }, 170, 180);
  expect(performanceDrainWitness(witness, late, { ...context, checkedMs: 190 })).toBe(witness);
  expect(performanceDrainWitness(witness, late, { ...context, checkedMs: 2200 })).toBe(witness);
  expect(witness.sample).toBe(clean); expect(witness.checkedMs).toBe(160);
  expect(performanceDrainComplete(witness.sample, { ...context, checkedMs: witness.checkedMs, samplerError: 'observer failed' })).toBe(false);
});
