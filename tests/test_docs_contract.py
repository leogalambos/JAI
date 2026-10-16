# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Exercise documentation scenario contracts against real temporary files."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import tempfile
import unittest


_SOURCE = Path(__file__).resolve().parents[1] / '.ai/runtime/tools/docs_contract.py'
_SPEC = importlib.util.spec_from_file_location('docs_contract', _SOURCE)
assert _SPEC is not None and _SPEC.loader is not None
docs_contract = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(docs_contract)


class DocumentationScenarioContractTests(unittest.TestCase):
    def _scenario_problems(self, pages: dict[str, str]) -> list[str]:
        # The fixture isolates scenario classification; global manual requirements
        # remain enabled and their unrelated findings are not part of this test.
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            navigation = ['nav:']
            for number, (relative, content) in enumerate(pages.items()):
                target = root / 'docs' / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(content, encoding='utf-8')
                navigation.append(f'  - Page {number}: {relative}')
            (root / 'mkdocs.yml').write_text('\n'.join(navigation), encoding='utf-8')
            problems = docs_contract.check(root)
        return [problem for problem in problems if 'scenario lacks operator entry' in problem]

    def test_check_rejects_missing_checkout_structure(self):
        with tempfile.TemporaryDirectory() as directory:
            self.assertEqual(
                ['canonical docs/ directory or mkdocs.yml missing'],
                docs_contract.check(Path(directory)),
            )

    def test_check_accepts_executable_scenario_with_operator_boundary(self):
        self.assertEqual([], self._scenario_problems({
            'examples/proposal.md': '# Proposal\n\n## Run this scenario in the provider CLI\n',
        }))

    def test_check_accepts_directory_indexes_without_scenario_heading(self):
        self.assertEqual([], self._scenario_problems({
            'examples/index.md': '# Example reading map\n',
            'examples/how-to-use-JAI/index.md': '# Learning path\n',
        }))

    def test_check_still_rejects_non_index_examples_without_boundary(self):
        self.assertEqual([
            'docs/examples/index-overview.md: scenario lacks operator entry and implementation boundary',
            'docs/examples/nested/scenario.md: scenario lacks operator entry and implementation boundary',
        ], self._scenario_problems({
            'examples/index-overview.md': '# A scenario with an index-like name\n',
            'examples/nested/scenario.md': '# An executable scenario\n',
        }))


if __name__ == '__main__':
    unittest.main()
