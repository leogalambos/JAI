/** Worker-generated graph records avoid repeated public schema admission. */
import { afterEach, expect, it, vi } from 'vitest';
import * as contracts from '@jai/fabric-explorer-contracts';
import { projectedFactOrigin } from '../src/import/facts.js';
import { ImportModel } from '../src/import/model.js';
import { modelInput, ref, revision, versionFact } from './import-fixtures.js';
afterEach(() => vi.restoreAllMocks());
it('constructs typed graph records without invoking public key or vertex/edge validators', () => {
  const model = new ImportModel(modelInput());
  const calls = ['elementKey', 'edgeKey', 'stableLocator', 'assertEdge', 'assertVertex'].map(name => vi.spyOn(contracts, name as 'elementKey'));
  const fact = versionFact(); model.consumeDirect(fact);
  model.consumeDirect({ kind: 'reference', sourceId: 'fabric', origin: fact.origin, originRef: ref, originUseScope: null, fieldPointer: '/related/0', occurrence: 0, targetRef: { ...ref, version_id: 'd'.repeat(64) }, targetUseScope: null, historicalCausal: false, governing: false, dependencyBasis: 'association' });
  for (const call of calls) expect(call).not.toHaveBeenCalled();
});

function finding(findingId = 'F-0001'): import('../src/broker/semantic-types.js').CanonicalFact {
  return { kind: 'finding', sourceId: 'findings', origin: versionFact().origin, findingId, state: 'open', severity: 'high', findingKind: 'defect', rounds: '0', recordedExpiry: null, label: 'Finding', target: null, location: null, attributes: { kind: 'inline', value: { type: 'string', value: '\ud800' } }, effectiveMaxRounds: 3, historicalMaxRoundsKnown: false };
}
it('rejects isolated surrogate identity strings but retains identical lossless tagged attribute values', () => {
  const input = { ...modelInput(), sources: [revision('findings')] };
  const model = new ImportModel(input); model.consumeDirect(finding());
  model.finalizeSources(input.sources, input.report); model.finish();
  expect([...model.records()]).toContainEqual(expect.objectContaining({ kind: 'finding', attributes: { kind: 'inline', value: { type: 'string', value: '\ud800' } } }));
  for (const id of ['F-\ud800', 'F-\udfff', '']) {
    const rejected = new ImportModel(input); expect(() => rejected.consumeDirect(finding(id))).toThrow(); expect(() => rejected.finish()).toThrow();
  }
});
it('retains source/span and identity construction bounds without whole-record schemas', () => {
  for (const changed of [{ sourceId: 'foreign' }, { origin: { ...versionFact().origin, byteOffset: '1001' } }, { ref: { ...ref, version_id: 'bad' } }, { ref: { ...ref, logical_id: '' } }]) {
    const model = new ImportModel(modelInput()); expect(() => model.consumeDirect({ ...versionFact(), ...changed } as import('../src/broker/semantic-types.js').CanonicalFact)).toThrow();
  }
});

it('checks only direct source ownership and exact physical span limits at the typed sink', () => {
  const fact = versionFact(); const sources = new Map([['fabric', revision()]]);
  expect(() => projectedFactOrigin(fact, sources)).not.toThrow();
  expect(() => projectedFactOrigin({ ...fact, origin: { ...fact.origin, byteOffset: '1000', byteLength: '0' } }, sources)).not.toThrow();
  expect(() => projectedFactOrigin({ ...fact, origin: { ...fact.origin, byteOffset: '1000', byteLength: '1' } }, sources)).toThrow();
});
