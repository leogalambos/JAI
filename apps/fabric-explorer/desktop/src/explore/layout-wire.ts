// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Exact IEEE754 coordinate transport inside the private app channel, not source semantic JSON. */
import { ContractError, encodeWire } from '@jai/fabric-explorer-contracts';
import type { LayoutResult } from '../layout/types.js';
import { EXPLORE_LIMITS } from './types.js';
/** Private coordinate frame uses exact big-endian IEEE754 bytes; no source number domain is reinterpreted. */
export type LayoutWireResult = Omit<LayoutResult, 'positions'> & { readonly positions: readonly { readonly handle: number; readonly x: string; readonly y: string }[] };
function bits(value: number): string { if (!Number.isFinite(value)) throw new Error('Nonfinite layout coordinate'); const buffer = new ArrayBuffer(8); new DataView(buffer).setFloat64(0, value, false); return [...new Uint8Array(buffer)].map(byte => byte.toString(16).padStart(2, '0')).join(''); }
function number(value: string): number { if (typeof value !== 'string' || !/^[0-9a-f]{16}$/.test(value)) throw new Error('Invalid coordinate bits'); const buffer = new ArrayBuffer(8); const bytes = new Uint8Array(buffer); for (let i = 0; i < 8; i++) bytes[i] = Number.parseInt(value.slice(i * 2, i * 2 + 2), 16); const result = new DataView(buffer).getFloat64(0, false); if (!Number.isFinite(result)) throw new Error('Nonfinite layout coordinate'); return result; }
/**
 * Encode fractional derived coordinates exactly while retaining strict integer-only administrative JSON.
 * @param result Worker-authored bounded numeric layout result.
 * @returns Closed wire-safe layout DTO with exact64bit coordinate strings.
 * @throws {Error} For nonfinite coordinates or excessive wire size.
 */
export function encodeLayout(result: LayoutResult): LayoutWireResult {
  const value = { ...result, positions: result.positions.map(position => ({ handle: position.handle, x: bits(position.x), y: bits(position.y) })) };
  if (new TextEncoder().encode(encodeWire(value)).length > EXPLORE_LIMITS.frameBytes) throw new ContractError('resource-limit', 'Layout frame exceeds limit'); return value;
}
/**
 * Decode a bounded worker-authored layout DTO, preserving exact coordinate bits.
 * @param input Closed numeric-handle layout with wire-safe hex coordinates.
 * @returns Finite numeric coordinates without changing binding, groups or handles.
 * @throws {Error} For malformed positions, duplicate handles or oversized data.
 */
export function decodeLayout(input: LayoutWireResult): LayoutResult {
  if (!input || typeof input !== 'object' || Object.keys(input).sort().join() !== 'algorithm,binding,complete,groups,iterations,positions,work' || !Array.isArray(input.positions) || input.positions.length > 5000 || new Set(input.positions.map(position => position.handle)).size !== input.positions.length) throw new Error('Invalid layout frame');
  if (input.complete !== true || !['layered', 'force'].includes(input.algorithm) || !Number.isInteger(input.work) || input.work < 0 || input.work > 50000000 || !Number.isInteger(input.iterations) || input.iterations < 0 || input.iterations > 200 || !Array.isArray(input.groups) || input.groups.length > 5000 || !input.binding || Object.keys(input.binding).sort().join() !== 'capability,generation,projectionId,requestId,sessionId' || Object.values(input.binding).some(value => typeof value !== 'string' || value.length === 0)) throw new Error('Invalid layout metadata');
  const handles = new Set(input.positions.map(position => position.handle)); const members = new Set<number>(); const ids = new Set<number>();
  for (const group of input.groups) {
    if (!group || Object.keys(group).sort().join() !== 'cyclic,derived,id,incomingEdges,internalEdges,members,outgoingEdges' || !Number.isInteger(group.id) || group.id < 0 || ids.has(group.id) || typeof group.cyclic !== 'boolean' || group.derived !== true || !Array.isArray(group.members) || group.members.length === 0 || group.members.length > 5000 || [group.internalEdges, group.incomingEdges, group.outgoingEdges].some(value => !Number.isInteger(value) || value < 0 || value > 20000)) throw new Error('Invalid layout groups');
    ids.add(group.id); for (const handle of group.members) { if (!handles.has(handle) || members.has(handle)) throw new Error('Invalid layout membership'); members.add(handle); }
  }
  if (members.size !== handles.size) throw new Error('Incomplete layout membership');
  if (new TextEncoder().encode(encodeWire(input)).length > EXPLORE_LIMITS.frameBytes) throw new ContractError('resource-limit', 'Layout frame exceeds limit');
  return { ...input, positions: input.positions.map(position => { if (!position || Object.keys(position).sort().join() !== 'handle,x,y' || !Number.isInteger(position.handle) || position.handle < 0 || position.handle > 0xffffffff) throw new Error('Invalid layout position'); return { handle: position.handle, x: number(position.x), y: number(position.y) }; }) };
}
