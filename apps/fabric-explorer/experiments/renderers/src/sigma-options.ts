/** Disposable Sigma options shared by the renderer and real-SDK display-data checks. */
import { pathLine, pathCurved, pathLoop, extremityArrow } from 'sigma/rendering';
import { DEFAULT_STYLES } from 'sigma/types';
import type { SigmaOptions } from 'sigma/types';

/**
 * Build the exact options passed to the pinned Sigma renderer.
 * @returns Experiment styles, primitives and interaction settings.
 */
export function sigmaOptions(): SigmaOptions {
  return {
    primitives: { edges: { paths: [pathLine(), pathCurved(), pathLoop()], extremities: [extremityArrow()], defaultHead: 'arrow' } },
    // Sigma spread is a dimensionless curvature factor, not pixel spacing.
    // Sigma replaces the whole edge branch; retain its attribute/state bindings.
    styles: { edges: { ...DEFAULT_STYLES.edges, head: 'arrow', parallelPath: 'curved', selfLoopPath: 'loop', parallelSpread: 0.25,
      labelVisibility: (_attributes, state) => state.isHighlighted ? 'visible' : 'auto' } },
    settings: { renderEdgeLabels: true, enableEdgeEvents: true, hideEdgesOnMove: false, hideLabelsOnMove: false },
  };
}
