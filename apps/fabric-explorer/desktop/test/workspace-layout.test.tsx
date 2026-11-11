// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Pane geometry is pure; real React splitter handlers expose only session width changes. */
import { createElement } from 'react';
import type { ReactElement } from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import { expect, it, vi } from 'vitest';
import { PaneSplitter, splitterStep, workspaceGeometry } from '../src/renderer/workspace-layout.js';
import type { PaneSplitterProps } from '../src/renderer/workspace-layout.js';
it('reserves graph space and clamps both side minima at the exact drawer boundary', () => {
  expect(workspaceGeometry(1240, true, true)).toMatchObject({ drawer: false, navigation: 276, inspector: 340 });
  expect(workspaceGeometry(904, true, true, 900, 900)).toMatchObject({ drawer: false, navigation: 240, inspector: 280 });
  expect(workspaceGeometry(903, true, true).drawer).toBe(true);
  for (const width of [904, 950, 1240, 1800]) { const value = workspaceGeometry(width, true, true, 10000, 10000); expect(value.navigation + value.inspector + 384).toBeLessThanOrEqual(width); }
  expect(workspaceGeometry(NaN, true, true)).toMatchObject({ navigation: 276, inspector: 340 });
});
it('retains only requested visible pane geometry and does not mutate session inputs', () => {
  expect(workspaceGeometry(1240, false, true).navigation).toBe(0); expect(workspaceGeometry(1240, true, false).inspector).toBe(0);
  const widths = { left: 300, right: 360 }; workspaceGeometry(904, true, true, widths.left, widths.right); expect(widths).toEqual({ left: 300, right: 360 });
});
it('matches physical boundary direction, exact keyboard steps, reset and min/max', () => {
  expect(splitterStep('ArrowRight', 300, 'navigation', 240, 500)).toBe(308); expect(splitterStep('ArrowRight', 300, 'inspector', 280, 500)).toBe(292);
  expect(splitterStep('ArrowLeft', 300, 'inspector', 280, 500, true)).toBe(332); expect(splitterStep('Home', 300, 'navigation', 240, 500)).toBe(240);
  expect(splitterStep('End', 300, 'inspector', 280, 500)).toBe(500); expect(splitterStep('Enter', 300, 'navigation', 240, 500)).toBe(276);
  expect(splitterStep('ArrowLeft', 240, 'navigation', 240, 500)).toBe(240); expect(splitterStep('Unrelated', 300, 'navigation', 240, 500)).toBeNull();
});
it('captures a pointer and clamps actual splitter movement without invoking graph operations', () => {
  const change = vi.fn(); let tree!: ReactElement<Record<string, unknown>>;
  const props: PaneSplitterProps = { side: 'inspector', width: 340, maximum: 500, onChange: change };
  function Mounted() { tree = PaneSplitter(props); return tree; }
  const html = renderToStaticMarkup(createElement(Mounted)); expect(html).toContain('role="separator"'); expect(html).toContain('aria-orientation="vertical"'); expect(html).toContain('aria-valuemin="280"');
  const target = { focus: vi.fn(), setPointerCapture: vi.fn(), hasPointerCapture: () => true, releasePointerCapture: vi.fn() };
  (tree.props.onPointerDown as (event: unknown) => void)({ button: 0, pointerId: 7, clientX: 400, currentTarget: target, preventDefault() {} });
  (tree.props.onPointerMove as (event: unknown) => void)({ pointerId: 7, clientX: 1000 }); expect(change).toHaveBeenLastCalledWith(280);
  (tree.props.onPointerMove as (event: unknown) => void)({ pointerId: 8, clientX: 0 }); expect(change).toHaveBeenCalledOnce();
  (tree.props.onPointerUp as (event: unknown) => void)({ currentTarget: target }); expect(target.releasePointerCapture).toHaveBeenCalledWith(7);
});
