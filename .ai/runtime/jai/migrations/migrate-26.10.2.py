#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Forward-only 26.10.2 -> 26.10.4 JAI-native normalization."""
from __future__ import annotations
import argparse, json
from pathlib import Path
RELEASE='26.10.4'
RETENTION_DEFAULT='inherit enterprise records/engagement retention policy'

def migrate(c):
    if c.get('version')!='3.0.0' or 'jai' not in c:
        raise ValueError(f"{c.get('id','<unknown>')}: expected ArtifactContract v3/JAI input")
    out=json.loads(json.dumps(c))
    out.setdefault('lifecycle',{})['retention']=out.get('lifecycle',{}).get('retention',RETENTION_DEFAULT)
    comp=out.setdefault('compatibility',{})
    comp['reads']=sorted(set(comp.get('reads',[])+['26.10.0/ArtifactContract-v2','26.10.1/ArtifactContract-v3','26.10.2/ArtifactContract-v3','26.10.3/ArtifactContract-v3']))
    comp['writes']='26.10.4/ArtifactContract-v3'; comp['migration']='forward-only'
    return out

def main():
    p=argparse.ArgumentParser(); p.add_argument('input'); p.add_argument('output'); a=p.parse_args()
    d=json.loads(Path(a.input).read_text()); rows=[migrate(x) for x in d.get('contracts',[d])]
    out={**d,'release':RELEASE,'authoritative_write_model':True,'native_write_enforced':True,'contracts':rows,'deliverable_count':len(rows)} if 'contracts' in d else rows[0]
    Path(a.output).write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
if __name__=='__main__': main()
