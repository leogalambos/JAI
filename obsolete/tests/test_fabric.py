# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Fabric helper regression tests use disposable state and synthetic authority keys."""
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from argparse import Namespace
import pytest
from lifecycle_fixtures import SyntheticOperator

SOURCE = Path(__file__).resolve().parents[1] / '.ai/runtime/fabric/fabric.py'
SPEC = importlib.util.spec_from_file_location('fabric_helper_test', SOURCE)
fabric = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(fabric)


class FabricHelperTests(unittest.TestCase):
    def _memory_graph(self, rows=(), edges=()):
        """Replay actual fresh transactions; L0 nodes use synthetic signed requests."""
        temporary=tempfile.TemporaryDirectory();self.addCleanup(temporary.cleanup)
        directory=Path(temporary.name)
        isolated=pytest.MonkeyPatch();self.addCleanup(isolated.undo)
        isolated.setattr(fabric,'FABRIC_DIR',str(directory))
        isolated.setattr(fabric,'open_fabric',lambda engagement: fabric.Fabric(engagement,fabric.load(engagement)))
        signer=SyntheticOperator(directory,isolated)
        graph=fabric.Fabric('fresh-fixture',[])
        for name,kind,layer,extra in rows:
            if layer==0:
                subject=next((source for source,label,target in edges
                              if label=='resolved_by' and target==name),None)
                escalation=graph.nodes[subject] if subject else graph.add_node('esc',1,'Synthetic authority fixture')
                request=directory/(name+'.request.json')
                decision=extra.get('decision','exception')
                fabric.cmd_authorise(Namespace(engagement=graph.eng,escalation=escalation['id'],
                    decision=decision,signer='Synthetic test operator',rationale='Disposable graph fixture',
                    expires=1,revise_text='Fresh synthetic formulation',supersedes=None,
                    adopt=None,beyond_round_limit=False,request_out=str(request)))
                signer.apply(fabric,request)
                graph=fabric.open_fabric(graph.eng)
                if name not in graph.nodes:
                    raise AssertionError('fixture must name the generated authority identity')
            else:
                graph.append('node',{'id':name,'type':kind,'layer':layer,'text':'Synthetic '+name,**extra})
        for source,label,target in edges:
            if label=='resolved_by':
                continue  # Already part of the exact signed authority transaction.
            graph.add_edge(source,label,target)
        return fabric.Fabric(graph.eng,fabric.load(graph.eng)) if rows else graph

    def test_round_no_counts_only_human_revisions_and_rejects_malformed_nodes(self):
        model = self._memory_graph()
        self.assertEqual(model.round_no(), 1)
        model = self._memory_graph([('auth-0001', 'auth', 0, {'decision': 'exception'}),
            ('auth-0002', 'auth', 0, {'decision': 'revise'}),
            ('auth-0003', 'auth', 0, {'decision': 'revise'})])
        self.assertEqual(model.round_no(), 3)
        model.nodes['broken'] = {}
        with self.assertRaises(KeyError):
            model.round_no()

    def test_contracts_this_round_resets_at_latest_revision_and_ignores_noncontracts(self):
        self.assertEqual(self._memory_graph().contracts_this_round(), 0)
        model = self._memory_graph([('old', 'ctr', 1, {}),
            ('auth-0001', 'auth', 0, {'decision': 'revise'}), ('new1', 'ctr', 1, {}),
            ('noise', 'req', 2, {}), ('new2', 'ctr', 2, {})])
        self.assertEqual(model.contracts_this_round(), 2)
        model.seq_of['new1'] = model.seq_of['auth-0001']
        self.assertEqual(model.contracts_this_round(), 1)
        del model.seq_of['new2']
        with self.assertRaises(KeyError):
            model.contracts_this_round()

    def test_steps_this_round_counts_episode_transitions_but_not_requirements(self):
        self.assertEqual(self._memory_graph().steps_this_round(), 0)
        model = self._memory_graph([('old', 'att', 2, {}),
            ('auth-0001', 'auth', 0, {'decision': 'revise'}), ('req', 'req', 2, {}),
            ('attempt', 'att', 2, {}), ('evidence', 'evd', 6, {}), ('review', 'rev', 1, {})])
        self.assertEqual(model.steps_this_round(), 3)
        model.seq_of['attempt'] = model.seq_of['auth-0001']
        self.assertEqual(model.steps_this_round(), 2)
        del model.seq_of['evidence']
        with self.assertRaises(KeyError):
            model.steps_this_round()

    def test_reformulations_this_round_separates_layer_and_round_budget(self):
        self.assertEqual(self._memory_graph().reformulations_this_round(2), 0)
        model = self._memory_graph([('old', 'req', 2, {'reformulates': 'old-escalation'}),
            ('auth-0001', 'auth', 0, {'decision': 'revise'}),
            ('plain', 'req', 2, {}), ('different-layer', 'req', 3, {'reformulates': 'esc-3'}),
            ('current', 'req', 2, {'reformulates': 'esc-2'})])
        self.assertEqual(model.reformulations_this_round(2), 1)
        self.assertEqual(model.reformulations_this_round(4), 0)
        del model.nodes['current']['layer']
        with self.assertRaises(KeyError):
            model.reformulations_this_round(2)

    def test_esc_open_closes_on_relay_resolution_or_reformulation(self):
        rows = [('escalation', 'esc', 2, {}), ('upward', 'esc', 1, {})]
        self.assertTrue(self._memory_graph(rows).esc_open('escalation'))
        model=self._memory_graph(rows,[('escalation','escalates','upward')])
        self.assertFalse(model.esc_open('escalation'))
        resolved=self._memory_graph([('escalation','esc',1,{}),('auth-0001','auth',0,{})],
                                    [('escalation','resolved_by','auth-0001')])
        self.assertFalse(resolved.esc_open('escalation'))
        model = self._memory_graph(rows + [('new-req', 'req', 2, {'reformulates': 'escalation'})])
        self.assertFalse(model.esc_open('escalation'))

    def test_esc_chain_follows_relays_to_conflicts_and_rejects_missing_nodes(self):
        model = self._memory_graph([('conflict', 'conf', 3, {}), ('lower', 'esc', 3, {}), ('upper', 'esc', 2, {})],
            [('conflict', 'escalates', 'lower'), ('lower', 'escalates', 'upper')])
        self.assertEqual(model.esc_chain('conflict'), ([], ['conflict']))
        self.assertEqual(model.esc_chain('upper'), (['upper', 'lower'], ['conflict']))
        with self.assertRaises(KeyError):
            model.esc_chain('absent')

    def test_origin_req_traces_evidence_conflict_and_escalation_without_inventing_origin(self):
        rows = [('requirement', 'req', 2, {}), ('contract', 'ctr', 2, {}),
            ('fragment', 'frag', 3, {}), ('conflict', 'conf', 3, {}),
            ('escalation', 'esc', 3, {}), ('evidence', 'evd', 3, {}), ('unrelated', 'intent', 1, {})]
        edges = [('requirement', 'derives', 'contract'), ('contract', 'requests', 'fragment'),
            ('fragment', 'may_create', 'conflict'), ('conflict', 'escalates', 'escalation'),
            ('evidence', 'supports', 'fragment')]
        model = self._memory_graph(rows, edges)
        for node in ('requirement', 'fragment', 'conflict', 'escalation', 'evidence'):
            self.assertEqual(model.origin_req(node), 'requirement')
        self.assertIsNone(model.origin_req('unrelated'))
        with self.assertRaises(KeyError):
            model.origin_req('absent')

    def test_ancestry_includes_prior_formulation_and_parent_then_stops_on_cycle_or_gap(self):
        rows = [('parent', 'req', 1, {}), ('contract', 'ctr', 1, {}),
                ('earlier', 'req', 2, {}), ('newest', 'req', 2, {})]
        edges = [('parent', 'derives', 'contract'), ('contract', 'refines', 'earlier'),
                 ('earlier', 'refines', 'newest')]
        model = self._memory_graph(rows, edges)
        self.assertEqual(model.ancestry('parent'), ['parent'])
        self.assertEqual(model.ancestry('newest'), ['newest', 'earlier', 'parent'])
        self.assertEqual(self._memory_graph(rows, [('contract', 'refines', 'earlier')]).ancestry('earlier'), ['earlier'])
        # A persisted causal cycle now fails at the authoritative write boundary.
        cycle = self._memory_graph(rows, [('earlier', 'refines', 'newest')])
        before=Path(fabric.log_path(cycle.eng)).read_bytes()
        with self.assertRaises((ValueError,fabric.FabricError)):
            cycle.add_edge('newest','refines','earlier')
        self.assertEqual(Path(fabric.log_path(cycle.eng)).read_bytes(),before)

    def test_owned_formulation_is_at_escalating_layer_and_missing_owner_stays_missing(self):
        rows = [('parent', 'req', 1, {}), ('parent-contract', 'ctr', 1, {}), ('local', 'req', 2, {}),
            ('contract', 'ctr', 2, {}), ('fragment', 'frag', 3, {}), ('conflict', 'conf', 3, {}),
            ('leaf-escalation', 'esc', 3, {}), ('local-escalation', 'esc', 2, {}),
            ('top-escalation', 'esc', 1, {}), ('orphan', 'esc', 4, {})]
        edges = [('parent', 'derives', 'parent-contract'), ('parent-contract', 'refines', 'local'),
            ('local', 'derives', 'contract'), ('contract', 'requests', 'fragment'),
            ('fragment', 'may_create', 'conflict'), ('conflict', 'escalates', 'leaf-escalation'),
            ('leaf-escalation', 'escalates', 'local-escalation'),
            ('local-escalation', 'escalates', 'top-escalation')]
        model = self._memory_graph(rows, edges)
        self.assertEqual(model.owned_formulation('local-escalation'), 'local')
        self.assertEqual(model.owned_formulation('top-escalation'), 'parent')
        self.assertIsNone(model.owned_formulation('orphan'))
        with self.assertRaises(KeyError):
            model.owned_formulation('absent')

    def test_latest_review_uses_governed_exact_selection_instead_of_chronology(self):
        rows = [('fragment', 'frag', 3, {})]
        self.assertIsNone(self._memory_graph(rows).latest_review('fragment'))
        model = self._memory_graph(rows)
        for name,layer in [('same-layer',3),('higher-old',2),('higher-new',2)]:
            model.append('node',{'id':name,'type':'rev','layer':layer,'text':'Independent fixture review',
                                 'subject':model.nodes['fragment']['version_id'],'state':'accepts'})
            if layer==2:model.add_edge('fragment','reviewed_by',name)
        self.assertIsNone(model.latest_review('fragment'))
        directory=Path(fabric.FABRIC_DIR)
        with pytest.MonkeyPatch.context() as isolated:
            signer=SyntheticOperator(directory,isolated)
            spec={'scope':'default','reason':'Select exact independent review', 'proposed':[],
                  'selections':[],'reinstatements':[],'invalidations':[],'verification':[],
                  'allowed_verification_path':'synthetic-check',
                  'proofs':[{'subject':model.nodes['fragment']['version_id'],'role':'reviewer',
                             'proof':model.nodes['higher-old']['version_id']}]}
            spec_path=directory/'proof-selection.json';spec_path.write_text(json.dumps(spec))
            request_path=directory/'proof-request.json'
            fabric.cmd_lifecycle_plan(Namespace(engagement=model.eng,spec=str(spec_path),out=str(request_path)))
            signer.apply(fabric,request_path)
            model=fabric.open_fabric(model.eng)
            self.assertEqual(model.latest_review('fragment'),'higher-old')
            del model.nodes['higher-old']
            self.assertIsNone(model.latest_review('fragment'))

    def test_supervision_policy_normal_and_missing_invalid_empty_rules(self):
        self.assertEqual(fabric.supervision_policy()['schema'], 1)
        with tempfile.TemporaryDirectory() as directory:
            policy = Path(directory) / 'policy.json'
            with patch.object(fabric, 'POLICY_PATH', str(policy)):
                with self.assertRaises(fabric.FabricError):
                    fabric.supervision_policy()
                for value in ('{', json.dumps({'schema': 1, 'rules': []}), json.dumps({'schema': 2, 'rules': [{}]})):
                    policy.write_text(value)
                    with self.assertRaises(fabric.FabricError):
                        fabric.supervision_policy()

    def test_failure_class_retry_contradiction_and_unclassified(self):
        policy = fabric.supervision_policy()
        for state in policy['failure_classes']['retryable']:
            self.assertEqual(fabric.failure_class(state), 'retryable')
        for state in policy['failure_classes']['contradictory']:
            self.assertEqual(fabric.failure_class(state), 'contradictory')
        for state in ('', 'unknown'):
            with self.assertRaises(fabric.FabricError):
                fabric.failure_class(state)

    def test_norm_text_empty_whitespace_unicode_and_conversion_failure(self):
        self.assertEqual(fabric.norm_text('  An\tExample\n'), 'an example')
        self.assertEqual(fabric.norm_text(' \n\t'), '')
        self.assertEqual(fabric.norm_text('CAFÉ'), 'café')
        self.assertEqual(fabric.norm_text(None), 'none')
        class InvalidText:
            def __str__(self):
                raise ValueError('unrepresentable')
        with self.assertRaises(ValueError):
            fabric.norm_text(InvalidText())

    def test_edge_layer_direction_adjacency_and_authority_boundaries(self):
        node = lambda kind, layer: {'type': kind, 'layer': layer}
        self.assertTrue(fabric.edge_layer_ok('requests', node('ctr', 2), node('frag', 3)))
        self.assertFalse(fabric.edge_layer_ok('requests', node('ctr', 2), node('frag', 4)))
        self.assertTrue(fabric.edge_layer_ok('reviewed_by', node('frag', 1), node('rev', 0)))
        self.assertFalse(fabric.edge_layer_ok('reviewed_by', node('frag', 2), node('rev', 0)))
        self.assertTrue(fabric.edge_layer_ok('resolved_by', node('esc', 1), node('auth', 0)))
        self.assertFalse(fabric.edge_layer_ok('resolved_by', node('esc', 2), node('auth', 0)))
        self.assertTrue(fabric.edge_layer_ok('supports', node('evd', 6), node('frag', 6)))
        self.assertFalse(fabric.edge_layer_ok('supports', node('evd', 6), node('frag', 5)))
        with self.assertRaises(KeyError):
            fabric.edge_layer_ok('requests', {}, node('frag', 3))

    def test_log_path_length_and_traversal_boundaries(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(fabric, 'FABRIC_DIR', directory):
            self.assertEqual(fabric.log_path('project'), str(Path(directory) / 'project.jsonl'))
            self.assertEqual(fabric.log_path('a' * 64), str(Path(directory) / ('a' * 64 + '.jsonl')))
            for engagement in ('', '.', '../escape', 'a/b', 'a\\b', 'a' * 65):
                with self.assertRaises(fabric.FabricError):
                    fabric.log_path(engagement)

    def test_load_missing_empty_unmarked_blank_lines_and_malformed_ledger_fail_closed(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(fabric, 'FABRIC_DIR', directory):
            with self.assertRaises(fabric.FabricError):
                fabric.load('fixture')
            path = Path(directory) / 'fixture.jsonl'
            for raw in ('',' \n','\n'+json.dumps({'seq':1})+'\n\n'):
                path.write_text(raw)
                with self.assertRaises(ValueError):
                    fabric.load('fixture')
            path.write_text('{')
            with self.assertRaises(json.JSONDecodeError):
                fabric.load('fixture')

    def test_local_authority_key_creation_denies_even_with_selftest_marker(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'authority.key'
            with patch.object(fabric, 'KEY_PATH', str(path)), patch.object(fabric, 'FABRIC_DIR', str(Path(directory) / 'fab')), patch.object(fabric, '_SELFTEST_AUTHORITY_ROOT', directory):
                with self.assertRaises(fabric.FabricError):
                    fabric.authority_key(create=False)
                with self.assertRaises(fabric.FabricError):
                    fabric.authority_key()
                self.assertFalse(path.exists())

    def test_authority_persistence_and_keygen_default_deny_before_effect(self):
        from argparse import Namespace
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with patch.object(fabric, 'FABRIC_DIR', str(root / 'fab')), patch.object(fabric, 'KEY_PATH', str(root / 'authority.key')), patch.object(fabric, '_SELFTEST_AUTHORITY_ROOT', None):
                ledger = fabric.Fabric('fixture', [])
                node = {'id': 'auth-0001', 'type': 'auth', 'layer': 0, 'decision': 'exception'}
                attempts = [lambda: ledger.append('node', node),
                            lambda: ledger.append('node', node, sign=True),
                            lambda: ledger.append('node', {'id': 'req-1', 'layer': 1}, sign=True),
                            lambda: ledger.append('node', {**node, 'layer': 1}),
                            lambda: ledger.add_node('req', 1, type='auth'),
                            lambda: ledger.add_node('req', 1, layer_override=0, id='auth-evil'),
                            lambda: ledger.add_node('auth', 0, decision='exception'),
                            lambda: ledger.add_node('auth', 0, sign=True, decision='exception'),
                            lambda: fabric.authority_key(create=True),
                            lambda: fabric.cmd_keygen(Namespace())]
                ledger.nodes['auth-0001'] = node
                ledger.nodes['esc-0001'] = {'id': 'esc-0001', 'type': 'esc', 'layer': 1}
                attempts.append(lambda: ledger.add_edge('esc-0001', 'resolved_by', 'auth-0001'))
                for attempt in attempts:
                    with self.assertRaises(fabric.FabricError):
                        attempt()
                    self.assertEqual(ledger.entries, [])
                    self.assertEqual(list(root.iterdir()), [])

    def test_hook_filename_detection_does_not_grant_authority(self):
        with tempfile.TemporaryDirectory() as directory, patch.dict(os.environ, {'CLAUDE_HOME': directory}), patch.object(fabric.os, 'getcwd', return_value=directory):
            self.assertFalse(fabric.confirmation_gate_active())
            settings = Path(directory) / 'settings.json'
            settings.write_text('{}')
            self.assertFalse(fabric.confirmation_gate_active())
            settings.write_text(json.dumps({'hook': 'guard_authority.py'}))
            self.assertTrue(fabric.confirmation_gate_active())
            with self.assertRaises(fabric.FabricError):
                fabric.require_human('untrusted hook filename')

    def test_next_id_is_separate_per_node_type_and_increases(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(fabric, 'FABRIC_DIR', directory):
            ledger = fabric.Fabric('fixture', [])
            self.assertEqual(ledger.next_id('req'), 'req-0001')
            self.assertEqual(ledger.next_id('frag'), 'frag-0001')
            ledger.add_node('req', 1, 'First requirement')
            self.assertEqual(ledger.next_id('req'), 'req-0002')
            self.assertEqual(ledger.next_id('frag'), 'frag-0001')
            with self.assertRaises(fabric.FabricError):
                ledger.add_node('unknown', 1)
            self.assertEqual(ledger.next_id('req'), 'req-0002')

    def test_flush_commits_complete_batch_and_rejects_a_concurrent_head(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(fabric,'FABRIC_DIR',directory):
            empty=fabric.Fabric('empty',[])
            empty.flush()
            self.assertFalse(Path(fabric.log_path('empty')).exists())
            with patch.object(fabric,'_COMMAND_FABRICS',[]):
                graph=fabric.Fabric('batch',[])
                graph.add_node('req',1,'First member')
                graph.add_node('req',1,'Second member')
                self.assertFalse(Path(fabric.log_path('batch')).exists())
                graph.flush()
                self.assertEqual(len(fabric.load('batch')),1)
                self.assertEqual(len(fabric.Fabric('batch',fabric.load('batch')).nodes),2)
                self.assertEqual(graph.pending,[])
                stale=fabric.Fabric('batch',fabric.load('batch'))
                graph.add_node('req',1,'Winning update')
                stale.add_node('req',1,'Stale competing update')
                graph.flush()
                committed=Path(fabric.log_path('batch')).read_bytes()
                with self.assertRaises(ValueError):
                    stale.flush()
                self.assertEqual(Path(fabric.log_path('batch')).read_bytes(),committed)
                self.assertTrue(stale.pending)

    def test_verify_integrity_accepts_fresh_transactions_and_rejects_semantic_tamper(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(fabric,'FABRIC_DIR',directory):
            graph=fabric.Fabric('integrity',[])
            graph.add_node('req',1,'Exact immutable subject')
            state=graph.verify_integrity()
            self.assertTrue(state.initialized)
            self.assertEqual(set(state.graph_ids),set(graph.nodes))
            before=Path(fabric.log_path('integrity')).read_bytes()
            graph.transactions[-1]['operations'][-1]['data']['text']='Substituted subject'
            with self.assertRaises(ValueError):
                graph.verify_integrity()
            self.assertEqual(Path(fabric.log_path('integrity')).read_bytes(),before)

    def test_round_start_tracks_latest_revision_and_ignores_other_decisions(self):
        self.assertEqual(self._memory_graph().round_start(),0)
        rows=[]
        latest=None
        for number,decision in enumerate(('exception','revise','reject','revise'),1):
            identifier='auth-'+str(number).zfill(4)
            rows.append((identifier,'auth',0,{'decision':decision}))
            ledger=self._memory_graph(rows)
            if decision=='revise':latest=identifier
            self.assertEqual(ledger.round_start(),ledger.seq_of[latest] if latest else 0)


class FabricReleaseSecurityTests(unittest.TestCase):
    """Exercise each previously unmapped function against disposable actual models."""
    _memory_graph = FabricHelperTests._memory_graph

    def setUp(self):
        from argparse import Namespace
        from contextlib import ExitStack
        self.ns = Namespace
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.scope = ExitStack()
        self.addCleanup(self.scope.close)
        self.scope.enter_context(patch.object(fabric, 'FABRIC_DIR', self.temp.name))
        self.scope.enter_context(patch.object(fabric, 'KEY_PATH', self.temp.name + '/synthetic.key'))
        self.scope.enter_context(patch.object(fabric, '_SELFTEST_AUTHORITY_ROOT', None))
        self.fb = fabric.Fabric('case', [])
        self.scope.enter_context(patch.object(fabric, 'open_fabric', return_value=self.fb))

    def invoke(self, function, **values):
        import io
        from contextlib import redirect_stdout
        output = io.StringIO()
        with redirect_stdout(output):
            result = function(self.ns(engagement='case', **values))
        return result, output.getvalue()

    def missing(self, function, **values):
        before = list(self.fb.entries)
        with self.assertRaises(fabric.FabricError):
            self.invoke(function, **values)
        self.assertEqual(self.fb.entries, before)

    def test_support_graph(self):
        model = self._memory_graph([('f', 'frag', 2, {}), ('e', 'evd', 2, {})], [('e', 'supports', 'f')])
        self.assertEqual(model.support_graph('f'), {'f', 'e'})
        self.assertEqual(model.support_graph('absent'), {'absent'})

    def test_conflicts_of(self):
        model = self._memory_graph([('f', 'frag', 2, {}), ('c', 'conf', 2, {})], [('f', 'may_create', 'c')])
        self.assertEqual(model.conflicts_of('f'), {'c'})
        self.assertEqual(model.conflicts_of('absent'), set())

    def test_resolution(self):
        model = self._memory_graph([('c', 'conf', 1, {}), ('x', 'esc', 1, {}), ('auth-0001', 'auth', 0, {})], [('c', 'escalates', 'x'), ('x', 'resolved_by', 'auth-0001')])
        self.assertEqual(model.resolution('c')['id'], 'auth-0001')
        self.assertIsNone(model.resolution('absent'))

    def test_justify(self):
        node = self.fb.add_node('frag', 2, 'unreviewed')
        for strict in (False, True):
            ok, reasons = self.fb.justify(node['id'], strict=strict)
            self.assertFalse(ok)
            self.assertTrue(reasons)

    def test_check_contract_budget(self):
        fabric.check_contract_budget(self.fb, fabric.MAX_CONTRACTS)
        with self.assertRaises(fabric.FabricError):
            fabric.check_contract_budget(self.fb, fabric.MAX_CONTRACTS + 1)
        self.assertFalse(self.fb.entries)
        model = self._memory_graph([('spent-1', 'ctr', 1, {}), ('spent-2', 'ctr', 2, {})])
        before = json.dumps(model.entries, sort_keys=True)
        fabric.check_contract_budget(model, fabric.MAX_CONTRACTS - 2)
        with self.assertRaisesRegex(fabric.FabricError, 'contract budget'):
            fabric.check_contract_budget(model, fabric.MAX_CONTRACTS - 1)
        self.assertEqual(json.dumps(model.entries, sort_keys=True), before)

    def test_check_contract_budget_resets_only_after_governed_revision(self):
        model = self._memory_graph([('spent', 'ctr', 1, {}),
            ('auth-0001', 'auth', 0, {'decision': 'revise'}), ('current', 'ctr', 1, {})])
        before = json.dumps(model.entries, sort_keys=True)
        fabric.check_contract_budget(model, fabric.MAX_CONTRACTS - 1)
        with self.assertRaisesRegex(fabric.FabricError, 'contract budget'):
            fabric.check_contract_budget(model, fabric.MAX_CONTRACTS)
        self.assertEqual(json.dumps(model.entries, sort_keys=True), before)

    def test_check_episode_budget(self):
        fabric.check_episode_budget(self.fb, fabric.MAX_STEPS)
        with self.assertRaises(fabric.FabricError):
            fabric.check_episode_budget(self.fb, fabric.MAX_STEPS + 1)
        self.assertFalse(self.fb.entries)

    def test_engagement_protocol(self):
        self.assertEqual(fabric.engagement_protocol(self.fb), '3.2')
        self.fb.add_node('intent', 1, 'intent', protocol='3.1')
        self.assertEqual(fabric.engagement_protocol(self.fb), '3.1')

    def contract(self):
        r = self.fb.add_node('req', 1, 'public requirement')
        c = self.fb.add_node('ctr', 1, 'bounded contract', target_layer=2,
                             fields={key: 'fixture ' + key for key in fabric.CONTRACT_FIELDS})
        self.fb.add_edge(r['id'], 'derives', c['id'])
        return c

    def test_cmd_render(self):
        self.missing(fabric.cmd_render, contract='missing')
        c = self.contract()
        _, output = self.invoke(fabric.cmd_render, contract=c['id'])
        self.assertIn(fabric.contract_context_packet(self.fb, c)[1], output)
        self.assertIn('fixture sanitise', output)

    def test_cmd_packet(self):
        self.missing(fabric.cmd_packet, contract='missing')
        c = self.contract()
        packet = json.loads(self.invoke(fabric.cmd_packet, contract=c['id'])[1])
        self.assertEqual(packet['context_digest'], fabric.contract_context_packet(self.fb, c)[1])
        self.assertEqual(packet['packet']['fields'], c['fields'])

    def test_cmd_failure(self):
        self.missing(fabric.cmd_failure, contract='missing')
        c = self.contract()
        status, output = self.invoke(fabric.cmd_failure, contract=c['id'], reason='fixture timeout', state='timeout', actor='worker', model='fixture')
        self.assertEqual(status, 0)
        self.assertIn('local repair', output)
        self.assertEqual(sum(n['type'] == 'att' for n in self.fb.nodes.values()), 1)

    def test_cmd_policy(self):
        _, output = self.invoke(fabric.cmd_policy)
        self.assertEqual(json.loads(output), fabric.supervision_policy())
        self.assertFalse(self.fb.entries)

    def test_cmd_invalidate(self):
        self.missing(fabric.cmd_invalidate, changed='missing', reason='changed')
        node = self.fb.add_node('req', 1, 'no dependents')
        before = list(self.fb.entries)
        request=Path(self.temp.name)/'invalidation-request.json'
        self.invoke(fabric.cmd_invalidate, changed=node['id'], reason='changed',request_out=str(request))
        self.assertEqual(self.fb.entries, before)
        plan=json.loads(request.read_text())
        self.assertEqual(plan['kind'],'lifecycle-update')
        self.assertIn(node['version_id'],plan['parameters']['effects']['affected'])
        self.assertEqual(self.fb.lifecycle.states[node['version_id']]['validity'],'pending')

    def test_cmd_answer(self):
        self.missing(fabric.cmd_answer, requirement='missing')
        node = self.fb.add_node('req', 1, 'requirement')
        self.missing(fabric.cmd_answer, requirement=node['id'], supported_by=['forged'], text='product')
        child = self.fb.add_node('frag', 2, 'qualified child')
        review = self.fb.add_node('rev', 1, 'evidence reviewed', state='accepts')
        self.fb.add_edge(child['id'], 'reviewed_by', review['id'])
        self.missing(fabric.cmd_answer, requirement=node['id'], supported_by=[child['id']], text='product')
        products = [n for n in self.fb.nodes.values() if n.get('kind') == 'product']
        self.assertEqual(products, [])

    def test_cmd_release(self):
        node = self.fb.add_node('frag', 1, 'unqualified product')
        status, output = self.invoke(fabric.cmd_release, fragment=node['id'])
        self.assertEqual(status, 1)
        self.assertIn('NOT', output)

    def test_cmd_render_review(self):
        self.missing(fabric.cmd_render_review, contract='missing')
        c = self.contract()
        _, output = self.invoke(fabric.cmd_render_review, contract=c['id'])
        self.assertIn('fixture evidence', output)
        self.assertIn('no evidence', output)

    def test_cmd_ingest_reviews(self):
        path = Path(self.temp.name) / 'reviews.json'
        path.write_text(json.dumps({'reviews': [{'fragment': 'forged', 'state': 'accepts'}]}))
        self.missing(fabric.cmd_ingest_reviews, result=str(path), layer=0, reviewer='agent', model='fixture')
        path.write_text(json.dumps({'reviews': [], 'authority': 'forged'}))
        self.missing(fabric.cmd_ingest_reviews, result=str(path), layer=1, reviewer='agent', model='fixture')

    def test_cmd_dossier(self):
        self.missing(fabric.cmd_dossier, escalation='missing')
        self.fb.add_node('intent', 1, 'public fixture intent')
        x = self.fb.add_node('esc', 1, 'needs human', effective='outside_authority')
        before = list(self.fb.entries)
        _, output = self.invoke(fabric.cmd_dossier, escalation=x['id'], examples=1)
        self.assertIn('public fixture intent', output)
        self.assertIn('remain denied', output)
        self.assertEqual(self.fb.entries, before)

    def test_make_evidence(self):
        import hashlib
        path = Path(self.temp.name) / 'evidence.txt'
        path.write_bytes(b'exact evidence')
        node = fabric.make_evidence(self.fb, 6, 'fixture', 'deterministic', str(path))
        self.assertEqual(node['sha256'], hashlib.sha256(path.read_bytes()).hexdigest())
        before = list(self.fb.entries)
        for confidence, file in [('deterministic', None), ('forged', str(path)), ('observation', str(path) + '.missing')]:
            with self.assertRaises(fabric.FabricError):
                fabric.make_evidence(self.fb, 6, 'fixture', confidence, file)
        self.assertEqual(self.fb.entries, before)

    def test_cmd_evidence(self):
        self.invoke(fabric.cmd_evidence, layer=6, source='fixture', confidence='observation', file=None, supports=[], contradicts=[])
        self.assertEqual(len(self.fb.entries), 1)
        self.assertEqual(next(iter(self.fb.nodes.values()))['confidence'], 'observation')

    def test_cmd_consolidate(self):
        node = self.fb.add_node('frag', 2, 'fixture')
        self.missing(fabric.cmd_consolidate, fragment=node['id'], layer=1)
        for state in ('accepts', 'conflicts'):
            review = self.fb.add_node('rev', 1, 'independent rationale', state=state)
            self.fb.add_edge(node['id'], 'reviewed_by', review['id'])
        self.invoke(fabric.cmd_consolidate, fragment=node['id'], layer=1)
        review = next(value for value in self.fb.nodes.values() if value.get('consolidated'))
        self.assertEqual(review['state'], 'conflicts')
        self.assertIsNone(self.fb.latest_review(node['id']))
        self.assertTrue(self.fb.conflicts_of(node['id']))

    def test_cmd_conflict(self):
        node = self.fb.add_node('frag', 2, 'fixture')
        self.invoke(fabric.cmd_conflict, layer=2, text='cannot meet contract', **{'from': node['id']})
        self.assertEqual(len(self.fb.conflicts_of(node['id'])), 1)
        self.assertFalse(self.fb.justify(node['id'])[0])

    def test_escalate_one(self):
        node = self.fb.add_node('conf', 2, 'outside authority')
        x = fabric.escalate_one(self.fb, node['id'], 2, 'outside_authority', 'must relay')
        before = list(self.fb.entries)
        with self.assertRaises(fabric.FabricError):
            fabric.escalate_one(self.fb, x['id'], 1, 'exhausted', 'downgrade')
        self.assertEqual(self.fb.entries, before)
        relayed = fabric.escalate_one(self.fb, x['id'], 1, 'relay', 'operator')
        self.assertEqual(relayed['effective'], 'outside_authority')

    def test_cmd_escalate(self):
        node = self.fb.add_node('conf', 2, 'fixture')
        status, output = self.invoke(fabric.cmd_escalate, **{'from': node['id']}, to_top=True, code='outside_authority', reason='operator', layer=None)
        self.assertEqual(status, 0)
        self.assertIn('stop', output)
        self.assertEqual(sorted(n['layer'] for n in self.fb.nodes.values() if n['type'] == 'esc'), [1, 2])
        self.assertFalse(any(n['layer'] == 0 for n in self.fb.nodes.values()))

    def test_next_action(self):
        x = self.fb.add_node('esc', 1, 'operator', effective='outside_authority')
        allowed, why = fabric.next_action(self.fb, x['id'])
        self.assertFalse(allowed)
        self.assertIn('authority', why)

    def test_cmd_propose(self):
        self.missing(fabric.cmd_propose, requirement='missing')
        r = self.fb.add_node('req', 1, 'original')
        self.invoke(fabric.cmd_propose, requirement=r['id'], text='alternative', tradeoff='reduced scope')
        proposals = [n for n in self.fb.nodes.values() if n.get('kind') == 'reformulation']
        self.assertEqual(len(proposals), 1)
        self.assertEqual(self.fb.nodes[r['id']]['text'], 'original')
        self.assertEqual(proposals[0]['tradeoff'], 'reduced scope')

    def test_cmd_reformulate(self):
        self.missing(fabric.cmd_reformulate, escalation='missing')
        x = self.fb.add_node('esc', 1, 'operator', effective='outside_authority')
        self.missing(fabric.cmd_reformulate, escalation=x['id'])

    def test_cmd_authorise(self):
        self.missing(fabric.cmd_authorise)
        self.assertFalse(Path(fabric.KEY_PATH).exists())

    def test_cmd_keygen(self):
        self.missing(fabric.cmd_keygen)
        self.assertFalse(Path(fabric.KEY_PATH).exists())

    def test_persisted_node_identity_is_immutable_and_replayed_duplicates_block(self):
        import copy
        node = self.fb.add_node('req', 1, 'reviewed original')
        before = copy.deepcopy(self.fb.entries)
        original_bytes = Path(fabric.log_path('case')).read_bytes()
        for identifier in (node['id'], '', None, '   ', '\x00', 'x' * 257):
            with self.assertRaises(fabric.FabricError):
                self.fb.append('node', {**node, 'id': identifier, 'text': 'substitution'})
            self.assertEqual(self.fb.entries, before)
            self.assertEqual(self.fb.nodes[node['id']]['text'], 'reviewed original')
            self.assertEqual(Path(fabric.log_path('case')).read_bytes(), original_bytes)
        transactions=copy.deepcopy(self.fb.transactions)
        duplicate=fabric.lifecycle.envelope('case',transactions[-1]['hash'],len(transactions)+1,
            [{'op':'node','data':copy.deepcopy(node)}])
        with self.assertRaises(ValueError):
            fabric.Fabric('case',transactions+[duplicate])
        self.assertEqual(Path(fabric.log_path('case')).read_bytes(),original_bytes)

    def test_historical_opaque_node_identity_remains_accepted_and_unique(self):
        node = {'id': 'req-historical-opaque', 'type': 'req', 'layer': 1, 'text': 'historical subject'}
        self.fb.append('node', node)
        self.assertEqual(self.fb.verify(), ([], []))
        self.assertEqual(self.fb.nodes[node['id']], node)
        before = Path(fabric.log_path('case')).read_bytes()
        with self.assertRaises(fabric.FabricError):
            self.fb.append('node', {**node, 'text': 'substitution'})
        self.assertEqual(Path(fabric.log_path('case')).read_bytes(), before)

    def test_cmd_verify(self):
        self.assertEqual(self.invoke(fabric.cmd_verify)[0], 0)
        self.fb.add_node('req', 1, 'original')
        self.fb.transactions[-1]['operations'][-1]['data']['text'] = 'tampered'
        self.assertEqual(self.invoke(fabric.cmd_verify)[0], 1)

    def test_cmd_justify(self):
        node = self.fb.add_node('frag', 2, 'unqualified')
        status, output = self.invoke(fabric.cmd_justify, fragment=node['id'], strict=True, json=True)
        self.assertEqual(status, 1)
        self.assertFalse(json.loads(output)[0]['justifiable'])

    def test_cmd_status(self):
        self.fb.add_node('frag', 2, 'unreviewed')
        before = list(self.fb.entries)
        _, output = self.invoke(fabric.cmd_status)
        self.assertIn('unreviewed=1', output)
        self.assertEqual(self.fb.entries, before)

    def test_cmd_report(self):
        self.fb.add_node('intent', 1, 'public fixture', owner='fixture')
        self.fb.add_node('frag', 2, 'table | value')
        before = list(self.fb.entries)
        _, output = self.invoke(fabric.cmd_report)
        self.assertIn(r'table \| value', output)
        self.assertIn('public fixture', output)
        self.assertEqual(self.fb.entries, before)


if __name__ == '__main__':
    unittest.main()
