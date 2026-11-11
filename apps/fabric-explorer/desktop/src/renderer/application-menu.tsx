// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Labeled menu equivalents for renderer-owned commands; no privileged bridge is introduced. */
import { useEffect, useLayoutEffect, useRef, useState } from 'react';
import type { KeyboardEvent } from 'react';

/** One existing command or checkbox-style visibility command. */
export interface MenuCommand {
  readonly id: string;
  readonly label: string;
  readonly shortcut?: string;
  readonly disabled?: boolean;
  readonly reason?: string;
  readonly checked?: boolean;
  readonly action: () => void | Promise<void>;
}
/** Fixed top-level command group, in its displayed order. */
export interface MenuGroup { readonly id: string; readonly label: string; readonly commands: readonly MenuCommand[] }
/**
 * Render keyboard-operable application menus with stable trigger focus restoration.
 * @param props Labeled groups of existing renderer actions.
 * @returns Menubar supporting arrows, Home/End, Enter/Space, Escape and native Tab exit.
 */
export function ApplicationMenu({ groups }: { readonly groups: readonly MenuGroup[] }) {
  const [open, setOpen] = useState<number | null>(null); const [active, setActive] = useState(0);
  const root = useRef<HTMLElement>(null); const trigger = useRef<(HTMLButtonElement | null)[]>([]); const firstItem = useRef<'first' | 'last' | null>(null);
  const close = (restore = true) => { const previous = open; setOpen(null); firstItem.current = null; if (restore && previous !== null) trigger.current[previous]?.focus(); };
  const show = (index: number, item: 'first' | 'last' = 'first') => {
    if (open === index) { const items = root.current?.querySelectorAll<HTMLButtonElement>('[role=menu] [role^=menuitem]'); (item === 'last' ? items?.[items.length - 1] : items?.[0])?.focus(); return; }
    firstItem.current = item; setActive(index); setOpen(index);
  };
  useLayoutEffect(() => { if (open === null || !firstItem.current) return; const items = root.current?.querySelectorAll<HTMLButtonElement>('[role=menu] [role^=menuitem]'); const target = firstItem.current === 'last' ? items?.[items.length - 1] : items?.[0]; firstItem.current = null; target?.focus(); }, [open]);
  useEffect(() => {
    if (open === null) return;
    const outside = (event: Event) => { if (event.target instanceof Node && !root.current?.contains(event.target)) close(false); };
    document.addEventListener('pointerdown', outside); document.addEventListener('focusin', outside);
    return () => { document.removeEventListener('pointerdown', outside); document.removeEventListener('focusin', outside); };
  }, [open]);
  const menuKeys = (event: KeyboardEvent, index: number) => {
    if (event.altKey || event.ctrlKey || event.metaKey || event.isDefaultPrevented() || event.nativeEvent.isComposing) return;
    const buttons = [...(root.current?.querySelectorAll<HTMLButtonElement>('[role=menu] [role^=menuitem]') ?? [])]; const current = buttons.indexOf(event.target as HTMLButtonElement);
    const next = event.key === 'ArrowDown' ? (current + 1) % buttons.length : event.key === 'ArrowUp' ? (current + buttons.length - 1) % buttons.length : event.key === 'Home' ? 0 : event.key === 'End' ? buttons.length - 1 : null;
    if (next !== null) { event.preventDefault(); event.stopPropagation(); buttons[next]?.focus(); }
    else if (event.key === 'ArrowRight' || event.key === 'ArrowLeft') { event.preventDefault(); event.stopPropagation(); show((index + (event.key === 'ArrowRight' ? 1 : groups.length - 1)) % groups.length); }
    else if (event.key === 'Escape') { event.preventDefault(); event.stopPropagation(); close(); }
    else if (event.key === 'Tab') close();
  };
  return <nav ref={root} className="application-menu" role="menubar" aria-label="Application menu">{groups.map((group, index) => <div className="menu-group" key={group.id}>
    <button id={group.id} ref={element => { trigger.current[index] = element; }} role="menuitem" aria-haspopup="menu" aria-expanded={open === index} aria-controls={`${group.id}-items`} tabIndex={active === index ? 0 : -1} onFocus={() => setActive(index)} onClick={() => open === index ? close() : show(index)} onKeyDown={event => {
      if (event.altKey || event.ctrlKey || event.metaKey || event.nativeEvent.isComposing) return;
      const next = event.key === 'ArrowRight' ? (index + 1) % groups.length : event.key === 'ArrowLeft' ? (index + groups.length - 1) % groups.length : event.key === 'Home' ? 0 : event.key === 'End' ? groups.length - 1 : null;
      if (next !== null) { event.preventDefault(); event.stopPropagation(); setActive(next); trigger.current[next]?.focus(); if (open !== null) show(next); }
      else if (['ArrowDown', 'ArrowUp', 'Enter', ' '].includes(event.key)) { event.preventDefault(); event.stopPropagation(); show(index, event.key === 'ArrowUp' ? 'last' : 'first'); }
      else if (event.key === 'Escape' && open !== null) { event.preventDefault(); event.stopPropagation(); close(); }
    }}>{group.label}</button>
    {open === index && <div id={`${group.id}-items`} role="menu" aria-labelledby={group.id} className="menu-popup" onKeyDown={event => menuKeys(event, index)}>{group.commands.map(command => <button id={command.id} key={command.id} role={command.checked === undefined ? 'menuitem' : 'menuitemcheckbox'} aria-checked={command.checked} aria-disabled={!!command.disabled} tabIndex={-1} onClick={() => { if (command.disabled) return; close(); void command.action(); }}><span>{command.checked === undefined ? '' : command.checked ? '✓ ' : '　'}{command.label}{command.disabled && command.reason && <small>{command.reason}</small>}</span>{command.shortcut && <kbd>{command.shortcut}</kbd>}</button>)}</div>}
  </div>)}</nav>;
}
