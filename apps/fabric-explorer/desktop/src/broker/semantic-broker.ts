/** Safe semantic rejection values retained by fixture and diagnostic consumers. */
import type { ImportReport, ReaderDiagnostic, SourceCompatibility } from './semantic-types.js';

/** Typed candidate rejection with value-redacted diagnostics and observed compatibility. */
export class SemanticError extends Error {
  /**
   * Retain a safe failure report without publishing a partial candidate.
   * @param code Fixed reader failure category.
   * @param report Bounded selected-source outcome report.
   * @param compatibility Actual observed format/adapter facts where available.
   */
  constructor(readonly code: ReaderDiagnostic['code'], readonly report: ImportReport, readonly compatibility: readonly SourceCompatibility[]) {
    super('Selected sources could not be imported.'); this.name = 'SemanticError';
  }
}
