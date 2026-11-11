// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Fixed development CLI: performance-corpus-oracle.cjs ABS_MANIFEST base|append|malformed ABS_REPORT [--size]. */
import { importProgressText } from '../src/import/progress.js';
import { writeFile } from 'node:fs/promises';
import { isAbsolute, join } from 'node:path';
import { canonicalPerformanceOracle, canonicalPerformanceSizingOracle, loadPerformanceSourceSet } from './performance-corpus.js';
import { performanceFailure } from './performance-failure.js';

async function run(): Promise<void> {
  const [manifest, variant, output, ...flags] = process.argv.slice(2); const size = flags.includes('--size');
  if (flags.includes('--cap-diagnostic')) throw new Error('Python helper cap diagnostics are retired for direct TypeScript import; no fallback is available.');
  if (!manifest || !variant || !output || !isAbsolute(output) || flags.some(flag => flag !== '--size') || new Set(flags).size !== flags.length || !['base', 'append', 'malformed'].includes(variant)) throw new Error('Usage: performance-corpus-oracle.cjs ABS_MANIFEST base|append|malformed ABS_REPORT [--size]');
  const selected = await loadPerformanceSourceSet(manifest, variant as 'base' | 'append' | 'malformed');
  const phases: { phase: number; label: string; elapsedMs: number }[] = []; const started = performance.now();
  const rejections: ReturnType<typeof performanceFailure>[] = [];
  const cancellation = new AbortController(); const diagnosticMs = 175000;
  const deadline = setTimeout(() => cancellation.abort(), diagnosticMs); let latest = 'Prepare import';
  const countdown = setInterval(() => console.error(`Oracle: ${latest}; ${Math.max(0, Math.ceil((diagnosticMs - (performance.now() - started)) / 1000))} seconds to diagnostic cancellation.`), 10000);
  try {
    const fixedRuntime = { workerFile: join(__dirname, 'import-worker.cjs') };
    const result = await (size ? canonicalPerformanceSizingOracle : canonicalPerformanceOracle)(selected, fixedRuntime, {
      signal: cancellation.signal, importProgress: value => console.error(`Import progress: ${importProgressText(value)}`), progress: (phase, label) => { latest = `phase ${phase}/6: ${label}`; phases.push({ phase, label, elapsedMs: performance.now() - started }); console.error(`Oracle ${latest}`); },
      rejected: summary => { if (rejections.length < 8) rejections.push(summary); },
    });
    await writeFile(output, JSON.stringify({ ...result, diagnosticPhases: phases }, null, 2) + '\n', { flag: 'wx', mode: 0o600 });
    console.log(JSON.stringify({ recordedAdmission: result.recordedAdmission, canonicalAdmission: result.canonicalAdmission, counts: result.counts }));
  } catch (error) {
    await writeFile(output + '.failed.json', JSON.stringify({ format: 'jai.fabric-explorer.performance-oracle-failure/1', recordedAdmission: false, canonicalAdmission: false, diagnosticCancellationMs: diagnosticMs, elapsedMs: performance.now() - started, phases, failure: error instanceof Error ? error.message : 'Oracle failed', typedFailure: performanceFailure(error), directImportRejections: rejections }, null, 2) + '\n', { flag: 'wx', mode: 0o600 });
    throw error;
  } finally { clearTimeout(deadline); clearInterval(countdown); }
}
void run().catch(error => { console.error(error instanceof Error ? error.message : 'Corpus oracle failed.'); process.exitCode = 1; });
