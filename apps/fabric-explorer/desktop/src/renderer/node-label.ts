// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Pure bounded display names; aliases never replace semantic labels, exact IDs or query meaning. */
import { decodeSemantic } from '@jai/fabric-explorer-contracts';
import type { RecordedLabel } from '../import/recorded-label.js';
import type { GraphProjection, Vertex } from '@jai/fabric-explorer-contracts';
const DIGEST = /^[a-f0-9]{64}$/i;
function compact(text: string, maximum: number): string { const normalized = text.slice(0, maximum * 2).replace(/[\u0000-\u001f\u007f]/g, ' ').replace(/[\ud800-\udbff]$/, '').trim(); const points = Array.from(normalized); return points.length > maximum ? points.slice(0, maximum - 1).join('') + '…' : normalized; }
function findingLabel(vertex: Vertex, text: string): string {
  if (vertex.kind !== 'finding') return text;
  const id = vertex.identity.findingId; const prefix = `${id} · `;
  const title = text === id ? '' : text.startsWith(prefix) ? text.slice(prefix.length) : text;
  return title ? `${prefix}${compact(title, 96)}` : id;
}
function authored(vertex: Vertex): string | null {
  if (vertex.attributes.kind !== 'inline' || vertex.attributes.value.type !== 'object') return null;
  for (const field of ['title', 'name']) { const entry = vertex.attributes.value.entries.find(item => item.key === field); if (entry?.value.type === 'string') { const text = compact(entry.value.value, 96); if (text && !DIGEST.test(text)) return vertex.kind === 'finding' ? findingLabel(vertex, entry.value.value) : text; } }
  return null;
}
function fallback(vertex: Vertex): string {
  const title = authored(vertex); if (title) return findingLabel(vertex, title);
  const label = vertex.kind === 'finding' && vertex.label === vertex.identity.findingId ? vertex.label : compact(vertex.label, 96); if (label && !DIGEST.test(vertex.label)) return findingLabel(vertex, label);
  const digest = vertex.identity.kind === 'blob' ? vertex.identity.blobId : vertex.label;
  return findingLabel(vertex, `${vertex.kind === 'blob' ? 'Material' : vertex.kind} · ${digest.slice(0, 10)}…${digest.slice(-8)}`);
}
/** Read recorded presentation from an already validated public graph vertex.
 * @param vertex Version or use carrying the admitted presentation extension.
 * @returns The recorded presentation when supplied by the adapter.
 */
export function nodePresentation(vertex: Vertex): RecordedLabel | null {
  if (vertex.kind !== 'version' && vertex.kind !== 'use') return null;
  const extension = vertex.extensions?.['jai.recorded-label'];
  if (extension?.type !== 'object') return null;
  const presentation = decodeSemantic(extension) as Partial<RecordedLabel>;
  const validSource = (source: RecordedLabel['source'] | undefined): boolean => {
    if (!source || typeof source.versionId !== 'string') return false;
    if (source.kind === 'unavailable') return typeof source.reason === 'string';
    if (source.kind === 'record-field') return typeof source.pointer === 'string';
    return source.kind === 'companion-excerpt' && typeof source.pointer === 'string' && typeof source.blobId === 'string';
  };
  return presentation.text === vertex.label && validSource(presentation.source)
    && (presentation.additionalSources === undefined
      || Array.isArray(presentation.additionalSources) && presentation.additionalSources.every(validSource))
    ? presentation as RecordedLabel : null;
}
/** Check whether this vertex carries the recorded presentation label.
 * @param vertex The exact public vertex.
 * @returns Whether its label is backed by the recorded presentation extension.
 */
export function hasRecordedLabel(vertex: Vertex): boolean {
  if (vertex.kind !== 'version' && vertex.kind !== 'use') return false;
  const value = vertex.extensions?.['jai.recorded-label'];
  return value?.type === 'object' && value.entries.some(entry =>
    entry.key === 'text' && entry.value.type === 'string' && entry.value.value === vertex.label);
}
/**
 * Resolve the recorded label or a bounded legacy display name without changing the source record.
 * @param vertex Existing immutable public vertex; its original label remains inspector evidence.
 * @param labels Optional map staged once from the current visible projection.
 * @returns A display-only authored name, semantic label, recorded material association or typed short digest.
 * Finding names retain the full ledger-local finding ID before their bounded literal title, including mapped aliases.
 */
export function displayNodeLabel(vertex: Vertex, labels?: ReadonlyMap<string, string>): string {
  return hasRecordedLabel(vertex) ? vertex.label : findingLabel(vertex, labels?.get(vertex.id) ?? fallback(vertex));
}

/** Resolve the canvas-sized form of the same node label.
 * @param vertex Exact projected vertex.
 * @param labels Bounded projection aliases for legacy records and materials.
 * @returns Compact recorded label or the existing legacy display name.
 */
export function compactNodeLabel(vertex: Vertex, labels: ReadonlyMap<string, string>): string {
  const text = displayNodeLabel(vertex, labels);
  if (!hasRecordedLabel(vertex)) return text;
  const points = Array.from(text);
  return points.length > 96 ? points.slice(0, 95).join('') + '…' : text;
}
/**
 * Stage presentation aliases once for a bounded visible projection, retaining only compact strings.
 * @param projection Current immutable graph with at most 5,000 vertices and 20,000 relations.
 * @returns Exact-ID lookup of display text; material associations identify the recorded neighbour and source field, not an authored blob title.
 * @throws {Error} For an excessive projection; the function does not read source pages or modify source attributes.
 */
export function projectionLabelMap(projection: GraphProjection): ReadonlyMap<string, string> {
  if (projection.vertices.length > 5000 || projection.edges.length > 20000) throw new Error('Display label projection limit exceeded');
  const authoredIds = new Set(projection.vertices.filter(vertex => authored(vertex) !== null).map(vertex => vertex.id));
  const vertices = new Map(projection.vertices.map(vertex => [vertex.id, vertex])); const result = new Map(projection.vertices.map(vertex => [vertex.id, displayNodeLabel(vertex)]));
  const associations = new Map<string, { first: string; owners: Set<string> }>();
  for (const edge of projection.edges) {
    if (edge.relation !== 'material-attachment') continue;
    const from = vertices.get(edge.from); const to = vertices.get(edge.to); const material = from?.kind === 'blob' ? from : to?.kind === 'blob' ? to : null; const owner = material === from ? to : from;
    if (!material || !owner || owner.kind === 'blob' || authoredIds.has(material.id) || (compact(material.label, 96) && !DIGEST.test(material.label))) continue;
    const pointer = edge.identity.kind === 'occurrence' ? edge.identity.pointer : edge.label;
    const association = `${compact(result.get(owner.id)!, 36)} · ${compact(pointer || edge.label, 30)}`;
    const existing = associations.get(material.id);
    if (existing) { existing.owners.add(owner.id); if (association < existing.first) existing.first = association; }
    else associations.set(material.id, { first: association, owners: new Set([owner.id]) });
  }
  for (const [id, item] of associations) { const vertex = vertices.get(id)!; const digest = vertex.identity.kind === 'blob' ? vertex.identity.blobId : vertex.label; result.set(id, `Material · ${item.first}${item.owners.size > 1 ? ` (+${item.owners.size - 1} related nodes)` : ''} · ${digest.slice(0, 8)}…${digest.slice(-6)}`); }
  // A short digest can collide; deterministic ordinal disambiguation preserves compactness without claiming identity.
  const collisions = new Map<string, string[]>();
  for (const vertex of projection.vertices) if (vertex.kind === 'blob') { const text = result.get(vertex.id)!; const ids = collisions.get(text); if (ids) ids.push(vertex.id); else collisions.set(text, [vertex.id]); }
  for (const [text, ids] of collisions) if (ids.length > 1) ids.sort().forEach((id, index) => result.set(id, `${text} [${index + 1}]`));
  return result;
}
