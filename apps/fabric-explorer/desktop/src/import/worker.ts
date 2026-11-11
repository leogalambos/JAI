// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Fixed application worker entry; main supplies recorded-source facts, never executable project code. */
import { parentPort } from 'node:worker_threads';
import { encodeWire } from '@jai/fabric-explorer-contracts';
import { ImportProgressReporter } from './progress.js';
import { ImportModel } from './model.js';
import { buildDirectModel } from './direct-import.js';
import type { DirectWorkerInput } from '../broker/direct-types.js';
import type { ModelInput } from './model.js';
import { ImportError } from './types.js';
import { encodeLayout } from '../explore/layout-wire.js';
import { ExploreService } from '../explore/service.js';
import { QueryIndex } from '../graph/query-index.js';
import type { GraphRequest } from '../graph/types.js';
import type { QueryContinuation, QueryDrop, LayoutSelection, GroupSelection, ProjectionFilterSelection } from '../explore/types.js';
const port = parentPort;
if (!port) throw new Error('Import worker requires a parent channel.');
let model: ImportModel | null = null;
let sequence = 0;
let explore: ExploreService | null = null;
let binding: ModelInput['binding'] | null = null;
let materialId = 0;
const materialCalls = new Map<number, (value: 'available' | 'missing' | 'unknown') => void>();
port.on('message', async (input: unknown) => {
  let id = 0;
  try {
    if (!input || typeof input !== 'object' || Array.isArray(input)) throw new ImportError('invalid-model', 'Invalid worker request.');
    const material = input as { kind?: string; id?: number; availability?: string };
    if (material.kind === 'materialResult') {
      if (Object.keys(input).sort().join() !== 'availability,id,kind' || !Number.isSafeInteger(material.id) || !['available', 'missing', 'unknown'].includes(material.availability ?? '')) throw new ImportError('invalid-model', 'Invalid companion observation.');
      const done = materialCalls.get(material.id!); if (!done) throw new ImportError('invalid-model', 'Unknown companion observation.'); materialCalls.delete(material.id!); done(material.availability as 'available' | 'missing' | 'unknown'); return;
    }
    const message = input as { id: number; operation: string; value: unknown; cancel?: SharedArrayBuffer };
    const keys = Object.keys(message).sort().join();
    if (keys !== 'id,operation,value' && keys !== 'cancel,id,operation,value') throw new ImportError('invalid-model', 'Invalid worker envelope.');
    if (message.cancel !== undefined && (!(message.cancel instanceof SharedArrayBuffer) || message.cancel.byteLength !== 4)) throw new ImportError('invalid-model', 'Invalid worker cancellation flag.');
    if (message.operation === 'directImport') { const direct = message.value as DirectWorkerInput; if (!direct || !Array.isArray(direct.files) || direct.files.length > 128) throw new ImportError('invalid-model', 'Invalid direct sources.'); encodeWire({ id: message.id, operation: message.operation, value: { binding: direct.binding, generation: direct.generation, limits: direct.limits, files: direct.files.map(file => ({ revision: file.revision, stamp: file.stamp })) } }); } else encodeWire({ id: message.id, operation: message.operation, value: message.value });
    const flag = message.cancel ? new Int32Array(message.cancel) : null;
    const control = { cancelled: () => flag !== null && Atomics.load(flag, 0) !== 0 };
    id = message.id;
    if (id !== sequence + 1) throw new ImportError('invalid-model', 'Invalid worker request order.'); sequence = id;
    let value: unknown = null;
    if (message.operation === 'directImport') {
      if (model) throw new ImportError('invalid-model', 'Worker is already initialized.');
      const direct = message.value as DirectWorkerInput; binding = direct.binding;
      const progress = new ImportProgressReporter(direct.files.reduce((sum, file) => sum + Number(file.revision.byteLength), 0), direct.files.length, value => { if (!control.cancelled()) port.postMessage({ kind: 'importProgress', id, value }); });
      const result = await buildDirectModel(direct, { ...control, progress: value => progress.update(value), materialAvailable: (sourceId, blobId) => new Promise(resolve => { const id = ++materialId; materialCalls.set(id, resolve); port.postMessage({ kind: 'materialAvailability', id, sourceId, blobId }); }) });
      model = result.model; explore = new ExploreService(new QueryIndex({ snapshot: result.ready.descriptor, store: model.graph() }, { ...binding!, generation: result.ready.descriptor.generation }), { ...binding!, generation: result.ready.descriptor.generation }); value = result.ready; progress.complete();
    } else if (message.operation === 'initialize') { if (model) throw new ImportError('invalid-model', 'Worker is already initialized.'); model = new ImportModel(message.value as ModelInput); binding = (message.value as ModelInput).binding; }
    else {
      if (!model) throw new ImportError('invalid-model', 'Worker is not initialized.');
      if (message.operation === 'consume') model.consume(message.value);
      else if (message.operation === 'finish') { if (message.value !== null) throw new ImportError('invalid-model', 'Invalid finish request.'); const ready = model.finish(); if (!explore) explore = new ExploreService(new QueryIndex({ snapshot: ready.descriptor, store: model.graph() }, { ...binding!, generation: ready.descriptor.generation }), { ...binding!, generation: ready.descriptor.generation }); value = ready; }
      else if (message.operation === 'span') { const locator = message.value as { sourceId: string; pointer: string; sequence: string | null }; if (!locator || Object.keys(locator).sort().join() !== 'pointer,sequence,sourceId') throw new ImportError('invalid-model', 'Invalid source locator.'); value = model.span(locator.sourceId, locator.pointer, locator.sequence); }
      else if (explore && message.operation === 'queryStart') value = explore.start(message.value as GraphRequest, control);
      else if (explore && message.operation === 'searchFindings') value = explore.start(message.value as GraphRequest, control, 'findings');
      else if (explore && message.operation === 'filterProjection') value = explore.filterProjection(message.value as ProjectionFilterSelection, control);
      else if (explore && message.operation === 'queryNext') value = explore.next(message.value as QueryContinuation, control);
      else if (explore && message.operation === 'queryDrop') explore.drop(message.value as QueryDrop);
      else if (explore && message.operation === 'layout') value = encodeLayout(await explore.layout(message.value as LayoutSelection, control));
      else if (explore && message.operation === 'groups') value = explore.groups(message.value as GroupSelection, control);
      else throw new ImportError('invalid-model', 'Unknown worker operation.');
    }
    port.postMessage({ id, ok: true, value });
  } catch (error) {
    // Transfer ownership begins at receipt, even when envelope validation rejects before parsing.
    const direct = input as { operation?: unknown; value?: { files?: unknown } } | null;
    if (direct?.operation === 'directImport' && Array.isArray(direct.value?.files)) {
      const handles = new Set<import('node:fs/promises').FileHandle>();
      for (const file of direct.value.files) if (file && typeof file === 'object') {
        for (const handle of [file.sourceHandle, file.archiveHandle]) if (handle && typeof handle.close === 'function') handles.add(handle);
      }
      await Promise.allSettled([...handles].map(handle => handle.close()));
    }
    port.postMessage({ id, ok: false, value: { code: error && typeof error === 'object' && 'code' in error && typeof error.code === 'string' ? error.code : 'invalid-model', message: 'Import candidate rejected.', report: error instanceof ImportError ? error.report : null } }); }
});
