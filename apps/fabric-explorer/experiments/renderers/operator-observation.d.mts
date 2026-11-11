/** Shared experiment-only observation contract; no automatic or authority verdicts. */
export const observationCriteria: readonly string[];
export type OperatorObservation = {
  format: 'jai.renderer-probe.operator-observation/2';
  method: string;
  criteria: Record<string, 'pass' | 'fail' | 'unknown'>;
  note: string;
  observedAt: string | null;
};
export function unknownObservation(method: string): OperatorObservation;
export function parseOperatorObservation(answer: string, observedAt: string): OperatorObservation;
