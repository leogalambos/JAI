#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Validate licensing of release-owned sources, excluding private workspace inputs.

The release packager owns the traversal policy: INBOX and generated/private trees
are pruned before descent. This gate does not license or inspect private inputs.
"""
import importlib.util
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[3]
SPDX='SPDX-License-Identifier: BSD-4-Clause'
COPY='Copyright (c) 2026 Leo Galambos and the Egothor team'
FULL_SENTENCE='Redistribution and use in source and binary forms'

def _distribution_files(root):
    spec = importlib.util.spec_from_file_location(
        '_jai_license_release_bundle', Path(__file__).with_name('release_bundle.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.files(root)

def check(root=ROOT):
    """Return policy violations for the root licence and packaged source files.

    Args:
        root: Existing release source directory; private inputs are not traversed.
    Returns:
        A list of diagnostics, empty when every applicable policy passes.
    Raises:
        OSError: If maintained input cannot be enumerated or read.
        ValueError: If the root is not a real distribution directory.
    """
    root = Path(root)
    if root.is_symlink():
        raise ValueError('release source root must not be a symbolic link')
    root = root.resolve()
    probs=[]; lic=root/'LICENSE'
    if not lic.is_file(): probs.append('root LICENSE missing')
    else:
        t=lic.read_text(encoding='utf-8')
        for token in ('BSD 4-Clause License','Egothor team','Leo Galambos','https://www.egothor.org',FULL_SENTENCE):
            if token not in t: probs.append(f'LICENSE missing {token!r}')
    for p in _distribution_files(root):
        rel=p.relative_to(root).as_posix()
        if rel in {'LICENSE','SBOM.spdx.json','PROVENANCE.json','COMPATIBILITY.json'}: continue
        if rel.startswith('.ai/') and p.suffix == '.md':
            if 'licence: internal-use' in p.read_text(encoding='utf-8',errors='replace'):
                probs.append(f'{rel}: stale internal-use licence metadata')
        # AI-consumed knowledge/prompt material intentionally avoids repetitive headers.
        if rel.startswith('.ai/skills/') or rel.startswith('.ai/agents/') or rel.startswith('.ai/commands/'):
            txt=p.read_text(encoding='utf-8')
            if FULL_SENTENCE in txt: probs.append(f'{rel}: full license boilerplate must not consume AI context')
            continue
        if p.suffix in {'.py','.sh','.yaml','.yml','.cmd'}:
            head='\n'.join(p.read_text(encoding='utf-8',errors='replace').splitlines()[:8])
            if SPDX not in head: probs.append(f'{rel}: compact SPDX header missing')
            if COPY not in head: probs.append(f'{rel}: compact copyright header missing')
            lines=p.read_text(encoding='utf-8',errors='replace').splitlines()
            if lines and any(line.startswith('#!') for line in lines[:8]):
                if not lines[0].startswith('#!'):
                    probs.append(f'{rel}: shebang must remain the first line')
    return probs

def main():
    """Print diagnostics for an optional CLI root and return zero only on success."""
    root=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT; p=check(root)
    [print('FAIL',x) for x in p]
    if not p: print('PASS BSD-4-Clause license policy: root full text + compact source headers + AI-context exemption')
    return 1 if p else 0
if __name__=='__main__': raise SystemExit(main())
