/** Disposable manual-observation parser; human feedback remains separate from qualification and authority. */
/** Exact feature names shown to the operator, with no default positive verdict. */
export const observationCriteria = ['vertexPointerPicking', 'vertexLabelReadability', 'edgeLabelReadability', 'edgeCanvasLabelReadability', 'parallelEdgePicking', 'selfLoopPicking', 'arrowDirection'];

/**
 * Create an unanswered observation record.
 * @param {string} method Explicit recording method, never an authority identity.
 * @returns {object} Fresh record whose every criterion is unknown.
 */
export function unknownObservation(method) {
  return { format: 'jai.renderer-probe.operator-observation/2', method, criteria: Object.fromEntries(observationCriteria.map(key => [key, 'unknown'])), note: '', observedAt: null };
}

/**
 * Validate one operator-entered JSON object without inferring missing answers.
 * @param {string} answer Terminal input; an empty answer leaves all verdicts unknown.
 * @param {string} observedAt Recorder timestamp for this explicit response.
 * @returns {object} Operator-observed verdicts, distinct from automatic test results.
 * @throws {Error} If JSON, criterion names, verdicts or bounded note are invalid.
 */
export function parseOperatorObservation(answer, observedAt) {
  const result = unknownObservation('explicit-operator-observation');
  if (!answer.trim()) return { ...result, observedAt };
  const value = JSON.parse(answer);
  if (!value || typeof value !== 'object' || Array.isArray(value)) throw new Error('An object is required');
  for (const key of Object.keys(value)) {
    if (key === 'note') {
      if (typeof value.note !== 'string' || value.note.length > 2000) throw new Error('Invalid note');
    } else if (!observationCriteria.includes(key) || !['pass', 'fail', 'unknown'].includes(value[key])) {
      throw new Error('Unknown criterion or verdict');
    }
  }
  for (const key of observationCriteria) if (Object.hasOwn(value, key)) result.criteria[key] = value[key];
  result.note = value.note ?? '';
  result.observedAt = observedAt;
  return result;
}
