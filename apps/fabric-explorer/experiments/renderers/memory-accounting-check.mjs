/** Disposable accounting regressions; no native browser-memory verdict is made. */
import assert from 'node:assert/strict';
import { accountMemorySnapshot, parsePsRows, parseSmapsRollup, captureMemorySample } from './memory-accounting.mjs';

const inventory = [{ id: 20, type: 'browser' }, { id: 22, type: 'renderer' }];
const rows = [
  { pid: 10, parentPid: 1, rssBytes: 100 },
  { pid: 20, parentPid: 10, rssBytes: 200 },
  { pid: 21, parentPid: 20, rssBytes: 50 },
  { pid: 22, parentPid: 21, rssBytes: 300 },
  { pid: 90, parentPid: 1, rssBytes: 9999 },
];
const diagnostic = new Map([[20, { pssBytes: 100, privateBytes: 80 }], [21, { pssBytes: 20, privateBytes: 10 }], [22, { pssBytes: 180, privateBytes: 100 }]]);
const input = { before: inventory, after: inventory, rows, driverPid: 10, diagnostics: diagnostic };
const stable = accountMemorySnapshot(input);
assert.equal(stable.complete, true);
assert.equal(stable.browserRssBytes, 550, 'Browser tree excludes the measurement driver and unrelated browser');
assert.equal(stable.driverRssBytes, 100);
assert.equal(stable.combinedRssBytes, 650);
assert.equal(stable.browserPssBytes, 300, 'PSS remains a separate diagnostic, never replacing RSS');
assert.equal(stable.browserPrivateBytes, 190);
assert.deepEqual(stable.unlistedDescendantPids, [21], 'CDP can omit a zygote; tree closure still accounts for it');
assert.equal(accountMemorySnapshot({ ...input, rows: [...rows, rows[1]] }).browserRssBytes, 550, 'Duplicate identical PID rows cannot double count');
const conflicting = accountMemorySnapshot({ ...input, rows: [...rows, { ...rows[1], rssBytes: 201 }] });
assert.equal(conflicting.complete, false);
assert.equal(conflicting.browserRssBytes, null);
const missing = accountMemorySnapshot({ ...input, rows: rows.filter(row => row.pid !== 22) });
assert.deepEqual(missing.missingPids, [22]);
assert.equal(missing.browserRssBytes, null, 'Missing counters never look like reduced successful memory');
assert.equal(missing.observedBrowserRssBytes, 250);
const churn = accountMemorySnapshot({ ...input, after: [{ id: 20, type: 'browser' }, { id: 23, type: 'renderer' }] });
assert.deepEqual(churn.newPids, [23]);
assert.deepEqual(churn.exitedPids, [22]);
assert.equal(churn.browserRssBytes, null);
const detached = accountMemorySnapshot({ ...input, before: [...inventory, { id: 90, type: 'renderer' }], after: [...inventory, { id: 90, type: 'renderer' }] });
assert.deepEqual(detached.unexpectedPids, [90]);
assert.equal(detached.browserRssBytes, null, 'Detached inventoried process is reported, not silently omitted');
assert.equal(accountMemorySnapshot({ ...input, before: [], after: [] }).browserRssBytes, null);
assert.equal(accountMemorySnapshot({ ...input, rows: rows.filter(row => row.pid !== 10) }).driverRssBytes, null);
assert.equal(accountMemorySnapshot({ ...input, diagnostics: new Map() }).browserPssBytes, null);
assert.equal(accountMemorySnapshot({ ...input, before: [{ id: 10, type: 'browser' }], after: [{ id: 10, type: 'browser' }] }).browserRssBytes, null, 'Driver cannot be accepted as browser root');
assert.deepEqual(parsePsRows('20 10 200\n22 20 300\n'), [{ pid: 20, parentPid: 10, rssBytes: 204800 }, { pid: 22, parentPid: 20, rssBytes: 307200 }]);
assert.throws(() => parsePsRows('20 10 -1'));
assert.throws(() => parsePsRows('20 10 unknown'));
assert.deepEqual(parseSmapsRollup('Pss: 10 kB\nPrivate_Clean: 2 kB\nPrivate_Dirty: 3 kB\nPrivate_Hugetlb: 1 kB\n'), { pssBytes: 10240, privateBytes: 6144 });
assert.equal(parseSmapsRollup('Rss: 20 kB\n').pssBytes, null);

// Controlled adapters exercise capture ordering and failure without a real process or browser.
let now = 100;
let inventories = 0;
const adapters = {
  platform: 'linux', now: () => now++,
  readRows: async () => rows,
  readDiagnostic: async pid => diagnostic.get(pid) ?? { pssBytes: null, privateBytes: null },
};
const session = { send: async method => { assert.equal(method, 'SystemInfo.getProcessInfo'); inventories++; return { processInfo: inventory }; } };
const captured = await captureMemorySample(session, 10, adapters);
assert.equal(inventories, 2);
assert.equal(captured.complete, true);
assert.ok(captured.inventory.beforeAtMs < captured.counters.startedAtMs);
assert.ok(captured.counters.startedAtMs < captured.counters.rssFinishedAtMs);
assert.ok(captured.counters.finishedAtMs < captured.inventory.afterAtMs);
assert.equal(captured.browserRssBytes, 550);
const unavailable = await captureMemorySample({ send: async () => { throw new Error('inventory denied'); } }, 10, adapters);
assert.equal(unavailable.complete, false);
assert.equal(unavailable.browserRssBytes, null);
assert.ok(unavailable.errors.some(error => error.includes('inventory denied')));
const diagnosticsDenied = await captureMemorySample(session, 10, { ...adapters, readDiagnostic: async () => { throw new Error('smaps denied'); } });
assert.equal(diagnosticsDenied.complete, true, 'Optional diagnostics do not invalidate complete RSS');
assert.equal(diagnosticsDenied.browserPssBytes, null);
assert.ok(diagnosticsDenied.counters.diagnostics.every(item => item.status === 'unavailable'));
const countersDenied = await captureMemorySample(session, 10, { ...adapters, readRows: async () => { throw new Error('ps denied'); } });
assert.equal(countersDenied.complete, false);
assert.equal(countersDenied.browserRssBytes, null);
assert.equal(countersDenied.driverRssBytes, null);
console.log('PASS: browser/driver separation, tree closure, RSS/PSS diagnostics, duplicates, missing/churn/unavailable counters and capture chronology.');
