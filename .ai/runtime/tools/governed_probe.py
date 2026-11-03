#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Native qualification observations for governed identity and missing human proof.

This probe cannot establish positive dispatcher enrollment or host confinement.
Those require the separately signed runtime tests and effective provider tests.
"""
from __future__ import annotations

import tempfile
import time
import sys
from pathlib import Path

import governed_delivery
import lifecycle


def governed_record_probe():
    """Check actual record identity and refusal of missing human authority proof.

    Returns:
        True only when record bytes use the shared immutable formula and the
        human verifier rejects missing proof without creating a ledger.
    Raises:
        OSError: Local disposable material cannot be created or read.
        ValueError: The active runtime or required contract is inconsistent.
    """
    with tempfile.TemporaryDirectory(prefix='jai-governed-probe-') as directory:
        path = Path(directory) / 'native-probe.jsonl'
        store = lifecycle.Store(path, 'native-probe')
        material = store.put_blob(b'Native governed identity probe.\n')
        source = {'owner': {'kind': 'authority', 'id': 'native-probe-human'},
                  'source_role': 'input', 'origin': {'kind': 'authority', 'id': 'native-probe-human'},
                  'material': [material], 'criteria': [], 'inherited': []}
        manifest = lifecycle.record_manifest('native-probe', 'default', 'native-input', 'source', source)
        expected = lifecycle.manifest('native-input', 'delivery.source',
                                      {'engagement': 'native-probe', 'scope': 'default', 'record': source})
        now = int(time.time() * 1000)
        reference = {'logical_id': manifest['logical_id']}
        reference.update(version_id=lifecycle.version_id(manifest), engagement='native-probe', scope='default')
        payload = {'action': 'terminate', 'subjects': [reference],
                   'reason': 'Probe missing human proof', 'authority_proof': '0' * 64}
        governed_delivery.validate(payload, 'decision.schema.json')
        message = {'message_type': 'decision', 'payload': payload}
        denied = False
        try:
            lifecycle._verify_human(message, None, profile=None, at=now, live=True)
        except lifecycle.ERROR as error:
            denied = error.code == 'P_SCOPE'
        return (manifest == expected and lifecycle.version_id(manifest) == lifecycle.version_id(expected)
                and denied and not path.exists())


if __name__ == '__main__':
    passed = governed_record_probe()
    print('Governed identity and missing human-proof probe: ' + ('PASS' if passed else 'FAIL'))
    sys.exit(0 if passed else 1)
