// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Consistent inert command icons; full accessible command names remain on controls and menus. */
import { useId, useState } from 'react';

/** Fixed visual vocabulary; source records cannot select executable artwork. */
export type IconName = 'open' | 'refresh' | 'back' | 'forward' | 'close' | 'cancel' | 'settings' | 'search' | 'findings' | 'elements' | 'inspect' | 'explore' | 'path' | 'fit' | 'zoom-in' | 'zoom-out' | 'focus' | 'help' | 'source' | 'relations' | 'raw' | 'navigation';
const paths: Record<IconName, string> = {
  open: 'M3 7h7l2 2h9l-3 11H3V5h7l2 2', refresh: 'M20 7v5h-5 M4 17v-5h5 M19 12a7 7 0 0 0-12-5 M5 12a7 7 0 0 0 12 5',
  back: 'M15 5l-7 7 7 7 M8 12h13', forward: 'M9 5l7 7-7 7 M3 12h13', close: 'M6 6l12 12 M18 6L6 18', cancel: 'M7 3h10l4 4v10l-4 4H7l-4-4V7z M8 8l8 8 M16 8l-8 8',
  settings: 'M12 8a4 4 0 1 0 0 8 4 4 0 0 0 0-8 M12 2v3 M12 19v3 M2 12h3 M19 12h3 M5 5l2 2 M17 17l2 2 M5 19l2-2 M17 7l2-2',
  search: 'M10 3a7 7 0 1 0 0 14 7 7 0 0 0 0-14 M15 15l6 6', findings: 'M12 2l10 10-10 10L2 12z M12 7v6 M12 16h.01', elements: 'M3 3h7v7H3z M14 3h7v7h-7z M3 14h7v7H3z M14 14h7v7h-7z',
  inspect: 'M3 5h18v15H3z M15 5v15 M18 9h.01 M18 13h.01', explore: 'M12 9v6 M9 12h6 M12 2v4 M12 18v4 M2 12h4 M18 12h4 M5 5l3 3 M16 16l3 3 M5 19l3-3 M16 8l3-3',
  path: 'M5 5h7v14h7 M2 2h6v6H2z M16 16h6v6h-6z', fit: 'M3 9V3h6 M15 3h6v6 M21 15v6h-6 M9 21H3v-6',
  'zoom-in': 'M3 12h18 M12 3v18', 'zoom-out': 'M3 12h18', focus: 'M3 8V3h5 M16 3h5v5 M21 16v5h-5 M8 21H3v-5 M9 12h6 M12 9v6',
  help: 'M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20 M9 8a3 3 0 0 1 6 0c0 2-3 2-3 5 M12 17h.01',
  source: 'M6 2h9l4 4v16H6z M14 2v5h5 M9 11h7 M9 15h7', relations: 'M3 5h5v5H3z M16 14h5v5h-5z M8 8h5v9h3 M11 15l2 2-2 2', raw: 'M8 4L2 12l6 8 M16 4l6 8-6 8 M14 3l-4 18', navigation: 'M3 5h18v15H3z M9 5v15 M5 9h2 M5 13h2',
};
/**
 * Render a decorative line icon; its surrounding control supplies the accessible command name.
 * @param props A fixed icon name.
 * @returns Inert SVG without source-driven markup, URLs or event handlers.
 */
export function CommandIcon({ name }: { readonly name: IconName }) { return <svg className="command-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d={paths[name]} fill="none" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round"/></svg>; }
/** Fully named command; disabled explanations are available in menus and focusable wrappers. */
export interface IconButtonProps {
  readonly id?: string;
  readonly icon: IconName;
  readonly label: string;
  readonly shortcut?: string;
  readonly disabled?: boolean;
  readonly reason?: string;
  readonly primary?: boolean;
  readonly pressed?: boolean;
  readonly onClick: () => void | Promise<void>;
}
/**
 * Present a compact command with a keyboard/hover tooltip and full accessible name.
 * @param props Fixed app action, optional availability explanation and icon.
 * @returns Native button; Escape dismisses its focused tooltip before global cancellation.
 */
export function IconButton(props: IconButtonProps) {
  const tooltip = useId(); const [visible, setVisible] = useState(false); const description = `${props.label}${props.shortcut ? ` (${props.shortcut})` : ''}${props.disabled && props.reason ? ` — ${props.reason}` : ''}`;
  return <span className="icon-command" tabIndex={props.disabled ? 0 : undefined} aria-label={props.disabled ? description : undefined} onMouseEnter={() => setVisible(true)} onMouseLeave={() => setVisible(false)} onFocus={() => setVisible(true)} onBlur={() => setVisible(false)} onKeyDown={event => { if (event.key === 'Escape' && visible) { event.preventDefault(); event.stopPropagation(); setVisible(false); } }}>
    <button id={props.id} className={`icon-button${props.primary ? ' primary' : ''}`} aria-label={props.label} aria-describedby={tooltip} aria-pressed={props.pressed} disabled={props.disabled} onClick={() => { if (!props.disabled) return props.onClick(); }}><CommandIcon name={props.icon}/></button>
    <span id={tooltip} role="tooltip" className="command-tooltip" hidden={!visible}>{description}</span>
  </span>;
}
