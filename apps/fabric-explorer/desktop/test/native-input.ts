// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Development-only native keyboard boundary, independent of Electron and product implementation. */
/** Exact native/DOM focus; targetEnabled gates activation and text, while navigation may retain an aria-disabled target. */
export interface InputOwnership { readonly windowFocused: boolean; readonly contentsFocused: boolean; readonly documentFocused: boolean; readonly targetActive: boolean; readonly targetVisible: boolean; readonly targetEnabled: boolean }
/** Trusted native input composition; no source-controlled expressions enter this port. */
export interface NativeInputPort {
  /** Ask the actual native window and contents to own keyboard input. */
  acquire(): void;
  /** Observe two render frames, without a sleep or retry. */
  paint(): Promise<void>;
  /** Focus and remember one explicit trusted target expression. */
  focus(expression: string): Promise<void>;
  /** Read current native and exact DOM target ownership. */
  ownership(): Promise<InputOwnership>;
  /** Deliver one actual native key pair or character event sequence. */
  send(key: string, modifiers: readonly string[], character?: string): void;
  /** Remember the current active element after a legitimate native action. */
  acceptActive(): Promise<void>;
  /** Deliver actual native inserted text. */
  insert(value: string): Promise<void>;
}
/** One bounded helper input driver; no action retries or production focus hooks. */
export class NativeInput {
  /** @param port Trusted native composition, controlled explicitly in direct tests. */
  constructor(private readonly port: NativeInputPort) {}
  /**
   * Request actual native input ownership, then focus and verify one exact DOM target.
   * @param expression Trusted target expression; never arbitrary imported text.
   * @throws {Error} If native/document focus or exact visible DOM ownership is absent.
   */
  async focus(expression: string): Promise<void> { this.port.acquire(); await this.port.paint(); await this.verify(false); await this.port.focus(expression); await this.port.paint(); await this.verify(true); }
  /**
   * Deliver one verified native action and retain the resulting active element.
   * @param key Actual Electron key name.
   * @param modifiers Fixed native modifiers.
   * @param character Optional native character payload.
   * @throws {Error} For lost ownership; activation/typing also reject disabled targets. Navigation remains allowed on focusable aria-disabled controls.
   */
  async key(key: string, modifiers: readonly string[] = [], character?: string): Promise<void> { await this.verify(true, key === 'Enter' || key === 'Space' || character !== undefined); this.port.send(key, modifiers, character); await this.port.paint(); await this.port.acceptActive(); }
  /**
   * Change a native select with keyboard navigation and a committed Tab boundary.
   * @param expression Trusted select target.
   * @param index Required option index.
   * @param count Actual finite option count.
   * @param committed Check required value and focus on a different live control after Tab.
   * @throws {Error} If ownership, option addressing or committed selection is not established.
   */
  async choice(expression: string, index: number, count: number, committed: () => Promise<boolean>): Promise<void> {
    if (!Number.isInteger(index) || !Number.isInteger(count) || index < 0 || index >= count) throw new Error('Native select option unavailable');
    await this.focus(expression); await this.verify(true, true);
    if (index === count - 1) await this.key('End'); else { await this.key('Home'); for (let at = 0; at < index; at++) await this.key('Down'); }
    await this.key('Tab'); await this.verify(true);
    if (!(await committed())) throw new Error('Native select value or next focus was not committed');
  }
  private async verify(target: boolean, enabled = false): Promise<void> { const state = await this.port.ownership(); if (!state.windowFocused || !state.contentsFocused || !state.documentFocused || (target && (!state.targetActive || !state.targetVisible || (enabled && !state.targetEnabled)))) throw new Error('Native input ownership precondition failed'); }
  /**
   * Insert native text only into the verified active enabled target.
   * @param value Literal text passed to the actual contents API.
   * @throws {Error} If exact enabled input ownership is absent.
   */
  async insert(value: string): Promise<void> { await this.verify(true, true); await this.port.insert(value); await this.port.paint(); await this.port.acceptActive(); }
}

/** Persisted and draft preferences relevant to the bounded visual/keyboard checks. */
export interface InputPreferences { readonly theme: string; readonly reducedMotion: boolean }
/** Trusted test composition for a real preference write and its observed completion. */
export interface PreferenceSavePort {
  /** Read persisted values through the existing read-only application bridge. */
  persisted(): Promise<InputPreferences>;
  /** Activate the real Save button through verified native keyboard input. */
  activate(): Promise<void>;
  /** Observe requested persisted values and resolved UI state together; reject incomplete evidence. */
  completed(desired: InputPreferences): Promise<void>;
}
/**
 * Reuse already-persisted preferences; otherwise require the actual new values and resolved UI.
 * @param desired Current native-control draft values.
 * @param port Existing read-only state observation and native Save composition.
 * @returns Whether a required write was observed or an unchanged state was reused.
 * @throws {Error} If activation or completion observation fails; no retries are performed.
 */
export async function saveChangedPreferences(desired: InputPreferences, port: PreferenceSavePort): Promise<'saved' | 'unchanged'> {
  const before = await port.persisted();
  if (before.theme === desired.theme && before.reducedMotion === desired.reducedMotion) return 'unchanged';
  await port.activate(); await port.completed(desired); return 'saved';
}
