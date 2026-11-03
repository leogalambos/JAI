#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Canonical local-writer delivery CLI; legacy graph mutation is archive-only.

Use validate for pure shape/identity checks. The sole local runtime records ordinary
controller operations; only explicit L0 decisions require an external signature.
Local operator queries need no read credential. This command never performs an L0 act.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import governed_delivery as delivery
import lifecycle
import operator_actions as operator

FABRIC_DIR = os.path.expanduser(os.environ.get('FABRIC_HOME') or '~/.ai/fabric')
FabricError = delivery.ProtocolError


def log_path(engagement):
    """Return the local ledger locator for a bounded nontraversing engagement ID.

    Args:
        engagement: Nonempty identifier containing no path separators or dot components.
    Returns:
        Ledger path; a locator grants no read or mutation authority.
    Raises:
        ValueError: The identifier could escape the configured ledger directory.
    """
    if not isinstance(engagement, str) or not engagement or len(engagement) > 128 or any(char in engagement for char in '/\\') or engagement in {'.', '..'}:
        raise ValueError('bounded nontraversing engagement identity required')
    return str(Path(FABRIC_DIR) / (engagement + '.jsonl'))


def open_fabric(engagement):
    """Return the sole Store; retired graph mutation methods are not provided.

    Args:
        engagement: Exact governed engagement identifier.
    Returns:
        Authoritative local runtime Store.
    """
    return lifecycle.Store(log_path(engagement), engagement)



def main(argv=None):
    """Dispatch canonical validation, ingestion and authenticated read operations.

    Args:
        argv: Optional argument sequence for a host integration or isolated test.
    Returns:
        Zero on success and two for safe rejection or unsupported archived operations.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    validate = commands.add_parser('validate', help='Pure offline message shape and identity check')
    validate.add_argument('--message', required=True)
    submit = commands.add_parser('submit', help='Record one local host protocol request')
    submit.add_argument('engagement')
    submit.add_argument('--message', required=True)
    submit.add_argument('--authority-proof')
    basis = commands.add_parser('current-basis', help='Local exact current-basis query')
    basis.add_argument('engagement')
    basis.add_argument('--query', required=True)
    for operation in ('verify', 'status', 'justify', 'report'):
        command = commands.add_parser(operation, help='Local read-only governed assessment')
        command.add_argument('engagement')
        command.add_argument('--query', required=True)
    retired = {'init', 'req', 'contract', 'ingest', 'ingest-reviews', 'review', 'evidence', 'answer',
               'authorise', 'reformulate', 'invalidate', 'consolidate', 'conflict', 'escalate', 'propose',
               'release', 'lifecycle-plan', 'lifecycle-apply', 'apply-operator', 'keygen', 'selftest'}
    actual = sys.argv[1:] if argv is None else list(argv)
    if actual and actual[0] in retired:
        print('Unsupported archive workflow: use current local governed messages; archived mutation commands are unsupported.', file=sys.stderr)
        return 2
    args = parser.parse_args(actual)
    try:
        if args.command == 'validate':
            message = lifecycle._parse_message(operator.regular(args.message))
            print(json.dumps({'protocol': delivery.PROTOCOL, 'message_id': message['message_id'], 'structurally_valid': True, 'authority_granted': False}))
            return 0
        store = open_fabric(args.engagement)
        if args.command == 'submit':
            result = store.submit(operator.regular(args.message),
                                  authority_proof=operator.regular(args.authority_proof) if args.authority_proof else None)
            print(json.dumps(result, ensure_ascii=False, sort_keys=True))
            return 2 if result['status'] == 'rejected' else 0
        query = lifecycle.loads(operator.regular(args.query))
        result = store.current_basis(query)
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0
    except (ValueError, OSError) as error:
        print('Governed operation rejected: ' + str(error), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
