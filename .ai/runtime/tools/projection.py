#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""JAI-native Publication Projection Contract for AI IT House.

Every newly written ProjectionManifest carries L1-L6 lineage. Compatibility inputs may omit
explicit lineage; the projection boundary deterministically binds them to the semantic snapshot,
publication policy/design, renderer and evidence identities before the manifest is persisted.
"""
from __future__ import annotations
import argparse, hashlib, json, re
from pathlib import Path
try:
    import jsonschema
except Exception:
    jsonschema=None

ROOT=Path(__file__).resolve().parents[1]
PACKAGE=ROOT.parents[1]
RELEASE=(PACKAGE/'VERSION').read_text().strip()
PROFILE_DIR=ROOT/'publication/archetypes'
SCHEMA=ROOT/'schema'/RELEASE/'projection-manifest.schema.json'

def canonical(x): return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def sha(x): return hashlib.sha256(canonical(x)).hexdigest()
def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))

def field_present(model, field):
    if field=='traceability':
        return bool(model.get('traceability') or any(s.get('table',{}).get('headers') and any('trace' in str(h).lower() for h in s['table']['headers']) for s in model.get('sections',[])))
    if field=='approvals': return bool(model.get('approvals') or model.get('approver'))
    if field=='decisions': return bool(model.get('decisions') or any('decision' in s.get('heading','').lower() for s in model.get('sections',[])))
    if field=='risks': return bool(model.get('risks') or any('risk' in s.get('heading','').lower() for s in model.get('sections',[])))
    if field=='evidence': return bool(model.get('evidence') or any(c.get('evidence') for c in model.get('claims',[])))
    return bool(model.get(field))

def evidence_refs(model):
    refs=[]
    for item in model.get('evidence',[]):
        raw=item.get('id') if isinstance(item,dict) else str(item)
        if raw: refs.append(raw if ':' in raw else f'evidence:{raw}')
    for claim in model.get('claims',[]):
        for item in claim.get('evidence',[]):
            raw=item.get('id') if isinstance(item,dict) else str(item)
            if raw: refs.append(raw if ':' in raw else f'evidence:{raw}')
    return sorted(set(refs))

def jai_lineage(model, profile, semantic_hash):
    supplied=model.get('jai',{}) if isinstance(model.get('jai'),dict) else {}
    aid=str(model.get('artifact_id') or 'UNKNOWN')
    pid=str(profile['id'])
    return {
      'intent_ref':supplied.get('intent_ref') or f'intent:{aid}',
      'semantic_snapshot_ref':supplied.get('semantic_snapshot_ref') or f'semantic-snapshot:sha256:{semantic_hash}',
      'policy_ref':supplied.get('policy_ref') or f'policy:publication:{pid}',
      'design_ref':supplied.get('design_ref') or f'publication-design:{pid}',
      'realisation_ref':supplied.get('realisation_ref') or f'renderer:tools/publication.py@{RELEASE}',
      'evidence_refs':sorted(set(supplied.get('evidence_refs',[])+evidence_refs(model))),
    }

def select_sections(model, profile):
    by={s.get('heading','').strip().lower():s for s in model.get('sections',[])}
    selected=[]; mappings=[]; omitted=[]; just={}
    for req in profile['mandatory_sections']:
        k=req.strip().lower()
        if k in by:
            selected.append(by[k]); mappings.append({'source':f'sections:{by[k]["heading"]}','destination':f'sections:{req}'})
        else: omitted.append(f'section:{req}')
    mandatory=set(profile.get('mandatory_semantic_fields',[]))
    for f in mandatory:
        if field_present(model,f): mappings.append({'source':f,'destination':f})
        else: omitted.append(f'field:{f}')
    allowed=model.get('publication_omissions',{})
    for item in list(omitted):
        if item in allowed and str(allowed[item]).strip(): just[item]=str(allowed[item]).strip()
    include=[m['source'] for m in mappings]
    total=len(profile['mandatory_sections'])+len(mandatory)
    satisfied=total-len([x for x in omitted if x not in just])
    coverage=100.0 if total==0 else round(100*satisfied/total,2)
    semantic_hash=sha(model)
    lineage=jai_lineage(model,profile,semantic_hash)
    pm={
      'title':model.get('title'),'subtitle':model.get('subtitle'),'artifact_id':model.get('artifact_id'),'audience':profile['audience'],
      'owner':model.get('owner'),'approver':model.get('approver'),'classification':model.get('classification'),'version':model.get('version'),
      'claims':model.get('claims',[]),'decisions':model.get('decisions',[]),'risks':model.get('risks',[]),'evidence':model.get('evidence',[]),'traceability':model.get('traceability',[]),
      'sections':selected,'profile_id':profile['id'],'jai':lineage
    }
    manifest={
      'jai':lineage,
      'id':f"PROJ-{model.get('artifact_id','UNKNOWN')}-{profile['id']}",'profile':profile['id'],'source_semantic_hash':semantic_hash,
      'mandatory_fields':[f'field:{x}' for x in profile.get('mandatory_semantic_fields',[])]+[f'section:{x}' for x in profile['mandatory_sections']],
      'included_fields':sorted(set(include)),'omitted_fields':sorted(omitted),'mappings':mappings,'omission_justifications':just,'mandatory_coverage':coverage,
      'projection_hash':'','render':{'renderer':'tools/publication.py','renderer_version':RELEASE,'render_hash':None}
    }
    manifest['projection_hash']=sha(pm)
    return pm,manifest

def validate_manifest(manifest):
    probs=[]
    if manifest.get('mandatory_coverage') != 100.0: probs.append(f"mandatory coverage {manifest.get('mandatory_coverage')}% < 100%")
    unjust=[x for x in manifest.get('omitted_fields',[]) if x not in manifest.get('omission_justifications',{})]
    if unjust: probs.append('unjustified omissions: '+', '.join(unjust))
    if not re.fullmatch(r'[0-9a-f]{64}',manifest.get('source_semantic_hash','')): probs.append('invalid semantic hash')
    if not re.fullmatch(r'[0-9a-f]{64}',manifest.get('projection_hash','')): probs.append('invalid projection hash')
    lineage=manifest.get('jai',{})
    for key in ('intent_ref','semantic_snapshot_ref','policy_ref','design_ref','realisation_ref'):
        if not str(lineage.get(key,'')).strip(): probs.append(f'JAI lineage missing {key}')
    if not isinstance(lineage.get('evidence_refs'),list): probs.append('JAI lineage evidence_refs must be a list')
    if jsonschema and SCHEMA.is_file():
        for err in jsonschema.Draft202012Validator(load(SCHEMA)).iter_errors(manifest): probs.append('projection schema: '+err.message)
    return probs

def build(model_path,profile_path,outdir):
    model=load(model_path); profile=load(profile_path)
    pub,man=select_sections(model,profile); probs=validate_manifest(man)
    out=Path(outdir); out.mkdir(parents=True,exist_ok=True)
    if not probs:
        (out/'publication-model.json').write_text(json.dumps(pub,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
        (out/'projection-manifest.json').write_text(json.dumps(man,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    return probs,pub,man

def self_test():
    profile={'id':'decision-paper','audience':['ARB'],'mandatory_sections':['Decision required','Context'],'mandatory_semantic_fields':['claims','decisions','evidence']}
    good={'title':'X','artifact_id':'A','owner':'O','classification':'Internal','claims':[{'id':'C','statement':'x','basis':'stated','evidence':['E']}],'decisions':[{'id':'D'}],'sections':[{'heading':'Decision required','body':'Approve'},{'heading':'Context','body':'Context'}]}
    pub,man=select_sections(good,profile)
    tests=[('good-coverage',man['mandatory_coverage']==100),('hashes',len(man['source_semantic_hash'])==64 and len(man['projection_hash'])==64),('jai-lineage',set(man['jai'])=={'intent_ref','semantic_snapshot_ref','policy_ref','design_ref','realisation_ref','evidence_refs'} and 'evidence:E' in man['jai']['evidence_refs']),('schema-and-policy-valid',not validate_manifest(man))]
    bad=dict(good); bad['sections']=[{'heading':'Context','body':'x'}]; bad['decisions']=[]
    _,bm=select_sections(bad,profile); tests += [('bad-fails',bool(validate_manifest(bm))),('omissions-recorded',len(bm['omitted_fields'])>=2)]
    for n,v in tests: print(('PASS' if v else 'FAIL'),n)
    print(f"{sum(v for _,v in tests)}/{len(tests)} PASS")
    return 0 if all(v for _,v in tests) else 1

def main():
    ap=argparse.ArgumentParser(); sp=ap.add_subparsers(dest='cmd',required=True)
    b=sp.add_parser('build'); b.add_argument('model'); b.add_argument('--profile',required=True); b.add_argument('--out',required=True)
    v=sp.add_parser('validate'); v.add_argument('manifest')
    sp.add_parser('self-test'); a=ap.parse_args()
    if a.cmd=='self-test': raise SystemExit(self_test())
    if a.cmd=='validate':
        probs=validate_manifest(load(a.manifest)); [print('FAIL',x) for x in probs]; print('PASS' if not probs else 'FAILED'); raise SystemExit(bool(probs))
    probs,_,_=build(a.model,a.profile,a.out); [print('FAIL',x) for x in probs]; print('PASS' if not probs else 'FAILED'); raise SystemExit(bool(probs))
if __name__=='__main__': main()
