// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Landscape composition regressions; actual viewport geometry and visual acceptance require native captures. */
import { createElement } from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import { readFileSync } from 'node:fs';
import { describe, expect, it, vi } from 'vitest';
vi.hoisted(() => { Object.defineProperty(globalThis, 'WebGL2RenderingContext', { configurable: true, value: { FLOAT: 5126, UNSIGNED_BYTE: 5121, UNSIGNED_SHORT: 5123, TRIANGLES: 4 } }); });
import { ExplorerApp } from '../src/renderer/app.js';
import { ExploreController } from '../src/renderer/presentation/controller.js';
import type { DesktopBridge } from '../src/shell/bridge.js';
import { tableProjection } from './element-table-fixtures.js';
const api = {} as DesktopBridge;
function render() { const presentation = new ExploreController(api); return renderToStaticMarkup(createElement(ExplorerApp, { api, presentation })); }
describe('landscape graph-first application composition', () => {
  it('makes menus, four navigation sections and both resizing boundaries discoverable without panel scrolling', () => {
    const html = render();
    expect(html).toContain('role="menubar"'); expect(html).toContain('aria-label="Application menu"');
    for (const id of ['menu-file', 'menu-view', 'menu-navigate', 'menu-help', 'tab-sources', 'tab-search', 'tab-findings', 'show-elements', 'navigation-splitter', 'inspector-splitter']) expect(html).toContain(`id="${id}"`);
    expect(html).toContain('role="tablist"'); expect(html).toContain('role="separator"');
  });
  it('places source details and semantic rows inside side panes rather than above or below the graph', () => {
    const html = render(); expect(html).toContain('class="app-shell ergonomic-shell"'); expect(html).toContain('id="navigation-content"'); expect(html).toContain('id="elements-content"');
    expect(html.indexOf('id="families"')).toBeGreaterThan(html.indexOf('id="main-workspace"'));
    expect(html.indexOf('Visible vertices in the current bounded graph projection')).toBeLessThan(html.indexOf('aria-label="Graph workspace"'));
  });
  it('keeps visible counts and completeness outside the compact disclosure while retaining snapshot/filter scope details', () => {
    const html = render(); expect(html).toContain('Snapshot totals'); expect(html).toContain('Filter matches'); expect(html).toContain('Visible graph'); expect(html).toContain('Select or search a starting point');
    expect(html.indexOf('Visible graph')).toBeLessThan(html.indexOf('class="graph-query-details"')); expect(html.indexOf('Hidden globally:')).toBeLessThan(html.indexOf('class="graph-query-details"')); expect(html.indexOf('Snapshot totals')).toBeGreaterThan(html.indexOf('class="graph-query-details"'));
  });
  it('provides named pane destinations and retained tab panels with a narrow-screen drawer policy', () => {
    const html = render(); for (const id of ['show-navigation', 'show-elements', 'show-graph', 'show-inspector']) expect(html).toContain(`id="${id}"`);
    for (const name of ['Navigation and elements', 'Evidence panel']) expect(html).toContain(`aria-label="${name}"`);
    const css = readFileSync(new URL('../src/renderer/renderer.css', import.meta.url), 'utf8');
    expect(css).toContain('.drawer-mode'); expect(css).toContain('scrollbar-gutter: stable'); expect(css).not.toMatch(/\.workspace\s*\{[^}]*flex-direction:\s*column/); expect(css).not.toMatch(/\.inspector\s*\{[^}]*grid-column:\s*1\s*\/\s*-1/);
  });
  it('does not confuse a small current neighbourhood with accepted snapshot totals or filter matches', () => {
    const projection = tableProjection(2, 1); const snapshot = { ...projection.snapshot, counts: { vertices: '360', edges: '641', findings: '6' } };
    const state = { ...new ExploreController(api).getSnapshot(), shell: { sessionId: 'session', capability: 'capability', snapshot, sources: [], report: null, stale: false, warning: null, preferences: { version: 1 as const, theme: 'light' as const, reducedMotion: false } }, projection: { ...projection, snapshot }, counts: { vertices: '12', edges: '20', findings: '1' } };
    const presentation = { getSnapshot: () => state, subscribe: () => () => {} } as unknown as ExploreController;
    const html = renderToStaticMarkup(createElement(ExplorerApp, { api, presentation }));
    expect(html).toContain('Snapshot totals</strong>: 360 vertices · 641 relations · 6 findings'); expect(html).toContain('data-testid="count-vertices">12</span>'); expect(html).toContain('Visible graph</strong>: 2 vertices · 1 relations');
    expect(html).toContain('not the entire snapshot'); expect(html.indexOf('Visible graph')).toBeLessThan(html.indexOf('class="graph-stage"'));
  });
});
