# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Disposable external-signature fixtures; these never grant production authority."""
import base64
import json
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / '.ai/runtime/tools'))
import operator_actions as op


class SyntheticOperator:
    """Pin a disposable Ed25519 public identity and sign exact synthetic requests."""

    def __init__(self, tmp_path, monkeypatch):
        """Create test-only key custody and patch only the external public trust pin."""
        self.directory = tmp_path
        self.private = tmp_path / 'synthetic-private.pem'
        public = tmp_path / 'synthetic-public.pem'
        subprocess.run(['openssl', 'genpkey', '-algorithm', 'ED25519', '-out', str(self.private)],
                       check=True, capture_output=True)
        subprocess.run(['openssl', 'pkey', '-in', str(self.private), '-pubout', '-out', str(public)],
                       check=True, capture_output=True)
        self.trust = {'schema_version': 2, 'policy_version': 'local-operator-attestation/2',
                      'key_id': op.sha(public.read_bytes()), 'public_key': public.read_text(),
                      'signer': 'Synthetic test operator',
                      'capabilities': ['lifecycle-update', 'accept', 'authorise']}
        monkeypatch.setattr(op, 'trusted_key', lambda: self.trust)

    def sign(self, request, accepted=True):
        """Return a real exact-request Ed25519 receipt without applying any effect."""
        receipt = op.response(request, accepted)
        receipt.update(key_id=self.trust['key_id'], assurance=op.ASSURANCE)
        payload = self.directory / 'synthetic-signing-payload'
        signature = self.directory / 'synthetic-signature'
        payload.write_bytes(op.canonical(receipt))
        subprocess.run(['openssl', 'pkeyutl', '-sign', '-inkey', str(self.private), '-rawin',
                        '-in', str(payload), '-out', str(signature)], check=True, capture_output=True)
        receipt['signature'] = base64.b64encode(signature.read_bytes()).decode()
        return receipt

    def apply(self, module, request_path):
        """Sign and apply a generated request through the real receipt-verifying CLI."""
        request = json.loads(request_path.read_text())
        receipt_path = request_path.with_suffix('.receipt.json')
        receipt_path.write_text(json.dumps(self.sign(request)))
        assert module.cmd_apply_operator(SimpleNamespace(request=str(request_path),
                                                        receipt=str(receipt_path))) == 0


def accepted_graph(module, tmp_path, monkeypatch, text, engagement='synthetic-content', acceptance_state='accepts', requirement_text=None):
    """Build a fresh qualified graph and real synthetic exact-output acceptance.

    Uses ordinary graph writes, governed proposal/verification plans, and the
    existing human-review request/apply path. No qualification or proof verifier
    is patched. All authority is restricted to this disposable test identity.
    """
    monkeypatch.setattr(module, 'FABRIC_DIR', str(tmp_path))
    signer = SyntheticOperator(tmp_path, monkeypatch)
    lc = module.lifecycle
    graph = module.Fabric(engagement, [])
    graph.add_node('intent', 1, 'Synthetic fixture only')
    sequence = 0

    def update(proposed=(), verification=(), proofs=()):
        nonlocal sequence
        sequence += 1
        spec = {'scope': 'default', 'reason': 'Disposable qualification fixture',
                'proposed': list(proposed),
                'selections': [{'logical_id': item['manifest']['logical_id'],
                                'version_id': lc.version_id(item['manifest'])} for item in proposed],
                'reinstatements': [], 'invalidations': [], 'verification': list(verification),
                'proofs': list(proofs), 'allowed_verification_path': 'synthetic-observation'}
        spec_path = tmp_path / ('spec-' + str(sequence) + '.json')
        request_path = tmp_path / ('request-' + str(sequence) + '.json')
        spec_path.write_text(json.dumps(spec))
        module.cmd_lifecycle_plan(SimpleNamespace(engagement=engagement, spec=str(spec_path), out=str(request_path)))
        signer.apply(module, request_path)

    obligations = {'categories': {category: {'minimum': 1, 'allow_exclusion': False}
                                  for category in lc.CATEGORIES},
                   'evidence_roles': [], 'review_roles': ['reviewer']}
    bases = {category: lc.manifest('fixture:' + category,
                                  'contract' if category == 'contract' else category,
                                  {'obligations': obligations} if category == 'contract' else {'fixture': category})
             for category in lc.CATEGORIES}
    update(proposed=[{'manifest': value} for value in bases.values()])
    bindings = {category: {'refs': [lc.version_id(value)]} for category, value in bases.items()}
    observation = tmp_path / 'observed-bytes.txt'
    observation.write_text('Synthetic immutable verification observation.\n')
    graph = module.open_fabric(engagement)
    requirement = graph.add_node('req', 1, requirement_text) if requirement_text is not None else None
    evidence = graph.add_node('evd', 1, 'Synthetic observed verification', confidence='observation',
                              file=str(observation), bindings=bindings)
    fragment = graph.add_node('frag', 1, text, bindings=bindings)
    if requirement is not None:
        graph.add_edge(requirement['id'], 'requests', fragment['id'])
    graph.add_edge(evidence['id'], 'supports', fragment['id'])
    reviews = [lc.manifest('fixture:review:' + node['id'], 'rev',
                           {'subject': node['version_id'], 'state': 'accepts',
                            'reviewer': 'Synthetic independent reviewer'})
               for node in (evidence, fragment)]
    update(proposed=[{'manifest': value} for value in reviews])
    versions = [lc.version_id(value) for value in bases.values()]
    versions += [evidence['version_id'], fragment['version_id']]
    if requirement is not None:
        versions.append(requirement['version_id'])
    versions += [lc.version_id(value) for value in reviews]
    update(verification=[{'version_id': identifier, 'evidence': [evidence['version_id']],
                          'path': 'synthetic-observation',
                          'changes': {'validity': 'valid', 'applicable': True,
                                      'sufficient': True, 'reviewed': True}} for identifier in versions],
           proofs=[{'subject': node['version_id'], 'role': 'reviewer', 'proof': lc.version_id(review)}
                   for node, review in zip((evidence, fragment), reviews)])
    if acceptance_state is not None:
        request_path = tmp_path / 'acceptance-request.json'
        module.cmd_review(SimpleNamespace(engagement=engagement, fragment=fragment['id'], layer=0,
                                          state=acceptance_state, rationale='Synthetic exact-closure acceptance',
                                          reviewer='Synthetic domain authority', model='human-fixture',
                                          constraints='Synthetic explicit constraints' if acceptance_state=='accepts_with_constraints' else None,
                                          request_out=str(request_path)))
        signer.apply(module, request_path)
    graph = module.open_fabric(engagement)
    return graph, fragment['id'], signer
