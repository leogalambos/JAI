/** Closed failure categories from structural and contextual contract enforcement. */
export type ContractErrorCode = 'invalid-message' | 'resource-limit' | 'unsupported-protocol' | 'unknown-operation' | 'session-mismatch' | 'capability-mismatch' | 'stale-generation' | 'cursor-mismatch' | 'invalid-model';

/** Typed, value-redacted boundary rejection; it never supplies a successful authority result. */
export class ContractError extends Error {
  /** Stable rejection category suitable for bounded telemetry without logging source payloads. */
  readonly code: ContractErrorCode;

  /**
   * Construct a contract rejection without embedding untrusted field values.
   * @param code Closed rejection category.
   * @param message Maintainer-provided explanation; callers must not interpolate source secrets.
   * @returns A typed Error instance.
   */
  constructor(code: ContractErrorCode, message: string) {
    super(message);
    this.name = 'ContractError';
    this.code = code;
  }
}
