// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Controlled native ownership and focus-loss ordering; no OS focus success is simulated. */
import { expect, it } from 'vitest';
import { NativeInput } from './native-input.js';
import type { InputOwnership } from './native-input.js';
function fixture() { let state: InputOwnership = { windowFocused: true, contentsFocused: true, documentFocused: true, targetActive: true, targetVisible: true, targetEnabled: true }; const calls: string[] = []; let disableAfterTab = false; const input = new NativeInput({ acquire: () => { calls.push('acquire'); }, paint: async () => { calls.push('paint'); }, focus: async () => { calls.push('focus'); }, ownership: async () => state, send: key => { calls.push(key); if (key === 'Tab' && disableAfterTab) state = { ...state, targetEnabled: false }; }, acceptActive: async () => { calls.push('accept'); }, insert: async () => { calls.push('insert'); } }); return { input, calls, landingAriaDisabled: () => { disableAfterTab = true; }, change: (patch: Partial<InputOwnership>) => { state = { ...state, ...patch }; } }; }
it('establishes native focus and paint before exact target verification and input', async () => { const t = fixture(); await t.input.focus('target'); await t.input.key('Enter'); expect(t.calls).toEqual(['acquire', 'paint', 'focus', 'paint', 'Enter', 'paint', 'accept']); });
it.each(['windowFocused', 'contentsFocused', 'documentFocused', 'targetActive', 'targetVisible', 'targetEnabled'] as const)('rejects lost %s before key delivery', async field => { const t = fixture(); t.change({ [field]: false }); await expect(t.input.key('Enter')).rejects.toThrow('ownership'); expect(t.calls).not.toContain('Enter'); });
it('checks ownership again after focus and before inserted text', async () => { const t = fixture(); await t.input.focus('target'); t.change({ targetActive: false }); await expect(t.input.insert('text')).rejects.toThrow('ownership'); expect(t.calls).not.toContain('insert'); });

it('commits native choices with Tab and verifies a different next focus without popup Enter', async () => { const t = fixture(); await t.input.choice('select', 1, 3, async () => true); expect(t.calls.filter(item => ['Home', 'Down', 'End', 'Tab', 'Enter'].includes(item))).toEqual(['Home', 'Down', 'Tab']); });
it('rejects uncommitted native choice and invalid option addresses without retrying', async () => { const t = fixture(); await expect(t.input.choice('select', 2, 3, async () => false)).rejects.toThrow('committed'); expect(t.calls.filter(item => item === 'Tab')).toHaveLength(1); await expect(t.input.choice('select', -1, 3, async () => true)).rejects.toThrow('unavailable'); });

it('does not claim native focus just because a request was issued', async () => { const t = fixture(); t.change({ windowFocused: false }); await expect(t.input.focus('target')).rejects.toThrow('ownership'); expect(t.calls).toEqual(['acquire', 'paint']); });

it('accepts Tab landing on a focusable aria-disabled paging control while still rejecting activation', async () => { const t = fixture(); t.landingAriaDisabled(); await t.input.choice('select', 1, 3, async () => true); await expect(t.input.key('Enter')).rejects.toThrow('ownership'); await expect(t.input.key('Tab')).resolves.toBeUndefined(); });
it('permits Escape navigation from a newly disabled refresh control without enabling activation or typing', async () => { const t = fixture(); t.change({ targetEnabled: false }); await expect(t.input.key('Escape')).resolves.toBeUndefined(); await expect(t.input.key('Space')).rejects.toThrow('ownership'); await expect(t.input.insert('text')).rejects.toThrow('ownership'); });

import { saveChangedPreferences } from './native-input.js';
it('skips redundant preference writes but does not mistake existing light appearance for persisted light', async () => {
  const calls: string[] = []; const desired = { theme: 'light', reducedMotion: false }; let current = { theme: 'system', reducedMotion: false };
  const port = { persisted: async () => current, activate: async () => { calls.push('save'); }, completed: async (requested: typeof desired) => { calls.push('observe-persisted-and-resolved'); current = requested; } };
  expect(await saveChangedPreferences(desired, port)).toBe('saved'); expect(calls).toEqual(['save', 'observe-persisted-and-resolved']); expect(await saveChangedPreferences(desired, port)).toBe('unchanged'); expect(calls).toHaveLength(2);
});
it('requires completion for motion and theme changes and propagates incomplete state instead of accepting an old Saved status', async () => {
  for (const desired of [{ theme: 'light', reducedMotion: true }, { theme: 'dark', reducedMotion: false }]) {
    let activated = 0; await expect(saveChangedPreferences(desired, { persisted: async () => ({ theme: 'light', reducedMotion: false }), activate: async () => { activated++; }, completed: async () => { throw new Error('Persisted or resolved values have not changed'); } })).rejects.toThrow('not changed'); expect(activated).toBe(1);
  }
});
