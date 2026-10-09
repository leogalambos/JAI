#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""License-policy validator for AI IT House."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[3]
SPDX='SPDX-License-Identifier: BSD-4-Clause'
COPY='Copyright (c) 2026 Leo Galambos and the Egothor team'
FULL_SENTENCE='Redistribution and use in source and binary forms'

def check(root=ROOT):
    root=Path(root); probs=[]; lic=root/'LICENSE'
    if not lic.is_file(): probs.append('root LICENSE missing')
    else:
        t=lic.read_text(encoding='utf-8')
        for token in ('BSD 4-Clause License','Egothor team','Leo Galambos','https://www.egothor.org',FULL_SENTENCE):
            if token not in t: probs.append(f'LICENSE missing {token!r}')
    for p in root.rglob('*'):
        if not p.is_file() or '__pycache__' in p.parts: continue
        rel=p.relative_to(root).as_posix()
        if rel in {'LICENSE','SBOM.spdx.json','PROVENANCE.json','COMPATIBILITY.json'}: continue
        # AI-consumed knowledge/prompt material intentionally avoids repetitive headers.
        if rel.startswith('.ai/skills/') or rel.startswith('.ai/agents/') or rel.startswith('.ai/commands/'):
            try:
                txt=p.read_text(encoding='utf-8')
                if FULL_SENTENCE in txt: probs.append(f'{rel}: full license boilerplate must not consume AI context')
            except Exception: pass
            continue
        if p.suffix in {'.py','.sh','.yaml','.yml','.cmd'}:
            try: head='\n'.join(p.read_text(encoding='utf-8',errors='replace').splitlines()[:8])
            except Exception: continue
            if SPDX not in head: probs.append(f'{rel}: compact SPDX header missing')
            if COPY not in head: probs.append(f'{rel}: compact copyright header missing')
            lines=p.read_text(encoding='utf-8',errors='replace').splitlines()
            if lines and any(line.startswith('#!') for line in lines[:8]):
                if not lines[0].startswith('#!'):
                    probs.append(f'{rel}: shebang must remain the first line')
    # Old internal-use metadata would contradict the release licence.
    for p in (root/'.ai').rglob('*.md'):
        if 'licence: internal-use' in p.read_text(encoding='utf-8',errors='replace'): probs.append(f'{p.relative_to(root)}: stale internal-use licence metadata')
    return probs

def main():
    root=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT; p=check(root)
    [print('FAIL',x) for x in p]
    if not p: print('PASS BSD-4-Clause license policy: root full text + compact source headers + AI-context exemption')
    return 1 if p else 0
if __name__=='__main__': raise SystemExit(main())
