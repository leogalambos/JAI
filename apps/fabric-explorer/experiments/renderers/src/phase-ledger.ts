/** Disposable phase ledger; retain overall startup tasks and every cross-boundary overlap. */
/** Original task interval in browser performance-clock milliseconds. */
export type TaskEntry = { startTime: number; duration: number; name?: string };
/** Named interval in browser performance-clock milliseconds; absent end means still open. */
export type PhaseBoundary = { name: string; startTime: number; endTime?: number };
/**
 * Attribute one task to all intersecting phases without shortening its raw cost.
 * @param task Original observer entry.
 * @param phases Recorded browser-clock phase boundaries.
 * @param now Snapshot endpoint for the currently open phase.
 * @returns Every intersecting phase occurrence and actual overlap duration.
 */
export function overlaps(task: TaskEntry, phases: PhaseBoundary[], now: number) {
  return phases.flatMap((phase, phaseIndex) => {
    const milliseconds = Math.min(task.startTime + task.duration, phase.endTime ?? now) - Math.max(task.startTime, phase.startTime);
    return milliseconds > 0 ? [{ phase: phase.name, phaseIndex, overlapMs: milliseconds }] : [];
  });
}
/**
 * Record browser task entries independently of the driver clock.
 * @param now Monotonic browser clock.
 * @returns Phase markers, raw entry admission and a non-filtering snapshot.
 */
export function createPhaseLedger(now: () => number) {
  const coverageStart = now(); const phases: PhaseBoundary[] = []; const tasks: TaskEntry[] = [];
  return {
    mark(name: string) { const at = now(); if (phases.length) phases[phases.length - 1].endTime = at; phases.push({ name, startTime: at }); },
    record(entries: TaskEntry[]) { tasks.push(...entries); },
    snapshot() {
      const at = now(); const records = tasks.map(task => ({ ...task, overlaps: overlaps(task, phases, at) }));
      return { coverageStartMs: coverageStart, beforeCoverage: 'unknown-even-when-buffered-entries-exist', clock: 'browser-performance-time', capturedAtMs: at,
        phases: phases.map((phase, phaseIndex) => ({ ...phase, phaseIndex, endTime: phase.endTime ?? at })), tasks: records,
        overallMaxTaskMs: tasks.length ? Math.max(...tasks.map(task => task.duration)) : null,
        noObservedTaskOver200ms: tasks.every(task => task.duration <= 200),
        // Names recur across rebuilds; only occurrence identity joins an overlap.
        phaseSummaries: phases.map((phase, phaseIndex) => { const related = records.filter(task => task.overlaps.some(overlap => overlap.phaseIndex === phaseIndex)); return { name: phase.name, phaseIndex, startTime: phase.startTime, endTime: phase.endTime ?? at, taskCount: related.length, maxWholeTaskMs: related.length ? Math.max(...related.map(task => task.duration)) : null, note: 'Overlapping tasks may appear in multiple phases; never sum phase costs as unique time.' }; }) };
    },
  };
}
