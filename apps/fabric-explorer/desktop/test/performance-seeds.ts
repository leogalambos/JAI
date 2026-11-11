// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Bounded source-derived version seeds; lexical use ordering never stands in for a version population. */
import { elementKey } from '@jai/fabric-explorer-contracts';
import type { ElementIdentity, Vertex } from '@jai/fabric-explorer-contracts';

/** Only identity metadata crosses the seed boundary; complete attributes are not retained. */
export type PerformanceIdentitySeed = Pick<Vertex, 'kind' | 'id' | 'identity'>;
/** Present, independently addressable second version, and explicitly checked negative lookup identity. */
export interface PerformanceLookupSeeds {
  readonly present: Extract<ElementIdentity, { kind: 'version' }>;
  readonly second: Extract<ElementIdentity, { kind: 'version' }> | null;
  readonly absent: Extract<ElementIdentity, { kind: 'version' }>;
  readonly presentId: string;
  readonly secondId: string | null;
  readonly coverage: 'paired-versions' | 'partial-single-version';
}
/**
 * Select exact source versions from the bounded input-A result population.
 * @param rows At most 25 validated public identities; use records may sort before versions.
 * @returns Same-logical version pair when actually observed, otherwise explicit single-version coverage.
 * @throws {Error} For a missing version, excessive population or identity/key mismatch.
 * @remarks The absent candidate is verified by actual lookup; no canonical record/hash is fabricated.
 */
export function performanceLookupSeeds(rows: readonly PerformanceIdentitySeed[]): PerformanceLookupSeeds {
  if (!rows.length || rows.length > 25 || rows.some(row => row.id !== elementKey(row.identity))) throw new Error('Bounded exact source identity population required.');
  const groups = new Map<string, Map<string, { id: string; identity: Extract<ElementIdentity, { kind: 'version' }> }>>();
  for (const row of rows) {
    if (row.kind !== 'version' || row.identity.kind !== 'version' || row.identity.ref.logical_id !== 'input-A') continue;
    const value = row.identity; const ref = value.ref; const key = JSON.stringify([value.projectId, ref.engagement, ref.scope, ref.logical_id]);
    let group = groups.get(key); if (!group) { group = new Map(); groups.set(key, group); }
    group.set(ref.version_id, { id: row.id, identity: value });
  }
  const ordered = [...groups.entries()].sort(([left], [right]) => left < right ? -1 : left > right ? 1 : 0).map(([, group]) => [...group.values()].sort((left, right) => left.id < right.id ? -1 : left.id > right.id ? 1 : 0));
  const chosen = ordered.find(group => group.length >= 2) ?? ordered[0];
  if (!chosen?.length) throw new Error('Source-derived input-A version seed absent.');
  const present = structuredClone(chosen[0]!.identity); const second = chosen[1] ? structuredClone(chosen[1].identity) : null;
  const observed = new Set(rows.map(row => row.id));
  const candidates = ['f'.repeat(64), ...Array.from({ length: 26 }, (_, index) => index.toString(16).padStart(64, '0'))];
  const absent = candidates.map(version_id => ({ ...present, ref: { ...present.ref, version_id } })).find(value => !observed.has(elementKey(value)))!;
  return { present, second, absent, presentId: elementKey(present), secondId: second ? elementKey(second) : null, coverage: second ? 'paired-versions' : 'partial-single-version' };
}
