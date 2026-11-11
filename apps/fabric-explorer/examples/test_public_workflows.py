"""Public-source extraction and real canonical-writer coverage; no example authority decisions."""
import json
from pathlib import Path
import tempfile
import unittest
from public_workflows import collect_workflows, generate

class PublicWorkflowsTest(unittest.TestCase):
    """Keep exact public quotations, isolated destinations and source-only history."""
    def test_public_stages_and_real_canonical_capture(self):
        """Import real maintained table rows and submit a source-only canonical message."""
        rows = collect_workflows()
        self.assertEqual([len(row['stages']) for row in rows], [13, 8])
        self.assertEqual(rows[0]['stages'][6]['role'], 'Software Engineer')
        self.assertEqual(rows[0]['stages'][6]['activity'], 'implements with tests and telemetry')
        with tempfile.TemporaryDirectory() as directory:
            manifest = generate(Path(directory))
            self.assertEqual(manifest['source_records'], 42)
            roles = {item['role']: item for item in manifest['roles']}
            self.assertEqual(len(roles['Software Engineer']['occurrences']), 2)
            self.assertEqual(len(roles['Change Manager']['occurrences']), 2)
            transactions = [json.loads(line) for line in (Path(directory) / manifest['journal']).read_text().splitlines()]
            self.assertEqual(len(transactions), 1)
            self.assertNotIn('assessment', (Path(directory) / 'capture-request.json').read_text())
            inputs = json.loads((Path(directory) / 'capture-request.json').read_text())['payload']['l0_inputs']
            self.assertEqual(len(inputs), 42)
            stages = [item for item in inputs if item['logical_id'].startswith(('Delivery ', 'Remediation '))]
            self.assertEqual(len(stages), 21)
            for stage in stages:
                roles = [ref for ref in stage['record']['inherited'] if ref['logical_id'].startswith('Role · ')]
                self.assertEqual(len(roles), 1)
                self.assertEqual(roles[0]['logical_id'], 'Role · ' + stage['logical_id'].split(' · ', 1)[1])
    def test_rejects_nonempty_or_relative_output_without_overwrite(self):
        """Protect an existing directory and require explicit absolute output."""
        with self.assertRaises(ValueError): generate(Path('relative-output'))
        with tempfile.TemporaryDirectory() as directory:
            sentinel = Path(directory) / 'keep'; sentinel.write_text('unchanged')
            with self.assertRaises(ValueError): generate(Path(directory))
            self.assertEqual(sentinel.read_text(), 'unchanged')
    def test_rejects_missing_stage_table(self):
        """Missing public table input cannot silently become an empty graph."""
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory) / 'docs/workflow-library'; base.mkdir(parents=True)
            (base / 'idea-to-production.md').write_text('# Missing stage table\n')
            with self.assertRaises(ValueError): collect_workflows(Path(directory))

if __name__ == '__main__': unittest.main()
