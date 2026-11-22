/** Main-only native descriptors; these capabilities never cross the renderer bridge. */
import type { FileHandle } from 'node:fs/promises';
import type { AdmittedSource, SourceRevision } from '@jai/fabric-explorer-contracts';
/** Exact file identity and capture markers, represented losslessly across worker messages. */
export interface NativeFileStamp { readonly device: string; readonly inode: string; readonly size: string; readonly modified: string; readonly changed: string }
/** One owned source capture, to be transferred exactly once to a candidate worker. */
export interface DirectSourceFile { readonly admitted: AdmittedSource; readonly revisionId: string; readonly observedAt: string; readonly stamp: NativeFileStamp; readonly handle: FileHandle }
/** Main-owned observation of a companion examined during label derivation. */
export interface CompanionObservation {
  readonly sourceId: string;
  readonly blobId: string;
  readonly state: NativeFileStamp | 'missing' | 'read-denied';
}
/** Main owns the selection; transferred descriptors belong to the candidate worker. */
export interface DirectCapture {
  readonly files: readonly DirectSourceFile[];
  /** Revalidate the admitted source identities and capture markers before publication. */
  validate(): Promise<void>;
  /** Return detached companion dependencies observed by this candidate. */
  companionObservations(): readonly CompanionObservation[];
  /** Recheck exact companion access and file markers without reading payloads. */
  companionsUnchanged(previous: readonly CompanionObservation[]): Promise<boolean>;
  /** Close descriptors still owned here; transferred handles are already detached. */
  dispose(): Promise<void>;
  /** Observe companion readability without granting arbitrary path access. */
  materialAvailable(sourceId: string, blobId: string): Promise<'available' | 'missing' | 'unknown'>;
  /** Read one exact admitted companion designated as record text by the projection. */
  materialExcerpt?: MaterialExcerpt;
}
/** Serializable metadata matching source handles transferred separately. */
export interface DirectWorkerSource { readonly revision: SourceRevision; readonly stamp: NativeFileStamp; readonly sourceHandle: FileHandle; readonly archiveHandle: FileHandle }
/** Allocate the existing archive once, let the worker write it, then adopt the same files. */
export interface DirectArchiveStage {
  readonly outputs: ReadonlyMap<string, FileHandle>;
  /** Open immutable read handles after the writer worker has closed its handles. */
  adopt(sources: readonly SourceRevision[]): Promise<import('./semantic-types.js').CapturedSources>;
  /** Remove only this stage after its writer is stopped. */
  dispose(): Promise<void>;
}
/** Candidate worker call; handles are transferred, all other fields remain bounded metadata. */
export interface DirectWorkerInput {
  readonly binding: import('@jai/fabric-explorer-contracts').Binding;
  readonly generation: string;
  readonly files: readonly DirectWorkerSource[];
  readonly limits: import('../import/types.js').ImportLimits;
}
/** Named main-owned companion readability callback, never a path or general filesystem operation. */
export interface MaterialAvailability { (sourceId: string, blobId: string): Promise<'available' | 'missing' | 'unknown'> }
/** Exact source-bound attachment designation from a recorded version. */
export interface ExcerptRequest { readonly sourceId: string; readonly blobId: string; readonly versionId: string; readonly byteLength: number; readonly media: 'text/plain' | 'text/markdown'; readonly rowOffset: number; readonly rowLength: number; readonly effectIndex: number }
/** Fixed companion read limits in bytes. */
export const EXCERPT_LIMIT = 16 * 1024;
/** Maximum bytes attempted across one captured candidate import. */
export const IMPORT_EXCERPT_LIMIT = 1024 * 1024;
/** Closed reason vocabulary for a companion that could not supply display text. */
export type ExcerptFailure = 'missing' | 'read-denied' | 'oversized' | 'digest-mismatch' | 'invalid-utf8' | 'import-budget-exhausted';
/** A result contains exact decoded text or a redacted failure reason. */
export type ExcerptResult = { readonly kind: 'text'; readonly text: string } | { readonly kind: ExcerptFailure };
/** Candidate-only companion content callback. */
export interface MaterialExcerpt { (request: ExcerptRequest): Promise<ExcerptResult> }

/** Private draft: revision identity is fixed before bytes, final content observations bind before seal.
 * @param source Owned selected-file capture with fixed revision identity.
 */
export function draftDirectRevision(source: DirectSourceFile): SourceRevision {
  return { revisionId: source.revisionId, projectId: source.admitted.projectId, rootId: source.admitted.rootId, sourceId: source.admitted.sourceId, family: source.admitted.family, relativePath: source.admitted.relativePath, adapterVersion: `jai.fabric-explorer.${source.admitted.family}/2`, byteLength: source.stamp.size, digest: '0'.repeat(64), head: null, sequence: null, observedAt: source.observedAt, verification: { mode: 'recorded', decoded: 'decoded', chain: 'unknown', replay: 'recorded', publicTrust: 'unknown', material: 'not-observed', recordedApplicability: null, authorityGranted: false, freshAssessment: false } };
}
