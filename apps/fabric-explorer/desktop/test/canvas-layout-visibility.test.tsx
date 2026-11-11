// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Pending-canvas markup/layout contract and actual SDK scheduled-size precondition; not native pixel qualification. */
import { expect, it, vi } from 'vitest';
import { readFileSync } from 'node:fs';
import { createElement } from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
vi.hoisted(() => { Object.defineProperty(globalThis, 'WebGL2RenderingContext', { configurable: true, value: { FLOAT: 5126, UNSIGNED_BYTE: 5121, UNSIGNED_SHORT: 5123, TRIANGLES: 4 } }); });
import Sigma from 'sigma';
import golden from '../../packages/contracts/test/fixtures/projection.json' with { type: 'json' };
import type { GraphProjection } from '@jai/fabric-explorer-contracts';
import { workspaceGeometry } from '../src/renderer/workspace-layout.js';
import { ExplorerApp } from '../src/renderer/app.js';
import { ExploreController } from '../src/renderer/presentation/controller.js';
import type { DesktopBridge } from '../src/shell/bridge.js';
it('keeps pending canvas geometry while making stale graphics invisible and noninteractive', () => {
  const api = {} as DesktopBridge; const state = { ...new ExploreController(api).getSnapshot(), projection: golden as GraphProjection, layout: null };
  const controller = { getSnapshot: () => state, subscribe: () => () => {} } as unknown as ExploreController;
  const html = renderToStaticMarkup(createElement(ExplorerApp, { api, presentation: controller }));
  const canvas = html.match(/<div[^>]*class="graph-canvas"[^>]*>/)?.[0]; expect(canvas).toBeDefined(); expect(canvas).not.toMatch(/\shidden(?:=|\s|>)/); expect(canvas).toContain('aria-hidden="true"'); expect(canvas).toContain('visibility:hidden'); expect(canvas).toContain('pointer-events:none');
  const css = readFileSync(new URL('../src/renderer/renderer.css', import.meta.url), 'utf8'); const rule = css.match(/\.graph-stage\s*\{([^}]+)\}/)?.[1]; expect(rule).toContain('min-width: 0'); expect(rule).toContain('min-height: 100px');
  expect(css).toMatch(/@media \(max-height: 560px\)[\s\S]*\.graph-stage\s*\{[^}]*min-height: 60px/);
  const geometry = workspaceGeometry(904, true, true); const graphWidth = 904 - geometry.navigation - geometry.inspector - 24; expect(Number.isFinite(graphWidth)).toBe(true); expect(graphWidth).toBe(360); expect(graphWidth).toBeGreaterThan(0);
});
it('allows actual SDK scheduled render sizing at the retained minimum geometry without invalid-container permission', () => {
  let next: FrameRequestCallback | null = null; vi.stubGlobal('requestAnimationFrame', (callback: FrameRequestCallback) => { next = callback; return 1; }); vi.stubGlobal('window', { devicePixelRatio: 1 });
  try {
    const receiver = { container: { offsetWidth: 360, offsetHeight: 60 }, width: 360, height: 60, internals: { settings: { allowInvalidContainer: false }, pixelRatio: 1 }, renderFrame: 0, render: () => Sigma.prototype.resize.call(receiver as unknown as Sigma) };
    Sigma.prototype.scheduleRender.call(receiver as unknown as Sigma); expect(next).not.toBeNull(); expect(() => next!(0)).not.toThrow(); expect(receiver.internals.settings.allowInvalidContainer).toBe(false);
  } finally { vi.unstubAllGlobals(); }
});

it('observes the actual SDK public resize invalidating backing pixels without drawing primitives', () => {
  vi.stubGlobal('window', { devicePixelRatio: 1 }); let visibleBodies = true; const attributes: string[] = []; const emitted: string[] = [];
  try {
    const receiver = { container: { offsetWidth: 640, offsetHeight: 400 }, width: 320, height: 200, internals: { settings: { allowInvalidContainer: false }, pixelRatio: 1 }, labelRenderer: { labelsDirty: false }, mouseLayer: { style: {} }, extraElements: {}, stageCanvas: { setAttribute: (key: string) => { attributes.push(key); visibleBodies = false; } }, webGLContext: { viewport() {} }, emit: (event: string) => { emitted.push(event); } };
    Sigma.prototype.resize.call(receiver as unknown as Sigma); expect(attributes).toEqual(['width', 'height']); expect(visibleBodies).toBe(false); expect(emitted).toEqual(['resize']); expect(receiver.width).toBe(640); expect(receiver.height).toBe(400);
  } finally { vi.unstubAllGlobals(); }
});
it('does not call a worker layout alone a committed usable graph', () => {
  const api = {} as DesktopBridge;
  const state = { ...new ExploreController(api).getSnapshot(), projection: golden as GraphProjection, layout: { binding: golden.snapshot } };
  const controller = { getSnapshot: () => state, subscribe: () => () => {} } as unknown as ExploreController;
  const html = renderToStaticMarkup(createElement(ExplorerApp, { api, presentation: controller }));
  expect(html).toContain('data-canvas-ready="false"'); expect(html).toContain('Preparing graph display...'); expect(html).toContain('aria-busy="true"');
  expect(html.match(/<button[^>]*id="fit-graph"[^>]*>/)?.[0]).toContain('disabled');
  expect(html.match(/<div[^>]*class="graph-canvas"[^>]*>/)?.[0]).toContain('opacity:0');
});
