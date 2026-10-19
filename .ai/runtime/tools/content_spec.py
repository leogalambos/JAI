#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Resolve proposed DCS profiles without replacing JAI authority or content QA.

Inputs are JSON (including JSON-compatible YAML). Compilation establishes a
structural blueprint; it cannot certify the truth or quality of a document.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
import sys

import jsonschema


class SpecError(ValueError):
    """Indicate malformed, ambiguous or conflicting content specifications."""


def canonical_hash(value):
    """Return a stable SHA256 of JSON-compatible value; reject nonfinite numbers.

    Args:
        value: JSON-compatible data, independent of mapping insertion order.
    Returns:
        Lowercase SHA256 hexadecimal digest.
    Raises:
        ValueError: If value is not valid finite JSON.
        TypeError: If value contains unsupported Python objects.
    """
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False).encode()).hexdigest()


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise SpecError(f'DUPLICATE_KEY: {key}')
        result[key] = value
    return result


def load_json(path):
    """Read strict JSON, also usable as the supported YAML subset.

    Args:
        path: Local file path; caller establishes trust and confinement.
    Returns:
        Parsed JSON value without duplicate keys or nonfinite numbers.
    Raises:
        SpecError: If parsing fails or a duplicate/nonfinite value appears.
        OSError: If the path cannot be read.
    """
    try:
        return json.loads(Path(path).read_text(encoding='utf-8'), object_pairs_hook=_pairs,
                          parse_constant=lambda value: (_ for _ in ()).throw(SpecError(f'NONFINITE: {value}')))
    except (json.JSONDecodeError, UnicodeError) as exc:
        raise SpecError(f'INVALID_JSON: {path}: {exc}') from exc


class ContentSpec:
    """Read and compile repository-local DCS drafts with fail-closed references.

    Args:
        root: Repository root, defaulting to this tool's repository.
    Raises:
        SpecError: If the registry is malformed or references escape content/.
        OSError: If required registry files cannot be read.
    """

    def __init__(self, root=None):
        self.root = Path(root if root is not None else Path(__file__).resolve().parents[1]).resolve()
        self.base = self.root / '.ai/runtime/content' if (self.root / '.ai/runtime').is_dir() else self.root / 'content'
        self.registry = load_json(self.base / 'registry.json')
        self.schema_path = Path(__file__).resolve().parent.parent / 'content/schema/document-content-spec.schema.json'
        self.schema = load_json(self.schema_path)
        if self.registry.get('schema_version') != '1.0.0':
            raise SpecError('UNSUPPORTED_SCHEMA_VERSION')
        entries = self.registry.get('specifications', self.registry.get('specs', []))
        self.entries = self._index(entries, 'specification')
        self.kinds = self._index(self.registry.get('document_kinds', []), 'document_kind')
        self.specs = {}
        for ident, entry in self.entries.items():
            spec = load_json(self._path(entry['path']))
            self._validate_spec(spec)
            if spec['id'] != ident or spec['version'] != entry.get('version', spec['version']):
                raise SpecError(f'VERSION_OR_ID_MISMATCH: {ident}')
            for metadata in ('category', 'status', 'completeness'):
                if metadata in entry and metadata in spec and entry[metadata] != spec[metadata]:
                    raise SpecError(f'REGISTRY_METADATA_MISMATCH: {ident}: {metadata}')
            self.specs[ident] = spec
        if 'binding_map_ref' in self.registry:
            mapping = load_json(self._path(self.registry['binding_map_ref']))
            bindings = mapping['bindings']
        else:
            bindings = self.registry.get('bindings', [])
        self.bindings = self._index(bindings, 'binding', 'artifact_id')

    def _index(self, records, label, key='id'):
        result = {}
        for record in records:
            ident = record.get(key)
            if not isinstance(ident, str) or not ident or ident in result:
                raise SpecError(f'INVALID_OR_DUPLICATE_{label.upper()}: {ident}')
            result[ident] = record
        return result

    def _path(self, relative):
        path = Path(relative)
        if path.is_absolute() or '..' in path.parts:
            raise SpecError(f'UNSAFE_PATH: {relative}')
        resolved = (self.base / path).resolve()
        if not resolved.is_relative_to(self.base.resolve()):
            raise SpecError(f'UNSAFE_PATH: {relative}')
        return resolved

    def _validate_spec(self, spec):
        if spec.get('completeness') == 'complete':
            try:
                jsonschema.Draft202012Validator(self.schema).validate(spec)
            except jsonschema.ValidationError as exc:
                raise SpecError(f'SCHEMA_INVALID: {spec.get("id")}: {exc.message}') from exc
        required = ('id', 'version', 'status', 'inherits', 'applies_to', 'purpose',
                    'required_information', 'conditional_information', 'optional_information', 'forbidden_information', 'size_budget')
        for key in required:
            if key not in spec:
                raise SpecError(f'MISSING_SPEC_FIELD: {spec.get("id")}: {key}')
        if spec['status'] not in ('proposed', 'approved', 'deprecated'):
            raise SpecError(f'INVALID_STATUS: {spec["id"]}')
        if spec.get('mode', spec.get('enforcement_mode', 'advisory')) != 'advisory':
            raise SpecError('HUMAN_L0_ACTIVATION_REQUIRED: foundation supports advisory only')
        if not isinstance(spec['inherits'], list) or any(not isinstance(ref, str) for ref in spec['inherits']):
            raise SpecError(f'INVALID_INHERITANCE: {spec["id"]}')
        if spec.get('completeness') == 'complete':
            for key in ('owner', 'effective_from', 'target_audience', 'decisions_supported', 'intended_usage', 'non_goals', 'sources', 'overlap', 'runtime', 'lifecycle', 'jai', 'approval', 'calibration_status'):
                if key not in spec:
                    raise SpecError(f'MISSING_COMPLETE_SPEC_FIELD: {spec["id"]}: {key}')
            if not spec['required_information'] or not spec['forbidden_information']:
                raise SpecError(f'EMPTY_COMPLETE_SPEC: {spec["id"]}')
        seen = set()
        for category in ('required_information', 'conditional_information', 'optional_information', 'forbidden_information', 'low_value_information'):
            for unit in spec.get(category, []):
                ident = unit.get('id')
                if not ident or ident in seen:
                    raise SpecError(f'DUPLICATE_UNIT: {spec["id"]}: {ident}')
                seen.add(ident)
                if spec.get('completeness') == 'complete':
                    for key in ('semantic_fields', 'datatype', 'obligation', 'acceptance_predicate', 'evidence_policy', 'rationale'):
                        if key not in unit:
                            raise SpecError(f'MISSING_UNIT_FIELD: {ident}: {key}')
                    if not unit['rationale'].get('reason') or not unit['semantic_fields']:
                        raise SpecError(f'UNJUSTIFIED_UNIT: {ident}')
                predicate = unit.get('acceptance_predicate')
                if predicate is not None and (not isinstance(predicate, dict) or predicate.get('op') not in ('nonempty', 'evidence', 'review')):
                    raise SpecError(f'INVALID_ACCEPTANCE_PREDICATE: {ident}')
                expected_obligation = {'required_information': 'MUST', 'conditional_information': 'CONDITIONAL', 'optional_information': 'MAY', 'forbidden_information': 'MUST NOT'}.get(category)
                if unit.get('obligation') and expected_obligation and unit['obligation'] != expected_obligation:
                    raise SpecError(f'INCONSISTENT_OBLIGATION: {ident}')
                if category == 'conditional_information' and not unit.get('when'):
                    raise SpecError(f'MISSING_APPLICABILITY: {ident}')
                if unit.get('when'):
                    self._condition(unit['when'], {}, validate_only=True)
                datatype = unit.get('datatype', unit.get('data_type'))
                if datatype is not None and datatype not in ('string', 'number', 'integer', 'boolean', 'array', 'object', 'reference', 'any'):
                    raise SpecError(f'INVALID_DATATYPE: {ident}')
        budget = spec['size_budget']
        for limit in ('soft_max', 'hard_max', 'max_limit'):
            value = budget.get(limit)
            if value is not None and (not isinstance(value, (int, float)) or isinstance(value, bool) or value < 0):
                raise SpecError(f'INVALID_BUDGET: {spec["id"]}: {limit}')
        canonical_hash(budget)
        target = budget.get('target', budget.get('target_range'))
        if target is not None and (not isinstance(target, list) or len(target) != 2 or any(not isinstance(n, (int, float)) or isinstance(n, bool) or n < 0 for n in target) or target[0] > target[1]):
            raise SpecError(f'INVALID_BUDGET: {spec["id"]}')

    def _condition(self, condition, context, validate_only=False):
        if not isinstance(condition, dict) or condition.get('op') not in ('eq', 'ne', 'in', 'present'):
            raise SpecError('INVALID_APPLICABILITY: only structured predicates are supported')
        field = condition.get('field', '')
        if field.startswith('context.'):
            field = field[8:]
        allowed = self.registry.get('context_fields', {})
        if field not in allowed:
            raise SpecError(f'UNKNOWN_CONTEXT_FIELD: {field}')
        if condition['op'] == 'in' and not isinstance(condition.get('value'), list):
            raise SpecError('INVALID_APPLICABILITY: in requires a list')
        if condition['op'] != 'present' and 'value' not in condition:
            raise SpecError('INVALID_APPLICABILITY: missing comparison value')
        if condition['op'] == 'present' and 'value' in condition:
            raise SpecError('INVALID_APPLICABILITY: present forbids a comparison value')
        if condition['op'] != 'present':
            operands = condition['value'] if condition['op'] == 'in' else [condition['value']]
            for operand in operands:
                try:
                    self._context({field: operand})
                except SpecError as exc:
                    raise SpecError(f'INVALID_APPLICABILITY: operand type for {field}') from exc
        if validate_only:
            return True
        if condition['op'] == 'present':
            return field in context
        if field not in context or context[field] is None:
            return None
        value, expected = context[field], condition.get('value')
        if condition['op'] == 'eq':
            return value == expected
        if condition['op'] == 'ne':
            return value != expected
        if not isinstance(expected, list):
            raise SpecError('INVALID_APPLICABILITY: in requires a list')
        return value in expected

    def _context(self, context):
        if context is not None and not isinstance(context, dict):
            raise SpecError('INVALID_CONTEXT: expected object')
        context = copy.deepcopy(context if context is not None else {})
        types = {'boolean': bool, 'string': str, 'number': (int, float), 'integer': int, 'array': list, 'object': dict}
        for field, value in context.items():
            definition = self.registry.get('context_fields', {}).get(field)
            if definition is None:
                raise SpecError(f'UNKNOWN_CONTEXT_FIELD: {field}')
            kind = definition.get('type') if isinstance(definition, dict) else definition
            if value is None:
                continue
            if kind not in types or not isinstance(value, types[kind]) or (kind in ('number', 'integer') and isinstance(value, bool)):
                raise SpecError(f'CONTEXT_TYPE_MISMATCH: {field}')
            if isinstance(definition, dict) and 'enum' in definition and not any(type(value) is type(candidate) and value == candidate for candidate in definition['enum']):
                raise SpecError(f'CONTEXT_ENUM_MISMATCH: {field}')
        canonical_hash(context)
        return context

    def list_specs(self):
        """Return independent registry entries sorted by ID.

        Returns:
            List of specification metadata dictionaries.
        """
        return [copy.deepcopy(self.entries[key]) for key in sorted(self.entries)]

    def compile(self, spec_ref, context=None, overlays=None):
        """Compile registered inheritance into a deterministic advisory blueprint.

        Args:
            spec_ref: Registered specification ID, optionally suffixed @version.
            context: Explicit typed applicability values; absent values stay pending.
            overlays: Registered overlay IDs applied after the selected profile.
        Returns:
            Compiled specification, hashes, units, budgets and approval limitations.
            Registered status/calibration metadata is preserved as a declaration;
            compilation never verifies approval or activates enforcement.
        Raises:
            SpecError: For unknown references, cycles, conflicts or invalid context.
        """
        context = self._context(context)
        if (self.base.parent / 'artifacts/contracts/role-deliverables.v3.json').is_file() and 'global/invariants' not in self.specs:
            raise SpecError('MISSING_GLOBAL_INVARIANTS')
        ordered, visiting, visited = [], set(), set()
        def visit(ref):
            ident, separator, version = ref.partition('@')
            if ident not in self.specs:
                raise SpecError(f'UNREGISTERED_REFERENCE: {ref}')
            if separator and self.specs[ident]['version'] != version:
                raise SpecError(f'VERSION_MISMATCH: {ref}')
            if ident in visiting:
                raise SpecError(f'INHERITANCE_CYCLE: {ident}')
            if ident in visited:
                return
            visiting.add(ident)
            for parent in self.specs[ident]['inherits']:
                visit(parent)
            visiting.remove(ident)
            visited.add(ident)
            ordered.append(self.specs[ident])
        if 'global/invariants' in self.specs:
            visit('global/invariants')
        selected_spec = self.specs.get(spec_ref.partition('@')[0], {})
        applicable_types = selected_spec.get('applies_to', {}).get('artifact_types', [])
        for artifact_type in applicable_types:
            type_ref = self.registry.get('mappings', {}).get('artifact_types', {}).get(artifact_type)
            if isinstance(type_ref, dict):
                type_ref = type_ref.get('spec_ref')
            if type_ref and type_ref != spec_ref:
                visit(type_ref)
        visit(spec_ref)
        for overlay in overlays or []:
            entry = self.entries.get(overlay.partition('@')[0], {})
            if entry.get('category') not in ('archetype', 'sabsa', 'domain'):
                raise SpecError(f'INVALID_OVERLAY_CATEGORY: {overlay}')
            visit(overlay)
        units, budgets = {}, {}
        for spec in ordered:
            for category in ('required_information', 'conditional_information', 'optional_information', 'forbidden_information', 'low_value_information'):
                for original in spec.get(category, []):
                    unit = copy.deepcopy(original)
                    if 'category' in unit:
                        unit['rule_category'] = unit['category']
                    unit['category'] = category
                    unit['source_spec'] = spec['id']
                    old = units.get(unit['id'])
                    if old:
                        self._merge_unit(old, unit)
                    else:
                        units[unit['id']] = unit
            budget = spec['size_budget']
            metric = budget.get('metric', budget.get('size_metric'))
            if metric:
                if metric in budgets:
                    old = budgets[metric]
                    for limit in ('soft_max', 'hard_max', 'max_limit'):
                        if limit in old and limit in budget and budget[limit] > old[limit]:
                            raise SpecError(f'SPEC_CONFLICT: weakened {limit} budget')
                    merged = dict(old)
                    merged.update(budget)
                    budgets[metric] = merged
                else:
                    budgets[metric] = copy.deepcopy(budget)
        field_rules = {}
        for unit in units.values():
            unit['applicability'] = self._condition(unit['when'], context) if unit.get('when') else True
        for unit in units.values():
            for field in unit.get('semantic_fields', []):
                previous_rules = field_rules.setdefault(field, [])
                for previous in previous_rules:
                    categories = {previous['category'], unit['category']}
                    requirements = {'required_information', 'conditional_information'}
                    if 'forbidden_information' in categories and categories & requirements and previous['applicability'] is not False and unit['applicability'] is not False:
                        raise SpecError(f'SPEC_CONFLICT: required and forbidden semantic field {field}')
                    if previous.get('datatype') != unit.get('datatype'):
                        raise SpecError(f'SPEC_CONFLICT: incompatible datatype for semantic field {field}')
                previous_rules.append(unit)
        selected = self.specs[spec_ref.partition('@')[0]]
        body = {'schema_version': '1.0.0', 'spec_id': selected['id'], 'spec_version': selected['version'],
                'resolved_content_spec_version': selected['version'], 'context_hash': canonical_hash(context),
                'context': context, 'inheritance': [{'id': s['id'], 'version': s['version'], 'hash': canonical_hash(s)} for s in ordered],
                'blueprint': {'semantic_units': [units[k] for k in sorted(units)], 'budgets': budgets},
                'status': selected['status'], 'mode': 'advisory', 'calibration_status': selected.get('calibration_status', 'synthetic-only'),
                'approval_status': 'pending-human-L0', 'production_ready': False,
                'jai_core': 'L1-L6', 'authority': 'existing JAI L0; no DCS authority acts',
                'limitations': ['Structural blueprint only; no semantic content certification.', 'Human professional approval and human-gold calibration remain required.']}
        body['compiled_spec_hash'] = canonical_hash(body)
        return body

    def _merge_unit(self, old, new):
        ident = new['id']
        for key in ('datatype', 'data_type', 'semantic_fields', 'semantic_field', 'when', 'evidence_policy', 'acceptance_predicate', 'acceptance_criteria', 'severity', 'thresholds', 'rule_category'):
            if key in old and old.get(key) != new.get(key, old[key]):
                raise SpecError(f'SPEC_CONFLICT: {ident}: incompatible {key}')
        if old['category'] in ('required_information', 'conditional_information', 'forbidden_information') and old['category'] != new['category']:
            raise SpecError(f'SPEC_CONFLICT: {ident}: obligation weakening')
        if not old.get('when') and new.get('when'):
            raise SpecError(f'SPEC_CONFLICT: {ident}: narrowed applicability')
        old.update(new)

    def resolve(self, artifact_id, context=None):
        """Resolve an explicit role-contract binding without name inference.

        Args:
            artifact_id: Exact stable v3 role contract ID.
            context: Typed context values used for applicability.
        Returns:
            Compiled blueprint with selection reason and migration state.
        Raises:
            SpecError: If binding, kind or selected reference is invalid.
        """
        binding = self.bindings.get(artifact_id)
        if binding is None:
            raise SpecError(f'UNBOUND_ARTIFACT: {artifact_id}')
        self._check_binding_provenance(artifact_id, binding)
        kind = self.kinds.get(binding.get('document_kind'))
        if kind is None:
            raise SpecError(f'UNREGISTERED_DOCUMENT_KIND: {binding.get("document_kind")}')
        artifact_type = binding.get('artifact_type')
        if artifact_type not in kind.get('artifact_types', []):
            raise SpecError(f'KIND_TYPE_MISMATCH: {artifact_id}')
        ref = binding.get('content_spec_ref', kind.get('spec_ref'))
        if ref != kind.get('spec_ref'):
            raise SpecError(f'KIND_SPEC_MISMATCH: {artifact_id}')
        selected = self.specs.get(ref.partition('@')[0], {})
        scope = selected.get('applies_to', {})
        if selected.get('category', 'document_kind') != 'document_kind' or scope.get('document_kind', kind['id']) != kind['id']:
            raise SpecError(f'KIND_SCOPE_MISMATCH: {artifact_id}')
        if scope.get('artifact_types') and artifact_type not in scope['artifact_types']:
            raise SpecError(f'KIND_SCOPE_TYPE_MISMATCH: {artifact_id}')
        for overlay in binding.get('overlays', []):
            overlay_spec = self.specs.get(overlay.partition('@')[0], {})
            overlay_types = overlay_spec.get('applies_to', {}).get('artifact_types', [])
            if overlay_types and artifact_type not in overlay_types:
                raise SpecError(f'OVERLAY_SCOPE_MISMATCH: {artifact_id}')
        result = self.compile(ref, context, binding.get('overlays', []))
        result.update(artifact_id=artifact_id, document_kind=kind['id'], spec_selection_reason='explicit stable role-contract binding',
                      decision_supported=copy.deepcopy(binding.get('decision_supported', {'status': 'pending-correction'})))
        result['resolution_hash'] = canonical_hash({'artifact_id': artifact_id, 'binding': binding, 'compiled_spec_hash': result['compiled_spec_hash'], 'context_hash': result['context_hash']})
        return result

    def outline(self, artifact_id, context=None):
        """Create an unfilled, hash-bound authoring outline without inventing facts.

        Args:
            artifact_id: Exact stable role contract identifier, not an instance ID.
            context: Explicit applicability values; unknown values stay pending.
        Returns:
            Semantic draft and separate blueprint with all required fields null.
        Raises:
            SpecError: If selection or applicability context is invalid.
        """
        compiled = self.resolve(artifact_id, context)
        fields = {}
        sections = []
        for unit in compiled['blueprint']['semantic_units']:
            if unit['category'] in ('required_information', 'conditional_information'):
                for field in unit['semantic_fields']:
                    current = fields
                    parts = field.split('.')
                    for part in parts[:-1]:
                        current = current.setdefault(part, {})
                    current[parts[-1]] = None
                sections.append({'unit_id': unit['id'], 'semantic_fields': unit['semantic_fields'],
                                 'datatype': unit['datatype'], 'applicability': unit['applicability'],
                                 'acceptance_criteria': unit.get('acceptance_criteria', []),
                                 'evidence_policy': unit.get('evidence_policy', {}),
                                 'rationale': unit.get('rationale', {})})
        return {'semantic_model': {'artifact_id': None, 'contract_id': artifact_id,
                                  'document_kind': compiled['document_kind'],
                                  'compiled_spec_hash': compiled['compiled_spec_hash'],
                                  'context': compiled['context'], 'semantic_units': fields,
                                  'claims': [], 'evidence': [], 'evaluation_date': None},
                'blueprint': sections, 'compiled_spec': compiled,
                'authoring_status': 'DRAFT_INCOMPLETE', 'production_ready': False}

    def _check_binding_provenance(self, artifact_id, binding):
        path = self.base.parent / 'artifacts/contracts/role-deliverables.v3.json'
        if not path.is_file():
            return
        if not hasattr(self, '_contracts'):
            self._contracts = {c['id']: c for c in load_json(path)['contracts']}
        contract = self._contracts.get(artifact_id)
        if contract is None or binding.get('source_fingerprint') != contract.get('source_fingerprint') or binding.get('source_hash') != canonical_hash(contract):
            raise SpecError(f'BINDING_PROVENANCE_MISMATCH: {artifact_id}')
        if binding.get('artifact_type') != contract['jai']['semantics']['artifact_type']:
            raise SpecError(f'BINDING_TYPE_MISMATCH: {artifact_id}')

    def lint_registry(self):
        """Collect deterministic registry and binding errors without changing files.

        Returns:
            Sorted unique error strings; an empty list means structural consistency.
        """
        errors = []
        contract_path = self.base.parent / 'artifacts/contracts/role-deliverables.v3.json'
        if contract_path.is_file():
            contracts = {c['id']: c for c in load_json(contract_path)['contracts']}
            for ident in sorted(set(contracts) ^ set(self.bindings)):
                errors.append(f'BINDING_CATALOG_MISMATCH: {ident}')
            for ident in sorted(set(contracts) & set(self.bindings)):
                binding, contract = self.bindings[ident], contracts[ident]
                if binding.get('artifact_type') != contract['jai']['semantics']['artifact_type']:
                    errors.append(f'BINDING_TYPE_MISMATCH: {ident}')
                if binding.get('source_fingerprint') != contract.get('source_fingerprint') or binding.get('source_hash') != canonical_hash(contract):
                    errors.append(f'BINDING_PROVENANCE_MISMATCH: {ident}')
        for ident in self.specs:
            try:
                self.compile(ident)
            except (SpecError, KeyError, TypeError) as exc:
                errors.append(str(exc))
        for ident in self.bindings:
            try:
                self.resolve(ident)
            except (SpecError, KeyError, TypeError) as exc:
                errors.append(f'{ident}: {exc}')
        canonical_sets = {}
        type_path = self.base.parent / 'artifacts/schema/artifact-types.json'
        sabsa_path = self.base.parent / 'sabsa/schema/documents.json'
        archetype_dir = self.base.parent / 'publication/archetypes'
        if type_path.is_file():
            canonical_sets['artifact_types'] = set(load_json(type_path)['artifact_types'])
        if sabsa_path.is_file():
            canonical_sets['sabsa_views'] = set(load_json(sabsa_path)['views'])
        if archetype_dir.is_dir():
            canonical_sets['archetypes'] = {p.stem for p in archetype_dir.glob('*.json')}
        for category, expected in canonical_sets.items():
            actual = set(self.registry.get('mappings', {}).get(category, {}))
            for ident in sorted(expected ^ actual):
                errors.append(f'MAPPING_CATALOG_MISMATCH: {category}/{ident}')
        if canonical_sets:
            if 'global/invariants' not in self.specs or self.entries.get('global/invariants', {}).get('category') != 'global':
                errors.append('MISSING_GLOBAL_INVARIANTS')
            priorities = self.registry.get('priority_document_kinds', [])
            expected = {'decision-paper', 'adr', 'business-case', 'risk-assessment', 'assurance-report', 'architecture-definition', 'hld', 'operational-handover', 'runbook', 'test-report'}
            if set(priorities) != expected or len(priorities) != 10:
                errors.append('PRIORITY_CATALOG_MISMATCH')
            for kind in priorities:
                definition = self.kinds.get(kind, {})
                if self.specs.get(definition.get('spec_ref'), {}).get('completeness') != 'complete':
                    errors.append(f'PRIORITY_NOT_COMPLETE: {kind}')
        for category, mapping in self.registry.get('mappings', {}).items():
            for ident, ref in mapping.items():
                if isinstance(ref, dict):
                    ref = ref.get('spec_ref')
                expected_category = {'artifact_types': 'type', 'archetypes': 'archetype', 'sabsa_views': 'sabsa'}.get(category)
                if ref in self.entries and expected_category and self.entries[ref].get('category') != expected_category:
                    errors.append(f'MAPPING_CATEGORY_MISMATCH: {category}/{ident}')
                if ref not in self.specs:
                    errors.append(f'UNREGISTERED_MAPPING: {category}/{ident}: {ref}')
        return sorted(set(errors))

    def coverage(self):
        """Report structural counts and approval gaps without certifying completion.

        Returns:
            JSON-compatible coverage dictionary including pending decision migration.
        """
        counts = {}
        for category in ('artifact_types', 'archetypes', 'sabsa_views'):
            counts[category] = len(self.registry.get('mappings', {}).get(category, self.registry.get(category, [])))
        priorities = self.registry.get('priority_document_kinds', [])
        complete = [k for k in priorities if k in self.kinds and self.specs.get(self.kinds[k]['spec_ref'], {}).get('completeness') == 'complete']
        decisions = {}
        for binding in self.bindings.values():
            decision = binding.get('decision_supported', {})
            status = decision.get('status', 'pending-correction') if isinstance(decision, dict) else 'pending-correction'
            decisions[status] = decisions.get(status, 0) + 1
        return {'schema_version': '1.0.0', 'bindings': len(self.bindings), 'document_kinds': len(self.kinds),
                **counts, 'priority_complete': len(complete), 'priority_document_kinds': priorities,
                'decision_supported_migration': decisions, 'errors': self.lint_registry(),
                'calibration_status': 'synthetic-only', 'production_ready': False, 'approval_status': 'pending-human-L0'}


def lint_registry(root=None):
    """Return structural lint errors for integration with existing artifact checks.

    Args:
        root: Repository root; defaults to this tool's repository.
    Returns:
        List of error messages, empty on structural success.
    """
    try:
        return ContentSpec(root).lint_registry()
    except (SpecError, OSError, KeyError, TypeError, ValueError) as exc:
        return [str(exc)]


def main(argv=None):
    """Run the read-only DCS CLI and print JSON.

    Args:
        argv: Argument list or None to read process arguments.
    Returns:
        Zero for structural success; one for invalid inputs or lint errors.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root')
    sub = parser.add_subparsers(dest='command', required=True)
    for name in ('list', 'compile', 'resolve', 'lint-registry', 'coverage', 'outline'):
        command = sub.add_parser(name)
        command.add_argument('--root', dest='command_root')
        command.add_argument('--output')
        if name in ('compile', 'resolve', 'outline'):
            command.add_argument('--context')
        if name == 'compile':
            command.add_argument('--spec-ref', '--spec', required=True)
        if name in ('resolve', 'outline'):
            command.add_argument('--artifact-id', required=True)
    args = parser.parse_args(argv)
    try:
        engine = ContentSpec(args.command_root or args.root)
        context = load_json(args.context) if getattr(args, 'context', None) else None
        if args.command == 'list':
            result = engine.list_specs()
        elif args.command == 'compile':
            result = engine.compile(args.spec_ref, context)
        elif args.command == 'resolve':
            result = engine.resolve(args.artifact_id, context)
        elif args.command == 'outline':
            result = engine.outline(args.artifact_id, context)
        elif args.command == 'lint-registry':
            result = {'errors': engine.lint_registry()}
        else:
            result = engine.coverage()
        serialized = json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False)
        if args.output:
            Path(args.output).write_text(serialized + '\n', encoding='utf-8')
        else:
            print(serialized)
        return 1 if isinstance(result, dict) and result.get('errors') else 0
    except (SpecError, OSError, KeyError, TypeError, ValueError) as exc:
        print(json.dumps({'error': str(exc)}))
        return 1


if __name__ == '__main__':
    sys.exit(main())
