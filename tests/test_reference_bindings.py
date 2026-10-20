# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Explicit reference mapping, proposed semantics and historical compatibility."""
import copy
import hashlib
import json
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
sys.path.insert(0,str(ROOT/'.ai/runtime/tools'))
from generate_content_catalog import validate_reference_bindings
from content_spec import ContentSpec


class ReferenceBindingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine=ContentSpec(ROOT)
        cls.document=json.loads((ROOT/'.ai/runtime/content/expert-reference-bindings.json').read_text())
        cls.contracts=json.loads((ROOT/'.ai/runtime/artifacts/contracts/role-deliverables.v3.json').read_text())['contracts']
        cls.contract_ids={row['id'] for row in cls.contracts}

    def test_all_reference_review_supplements_preserve_unexecuted_evidence_and_external_authority(self):
        manifest=json.loads((ROOT/'.ai/runtime/content/expert_references/index.json').read_text())
        for entry in manifest['entries']:
            path=ROOT/'.ai/runtime/content/expert_references'/entry['path']
            text=path.read_text()
            with self.subTest(reference_id=entry['reference_id']):
                supplement=text.split('## Evidence-led expert review supplement (v2.3.0)',1)[1]
                self.assertIn('fictional',supplement)
                self.assertIn('OPEN until attributable evidence exists',supplement)
                self.assertIn('NOT_EXECUTED if no actual test or review',supplement)
                self.assertIn('PENDING, never inferred approval',supplement)
                self.assertIn('Human-approved status remains **false**',supplement)
                self.assertIn('Missing renderer = NOT_EXECUTED, not PASS',supplement)
                self.assertIn('DEFER external commitment or release',supplement)
                self.assertIn('Source fidelity',supplement)
                self.assertIn('Cross-artifact consistency',supplement)
                self.assertIn('No underlying customer system',supplement)

    def test_security_review_supplements_require_observed_negative_test_evidence(self):
        families=('security-architecture-assessment','threat-model','security-control-assessment',
                  'devsecops-pipeline-design','cicd-pipeline-assurance','appsec-verification-report',
                  'software-supply-chain-assessment')
        for family in families:
            for level in ('simple','medium','complex'):
                text=(ROOT/'.ai/runtime/content/expert_references'/family/(level+'.md')).read_text()
                supplement=text.split('## Evidence-led expert review supplement (v2.3.0)',1)[1]
                with self.subTest(family=family,complexity=level):
                    self.assertIn('planned negative scenario',supplement)
                    self.assertIn('required technical trace and control owner',supplement)
                    self.assertIn('absent observed evidence is NOT_EXECUTED',supplement)
                    self.assertIn('Separate design review from observed operating effectiveness',supplement)

    def test_all_135_manifest_documents_have_exact_one_to_one_registered_anchor_mappings(self):
        manifest=json.loads((ROOT/'.ai/runtime/content/expert_references/index.json').read_text())
        by_family={row['reference_family']:row for row in self.document['families']}
        self.assertEqual(len(by_family),45)
        self.assertEqual(len(manifest['entries']),135)
        validate_reference_bindings(self.document,self.engine.specs,self.contract_ids)
        for entry in manifest['entries']:
            mapping=by_family[entry['document_kind']]
            expected={row['source_anchor'].removeprefix('dcs-') for row in mapping['anchor_bindings']}
            self.assertEqual(set(entry['anchor_ids']),expected,entry['reference_id'])
            compiled=self.engine.compile(mapping['spec_ref'])
            units={row['id']:row for row in compiled['blueprint']['semantic_units']}
            self.assertIn('global.secret_disclosure',units)
            for translation in mapping['anchor_bindings']:
                unit=units[translation['unit_id']]
                self.assertEqual(unit['obligation'],'MUST')
                self.assertGreater(len(unit['rationale']['reason']),50)
                self.assertEqual(unit['acceptance_predicate']['op'],'review')
            self.assertEqual(compiled['approval_status'],'pending-human-L0')
            self.assertFalse(compiled['production_ready'])

    def test_ten_proposal_kinds_are_substantive_proposed_existing_jai_integrations(self):
        families=['client-proposal','executive-proposal','technical-proposal','delivery-proposal',
            'commercial-proposal','statement-of-work','rfp-response','proposal-compliance-matrix',
            'cybersecurity-transformation-proposal','managed-security-services-proposal']
        for family in families:
            policy=self.engine.specs['kind/'+family]
            self.assertGreaterEqual(len(policy['required_information']),5)
            self.assertEqual(policy['commercial_integration']['profile'],'commercial-delivery/1')
            self.assertEqual(policy['approval']['status'],'pending')
            self.assertIsNone(policy['approval']['authority_ref'])
            self.assertTrue(any(u['id']==family+'.unapproved_commitment' for u in policy['forbidden_information']))
        self.assertIn('separately priced',self.engine.specs['kind/commercial-proposal']['required_information'][2]['rationale']['reason'])
        self.assertEqual(len(self.engine.bindings),1139)
        self.assertEqual(set(self.engine.bindings),self.contract_ids)
        for contract in self.contracts:
            binding=self.engine.bindings[contract['id']]
            self.assertEqual(binding['artifact_type'],contract['jai']['semantics']['artifact_type'])
            self.assertEqual(binding['source_fingerprint'],contract['source_fingerprint'])

    def test_conflicting_unknown_missing_and_false_approval_mappings_fail(self):
        mutations=[
            lambda d:d['families'].append(copy.deepcopy(d['families'][0])),
            lambda d:d['families'][0]['anchor_bindings'].append(copy.deepcopy(d['families'][0]['anchor_bindings'][0])),
            lambda d:d['families'][0]['anchor_bindings'].pop(),
            lambda d:d['families'][0]['anchor_bindings'][0].update(unit_id='unknown.unit'),
            lambda d:d['families'][0]['anchor_bindings'][0].update(source_anchor='dcs-unknown.unit'),
            lambda d:d['families'][0].update(spec_ref='kind/unknown'),
            lambda d:d['families'][0].update(role_contract_ids=['unknown:1']),
            lambda d:d.update(professional_approval='human-approved'),
        ]
        for mutate in mutations:
            document=copy.deepcopy(self.document)
            mutate(document)
            with self.assertRaisesRegex(ValueError,'REFERENCE_BINDING_'):
                validate_reference_bindings(document,self.engine.specs,self.contract_ids)

    def test_inherited_obligations_are_not_misreported_as_anchor_coverage(self):
        mapping=next(row for row in self.document['families'] if row['reference_family']=='service-design-sla')
        covered={row['unit_id'] for row in mapping['anchor_bindings']}
        compiled=self.engine.compile(mapping['spec_ref'])
        all_required={u['id'] for u in compiled['blueprint']['semantic_units'] if u['obligation']=='MUST'}
        self.assertTrue(covered<all_required)
        self.assertIn('additional authoring requirements',mapping['coverage_scope'])

    def test_standalone_kind_resolution_is_explicit_and_grants_no_role_authority(self):
        resolved=self.engine.resolve('kind/client-proposal',{'processes_personal_data':False})
        self.assertEqual(resolved['binding_kind'],'registered-document-kind')
        self.assertEqual(resolved['document_kind'],'client-proposal')
        self.assertIsNone(resolved['source_role_contract_id'])
        self.assertFalse(resolved['role_authority'])
        self.assertFalse(resolved['production_ready'])
        self.assertEqual(resolved,self.engine.resolve('kind/client-proposal',{'processes_personal_data':False}))
        changed=self.engine.resolve('kind/client-proposal',{'processes_personal_data':True})
        self.assertNotEqual(resolved['context_hash'],changed['context_hash'])
        self.assertNotEqual(resolved['resolution_hash'],changed['resolution_hash'])
        self.assertEqual(self.engine.resolve('bid-proposal-manager:3')['artifact_id'],'bid-proposal-manager:3')
        for invalid in ['kind/unknown','kind/type/document','kind/role/bid-proposal-manager:3','kind/client-proposal@99']:
            with self.assertRaises(ValueError):
                self.engine.resolve(invalid)

    def test_standalone_resolution_does_not_bypass_category_scope_or_global_controls(self):
        from content_spec import SpecError
        engine=ContentSpec(ROOT)
        policy=engine.specs['kind/client-proposal']
        policy['category']='type'
        with self.assertRaisesRegex(SpecError,'KIND_SCOPE_MISMATCH'):
            engine.resolve('kind/client-proposal')
        policy['category']='document_kind'
        policy['applies_to']['document_kind']='commercial-proposal'
        with self.assertRaisesRegex(SpecError,'KIND_SCOPE_MISMATCH'):
            engine.resolve('kind/client-proposal')
        policy['applies_to']['document_kind']='client-proposal'
        engine.specs.pop('global/invariants')
        with self.assertRaisesRegex(SpecError,'MISSING_GLOBAL_INVARIANTS'):
            engine.resolve('kind/client-proposal')

    def test_standalone_content_report_detects_credentials_and_rejects_rehashed_forgery(self):
        from content_lint import evaluate, verify_report
        from content_spec import canonical_hash
        spec=self.engine.resolve('kind/client-proposal',{'processes_personal_data':False,'regulatory_requirement':False})
        model={'artifact_id':'public-synthetic-proposal','contract_id':'kind/client-proposal',
            'document_kind':'client-proposal','context':spec['context'],'semantic_units':{},'claims':[],'evidence':[]}
        report=evaluate(model,spec)
        forged=copy.deepcopy(report)
        forged['compiled_spec_hash']='0'*64
        forged.pop('report_hash')
        forged['report_hash']=canonical_hash(forged)
        self.assertTrue(verify_report(forged,model,spec))
        changed=copy.deepcopy(model)
        changed['artifact_id']='changed-source-instance'
        self.assertTrue(verify_report(report,changed,spec))
        unsafe=copy.deepcopy(model)
        unsafe['semantic_units']['customer_need']={'password':'literal-credential-should-be-blocked'}
        blocked=evaluate(unsafe,spec)
        self.assertTrue(any(f['rule_id']=='global.secret_disclosure' and f['blocking'] for f in blocked['findings']))


    def test_explicit_role_reference_defaults_are_valid_without_changing_role_bindings(self):
        expected={'delivery-manager:1':'delivery-proposal','bid-proposal-manager:1':'rfp-response',
                  'bid-proposal-manager:3':'client-proposal'}
        self.assertEqual(self.document['authoring_defaults'],expected)
        for cid,family in expected.items():
            self.assertIn(cid,self.engine.bindings)
            record=next(row for row in self.document['families'] if row['reference_family']==family)
            self.assertIn(cid,record['role_contract_ids'])
        invalid=copy.deepcopy(self.document)
        invalid['authoring_defaults']['bid-proposal-manager:3']='runbook'
        with self.assertRaisesRegex(ValueError,'REFERENCE_BINDING_DEFAULT_INVALID'):
            validate_reference_bindings(invalid,self.engine.specs,self.contract_ids)


    def test_every_standalone_kind_has_three_complexities_and_defect_boundary_recipes(self):
        manifest=json.loads((ROOT/'.ai/runtime/evals/content_quality/manifest.json').read_text())
        standalone={record['spec_ref'] for record in self.document['families'] if record['registration']!='reused-priority-kind'}
        cases={ref:json.loads((ROOT/'.ai/runtime'/ref).read_text()) for ref in manifest['enterprise_cases']}
        selected=[case for case in cases.values() if case['contract_id'] in standalone]
        self.assertEqual(len(selected),105)
        for ref in standalone:
            matching=[case for case in selected if case['contract_id']==ref]
            self.assertEqual(len(matching),3,ref)
            self.assertEqual({case['scenario']['name'] for case in matching},
                {'Inventory service recovery','Regional order integration','Regulated payment platform transition'})
            for case in matching:
                self.assertTrue(case['structural_probe'])
                variants={variant['id']:variant for variant in case['variants']}
                self.assertIn('missing-core',variants)
                self.assertTrue(variants['missing-core']['expected_rule_ids'])
                self.assertEqual(variants['valid-conditional-na']['expected_category'],'borderline-review')
                self.assertFalse(case['reference_expectation']['production_pass_claim'])


    def test_standalone_binding_metadata_is_hashed_and_valid_for_actual_content_qa(self):
        from content_lint import evaluate
        from content_eval import prepare_case
        fixture=json.loads((ROOT/'.ai/runtime/evals/content_quality/enterprise/kind-client-proposal-simple.json').read_text())
        model,spec=prepare_case(fixture,self.engine)
        report=evaluate(model,spec)
        self.assertNotIn('COMPILED_SPEC_HASH_MISMATCH',{f['rule_id'] for f in report['findings']})
        tampered=copy.deepcopy(spec)
        tampered['role_authority']=True
        rejected=evaluate(model,tampered)
        self.assertIn('COMPILED_SPEC_HASH_MISMATCH',{f['rule_id'] for f in rejected['findings']})

    def test_engineering_specializations_are_explicit_proposals_without_role_activation(self):
        """New example namespaces never rebind existing production role contracts."""
        from content_reference_definitions import ENGINEERING_REFERENCE_KINDS
        self.assertEqual(len(ENGINEERING_REFERENCE_KINDS),13)
        for family in ENGINEERING_REFERENCE_KINDS:
            mapping=next(row for row in self.document['families'] if row['reference_family']==family)
            self.assertEqual(mapping['document_kind'],family)
            self.assertEqual(mapping['source_binding_status'],'proposed-not-mapped')
            self.assertEqual(mapping['role_contract_ids'],[])
            policy=self.engine.specs[mapping['spec_ref']]
            self.assertFalse(policy['reference_integration']['normative_activation'])
            self.assertEqual(policy['reference_integration']['selection_mode'],'explicit-kind-only')
            self.assertEqual(policy['approval']['status'],'pending')
            resolved=self.engine.resolve(mapping['spec_ref'])
            self.assertFalse(resolved['production_ready'])
            self.assertFalse(resolved['role_authority'])
            self.assertIsNone(resolved['source_role_contract_id'])
        self.assertEqual(len(self.engine.bindings),1139)
        self.assertFalse(any(row['document_kind'] in ENGINEERING_REFERENCE_KINDS for row in self.engine.bindings.values()))

    def test_established_reference_relationships_remain_exactly_compatible(self):
        """Pin the public v2.1 mapping, independently of newly added examples."""
        rows=self.document['families'][:32]
        digest=hashlib.sha256(json.dumps(rows,sort_keys=True,separators=(',',':')).encode()).hexdigest()
        self.assertEqual(digest,'f0d96418636baebe3fc036db96e95bbfbe262c6c22da9b793adced0e6d41ad6c')
        self.assertEqual(sum(len(row['anchor_bindings']) for row in rows),169)
