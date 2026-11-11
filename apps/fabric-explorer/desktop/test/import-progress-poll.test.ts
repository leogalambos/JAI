/** Controlled UI polling prevents overlapping state reads and drops stale completions. */
import { afterEach, expect, it, vi } from 'vitest';
import { pollImportProgress } from '../src/renderer/import-progress.js';
import type { ImportProgress } from '../src/import/progress.js';
afterEach(() => vi.useRealTimers());
it('polls the existing state at one-second intervals with at most one read pending', async () => {
  vi.useFakeTimers(); let release!: (value: ImportProgress | undefined) => void;
  const read = vi.fn(() => new Promise<ImportProgress | undefined>(resolve => { release = resolve; })); const accept = vi.fn(); const stop = pollImportProgress(read, accept);
  expect(read).toHaveBeenCalledTimes(1); await vi.advanceTimersByTimeAsync(5000); expect(read).toHaveBeenCalledTimes(1);
  release(undefined); await Promise.resolve(); await vi.advanceTimersByTimeAsync(1000); expect(read).toHaveBeenCalledTimes(2); stop(); release(undefined);
});
it('ignores late reads after cancellation or replacement and removes its timer', async () => {
  vi.useFakeTimers(); let release!: (value: ImportProgress) => void;
  const accept = vi.fn(); const stop = pollImportProgress(() => new Promise(resolve => { release = resolve; }), accept);
  stop(); release({ phase: 'complete', bytesRead: 0, totalBytes: 0, records: 0, factsProcessed: 0, sourcesCompleted: 1, totalSources: 1 }); await Promise.resolve();
  expect(accept).not.toHaveBeenCalled(); expect(vi.getTimerCount()).toBe(0);
});
it('retains the owning request failure path when an observational poll fails', async () => {
  vi.useFakeTimers(); const accept = vi.fn(); const read = vi.fn(async () => { throw Error('State unavailable'); }); const stop = pollImportProgress(read, accept);
  await Promise.resolve(); await vi.advanceTimersByTimeAsync(1000); stop(); expect(read).toHaveBeenCalledTimes(2); expect(accept).not.toHaveBeenCalled();
});
