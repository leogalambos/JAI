# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Source fidelity, typed narrative publication and example integration contracts."""
import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from argparse import Namespace
from unittest.mock import patch

TOOLS = Path(__file__).resolve().parents[1] / '.ai/runtime/tools'
sys.path.insert(0, str(TOOLS))
import sabsa
import sabsa_narrative as narrative
import sabsa_publication_demo as demo


class SabsaNarrativeTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.output = Path(self.temporary.name) / 'example'
        # Python redirects do not capture output inherited by real subprocesses.
        run = demo.subprocess.run
        captured = []
        def capture_command(command, **kwargs):
            result = run(command, **{**kwargs, 'check': False, 'capture_output': True, 'text': True})
            self.assertEqual(result.returncode, 0, f'{command!r}\n{result.stdout}\n{result.stderr}')
            self.assertEqual(result.stderr, '', f'{command!r}\n{result.stdout}\n{result.stderr}')
            captured.append(result.stdout)
            return result
        with patch.object(demo.subprocess, 'run', side_effect=capture_command), contextlib.redirect_stdout(io.StringIO()):
            self.lib = demo.build_example(self.output)
        self.assertEqual(len(captured), len(sabsa.LAYER_KEYS) + 1)
        for layer, output in zip(sabsa.LAYER_KEYS, captured):
            self.assertIn(f'wrote {self.output / (layer + ".md")}', output)
        self.assertEqual(captured[-1].strip(), f'CSV catalogue export: {self.output / "csv"}')

    def test_build_example_profiles_preserve_body_fields_and_trace(self):
        model = sabsa.build_model(str(self.lib))
        document = narrative.publication_model(sabsa, str(self.lib), model, 'logical')
        records = [record for group in document['publication_groups'] for record in group['records']]
        service = next(record for record in records if record['id'] == 'SS-001')
        self.assertIn('A deny result does not reveal whether the document exists.', service['body'])
        fields = {field['name']: field['value'] for field in service['fields']}
        self.assertEqual('stated', fields['Basis'])
        self.assertEqual('00-sources/example-brief.md', fields['Source'])
        self.assertEqual('target', fields['Horizon'])
        self.assertIn('Canonical ref', fields)
        self.assertIn('—[objectives]→ CO-001', service['paths'][0]['text'])
        self.assertIn('Business outcome:', service['paths'][0]['text'])
        self.assertFalse(document['has_publication_gaps'])
        for layer in sabsa.LAYER_KEYS:
            text = (self.output / (layer + '.md')).read_text()
            self.assertIn('fictional', text.lower())
            self.assertNotRegex(text, r'<[^>]+>')
            self.assertIn('\n\n## Purpose, scope and applicability', text)
        contextual = narrative.publication_model(sabsa, str(self.lib), model, 'contextual')
        driver = contextual['publication_groups'][0]['records'][0]
        self.assertTrue(any('SC-001' in path['text'] for path in driver['paths']))

    def test_narrative_changes_invalidate_approved_snapshot(self):
        with contextlib.redirect_stdout(io.StringIO()):
            sabsa.cmd_approve(Namespace(lib=str(self.lib), by='Fictional test owner', note='Synthetic disposable approval test'))
        self.assertTrue(sabsa.approval_state(str(self.lib))['valid'])
        chapter = self.lib / 'narratives/logical/service-design.md'
        chapter.write_text(chapter.read_text() + '\nAuthored change to the service contract.\n')
        self.assertFalse(sabsa.approval_state(str(self.lib))['valid'])
        self.assertIn('narratives/logical/service-design.md', sabsa.collect_citations(str(self.lib))['00-sources/example-brief.md'])

    def test_source_placeholder_and_missing_narrative_are_explicit_draft(self):
        chapter = self.lib / 'narratives/logical/service-design.md'
        chapter.unlink()
        service = self.lib / '03-logical/services/SS-001.md'
        sabsa._frontmatter_set(service, 'owner', '<A named person or role.>')
        model = sabsa.build_model(str(self.lib)); model['approved'] = True; model['draft'] = False
        document = narrative.publication_model(sabsa, str(self.lib), model, 'logical')
        self.assertTrue(document['draft']); self.assertFalse(document['approved'])
        self.assertTrue(document['has_publication_gaps'])
        fields = [f for g in document['publication_groups'] for r in g['records'] for f in r['fields']]
        self.assertTrue(any('Authoring gap — original source placeholder:' in f['value'] for f in fields))

    def test_wrong_type_and_dangling_paths_never_claim_business_justification(self):
        service = self.lib / '03-logical/services/SS-001.md'
        sabsa._frontmatter_set(service, 'objectives', 'BD-001, CO-999')
        document = narrative.publication_model(sabsa, str(self.lib), sabsa.build_model(str(self.lib)), 'logical')
        record = next(r for g in document['publication_groups'] for r in g['records'] if r['id'] == 'SS-001')
        self.assertTrue(any('TYPE MISMATCH' in p['text'] for p in record['paths']))
        self.assertTrue(any('UNRESOLVED TARGET' in p['text'] for p in record['paths']))
        self.assertFalse(any('Business outcome:' in p['text'] for p in record['paths']))

    def test_provenance_language_validation_and_scaffold_preservation(self):
        chapter = self.lib / 'narratives/logical/service-design.md'
        before = chapter.read_bytes()
        self.assertEqual(0, narrative.scaffold_narratives(self.lib, 'logical'))
        self.assertEqual(before, chapter.read_bytes())
        sabsa._frontmatter_set(chapter, 'language', 'cs')
        sabsa._frontmatter_set(chapter, 'source', '00-sources/nonexistent.md')
        errors, warnings = narrative.narrative_issues(sabsa, self.lib)
        self.assertTrue(any('does not resolve' in error for error in errors))
        self.assertTrue(any('English edition' in warning for warning in warnings))
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(0, sabsa.cmd_narrative_init(Namespace(lib=str(self.lib), layer='operational')))

    def test_existing_destination_is_never_overwritten(self):
        existing = Path(self.temporary.name) / 'occupied'; existing.mkdir()
        target = existing / 'logical.md'; target.write_text('User content')
        with self.assertRaises(FileExistsError): demo.build_example(existing)
        self.assertEqual('User content', target.read_text())
        self.assertEqual([target], list(existing.iterdir()))


if __name__ == '__main__':
    unittest.main()
