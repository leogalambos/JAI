#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""JAI-profile-native tamper-evident Execution Record support for AI IT House."""
from __future__ import annotations
import argparse, datetime as dt, hashlib, json, tempfile, uuid
from pathlib import Path
try: import jsonschema
except Exception: jsonschema=None
RUNTIME=Path(__file__).resolve().parents[1]
import schema_resolver
SCHEMA_NAME='ExecutionRecord'
PACKAGE=RUNTIME.parents[1]
RELEASE=((PACKAGE/'VERSION') if (PACKAGE/'VERSION').is_file() else RUNTIME/'VERSION').read_text().strip()
L6_ACCEPTANCE='Is the observable result evidenced, attributable, reproducible and suitable for authority review?'

def jai_binding(agent, input_refs, outputs):
    return {'core_version':'1.0.0','layer':6,'layer_name':'Execution and Evidence','profile':'runtime',
            'responsibility':'Record attributable runtime effects and evidence for authority review',
            'input_refs':list(input_refs),'output_refs':list(outputs),
            'authority_ref':f'agent:{agent}' if agent else None,'acceptance_question':L6_ACCEPTANCE,
            'evidence_obligations':['source hashes','tool/effect observations','output hashes','exceptions']}


def canonical(o): return json.dumps(o,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def digest_record(o):
    x=dict(o); x.pop('record_hash',None); return hashlib.sha256(canonical(x)).hexdigest()
def validate(o):
    if jsonschema: jsonschema.Draft202012Validator(schema_resolver.schema(SCHEMA_NAME)).validate(o)
    if o.get('record_hash')!=digest_record(o): raise ValueError('record_hash mismatch')
    return True

def make(**kw):
    now=dt.datetime.now(dt.timezone.utc).isoformat().replace('+00:00','Z')
    agent=kw.get('agent','unknown'); input_refs=kw.get('input_refs',[]); outputs=kw.get('outputs',[])
    r={'schema_version':'1.0.0','release':RELEASE,'profile':'runtime','jai':kw.get('jai') or jai_binding(agent,input_refs,outputs),
       'id':kw.get('id') or f'EXE-{uuid.uuid4()}','timestamp':kw.get('timestamp') or now,
       'provider':kw.get('provider','unknown'),'model':kw.get('model','unknown'),'agent':agent,'skills':kw.get('skills',[]),
       'input_refs':input_refs,'source_hashes':kw.get('source_hashes',{}),'policies':kw.get('policies',[]),'approvals':kw.get('approvals',[]),
       'tools_used':kw.get('tools_used',[]),'external_system_calls':kw.get('external_system_calls',[]),'outputs':outputs,
       'semantic_hash':kw.get('semantic_hash'),'projection_hash':kw.get('projection_hash'),'render_hash':kw.get('render_hash'),
       'findings':kw.get('findings',[]),'exceptions':kw.get('exceptions',[]),'previous_record_hash':kw.get('previous_record_hash')}
    r['record_hash']=digest_record(r); validate(r); return r

def append(log:Path,record:dict):
    if log.exists() and log.is_dir(): raise ValueError('log path is directory')
    previous=None
    if log.exists() and log.stat().st_size:
        lines=log.read_text(encoding='utf-8').splitlines(); last=json.loads(lines[-1]); validate(last); previous=last['record_hash']
    if record.get('previous_record_hash')!=previous:
        record=dict(record); record['previous_record_hash']=previous; record['record_hash']=digest_record(record); validate(record)
    with log.open('a',encoding='utf-8') as f: f.write(json.dumps(record,sort_keys=True,ensure_ascii=False)+'\n')
    return record['record_hash']

def verify(log:Path):
    prev=None; n=0
    for i,line in enumerate(log.read_text(encoding='utf-8').splitlines(),1):
        if not line.strip(): continue
        r=json.loads(line); validate(r)
        if r.get('previous_record_hash')!=prev: raise ValueError(f'line {i}: chain mismatch')
        prev=r['record_hash']; n+=1
    return n

def self_test():
    with tempfile.TemporaryDirectory() as td:
        p=Path(td)/'execution.jsonl'; a=make(provider='codex',model='test',agent='reviewer',skills=['s1']); append(p,a); b=make(provider='claude',model='test',agent='author',skills=['s2']); append(p,b)
        assert verify(p)==2
        lines=p.read_text().splitlines(); x=json.loads(lines[0]); x['agent']='tampered'; lines[0]=json.dumps(x); p.write_text('\n'.join(lines)+'\n')
        try: verify(p); raise AssertionError('tamper not detected')
        except ValueError: pass
    print('PASS execution-record: JAI L6 profile + hash-chain tamper detection; local storage remains mutable'); return 0

def main():
    ap=argparse.ArgumentParser(); sub=ap.add_subparsers(dest='cmd',required=True); sub.add_parser('self-test'); v=sub.add_parser('verify-log'); v.add_argument('log')
    c=sub.add_parser('create'); c.add_argument('--out',required=True); c.add_argument('--provider',default='unknown'); c.add_argument('--model',default='unknown'); c.add_argument('--agent',default='unknown'); c.add_argument('--skills',nargs='*',default=[])
    a=ap.parse_args()
    if a.cmd=='self-test': return self_test()
    if a.cmd=='verify-log': print('PASS records',verify(Path(a.log))); return 0
    out=Path(a.out)
    if out.exists(): raise SystemExit('refusing to overwrite immutable execution record')
    out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(make(provider=a.provider,model=a.model,agent=a.agent,skills=a.skills),indent=2)+'\n'); print(out); return 0
if __name__=='__main__': raise SystemExit(main())
