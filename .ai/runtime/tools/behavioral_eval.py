#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Behavioral Quality harness for AI IT House.

The evaluator is deterministic. It scores captured agent/workflow results against explicit
enterprise scenario expectations; it does not use a single LLM judge as a release authority.
"""
from __future__ import annotations
import argparse, copy, hashlib, json, math, sys
from pathlib import Path
try:
    import jsonschema
except Exception:
    jsonschema=None

RUNTIME=Path(__file__).resolve().parents[1]
EVALS=RUNTIME/'evals'
import schema_resolver
SCENARIOS=EVALS/'scenarios'
REFS=EVALS/'reference-results'

def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))

def f1(expected,actual):
    e=set(expected); a=set(actual)
    if not e and not a: return 1.0
    if not e or not a: return 0.0
    tp=len(e&a); p=tp/len(a); r=tp/len(e)
    return 0.0 if p+r==0 else 2*p*r/(p+r)

def coverage(expected,actual):
    e=set(expected); a=set(actual)
    return 1.0 if not e else len(e&a)/len(e)

def scenario_files(): return sorted(SCENARIOS.glob('*.json'))

def validate_case(case):
    if jsonschema:
        jsonschema.Draft202012Validator(schema_resolver.schema('EvaluationCase')).validate(case)
    return True

def validate_result(result):
    if jsonschema:
        jsonschema.Draft202012Validator(schema_resolver.schema('EvaluationResult')).validate(result)
    return True

def evaluate(case,result):
    validate_case(case); validate_result(result)
    if result['case_id']!=case['id']: raise ValueError('case_id mismatch')
    exp=case['expected']; req=[x['id'] for x in exp['critical_requirements']]
    claims=result.get('claims',[])
    unsupported=sum(1 for c in claims if c.get('critical') and not c.get('evidence'))
    dr=result.get('decision_rationale',{}); required=exp['decision_rationale']['required_fields']
    present=sum(1 for x in required if dr.get(x) not in (None,'',[],{})); field_score=present/len(required)
    alts=dr.get('alternatives',[]); alt_score=min(1.0,len(alts)/max(1,exp['decision_rationale']['alternatives_min']))
    rationale=(field_score+alt_score)/2
    seeded=set(exp['seeded_reviewer_defects']); found=set(result.get('reviewer_findings',[]))
    recall=1.0 if not seeded else len(seeded&found)/len(seeded)
    fp=len(found-seeded); fp_rate=0.0 if not found else fp/len(found)
    broken=sum(1 for x in result.get('artifact_status',[]) if not x.get('ok'))
    cross=result.get('cross_agent',{}); checks=max(1,int(cross.get('checks',0))); conflicts=int(cross.get('conflicts',0))
    metrics={
      'role_routing_accuracy':f1(exp['roles'],result.get('roles',[])),
      'workflow_routing_accuracy':f1(exp['workflow_routes'],result.get('workflows',[])),
      'critical_requirement_coverage':coverage(req,result.get('requirements_covered',[])),
      'evidence_linkage':coverage(exp['critical_evidence'],result.get('evidence_links',[])),
      'unsupported_critical_claims':unsupported,
      'decision_rationale_quality':rationale,
      'traceability_completeness':coverage(exp['traceability_links'],result.get('traceability_links',[])),
      'critical_reviewer_defect_recall':recall,
      'reviewer_false_positive_rate':fp_rate,
      'sod_violations':len(result.get('sod_violations',[])),
      'mandatory_publication_coverage':coverage(exp['mandatory_artifacts'],result.get('publications',[])),
      'broken_artifact_production':broken,
      'visual_quality':float(result.get('visual_qa',{}).get('score',0.0)) if int(result.get('visual_qa',{}).get('critical_defects',0))==0 else 0.0,
      'cross_agent_consistency':max(0.0,1.0-conflicts/checks),
    }
    return metrics

def passes(value,rule):
    op=rule['operator']; target=rule['value']
    return {'>=':value>=target,'<=':value<=target,'==':value==target}.get(op,False)

def reference_result(case):
    exp=case['expected']; req=[x['id'] for x in exp['critical_requirements']]
    evidence=exp['critical_evidence']
    claims=[{'id':f'CLAIM-{i+1}','critical':True,'evidence':[evidence[i%len(evidence)]]} for i,_ in enumerate(req)]
    dr={'chosen_option':'Option A','alternatives':['Option A','Option B'],'trade_offs':['cost vs risk','speed vs control'],'rationale':'Evidence-backed choice within stated constraints','residual_risk':'Owned residual risk remains','decision_owner':'Named authority'}
    return {'case_id':case['id'],'roles':exp['roles'],'workflows':exp['workflow_routes'],'requirements_covered':req,'evidence_links':evidence,'claims':claims,'decision_rationale':dr,'traceability_links':exp['traceability_links'],'reviewer_findings':exp['seeded_reviewer_defects'],'sod_violations':[],'publications':exp['mandatory_artifacts'],'artifact_status':[{'name':x,'ok':True} for x in exp['mandatory_artifacts']],'visual_qa':{'score':1.0,'critical_defects':0},'cross_agent':{'checks':max(4,len(exp['roles'])),'conflicts':0}}

def write_references():
    REFS.mkdir(parents=True,exist_ok=True)
    for p in scenario_files():
        c=load(p); validate_case(c); r=reference_result(c); validate_result(r)
        (REFS/f"{c['id']}.json").write_text(json.dumps(r,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(f'wrote {len(scenario_files())} reference result fixtures')

def structural_problems():
    probs=[]; roles={r['slug'] for r in load(RUNTIME/'roles.json')['roles']}; workflows={w['key'] for w in load(RUNTIME/'workflows.json')['workflows']}
    files=scenario_files()
    if len(files)<10: probs.append(f'expected >=10 enterprise scenarios, found {len(files)}')
    ids=set()
    for p in files:
        try: c=load(p); validate_case(c)
        except Exception as e: probs.append(f'{p.name}: schema {e}'); continue
        if c['id'] in ids: probs.append(f'duplicate scenario {c["id"]}')
        ids.add(c['id'])
        for r in c['expected']['roles']:
            if r not in roles: probs.append(f'{c["id"]}: unknown expected role {r}')
        for w in c['expected']['workflow_routes']:
            if w not in workflows: probs.append(f'{c["id"]}: unknown expected workflow {w}')
    return probs

def file_sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def validate_live_evidence(results_dir, evidence_path):
    if not evidence_path: return ['live/provider qualification requires --evidence manifest']
    p=Path(evidence_path)
    if not p.is_file(): return [f'qualification evidence missing: {p}']
    try: e=load(p)
    except Exception as exc: return [f'qualification evidence invalid JSON: {exc}']
    probs=[]
    if jsonschema:
        try: jsonschema.Draft202012Validator(schema_resolver.schema('BehavioralQualificationEvidence')).validate(e)
        except Exception as exc: probs.append(f'qualification evidence schema: {exc}')
    if e.get('capture_type')!='live-provider': probs.append('capture_type must be live-provider')
    for k in ('provider','model','generated_at'):
        if not str(e.get(k,'')).strip(): probs.append(f'evidence missing {k}')
    hashes=e.get('result_hashes',{})
    if not isinstance(hashes,dict): probs.append('result_hashes must be object'); hashes={}
    for sp in scenario_files():
        rp=Path(results_dir)/f'{load(sp)["id"]}.json'
        if not rp.is_file(): continue
        expected=hashes.get(rp.name)
        actual=file_sha(rp)
        if expected != actual: probs.append(f'{rp.name}: evidence hash missing/mismatch')
    if e.get('scenario_count') != len(scenario_files()): probs.append('scenario_count does not match packaged scenario corpus')
    return probs

def qualify(reference_dir, evidence_path=None, fixture_mode=False):
    reference_dir=Path(reference_dir).resolve()
    if reference_dir == REFS.resolve() and not fixture_mode:
        return ['reference-results are evaluator fixtures, not release qualification evidence; use --fixture-mode only for corpus conformance'],{}
    probs=[] if fixture_mode else validate_live_evidence(reference_dir,evidence_path)
    probs += structural_problems(); thresholds=load(EVALS/'behavioral-thresholds.json')['thresholds']; all_metrics=[]
    for p in scenario_files():
        c=load(p); rp=Path(reference_dir)/f"{c['id']}.json"
        if not rp.is_file(): probs.append(f'missing result {rp.name}'); continue
        try: m=evaluate(c,load(rp)); all_metrics.append((c['id'],m))
        except Exception as e: probs.append(f'{c["id"]}: evaluation failed: {e}')
    if not all_metrics: probs.append('no evaluable results'); return probs,{}
    aggregate={}
    keys=thresholds.keys()
    count_metrics={'unsupported_critical_claims','sod_violations','broken_artifact_production'}
    for k in keys:
        vals=[m[k] for _,m in all_metrics]
        aggregate[k]=sum(vals) if k in count_metrics else sum(vals)/len(vals)
        if not passes(aggregate[k],thresholds[k]): probs.append(f'{k}={aggregate[k]:.4f} fails {thresholds[k]["operator"]}{thresholds[k]["value"]}')
    # Critical per-case invariants: requirements/publication/unsupported claims/SoD/broken artefacts must never average away.
    for cid,m in all_metrics:
        for k in ('critical_requirement_coverage','mandatory_publication_coverage'):
            if m[k] != 1.0: probs.append(f'{cid}: {k}={m[k]:.3f} critical per-case gate')
        for k in ('unsupported_critical_claims','sod_violations','broken_artifact_production'):
            if m[k] != 0: probs.append(f'{cid}: {k}={m[k]} critical per-case gate')
    return probs,aggregate

def self_test():
    write_references(); probs,agg=qualify(REFS,fixture_mode=True)
    if probs:
        print('FAIL reference corpus'); [print(' -',x) for x in probs]; return 1
    # Adversarial mutation proves the evaluator rejects defects rather than merely accepting fixture shape.
    c=load(scenario_files()[0]); bad=copy.deepcopy(reference_result(c))
    bad['roles']=bad['roles'][:-2]; bad['workflows']=[]; bad['requirements_covered']=bad['requirements_covered'][:-1]; bad['evidence_links']=bad['evidence_links'][:-1]
    bad['claims'][0]['evidence']=[]; bad['decision_rationale'].pop('trade_offs',None); bad['traceability_links']=bad['traceability_links'][:-1]
    bad['reviewer_findings']=bad['reviewer_findings'][:-2]+['FALSE-POSITIVE']; bad['sod_violations']=['producer-self-approved']; bad['publications']=bad['publications'][:-1]
    bad['artifact_status'][0]['ok']=False; bad['visual_qa']={'score':0.6,'critical_defects':1}; bad['cross_agent']={'checks':6,'conflicts':2}
    m=evaluate(c,bad); th=load(EVALS/'behavioral-thresholds.json')['thresholds']; failed=[k for k,v in m.items() if k in th and not passes(v,th[k])]
    required_fail={'role_routing_accuracy','workflow_routing_accuracy','critical_requirement_coverage','unsupported_critical_claims','sod_violations','mandatory_publication_coverage','broken_artifact_production','visual_quality'}
    if not required_fail <= set(failed): print('FAIL mutation detection',sorted(required_fail-set(failed))); return 1
    refused,_=qualify(REFS,fixture_mode=False)
    if not refused or 'evaluator fixtures' not in refused[0]: print('FAIL reference corpus accepted as live qualification'); return 1
    print(f'PASS Behavioral Quality: {len(scenario_files())} scenarios, {len(th)} metrics, adversarial mutation detected {len(failed)} metric failures; fixture/live qualification boundary enforced')
    return 0

def main():
    ap=argparse.ArgumentParser(); sub=ap.add_subparsers(dest='cmd',required=True)
    sub.add_parser('self-test'); sub.add_parser('write-references'); q=sub.add_parser('qualify'); q.add_argument('--results',required=True); q.add_argument('--evidence'); q.add_argument('--fixture-mode',action='store_true'); e=sub.add_parser('evaluate'); e.add_argument('--case',required=True); e.add_argument('--result',required=True)
    a=ap.parse_args()
    if a.cmd=='self-test': return self_test()
    if a.cmd=='write-references': write_references(); return 0
    if a.cmd=='evaluate':
        c=load(SCENARIOS/f'{a.case}.json'); m=evaluate(c,load(a.result)); print(json.dumps(m,indent=2)); return 0
    probs,agg=qualify(Path(a.results),a.evidence,a.fixture_mode); print(json.dumps(agg,indent=2));
    if probs: [print('FAIL',x) for x in probs]; return 1
    print('PASS behavioral thresholds'); return 0
if __name__=='__main__': raise SystemExit(main())
