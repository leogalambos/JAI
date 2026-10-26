#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Build qualified AI IT House distribution archives for automatic publication.

Packaging is independent of Git and never traverses private input, local audit,
provider-local state or generated output directories. Maintained runtime resources
and required qualification evidence remain package inputs. Source trees must remain
unchanged during a build; symbolic links are not distribution resources.
"""
from __future__ import annotations

import argparse, hashlib, json, zipfile, subprocess, sys, os, stat, tempfile, unicodedata
from pathlib import Path, PurePosixPath

TOOLS = Path(__file__).resolve().parent
PY = sys.executable

# Keep this contract explicit: release evidence may be Git-ignored but is required
# in a qualified archive, whereas private workspace material must never be visited.
ROOT_EXCLUDED_DIRECTORIES = frozenset({"INBOX", "build", "out", "dist", "site"})
EXCLUDED_DIRECTORY_NAMES = frozenset({".git", ".venv", "__pycache__", ".findings", ".fabric",
                                     ".direnv", ".secrets", ".pytest_cache", ".cache", ".mypy_cache",
                                     ".ruff_cache", ".tox", "node_modules", '.aws', '.ssh',
                                     '.gnupg', '.kube', '.docker', '.config', '.local'})
PRIVATE_FILE_SUFFIXES = frozenset({".pem", ".key", ".p12", ".pfx"})
PUBLIC_ENV_EXAMPLES = frozenset({".env.example", ".env.sample", ".env.template"})
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
    """Require current-release executed A-H evidence before a qualified build.

    Args:
        root: Distribution source containing VERSION and qualification evidence.
    Returns:
        None only when release policy and every current gate pass, source bytes
        match the verified SBOM/provenance, and the provenance A-G execution
        records agree with the final qualification. Same-version historical PASS
        files alone never authorize a changed tree.
    Raises:
        SystemExit: If policy, identity, gate coverage or execution is non-passing.
        OSError, ValueError: If required local evidence cannot be processed.
    """
    from qualification_core import gate_report_problems, source_fingerprint
    from schema_resolver import release_scope
    scope=release_scope(root)
    root=Path(root)
    if subprocess.run([PY,str(TOOLS/'release_policy.py'),'check','--final'],cwd=root).returncode:
        raise SystemExit('release policy is not final-ready')
    q=json.loads((root/'QUALIFICATION-A-H.json').read_text())
    release=(root/'VERSION').read_text().strip()
    if (not isinstance(q,dict) or q.get('all_pass') is not True
            or q.get('release')!=release or not isinstance(q.get('gates'),dict)
            or not isinstance(q.get('checks'),dict)
            or set(q['gates'])!=set('ABCDEFGH') or set(q['checks'])!=set('ABCDEFGH')):
        raise SystemExit('QUALIFICATION-A-H.json is not current-release all PASS')
    if q.get('supported_capabilities')!=scope:
        raise SystemExit('qualification release scope disagrees with canonical manifest')
    fingerprint=source_fingerprint(root)
    for gate in 'ABCDEFGH':
        if gate_report_problems({'gate':gate,'release':q['release'],'pass':q['gates'][gate],
                                 'checks':q['checks'][gate],'source_binding':q.get('source_bindings',{}).get(gate)},gate,release,fingerprint):
            raise SystemExit('QUALIFICATION-A-H.json lacks current-release all PASS execution')
    import supply_chain
    try:
        supply_chain.verify(root, root/'SBOM.spdx.json', root/'PROVENANCE.json', root/'COMPATIBILITY.json')
        provenance = json.loads((root/'PROVENANCE.json').read_text())
    except (OSError, ValueError, KeyError, TypeError) as exc:
        raise SystemExit('release source integrity prerequisite failed') from exc
    source = provenance.get('test_results', {})
    if (not isinstance(source, dict) or source.get('release') != release
            or source.get('gates') != {g: q['gates'][g] for g in 'ABCDEFG'}
            or source.get('checks') != {g: q['checks'][g] for g in 'ABCDEFG'}
            or source.get('source_bindings') != {g: q['source_bindings'][g] for g in 'ABCDEFG'}):
        raise SystemExit('source provenance qualification does not match final A-G execution')


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


def build(root,dist):
    """Build an exclusive deterministic qualified archive and companion digest.

    Args:
        root: Source distribution with current executed qualification evidence.
        dist: Output directory excluded from archive input discovery.
    Returns:
        Zero after writing the archive and its SHA-256 companion.
    Raises:
        SystemExit: If qualification fails or the artifact already exists.
        OSError, ValueError: If sources or destinations cannot be processed.
    """
    root=Path(root).resolve(); dist=Path(dist).resolve(); dependency_closure(root); check_ready(root)
    version=(root/'VERSION').read_text().strip(); prefix=f'ai-it-house-{version}'; base=f'ai-it-house-universal-{version}'
    dist.mkdir(parents=True,exist_ok=True)
    archive=dist/f'{base}.zip'
    if archive.exists():
        raise SystemExit(f'release artifact already exists: {archive}; refuse accidental overwrite')
    build_zip(root,archive,prefix)
    digest=hashlib.sha256(archive.read_bytes()).hexdigest()
    (dist/f'{base}.sha256').write_text(f'{digest}  {archive.name}\n', encoding='utf-8')
    print(f'PASS production ZIP built {version}: SHA-256 {digest}')
    print(archive)
    return 0


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
    return build(a.root,a.dist)


if __name__=='__main__': raise SystemExit(main())
