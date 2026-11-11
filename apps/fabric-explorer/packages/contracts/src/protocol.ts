import type { Attributes, Counts, ElementIdentity, FindingState, GraphProjection, RecordFamily, RelationClass, SnapshotDescriptor, SourceFamily, SourceLocator, UnsignedDecimal, Vertex, Edge } from './model.js';
import type { ContractErrorCode } from './errors.js';

/** Exact allowlisted read-only consumer protocol version. */
export const PROTOCOL = 'jai.fabric-explorer.consumer/1' as const;

/** Ephemeral broker context; stable model identities never contain these handles. */
export interface Binding {
  readonly sessionId: string;
  readonly capability: string | null;
  readonly generation: UnsignedDecimal | null;
}

/** Source picked by the user and admitted by the broker; readHandle is opaque, never a renderer path. */
export interface AdmittedSource {
  readonly projectId: string;
  readonly rootId: string;
  readonly sourceId: string;
  readonly family: SourceFamily;
  readonly relativePath: string;
  readonly readHandle: string;
}

/** Explicit query filters; empty sets mean all values rather than an implicit source mutation. */
export interface Filter {
  readonly projectIds: readonly string[];
  readonly families: readonly RecordFamily[];
  readonly findingStates: readonly FindingState[];
  readonly relations: readonly RelationClass[];
}

/** Opaque server token plus inspectable query/session/generation binding; token authenticity is a broker duty. */
export interface Cursor {
  readonly binding: Binding;
  readonly operation: 'search.page';
  readonly queryKey: string;
  readonly offset: UnsignedDecimal;
  readonly token: string;
}

/** Explicit bounded traversal work and visible-result limits. */
export interface QueryLimits {
  readonly maxVertices: number;
  readonly maxEdges: number;
  readonly maxVisitedVertices: number;
  readonly maxScannedEdges: number;
  readonly maxHops: number;
}

/** Closed request payload map; no path, command, write, approval or annotation operation exists. */
export interface RequestPayloads {
  readonly 'roots.pick': { readonly families: readonly SourceFamily[] };
  readonly 'roots.close': Record<string, never>;
  readonly 'snapshot.import': { readonly sourceIds: readonly string[] };
  readonly 'snapshot.refresh': Record<string, never>;
  readonly 'request.cancel': { readonly targetRequestId: string };
  readonly 'element.lookup': { readonly identity: ElementIdentity };
  readonly 'search.page': { readonly text: string; readonly filter: Filter; readonly order: 'identity' | 'label'; readonly limit: number; readonly cursor: Cursor | null };
  readonly 'graph.counts': { readonly filter: Filter };
  readonly 'graph.neighbours': { readonly identity: ElementIdentity; readonly direction: 'forward' | 'reverse' | 'both'; readonly relations: readonly RelationClass[]; readonly causalOnly: boolean; readonly limits: QueryLimits };
  readonly 'graph.path': { readonly from: ElementIdentity; readonly to: ElementIdentity; readonly direction: 'forward' | 'reverse' | 'both'; readonly relations: readonly RelationClass[]; readonly causalOnly: boolean; readonly limits: QueryLimits };
  readonly 'element.details': { readonly identity: ElementIdentity };
  readonly 'source.page': { readonly sourceId: string; readonly pointer: string; readonly sequence: UnsignedDecimal | null; readonly offset: UnsignedDecimal; readonly length: number };
}

/** Closed operation vocabulary derived from the read-only payload map. */
export type Operation = keyof RequestPayloads;

/** Discriminated request envelope with exact operation-specific arguments. */
export type Request = { [K in Operation]: { readonly protocol: typeof PROTOCOL; readonly kind: 'request'; readonly requestId: string; readonly binding: Binding; readonly operation: K; readonly payload: RequestPayloads[K] } }[Operation];

/** Value-redacted errors suitable for UI diagnostics; source evidence is an optional relative locator. */
export interface Diagnostic {
  readonly code: ContractErrorCode | 'not-found' | 'cancelled' | 'incompatible-source' | 'read-failed' | 'worker-failed';
  readonly message: string;
  readonly source: SourceLocator | null;
  readonly severity: 'error' | 'warning' | 'info';
}

/** Exact byte page; byteLength is decoded length and is limited independently of base64 overhead. */
export interface BytePage {
  readonly sourceId: string;
  readonly pointer: string;
  readonly sequence: UnsignedDecimal | null;
  readonly offset: UnsignedDecimal;
  readonly byteLength: number;
  readonly bytesBase64: string;
  readonly eof: boolean;
}

/** Operation-specific successes; snapshot generations are candidate metadata inside the payload. */
export interface ResponsePayloads {
  readonly 'roots.pick': { readonly capability: string; readonly sources: readonly AdmittedSource[] };
  readonly 'roots.close': { readonly closed: true };
  readonly 'snapshot.import': { readonly snapshot: SnapshotDescriptor };
  readonly 'snapshot.refresh': { readonly snapshot: SnapshotDescriptor };
  readonly 'request.cancel': { readonly targetRequestId: string; readonly acknowledgement: 'accepted' | 'not-active' };
  readonly 'element.lookup': { readonly vertex: Vertex | null };
  readonly 'search.page': { readonly items: readonly Vertex[]; readonly hidden: UnsignedDecimal; readonly complete: boolean; readonly nextCursor: Cursor | null };
  readonly 'graph.counts': Counts;
  readonly 'graph.neighbours': { readonly projection: GraphProjection };
  readonly 'graph.path': { readonly projection: GraphProjection; readonly found: boolean | null; readonly complete: boolean };
  readonly 'element.details': { readonly identity: ElementIdentity; readonly attributes: Attributes };
  readonly 'source.page': BytePage;
}

/** Bound success or error; the request context is echoed rather than advanced silently. */
export type Response = { [K in Operation]: { readonly protocol: typeof PROTOCOL; readonly kind: 'response'; readonly requestId: string; readonly binding: Binding; readonly operation: K } & ({ readonly status: 'ok'; readonly payload: ResponsePayloads[K] } | { readonly status: 'error'; readonly error: Diagnostic }) }[Operation];

/** Unbound typed rejection cannot impersonate a successful response for a source capability. */
export interface RejectionNotice {
  readonly protocol: typeof PROTOCOL;
  readonly kind: 'rejection';
  readonly requestId: string | null;
  readonly error: Diagnostic;
}

/** Operations whose bounded logical results can exceed a single 8 MiB frame. */
export type ChunkOperation = 'search.page' | 'graph.neighbours' | 'graph.path';

/** Graph-query terminal metadata; records are accumulated separately before full projection validation. */
export type GraphTerminal = Omit<GraphProjection, 'format' | 'vertices' | 'edges'>;

/** Operation-specific chunk terminal metadata; null terminal means more data remains. */
export interface ChunkTerminals {
  readonly 'search.page': { readonly hidden: UnsignedDecimal; readonly complete: boolean; readonly nextCursor: Cursor | null };
  readonly 'graph.neighbours': GraphTerminal;
  readonly 'graph.path': GraphTerminal & { readonly found: boolean | null };
}

/** Bounded query records with a contiguous sequence; endpoints may be in another staged chunk. */
export type ResponseChunk = { [K in ChunkOperation]: { readonly protocol: typeof PROTOCOL; readonly kind: 'response-chunk'; readonly requestId: string; readonly binding: Binding; readonly operation: K; readonly sequence: UnsignedDecimal; readonly vertices: readonly Vertex[]; readonly edges: readonly Edge[]; readonly terminal: ChunkTerminals[K] | null } }[ChunkOperation];

/** Receiver-owned immutable progress; it carries no assembled graph or source authority. */
export interface ChunkState {
  readonly requestId: string;
  readonly binding: Binding;
  readonly operation: ChunkOperation;
  readonly nextSequence: UnsignedDecimal;
  readonly vertices: number;
  readonly edges: number;
  readonly ended: boolean;
}

/** Canonical-helper input binding; actual capability resolution is outside this pure contract package. */
export interface AdapterReadInput {
  readonly binding: Binding;
  readonly sources: readonly AdmittedSource[];
  readonly previous: SnapshotDescriptor | null;
  readonly checkpointToken: string | null;
}

/** Bounded helper stream; only a final complete message may supply a publishable candidate descriptor. */
export type AdapterChunk =
  | { readonly kind: 'records'; readonly binding: Binding; readonly vertices: readonly Vertex[]; readonly edges: readonly Edge[] }
  | { readonly kind: 'diagnostics'; readonly binding: Binding; readonly diagnostics: readonly Diagnostic[]; readonly total: UnsignedDecimal }
  | { readonly kind: 'complete'; readonly binding: Binding; readonly snapshot: SnapshotDescriptor; readonly checkpointToken: string | null };

/** Read-only adapter boundary for the maintained canonical helper; no writer or evaluator is exposed. */
export interface CanonicalReaderAdapter {
  /** Exact adapter contract implementation version attached to source provenance. */
  readonly adapterVersion: string;
  /**
   * Read admitted sources into bounded chunks without modifying their files.
   * @param input Trusted broker-admitted handles and the optional accepted previous descriptor.
   * @param signal Cancellation signal; implementations preserve the previous snapshot on failure.
   * @returns Bounded record/diagnostic chunks followed by one candidate-complete descriptor.
   * @throws {Error} Implementations reject denied reads, incompatible sources, cancellation or canonical verification failure.
   */
  read(input: AdapterReadInput, signal: AbortSignal): AsyncIterable<AdapterChunk>;
}
