# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Operational source applicability remains a reviewed, proposed DCS obligation."""
import importlib.util
import json
from pathlib import Path
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import generate_content_catalog as catalog
import generate_content_corpus as corpus


@pytest.fixture(scope='module')
def generated_catalog():
    return catalog.build()


def test_global_framework_obligation_requires_method_and_evidence_not_a_bibliography(generated_catalog):
    policy = generated_catalog[catalog.CONTENT / 'rules/global-invariants.yaml']
    units = {item['id']: item for item in policy['required_information']}
    unit = units['global.framework_applicability']
    assert unit['datatype'] == 'array'
    assert unit['acceptance_predicate'] == {'op': 'review'}
    criteria = '\n'.join(unit['acceptance_criteria'])
    for concept in ('edition', 'authoritative', 'normative', 'informative',
                    'jurisdiction', 'tailoring', 'precedence', 'method',
                    'evidence', 'reviewer', 'change trigger', 'not applicable',
                    'pending', 'clause'):
        assert concept in criteria
    assert 'bibliography' in criteria
    assert policy['status'] == 'proposed'
    assert policy['approval']['authority_ref'] is None


def test_all_six_shared_domains_have_scoped_external_sources_and_methods(generated_catalog):
    domain_refs = {}
    for name in catalog.DOMAIN_REQUIREMENTS:
        policy = generated_catalog[catalog.CONTENT / f'domain/{name}.yaml']
        references = policy['sources']['professional_references']
        domain_refs[name] = {item['id'] for item in references}
        assert references and all(item['url'].startswith('https://') for item in references)
        assert all(item['basis'] == 'informed-by' for item in references)
        assert all('No clause-level conformance' in item['limits'] for item in references)
        assert len(policy['required_information']) == 2
        assert all(len(item['acceptance_criteria']) >= 3 for item in policy['required_information'])
        assert policy['approval']['status'] == 'pending'
    assert 'architecture-description' in domain_refs['architecture']
    assert 'software-testing' in domain_refs['testing']
    assert 'data-quality' in domain_refs['data']
    assert 'control-assessment' in domain_refs['security']


def test_every_role_domain_gets_method_context_without_mandating_all_frameworks(generated_catalog):
    contexts = []
    for value in generated_catalog.values():
        contexts.extend(value.get('sources', {}).get('role_framework_context', []))
    assert len(contexts) == 1139
    assert {item['domain_index'] for item in contexts} == set(range(1, 18))
    for item in contexts:
        assert item['method_focus']
        assert item['applicability_rule'] == 'global.framework_applicability'
        assert item['frameworks']
        assert 'not proof' in item['basis']
        assert item['framework_selection'] == 'Relevant candidates only; this is not a mandatory framework list.'


def test_unknown_authored_domain_fails_instead_of_silently_falling_back():
    policy = catalog.spec('domain/unknown', 'domain', 'Unknown domain', 'complete')
    with pytest.raises(KeyError):
        catalog.enrich_professional_guidance({'policy': policy}, [], [])


def test_framework_unit_is_inherited_once_and_remains_pending_review(tmp_path, generated_catalog):
    module_spec = importlib.util.spec_from_file_location(
        'framework_content_spec', ROOT / '.ai/runtime/tools/content_spec.py')
    resolver_module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(resolver_module)
    base = tmp_path / '.ai/runtime/content'
    base.mkdir(parents=True)
    global_policy = generated_catalog[catalog.CONTENT / 'rules/global-invariants.yaml']
    child = catalog.spec('kind/subject', 'document_kind', 'Bounded subject', 'skeleton',
                         ['global/invariants'])
    child['applies_to'] = {'document_kind': 'subject'}
    (base / 'global.json').write_text(json.dumps(global_policy))
    (base / 'subject.json').write_text(json.dumps(child))
    registry = {'schema_version': '1.0.0', 'context_fields': {},
                'specifications': [
                    {'id': 'global/invariants', 'version': global_policy['version'], 'path': 'global.json'},
                    {'id': 'kind/subject', 'version': child['version'], 'path': 'subject.json'}],
                'document_kinds': [{'id': 'subject', 'spec_ref': 'kind/subject', 'artifact_types': ['document']}]}
    (base / 'registry.json').write_text(json.dumps(registry))
    compiled = resolver_module.ContentSpec(tmp_path).compile('kind/subject')
    units = [item for item in compiled['blueprint']['semantic_units']
             if item['id'] == 'global.framework_applicability']
    assert len(units) == 1
    assert units[0]['applicability'] is True
    assert units[0]['acceptance_predicate']['op'] == 'review'
    assert compiled['production_ready'] is False


def test_synthetic_framework_record_has_real_structure_but_no_claimed_qualification(generated_catalog):
    unit = next(item for item in generated_catalog[catalog.CONTENT / 'rules/global-invariants.yaml']['required_information']
                if item['id'] == 'global.framework_applicability')
    records = corpus.synthetic_value(unit, corpus.SCENARIOS['simple'], 'framework_applicability')
    assert len(records) == 1
    record = records[0]
    assert record['knowledge_status'] == 'synthetic-assumption'
    assert record['basis'] == 'jai-interpretation'
    assert record['applicability'] == 'applicable'
    assert record['source']['edition']
    assert record['source']['authoritative_location']
    assert record['method_mapping'][0]['output_unit_ref']
    assert record['method_mapping'][0]['reviewer_test']
    assert record['review']['status'] == 'pending-independent-review'
    assert record['human_approval_ref'] is None
