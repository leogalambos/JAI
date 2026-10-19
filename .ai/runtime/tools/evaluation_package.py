#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Build and verify optional, local-only synthetic evaluation data packages.

The core distribution pins every payload digest. Availability or digest checking
is not a passing evaluation and never grants professional acceptance.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import zipfile

from content_spec import canonical_hash


def _runtime(root):
    root = Path(root).resolve()
    return root / '.ai/runtime' if (root / '.ai/runtime').is_dir() else root


def _descriptor(runtime):
    descriptor = json.loads((runtime / 'content/evaluation-package.json').read_text())
    entries = descriptor.get('files')
    if (descriptor.get('schema_version') != '1.0.0'
            or descriptor.get('package_kind') != 'optional-extended-synthetic-evaluation'
            or not isinstance(entries, dict) or not entries
            or descriptor.get('payload_hash') != canonical_hash(entries)):
        raise ValueError('invalid pinned evaluation descriptor')
    for relative, digest in entries.items():
        path = PurePosixPath(relative)
        if (not relative.startswith('evals/content_quality/enterprise/')
                or path.is_absolute() or '..' in path.parts or '\\' in relative
                or not isinstance(digest, str) or len(digest) != 64
                or any(char not in '0123456789abcdef' for char in digest)):
            raise ValueError('invalid pinned evaluation resource')
    manifest = json.loads((runtime / 'evals/content_quality/manifest.json').read_text())
    if set(entries) != set(manifest.get('enterprise_cases', [])):
        raise ValueError('evaluation descriptor differs from required corpus')
    return descriptor


def validate_package(root, data_root=None):
    """Verify every required synthetic data file against the core-pinned manifest.

    Args:
        root: Core source/runtime root providing the trusted package descriptor.
        data_root: Locally provisioned unpacked package; defaults to core runtime.
    Returns:
        AVAILABLE only when all required files match. UNAVAILABLE or INVALID has
        sanitized diagnostics, no private directory, filenames or payload hashes.
    Raises:
        OSError, ValueError: For an invalid trusted core descriptor.
    """
    runtime = _runtime(root)
    descriptor = _descriptor(runtime)
    data_root = Path(data_root) if data_root else runtime
    if data_root.is_symlink():
        return {'state': 'INVALID', 'reason': 'Evaluation data root is a symbolic link.'}
    data_root = data_root.resolve()
    missing = 0
    for relative, expected in descriptor['files'].items():
        path = data_root / relative
        if any(parent.is_symlink() for parent in [path, *path.parents] if parent != data_root.parent):
            return {'state': 'INVALID', 'reason': 'Evaluation resources must not be symbolic links.'}
        if not path.is_file():
            missing += 1
        elif hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            return {'state': 'INVALID', 'reason': 'Evaluation resource integrity mismatch.'}
    if missing:
        return {'state': 'UNAVAILABLE', 'reason': 'Required extended evaluation data is not locally available.',
                'missing_count': missing}
    return {'state': 'AVAILABLE', 'file_count': len(descriptor['files']),
            'release': descriptor['release'], 'evidence_class': 'synthetic-regression',
            'professional_approval': False}


def build_package(root, output):
    """Create a deterministic exclusive ZIP containing only pinned synthetic data.

    Args:
        root: Full source/runtime root containing all extended evaluation inputs.
        output: New destination ZIP outside its input resource subtree.
    Returns:
        Public package digest and file count. Writes a SHA-256 companion file.
    Raises:
        ValueError, OSError: For incomplete/changed data or an existing destination.
    """
    runtime = _runtime(root)
    availability = validate_package(runtime)
    if availability['state'] != 'AVAILABLE':
        raise ValueError('complete matching local evaluation data is required')
    descriptor = _descriptor(runtime)
    output = Path(output)
    if output.with_suffix(output.suffix + '.sha256').exists():
        raise FileExistsError('evaluation digest destination already exists')
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, 'x', zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for relative in sorted(descriptor['files']):
            info = zipfile.ZipInfo(relative, (1980, 1, 1, 0, 0, 0))
            info.external_attr = 0o644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, (runtime / relative).read_bytes())
    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    output.with_suffix(output.suffix + '.sha256').write_text(digest + '  ' + output.name + '\n')
    return {'state': 'BUILT', 'release': descriptor['release'], 'sha256': digest,
            'file_count': len(descriptor['files']), 'professional_approval': False}


def main(argv=None):
    """Build or inspect explicitly local optional data; never fetch missing inputs.

    Args:
        argv: Optional command-line tokens.
    Returns:
        Zero only for complete verified availability or successful package creation.
    Raises:
        SystemExit: For invalid CLI syntax.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('build', 'check'))
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--data-root', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args(argv)
    try:
        if args.command == 'build':
            if not args.output:
                raise ValueError('--output is required')
            result = build_package(args.root, args.output)
        else:
            result = validate_package(args.root, args.data_root)
        print(json.dumps(result, indent=2))
        return 0 if result['state'] in ('AVAILABLE', 'BUILT') else 1
    except (OSError, ValueError, KeyError):
        parser.exit(1, 'Evaluation package failed: invalid local inputs or destination.\n')


if __name__ == '__main__':
    raise SystemExit(main())
