// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Display-only style callbacks shared by the adapter and actual SDK contract tests. */
import { DEFAULT_CANVAS_PALETTE } from './palette.js';
import type { CanvasPalette } from './palette.js';
import type { SigmaOptions } from 'sigma/types';
/**
 * Create active theme/selection reducers without changing semantic graph attributes.
 * @param selected Read the current exact selected ID, or null.
 * @param palette Read the current frozen resolved presentation colors.
 * @returns Public Sigma reducer callbacks using the current presentation selection.
 */
export function canvasReducers(selected: () => string | null, palette: () => CanvasPalette = () => DEFAULT_CANVAS_PALETTE): Pick<SigmaOptions, 'nodeReducer' | 'edgeReducer'> {
  return {
    nodeReducer: (key, _data, attrs) => { const colors = palette(); return key === selected() ? { color: colors.selected, size: Number(attrs.size) + 2, depth: 'topNodes' } : { color: attrs.kind === 'finding' ? colors.finding : attrs.kind === 'unresolved' ? colors.unresolved : colors.node }; },
    edgeReducer: key => key === selected() ? { color: palette().selected, size: 3, depth: 'topEdges' } : { color: palette().edge },
  };
}
