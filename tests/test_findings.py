# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Findings archive preserves event bytes and refuses unsafe or active inputs."""
from argparse import Namespace
import contextlib
import hashlib
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

TOOLS = Path(__file__).resolve().parents[1] / '.ai/runtime/tools'
sys.path.insert(0, str(TOOLS))
import findings


class FindingsArchiveTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.workspace = Path(self.temporary.name)
        previous = Path.cwd()
        os.chdir(self.workspace)
        self.addCleanup(os.chdir, previous)
        home = patch.object(findings, 'HOME', str(self.workspace / '.findings'))
        home.start()
        self.addCleanup(home.stop)

    def create_ledger(self, name='complete', complete=True):
        events = []
        findings.append(name, events, [{'op': 'add', 'reviewer': 'reviewer',
            'target': 'docs/', 'criteria': 'synthetic review criteria',
            'findings': [{'id': 'F-0001', 'title': 'Synthetic finding',
                'kind': 'defect', 'severity': 'low', 'location': 'docs/example.md:1',
                'criterion': 'accuracy', 'evidence': 'Synthetic test evidence',
                'recommendation': 'Correct the example'}]}])
        if complete:
            findings.append(name, events, [
                {'op': 'resolve', 'id': 'F-0001', 'by': 'author', 'note': 'Reworked'},
                {'op': 'verify', 'id': 'F-0001', 'by': 'reviewer', 'ok': True, 'note': 'Verified'}])
        return Path(findings.path(name))

    def archive(self, ledger='complete'):
        with contextlib.redirect_stdout(io.StringIO()):
            return findings.cmd_archive_private(Namespace(ledger=ledger, exclusive_maintenance=True))

    def test_exclusive_maintenance_confirmation_is_required_without_mutation(self):
        source = self.create_ledger()
        original = source.read_bytes()
        with self.assertRaisesRegex(findings.LedgerError, 'exclusive-maintenance'):
            findings.cmd_archive_private(Namespace(ledger='complete'))
        self.assertEqual(original, source.read_bytes())
        self.assertFalse((self.workspace / 'INBOX').exists())

    def test_source_replacement_at_move_is_restored_without_deleting_either_record(self):
        source = self.create_ledger()
        original = source.read_bytes()
        saved = self.workspace / 'original.jsonl'
        rename = findings._rename_noreplace
        calls = []
        def replace_before_move(source_dir, name, destination_dir):
            calls.append(name)
            if len(calls) == 1:
                source.rename(saved)
                source.write_bytes(b'Concurrent replacement')
            return rename(source_dir, name, destination_dir)
        with patch.object(findings, '_rename_noreplace', side_effect=replace_before_move):
            with self.assertRaises(findings.LedgerError):
                self.archive()
        self.assertEqual(original, saved.read_bytes())
        self.assertEqual(b'Concurrent replacement', source.read_bytes())
        self.assertFalse((self.workspace / 'INBOX/private-audit/complete.jsonl').exists())
        self.assertEqual(2, len(calls))

    def test_restoration_collision_preserves_records_and_reports_maintenance_violation(self):
        source = self.create_ledger()
        original = source.read_bytes()
        saved = self.workspace / 'original.jsonl'
        rename = findings._rename_noreplace
        calls = []
        def collide_during_restoration(source_dir, name, destination_dir):
            calls.append(name)
            if len(calls) == 1:
                source.rename(saved)
                source.write_bytes(b'Replaced before move')
                rename(source_dir, name, destination_dir)
                source.write_bytes(b'New concurrent source')
                return
            return rename(source_dir, name, destination_dir)
        with patch.object(findings, '_rename_noreplace', side_effect=collide_during_restoration):
            with self.assertRaisesRegex(findings.LedgerError, 'maintenance violation'):
                self.archive()
        self.assertEqual(original, saved.read_bytes())
        self.assertEqual(b'New concurrent source', source.read_bytes())
        self.assertEqual(b'Replaced before move',
            (self.workspace / 'INBOX/private-audit/complete.jsonl').read_bytes())

    def test_successful_archive_never_unlinks_a_pathname(self):
        source = self.create_ledger()
        original = source.read_bytes()
        with patch.object(findings.os, 'unlink', side_effect=AssertionError('No pathname deletion permitted')):
            self.assertEqual(0, self.archive())
        self.assertFalse(source.exists())
        self.assertEqual(original, (self.workspace / 'INBOX/private-audit/complete.jsonl').read_bytes())

    def test_complete_ledger_retains_exact_bytes_hash_chain_and_load(self):
        source = self.create_ledger()
        source.write_bytes(source.read_bytes().replace(b'\n', b'\r\n'))
        original = source.read_bytes()
        events = findings.load('complete')
        self.assertEqual(0, self.archive())
        destination = self.workspace / 'INBOX/private-audit/complete.jsonl'
        self.assertFalse(source.exists())
        self.assertEqual(original, destination.read_bytes())
        self.assertEqual(hashlib.sha256(original).digest(), hashlib.sha256(destination.read_bytes()).digest())
        with patch.object(findings, 'HOME', str(destination.parent)):
            self.assertEqual(events, findings.load('complete'))
            self.assertEqual('verified', findings.state(findings.load('complete'))['F-0001']['state'])

    def test_active_ledger_rejected_before_creating_archive(self):
        source = self.create_ledger(complete=False)
        original = source.read_bytes()
        with self.assertRaisesRegex(findings.LedgerError, 'COMPLETE'):
            self.archive()
        self.assertEqual(original, source.read_bytes())
        self.assertFalse((self.workspace / 'INBOX').exists())

    def test_corrupt_hash_rejected_without_mutation(self):
        source = self.create_ledger()
        source.write_bytes(source.read_bytes().replace(b'Synthetic finding', b'Changed finding'))
        original = source.read_bytes()
        with self.assertRaises(findings.LedgerError):
            self.archive()
        self.assertEqual(original, source.read_bytes())
        self.assertFalse((self.workspace / 'INBOX').exists())

    def test_missing_empty_and_traversal_rejected(self):
        with self.assertRaises(findings.LedgerError):
            self.archive('missing')
        self.assertFalse((self.workspace / 'INBOX').exists())
        source = self.create_ledger()
        original = source.read_bytes()
        with self.assertRaises(findings.LedgerError):
            self.archive('../complete')
        self.assertEqual(original, source.read_bytes())
        source.write_bytes(b'')
        with self.assertRaisesRegex(findings.LedgerError, 'empty'):
            self.archive()
        self.assertEqual(b'', source.read_bytes())

    def test_destination_collision_never_overwrites_either_file(self):
        source = self.create_ledger()
        original = source.read_bytes()
        archive = self.workspace / 'INBOX/private-audit'
        archive.mkdir(parents=True)
        destination = archive / source.name
        destination.write_bytes(b'Existing archive content')
        with self.assertRaises(findings.LedgerError):
            self.archive()
        self.assertEqual(original, source.read_bytes())
        self.assertEqual(b'Existing archive content', destination.read_bytes())

    def test_source_symlink_is_rejected(self):
        source = self.create_ledger()
        target = self.workspace / 'original.jsonl'
        source.rename(target)
        original = target.read_bytes()
        source.symlink_to(target)
        with self.assertRaises(findings.LedgerError):
            self.archive()
        self.assertTrue(source.is_symlink())
        self.assertEqual(original, target.read_bytes())
        self.assertFalse((self.workspace / 'INBOX').exists())

    def test_source_directory_symlink_is_rejected(self):
        source = self.create_ledger()
        original = source.read_bytes()
        alias = self.workspace / 'alias'
        alias.symlink_to(source.parent, target_is_directory=True)
        with patch.object(findings, 'HOME', str(alias)):
            with self.assertRaises(findings.LedgerError):
                self.archive()
        self.assertEqual(original, source.read_bytes())
        self.assertFalse((self.workspace / 'INBOX').exists())

    def test_destination_directory_symlink_is_rejected(self):
        source = self.create_ledger()
        original = source.read_bytes()
        outside = self.workspace / 'unrelated'
        outside.mkdir()
        (self.workspace / 'INBOX').symlink_to(outside, target_is_directory=True)
        with self.assertRaises(findings.LedgerError):
            self.archive()
        self.assertEqual(original, source.read_bytes())
        self.assertEqual([], list(outside.iterdir()))

    def test_out_of_workspace_home_is_rejected(self):
        with tempfile.TemporaryDirectory() as outside:
            with patch.object(findings, 'HOME', outside):
                source = self.create_ledger()
                original = source.read_bytes()
                with self.assertRaisesRegex(findings.LedgerError, 'workspace'):
                    self.archive()
                self.assertEqual(original, source.read_bytes())
        self.assertFalse((self.workspace / 'INBOX').exists())

    def test_load_reports_malformed_serialization_and_missing_ledger(self):
        self.assertEqual([], findings.load('missing'))
        source = self.create_ledger()
        source.write_bytes(b'not an event\n')
        with self.assertRaisesRegex(findings.LedgerError, 'serialization'):
            findings.load('complete')

    def test_canonical_order_and_ledger_identifier_boundaries(self):
        self.assertEqual(findings.canonical({'b': 'value', 'a': 1}),
                         findings.canonical({'a': 1, 'b': 'value'}))
        self.assertEqual(self.workspace / '.findings' / ('a' * 64 + '.jsonl'),
                         Path(findings.path('a' * 64)))
        for name in ('', '../other', 'a/b', 'a\\b', 'a.b', 'a' * 65):
            with self.subTest(name=name), self.assertRaises(findings.LedgerError):
                findings.path(name)

    def test_review_resolution_verification_and_reports_survive_snapshot_parser(self):
        review = self.workspace / 'review.json'
        review.write_text(json.dumps({'reviewer': 'reviewer', 'target': 'docs/',
            'criteria': 'synthetic accuracy criterion', 'findings': [{
                'title': 'A synthetic inaccurate statement', 'severity': 'medium',
                'kind': 'defect', 'location': 'docs/example.md:3',
                'criterion': 'accuracy', 'evidence': 'Synthetic source disagrees',
                'recommendation': 'Correct the statement'}]}), encoding='utf-8')
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            findings.cmd_add(Namespace(ledger='lifecycle', file=str(review)))
            self.assertEqual(1, findings.cmd_status(Namespace(ledger='lifecycle')))
            with self.assertRaises(findings.LedgerError):
                findings.cmd_resolve(Namespace(ledger='lifecycle', id='F-0001',
                    by='reviewer', note='Cannot self-fix', ref=None))
            findings.cmd_resolve(Namespace(ledger='lifecycle', id='F-0001',
                by='author', note='Reworked from source', ref='docs/example.md'))
            with self.assertRaises(findings.LedgerError):
                findings.cmd_verify(Namespace(ledger='lifecycle', id='F-0001',
                    by='author', ok=True, note='Cannot self-verify'))
            findings.cmd_verify(Namespace(ledger='lifecycle', id='F-0001',
                by='reviewer', ok=True, note='Compared with source'))
            findings.cmd_list(Namespace(ledger='lifecycle', state='verified'))
            findings.cmd_report(Namespace(ledger='lifecycle'))
            self.assertEqual(0, findings.cmd_status(Namespace(ledger='lifecycle')))
        events = findings.load('lifecycle')
        self.assertEqual(['add', 'resolve', 'verify'], [event['data']['op'] for event in events])
        self.assertEqual('verified', findings.get(events, 'F-0001')['state'])
        with self.assertRaises(findings.LedgerError):
            findings.get(events, 'F-9999')
        blocking, counts = findings.summary(findings.state(events))
        self.assertEqual([], blocking)
        self.assertEqual(1, counts['verified'])
        self.assertIn('F-0001', output.getvalue())
        self.assertIn('# Findings: lifecycle', output.getvalue())
        self.assertIn('COMPLETE', output.getvalue())

    def test_withdraw_and_simulated_fixture_risk_acceptance_remain_distinct(self):
        self.create_ledger('withdrawn', complete=False)
        self.create_ledger('accepted', complete=False)
        with contextlib.redirect_stdout(io.StringIO()):
            findings.cmd_withdraw(Namespace(ledger='withdrawn', id='F-0001',
                by='reviewer', note='Synthetic allegation was unsupported'))
            with self.assertRaisesRegex(findings.LedgerError, 'time-bound'):
                findings.cmd_accept(Namespace(ledger='accepted', id='F-0001',
                    by='fixture-owner', rationale='Disposable test only', expires=0))
            # This existing test-only mode cannot record authority in any real workspace:
            # HOME and cwd point exclusively to this disposable fixture.
            with patch.dict(os.environ, {'FINDINGS_TEST_AUTHORITY': '1'}):
                self.assertEqual('test', findings.require_person())
                findings.cmd_accept(Namespace(ledger='accepted', id='F-0001',
                    by='fixture-owner', rationale='Disposable test only', expires=1))
        self.assertEqual('withdrawn', findings.get(findings.load('withdrawn'), 'F-0001')['state'])
        accepted = findings.load('accepted')
        self.assertEqual('accepted', findings.get(accepted, 'F-0001')['state'])
        self.assertEqual('test', accepted[-1]['data']['approved_via'])
        self.assertIn('expires', accepted[-1]['data'])

    def test_authority_requires_terminal_or_configured_gate_outside_test_mode(self):
        with patch.dict(os.environ, {'FINDINGS_TEST_AUTHORITY': '0'}):
            with patch.object(findings.sys.stdin, 'isatty', return_value=True), \
                    patch.object(findings.sys.stdout, 'isatty', return_value=True):
                self.assertEqual('terminal', findings.require_person())
            with patch.object(findings.sys.stdin, 'isatty', return_value=False), \
                    patch.object(findings.sys.stdout, 'isatty', return_value=False), \
                    patch('findings.open', side_effect=FileNotFoundError, create=True):
                with self.assertRaisesRegex(findings.LedgerError, 'no approval gate'):
                    findings.require_person()

    def test_existing_selftest_runs_in_disposable_fixture_without_leaking_authority_mode(self):
        folder = self.workspace / 'selftest'
        folder.mkdir()
        original_home = findings.HOME
        output = io.StringIO()
        with patch.object(findings, 'HOME', original_home), \
                patch.dict(os.environ), \
                patch.object(findings.tempfile, 'mkdtemp', return_value=str(folder)), \
                contextlib.redirect_stdout(output):
            self.assertEqual(0, findings.cmd_selftest(Namespace()))
        self.assertEqual(original_home, findings.HOME)
        self.assertIn('checks passed', output.getvalue())


if __name__ == '__main__':
    unittest.main()
