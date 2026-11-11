/** Main-only native descriptors; these capabilities never cross the renderer bridge. */
import type { FileHandle } from 'node:fs/promises';
import type { AdmittedSource, SourceRevision } from '@jai/fabric-explorer-contracts';
/** Exact file identity and capture markers, represented losslessly across worker messages. */
export interface NativeFileStamp { readonly device: string; readonly inode: string; readonly size: string; readonly modified: string; readonly changed: string }
/** One owned source capture, to be transferred exactly once to a candidate worker. */
export interface DirectSourceFile { readonly admitted: AdmittedSource; readonly revisionId: string; readonly observedAt: string; readonly stamp: NativeFileStamp; readonly handle: FileHandle }
/** Main owns the selection; transferred descriptors belong to the candidate worker. */
export interface DirectCapture {
  readonly files: readonly DirectSourceFile[];
  /** Revalidate the admitted source identities and capture markers before publication. */
  validate(): Promise<void>;
  /** Close descriptors still owned here; transferred handles are already detached. */
  dispose(): Promise<void>;
  /** Observe companion readability without granting arbitrary path access. */
  materialAvailable(sourceId: string, blobId: string): Promise<'available' | 'missing' | 'unknown'>;
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

/** Private draft: revision identity is fixed before bytes, final content observations bind before seal.
 * @param source Owned selected-file capture with fixed revision identity.
 */
export function draftDirectRevision(source: DirectSourceFile): SourceRevision {
  return { revisionId: source.revisionId, projectId: source.admitted.projectId, rootId: source.admitted.rootId, sourceId: source.admitted.sourceId, family: source.admitted.family, relativePath: source.admitted.relativePath, adapterVersion: `jai.fabric-explorer.${source.admitted.family}/2`, byteLength: source.stamp.size, digest: '0'.repeat(64), head: null, sequence: null, observedAt: source.observedAt, verification: { mode: 'recorded', decoded: 'decoded', chain: 'unknown', replay: 'recorded', publicTrust: 'unknown', material: 'not-observed', recordedApplicability: null, authorityGranted: false, freshAssessment: false } };
}
