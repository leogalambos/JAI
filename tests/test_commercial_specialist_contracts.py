# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Native commercial contract provenance, migration preservation and projection regressions.

Fixtures contain only the five new commercial role sources; no full role-tree scan is needed.
"""
from __future__ import annotations

import copy
import contextlib
import hashlib
import importlib.util
import json
import io
import shutil
import tempfile
import unittest
from types import SimpleNamespace
from unittest.mock import patch
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('specialist_artifacts', ROOT / '.ai/runtime/tools/artifacts.py')
artifacts = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(artifacts)
SLUGS = {
    'bid-proposal-manager', 'commercial-pricing-deal-finance-specialist',
    'estimation-cost-engineering-specialist', 'independent-commercial-assurance-reviewer',
    'supplier-commercial-deal-manager',
}


class CommercialSpecialistContractsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.runtime = self.root / '.ai/runtime'
        self.runtime.mkdir(parents=True)
        canonical = ROOT / '.ai/runtime'
        for rel in (
            'artifacts/schema/artifact-types.json', 'schema/contracts/artifact-v3.schema.json',
            'artifacts/profiles/acceptance-evidence.json',
            'artifacts/contracts/commercial-specialists.native-v3.json',
        ):
            destination = self.runtime / rel
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(canonical / rel, destination)
        roles = json.loads((canonical / 'roles.json').read_text())
        roles['roles'] = [r for r in roles['roles'] if r['slug'] in SLUGS]
        self.assertEqual(5, len(roles['roles']))
        self.write('roles.json', roles)
        for role in roles['roles']:
            relative = Path(role['path'])
            destination = self.root / '.ai' / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / '.ai' / relative, destination)
        source = json.loads((canonical / 'artifacts/contracts/role-deliverables.v3.json').read_text())
        source['contracts'] = [r for r in source['contracts'] if r['role_slug'] in SLUGS]
        source.update(role_count=5, deliverable_count=15)
        self.source = source
        self.save_source()
        self.write('artifacts/contracts/role-deliverables.v2.json', {'contracts': []})
        self.write('artifacts/contracts/golden-classification.json', {'cases': []})
        taxonomy = json.loads((canonical / 'artifacts/schema/artifact-types.json').read_text())
        # Full validation checks path presence, not implementation execution. Copy only
        # the declared schema/producer/renderer dependencies of the selected contracts.
        for record in source['contracts']:
            definition = taxonomy['artifact_types'][record['jai']['semantics']['artifact_type']]
            for field in ('schema_ref', 'producer', 'renderer'):
                relative = definition[field].split()[0]
                destination = self.runtime / relative
                destination.parent.mkdir(parents=True, exist_ok=True)
                if not destination.exists():
                    shutil.copyfile(canonical / relative, destination)

    def write(self, relative, value):
        path = self.runtime / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value, indent=2) + '\n')

    def save_source(self):
        self.write('artifacts/contracts/role-deliverables.v3.json', self.source)

    def problems(self):
        self.save_source()
        return artifacts.validate(self.root)[0]

    def test_native_contracts_validate_and_projection_matches_canonical(self):
        self.assertEqual([], self.problems())
        projected, problems = artifacts.generated_registry(self.root)
        self.assertEqual([], problems)
        canonical = json.loads((ROOT / '.ai/runtime/artifacts/role-deliverables.json').read_text())
        expected = [c for c in canonical['contracts'] if c['role_slug'] in SLUGS]
        self.assertEqual(expected, projected['contracts'])
        self.assertEqual((5, 15), (projected['role_count'], projected['deliverable_count']))

    def test_missing_origin_is_rejected_by_runtime_and_schema(self):
        row = self.source['contracts'][0]
        del row['native_creation']
        self.assertTrue(any('exactly one' in p for p in self.problems()))
        schema = json.loads((self.runtime / 'schema/contracts/artifact-v3.schema.json').read_text())
        self.assertTrue(list(artifacts.jsonschema.Draft202012Validator(schema).iter_errors(row)))

    def test_native_manifest_hash_and_contract_content_are_bound(self):
        self.source['contracts'][0]['jai']['intent']['purpose'] += ' altered'
        self.assertTrue(any('contract binding mismatch' in p for p in self.problems()))
        self.source['contracts'][0]['native_creation']['evidence_hash'] = '0' * 64
        self.assertTrue(any('evidence hash mismatch' in p for p in self.problems()))

    def test_section_six_drift_and_source_path_mismatch_are_rejected(self):
        self.source['contracts'][0]['source_fingerprint'] = '0' * 64
        self.source['contracts'][0]['native_creation']['source_path'] = 'skills/unrelated/references/other.md'
        problems = self.problems()
        self.assertTrue(any('Section 6 drift' in p for p in problems))
        self.assertTrue(any('role source mismatch' in p for p in problems))

    def test_duplicate_contract_and_stable_identity_mismatch_are_rejected(self):
        self.source['contracts'].append(copy.deepcopy(self.source['contracts'][0]))
        self.assertIn('duplicate or empty contract ids in authoritative source', self.problems())
        self.source['contracts'].pop()
        self.source['contracts'][0]['deliverable_number'] = 99
        self.assertTrue(any('identity differs' in p for p in self.problems()))

    def test_existing_legacy_id_cannot_be_laundered_as_native(self):
        row = self.source['contracts'][0]
        self.write('artifacts/contracts/role-deliverables.v2.json', {'contracts': [{'id': row['id'], 'historic': True}]})
        self.assertTrue(any('cannot be relabelled' in p for p in self.problems()))

    def test_valid_legacy_migration_remains_valid_and_tampering_is_rejected(self):
        legacy = {'id': 'example:1', 'version': '2.0.0'}
        row = {'id': 'example:1', 'role_slug': 'example', 'deliverable_number': 1,
               'compatibility': {'migration': 'forward-only', 'classification_source': 'explicit-ga-26.10.0'},
               'migration': {'source_id': 'example:1', 'source_hash': artifacts._record_hash(legacy)}}
        self.assertEqual([], artifacts._origin_problems(row, {'example:1': legacy}, None, self.runtime))
        row['migration']['source_hash'] = '0' * 64
        self.assertTrue(any('migration provenance/hash mismatch' in p for p in artifacts._origin_problems(row, {'example:1': legacy}, None, self.runtime)))
        self.assertTrue(any('legacy migration source missing' in p for p in artifacts._origin_problems(row, {}, None, self.runtime)))

    def test_dual_origin_and_malformed_native_reference_are_rejected(self):
        row = self.source['contracts'][0]
        row['migration'] = {'source_id': row['id']}
        self.assertTrue(any('exactly one' in p for p in self.problems()))
        del row['migration']
        row['native_creation']['evidence_ref'] = '../outside.json'
        self.assertTrue(any('invalid native provenance reference' in p for p in self.problems()))

    def test_duplicate_manifest_ids_are_rejected_even_with_matching_file_hash(self):
        path = self.runtime / 'artifacts/contracts/commercial-specialists.native-v3.json'
        manifest = json.loads(path.read_text())
        manifest['contracts'].append(manifest['contracts'][0])
        path.write_text(json.dumps(manifest))
        new_hash = hashlib.sha256(path.read_bytes()).hexdigest()
        for row in self.source['contracts']:
            row['native_creation']['evidence_hash'] = new_hash
        self.assertTrue(any('duplicate native provenance ids' in p for p in self.problems()))

    def test_schema_preserves_every_existing_legacy_contract(self):
        canonical = ROOT / '.ai/runtime'
        schema = json.loads((canonical / 'schema/contracts/artifact-v3.schema.json').read_text())
        validator = artifacts.jsonschema.Draft202012Validator(schema)
        rows = json.loads((canonical / 'artifacts/contracts/role-deliverables.v3.json').read_text())['contracts']
        legacy = [row for row in rows if 'migration' in row]
        self.assertEqual(1124, len(legacy))
        for row in legacy:
            with self.subTest(contract=row['id']):
                self.assertEqual([], list(validator.iter_errors(row)))

    def test_missing_or_malformed_manifest_fails_closed(self):
        path = self.runtime / 'artifacts/contracts/commercial-specialists.native-v3.json'
        path.unlink()
        self.assertTrue(any('evidence missing or invalid' in p for p in self.problems()))
        path.write_text('[]')
        self.assertTrue(any('must contain contract objects' in p for p in self.problems()))

    def test_registry_helpers_preserve_numbered_source_identity(self):
        roles_path, skills, _, runtime = artifacts.locate(self.root)
        self.assertEqual(self.runtime, runtime)
        self.assertEqual(self.runtime / 'roles.json', roles_path)
        self.assertEqual(self.runtime, artifacts.paths(self.root)['runtime'])
        self.assertEqual('One two', artifacts.clean(' **One**  `two` '))
        text = '## 3. Inputs\nitem\n## 6. Deliverables\nvalue\n'
        self.assertEqual(['item'], artifacts.sections(text)[3])
        state = artifacts.load_all(self.root)
        self.assertEqual(5, len(state[-1]))
        live = artifacts.live_deliverables(state[0], state[-1])
        self.assertEqual(15, len(live))
        role = state[-1][0]
        _, gates, deliverables = artifacts.parse_role(skills / Path(*Path(role['path']).parts[1:]))
        self.assertTrue(gates)
        self.assertTrue(deliverables)
        self.assertEqual(live[f"{role['slug']}:{deliverables[0]['number']}"]['fingerprint'], artifacts.fingerprint(deliverables[0]))
        changed = dict(deliverables[0], acceptance_criterion='Different obligation')
        self.assertNotEqual(artifacts.fingerprint(deliverables[0]), artifacts.fingerprint(changed))
        self.assertTrue(artifacts.runtime_path_exists(runtime, 'roles.json'))
        self.assertFalse(artifacts.runtime_path_exists(runtime, 'external:service'))
        flattened = artifacts.flatten_v3(self.source['contracts'][0])
        self.assertEqual(self.source['contracts'][0]['jai']['intent']['purpose'], flattened['purpose'])
        self.assertEqual({'version': '2.0.0'}, artifacts.flatten_v3({'version': '2.0.0'}))

    def test_command_facades_generate_inspect_check_and_reject_drift(self):
        args = SimpleNamespace(root=str(self.root), role=next(iter(SLUGS)))
        with contextlib.redirect_stdout(io.StringIO()) as output:
            self.assertEqual(0, artifacts.cmd_sync(args))
            self.assertEqual(0, artifacts.cmd_check(args))
            self.assertEqual(0, artifacts.cmd_golden(args))
            self.assertEqual(0, artifacts.cmd_show(args))
        self.assertIn('15 explicit contracts', output.getvalue())
        self.assertTrue((self.runtime / 'artifacts/role-deliverables.json').is_file())
        args.role = 'unknown-role'
        with self.assertRaises(SystemExit):
            artifacts.cmd_show(args)
        self.source['contracts'][0]['source_fingerprint'] = '0' * 64
        self.save_source()
        with contextlib.redirect_stdout(io.StringIO()) as output:
            self.assertEqual(1, artifacts.cmd_sync(args))
            self.assertEqual(1, artifacts.cmd_check(args))
        self.assertIn('Section 6 drift', output.getvalue())
        self.write('artifacts/contracts/golden-classification.json', {'cases': [{'id': self.source['contracts'][0]['id'], 'expected_artifact_type': 'wrong'}]})
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(1, artifacts.cmd_golden(args))

    def test_handoff_requires_explicit_external_contract_and_adapter(self):
        args = SimpleNamespace(root=str(self.root), contract_id='unknown:1')
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(1, artifacts.cmd_handoff(args))
            args.contract_id = self.source['contracts'][0]['id']
            self.assertEqual(1, artifacts.cmd_handoff(args))
            realisation = self.source['contracts'][0]['jai']['realisation']
            realisation['production_mode'] = 'external_handoff'
            self.save_source()
            self.assertEqual(1, artifacts.cmd_handoff(args))
            realisation['external_handoff_adapter'] = 'external:approved-tool-handoff'
            self.save_source()
            self.assertEqual(0, artifacts.cmd_handoff(args))

    def test_migration_classifier_and_proposal_remain_proposal_only(self):
        self.assertEqual('business-case', artifacts.propose_type('Business case', 'Document'))
        self.assertEqual('document', artifacts.propose_type('Unclassified', 'Text'))
        destination = self.root / 'proposal.json'
        args = SimpleNamespace(root=str(self.root), out=str(destination))
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(0, artifacts.cmd_propose(args))
        proposal = json.loads(destination.read_text())
        self.assertTrue(proposal['proposal_only'])
        self.assertEqual(15, len(proposal['contracts']))
        self.assertEqual({'migration-proposal-inferred'}, {row['classification_source'] for row in proposal['contracts']})
        self.assertEqual([], self.problems())

    def test_main_dispatches_read_only_command_and_propagates_failure(self):
        with patch('sys.argv', ['artifacts.py', 'check', '--root', str(self.root)]), contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaises(SystemExit) as raised:
                artifacts.main()
        self.assertEqual(0, raised.exception.code)
        self.source['contracts'][0]['source_fingerprint'] = '0' * 64
        self.save_source()
        with patch('sys.argv', ['artifacts.py', 'check', '--root', str(self.root)]), contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaises(SystemExit) as raised:
                artifacts.main()
        self.assertEqual(1, raised.exception.code)


if __name__ == '__main__':
    unittest.main()
