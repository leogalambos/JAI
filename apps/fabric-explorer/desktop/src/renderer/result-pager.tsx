// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Read-only paging controls distinguish a displayed server page from an unsubmitted draft input. */
import type { ExplorePage } from './presentation/types.js';
/** Fixed next-page action and the currently displayed page. */
export interface ResultPagerProps {
  readonly page: ExplorePage | null;
  readonly busy: boolean;
  readonly id: string;
  readonly label: string;
  readonly next: (text: string, order: 'identity' | 'label') => void;
}
/**
 * Advance a displayed page only when its authenticated continuation exists.
 * @param props Current server page, status and named action; draft text is not submitted here.
 * @returns Native next-page button with explicit disabled/empty behavior.
 */
export function ResultPager(props: ResultPagerProps) {
  return <button id={props.id} disabled={!props.page?.nextCursor || props.busy} onClick={() => { if (props.page?.nextCursor && !props.busy) props.next(props.page.text, props.page.order); }}>{props.label}</button>;
}
