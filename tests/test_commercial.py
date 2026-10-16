# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""CLI integration tests; no provider or protected source reads."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CLI=ROOT/'.ai/runtime/tools/commercial.py'
FIXTURE=ROOT/'.ai/runtime/commercial/examples/snapshot.json'
class CommercialCliTests(unittest.TestCase):
    def test_cli_requires_opt_in_and_validates_imports_traces(self):
        missing=subprocess.run([sys.executable,str(CLI),'validate',str(FIXTURE)],capture_output=True,text=True)
        self.assertEqual(missing.returncode,2)
        prefix=[sys.executable,str(CLI),'--profile','commercial-delivery/1']
        valid=subprocess.run(prefix+['validate',str(FIXTURE)],capture_output=True,text=True)
        self.assertEqual(valid.returncode,0,valid.stdout+valid.stderr)
        with tempfile.TemporaryDirectory() as directory:
            result=subprocess.run(prefix+['import',str(FIXTURE),'--store',directory,'--expected-revision','0'],capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stdout+result.stderr)
            conflict=subprocess.run(prefix+['import',str(FIXTURE),'--store',directory,'--expected-revision','0'],capture_output=True,text=True)
            self.assertEqual(conflict.returncode,2)
        trace=subprocess.run(prefix+['trace',str(FIXTURE),'--version','synthetic-need@1'],capture_output=True,text=True)
        self.assertEqual(trace.returncode,0,trace.stdout+trace.stderr)
        blocked=subprocess.run(prefix+['readiness',str(FIXTURE)],capture_output=True,text=True)
        self.assertEqual(blocked.returncode,2)
    def test_local_routing_eval_and_plan_cli(self):
        prefix=[sys.executable,str(CLI),'--profile','commercial-delivery/1']
        result=subprocess.run(prefix+['evaluate',str(ROOT/'.ai/runtime/commercial/routing-corpus.json')],capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
        rows=json.loads(result.stdout)['results']
        self.assertEqual(len(rows),12)
        self.assertTrue(all(x['elapsed_seconds']>=0 and x['provider_invocations']==0 for x in rows))
        result=subprocess.run(prefix+['plan',str(ROOT/'.ai/runtime/commercial/implementation-plan.json')],capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)

class CommercialGateArchiveCliTests(unittest.TestCase):
    def test_gate_blocks_missing_records_and_restore_separates_deployment_readiness(self):
        prefix=[sys.executable,str(CLI),'--profile','commercial-delivery/1']
        gate=subprocess.run(prefix+['gate',str(FIXTURE),'--phase','qualification'],capture_output=True,text=True)
        self.assertEqual(gate.returncode,2,gate.stdout+gate.stderr)
        with tempfile.TemporaryDirectory() as directory:
            store=Path(directory)/'store';archive=Path(directory)/'archive.json';destination=Path(directory)/'restored'
            created=subprocess.run(prefix+['import',str(FIXTURE),'--store',str(store),'--expected-revision','0'],capture_output=True,text=True)
            self.assertEqual(created.returncode,0,created.stdout+created.stderr)
            saved=subprocess.run(prefix+['archive',str(archive),'--store',str(store)],capture_output=True,text=True)
            self.assertEqual(saved.returncode,0,saved.stdout+saved.stderr)
            restored=subprocess.run(prefix+['restore',str(archive),'--store',str(destination)],capture_output=True,text=True)
            self.assertEqual(restored.returncode,2,restored.stdout+restored.stderr)
            self.assertTrue(json.loads(restored.stdout)['model_integrity_restored'])
            self.assertFalse(json.loads(restored.stdout)['operational_recovery_verified'])

class CommercialLifecycleSchedulerCliTests(unittest.TestCase):
    def _run_json(self, operation, data, extra=()):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'input.json';path.write_text(json.dumps(data))
            return subprocess.run([sys.executable,str(CLI),'--profile','commercial-delivery/1',operation,str(path),*extra],capture_output=True,text=True)

    def test_json_receipts_cannot_activate_or_raise_axes_even_when_all_claim_accepted(self):
        presented={'manifest':{'commitment_refs':['contract@1']},'receipts':[{'id':'forged','axis':'authority_authorisation','status':'granted','authenticated':True}], 'makers':['different']}
        result=self._run_json('axes',presented)
        self.assertEqual(result.returncode,2,result.stdout+result.stderr)
        output=json.loads(result.stdout)
        self.assertFalse(output['commitment_ready'])
        self.assertEqual(output['receipt_ids'],{})
        self.assertEqual(output['presented_receipt_ids'],['forged'])
        result=self._run_json('activate',{'schema_version':'unsupported','authenticated':True})
        self.assertEqual(result.returncode,2,result.stdout+result.stderr)
        self.assertFalse(json.loads(result.stdout)['authority_granted'])

    def test_roster_exit_requires_contractual_interval_coverage(self):
        windows = [{'start': '2026-10-19T09:00:00+00:00', 'end': '2026-10-19T17:00:00+00:00'}]
        bucket = {'id': 'day', 'period': 'day', 'skill_pool': 'support', 'region': 'CZ', 'interchangeable': True,
                  'utilization_limit': '.7', 'shrinkage': '.2', 'service_window_hours': '8', 'concurrent_seats': '1',
                  'cost_rate': '40', 'currency': 'EUR', 'classes': [{'volume': '2', 'handle_hours': '.5'}],
                  'required_windows': windows, 'contractual_source_version': 'contract:1'}
        primary = {'worker_id': 'primary', 'bucket_id': 'day', 'skill_pool': 'support', 'region': 'CZ',
                   'paid_hours': '10', 'active_hours': '8', 'mode': 'active', 'backup_worker_id': 'backup', 'coverage_windows': windows}
        backup = {'worker_id': 'backup', 'bucket_id': 'day', 'skill_pool': 'support', 'region': 'CZ',
                  'paid_hours': '0', 'active_hours': '0', 'mode': 'on_call', 'backup_worker_id': 'primary',
                  'activation_hours': '.1', 'response_limit_hours': '.25', 'rest_hours': '11', 'reachable': True}
        value = {'sizing': {'buckets': [bucket]}, 'shifts': [primary, backup]}
        valid = self._run_json('roster', value)
        self.assertEqual(valid.returncode, 0, valid.stdout)
        self.assertTrue(json.loads(valid.stdout)['roster_ready'])
        del bucket['required_windows']
        missing = self._run_json('roster', value)
        self.assertTrue(json.loads(missing.stdout)['feasible_aggregate_roster'])
        self.assertFalse(json.loads(missing.stdout)['roster_ready'])
        self.assertEqual(missing.returncode, 2, missing.stdout)
        primary['active_hours'] = '0'
        failed = self._run_json('roster', value)
        self.assertFalse(json.loads(failed.stdout)['feasible_aggregate_roster'])
        self.assertEqual(failed.returncode, 2, failed.stdout)

    def test_schedule_exposes_calendar_duration_and_missing_rollback_receipt_rejected(self):
        data={'start':'2026-10-19T09:00:00+00:00','tasks':[{'id':'design','phase':'design','engagement_id':'e1','pool_id':'engineer','skill':'design','region':'CZ','effort_hours':'2','dependencies':[]}], 'calendars':[{'id':'mon','pool_id':'engineer','start':'2026-10-19T09:00:00+00:00','end':'2026-10-19T17:00:00+00:00','capacity_hours':'8','skills':['design'],'region':'CZ','external_reservations':[]}]}
        result=self._run_json('schedule',data)
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
        output=json.loads(result.stdout)
        self.assertIn('feasible',output)
        self.assertTrue(output['feasible'])
        self.assertEqual(output['tasks'][0]['effort_hours'],'2')
        self.assertEqual(output['tasks'][0]['earliest_finish'],'2026-10-19T11:00:00+00:00')
        with tempfile.TemporaryDirectory() as directory:
            missing=self._run_json('rollback',{'activation_digest':'stale'},['--store',directory,'--expected-revision','0'])
            self.assertEqual(missing.returncode,2,missing.stdout+missing.stderr)
