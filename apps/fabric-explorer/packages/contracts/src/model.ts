/** Read-only projection contracts; successful shape validation never establishes source authority. */

/** Canonical unsigned decimal integer, including zero, without IEEE-754 coercion. */
export type UnsignedDecimal = string;
/** Exact lowercase 256-bit source digest; its domain and verification belong to the canonical reader. */
export type Digest = string;
/** Stable local address generated from an identity tuple, never a source hash. */
export type ElementKey = string;
/** Read-only source families; audit data is a saved projection rather than a full journal. */
export type SourceFamily = 'fabric' | 'findings' | 'audit';
/** Six maintained record families plus the canonical engine's derived decision manifestation. */
export type RecordFamily = 'source' | 'profile' | 'assignment' | 'context' | 'product' | 'assessment' | 'decision';

/** Unambiguous lossless semantic tree; object entry order and exact strings are preserved. */
export type SemanticValue =
  | { readonly type: 'null' }
  | { readonly type: 'boolean'; readonly value: boolean }
  | { readonly type: 'string'; readonly value: string }
  | { readonly type: 'integer'; readonly value: string }
  | { readonly type: 'float64'; readonly bits: string }
  | { readonly type: 'array'; readonly items: readonly SemanticValue[] }
  | { readonly type: 'object'; readonly entries: readonly { readonly key: string; readonly value: SemanticValue }[] };

/** Opaque, explicitly namespaced presentation metadata; no extension grants authority or dispatches code. */
export type Extensions = Readonly<Record<string, SemanticValue>>;

/** Exact canonical reference; origin scope is distinct from a use point's use_scope. */
export interface SourceReference {
  readonly engagement: string;
  readonly scope: string;
  readonly logical_id: string;
  readonly version_id: Digest;
}

/** Canonical participant descriptor, retained as provenance rather than a permission. */
export type Participant =
  | { readonly kind: 'assignment'; readonly ref: SourceReference }
  | { readonly kind: 'authority' | 'controller'; readonly id: string };

/** Canonical ownership tuple, without enterprise identity or authorization inference. */
export type Ownership =
  | { readonly layer: number; readonly work_kind: 'question'; readonly question: 'what' | 'why' | 'how' | 'who' | 'where' | 'when'; readonly work_item: string }
  | { readonly layer: number; readonly work_kind: 'integration' | 'handoff' | 'measurement'; readonly question: null; readonly work_item: string };

/** Stable record address; excludes mutable file head/revision and ephemeral session capabilities. */
export interface StableLocator {
  readonly projectId: string;
  readonly rootId: string;
  readonly sourceId: string;
  readonly family: SourceFamily;
  readonly relativePath: string;
  readonly pointer: string;
  readonly sequence: UnsignedDecimal | null;
}

/** Revision-bearing provenance pointing into the snapshot's exact observed source revision set. */
export interface SourceLocator extends StableLocator {
  readonly revisionId: string;
  readonly adapterVersion: string;
}

/** Full source fields inline or by explicit bounded-paging descriptor; no silent field dropping. */
export type Attributes =
  | { readonly kind: 'inline'; readonly value: SemanticValue }
  | { readonly kind: 'paged'; readonly source: SourceLocator; readonly byteLength: UnsignedDecimal; readonly mediaType: string };

/** Renderer-independent stable vertex identity; labels and source heads never participate. */
export type ElementIdentity =
  | { readonly kind: 'version'; readonly projectId: string; readonly ref: SourceReference }
  | { readonly kind: 'use'; readonly projectId: string; readonly ref: SourceReference; readonly useScope: string }
  | { readonly kind: 'finding'; readonly projectId: string; readonly ledgerId: string; readonly findingId: string }
  | { readonly kind: 'blob'; readonly projectId: string; readonly rootId: string; readonly blobId: Digest }
  | { readonly kind: 'participant'; readonly projectId: string; readonly participant: Participant }
  | { readonly kind: 'ownership'; readonly projectId: string; readonly owner: Ownership }
  | { readonly kind: 'location'; readonly projectId: string; readonly origin: StableLocator; readonly text: string };

/** Exact edge address; immutable origin and endpoints prevent version/use-point rebinding. */
export type EdgeIdentity =
  | { readonly kind: 'explicit'; readonly projectId: string; readonly origin: ElementIdentity; readonly sourceEdgeId: string; readonly from: ElementIdentity; readonly to: ElementIdentity }
  | { readonly kind: 'occurrence'; readonly projectId: string; readonly origin: ElementIdentity; readonly pointer: string; readonly occurrence: number; readonly from: ElementIdentity; readonly to: ElementIdentity };

/** Future overlay address only; no notes, styling persistence or mutation operation is included. */
export interface OverlayTarget {
  readonly format: 'jai.fabric-explorer.overlay-target/1';
  readonly target: { readonly kind: 'element'; readonly identity: ElementIdentity } | { readonly kind: 'edge'; readonly identity: EdgeIdentity };
}

/** Explicit source observation facts; recorded mode makes no chain or authority verification claim. */
export interface Verification {
  readonly mode: 'canonical' | 'diagnostic' | 'recorded';
  readonly decoded: 'decoded' | 'unknown' | 'failed';
  readonly chain: 'verified' | 'unknown' | 'failed';
  readonly replay: 'verified' | 'unknown' | 'failed' | 'recorded';
  readonly publicTrust: 'available' | 'missing' | 'not-required' | 'unknown';
  readonly material: 'available' | 'missing' | 'not-observed';
  readonly recordedApplicability: SemanticValue | null;
  readonly authorityGranted: false;
  readonly freshAssessment: false;
}

/** One captured source revision; sequence/head are local to this source, not globally atomic. */
export interface SourceRevision {
  readonly revisionId: string;
  readonly projectId: string;
  readonly rootId: string;
  readonly sourceId: string;
  readonly family: SourceFamily;
  readonly relativePath: string;
  readonly adapterVersion: string;
  readonly byteLength: UnsignedDecimal;
  readonly digest: Digest;
  readonly head: Digest | null;
  readonly sequence: UnsignedDecimal | null;
  readonly observedAt: string;
  readonly verification: Verification;
}

/** Source-recorded findings reducer states; accepted is not a runtime permission or automatic expiry. */
export type FindingState = 'open' | 'resolved' | 'verified' | 'stuck' | 'withdrawn' | 'accepted';
/** Maintained findings severity vocabulary. */
export type Severity = 'critical' | 'high' | 'medium' | 'low';
/** Maintained findings kind vocabulary. */
export type FindingKind = 'defect' | 'gap' | 'risk' | 'inconsistency' | 'suggestion';

/** Shared projection metadata; complete source fields remain in tagged attributes or source paging. */
export interface VertexBase {
  readonly id: ElementKey;
  readonly identity: ElementIdentity;
  readonly label: string;
  readonly source: SourceLocator;
  readonly attributes: Attributes;
  readonly extensions?: Extensions;
}

/** Read-only vertex variants; unresolved exact targets keep the eventual resolved identity. */
export type Vertex =
  | (VertexBase & { readonly kind: 'version'; readonly identity: Extract<ElementIdentity, { kind: 'version' }>; readonly family: RecordFamily })
  | (VertexBase & { readonly kind: 'use'; readonly identity: Extract<ElementIdentity, { kind: 'use' }> })
  | (VertexBase & { readonly kind: 'finding'; readonly identity: Extract<ElementIdentity, { kind: 'finding' }>; readonly state: FindingState; readonly severity: Severity; readonly findingKind: FindingKind; readonly rounds: UnsignedDecimal; readonly recordedExpiry: string | null })
  | (VertexBase & { readonly kind: 'blob'; readonly identity: Extract<ElementIdentity, { kind: 'blob' }>; readonly availability: 'available' | 'missing' | 'unknown' })
  | (VertexBase & { readonly kind: 'participant'; readonly identity: Extract<ElementIdentity, { kind: 'participant' }> })
  | (VertexBase & { readonly kind: 'ownership'; readonly identity: Extract<ElementIdentity, { kind: 'ownership' }> })
  | (VertexBase & { readonly kind: 'unresolved'; readonly identity: Extract<ElementIdentity, { kind: 'version' | 'use' | 'location' }>; readonly reason: 'missing-reference' | 'textual-location' | 'unavailable-source' });

/** Field-specific relationship classes; causal membership is supplied by the canonical engine. */
export type RelationClass = 'causal-dependency' | 'input-binding' | 'profile' | 'criteria' | 'inheritance' | 'assignment' | 'assessed-subject' | 'material-attachment' | 'participant' | 'ownership' | 'decision-effect' | 'finding-subject' | 'location-association' | 'other-reference';

/** Addressable parallel relation, with explicit source basis and semantic arrow endpoints. */
export interface Edge {
  readonly id: ElementKey;
  readonly identity: EdgeIdentity;
  readonly from: ElementKey;
  readonly to: ElementKey;
  readonly relation: RelationClass;
  readonly label: string;
  readonly source: SourceLocator;
  readonly basis: 'canonical-dependency' | 'exact-reference' | 'recorded-effect' | 'textual-location';
  readonly causal: boolean;
  readonly attributes: Attributes;
  readonly extensions?: Extensions;
}

/** Lossless graph cardinalities; these count the indexed projection model, not raw journal transactions. */
export interface Counts {
  readonly vertices: UnsignedDecimal;
  readonly edges: UnsignedDecimal;
  readonly findings: UnsignedDecimal;
}

/** Snapshot metadata only; a whole source graph is not implicitly transferred to the UI. */
export interface SnapshotDescriptor {
  readonly format: 'jai.fabric-explorer.snapshot/1';
  readonly sessionId: string;
  readonly generation: UnsignedDecimal;
  readonly sources: readonly SourceRevision[];
  readonly counts: Counts;
  readonly authorityGranted: false;
  readonly freshAssessment: false;
}

/** Explicit reason why the displayed result is not a complete graph. */
export type OmissionReason = 'filter' | 'visible-limit' | 'work-limit' | 'unresolved' | 'unavailable';

/** Bounded visible graph and source revision set; every endpoint has a represented vertex. */
export interface GraphProjection {
  readonly format: 'jai.fabric-explorer.projection/1';
  readonly snapshot: SnapshotDescriptor;
  readonly vertices: readonly Vertex[];
  readonly edges: readonly Edge[];
  readonly hiddenVertices: UnsignedDecimal;
  readonly hiddenEdges: UnsignedDecimal;
  readonly complete: boolean;
  readonly omissions: readonly OmissionReason[];
}

/** Public defaults and resource bounds copied from the maintained qualification baseline. */
export const LIMITS = Object.freeze({ frameBytes: 8 * 1024 * 1024, rawPageBytes: 256 * 1024, semanticDepth: 64, wireDepth: 256, visibleVertices: 5000, visibleEdges: 20000, defaultVertices: 2000, defaultEdges: 8000, visitedVertices: 10000, scannedEdges: 50000, hops: 32, diagnostics: 1000, helperRequests: 2, workerTasks: 8 });

/** Immutable semantic-arrow registry; layout orientation never replaces these meanings. */
export const RELATION_DIRECTIONS: Readonly<Record<RelationClass, { readonly arrow: string; readonly allowsCanonicalCausality: boolean }>> = Object.freeze({
  'causal-dependency': { arrow: 'dependency-to-consumer', allowsCanonicalCausality: true },
  'input-binding': { arrow: 'input-to-consumer', allowsCanonicalCausality: true },
  profile: { arrow: 'prerequisite-to-record', allowsCanonicalCausality: true },
  criteria: { arrow: 'prerequisite-to-record', allowsCanonicalCausality: true },
  inheritance: { arrow: 'prerequisite-to-record', allowsCanonicalCausality: true },
  assignment: { arrow: 'prerequisite-to-record', allowsCanonicalCausality: true },
  'assessed-subject': { arrow: 'subject-to-assessment', allowsCanonicalCausality: true },
  'material-attachment': { arrow: 'record-to-blob', allowsCanonicalCausality: false },
  participant: { arrow: 'record-to-participant', allowsCanonicalCausality: false },
  ownership: { arrow: 'record-to-owner', allowsCanonicalCausality: false },
  'decision-effect': { arrow: 'decision-to-use', allowsCanonicalCausality: false },
  'finding-subject': { arrow: 'finding-to-exact-subject', allowsCanonicalCausality: false },
  'location-association': { arrow: 'record-to-textual-location', allowsCanonicalCausality: false },
  'other-reference': { arrow: 'record-to-reference', allowsCanonicalCausality: false },
});

// Presentation consumers must not accidentally change traversal classification.
for (const direction of Object.values(RELATION_DIRECTIONS)) Object.freeze(direction);
