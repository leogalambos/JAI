// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Main-owned fixed worker facade with bounded concurrent requests and accepted-worker exploration. */
import { Worker, type TransferListItem } from 'node:worker_threads';
import type { DirectWorkerInput, MaterialAvailability } from '../broker/direct-types.js';
import { isAbsolute } from 'node:path';
import { assertSnapshot, encodeWire } from '@jai/fabric-explorer-contracts';
import type { ModelInput, ModelReady, SourceSpan } from './model.js';
import { importProgress, type ImportProgress } from './progress.js';
import { ImportError } from './types.js';
import { queryPage, projectionFilterView } from '../explore/transport.js';
import type { GraphRequest, GraphGroups } from '../graph/types.js';
import type { QueryPage, QueryContinuation, QueryDrop, LayoutSelection, GroupSelection, ProjectionFilterSelection, ProjectionFilterView } from '../explore/types.js';
import type { LayoutWireResult } from '../explore/layout-wire.js';
/** Owned worker API; graph records never return to the main process. */
export interface ImportWorkerPort {
  /** Stream admitted native descriptors directly; no facts or source paths return to main. */
  importDirect?(input: DirectWorkerInput, materialAvailable: MaterialAvailability, signal?: AbortSignal, progress?: (value: ImportProgress) => void): Promise<ModelReady>;
  /** Initialize one candidate with fixed captured revisions and resource limits. */
  initialize(input: ModelInput): Promise<void>;
  /** Consume one bounded chunk and acknowledge it before the next pull. */
  consume(chunk: unknown): Promise<void>;
  /** Seal one candidate and return only its descriptor/report. */
  finish(): Promise<ModelReady>;
  /** Resolve a source locator in the sealed worker's immutable capture. */
  span(sourceId: string, pointer: string, sequence: string | null): Promise<SourceSpan | null>;
  /** Execute an accepted-generation query with cancellation, retaining graph records in the worker. */
  queryStart?(request: GraphRequest, signal?: AbortSignal): Promise<QueryPage>;
  /** Search only finding records using the existing S04 staged response contract. */
  searchFindings?(request: Extract<GraphRequest, { operation: 'search.page' }>, signal?: AbortSignal): Promise<QueryPage>;
  /** Filter an owned bounded projection and retain a separate numeric layout token. */
  filterProjection?(input: ProjectionFilterSelection, signal?: AbortSignal): Promise<ProjectionFilterView>;
  /** Pull the next correlated bounded query frame. */
  queryNext?(input: QueryContinuation, signal?: AbortSignal): Promise<QueryPage>;
  /** Release only owned ephemeral exploration tokens. */
  queryDrop?(input: QueryDrop): Promise<void>;
  /** Layout an owned bounded projection by numeric handles. */
  layout?(input: LayoutSelection, signal?: AbortSignal): Promise<LayoutWireResult>;
  /** Group accepted records through the shared filter view. */
  groups?(input: GroupSelection, signal?: AbortSignal): Promise<GraphGroups>;
  /** Terminate work and release worker-owned graph memory idempotently. */
  terminate(): Promise<void>;
}
/** Trusted constructor callback, implemented by fixed native workers or owned test ports. */
export interface ImportWorkerFactory { (): ImportWorkerPort }
interface Pending { readonly id: number; readonly resolve: (value: unknown) => void; readonly reject: (error: Error) => void; readonly cleanup: () => void }
/** Actual Node worker adapter; candidate heap failures are isolated from the published worker. */
export class NativeImportWorker implements ImportWorkerPort {
  private readonly worker: Worker;
  private readonly pending = new Map<number, Pending>();
  private nextId = 0;
  private stopped = false;
  private material: MaterialAvailability | null = null;
  private materialSources = new Set<string>();
  private materialPending = 0;
  private progress: ((value: ImportProgress) => void) | null = null;
  private directRequestId: number | null = null;
  /**
   * Launch the fixed compiled application worker, never source-controlled project code.
   * @param entry Absolute application-owned import-worker.cjs path supplied by composition.
   * @throws {ImportError} For relative entry paths or native worker creation failure.
   */
  constructor(entry: string) {
    if (!isAbsolute(entry)) throw new ImportError('worker-failed', 'Import worker path is not fixed.');
    this.worker = new Worker(entry, { resourceLimits: { maxOldGenerationSizeMb: 1152, maxYoungGenerationSizeMb: 32 } });
    this.worker.on('message', (input: unknown) => {
      if (!input || typeof input !== 'object' || Array.isArray(input)) { void this.terminate(); return; }
      const message = input as Record<string, unknown>;
      if (message.kind === 'importProgress') {
        if (Object.keys(message).sort().join() !== 'id,kind,value' || message.id !== this.directRequestId || !this.pending.has(Number(message.id))) return;
        try { this.progress?.(importProgress(message.value)); } catch { this.fail(new ImportError('worker-failed', 'Invalid import progress.')); }
        return;
      }
      if (message.kind === 'materialAvailability') {
        if (!this.material || Object.keys(message).sort().join() !== 'blobId,id,kind,sourceId' || !Number.isSafeInteger(message.id) || Number(message.id) < 1 || typeof message.sourceId !== 'string' || !this.materialSources.has(message.sourceId) || typeof message.blobId !== 'string' || !/^[0-9a-f]{64}$/.test(message.blobId) || this.materialPending >= 2) { this.fail(new ImportError('worker-failed', 'Invalid companion capability request.')); return; }
        this.materialPending++;
        void this.material(message.sourceId, message.blobId).then(availability => { if (!this.stopped) this.worker.postMessage({ kind: 'materialResult', id: message.id, availability }); }, () => { if (!this.stopped) this.worker.postMessage({ kind: 'materialResult', id: message.id, availability: 'unknown' }); }).finally(() => { this.materialPending--; });
        return;
      }
      const pending = typeof message.id === 'number' ? this.pending.get(message.id) : undefined;
      if (Object.keys(message).sort().join() !== 'id,ok,value' || !pending || typeof message.ok !== 'boolean') { this.fail(new ImportError('worker-failed', 'Invalid import worker response.')); return; }
      try { encodeWire(message.value); } catch { this.fail(new ImportError('worker-failed', 'Oversized import worker response.')); return; }
      this.pending.delete(pending.id); pending.cleanup();
      if (message.ok) pending.resolve(message.value);
      else {
        const failure = message.value as { code?: unknown; message?: unknown; report?: import('./types.js').ImportReport | null };
        const code = ['invalid-model', 'resource-limit', 'incompatible-source', 'cancelled', 'not-found', 'stale-generation', 'invalid-message', 'capability-mismatch', 'cursor-mismatch', 'read-failed'].includes(failure?.code as string) ? failure.code as ImportError['code'] : 'worker-failed';
        pending.reject(new ImportError(code, code === 'resource-limit' ? 'Import worker resource limit exceeded.' : code === 'incompatible-source' ? 'The selected source format is unsupported.' : 'Import worker rejected the candidate.', failure.report ?? null));
      }
    });
    this.worker.on('error', (error: Error & { code?: string }) => this.fail(new ImportError(error.code === 'ERR_WORKER_OUT_OF_MEMORY' ? 'resource-limit' : 'worker-failed', 'Import worker failed.')));
    this.worker.on('exit', () => this.fail(new ImportError('worker-failed', 'Import worker stopped.')));
  }
  private fail(error: ImportError): void { for (const pending of this.pending.values()) { pending.cleanup(); pending.reject(error); } this.pending.clear(); this.stopped = true; void this.worker.terminate(); }
  private async request(operation: string, value: unknown, signal?: AbortSignal, transfer: readonly TransferListItem[] = []): Promise<unknown> {
    if (this.stopped) throw new ImportError('worker-failed', 'Import worker is unavailable.');
    if ((this.pending.size > 0 && !['queryStart', 'searchFindings', 'filterProjection', 'queryNext', 'queryDrop', 'layout', 'groups', 'span'].includes(operation)) || this.pending.size >= 16) throw new ImportError('resource-limit', 'Import worker request limit exceeded.');
    if (signal?.aborted) throw new ImportError('cancelled', 'Exploration cancelled.');
    if (operation === 'directImport') { const direct = value as DirectWorkerInput; encodeWire({ binding: direct.binding, generation: direct.generation, limits: direct.limits, files: direct.files.map(file => ({ revision: file.revision, stamp: file.stamp })) }); } else encodeWire(value);
    const cancel = signal ? new SharedArrayBuffer(4) : undefined;
    const abort = () => { if (cancel) Atomics.store(new Int32Array(cancel), 0, 1); };
    signal?.addEventListener('abort', abort, { once: true });
    return new Promise((resolve, reject) => {
      const id = ++this.nextId; if (operation === 'directImport') this.directRequestId = id;
      this.pending.set(id, { id, resolve: result => {
        if (!signal?.aborted) { resolve(result); return; }
        const failure = new ImportError('cancelled', 'Exploration cancelled.');
        if (operation === 'queryStart' || operation === 'searchFindings' || operation === 'queryNext') {
          try { const page = queryPage(result); const owner = value as { binding: GraphRequest['binding']; requestId: string }; void this.request('queryDrop', { binding: owner.binding, requestId: owner.requestId, continuationToken: page.continuationToken, projectionToken: page.projectionToken }).then(() => reject(failure), () => reject(failure)); }
          catch { reject(failure); }
        } else if (operation === 'filterProjection') {
          try { const view = projectionFilterView(result, value as ProjectionFilterSelection); const owner = value as ProjectionFilterSelection; void this.request('queryDrop', { binding: owner.binding, requestId: owner.requestId, continuationToken: null, projectionToken: view.projectionToken }).then(() => reject(failure), () => reject(failure)); } catch { reject(failure); }
        } else reject(failure);
      }, reject, cleanup: () => signal?.removeEventListener('abort', abort) });
      try { this.worker.postMessage({ id, operation, value, ...(cancel ? { cancel } : {}) }, transfer); } catch { this.fail(new ImportError('worker-failed', 'Import worker dispatch failed.')); }
    });
  }
  /**
   * Transfer the selected source and archive descriptors once into this candidate.
   * @param input Main-bound source revisions, file stamps and owned native handles.
   * @param materialAvailable Named read-only companion capability, not a path operation.
   * @param signal Optional candidate cancellation.
   * @param progress Bounded candidate progress observer.
   * @returns Sealed metadata only; graph and parsing data remain worker-local.
   */
  async importDirect(input: DirectWorkerInput, materialAvailable: MaterialAvailability, signal?: AbortSignal, progress?: (value: ImportProgress) => void): Promise<ModelReady> {
    this.progress = progress ? value => { if (!signal?.aborted) progress(value); } : null; this.material = materialAvailable; this.materialSources = new Set(input.files.map(file => file.revision.sourceId));
    try { return await this.request('directImport', input, signal, input.files.flatMap(file => [file.sourceHandle, file.archiveHandle])) as ModelReady; }
    finally { this.material = null; this.materialSources.clear(); this.progress = null; this.directRequestId = null; }
  }
  /** Initialize the candidate; @param input Exact bound captured metadata. */
  async initialize(input: ModelInput): Promise<void> { await this.request('initialize', input); }
  /** Consume one helper frame; @param chunk Untrusted bounded canonical facts. */
  async consume(chunk: unknown): Promise<void> { await this.request('consume', chunk); }
  /** Seal the model without copying graph arrays back to main. */
  async finish(): Promise<ModelReady> { const value = await this.request('finish', null) as ModelReady; assertSnapshot(value.descriptor); return value; }
  /**
   * Resolve one accepted locator without reading a live source path.
   * @param sourceId Captured source ID.
   * @param pointer Exact source pointer.
   * @param sequence Captured local row sequence.
   * @returns Exact captured span or null.
   */
  async span(sourceId: string, pointer: string, sequence: string | null): Promise<SourceSpan | null> { return await this.request('span', { sourceId, pointer, sequence }) as SourceSpan | null; }
  /** Execute a current snapshot query; cancellation sets an atomic flag without terminating the worker. */
  async queryStart(request: GraphRequest, signal?: AbortSignal): Promise<QueryPage> { return await this.request('queryStart', request, signal) as QueryPage; }
  /** Search findings through the fixed worker route without widening the S04 operation set. */
  async searchFindings(request: Extract<GraphRequest, { operation: 'search.page' }>, signal?: AbortSignal): Promise<QueryPage> { return await this.request('searchFindings', request, signal) as QueryPage; }
  /** Filter a bounded projection while preserving exact generation and token ownership. */
  async filterProjection(input: ProjectionFilterSelection, signal?: AbortSignal): Promise<ProjectionFilterView> { return projectionFilterView(await this.request('filterProjection', input, signal), input); }
  /** Pull a finite-progress frame for an exact retained request. */
  async queryNext(input: QueryContinuation, signal?: AbortSignal): Promise<QueryPage> { return await this.request('queryNext', input, signal) as QueryPage; }
  /** Revoke worker-local continuation/projection ownership. */
  async queryDrop(input: QueryDrop): Promise<void> { await this.request('queryDrop', input); }
  /** Compute numeric coordinates on an existing bounded worker-local projection. */
  async layout(input: LayoutSelection, signal?: AbortSignal): Promise<LayoutWireResult> { return await this.request('layout', input, signal) as LayoutWireResult; }
  /** Obtain deterministic facets under the current indexed filter. */
  async groups(input: GroupSelection, signal?: AbortSignal): Promise<GraphGroups> { return await this.request('groups', input, signal) as GraphGroups; }
  /** Stop this worker and reject its outstanding request; repeated calls are safe. */
  async terminate(): Promise<void> { if (!this.stopped) { this.stopped = true; for (const pending of this.pending.values()) { pending.cleanup(); pending.reject(new ImportError('cancelled', 'Import worker cancelled.')); } this.pending.clear(); } await this.worker.terminate(); }
}
