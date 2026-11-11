/** Internal typed tuple codec; callers establish identity invariants at their admission boundary. */
import type { EdgeIdentity, ElementIdentity, SourceLocator, SourceReference, StableLocator } from './model.js';

const referenceTuple = (ref: SourceReference) => [ref.engagement, ref.scope, ref.logical_id, ref.version_id];

/**
 * Detach a stable source address from revision-bearing provenance.
 * @param source Valid complete source locator with exact relative record address.
 * @returns Stable project/root/source/file/pointer/sequence fields, excluding revision/time/adapter.
 * Input must already satisfy the source-locator contract.
 */
export function encodeStableLocator(source: SourceLocator): StableLocator {
  const { projectId, rootId, sourceId, family, relativePath, pointer, sequence } = source;
  return { projectId, rootId, sourceId, family, relativePath, pointer, sequence };
}

/**
 * Address a vertex using an injective tagged tuple without canonical hashing or normalization.
 * @param identity Exact namespaced source identity; labels/capabilities/revisions are not accepted.
 * @returns A stable local element key, preserving arbitrary source strings and version/use distinctions.
 * Input must already satisfy identity shape and namespace invariants.
 */
export function encodeElementKey(identity: ElementIdentity): string {
  const base = ['jai.fabric-explorer.element/1', identity.kind, identity.projectId];
  switch (identity.kind) {
    case 'version': return JSON.stringify([...base, ...referenceTuple(identity.ref)]);
    case 'use': return JSON.stringify([...base, ...referenceTuple(identity.ref), identity.useScope]);
    case 'finding': return JSON.stringify([...base, identity.ledgerId, identity.findingId]);
    case 'blob': return JSON.stringify([...base, identity.rootId, identity.blobId]);
    case 'participant': return JSON.stringify([...base, identity.participant.kind, ...(identity.participant.kind === 'assignment' ? referenceTuple(identity.participant.ref) : [identity.participant.id])]);
    case 'ownership': return JSON.stringify([...base, String(identity.owner.layer), identity.owner.work_kind, identity.owner.question, identity.owner.work_item]);
    case 'location': {
      const origin = identity.origin;
      return JSON.stringify([...base, origin.rootId, origin.sourceId, origin.family, origin.relativePath, origin.pointer, origin.sequence, identity.text]);
    }
  }
}

/**
 * Address an explicit or occurrence-derived relation without collapsing parallel edges.
 * @param identity Exact immutable origin and endpoints, plus explicit ID or field occurrence.
 * @returns A stable local edge key; no source-domain digest or permission is computed.
 * Input must already satisfy edge and nested identity invariants.
 */
export function encodeEdgeKey(identity: EdgeIdentity): string {
  const base = ['jai.fabric-explorer.edge/1', identity.kind, identity.projectId, encodeElementKey(identity.origin)];
  const address = identity.kind === 'explicit' ? [identity.sourceEdgeId] : [identity.pointer, String(identity.occurrence)];
  return JSON.stringify([...base, ...address, encodeElementKey(identity.from), encodeElementKey(identity.to)]);
}
