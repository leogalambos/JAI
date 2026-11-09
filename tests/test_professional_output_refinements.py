# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Keep professional conclusions reconstructible from their selected contracts."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.ai/runtime/tools'))
from content_spec import ContentSpec
from content_spec import canonical_hash
sys.path.insert(0, str(ROOT / 'tools'))
from professional_output_refinements import delivery_form_for


def test_family_form_is_explicit_independent_and_rejects_unknown_family():
    import pytest
    form = delivery_form_for('automated-tests')
    assert form['primary_artifact'] == 'executable-test-suite'
    form['evidence'].append('Unrelated mutation')
    assert 'Unrelated mutation' not in delivery_form_for('automated-tests')['evidence']
    assert delivery_form_for('document', 'enterprise-architect:4')['primary_artifact'] == 'architecture-decision-record'
    with pytest.raises(KeyError):
        delivery_form_for('unregistered-family')


def test_accessibility_conclusion_requires_criterion_results_and_sampling():
    compiled = ContentSpec(ROOT).resolve('accessibility-tester:1')
    fields = {field for unit in compiled['blueprint']['semantic_units']
              for field in unit['semantic_fields']}
    assert {'accessibility_target', 'accessibility_sample',
            'accessibility_results', 'accessibility_conclusion'} <= fields
    assert compiled['semantic_family'] == 'assurance-report'


def test_principles_require_rationale_and_exception_rules_without_forced_ea_model():
    compiled = ContentSpec(ROOT).resolve('enterprise-architect:2')
    fields = {field for unit in compiled['blueprint']['semantic_units']
              for field in unit['semantic_fields']}
    assert {'principle_records', 'principle_conflicts', 'principle_verification'} <= fields
    assert compiled['semantic_family'] == 'register'


def test_delivery_form_distinguishes_native_output_from_legacy_storage_type():
    catalogue = ContentSpec(ROOT)
    for cid, native in [('software-engineer:1', 'versioned-source-change'),
                        ('software-engineer:2', 'executable-test-suite'),
                        ('enterprise-architect:4', 'architecture-decision-record')]:
        compiled = catalogue.resolve(cid)
        assert compiled['delivery_form']['primary_artifact'] == native
        assert compiled['delivery_form']['legacy_type_is_compatibility_only'] is True
        assert compiled['delivery_form']['evidence']


def test_delivery_instruction_is_bound_to_review_digest():
    catalogue = ContentSpec(ROOT)
    ref = catalogue.bindings['software-engineer:1']['content_spec_ref']
    original = catalogue.compile(ref)
    catalogue.specs[ref]['delivery_form']['representation'] = 'Different primary work product.'
    changed = catalogue.compile(ref)
    assert original['compiled_spec_hash'] != changed['compiled_spec_hash']
    assert changed['compiled_spec_hash'] == canonical_hash(
        {key: value for key, value in changed.items() if key != 'compiled_spec_hash'})


def test_public_contract_explains_native_output_instead_of_a_decision_paper():
    import importlib.util
    source = importlib.util.spec_from_file_location(
        'professional_docs', ROOT / 'tools/generate_output_contract_docs.py')
    module = importlib.util.module_from_spec(source)
    source.loader.exec_module(module)
    projection = module.Projection(ROOT)
    ref = projection.catalogue.bindings['software-engineer:1']['content_spec_ref']
    page = projection.spec_body(ref)
    assert 'versioned-source-change' in page
    assert 'exact source revision' in page
    assert 'retained for compatibility' in page
    assert '**Practical method:** Trace required behaviour' in page
    assert '**Selection:** Relevant candidates only' in page
    assert '**Applicability assessment:** `global.framework_applicability`' in page
