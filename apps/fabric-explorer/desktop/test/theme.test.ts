// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Resolved shipped theme contrast and controlled matchMedia ownership tests, not rendered visual qualification. */
import { describe, expect, it } from 'vitest';
import { readFileSync } from 'node:fs';
import { DARK_THEME, LIGHT_THEME, observeTheme, resolveTheme } from '../src/renderer/theme.js';
import type { ResolvedTheme, ThemeMedia, ThemePreference } from '../src/renderer/theme.js';
function luminance(hex: string): number { const values = [1, 3, 5].map(start => { const value = parseInt(hex.slice(start, start + 2), 16) / 255; return value <= 0.04045 ? value / 12.92 : ((value + 0.055) / 1.055) ** 2.4; }); return values[0]! * 0.2126 + values[1]! * 0.7152 + values[2]! * 0.0722; }
function contrast(left: string, right: string): number { const values = [luminance(left), luminance(right)].sort((a, b) => b - a); return (values[0]! + 0.05) / (values[1]! + 0.05); }
describe('shared resolved CSS and canvas themes', () => {
  it.each([LIGHT_THEME, DARK_THEME])('keeps actual secondary header command declarations readable in $name rather than inheriting header text', theme => {
    const css = readFileSync(new URL('../src/renderer/renderer.css', import.meta.url), 'utf8');
    const control = css.match(/button, select, input\[type=text\], input\[type=number\]\s*\{([^}]+)\}/)?.[1]; const header = css.match(/\n\.app-header\s*\{([^}]+)\}/)?.[1];
    expect(control).toBeDefined(); expect(header).toBeDefined();
    const declaration = (block: string, name: string) => block.match(new RegExp(`(?:^|;)\\s*${name}:\\s*([^;]+);`))?.[1]?.trim();
    const resolve = (value: string | undefined): string => { const token = value?.match(/^var\((--[a-z-]+)\)$/)?.[1]; if (!token || !theme.css[token]) throw new Error('Unrecognized control color declaration.'); return theme.css[token]!; };
    const foreground = declaration(control!, 'color') === 'inherit' ? resolve(declaration(header!, 'color')) : resolve(declaration(control!, 'color'));
    // Enabled secondary controls use their own surface; disabled secondary controls use the muted token without opacity.
    for (const background of [resolve(declaration(control!, 'background')), theme.css['--surface']!, theme.css['--selected']!]) expect(contrast(foreground, background)).toBeGreaterThanOrEqual(4.5);
    const disabled = css.match(/button:disabled, \[aria-disabled=true\]\s*\{([^}]+)\}/)?.[1]; expect(disabled).toBeDefined();
    for (const background of [theme.css['--surface']!, theme.css['--selected']!, theme.css['--background']!]) expect(contrast(resolve(declaration(disabled!, 'color')), background)).toBeGreaterThanOrEqual(4.5);
    expect(css).toMatch(/button\.primary\s*\{[^}]*color:\s*var\(--on-accent\)/); expect(css).not.toMatch(/opacity\s*:/);
  });
  it.each([LIGHT_THEME, DARK_THEME])('meets the project text contrast minimum in $name, including disabled text without opacity reduction', theme => {
    const color = (key: string) => theme.css[key]!;
    for (const [foreground, background] of [['--text', '--background'], ['--text', '--surface'], ['--text', '--selected'], ['--text', '--canvas'], ['--muted', '--surface'], ['--muted', '--background'], ['--muted', '--selected'], ['--muted', '--canvas'], ['--on-accent', '--accent'], ['--warning-text', '--warning-background'], ['--error-text', '--error-background'], ['--header-text', '--header-background'], ['--header-muted', '--header-background']]) expect(contrast(color(foreground!), color(background!))).toBeGreaterThanOrEqual(4.5);
    expect(contrast(theme.canvas.labelText, theme.canvas.labelBackground)).toBeGreaterThanOrEqual(4.5);
    for (const key of ['node', 'finding', 'unresolved', 'edge', 'selected'] as const) expect(contrast(theme.canvas[key], theme.canvas.background)).toBeGreaterThanOrEqual(3);
  });
  it('resolves light/dark/system without modifying the persisted preference or accepting another value', () => {
    expect(resolveTheme('light', true)).toBe(LIGHT_THEME); expect(resolveTheme('dark', false)).toBe(DARK_THEME); expect(resolveTheme('system', false)).toBe(LIGHT_THEME); expect(resolveTheme('system', true)).toBe(DARK_THEME);
    expect(() => resolveTheme('other' as ThemePreference, false)).toThrow(RangeError); expect(Object.isFrozen(DARK_THEME.canvas)).toBe(true);
  });
  it('tracks live system changes, releases the exact listener and ignores late queued observations', () => {
    let listener: ((event: { matches: boolean }) => void) | null = null; let removed: unknown = null;
    const media: ThemeMedia = { matches: false, addEventListener(_type, next) { listener = next; }, removeEventListener(_type, prior) { removed = prior; } };
    const themes: ResolvedTheme[] = []; const stop = observeTheme('system', media, theme => themes.push(theme)); const saved = listener!;
    saved({ matches: true }); expect(themes).toEqual([LIGHT_THEME, DARK_THEME]); stop(); stop(); expect(removed).toBe(saved); saved({ matches: false }); expect(themes).toHaveLength(2);
  });
  it('does not subscribe fixed preferences or mutate a system choice during publication', () => {
    const subscriptions: unknown[] = []; const media: ThemeMedia = { matches: true, addEventListener(_type, listener) { subscriptions.push(listener); }, removeEventListener() {} };
    const themes: ResolvedTheme[] = []; observeTheme('light', media, value => themes.push(value))(); expect(themes).toEqual([LIGHT_THEME]); expect(subscriptions).toEqual([]);
    const preferences = Object.freeze({ theme: 'system' as const }); observeTheme(preferences.theme, media, value => themes.push(value))(); expect(preferences.theme).toBe('system');
  });
  it('keeps CSS startup colors consistent and preserves text contrast for disabled and primary hover controls', () => {
    const css = readFileSync(new URL('../src/renderer/renderer.css', import.meta.url), 'utf8');
    const startup = Object.fromEntries([...css.matchAll(/^\s*(--[a-z-]+):\s*(#[a-f0-9]{6});/gm)].map(match => [match[1], match[2]]));
    expect(startup).toEqual(LIGHT_THEME.css); expect(css).not.toMatch(/opacity\s*:/); expect(css).toContain('color: var(--on-accent)'); expect(css).toContain('button:hover:not(:disabled):not([aria-disabled=true]):not(.primary)');
  });
});
