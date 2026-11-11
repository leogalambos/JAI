// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Development-only direct recorded-source admission oracle; projection DTOs are never substituted for input. */
import { lstat, readFile, mkdtemp, rm } from 'node:fs/promises';
import { basename, dirname, isAbsolute, join, resolve } from 'node:path';
import { tmpdir } from 'node:os';
import type { Counts, SourceFamily, SourceRevision } from '@jai/fabric-explorer-contracts';
import { ReadBroker } from '../src/broker/read-broker.js';
import { CaptureArchiveStore } from '../src/broker/capture-archive.js';
import { ImportSession } from '../src/import/session.js';
import { NativeImportWorker } from '../src/import/worker-client.js';
import { buildDirectModel, draftDirectRevision } from '../src/import/direct-import.js';
import { DEFAULT_IMPORT_LIMITS } from '../src/import/types.js';
import { initializeApplicationPaths } from '../src/shell/paths.js';
import { PersistentNamespaceRegistry } from '../src/shell/preferences.js';
import { observedTopology } from './performance-topology.js';
import { performanceFailure } from './performance-failure.js';

/** One immutable prepared variant; paths are relative to its base/append/malformed directory. */
export interface PerformanceSourceSet {
  readonly sources: readonly { readonly family: SourceFamily; readonly path: string; readonly projectPath: string }[];
  readonly expected: { readonly vertices: string | null; readonly edges: string | null; readonly findings: string | null };
  readonly revisions: readonly Pick<SourceRevision, 'family' | 'relativePath' | 'byteLength' | 'digest' | 'head' | 'sequence'>[];
}
/** Trusted fixed development worker; selected input cannot choose executable code. */
export interface PerformanceRuntime { readonly workerFile: string }
/** Development observation only; cancellation uses the production import signal. */
export interface PerformanceOracleControl {
  readonly importProgress?: (value: import('../src/import/progress.js').ImportProgress) => void;
  readonly signal?: AbortSignal; readonly progress?: (phase: number, label: string) => void;
  /** Private observer of typed direct-import rejection before import-facing category mapping. */
  readonly rejected?: (summary: ReturnType<typeof performanceFailure>) => void;
  /** Trusted development collector after worker disposal, before owned scratch removal. */
  readonly beforeCleanup?: (scratchDirectory: string) => Promise<void>;
}

function childPath(root: string, value: unknown, directory: boolean): string {
  if (typeof value !== 'string' || (!directory && value === '.') || !value || isAbsolute(value) || value.includes('\\') || value.split('/').some(part => part === '..' || part === '')) throw new Error('Corpus path must be an explicit relative child.');
  return resolve(root, value);
}

async function oracleBroker(runtime: PerformanceRuntime) {
  if (!isAbsolute(runtime.workerFile)) throw new Error('Fixed absolute oracle runtime required.');
  const scratch = await mkdtemp(join(tmpdir(), 'jai-performance-oracle-'));
  const paths = initializeApplicationPaths({ appData: () => scratch, setPath: () => {}, setLogsPath: () => {}, setCachePath: () => {}, setTemporaryEnvironment: () => {} });
  return { scratch, archiveDirectory: join(paths.temp, 'captures'), broker: new ReadBroker({ writeRoots: [scratch], registry: new PersistentNamespaceRegistry(paths) }) };
}

/**
 * Decode the fixed synthetic manifest's selected variant without opening source bytes.
 * @param root Absolute corpus directory containing variant directories.
 * @param manifest Parsed generator manifest; only its selected source/count fields are consumed.
 * @param variant Prepared immutable input variant.
 * @returns Explicit absolute admission paths and nullable count expectations.
 * @throws {Error} For unsupported shape, path escape, family, count or selection size.
 */
export function performanceSourceSet(root: string, manifest: unknown, variant: 'base' | 'append' | 'malformed'): PerformanceSourceSet {
  if (!isAbsolute(root) || !manifest || typeof manifest !== 'object' || Array.isArray(manifest)) throw new Error('Absolute corpus root and generator manifest required.');
  const value = manifest as Record<string, unknown>;
  if (value.format !== 'jai.fabric-explorer.performance-corpus/1' || !['base', 'append', 'malformed'].includes(variant)) throw new Error('Unsupported performance corpus manifest.');
  const selected = (value.sourceSets as Record<string, unknown> | undefined)?.[variant] as Record<string, unknown> | undefined;
  if (!selected || !Array.isArray(selected.sourcePaths) || selected.sourcePaths.length < 1 || selected.sourcePaths.length > 128) throw new Error('Corpus requires one to 128 explicit sources.');
  const base = join(root, variant);
  const revisions: PerformanceSourceSet['revisions'][number][] = [];
  const sources = selected.sourcePaths.map(input => {
    if (!input || typeof input !== 'object' || Array.isArray(input)) throw new Error('Invalid source selection.');
    const row = input as Record<string, unknown>;
    if (!['fabric', 'findings'].includes(String(row.family))) throw new Error('Unsupported performance source family.');
    if (!Number.isSafeInteger(row.byteLength) || (row.byteLength as number) < 0 || !Number.isSafeInteger(row.sequence) || (row.sequence as number) < 0 || typeof row.sha256 !== 'string' || !/^[0-9a-f]{64}$/.test(row.sha256) || typeof row.head !== 'string' || !/^[0-9a-f]{64}$/.test(row.head)) throw new Error('Exact corpus byte length, digest, head and sequence required.');
    const path = childPath(base, row.path, false);
    revisions.push({ family: row.family as SourceFamily, relativePath: basename(path), byteLength: String(row.byteLength), digest: row.sha256, head: row.head, sequence: String(row.sequence) });
    return { family: row.family as SourceFamily, path, projectPath: childPath(base, row.projectRoot, true) };
  });
  if (new Set(sources.map(source => source.path)).size !== sources.length) throw new Error('Duplicate performance source.');
  const raw = (selected.countsExpected === null && variant === 'malformed'
    ? { vertices: null, edges: null, findings: null } : selected.countsExpected) as Record<string, unknown> | undefined;
  if (!raw || ['vertices', 'edges', 'findings'].some(key => raw[key] !== null && (typeof raw[key] !== 'string' || !/^(0|[1-9][0-9]*)$/.test(raw[key] as string)))) throw new Error('Explicit decimal or null count expectations required.');
  return { sources, revisions, expected: { vertices: raw.vertices as string | null, edges: raw.edges as string | null, findings: raw.findings as string | null } };
}

/**
 * Bind captured recorded revisions to the prepared manifest independently of counts or opaque namespaces.
 * @param selected Explicit file grants and generator revision expectations.
 * @param actual Revisions captured by the actual recorded importer, not filesystem stat guesses.
 * @returns Nothing after exact multiset equality, including repeated basenames from distinct selected roots.
 * @throws {Error} For missing, extra, changed or duplicated captured revisions.
 */
export function assertPerformanceRevisions(selected: PerformanceSourceSet, actual: PerformanceSourceSet['revisions']): void {
  const key = (source: PerformanceSourceSet['revisions'][number]) => JSON.stringify([source.family, source.relativePath, source.byteLength, source.digest, source.head, source.sequence]);
  const expected = selected.revisions.map(key).sort(); const observed = actual.map(key).sort();
  if (expected.length !== selected.sources.length || expected.length !== observed.length || expected.some((value, index) => value !== observed[index])) throw new Error('Captured corpus revisions differ from the prepared manifest.');
}

/**
 * Read a bounded regular generator manifest and bind its source paths to its own directory.
 * @param filename Absolute manifest.json filename.
 * @param variant Prepared input set; malformed is an explicit negative oracle.
 * @returns Validated explicit selection and expectations.
 * @throws {Error} For unreadable/nonregular/oversized manifest or invalid selected fields.
 */
export async function loadPerformanceSourceSet(filename: string, variant: 'base' | 'append' | 'malformed'): Promise<PerformanceSourceSet> {
  if (!isAbsolute(filename) || basename(filename) !== 'manifest.json') throw new Error('Absolute manifest.json required.');
  const info = await lstat(filename);
  if (!info.isFile() || info.isSymbolicLink() || info.size > 1024 * 1024) throw new Error('Bounded regular corpus manifest required.');
  return performanceSourceSet(dirname(filename), JSON.parse(await readFile(filename, 'utf8')), variant);
}

/**
 * Admit recorded sources through the production direct TypeScript worker and archive.
 * @param selected Explicit prepared source set.
 * @param runtime Fixed trusted local toolchain and built worker paths.
 * @param control Optional phase observer and cancellation, neither of which changes acceptance budgets.
 * @returns Actual graph counts and redacted recorded-source import report; no performance verdict.
 * @throws {Error} For invalid runtime, rejected source/import, or any non-null count mismatch.
 */
export async function canonicalPerformanceOracle(selected: PerformanceSourceSet, runtime: PerformanceRuntime, control: PerformanceOracleControl = {}) {
  const { scratch, archiveDirectory, broker } = await oracleBroker(runtime); const owner = 'performance-corpus-oracle';
  let session: ImportSession | null = null;
  try {
    control.progress?.(1, 'Admit selected sources');
    const opened = await broker.open(owner, selected.sources, control.signal);
    session = new ImportSession({ sessionId: owner, capability: opened.capability, sources: opened.sources, broker, archiveDirectory,
      workerFactory: () => {
        const worker = new NativeImportWorker(runtime.workerFile);
        return { initialize: input => worker.initialize(input), consume: chunk => worker.consume(chunk), finish: () => worker.finish(),
          importDirect: async (input, materialAvailable, signal, progress) => {
            control.progress?.(3, 'Stream recorded sources into the compact worker');
            const ready = await worker.importDirect(input, materialAvailable, signal, value => { progress?.(value); control.importProgress?.(value); });
            control.progress?.(4, 'Complete direct graph and query index'); return ready;
          }, span: (source, pointer, sequence) => worker.span(source, pointer, sequence), terminate: () => worker.terminate() };
      } });
    control.progress?.(2, 'Prepare direct captured source handles');
    const snapshot = await session.import(opened.sources.map(source => source.sourceId), null, control.signal).catch(error => { control.rejected?.(performanceFailure(error)); throw error; });
    control.progress?.(5, 'Publish snapshot and adopt captured source archive');
    control.progress?.(6, 'Verify captured revisions and observed counts');
    const state = session.state();
    if (state.report?.status !== 'ready') throw new Error('Recorded import did not publish a complete ready snapshot.');
    assertPerformanceRevisions(selected, snapshot.sources);
    for (const key of ['vertices', 'edges', 'findings'] as const) if (selected.expected[key] !== null && selected.expected[key] !== snapshot.counts[key]) throw new Error(`Corpus ${key} differs: expected ${selected.expected[key]}, observed ${snapshot.counts[key]}.`);
    return { format: 'jai.fabric-explorer.performance-oracle/1', counts: snapshot.counts as Counts,
      recordedAdmission: true, canonicalAdmission: false, expectedCountsChecked: selected.expected, report: state.report,
      sources: snapshot.sources.map(source => ({ family: source.family, relativePath: source.relativePath, byteLength: source.byteLength, digest: source.digest, head: source.head, sequence: source.sequence })),
      scope: 'Actual direct TypeScript recorded-source importer and production worker; no GUI, rendering or authority qualification.' };
  } finally {
    await session?.dispose(); await broker.disposeSession(owner);
    try { await control.beforeCleanup?.(scratch); }
    finally { await rm(scratch, { recursive: true, force: true }); }
  }
}

/**
 * Size the direct recorded model and compact storage, with expanded DTOs reported separately.
 * @param selected Explicit prepared source set, never a bare DTO graph.
 * @param runtime Fixed worker artifact and production-format namespace provider.
 * @param control Optional diagnostic observer and production capture cancellation.
 * @returns Actual model counts/compact accounting, logical fact bytes and expanded JSON diagnostics.
 * @throws {Error} For rejected recorded input, malformed facts, model limits or count mismatch.
 */
export async function canonicalPerformanceSizingOracle(selected: PerformanceSourceSet, runtime: PerformanceRuntime, control: PerformanceOracleControl = {}) {
  const { scratch, archiveDirectory, broker } = await oracleBroker(runtime); const owner = 'performance-corpus-sizing';
  let capture: Awaited<ReturnType<ReadBroker['captureDirect']>> | null = null;
  let stage: Awaited<ReturnType<CaptureArchiveStore['stageDirect']>> | null = null;
  try {
    control.progress?.(1, 'Admit selected sources');
    const opened = await broker.open(owner, selected.sources, control.signal); const ids = opened.sources.map(source => source.sourceId);
    control.progress?.(2, 'Prepare direct source and archive handles');
    capture = await broker.captureDirect(owner, opened.capability, ids, control.signal);
    stage = await new CaptureArchiveStore(archiveDirectory).stageDirect(capture.files, control.signal);
    const input = { binding: { sessionId: owner, capability: opened.capability, generation: null }, generation: '1', limits: DEFAULT_IMPORT_LIMITS,
      files: capture.files.map(source => ({ revision: draftDirectRevision(source), stamp: source.stamp, sourceHandle: source.handle, archiveHandle: stage!.outputs.get(source.admitted.sourceId)! })) };
    control.progress?.(3, 'Stream recorded sources into the direct model');
    const { model, ready } = await buildDirectModel(input, { cancelled: () => !!control.signal?.aborted, materialAvailable: (sourceId, blobId) => capture!.materialAvailable(sourceId, blobId) });
    await capture.validate(); assertPerformanceRevisions(selected, ready.descriptor.sources);
    control.progress?.(4, 'Complete compact graph and query index');
    let expandedDtoJsonBytes = 0; let largestRecordBytes = 0;
    control.progress?.(5, 'Collect expanded-size and topology diagnostics');
    const byKind: Record<string, { count: number; bytes: number }> = Object.create(null);
    const versions = new Map<string, { id: string; versionId: string; source: unknown; multiple: boolean }>();
    const versionSamples: { logicalIdentity: string; versions: readonly { id: string; versionId: string; source: unknown }[] }[] = []; let multipleVersionGroups = 0;
    let maximumLabelCodePoints = 0; let longUnicodeLabels = 0;
    const templates = new Map<string, { sourceRelativePath: string; relation: string; originKind: string; count: number; bytes: number; minimum: number; maximum: number }>();
    for (const record of model.records()) {
      const bytes = Buffer.byteLength(JSON.stringify(record)); expandedDtoJsonBytes += bytes; largestRecordBytes = Math.max(largestRecordBytes, bytes);
      const kind = 'relation' in record ? 'edge' : record.kind;
      byKind[kind] ??= { count: 0, bytes: 0 }; byKind[kind]!.count++; byKind[kind]!.bytes += bytes;
      if ('kind' in record) {
        let codePoints = 0; for (const _character of record.label) codePoints++;
        maximumLabelCodePoints = Math.max(maximumLabelCodePoints, codePoints);
        if (codePoints >= 96 && /[^\u0000-\u007f]/u.test(record.label)) longUnicodeLabels++;
      }
      if ('kind' in record && record.kind === 'version' && record.identity.kind === 'version') {
        const reference = record.identity.ref; const key = JSON.stringify([record.identity.projectId, reference.engagement, reference.scope, reference.logical_id]);
        const previous = versions.get(key);
        if (!previous) versions.set(key, { id: record.id, versionId: reference.version_id, source: record.source, multiple: false });
        else if (!previous.multiple && previous.versionId !== reference.version_id) {
          previous.multiple = true; multipleVersionGroups++;
          if (versionSamples.length < 8) versionSamples.push({ logicalIdentity: key, versions: [{ id: previous.id, versionId: previous.versionId, source: previous.source }, { id: record.id, versionId: reference.version_id, source: record.source }] });
        }
      }
      if ('relation' in record) {
        const key = JSON.stringify([record.source.relativePath, record.relation, record.identity.origin.kind]);
        let template = templates.get(key);
        if (!template) { template = { sourceRelativePath: record.source.relativePath, relation: record.relation, originKind: record.identity.origin.kind, count: 0, bytes: 0, minimum: bytes, maximum: bytes }; templates.set(key, template); }
        template.count++; template.bytes += bytes; template.minimum = Math.min(template.minimum, bytes); template.maximum = Math.max(template.maximum, bytes);
      }
    }
    for (const key of ['vertices', 'edges', 'findings'] as const) if (selected.expected[key] !== null && selected.expected[key] !== ready.descriptor.counts[key]) throw new Error(`Corpus ${key} differs from its sizing expectation.`);
    control.progress?.(6, 'Verify counts and complete diagnostic report');
    return { format: 'jai.fabric-explorer.performance-sizing/2', recordedAdmission: true, canonicalAdmission: false, counts: ready.descriptor.counts,
      semanticFactBytes: model.usage().semanticFactBytes, compactGraphBytes: model.compactBytes(), compactUsage: model.usage(), expandedDtoJsonBytes, largestRecordBytes, byKind, edgeTemplates: [...templates.values()],
      topology: { ...observedTopology(model.graph()), multipleVersionGroups, versionSamples, maximumLabelCodePoints, longUnicodeLabels, longLabelDefinition: 'At least 96 Unicode code points, with at least one non-ASCII code point.' },
      namespaceFormat: 'Unmodified production PersistentNamespaceRegistry UUID identifiers',
      scope: 'Actual direct TypeScript parser and shipped ImportModel sizing only; not a timing, native-worker or rendering measurement.' };
  } finally {
    await capture?.dispose(); await stage?.dispose(); await broker.disposeSession(owner);
    try { await control.beforeCleanup?.(scratch); }
    finally { await rm(scratch, { recursive: true, force: true }); }
  }
}
