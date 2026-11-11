// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Single-pass admitted-handle reads tee exact bytes to an owned archive and feed a worker-local model. */
import { createHash } from 'node:crypto';
import type { Verification } from '@jai/fabric-explorer-contracts';
import type { CanonicalFact, SourceCompatibility, ReaderDiagnostic } from '../broker/semantic-types.js';
import { parseRecordedJSON } from './recorded-json.js';
import { RecordedProjection } from './recorded-projection.js';
import type { RecordedControl } from './recorded-projection.js';
import { ImportError } from './types.js';

/** Owned read boundary; production supplies a transferred admitted FileHandle. */
export interface RecordedReadHandle { read(buffer: Buffer, offset: number, length: number, position: number): Promise<{ bytesRead: number }> }
/** Owned write boundary; production supplies only its newly allocated archive FileHandle. */
export interface RecordedWriteHandle { write(buffer: Buffer, offset: number, length: number, position: number): Promise<{ bytesWritten: number }> }
/** Source paths are deliberately absent; only opaque metadata and already admitted capabilities enter. */
export interface RecordedInput { readonly sourceId: string; readonly family: 'fabric' | 'findings' | 'audit'; readonly byteLength: number; readonly sourceHandle: RecordedReadHandle; readonly archiveHandle: RecordedWriteHandle }
/** Final captured-byte observation merged into the main owner's immutable source namespace. */
export interface RecordedObservation { readonly sourceId: string; readonly family: 'fabric' | 'findings' | 'audit'; readonly byteLength: string; readonly digest: string; readonly head: string | null; readonly sequence: string; readonly adapterVersion: string; readonly compatibility: SourceCompatibility; readonly verification: Verification }
/** Worker cancellation/material capability callbacks; no arbitrary filesystem operation is exposed. */
export type RecordedImportControl = RecordedControl;
const TOTAL = 1024 * 1024 * 1024; const RECORD = 100 * 1024 * 1024; const READ = 256 * 1024;
const verification: Verification = Object.freeze({ mode: 'recorded', decoded: 'decoded', chain: 'unknown', replay: 'recorded', publicTrust: 'unknown', material: 'not-observed', recordedApplicability: null, authorityGranted: false, freshAssessment: false });

/** Source-bound fixed-category failure; no native exception text or source values are serialized. */
export class RecordedReadError extends ImportError {
  readonly diagnostic: ReaderDiagnostic;
  readonly compatibility: readonly SourceCompatibility[];
  /**
   * Bind an authored failure to metadata already observed by the source projection.
   * @param failure Fixed application failure category/message.
   * @param sourceId Admitted opaque source ID.
   * @param context Bounded prior format/sequence observations; never reparsed input.
   */
  constructor(failure: ImportError, sourceId: string, context: { sequence: string | null; compatibility: readonly SourceCompatibility[] }) {
    super(failure.code, failure.message); this.name = 'RecordedReadError';
    const code = ['cancelled', 'incompatible-source', 'read-failed', 'resource-limit'].includes(failure.code) ? failure.code as ReaderDiagnostic['code'] : 'read-failed';
    this.diagnostic = { code, message: failure.message, sourceId, pointer: '', sequence: context.sequence }; this.compatibility = context.compatibility;
  }
}

/** Bounded row-fragment owner; a failed instance is discarded with its candidate. */
export class RecordedRowFramer {
  private pieces: Buffer[] = []; private size = 0; private start = 0; private pendingCR = false;
  /**
   * Bind the physical-row consumer and an app-owned body limit.
   * @param emit Synchronous row consumer; body excludes LF/CR/CRLF while span includes it.
   * @param maximum Trusted reduced test/application ceiling, never above the maintained100MiB body bound.
   * @throws {ImportError} For an invalid or enlarged ceiling.
   */
  constructor(private readonly emit: (body: Buffer, offset: number, span: number) => void, private readonly maximum = RECORD) {
    if (!Number.isSafeInteger(maximum) || maximum < 1 || maximum > RECORD) throw new ImportError('resource-limit', 'Invalid source row limit.');
  }
  private append(part: Buffer): void { this.size += part.length; if (this.size > this.maximum + 2) throw new ImportError('resource-limit', 'Selected source row exceeds its body limit.'); this.pieces.push(part); }
  private flush(): void {
    const row = this.pieces.length === 1 ? this.pieces[0]! : Buffer.concat(this.pieces, this.size); let body = row.length;
    if (row[body - 1] === 10) body--; if (row[body - 1] === 13) body--;
    if (body > this.maximum) throw new ImportError('resource-limit', 'Selected source row exceeds its body limit.');
    this.emit(row.subarray(0, body), this.start, this.size); this.start += this.size; this.size = 0; this.pieces = []; this.pendingCR = false;
  }
  /**
   * Retain immutable fragments and emit complete rows without repeated concatenation.
   * @param chunk A read buffer that its owner will not overwrite after this call.
   * @throws {ImportError} If the current physical row cannot fit the fixed body/terminator budget.
   */
  push(chunk: Buffer): void {
    if (!chunk.length) return;
    let start = 0;
    if (this.pendingCR) { if (chunk[0] === 10) { this.append(chunk.subarray(0, 1)); start = 1; } this.flush(); }
    while (start < chunk.length) {
      const lf = chunk.indexOf(10, start); const cr = chunk.indexOf(13, start); const end = lf < 0 ? cr : cr < 0 ? lf : Math.min(lf, cr);
      if (end < 0) { this.append(chunk.subarray(start)); break; }
      if (chunk[end] === 13 && end + 1 === chunk.length) { this.append(chunk.subarray(start)); this.pendingCR = true; break; }
      const through = end + (chunk[end] === 13 && chunk[end + 1] === 10 ? 2 : 1);
      this.append(chunk.subarray(start, through)); this.flush(); start = through;
    }
  }
  /** Emit a final complete unterminated row, if present; malformed JSON remains the consumer's failure. */
  finish(): void { if (this.size) this.flush(); }
}

/**
 * Stream selected sources once, preserve exact archived bytes and map generated facts in the same worker.
 * @param inputs Selected admitted read handles and owned archive outputs, without paths.
 * @param sink Synchronous compact-model insertion with cumulative fact/graph accounting.
 * @param control Cancellation and main-owned companion readability port.
 * @returns Final byte/projection observations; caller finalizes metadata before model seal.
 * @throws {ImportError} For unreadable data, limits, cancellation or I/O failure. Caller closes every handle in finally.
 */
export async function importRecordedSources(inputs: readonly RecordedInput[], sink: (fact: CanonicalFact) => void, control: RecordedImportControl): Promise<readonly RecordedObservation[]> {
  if (!inputs.length || inputs.length > 128 || new Set(inputs.map(input => input.sourceId)).size !== inputs.length || inputs.some(input => !Number.isSafeInteger(input.byteLength) || input.byteLength < 0) || inputs.reduce((sum, input) => sum + input.byteLength, 0) > TOTAL) throw new ImportError('resource-limit', 'Selected source bytes exceed their resource limit.');
  const observations: RecordedObservation[] = [];
  const totalBytes = inputs.reduce((sum, input) => sum + input.byteLength, 0); let completedBytes = 0; let records = 0; let factsProcessed = 0;
  const currentProgress = { phase: 'processing' as const, bytesRead: 0, totalBytes, records: 0, factsProcessed: 0, sourcesCompleted: 0, totalSources: inputs.length };
  const progress = () => { if (!control.progress) return; currentProgress.bytesRead = completedBytes; currentProgress.records = records; currentProgress.factsProcessed = factsProcessed; currentProgress.sourcesCompleted = observations.length; control.progress(currentProgress); };
  const cancelled = (): void => { if (control.cancelled()) throw new ImportError('cancelled', 'Recorded import cancelled.'); };
  for (const input of inputs) {
    cancelled();
    if (input.family === 'audit') throw new RecordedReadError(new ImportError('incompatible-source', 'The optional audit adapter is unavailable in this build.'), input.sourceId, { sequence: null, compatibility: [{ sourceId: input.sourceId, family: 'audit', declaredFormat: null, declaredProtocol: null, supported: false, adapterVersion: 'jai.fabric-explorer.audit/2' }] });
    const projection = new RecordedProjection(input.sourceId, input.family); const digest = createHash('sha256'); const decoder = new TextDecoder('utf-8', { fatal: true });
    let position = 0; let rowOrdinal = 0; let activeSequence: string | null = null; let activePointer = '';
    const framer = new RecordedRowFramer((body, offset, span) => { cancelled(); activeSequence = String(++rowOrdinal); records++; projection.consume(parseRecordedJSON(decoder.decode(body), input.family), offset, span); activeSequence = null; });
    try {
      while (position < input.byteLength) {
        cancelled();
        // Each read has its own buffer: retained row fragments never alias a
        // buffer overwritten by the next read. Each completed row concatenates once.
        const buffer = Buffer.allocUnsafe(Math.min(READ, input.byteLength - position));
        const { bytesRead } = await input.sourceHandle.read(buffer, 0, buffer.length, position);
        if (!Number.isSafeInteger(bytesRead) || bytesRead < 1 || bytesRead > buffer.length) throw new ImportError('read-failed', 'Selected source changed during capture.');
        const chunk = buffer.subarray(0, bytesRead); digest.update(chunk);
        let written = 0;
        while (written < bytesRead) { cancelled(); const result = await input.archiveHandle.write(chunk, written, bytesRead - written, position + written); if (!Number.isSafeInteger(result.bytesWritten) || result.bytesWritten < 1 || result.bytesWritten > bytesRead - written) throw new ImportError('read-failed', 'Private archive write was incomplete.'); written += result.bytesWritten; }
        position += bytesRead; completedBytes += bytesRead; framer.push(chunk); progress();
      }
      framer.finish();
      cancelled();
      for await (const fact of projection.facts(control)) { cancelled(); activeSequence = fact.origin.sequence; activePointer = fact.origin.pointer; sink(fact); factsProcessed++; progress(); activeSequence = null; activePointer = ''; }
      const summary = projection.summary();
      observations.push({ sourceId: input.sourceId, family: input.family, byteLength: String(position), digest: digest.digest('hex'), head: summary.head, sequence: summary.sequence, adapterVersion: summary.compatibility.adapterVersion, compatibility: summary.compatibility, verification }); progress();
    } catch (error) { const failure = error instanceof ImportError ? error : new ImportError('read-failed', 'The selected source or private archive could not be read.'); const wrapped = new RecordedReadError(failure, input.sourceId, { ...projection.failureContext(), sequence: activeSequence }); if (activePointer) Object.assign(wrapped.diagnostic, { pointer: activePointer }); throw wrapped; }
  }
  return observations;
}
