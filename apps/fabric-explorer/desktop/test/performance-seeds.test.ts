// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Synthetic consumer identity tests; actual canonical admission remains a separate corpus oracle. */
import { describe, expect, it } from 'vitest';
import { createHash } from 'node:crypto';
import { elementKey } from '@jai/fabric-explorer-contracts';
import type { ElementIdentity } from '@jai/fabric-explorer-contracts';
import { performanceLookupSeeds } from './performance-seeds.js';
import type { PerformanceIdentitySeed } from './performance-seeds.js';
const identity = (name: string, logical = 'input-A', projectId = 'project'): Extract<ElementIdentity, { kind: 'version' }> => ({ kind: 'version', projectId, ref: { engagement: 'synthetic-rich', scope: 'origin', logical_id: logical, version_id: createHash('sha256').update(name).digest('hex') } });
const version = (value: ReturnType<typeof identity>): PerformanceIdentitySeed => ({ kind: 'version', id: elementKey(value), identity: value });
describe('bounded actual-identity lookup seeds', () => {
  it('finds both exact versions even when many use keys sort before every version', () => {
    const first = identity('one'); const second = identity('two');
    const uses: PerformanceIdentitySeed[] = Array.from({ length: 12 }, (_, ordinal) => { const value = { ...first, kind: 'use' as const, useScope: `scope-${ordinal}` }; return { kind: 'use', id: elementKey(value), identity: value }; });
    const rows = [...uses, version(first), version(second)].sort((left, right) => left.id < right.id ? -1 : left.id > right.id ? 1 : 0);
    expect(rows.slice(0, 10).every(row => row.kind === 'use')).toBe(true);
    const result = performanceLookupSeeds(rows);
    expect(result.coverage).toBe('paired-versions'); expect(result.second).not.toBeNull();
    expect(result.present.ref.logical_id).toBe('input-A'); expect(result.second!.ref.logical_id).toBe('input-A');
    expect(result.present.ref.version_id).not.toBe(result.second!.ref.version_id);
    expect(result.presentId).toBe(elementKey(result.present)); expect(result.secondId).toBe(elementKey(result.second!));
  });
  it('keeps old single-version input partial rather than inventing a second recorded version', () => {
    const result = performanceLookupSeeds([version(identity('one'))]);
    expect(result.coverage).toBe('partial-single-version'); expect(result.second).toBeNull(); expect(result.secondId).toBeNull();
    expect(elementKey(result.absent)).not.toBe(result.presentId);
  });
  it('does not pair different logical, project, engagement or scope identities', () => {
    const first = identity('one');
    expect(performanceLookupSeeds([version(first), version(first)]).coverage).toBe('partial-single-version');
    for (const other of [identity('two', 'input-A-other'), identity('two', 'input-A', 'other-project'), { ...identity('two'), ref: { ...identity('two').ref, engagement: 'other-engagement' } }, { ...identity('two'), ref: { ...identity('two').ref, scope: 'other-scope' } }]) expect(performanceLookupSeeds([version(first), version(other)]).coverage).toBe('partial-single-version');
    expect(() => performanceLookupSeeds([])).toThrow();
    expect(() => performanceLookupSeeds(Array(26).fill(version(first)))).toThrow('Bounded');
    expect(() => performanceLookupSeeds([{ ...version(first), id: 'invented' }])).toThrow('identity');
  });
});
