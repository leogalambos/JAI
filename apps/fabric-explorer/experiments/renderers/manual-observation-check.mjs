/** Disposable smoke checks: missing/manual answers never become automatic positive verdicts. */
import assert from 'node:assert/strict';
import { parseOperatorObservation, unknownObservation } from './operator-observation.mjs';
const timestamp = '2030-01-01T00:00:00Z';
assert.ok(Object.values(unknownObservation('not-requested').criteria).every(value => value === 'unknown'));
assert.equal(unknownObservation('not-requested').format, 'jai.renderer-probe.operator-observation/2');
assert.equal(Object.keys(unknownObservation('not-requested').criteria).length, 7);
assert.ok(Object.values(parseOperatorObservation('', timestamp).criteria).every(value => value === 'unknown'));
const partial = parseOperatorObservation('{"parallelEdgePicking":"pass","selfLoopPicking":"fail"}', timestamp);
assert.equal(partial.criteria.parallelEdgePicking, 'pass');
assert.equal(partial.criteria.selfLoopPicking, 'fail');
assert.equal(partial.criteria.arrowDirection, 'unknown');
assert.equal(partial.observedAt, timestamp);
assert.equal(partial.criteria.edgeCanvasLabelReadability, 'unknown');
const inspectorOnly = parseOperatorObservation('{"edgeLabelReadability":"pass"}', timestamp);
assert.equal(inspectorOnly.criteria.edgeLabelReadability, 'pass');
assert.equal(inspectorOnly.criteria.edgeCanvasLabelReadability, 'unknown');
const canvasOnly = parseOperatorObservation('{"edgeCanvasLabelReadability":"fail"}', timestamp);
assert.equal(canvasOnly.criteria.edgeCanvasLabelReadability, 'fail');
assert.equal(canvasOnly.criteria.edgeLabelReadability, 'unknown');
for (const invalid of ['null', '[]', '{', '{"approved":true}', '{"arrowDirection":true}', '{"edgeCanvasLabelReadability":true}', '{"arrowDirection":"yes"}', JSON.stringify({ note: 'x'.repeat(2001) })]) {
  assert.throws(() => parseOperatorObservation(invalid, timestamp));
}
console.log('PASS: manual observation parsing preserves unknown answers and rejects invalid positive/authority fields.');
