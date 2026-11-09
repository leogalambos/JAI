# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Every selected professional family has usable illustrative references."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.ai/runtime/tools'))
from content_spec import ContentSpec
from expert_references import ExpertReferences


def test_every_role_output_selects_a_reference_for_its_effective_family():
    catalogue = ContentSpec(ROOT)
    library = ExpertReferences(ROOT)
    gaps = []
    for cid, binding in catalogue.bindings.items():
        try:
            family = library.canonical_family(binding['semantic_family'], contract_id=cid)
            assert all(any(row['document_kind'] == family and row['complexity'] == level
                           for row in library.entries)
                       for level in ('simple', 'medium', 'complex'))
        except ValueError:
            gaps.append(cid)
    assert gaps == []


def test_new_reference_examples_explain_a_concrete_counterexample():
    library = ExpertReferences(ROOT)
    for family in ('software-change', 'dataset', 'diagram', 'dashboard', 'register'):
        path = library.base / family / 'medium.md'
        text = path.read_text()
        assert '## Plausible but incorrect conclusion' in text
        assert '## Reasoned disposition and downstream action' in text
        assert 'SYN-INPUT-01' in text and 'not executed' in text.lower()
        assert library.validate(path, family, 'medium', bundled=True)['structural_coverage'] == 'PASS'
