#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""GA regression suite under the current production schemas."""
from __future__ import annotations
import argparse, json, subprocess, sys, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
RUNTIME=ROOT/'runtime'
TOOLS=RUNTIME/'tools'

def run(name, cmd):
    p=subprocess.run(cmd,cwd=ROOT.parent,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    ok=p.returncode==0
    print(('PASS' if ok else 'FAIL'),name)
    if not ok: print(p.stdout[-6000:])
    return ok

def schema_instances():
    try:
        import jsonschema
    except ImportError:
        print('FAIL jsonschema missing'); return False
    # Contract schemas are selected by registry, never inferred from product VERSION.
    reg=json.loads((RUNTIME/'schema/schema-registry.json').read_text())
    names={item['name']:RUNTIME/item['path'] for item in reg['schemas']}
    base=RUNTIME/'schema/26.10.4'  # Historical fallback only for schemas not yet moved.
    checks=[]
    # projection schema instance from deterministic projection self-test shape
    from importlib.util import spec_from_file_location,module_from_spec
    sp=spec_from_file_location('projection',TOOLS/'projection.py'); mod=module_from_spec(sp); sp.loader.exec_module(mod)
    profile=json.loads((RUNTIME/'publication/archetypes/decision-paper.json').read_text())
    m={'title':'Decision','artifact_id':'QUAL-1','audience':['ARB'],'owner':'Architect','approver':'ARB','classification':'Internal','claims':[{'id':'C1','statement':'Claim','basis':'stated','evidence':['E1']}],'decisions':[{'id':'D1'}],'risks':[{'id':'R1'}],'evidence':['E1'],'sections':[{'heading':x,'body':'qualification'} for x in profile['mandatory_sections']]}
    pub,man=mod.select_sections(m,profile)
    instances=[('ProjectionManifest',names['ProjectionManifest'],man),
               ('AgentContract',names['AgentContract'],json.loads((RUNTIME/'agents/agent-contracts.json').read_text())['contracts'][0]),
               ('PolicyContract',names['PolicyContract'],json.loads((RUNTIME/'policy/managed-policy.json').read_text()))]
    for name,path,obj in instances:
        try: jsonschema.Draft202012Validator(json.loads(path.read_text())).validate(obj); checks.append(True); print('PASS schema',name)
        except Exception as e: checks.append(False); print('FAIL schema',name,e)
    ps=json.loads((names['PublicationProfile']).read_text()); val=jsonschema.Draft202012Validator(ps)
    for f in sorted((RUNTIME/'publication/archetypes').glob('*.json')):
        try: val.validate(json.loads(f.read_text())); checks.append(True)
        except Exception as e: checks.append(False); print('FAIL profile',f.name,e)
    print(('PASS' if all(checks) else 'FAIL'),'publication profiles',len(list((RUNTIME/'publication/archetypes').glob('*.json'))))
    return all(checks)

def negative_policy_tests():
    sys.path.insert(0,str(TOOLS)); import agent_runtime
    cs=agent_runtime.contracts(); tests=[]
    for n,c in cs.items():
        if c['authority_boundary']=='read-only-review': tests.append((n+' cannot write', not agent_runtime.authorize(c,'write')[0]))
    for n in ['role-author','artifact-author','workflow-author','migration-author']:
        c=cs[n]; tests.append((n+' cannot mutate policy',not agent_runtime.authorize(c,'policy-change')[0])); tests.append((n+' cannot self-approve',not agent_runtime.authorize(c,'self-approve')[0])); tests.append((n+' cannot bypass MCP via shell',not agent_runtime.authorize(c,'restricted-mcp-via-shell')[0]))
    for n,v in tests: print(('PASS' if v else 'FAIL'),'negative',n)
    return all(v for _,v in tests)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--cross-gate',action='store_true'); a=ap.parse_args()
    tests=[]
    tests.append(schema_instances())
    tests.append(negative_policy_tests())
    py=sys.executable
    if not a.cross_gate:
        tests += [
          run('projection contract',[py,str(TOOLS/'projection.py'),'self-test']),
          run('publication renderers',[py,str(TOOLS/'publication.py'),'self-test']),
          run('render-based visual QA',[py,str(TOOLS/'visual_qa.py'),'self-test']),
          run('agent contract enforcement',[py,str(TOOLS/'agent_runtime.py'),'self-test']),
          run('provider parity',[py,str(TOOLS/'provider_parity.py')]),
          run('full schema registry',[py,str(TOOLS/'schema_check.py'),'self-test','--root',str(ROOT.parent)]),
          run('artifact contracts',[py,str(TOOLS/'artifacts.py'),'check','--root',str(ROOT.parent)]),
          run('artifact golden corpus',[py,str(TOOLS/'artifacts.py'),'golden-test','--root',str(ROOT.parent)]),
          run('SABSA-EA bridge',[py,str(TOOLS/'sabsa_ea.py'),'self-test']),
          run('EA conformance',[py,str(TOOLS/'ea_conformance.py'),'self-test']),
          run('agent policy structural',[py,str(RUNTIME/'scripts/check_agent_policy.py'),'--fast',str(ROOT.parent)])
        ]
    else:
        tests += [
          run('current schema resolver',[py,str(TOOLS/'schema_resolver.py'),'self-test']),
          run('architecture claim lint',[py,str(TOOLS/'architecture_claim_lint.py')]),
        ]
    print(f'GA regression suite: {sum(bool(x) for x in tests)}/{len(tests)} checks PASS')
    return 0 if all(tests) else 1
if __name__=='__main__': raise SystemExit(main())
