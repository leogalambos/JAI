/** Document-bound sender authentication and fixed preload channel regressions. */
import { describe, expect, it } from 'vitest';
import { authenticateSender, assertSafeArguments, CONTENT_SECURITY_POLICY, installSessionPolicy } from '../src/shell/security.js';
import { createBridge, CHANNELS } from '../src/shell/bridge.js';
describe('desktop policy', () => {
  it('authenticates exact sender, main frame, session and URL before payload work', () => {
    const sender = {}; const frame = {}; const session = {}; const trusted = { sender, frame, session, url: 'file:///application/index.html' }; const actual = { session, url: trusted.url, destroyed: false };
    expect(() => authenticateSender({ sender, senderFrame: frame }, trusted, actual)).not.toThrow();
    for (const event of [{ sender: {}, senderFrame: frame }, { sender, senderFrame: {} }]) expect(() => authenticateSender(event, trusted, actual)).toThrow('Sender rejected');
    for (const changed of [{ ...actual, session: {} }, { ...actual, url: 'file:///other' }, { ...actual, destroyed: true }]) expect(() => authenticateSender({ sender, senderFrame: frame }, trusted, changed)).toThrow();
  });
  it('rejects boundary-weakening launch switches and restrictive CSP has no unsafe directives', () => {
    for (const flag of ['--no-sandbox', '--remote-debugging-port=9222', '--disable-web-security', '--inspect']) expect(() => assertSafeArguments(['app', flag])).toThrow();
    expect(() => assertSafeArguments(['app'])).not.toThrow(); expect(CONTENT_SECURITY_POLICY).toContain("connect-src 'none'"); expect(CONTENT_SECURITY_POLICY).not.toMatch(/unsafe-inline|unsafe-eval|https:/);
  });
  it('allows only exact immutable packaged assets and denies permissions and downloads', () => {
    let resource!: (url: string) => boolean; let permission!: () => false; let download!: () => false; const assets = new Set(['file:///app/index.html']);
    installSessionPolicy({ resource: handler => { resource = handler; }, permissions: handler => { permission = handler; }, downloads: handler => { download = handler; } }, assets);
    assets.add('https://example.test'); expect(resource('file:///app/index.html')).toBe(true);
    for (const url of ['https://example.test', 'file:///source.jsonl', 'file:///app/index.html?x=1', 'data:text/html,test']) expect(resource(url)).toBe(false);
    expect(permission()).toBe(false); expect(download()).toBe(false);
  });
  it('exports frozen named methods and cannot choose arbitrary IPC channels', async () => {
    const calls: unknown[] = []; const bridge = createBridge({ invoke: async (...args) => { calls.push(args); return {}; } });
    expect(Object.isFrozen(bridge)).toBe(true); expect(Object.keys(bridge).sort()).toEqual(['cancelRequest', 'cancelSelection', 'closeRoots', 'counts', 'details', 'dropQuery', 'filterProjection', 'getState', 'groups', 'importSnapshot', 'layout', 'lookup', 'neighbours', 'pageSource', 'path', 'pickRoots', 'refreshSnapshot', 'search', 'searchFindings', 'updatePreferences']);
    await bridge.getState(); expect(calls).toEqual([[CHANNELS.state]]);
  });
});
