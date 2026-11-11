/** Internal codec parity with the fully validating public identity boundary. */
import { expect, it } from 'vitest';
import { elementKey, edgeKey, stableLocator } from '../src/identity.js';
import { encodeElementKey, encodeEdgeKey, encodeStableLocator } from '../src/identity-codec.js';
import type { ElementIdentity, EdgeIdentity, SourceLocator } from '../src/model.js';
const source: SourceLocator = { projectId: 'project', rootId: 'root', sourceId: 'source', family: 'findings', relativePath: 'review.jsonl', pointer: '/record', sequence: '1', revisionId: 'revision', adapterVersion: '2' };
const ref = { engagement: 'work', scope: 'origin', logical_id: 'Name " \\ \n café 🎨', version_id: 'a'.repeat(64) };
const identities: ElementIdentity[] = [
  { kind: 'version', projectId: 'project', ref }, { kind: 'use', projectId: 'project', ref, useScope: 'selected' },
  { kind: 'finding', projectId: 'project', ledgerId: 'ledger', findingId: 'F-0001' }, { kind: 'blob', projectId: 'project', rootId: 'root', blobId: 'b'.repeat(64) },
  { kind: 'participant', projectId: 'project', participant: { kind: 'assignment', ref } }, { kind: 'participant', projectId: 'project', participant: { kind: 'authority', id: 'actor' } },
  { kind: 'ownership', projectId: 'project', owner: { layer: 1, work_kind: 'question', question: 'what', work_item: 'item' } },
  { kind: 'location', projectId: 'project', origin: encodeStableLocator(source), text: 'docs/café.md:12' },
];
it('preserves every typed identity tuple and source address exactly', () => {
  for (const identity of identities) expect(encodeElementKey(identity)).toBe(elementKey(identity));
  expect(encodeStableLocator(source)).toEqual(stableLocator(source));
});
it('preserves explicit and parallel occurrence keys and lexical ordering with third-origin identities', () => {
  const keys: EdgeIdentity[] = [2, 10, Number.MAX_SAFE_INTEGER].map(occurrence => ({ kind: 'occurrence', projectId: 'project', origin: identities[2]!, from: identities[0]!, to: identities[1]!, pointer: '/x/"\\\n', occurrence }));
  keys.push({ kind: 'explicit', projectId: 'project', origin: identities[2]!, from: identities[0]!, to: identities[1]!, sourceEdgeId: 'edge-🎨' });
  expect(encodeEdgeKey(keys[0]!)).toBe(edgeKey(keys[0]!));
  expect(keys.map(encodeEdgeKey)).toEqual(keys.map(edgeKey)); expect(keys.map(encodeEdgeKey).sort()).toEqual(keys.map(edgeKey).sort());
});
it('retains public nested location namespace and Unicode rejection', () => {
  const invalid = { ...identities[7]!, projectId: 'other' } as ElementIdentity;
  expect(() => elementKey(invalid)).toThrow();
  for (const slot of ['origin', 'from', 'to'] as const) {
    const edge: EdgeIdentity = { kind: 'explicit', projectId: 'project', origin: identities[0]!, from: identities[0]!, to: identities[1]!, sourceEdgeId: 'edge', [slot]: invalid };
    expect(() => edgeKey(edge)).toThrow();
  }
  expect(() => elementKey({ kind: 'finding', projectId: 'project', ledgerId: 'ledger', findingId: '\ud800' })).toThrow();
});
