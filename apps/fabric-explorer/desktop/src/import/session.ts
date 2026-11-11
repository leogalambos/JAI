// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Atomic import publication with independent accepted worker and immutable source archive ownership. */
import { assertAdapterInput, assertSnapshot, decodeBytePage } from '@jai/fabric-explorer-contracts';
import type { AdmittedSource, BytePage, SnapshotDescriptor } from '@jai/fabric-explorer-contracts';
import type { CapturedSources, SemanticBrokerPort, SemanticLease } from '../broker/semantic-types.js';
import { unsigned } from './facts.js';
import { CacheUnavailableError, CaptureArchiveStore } from '../broker/capture-archive.js';
import { ReadBroker, BrokerError, sameFileStamp } from '../broker/read-broker.js';
import type { NativeFileStamp, DirectCapture, DirectArchiveStage } from '../broker/direct-types.js';
import { draftDirectRevision } from '../broker/direct-types.js';
import { SemanticError } from '../broker/semantic-broker.js';
import { captureReport, failedReport, readerFailureReport } from './report.js';
import { ImportError, importLimits } from './types.js';
import type { ImportLimits, ImportReport, ImportState } from './types.js';
import type { GraphRequest, GraphGroups } from '../graph/types.js';
import type { QueryPage, QueryContinuation, QueryDrop, LayoutSelection, GroupSelection, ProjectionFilterSelection, ProjectionFilterView } from '../explore/types.js';
import type { LayoutWireResult } from '../explore/layout-wire.js';
import type { ImportWorkerFactory, ImportWorkerPort } from './worker-client.js';
/** Exact record-local source page, served only from the accepted immutable archive. */
export interface SourcePageInput { readonly sourceId: string; readonly pointer: string; readonly sequence: string | null; readonly offset: string; readonly length: number }
/** Controller-facing importer; root selection and IPC authentication remain outside this facade. */
export interface ImportSessionPort {
  /** Import an admitted subset against the exact current generation. */
  import(sourceIds: readonly string[], expectedGeneration: string | null, signal?: AbortSignal): Promise<SnapshotDescriptor>;
  /** Explicitly refresh the previously published subset. */
  refresh(expectedGeneration: string, signal?: AbortSignal): Promise<SnapshotDescriptor>;
  /** Read a bounded accepted-revision page without reopening live inputs. */
  sourcePage(payload: SourcePageInput, expectedGeneration: string, signal?: AbortSignal): Promise<BytePage>;
  /** Start an accepted-generation indexed query without transferring the whole model. */
  queryStart?(request: GraphRequest, signal?: AbortSignal): Promise<QueryPage>;
  /** Search only finding records using the existing S04 staged response contract. */
  searchFindings?(request: Extract<GraphRequest, { operation: 'search.page' }>, signal?: AbortSignal): Promise<QueryPage>;
  /** Filter an owned bounded projection and retain a separate numeric layout token. */
  filterProjection?(input: ProjectionFilterSelection, signal?: AbortSignal): Promise<ProjectionFilterView>;
  /** Pull one retained current-generation query frame. */
  queryNext?(input: QueryContinuation, signal?: AbortSignal): Promise<QueryPage>;
  /** Release explicitly owned ephemeral job/projection tokens. */
  queryDrop?(input: QueryDrop): Promise<void>;
  /** Layout a bounded current-generation projection by opaque token. */
  layout?(input: LayoutSelection, signal?: AbortSignal): Promise<LayoutWireResult>;
  /** Query deterministic grouping under the shared indexed filter. */
  groups?(input: GroupSelection, signal?: AbortSignal): Promise<GraphGroups>;
  /** Obtain detached metadata/report; no full graph is transferred. */
  state(): ImportState;
  /** Revoke work and release owned workers/captures. */
  dispose(): Promise<void>;
}
/** Trusted immutable session authority and fixed worker construction. */
export interface ImportSessionOptions { readonly sessionId: string; readonly capability: string; readonly sources: readonly AdmittedSource[]; readonly broker: SemanticBrokerPort | ReadBroker; readonly archiveDirectory?: string; readonly workerFactory: ImportWorkerFactory; readonly limits?: ImportLimits }
interface Published { readonly worker: ImportWorkerPort; readonly archive: CapturedSources; readonly descriptor: SnapshotDescriptor; readonly selected: readonly string[]; readonly report: ImportReport; readonly stamps?: ReadonlyMap<string, NativeFileStamp> }
/** One root session; failure of a candidate never destroys its separate accepted worker/archive. */
export class ImportSession implements ImportSessionPort {
  private readonly limits: ImportLimits;
  private readonly sources: readonly AdmittedSource[];
  private published: Published | null = null;
  private readonly exploration = new Set<AbortController>();
  private report: ImportReport | null = null;
  private stale = false;
  private progress: import('./progress.js').ImportProgress | null = null;
  private disposed = false;
  private epoch = 0;
  private active: AbortController | null = null;
  private candidateWorker: ImportWorkerPort | null = null;
  private running: Promise<SnapshotDescriptor> | null = null;
  /**
   * Bind one native-admitted capability without reading any source or starting a worker.
   * @param options Trusted session/capability/catalog and owned broker/worker factories.
   * @throws {ImportError} For duplicate catalog IDs or invalid trusted configuration.
   */
  constructor(private readonly options: ImportSessionOptions) {
    this.limits = importLimits(options.limits); this.sources = structuredClone(options.sources);
    if (!options.sessionId || !options.capability || !this.sources.length || new Set(this.sources.map(source => source.sourceId)).size !== this.sources.length) throw new ImportError('invalid-model', 'Invalid admitted import catalog.');
  }
  private checkGeneration(expected: string | null): void {
    if (this.disposed) throw new ImportError('session-mismatch', 'Import session is closed.');
    if (expected !== (this.published?.descriptor.generation ?? null)) throw new ImportError('stale-generation', 'The snapshot generation changed.');
  }
  /**
   * Import one explicit subset, retaining the complete previous generation on any candidate failure.
   * @param sourceIds Duplicate-free admitted source IDs.
   * @param expectedGeneration Exact current published generation, or null for a cold import.
   * @param signal Optional cancellation; native dialogs are not involved.
   * @returns Detached new snapshot metadata after atomic publication.
   * @throws {ImportError} For stale context, overlap, unsupported data, cancellation or failed candidate work.
   */
  async import(sourceIds: readonly string[], expectedGeneration: string | null, signal?: AbortSignal): Promise<SnapshotDescriptor> { return this.importSelected(sourceIds, expectedGeneration, signal, false); }
  private async importSelected(sourceIds: readonly string[], expectedGeneration: string | null, signal: AbortSignal | undefined, reuseUnchanged: boolean): Promise<SnapshotDescriptor> {
    this.checkGeneration(expectedGeneration);
    if (this.active) throw new ImportError('resource-limit', 'An import is already active.');
    if (!Array.isArray(sourceIds) || !sourceIds.length || sourceIds.length > this.sources.length || new Set(sourceIds).size !== sourceIds.length || sourceIds.some(id => !this.sources.some(source => source.sourceId === id))) throw new ImportError('capability-mismatch', 'Import selection contains an unadmitted source.');
    if (signal?.aborted) throw new ImportError('cancelled', 'Import cancelled.');
    assertAdapterInput({ binding: { sessionId: this.options.sessionId, capability: this.options.capability, generation: expectedGeneration }, sources: this.sources.filter(source => sourceIds.includes(source.sourceId)), previous: this.published?.descriptor ?? null, checkpointToken: null });
    const selected = [...sourceIds]; const abort = new AbortController(); this.active = abort;
    const cancel = () => { abort.abort(); void this.candidateWorker?.terminate(); };
    signal?.addEventListener('abort', cancel, { once: true });
    const epoch = this.epoch;
    this.running = this.run(selected, expectedGeneration, epoch, abort, reuseUnchanged);
    try { return await this.running; }
    finally { signal?.removeEventListener('abort', cancel); this.active = null; this.running = null; this.candidateWorker = null; }
  }
  private async run(selected: readonly string[], expected: string | null, epoch: number, abort: AbortController, reuseUnchanged: boolean): Promise<SnapshotDescriptor> {
    if ('captureDirect' in this.options.broker) return this.runDirect(this.options.broker, selected, expected, epoch, abort, reuseUnchanged);
    let lease: SemanticLease | null = null; let worker: ImportWorkerPort | null = null; let archive: CapturedSources | null = null;
    const check = () => { if (abort.signal.aborted || this.disposed || this.epoch !== epoch) throw new ImportError('cancelled', 'Import cancelled.'); this.checkGeneration(expected); };
    try {
      check(); lease = await this.options.broker.capture(this.options.sessionId, this.options.capability, selected, abort.signal); check();
      const binding = { sessionId: this.options.sessionId, capability: this.options.capability, generation: expected };
      const report = captureReport(lease, binding, selected, this.limits);
      for (const revision of lease.sources) {
        const admitted = this.sources.find(source => source.sourceId === revision.sourceId);
        if (!admitted || (['projectId', 'rootId', 'family', 'relativePath'] as const).some(key => admitted[key] !== revision[key])) throw new ImportError('invalid-model', 'Captured source differs from its admitted namespace.');
      }
      worker = this.options.workerFactory(); this.candidateWorker = worker;
      await worker.initialize({ binding, generation: String(BigInt(expected ?? '0') + 1n), sources: lease.sources, report, limits: this.limits }); check();
      let cursor: string | null = null;
      do {
        const chunk = await lease.chunk(cursor, abort.signal); check();
        await worker.consume(chunk); check(); cursor = chunk.next;
      } while (cursor !== null);
      const ready = await worker.finish(); check(); assertSnapshot(ready.descriptor);
      if (ready.descriptor.sessionId !== this.options.sessionId || ready.descriptor.generation !== String(BigInt(expected ?? '0') + 1n) || JSON.stringify(ready.descriptor.sources) !== JSON.stringify(lease.sources) || ready.report.status !== 'ready') throw new ImportError('invalid-model', 'Candidate worker metadata differs from its capture.');
      archive = await lease.persist(abort.signal); check();
      await lease.release(); lease = null; check();
      const old = this.published;
      // There is no asynchronous gap between final generation validation and this publication reference swap.
      this.published = { worker, archive, descriptor: structuredClone(ready.descriptor), selected: [...selected], report: structuredClone(ready.report) };
      this.report = structuredClone(ready.report); this.stale = false; worker = null; archive = null; this.candidateWorker = null;
      if (old) {
        for (const work of this.exploration) work.abort();
        const cleanup = await Promise.allSettled([old.worker.terminate(), old.archive.dispose()]);
        if (cleanup.some(result => result.status === 'rejected')) this.report = { ...this.report, limitation: 'Previous snapshot resource cleanup failed; close the session before reopening sources.' };
      }
      return structuredClone(this.published.descriptor);
    } catch (error) {
      const failure = abort.signal.aborted || this.disposed ? new ImportError('cancelled', 'Import cancelled.') : error instanceof ImportError ? error : this.brokerFailure(error, selected);
      if (!this.disposed && this.epoch === epoch) { this.report = failedReport(selected.length, failure); this.stale = this.published !== null; }
      throw failure;
    } finally { await Promise.allSettled([...(worker ? [worker.terminate()] : []), ...(archive ? [archive.dispose()] : []), ...(lease ? [lease.release()] : [])]); }
  }
  private async runDirect(broker: ReadBroker, selected: readonly string[], expected: string | null, epoch: number, abort: AbortController, reuseUnchanged: boolean): Promise<SnapshotDescriptor> {
    let capture: DirectCapture | null = null; let stage: DirectArchiveStage | null = null; let worker: ImportWorkerPort | null = null; let archive: CapturedSources | null = null;
    const check = () => { if (abort.signal.aborted || this.disposed || this.epoch !== epoch) throw new ImportError('cancelled', 'Import cancelled.'); this.checkGeneration(expected); };
    try {
      check(); capture = await broker.captureDirect(this.options.sessionId, this.options.capability, selected, abort.signal); check();
      const old = this.published;
      if (reuseUnchanged && old?.stamps && JSON.stringify(old.selected) === JSON.stringify(selected) && capture.files.every(file => { const prior = old.stamps!.get(file.admitted.sourceId); return prior && sameFileStamp(prior, file.stamp); })) {
        await capture.validate(); check(); this.report = structuredClone(old.report); this.stale = false; return structuredClone(old.descriptor);
      }
      if (!this.options.archiveDirectory) throw new ImportError('read-failed', 'Private capture archive is not configured.');
      stage = await new CaptureArchiveStore(this.options.archiveDirectory).stageDirect(capture.files, abort.signal); check();
      worker = this.options.workerFactory(); this.candidateWorker = worker; if (!worker.importDirect) throw new ImportError('worker-failed', 'Direct import worker is unavailable.');
      const ready = await worker.importDirect({ binding: { sessionId: this.options.sessionId, capability: this.options.capability, generation: expected }, generation: String(BigInt(expected ?? '0') + 1n), limits: this.limits, files: capture.files.map(file => ({ revision: draftDirectRevision(file), stamp: file.stamp, sourceHandle: file.handle, archiveHandle: stage!.outputs.get(file.admitted.sourceId)! })) }, capture.materialAvailable, abort.signal, value => { if (!this.disposed && this.epoch === epoch && this.active === abort && worker !== null && this.candidateWorker === worker && !abort.signal.aborted) this.progress = { ...value }; });
      check(); assertSnapshot(ready.descriptor);
      if (ready.descriptor.sessionId !== this.options.sessionId || ready.descriptor.generation !== String(BigInt(expected ?? '0') + 1n) || ready.report.status !== 'ready' || ready.descriptor.sources.length !== selected.length || selected.some(sourceId => !ready.descriptor.sources.some(source => source.sourceId === sourceId))) throw new ImportError('invalid-model', 'Direct candidate metadata differs from selection.');
      for (const source of ready.descriptor.sources) { const original = capture.files.find(file => file.admitted.sourceId === source.sourceId); if (!original || source.revisionId !== original.revisionId || source.byteLength !== original.stamp.size || (['projectId', 'rootId', 'relativePath', 'family'] as const).some(key => source[key] !== original.admitted[key])) throw new ImportError('invalid-model', 'Direct candidate source binding changed.'); }
      await capture.validate(); check(); archive = await stage.adopt(ready.descriptor.sources); check();
      this.published = { worker, archive, descriptor: structuredClone(ready.descriptor), selected: [...selected], report: structuredClone(ready.report), stamps: new Map(capture.files.map(file => [file.admitted.sourceId, file.stamp])) };
      this.report = structuredClone(ready.report); this.stale = false; this.candidateWorker = null; worker = null; archive = null; stage = null;
      if (old) { const cleanup = await Promise.allSettled([old.worker.terminate(), old.archive.dispose()]); if (cleanup.some(result => result.status === 'rejected')) this.report = { ...this.report, limitation: 'Previous snapshot resource cleanup failed; close the session before reopening sources.' }; }
      return structuredClone(this.published.descriptor);
    } catch (error) {
      const failure = abort.signal.aborted || this.disposed ? new ImportError('cancelled', 'Import cancelled.') : error instanceof ImportError ? error : this.brokerFailure(error, selected);
      if (!this.disposed && this.epoch === epoch) { this.report = failedReport(selected.length, failure); this.stale = this.published !== null; } throw failure;
    } finally {
      if (this.epoch === epoch) this.progress = null;
      // A failed stop retains the owned stage, but cannot skip independent handle cleanup.
      let stopped = !worker; let cleanupFailed = false;
      if (worker) { try { await worker.terminate(); stopped = true; } catch { cleanupFailed = true; } }
      const cleanup = await Promise.allSettled([...(capture ? [capture.dispose()] : []), ...(stage ? [...stage.outputs.values()].map(file => file.close()) : []), ...(stopped && archive ? [archive.dispose()] : []), ...(stopped && stage ? [stage.dispose()] : [])]);
      cleanupFailed ||= cleanup.some(result => result.status === 'rejected');
      if (cleanupFailed && this.report && this.epoch === epoch) this.report = { ...this.report, limitation: 'Candidate cleanup could not be confirmed; close the viewer before clearing only its temporary capture cache.' };
    }
  }
  private brokerFailure(error: unknown, selected: readonly string[]): ImportError {
    if (error instanceof BrokerError) {
      const failure = new ImportError(error.code === 'cancelled' ? 'cancelled' : error.code === 'resource-limit' ? 'resource-limit' : 'read-failed', error.message);
      return error.code === 'source-changed' ? new ImportError('read-failed', error.message, { ...failedReport(selected.length, failure), limitation: error.message }) : failure;
    }
    if (error instanceof CacheUnavailableError) {
      const recovery = 'Capture cache is in use or stale; close other viewer instances and clear only the viewer temporary capture cache.';
      const failure = new ImportError('read-failed', recovery);
      return new ImportError('read-failed', recovery, { ...failedReport(selected.length, failure), limitation: recovery });
    }
    if (error instanceof SemanticError) {
      try { const report = readerFailureReport(error.report, error.compatibility, selected, this.limits); const code = ['resource-limit', 'cancelled', 'incompatible-source'].includes(error.code) ? error.code as 'resource-limit' | 'cancelled' | 'incompatible-source' : 'read-failed'; return new ImportError(code, error.code === 'source-changed' ? 'Selected file was replaced; reopen sources to admit the new file.' : 'The selected sources could not be imported.', report); }
      catch { return new ImportError('read-failed', 'The selected sources could not be imported.'); }
    }
    const code = error && typeof error === 'object' ? (error as { code?: unknown }).code : null;
    if (code === 'resource-limit' || code === 'cancelled' || code === 'incompatible-source') return new ImportError(code, code === 'resource-limit' ? 'Import resource limit exceeded.' : code === 'cancelled' ? 'Import cancelled.' : 'The selected source format is unsupported.');
    return new ImportError('read-failed', 'The selected sources could not be imported.');
  }
  /**
   * Explicitly refresh the exact accepted source subset.
   * @param expectedGeneration Current published generation.
   * @param signal Optional cancellation signal.
   * @returns New descriptor only after a complete successful candidate.
   * @throws {ImportError} For no prior snapshot or any import failure.
   */
  async refresh(expectedGeneration: string, signal?: AbortSignal): Promise<SnapshotDescriptor> { this.checkGeneration(expectedGeneration); if (!this.published) throw new ImportError('stale-generation', 'There is no snapshot to refresh.'); return this.importSelected(this.published.selected, expectedGeneration, signal, true); }
  /**
   * Page an exact accepted raw record span from independent captured bytes.
   * @param payload Exact source/record locator and record-relative page bounds.
   * @param expectedGeneration Current accepted generation.
   * @param signal Optional cancellation of this page request.
   * @returns Bounded raw bytes with the requested locator and record-relative EOF.
   * @throws {ImportError} For stale generation, unknown locator, invalid bounds, cancellation or failed archive read.
   */
  async sourcePage(payload: SourcePageInput, expectedGeneration: string, signal?: AbortSignal): Promise<BytePage> {
    this.checkGeneration(expectedGeneration); const published = this.published;
    if (!published || signal?.aborted) throw new ImportError('cancelled', 'Source page cancelled.');
    if (!payload || Object.keys(payload).sort().join() !== 'length,offset,pointer,sequence,sourceId' || typeof payload.sourceId !== 'string' || typeof payload.pointer !== 'string' || payload.pointer.length > 1024 * 1024 || (payload.sequence !== null && unsigned(payload.sequence) < 0n) || !Number.isSafeInteger(payload.length) || payload.length < 1 || payload.length > 256 * 1024) throw new ImportError('invalid-message', 'Invalid source page bounds.');
    const offset = unsigned(payload.offset); const span = await published.worker.span(payload.sourceId, payload.pointer, payload.sequence);
    this.checkGeneration(expectedGeneration);
    if (!span || offset > unsigned(span.length)) throw new ImportError('not-found', 'The source locator is not represented in this snapshot.');
    const remaining = unsigned(span.length) - offset; const length = Number(remaining < BigInt(payload.length) ? remaining : BigInt(payload.length));
    let bytes: Uint8Array<ArrayBufferLike> = new Uint8Array(0);
    if (length) {
      const page = await published.archive.page(payload.sourceId, String(unsigned(span.offset) + offset), length);
      if (page.sourceId !== payload.sourceId || page.offset !== String(unsigned(span.offset) + offset)) throw new ImportError('read-failed', 'Captured source page differs from the requested revision.');
      bytes = decodeBytePage(page); if (bytes.length !== length) throw new ImportError('read-failed', 'Captured source page is incomplete.');
    }
    this.checkGeneration(expectedGeneration); if (signal?.aborted || this.published !== published) throw new ImportError('cancelled', 'Source page cancelled.');
    return { sourceId: payload.sourceId, pointer: payload.pointer, sequence: payload.sequence, offset: payload.offset, byteLength: bytes.length, bytesBase64: Buffer.from(bytes).toString('base64'), eof: offset + BigInt(bytes.length) >= unsigned(span.length) };
  }
  private async accepted<T>(binding: { sessionId: string; capability: string | null; generation: string | null }, signal: AbortSignal | undefined, work: (worker: ImportWorkerPort, signal: AbortSignal) => Promise<T>, release?: (worker: ImportWorkerPort, result: T) => Promise<void>): Promise<T> {
    this.checkGeneration(binding.generation);
    const published = this.published;
    if (!published || binding.sessionId !== this.options.sessionId || binding.capability !== this.options.capability) throw new ImportError('capability-mismatch', 'Exploration context rejected.');
    if (signal?.aborted || this.exploration.size >= 8) throw new ImportError(signal?.aborted ? 'cancelled' : 'resource-limit', 'Exploration is unavailable.');
    const abort = new AbortController(); const cancel = () => abort.abort(); this.exploration.add(abort); signal?.addEventListener('abort', cancel, { once: true });
    try {
      const result = await work(published.worker, abort.signal);
      try {
        if (abort.signal.aborted || this.published !== published) throw new ImportError('cancelled', 'Exploration result discarded.');
        this.checkGeneration(binding.generation); return result;
      } catch (error) { await release?.(published.worker, result).catch(() => {}); throw error; }
    } finally { signal?.removeEventListener('abort', cancel); this.exploration.delete(abort); }
  }
  /** Start a worker-local query against the exact current sealed generation. */
  async queryStart(request: GraphRequest, signal?: AbortSignal): Promise<QueryPage> { return this.accepted(request.binding, signal, (worker, cancel) => { if (!worker.queryStart) throw new ImportError('worker-failed', 'Exploration is unavailable.'); return worker.queryStart(request, cancel); }, async (worker, page) => { await worker.queryDrop?.({ binding: request.binding, requestId: request.requestId, continuationToken: page.continuationToken, projectionToken: page.projectionToken }); }); }
  /** Search accepted findings using the existing finite staged response protocol. */
  async searchFindings(request: Extract<GraphRequest, { operation: 'search.page' }>, signal?: AbortSignal): Promise<QueryPage> { return this.accepted(request.binding, signal, (worker, cancel) => { if (!worker.searchFindings) throw new ImportError('worker-failed', 'Findings search is unavailable.'); return worker.searchFindings(request, cancel); }, async (worker, page) => { await worker.queryDrop?.({ binding: request.binding, requestId: request.requestId, continuationToken: page.continuationToken, projectionToken: page.projectionToken }); }); }
  /** Filter accepted numeric projection handles and release late cancelled output ownership. */
  async filterProjection(input: ProjectionFilterSelection, signal?: AbortSignal): Promise<ProjectionFilterView> { return this.accepted(input.binding, signal, (worker, cancel) => { if (!worker.filterProjection) throw new ImportError('worker-failed', 'Projection filtering is unavailable.'); return worker.filterProjection(input, cancel); }, async (worker, view) => { await worker.queryDrop?.({ binding: input.binding, requestId: input.requestId, continuationToken: null, projectionToken: view.projectionToken }); }); }
  /** Pull the next retained finite-progress query frame without reopening sources. */
  async queryNext(input: QueryContinuation, signal?: AbortSignal): Promise<QueryPage> { return this.accepted(input.binding, signal, (worker, cancel) => { if (!worker.queryNext) throw new ImportError('worker-failed', 'Exploration is unavailable.'); return worker.queryNext(input, cancel); }, async (worker, page) => { await worker.queryDrop?.({ binding: input.binding, requestId: input.requestId, continuationToken: page.continuationToken, projectionToken: page.projectionToken }); }); }
  /** Release only current-generation ephemeral worker tokens. */
  async queryDrop(input: QueryDrop): Promise<void> { await this.accepted(input.binding, undefined, worker => { if (!worker.queryDrop) throw new ImportError('worker-failed', 'Exploration is unavailable.'); return worker.queryDrop(input); }); }
  /** Compute layout on the exact current retained numeric projection. */
  async layout(input: LayoutSelection, signal?: AbortSignal): Promise<LayoutWireResult> { return this.accepted(input.binding, signal, (worker, cancel) => { if (!worker.layout) throw new ImportError('worker-failed', 'Layout is unavailable.'); return worker.layout(input, cancel); }); }
  /** Compute facets under the current accepted query index. */
  async groups(input: GroupSelection, signal?: AbortSignal): Promise<GraphGroups> { return this.accepted(input.binding, signal, (worker, cancel) => { if (!worker.groups) throw new ImportError('worker-failed', 'Grouping is unavailable.'); return worker.groups(input, cancel); }); }
  /** Return detached descriptor/report metadata; failed candidates never replace the descriptor. */
  state(): ImportState { return structuredClone({ snapshot: this.published?.descriptor ?? null, report: this.report, stale: this.stale, ...(this.progress ? { progress: this.progress } : {}) }); }
  /** Abort the candidate and release both accepted model and captured bytes idempotently. */
  async dispose(): Promise<void> {
    if (this.disposed) return; this.disposed = true; this.epoch++; this.active?.abort(); for (const work of this.exploration) work.abort();
    const published = this.published; this.published = null;
    await Promise.allSettled([...(this.candidateWorker ? [this.candidateWorker.terminate()] : []), ...(published ? [published.worker.terminate(), published.archive.dispose()] : []), ...(this.running ? [this.running] : [])]);
    this.report = null; this.stale = false;
  }
}
