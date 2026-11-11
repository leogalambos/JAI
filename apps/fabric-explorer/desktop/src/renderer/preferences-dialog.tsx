// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Dedicated presentation settings; selected sources and authority state are never persisted here. */
import { useEffect, useRef, useState } from 'react';
import type { DesktopBridge } from '../shell/bridge.js';
import type { Preferences } from '../shell/preferences.js';

/** Controlled modal lifetime; only Save calls the existing app-only persistence boundary. */
export interface PreferencesDialogProps {
  readonly open: boolean;
  readonly api: Pick<DesktopBridge, 'updatePreferences'>;
  readonly preferences: Preferences;
  readonly onSaved: (preferences: Preferences) => void | Promise<void>;
  readonly onClose: () => void;
  readonly onStatus: (message: string) => void;
}
/**
 * Edit a local two-setting draft in a native modal dialog.
 * @param props Current preferences, narrow persistence API and publication/close/status callbacks.
 * @returns Labelled modal markup. Native showModal contains focus; closing restores its invoking control.
 * Persistence/publication failures remain visible without closing; outstanding save completion is ignored after teardown.
 */
export function PreferencesDialog(props: PreferencesDialogProps) {
  const dialog = useRef<HTMLDialogElement>(null); const themeControl = useRef<HTMLSelectElement>(null);
  const draft = useRef(props.preferences); const pending = useRef(false); const lifetime = useRef(0);
  const [values, setValues] = useState(props.preferences); const [saving, setSaving] = useState(false); const [error, setError] = useState('');
  useEffect(() => {
    const node = dialog.current; if (!node || !props.open) return;
    const invoker = document.activeElement instanceof HTMLElement ? document.activeElement : null;
    const epoch = ++lifetime.current; draft.current = props.preferences; setValues(props.preferences); setError(''); pending.current = false; setSaving(false);
    node.showModal(); themeControl.current?.focus();
    return () => { if (lifetime.current === epoch) lifetime.current++; node.close(); if (invoker?.isConnected) invoker.focus(); };
  }, [props.open]);
  const discard = () => { if (!pending.current) { lifetime.current++; props.onClose(); } };
  const save = async () => {
    if (pending.current) return; pending.current = true; setSaving(true); setError(''); const epoch = lifetime.current;
    try {
      const saved = await props.api.updatePreferences(draft.current);
      if (epoch !== lifetime.current) return;
      await props.onSaved(saved);
      if (epoch !== lifetime.current) return;
      props.onStatus('Preferences saved.'); props.onClose();
    } catch {
      if (epoch === lifetime.current) { setError('Preferences could not be saved.'); props.onStatus('Preferences could not be saved.'); }
    } finally { if (epoch === lifetime.current) { pending.current = false; setSaving(false); } }
  };
  return <dialog ref={dialog} className="preferences-dialog" aria-labelledby="preferences-title" aria-describedby="preferences-description" onCancel={event => { event.preventDefault(); discard(); }}>
    <h2 id="preferences-title">Preferences</h2><div className="preferences-body"><p id="preferences-description">Presentation settings apply only to this application.</p>
    <label htmlFor="theme">Theme</label><select ref={themeControl} id="theme" value={values.theme} disabled={saving} onChange={event => {
      const theme = event.target.value; if (theme !== 'system' && theme !== 'light' && theme !== 'dark') return;
      draft.current = { ...draft.current, theme }; setValues(draft.current);
    }}><option value="system">System</option><option value="light">Light</option><option value="dark">Dark</option></select>
    <label><input id="motion" type="checkbox" checked={values.reducedMotion} disabled={saving} onChange={event => { draft.current = { ...draft.current, reducedMotion: event.target.checked }; setValues(draft.current); }}/> Reduce motion</label>
    {error && <p role="alert">{error}</p>}{saving && <p role="status">Saving preferences…</p>}
    </div><div className="dialog-actions"><button id="preferences-cancel" disabled={saving} onClick={discard}>Cancel</button><button id="save" disabled={saving} onClick={save}>Save preferences</button></div>
  </dialog>;
}
