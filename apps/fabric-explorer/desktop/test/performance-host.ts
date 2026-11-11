// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** External Linux observer: performance-host.cjs ABS_ELECTRON ABS_INPUT ABS_NEW_OUTPUT smoke|qualification|endurance|all. */
import assert from 'node:assert/strict';
import { spawn, execFileSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { createReadStream, createWriteStream, readFileSync } from 'node:fs';
import { access, mkdir, open, readFile, readdir, realpath, statfs, writeFile } from 'node:fs/promises';
import { cpus, freemem, release, totalmem, type, version } from 'node:os';
import { isAbsolute, join } from 'node:path';
import { createInterface } from 'node:readline';
import { loadPerformanceSourceSet } from './performance-corpus.js';
import type { PerformanceSourceSet } from './performance-corpus.js';
import { assessMeasurements, MEMORY_BUDGET_BYTES, UI_TASK_BUDGET_MS, UI_TASK_TARGET_MS } from './performance-metrics.js';
import { assessShellReadiness, coldImportCohort, nextPerformanceCaseAllowed, performanceCases } from './performance-plan.js';
import type { NativePerformanceInput, PerformanceCase, PerformanceMode, PerformanceTier } from './performance-plan.js';
import { readResidentPopulation, ResidentTree } from './performance-process.js';
import { assessResidentWindow } from './performance-resident-window.js';
import type { ResidentSample } from './performance-resident-window.js';
import { performanceEvent, performanceProcessExit, performanceSourceSnapshot, settledCloseRetention } from './performance-host-support.js';
import { PERFORMANCE_DRAIN_MS, performanceDrainComplete, performanceDrainWitness } from './performance-drain.js';
import type { PerformanceDrainWitness } from './performance-drain.js';
import type { PerformanceEvent, PerformanceSourceEntry } from './performance-host-support.js';
import { rendererCpuProfileEnabled } from './renderer-cpu-profile.js';

interface HostInput { readonly format: 'jai.fabric-explorer.performance-host-input/1'; readonly corpora: Partial<Record<PerformanceTier, string>>; readonly rendererCpuProfile?: true }
interface CaseResult { readonly id: string; readonly kind: string; readonly tier: PerformanceTier | null; readonly status: 'collected' | 'failed' | 'interrupted' | 'blocked'; readonly value: unknown }
const [electronArgument, inputArgument, outputArgument, modeArgument] = process.argv.slice(2);
assert(electronArgument && inputArgument && outputArgument && modeArgument && [electronArgument, inputArgument, outputArgument].every(isAbsolute), 'Absolute Electron, input and new evidence paths plus explicit mode required.');
assert.equal(process.platform, 'linux', 'This sampler qualifies only actual Linux observations.');
assert(!process.env.ELECTRON_RUN_AS_NODE && !process.env.NODE_OPTIONS, 'Qualification requires ordinary pinned runtimes without inherited Node startup hooks.');
const electron = electronArgument; const output = outputArgument; const mode = modeArgument as PerformanceMode;
const hostInputPath = inputArgument;
const hostInputBytes = readFileSync(hostInputPath); const consumedHostInputSha256 = createHash('sha256').update(hostInputBytes).digest('hex');
const plan = performanceCases(mode); const input = JSON.parse(hostInputBytes.toString('utf8')) as HostInput;
assert.equal(input.format, 'jai.fabric-explorer.performance-host-input/1'); assert(input.corpora && typeof input.corpora === 'object');
const rendererProfileDiagnostic = rendererCpuProfileEnabled(mode, input.rendererCpuProfile);
const pageBytes = Number(execFileSync('getconf', ['PAGESIZE'], { encoding: 'utf8' }).trim());
const clockTicks = Number(execFileSync('getconf', ['CLK_TCK'], { encoding: 'utf8' }).trim());
assert(Number.isSafeInteger(pageBytes) && pageBytes > 0 && Number.isSafeInteger(clockTicks) && clockTicks > 0);
const counts = { S: ['1000', '3000', '100'], M: ['25000', '100000', '5000'], L: ['100000', '500000', '20000'] } as const;
const inputBytes = { S: 10 * 1024 * 1024, M: 250 * 1024 * 1024, L: 1024 * 1024 * 1024 } as const;
const corpora = new Map<PerformanceTier, { manifest: string; selected: PerformanceSourceSet; before: readonly PerformanceSourceEntry[] }>();
const cases: CaseResult[] = []; const blocked = new Set<PerformanceTier>();
const coldSkipped = new Set<PerformanceTier>();
let stopped = false; let operatorStop = false; let active: ReturnType<typeof spawn> | null = null; let stoppedReason: string | null = null;
let activeCase: { id: string; ordinal: number; rootPid: number | null; phase: 'running' | 'draining' | 'evaluating'; latestSample: ResidentSample | null } | null = null;
let observerPeakBytes = 0; let totalSamplingCpuMicros = 0; let totalSamplingWallMs = 0; let metadata: unknown = null; let provenance: unknown = null; let integrity: unknown = null;
let phaseDeadline: ReturnType<typeof setTimeout> | null = null;
const startNs = process.hrtime.bigint();
const now = () => Number(process.hrtime.bigint() - startNs) / 1000000;
const delay = async (milliseconds: number): Promise<void> => await new Promise(resolve => setTimeout(resolve, milliseconds));
function stop(reason: string, byOperator = false): void {
  stopped = true; operatorStop ||= byOperator; stoppedReason = reason; const child = active;
  if (child && child.exitCode === null && child.pid) {
    try { process.kill(-child.pid, 'SIGTERM'); } catch { child.kill('SIGTERM'); }
    const hardStop = setTimeout(() => { if (child.exitCode === null && child.pid) { try { process.kill(-child.pid, 'SIGKILL'); } catch { child.kill('SIGKILL'); } } }, 2000); hardStop.unref();
  }
  if (byOperator) { void save().catch(() => {}); const forceStop = setTimeout(() => process.exit(130), 2500); forceStop.unref(); }
}
process.once('SIGINT', () => stop('Ctrl+C', true)); process.once('SIGTERM', () => stop('SIGTERM', true));
async function save(): Promise<void> {
  await writeFile(join(output, 'observations.json'), JSON.stringify({ format: 'jai.fabric-explorer.performance-host/1', mode, plannedCases: plan.length, observedCases: cases.length, cases, activeCase, stopped, stoppedReason, metadata, provenance, integrity,
    purpose: rendererProfileDiagnostic ? 'renderer-cpu-diagnostic-only-not-timing-or-RSS-qualification' : 'performance-observations',
    thresholds: { uiTaskMaximumMs: UI_TASK_BUDGET_MS, uiTaskOptimizationTargetMs: UI_TASK_TARGET_MS, grossMemoryBytes: MEMORY_BUDGET_BYTES },
    coldImportCohorts: (['M', 'L'] as const).map(tier => coldImportCohort(tier, cases.filter(row => row.kind === 'import' && row.tier === tier).map(row => ({ status: row.status, durationMs: (row.value as { importMs?: number | null }).importMs ?? null })))), observedThresholdFailures: thresholdFailures(),
    observer: { platform: process.platform, pageBytes, clockTicks, configuredSamplingIntervalMs: 50, maximumAllowedGapMs: 100, peakSampledObserverRssBytes: observerPeakBytes, samplingCpuMicroseconds: totalSamplingCpuMicros, samplingWallMs: totalSamplingWallMs, processOutsideMeasuredTree: true },
    qualification: { developmentShell: 'compiled-development-composition-with-owner-adopted-3.5-second-budget', packagedShell: 'required-after-packaging-before-release', minimumReferenceHost: 'not-enrolled', windowsAndMacOS: 'deferred-by-user', mainUiTaskCoverage: 'partial-polling-delay-is-not-task-duration', productionRepresentativeness: 'unknown', elapsedMs: now() } }, null, 2) + '\n', { mode: 0o600 });
}
function thresholdFailures(): { caseId: string; metric: string }[] {
  if (rendererProfileDiagnostic) return [];
  const failures: { caseId: string; metric: string }[] = [];
  for (const row of cases) {
    const value = row.value as { assessments?: Record<string, unknown>; native?: { animation?: { assessment?: { status: string } }; rendererTasks?: { maximumMs?: number }; observations?: { title: string; value: { assessment?: { status: string } } }[] }; retention?: { assessment?: { status: string } } };
    for (const [metric, assessment] of Object.entries(value.assessments ?? {})) if (assessment === 'fail' || assessment && typeof assessment === 'object' && (assessment as { status?: string }).status === 'fail') failures.push({ caseId: row.id, metric });
    if (value.native?.animation?.assessment?.status === 'fail') failures.push({ caseId: row.id, metric: 'active-frame-p95' });
    if ((value.native?.rendererTasks?.maximumMs ?? 0) > UI_TASK_BUDGET_MS) failures.push({ caseId: row.id, metric: 'renderer-UI-task-maximum' });
    for (const observation of value.native?.observations ?? []) if (observation.value?.assessment?.status === 'fail') failures.push({ caseId: row.id, metric: observation.title });
    if (value.retention?.assessment?.status === 'fail') failures.push({ caseId: row.id, metric: 'close-retention' });
  }
  return failures;
}
function phaseLimit(label: string): void {
  if (phaseDeadline) clearTimeout(phaseDeadline);
  phaseDeadline = setTimeout(() => { stop(`Vypršel 180sekundový limit fáze ${label}.`); void save().catch(() => {}).finally(() => process.exit(2)); const force = setTimeout(() => process.exit(2), 2000); force.unref(); }, 180000);
}
async function digest(path: string): Promise<{ path: string; actualPath: string; sha256: string }> {
  const actualPath = await realpath(path); const hash = createHash('sha256');
  for await (const chunk of createReadStream(actualPath, { highWaterMark: 65536 })) hash.update(chunk);
  return { path, actualPath, sha256: hash.digest('hex') };
}
async function hostMetadata(): Promise<unknown> {
  const power: unknown[] = [];
  try {
    for (const name of await readdir('/sys/class/power_supply')) {
      const path = join('/sys/class/power_supply', name); const supplyType = (await readFile(join(path, 'type'), 'utf8')).trim();
      if (['Mains', 'USB', 'USB_C'].includes(supplyType)) power.push({ name, type: supplyType, online: (await readFile(join(path, 'online'), 'utf8')).trim() });
    }
  } catch { /* Unavailable host metadata stays unknown rather than assuming AC power. */ }
  const filesystem = await statfs(output);
  return { os: { type: type(), release: release(), version: version(), architecture: process.arch }, cpus: cpus().map(cpu => ({ model: cpu.model, reportedMhz: cpu.speed })), totalMemoryBytes: totalmem(), availableMemoryBytesAtSetup: freemem(),
    storage: { evidenceFileSystemType: filesystem.type, blockSize: filesystem.bsize, backingDeviceModel: 'not-observed' }, power: power.length ? power : 'not-observed',
    session: { x11DisplayPresent: !!process.env.DISPLAY, waylandDisplayPresent: !!process.env.WAYLAND_DISPLAY, xdgSessionType: process.env.XDG_SESSION_TYPE ?? null },
    cacheCondition: 'OS caches may be warm; exact integrity hashing is performed before the population. No privileged cache flush.', referenceHostEnrolled: false };
}
async function runCase(definition: PerformanceCase, ordinal: number): Promise<CaseResult> {
  const directory = join(output, `${String(ordinal).padStart(2, '0')}-${definition.id}`); await mkdir(directory, { mode: 0o700 });
  const corpus = definition.tier ? corpora.get(definition.tier)! : null;
  const caseInput: NativePerformanceInput = { format: 'jai.fabric-explorer.performance-case/1', definition, ordinal, total: plan.length, manifest: corpus?.manifest ?? null, ...(rendererProfileDiagnostic ? { mode: 'smoke' as const, rendererCpuProfile: true as const } : {}) };
  const casePath = join(directory, 'case-input.json'); await writeFile(casePath, JSON.stringify(caseInput, null, 2) + '\n', { mode: 0o600 });
  const cache = join(directory, 'application/JAI Fabric Explorer/cache'); await mkdir(cache, { recursive: true, mode: 0o700 });
  console.log(`Případ ${ordinal}/${plan.length}: ${definition.id}. Pevný diagnostický limit ${definition.watchdogMs / 1000} sekund; žádné opakování.`);
  const launchedNs = process.hrtime.bigint(); const relativeNow = () => Number(process.hrtime.bigint() - launchedNs) / 1000000;
  const observerCpuStart = process.cpuUsage();
  const child = spawn(electron, [join(__dirname, 'performance-native.cjs'), casePath, directory], { stdio: ['ignore', 'pipe', 'pipe'], detached: true, env: { ...process.env, MESA_SHADER_CACHE_DISABLE: 'true', XDG_CACHE_HOME: cache, GSETTINGS_BACKEND: 'memory' } }); active = child;
  activeCase = { id: definition.id, ordinal, rootPid: child.pid ?? null, phase: 'running', latestSample: null };
  const completion = performanceProcessExit({ exit: callback => { child.once('exit', callback); }, error: callback => { child.once('error', callback); }, closed: callback => { child.once('close', callback); } });
  const events: PerformanceEvent[] = []; const log = createWriteStream(join(directory, 'native.log'), { mode: 0o600 });
  let protocolError: string | null = null; let nativeCollectedMs: number | null = null; let enduranceDeadline: ReturnType<typeof setTimeout> | null = null;
  let timedOut = false; let emergencyExit: ReturnType<typeof setTimeout> | null = null;
  const timeoutCase = (reason: string) => { timedOut = true; process.exitCode = 2; stop(reason); void save().catch(() => {}); emergencyExit = setTimeout(() => process.exit(2), 2000); };
  let lines: ReturnType<typeof createInterface> | null = null;
  if (child.stdout) {
    lines = createInterface({ input: child.stdout });
    lines.on('line', line => {
      log.write(line + '\n'); console.log(line);
      try {
        const event = performanceEvent(line);
        if (event) {
          if (BigInt(event.monotonicNs) < launchedNs || events.length && BigInt(event.monotonicNs) < BigInt(events.at(-1)!.monotonicNs)) throw new Error('Native clock sequence differs from host monotonic time.');
          events.push(event); if (event.name === 'collected') nativeCollectedMs = Number(BigInt(event.monotonicNs) - launchedNs) / 1000000;
          if (event.name === 'endurance-started') enduranceDeadline = setTimeout(() => timeoutCase('Vypršel pevný 1950sekundový limit měřicí části výdrže.'), Math.max(0, 1950000 - (relativeNow() - Number(BigInt(event.monotonicNs) - launchedNs) / 1000000)));
          if (event.name === 'stopped') stop('Native stop control', (event.value as { code?: number }).code === 130);
        }
      } catch (error) { protocolError = error instanceof Error ? error.message : 'Invalid native event'; stop('Invalid native evidence protocol'); }
    });
  }
  child.stderr?.on('data', chunk => { log.write(chunk); process.stderr.write(chunk); });
  log.on('error', error => { protocolError = error.message; stop('Evidence log unavailable'); });
  const watchdog = setTimeout(() => timeoutCase(`Diagnostický limit případu ${definition.id}`), definition.watchdogMs);
  const samples: ResidentSample[] = []; const raw = await open(join(directory, 'resident-samples.jsonl'), 'wx', 0o600);
  let sampling = true; let samplerError: string | null = null;
  let rootExitObservedMs: number | null = null; let terminalDrain: PerformanceDrainWitness | null = null;
  const tree = child.pid ? new ResidentTree(child.pid) : null;
  const sampler = (async () => {
    if (!tree) return;
    while (sampling) {
      const startedMs = relativeNow(); const cpu = process.cpuUsage(); const wallStart = process.hrtime.bigint();
      try {
        const population = await readResidentPopulation(pageBytes); const selected = tree.select(population); const endedMs = relativeNow();
        const sample = { startedMs, endedMs, selected }; samples.push(sample); if (activeCase) activeCase.latestSample = sample;
        const self = population.processes.find(row => row.pid === process.pid); if (self) observerPeakBytes = Math.max(observerPeakBytes, self.residentBytes);
        await raw.write(JSON.stringify(sample) + '\n');
        // Only this serialized sampler can accept its successfully appended terminal row.
        if (rootExitObservedMs !== null) {
          terminalDrain = performanceDrainWitness(terminalDrain, sample, { rootExitObservedMs, checkedMs: relativeNow(), stdioClosed: completion.stdioClosed(), samplerError });
          if (terminalDrain) sampling = false;
        }
      } catch (error) { samplerError = error instanceof Error ? error.message : 'Host sampler failed'; stop('RSS observer failed'); }
      const consumed = process.cpuUsage(cpu); totalSamplingCpuMicros += consumed.user + consumed.system; totalSamplingWallMs += Number(process.hrtime.bigint() - wallStart) / 1000000;
      if (!sampling || samplerError) break;
      await delay(Math.max(0, 50 - (relativeNow() - startedMs)));
    }
  })();
  const outcome = await completion.exited; const launchError = outcome.launchError; rootExitObservedMs = relativeNow(); active = null; if (activeCase) activeCase.phase = 'draining';
  // Collection continues through native shutdown. Previously observed orphan lifetimes remain attributed.
  const drainDeadlineMs = rootExitObservedMs + PERFORMANCE_DRAIN_MS;
  while (!terminalDrain && !samplerError && relativeNow() < drainDeadlineMs) {
    await delay(Math.min(50, Math.max(0, drainDeadlineMs - relativeNow())));
  }
  sampling = false; await sampler; await raw.close();
  lines?.removeAllListeners('line'); lines?.close(); child.stdout?.destroy(); child.stderr?.removeAllListeners('data'); child.stderr?.destroy();
  await new Promise<void>(resolve => log.end(resolve));
  if (activeCase) activeCase.phase = 'evaluating';
  let native: Record<string, unknown> | null = null;
  try { native = JSON.parse(await readFile(join(directory, 'native-observations.json'), 'utf8')) as Record<string, unknown>; } catch { /* Missing native evidence is an explicit incomplete case. */ }
  const rootObserved = samples.filter(row => row.selected.rootPresent);
  const activeEndMs = nativeCollectedMs ?? rootObserved.at(-1)?.endedMs ?? relativeNow();
  const activeSamples = samples.filter(row => row.endedMs <= activeEndMs);
  const memoryBudgetApplies = definition.tier === 'M' || definition.tier === 'L';
  const budgetBytes = definition.tier === 'L' ? MEMORY_BUDGET_BYTES.L : MEMORY_BUDGET_BYTES.M;
  const memory = memoryBudgetApplies && activeEndMs > 0 ? assessResidentWindow(activeSamples, { startedMs: 0, endedMs: activeEndMs, budgetBytes, maximumGapMs: 100 }) : null;
  const allPeakBytes = samples.length ? samples.reduce((peak, row) => Math.max(peak, row.selected.residentBytes), 0) : null;
  // Incomplete drains retain the actual latest row; a pass uses only its accepted terminal witness.
  const acceptedDrain = terminalDrain as PerformanceDrainWitness | null;
  const evidence = acceptedDrain?.sample ?? samples.at(-1); const last = evidence?.selected;
  const drain = { rootExitObservedMs, observedUntilMs: samples.at(-1)?.endedMs ?? null, remaining: last?.processes.map(row => ({ pid: row.pid, startTicks: row.startTicks })) ?? [], collectionErrors: last?.collectionErrors ?? [], rootObserved: last?.rootObserved ?? false, stdioClosed: completion.stdioClosed(),
    terminalWitness: acceptedDrain ? { startedMs: acceptedDrain.sample.startedMs, endedMs: acceptedDrain.sample.endedMs, checkedMs: acceptedDrain.checkedMs } : null,
    complete: !!acceptedDrain && performanceDrainComplete(acceptedDrain.sample, { rootExitObservedMs, checkedMs: acceptedDrain.checkedMs, stdioClosed: completion.stdioClosed(), samplerError }) };
  const clocks = (name: string) => events.filter(event => event.name === name).map(event => ({ event, milliseconds: Number(BigInt(event.monotonicNs) - launchedNs) / 1000000 }));
  const settledStarts = clocks('settle-start'); const settledEnds = clocks('settle-end');
  const windows = settledEnds.flatMap(end => {
    const value = end.event.value as { cycle: number | null }; if (value.cycle === null) return [];
    const start = settledStarts.find(row => (row.event.value as { cycle: number | null }).cycle === value.cycle);
    return start ? [{ cycle: value.cycle, startedMs: start.milliseconds, endedMs: end.milliseconds }] : [];
  });
  const retention = definition.kind === 'retention' ? settledCloseRetention(samples, windows) : null;
  const shellMs = clocks('shell-ready')[0]?.milliseconds ?? null;
  const importMs = typeof native?.importMs === 'number' ? native.importMs : null;
  const assessments = {
    developmentShell: definition.kind === 'shell' && shellMs !== null ? assessShellReadiness([shellMs], 1) : null,
    importedOverview: definition.kind === 'import' && importMs !== null && definition.tier !== 'S' ? assessMeasurements([importMs], 1, definition.tier === 'L' ? 45000 : 10000, 'maximum') : null,
    grossMemory: memory,
    shutdownPeak: memoryBudgetApplies ? allPeakBytes !== null && allPeakBytes > budgetBytes ? 'fail' : drain.complete ? 'observed-no-over-budget-sample' : 'partial' : 'descriptive-no-S-or-baseline-budget-adopted',
  };
  const caseStopped = stopped || outcome.code === 130 || outcome.signal === 'SIGINT' || outcome.signal === 'SIGTERM';
  if (!native && outcome.code === 0) stop('Window closed before completing native evidence');
  const status = caseStopped && operatorStop ? 'interrupted' : timedOut || launchError || protocolError || samplerError || !drain.complete ? 'failed' : caseStopped ? 'interrupted' : outcome.code !== 0 || native?.status !== 'collected' ? 'failed' : 'collected';
  clearTimeout(watchdog); if (emergencyExit) clearTimeout(emergencyExit); if (enduranceDeadline) clearTimeout(enduranceDeadline); activeCase = null;
  return { id: definition.id, kind: definition.kind, tier: definition.tier, status, value: { outcome, launchError, protocolError, samplerError, timedOut, native, events, shellMs, importMs, assessments: rendererProfileDiagnostic ? null : assessments, diagnosticObservedAssessments: rendererProfileDiagnostic ? assessments : null, measurementPurpose: rendererProfileDiagnostic ? 'diagnostic-only' : 'performance-observation', memory, allPeakBytes, drain, retention,
    observerCpuDuringCase: process.cpuUsage(observerCpuStart), observerCaseWallMs: relativeNow(),
    measurementBoundary: { launchedNs: String(launchedNs), activeEndMs, samples: samples.length, activeSamples: activeSamples.length },
    method: 'Gross sum of observed Linux process RSS; shared pages are conservatively counted in every process. A child born and exited wholly between samples is unobserved. Probe runs outside the measured tree; its own sampled RSS and CPU cost are reported.' } };
}
async function run(): Promise<void> {
  await access(electron); await access(join(__dirname, 'performance-native.cjs')); await mkdir(output, { mode: 0o700 });
  phaseLimit('přípravy');
  console.log(`Konečný běh: ${plan.length} případů. Součet pevných limitů nejvýše ${Math.ceil(plan.reduce((total, row) => total + row.watchdogMs + 2000, 0) / 60 / 1000)} minut, plus úvodní a závěrečné ověření dat.`);
  console.log('Žádné ruční hodnocení ani opakování. Zastavení: tlačítko v aplikaci, Escape, zavření testovacího okna nebo Ctrl+C.');
  if (rendererProfileDiagnostic) console.log('Pouze diagnostika CPU rendereru v jednom případu S. Časy a RSS tohoto běhu nejsou kvalifikační měření; výkonové limity se nevyhodnocují.');
  console.log(`Adresář výsledků: ${output}`);
  console.log('Úvodní a závěrečné porovnání dat má samostatně pevný limit 180 sekund.');
  console.log('Výdrž má samostatnou přípravu nejvýše 150 sekund a jedinou měřicí část: 1800 sekund aktivity, nejvýše 120 sekund dokončení práce a 30 sekund ukončení.');
  console.log('Fáze 1/3: přesné vstupy, sestavení a prostředí; mimo měřenou dobu.');
  const required = [...new Set(plan.flatMap(row => row.tier ? [row.tier] : []))];
  for (const tier of required) {
    const manifest = input.corpora[tier]; assert(manifest && isAbsolute(manifest), `Prepared ${tier} corpus required.`);
    const selected = await loadPerformanceSourceSet(manifest, 'base');
    assert.deepEqual([selected.expected.vertices, selected.expected.edges, selected.expected.findings], counts[tier], `Frozen ${tier} counts must not be substituted.`);
    const declared = JSON.parse(await readFile(manifest, 'utf8'));
    assert.equal(declared.sourceSets.base.byteDimensions.totalReferencedInputBytes, inputBytes[tier], `Frozen ${tier} input dimension required.`);
    corpora.set(tier, { manifest, selected, before: await performanceSourceSnapshot(selected) });
  }
  const artifacts = ['main.cjs', 'preload.cjs', 'import-worker.cjs', 'performance-native.cjs', 'performance-host.cjs', 'renderer/index.html', 'renderer/renderer.js', 'renderer/renderer.css'].map(path => join(__dirname, path));
  const hashes = [];
  const importerDirectory = join(__dirname, '../src/import');
  const importerSources = (await readdir(importerDirectory)).filter(name => name.endsWith('.ts')).sort().map(name => join(importerDirectory, name));
  for (const path of [...artifacts, hostInputPath, process.execPath, electron, ...importerSources, ...[...corpora.values()].map(row => row.manifest)]) { const hashed = await digest(path); if (path === hostInputPath) assert.equal(hashed.sha256, consumedHostInputSha256, 'Trusted host input changed before measurement freeze.'); hashes.push(hashed); }
  metadata = await hostMetadata(); provenance = { hashes, consumedHostInputSha256, preparedCorpora: [...corpora].map(([tier, row]) => ({ tier, manifest: row.manifest, before: row.before })), scope: 'Explicit prepared sources and immutable compiled development composition; source hashes are private evidence.' }; await save();
  clearTimeout(phaseDeadline!); phaseDeadline = null;
  console.log('Fáze 2/3: jednotlivé očíslované případy; paměť aplikace se měří bez odečítání režie Chromia.');
  for (const [index, definition] of plan.entries()) {
    if (stopped || definition.tier && (blocked.has(definition.tier) || definition.kind === 'import' && coldSkipped.has(definition.tier))) {
      console.log(`Případ ${index + 1}/${plan.length}: ${definition.id} se nespouští; předchozí výsledek již určil nesplněný limit nebo chybějící podmínku.`);
      cases.push({ id: definition.id, kind: definition.kind, tier: definition.tier, status: 'blocked', value: { reason: stoppedReason ?? (definition.tier && coldSkipped.has(definition.tier) ? 'Cold cohort each-run budget already failed; remaining repetitions are explicitly unexecuted.' : 'Actual corpus import failed in an earlier independent case.') } }); continue;
    }
    const result = await runCase(definition, index + 1); cases.push(result);
    if (!nextPerformanceCaseAllowed((result.value as { drain: { complete: boolean } }).drain.complete)) { console.error('Uvolnění sledovaných procesů není doložené. Další případy se nespustí; přesné PID a jejich začátky jsou uložené ve výsledcích.'); stop('Observed owned descendant drain is incomplete; no further cases may start.'); }
    if (result.status === 'failed' && definition.tier && definition.kind === 'import') blocked.add(definition.tier);
    if (definition.kind === 'import' && (definition.tier === 'M' || definition.tier === 'L')) {
      const assessment = coldImportCohort(definition.tier, [{ status: result.status, durationMs: (result.value as { importMs: number | null }).importMs }]);
      if (assessment.skipRemainingColdImports) coldSkipped.add(definition.tier);
      if (assessment.blockDependentCases) blocked.add(definition.tier);
    }
    await save();
  }
  console.log('Fáze 3/3: porovnání původních bajtů, identit a položek adresářů; mimo měřenou dobu.');
  phaseLimit('závěrečného porovnání');
  const integrityRows = [];
  for (const [tier, corpus] of corpora) { const after = await performanceSourceSnapshot(corpus.selected); const unchanged = JSON.stringify(after) === JSON.stringify(corpus.before); integrityRows.push({ tier, unchanged, after }); }
  const afterHashes = []; for (const prior of hashes) afterHashes.push(await digest(prior.path));
  const artifactsUnchanged = JSON.stringify(afterHashes) === JSON.stringify(hashes);
  integrity = { sources: integrityRows, artifactsUnchanged, afterHashes }; await save(); clearTimeout(phaseDeadline!); phaseDeadline = null;
  const failed = cases.some(row => row.status === 'failed') || integrityRows.some(row => !row.unchanged) || !artifactsUnchanged || thresholdFailures().length > 0;
  console.log(`Uloženo ${cases.filter(row => row.status === 'collected').length}/${plan.length} úplných pozorování. Nezávislé vyhodnocení výkonu a otevřených podmínek je samostatný krok.`);
  process.exitCode = operatorStop ? 130 : failed || stopped ? 1 : mode === 'smoke' ? 0 : 2;
}
void run().catch(async error => { if (phaseDeadline) clearTimeout(phaseDeadline); stoppedReason = error instanceof Error ? error.message : 'Unknown host observation failure'; stop(stoppedReason); try { await save(); } catch { /* Keep the original diagnostic when evidence setup itself failed. */ } console.error(`Pozorování se nepodařilo dokončit: ${stoppedReason}`); process.exitCode = 1; });
