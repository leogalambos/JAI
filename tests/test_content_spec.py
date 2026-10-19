# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""DCS foundation contract and adversarial filesystem integration tests."""
import importlib.util
import json
from pathlib import Path
import tempfile
import shutil
import subprocess
import sys
import unittest

MODULE = Path(__file__).resolve().parents[1] / '.ai/runtime/tools/content_spec.py'
SPEC = importlib.util.spec_from_file_location('content_spec_tested', MODULE)
cs = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(cs)


class ContentSpecTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.base = self.root / '.ai/runtime/content'
        self.base.mkdir(parents=True)
        self.spec = {'id': 'kind/test', 'version': '1.0.0', 'status': 'proposed', 'completeness': 'skeleton',
                     'inherits': [], 'applies_to': {}, 'purpose': 'Support a decision.',
                     'required_information': [{'id': 'decision', 'semantic_fields': ['decision.question'], 'datatype': 'string'}],
                     'conditional_information': [], 'optional_information': [], 'forbidden_information': [],
                     'size_budget': {'metric': 'pages', 'target': [1, 3], 'soft_max': 4}}
        self.registry = {'schema_version': '1.0.0', 'specifications': [{'id': 'kind/test', 'version': '1.0.0', 'path': 'test.yaml'}],
                         'document_kinds': [{'id': 'test', 'artifact_types': ['document'], 'spec_ref': 'kind/test'}],
                         'bindings': [{'artifact_id': 'role:1', 'artifact_type': 'document', 'document_kind': 'test', 'content_spec_ref': 'kind/test'}],
                         'priority_document_kinds': ['test'], 'context_fields': {'private': {'type': 'boolean'}}}
        self.write()

    def write(self):
        (self.base / 'registry.json').write_text(json.dumps(self.registry))
        (self.base / 'test.yaml').write_text(json.dumps(self.spec))

    def engine(self):
        self.write()
        return cs.ContentSpec(self.root)

    def test_explicit_binding_resolves_and_never_infers_names(self):
        engine = self.engine()
        result = engine.resolve('role:1')
        self.assertEqual(result['document_kind'], 'test')
        self.assertFalse(result['production_ready'])
        self.assertEqual(result['approval_status'], 'pending-human-L0')
        with self.assertRaisesRegex(cs.SpecError, 'UNBOUND_ARTIFACT'):
            engine.resolve('decision-paper')

    def test_canonical_hash_ignores_mapping_key_order(self):
        self.assertEqual(cs.canonical_hash({'a': 1, 'b': 2}), cs.canonical_hash({'b': 2, 'a': 1}))
        self.assertNotEqual(cs.canonical_hash({'a': 1}), cs.canonical_hash({'a': 2}))

    def test_context_types_unknown_fields_and_missing_applicability(self):
        self.spec['conditional_information'] = [{'id': 'privacy', 'when': {'field': 'private', 'op': 'eq', 'value': True}}]
        engine = self.engine()
        unit = next(u for u in engine.compile('kind/test')['blueprint']['semantic_units'] if u['id'] == 'privacy')
        self.assertIsNone(unit['applicability'])
        self.assertTrue(next(u for u in engine.compile('kind/test', {'private': True})['blueprint']['semantic_units'] if u['id'] == 'privacy')['applicability'])
        for context in ({'unexpected': True}, {'private': 'true'}):
            with self.assertRaises(cs.SpecError):
                engine.compile('kind/test', context)

    def test_duplicate_json_keys_are_rejected(self):
        path = self.base / 'duplicate.json'
        path.write_text('{"id":1,"id":2}')
        with self.assertRaisesRegex(cs.SpecError, 'DUPLICATE_KEY'):
            cs.load_json(path)

    def test_paths_cannot_traverse_or_escape_through_symlinks(self):
        self.registry['specifications'][0]['path'] = '../outside.json'
        with self.assertRaisesRegex(cs.SpecError, 'UNSAFE_PATH'):
            self.engine()
        outside = self.root / 'outside.json'
        outside.write_text(json.dumps(self.spec))
        (self.base / 'link.yaml').symlink_to(outside)
        self.registry['specifications'][0]['path'] = 'link.yaml'
        with self.assertRaisesRegex(cs.SpecError, 'UNSAFE_PATH'):
            self.engine()

    def test_cycles_unknown_refs_and_version_mismatch_fail_closed(self):
        for parent, expected in [('kind/test', 'INHERITANCE_CYCLE'), ('missing', 'UNREGISTERED_REFERENCE'), ('kind/test@9', 'VERSION_MISMATCH')]:
            self.spec['inherits'] = [parent]
            with self.assertRaisesRegex(cs.SpecError, expected):
                self.engine().compile('kind/test')

    def test_overlay_cannot_weaken_must_or_change_type_or_evidence(self):
        parent = dict(self.spec)
        parent['id'] = 'type/base'
        (self.base / 'base.yaml').write_text(json.dumps(parent))
        self.registry['specifications'].append({'id': 'type/base', 'version': '1.0.0', 'path': 'base.yaml'})
        self.spec['inherits'] = ['type/base']
        self.spec['required_information'] = []
        self.spec['optional_information'] = [{'id': 'decision', 'semantic_fields': ['decision.question'], 'datatype': 'string'}]
        with self.assertRaisesRegex(cs.SpecError, 'obligation weakening'):
            self.engine().compile('kind/test')
        self.spec['optional_information'] = []
        self.spec['required_information'] = [{'id': 'decision', 'semantic_fields': ['decision.question'], 'datatype': 'number'}]
        with self.assertRaisesRegex(cs.SpecError, 'incompatible datatype'):
            self.engine().compile('kind/test')

    def test_lint_coverage_and_cli_expose_draft_status(self):
        engine = self.engine()
        self.assertEqual(engine.lint_registry(), [])
        self.assertEqual(cs.lint_registry(self.root), [])
        self.assertEqual(engine.coverage()['priority_complete'], 0)
        self.assertEqual(len(engine.list_specs()), 1)
        self.assertEqual(cs.main(['list', '--root', str(self.root)]), 0)

    def test_malformed_conditions_nonobject_context_and_negative_limits_fail(self):
        engine = self.engine()
        for context in ([], False, 'context'):
            with self.assertRaisesRegex(cs.SpecError, 'INVALID_CONTEXT'):
                engine.compile('kind/test', context)
        for condition in ({'field': 'private', 'op': 'in', 'value': True}, {'field': 'private', 'op': 'eq'}):
            self.spec['conditional_information'] = [{'id': 'conditional', 'when': condition}]
            with self.assertRaisesRegex(cs.SpecError, 'INVALID_APPLICABILITY'):
                self.engine()
        self.spec['conditional_information'] = []
        self.spec['size_budget']['hard_max'] = -1
        with self.assertRaisesRegex(cs.SpecError, 'INVALID_BUDGET'):
            self.engine()

    def test_predicate_operands_match_registered_context_types(self):
        for condition in ({'field': 'private', 'op': 'eq', 'value': 'false'},
                          {'field': 'private', 'op': 'eq', 'value': 1},
                          {'field': 'private', 'op': 'in', 'value': [True, 1]},
                          {'field': 'private', 'op': 'present', 'value': True}):
            self.spec['conditional_information'] = [{'id': 'privacy', 'when': condition}]
            with self.assertRaisesRegex(cs.SpecError, 'INVALID_APPLICABILITY'):
                self.engine()

    def test_compilation_preserves_security_and_editorial_rule_categories(self):
        self.spec['forbidden_information'] = [{'id': 'secret', 'semantic_fields': ['secret'], 'category': 'security-policy'}]
        self.spec['low_value_information'] = [{'id': 'verbosity', 'semantic_fields': ['verbosity'], 'category': 'editorial'}]
        units = {unit['id']: unit for unit in self.engine().compile('kind/test')['blueprint']['semantic_units']}
        self.assertEqual(units['secret']['rule_category'], 'security-policy')
        self.assertEqual(units['verbosity']['rule_category'], 'editorial')
        self.assertEqual(units['secret']['category'], 'forbidden_information')

    def test_obligation_cannot_contradict_its_category(self):
        self.spec['required_information'][0]['obligation'] = 'MAY'
        with self.assertRaisesRegex(cs.SpecError, 'INCONSISTENT_OBLIGATION'):
            self.engine()

    def test_same_semantic_field_cannot_be_required_and_forbidden(self):
        self.spec['forbidden_information'] = [{'id': 'forbid-decision', 'semantic_fields': ['decision.question'], 'datatype': 'string'}]
        with self.assertRaisesRegex(cs.SpecError, 'required and forbidden'):
            self.engine().compile('kind/test')

    def test_optional_duplicate_cannot_hide_required_forbidden_conflict(self):
        self.spec['optional_information'] = [{'id': 'optional-decision', 'semantic_fields': ['decision.question'], 'datatype': 'string'}]
        self.spec['forbidden_information'] = [{'id': 'forbid-decision', 'semantic_fields': ['decision.question'], 'datatype': 'string'}]
        with self.assertRaisesRegex(cs.SpecError, 'required and forbidden'):
            self.engine().compile('kind/test')

    def test_conditional_requirement_cannot_override_active_prohibition(self):
        self.spec['required_information'] = []
        self.spec['conditional_information'] = [{'id': 'need-secret', 'semantic_fields': ['secret'], 'datatype': 'string',
                                                  'when': {'field': 'private', 'op': 'eq', 'value': True}}]
        self.spec['forbidden_information'] = [{'id': 'forbid-secret', 'semantic_fields': ['secret'], 'datatype': 'string'}]
        engine = self.engine()
        for context in ({'private': True}, {}):
            with self.assertRaisesRegex(cs.SpecError, 'required and forbidden'):
                engine.compile('kind/test', context)
        self.assertIn('blueprint', engine.compile('kind/test', {'private': False}))

    def test_arbitrary_registered_kind_is_not_an_overlay(self):
        with self.assertRaisesRegex(cs.SpecError, 'INVALID_OVERLAY_CATEGORY'):
            self.engine().compile('kind/test', overlays=['kind/test'])

    def test_binding_resolution_hash_changes_with_artifact_selection(self):
        second = dict(self.registry['bindings'][0], artifact_id='role:2')
        self.registry['bindings'].append(second)
        engine = self.engine()
        first, second = engine.resolve('role:1'), engine.resolve('role:2')
        self.assertEqual(first['compiled_spec_hash'], second['compiled_spec_hash'])
        self.assertNotEqual(first['resolution_hash'], second['resolution_hash'])

    def test_selected_kind_scope_must_match_explicit_binding(self):
        self.spec['applies_to'] = {'document_kind': 'wrong-kind'}
        with self.assertRaisesRegex(cs.SpecError, 'KIND_SCOPE_MISMATCH'):
            self.engine().resolve('role:1')

    def test_resolve_rejects_tampered_source_provenance_before_compilation(self):
        contract = {'id': 'role:1', 'source_fingerprint': 'original', 'jai': {'semantics': {'artifact_type': 'document'}}}
        path = self.base.parent / 'artifacts/contracts/role-deliverables.v3.json'
        path.parent.mkdir(parents=True)
        path.write_text(json.dumps({'contracts': [contract]}))
        self.registry['bindings'][0].update(source_fingerprint='tampered', source_hash=cs.canonical_hash(contract))
        with self.assertRaisesRegex(cs.SpecError, 'BINDING_PROVENANCE_MISMATCH'):
            self.engine().resolve('role:1')

    def test_relocated_installed_cli_defaults_to_its_runtime(self):
        installed = self.root / 'home/.ai/it-role-house'
        (installed / 'tools').mkdir(parents=True)
        shutil.copytree(self.base, installed / 'content')
        shutil.copytree(MODULE.parent.parent / 'content/schema', installed / 'content/schema')
        shutil.copy2(MODULE, installed / 'tools/content_spec.py')
        result = subprocess.run([sys.executable, str(installed / 'tools/content_spec.py'), 'list'],
                                cwd=self.root, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout)[0]['id'], 'kind/test')

    def test_runtime_root_and_repository_root_load_same_registry(self):
        self.write()
        self.assertEqual(cs.ContentSpec(self.root).list_specs(), cs.ContentSpec(self.base.parent).list_specs())

    def test_complete_profiles_cannot_omit_schema_content(self):
        self.spec['completeness'] = 'complete'
        with self.assertRaisesRegex(cs.SpecError, 'SCHEMA_INVALID|MISSING_COMPLETE_SPEC_FIELD'):
            self.engine()

    def test_distinct_budget_dimensions_remain_independently_visible(self):
        parent = dict(self.spec, id='type/base', size_budget={'metric': 'semantic_units', 'soft_max': 20})
        parent['required_information'] = []
        (self.base / 'base.yaml').write_text(json.dumps(parent))
        self.registry['specifications'].append({'id': 'type/base', 'version': '1.0.0', 'path': 'base.yaml'})
        self.spec['inherits'] = ['type/base']
        result = self.engine().compile('kind/test')
        self.assertEqual(result['blueprint']['budgets']['semantic_units']['soft_max'], 20)
        self.assertEqual(result['blueprint']['budgets']['pages']['soft_max'], 4)

    def test_unsupported_modes_and_budget_ranges_fail(self):
        self.spec['mode'] = 'blocking'
        with self.assertRaisesRegex(cs.SpecError, 'HUMAN_L0'):
            self.engine()
        del self.spec['mode']
        self.spec['size_budget']['target'] = [3, 1]
        with self.assertRaisesRegex(cs.SpecError, 'INVALID_BUDGET'):
            self.engine()


if __name__ == '__main__':
    unittest.main()
