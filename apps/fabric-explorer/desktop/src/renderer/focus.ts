// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Exact user focus intents are distinct from graph selection and cannot survive stale navigation. */
/** Minimal owned focus observation; actual browser elements provide the same connectivity fact. */
export interface FocusObservation { readonly isConnected: boolean }
/**
 * Recover an operation's initiating control only when focus was lost or stayed there.
 * @param previous Element focused when the explicit operation began, if any.
 * @param current Current active element after the operation.
 * @param body Document fallback element, not an intentional user control.
 * @returns False after the user deliberately focused another connected element.
 */
export function shouldRecoverFocus(previous: FocusObservation | null, current: FocusObservation | null, body: FocusObservation): boolean { return current === null || current === body || current === previous || !current.isConnected; }
/** One exact semantic-selection intent; canvas pointer changes do not create one. */
export class InspectorFocusIntent {
  private sequence = 0;
  private pending: { ticket: number; id: string; binding: string; ready: boolean } | null = null;
  /**
   * Register an explicit semantic selection, superseding any earlier focus request.
   * @param id Exact canonical element or edge key.
   * @param binding Current serialized session/capability/generation, never a native path.
   * @returns Monotonic request ticket local to this mounted interface.
   */
  request(id: string, binding: string): number { const ticket = ++this.sequence; this.pending = { ticket, id, binding, ready: false }; return ticket; }
  /**
   * Mark successful completion only if the accepted selection and binding still match.
   * @param ticket Original local focus ticket.
   * @param selectedId Current accepted exact selection, or null after rejection/close.
   * @param binding Current serialized work binding.
   * @returns Whether the application should schedule a post-commit focus observation.
   */
  complete(ticket: number, selectedId: string | null, binding: string): boolean {
    const pending = this.pending; if (!pending || pending.ticket !== ticket) return false;
    if (pending.id !== selectedId || pending.binding !== binding) { this.pending = null; return false; }
    pending.ready = true; return true;
  }
  /**
   * Consume one completed intent after the matching inspector DOM is committed.
   * @param ticket Completion ticket emitted to the component.
   * @param selectedId Exact currently rendered selection.
   * @param binding Exact currently rendered work binding.
   * @returns True once; focus is otherwise left where the user placed it.
   */
  consume(ticket: number, selectedId: string | null, binding: string): boolean {
    const pending = this.pending; if (!pending || pending.ticket !== ticket || !pending.ready) return false;
    this.pending = null; return pending.id === selectedId && pending.binding === binding;
  }
  /** Invalidate any focus intent after generation replacement or unmount. */
  reset(): void { this.pending = null; this.sequence++; }
}
