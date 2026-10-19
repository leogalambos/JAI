# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Integration coverage for optional DCS packaging and provider parity."""
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / '.ai/runtime'
SPEC = importlib.util.spec_from_file_location('content_artifacts_integration', RUNTIME / 'tools/artifacts.py')
ARTIFACTS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ARTIFACTS)


class ContentPackagingIntegrationTests(unittest.TestCase):
    def test_old_unprofiled_installation_remains_readable(self):
        with tempfile.TemporaryDirectory() as directory:
            self.assertEqual(ARTIFACTS.content_profile_problems(Path(directory)), [])

    def test_packaged_profile_fails_closed_without_resolver(self):
        with tempfile.TemporaryDirectory() as directory:
            runtime = Path(directory)
            profile = runtime / 'jai/profiles/content-profile.json'
            profile.parent.mkdir(parents=True)
            profile.write_text((RUNTIME / 'jai/profiles/content-profile.json').read_text())
            problems = ARTIFACTS.content_profile_problems(runtime)
            self.assertTrue(problems)
            self.assertIn('DCS:', problems[0])

    def test_malformed_profile_is_rejected_before_resolution(self):
        with tempfile.TemporaryDirectory() as directory:
            runtime = Path(directory)
            profile = runtime / 'jai/profiles/content-profile.json'
            profile.parent.mkdir(parents=True)
            profile.write_text('{}')
            self.assertIn('canonical registry', ARTIFACTS.content_profile_problems(runtime)[0])

    def test_source_runtime_and_installed_runtime_lint_equally(self):
        with tempfile.TemporaryDirectory() as directory:
            installed = Path(directory) / 'it-role-library'
            shutil.copytree(RUNTIME, installed, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            self.assertEqual(ARTIFACTS.content_profile_problems(RUNTIME), [])
            self.assertEqual(ARTIFACTS.content_profile_problems(installed), [])
            (installed / 'content/registry.json').unlink()
            self.assertTrue(ARTIFACTS.content_profile_problems(installed))

    def test_provider_bindings_use_one_profile_without_permission_changes(self):
        names = ('artifact-author', 'role-author', 'enterprise-publication-editor',
                 'evidence-rationale-reviewer', 'visual-quality-reviewer',
                 'architecture-reviewer', 'sabsa-reviewer')
        for name in names:
            with self.subTest(agent=name):
                adapters = [json.loads((RUNTIME / 'providers' / provider / (name + '.json')).read_text())
                            for provider in ('codex', 'claude')]
                self.assertEqual([item['content_profile_ref'] for item in adapters],
                                 ['jai/profiles/content-profile.json'] * 2)
                self.assertEqual(adapters[0]['allowed_tools'], adapters[1]['tools'])
                self.assertEqual(adapters[0]['denied_tools'], adapters[1]['deny'])
                self.assertEqual(adapters[0]['approval_required_for'], adapters[1]['approval_required_for'])

    def test_profile_preserves_v3_and_does_not_claim_content_approval(self):
        profile = json.loads((RUNTIME / 'jai/profiles/content-profile.json').read_text())
        self.assertEqual(profile['compatibility']['write'], 'ArtifactContract-v3')
        self.assertTrue(profile['compatibility']['historical_contracts_unchanged'])
        self.assertEqual(profile['status'], 'proposed')
        self.assertEqual(profile['calibration_status'], 'synthetic-only')
        self.assertEqual(profile['enforcement'], 'advisory')
        schema = json.loads((RUNTIME / 'schema/contracts/artifact-v3.schema.json').read_text())
        self.assertNotIn('content_spec_ref', schema.get('required', []))


if __name__ == '__main__':
    unittest.main()
