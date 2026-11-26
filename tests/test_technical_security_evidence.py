# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Exercise offline scoped selection, evidence limits and referral preconditions."""

from datetime import datetime, timezone
import json
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.ai/runtime/tools'))
from technical_security_evidence import load_method_manifest

MANIFEST = ROOT / '.ai/skills/it-role-workflows/references/technical-security-evidence-methods.v1.json'
APP = 'application-server-management-account-scope'
MQ = 'messaging-channel-authorization'
JOINT = 'shared-interface-identity'
APP_ASSET = {'id': 'server', 'product': 'JBoss EAP', 'edition': 'fixture', 'version': 'fixture-1',
             'deployment': 'standalone-fixture', 'source': 'inventory-export', 'revision': 'i1',
             'hints': ['middleware', 'java-server-faces']}
MQ_ASSET = {'id': 'broker', 'product': 'IBM MQ', 'edition': 'fixture', 'version': 'fixture-1',
            'deployment': 'queue-manager-fixture', 'source': 'inventory-export', 'revision': 'i2',
            'hints': ['messaging', 'microservices']}
INTERFACE = {'interface': 'orders', 'endpoints': ['server', 'broker'], 'protocol': 'mq',
             'profile': 'fixture-client-channel', 'source': 'interface-inventory', 'revision': 'n1'}
APP_CLAIM = {'id': 'account', 'criterion': APP, 'assets': ['server'],
             'receiving_duty': 'platform-owner'}
JOINT_CLAIM = {'id': 'connection', 'criterion': JOINT, 'assets': ['server', 'broker'],
               'interface': 'orders', 'receiving_duty': 'application-owner'}
APP_EVIDENCE = {'id': 'export', 'criterion': APP, 'criterion_revision': '1',
                'assets': ['server'], 'asset_revisions': {'server': 'i1'},
                'format': 'configuration-observation', 'format_revision': '1',
                'source': 'management export', 'revision': 'c1', 'status': 'conforming'}
JOINT_EVIDENCE = {'id': 'paired-records', 'criterion': JOINT, 'criterion_revision': '1',
                  'assets': ['server', 'broker'], 'asset_revisions': {'server': 'i1', 'broker': 'i2'},
                  'format': 'joint-interface-observation', 'format_revision': '1',
                  'source': 'reviewed paired records', 'revision': 'b1', 'status': 'deviation',
                  'interface': 'orders',
                  'interface_evidence': [{'source': 'interface-inventory', 'revision': 'n1'}]}


def test_mixed_assessment_keeps_unmapped_mandatory_question():
    manifest = load_method_manifest(MANIFEST)
    result = manifest.assess([APP_ASSET, MQ_ASSET], [APP_CLAIM, JOINT_CLAIM],
                             [APP_EVIDENCE, JOINT_EVIDENCE], [INTERFACE])
    assert result['asset_methods'] == {'server': 'application-server', 'broker': 'messaging'}
    assert result['claims']['account']['status'] == 'conforming'
    assert result['claims']['account']['assessment_question'] == manifest.criteria[APP]['question']
    assert result['claims']['account']['attack_context'] == 'T1078'
    assert result['claims']['connection']['status'] == 'deviation'
    assert result['claims']['connection']['methods'] == ['application-server', 'messaging']
    assert result['missing_mandatory_questions'] == [{'asset': 'broker', 'criterion': MQ}]
    assert result['manifest_sha256'] == manifest.digest


@pytest.mark.parametrize('interfaces', [
    [],
    [{**INTERFACE, 'protocol': 'unregistered'}],
    [INTERFACE, {**INTERFACE, 'protocol': 'unregistered', 'revision': 'n2'}],
])
def test_unknown_or_conflicting_protocol_holds_only_dependent_claim(interfaces):
    manifest = load_method_manifest(MANIFEST)
    result = manifest.assess([APP_ASSET, MQ_ASSET], [APP_CLAIM, JOINT_CLAIM],
                             [APP_EVIDENCE, JOINT_EVIDENCE], interfaces)
    assert result['claims']['account']['status'] == 'conforming'
    assert result['claims']['connection']['reason'] == 'unknown-or-conflicting-interface'


def test_hint_cannot_select_method_and_prior_revision_cannot_supply_evidence():
    manifest = load_method_manifest(MANIFEST)
    unsupported = manifest.assess([{**APP_ASSET, 'version': 'unknown'}], [APP_CLAIM],
                                  [APP_EVIDENCE])
    assert unsupported['asset_methods']['server'] is None
    assert unsupported['claims']['account']['reason'] == 'unsupported-scope'
    stale = manifest.assess([{**APP_ASSET, 'revision': 'i2'}], [APP_CLAIM], [APP_EVIDENCE])
    assert stale['claims']['account']['reason'] == 'missing-or-conflicting-evidence'


@pytest.mark.parametrize('mutate', [
    lambda raw: raw['products'].append(raw['products'][0]),
    lambda raw: raw['methods'][0]['criteria'].append('unknown-criterion'),
    lambda raw: raw['aliases'].append({**raw['aliases'][0], 'product': 'ibm-mq'}),
])
def test_invalid_manifest_stops_registration(tmp_path, mutate):
    raw = json.loads(MANIFEST.read_bytes())
    mutate(raw)
    path = tmp_path / 'manifest.json'
    path.write_text(json.dumps(raw))
    with pytest.raises(ValueError):
        load_method_manifest(path)


def test_duplicate_claim_ids_fail_intake():
    manifest = load_method_manifest(MANIFEST)
    with pytest.raises(ValueError, match='claim identifier'):
        manifest.assess([APP_ASSET], [APP_CLAIM, APP_CLAIM], [])


def test_canonical_product_ids_cannot_shadow_each_other(tmp_path):
    raw = json.loads(MANIFEST.read_bytes())
    scope = raw['products'][0]
    raw['products'].append({**scope, 'product': scope['product'].upper(), 'method': 'messaging'})
    raw['aliases'] = [alias for alias in raw['aliases'] if alias['product'] != scope['product']]
    path = tmp_path / 'manifest.json'
    path.write_text(json.dumps(raw))
    with pytest.raises(ValueError, match='Ambiguous canonical product names'):
        load_method_manifest(path)


def test_unregistered_question_remains_pending_without_fabricated_authority():
    manifest = load_method_manifest(MANIFEST)
    claim = {**APP_CLAIM, 'criterion': 'unregistered-criterion'}
    result = manifest.assess([APP_ASSET], [claim], [APP_EVIDENCE])
    assert result['claims']['account']['reason'] == 'unsupported-scope'
    assert result['claims']['account']['assessment_question'] is None
    assert result['claims']['account']['attack_context'] is None
    assert result['missing_mandatory_questions'] == [{'asset': 'server', 'criterion': APP}]


def test_referral_permission_matches_exact_current_report_and_recipient():
    from technical_security_evidence import evaluate_referral_precondition

    now = datetime(2026, 11, 1, 12, tzinfo=timezone.utc)
    referral = {'report_sha256': 'report-digest', 'finding': 'f1',
                'recipient': 'platform-owner', 'scope': 'server',
                'purpose': 'remediation', 'permission': 'grant-1'}
    permission = {**referral, 'id': 'grant-1', 'status': 'active',
                  'expires_at': '2026-11-01T12:01:00+00:00'}
    assert evaluate_referral_precondition(referral, [permission], now=now) == 'eligible'
    assert evaluate_referral_precondition(
        referral, [{**permission, 'expires_at': now.isoformat()}], now=now,
    ) == 'held-expired-permission'
    assert evaluate_referral_precondition(
        referral, [{**permission, 'status': 'revoked'}], now=now,
    ) == 'held-inactive-permission'
    for field in ('recipient', 'scope', 'report_sha256'):
        assert evaluate_referral_precondition(
            {**referral, field: 'changed'}, [permission], now=now,
        ) == 'held-out-of-scope'
    assert evaluate_referral_precondition(
        referral, [permission, permission], now=now,
    ) == 'held-missing-or-ambiguous-permission'


def test_registered_product_versions_support_only_normalized_supplied_records():
    manifest = load_method_manifest(MANIFEST)
    server = {**APP_ASSET, 'edition': 'eap', 'version': '7.4.0', 'deployment': 'standalone'}
    broker = {**MQ_ASSET, 'edition': 'lts', 'version': '9.4.0.0',
              'deployment': 'distributed-queue-manager'}
    mq_claim = {'id': 'channel', 'criterion': MQ, 'assets': ['broker'],
                'receiving_duty': 'messaging-owner'}
    mq_evidence = {**APP_EVIDENCE, 'id': 'mq-export', 'criterion': MQ, 'assets': ['broker'],
                   'asset_revisions': {'broker': 'i2'}, 'status': 'deviation'}
    interface = {**INTERFACE, 'profile': 'client-channel'}
    result = manifest.assess([server, broker], [APP_CLAIM, mq_claim, JOINT_CLAIM],
                             [APP_EVIDENCE, mq_evidence, JOINT_EVIDENCE], [interface])
    assert result['asset_methods'] == {'server': 'application-server', 'broker': 'messaging'}
    assert [result['claims'][name]['status'] for name in ('account', 'channel', 'connection')] == [
        'conforming', 'deviation', 'deviation',
    ]
    native = {**APP_EVIDENCE, 'format': 'arbitrary-vendor-export'}
    assert manifest.assess([server], [APP_CLAIM], [native])['claims']['account']['status'] == 'pending'


def test_cli_pins_the_supplied_intake(tmp_path):
    from hashlib import sha256
    import subprocess

    intake = tmp_path / 'intake.json'
    raw = json.dumps({'assets': [APP_ASSET], 'claims': [APP_CLAIM],
                      'observations': [APP_EVIDENCE]}).encode()
    intake.write_bytes(raw)
    result = subprocess.run(
        [sys.executable, str(ROOT / '.ai/runtime/tools/technical_security_evidence.py'),
         str(MANIFEST), str(intake)],
        check=True, capture_output=True, text=True,
    )
    report = json.loads(result.stdout)
    assert report['intake_sha256'] == sha256(raw).hexdigest()
    assert report['manifest_sha256'] == sha256(MANIFEST.read_bytes()).hexdigest()
    assert report['claims']['account']['status'] == 'conforming'


def test_channel_criterion_rejects_evidence_for_a_different_channel():
    manifest = load_method_manifest(MANIFEST)
    criterion = 'ibm-mq-channel-client-certificate-required'
    claim = {'id': 'tls', 'criterion': criterion, 'assets': ['broker'],
             'receiving_duty': 'messaging-owner', 'channel': 'NEW.CHANNEL'}
    record = {**APP_EVIDENCE, 'criterion': criterion, 'assets': ['broker'],
              'asset_revisions': {'broker': 'i2'}, 'channel': 'OTHER.CHANNEL'}
    assert manifest.assess([MQ_ASSET], [claim], [record])['claims']['tls']['status'] == 'pending'
    matched = manifest.assess([MQ_ASSET], [claim], [{**record, 'channel': 'NEW.CHANNEL'}])
    assert matched['claims']['tls']['status'] == 'conforming'
    del claim['channel']
    assert manifest.assess([MQ_ASSET], [claim], [record])['claims']['tls']['reason'] == 'claim-scope-required'
