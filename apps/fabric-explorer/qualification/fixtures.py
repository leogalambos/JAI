# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Prepare/check/restore owned synthetic ACL sources outside the traced product interval.

Usage: pinned-python fixtures.py prepare --directory ABS --python ABS --electron ABS
--initial-cwd ABS; check --manifest ABS --output ABS; restore --manifest ABS.
Only new synthetic-source/application children are created. Restore changes modes
only on the same recorded physical entries and never deletes unknown content.
"""
from __future__ import annotations

import argparse
import errno
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess

FORMAT = 'jai.fabric-explorer.security-input/1'
REPOSITORY = Path(__file__).resolve().parents[3]



NATIVE_EXECUTABLES = tuple(Path(path) for path in (
    '/usr/bin/bwrap', '/usr/bin/true',
    '/usr/libexec/glycin-loaders/2+/glycin-svg',
    '/usr/libexec/glycin-loaders/2+/glycin-image-rs'))
NATIVE_CONFIG = Path('/usr/share/glycin-loaders/2+/conf.d')


def native_runtime_identities() -> dict:
    """Observe fixed OS components without admitting them as application executables.

    Returns:
        Actual owner/physical identities and hashes, with explicit missing entries.
    Raises:
        OSError: An existing fixed component cannot be inspected or read.
        ValueError: Config directory exceeds 32 entries or a config exceeds 64 KiB.
    """
    def metadata(info):
        return {'uid': str(info.st_uid), 'gid': str(info.st_gid),
                'mode': str(stat.S_IMODE(info.st_mode)), 'device': str(info.st_dev),
                'inode': str(info.st_ino), 'size': str(info.st_size)}

    def observe(path, limit):
        try:
            info = path.lstat()
        except FileNotFoundError:
            return {'path': str(path), 'status': 'missing'}
        resolved = path.resolve(strict=True)
        target = resolved.stat()
        row = {'path': str(path), 'status': 'observed', 'lstat': metadata(info),
               'resolvedPath': str(resolved), 'resolved': metadata(target)}
        if stat.S_ISLNK(info.st_mode):
            row['linkTarget'] = os.readlink(path)
        if not stat.S_ISREG(target.st_mode) or target.st_size > limit:
            raise ValueError('Fixed native component has unsupported type or exceeds its evidence bound.')
        with resolved.open('rb') as stream:
            row['resolved']['sha256'] = hashlib.file_digest(stream, 'sha256').hexdigest()
        return row

    executables = [observe(path, 512 * 1024 * 1024) for path in NATIVE_EXECUTABLES]
    try:
        info = NATIVE_CONFIG.lstat()
    except FileNotFoundError:
        configs = {'path': str(NATIVE_CONFIG), 'status': 'missing', 'entries': []}
    else:
        if not stat.S_ISDIR(info.st_mode):
            raise ValueError('Fixed native config root must be a real directory.')
        entries = []
        for path in NATIVE_CONFIG.iterdir():
            if len(entries) == 32:
                raise ValueError('Fixed native config entry count exceeds 32.')
            entries.append(path)
        configs = {'path': str(NATIVE_CONFIG), 'status': 'observed', 'lstat': metadata(info),
                   'entries': [observe(path, 64 * 1024) for path in sorted(entries)]}
    return {'format': 'jai.fabric-explorer.native-runtime-identities/1',
            'executables': executables, 'configs': configs}


def snapshot_source(root: Path) -> list[dict]:
    """Read exact synthetic bytes, directory membership and lossless physical metadata.

    Args:
        root: Absolute, nonlinked source root readable by the current nonroot user.
    Returns:
        Path-sorted entries; atime/ctime are excluded because reads/driver ACLs change them.
    Raises:
        OSError: An entry cannot be inspected or read.
        ValueError: A source entry is linked or nonregular.
    """
    if not stat.S_ISDIR(root.lstat().st_mode):
        raise ValueError('Synthetic source root must be a nonlinked directory.')
    entries = []
    pending = [root]
    while pending:
        path = pending.pop()
        info = path.lstat()
        directory = stat.S_ISDIR(info.st_mode)
        if not directory and (not stat.S_ISREG(info.st_mode) or info.st_nlink != 1):
            raise ValueError('Synthetic sources must be nonlinked regular files and directories.')
        item = {'path': path.relative_to(root).as_posix(), 'kind': 'directory' if directory else 'file',
                'device': str(info.st_dev), 'inode': str(info.st_ino),
                'mode': str(stat.S_IMODE(info.st_mode)), 'size': str(info.st_size)}
        if directory:
            pending.extend(sorted(path.iterdir(), reverse=True))
        else:
            item['sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()
        entries.append(item)
    return sorted(entries, key=lambda item: item['path'])


def _absolute(value: str | Path) -> Path:
    path = Path(value)
    if not path.is_absolute() or path != Path(os.path.abspath(path)):
        raise ValueError('An explicit normalized absolute test path is required.')
    return path


def _seal(root: Path) -> None:
    entries = snapshot_source(root)
    for item in reversed(entries):
        path = root / item['path']
        subprocess.run(['/usr/bin/setfacl', '-m', 'u::r-x' if item['kind'] == 'directory' else 'u::r--', str(path)], check=True, capture_output=True)


def _negative_probes(root: Path, journal: Path) -> list[dict]:
    probes = []
    actions = [('file-write', lambda: journal.open('ab')),
               ('directory-create', lambda: (root / 'denied-create').open('xb')),
               ('source-rename', lambda: journal.rename(root / 'denied-rename')),
               ('source-unlink', lambda: journal.unlink())]
    for name, action in actions:
        try:
            value = action()
            if hasattr(value, 'close'):
                value.close()
            probes.append({'operation': name, 'denied': False})
        except OSError as error:
            probes.append({'operation': name, 'denied': error.errno in (errno.EACCES, errno.EPERM, errno.EROFS), 'errno': error.errno})
    return probes


def prepare_fixture(directory: Path, python: Path, electron: Path, initial_cwd: Path) -> Path:
    """Create one finite actual canonical fixture, seal it and prove real write denial.

    Args:
        directory: Existing absolute evidence directory; both owned children must be absent.
        python: Trusted isolated fixture interpreter used only before the traced application run.
        electron: Trusted fixed Electron executable recorded for process evidence.
        initial_cwd: Exact runner working directory for relative syscall interpretation.
    Returns:
        Absolute security-input.json manifest path with post-ACL source baseline.
    Raises:
        ValueError: Account is root or the output/path contract is invalid.
        OSError: Fixture creation, ACL application or evidence writing fails.
        RuntimeError: Any negative write probe unexpectedly succeeds.
    """
    directory, python, electron, initial_cwd = map(_absolute, (directory, python, electron, initial_cwd))
    if os.geteuid() == 0 or not directory.is_dir() or directory.is_symlink():
        raise ValueError('Existing owned directory and nonroot account required.')
    source, application = directory / 'synthetic-source', directory / 'application'
    source.mkdir(mode=0o700)
    application.mkdir(mode=0o700)
    completed = subprocess.run([str(python), '-I', '-B', str(REPOSITORY / 'apps/fabric-explorer/reader/test/make_fabric_fixture.py'), str(source)],
                               cwd=application, env={'LANG': 'C.UTF-8', 'PATH': ''}, capture_output=True, text=True, check=True, timeout=30)
    generated = json.loads(completed.stdout)
    findings = source / 'review.jsonl'
    shutil.copyfile(REPOSITORY / 'apps/fabric-explorer/test/fixtures/findings-review.jsonl', findings)
    # Use the maintained canonical serializer for this test-only, unsigned hostile-label variant.
    hostile = '<img src=x onerror="globalThis.__sourceExecuted=true"> <script>globalThis.__sourceExecuted=true</script>'
    script = "import hashlib,json,pathlib,sys;sys.path.insert(0,sys.argv[1]);import findings;p=pathlib.Path(sys.argv[2]);rows=[json.loads(x) for x in p.read_bytes().splitlines()];rows[0]['data']['findings'][0]['title']=sys.argv[3];previous='0'*64\nfor row in rows:\n row['prev']=previous;row['hash']=hashlib.sha256((previous+findings.canonical(row['data'])+str(row['seq'])).encode()).hexdigest();previous=row['hash']\np.write_bytes(b''.join(findings.canonical(row).encode()+b'\\n' for row in rows))"
    subprocess.run([str(python), '-I', '-B', '-c', script, str(REPOSITORY / '.ai/runtime/tools'), str(findings), hostile], cwd=application, env={'LANG': 'C.UTF-8', 'PATH': ''}, check=True, capture_output=True, timeout=10)
    marker = application / 'project-code-executed'
    sentinel = "from pathlib import Path\nPath(" + repr(str(marker)) + ").write_text('Unexpected project-controlled import')\n"
    (source / 'sitecustomize.py').write_text(sentinel)
    (source / 'usercustomize.py').write_text(sentinel)
    before = snapshot_source(source)
    _seal(source)
    baseline = snapshot_source(source)
    journal = source / generated['filename']
    probes = _negative_probes(source, journal)
    if not all(probe['denied'] for probe in probes):
        raise RuntimeError('OS write denial was not demonstrated; do not launch the product.')
    if snapshot_source(source) != baseline:
        raise RuntimeError('Negative probes changed synthetic source evidence.')
    executables = {electron, electron.resolve()}
    for name in ('chrome_crashpad_handler', 'chrome-sandbox'):
        candidate = electron.parent / name
        if candidate.is_file():
            executables.update((candidate, candidate.resolve()))
    manifest = {'format': FORMAT, 'sourceRoot': str(source), 'projectRoot': str(source),
                'fabric': str(journal), 'findings': str(findings), 'appRoot': str(application),
                'initialCwd': str(initial_cwd), 'trustedExecutables': sorted(str(path) for path in executables),
                'sourceSnapshotBefore': baseline, 'negativeWriteProbes': probes}
    output = directory / 'security-input.json'
    with output.open('x') as stream:
        json.dump(manifest, stream, indent=2)
        stream.write('\n')
    runtime_hashes = {}
    for executable in sorted(executables):
        with executable.open('rb') as stream:
            runtime_hashes[str(executable)] = hashlib.file_digest(stream, 'sha256').hexdigest()
    (directory / 'fixture-preparation.json').write_text(json.dumps({'method': 'test-driver setup before tracing', 'generated': generated, 'initialEntries': len(before), 'sealedEntries': len(baseline), 'runtimeSha256': runtime_hashes, 'acl': subprocess.run(['/usr/bin/getfacl', '--absolute-names', str(source), str(journal)], check=True, capture_output=True, text=True).stdout}, indent=2) + '\n')
    (directory / 'native-runtime-identities.json').write_text(json.dumps(native_runtime_identities(), indent=2) + '\n')
    return output


def load_manifest(path: Path) -> dict:
    """Load only the fixed owned-fixture schema, refusing path aliases and unowned roots.

    Args:
        path: Absolute regular security-input.json path produced by preparation.
    Returns:
        Manifest with roots bound to the manifest's own directory.
    Raises:
        ValueError: Shape, filename or root binding differs.
        OSError: Manifest cannot be read.
    """
    path = _absolute(path)
    if path.name != 'security-input.json' or path.is_symlink():
        raise ValueError('Fixed regular security manifest required.')
    data = json.loads(path.read_text())
    expected = {'format', 'sourceRoot', 'projectRoot', 'fabric', 'findings', 'appRoot', 'initialCwd', 'trustedExecutables', 'sourceSnapshotBefore', 'negativeWriteProbes'}
    if not isinstance(data, dict) or set(data) != expected or data['format'] != FORMAT:
        raise ValueError('Invalid qualification manifest.')
    if data['sourceRoot'] != str(path.parent / 'synthetic-source') or data['appRoot'] != str(path.parent / 'application') or data['projectRoot'] != data['sourceRoot']:
        raise ValueError('Qualification roots are not the owned fixture children.')
    for key in ('sourceRoot', 'appRoot', 'fabric', 'findings', 'initialCwd'):
        value = _absolute(data[key])
        if value.is_symlink():
            raise ValueError('Linked qualification paths are not admitted.')
    if any(Path(data[key]).parent != Path(data['sourceRoot']) for key in ('fabric', 'findings')):
        raise ValueError('Selected fixture journals must belong to the owned source root.')
    return data


def check_fixture(manifest: dict) -> dict:
    """Compare all current source bytes, entries, modes and identities before cleanup.

    Args:
        manifest: Validated fixed fixture manifest.
    Returns:
        Explicit unchanged flag and complete before/after entry sets.
    Raises:
        OSError: Current sources cannot be observed.
        ValueError: A new linked or nonregular entry is present.
    """
    after = snapshot_source(Path(manifest['sourceRoot']))
    sidecar = Path(manifest['appRoot']).parent / 'native-runtime-identities.json'
    before_runtime = json.loads(sidecar.read_text())
    after_runtime = native_runtime_identities()
    runtime = {'unchanged': before_runtime == after_runtime, 'before': before_runtime, 'after': after_runtime}
    return {'unchanged': after == manifest['sourceSnapshotBefore'] and runtime['unchanged'],
            'before': manifest['sourceSnapshotBefore'], 'after': after, 'runtimeIdentities': runtime}


def restore_fixture(manifest: dict) -> None:
    """Restore only owned same-identity fixture modes after integrity comparison, without deletion.

    Args:
        manifest: Validated fixed fixture manifest.
    Raises:
        ValueError: Any recorded path escapes, disappears or has a different physical identity.
        OSError: Mode restoration fails.
    """
    root = Path(manifest['sourceRoot'])
    for item in manifest['sourceSnapshotBefore']:
        relative = Path(item['path'])
        if relative.is_absolute() or '..' in relative.parts:
            raise ValueError('Recorded fixture path escapes its root.')
        path = root / relative
        info = path.lstat()
        if str(info.st_dev) != item['device'] or str(info.st_ino) != item['inode'] or path.is_symlink():
            raise ValueError('Refusing restoration of an unowned/replaced fixture entry.')
    for item in manifest['sourceSnapshotBefore']:
        os.chmod(root / item['path'], 0o700 if item['kind'] == 'directory' else 0o600)


def main() -> int:
    """Execute one explicit fixture operation and return nonzero for failed integrity.

    Returns:
        Zero for preparation/restoration or unchanged check; two for changed source evidence.
    Raises:
        ValueError: CLI paths/schema are invalid.
        OSError: Fixture operations fail.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='operation', required=True)
    prepare = commands.add_parser('prepare')
    for name in ('directory', 'python', 'electron', 'initial-cwd'):
        prepare.add_argument('--' + name, required=True, type=Path)
    check = commands.add_parser('check')
    check.add_argument('--manifest', required=True, type=Path)
    check.add_argument('--output', required=True, type=Path)
    restore = commands.add_parser('restore')
    restore.add_argument('--manifest', required=True, type=Path)
    args = parser.parse_args()
    if args.operation == 'prepare':
        print(prepare_fixture(args.directory, args.python, args.electron, args.initial_cwd))
    else:
        manifest = load_manifest(args.manifest)
        if args.operation == 'restore':
            restore_fixture(manifest)
        else:
            report = check_fixture(manifest)
            _absolute(args.output).write_text(json.dumps(report, indent=2) + '\n')
            return 0 if report['unchanged'] else 2
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
