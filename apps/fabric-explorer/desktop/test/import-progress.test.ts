/** Controlled-clock progress throttling, counters and private transport boundary. */
import { expect, it } from 'vitest';
import { ImportProgressReporter, importProgress, importProgressText, type ImportProgress } from '../src/import/progress.js';
const value: ImportProgress = { phase: 'processing', bytesRead: 0, totalBytes: 100, records: 0, factsProcessed: 0, sourcesCompleted: 0, totalSources: 1 };
it('emits at most once per second during processing and immediately for indexing/completion', () => {
  let now = 0; const events: ImportProgress[] = []; const reporter = new ImportProgressReporter(100, 1, event => events.push(event), () => now);
  for (let row = 1; row <= 10000; row++) reporter.update({ ...value, records: row });
  expect(events).toHaveLength(1); now = 999; reporter.update({ ...value, bytesRead: 50, records: 10000 }); expect(events).toHaveLength(1);
  now = 1000; reporter.update({ ...value, bytesRead: 100, records: 12000, factsProcessed: 5, sourcesCompleted: 1 }); expect(events).toHaveLength(2);
  reporter.update({ ...events[1]!, phase: 'indexing' }); reporter.complete();
  expect(events.map(event => event.phase)).toEqual(['processing', 'processing', 'indexing', 'complete']); expect(events.at(-1)).toMatchObject({ bytesRead: 100, records: 12000, factsProcessed: 5 });
});
it('detaches emitted observations from reused local counter objects without per-row transport', () => {
  let now = 0; const events: ImportProgress[] = []; const reporter = new ImportProgressReporter(100, 1, event => events.push(event), () => now);
  const current = { ...value }; reporter.update(current); current.bytesRead = 50; now = 1000; reporter.update(current); current.bytesRead = 100;
  expect(events.map(event => event.bytesRead)).toEqual([0, 50]); expect(events.some(event => event.phase === 'complete')).toBe(false);
});
it('rejects false totals, unexpected fields and invalid phases at the private boundary', () => {
  expect(importProgress(value)).toEqual(value); expect(importProgress({ ...value, bytesRead: 100 })).toMatchObject({ bytesRead: 100 });
  for (const bad of [{ ...value, bytesRead: 101 }, { ...value, records: -1 }, { ...value, phase: 'complete' }, { ...value, totalSources: 129 }, { ...value, sourcePath: '/private' }]) expect(() => importProgress(bad)).toThrow();
});
it('formats real counts and names indexing without guessing row or fact denominators', () => {
  expect(importProgressText({ ...value, records: 1234 })).toBe('Loading sources: 0 / 100 bytes; 1,234 records read; 0 facts projected; 0 / 1 sources processed.');
  expect(importProgressText({ ...value, phase: 'indexing', bytesRead: 100, sourcesCompleted: 1 })).toContain('Building graph indexes');
  expect(importProgressText({ ...value, phase: 'complete', bytesRead: 100, sourcesCompleted: 1 })).toContain('Import complete');
});
