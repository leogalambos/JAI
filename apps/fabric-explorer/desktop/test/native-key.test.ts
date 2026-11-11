// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Actual native sender encoder regression; focus-port mocks cannot prove emitted Electron events. */
import { expect, it } from 'vitest';
import { nativeKeyEvents } from './native-key.js';
it('encodes Enter activation as keyDown, carriage-return char and keyUp', () => { expect(nativeKeyEvents('Enter', [])).toEqual([{ type: 'keyDown', keyCode: 'Enter', modifiers: [] }, { type: 'char', keyCode: '\r', modifiers: [] }, { type: 'keyUp', keyCode: 'Enter', modifiers: [] }]); });
it('preserves an explicit typing character and modifiers without adding characters to navigation or Space', () => {
  expect(nativeKeyEvents('F', ['shift'], 'F')).toEqual([{ type: 'keyDown', keyCode: 'F', modifiers: ['shift'] }, { type: 'char', keyCode: 'F', modifiers: ['shift'] }, { type: 'keyUp', keyCode: 'F', modifiers: ['shift'] }]);
  for (const key of ['Tab', 'Down', 'Home', 'Escape', 'Space']) expect(nativeKeyEvents(key, []).map(event => event.type)).toEqual(['keyDown', 'keyUp']);
  expect(nativeKeyEvents('Space', []).at(-1)).toMatchObject({ type: 'keyUp', keyCode: 'Space' });
});
