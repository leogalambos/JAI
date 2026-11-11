import { describe, expect, it } from 'vitest';
import { edgeKey, elementKey, stableLocator } from '../src/identity.js';
import type { EdgeIdentity, ElementIdentity, SourceLocator } from '../src/model.js';

const version = (projectId = 'project', versionId = 'a'.repeat(64)): ElementIdentity => ({ kind: 'version', projectId, ref: { engagement: 'work', scope: 'origin:' + 'x'.repeat(160), logical_id: 'same-title', version_id: versionId } });
const source: SourceLocator = { projectId: 'project', rootId: 'root', sourceId: 'ledger', family: 'findings', relativePath: 'review.jsonl', pointer: '/data/location', sequence: '1', revisionId: 'head-one', adapterVersion: '1' };

describe('stable source identity', () => {
  it('does not collide across project, version, origin scope or use scope', () => {
    const a = version(); const b = version('second'); const c = version('project', 'b'.repeat(64));
    const useA: ElementIdentity = { ...version(), kind: 'use', useScope: 'one' } as ElementIdentity;
    const useB: ElementIdentity = { ...useA, useScope: 'two' } as ElementIdentity;
    expect(new Set([a, b, c, useA, useB].map(elementKey)).size).toBe(5);
  });

  it('does not use labels, separators or property insertion order as identity', () => {
    const a = version();
    if (a.kind !== 'version') throw new Error('Fixture kind');
    const b = { ref: { version_id: a.ref.version_id, logical_id: a.ref.logical_id, scope: a.ref.scope, engagement: a.ref.engagement }, projectId: a.projectId, kind: 'version' } as const;
    expect(elementKey(a)).toBe(elementKey(b));
    expect(elementKey({ kind: 'finding', projectId: 'a:b', ledgerId: 'c', findingId: 'F-0001' })).not.toBe(elementKey({ kind: 'finding', projectId: 'a', ledgerId: 'b:c', findingId: 'F-0001' }));
    expect(elementKey({ kind: 'finding', projectId: 'p', ledgerId: 'one', findingId: 'F-0001' })).not.toBe(elementKey({ kind: 'finding', projectId: 'p', ledgerId: 'two', findingId: 'F-0001' }));
  });

  it('retains unresolved textual identity across append revision and adapter changes', () => {
    const next = { ...source, revisionId: 'head-two', adapterVersion: '2' };
    const location = (locator: SourceLocator): ElementIdentity => ({ kind: 'location', projectId: 'project', origin: stableLocator(locator), text: 'docs/café.md:12' });
    expect(elementKey(location(source))).toBe(elementKey(location(next)));
    expect(stableLocator(source)).not.toHaveProperty('revisionId');
  });

  it('preserves explicit IDs across references without rebinding another origin version', () => {
    const identity: EdgeIdentity = { kind: 'explicit', projectId: 'project', origin: version(), sourceEdgeId: 'relation-one', from: version(), to: version('project', 'b'.repeat(64)) };
    expect(edgeKey(identity)).not.toBe(edgeKey({ ...identity, origin: version('project', 'c'.repeat(64)) }));
    const occurrence: EdgeIdentity = { kind: 'occurrence', projectId: 'project', origin: version(), pointer: '/inputs/0/refs', occurrence: 0, from: identity.from, to: identity.to };
    expect(edgeKey(occurrence)).not.toBe(edgeKey({ ...occurrence, occurrence: 1 }));
  });

  it('rejects malformed refs, use-scope overflow, traversal and namespace mismatches', () => {
    expect(() => elementKey({ ...version(), extraAuthority: true } as ElementIdentity)).toThrow();
    expect(() => elementKey({ ...version(), kind: 'use', useScope: 'x'.repeat(129) } as ElementIdentity)).toThrow();
    expect(() => stableLocator({ ...source, relativePath: '../review.jsonl' })).toThrow();
    expect(() => elementKey({ kind: 'location', projectId: 'other', origin: stableLocator(source), text: 'x' })).toThrow();
  });
});
