/** Disposable early observer installed before the application/harness bundle is evaluated. */
import { createPhaseLedger } from './phase-ledger';
const ledger = createPhaseLedger(() => performance.now());
let observer: PerformanceObserver | undefined;
let available = false;
const admit = (entries: PerformanceEntry[]) => ledger.record(entries.map(entry => ({ startTime: entry.startTime, duration: entry.duration, name: entry.name })));
try { observer = new PerformanceObserver(list => admit(list.getEntries())); observer.observe({ type: 'longtask', buffered: true }); available = true; } catch { /* Unknown observation is not a successful task-budget result. */ }
const drain = () => { if (observer) admit(observer.takeRecords()); };
const api = {
  mark(name: string) { drain(); ledger.mark(name); },
  snapshot() { drain(); const snapshot = ledger.snapshot(); return { ...snapshot, observerAvailable: available, noObservedTaskOver200ms: available ? snapshot.noObservedTaskOver200ms : null }; },
};
Object.assign(window, { rendererProbePhases: api });
api.mark('browser-blank');
