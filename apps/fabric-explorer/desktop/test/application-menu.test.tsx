// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Real menu state and owned action boundaries; actual browser focus remains a native UI check. */
import { createElement, isValidElement } from 'react';
import type { ReactElement } from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import { expect, it, vi } from 'vitest';
import { ApplicationMenu } from '../src/renderer/application-menu.js';
import type { MenuCommand, MenuGroup } from '../src/renderer/application-menu.js';
function find(input: unknown, id: string): ReactElement<Record<string, unknown>> | undefined {
  if (Array.isArray(input)) return input.map(item => find(item, id)).find(Boolean);
  if (!isValidElement(input)) return undefined; const element = input as ReactElement<Record<string, unknown>>;
  return element.props.id === id ? element : find(element.props.children, id);
}
it('has a labeled menubar, one tab stop and complete unavailable-action explanations', () => {
  const command: MenuCommand = { id: 'not-ready', label: 'Refresh snapshot', disabled: true, reason: 'Open sources first.', action: vi.fn() };
  const groups: MenuGroup[] = [{ id: 'menu-file', label: 'File', commands: [command] }, { id: 'menu-help', label: 'Help', commands: [] }];
  let phase = 0; let tree!: ReactElement;
  function Mounted() { tree = ApplicationMenu({ groups }); if (phase++ === 0) (find(tree, 'menu-file')!.props.onClick as () => void)(); return tree; }
  const html = renderToStaticMarkup(createElement(Mounted)); expect(html).toContain('role="menubar"'); expect(html).toContain('Open sources first.');
  expect(find(tree, 'menu-help')!.props.tabIndex).toBe(-1); (find(tree, command.id)!.props.onClick as () => void)(); expect(command.action).not.toHaveBeenCalled();
});
it('closes the menu before invoking its enabled command and exposes checkbox state', () => {
  const events: string[] = []; const action = vi.fn(() => { events.push('action'); }); let phase = 0;
  const groups: MenuGroup[] = [{ id: 'menu-view', label: 'View', commands: [{ id: 'toggle-pane', label: 'Navigation', checked: true, action }] }];
  function Mounted() { const tree = ApplicationMenu({ groups }); if (phase++ === 0) (find(tree, 'menu-view')!.props.onClick as () => void)(); else if (phase === 2) { const item = find(tree, 'toggle-pane')!; expect(item.props.role).toBe('menuitemcheckbox'); expect(item.props['aria-checked']).toBe(true); (item.props.onClick as () => void)(); } return tree; }
  const html = renderToStaticMarkup(createElement(Mounted)); expect(action).toHaveBeenCalledOnce(); expect(html).not.toContain('id="toggle-pane"'); expect(events).toEqual(['action']);
});
it('opens a top menu with ArrowDown and consumes Escape locally', () => {
  let phase = 0; let tree!: ReactElement; const down = { key: 'ArrowDown', nativeEvent: {}, preventDefault: vi.fn(), stopPropagation: vi.fn() }; const escape = { ...down, key: 'Escape', preventDefault: vi.fn(), stopPropagation: vi.fn() };
  const groups: MenuGroup[] = [{ id: 'menu-file', label: 'File', commands: [{ id: 'open', label: 'Open sources…', action() {} }] }];
  function Mounted() { tree = ApplicationMenu({ groups }); if (phase++ === 0) (find(tree, 'menu-file')!.props.onKeyDown as (event: unknown) => void)(down); else if (phase === 2) (find(tree, 'menu-file')!.props.onKeyDown as (event: unknown) => void)(escape); return tree; }
  renderToStaticMarkup(createElement(Mounted)); expect(down.preventDefault).toHaveBeenCalledOnce(); expect(escape.preventDefault).toHaveBeenCalledOnce(); expect(find(tree, 'menu-file')!.props['aria-expanded']).toBe(false);
});
it('refocuses first and last items when the same already-open trigger receives a keyboard open', () => {
  const first = { focus: vi.fn() }; const last = { focus: vi.fn() }; let phase = 0;
  const groups: MenuGroup[] = [{ id: 'menu-file', label: 'File', commands: [{ id: 'open', label: 'Open sources…', action() {} }] }];
  function Mounted() {
    const tree = ApplicationMenu({ groups }); const trigger = find(tree, 'menu-file')!;
    const root = tree.props as { ref: { current: unknown } }; root.ref.current = { querySelectorAll: () => [first, last] };
    if (phase++ === 0) (trigger.props.onClick as () => void)();
    else if (phase === 2) for (const key of ['ArrowDown', 'ArrowUp']) (trigger.props.onKeyDown as (event: unknown) => void)({ key, nativeEvent: {}, preventDefault() {}, stopPropagation() {} });
    return tree;
  }
  renderToStaticMarkup(createElement(Mounted)); expect(first.focus).toHaveBeenCalledOnce(); expect(last.focus).toHaveBeenCalledOnce();
});
