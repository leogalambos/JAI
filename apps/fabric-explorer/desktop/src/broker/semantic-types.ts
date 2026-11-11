/** App-owned canonical helper wire and immutable capture ports; not renderer authority. */
import type { BytePage, Digest, FindingKind, FindingState, Ownership, Participant, RecordFamily, SemanticValue, Severity, SourceFamily, SourceReference, SourceRevision } from '@jai/fabric-explorer-contracts';

/** Exact originating row span and record pointer in one immutable captured source. */
export interface FactOrigin { readonly pointer: string; readonly sequence: string | null; readonly byteOffset: string; readonly byteLength: string }
/** Complete inspector fields inline or retained at the exact captured record locator. */
export type FactAttributes = { readonly kind: 'inline'; readonly value: SemanticValue } | { readonly kind: 'paged'; readonly byteLength: string; readonly mediaType: string };
/** Exact canonical use point; origin reference scope and selected use scope remain distinct. */
export interface CanonicalPoint { readonly ref: SourceReference; readonly use_scope: string }
/** Common helper provenance; namespaces/revisions are supplied by the owning capture lease. */
export interface FactBase { readonly sourceId: string; readonly origin: FactOrigin }
/** Versioned semantic facts from canonical replay, with no JavaScript replay or scope inference. */
export type CanonicalFact = FactBase & (
  | { readonly kind: 'version'; readonly ref: SourceReference; readonly family: RecordFamily; readonly label: string; readonly attributes: FactAttributes }
  | { readonly kind: 'use'; readonly point: CanonicalPoint; readonly state: SemanticValue }
  | { readonly kind: 'reference'; readonly originRef: SourceReference; readonly originUseScope: string | null; readonly fieldPointer: string; readonly occurrence: number; readonly targetRef: SourceReference; readonly targetUseScope: string | null; readonly historicalCausal: boolean; readonly governing: boolean; readonly dependencyBasis: 'historical' | 'association' }
  | { readonly kind: 'governing-dependency'; readonly originPoint: CanonicalPoint; readonly prerequisitePoint: CanonicalPoint; readonly occurrence: number; readonly dependencyBasis: 'governing' }
  | { readonly kind: 'participant'; readonly originRef: SourceReference; readonly participant: Participant; readonly fieldPointer: string }
  | { readonly kind: 'ownership'; readonly originRef: SourceReference; readonly owner: Ownership }
  | { readonly kind: 'material'; readonly originRef: SourceReference; readonly blobId: Digest; readonly availability: 'available' | 'missing' | 'unknown'; readonly fieldPointer: string }
  | { readonly kind: 'decision-effect'; readonly decisionRef: SourceReference; readonly effectKind: string; readonly targetPoint: CanonicalPoint | null; readonly effect: SemanticValue; readonly occurrence: number }
  | { readonly kind: 'finding'; readonly findingId: string; readonly state: FindingState; readonly severity: Severity; readonly findingKind: FindingKind; readonly rounds: string; readonly recordedExpiry: string | null; readonly label: string; readonly target: string | null; readonly location: string | null; readonly attributes: FactAttributes; readonly effectiveMaxRounds: number; readonly historicalMaxRoundsKnown: false }
  | { readonly kind: 'audit'; readonly attributes: FactAttributes }
);
/** Source compatibility observation, never an invented findings schema version. */
export interface SourceCompatibility { readonly sourceId: string; readonly family: SourceFamily; readonly declaredFormat: string | null; readonly declaredProtocol: string | null; readonly supported: boolean; readonly adapterVersion: string }
/** Value-redacted import diagnostic; source IDs and exact relative pointers are safe provenance. */
export interface ReaderDiagnostic { readonly code: 'incompatible-source' | 'read-failed' | 'resource-limit' | 'cancelled' | 'missing-public-trust' | 'missing-material' | 'source-changed' | 'helper-failed'; readonly message: string; readonly sourceId: string | null; readonly pointer: string; readonly sequence: string | null }
/** Exact selected-source import outcome; failed candidates are never partly publishable. */
export interface ImportReport { readonly selected: string; readonly accepted: string; readonly rejected: string; readonly skipped: string; readonly diagnostics: readonly ReaderDiagnostic[]; readonly diagnosticTotal: string }
/** Contiguous bounded pull chunk; null next is terminal, never a partial-success indicator. */
export interface SemanticFactChunk { readonly sequence: string; readonly facts: readonly CanonicalFact[]; readonly next: string | null }
/** Main-owned immutable byte archive, independent of helper/worker lifetime. */
export interface CapturedSources {
  /**
   * Read one bounded page from an exact archived revision.
   * @param sourceId Source in this captured set.
   * @param offset Unsigned decimal byte offset.
   * @param length Requested bytes, 1..256 KiB.
   * @returns Exact bytes and captured EOF; caller supplies semantic pointer/sequence.
   * @throws {Error} For foreign source, invalid bounds, disposed archive or changed cache.
   */
  page(sourceId: string, offset: string, length: number): Promise<BytePage>;
  /** Release only this archive's owned files and native handles idempotently. */
  dispose(): Promise<void>;
}
/** Helper-owned immutable candidate; persist raw bytes before publishing a worker snapshot. */
export interface SemanticLease {
  readonly leaseId: string;
  readonly sources: readonly SourceRevision[];
  readonly compatibility: readonly SourceCompatibility[];
  readonly report: ImportReport;
  /**
   * Pull the next ordered canonical fact frame.
   * @param cursor Null for first frame, then exact opaque next token from prior frame.
   * @param signal Optional candidate cancellation.
   * @returns A contiguous bounded fact frame.
   * @throws {Error} For stale/foreign cursor, helper failure or cancellation.
   */
  chunk(cursor: string | null, signal?: AbortSignal): Promise<SemanticFactChunk>;
  /**
   * Persist exact source bytes into an independent main-owned bounded disk archive.
   * @param signal Optional cancellation; partial owned files are removed on failure.
   * @returns Archive surviving this helper lease's release or helper termination.
   * @throws {Error} For limits, changed capture, digest mismatch, cancellation or storage failure.
   */
  persist(signal?: AbortSignal): Promise<CapturedSources>;
  /** Release helper-native candidate resources; a persisted archive remains owned by its caller. */
  release(): Promise<void>;
}
/** Trusted staging limits; changing them never bypasses source or transport guardrails. */
export interface SemanticLimits { readonly maxVertices: number; readonly maxEdges: number; readonly maxEncodedGraphBytes: number }
/** Main-only semantic acquisition; no renderer path or caller authority callback exists. */
export interface SemanticBrokerPort {
  /**
   * Capture and canonically interpret selected admitted sources as one observed revision set.
   * @param sessionId Trusted owner.
   * @param capability Active broker source-selection handle.
   * @param sourceIds Explicit subset of the admitted source catalog.
   * @param signal Optional cancellation of candidate work.
   * @returns A helper-owned lease; prior published snapshots remain independent.
   * @throws {Error} For failed source verification, limits, ownership, helper failure or cancellation.
   */
  capture(sessionId: string, capability: string, sourceIds: readonly string[], signal?: AbortSignal): Promise<SemanticLease>;
}
