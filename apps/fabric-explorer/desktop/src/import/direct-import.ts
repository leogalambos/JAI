/** Worker-local streaming import; source bytes and facts never pass through a helper process. */
import { assertSnapshot, type SourceRevision } from '@jai/fabric-explorer-contracts';
import type { DirectSourceFile, DirectWorkerInput, MaterialAvailability } from '../broker/direct-types.js';
import { nativeFileStamp, sameFileStamp } from '../broker/read-broker.js';
import { importRecordedSources, RecordedReadError } from './recorded-import.js';
export { draftDirectRevision } from '../broker/direct-types.js';
import { ImportModel, type ModelReady } from './model.js';
import { ImportError, type ImportReport } from './types.js';
import { captureReport, readerFailureReport } from './report.js';
/** Cancellation/material boundary supplied by the actual candidate worker owner. */
export interface DirectImportControl { progress?(value: import('./progress.js').ImportProgress): void; cancelled(): boolean; materialAvailable?: MaterialAvailability }
/**
 * Build one candidate from owned descriptors and leave only a sealed compact model.
 * @param input Main-bound identities, private output handles and unchanged logical limits.
 * @param control Candidate cancellation and named companion readability capability.
 * @returns Worker-local model plus bounded ready metadata; all transferred descriptors are closed.
 * @throws {ImportError} For changed files, malformed sources, cancellation or existing resource limits.
 */
export async function buildDirectModel(input: DirectWorkerInput, control: DirectImportControl): Promise<{ model: ImportModel; ready: ModelReady }> {
  const check = () => { if (control.cancelled()) throw new ImportError('cancelled', 'Import cancelled.'); };
  const selected = String(input.files.length);
  const report: ImportReport = { status: 'ready', selectedSources: selected, acceptedSources: selected, rejectedSources: '0', vertices: '0', edges: '0', unresolvedVertices: '0', skippedItems: '0', diagnosticTotal: '0', diagnostics: [], supportedVersions: [], observation: 'observed-revision-set', limitation: 'Recorded content is displayed; chain, signature and lifecycle verification was not performed.' };
  try {
    check(); if (!input.files.length || input.files.length > 128 || new Set(input.files.map(file => file.revision.sourceId)).size !== input.files.length) throw new ImportError('invalid-model', 'Invalid direct source set.');
    for (const file of input.files) {
      const info = await file.sourceHandle.stat({ bigint: true });
      if (!info.isFile() || info.nlink !== 1n || !sameFileStamp(nativeFileStamp(info), file.stamp)) throw new ImportError('read-failed', 'Selected source changed before import.');
    }
    const model = new ImportModel({ binding: input.binding, generation: input.generation, sources: input.files.map(file => file.revision), report, limits: input.limits });
    let projectedFacts = 0;
    const materials = new Map<string, Promise<'available' | 'missing' | 'unknown'>>();
    const observations = await importRecordedSources(input.files.map(file => ({ sourceId: file.revision.sourceId, family: file.revision.family, byteLength: Number(file.stamp.size), sourceHandle: file.sourceHandle, archiveHandle: file.archiveHandle })), fact => { check(); model.consumeDirect(fact); projectedFacts++; }, { cancelled: control.cancelled, ...(control.progress ? { progress: control.progress } : {}), materialAvailability: async (sourceId, blobId) => {
      check(); if (!input.files.some(file => file.revision.sourceId === sourceId) || !/^[0-9a-f]{64}$/.test(blobId)) throw new ImportError('invalid-model', 'Invalid companion capability.');
      const key = JSON.stringify([sourceId, blobId]); let value = materials.get(key);
      if (!value) { value = control.materialAvailable?.(sourceId, blobId) ?? Promise.resolve('unknown' as const); materials.set(key, value); }
      return await value;
    } });
    check(); if (observations.length !== input.files.length || new Set(observations.map(item => item.sourceId)).size !== observations.length) throw new ImportError('invalid-model', 'Direct source observations differ.');
    const sources = input.files.map(file => {
      const observed = observations.find(item => item.sourceId === file.revision.sourceId); if (!observed || observed.family !== file.revision.family || observed.byteLength !== file.revision.byteLength || observed.adapterVersion !== file.revision.adapterVersion) throw new ImportError('invalid-model', 'Missing or mismatched direct source observation.');
      return { ...file.revision, digest: observed.digest, head: observed.head, sequence: observed.sequence, adapterVersion: observed.adapterVersion, verification: observed.verification };
    });
    for (const file of input.files) {
      check(); const info = await file.sourceHandle.stat({ bigint: true }); const output = await file.archiveHandle.stat({ bigint: true });
      if (!info.isFile() || info.nlink !== 1n || !sameFileStamp(nativeFileStamp(info), file.stamp) || !output.isFile() || output.nlink !== 1n || output.size !== BigInt(file.stamp.size)) throw new ImportError('read-failed', 'Selected source changed during import.');
    }
    assertSnapshot({ format: 'jai.fabric-explorer.snapshot/1', sessionId: input.binding.sessionId, generation: input.generation, sources, counts: { vertices: '0', edges: '0', findings: '0' }, authorityGranted: false, freshAssessment: false });
    const finalReport = captureReport({ sources, compatibility: observations.map(item => item.compatibility), report: { selected, accepted: selected, rejected: '0', skipped: '0', diagnostics: [], diagnosticTotal: '0' } }, input.binding, sources.map(source => source.sourceId), input.limits);
    model.finalizeSources(sources, finalReport); control.progress?.({ phase: 'indexing', bytesRead: sources.reduce((sum, source) => sum + Number(source.byteLength), 0), totalBytes: sources.reduce((sum, source) => sum + Number(source.byteLength), 0), records: sources.reduce((sum, source) => sum + Number(source.sequence ?? '0'), 0), factsProcessed: projectedFacts, sourcesCompleted: sources.length, totalSources: sources.length }); const ready = model.finish(); return { model, ready };
  } catch (error) {
    if (error instanceof RecordedReadError) {
      const rejected = readerFailureReport({ selected, accepted: '0', rejected: '1', skipped: String(Math.max(0, input.files.length - 1)), diagnostics: [error.diagnostic], diagnosticTotal: '1' }, error.compatibility, input.files.map(file => file.revision.sourceId), input.limits);
      throw new ImportError(error.code, error.message, rejected);
    }
    throw error;
  } finally {
    await Promise.allSettled(input.files.flatMap(file => [file.sourceHandle.close(), file.archiveHandle.close()]));
  }
}
