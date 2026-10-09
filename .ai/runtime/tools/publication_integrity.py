#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Verify publication-model fidelity to a ProjectionManifest v2 and rendered output hashes."""
import argparse, hashlib, json, tempfile
from pathlib import Path
def canonical(x): return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def sha(x): return hashlib.sha256(canonical(x)).hexdigest()
def file_sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def check(pub,man,rendered=None):
    probs=[]
    if man.get('projection_hash')!=sha(pub): probs.append('publication model does not match projection_hash')
    if man.get('mandatory_coverage')!=100: probs.append('mandatory publication coverage is not 100%')
    claims={c.get('id') for c in pub.get('claims',[]) if c.get('id')}; evidence=set(pub.get('evidence',[]))
    for c in pub.get('claims',[]): evidence.update(c.get('evidence',[]))
    for mapping in man.get('mappings',[]):
        src=mapping.get('source','')
        if src.startswith('claim:') and src.split(':',1)[1] not in claims: probs.append(f'mapped claim missing: {src}')
        if src.startswith('evidence:') and src.split(':',1)[1] not in evidence: probs.append(f'mapped evidence missing: {src}')
    if rendered:
        expected=(man.get('render') or {}).get('render_hash')
        if expected and expected!=file_sha(rendered): probs.append('render hash mismatch')
    return probs
def self_test():
    pub={'claims':[{'id':'C1','statement':'approved','evidence':['E1']}],'evidence':['E1']}
    man={'projection_hash':sha(pub),'mandatory_coverage':100,'mappings':[{'source':'claim:C1','destination':'claims[0]'},{'source':'evidence:E1','destination':'evidence[0]'}],'render':{}}
    if check(pub,man): print('FAIL valid projection rejected'); return 1
    bad=json.loads(json.dumps(man)); bad['mandatory_coverage']=99
    if not check(pub,bad): print('FAIL incomplete projection accepted'); return 1
    bad=json.loads(json.dumps(man)); bad['mappings'].append({'source':'claim:MISSING','destination':'claims[1]'})
    if not check(pub,bad): print('FAIL missing mapped claim accepted'); return 1
    with tempfile.TemporaryDirectory() as td:
        f=Path(td)/'render'; f.write_bytes(b'render'); ok=json.loads(json.dumps(man)); ok['render']={'render_hash':file_sha(f)}
        if check(pub,ok,f): print('FAIL valid render hash rejected'); return 1
        f.write_bytes(b'tampered')
        if not check(pub,ok,f): print('FAIL render tamper accepted'); return 1
    print('PASS publication integrity: coverage, claim/evidence mapping and render hash tamper detection'); return 0
def main():
    ap=argparse.ArgumentParser(); sub=ap.add_subparsers(dest='cmd'); sub.add_parser('self-test'); ap.add_argument('publication_model',nargs='?'); ap.add_argument('manifest',nargs='?'); ap.add_argument('--rendered'); a=ap.parse_args()
    if a.cmd=='self-test': raise SystemExit(self_test())
    if not a.publication_model or not a.manifest: ap.error('publication_model and manifest are required')
    probs=check(load(a.publication_model),load(a.manifest),a.rendered); [print('FAIL',p) for p in probs]; print('PASS' if not probs else 'FAILED'); raise SystemExit(bool(probs))
if __name__=='__main__': main()
