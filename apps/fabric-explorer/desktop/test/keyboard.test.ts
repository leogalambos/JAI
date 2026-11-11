// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Exact shortcut classification, including Orca structural modifiers and native editing exclusions. */
import { describe, expect, it } from 'vitest';
import { keyboardAction } from '../src/renderer/keyboard.js';
import type { ShortcutContext, ShortcutEvent } from '../src/renderer/keyboard.js';
const enabled: ShortcutContext = { editing: false, search: true, fit: true, back: true, forward: true, activeWork: true };
const event = (key: string, changes: Partial<ShortcutEvent> = {}): ShortcutEvent => ({ key, ctrlKey: false, metaKey: false, altKey: false, shiftKey: false, defaultPrevented: false, isComposing: false, repeat: false, ...changes });
describe('safe application shortcuts', () => {
  it.each(['ctrlKey', 'metaKey'] as const)('uses exact %s modifiers for search and fit', primary => {
    expect(keyboardAction(event('k', { [primary]: true }), enabled)).toBe('search'); expect(keyboardAction(event('F', { [primary]: true, shiftKey: true }), enabled)).toBe('fit');
    expect(keyboardAction(event('k', { [primary]: true, shiftKey: true }), enabled)).toBeNull(); expect(keyboardAction(event('f', { [primary]: true }), enabled)).toBeNull(); expect(keyboardAction(event('k', { ctrlKey: true, metaKey: true }), enabled)).toBeNull();
  });
  it('preserves Orca Alt+Shift structural table navigation and rejects extra history modifiers', () => {
    expect(keyboardAction(event('ArrowLeft', { altKey: true }), enabled)).toBe('back'); expect(keyboardAction(event('ArrowRight', { altKey: true }), enabled)).toBe('forward');
    for (const key of ['ArrowLeft', 'ArrowRight']) for (const modifier of ['shiftKey', 'ctrlKey', 'metaKey'] as const) expect(keyboardAction(event(key, { altKey: true, [modifier]: true }), enabled)).toBeNull();
  });
  it.each(['defaultPrevented', 'isComposing', 'repeat'] as const)('never consumes %s events', flag => {
    expect(keyboardAction(event('k', { ctrlKey: true, [flag]: true }), enabled)).toBeNull(); expect(keyboardAction(event('Escape', { [flag]: true }), enabled)).toBeNull();
  });
  it('does not steal native editing keys, bare characters or inactive actions', () => {
    for (const input of [event('k', { ctrlKey: true }), event('F', { ctrlKey: true, shiftKey: true }), event('ArrowLeft', { altKey: true }), event('Escape')]) expect(keyboardAction(input, { ...enabled, editing: true })).toBeNull();
    for (const key of ['/', 'f', 'F', 'k']) expect(keyboardAction(event(key), enabled)).toBeNull();
    expect(keyboardAction(event('k', { ctrlKey: true }), { ...enabled, search: false })).toBeNull(); expect(keyboardAction(event('F', { ctrlKey: true, shiftKey: true }), { ...enabled, fit: false })).toBeNull();
    expect(keyboardAction(event('ArrowLeft', { altKey: true }), { ...enabled, back: false })).toBeNull(); expect(keyboardAction(event('ArrowRight', { altKey: true }), { ...enabled, forward: false })).toBeNull();
  });
  it('cancels only active work with an unmodified Escape outside native editing', () => {
    expect(keyboardAction(event('Escape'), enabled)).toBe('cancel'); expect(keyboardAction(event('Escape'), { ...enabled, activeWork: false })).toBeNull();
    for (const modifier of ['ctrlKey', 'metaKey', 'altKey', 'shiftKey'] as const) expect(keyboardAction(event('Escape', { [modifier]: true }), enabled)).toBeNull();
  });
});
