/** Counter propagation unit contracts; these controlled flags are not native trusted-delivery evidence. */
import { createElement } from 'react';
import type { ReactElement } from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import { expect, it, vi } from 'vitest';
import { PaneSplitter } from '../src/renderer/workspace-layout.js';
import { installKeyCounter } from './ergonomics-key-counter.js';
it.each([true, false])('observes isTrusted=%s before the actual splitter consumes its bubble event', trusted => {
  let listener!: (event: { isTrusted: boolean }) => void; let capture = false;
  const counts = installKeyCounter({ addEventListener(type, callback, phase) { expect(type).toBe('keydown'); listener = callback; capture = phase; } });
  let tree!: ReactElement<Record<string, unknown>>; const onChange = vi.fn();
  function Mounted() { tree = PaneSplitter({ side: 'navigation', width: 276, maximum: 900, onChange }); return tree; }
  renderToStaticMarkup(createElement(Mounted)); let stopped = false;
  const event = { key: 'ArrowRight', isTrusted: trusted, nativeEvent: { isComposing: false }, preventDefault: vi.fn(), stopPropagation() { stopped = true; } };
  if (capture) listener(event);
  (tree.props.onKeyDown as Function)(event);
  if (!stopped && !capture) listener(event);
  expect(stopped).toBe(true); expect(onChange).toHaveBeenCalledExactlyOnceWith(284);
  expect(counts).toEqual(trusted ? { trusted: 1, untrusted: 0 } : { trusted: 0, untrusted: 1 });
});
it('retains every delivered event and distinguishes untrusted input without changing event propagation', () => {
  let listener!: (event: { isTrusted: boolean }) => void;
  const counts = installKeyCounter({ addEventListener(_type, callback) { listener = callback; } });
  for (const isTrusted of [true, true, false]) listener({ isTrusted });
  expect(counts).toEqual({ trusted: 2, untrusted: 1 });
});
