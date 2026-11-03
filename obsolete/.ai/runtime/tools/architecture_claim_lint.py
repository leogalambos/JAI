#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Release-blocking lint for JAI authority scope and active legacy write/schema paths."""
from __future__ import annotations
from pathlib import Path
import re
PACKAGE=Path(__file__).resolve().parents[3]
RUNTIME=Path(__file__).resolve().parents[1]
RELEASE=((PACKAGE/'VERSION') if (PACKAGE/'VERSION').is_file() else RUNTIME/'VERSION').read_text().strip()

STATIC=[
 PACKAGE/'README.md', RUNTIME/'README.md', RUNTIME/'ea/README.md', RUNTIME/'ea/adapters/README.md', RUNTIME/'publication/README.md',
 PACKAGE/'.ai/agents/architecture-repository-engineer.md', PACKAGE/'.ai/commands/repository.md',
 PACKAGE/'.ai/skills/it-role-workflows/references/architecture-model-to-repository-governance.md',
]
FORBIDDEN=[
 ('v2-production-authority',re.compile(r'authoritative Artifact Contract v2|Artifact Contract v2 binds',re.I)),
 ('unscoped-ea-source-of-truth',re.compile(r'(canonical (EA )?repository|repository JSON).{0,50}(persistent )?source of truth',re.I)),
 ('stale-3.6-ea',re.compile(r'3\.6 canonical EA repository',re.I)),
]
ACTIVE_TOOLS=['integration_adapters.py','execution_record.py','behavioral_eval.py','agent_runtime.py','repository.py','sabsa_ea.py']
LEGACY_SCHEMA_REFS=[r"integrations/adapter-contract\.schema",r"audit/execution-record\.schema",r"evals/evaluation-(case|result)\.schema",r"schema/26\.10/"]

def main():
    problems=[]
    for p in STATIC:
        if not p.is_file(): problems.append(f'missing static authority surface {p.relative_to(PACKAGE)}'); continue
        text=p.read_text(encoding='utf-8')
        for name,pat in FORBIDDEN:
            if pat.search(text): problems.append(f'{p.relative_to(PACKAGE)}: {name}')
    for p in PACKAGE.glob('.ai/skills/**/references/*.md'):
        text=p.read_text(encoding='utf-8')
        if 'Every Section 6 row is registered in Artifact Contract v2' in text: problems.append(f'{p.relative_to(PACKAGE)}: stale Artifact Contract v2 authority')
        if '3.6 canonical EA repository' in text: problems.append(f'{p.relative_to(PACKAGE)}: stale 3.6 EA authority')
    for name in ACTIVE_TOOLS:
        p=RUNTIME/'tools'/name; text=p.read_text(encoding='utf-8')
        for pat in LEGACY_SCHEMA_REFS:
            if re.search(pat,text): problems.append(f'tools/{name}: active legacy schema path {pat}')
    repo=(RUNTIME/'tools/repository.py').read_text(encoding='utf-8')
    if '"schema_version": "26.10"' in repo or "'schema_version':'26.10'" in repo: problems.append('repository.py: native write still hard-codes schema_version 26.10')
    sab=(RUNTIME/'tools/sabsa_ea.py').read_text(encoding='utf-8')
    for token in ("'canonical_ref':","'jai':","'source_specialisations':","BRIDGE='sabsa-ea-jai-profile'"):
        if token not in sab: problems.append(f'sabsa_ea.py: missing profile-native token {token}')
    if problems:
        for x in problems: print('FAIL',x)
        return 1
    print(f'PASS architecture claim lint: JAI authority/write-path claims scoped for {RELEASE}')
    return 0
if __name__=='__main__': raise SystemExit(main())
