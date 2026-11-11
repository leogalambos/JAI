// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Owned facade around the selected Sigma public API; no dependency internals are patched. */
import Sigma from 'sigma';
import { CAMERA_LIMITS } from './camera.js';
import type { AbstractGraph } from 'graphology-types';
import type { SigmaOptions } from 'sigma/types';
import { pathLine, pathCurved, pathLoop, extremityArrow, layerPlain, sdfCircle, sdfDiamond, sdfTriangle } from 'sigma/rendering';
/** Fixed renderer events used by the canvas lifetime. */
export type CanvasEvent = 'clickNode' | 'clickEdge' | 'clickStage' | 'enterEdge' | 'leaveEdge' | 'enterNode' | 'leaveNode' | 'afterRender' | 'resize' | 'webglContextLost';
/** Camera state uses normalized graph coordinates and a positive zoom ratio. */
export interface CanvasCameraState { readonly x: number; readonly y: number; readonly angle: number; readonly ratio: number }
/** App-owned rendering boundary; unit tests substitute this collaborator, never Sigma internals. */
export interface CanvasRenderer {
  /** Listen only to the fixed public event vocabulary. */
  on(event: CanvasEvent, callback: (payload?: unknown) => void): void;
  /** Remove a previously installed owned listener. */
  off(event: CanvasEvent, callback: (payload?: unknown) => void): void;
  /** Refresh the original Graphology instance after public mutations. */
  refresh(): void;
  /** Recompute the owned stage dimensions after a container resize. */
  resize(): void;
  /** Read CSS-pixel viewport dimensions. */
  dimensions(): { width: number; height: number };
  /** Convert source layout coordinates to current CSS-pixel viewport coordinates. */
  project(point: { x: number; y: number }): { x: number; y: number };
  /** Convert layout coordinates to normalized camera coordinates. */
  normalize(point: { x: number; y: number }): { x: number; y: number };
  /** Read the active public camera state. */
  camera(): CanvasCameraState;
  /** Set a bounded camera state without an asynchronous animation publication. */
  move(state: Partial<CanvasCameraState>): void;
  /** Read active node size/color after public SDK styles and application reducers. */
  nodeData(id: string): { readonly size: number; readonly color: string; readonly shape?: string } | undefined;
  /** Read the public active display values after SDK parallel-path resolution. */
  edgeData(id: string): Record<string, unknown> | undefined;
  /** Convert a graph style radius to CSS pixels at the current zoom. */
  scaleSize(size: number): number;
  /** Release all SDK-owned GPU resources and internal observers. */
  kill(): void;
}
/** Trusted construction callback; callers cannot provide a renderer through the exposed application bridge. */
export interface CanvasRendererFactory { (graph: AbstractGraph, container: HTMLElement, options: SigmaOptions): CanvasRenderer }
/**
 * Build the pinned SDK's public primitive/style configuration for directed multigraphs.
 * @returns Fresh options with straight, curved, loop and arrow primitives, inert labels and no node dragging.
 * @throws {Error} If the browser lacks SDK-required WebGL2 constants during primitive construction.
 */
export function canvasOptions(): SigmaOptions {
  return {
    primitives: { nodes: { labelPrograms: false, shapes: [sdfCircle(), sdfDiamond(), sdfTriangle()] }, edges: { paths: [pathLine(), pathCurved(), pathLoop()], extremities: [extremityArrow()], layers: [layerPlain()], defaultHead: 'arrow' } },
    styles: {
      nodes: { x: { attribute: 'x' }, y: { attribute: 'y' }, shape: { attribute: 'shape' }, size: { attribute: 'size' }, color: { attribute: 'color' }, label: { attribute: 'label' } },
      edges: { color: { attribute: 'color' }, size: { attribute: 'size' }, label: { attribute: 'label' }, path: 'straight', parallelPath: 'curved', selfLoopPath: 'loop', parallelSpread: 0.35, head: 'arrow' },
    },
    settings: { enableEdgeEvents: true, nodeLabelEvents: false, renderLabels: false, renderEdgeLabels: false, enableNodeDrag: false, enableCameraRotation: false, enableCameraMouseRotation: false, minCameraRatio: CAMERA_LIMITS.minimum, maxCameraRatio: CAMERA_LIMITS.maximum, itemSizesReference: 'screen', zoomToSizeRatioFunction: () => 1, autoRescale: true, stagePadding: 48, edgePickingPadding: 4, nodePickingPadding: 3 },
  };
}
/**
 * Create the actual SDK renderer behind the application's owned facade.
 * @param graph Original directed multigraph retained for this renderer lifetime.
 * @param container Owned stage element, separate from the label overlay.
 * @param options Selected pinned public primitive/style settings.
 * @returns Public API forwarding adapter with no setGraph or internal patch path.
 * @throws {Error} For unavailable WebGL2 or invalid SDK/container configuration.
 */
export const createSigmaRenderer: CanvasRendererFactory = (graph, container, options) => {
  const sigma = new Sigma(graph, container, options);
  return { on: (event, callback) => { sigma.on(event, callback); }, off: (event, callback) => { sigma.removeListener(event, callback); }, refresh: () => { sigma.refresh(); }, resize: () => { sigma.resize(); }, dimensions: () => sigma.getDimensions(), project: point => sigma.graphToViewport(point), normalize: point => sigma.graphToFramedGraph(point), camera: () => sigma.getCamera().getState(), move: state => { sigma.getCamera().cancelAnimation().setState(state); }, nodeData: id => sigma.getNodeDisplayData(id), edgeData: id => sigma.getEdgeDisplayData(id) as unknown as Record<string, unknown> | undefined, scaleSize: size => sigma.scaleSize(size), kill: () => { sigma.kill(); } };
};
