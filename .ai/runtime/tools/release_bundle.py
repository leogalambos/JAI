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

import argparse, hashlib, json, zipfile, subprocess, sys, os, stat
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
PY = sys.executable

# Keep this contract explicit: release evidence may be Git-ignored but is required
# in a qualified archive, whereas private workspace material must never be visited.
ROOT_EXCLUDED_DIRECTORIES = frozenset({"INBOX", "build", "out", "dist", "site"})
EXCLUDED_DIRECTORY_NAMES = frozenset({".git", ".venv", "__pycache__", ".findings", ".fabric",
                                     ".direnv", ".secrets", ".pytest_cache", ".cache", ".mypy_cache",
                                     ".ruff_cache", ".tox", "node_modules"})
PRIVATE_FILE_SUFFIXES = frozenset({".pem", ".key", ".p12", ".pfx"})
PUBLIC_ENV_EXAMPLES = frozenset({".env.example", ".env.sample", ".env.template"})


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
            if (path.is_symlink() or not path.is_file() or path.suffix == ".pyc"
                    or name == "AGENTS.md"
                    or ("/" not in relative and path.suffix in {".zip", ".log", ".tmp"})
                    or path.suffix in PRIVATE_FILE_SUFFIXES
                    or ((name == ".env" or name.startswith(".env.")) and name not in PUBLIC_ENV_EXAMPLES)
                    or relative in {".claude/settings.local.json", ".codex/config.local.toml",
                                    ".ai/runtime/_meta/qualification-A-G.json"}):
                continue
            yield path


def check_ready(root):
    """Require current-release executed A-H evidence before a qualified build.

    Args:
        root: Distribution source containing VERSION and qualification evidence.
    Returns:
        None only when release policy and every actual current gate pass.
    Raises:
        SystemExit: If policy, identity, gate coverage or execution is non-passing.
        OSError, ValueError: If required local evidence cannot be processed.
    """
    from qualification_core import gate_report_problems
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
    for gate in 'ABCDEFGH':
        if gate_report_problems({'gate':gate,'release':q['release'],'pass':q['gates'][gate],
                                 'checks':q['checks'][gate]},gate,release):
            raise SystemExit('QUALIFICATION-A-H.json lacks current-release all PASS execution')


def build_zip(root,out,prefix):
    """Write deterministic ZIP entries from the explicit distribution resource contract.

    Args:
        root: Package source directory, unchanged throughout this operation.
        out: Destination ZIP path; its parent subtree is excluded from input discovery.
        prefix: Archive root directory name supplied by the release builder.
    Returns:
        None. File bytes, stable timestamps and source permission bits are recorded.
    Raises:
        OSError: If a resource cannot be opened safely or the archive cannot be written.
        ValueError: If the source is invalid or a resource is not a regular file.
    """
    root = Path(root)
    if root.is_symlink():
        raise ValueError("package root must be a real directory")
    root = root.resolve()
    out = Path(out).absolute()
    if root.is_relative_to(out.parent.resolve()):
        raise ValueError("archive output directory must not equal or contain the package source")
    with zipfile.ZipFile(out,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as zf:
        for path in files(root, out.parent):
            flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
            with os.fdopen(os.open(path, flags), "rb") as resource:
                properties = os.fstat(resource.fileno())
                if not stat.S_ISREG(properties.st_mode):
                    raise ValueError("distribution resources must be regular files")
                data = resource.read()
            rel=path.relative_to(root).as_posix(); info=zipfile.ZipInfo(f'{prefix}/{rel}')
            info.date_time=(1980,1,1,0,0,0); info.external_attr=((properties.st_mode & 0o777)&0xFFFF)<<16; info.compress_type=zipfile.ZIP_DEFLATED; info.create_system=3
            zf.writestr(info,data)


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
    root=Path(root).resolve(); dist=Path(dist).resolve(); check_ready(root)
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
    ap=argparse.ArgumentParser(); ap.add_argument('cmd',choices=['build']); ap.add_argument('--root',required=True); ap.add_argument('--dist',required=True); a=ap.parse_args(); return build(a.root,a.dist)


if __name__=='__main__': raise SystemExit(main())
