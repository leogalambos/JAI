# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Routing discovery, consultation and fail-closed adapter regression tests."""
import copy
import hashlib
import importlib.util
import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

PATH = Path(__file__).resolve().parents[1] / '.ai/runtime/tools/commercial_router.py'
spec = importlib.util.spec_from_file_location('commercial_router', PATH)
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)


class CommercialRouterTests(unittest.TestCase):
    def test_compact_root_and_selected_shard_do_not_read_role_bodies(self):
        catalog = r.Catalog()
        self.assertEqual(catalog.loaded, [])
        self.assertEqual(len(catalog.domains()), 17)
        result = catalog.route('firewall perimeter', 'ctr-1', ['network-and-telecommunications'])
        self.assertEqual(result['loaded_domains'], ['network-and-telecommunications'])
        self.assertTrue(any('firewall' in x['role_id'] for x in result['candidates']))
        self.assertFalse(result['authority_granted'])
        self.assertNotIn('model', result)

    def test_flat_and_exact_baselines_and_unresolved_unknown(self):
        catalog = r.Catalog()
        result = catalog.route('Firewall and Perimeter Engineer', 'ctr-1', strategy='deterministic')
        self.assertEqual(result['status'], 'candidate')
        self.assertEqual(len(result['loaded_domains']), 17)
        self.assertTrue(r.Catalog().route('firewall', 'ctr-1', strategy='flat')['candidates'])
        self.assertEqual(r.Catalog().route('zzzzzz', 'ctr-1')['status'], 'unresolved')
        with self.assertRaises(ValueError):
            catalog.route('firewall', '', tier='author')

    def test_integration_missing_corrupt_and_truncated_catalog_fail(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / 'catalog.json'
            data = copy.deepcopy(r.Catalog().data)
            data['complete'] = False
            path.write_text(json.dumps(data))
            with self.assertRaises(ValueError):
                r.Catalog(path)
            data['complete'] = True
            path.write_text(json.dumps(data))
            cat = r.Catalog(path)
            with self.assertRaises(OSError):
                cat.shard(data['domains'][0]['domain_id'])
            row = data['domains'][0]
            shard = path.parent / row['shard']
            shard.parent.mkdir(parents=True)
            shard.write_text('{}')
            with self.assertRaises(ValueError):
                cat.shard(row['domain_id'])
            row['sha256'] = hashlib.sha256(b'{}').hexdigest()
            path.write_text(json.dumps(data))
            with self.assertRaises(ValueError):
                r.Catalog(path).shard(row['domain_id'])

    def test_both_providers_not_run_are_blocked_and_documentation_is_not_test(self):
        for provider in ('codex', 'claude'):
            self.assertEqual(r.provider_readiness(provider, {})['status'], 'blocked')
            config = dict(provider_version='1', adapter_version='1', configuration_digest='hash',
                          deployment='local', product='CLI', model='allowed')
            record = dict(config, provider=provider, capability='tool_ceiling',
                          documentation_status='documented', local_status='not_run')
            self.assertEqual(r.provider_readiness(provider, config, [record], ['tool_ceiling'])['status'], 'blocked')
            record.update(local_status='tested', test_result='pass', evidence_ref='evidence:1',
                          observed_at=datetime.now(timezone.utc).isoformat(), provenance_kind='negative-runtime-test')
            self.assertEqual(r.provider_readiness(provider, config, [record], ['tool_ceiling'])['status'], 'ready')
            config['configuration_digest'] = 'changed'
            self.assertEqual(r.provider_readiness(provider, config, [record], ['tool_ceiling'])['status'], 'blocked')
            config['configuration_digest'] = 'hash'
            del record['evidence_ref']
            with self.assertRaises(ValueError):
                r.provider_readiness(provider, config, [record], ['tool_ceiling'])

    def _consultation(self):
        request = dict(consultation_id='consult-1', purpose='bid sizing', question='firewall effort?',
                       minimal_input=[dict(ref='constraint:1', version='1', classification='client')],
                       classification='client', evidence=['source passages and applicability'],
                       deadline='2026-10-17T00:00:00Z', budget='50', recipient='firewall-engineer',
                       contracting_owner='commercial-owner', requester_contract='ctr-1',
                       output_schema='consultation-response/1', ancestry=[])
        context = dict(actor_role='orchestrator', contracting_owner='commercial-owner',
                       requester_contract='ctr-1', clearance='internal',
                       allowed_recipients=['firewall-engineer'], allowed_inputs=[['constraint:1', '1']],
                       episode_ids=[], max_depth=3, remaining_budget='50', input_classifications={'constraint:1':'client'})
        return request, context

    def test_procurement_firewall_retains_owner_and_reserves_budget(self):
        request, context = self._consultation()
        result = r.consultation_request(request, context, datetime(2026, 10, 16, tzinfo=timezone.utc))
        self.assertEqual(result['status'], 'validated')
        self.assertEqual(result['remaining_budget_after_reservation'], '0')
        self.assertEqual(result['request']['contracting_owner'], 'commercial-owner')
        self.assertFalse(result['authority_granted'])
        self.assertTrue(result['requires_atomic_episode_reservation'])

    def test_consultation_rejects_leaks_leaf_loops_owner_and_exhaustion(self):
        for key, value in [('actor_role', 'leaf'), ('contracting_owner', 'other'), ('allowed_inputs', [])]:
            request, context = self._consultation()
            context[key] = value
            with self.assertRaises(ValueError):
                r.consultation_request(request, context)
        request, context = self._consultation()
        request['minimal_input'][0]['classification'] = 'internal'
        with self.assertRaises(ValueError):
            r.consultation_request(request, context)
        request, context = self._consultation()
        request['ancestry'] = ['consult-1']
        with self.assertRaises(ValueError):
            r.consultation_request(request, context)
        request, context = self._consultation()
        request['budget'] = '51'
        self.assertEqual(r.consultation_request(request, context)['status'], 'unresolved')
        request['budget'] = 'NaN'
        with self.assertRaises(ValueError):
            r.consultation_request(request, context)

    def test_response_requires_authentication_independence_and_exact_digest(self):
        request, _ = self._consultation()
        response = dict(consultation_id='consult-1', assumptions=['bounded scope'],
                        source_passage_ids=['passage:1'], applicability='same product',
                        estimate_state='supported', unit='h', interval=['8', '16'],
                        uncertainty='scope', execution_id='worker')
        digest = hashlib.sha256(json.dumps(response, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
        review = dict(execution_id='checker', result='accepted', response_sha256=digest)
        executions = {'worker': dict(authenticated=True, principal='engineer'),
                      'checker': dict(authenticated=True, principal='reviewer')}
        result = r.incorporate_response(request, response, review, 'commercial-owner', executions)
        self.assertEqual(result['contracting_owner'], 'commercial-owner')
        executions['checker']['principal'] = 'engineer'
        with self.assertRaises(ValueError):
            r.incorporate_response(request, response, review, 'commercial-owner', executions)
        executions['checker']['principal'] = 'reviewer'
        response['interval'] = ['1', '2']
        with self.assertRaises(ValueError):
            r.incorporate_response(request, response, review, 'commercial-owner', executions)

class CommercialAdapterRenderingTests(unittest.TestCase):
    def test_provider_rendering_only_reads_new_sources_and_preserves_workload_policy(self):
        root = PATH.parents[3]
        setup_spec = importlib.util.spec_from_file_location('commercial_installer', root / '.ai/setup/installer.py')
        installer = importlib.util.module_from_spec(setup_spec)
        setup_spec.loader.exec_module(installer)
        registry = json.loads((root / '.ai/runtime/models/model-registry.json').read_text())
        agent = root / '.ai/agents/commercial-coordinator.md'
        codex = installer.render_codex_skill(agent, 'agent', 'commercial-coordinator', registry).decode()
        claude = installer.render_claude_agent(agent, registry).decode()
        self.assertIn('agent-commercial-coordinator', codex)
        self.assertIn('Workload class: `standard`', codex)
        self.assertNotIn('model_class:', claude)
        command = installer.render_codex_skill(root / '.ai/commands/commercial.md', 'command', 'commercial', registry).decode()
        self.assertIn('workflow-commercial', command)
        skill = installer.render_codex_skill(root / '.ai/skills/commercial-delivery/SKILL.md', 'skill', 'commercial-delivery', registry).decode()
        self.assertIn('name: commercial-delivery', skill)
        self.assertIn('not_run', skill)

class CommercialReservationTests(unittest.TestCase):
    _consultation = CommercialRouterTests._consultation
    def test_integration_atomic_budget_replay_stale_revision_and_exhaustion(self):
        request, context = self._consultation()
        now = datetime(2026, 10, 16, tzinfo=timezone.utc)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'episode.json'
            result = r.reserve_consultation(path, request, context, 0, now)
            self.assertEqual(result['revision'], 1)
            self.assertFalse(result['requires_atomic_episode_reservation'])
            with self.assertRaises(ValueError):
                r.reserve_consultation(path, request, context, 0, now)
            with self.assertRaises(ValueError):
                r.reserve_consultation(path, request, context, 1, now)
            request['consultation_id'] = 'consult-2'
            self.assertEqual(r.reserve_consultation(path, request, context, 1, now)['status'], 'unresolved')
            self.assertEqual(json.loads(path.read_text())['revision'], 1)


if __name__ == '__main__':
    unittest.main()

class CapabilityTimestampTests(unittest.TestCase):
    def test_malformed_future_stale_observations_never_pass(self):
        config = dict(provider_version='1', adapter_version='1', configuration_digest='hash', deployment='local', product='CLI', model='allowed')
        record = dict(config, provider='codex', capability='tool_ceiling', local_status='tested', test_result='pass', evidence_ref='evidence:1', provenance_kind='negative-runtime-test')
        for timestamp in ('not-a-date', '2026-10-16T00:00:00'):
            record['observed_at'] = timestamp
            with self.assertRaises(ValueError):
                r.provider_readiness('codex', config, [record], ['tool_ceiling'])
        for timestamp in ('2026-10-18T00:00:00Z', '2026-10-01T00:00:00Z'):
            record['observed_at'] = timestamp
            self.assertEqual(r.provider_readiness('codex', config, [record], ['tool_ceiling'], now=datetime(2026,10,16,tzinfo=timezone.utc))['status'], 'blocked')

class RoutingEvaluationTests(unittest.TestCase):
    def test_evaluate_routing_reports_observed_metrics_and_unknowns(self):
        corpus={'version':'1','cases':[{'question':'Firewall and Perimeter Engineer','expected_roles':['firewall-and-perimeter-engineer']},{'question':'zzzzz','expected_roles':[]}]}
        result=r.evaluate_routing(corpus)
        self.assertEqual(len(result['results']),6)
        self.assertTrue(all(row['provider_invocations']==0 and row['elapsed_seconds']>=0 and row['root_bytes']>0 for row in result['results']))
        exact=next(row for row in result['results'] if row['strategy']=='deterministic' and row['question'].startswith('Firewall'))
        self.assertEqual(exact['recall'],1)
        self.assertTrue(exact['top_correct'])
        with self.assertRaises(ValueError):r.evaluate_routing({'version':'1','cases':[]})
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(OSError):r.evaluate_routing(corpus,Path(directory)/'missing.json')

class RootDomainRecallTests(unittest.TestCase):
    def test_basic_exact_roles_route_uniquely_and_bounded_in_hierarchy_and_baselines(self):
        cases=[('IT Procurement Specialist','it-procurement-specialist'),('Business Analyst','business-analyst'),('Firewall and Perimeter Engineer','firewall-and-perimeter-engineer')]
        corpus={'version':'1','cases':[{'question':question,'expected_roles':[role]} for question,role in cases]}
        result=r.evaluate_routing(corpus)
        self.assertTrue(all(row['top_correct'] and row['recall']==1 for row in result['results']))
        for question,role in cases:
            decision=r.Catalog().route(question,'ctr')
            top=decision['candidates'][0]
            self.assertEqual(top['role_id'],role)
            self.assertEqual(decision['status'],'candidate')
            self.assertEqual(len(decision['loaded_domains']),1)
        self.assertEqual(r.Catalog().route('engineer and IT specialist','ctr')['candidates'],[])
        self.assertEqual(r.Catalog().route('zzzz unknown','ctr')['loaded_domains'],[])

class CzechConsultationRoutingTests(unittest.TestCase):
    def test_czech_procurement_firewall_consultation_selects_network_specialist(self):
        result=r.Catalog().route('Odhad pracnosti firewallu pro nabídku nákup požaduje', 'ctr-procurement', ['network-and-telecommunications'])
        self.assertTrue(any('firewall' in role['role_id'] for role in result['candidates']))
        self.assertEqual(result['loaded_domains'],['network-and-telecommunications'])
        automatic=r.Catalog().route('správa firewallu síť', 'ctr')
        self.assertIn('network-and-telecommunications',automatic['loaded_domains'])
        self.assertLessEqual(len(automatic['loaded_domains']),3)


class CommercialSpecialistIntentTests(unittest.TestCase):
    def test_supplier_specialist_intents_choose_fit_for_purpose_roles(self):
        cases = {
            'Supplier bid proposal management': 'bid-proposal-manager',
            'Commercial pricing deal finance margin cashflow': 'commercial-pricing-deal-finance-specialist',
            'Prepare basis of estimate and effort estimation': 'estimation-cost-engineering-specialist',
            'Independent commercial assurance review': 'independent-commercial-assurance-reviewer',
            'Supplier deal negotiation and commercial lifecycle': 'supplier-commercial-deal-manager',
            'Proved odhad pracnosti': 'estimation-cost-engineering-specialist',
            'Zajisti cenotvorba a prodejni cena': 'commercial-pricing-deal-finance-specialist',
            'Koordinuj tvorbu nabídky': 'bid-proposal-manager',
        }
        for question, expected in cases.items():
            with self.subTest(question=question):
                result = r.Catalog().route(question, 'supplier-contract')
                self.assertEqual(result['status'], 'candidate')
                self.assertEqual(result['candidates'][0]['role_id'], expected)
                self.assertEqual(result['loaded_domains'], ['commercial-sourcing-and-enablement'])
                self.assertFalse(result['authority_granted'])

    def test_independent_reviewer_preserves_advise_tier_and_explicit_tier_boundary(self):
        question = 'Independent commercial assurance review'
        candidate = r.Catalog().route(question, 'supplier-contract')['candidates'][0]
        self.assertEqual(candidate['tool_tier'], 'advise')
        restricted = r.Catalog().route(question, 'supplier-contract', tier='author')
        self.assertFalse(any(c['role_id'] == candidate['role_id'] for c in restricted['candidates']))

    def test_mixed_specialisms_are_unresolved_and_buyer_scope_keeps_its_own_role(self):
        result = r.Catalog().route('commercial pricing and effort estimation', 'supplier-contract')
        self.assertEqual(result['status'], 'unresolved')
        best = result['candidates'][0]['score']
        self.assertEqual({row['role_id'] for row in result['candidates'] if row['score'] == best},
                         {'commercial-pricing-deal-finance-specialist', 'estimation-cost-engineering-specialist'})
        buyer = r.Catalog().route('IT Procurement Specialist', 'buyer-contract')
        self.assertEqual(buyer['candidates'][0]['role_id'], 'it-procurement-specialist')
        unknown = r.Catalog().route('pricing', 'ambiguous-contract')
        self.assertTrue(all(row['score'] < 200 for row in unknown['candidates']))
        buyer = r.Catalog().route('buyer procurement evaluation of commercial pricing', 'buyer-contract')
        self.assertTrue(all(row['score'] < 200 for row in buyer['candidates']))

    def test_supplier_bid_keeps_buyer_clarifications_in_supplier_scope(self):
        result = r.Catalog().route('Prepare supplier bid including procurement clarifications', 'supplier-contract')
        self.assertEqual(result['status'], 'candidate')
        self.assertEqual(result['candidates'][0]['role_id'], 'bid-proposal-manager')

    def test_review_subject_does_not_dispatch_authors_but_separate_author_and_review_decomposes(self):
        result = r.Catalog().route('Independent commercial assurance of selling price and basis of estimate', 'supplier-contract')
        self.assertEqual(result['status'], 'candidate')
        self.assertEqual(result['candidates'][0]['role_id'], 'independent-commercial-assurance-reviewer')
        result = r.Catalog().route('Prepare commercial pricing and then independent commercial assurance', 'supplier-contract')
        self.assertEqual(result['status'], 'unresolved')
        self.assertEqual({c['role_id'] for c in result['candidates']}, {'commercial-pricing-deal-finance-specialist', 'independent-commercial-assurance-reviewer'})

    def test_cloud_resource_pricing_does_not_claim_supplier_deal_finance_scope(self):
        result = r.Catalog().route('Review the cloud pricing options for AWS compute', 'technology-contract')
        self.assertEqual(result['status'], 'unresolved')
        self.assertEqual(result['candidates'], [])
        result = r.Catalog().route('Supplier selling price for cloud AWS managed service deal', 'supplier-contract')
        self.assertEqual(result['status'], 'candidate')
        self.assertEqual(result['candidates'][0]['role_id'], 'commercial-pricing-deal-finance-specialist')


    def test_explicit_supplier_bid_action_keeps_customer_procurement_context(self):
        result = r.Catalog().route('Prepare supplier bid for buyer procurement RFP', 'supplier-contract')
        self.assertEqual(result['status'], 'candidate')
        self.assertEqual(result['candidates'][0]['role_id'], 'bid-proposal-manager')

    def test_explicit_technical_consultation_domain_preserves_its_estimate_owner(self):
        result = r.Catalog().route('Odhad pracnosti firewallu pro nabídku nákup požaduje', 'consultation-contract', ['network-and-telecommunications'])
        self.assertTrue(any('firewall' in role['role_id'] for role in result['candidates']))
        self.assertEqual(result['loaded_domains'], ['network-and-telecommunications'])
