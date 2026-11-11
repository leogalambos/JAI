// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Pure React callback tests invoke the actual owned component, without mocking React or cursor validation. */
import { expect, it } from 'vitest';
import { ResultPager } from '../src/renderer/result-pager.js';
import type { ExplorePage } from '../src/renderer/presentation/types.js';
const page: ExplorePage = { items: [], text: 'displayed-query', order: 'identity', hidden: '1', complete: false, nextCursor: { binding: { sessionId: 'session', capability: 'capability', generation: '1' }, operation: 'search.page', queryKey: 'displayed-key', token: 'opaque', offset: '50' } };
it('advances the displayed page even when an unsubmitted input draft differs', () => {
  const calls: string[] = []; const button = ResultPager({ page, busy: false, id: 'next', label: 'Next', next: text => calls.push(text) });
  button.props.onClick(); expect(calls).toEqual(['displayed-query']);
});
it('does not advance absent, terminal or busy pages', () => {
  const calls: string[] = [];
  for (const [current, busy] of [[null, false], [{ ...page, complete: true, nextCursor: null }, false], [page, true]] as const) {
    const button = ResultPager({ page: current, busy, id: 'next', label: 'Next', next: text => calls.push(text) }); expect(button.props.disabled).toBe(true); button.props.onClick();
  }
  expect(calls).toEqual([]);
});
