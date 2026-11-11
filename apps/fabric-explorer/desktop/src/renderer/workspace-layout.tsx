// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Session-only workspace geometry and pointer/keyboard resizing, independent of graph state. */
import { useRef } from 'react';

/** Pane geometry derived from the current available CSS-pixel width. */
export interface WorkspaceGeometry { readonly drawer: boolean; readonly navigation: number; readonly inspector: number; readonly navigationMax: number; readonly inspectorMax: number }
/**
 * Clamp requested pane widths while reserving 360px for the graph and two 12px separators.
 * @param width Available CSS pixels; nonfinite values use the 1240px design baseline.
 * @param navigation Whether the navigation pane is requested in desktop layout.
 * @param inspector Whether the inspector pane is requested in desktop layout.
 * @param left Session navigation width preference, without persistence.
 * @param right Session inspector width preference, without persistence.
 * @returns Safe widths and drawer mode when both side minima cannot fit.
 */
export function workspaceGeometry(width: number, navigation: boolean, inspector: boolean, left = 276, right = 340): WorkspaceGeometry {
  const available = Number.isFinite(width) ? Math.max(0, width) : 1240;
  const minimum = 360 + (navigation ? 252 : 0) + (inspector ? 292 : 0);
  const drawer = available < 904;
  const clamp = (value: number, min: number, max: number) => Math.min(max, Math.max(min, Number.isFinite(value) ? value : min));
  if (drawer) return { drawer, navigation: clamp(left, 240, Math.max(240, available - 40)), inspector: clamp(right, 280, Math.max(280, available - 40)), navigationMax: Math.max(240, available - 40), inspectorMax: Math.max(280, available - 40) };
  const total = Math.max(minimum, available); const navigationMax = total - 360 - (navigation ? 12 : 0) - (inspector ? 292 : 0);
  const nav = navigation ? clamp(left, 240, navigationMax) : 0;
  const inspectorMax = total - 360 - (inspector ? 12 : 0) - (navigation ? nav + 12 : 0);
  const detail = inspector ? clamp(right, 280, inspectorMax) : 0;
  return { drawer, navigation: nav, inspector: detail, navigationMax: total - 360 - (navigation ? 12 : 0) - (inspector ? detail + 12 : 0), inspectorMax };
}
/**
 * Compute one horizontal splitter keyboard step without changing graph or preference state.
 * @param key Native key name.
 * @param width Current adjacent pane width.
 * @param side Pane side; moving a right boundary right reduces inspector width.
 * @param minimum Minimum pane width.
 * @param maximum Current layout maximum.
 * @param shifted Whether Shift requests the 32px rather than 8px step.
 * @returns Clamped next width, reset default on Enter, or null for an unrelated key.
 */
export function splitterStep(key: string, width: number, side: 'navigation' | 'inspector', minimum: number, maximum: number, shifted = false): number | null {
  const delta = (shifted ? 32 : 8) * (side === 'navigation' ? 1 : -1);
  const next = key === 'ArrowRight' ? width + delta : key === 'ArrowLeft' ? width - delta : key === 'Home' ? minimum : key === 'End' ? maximum : key === 'Enter' ? side === 'navigation' ? 276 : 340 : null;
  return next === null ? null : Math.max(minimum, Math.min(maximum, next));
}
/** A separator changes only one session-local pane width. */
export interface PaneSplitterProps {
  readonly side: 'navigation' | 'inspector';
  readonly width: number;
  readonly maximum: number;
  readonly hidden?: boolean;
  readonly onChange: (width: number) => void;
}
/**
 * Render a visible-grip splitter supporting captured mouse/touch dragging and keyboard steps.
 * @param props Current bounded geometry and a session-only width publisher.
 * @returns Focusable vertical separator; Enter or double-click resets its default width.
 */
export function PaneSplitter({ side, width, maximum, hidden, onChange }: PaneSplitterProps) {
  const drag = useRef<{ id: number; start: number; width: number } | null>(null); const minimum = side === 'navigation' ? 240 : 280;
  const stop = (target: HTMLDivElement) => { const active = drag.current; drag.current = null; if (active && target.hasPointerCapture(active.id)) target.releasePointerCapture(active.id); };
  return <div id={`${side}-splitter`} className={`pane-splitter ${side}-splitter`} role="separator" aria-label={`${side === 'navigation' ? 'Navigation' : 'Inspector'} width`} aria-orientation="vertical" aria-controls={side === 'navigation' ? 'navigation-content' : 'evidence-content'} aria-valuemin={minimum} aria-valuemax={Math.round(maximum)} aria-valuenow={Math.round(width)} aria-valuetext={`${Math.round(width)} pixels. Arrow keys resize; Enter resets.`} tabIndex={0} hidden={hidden}
    onPointerDown={event => { if (event.button !== 0) return; event.preventDefault(); event.currentTarget.focus(); drag.current = { id: event.pointerId, start: event.clientX, width }; event.currentTarget.setPointerCapture(event.pointerId); }}
    onPointerMove={event => { const active = drag.current; if (!active || active.id !== event.pointerId) return; const next = active.width + (event.clientX - active.start) * (side === 'navigation' ? 1 : -1); onChange(Math.max(minimum, Math.min(maximum, next))); }}
    onPointerUp={event => stop(event.currentTarget)} onPointerCancel={event => stop(event.currentTarget)} onLostPointerCapture={() => { drag.current = null; }}
    onDoubleClick={() => onChange(splitterStep('Enter', width, side, minimum, maximum)!)} onKeyDown={event => { if (event.altKey || event.ctrlKey || event.metaKey || event.nativeEvent.isComposing) return; const next = splitterStep(event.key, width, side, minimum, maximum, event.shiftKey); if (next !== null) { event.preventDefault(); event.stopPropagation(); onChange(next); } else if (event.key === 'Escape' && drag.current) { event.preventDefault(); event.stopPropagation(); const original = drag.current.width; stop(event.currentTarget); onChange(original); } }}><span aria-hidden="true"/></div>;
}
