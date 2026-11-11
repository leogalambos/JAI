// SPDX-License-Identifier: BSD-4-Clause
// Copyright (c) 2026 Leo Galambos and the Egothor team
/** Recorded effects and structural selectors only; no chain, signature or authority adjudication. */
import { createHash } from 'node:crypto';
import type { SemanticValue, SourceReference } from '@jai/fabric-explorer-contracts';
import type { CanonicalFact, CanonicalPoint, FactAttributes, FactOrigin, SourceCompatibility } from '../broker/semantic-types.js';
import { recordedEntries } from './recorded-json.js';
import type { RecordedValue } from './recorded-json.js';
import { ImportError } from './types.js';

type Data = Record<string, any>;
const PROTOCOL = 'jai.governed-delivery/1';
const INLINE = 256 * 1024; const FACT = 1024 * 1024;
const kinds = new Set(['source', 'profile', 'assignment', 'context', 'product', 'assessment', 'decision']);
const bad = (): never => { throw new ImportError('read-failed', 'The selected record has unreadable recorded structure.'); };
const resource = (): never => { throw new ImportError('resource-limit', 'A complete semantic fact exceeds its resource limit.'); };
const object = (value: unknown): Data => { if (!value || typeof value !== 'object' || Array.isArray(value)) return bad(); return value as Data; };
const array = (value: unknown): any[] => { if (!Array.isArray(value)) return bad(); return value; };
const text = (value: unknown): string => { if (typeof value !== 'string') return bad(); return value; };
const integer = (value: unknown): bigint => { if (typeof value !== 'bigint') return bad(); return value; };
const pointer = (value: string): string => value.replaceAll('~', '~0').replaceAll('/', '~1');
const equal = (left: unknown, right: unknown): boolean => stable(left) === stable(right);
const stable = (value: any): string => {
  if (typeof value === 'bigint') return value.toString();
  if (value === null || typeof value !== 'object') return JSON.stringify(value);
  if (Array.isArray(value)) return '[' + value.map(stable).join(',') + ']';
  return '{' + Object.keys(value).sort(compareCodepoints).map(key => JSON.stringify(key) + ':' + stable(value[key])).join(',') + '}';
};
const recordedTruthy = (value: any): boolean => {
  if (value === null || value === undefined || value === false) return false;
  if (typeof value === 'number') return value !== 0;
  if (typeof value === 'bigint') return value !== 0n;
  if (typeof value === 'string' || Array.isArray(value)) return value.length > 0;
  if (typeof value === 'object') return Object.keys(value).length > 0;
  return true;
};

const keyOf = (point: CanonicalPoint): string => JSON.stringify([point.use_scope, point.ref.version_id]);
const reference = (value: any): SourceReference => {
  const source = object(value);
  return { engagement: text(source.engagement), scope: text(source.scope), logical_id: text(source.logical_id), version_id: text(source.version_id) };
};
const pointOf = (value: any): CanonicalPoint => ({ ref: reference(object(value).ref), use_scope: text(value.use_scope) });

/**
 * Compare strings using Unicode scalar/codepoint ordering, matching the published Python identity codec.
 * @param left First string.
 * @param right Second string.
 * @returns Negative, zero or positive ordering result.
 */
export function compareCodepoints(left: string, right: string): number {
  const a = left[Symbol.iterator](); const b = right[Symbol.iterator]();
  while (true) { const x = a.next(); const y = b.next(); if (x.done || y.done) return x.done ? y.done ? 0 : -1 : 1; const difference = x.value.codePointAt(0)! - y.value.codePointAt(0)!; if (difference) return difference; }
}
function identityString(value: string): string {
  const normalized = value.normalize('NFC');
  for (const char of normalized) { const code = char.codePointAt(0)!; if (code >= 0xd800 && code <= 0xdfff) return bad(); }
  return JSON.stringify(normalized);
}
/**
 * Encode integer-only immutable manifest identity data; this does not verify recorded history.
 * @param value Recorded manifest data with bigint integer tokens.
 * @returns Published NFC/sorted-key compact representation.
 * @throws {ImportError} For float tokens, normalized key collisions or invalid identity strings.
 */
export function identityJSON(value: unknown): string {
  if (value === null || typeof value === 'boolean') return String(value);
  if (typeof value === 'bigint') return value.toString();
  if (typeof value === 'string') return identityString(value);
  if (typeof value !== 'object') return bad();
  if (Array.isArray(value)) return '[' + value.map(identityJSON).join(',') + ']';
  const entries = recordedEntries(value).map(([key, item]) => [key.normalize('NFC'), item] as const).sort(([a], [b]) => compareCodepoints(a, b));
  if (entries.some(([key], index) => index > 0 && entries[index - 1]![0] === key)) return bad();
  return '{' + entries.map(([key, item]) => identityString(key) + ':' + identityJSON(item)).join(',') + '}';
}
/**
 * Compute a display version ID with the published immutable domain and codec.
 * @param manifest Recorded manifest, not a trust input.
 * @returns Lowercase domain-separated SHA256 identifier.
 * @throws {ImportError} If the immutable identity value is unsupported.
 */
export function recordedVersionId(manifest: unknown): string { return createHash('sha256').update('jai.lifecycle.version.v2\0').update(identityJSON(manifest), 'utf8').digest('hex'); }

function* referencePaths(value: any, path = ''): Generator<[string, SourceReference]> {
  if (!value || typeof value !== 'object') return;
  if (Array.isArray(value)) { for (let index = 0; index < value.length; index++) yield* referencePaths(value[index], path + '/' + index); }
  else if (Object.keys(value).sort().join() === 'engagement,logical_id,scope,version_id') yield [path, reference(value)];
  else for (const key of Object.keys(value).sort(compareCodepoints)) yield* referencePaths(value[key], path + '/' + pointer(key));
}
function* causalPaths(record: Data): Generator<[string, SourceReference]> {
  for (const [path, ref] of referencePaths(record)) {
    const parts = path.split('/');
    if (path.startsWith('/handling/') || record.product_kind === 'escalation' && (path.startsWith('/episode/') || path.startsWith('/related/'))) continue;
    if ('issued_under' in record && parts.length === 5 && parts[1] === 'effects' && parts[3] === 'targets' && record.effects[Number(parts[2])]?.operation === 'read') continue;
    yield [path, ref];
  }
}
function* walk(value: any, path = ''): Generator<[string, Data]> {
  if (!value || typeof value !== 'object') return;
  if (Array.isArray(value)) { for (let index = 0; index < value.length; index++) yield* walk(value[index], path + '/' + index); }
  else { yield [path, value]; for (const [key, item] of recordedEntries(value)) yield* walk(item, path + '/' + pointer(key)); }
}
function stringBytes(value: string, maximum: number): number {
  let size = 2;
  for (let index = 0; index < value.length; index++) {
    const code = value.charCodeAt(index);
    if (code === 34 || code === 92 || [8, 9, 10, 12, 13].includes(code)) size += 2;
    else if (code < 32) size += 6;
    else if (code < 128) size++;
    else if (code < 2048) size += 2;
    else if (code >= 0xd800 && code <= 0xdbff && value.charCodeAt(index + 1) >= 0xdc00 && value.charCodeAt(index + 1) <= 0xdfff) { size += 4; index++; }
    else size += code >= 0xd800 && code <= 0xdfff ? 6 : 3;
    if (size > maximum) return resource();
  }
  return size;
}
function tag(value: any, maximum = FACT, depth = 0): { value: SemanticValue; size: number } {
  let output: SemanticValue; let size: number;
  if (value === null) { output = { type: 'null' }; size = 15; }
  else if (typeof value === 'boolean') { output = { type: 'boolean', value }; size = value ? 31 : 32; }
  else if (typeof value === 'string') { output = { type: 'string', value }; size = 26 + stringBytes(value, maximum); }
  else if (typeof value === 'bigint') { const decimal = value.toString(); output = { type: 'integer', value: decimal }; size = 27 + stringBytes(decimal, maximum); }
  else if (typeof value === 'number') { const bytes = Buffer.allocUnsafe(8); bytes.writeDoubleBE(value); output = { type: 'float64', bits: bytes.toString('hex') }; size = 44; }
  else {
    if (depth >= 64) return resource();
    if (Array.isArray(value)) {
      const items: SemanticValue[] = []; size = 27;
      for (const item of value) { const child = tag(item, maximum - size - (items.length ? 1 : 0), depth + 1); size += child.size + (items.length ? 1 : 0); items.push(child.value); }
      output = { type: 'array', items };
    } else {
      const entries: { key: string; value: SemanticValue }[] = []; size = 30;
      for (const [key, item] of recordedEntries(object(value))) {
        const overhead = 17 + stringBytes(key, maximum) + (entries.length ? 1 : 0);
        const child = tag(item, maximum - size - overhead, depth + 1); size += overhead + child.size; entries.push({ key, value: child.value });
      }
      output = { type: 'object', entries };
    }
  }
  if (size > maximum) return resource();
  return { value: output, size };
}
function fitsInline(value: any, budget = INLINE, depth = 0): number {
  if (depth > 64) return resource();
  if (typeof value === 'string') { if (value.length > budget) return -1; let count = 0; for (const _char of value) count++; return budget - count * 6 - 40; }
  if (value === null || typeof value === 'boolean' || typeof value === 'number') return budget - 64;
  if (typeof value === 'bigint') return budget - value.toString().length - 40;
  if (Array.isArray(value)) { for (const item of value) { budget = fitsInline(item, budget - 2, depth + 1); if (budget < 0) return budget; } }
  else for (const [key, item] of recordedEntries(object(value))) { let count = 0; for (const _char of key) count++; budget = fitsInline(item, budget - count * 6 - 48, depth + 1); if (budget < 0) return budget; }
  return budget - 40;
}
function attributes(value: any, origin: FactOrigin): FactAttributes {
  if (fitsInline(value) >= 0) { const encoded = tag(value); if (encoded.size <= INLINE) return { kind: 'inline', value: encoded.value }; }
  return { kind: 'paged', byteLength: origin.byteLength, mediaType: 'application/json' };
}
function origin(offset: number, length: number, sequence: bigint | null, path: string): FactOrigin { return { pointer: path, sequence: sequence === null ? null : sequence.toString(), byteOffset: String(offset), byteLength: String(length) }; }

/** Material lookup stays at the main capability boundary, never a worker pathname read. */
export interface RecordedControl { progress?(value: import('./progress.js').ImportProgress): void; cancelled(): boolean; materialAvailability?(sourceId: string, blobId: string): Promise<'available' | 'missing' | 'unknown'> }
/** Parsed source summary before namespace/revision metadata is finalized by the owner. */
export interface ProjectionSummary { readonly head: string | null; readonly sequence: string; readonly compatibility: SourceCompatibility }
interface Registration { readonly manifest: Data; readonly provenance: Data; readonly origin: FactOrigin; readonly effects: readonly Data[]; readonly scope: string }

/** One source's necessary recorded indexes; release it after draining directly to the model. */
export class RecordedProjection {
  private readonly versions = new Map<string, Registration>();
  private readonly states = new Map<string, { point: CanonicalPoint; state: Data }>();
  private readonly reliance = new Map<string, CanonicalPoint[]>();
  private readonly requirements = new Map<string, Data[]>();
  private readonly sources = new Map<string, { scope: string; ref: SourceReference }>();
  private readonly findings = new Map<string, { value: Data; events: Data[]; origin: FactOrigin }>();
  private initialized = false; private scope = 'default'; private anchor = 'default'; private rows = 0;
  private head: string | null; private sequence = '0'; private declaredFormat: string | null = null; private declaredProtocol: string | null = null; private supported = true; private currentSequence: string | null = null;
  /**
   * Bind projection state to one admitted opaque source.
   * @param sourceId Opaque selected source identifier.
   * @param family Supported source family; audit remains explicitly unavailable in the model.
   */
  constructor(readonly sourceId: string, readonly family: 'fabric' | 'findings' | 'audit') { this.head = family === 'fabric' ? '0'.repeat(64) : null; }
  private check(control: RecordedControl): void { if (control.cancelled()) throw new ImportError('cancelled', 'Recorded import cancelled.'); }
  private ref(identifier: string): SourceReference { const value = this.versions.get(identifier)?.manifest ?? bad(); return { engagement: text(value.content.engagement), scope: text(value.content.scope), logical_id: text(value.logical_id), version_id: identifier }; }
  private point(ref: SourceReference, scope = this.scope): CanonicalPoint { return { ref, use_scope: scope }; }
  private record(ref: SourceReference): Data | null { return this.versions.get(ref.version_id)?.manifest.content.record ?? null; }
  private assignmentUse(assignment: Data, path: string, ref: SourceReference): CanonicalPoint {
    const selectors = new Map(array(assignment.input_uses ?? []).map(item => [text(item.at), text(item.use_scope)]));
    if (path === '/routing/policy') return this.point(ref, this.anchor);
    if (path === '/issued_under') return this.point(ref, this.record(ref)?.use_scope ?? this.scope);
    return this.point(ref, selectors.get(path) ?? assignment.use_scope ?? this.scope);
  }
  private subjectUse(subject: SourceReference, assignment: Data): CanonicalPoint {
    const matches = [...referencePaths(assignment)].filter(([path, ref]) => path.startsWith('/inputs/') && equal(ref, subject)).map(([path, ref]) => this.assignmentUse(assignment, path, ref));
    return matches[0] ?? this.point(subject, assignment.use_scope ?? this.scope);
  }
  private dependency(record: Data, path: string, ref: SourceReference): CanonicalPoint {
    const assignment = 'issued_under' in record ? record : record.assignment ? this.record(reference(record.assignment)) : null;
    if (path.startsWith('/assessed_closure/')) return pointOf(record.assessed_closure[Number(path.split('/')[2])]);
    if (assignment === record) return this.assignmentUse(assignment, path, ref);
    if (assignment) {
      if (path === '/assignment') return this.point(ref, assignment.use_scope ?? this.scope);
      const paths = [...causalPaths(assignment)]; const exact = paths.find(([at, bound]) => at === path && equal(bound, ref));
      if (exact) return this.assignmentUse(assignment, path, ref);
      const matches = paths.filter(([at, bound]) => at !== '/issued_under' && equal(bound, ref)).map(([at, bound]) => this.assignmentUse(assignment, at, bound));
      return new Set(matches.map(item => item.use_scope)).size === 1 ? matches[0]! : this.point(ref, assignment.use_scope ?? this.scope);
    }
    return this.point(ref);
  }
  private dependencies(record: Data): CanonicalPoint[] { const result = new Map<string, CanonicalPoint>(); for (const [path, ref] of causalPaths(record)) { const point = this.dependency(record, path, ref); result.set(keyOf(point), point); } return [...result.values()].sort((a, b) => compareCodepoints(identityJSON(a), identityJSON(b))); }
  private governing(point: CanonicalPoint, active = new Set<string>()): CanonicalPoint[] {
    const key = keyOf(point); if (active.has(key)) return []; active.add(key);
    const previous = this.scope; this.scope = point.use_scope;
    try {
      const record = this.record(point.ref); if (!record) return [];
      const family = this.versions.get(point.ref.version_id)!.manifest.kind;
      if (family === 'delivery.decision') return this.reliance.get(key) ?? [];
      const assignment = family === 'delivery.assignment' ? record : record.assignment ? this.record(reference(record.assignment)) : null;
      const inspection: Data = { reviewer: 'assessed-subject', integration_reviewer: 'assessed-subject', receiver: 'incoming_handoff', measurement: 'measured-subject' };
      const result = new Map<string, CanonicalPoint>();
      for (const [path, ref] of causalPaths(record)) {
        let keep = false;
        if (family === 'delivery.source') keep = path.startsWith('/inherited/');
        else if (family === 'delivery.profile') keep = path.startsWith('/source_profiles/');
        else if (family === 'delivery.assignment') keep = ['/profile', '/criteria', '/routing/policy'].includes(path) || ['/inherited/', '/inputs/', '/effects/'].some(prefix => path.startsWith(prefix));
        else if (family === 'delivery.context') keep = ['/assignment', '/profile', '/execution/selection', '/speculation'].includes(path) || path.startsWith('/inputs/');
        else if (family === 'delivery.product') { keep = path === '/profile' || ['/inputs/', '/evidence/', '/related/', '/outcome/evidence/'].some(prefix => path.startsWith(prefix)); if (record.product_kind === 'finding' && path.startsWith('/related/')) keep = record.related[Number(path.split('/')[2])].slot_id !== 'subject'; }
        else if (family === 'delivery.assessment') keep = ['/profile', '/criteria'].includes(path) || ['/conditions/', '/findings/'].some(prefix => path.startsWith(prefix));
        const parts = path.split('/'); if (keep && assignment && parts.length === 5 && parts[1] === 'inputs' && parts[3] === 'refs') keep = assignment.inputs[Number(parts[2])].slot_id !== inspection[assignment.responsibility];
        if (keep) { const dependency = this.dependency(record, path, ref); if (!result.has(keyOf(dependency))) result.set(keyOf(dependency), dependency); }
      }
      if (family === 'delivery.assessment' && assignment) for (const dependency of [...this.governing(this.point(reference(record.assignment), assignment.use_scope ?? this.scope), active), ...this.governing(this.subjectUse(reference(record.subject), assignment), active)]) if (!result.has(keyOf(dependency))) result.set(keyOf(dependency), dependency);
      for (const requirement of this.requirements.get(key) ?? []) { const dependency = pointOf(requirement.point); if (!result.has(keyOf(dependency))) result.set(keyOf(dependency), dependency); }
      return [...result.values()];
    } finally { this.scope = previous; active.delete(key); }
  }
  private ensureUse(point: CanonicalPoint, active = new Set<string>()): void {
    const key = keyOf(point); if (this.states.has(key) || active.has(key) || !this.versions.has(point.ref.version_id)) return;
    active.add(key); const previous = this.scope; this.scope = point.use_scope;
    try {
      const value = this.versions.get(point.ref.version_id)!.manifest; const record = value.content.record; const dependencies = this.dependencies(record);
      for (const dependency of dependencies) this.ensureUse(dependency, active);
      this.reliance.set(key, dependencies); let primitive = ['delivery.source', 'delivery.profile'].includes(value.kind);
      if (value.kind === 'delivery.source' && record.owner?.kind === 'authority' && this.initialized) primitive = [...this.sources.values()].some(source => source.scope === point.use_scope && equal(source.ref, point.ref));
      this.states.set(key, { point, state: { validity: primitive ? 'valid' : 'pending', applicable: primitive } });
    } finally { this.scope = previous; active.delete(key); }
  }
  /**
   * Index one parsed source row without executing or verifying its recorded effects.
   * @param value Lossless native-parsed recorded value.
   * @param offset Exact physical source byte offset.
   * @param length Exact source row byte length including its terminator.
   * @throws {ImportError} For unsupported format or unreadable required structures.
   */
  consume(value: RecordedValue, offset: number, length: number): void {
    const row = object(value); this.currentSequence = String(this.rows + 1);
    if (this.family === 'audit') throw new ImportError('incompatible-source', 'The optional audit adapter is unavailable in this build.');
    if (this.family === 'findings') { this.finding(row, offset, length); this.rows++; this.sequence = String(this.rows); return; }
    if (this.rows === 0) { this.declaredFormat = ['bigint', 'string', 'number'].includes(typeof row.format) && String(row.format).length <= 128 ? String(row.format) : null; this.declaredProtocol = typeof row.protocol === 'string' && row.protocol.length <= 128 ? row.protocol : null; }
    if (row.format !== 9n || row.protocol !== PROTOCOL) { this.supported = false; throw new ImportError('incompatible-source', 'The selected recorded source format is unsupported.'); }
    const operations = array(row.operations); if (operations.length !== 1 || object(operations[0]).op !== 'governed') return bad();
    const data = object(operations[0].data); const message = object(data.message); const effects = array(data.effects); const sequence = integer(row.sequence); if (sequence < 1n) return bad();
    this.scope = text(message.scope); if (!this.rows) this.anchor = this.scope;
    for (let effectIndex = 0; effectIndex < effects.length; effectIndex++) {
      const effect = object(effects[effectIndex]); const operation = text(effect.op);
      if (operation === 'register' || operation === 'decision-record') {
        const manifest = object(effect.manifest); const content = object(manifest.content); object(content.record);
        if (manifest.schema !== 'jai.lifecycle.manifest/2' || typeof manifest.kind !== 'string' || !manifest.kind.startsWith('delivery.') || !kinds.has(manifest.kind.replace(/^delivery\./, ''))) return bad();
        text(content.engagement); text(content.scope); text(manifest.logical_id); const dependencies = array(effect.dependencies).map(pointOf);
        const id = recordedVersionId(manifest); const provenance: Data = { origin: operation === 'register' ? effect.origin : message.sender, context: operation === 'register' ? effect.context : message.context, sequence };
        object(provenance.origin); if (provenance.context !== null) object(provenance.context);
        if (operation === 'decision-record' && typeof row.authority_proof === 'string') {
          try { const proof = JSON.parse(Buffer.from(row.authority_proof, 'base64').toString('utf8')); if (typeof proof.request?.kind === 'string' && typeof proof.receipt?.key_id === 'string') provenance.authority = { purpose: proof.request.kind, key_id: proof.receipt.key_id }; } catch { /* Malformed recorded proof claims do not authenticate or block viewing. */ }
        }
        this.versions.set(id, { manifest, provenance, origin: origin(offset, length, BigInt(this.rows + 1), '/operations/0/data/effects/' + effectIndex + '/manifest'), effects: manifest.kind === 'delivery.decision' ? effects : [], scope: this.scope });
        const point = this.point(this.ref(id), typeof effect.use_scope === 'string' ? effect.use_scope : this.scope);
        for (const dependency of dependencies) this.ensureUse(dependency);
        this.reliance.set(keyOf(point), dependencies); this.states.set(keyOf(point), { point, state: { validity: operation === 'decision-record' ? 'valid' : 'pending', applicable: operation === 'decision-record' } });
      } else if (operation === 'qualify') {
        const id = text(effect.subject); const point = this.point(this.versions.has(id) ? this.ref(id) : { engagement: '', scope: '', logical_id: '', version_id: id }, typeof effect.use_scope === 'string' ? effect.use_scope : this.scope);
        if (!this.states.has(keyOf(point)) && this.versions.has(id)) this.ensureUse(point);
        this.states.set(keyOf(point), { point, state: { validity: 'valid', applicable: Object.hasOwn(effect, 'applicable') ? effect.applicable : true } }); if ('requirements' in effect) this.requirements.set(keyOf(point), array(effect.requirements));
      } else if (operation === 'cancel' || operation === 'withdraw') for (const raw of array(effect.subjects)) { const point = pointOf(raw); const key = keyOf(point); if (operation === 'cancel') this.states.set(key, { point, state: { validity: 'invalid', applicable: false } }); else if (this.states.has(key)) this.states.set(key, { point, state: { ...this.states.get(key)!.state, applicable: false } }); }
      else if (operation === 'bootstrap-use') this.ensureUse(pointOf(effect.point));
      else if (operation === 'initialize') this.initialized = true;
      else if (operation === 'initial-source') this.sources.set(JSON.stringify([text(effect.use_scope), text(effect.source.logical_id)]), { scope: text(effect.use_scope), ref: reference(effect.source) });
      else if (operation === 'source-select') for (const [key, source] of this.sources) if (source.scope === this.scope && equal(source.ref, effect.previous)) this.sources.set(key, { scope: source.scope, ref: reference(effect.replacement) });
    }
    this.head = text(row.hash); this.rows++; this.sequence = String(this.rows);
  }
  private finding(row: Data, offset: number, length: number): void {
    const sequence = integer(row.seq); if (sequence < 1n) return bad(); const data = object(row.data); const operation = text(data.op);
    if (!['add', 'resolve', 'verify', 'withdraw', 'accept-risk'].includes(operation)) return bad();
    if (operation === 'add') {
      const values = array(data.findings);
      for (let index = 0; index < values.length; index++) {
        const input = object(values[index]); const id = text(input.id); if (this.findings.has(id)) return bad();
        this.findings.set(id, { value: { ...input, state: 'open', rounds: 0n, resolver: null, history: [], reviewer: data.reviewer, target: data.target ?? null }, events: [row], origin: origin(offset, length, BigInt(this.rows + 1), '/data/findings/' + index) });
      }
    } else {
      const finding = this.findings.get(text(data.id)) ?? bad(); const value = finding.value;
      finding.events.push(row); value.history.push({ op: operation, by: data.by ?? null, note: recordedTruthy(data.note) ? data.note : data.rationale ?? null, ts: row.ts });
      if (operation === 'resolve') { value.state = 'resolved'; value.resolver = data.by; }
      else if (operation === 'verify') { if (!Object.hasOwn(data, 'ok')) return bad(); if (recordedTruthy(data.ok)) value.state = 'verified'; else { value.rounds++; value.state = value.rounds >= 3n ? 'stuck' : 'open'; } }
      else if (operation === 'withdraw') value.state = 'withdrawn';
      else if (operation === 'accept-risk') { value.state = 'accepted'; value.expires = data.expires ?? null; }
    }
    this.head = text(row.hash);
  }
  /**
   * Read final recorded claims without treating them as verified history.
   * @returns Recorded last head claim, physical row count and supported outer-format observation.
   */
  summary(): ProjectionSummary { return { head: this.head, sequence: this.sequence, compatibility: { sourceId: this.sourceId, family: this.family, declaredFormat: this.declaredFormat, declaredProtocol: this.declaredProtocol, supported: this.supported, adapterVersion: 'jai.fabric-explorer.' + this.family + '/2' } }; }
  /**
   * Return only already observed bounded source metadata for a redacted failure.
   * @returns Physical row ordinal and known outer-format observation; no raw row or native message.
   */
  failureContext(): { sequence: string | null; compatibility: readonly SourceCompatibility[] } {
    return { sequence: this.currentSequence, compatibility: this.rows > 0 || this.declaredFormat !== null || this.declaredProtocol !== null ? [this.summary().compatibility] : [] };
  }
  /**
   * Generate current recorded display facts directly, without retaining a complete fact array.
   * @param control Worker cancellation and bounded main-owned material observation port.
   * @returns Facts in registration/use/reference/event order for synchronous compact insertion.
   * @throws {ImportError} For cancellation, unsupported attributes or exhausted complete-fact bounds.
   */
  async *facts(control: RecordedControl): AsyncGenerator<CanonicalFact> {
    if (this.family === 'findings') {
      for (const [id, finding] of this.findings) {
        this.check(control); const value = finding.value;
        const fields = { record: value, events: finding.events, effectiveMaxRounds: 3n, historicalMaxRoundsKnown: false };
        yield { sourceId: this.sourceId, origin: finding.origin, kind: 'finding', findingId: id, state: value.state, severity: text(value.severity) as any, findingKind: text(value.kind) as any,
          rounds: integer(value.rounds).toString(), recordedExpiry: value.expires === undefined || value.expires === null ? null : text(value.expires), label: text(value.title), target: typeof value.target === 'string' ? value.target : null, location: typeof value.location === 'string' ? value.location : null,
          attributes: { kind: 'inline', value: tag(fields).value }, effectiveMaxRounds: 3, historicalMaxRoundsKnown: false };
      }
      return;
    }
    const uses = new Map<string, { point: CanonicalPoint; state: Data }[]>();
    for (const use of this.states.values()) { const rows = uses.get(use.point.ref.version_id) ?? []; rows.push(use); uses.set(use.point.ref.version_id, rows); }
    for (const [id, registration] of this.versions) {
      this.check(control); const manifest = registration.manifest; const record = manifest.content.record; const ref = this.ref(id); const base = { sourceId: this.sourceId, origin: registration.origin };
      yield { ...base, kind: 'version', ref, family: manifest.kind.slice('delivery.'.length), label: manifest.logical_id, attributes: attributes({ manifest, provenance: registration.provenance }, registration.origin) };
      const owner = record.owner;
      if (owner && typeof owner === 'object' && !Array.isArray(owner) && Object.keys(owner).sort().join() === 'layer,question,work_item,work_kind') {
        const layer = integer(owner.layer); if (layer < 0n || layer > BigInt(Number.MAX_SAFE_INTEGER)) return bad();
        const workKind = text(owner.work_kind); const question = owner.question === null ? null : text(owner.question);
        if (!['question', 'integration', 'measurement', 'handoff'].includes(workKind) || question !== null && !['what', 'why', 'how', 'who', 'where', 'when'].includes(question)) return bad();
        yield { ...base, kind: 'ownership', originRef: ref, owner: { layer: Number(layer), work_kind: workKind as any, question: question as any, work_item: text(owner.work_item) } };
      }
      for (const field of ['owner', 'origin', 'assigned_actor', 'issued_to']) {
        const participant = record[field];
        if (participant && typeof participant === 'object' && ['authority', 'controller', 'assignment'].includes(participant.kind)) yield { ...base, kind: 'participant', originRef: ref, participant, fieldPointer: '/' + field };
      }
      const material = async (path: string, blobId: unknown): Promise<CanonicalFact | null> => {
        if (typeof blobId !== 'string' || !/^[0-9a-f]{64}$/.test(blobId)) return null;
        this.check(control); const availability = control.materialAvailability ? await control.materialAvailability(this.sourceId, blobId) : 'unknown'; this.check(control);
        return { ...base, kind: 'material', originRef: ref, blobId, availability, fieldPointer: path };
      };
      for (const [path, item] of walk(record)) if (typeof item.blob_id === 'string') { const fact = await material(path + '/blob_id', item.blob_id); if (fact) yield fact; }
      for (let index = 0; index < (record.material ?? []).length; index++) { const fact = await material('/material/' + index, record.material[index]); if (fact) yield fact; }
      const causal = new Set([...causalPaths(record)].map(([path]) => path)); const references = [...referencePaths(record)];
      for (let occurrence = 0; occurrence < references.length; occurrence++) {
        const [path, target] = references[occurrence]!;
        yield { ...base, kind: 'reference', originRef: ref, originUseScope: null, fieldPointer: path, occurrence, targetRef: target, targetUseScope: null, historicalCausal: false, governing: false, dependencyBasis: 'association' };
      }
      for (const use of uses.get(id) ?? []) {
        this.check(control); const point = use.point; const scope = point.use_scope;
        yield { ...base, kind: 'use', point, state: tag(use.state).value };
        const governing = this.governing(point); const represented = new Set<string>(); const previous = this.scope; this.scope = scope;
        try {
          for (let occurrence = 0; occurrence < references.length; occurrence++) {
            const [path, target] = references[occurrence]!; const targetPoint = this.dependency(record, path, target); const historical = causal.has(path); if (historical) represented.add(keyOf(targetPoint));
            yield { ...base, kind: 'reference', originRef: ref, originUseScope: scope, fieldPointer: path, occurrence, targetRef: target, targetUseScope: targetPoint.use_scope, historicalCausal: historical,
              governing: historical && governing.some(item => keyOf(item) === keyOf(targetPoint)), dependencyBasis: historical ? 'historical' : 'association' };
          }
        } finally { this.scope = previous; }
        for (let occurrence = 0; occurrence < governing.length; occurrence++) if (!represented.has(keyOf(governing[occurrence]!))) yield { ...base, kind: 'governing-dependency', originPoint: point, prerequisitePoint: governing[occurrence]!, occurrence, dependencyBasis: 'governing' };
      }
      if (manifest.kind === 'delivery.decision') for (let occurrence = 0; occurrence < registration.effects.length; occurrence++) {
        this.check(control); const effect = registration.effects[occurrence]!; const targets: any[] = [];
        if (Array.isArray(effect.subjects)) targets.push(...effect.subjects);
        if (effect.subject && typeof effect.subject === 'object' && !Array.isArray(effect.subject)) targets.push(effect.subject);
        if (effect.ref && typeof effect.ref === 'object' && !Array.isArray(effect.ref)) targets.push(effect.ref);
        const exact: CanonicalPoint[] = [];
        for (const target of targets) if (target && typeof target === 'object' && !Array.isArray(target)) {
          const keys = Object.keys(target).sort().join();
          if (keys === 'ref,use_scope') exact.push(pointOf(target));
          else if (keys === 'engagement,logical_id,scope,version_id') exact.push(this.point(reference(target), effect.use_scope ?? effect.scope ?? registration.scope));
        }
        for (const target of exact.length ? exact : [null]) yield { ...base, kind: 'decision-effect', decisionRef: ref, effectKind: text(effect.op), targetPoint: target, effect: tag(effect).value, occurrence };
      }
    }
  }
}

/**
 * Tag a lossless parsed scalar/container with exact integer or float64 representation.
 * @param value Lossless parsed or application-constructed recorded value.
 * @param maximum Maximum encoded tag bytes; defaults to the existing complete-fact guard.
 * @returns Semantic value and exact compact UTF-8/backslashreplace byte count.
 * @throws {ImportError} For unsupported values, depth or encoded-size exhaustion.
 */
export function recordedSemantic(value: RecordedValue, maximum = FACT): { value: SemanticValue; size: number } { return tag(value, maximum); }
