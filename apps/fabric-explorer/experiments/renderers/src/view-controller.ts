/** Disposable adapter lifetime boundary, separate from measured SDK work. */
export type ReplaceableViewAdapter<T> = { destroy(): void; replace?(view: T): void };
/**
 * Own one current adapter and release it on final disposal.
 * @param create Creates an adapter when none exists.
 * @returns Current-view admission and final disposal operations.
 */
export function createViewController<T, A extends ReplaceableViewAdapter<T>>(create: (view: T) => A) {
  let current: A | undefined;
  return {
    set(view: T): A {
      if (current?.replace) current.replace(view);
      else { current?.destroy(); current = create(view); }
      return current;
    },
    dispose() { current?.destroy(); current = undefined; },
  };
}
