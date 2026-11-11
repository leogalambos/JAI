// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Actual React command controls preserve accessible labels, disabled guards and tooltip Escape priority. */
import { createElement } from 'react';
import type { ReactElement } from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import { expect, it, vi } from 'vitest';
import { CommandIcon, IconButton } from '../src/renderer/commands.js';
import type { IconButtonProps } from '../src/renderer/commands.js';
it('renders fixed decorative icons with complete native command names and disabled explanations', () => {
  const action = vi.fn(); let tree!: ReactElement<Record<string, unknown>>;
  const props: IconButtonProps = { id: 'command', icon: 'open', label: 'Open sources…', shortcut: 'Ctrl/Cmd+O', disabled: true, reason: 'Close the current sources first.', onClick: action };
  function Mounted() { tree = IconButton(props); return tree; }
  const html = renderToStaticMarkup(createElement(Mounted));
  expect(html).toContain('aria-label="Open sources…"'); expect(html).toContain('role="tooltip"'); expect(html).toContain('Close the current sources first.'); expect(html).toContain('aria-hidden="true"');
  const button = (tree.props.children as ReactElement<Record<string, unknown>>[])[0]!;
  (button.props.onClick as () => void)(); expect(action).not.toHaveBeenCalled();
  expect(renderToStaticMarkup(CommandIcon({ name: 'relations' }))).not.toContain('onclick');
});
it('forwards one enabled native command action without interpreting icon data as code', () => {
  const action = vi.fn(); let tree!: ReactElement<Record<string, unknown>>;
  function Mounted() { tree = IconButton({ icon: 'refresh', label: 'Refresh snapshot', onClick: action }); return tree; }
  renderToStaticMarkup(createElement(Mounted)); const button = (tree.props.children as ReactElement<Record<string, unknown>>[])[0]!;
  (button.props.onClick as () => void)(); expect(action).toHaveBeenCalledOnce();
});
it('uses actual React state to show a focus tooltip and consumes Escape before global cancellation', () => {
  let phase = 0; const hidden: boolean[] = []; const event = { key: 'Escape', preventDefault: vi.fn(), stopPropagation: vi.fn() };
  function Mounted() {
    const tree = IconButton({ icon: 'fit', label: 'Fit graph', onClick() {} }) as ReactElement<Record<string, unknown>>;
    const tip = (tree.props.children as ReactElement<Record<string, unknown>>[])[1]!; hidden.push(!!tip.props.hidden);
    if (phase++ === 0) (tree.props.onFocus as () => void)(); else if (phase === 2) (tree.props.onKeyDown as (event: unknown) => void)(event);
    return tree;
  }
  renderToStaticMarkup(createElement(Mounted)); expect(hidden).toEqual([true, false, true]); expect(event.preventDefault).toHaveBeenCalledOnce(); expect(event.stopPropagation).toHaveBeenCalledOnce();
});
