// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Ephemeral visible-layout contracts; numeric handles belong only to one sealed generation. */
import type { HandleProjection } from '../graph/types.js';
/** Exact current request/projection context; no layout position grants source authority. */
export interface LayoutBinding { readonly sessionId: string; readonly capability: string; readonly generation: string; readonly requestId: string; readonly projectionId: string }
/** Finite deterministic work configuration in abstract layout-space units. */
export interface LayoutOptions { readonly algorithm: 'layered' | 'force'; readonly seed: number; readonly iterations: number; readonly nodeSpacing: number; readonly layerSpacing: number; readonly maxWork: number }
/** Trusted caller supplies only an already bounded visible handle projection. */
export interface LayoutInput { readonly binding: LayoutBinding; readonly graph: HandleProjection; readonly options?: Partial<LayoutOptions> }
/** Cooperative cancellation works with AbortSignal or a root-owned atomic cancellation predicate. */
export interface LayoutControl {
  /** Optional native task cancellation signal. */
  readonly signal?: AbortSignal;
  /** Poll a root-owned atomic cancellation flag without changing graph state. */
  cancelled?(): boolean;
  /** Yield to the owning worker event loop so control messages can progress. */
  yieldControl?(): Promise<void>;
}
/** Layout-derived cycle grouping, addressed only together with the result's exact projection binding. */
export interface LayoutGroup { readonly id: number; readonly members: readonly number[]; readonly cyclic: boolean; readonly internalEdges: number; readonly incomingEdges: number; readonly outgoingEdges: number; readonly derived: true }
/** Finite coordinates by vertex handle; original edge semantics remain in the unchanged projection. */
export interface LayoutResult { readonly binding: LayoutBinding; readonly algorithm: 'layered' | 'force'; readonly positions: readonly { readonly handle: number; readonly x: number; readonly y: number }[]; readonly groups: readonly LayoutGroup[]; readonly work: number; readonly iterations: number; readonly complete: true }
/** Maintained visible/layout bounds; none permit unbounded whole-snapshot work. */
export const LAYOUT_LIMITS = Object.freeze({ vertices: 5000, edges: 20000, encodedBytes: 2 * 1024 * 1024, iterations: 200, maxWork: 50_000_000, yieldWork: 2048, neighborSamples: 24 });
/** Stable defaults; force refinement is explicit rather than invoked on every selection. */
export const DEFAULT_LAYOUT_OPTIONS: LayoutOptions = Object.freeze({ algorithm: 'layered', seed: 1, iterations: 60, nodeSpacing: 48, layerSpacing: 160, maxWork: 20_000_000 });
/** Fixed value-redacted layout rejection; no partial coordinates are accepted as complete. */
export class LayoutError extends Error {
  /**
   * Construct a bounded failure category and fixed explanation.
   * @param code Layout validation, resource or cancellation category.
   * @param message Application-authored explanation without arbitrary source contents.
   */
  constructor(readonly code: 'invalid-message' | 'resource-limit' | 'cancelled', message: string) { super(message); this.name = 'LayoutError'; }
}
