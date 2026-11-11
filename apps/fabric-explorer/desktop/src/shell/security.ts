/** Fixed local-document policy and exact sender identity authentication. */
/** Strict local asset policy; inline code, network connections and embedded documents are forbidden. */
export const CONTENT_SECURITY_POLICY = "default-src 'none'; script-src 'self'; style-src 'self'; img-src 'none'; font-src 'none'; connect-src 'none'; object-src 'none'; frame-src 'none'; worker-src 'none'; base-uri 'none'; form-action 'none'; frame-ancestors 'none'";
/** Owned sender identity boundary usable with Electron events and deterministic test doubles. */
export interface SenderIdentity { readonly sender: unknown; readonly senderFrame: unknown }
/** Current trusted document identity; session and URL are checked from live objects by the wrapper. */
export interface TrustedDocument { readonly sender: unknown; readonly frame: unknown; readonly session: unknown; readonly url: string }
/**
 * Reject noncurrent window, subframe, foreign session and document before parsing payloads.
 * @param event Actual native event sender identity.
 * @param trusted Current application-owned document.
 * @param actual Live session, URL and destroyed state.
 * @throws {Error} If any sender identity component differs.
 */
export function authenticateSender(event: SenderIdentity, trusted: TrustedDocument, actual: { readonly session: unknown; readonly url: string; readonly destroyed: boolean }): void {
  if (actual.destroyed || event.sender !== trusted.sender || event.senderFrame !== trusted.frame || actual.session !== trusted.session || actual.url !== trusted.url) throw new Error('Sender rejected');
}
/**
 * Reject CLI switches that weaken the fixed desktop execution boundary.
 * @param args Actual process arguments, never source data.
 * @throws {Error} For a boundary-weakening launch option.
 */
export function assertSafeArguments(args: readonly string[]): void {
  if (args.some(argument => /^--(?:no-sandbox|disable-setuid-sandbox|disable-web-security|remote-debugging-port|remote-debugging-pipe|inspect|inspect-brk|load-extension|disable-features)(?:=|$)/.test(argument))) throw new Error('Unsupported application launch option');
}

/** Owned browser-session policy port; the Electron wrapper supplies only these fixed hooks. */
export interface SessionPolicyPort {
  /** Install an exact resource allowlist decision. */
  resource(handler: (url: string) => boolean): void;
  /** Install a deny-all permission decision. */
  permissions(handler: () => false): void;
  /** Install a deny-all download decision. */
  downloads(handler: () => false): void;
}
/**
 * Configure resource/permission/download boundaries independently of native runtime mechanics.
 * @param port Trusted session hook adapter.
 * @param assets Exact immutable packaged asset URLs.
 */
export function installSessionPolicy(port: SessionPolicyPort, assets: ReadonlySet<string>): void {
  const allowed = new Set(assets);
  port.resource(url => allowed.has(url)); port.permissions(() => false); port.downloads(() => false);
}
