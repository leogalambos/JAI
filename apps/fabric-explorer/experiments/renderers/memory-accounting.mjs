/** Disposable Chromium/driver memory accounting; RSS totals and diagnostic PSS are distinct. */
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';
import { readFile } from 'node:fs/promises';

const execute = promisify(execFile);
const validPid = pid => Number.isSafeInteger(pid) && pid > 0;
const bytes = value => Number.isSafeInteger(value) && value >= 0;
const sorted = iterable => [...iterable].sort((a, b) => a - b);

/**
 * Parse numeric process counters without retaining unrelated command lines.
 * @param text Standard ps PID, parent PID and RSS-in-KiB output.
 * @returns Numeric process rows with RSS converted to bytes.
 * @throws {Error} A row is malformed or contains an invalid counter.
 */
export function parsePsRows(text) {
  return text.trim().split('\n').filter(Boolean).map(line => {
    const fields = line.trim().split(/\s+/);
    const [pid, parentPid, rssKiB] = fields.map(Number);
    if (fields.length !== 3 || !validPid(pid) || !Number.isSafeInteger(parentPid) || parentPid < 0 || !bytes(rssKiB * 1024)) throw new Error('Invalid numeric ps PID/parent/RSS row');
    return { pid, parentPid, rssBytes: rssKiB * 1024 };
  });
}

/**
 * Parse optional Linux proportional/private memory diagnostics.
 * @param text One process's smaps_rollup content.
 * @returns Byte counters, or null for unavailable fields.
 */
export function parseSmapsRollup(text) {
  const values = new Map();
  for (const line of text.split('\n')) {
    const match = /^(Pss|Private_Clean|Private_Dirty|Private_Hugetlb):\s+(\d+) kB$/.exec(line.trim());
    if (match) values.set(match[1], Number(match[2]) * 1024);
  }
  return {
    pssBytes: bytes(values.get('Pss')) ? values.get('Pss') : null,
    privateBytes: values.has('Private_Clean') && values.has('Private_Dirty') ? values.get('Private_Clean') + values.get('Private_Dirty') + (values.get('Private_Hugetlb') ?? 0) : null,
  };
}

/**
 * Account a paired snapshot without substituting partial observations for totals.
 * @param before CDP inventory immediately before counter acquisition.
 * @param after CDP inventory immediately after counter acquisition.
 * @param rows Numeric ps counters from the intervening observation.
 * @param driverPid Measurement driver excluded from browser totals.
 * @param diagnostics Optional PID-keyed Linux proportional/private byte counters.
 * @param errors Prior acquisition errors that make RSS evidence incomplete.
 * @returns Separate browser/driver totals, nullable unavailable totals and raw attribution.
 */
export function accountMemorySnapshot({ before = [], after = [], rows = [], driverPid, diagnostics = new Map(), errors: priorErrors = [] }) {
  const errors = [...priorErrors];
  const normalize = (list, label) => {
    const map = new Map();
    for (const item of list) {
      if (!validPid(item.id) || typeof item.type !== 'string') { errors.push(`${label}: invalid process inventory entry`); continue; }
      if (map.has(item.id) && map.get(item.id) !== item.type) errors.push(`${label}: conflicting process role for ${item.id}`);
      map.set(item.id, item.type);
    }
    return map;
  };
  const first = normalize(before, 'before');
  const last = normalize(after, 'after');
  const rootsBefore = [...first].filter(([, type]) => type === 'browser').map(([pid]) => pid);
  const rootsAfter = [...last].filter(([, type]) => type === 'browser').map(([pid]) => pid);
  const rootPid = rootsBefore.length === 1 && rootsAfter.length === 1 && rootsBefore[0] === rootsAfter[0] && rootsBefore[0] !== driverPid ? rootsBefore[0] : null;
  if (rootPid === null) errors.push('A stable distinct Chromium browser root is unavailable');
  const counters = new Map();
  for (const row of rows) {
    if (!validPid(row.pid) || !Number.isSafeInteger(row.parentPid) || row.parentPid < 0 || !bytes(row.rssBytes)) { errors.push('Invalid process counter row'); continue; }
    const previous = counters.get(row.pid);
    if (previous && (previous.rssBytes !== row.rssBytes || previous.parentPid !== row.parentPid)) errors.push(`Conflicting process counter rows for ${row.pid}`);
    else counters.set(row.pid, row);
  }
  const rootedPids = new Set(rootPid === null ? [] : [rootPid]);
  if (rootPid !== null) {
    let grew = true;
    while (grew) {
      grew = false;
      for (const row of counters.values()) if (rootedPids.has(row.parentPid) && row.pid !== driverPid && !rootedPids.has(row.pid)) { rootedPids.add(row.pid); grew = true; }
    }
  }
  const browserPids = new Set([...rootedPids, ...first.keys(), ...last.keys()]);
  if (browserPids.has(driverPid)) errors.push('Measurement driver appeared in Chromium inventory');
  browserPids.delete(driverPid);
  const newPids = sorted([...last.keys()].filter(pid => !first.has(pid)));
  const exitedPids = sorted([...first.keys()].filter(pid => !last.has(pid)));
  const changedRolePids = sorted([...first.keys()].filter(pid => last.has(pid) && first.get(pid) !== last.get(pid)));
  const missingPids = sorted([...browserPids].filter(pid => !counters.has(pid)));
  const unexpectedPids = sorted([...browserPids].filter(pid => counters.has(pid) && !rootedPids.has(pid)));
  const unlistedDescendantPids = sorted([...browserPids].filter(pid => !first.has(pid) && !last.has(pid)));
  const processes = sorted(browserPids).map(pid => ({
    pid, parentPid: counters.get(pid)?.parentPid ?? null, role: last.get(pid) ?? first.get(pid) ?? 'unlisted-browser-descendant',
    rssBytes: counters.get(pid)?.rssBytes ?? null,
    pssBytes: diagnostics.get(pid)?.pssBytes ?? null, privateBytes: diagnostics.get(pid)?.privateBytes ?? null,
  }));
  const complete = rootPid !== null && errors.length === 0 && missingPids.length === 0 && unexpectedPids.length === 0 && newPids.length === 0 && exitedPids.length === 0 && changedRolePids.length === 0;
  const observedBrowserRssBytes = processes.reduce((total, item) => total + (item.rssBytes ?? 0), 0);
  const browserRssBytes = complete ? observedBrowserRssBytes : null;
  const driverRssBytes = counters.get(driverPid)?.rssBytes ?? null;
  const diagnosticTotal = key => complete && processes.every(item => bytes(item[key])) ? processes.reduce((total, item) => total + item[key], 0) : null;
  return {
    complete, rootPid, browserRssBytes, observedBrowserRssBytes,
    driverRssBytes, combinedRssBytes: browserRssBytes !== null && driverRssBytes !== null ? browserRssBytes + driverRssBytes : null,
    browserPssBytes: diagnosticTotal('pssBytes'), browserPrivateBytes: diagnosticTotal('privateBytes'),
    processes, missingPids, unexpectedPids, newPids, exitedPids, changedRolePids, unlistedDescendantPids, errors,
    measurement: 'sum-ps-rss-browser-tree-driver-separate; RSS-can-double-count-shared-pages; PSS/private-diagnostic-only',
  };
}

/**
 * Capture one non-atomic paired inventory/counter sample.
 * @param cdpSession Browser-level CDP session supporting SystemInfo.getProcessInfo.
 * @param driverPid Measurement driver PID to report separately.
 * @param adapters Optional controlled clock, platform and readers for deterministic checks.
 * @returns Raw timestamps/process attribution and nullable byte totals; acquisition errors are data.
 */
export async function captureMemorySample(cdpSession, driverPid, adapters = {}) {
  const now = adapters.now ?? Date.now;
  const platform = adapters.platform ?? process.platform;
  const startedAtMs = now();
  const errors = [];
  const inventory = {};
  async function captureInventory(label) {
    inventory[`${label}StartedAtMs`] = now();
    try {
      const reply = await cdpSession.send('SystemInfo.getProcessInfo');
      if (!Array.isArray(reply.processInfo)) throw new Error('Missing processInfo array');
      inventory[label] = reply.processInfo.map(({ id, type }) => ({ id, type }));
    } catch (error) { errors.push(`${label} inventory: ${String(error)}`); inventory[label] = []; }
    inventory[`${label}AtMs`] = now();
  }
  await captureInventory('before');
  const counters = { startedAtMs: now(), rssFinishedAtMs: null, finishedAtMs: null, method: 'ps -axo pid=,ppid=,rss=; KiB converted to bytes', diagnostics: [] };
  let rows = [];
  try {
    if (adapters.readRows) rows = await adapters.readRows();
    else {
      if (platform === 'win32') throw new Error('Windows process counters unavailable in this Linux/macOS experiment');
      const listing = await execute('ps', ['-axo', 'pid=,ppid=,rss='], { encoding: 'utf8', timeout: 2000, maxBuffer: 8 * 1024 * 1024 });
      rows = parsePsRows(listing.stdout);
    }
  } catch (error) { errors.push(`process counters: ${String(error)}`); }
  counters.rssFinishedAtMs = now();
  const preliminary = accountMemorySnapshot({ before: inventory.before, after: inventory.before, rows, driverPid });
  const diagnostics = new Map();
  if (platform === 'linux') await Promise.all(preliminary.processes.map(async ({ pid }) => {
    const detail = { pid, startedAtMs: now(), finishedAtMs: null, status: 'available' };
    try {
      const value = adapters.readDiagnostic ? await adapters.readDiagnostic(pid) : parseSmapsRollup(await readFile(`/proc/${pid}/smaps_rollup`, 'utf8'));
      diagnostics.set(pid, value);
      if (value.pssBytes === null || value.privateBytes === null) detail.status = 'incomplete';
    } catch (error) { detail.status = 'unavailable'; detail.error = String(error); }
    detail.finishedAtMs = now(); counters.diagnostics.push(detail);
  }));
  counters.finishedAtMs = now();
  await captureInventory('after');
  const account = accountMemorySnapshot({ before: inventory.before, after: inventory.after, rows, driverPid, diagnostics, errors });
  return { format: 'jai.renderer-probe.memory-sample/1', startedAtMs, finishedAtMs: now(), platform, inventory, counters, ...account,
    snapshotAtomic: false, diagnosticMethod: platform === 'linux' ? 'per-process smaps_rollup PSS/private; unavailable counters remain null' : 'PSS/private unavailable on this platform' };
}
