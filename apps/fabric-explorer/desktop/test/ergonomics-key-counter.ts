/** Test-owned observation boundary; capture precedes component bubble handlers that consume their keys. */
export interface KeyCounterTarget {
  /** Register the trusted test listener with an explicit propagation phase. */
  addEventListener(type: 'keydown', listener: (event: { readonly isTrusted: boolean }) => void, capture: boolean): void;
}
/**
 * Observe delivered keys without consuming them or changing application handlers.
 * @param target Actual document in the native helper; controlled propagation port in direct tests.
 * @returns Mutable trusted/untrusted totals retained by the listener; never evidence of trust by itself.
 */
export function installKeyCounter(target: KeyCounterTarget): { trusted: number; untrusted: number } {
  const counts = { trusted: 0, untrusted: 0 };
  target.addEventListener('keydown', event => { counts[event.isTrusted ? 'trusted' : 'untrusted']++; }, true);
  return counts;
}
