/** Standalone tiny-scene observations; old performance/manual reports keep their original semantics. */
export const labelCriteria = {
  pathSeparation: 'Can you visually distinguish the three separate paths e0, e1 and reverse e3 between the two vertices, and the e2 self-loop?',
  canvasLabelReadability: 'After selecting each relation, is its label directly on the edge in the graph readable without overlapping another label? Check e0, e1, e2 and e3; the inspector alone does not satisfy this check.',
  inspectorLabelReadability: 'Does the Full label card show the complete label of every selected relation e0, e1, e2 and e3?',
};
/** Return explicit unknown defaults; never infer a visual pass from SDK data. */
export function unknownLabelObservation() {
  return { format: 'jai.renderer-probe.label-observation/1', authority: 'operator-observed-not-product-qualification', ...Object.fromEntries(Object.keys(labelCriteria).map(key => [key, 'unknown'])), note: '' };
}
/** Validate only the standalone scene criteria and bounded operator text. */
export function parseLabelObservation(value) {
  const result = unknownLabelObservation();
  if (!value || typeof value !== 'object' || Array.isArray(value)) throw new Error('Label observation must be an object');
  for (const key of Object.keys(value)) if (![...Object.keys(result), 'skipped'].includes(key)) throw new Error(`Unknown observation field ${key}`);
  for (const key of Object.keys(labelCriteria)) {
    if (value[key] !== undefined && !['pass', 'fail', 'unknown'].includes(value[key])) throw new Error(`Invalid observation ${key}`);
    result[key] = value[key] ?? 'unknown';
  }
  if (value.note !== undefined && (typeof value.note !== 'string' || value.note.length > 2000)) throw new Error('Note must contain at most 2000 characters');
  result.note = value.note ?? '';
  return result;
}
