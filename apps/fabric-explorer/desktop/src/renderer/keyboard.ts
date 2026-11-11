// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Exact modifier shortcuts leave native editing, assistive-technology keys and unavailable actions alone. */
/** Keyboard facts observed by the application, without a DOM dependency in the classifier. */
export interface ShortcutEvent { readonly key: string; readonly ctrlKey: boolean; readonly metaKey: boolean; readonly altKey: boolean; readonly shiftKey: boolean; readonly defaultPrevented: boolean; readonly isComposing: boolean; readonly repeat: boolean }
/** Availability comes from actual controls/state, not from a global assumption of readiness. */
export interface ShortcutContext { readonly editing: boolean; readonly search: boolean; readonly fit: boolean; readonly back: boolean; readonly forward: boolean; readonly activeWork: boolean }
/** Fixed application action; source content cannot register a shortcut or callback. */
export type ShortcutAction = 'search' | 'fit' | 'back' | 'forward' | 'cancel';
/**
 * Classify one enabled exact shortcut without consuming its event or invoking any action.
 * @param event Native event facts, including prevention/composition and repetition state.
 * @param context Editing and action availability observed at the application boundary.
 * @returns A fixed supported action, or null to preserve native/assistive-technology behavior.
 */
export function keyboardAction(event: ShortcutEvent, context: ShortcutContext): ShortcutAction | null {
  if (event.defaultPrevented || event.isComposing || event.repeat || context.editing) return null;
  const primary = event.ctrlKey !== event.metaKey; const key = event.key.toLowerCase();
  if (primary && !event.altKey && !event.shiftKey && key === 'k') return context.search ? 'search' : null;
  if (primary && !event.altKey && event.shiftKey && key === 'f') return context.fit ? 'fit' : null;
  if (!event.ctrlKey && !event.metaKey && event.altKey && !event.shiftKey) {
    if (event.key === 'ArrowLeft') return context.back ? 'back' : null;
    if (event.key === 'ArrowRight') return context.forward ? 'forward' : null;
  }
  if (!event.ctrlKey && !event.metaKey && !event.altKey && !event.shiftKey && event.key === 'Escape') return context.activeWork ? 'cancel' : null;
  return null;
}
