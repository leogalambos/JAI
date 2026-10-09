#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Provider-neutral Agent Contract enforcement with configurable model routing."""
from __future__ import annotations
import argparse,json,tempfile
try: import jsonschema
except Exception: jsonschema=None
from model_router import effective_registry, resolve
from pathlib import Path
import schema_resolver
ROOT=Path(__file__).resolve().parents[1]
CONTRACTS=ROOT/'agents/agent-contracts.json'; POLICY=ROOT/'policy/managed-policy.json'; BINDINGS=ROOT/'jai/profiles/runtime-agent-bindings.json'

def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def contracts():
    rows=load(CONTRACTS)['contracts']; bindings=load(BINDINGS)['bindings']
    if jsonschema:
        validator=jsonschema.Draft202012Validator(schema_resolver.schema('AgentContract'))
        for row in rows: validator.validate(row)
    for row in rows:
        b=bindings.get(row['id'])
        if not b: raise ValueError(f"{row['id']}: missing runtime JAI binding")
        j=row.get('jai',{})
        if j.get('profile')!='runtime' or j.get('layer')!=b.get('primary_layer') or j.get('authority_ref')!=f"human-authority:{row['authority_boundary']}":
            raise ValueError(f"{row['id']}: embedded JAI binding disagrees with runtime profile")
    return {x['id']:x for x in rows}

def authorize(c,operation,tool=None):
    policy=load(POLICY)
    if operation in set(policy.get('denied_operations',[])): return False,f'{operation} denied by enterprise policy'
    if operation in ('write','edit','mutate') and not c['mutation_allowed']: return False,'reviewer-write denied'
    if operation=='policy-change': return False,'policy mutation requires independent human approval'
    if operation=='self-approve': return False,'self-approval denied'
    if operation=='restricted-mcp-via-shell': return False,'restricted MCP bypass via shell denied'
    if tool and tool in c.get('denied_tools',[]): return False,f'tool {tool} denied'
    if tool and c.get('allowed_tools') and tool not in c['allowed_tools']: return False,f'tool {tool} outside allowlist'
    return True,'allowed'

def provider_config(c,provider,model_config=None):
    if provider not in ('claude','codex'):
        raise ValueError('unsupported provider')
    workload_class=c.get('workload_class','standard')
    selector,mapping=resolve(provider,workload_class,model_config)
    registry,_=effective_registry(model_config); pspec=registry['providers'][provider]
    common={'name':c['id'],'provider':provider,'jai':c['jai'],'workload_class':workload_class,'selection_strategy':pspec.get('selection_strategy'),'strategy_scope':pspec.get('strategy_scope','project-internal'),'model_selector':selector}
    if mapping.get('reasoning_effort'): common['reasoning_effort']=mapping['reasoning_effort']
    if mapping.get('fallbacks'): common['fallbacks']=mapping['fallbacks']
    if provider=='codex':
        common.update({'sandbox_mode':c['sandbox']['mode'],'workspace_write':c['sandbox']['workspace_write'],'network':c['sandbox']['network'],'allowed_tools':c['allowed_tools'],'denied_tools':c['denied_tools'],'approval_required_for':c.get('approval_required_for',[])})
        common['native_codex']={'model':selector if selector!='inherit' else 'inherit-session','model_reasoning_effort':mapping.get('reasoning_effort')}
        return common
    common.update({'tools':c['allowed_tools'],'deny':c['denied_tools'],'sandbox':c['sandbox'],'approval_required_for':c.get('approval_required_for',[])})
    return common

def generate(outdir):
    out=Path(outdir); (out/'codex').mkdir(parents=True,exist_ok=True); (out/'claude').mkdir(parents=True,exist_ok=True)
    for c in contracts().values():
        for p in ('codex','claude'):(out/p/f"{c['id']}.json").write_text(json.dumps(provider_config(c,p),indent=2)+'\n')

def self_test():
    cs=contracts(); tests=[]
    for n in ['codebase-reviewer','gate-auditor','sod-reviewer','sabsa-reviewer','visual-quality-reviewer','evidence-rationale-reviewer']:
        if n in cs: tests.append((n+'-write-denied',not authorize(cs[n],'write')[0]))
    if 'role-author' in cs:
        tests += [('author-write',authorize(cs['role-author'],'write')[0]),('author-policy-denied',not authorize(cs['role-author'],'policy-change')[0]),('shell-bypass-denied',not authorize(cs['role-author'],'restricted-mcp-via-shell')[0])]
    with tempfile.TemporaryDirectory() as td:
        generate(td); tests.append(('codex-native-config',(Path(td)/'codex/codebase-reviewer.json').exists())); tests.append(('claude-config',(Path(td)/'claude/codebase-reviewer.json').exists())); tests.append(('model-class-preserved',provider_config(cs['codebase-reviewer'],'claude')['workload_class']==cs['codebase-reviewer']['workload_class'])); tests.append(('jai-binding-propagated',provider_config(cs['codebase-reviewer'],'codex')['jai']['profile']=='runtime'))
    for n,v in tests: print(('PASS' if v else 'FAIL'),n)
    print(f"{sum(v for _,v in tests)}/{len(tests)} PASS"); return 0 if all(v for _,v in tests) else 1

def main():
    ap=argparse.ArgumentParser();sp=ap.add_subparsers(dest='cmd',required=True);g=sp.add_parser('generate');g.add_argument('--out',required=True);c=sp.add_parser('check');c.add_argument('agent');c.add_argument('operation');c.add_argument('--tool');sp.add_parser('self-test');a=ap.parse_args()
    if a.cmd=='self-test': raise SystemExit(self_test())
    if a.cmd=='generate': generate(a.out); print(a.out); return
    cc=contracts().get(a.agent)
    if not cc: raise SystemExit('unknown agent')
    ok,why=authorize(cc,a.operation,a.tool); print(('ALLOW' if ok else 'DENY'),why); raise SystemExit(0 if ok else 3)
if __name__=='__main__': main()
