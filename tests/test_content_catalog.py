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
            else:
                self.assertEqual(b['decision_supported']['status'],'mapped-proposed')
                self.assertIn(contract['id'],b['decision_supported']['evidence_refs'][0])
                self.assertFalse(b['decision_supported']['human_approval'])
                self.assertNotEqual(b['decision_supported']['value'],contract['jai']['intent']['decision_supported'])

    def test_coverage_and_unique_kind_contracts(self):
        """Every registered layer has substantive proposed obligations and attribution."""
        registry=read(CONTENT/'registry.json')
        self.assertEqual([len(registry['mappings'][key]) for key in ['artifact_types','archetypes','sabsa_views']],[28,13,19])
        complete=[s for s in registry['specifications'] if s['completeness']=='complete']
        self.assertEqual(len(complete),1233)
        self.assertEqual(len(registry['mappings']['domains']),6)
        fieldsets=[]
        for entry in complete:
            spec=read(CONTENT/entry['path'])
            self.assertEqual(spec['status'],'proposed')
            self.assertIsNone(spec['approval']['authority_ref'])
            self.assertEqual(spec['calibration_status'],'synthetic-only')
            self.assertGreaterEqual(len(spec['required_information']),1)
            for group in ['required_information','conditional_information','optional_information','forbidden_information','low_value_information']:
                self.assertTrue(spec[group])
                for unit in spec[group]:
                    self.assertTrue(unit['rationale']['reason'])
                    self.assertFalse(unit['provenance']['normative_claim'])
            fieldsets.append(tuple(u['semantic_fields'][0] for u in spec['required_information']))
            self.assertFalse(spec['size_budget']['minimum_is_quality_gate'])
        self.assertGreaterEqual(len(set(fieldsets)),60)

    def test_coverage_separates_authorship_evaluation_and_authority(self):
        """Coverage never promotes policy metadata to trusted approval evidence."""
        import sys
        sys.path.insert(0,str(ROOT/'.ai/runtime/tools'))
        from content_spec import ContentSpec
        report=ContentSpec(ROOT).coverage()
        expected={'type':28,'archetype':13,'sabsa':19,'domain':12,'document_kind':1161}
        for category,count in expected.items():
            dimension=report['coverage_dimensions'][category]
            self.assertEqual(dimension['registered'],count)
            self.assertEqual(dimension['authored'],count)
            self.assertEqual(dimension['declared_human_approved'],0)
            self.assertIsNone(dimension['verified_human_approved'])
            self.assertIsNone(dimension['evaluated'])
        self.assertEqual(report['decision_supported_migration']['mapped-proposed'],1129)
        self.assertFalse(report['production_ready'])

    def test_role_proposals_retain_exact_inputs_gates_and_proposed_actions(self):
        """Contract proposals preserve source-specific substance and review boundaries."""
        registry=read(CONTENT/'registry.json')
        contracts={row['id']:row for row in read(ROOT/'.ai/runtime/artifacts/contracts/role-deliverables.v3.json')['contracts']}
        for entry in registry['document_kinds']:
            if not entry['id'].startswith('role/'):
                continue
            spec=read(CONTENT/f"document_kinds/roles/{entry['id'][5:].replace(':','-')}.yaml")
            cid=entry['id'][5:];contract=contracts[cid]
            units={row['semantic_fields'][0]:row for row in spec['required_information']}
            self.assertIn('decision_purpose_correction',units)
            self.assertTrue(units['role_gate_observations']['source_role_gate_refs'])
            self.assertTrue(units['delivery_verification']['source_deliverable']['acceptance_criterion'])
            for index,input_name in enumerate(contract['jai']['semantics']['required_inputs'],1):
                unit=units[f'contract_input_{index}']
                self.assertEqual(unit['source_input']['value'],input_name)
                self.assertEqual(unit['source_input']['contract_id'],cid)
                self.assertIn(input_name,unit['acceptance_criteria'][0])
            self.assertIn('domain/',spec['inherits'][1])
            self.assertEqual(spec['source_contract']['source_fingerprint'],contract['source_fingerprint'])

    def test_modality_and_view_obligations_are_distinct(self):
        """Data and models avoid prose quotas; SABSA risk treatment specialises risk."""
        for name,metric in [('dataset','rows'),('register','rows'),('model','elements'),('configuration-baseline','typed'),('presentation','slides')]:
            self.assertEqual(read(CONTENT/f'types/{name}.yaml')['size_budget']['metric'],metric)
        risk=read(CONTENT/'sabsa/risk-treatment-plan.yaml')
        self.assertIn('kind/risk-assessment',risk['inherits'])
        fields=[]
        for path in (CONTENT/'sabsa').glob('*.yaml'):
            view=read(path)
            fields.append(tuple(row['semantic_fields'][0] for row in view['required_information']))
            self.assertEqual(len(view['required_information']),4)
        self.assertEqual(len(set(fields)),19)

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


class SemanticTaxonomyTests(unittest.TestCase):
    """Historical IDs resolve through explicit shared families without reapproval."""

    def engine(self):
        import sys
        sys.path.insert(0,str(ROOT/'.ai/runtime/tools'))
        from content_spec import ContentSpec
        return ContentSpec(ROOT)

    def test_every_historical_kind_alias_has_one_shared_family(self):
        engine=self.engine()
        self.assertEqual(len(engine.registry['kind_aliases']),1139)
        self.assertEqual(len(engine.registry['semantic_families']),49)
        self.assertEqual(engine._taxonomy_errors(),[])
        for binding in engine.bindings.values():
            family=binding['semantic_family']
            self.assertNotIn('role/',family)
            self.assertEqual(binding['content_spec_ref'],'kind/'+binding['document_kind'])
        resolved=engine.resolve('chief-information-officer:1')
        self.assertEqual(resolved['document_kind'],'role/chief-information-officer:1')
        self.assertEqual(resolved['semantic_family'],'strategy')
        self.assertEqual(resolved['decision_supported']['status'],'mapped-proposed')
        self.assertFalse(resolved['production_ready'])

    def test_priority_anchors_and_historical_role_unit_ids_remain_stable(self):
        engine=self.engine()
        result=engine.resolve('enterprise-architect:4')
        self.assertEqual(result['document_kind'],'adr')
        self.assertEqual(result['semantic_family'],'adr')
        self.assertIn('adr.architecture_choice',{u['id'] for u in result['blueprint']['semantic_units']})
        legacy=engine.resolve('chief-information-officer:1')
        self.assertIn('role/chief-information-officer:1.decision_purpose_correction',
            {u['id'] for u in legacy['blueprint']['semantic_units']})

    def test_conflicting_duplicate_alias_and_unknown_family_fail_explicitly(self):
        engine=self.engine()
        engine.registry['kind_aliases'].append(dict(engine.registry['kind_aliases'][0]))
        self.assertIn('TAXONOMY_CONFLICT',engine._taxonomy_errors()[0])
        engine.registry['kind_aliases'].pop()
        engine.bindings['chief-information-officer:1']['semantic_family']='unregistered'
        with self.assertRaisesRegex(ValueError,'TAXONOMY_CONFLICT'):
            engine.resolve('chief-information-officer:1')

    def test_alias_cannot_change_binding_or_omit_shared_family(self):
        engine=self.engine()
        alias=next(a for a in engine.registry['kind_aliases'] if a['contract_id']=='chief-information-officer:1')
        alias['family']='release-notes'
        self.assertTrue(any('TAXONOMY_CONFLICT' in e for e in engine._taxonomy_errors()))
        alias['family']='strategy'
        engine.specs['kind/role/chief-information-officer:1']['inherits'].remove('family/strategy')
        with self.assertRaisesRegex(ValueError,'shared family not inherited'):
            engine.resolve('chief-information-officer:1')

    def test_proposed_action_requires_evidence_and_cannot_claim_approval(self):
        engine=self.engine()
        purpose=engine.bindings['chief-information-officer:1']['decision_supported']
        purpose['evidence_refs']=[]
        self.assertTrue(any('PURPOSE_MAPPING_INVALID' in e for e in engine._taxonomy_errors()))
        purpose['evidence_refs']=['public-source']
        purpose['human_approval']=True
        self.assertTrue(any('PURPOSE_MAPPING_INVALID' in e for e in engine._taxonomy_errors()))


    def test_copied_acceptance_and_wrong_recipient_cannot_masquerade_as_purpose(self):
        engine=self.engine()
        binding=engine.bindings['chief-information-officer:1']
        purpose=binding['decision_supported']
        original=purpose['value']
        purpose['value']=purpose['source_acceptance_text']
        with self.assertRaisesRegex(ValueError,'PURPOSE_MAPPING_PROVENANCE_MISMATCH'):
            engine.resolve('chief-information-officer:1')
        purpose['value']=original
        purpose['receiving_roles']=['Unrelated recipient']
        with self.assertRaisesRegex(ValueError,'PURPOSE_MAPPING_PROVENANCE_MISMATCH'):
            engine.resolve('chief-information-officer:1')


class PurposeMeaningTests(unittest.TestCase):
    """Source meanings take precedence over historically broad modalities."""

    def test_refined_and_implementation_purposes_match_the_actual_deliverable(self):
        bindings={b['artifact_id']:b for b in read(CONTENT/'migrations/26.10.5-binding-map.json')['bindings']}
        cases={
            'business-analyst:1':('requirements','Implement the specified parameters'),
            'chief-information-officer:1':('strategic choices','Sequence delivery increments'),
            'release-engineer:3':('deployment automation','Adopt, revise or abandon'),
            'software-engineer:2':('automated tests','Adopt, revise or abandon'),
        }
        for cid,(required,forbidden) in cases.items():
            value=bindings[cid]['decision_supported']['value']
            self.assertIn(required,value)
            self.assertNotIn(forbidden,value)


class CompiledPurposeConsistencyTests(unittest.TestCase):
    """Executed duties must not acquire incompatible historical modality rules."""

    def test_automation_and_software_artifacts_do_not_require_prototype_or_option_papers(self):
        import sys
        sys.path.insert(0,str(ROOT/'.ai/runtime/tools'))
        from content_spec import ContentSpec
        engine=ContentSpec(ROOT)
        for cid in ['release-engineer:3','software-engineer:1','software-engineer:2',
                    'software-engineer:4','devops-engineer:1','devops-engineer:2',
                    'devops-engineer:4','test-automation-engineer:3']:
            units=engine.resolve(cid)['blueprint']['semantic_units']
            ids={u['id'] for u in units}
            self.assertNotIn('type/prototype.prototype_hypothesis',ids,cid)
            self.assertNotIn('type/decision-paper.option_comparison',ids,cid)
            self.assertTrue(any(u['id'].startswith('global.') for u in units),cid)
            self.assertTrue(any('role_gate_observations' in u['id'] for u in units),cid)
        deployment=engine.resolve('release-engineer:3')['blueprint']['semantic_units']
        self.assertIn('family/deployment-automation.deployment_controls',{u['id'] for u in deployment})

    def test_refined_semantic_family_replaces_incompatible_legacy_modality(self):
        import sys
        sys.path.insert(0,str(ROOT/'.ai/runtime/tools'))
        from content_spec import ContentSpec
        engine=ContentSpec(ROOT)
        strategy=engine.resolve('chief-technology-officer:1')['blueprint']['semantic_units']
        self.assertNotIn('type/register.register_records',{u['id'] for u in strategy})
        self.assertIn('family/strategy.strategic_choices',{u['id'] for u in strategy})
        prototype=next(cid for cid,b in engine.bindings.items() if b['artifact_type']=='prototype' and cid not in ['software-engineer:4','release-engineer:3','devops-engineer:1','devops-engineer:2','devops-engineer:4'])
        self.assertIn('type/prototype.prototype_hypothesis',
            {u['id'] for u in engine.resolve(prototype)['blueprint']['semantic_units']})


    def test_all_exact_engineering_corrections_retain_source_identity_and_domain_controls(self):
        import sys
        sys.path.insert(0,str(ROOT/'.ai/runtime/tools'))
        sys.path.insert(0,str(ROOT/'tools'))
        from content_spec import ContentSpec
        from content_catalog_definitions import CONTRACT_PURPOSE_ACTIONS, TYPE_DOMAINS
        engine=ContentSpec(ROOT)
        contracts={c['id']:c for c in read(ROOT/'.ai/runtime/artifacts/contracts/role-deliverables.v3.json')['contracts']}
        for cid in CONTRACT_PURPOSE_ACTIONS:
            legacy=contracts[cid]['jai']['semantics']['artifact_type']
            result=engine.resolve(cid)
            self.assertEqual(engine.bindings[cid]['artifact_type'],legacy)
            inherited={item['id'] for item in result['inheritance']}
            self.assertIn('global/invariants',inherited,cid)
            self.assertIn('domain/'+TYPE_DOMAINS[legacy],inherited,cid)
            self.assertEqual(engine.specs[result['spec_id']]['applies_to']['artifact_types'],[legacy])
            self.assertFalse(result['production_ready'])

    def test_unknown_semantic_foundation_is_rejected_without_fallback(self):
        import sys
        sys.path.insert(0,str(ROOT/'.ai/runtime/tools'))
        from content_spec import ContentSpec
        engine=ContentSpec(ROOT)
        ref='kind/role/release-engineer:3'
        engine.specs[ref]['semantic_foundation_ref']='family/missing'
        with self.assertRaisesRegex(ValueError,'UNREGISTERED_SEMANTIC_FOUNDATION'):
            engine.compile(ref)


    def test_malformed_or_wrong_registered_foundation_fails_with_spec_error(self):
        import sys
        sys.path.insert(0,str(ROOT/'.ai/runtime/tools'))
        from content_spec import ContentSpec, SpecError
        engine=ContentSpec(ROOT)
        ref='kind/role/release-engineer:3'
        for value in [[],{},None,False,'']:
            engine.specs[ref]['semantic_foundation_ref']=value
            with self.assertRaisesRegex(SpecError,'INVALID_SEMANTIC_FOUNDATION'):
                engine.compile(ref)
        engine.specs[ref]['semantic_foundation_ref']='type/register'
        with self.assertRaisesRegex(SpecError,'SEMANTIC_FOUNDATION_MISMATCH'):
            engine.compile(ref)


    def test_foundation_requires_a_registered_semantic_family(self):
        import sys
        sys.path.insert(0,str(ROOT/'.ai/runtime/tools'))
        from content_spec import ContentSpec, SpecError
        engine=ContentSpec(ROOT)
        ref='kind/role/release-engineer:3'
        for value in [None,'missing']:
            engine.specs[ref]['semantic_family']=value
            with self.assertRaisesRegex(SpecError,'UNREGISTERED_SEMANTIC_FAMILY'):
                engine.compile(ref)


class CatalogGeneratorBehaviorTests(unittest.TestCase):
    """Exercise public generator contracts, including source-specific derivation."""

    def generator(self):
        import sys
        sys.path.insert(0,str(ROOT/'tools'))
        import generate_content_catalog
        return generate_content_catalog

    def test_canonical_bytes_and_modality_boundaries(self):
        generator=self.generator()
        self.assertEqual(generator.canonical({'z':2,'a':1}),b'{"a":1,"z":2}')
        with self.assertRaises(TypeError):
            generator.canonical({'unsupported':{1,2}})
        for artifact,metric in [('dataset','rows'),('model','elements'),('prototype','typed'),
                                ('presentation','slides'),('document','semantic_units')]:
            self.assertEqual(generator.modality(artifact),metric)

    def test_complete_policy_preserves_approval_boundary_and_required_content(self):
        generator=self.generator()
        policy=generator.spec('kind/synthetic-check','document_kind','Synthetic check','complete')
        required=generator.unit('synthetic-check','scope','object','Identify the explicit scope and evidence boundary.')
        policy['required_information']=[required]
        generator.complete_policy(policy,'synthetic-check')
        self.assertEqual(policy['required_information'],[required])
        self.assertEqual(policy['forbidden_information'][0]['obligation'],'MUST NOT')
        self.assertEqual(policy['conditional_information'][0]['when']['field'],'processes_personal_data')
        self.assertIsNone(policy['approval']['authority_ref'])
        self.assertEqual(policy['status'],'proposed')

    def test_contract_units_and_purposes_keep_specific_source_inputs_and_authorities(self):
        generator=self.generator()
        contract=read(ROOT/'.ai/runtime/artifacts/contracts/role-deliverables.v3.json')['contracts'][0]
        source={'deliverable':{'name':'Synthetic source deliverable','format':'Versioned JSON',
                'acceptance_criterion':'Trace concrete entries to versioned evidence'},
                'role':{'path':'skills/synthetic-role.md'},'gates':[{'id':'G1','criterion':'Evidence is attributable'}]}
        units=generator.contract_units(contract,'synthetic-check',source)
        inputs=[u['source_input'] for u in units if 'source_input' in u]
        self.assertEqual([u['value'] for u in inputs],contract['jai']['semantics']['required_inputs'])
        self.assertTrue(all(u['contract_id']==contract['id'] for u in inputs))
        purpose=generator.decision_mapping(contract,source)
        self.assertIn(source['deliverable']['name'],purpose['value'])
        self.assertEqual(purpose['receiving_roles'],contract['jai']['intent']['audience'])
        self.assertEqual(purpose['status'],'mapped-proposed')
        self.assertFalse(purpose['human_approval'])
        priority=generator.decision_mapping(contract,source,'Choose a bounded synthetic option')
        self.assertEqual(priority['value'],'Choose a bounded synthetic option')
        self.assertFalse(priority['human_approval'])

    def test_build_reproduces_registered_kinds_and_exact_legacy_binding_population(self):
        generator=self.generator()
        generated=generator.build()
        bindings=generated[CONTENT/'migrations/26.10.5-binding-map.json']['bindings']
        self.assertEqual(len(bindings),1139)
        self.assertEqual(len(generated[CONTENT/'expert-reference-bindings.json']['families']),32)
        registry=generated[CONTENT/'registry.json']
        self.assertEqual(len(registry['document_kinds']),1161)
        self.assertTrue(all(row['status']=='proposed' for row in registry['document_kinds']))


class CorpusGeneratorBehaviorTests(unittest.TestCase):
    """Direct behavioral contracts for the synthetic corpus generator APIs."""

    @classmethod
    def setUpClass(cls):
        import sys
        sys.path.insert(0,str(ROOT/'tools'))
        sys.path.insert(0,str(ROOT/'.ai/runtime/tools'))
        import generate_content_corpus
        from content_spec import ContentSpec
        cls.generator=generate_content_corpus
        cls.resolver=ContentSpec(ROOT)

    def test_populated_units_keep_financial_horizons_and_reject_unknown_inputs(self):
        for complexity in ('simple','medium','complex'):
            scenario=self.generator.SCENARIOS[complexity]
            units=self.generator.populated_units('business-case',complexity,scenario)
            self.assertIn('financial_model',units)
            self.assertTrue(units['investment_options'])
            self.assertTrue(units['financial_model'])
        with self.assertRaises(ValueError):
            self.generator.populated_units('business-case','invalid',self.generator.SCENARIOS['simple'])
        with self.assertRaises(KeyError):
            self.generator.populated_units('unknown','simple',self.generator.SCENARIOS['simple'])

    def test_compiled_case_preserves_standalone_and_role_identity_and_overlay_controls(self):
        standalone=self.generator.compiled_case(self.resolver,'kind/client-proposal',{})
        self.assertEqual(standalone['binding_kind'],'registered-document-kind')
        self.assertFalse(standalone['role_authority'])
        self.assertIsNone(standalone['source_role_contract_id'])
        role=self.generator.compiled_case(self.resolver,'enterprise-architect:1',{})
        overlay=self.generator.compiled_case(self.resolver,'enterprise-architect:1',{},['archetype/architecture-definition'])
        for key in ('artifact_id','document_kind','decision_supported'):
            self.assertEqual(role[key],overlay[key])
        self.assertNotEqual(role['compiled_spec_hash'],overlay['compiled_spec_hash'])
        with self.assertRaises(ValueError):
            self.generator.compiled_case(self.resolver,'missing:1',{})
        with self.assertRaises(ValueError):
            self.generator.compiled_case(self.resolver,'enterprise-architect:1',{},['archetype/missing'])

    def test_synthetic_value_respects_types_and_explicit_matrix_boundaries(self):
        unit={'datatype':'object','acceptance_criteria':['Identify the synthetic subject and criterion.']}
        scenario=self.generator.SCENARIOS['simple']
        value=self.generator.synthetic_value(unit,scenario,'new_subject')
        self.assertEqual(value['knowledge_status'],'synthetic-assumption')
        self.assertEqual(value['evidence_refs'],['SYN-01'])
        for datatype,expected_type in [('array',list),('string',str),('reference',str),
                                     ('integer',int),('number',int),('boolean',bool)]:
            self.assertIsInstance(self.generator.synthetic_value(dict(unit,datatype=datatype),scenario,'new_subject'),expected_type)
        matrix=self.generator.synthetic_value(dict(unit,datatype='array'),scenario,'matrix_coverage')
        self.assertEqual(len(matrix),36)
        self.assertEqual(len({(cell['row'],cell['column']) for cell in matrix}),36)
        with self.assertRaisesRegex(ValueError,'Unsupported synthetic datatype'):
            self.generator.synthetic_value(dict(unit,datatype='unsupported'),scenario,'new_subject')

    def test_enrich_case_preserves_authored_values_and_omits_inapplicable_or_optional_fields(self):
        document={'scenario':self.generator.SCENARIOS['simple'],'semantic_units':{'preserved':{'owner':'Authored synthetic owner'}}}
        required={'category':'required_information','applicability':True,'semantic_fields':['preserved','added'],
                  'datatype':'object','acceptance_criteria':['Identify the synthetic subject.']}
        excluded=dict(required,semantic_fields=['excluded'],applicability=False)
        optional=dict(required,semantic_fields=['optional'],category='optional_information')
        self.generator.enrich_case(document,{'blueprint':{'semantic_units':[required,excluded,optional]}})
        self.assertEqual(document['semantic_units']['preserved'],{'owner':'Authored synthetic owner'})
        self.assertIn('added',document['semantic_units'])
        self.assertNotIn('excluded',document['semantic_units'])
        self.assertNotIn('optional',document['semantic_units'])

    def test_enterprise_cases_include_all_standalone_complexities_and_real_binding_selection(self):
        cases=self.generator.enterprise_cases(self.resolver)
        self.assertEqual(len(cases),1291)
        standalone=[case for case in cases.values() if case['contract_id'].startswith('kind/')]
        self.assertEqual(len(standalone),66)
        for case in standalone:
            resolved=self.resolver.resolve(case['contract_id'],case['context'])
            self.assertEqual(case['document_kind'],resolved['document_kind'])
            self.assertTrue(case['structural_probe'])
            self.assertEqual(len(case['variants']),9)
        legacy=next(case for case in cases.values() if case['contract_id']=='chief-information-officer:1')
        self.assertEqual(legacy['document_kind'],'role/chief-information-officer:1')
