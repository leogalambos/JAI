# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Lifecycle semantics and secure atomic persistence use disposable state only."""
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / '.ai/runtime/tools'))
import lifecycle as lc


class LifecycleTests(unittest.TestCase):
    def test_canonical_unicode_collision_types_and_order(self):
        self.assertEqual(lc.normal('e\u0301'), 'é')
        self.assertEqual(lc.canonical({'é': '  A  '}), lc.canonical({'e\u0301': '  A  '}))
        self.assertNotEqual(lc.canonical([1, 2]), lc.canonical([2, 1]))
        for value in (1.5, float('nan'), {'é': 1, 'e\u0301': 2}, {1: 'bad'}):
            with self.assertRaises(lc.LifecycleError):
                lc.canonical(value)
        for raw in ('{"a":1,"a":2}', '{"é":1,"e\\u0301":2}', '1.5', 'NaN'):
            with self.assertRaises(lc.LifecycleError):
                lc.loads(raw)
        self.assertEqual(lc.loads('{}'), {})

    def test_identity_composite_and_distinct_conclusions(self):
        a = {'role': 'source', 'logical_id': 'a', 'version_id': 'v1'}
        b = {'role': 'source', 'logical_id': 'b', 'version_id': 'v2'}
        first = lc.manifest('subject', 'conclusion', {'text': 'x'}, members=[a, b])
        self.assertEqual(lc.version_id(first), lc.version_id(lc.manifest('subject', 'conclusion', {'text': 'x'}, members=[b, a])))
        self.assertNotEqual(lc.version_id(first), lc.version_id(lc.manifest('other', 'conclusion', {'text': 'x'}, members=[a, b])))
        self.assertNotEqual(lc.blob(b''), lc.blob(b' '))
        with self.assertRaises(lc.LifecycleError):
            lc.manifest('subject', 'conclusion', {}, members=[a, a])

    def fixture(self):
        state = lc.State()
        state.apply({'op': 'init', 'data': {'policy': lc.policy(), 'scope': 'default'}})
        def add(name):
            manifest = lc.manifest(name, 'source', {'text': name})
            version = lc.version_id(manifest)
            state.apply({'op': 'version', 'data': {'version_id': version, 'manifest': manifest}})
            state.apply({'op': 'select', 'data': {'scope': 'default', 'logical_id': name, 'version_id': version, 'previous': None}})
            return version
        return state, add

    def test_states_are_independent_and_reliance_is_acyclic(self):
        state, add = self.fixture()
        a, b, unrelated = add('a'), add('b'), add('unrelated')
        state.apply({'op': 'state', 'data': {'version_id': a, 'scope': 'default', 'changes': {'sufficient': True}}}, authorized=True)
        self.assertEqual(state.states[a]['validity'], 'pending')
        self.assertFalse(state.states[a]['reviewed'])
        state.apply({'op': 'rely', 'data': {'dependent': b, 'prerequisite': a, 'scope': 'other', 'prerequisite_scope': 'default', 'role': 'source'}})
        self.assertEqual(state.affected([a]), sorted([a, b]))
        self.assertNotIn(unrelated, state.affected([a]))
        state.check_cycles()
        state.apply({'op': 'rely', 'data': {'dependent': a, 'prerequisite': b, 'scope': 'default', 'prerequisite_scope': 'other', 'role': 'source'}})
        with self.assertRaises(lc.LifecycleError):
            state.check_cycles()

    def test_empty_dependencies_cannot_justify_conclusion(self):
        state, add = self.fixture()
        value = lc.manifest('claim', 'conclusion', {'text': 'PASS'})
        version = lc.version_id(value)
        state.apply({'op': 'version', 'data': {'version_id': version, 'manifest': value}})
        self.assertFalse(state.evaluate(version)['eligible'])

    def test_effects_cancel_complete_cross_scope_dependents_and_retain_other_branch(self):
        state, add = self.fixture()
        old, dependent, unrelated = add('source'), add('dependent'), add('unrelated')
        state.apply({'op': 'rely', 'data': {'dependent': dependent, 'prerequisite': old, 'scope': 'other', 'prerequisite_scope': 'default', 'role': 'source'}})
        replacement = lc.manifest('source', 'source', {'text': 'updated'})
        spec = {'scope': 'default', 'reason': 'verified source changed',
                'proposed': [{'manifest': replacement}],
                'selections': [{'logical_id': 'source', 'version_id': lc.version_id(replacement)}],
                'reinstatements': [], 'verification': [], 'invalidations': [], 'proofs': [],
                'allowed_verification_path': 'fresh-check'}
        effects = state.effects(spec)
        self.assertEqual(effects['affected'], sorted([old, dependent]))
        self.assertNotIn(unrelated, effects['affected'])
        for operation in effects['operations']:
            state.apply(operation, authorized=True)
        self.assertEqual(state.predicates(dependent, 'other')['validity'], 'invalid')
        self.assertEqual(state.states[lc.version_id(replacement)]['validity'], 'pending')
        with self.assertRaises(lc.LifecycleError):
            state.effects({**spec, 'unknown': True})

    def test_scoped_replacement_preserves_old_input_in_unrelated_scope_and_cancels_explicit_cross_scope_dependents(self):
        state, add = self.fixture()
        old, dependent = add('source'), add('dependent')
        policy_version = state.selections[('default', 'lifecycle-policy')]
        for logical, identifier in (('source', old), ('lifecycle-policy', policy_version)):
            state.apply({'op': 'select', 'data': {'scope': 'retained', 'logical_id': logical,
                         'version_id': identifier, 'previous': None}}, authorized=True)
            state.apply({'op': 'state', 'data': {'scope': 'retained', 'version_id': identifier,
                         'changes': {'validity': 'valid', 'applicable': True}}}, authorized=True)
        state.apply({'op': 'rely', 'data': {'dependent': dependent, 'prerequisite': old,
                     'scope': 'cross', 'prerequisite_scope': 'default', 'role': 'source'}})
        self.assertTrue(state.evaluate(old, scope='retained')['eligible'])
        points = state.affected_contexts([old], 'default')
        self.assertIn({'scope': 'cross', 'version_id': dependent}, points)
        self.assertNotIn({'scope': 'retained', 'version_id': old}, points)
        replacement = lc.manifest('source', 'source', {'text': 'changed source'})
        spec = {'scope': 'default', 'reason': 'Scoped change', 'proposed': [{'manifest': replacement}],
                'selections': [{'logical_id': 'source', 'version_id': lc.version_id(replacement)}],
                'reinstatements': [], 'invalidations': [], 'proofs': [], 'verification': [],
                'allowed_verification_path': 'fresh-check'}
        for operation in state.effects(spec)['operations']:
            state.apply(operation, authorized=True)
        self.assertEqual(state.predicates(old, 'default')['validity'], 'invalid')
        self.assertEqual(state.predicates(old, 'retained')['validity'], 'valid')
        self.assertEqual(state.predicates(dependent, 'cross')['validity'], 'invalid')
        self.assertTrue(state.evaluate(old, scope='retained')['eligible'])

    def test_transaction_replay_unknown_operations_and_archive_rejected(self):
        init = {'op': 'init', 'data': {'scope': 'default', 'policy': lc.policy()}}
        tx = lc.envelope('case', lc.ZERO, 1, [init])
        self.assertTrue(lc.replay([tx], 'case').initialized)
        with self.assertRaises(lc.LifecycleError):
            lc.replay([{'op': 'node', 'data': {}}])
        repeated = lc.envelope('case', tx['hash'], 2, [{'op': 'locate', 'data': {}}], transaction_id=tx['transaction_id'])
        with self.assertRaises(lc.LifecycleError):
            lc.replay([tx, repeated], 'case')
        bad = lc.envelope('case', tx['hash'], 2, [{'op': 'unknown', 'data': {}}])
        with self.assertRaises(lc.LifecycleError):
            lc.replay([tx, bad], 'case')

    def test_commit_is_atomic_on_invalid_candidate_and_concurrent_head(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'case.jsonl'
            tx = lc.commit(path, 'case', lc.ZERO, [{'op': 'init', 'data': {'scope': 'default', 'policy': lc.policy()}}])
            before = path.read_bytes()
            self.assertEqual(lc.read(path, 'case'), [tx])
            for head, operations in ((lc.ZERO, [{'op': 'edge', 'data': {}}]), (tx['hash'], [{'op': 'unknown', 'data': {}}])):
                with self.assertRaises(lc.LifecycleError):
                    lc.commit(path, 'case', head, operations)
                self.assertEqual(path.read_bytes(), before)


if __name__ == '__main__':
    unittest.main()
