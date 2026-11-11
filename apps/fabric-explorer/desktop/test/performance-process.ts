// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Read-only Linux sampled process-tree accounting; the collector runs outside the measured app tree. */
import { readdir, readFile } from 'node:fs/promises';
import { join } from 'node:path';

/** One host PID lifetime from Linux /proc stat; tick and resident counters are not interchangeable. */
export interface ResidentProcess { readonly pid: number; readonly parentPid: number; readonly startTicks: string; readonly cpuTicks: string; readonly residentBytes: number }
/** Discovery errors stay visible; a vanished process is separately counted rather than assigned zero RSS. */
export interface ProcessPopulation { readonly processes: readonly ResidentProcess[]; readonly vanished: number; readonly vanishedPids: readonly number[]; readonly errors: readonly { readonly pid: number; readonly code: string }[] }

/**
 * Decode documented Linux stat fields without splitting a parenthesized command name.
 * @param record Complete /proc/PID/stat contents.
 * @param pageBytes Actual host page size captured before measurement.
 * @returns Host PID/parent/start identity, cumulative CPU ticks and sampled resident bytes.
 * @throws {Error} For malformed, missing or unsafe counters or an invalid page size.
 */
export function parseResidentProcess(record: string, pageBytes: number): ResidentProcess {
  if (!Number.isSafeInteger(pageBytes) || pageBytes < 1) throw new Error('Actual positive host page size required.');
  const opening = record.indexOf(' ('); const closing = record.lastIndexOf(')');
  if (opening < 1 || closing <= opening) throw new Error('Malformed process stat command field.');
  const pid = Number(record.slice(0, opening)); const fields = record.slice(closing + 1).trim().split(/\s+/);
  const parentPid = Number(fields[1]); const residentPages = Number(fields[21]);
  if (!Number.isSafeInteger(pid) || pid < 1 || !Number.isSafeInteger(parentPid) || parentPid < 0 || !Number.isSafeInteger(residentPages) || residentPages < 0 || ![fields[11], fields[12], fields[19]].every(value => typeof value === 'string' && /^(0|[1-9][0-9]*)$/.test(value))) throw new Error('Malformed process stat counters.');
  const residentBytes = residentPages * pageBytes;
  if (!Number.isSafeInteger(residentBytes)) throw new Error('Resident bytes exceed exact numeric range.');
  return { pid, parentPid, residentBytes, startTicks: fields[19]!, cpuTicks: String(BigInt(fields[11]!) + BigInt(fields[12]!)) };
}

/**
 * Collect host PID metadata without reading command arguments, environments or source content.
 * @param pageBytes Actual host page size.
 * @param procRoot Trusted Linux proc mount, or an owned filesystem fixture in tests.
 * @returns Readable process records, expected disappearance count and explicit read/parse errors.
 * @throws {Error} If the process population cannot be enumerated at all.
 */
export async function readResidentPopulation(pageBytes: number, procRoot = '/proc'): Promise<ProcessPopulation> {
  const names = (await readdir(procRoot, { withFileTypes: true })).filter(entry => entry.isDirectory() && /^[1-9][0-9]*$/.test(entry.name)).map(entry => entry.name);
  const processes: ResidentProcess[] = []; const errors: { pid: number; code: string }[] = []; const vanishedPids: number[] = [];
  for (let offset = 0; offset < names.length; offset += 64) {
    await Promise.all(names.slice(offset, offset + 64).map(async name => {
      try {
        const value = parseResidentProcess(await readFile(join(procRoot, name, 'stat'), 'utf8'), pageBytes);
        if (value.pid !== Number(name)) throw new Error('Process stat PID differs from its directory.');
        processes.push(value);
      } catch (error) {
        const code = (error as NodeJS.ErrnoException).code;
        if (code === 'ENOENT' || code === 'ESRCH') vanishedPids.push(Number(name));
        else errors.push({ pid: Number(name), code: code ?? 'invalid-stat' });
      }
    }));
  }
  return { processes: processes.sort((a, b) => a.pid - b.pid), vanished: vanishedPids.length, vanishedPids: vanishedPids.sort((a, b) => a - b), errors: errors.sort((a, b) => a.pid - b.pid) };
}

/** Preserve observed descendant ownership through reparenting without treating a reused PID as the old process. */
export class ResidentTree {
  private rootStart: string | null = null;
  private readonly observed = new Map<number, Set<string>>();
  /**
   * Bind the actual spawned app root, excluding the parent qualification harness.
   * @param rootPid Actual positive root PID returned by the trusted child launcher.
   * @throws {Error} For an invalid process identifier.
   */
  constructor(private readonly rootPid: number) { if (!Number.isSafeInteger(rootPid) || rootPid < 1) throw new Error('Positive spawned app PID required.'); }
  /**
   * Attribute one sampled population by host ancestry and previously observed exact lifetimes.
   * @param population Actual host records and explicit collection errors.
   * @returns Gross resident sum, attributed rows, root presence and coverage information.
   * @throws {Error} For duplicated PID rows or a resident sum outside exact numeric range.
   */
  select(population: ProcessPopulation) {
    const byPid = new Map(population.processes.map(value => [value.pid, value]));
    if (byPid.size !== population.processes.length) throw new Error('Duplicate process population row.');
    const root = byPid.get(this.rootPid);
    if (root && this.rootStart === null) this.rootStart = root.startTicks;
    const selected = new Set<number>();
    for (const row of population.processes) if (this.observed.get(row.pid)?.has(row.startTicks) || row.pid === this.rootPid && row.startTicks === this.rootStart) selected.add(row.pid);
    let progress = true;
    while (progress) {
      progress = false;
      for (const row of population.processes) if (!selected.has(row.pid) && row.pid !== this.rootPid && selected.has(row.parentPid)) { selected.add(row.pid); progress = true; }
    }
    const rows = population.processes.filter(value => selected.has(value.pid));
    for (const row of rows) { if (!this.observed.has(row.pid)) this.observed.set(row.pid, new Set()); this.observed.get(row.pid)!.add(row.startTicks); }
    const residentBytes = rows.reduce((total, value) => total + value.residentBytes, 0);
    if (!Number.isSafeInteger(residentBytes)) throw new Error('Gross resident sum exceeds exact numeric range.');
    const rootPresent = !!root && root.startTicks === this.rootStart;
    return { residentBytes, processes: rows, rootPresent, rootObserved: this.rootStart !== null,
      rootPidReused: !!root && root.startTicks !== this.rootStart,
      observedOrphans: rows.filter(row => row.pid !== this.rootPid && !selected.has(row.parentPid)).map(row => row.pid),
      ownershipComplete: population.errors.length === 0 && this.rootStart !== null,
      collectionErrors: population.errors, vanishedDuringCollection: population.vanished,
      attributedVanishedPids: population.vanishedPids.filter(pid => this.observed.has(pid)) };
  }
}
