/** Capability regression: opt-out rejects dependencies without weakening ordinary picking. */
import { describe, expect, it, vi } from 'vitest';
// Keep upstream Bundler-resolution source outside the application's NodeNext compilation.
vi.hoisted(() => Object.defineProperty(globalThis, 'WebGL2RenderingContext', { configurable: true, value: { FLOAT: 5126, UNSIGNED_BYTE: 5121, UNSIGNED_SHORT: 5123, TRIANGLES: 4 } }));
const source = '../vendor/sigma/.cache/upstream/src/core/node-label-programs.ts';
const { assertNodeLabelPrograms } = await import(source) as { assertNodeLabelPrograms(enabled: boolean, settings: unknown, attachments: object): void };
import { resolveSettings } from 'sigma/settings';
describe('immutable SDK node label program capability', () => {
  it('retains default enabled behavior and accepts disabled SDK labels with edge picking', () => {
    expect(() => assertNodeLabelPrograms(true, resolveSettings({ renderLabels: true }), {})).not.toThrow();
    expect(() => assertNodeLabelPrograms(false, resolveSettings({ renderLabels: false, nodeLabelEvents: false, enableEdgeEvents: true }), {})).not.toThrow();
  });
  it.each([{ renderLabels: true }, { nodeLabelEvents: 'separate' }, { nodeLabelEvents: { click: 'separate' } }])('rejects incompatible prospective settings %j', settings => {
    expect(() => assertNodeLabelPrograms(false, resolveSettings(settings as never), {})).toThrow('labelPrograms');
  });
  it('rejects declared attachments independently of rendering flags', () => {
    expect(() => assertNodeLabelPrograms(false, resolveSettings({ renderLabels: false, nodeLabelEvents: false }), { badge: () => null })).toThrow('labelPrograms');
  });
});

import Sigma from 'sigma';
import { MultiDirectedGraph } from 'graphology';
it('rejects incompatible construction before requesting a DOM or GPU context', () => {
  expect(() => new Sigma(new MultiDirectedGraph(), null as unknown as HTMLElement, { primitives: { nodes: { labelPrograms: false } }, settings: { renderLabels: true } })).toThrow('labelPrograms');
});
it.each(['setSetting', 'updateSetting', 'setSettings'] as const)('rejects %s atomically and leaves renderer settings untouched', method => {
  const settings = resolveSettings({ renderLabels: false });
  const receiver = { nodeLabelProgramsEnabled: false, internals: { settings, primitives: { nodes: { labelPrograms: false } } }, handleSettingsUpdate: () => { throw new Error('must not publish'); }, scheduleRefresh: () => { throw new Error('must not schedule'); }, setSetting: Sigma.prototype.setSetting };
  const before = { ...settings };
  const call = () => method === 'setSettings' ? Sigma.prototype.setSettings.call(receiver as never, { renderLabels: true, stagePadding: 999 }) : method === 'updateSetting' ? Sigma.prototype.updateSetting.call(receiver as never, 'renderLabels', () => true) : Sigma.prototype.setSetting.call(receiver as never, 'renderLabels', true);
  expect(call).toThrow('labelPrograms'); expect(receiver.internals.settings).toBe(settings); expect(settings).toEqual(before);
});
it('does not expose live nested label-event settings to an updater rejected by the reduced capability', () => {
  const events = { click: false as false | 'separate' };
  const settings = resolveSettings({ renderLabels: false, nodeLabelEvents: events });
  const receiver = { nodeLabelProgramsEnabled: false, internals: { settings, primitives: { nodes: { labelPrograms: false } } }, handleSettingsUpdate: () => { throw new Error('must not publish'); }, scheduleRefresh: () => { throw new Error('must not schedule'); }, setSetting: Sigma.prototype.setSetting };
  expect(() => Sigma.prototype.updateSetting.call(receiver as never, 'nodeLabelEvents', value => {
    (value as typeof events).click = 'separate'; return value;
  })).toThrow('labelPrograms');
  expect(events.click).toBe(false); expect(settings.nodeLabelEvents).toEqual({ click: false });
});
it('retains nested label-event state when the reduced-mode updater itself throws', () => {
  const events = { click: false as false | 'separate' };
  const receiver = { nodeLabelProgramsEnabled: false, internals: { settings: resolveSettings({ renderLabels: false, nodeLabelEvents: events }) }, setSetting: Sigma.prototype.setSetting };
  expect(() => Sigma.prototype.updateSetting.call(receiver as never, 'nodeLabelEvents', value => {
    (value as typeof events).click = 'separate'; throw new Error('updater failed');
  })).toThrow('updater failed');
  expect(events.click).toBe(false);
});
it('preserves the default SDK updater input identity', () => {
  const events = { click: false as false | 'separate' };
  const publish = vi.fn();
  const receiver = { nodeLabelProgramsEnabled: true, internals: { settings: resolveSettings({ nodeLabelEvents: events }) }, setSetting: publish };
  Sigma.prototype.updateSetting.call(receiver as never, 'nodeLabelEvents', value => {
    expect(value).toBe(events); return value;
  });
  expect(publish).toHaveBeenCalledWith('nodeLabelEvents', events);
});
