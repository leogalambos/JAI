import { ContractError } from './errors.js';
import { edgeKey, elementKey } from './identity.js';
import { LIMITS, RELATION_DIRECTIONS } from './model.js';
import type { Attributes, Edge, ElementIdentity, GraphProjection, OverlayTarget, SnapshotDescriptor, SourceLocator, SourceRevision, Vertex } from './model.js';
import type { AdapterChunk, AdapterReadInput } from './protocol.js';
import { assertShape } from './schema-validation.js';
import { assertSemantic } from './semantic.js';

function invalid(message: string): never { throw new ContractError('invalid-model', message); }

function identity(value: ElementIdentity): void { elementKey(value); }

function locator(value: SourceLocator): void {
  assertShape('sourceLocator', value);
}

function attributes(value: Attributes, source: SourceLocator): void {
  if (value.kind === 'inline') assertSemantic(value.value, source.family === 'findings' ? 'findings' : 'lifecycle');
  else {
    locator(value.source);
    if ((['projectId', 'rootId', 'sourceId', 'family', 'relativePath', 'pointer', 'sequence', 'revisionId', 'adapterVersion'] as const).some(field => value.source[field] !== source[field])) invalid('Paged attributes are bound to another source record/revision');
    if (BigInt(value.byteLength) > 100n * 1024n * 1024n + 2n) throw new ContractError('resource-limit', 'Decoded source-record limit exceeded');
  }
}

function sourceRevision(value: SourceRevision): void {
  const evidence = value.verification;
  if (evidence.mode === 'recorded' && (evidence.decoded !== 'decoded' || evidence.chain !== 'unknown' || evidence.replay !== 'recorded' || evidence.publicTrust !== 'unknown' || evidence.material !== 'not-observed' || evidence.recordedApplicability !== null)) invalid('Recorded observations cannot claim fresh canonical verification');
  if (evidence.replay === 'recorded' && evidence.mode !== 'recorded') invalid('Recorded projection requires recorded observation mode');
  if (evidence.recordedApplicability !== null) assertSemantic(evidence.recordedApplicability);
  if (evidence.recordedApplicability !== null && evidence.replay !== 'verified') invalid('Recorded applicability requires successful canonical replay');
  if (evidence.mode === 'diagnostic' && (evidence.replay === 'verified' || evidence.recordedApplicability !== null)) invalid('Diagnostic evidence cannot claim canonical applicability');
  if (value.family !== 'fabric' && (evidence.replay === 'verified' || evidence.recordedApplicability !== null)) invalid('Non-fabric source evidence cannot claim lifecycle replay');
  if (evidence.replay === 'verified' && (evidence.decoded !== 'decoded' || evidence.chain !== 'verified' || !['available', 'not-required'].includes(evidence.publicTrust))) invalid('Canonical replay evidence is internally inconsistent');
  if (value.family === 'audit' && BigInt(value.byteLength) > 100n * 1024n * 1024n) throw new ContractError('resource-limit', 'Structured audit source limit exceeded');
}

/**
 * Validate a detached vertex DTO without evaluating source correctness.
 * @param value Candidate vertex with exact identity, provenance and inline/paged attributes.
 * @returns Nothing on structural and local identity consistency success; the input is not mutated.
 * @throws {ContractError} For incompatible identity/key/provenance, lossy semantic data or malformed attributes.
 */
export function assertVertex(value: unknown): asserts value is Vertex {
  assertShape('vertex', value);
  const vertex = value as Vertex;
  identity(vertex.identity);
  if (vertex.id !== elementKey(vertex.identity)) invalid('Vertex key does not match its identity');
  if (vertex.source.projectId !== vertex.identity.projectId) invalid('Vertex provenance belongs to another project');
  if (vertex.kind === 'finding' && vertex.source.family !== 'findings') invalid('Ledger finding requires findings provenance');
  if (vertex.kind === 'version' && vertex.source.family !== 'fabric') invalid('Version vertex requires canonical fabric provenance');
  if (vertex.kind === 'unresolved' && ((vertex.identity.kind === 'location') !== (vertex.reason === 'textual-location'))) invalid('Unresolved target reason does not match its identity');
  attributes(vertex.attributes, vertex.source);
  for (const item of Object.values(vertex.extensions ?? {})) assertSemantic(item);
}

/**
 * Validate one addressable relation and its source-backed direction/basis declaration.
 * @param value Candidate edge; source canonical dependency classification must already be supplied.
 * @returns Nothing on structural consistency success; no dependency is inferred or reclassified.
 * @throws {ContractError} For mismatched endpoints/keys, forbidden causal basis or invalid semantic attributes.
 */
export function assertEdge(value: unknown): asserts value is Edge {
  assertShape('edge', value);
  const edge = value as Edge;
  if (edge.id !== edgeKey(edge.identity) || edge.from !== elementKey(edge.identity.from) || edge.to !== elementKey(edge.identity.to)) invalid('Edge identity and endpoint keys differ');
  if (edge.source.projectId !== edge.identity.projectId) invalid('Edge provenance belongs to another project');
  if (edge.causal !== (edge.basis === 'canonical-dependency')) invalid('Causal edges require canonical dependency classification');
  if (edge.causal && !RELATION_DIRECTIONS[edge.relation].allowsCanonicalCausality) invalid('This relationship class is not causal');
  if (edge.relation === 'causal-dependency' && !edge.causal) invalid('Causal dependency must preserve canonical classification');
  if (edge.relation === 'finding-subject' && (edge.basis !== 'exact-reference' || !['version', 'use'].includes(edge.identity.to.kind))) invalid('Finding subjects require an exact source reference');
  if (edge.relation === 'location-association' && (edge.basis !== 'textual-location' || edge.identity.to.kind !== 'location')) invalid('Textual locations cannot become exact subject relations');
  if (edge.relation === 'decision-effect' && edge.basis !== 'recorded-effect') invalid('Decision effects require recorded-effect basis');
  attributes(edge.attributes, edge.source);
  for (const item of Object.values(edge.extensions ?? {})) assertSemantic(item);
}

/**
 * Validate source-revision metadata and distinct per-session snapshot generation.
 * @param value Snapshot metadata; whole graph arrays are not included.
 * @returns Nothing when source namespaces/revisions and verification claims are locally consistent.
 * @throws {ContractError} For duplicate source identities/revision IDs, invalid evidence or acquisition overflow.
 */
export function assertSnapshot(value: unknown): asserts value is SnapshotDescriptor {
  assertShape('snapshot', value);
  const snapshot = value as SnapshotDescriptor;
  const ids = new Set<string>(); const sourceIds = new Set<string>(); let size = 0n;
  for (const revision of snapshot.sources) {
    sourceRevision(revision);
    if (ids.has(revision.revisionId) || sourceIds.has(revision.sourceId)) invalid('Snapshot repeats an admitted source or revision identity');
    ids.add(revision.revisionId); sourceIds.add(revision.sourceId); size += BigInt(revision.byteLength);
  }
  if (size > 1024n * 1024n * 1024n) throw new ContractError('resource-limit', 'Selected source aggregate limit exceeded');
}

/**
 * Validate a complete bounded projection, including unresolved endpoint representation.
 * @param value Candidate visible graph; paging/stream assembly must finish before this check.
 * @returns Nothing for a consistent projection; cycles and separately addressed parallel edges are allowed.
 * @throws {ContractError} For duplicate IDs, missing endpoints, mismatched source revisions or false completeness.
 */
export function assertProjection(value: unknown): asserts value is GraphProjection {
  assertShape('projection', value);
  const projection = value as GraphProjection;
  assertSnapshot(projection.snapshot);
  const sources = new Map(projection.snapshot.sources.map(source => [source.revisionId, source]));
  const checkSource = (source: SourceLocator): void => {
    const revision = sources.get(source.revisionId);
    if (!revision || (['projectId', 'rootId', 'sourceId', 'family', 'relativePath', 'adapterVersion'] as const).some(field => revision[field] !== source[field])) invalid('Element source does not belong to this observed revision set');
    if (source.sequence !== null && revision.sequence !== null && BigInt(source.sequence) > BigInt(revision.sequence)) invalid('Element sequence exceeds its captured ledger revision');
  };
  const nodes = new Set<string>(); const edges = new Set<string>();
  for (const vertex of projection.vertices) {
    assertVertex(vertex); checkSource(vertex.source);
    if (nodes.has(vertex.id)) invalid('Projection contains duplicate vertex identity');
    nodes.add(vertex.id);
  }
  for (const edge of projection.edges) {
    assertEdge(edge); checkSource(edge.source);
    if (edges.has(edge.id) || !nodes.has(edge.from) || !nodes.has(edge.to)) invalid('Projection contains duplicate edge or absent endpoint');
    edges.add(edge.id);
  }
  if (projection.complete && projection.omissions.some(reason => reason !== 'filter')) invalid('Limited or unavailable projection cannot claim completeness');
  if (!projection.complete && projection.omissions.length === 0) invalid('Incomplete projection must explain omissions');
  if (BigInt(projection.snapshot.counts.vertices) < BigInt(nodes.size) || BigInt(projection.snapshot.counts.edges) < BigInt(edges.size)) invalid('Visible counts exceed the indexed graph counts');
}

/**
 * Validate a future annotation address while keeping annotation content/persistence absent.
 * @param value Versioned element/edge address only.
 * @returns Nothing when the target uses a valid stable identity.
 * @throws {ContractError} For unsupported versions, extra note/mutation fields or inconsistent identity.
 */
export function assertOverlayTarget(value: unknown): asserts value is OverlayTarget {
  assertShape('overlayTarget', value);
  const target = (value as OverlayTarget).target;
  if (target.kind === 'element') elementKey(target.identity); else edgeKey(target.identity);
}

/**
 * Validate a canonical adapter's trusted input contract without opening any source.
 * @param value Admitted opaque handles, expected binding and optional previous descriptor.
 * @returns Nothing on structural consistency success; handle authenticity remains broker-owned.
 * @throws {ContractError} For missing capability, duplicate sources or mismatched previous generation/session.
 */
export function assertAdapterInput(value: unknown): asserts value is AdapterReadInput {
  assertShape('adapterInput', value);
  const input = value as AdapterReadInput;
  if (input.binding.capability === null) invalid('Adapter reads require an admitted capability');
  const ids = new Set<string>();
  for (const source of input.sources) {
    if (ids.has(source.sourceId)) invalid('Adapter input repeats an admitted source');
    ids.add(source.sourceId);
  }
  if (input.previous !== null) {
    assertSnapshot(input.previous);
    if (input.previous.sessionId !== input.binding.sessionId || input.previous.generation !== input.binding.generation) invalid('Previous snapshot differs from adapter binding');
  } else if (input.binding.generation !== null) invalid('Adapter generation requires the corresponding previous snapshot');
}

/**
 * Validate a bounded canonical-helper chunk; partial records are not publishable snapshots.
 * @param value One typed adapter chunk with an unchanged request binding.
 * @returns Nothing when individual records/diagnostics or the final descriptor are structurally valid.
 * @throws {ContractError} For source/identity inconsistencies or invalid final-session metadata.
 */
export function assertAdapterChunk(value: unknown): asserts value is AdapterChunk {
  assertShape('adapterChunk', value);
  const chunk = value as AdapterChunk;
  if (chunk.binding.capability === null) invalid('Adapter chunks require an admitted capability');
  if (chunk.kind === 'records') { chunk.vertices.forEach(assertVertex); chunk.edges.forEach(assertEdge); }
  else if (chunk.kind === 'diagnostics') {
    if (BigInt(chunk.total) < BigInt(chunk.diagnostics.length) || chunk.diagnostics.length > LIMITS.diagnostics) invalid('Diagnostic totals are inconsistent');
  } else {
    assertSnapshot(chunk.snapshot);
    if (chunk.snapshot.sessionId !== chunk.binding.sessionId || (chunk.binding.generation !== null && BigInt(chunk.snapshot.generation) <= BigInt(chunk.binding.generation))) invalid('Adapter candidate generation does not advance the bound session');
  }
}
