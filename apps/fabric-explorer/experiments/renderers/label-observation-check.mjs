/** Controlled standalone schema checks; no simulated visual verdict. */
import assert from 'node:assert/strict';
import { parseLabelObservation, unknownLabelObservation } from './label-observation.mjs';
assert.deepEqual(parseLabelObservation({}), unknownLabelObservation());
assert.equal(parseLabelObservation({ pathSeparation: 'fail', canvasLabelReadability: 'pass' }).inspectorLabelReadability, 'unknown');
for (const value of [null, [], { pathSeparation: true }, { edgeLabelReadability: 'pass' }, { note: 'x'.repeat(2001) }]) assert.throws(() => parseLabelObservation(value));
console.log('PASS: standalone geometry/canvas criteria reject legacy keys and invalid answers; unanswered remains unknown.');
