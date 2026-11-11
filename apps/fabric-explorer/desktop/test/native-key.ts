// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Exact development-only Electron keyboard event encoding, separate from native focus ownership. */
/** One native keyboard event with literal character data and fixed test modifiers. */
export interface NativeKeyEvent { readonly type: 'keyDown' | 'char' | 'keyUp'; readonly keyCode: string; readonly modifiers: readonly string[] }
/**
 * Encode one complete native keyboard action, preserving its actual character event.
 * @param keyCode Electron native key name.
 * @param modifiers Fixed caller-selected native modifiers.
 * @param character Explicit typing character, if any.
 * @returns Ordered native key events used directly by the Electron sender.
 */
export function nativeKeyEvents(keyCode: string, modifiers: readonly string[], character?: string): readonly NativeKeyEvent[] {
  const events: NativeKeyEvent[] = [{ type: 'keyDown', keyCode, modifiers: [...modifiers] }];
  const text = character ?? (keyCode === 'Enter' ? '\r' : undefined);
  if (text) events.push({ type: 'char', keyCode: text, modifiers: [...modifiers] });
  events.push({ type: 'keyUp', keyCode, modifiers: [...modifiers] }); return events;
}
