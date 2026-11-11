# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Disposable one-shot canonical reader packaging probe; not a product API.

Results demonstrate only the exercised fixture and native host. No operation
writes an input, evaluates current permissions or executes project code.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
FORMAT = 'jai.fabric-explorer.reader-probe/1'


def _runtime():
    if not getattr(sys, 'frozen', False):
        owned = Path(__file__).resolve().parents[4] / '.ai/runtime/tools'
        sys.path.insert(0, str(owned))
        sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'reader'))
    import lifecycle
    import operator_actions
    import findings
    return lifecycle, operator_actions, findings


def _result(**fields):
    return {'format': FORMAT, 'authority_granted': False,
            'current_assessment': False, **fields}


def _verifier_path():
    name = 'openssl.exe' if os.name == 'nt' else 'openssl'
    base = Path(sys.executable).parent if getattr(sys, 'frozen', False) else None
    if base is None:
        raise ValueError('Bundled verifier proof requires the frozen executable')
    path = base / 'verifier' / name
    if not path.is_file() or path.is_symlink():
        raise ValueError('Fixed bundled verifier is unavailable')
    return path


def _verify_vector():
    # RFC 8032 section 7.1 test vector 2 contains only public verification data.
    public = bytes.fromhex('302a300506032b6570032100'
                           '3d4017c3e843895a92b70aa74d1b7ebc'
                           '9c982ccf2ec4968cc0cd55f12af4660c')
    signature = bytes.fromhex(
        '92a009a9f0d4cab8720e820b5f642540a2b27b5416503f8fb3762223ebdb69da'
        '085ac1e43e15996e458f3613d0f11d8c387b2eaeb4302aeeb00d291612bb0c00')
    executable = _verifier_path()
    environment = {'PATH': str(executable.parent), 'OPENSSL_CONF': os.devnull}
    if sys.platform.startswith('linux'):
        environment['LD_LIBRARY_PATH'] = str(executable.parent / 'lib')
    if os.name == 'nt' and os.environ.get('SystemRoot'):
        environment['SystemRoot'] = os.environ['SystemRoot']
    with tempfile.TemporaryDirectory(prefix='jai-reader-vector-') as temporary:
        root = Path(temporary)
        (root / 'key.der').write_bytes(public)
        (root / 'message').write_bytes(b'\x72')
        (root / 'signature').write_bytes(signature)
        command = [str(executable), 'pkeyutl', '-verify', '-pubin', '-keyform', 'DER',
                   '-inkey', str(root / 'key.der'), '-rawin', '-in', str(root / 'message'),
                   '-sigfile', str(root / 'signature')]
        verified = subprocess.run(command, env=environment, capture_output=True, timeout=15)
        (root / 'message').write_bytes(b'\x73')
        rejected = subprocess.run(command, env=environment, capture_output=True, timeout=15)
    if verified.returncode != 0 or rejected.returncode == 0:
        raise ValueError('Bundled verifier failed positive/negative Ed25519 vector')
    return _result(status='verified-vector', verifier='bundled',
                   positive_verified=True, tampered_rejected=True,
                   history_verified=False)


def main(argv=None):
    """Run one read-only fixture operation, printing one bounded JSON summary.

    Args:
        argv: Explicit CLI arguments, or None for this process's arguments.
    Returns:
        Zero for an observed read/vector result; two for safe rejection.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='operation', required=True)
    for operation in ('fabric', 'diagnostic', 'findings'):
        command = commands.add_parser(operation)
        command.add_argument('--journal', type=Path, required=True)
        if operation == 'fabric':
            command.add_argument('--engagement', required=True)
        if operation == 'findings':
            command.add_argument('--max-rounds', type=int)
    commands.add_parser('verifier')
    args = parser.parse_args(argv)
    rejections = (ValueError, OSError, KeyError, TypeError, subprocess.SubprocessError)
    try:
        if args.operation == 'verifier':
            result = _verify_vector()
        else:
            # No project-selected modules, config, enrollment or executable path
            # participate in the read-only operation's implementation.
            os.environ.pop('FINDINGS_MAX_ROUNDS', None)
            lc, operator, findings = _runtime()
            rejections = (*rejections, findings.LedgerError)
            if args.operation == 'fabric':
                # Missing Store paths represent empty state in the runtime; this
                # probe deliberately refuses them rather than implying import.
                if not args.journal.exists():
                    raise FileNotFoundError('Selected journal does not exist')
                store = lc.Store(args.journal, args.engagement)
                state = store.read()
                result = _result(status='canonical-history', history_verified=True,
                                 head=state.head, transactions=len(state.transactions),
                                 versions=len(state.versions), uses=len(state.states),
                                 families=dict(Counter(v['kind'] for v in state.versions.values())))
            elif args.operation == 'diagnostic':
                from readonly_files import read_snapshot
                raw = read_snapshot(args.journal)
                rows = lc._parse_transactions(raw)
                result = _result(status='diagnostic-only', history_verified=False,
                                 decoded_rows=len(rows), semantic_state='unknown',
                                 verification='not-attempted')
            else:
                from readonly_files import read_snapshot
                events = findings._parse_events(read_snapshot(args.journal),
                                                'selected-fixture')
                result = _result(status='findings-chain', chain_verified=True,
                                 history_verified=False, events=len(events),
                                 round_configuration='unknown', recorded_states=None)
                if args.max_rounds is not None:
                    if not 1 <= args.max_rounds <= 1000:
                        raise ValueError('Explicit rounds must be between 1 and 1000')
                    findings.MAX_ROUNDS = args.max_rounds
                    states = findings.state(events)
                    result.update(round_configuration=args.max_rounds,
                                  recorded_states=dict(Counter(v['state'] for v in states.values())))
        print(json.dumps(result, sort_keys=True, separators=(',', ':')))
        return 0
    except rejections as error:
        # Source paths, labels and receipt bytes are not safe routine diagnostics.
        print(json.dumps(_result(status='rejected', history_verified=False,
                                 code=getattr(error, 'code', type(error).__name__))))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
