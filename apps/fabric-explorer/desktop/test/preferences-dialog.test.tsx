// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Actual React callbacks and SSR contracts; browser modal focus requires native execution. */
import { createElement, isValidElement } from 'react';
import type { ReactElement } from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import { expect, it, vi } from 'vitest';
import { PreferencesDialog } from '../src/renderer/preferences-dialog.js';
import { DEFAULT_PREFERENCES } from '../src/shell/preferences.js';
function fixture(reject = false) {
  const api = { updatePreferences: vi.fn(async (value: typeof DEFAULT_PREFERENCES) => { if (reject) throw new Error('Unavailable'); return value; }) };
  const onSaved = vi.fn(); const onClose = vi.fn(); const onStatus = vi.fn(); let tree!: ReactElement;
  function Mounted() { tree = PreferencesDialog({ open: true, api, preferences: DEFAULT_PREFERENCES, onSaved, onClose, onStatus }); return tree; }
  const html = renderToStaticMarkup(createElement(Mounted));
  const find = (input: unknown, id: string): ReactElement<Record<string, unknown>> | undefined => {
    if (Array.isArray(input)) return input.map(item => find(item, id)).find(Boolean);
    if (!isValidElement(input)) return undefined; const item = input as ReactElement<Record<string, unknown>>;
    return item.props.id === id ? item : find(item.props.children, id);
  };
  return { api, onSaved, onClose, onStatus, tree, html, item: (id: string) => find(tree, id)! };
}
it('renders only current settings with a labelled native modal and explicit Save/Cancel', () => {
  const f = fixture(); expect(f.html).toContain('<dialog'); expect(f.html).toContain('aria-labelledby="preferences-title"'); expect(f.html).toContain('Theme'); expect(f.html).toContain('Reduce motion'); expect(f.html).not.toContain('network');
});
it('edits a draft and discards Cancel without touching persistence', () => {
  const f = fixture(); (f.item('theme').props.onChange as Function)({ target: { value: 'dark' } }); (f.item('preferences-cancel').props.onClick as Function)(); expect(f.api.updatePreferences).not.toHaveBeenCalled(); expect(f.onSaved).not.toHaveBeenCalled(); expect(f.onClose).toHaveBeenCalledOnce();
});
it('saves exactly the current draft once and closes only after parent publication', async () => {
  const f = fixture(); (f.item('theme').props.onChange as Function)({ target: { value: 'dark' } }); (f.item('motion').props.onChange as Function)({ target: { checked: true } });
  let release!: () => void; f.onSaved.mockImplementation(() => new Promise<void>(resolve => { release = resolve; }));
  const work = (f.item('save').props.onClick as () => Promise<void>)(); await Promise.resolve(); expect(f.onClose).not.toHaveBeenCalled(); release(); await work;
  expect(f.api.updatePreferences).toHaveBeenCalledExactlyOnceWith({ version: 1, theme: 'dark', reducedMotion: true }); expect(f.onClose).toHaveBeenCalledOnce();
});
it.each(['storage', 'publication'])('keeps the dialog open after %s failure', async failure => {
  const f = fixture(failure === 'storage'); if (failure === 'publication') f.onSaved.mockRejectedValue(new Error('Refresh unavailable'));
  await (f.item('save').props.onClick as () => Promise<void>)(); expect(f.onClose).not.toHaveBeenCalled(); expect(f.onStatus).toHaveBeenCalledWith('Preferences could not be saved.');
});
it('Escape discards unsaved changes through the native cancel event without a write', () => {
  const f = fixture(); const preventDefault = vi.fn(); (f.tree.props as Record<string, Function>).onCancel!({ preventDefault }); expect(preventDefault).toHaveBeenCalledOnce(); expect(f.onClose).toHaveBeenCalledOnce(); expect(f.api.updatePreferences).not.toHaveBeenCalled();
});
it('does not submit twice or discard a dispatched save while it is pending', async () => {
  const f = fixture(); let release!: (value: typeof DEFAULT_PREFERENCES) => void; f.api.updatePreferences.mockImplementation(() => new Promise(resolve => { release = resolve; }));
  const save = f.item('save').props.onClick as () => Promise<void>; const work = save(); await save();
  (f.item('preferences-cancel').props.onClick as Function)(); (f.tree.props as Record<string, Function>).onCancel!({ preventDefault() {} });
  expect(f.onClose).not.toHaveBeenCalled(); expect(f.api.updatePreferences).toHaveBeenCalledOnce(); release(DEFAULT_PREFERENCES); await work; expect(f.onClose).toHaveBeenCalledOnce();
});
it('ignores unsupported theme input rather than expanding the persisted schema', async () => {
  const f = fixture(); (f.item('theme').props.onChange as Function)({ target: { value: 'remote-theme' } }); await (f.item('save').props.onClick as () => Promise<void>)(); expect(f.api.updatePreferences).toHaveBeenCalledExactlyOnceWith(DEFAULT_PREFERENCES);
});

it('keeps the fixed title and action footer outside the scrollable settings body', () => {
  const f = fixture(); const children = (f.tree.props as { children: ReactElement<Record<string, unknown>>[] }).children;
  const body = children.find(item => isValidElement(item) && item.props.className === 'preferences-body')!;
  expect(body).toBeDefined(); expect(children[0]!.props.id).toBe('preferences-title');
  expect(children.at(-1)!.props.className).toBe('dialog-actions');
  const bodyHtml = renderToStaticMarkup(body); expect(bodyHtml).toContain('id="preferences-description"'); expect(bodyHtml).toContain('id="theme"'); expect(bodyHtml).toContain('id="motion"'); expect(bodyHtml).not.toContain('id="preferences-title"'); expect(bodyHtml).not.toContain('id="save"');
});
