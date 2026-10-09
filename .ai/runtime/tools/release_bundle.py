#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Build qualified AI IT House distribution archives for automatic publication."""
from __future__ import annotations

import argparse, hashlib, json, zipfile, subprocess, sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
PY = sys.executable


def files(root, excluded_directory=None):
    root = Path(root).resolve()
    excluded_directory = Path(excluded_directory).resolve() if excluded_directory else None
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(root).as_posix()
        if excluded_directory and path.is_relative_to(excluded_directory):
            continue
        if rel.split('/')[0] in {"dist", "site", ".venv", ".git"}:
            continue
        if "__pycache__" in path.parts or path.suffix == ".pyc":
            continue
        if rel == ".ai/runtime/_meta/qualification-A-G.json":
            continue
        if rel.startswith(".ai/runtime/_meta/gates/"):
            continue
        yield path


def check_ready(root):
    root=Path(root)
    if subprocess.run([PY,str(TOOLS/'release_policy.py'),'check','--final'],cwd=root).returncode:
        raise SystemExit('release policy is not final-ready')
    q=json.loads((root/'QUALIFICATION-A-H.json').read_text())
    if not q.get('all_pass') or set(q.get('gates',{})) != set('ABCDEFGH') or not all(q['gates'].values()):
        raise SystemExit('QUALIFICATION-A-H.json is not all PASS')


def build_zip(root,out,prefix):
    with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as zf:
        for path in files(root, out.parent):
            rel=path.relative_to(root).as_posix(); info=zipfile.ZipInfo(f'{prefix}/{rel}')
            info.date_time=(1980,1,1,0,0,0); info.external_attr=((path.stat().st_mode & 0o777)&0xFFFF)<<16; info.compress_type=zipfile.ZIP_DEFLATED; info.create_system=3
            zf.writestr(info,path.read_bytes())


def build(root,dist):
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
    ap=argparse.ArgumentParser(); ap.add_argument('cmd',choices=['build']); ap.add_argument('--root',required=True); ap.add_argument('--dist',required=True); a=ap.parse_args(); return build(a.root,a.dist)


if __name__=='__main__': raise SystemExit(main())
