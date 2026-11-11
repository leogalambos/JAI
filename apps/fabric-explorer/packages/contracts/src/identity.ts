import { ContractError } from './errors.js';
import type { EdgeIdentity, ElementIdentity, SourceLocator, StableLocator } from './model.js';
import { assertShape } from './schema-validation.js';
import { encodeElementKey, encodeEdgeKey, encodeStableLocator } from './identity-codec.js';

function locationNamespace(identity: ElementIdentity): void {
  if (identity.kind === 'location' && identity.projectId !== identity.origin.projectId) throw new ContractError('invalid-model', 'Location namespace differs from its source origin');
}
/**
 * Detach a stable source address from revision-bearing provenance.
 * @param source Valid complete source locator with exact relative record address.
 * @returns Stable project/root/source/file/pointer/sequence fields, excluding revision/time/adapter.
 * @throws {ContractError} For an invalid source locator.
 */
export function stableLocator(source: SourceLocator): StableLocator {
  assertShape('sourceLocator', source);
  return encodeStableLocator(source);
}

/**
 * Address a vertex using an injective tagged tuple without canonical hashing or normalization.
 * @param identity Exact namespaced source identity; labels/capabilities/revisions are not accepted.
 * @returns A stable local element key, preserving arbitrary source strings and version/use distinctions.
 * @throws {ContractError} For malformed identities or an inconsistent location namespace.
 */
export function elementKey(identity: ElementIdentity): string {
  assertShape('elementIdentity', identity);
  locationNamespace(identity);
  return encodeElementKey(identity);
}

/**
 * Address an explicit or occurrence-derived relation without collapsing parallel edges.
 * @param identity Exact immutable origin and endpoints, plus explicit ID or field occurrence.
 * @returns A stable local edge key; no source-domain digest or permission is computed.
 * @throws {ContractError} For invalid identity shape or a mismatched origin namespace.
 */
export function edgeKey(identity: EdgeIdentity): string {
  assertShape('edgeIdentity', identity);
  if (identity.projectId !== identity.origin.projectId) throw new ContractError('invalid-model', 'Edge namespace differs from its origin');
  locationNamespace(identity.origin); locationNamespace(identity.from); locationNamespace(identity.to);
  return encodeEdgeKey(identity);
}
