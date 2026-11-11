// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Manifest authority boundaries and real maintained-source import; no graph DTO substitutes for corpus admission. */
import { describe, expect, it } from 'vitest';
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';
import { mkdtemp, readFile, rm, writeFile, mkdir, symlink, lstat } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { assertPerformanceRevisions, canonicalPerformanceOracle, canonicalPerformanceSizingOracle, loadPerformanceSourceSet, performanceSourceSet } from './performance-corpus.js';
const execute = promisify(execFile);
const repository = resolve(dirname(fileURLToPath(import.meta.url)), '../../../..');
const python = join(repository, 'build/fabric-explorer/helper-venv/bin/python');
const runtime = { workerFile: join(repository, 'apps/fabric-explorer/desktop/dist/import-worker.cjs') };
function manifest(sources = [{ family: 'fabric', path: 'one.jsonl', projectRoot: '.' }]) {
  const set = { sourcePaths: sources.map(source => ({ byteLength: 0, sequence: 0, sha256: 'a'.repeat(64), head: 'b'.repeat(64), ...source })), countsExpected: { vertices: null, edges: null, findings: '1' } };
  return { format: 'jai.fabric-explorer.performance-corpus/1', sourceSets: { base: set, append: set, malformed: { ...set, countsExpected: null } } };
}
describe('performance canonical corpus oracle', () => {
  it('binds all paths to the selected immutable variant and preserves unknown counts', () => {
    const selected = performanceSourceSet('/corpus', manifest(), 'base');
    expect(selected.sources).toEqual([{ family: 'fabric', path: '/corpus/base/one.jsonl', projectPath: '/corpus/base' }]);
    expect(selected.expected).toEqual({ vertices: null, edges: null, findings: '1' });
    expect(performanceSourceSet('/corpus', manifest(), 'malformed').expected).toEqual({ vertices: null, edges: null, findings: null });
    expect(performanceSourceSet('/corpus', manifest(), 'append').sources[0]!.path).toBe('/corpus/append/one.jsonl');
  });
  it('admits exactly128 sources and rejects empty, duplicate, escaped or unsupported selections', () => {
    const sources = Array.from({ length: 128 }, (_, i) => ({ family: 'fabric', path: `${i}.jsonl`, projectRoot: '.' }));
    expect(performanceSourceSet('/corpus', manifest(sources), 'base').sources).toHaveLength(128);
    for (const value of [[], [...sources, { family: 'findings', path: 'extra', projectRoot: '.' }], [sources[0]!, sources[0]!], [{ family: 'fabric', path: '../outside', projectRoot: '.' }], [{ family: 'fabric', path: '/outside', projectRoot: '.' }], [{ family: 'fabric', path: 'one', projectRoot: '..' }], [{ family: 'enrollment', path: 'one', projectRoot: '.' }]]) {
      expect(() => performanceSourceSet('/corpus', manifest(value), 'base')).toThrow();
    }
    expect(() => performanceSourceSet('relative', manifest(), 'base')).toThrow();
    const invalid = manifest(); invalid.sourceSets.base.countsExpected.findings = '-1';
    expect(() => performanceSourceSet('/corpus', invalid, 'base')).toThrow('count');
  });
  it('reads a regular bounded manifest and rejects aliases, directories, malformed JSON and oversized input', async () => {
    const temporary = await mkdtemp(join(tmpdir(), 'jai-corpus-manifest-'));
    try {
      const file = join(temporary, 'manifest.json'); await writeFile(file, JSON.stringify(manifest()));
      expect((await loadPerformanceSourceSet(file, 'base')).sources[0]!.path).toBe(join(temporary, 'base/one.jsonl'));
      await expect(loadPerformanceSourceSet('relative/manifest.json', 'base')).rejects.toThrow('Absolute');
      await expect(loadPerformanceSourceSet(join(temporary, 'absent/manifest.json'), 'base')).rejects.toThrow();
      const directory = join(temporary, 'directory'); await mkdir(directory); await mkdir(join(directory, 'manifest.json'));
      await expect(loadPerformanceSourceSet(join(directory, 'manifest.json'), 'base')).rejects.toThrow('regular');
      const linked = join(temporary, 'linked'); await mkdir(linked); await symlink(file, join(linked, 'manifest.json'));
      await expect(loadPerformanceSourceSet(join(linked, 'manifest.json'), 'base')).rejects.toThrow('regular');
      await writeFile(file, '{'); await expect(loadPerformanceSourceSet(file, 'base')).rejects.toThrow();
      await writeFile(file, ' '.repeat(1024 * 1024 + 1)); await expect(loadPerformanceSourceSet(file, 'base')).rejects.toThrow('Bounded');
    } finally { await rm(temporary, { recursive: true, force: true }); }
  });
  it('requires exact revision metadata and matches the captured multiset independently of opaque IDs', () => {
    const selected = performanceSourceSet('/corpus', manifest(), 'base');
    const actual = selected.revisions[0]!;
    expect(() => assertPerformanceRevisions(selected, [actual])).not.toThrow();
    for (const changed of [{ digest: 'c'.repeat(64) }, { byteLength: '1' }, { head: 'd'.repeat(64) }, { sequence: '1' }, { relativePath: 'other' }, { family: 'findings' as const }]) expect(() => assertPerformanceRevisions(selected, [{ ...actual, ...changed }])).toThrow('revisions');
    expect(() => assertPerformanceRevisions(selected, [])).toThrow('revisions');
    expect(() => assertPerformanceRevisions(selected, [actual, actual])).toThrow('revisions');
    for (const field of ['byteLength', 'sha256', 'sequence', 'head'] as const) {
      const value = manifest(); delete (value.sourceSets.base.sourcePaths[0]! as Record<string, unknown>)[field];
      expect(() => performanceSourceSet('/corpus', value, 'base')).toThrow('Exact corpus');
    }
  });
  it('imports actual maintained pilot sources, verifies counts, and rejects count lies or malformed canonical input', async () => {
    const temporary = await mkdtemp(join(tmpdir(), 'jai-corpus-integration-'));
    try {
      const corpus = join(temporary, 'pilot');
      await execute(python, ['-I', '-B', join(repository, 'apps/fabric-explorer/benchmarks/corpus.py'), '--output', corpus, '--tier', 'pilot', '--bulk-records', '1', '--findings', '1', '--degree', '0'], { timeout: 30_000, maxBuffer: 1024 * 1024 });
      const file = join(corpus, 'manifest.json'); const before = await readFile(join(corpus, 'base/findings/review.jsonl'));
      const selected = await loadPerformanceSourceSet(file, 'base'); const phases: number[] = [];
      let cleanedDirectory = '';
      const result = await canonicalPerformanceOracle(selected, runtime, { progress: phase => phases.push(phase), beforeCleanup: async directory => { cleanedDirectory = directory; expect((await lstat(directory)).isDirectory()).toBe(true); } });
      await expect(lstat(cleanedDirectory)).rejects.toMatchObject({ code: 'ENOENT' });
      expect(result.recordedAdmission).toBe(true); expect(result.canonicalAdmission).toBe(false); expect(result.counts.findings).toBe('1'); expect(BigInt(result.counts.vertices)).toBeGreaterThan(1n); expect(result.report.acceptedSources).toBe('3');
      expect(phases.filter((phase, index) => index === 0 || phase !== phases[index - 1])).toEqual([1, 2, 3, 4, 5, 6]);
      const sizing = await canonicalPerformanceSizingOracle(selected, runtime);
      expect(sizing.counts).toEqual(result.counts); expect(sizing.compactGraphBytes).toBeGreaterThan(0);
      expect(sizing.compactUsage.compactGraphBytes).toBe(sizing.compactGraphBytes);
      expect(sizing.compactUsage.semanticFactBytes).toBe(sizing.semanticFactBytes);
      expect(sizing.compactGraphBytes).toBeLessThan(sizing.expandedDtoJsonBytes);
      expect(sizing.topology.multipleVersionGroups).toBeGreaterThanOrEqual(0); expect(sizing.topology.causalOnlyCycle).toBeNull();
      expect(sizing.semanticFactBytes).toBeGreaterThan(0); expect(sizing.byKind.edge?.count).toBe(Number(result.counts.edges));
      expect(Object.values(sizing.byKind).reduce((total, item) => total + item.bytes, 0)).toBe(sizing.expandedDtoJsonBytes);
      expect(sizing.edgeTemplates.reduce((total, item) => total + item.count, 0)).toBe(Number(result.counts.edges));
      expect(sizing.edgeTemplates.reduce((total, item) => total + item.bytes, 0)).toBe(sizing.byKind.edge?.bytes);
      expect(sizing.edgeTemplates.every(item => item.minimum > 0 && item.maximum >= item.minimum && item.bytes >= item.minimum * item.count)).toBe(true);
      await expect(canonicalPerformanceOracle({ ...selected, revisions: selected.revisions.map(source => ({ ...source, digest: '0'.repeat(64) })) }, runtime)).rejects.toThrow('revisions');
      await expect(canonicalPerformanceOracle({ ...selected, expected: { ...selected.expected, vertices: '0' } }, runtime)).rejects.toThrow('differs');
      await expect(canonicalPerformanceSizingOracle({ ...selected, expected: { ...selected.expected, vertices: '0' } }, runtime)).rejects.toThrow('expectation');
      await expect(canonicalPerformanceOracle(await loadPerformanceSourceSet(file, 'malformed'), runtime)).rejects.toThrow();
      await expect(canonicalPerformanceSizingOracle(await loadPerformanceSourceSet(file, 'malformed'), runtime)).rejects.toThrow();
      await expect(canonicalPerformanceOracle(selected, { ...runtime, workerFile: 'relative' })).rejects.toThrow('absolute');
      const cancellation = new AbortController(); cancellation.abort();
      await expect(canonicalPerformanceOracle(selected, runtime, { signal: cancellation.signal })).rejects.toThrow();
      expect(await readFile(join(corpus, 'base/findings/review.jsonl'))).toEqual(before);
    } finally { await rm(temporary, { recursive: true, force: true }); }
  }, 30_000);
});
