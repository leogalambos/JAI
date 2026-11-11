// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Retained selected-source loop observation calibrated against public SDK styles, display read and transforms. */
import { expect, it, vi } from 'vitest';
vi.hoisted(() => { Object.defineProperty(globalThis, 'WebGL2RenderingContext', { configurable: true, value: { FLOAT: 5126, UNSIGNED_BYTE: 5121, UNSIGNED_SHORT: 5123, TRIANGLES: 4 } }); });
import Sigma from 'sigma';
import { MultiDirectedGraph } from 'graphology';
import { evaluateNodeStyle } from 'sigma/types';
import { resolveSettings } from 'sigma/settings';
import { getMatrixImpact, matrixFromCamera, multiplyVec2 } from 'sigma/utils';
import { canvasOptions } from '../src/renderer/canvas/sdk.js';
import { canvasReducers } from '../src/renderer/canvas/styles.js';
import { edgeLabelAnchor, activeNodeSize } from '../src/renderer/canvas/display.js';
import type { CanvasNode, CanvasEdge } from '../src/renderer/canvas/model.js';
it('anchors a hovered loop to the active selected source size rather than its unchanged compact base size', () => {
  const graph = new MultiDirectedGraph(); const source: CanvasNode = { id: 'source', label: 'Source', x: 0.25, y: 0.5, size: 7, color: '#235d91', shape: 'circle', kind: 'version' }; graph.addNode(source.id, { ...source });
  const edge: CanvasEdge = { id: 'loop', from: source.id, to: source.id, label: 'Loop', color: '#65768a', size: 1.5 };
  const nodeState = { isHovered: false, isLabelHovered: false, isHidden: false, isHighlighted: false, isDragged: false };
  const graphState = { isIdle: true, isPanning: false, isZooming: false, isDragging: false, hasHovered: false, hasHighlighted: false };
  const options = canvasOptions(); const viewport = { width: 736, height: 400 }; const camera = { x: 0.5, y: 0.5, ratio: 1, angle: 0 }; const matrix = matrixFromCamera(camera, viewport, { width: 300, height: 1 }, 48); const settings = resolveSettings({});
  const css = (point: { x: number; y: number }) => { const clip = multiplyVec2(matrix, point); return { x: (1 + clip.x) * viewport.width / 2, y: (1 - clip.y) * viewport.height / 2 }; };
  const sizeReceiver = { camera, graphToViewportRatio: 1, internals: { settings }, getSetting: (key: keyof typeof settings) => settings[key] };
  const scaled = (size: number) => Sigma.prototype.scaleSize.call(sizeReceiver as unknown as Sigma, size);
  let selected: string | null = null; const reducers = canvasReducers(() => selected);
  for (const selection of [null, source.id]) {
    selected = selection;
    const active = evaluateNodeStyle(options.styles?.nodes, graph.getNodeAttributes(source.id), nodeState, graphState, graph);
    Object.assign(active, reducers.nodeReducer!(source.id, active, graph.getNodeAttributes(source.id), nodeState, graphState, graph));
    const receiver = { internals: { nodeDataCache: { [source.id]: active } } };
    const nodeData = (id: string) => Sigma.prototype.getNodeDisplayData.call(receiver as unknown as Sigma, id);
    expect(nodeData(source.id)?.size).toBe(selection ? 9 : 7);
    const facade = { normalize: (point: { x: number; y: number }) => point, project: css, scaleSize: scaled, edgeData: () => ({ loopRadius: 4 }), nodeData };
    const activeSize = nodeData(source.id)!.size;
    const worldRadius = activeSize * getMatrixImpact(matrix, camera, viewport) / (activeSize / scaled(activeSize)) * 4;
    const expected = css({ x: source.x, y: source.y + worldRadius });
    expect(edgeLabelAnchor(facade, edge, source, source)!.y).toBeCloseTo(expected.y, 5);
    expect(graph.getNodeAttribute(source.id, 'size')).toBe(7);
  }
});

it('defers labels when the active SDK display has not been created rather than guessing source size', () => {
  const source = { id: 'source', x: 0, y: 0, size: 7 } as CanvasNode; const edge = { id: 'loop', from: 'source', to: 'source' } as CanvasEdge;
  const facade = { normalize: (point: { x: number; y: number }) => point, project: (point: { x: number; y: number }) => point, scaleSize: (size: number) => size, edgeData: () => ({ loopRadius: 4 }), nodeData: () => undefined };
  expect(edgeLabelAnchor(facade, edge, source, source)).toBeNull();
});

it('reads finite positive active size and defers missing, zero or invalid SDK display values', () => {
  expect(activeNodeSize({ nodeData: () => ({ size: 9, color: '#123a63' }) }, 'source')).toBe(9);
  expect(activeNodeSize({ nodeData: () => undefined }, 'source')).toBeNull();
  for (const size of [0, -1, Infinity, NaN]) expect(activeNodeSize({ nodeData: () => ({ size, color: '#123a63' }) }, 'source')).toBeNull();
});
