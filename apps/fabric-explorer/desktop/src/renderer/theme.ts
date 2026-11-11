// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** One resolved presentation theme for CSS and canvas; stored preferences remain untouched. */
import type { CanvasPalette } from './canvas/palette.js';

/** Persisted presentation choice; system resolution is an observation, never a preference rewrite. */
export type ThemePreference = 'light' | 'dark' | 'system';
/** Concrete colors published together so controls and graph cannot resolve different themes. */
export interface ResolvedTheme { readonly name: 'light' | 'dark'; readonly css: Readonly<Record<string, string>>; readonly canvas: CanvasPalette }
/** Owned matchMedia boundary, allowing deterministic system-theme tests without browser mocks. */
export interface ThemeMedia {
  readonly matches: boolean;
  /** Subscribe to observed system appearance changes. */
  addEventListener(type: 'change', listener: (event: { readonly matches: boolean }) => void): void;
  /** Release the exact previously subscribed listener. */
  removeEventListener(type: 'change', listener: (event: { readonly matches: boolean }) => void): void;
}
/** Shipped light colors; every text state uses an explicit foreground/background pair. */
export const LIGHT_THEME: ResolvedTheme = Object.freeze({ name: 'light', css: Object.freeze({
  '--text': '#192d40', '--background': '#f3f6f9', '--surface': '#ffffff', '--border': '#71869a', '--muted': '#40566b', '--accent': '#145ba8', '--on-accent': '#ffffff', '--canvas': '#f8fafc', '--selected': '#e4efff', '--focus': '#145ba8',
  '--warning-text': '#673700', '--warning-background': '#fff3dd', '--warning-border': '#8a4500', '--error-text': '#81202a', '--error-background': '#fff0f1', '--error-border': '#a62b35', '--header-background': '#122a42', '--header-text': '#ffffff', '--header-muted': '#ccdeef',
}), canvas: Object.freeze({ background: '#f8fafc', node: '#235d91', finding: '#9b2c65', unresolved: '#8a5815', edge: '#65768a', selected: '#123a63', labelBackground: '#ffffff', labelText: '#162b43', labelBorder: '#66788a' }) });
/** Shipped dark colors, including primary-button text independent of the light theme. */
export const DARK_THEME: ResolvedTheme = Object.freeze({ name: 'dark', css: Object.freeze({
  '--text': '#dfebf6', '--background': '#142334', '--surface': '#1a2c3f', '--border': '#8fa5bb', '--muted': '#b2c4d5', '--accent': '#8cc4ff', '--on-accent': '#102338', '--canvas': '#152536', '--selected': '#264461', '--focus': '#8cc4ff',
  '--warning-text': '#ffe0a8', '--warning-background': '#3a2c14', '--warning-border': '#d99c43', '--error-text': '#ffd6dc', '--error-background': '#44252c', '--error-border': '#ff8e9f', '--header-background': '#102033', '--header-text': '#f0f5fa', '--header-muted': '#ccdeef',
}), canvas: Object.freeze({ background: '#152536', node: '#a8d2ff', finding: '#f4aed6', unresolved: '#ffd493', edge: '#9fb7cc', selected: '#ffffff', labelBackground: '#1a2c3f', labelText: '#f0f5fa', labelBorder: '#9fb7cc' }) });

/**
 * Resolve a trusted preference without modifying stored application state.
 * @param preference Persisted light, dark or system choice.
 * @param systemDark Whether the observed system appearance is dark.
 * @returns Existing frozen concrete theme shared by CSS and canvas.
 * @throws {RangeError} For an unsupported preference.
 */
export function resolveTheme(preference: ThemePreference, systemDark: boolean): ResolvedTheme {
  if (!['light', 'dark', 'system'].includes(preference)) throw new RangeError('Invalid theme preference.');
  return preference === 'dark' || preference === 'system' && systemDark ? DARK_THEME : LIGHT_THEME;
}
/**
 * Publish current appearance and follow live system changes only while system is selected.
 * @param preference Stored choice, retained unchanged throughout observation.
 * @param media Owned browser appearance-query port.
 * @param publish Receives the complete resolved theme; no native exception text is generated.
 * @returns Idempotent cleanup that also ignores any late queued change event.
 * @throws {RangeError} For an unsupported preference before any subscription is added.
 */
export function observeTheme(preference: ThemePreference, media: ThemeMedia, publish: (theme: ResolvedTheme) => void): () => void {
  publish(resolveTheme(preference, media.matches)); let active = true;
  const listener = (event: { readonly matches: boolean }) => { if (active) publish(resolveTheme(preference, event.matches)); };
  if (preference === 'system') media.addEventListener('change', listener);
  return () => { if (!active) return; active = false; if (preference === 'system') media.removeEventListener('change', listener); };
}
