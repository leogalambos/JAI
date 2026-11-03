#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Build qualified AI IT House distribution archives for automatic publication.

Packaging is independent of Git and never traverses private input, local audit,
provider-local state or generated output directories. Maintained runtime resources and public documentation remain package inputs;
internal development reports and historical qualification results do not. Source trees must remain
unchanged during a build; symbolic links are not distribution resources. The
single declared GUIDE alias is materialized from selected public source bytes.
"""
from __future__ import annotations

import argparse, hashlib, json, zipfile, subprocess, sys, os, stat, tempfile, unicodedata
from pathlib import Path, PurePosixPath
from guide_alias import GUIDE_ALIAS, GUIDE_SOURCE, guide_bytes

TOOLS = Path(__file__).resolve().parent
PY = sys.executable

# Private workspace material must be pruned before traversal, independently of Git.
ROOT_EXCLUDED_DIRECTORIES = frozenset({"INBOX", "build", "out", "dist", "site", "obsolete"})
EXCLUDED_DIRECTORY_NAMES = frozenset({".git", ".venv", "__pycache__", ".findings", ".fabric",
                                     ".direnv", ".secrets", ".pytest_cache", ".cache", ".mypy_cache",
                                     ".ruff_cache", ".tox", "node_modules", '.aws', '.ssh',
                                     '.gnupg', '.kube', '.docker', '.config', '.local'})
PRIVATE_FILE_SUFFIXES = frozenset({".pem", ".key", ".p12", ".pfx"})
PUBLIC_ENV_EXAMPLES = frozenset({".env.example", ".env.sample", ".env.template"})
INTERNAL_RELEASE_RECORDS = frozenset({'QUALIFICATION-A-H.json', 'COMPATIBILITY.json',
                                     'PROVENANCE.json', 'SBOM.spdx.json', 'VALIDATION.md'})
PRIVATE_FILE_NAMES = frozenset({'.git', 'auth.json', 'id_rsa', 'id_ed25519',
                                '.npmrc', '.pypirc', '.netrc', 'settings-security.xml', '.claude.json',
                                'credentials', 'credentials.json'})

# The compatible component deliberately does not distribute a privileged
# worker, broker, local approval service or agent-callable Git service.
HARDENED_MODULES = frozenset({'runtime_security.py', 'runtime_linux.py',
    'runtime_service.py', 'operator_approval.py', 'runtime_staging.py',
    'runtime_qualification.py', 'git_operation.py'})

def hardened_resource(relative):
    """Identify unsupported deployment files excluded from the public component.

    Args:
        relative: Package-relative path, not an agent capability selector.
    Returns:
        True for privileged implementation, its deployment samples and tests.
    """
    path=PurePosixPath(relative)
    return (str(path).startswith('.ai/runtime/deployments/')
            or (str(path.parent)=='.ai/runtime/tools' and path.name in HARDENED_MODULES)
            or (str(path).startswith('tests/') and
                (path.name in {'test_'+name for name in HARDENED_MODULES}
                 or path.name=='test_runtime_qualification.py')))


def files(root, excluded_directory=None):
    """Yield deterministic regular distribution files without traversing private trees.

    Args:
        root: Existing package source directory; symbolic-link roots are rejected.
        excluded_directory: Optional output directory whose subtree must not be packaged.
    Yields:
        Regular nonsymlink paths below root, in deterministic directory/file order.
        Private/generated directories are pruned before descent, independent of Git.
    Raises:
        ValueError: If root is a symbolic link or is not a directory.
        OSError: If a traversed maintained directory cannot be enumerated.
    """
    root = Path(root)
    if root.is_symlink() or not root.is_dir():
        raise ValueError("package root must be a real directory")
    root = root.resolve()
    excluded_directory = Path(excluded_directory).resolve() if excluded_directory else None

    def excluded(path):
        relative = path.relative_to(root)
        return (bool(excluded_directory and path.is_relative_to(excluded_directory))
                or bool(relative.parts and relative.parts[0] in ROOT_EXCLUDED_DIRECTORIES)
                or any(part in EXCLUDED_DIRECTORY_NAMES for part in relative.parts)
                or relative.as_posix() in {".ai/runtime/_meta/gates",
                    ".ai/runtime/evals/content_quality/enterprise"})

    def walk_error(error):
        raise error

    for directory, subdirectories, names in os.walk(root, topdown=True, followlinks=False,
                                                  onerror=walk_error):
        directory = Path(directory)
        if excluded(directory):
            subdirectories[:] = []
            continue
        subdirectories[:] = sorted(name for name in subdirectories
                                   if not (directory / name).is_symlink()
                                   and not excluded(directory / name))
        for name in sorted(names):
            path = directory / name
            relative = path.relative_to(root).as_posix()
            if (hardened_resource(relative) or name in PRIVATE_FILE_NAMES or path.is_symlink() or not path.is_file() or path.suffix == ".pyc"
                    or name == "AGENTS.md"
                    or ("/" not in relative and path.suffix in {".zip", ".log", ".tmp"})
                    or path.suffix in PRIVATE_FILE_SUFFIXES
                    or ((name == ".env" or name.startswith(".env.")) and name not in PUBLIC_ENV_EXAMPLES)
                    or ("/" not in relative and name in INTERNAL_RELEASE_RECORDS)
                    or relative in {".claude/settings.local.json", ".codex/config.local.toml",
                                    '.codex/config.toml', '.claude/settings.json',
                                    ".ai/runtime/_meta/qualification-A-G.json"}):
                continue
            yield path



def dependency_closure(root):
    """Reject references to retired non-optional modules in shipped Python files.

    Actual mandatory-module imports and installed regressions are also required
    at distribution acceptance; static closure alone is not product acceptance.
    """
    import ast
    root=Path(root);problems=[];retired={Path(name).stem for name in HARDENED_MODULES}
    for path in files(root):
        if path.suffix!='.py':continue
        for node in ast.walk(ast.parse(path.read_text(encoding='utf-8'))):
            names=[n.name.split('.')[0] for n in node.names] if isinstance(node,ast.Import) else ([node.module.split('.')[0]] if isinstance(node,ast.ImportFrom) and node.module else [])
            for name in names:
                if name in retired:problems.append(str(path.relative_to(root))+': absent retired dependency '+name)
    if problems:raise ValueError('distribution dependency closure failed: '+str(problems))
    return True


def check_ready(root):
    """Validate current source contracts before constructing a distribution.

    Args:
        root: Reviewed source checkout; no archived result grants readiness.
    Returns:
        Authoritative product version after identity, documentation and source
        dependency checks. Comprehensive tests remain a separate local operator
        prerequisite before publication.
    Raises:
        ValueError: Required public sources, synchronized identity or contracts
            are missing or invalid. No package output is created here.
        OSError: Maintained source files cannot be read.
    """
    root = Path(root).resolve()
    policy = json.loads((root / '.ai/runtime/release/release-policy.json').read_text())
    if policy.get('signing', {}).get('mode') != 'automated-ci-release':
        raise ValueError('automated release policy required')
    for relative in policy.get('required_release_files', []):
        if not _safe_member(relative) or not (root / relative).is_file():
            raise ValueError('required release source missing: ' + str(relative))
    for command in (
            [PY, str(root / 'scripts/versioning.py'), 'check', '--root', str(root)],
            [PY, str(root / '.ai/runtime/tools/docs_contract.py'), '--root', str(root)]):
        result = subprocess.run(command, cwd=root, capture_output=True, text=True)
        if result.returncode:
            raise ValueError('release source contract failed: ' + (result.stdout + result.stderr).strip())
    dependency_closure(root)
    return (root / 'VERSION').read_text().strip()


def _safe_member(name):
    if not isinstance(name, str):
        return False
    path = PurePosixPath(name)
    reserved = {'CON', 'PRN', 'AUX', 'NUL', *('COM' + str(n) for n in range(1, 10)),
                *('LPT' + str(n) for n in range(1, 10))}
    return (bool(name) and not path.is_absolute()
            and str(path) == name and all(part not in {'', '.', '..'} for part in path.parts)
            and all(part.rstrip(' .') == part and part.split('.')[0].upper() not in reserved
                    for part in path.parts)
            and not any(char in name for char in ('\\', ':', '\x00'))
            and not any(ord(char) < 32 or ord(char) == 127 for char in name))


def _read_resource(root, relative):
    if not _safe_member(relative) or os.open not in os.supports_dir_fd:
        raise ValueError('secure relative resource access unavailable')
    current = os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        parts = PurePosixPath(relative).parts
        for part in parts[:-1]:
            following = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=current)
            os.close(current)
            current = following
        descriptor = os.open(parts[-1], os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=current)
        with os.fdopen(descriptor, 'rb') as resource:
            before = os.fstat(resource.fileno())
            if not stat.S_ISREG(before.st_mode):
                raise ValueError('distribution resources must be regular files')
            data = resource.read()
            after = os.fstat(resource.fileno())
            identity = lambda item: (item.st_dev, item.st_ino, item.st_size, item.st_mtime_ns, item.st_ctime_ns)
            if identity(before) != identity(after):
                raise ValueError('distribution resource changed while reading')
            return data, before.st_mode & 0o777
    finally:
        os.close(current)


def _snapshot(root, excluded_directory):
    output = {}
    portable = set()
    for path in files(root, excluded_directory):
        relative = path.relative_to(root).as_posix()
        folded = unicodedata.normalize('NFC', relative).casefold()
        if not _safe_member(relative) or folded in portable:
            raise ValueError('unsafe or duplicate portable archive member')
        portable.add(folded)
        output[relative] = _read_resource(root, relative)
    if GUIDE_ALIAS in output or GUIDE_SOURCE in output:
        if GUIDE_SOURCE not in output:
            raise ValueError('GUIDE canonical public resource was not selected')
        canonical_bytes = output[GUIDE_SOURCE][0]
        alias_bytes = output[GUIDE_ALIAS][0] if GUIDE_ALIAS in output else None
        output[GUIDE_ALIAS] = (guide_bytes(root, canonical_bytes, alias_bytes), 0o644)
    return output


def verify_zip(path, expected=None, maximum_uncompressed_bytes=256 * 1024 * 1024):
    """Validate bounded regular archive members and optionally their exact hashes.

    Args:
        path: Existing ZIP to inspect, never extracted by this function.
        expected: Optional complete member-name to SHA-256 mapping from the
            independently frozen source manifest; partial coverage is refused.
        maximum_uncompressed_bytes: Positive total uncompressed size ceiling.
    Returns:
        Member count and exact member hashes after CRC, path, duplicate and mode
        validation. This is archive integrity, not release qualification/signing.
    Raises:
        ValueError: Unsafe names, duplicates, nonregular modes, size excess or
            expected-hash mismatch. Empty archives are refused.
        OSError, zipfile.BadZipFile: Archive cannot be read or CRC is invalid.
    """
    if type(maximum_uncompressed_bytes) is not int or maximum_uncompressed_bytes <= 0:
        raise ValueError('positive archive size limit required')
    observed, portable, total = {}, set(), 0
    with zipfile.ZipFile(path) as archive:
        for member in archive.infolist():
            normalized = unicodedata.normalize('NFC', member.filename).casefold()
            mode = member.external_attr >> 16
            if (not _safe_member(member.filename) or normalized in portable
                    or member.is_dir() or stat.S_IFMT(mode) not in {0, stat.S_IFREG}):
                raise ValueError('unsafe, duplicate or nonregular archive member')
            portable.add(normalized)
            total += member.file_size
            if total > maximum_uncompressed_bytes:
                raise ValueError('archive uncompressed size limit exceeded')
            observed[member.filename] = hashlib.sha256(archive.read(member)).hexdigest()
    if not observed or (expected is not None and observed != expected):
        raise ValueError('archive does not match the complete frozen source manifest')
    return {'member_count': len(observed), 'members': observed}


def build_zip(root,out,prefix):
    """Write deterministic ZIP entries from the explicit distribution resource contract.

    Args:
        root: Package source directory, unchanged throughout this operation.
        out: Destination ZIP path; its parent subtree is excluded from input discovery.
        prefix: One safe archive root component supplied by the release builder.
    Returns:
        None. A complete frozen snapshot is verified again before an exclusive
        atomic publication. File bytes, stable timestamps and safe source modes
        are recorded. No partially written archive survives a failed build.
    Raises:
        OSError: If a resource cannot be opened safely or the archive cannot be written.
        ValueError: If the source is invalid or a resource is not a regular file.
    """
    root = Path(root)
    if not _safe_member(prefix) or len(PurePosixPath(prefix).parts) != 1:
        raise ValueError('one safe archive prefix component required')
    if root.is_symlink():
        raise ValueError("package root must be a real directory")
    root = root.resolve()
    out = Path(out).absolute()
    if root.is_relative_to(out.parent.resolve()):
        raise ValueError("archive output directory must not equal or contain the package source")
    if out.exists() or out.is_symlink():
        raise FileExistsError(out)
    snapshot = _snapshot(root, out.parent)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(prefix='.jai-package-', suffix='.tmp', dir=out.parent, delete=False) as stream:
            temporary = Path(stream.name)
        with zipfile.ZipFile(temporary, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            for relative, (data, mode) in snapshot.items():
                info = zipfile.ZipInfo(f'{prefix}/{relative}')
                info.date_time = (1980, 1, 1, 0, 0, 0)
                info.external_attr = (stat.S_IFREG | mode) << 16
                info.compress_type, info.create_system = zipfile.ZIP_DEFLATED, 3
                archive.writestr(info, data)
        expected = {f'{prefix}/{relative}': hashlib.sha256(data).hexdigest()
                    for relative, (data, _) in snapshot.items()}
        verify_zip(temporary, expected)
        if _snapshot(root, out.parent) != snapshot:
            raise ValueError('distribution source changed during build')
        # Hard-link publication has O_EXCL semantics; never replace an existing
        # destination created after the initial check.
        os.link(temporary, out)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def build(root, dist):
    """Build the current version's deterministic archive and checksum locally.

    Args:
        root: Source checkout satisfying current public source contracts.
        dist: Local output directory, excluded from archive traversal.
    Returns:
        Archive and checksum paths. No Git operation, signing or publication is
        performed. Comprehensive local regressions are an operator prerequisite;
        the release workflow separately enforces its bounded source checks.
    Raises:
        OSError, ValueError: Source checks, archive construction or exclusive
            output creation fails. Existing output files are never overwritten.
    """
    version = check_ready(root)
    destination = Path(dist).absolute()
    archive = destination / ('ai-it-house-universal-' + version + '.zip')
    checksum = archive.with_suffix('.sha256')
    if archive.exists() or checksum.exists():
        raise FileExistsError('release outputs already exist; use a fresh directory')
    destination.mkdir(parents=True, exist_ok=True)
    build_zip(root, archive, 'ai-it-house-universal-' + version)
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    with checksum.open('x', encoding='utf-8') as stream:
        stream.write(digest + '  ' + archive.name + '\n')
    return {'archive': str(archive), 'checksum': str(checksum)}


def main():
    """Dispatch explicit build arguments without publication or authority acts.

    Returns:
        Build exit status.
    Raises:
        SystemExit: For invalid arguments or unmet qualification prerequisites.
    """
    ap=argparse.ArgumentParser(); ap.add_argument('cmd',choices=['build','check-closure']); ap.add_argument('--root',required=True); ap.add_argument('--dist'); a=ap.parse_args()
    if a.cmd=='check-closure':dependency_closure(a.root);print('PASS distribution dependency closure');return 0
    if not a.dist:ap.error('--dist required for build')
    print(json.dumps(build(a.root,a.dist), sort_keys=True)); return 0


if __name__=='__main__': raise SystemExit(main())
