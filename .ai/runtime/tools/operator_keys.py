# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Host-only operator key location and explicitly confirmed installation setup.

Key creation does not enroll public trust or authorize any JAI decision. The
installer calls this helper in the host console; runtime consumers need only the
location function and never inspect the private key.
"""
from __future__ import annotations

import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def default_private_key():
    """Return the conventional host private-key path without reading its contents.

    Returns:
        Absolute path under the current operator's home directory. No directories
        or files are created, and no authority or key availability is inferred.
    """
    return Path.home() / '.local/share/jai-operator/private.pem'


def provision_operator_key(*, force=False, dry_run=False):
    """Offer Ed25519 creation in a human terminal, preserving an existing key.

    Args:
        force: Offer replacement of an existing key, still requiring confirmation.
        dry_run: Report planned setup without prompting or writing anything.
    Returns:
        Public status/path metadata. Existing keys are left untouched without
        force; noninteractive, declined and dry-run calls never create material.
        Confirmed replacement retains a private backup and never changes trust.
    Raises:
        OSError: File creation, backup or replacement fails. An existing key is
            preserved if staging or backup fails.
        ValueError: OpenSSL fails or a forced target is not a regular file.
    """
    key = default_private_key()
    exists = key.exists() or key.is_symlink()
    result = {'path': str(key), 'status': 'existing' if exists else 'unavailable'}
    if exists and not force:
        print(f'Operator signing key already exists: {key}; not regenerated (use --force-genkey to request replacement).')
        return result
    if dry_run:
        print(f'Dry run: would offer operator key {"replacement" if exists else "creation"}: {key}; no key files written.')
        return {**result, 'status': 'dry-run'}
    if not sys.stdin.isatty():
        print(f'Operator signing key setup skipped: no interactive host terminal; key {"not replaced" if exists else "not created"}: {key}. Re-run install.sh in your host terminal.')
        return result
    if exists and (key.is_symlink() or not key.is_file()):
        raise ValueError('Operator key replacement requires an existing regular non-symlink file')
    if exists:
        print('Replacing this key does not update public enrollment; enroll its new public key explicitly before signing with it.')
    try:
        answer = input(f'{"Replace" if exists else "Create"} operator Ed25519 signing key at {key}? [Y/n] ').strip().lower()
    except EOFError:
        answer = 'n'
    if answer not in {'', 'y', 'yes'}:
        print(f'Operator signing key {"not replaced" if exists else "not created"}: confirmation declined.')
        return {**result, 'status': 'declined'}
    key.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    key.parent.chmod(0o700)
    descriptor, staged = tempfile.mkstemp(prefix='.private-', dir=key.parent)
    os.close(descriptor)
    staged = Path(staged)
    try:
        completed = subprocess.run(['/usr/bin/openssl', 'genpkey', '-algorithm', 'ED25519', '-out', str(staged)],
            capture_output=True, timeout=30,
            env={'PATH': '/usr/bin:/bin', 'LANG': 'C.UTF-8', 'OPENSSL_CONF': '/dev/null'})
        if completed.returncode:
            raise ValueError('OpenSSL operator key generation failed; existing key was not replaced')
        staged.chmod(0o600)
        if exists:
            descriptor, backup = tempfile.mkstemp(prefix='private.pem.backup-', dir=key.parent)
            with os.fdopen(descriptor, 'wb') as output, key.open('rb') as original:
                shutil.copyfileobj(original, output)
            result['backup'] = backup
            os.replace(staged, key)
        else:
            # Exclusive publication prevents a concurrent creator's key from
            # being overwritten without an explicit replacement request.
            os.link(staged, key)
        result['status'] = 'replaced' if exists else 'created'
        print(f'Operator signing key {result["status"]}: {key} (private mode 0600).')
        if 'backup' in result:
            print(f'Previous operator key preserved: {result["backup"]}')
        print('Public trust is unchanged. Export only the public key for explicit enrollment:')
        import shlex
        print(shlex.join(['/usr/bin/openssl', 'pkey', '-in', str(key), '-pubout']))
        return result
    finally:
        staged.unlink(missing_ok=True)
