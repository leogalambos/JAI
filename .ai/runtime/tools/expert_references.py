#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Validate and select proposed Markdown references without changing JAI policy.

All operations are local and offline. Public diagnostics never disclose private
paths, reference identifiers, source text or fingerprints. Successful validation
establishes metadata, structural coverage and content presence, not professional
adequacy, evidence validity, executed tests or human approval.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import sys
import tempfile
import uuid

import jsonschema
import yaml

from content_spec import ContentSpec, load_json

LEVELS = ('simple', 'medium', 'complex')
MAX_BYTES = 2 * 1024 * 1024


class ReferenceError(ValueError):
    """Indicate a safe diagnostic code, never containing private source details."""


class _UniqueLoader(yaml.SafeLoader):
    pass


def _mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if not isinstance(key, str) or key in result:
            raise ReferenceError('METADATA_DUPLICATE_OR_NONSTRING_KEY')
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


_UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _mapping)


def _read(path):
    try:
        path = Path(path)
        if path.is_symlink() or not path.is_file() or path.stat().st_size > MAX_BYTES:
            raise ReferenceError('SOURCE_NOT_REGULAR_OR_TOO_LARGE')
        return path.read_bytes()
    except OSError:
        raise ReferenceError('SOURCE_UNREADABLE') from None


def _parse(raw):
    try:
        text = raw.decode('utf-8')
        match = re.match(r'\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)', text, re.S)
        if not match:
            raise ReferenceError('METADATA_HEADER_REQUIRED')
        metadata = yaml.load(match.group(1), Loader=_UniqueLoader)
        if not isinstance(metadata, dict):
            raise ReferenceError('METADATA_OBJECT_REQUIRED')
        return metadata, text[match.end():]
    except (UnicodeError, yaml.YAMLError, TypeError, ValueError) as exc:
        if isinstance(exc, ReferenceError):
            raise
        raise ReferenceError('METADATA_INVALID') from None


class _Anchors(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = []
        self.bad = False

    def handle_starttag(self, tag, attrs):
        values = [value for key, value in attrs if key == 'id']
        for value in values:
            if value and value.startswith('dcs-'):
                self.ids.append(value[4:])
                if tag != 'a' or len(values) != 1:
                    self.bad = True


def _visible_lines(body):
    lines = body.splitlines()
    result = []
    fence = None
    comment = False
    for line in lines:
        if comment:
            if '-->' in line:
                comment = False
            result.append('')
            continue
        if line.lstrip().startswith('<!--'):
            comment = '-->' not in line
            result.append('')
            continue
        match = re.match(r'^ {0,3}(`{3,}|~{3,})', line)
        if match:
            mark = match.group(1)
            if fence is None:
                fence = mark
            elif mark[0] == fence[0] and len(mark) >= len(fence):
                fence = None
            result.append('')
            continue
        if fence is not None or line.startswith(('    ', '\t')):
            result.append('')
        else:
            result.append(line)
    return result


def _structure(body, required, allowed=None):
    allowed = required if allowed is None else allowed
    lines = _visible_lines(body)
    found = []
    sections = {}
    findings = []
    for position, line in enumerate(lines):
        parser = _Anchors()
        parser.feed(line)
        if not parser.ids:
            continue
        found.extend(parser.ids)
        if parser.bad or len(parser.ids) != 1 or not re.fullmatch(r'\s*<a\s+id=[\'"]dcs-[a-z0-9_.-]+[\'"]\s*>\s*</a>\s*', line):
            findings.append({'rule': 'anchor.inconsistent', 'unit': parser.ids[0] if parser.ids[0] in allowed else 'unrecognized'})
            continue
        unit = parser.ids[0]
        after = position + 1
        while after < len(lines) and not lines[after].strip():
            after += 1
        heading = re.match(r'^ {0,3}(#{1,6})\s+\S', lines[after]) if after < len(lines) else None
        if not heading:
            findings.append({'rule': 'anchor.heading_missing', 'unit': unit if unit in allowed else 'unrecognized'})
            continue
        end = after + 1
        while end < len(lines):
            other = re.match(r'^ {0,3}(#{1,6})\s+', lines[end])
            if 'dcs-' in lines[end] and '<a' in lines[end] or other and len(other.group(1)) <= len(heading.group(1)):
                break
            end += 1
        value = '\n'.join(lines[after + 1:end]).strip()
        cleaned = re.sub(r'<[^>]+>|[#*`_|>\[\]()=-]', ' ', value)
        substantive = re.sub(r'\b(?:todo|tbd|placeholder|pending|unknown|not applicable|n/a)\b', '', cleaned, flags=re.I)
        if not re.search(r'[A-Za-z0-9]', substantive):
            findings.append({'rule': 'content.empty_or_placeholder', 'unit': unit if unit in allowed else 'unrecognized'})
        sections[unit] = bool(re.search(r'[A-Za-z0-9]', substantive))
    counts = Counter(found)
    for unit in required:
        if counts[unit] == 0:
            findings.append({'rule': 'anchor.missing', 'unit': unit})
    for unit, count in counts.items():
        if count > 1:
            findings.append({'rule': 'anchor.duplicate', 'unit': unit if unit in allowed else 'unrecognized'})
        if unit not in allowed:
            findings.append({'rule': 'anchor.unknown', 'unit': 'unrecognized'})
    for target in re.findall(r'\]\(#(dcs-[a-z0-9_.-]+)\)', '\n'.join(lines)):
        if target[4:] not in counts:
            findings.append({'rule': 'reference.dangling_dcs_link', 'unit': target[4:] if target[4:] in allowed else 'unrecognized'})
    return sections, findings


def _root_path(root):
    path = Path(root).absolute()
    if path.resolve() != path or path.is_symlink() or path.exists() and not path.is_dir():
        raise ReferenceError('SCOPE_ROOT_INVALID_OR_SYMLINK')
    return path


def _child(root, relative):
    path = root / relative
    if path.resolve() != path.absolute() or not path.is_relative_to(root):
        raise ReferenceError('SOURCE_ESCAPE_OR_SYMLINK')
    return path


def _selection_context(context, audience):
    if context is not None:
        if not isinstance(context, dict) or not all(isinstance(key, str) for key in context):
            raise ReferenceError('REFERENCE_CONTEXT_INVALID')
        try:
            json.dumps(context, allow_nan=False)
        except (ValueError, TypeError):
            raise ReferenceError('REFERENCE_CONTEXT_INVALID') from None
    if audience is not None and (not isinstance(audience, str) or not audience.strip() or len(audience) > 160):
        raise ReferenceError('REFERENCE_AUDIENCE_INVALID')


class ExpertReferences:
    """Use the trusted installed DCS registry and immutable bundled defaults.

    Args:
        root: Source repository root or installed runtime root; None auto-detects.
    Raises:
        ReferenceError: If the reference manifest or registry cannot be loaded.
    """

    def __init__(self, root=None):
        try:
            self.specs = ContentSpec(root)
            self.base = self.specs.base / 'expert_references'
            self.manifest = load_json(self.base / 'index.json')
            self.schema = load_json(self.specs.base / 'schema/expert-reference.schema.json')
            self.entries = self.manifest['entries']
            self.families = tuple(self.manifest['families'])
            keys = {'reference_id', 'document_kind', 'complexity', 'path', 'language', 'provenance',
                    'approval_status', 'sha256', 'bytes', 'anchor_ids'}
            if not isinstance(self.entries, list) or any(
                    not isinstance(entry, dict) or not keys.issubset(entry)
                    or not all(isinstance(entry[key], str) for key in keys - {'bytes', 'anchor_ids'})
                    or not re.fullmatch(r'[0-9a-f]{64}', entry['sha256'])
                    or type(entry['bytes']) is not int or entry['bytes'] < 0
                    or not isinstance(entry['anchor_ids'], list)
                    or not all(isinstance(unit, str) for unit in entry['anchor_ids'])
                    for entry in self.entries):
                raise ReferenceError('MANIFEST_ENTRIES_INVALID')
            if len(self.families) != 45 or len(set(self.families)) != 45 or set(self.manifest['levels']) != set(LEVELS):
                raise ReferenceError('MANIFEST_FAMILIES_INVALID')
            self.bindings = self._load_bindings()
        except (OSError, ValueError, KeyError, TypeError, AttributeError):
            raise ReferenceError('REGISTRY_OR_MANIFEST_INVALID') from None

    def _load_bindings(self):
        document = load_json(self.specs.base / 'expert-reference-bindings.json')
        bindings = document['families']
        result = {}
        if document.get('status') != 'proposed' or len(bindings) != len(self.families):
            raise ReferenceError('REFERENCE_BINDING_MANIFEST_INVALID')
        for binding in bindings:
            family = binding['reference_family']
            if family not in self.families or family in result or binding.get('status') != 'proposed':
                raise ReferenceError('REFERENCE_BINDING_FAMILY_INVALID')
            definition = self.specs.specs[binding['spec_ref']]
            if definition.get('category') != 'document_kind' or definition.get('applies_to', {}).get('document_kind') != binding['document_kind']:
                raise ReferenceError('REFERENCE_BINDING_KIND_INVALID')
            sources = [item['source_anchor'] for item in binding['anchor_bindings']]
            targets = [item['unit_id'] for item in binding['anchor_bindings']]
            if (not sources or len(sources) != len(set(sources)) or len(targets) != len(set(targets))
                    or not all(isinstance(source, str) and re.fullmatch(r'dcs-[a-z0-9_.-]+', source) for source in sources)
                    or not all(isinstance(target, str) for target in targets)
                    or not all(contract in self.specs.bindings for contract in binding.get('role_contract_ids', []))):
                raise ReferenceError('REFERENCE_ANCHOR_BINDING_INVALID')
            result[family] = binding
        self.authoring_defaults = document.get('authoring_defaults', {})
        if not isinstance(self.authoring_defaults, dict) or any(
                contract not in self.specs.bindings or family not in result
                or contract not in result[family].get('role_contract_ids', [])
                for contract, family in self.authoring_defaults.items()):
            raise ReferenceError('REFERENCE_AUTHORING_DEFAULT_INVALID')
        return result

    def canonical_family(self, kind, contract_id=None):
        """Map an explicit reference family, canonical kind or role to one family.

        Args:
            kind: Registered reference family or canonical DCS document kind.
            contract_id: Optional existing role contract to disambiguate mappings.
        Returns:
            One public reference-family identifier.
        Raises:
            ReferenceError: On unsupported or ambiguous selection; titles are unused.
        """
        if contract_id in self.authoring_defaults:
            return self.authoring_defaults[contract_id]
        if contract_id is not None:
            role_choices = [family for family, binding in self.bindings.items()
                            if contract_id in binding.get('role_contract_ids', [])]
            if len(role_choices) == 1:
                return role_choices[0]
            if len(role_choices) > 1:
                role_choices = [family for family in role_choices
                                if family == kind or self.bindings[family]['document_kind'] == kind]
                if len(role_choices) == 1:
                    return role_choices[0]
                raise ReferenceError('REFERENCE_FAMILY_AMBIGUOUS')
        if kind in self.families:
            return kind
        choices = [family for family, binding in self.bindings.items()
                   if binding['document_kind'] == kind or binding['spec_ref'] == kind]
        if contract_id is not None:
            exact = [family for family in choices if contract_id in self.bindings[family].get('role_contract_ids', [])]
            if exact:
                choices = exact
        if not choices:
            raise ReferenceError('REFERENCE_SLOT_UNSUPPORTED')
        if len(choices) != 1:
            raise ReferenceError('REFERENCE_FAMILY_AMBIGUOUS')
        return choices[0]

    def validate(self, path, kind=None, complexity=None, bundled=False):
        """Check metadata, exact DCS anchors and nonempty English section bodies.

        Args:
            path: Local Markdown file; never included in returned diagnostics.
            kind: Expected registered family, or None to use validated metadata.
            complexity: Expected simple/medium/complex slot, or None from metadata.
            bundled: Require supplied synthetic provenance and manifest checksum.
        Returns:
            Sanitized structured result; professional/evidence quality stay pending.
        Raises:
            ReferenceError: On malformed metadata, file, identity, anchors or checksum.
        """
        return self._validate_raw(_read(path), kind, complexity, bundled)

    def _validate_raw(self, raw, kind=None, complexity=None, bundled=False):
        meta, body = _parse(raw)
        errors = list(jsonschema.Draft202012Validator(self.schema).iter_errors(meta))
        if errors:
            fields = sorted({str(error.path[0]) for error in errors if error.path and error.path[0] in self.schema['properties']})
            raise ReferenceError('METADATA_SCHEMA_INVALID' + (':' + ','.join(fields) if fields else ''))
        _selection_context(meta.get('applicability_context'), None)
        family = meta['document_kind']
        level = meta['complexity']
        if kind is not None:
            kind = self.canonical_family(kind)
        if family not in self.families or kind is not None and kind != family or complexity is not None and complexity != level:
            raise ReferenceError('REFERENCE_SLOT_MISMATCH')
        mapping = self.bindings[family]
        accepted_dcs = {'kind/' + family, 'proposed/kind/' + family}
        if meta['applicable_dcs'] not in accepted_dcs:
            raise ReferenceError('DCS_IDENTITY_MISMATCH')
        source_proposed = meta['applicable_dcs'].startswith('proposed/')
        if source_proposed and meta.get('dcs_status') not in ('proposed-unmapped', 'proposed-not-mapped', 'proposed-mapped'):
            raise ReferenceError('PROPOSED_DCS_STATUS_REQUIRED')
        try:
            dcs = self.specs.specs[mapping['spec_ref']]
            required = [unit['id'] for unit in dcs['required_information'] if unit.get('obligation') == 'MUST']
            allowed_units = [unit['id'] for key in ('required_information', 'conditional_information', 'optional_information') for unit in dcs.get(key, [])]
            translation = {item['source_anchor'][4:]: item['unit_id'] for item in mapping['anchor_bindings']}
            source_required = list(translation)
            if set(translation.values()) != set(required):
                raise ReferenceError('DCS_BINDING_COVERAGE_MISMATCH')
            allowed = list(translation) + [unit for unit in allowed_units if unit not in required]
        except (ValueError, KeyError, TypeError):
            raise ReferenceError('DCS_REGISTRY_INVALID') from None
        if bundled:
            expected = [item for item in self.entries if item['document_kind'] == family and item['complexity'] == level]
            if len(expected) != 1:
                raise ReferenceError('MANIFEST_SLOT_AMBIGUOUS')
            entry = expected[0]
            if (meta['classification'] != 'public-synthetic' or meta['provenance'] != 'ai-authored-proposed'
                    or meta['fictional_context'] is not True or entry['sha256'] != hashlib.sha256(raw).hexdigest()
                    or entry['bytes'] != len(raw) or entry['reference_id'] != meta['reference_id']
                    or set(entry['anchor_ids']) != set(source_required)
                    or len(entry['anchor_ids']) != len(source_required)
                    or entry.get('language') != meta['language']
                    or entry.get('provenance') != meta['provenance']
                    or entry.get('approval_status') != meta['approval_status']
                    or any(entry.get(field) != meta.get(field) for field in ('case_id', 'methodology_context'))
                    or entry.get('proposal_pack_id') != meta.get('proposal_pack_id')
                    or bool(meta.get('proposal_pack_id')) != (family in self.manifest.get('proposal_extension', {}).get('new_families', []))):
                raise ReferenceError('BUNDLED_INTEGRITY_MISMATCH')
        sections, findings = _structure(body, source_required, allowed)
        if findings:
            for finding in findings:
                unit = finding.get('unit')
                if unit in translation:
                    finding['source_anchor'] = 'dcs-' + unit
                    finding['unit'] = translation[unit]
            raise ReferenceError('REFERENCE_INVALID:' + json.dumps(findings, sort_keys=True, separators=(',', ':')))
        budget = dcs.get('size_budget', {})
        measure = len(re.findall(r'\b[\w]+\b', body)) if budget.get('metric') == 'words' else None
        upper = budget.get('soft_max')
        size_findings = []
        if measure is not None and type(upper) in (int, float) and measure > upper:
            size_findings.append({'rule': 'size.soft_max_exceeded', 'severity': 'advisory', 'blocking': False})
        return {'document_kind': family, 'reference_family': family, 'canonical_document_kind': mapping['document_kind'],
                'spec_ref': mapping['spec_ref'], 'mapping_status': 'proposed',
                'source_dcs_status': meta.get('dcs_status', 'existing-structural-binding'),
                'complexity': level, 'language': 'en',
                'classification': meta['classification'], 'provenance': meta['provenance'],
                'approval_status': 'not-human-approved', 'structural_coverage': 'PASS',
                'content_presence': 'PASS', 'content_adequacy': 'NOT_EVALUATED',
                'evidence_and_rationale_quality': 'NOT_EVALUATED',
                'professional_acceptance': 'NOT_APPROVED',
                'required_units': required, 'reference_required_anchors': ['dcs-' + unit for unit in source_required],
                'present_units': [translation[unit] for unit in source_required if sections.get(unit)],
                'cross_reference_integrity': 'PASS_DCS_LINKS_ONLY',
                'size_budget': {'metric': budget.get('metric'), 'status': 'NOT_MEASURED' if measure is None else 'MEASURED', 'excess': bool(size_findings)},
                'findings': size_findings}

    def validate_all(self):
        """Validate all 135 bundled manifest slots and their raw checksums.

        Returns:
            Sanitized collection count and results; contains only public metadata.
        Raises:
            ReferenceError: If slots, paths, checksums, metadata or anchors differ.
        """
        expected = {(kind, level) for kind in self.families for level in LEVELS}
        try:
            slots = [(item['document_kind'], item['complexity']) for item in self.entries]
            if (len(slots) != 135 or set(slots) != expected or self.manifest['reference_count'] != 135
                    or len({item['reference_id'] for item in self.entries}) != 135):
                raise ReferenceError('MANIFEST_COVERAGE_INVALID')
            results = []
            for entry in self.entries:
                kind, level = entry['document_kind'], entry['complexity']
                if entry['path'] != f'{kind}/{level}.md':
                    raise ReferenceError('MANIFEST_PATH_INVALID')
                results.append(self.validate(_child(_root_path(self.base), entry['path']), kind, level, bundled=True))
            actual = {str(path.relative_to(self.base)) for path in self.base.rglob('*.md') if path.name != 'README.md'}
            if actual != {item['path'] for item in self.entries}:
                raise ReferenceError('BUNDLED_UNINDEXED_REFERENCE')
            return {'status': 'PASS', 'reference_count': len(results), 'family_count': len(self.families),
                    'proposal_reference_count': sum('proposal_pack_id' in entry for entry in self.entries),
                    'professional_acceptance': 'NOT_APPROVED', 'results': results}
        except (KeyError, TypeError, OSError):
            raise ReferenceError('MANIFEST_INVALID') from None

    def resolve(self, kind, complexity, user_root=None, organisation_root=None, engagement_root=None,
                context=None, audience=None):
        """Select one reference at the highest existing applicable precedence.

        Args:
            kind: One of the bundled document families.
            complexity: simple, medium or complex.
            user_root: Explicit root, else XDG_CONFIG_HOME/jai/expert_references.
            organisation_root: Explicit root, else JAI_EXPERT_REFERENCES_DIR.
            engagement_root: Explicitly authorized engagement root, else absent.
            context: Optional explicit finite JSON applicability values; never logged.
            audience: Optional explicit target audience; never logged.
        Returns:
            (local Path, sanitized report); callers must keep the Path private.
        Raises:
            ReferenceError: On ambiguity, unsafe paths, invalid selected file or absence.
        """
        kind = self._slot(kind, complexity)
        _selection_context(context, audience)
        user_root = user_root if user_root is not None else Path(os.environ.get('XDG_CONFIG_HOME', str(Path.home() / '.config'))) / 'jai/expert_references'
        organisation_root = organisation_root if organisation_root is not None else os.environ.get('JAI_EXPERT_REFERENCES_DIR')
        scopes = [('engagement', engagement_root), ('organisation', organisation_root), ('user', user_root), ('bundled', self.base)]
        for scope, configured in scopes:
            if configured is None:
                continue
            root = _root_path(configured)
            candidates = self._candidates(root, kind, complexity)
            try:
                candidates = [candidate for candidate in candidates if self._applicable(candidate, context, audience, kind, complexity)]
            except ReferenceError as exc:
                raise ReferenceError('SELECTED_REFERENCE_INVALID:' + scope + ':' + str(exc)) from None
            if len(candidates) > 1:
                raise ReferenceError('REFERENCE_CONFLICT:' + scope)
            if candidates:
                try:
                    report = self.validate(candidates[0], kind, complexity, bundled=scope == 'bundled')
                except ReferenceError as exc:
                    raise ReferenceError('SELECTED_REFERENCE_INVALID:' + scope + ':' + str(exc)) from None
                report['scope'] = scope
                report['selection_context'] = {'context_supplied': context is not None, 'audience_supplied': audience is not None}
                return candidates[0], report
        raise ReferenceError('REFERENCE_NOT_FOUND')

    def _applicable(self, path, context, audience, kind, complexity):
        meta, _ = _parse(_read(path))
        if list(jsonschema.Draft202012Validator(self.schema).iter_errors(meta)):
            raise ReferenceError('METADATA_SCHEMA_INVALID')
        if meta['document_kind'] != kind or meta['complexity'] != complexity:
            raise ReferenceError('REFERENCE_SLOT_MISMATCH')
        if meta['applicable_dcs'] not in {'kind/' + kind, 'proposed/kind/' + kind}:
            raise ReferenceError('DCS_IDENTITY_MISMATCH')
        if meta['applicable_dcs'].startswith('proposed/') and meta.get('dcs_status') not in ('proposed-unmapped', 'proposed-not-mapped', 'proposed-mapped'):
            raise ReferenceError('PROPOSED_DCS_STATUS_REQUIRED')
        constraints = meta.get('applicability_context', {})
        _selection_context(constraints, None)
        if any(key not in (context or {}) or type((context or {})[key]) is not type(value)
               or (context or {})[key] != value for key, value in constraints.items()):
            return False
        audiences = meta.get('target_audiences')
        return audiences is None or audience is not None and audience in audiences

    def _candidates(self, root, kind, complexity):
        directory = _child(root, kind)
        canonical = _child(root, f'{kind}/{complexity}.md')
        candidates = [canonical] if canonical.exists() else []
        if directory.exists():
            if not directory.is_dir():
                raise ReferenceError('SCOPE_FAMILY_NOT_DIRECTORY')
            for other in sorted(directory.glob('*.md')):
                if other == canonical:
                    continue
                _child(root, str(other.relative_to(root)))
                try:
                    meta, _ = _parse(_read(other))
                except ReferenceError:
                    # Only canonical filenames or readable slot metadata select a reference.
                    continue
                if meta.get('document_kind') == kind and meta.get('complexity') == complexity:
                    candidates.append(other)
        return candidates

    def _slot(self, kind, complexity):
        kind = self.canonical_family(kind)
        if complexity not in LEVELS:
            raise ReferenceError('REFERENCE_SLOT_UNSUPPORTED')
        return kind

    def install(self, source, kind, complexity, scope_root):
        """Validate then atomically install an external override with a backup.

        Args:
            source: Local Markdown input; source identifiers stay private.
            kind: Registered family matching the source metadata.
            complexity: Slot matching the source metadata.
            scope_root: Explicit writable override root outside bundled content.
        Returns:
            Sanitized validation report, with backup_created boolean.
        Raises:
            ReferenceError: On invalid content, unsafe paths or atomic I/O failure.
        """
        kind = self._slot(kind, complexity)
        raw = _read(source)
        report = self._validate_raw(raw, kind, complexity)
        root = self._writable_root(scope_root)
        target = _child(root, f'{kind}/{complexity}.md')
        if any(candidate != target for candidate in self._candidates(root, kind, complexity)):
            raise ReferenceError('REFERENCE_CONFLICT:install-scope')
        try:
            target.parent.mkdir(parents=True, exist_ok=True)
            backup = target.exists()
            if backup:
                _atomic(target.with_name(target.name + '.backup-' + uuid.uuid4().hex), _read(target))
            _atomic(target, raw)
        except OSError:
            raise ReferenceError('INSTALL_IO_FAILED') from None
        report['backup_created'] = backup
        return report

    def reset(self, kind, complexity, scope_root):
        """Back up and remove only the requested canonical override slot.

        Args:
            kind: Registered document family.
            complexity: simple, medium or complex.
            scope_root: Explicit nonbundled writable root.
        Returns:
            Sanitized removed boolean; next resolution obeys normal precedence.
        Raises:
            ReferenceError: On unsafe root/path or failed file operations.
        """
        kind = self._slot(kind, complexity)
        root = self._writable_root(scope_root)
        target = _child(root, f'{kind}/{complexity}.md')
        try:
            if not target.exists():
                return {'removed': False}
            _atomic(target.with_name(target.name + '.backup-' + uuid.uuid4().hex), _read(target))
            target.unlink()
            return {'removed': True}
        except OSError:
            raise ReferenceError('RESET_IO_FAILED') from None

    def _writable_root(self, scope_root):
        root = _root_path(scope_root)
        bundled = self.base.resolve()
        if root == bundled or root.is_relative_to(bundled) or bundled.is_relative_to(root):
            raise ReferenceError('BUNDLED_REFERENCE_IMMUTABLE')
        return root


def _atomic(target, raw):
    descriptor, temporary = tempfile.mkstemp(prefix='.reference-', dir=target.parent)
    try:
        with os.fdopen(descriptor, 'wb') as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, target)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def main(argv=None):
    """Run the offline reference CLI and print sanitized JSON diagnostics.

    Args:
        argv: Optional argument sequence, otherwise process arguments.
    Returns:
        Zero for successful validation/selection; one for rejected operation.
    Raises:
        SystemExit: For argparse usage errors only.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('list', 'validate', 'resolve', 'inspect', 'install', 'reset'))
    parser.add_argument('--root')
    parser.add_argument('--source')
    parser.add_argument('--all', action='store_true')
    parser.add_argument('--kind')
    parser.add_argument('--complexity', choices=LEVELS)
    parser.add_argument('--context', help='Local JSON applicability context; values remain private.')
    parser.add_argument('--audience', help='Explicit target audience; value remains private.')
    parser.add_argument('--scope', choices=('user', 'organisation', 'engagement'))
    for scope in ('user', 'organisation', 'engagement'):
        parser.add_argument('--' + scope + '-root')
    args = parser.parse_args(argv)
    try:
        library = ExpertReferences(args.root)
        scopes = {scope + '_root': getattr(args, scope + '_root') for scope in ('user', 'organisation', 'engagement')}
        if args.command == 'list':
            result = {'families': list(library.families), 'complexity_levels': list(LEVELS), 'reference_count': len(library.entries)}
        elif args.command == 'validate':
            if args.all:
                if args.source:
                    raise ReferenceError('SOURCE_AND_ALL_CONFLICT')
                result = library.validate_all()
            elif args.source:
                result = library.validate(args.source, args.kind, args.complexity)
            else:
                raise ReferenceError('VALIDATE_SOURCE_OR_ALL_REQUIRED')
        elif args.command in ('resolve', 'inspect'):
            context = load_json(args.context) if args.context else None
            _, result = library.resolve(args.kind, args.complexity, context=context, audience=args.audience, **scopes)
        else:
            if not args.scope:
                raise ReferenceError('WRITE_SCOPE_REQUIRED')
            scope_root = scopes[args.scope + '_root']
            if scope_root is None and args.scope == 'user':
                scope_root = Path(os.environ.get('XDG_CONFIG_HOME', str(Path.home() / '.config'))) / 'jai/expert_references'
            if scope_root is None and args.scope == 'organisation':
                scope_root = os.environ.get('JAI_EXPERT_REFERENCES_DIR')
            if scope_root is None:
                raise ReferenceError('WRITE_SCOPE_ROOT_REQUIRED')
            if args.command == 'install':
                if not args.source:
                    raise ReferenceError('INSTALL_SOURCE_REQUIRED')
                result = library.install(args.source, args.kind, args.complexity, scope_root)
            else:
                result = library.reset(args.kind, args.complexity, scope_root)
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0
    except (ReferenceError, OSError, ValueError) as exc:
        code = str(exc) if isinstance(exc, ReferenceError) else 'REFERENCE_OPERATION_FAILED'
        print(json.dumps({'status': 'FAIL', 'diagnostic': code}, sort_keys=True))
        return 1


if __name__ == '__main__':
    sys.exit(main())
