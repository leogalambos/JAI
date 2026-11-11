/** Bounded scalar import observations; counts describe completed work, never guessed totals. */
export interface ImportProgress {
  readonly phase: 'processing' | 'indexing' | 'complete';
  readonly bytesRead: number; readonly totalBytes: number; readonly records: number; readonly factsProcessed: number;
  readonly sourcesCompleted: number; readonly totalSources: number;
}
/** One candidate's clock-throttled observer, without timers or per-record transport. */
export class ImportProgressReporter {
  private latest: ImportProgress;
  private emittedAt = -Infinity;
  private emittedPhase: ImportProgress['phase'] | null = null;
  /**
   * Bind known captured totals and a fixed observer.
   * @param totalBytes Sum of admitted capture lengths.
   * @param totalSources Selected source count.
   * @param emit Correlated worker message sink.
   * @param now Monotonic clock; tests control it explicitly.
   */
  constructor(totalBytes: number, totalSources: number, private readonly emit: (value: ImportProgress) => void, private readonly now: () => number = () => performance.now()) {
    this.latest = { phase: 'processing', bytesRead: 0, totalBytes, records: 0, factsProcessed: 0, sourcesCompleted: 0, totalSources };
    this.update(this.latest);
  }
  /**
   * Observe cumulative local work, emitting at most once per second except phase transitions.
   * @param value Actual completed stream/projection counters.
   */
  update(value: ImportProgress): void {
    this.latest = value; const at = this.now();
    if (value.phase !== this.emittedPhase || at - this.emittedAt >= 1000) { this.emittedPhase = value.phase; this.emittedAt = at; this.emit({ ...value }); }
  }
  /** Emit completion only after the candidate's query index is ready. */
  complete(): void { this.update({ ...this.latest, phase: 'complete' }); }
}
/**
 * Decode the fixed private progress message at the worker/main boundary.
 * @param value Unknown received scalar payload.
 * @returns A detached bounded progress observation.
 * @throws {Error} For malformed fields, invalid counts or false completed-byte totals.
 */
export function importProgress(value: unknown): ImportProgress {
  if (!value || typeof value !== 'object' || Array.isArray(value)) throw new Error('Invalid import progress.');
  const item = value as ImportProgress;
  if (Object.keys(item).sort().join() !== 'bytesRead,factsProcessed,phase,records,sourcesCompleted,totalBytes,totalSources' || !['processing', 'indexing', 'complete'].includes(item.phase)) throw new Error('Invalid import progress.');
  for (const name of ['bytesRead', 'totalBytes', 'records', 'factsProcessed', 'sourcesCompleted', 'totalSources'] as const) if (!Number.isSafeInteger(item[name]) || item[name] < 0) throw new Error('Invalid import progress.');
  if (item.totalBytes > 1024 * 1024 * 1024 || item.bytesRead > item.totalBytes || item.totalSources < 1 || item.totalSources > 128 || item.sourcesCompleted > item.totalSources || item.phase !== 'processing' && (item.bytesRead !== item.totalBytes || item.sourcesCompleted !== item.totalSources)) throw new Error('Invalid import progress.');
  return { ...item };
}
/**
 * Format exact counts without inventing record/fact denominators.
 * @param value Bounded observed candidate progress.
 * @returns A source-value-free English status line.
 */
export function importProgressText(value: ImportProgress): string {
  const phase = value.phase === 'processing' ? 'Loading sources' : value.phase === 'indexing' ? 'Building graph indexes' : 'Import complete';
  return `${phase}: ${value.bytesRead.toLocaleString('en-US')} / ${value.totalBytes.toLocaleString('en-US')} bytes; ${value.records.toLocaleString('en-US')} records read; ${value.factsProcessed.toLocaleString('en-US')} facts projected; ${value.sourcesCompleted} / ${value.totalSources} sources processed.`;
}
