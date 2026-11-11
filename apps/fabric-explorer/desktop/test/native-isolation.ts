/** Native test observation validator; absence and false values are failures on every platform. */
/**
 * Require both exact native isolation booleans without inferring platform defaults.
 * @param value Untrusted test-only IPC observation.
 * @throws {Error} For an absent, malformed, extra-field or false observation.
 */
export function assertNativeIsolation(value: unknown): void {
  if (!value || typeof value !== 'object' || Array.isArray(value)) throw new Error('Native isolation observation missing');
  const record = value as Record<string, unknown>;
  if (Object.keys(record).sort().join() !== 'contextIsolated,sandboxed' || record.sandboxed !== true || record.contextIsolated !== true) throw new Error('Native isolation observation failed');
}
