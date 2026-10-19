# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Foundation catalogue traceability and reproducible synthetic mutation checks.

These checks test data integrity; they cannot substitute for competent human
semantic assessment or the later production content lint enforcement release.
"""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
CONTENT=ROOT/'.ai/runtime/content'

def read(path):
    """Load the JSON-compatible subset used by the foundation YAML policies."""
    return json.loads(path.read_text())

class ContentCatalogueTests(unittest.TestCase):
    """Protect explicit classifications, lineage and substantive fixture coverage."""
    def test_exact_legacy_binding_coverage(self):
        """Every unchanged canonical contract has a unique fingerprinted binding."""
        contracts=read(ROOT/'.ai/runtime/artifacts/contracts/role-deliverables.v3.json')['contracts']
        bindings=read(CONTENT/'migrations/26.10.5-binding-map.json')['bindings']
        self.assertEqual(len(bindings),1139)
        self.assertEqual(len({b['artifact_id'] for b in bindings}),1139)
        byid={b['artifact_id']:b for b in bindings}
        for contract in contracts:
            b=byid[contract['id']]
            self.assertEqual(b['artifact_type'],contract['jai']['semantics']['artifact_type'])
            self.assertEqual(b['source_fingerprint'],contract['source_fingerprint'])
            digest=hashlib.sha256(json.dumps(contract,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
            self.assertEqual(b['source_hash'],digest)
            self.assertTrue(b['decision_supported_copy_detected'])
            if b['decision_supported']['status']=='mapped':
                self.assertNotEqual(b['decision_supported']['value'],contract['jai']['intent']['decision_supported'])
            else:self.assertEqual(b['decision_supported']['status'],'pending-correction')

    def test_coverage_and_unique_kind_contracts(self):
        """Only the approved ten families claim complete authored specifications."""
        registry=read(CONTENT/'registry.json')
        self.assertEqual([len(registry['mappings'][key]) for key in ['artifact_types','archetypes','sabsa_views']],[28,13,19])
        complete=[s for s in registry['specifications'] if s['completeness']=='complete']
        self.assertEqual(len(complete),10)
        fieldsets=[]
        for entry in complete:
            spec=read(CONTENT/entry['path'])
            self.assertEqual(spec['status'],'proposed')
            self.assertIsNone(spec['approval']['authority_ref'])
            self.assertEqual(spec['calibration_status'],'synthetic-only')
            self.assertGreaterEqual(len(spec['required_information']),5)
            for group in ['required_information','conditional_information','optional_information','forbidden_information','low_value_information']:
                self.assertTrue(spec[group])
                for unit in spec[group]:
                    self.assertTrue(unit['rationale']['reason'])
                    self.assertFalse(unit['provenance']['normative_claim'])
            fieldsets.append(tuple(u['semantic_fields'][0] for u in spec['required_information']))
            self.assertFalse(spec['size_budget']['minimum_is_quality_gate'])
        self.assertEqual(len(set(fieldsets)),10)

    def test_fixture_navigation_resolves_single_canonical_corpus(self):
        """Resolve all reference and mutation entries without duplicating documents."""
        counts={}
        seen=set()
        for category in ['valid','invalid','borderline']:
            index=read(CONTENT/f'fixtures/{category}/index.json')
            self.assertEqual(index['category'],category)
            counts[category]=len(index['entries'])
            for entry in index['entries']:
                case=read(ROOT/'.ai/runtime'/entry['case_ref'])
                key=(entry['case_ref'],entry['variant_id'])
                self.assertNotIn(key,seen);seen.add(key)
                if entry['variant_id'] is not None:
                    variant=next(v for v in case['variants'] if v['id']==entry['variant_id'])
                    self.assertEqual(entry['expected_category'],variant['expected_category'])
        self.assertEqual(counts,{'valid':30,'invalid':180,'borderline':90})

    def test_populated_reference_facts_and_all_mutations(self):
        """Check concrete cross-consistent case facts and execute all mutation recipes."""
        import sys
        sys.path.insert(0,str(ROOT/'tools'))
        from generate_content_corpus import observe_variant, apply_variant
        manifest=read(ROOT/'.ai/runtime/evals/content_quality/manifest.json')
        for ref in manifest['cases']:
            case=read(ROOT/'.ai/runtime'/ref);u=case['semantic_units'];family=case['document_kind']
            if family=='business-case':
                model=u['financial_model'];sensitivity=u['sensitivity']
                self.assertEqual(model['total_cost'],model['transition']+model['annual_operation']*model['horizon_years'])
                self.assertEqual(model['net_benefit'],model['gross_benefit']-model['total_cost'])
                fraction=sensitivity['benefit_downside']['reduction_fraction']
                self.assertEqual(fraction,{'simple':.25,'medium':.30,'complex':.35}[ref.split('-')[-1].split('.')[0]])
                self.assertEqual(sensitivity['benefit_downside']['net_benefit'],model['gross_benefit']*(1-fraction)-model['total_cost'])
                self.assertEqual(sensitivity['six_month_delay']['lost_benefit'],model['annual_avoided_manual_cost']*.5)
                self.assertEqual(u['investment_request']['requested_funding'],model['transition'])
            elif family=='risk-assessment':
                risk=u['risk_scenarios'][0]
                self.assertEqual(set(u['scoring_method']['likelihood_scale']),set('12345'))
                self.assertEqual(set(u['scoring_method']['impact_scale']),set('12345'))
                for kind in ['inherent','residual']:
                    self.assertEqual(risk[kind]['score'],risk[kind]['likelihood']*risk[kind]['impact'])
                self.assertEqual(u['risk_treatment'][0]['risk_ref'],risk['id'])
            elif family=='architecture-definition':
                ids={e['id'] for e in u['architecture_evolution']['entities']}
                for view in u['architecture_viewpoints']:self.assertTrue(set(view['element_refs'])<=ids)
                for interface in u['architecture_relations']:self.assertTrue({interface['source'],interface['target']}<=ids)
            elif family=='hld':
                ids={e['id'] for e in u['solution_components']}
                for interface in u['solution_interfaces']:
                    self.assertTrue({interface['source'],interface['target']}<=ids);self.assertIn('retry',interface['failure'])
            elif family=='runbook':
                self.assertEqual([s['step'] for s in u['procedure_steps']],[1,2,3])
                self.assertTrue(all(s['command'] and s['expected_output'] and s['stop_on'] for s in u['procedure_steps']))
                self.assertTrue(u['failure_recovery']['escalation_owner'])
            elif family=='test-report':
                self.assertEqual(u['test_conclusion']['executed'],len(u['execution_results']))
                self.assertEqual(u['test_conclusion']['passed'],sum(r['result']=='PASS' for r in u['execution_results']))
                for row in u['execution_results']:self.assertLess(row['started'],row['finished'])
                self.assertEqual(u['test_conclusion']['signoff']['status'],'pending-human-approval')
            elif family=='adr':
                self.assertIn(u['architecture_choice']['choice'],{r['id'] for r in u['architecture_options']})
            elif family=='decision-paper':
                self.assertIn(u['recommendation']['option_ref'],{r['id'] for r in u['options']})
                self.assertGreater(len(u['options']),1)
            elif family=='assurance-report':
                self.assertGreater(u['control_tests'][0]['sample_size'],0)
                self.assertTrue(u['assurance_findings'][0]['owner'])
                self.assertTrue(set(u['assurance_conclusion']['basis_refs'])<={row['id'] for row in u['assurance_conclusion']['execution_records']})
            elif family=='operational-handover':
                self.assertGreater(u['support_arrangements']['response_minutes'],0)
                self.assertEqual(u['acceptance_decision']['status'],'pending-human-approval')
            for variant in case['variants']:
                mutated=apply_variant(case,variant)
                self.assertNotEqual(mutated,case)
                observed=observe_variant(case,variant)
                self.assertEqual(observed['rule_ids'],sorted(variant['expected_rule_ids']))
                self.assertTrue(observed['semantic_review_required'])
                if variant['id']=='valid-conditional-na':
                    self.assertFalse(mutated['context']['processes_personal_data'])
                    self.assertEqual(mutated['semantic_units']['privacy_analysis']['evidence_refs'],['SYN-NA'])

    def test_corpus_mutations_are_observable_and_scoped(self):
        """Execute seeded core deficits rather than accepting asserted PASS labels."""
        registry=read(CONTENT/'registry.json')
        manifest=read(ROOT/'.ai/runtime/evals/content_quality/manifest.json')
        self.assertEqual(len(manifest['cases']),30)
        self.assertFalse(manifest['human_gold'])
        cases_by_family={}
        for ref in manifest['cases']:
            case=read(ROOT/'.ai/runtime'/ref)
            family=case['document_kind'];cases_by_family[family]=cases_by_family.get(family,0)+1
            spec=read(CONTENT/f'document_kinds/{family}.yaml')
            required={u['semantic_fields'][0]:u['id'] for u in spec['required_information']}
            self.assertTrue(set(required)<=case['semantic_units'].keys())
            for field in required:
                self.assertTrue(case['semantic_units'][field])
            variants={v['id']:v for v in case['variants']}
            self.assertEqual(len(variants),9)
            missing=copy.deepcopy(case['semantic_units']);field=variants['missing-core']['field'];del missing[field]
            detected=[rule for name,rule in required.items() if name not in missing]
            self.assertEqual(detected,variants['missing-core']['expected_rule_ids'])
            headings={name:'' for name in required}
            detected=[rule for name,rule in required.items() if not headings[name]]
            self.assertEqual(detected,variants['headings-only']['expected_rule_ids'])
            self.assertTrue(variants['excessive']['must_not_automatically_block'])
            self.assertIn('global.authority_bypass',variants['regulatory-exception']['expected_rule_ids'])
            self.assertFalse(case['reference_expectation']['production_pass_claim'])
        self.assertEqual(set(cases_by_family),set(registry['priority_document_kinds']))
        self.assertEqual(set(cases_by_family.values()),{3})

if __name__=='__main__':unittest.main()
