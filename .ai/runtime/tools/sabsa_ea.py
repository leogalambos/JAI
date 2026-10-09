#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""SABSA -> EA projection -> ArchiMate projection bridge for AI IT House.

SABSA remains authoritative for SABSA-domain classification and semantics; JAI owns global semantic identity. The bridge is intentionally one-way. Projection records preserve
SABSA stable IDs, layer/question/type metadata and per-object source hashes. `check` detects missing,
stale and orphaned EA projections. Open Exchange is handled by repository.py after projection.
"""
from __future__ import annotations
import argparse, copy, hashlib, importlib.util, json, re, sys, tempfile
from pathlib import Path
from typing import Any

HERE=Path(__file__).resolve().parent
RUNTIME=HERE.parent
MAPPING_FILE=RUNTIME/'ea/sabsa-mapping.json'
BRIDGE='sabsa-ea-jai-profile'
LEGACY_BRIDGES={'sabsa-ea-26.10'}
L2_NAME='Meaning and Domain Model'
L2_ACCEPTANCE='Do all parties mean the same thing and is uncertainty represented?'
SABSA_TOOL=HERE/'sabsa.py'
REPO_TOOL=HERE/'repository.py'


def load_module(name: str, path: Path):
    spec=importlib.util.spec_from_file_location(name,path); mod=importlib.util.module_from_spec(spec); assert spec and spec.loader; spec.loader.exec_module(mod); return mod

sabsa=load_module('aiithouse_sabsa',SABSA_TOOL)
repo_tool=load_module('aiithouse_repository',REPO_TOOL)


def load_json(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def canonical(x: Any)->bytes: return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def sha(x: Any)->str: return hashlib.sha256(canonical(x)).hexdigest()


def mapping(): return load_json(MAPPING_FILE)


def mapping_hash(doc=None): return sha(doc or mapping())


def semantic_payload(meta: dict) -> dict:
    return {k:v for k,v in meta.items() if not k.startswith('_') and k not in ('status',)}


def semantic_hash(meta: dict) -> str: return sha({'type':meta.get('_dirtype'),'payload':semantic_payload(meta)})


def ea_id(stable_id: str) -> str:
    clean=re.sub(r'[^A-Za-z0-9_.-]+','-',stable_id).strip('-')
    if not clean or not re.match(r'^[A-Za-z_]',clean): clean='id-'+clean
    if len(clean)>90: clean=clean[:65]+'-'+hashlib.sha1(stable_id.encode()).hexdigest()[:16]
    return 'sabsa-'+clean


def rel_id(source: str, field: str, target: str) -> str:
    return 'sabsa-rel-'+hashlib.sha1(f'{source}|{field}|{target}'.encode()).hexdigest()[:20]


def projected_snapshot(entries: dict) -> str:
    return sha([{'id':eid,'type':m.get('_dirtype'),'hash':semantic_hash(m)} for eid,m in sorted(entries.items())])


def element_from(eid: str, m: dict, rule: dict, project_id: str, mapping_version: str) -> dict:
    owner=m.get('owner') or m.get('authority') or 'SABSA owner required'
    state=m.get('lifecycle_state') or 'active'
    if state not in repo_tool.LIFECYCLE_STATES: state='active'
    horizon=m.get('horizon') or 'unspecified'
    if horizon not in repo_tool.HORIZONS: horizon='unspecified'
    source={
      'model':'SABSA','stable_id':eid,'sabsa_layer':rule['sabsa_layer'],'sabsa_question':rule['sabsa_question'],
      'sabsa_element_type':m.get('_dirtype'),'source_path':m.get('_path',''),'origin_library':m.get('_origin_library','')
    }
    projection={'ea_type':rule['ea_type'],'archimate_type':rule['archimate_type'],'specialization':rule['specialization'],'mapping_version':mapping_version,'source_hash':semantic_hash(m),'bridge':BRIDGE}
    props={'SABSA.Layer':rule['sabsa_layer'],'SABSA.Question':rule['sabsa_question'],'SABSA.ElementType':m.get('_dirtype'),'SABSA.Specialization':rule['specialization']}
    for k,v in semantic_payload(m).items():
        if k not in ('id','title','owner','lifecycle_state','horizon','valid_from','valid_until') and v not in ('',None): props[f'SABSA.{k}']=v
    return {
      'id':ea_id(eid),'type':rule['archimate_type'],'name':m.get('title') or eid,'project_id':project_id,'owner':owner,
      'lifecycle_state':state,'horizon':horizon,'description':m.get('statement') or m.get('description') or m.get('purpose') or '',
      'properties':props,'artifact_refs':[],'benefit_refs':[],'source_refs':[f'SABSA:{eid}'],'source':source,'projection':projection,
      'canonical_ref':{'id':f'semantic:{eid}','hash':'sha256:'+semantic_hash(m)},
      'jai':{'core_version':'1.0.0','layer':2,'layer_name':L2_NAME,'profile':'sabsa','responsibility':'Preserve SABSA-domain semantics as a JAI canonical semantic projection','input_refs':[f'sabsa:{eid}'],'output_refs':[f'ea:{ea_id(eid)}'],'authority_ref':f'sabsa:{owner}','acceptance_question':L2_ACCEPTANCE,'evidence_obligations':['source object hash preserved']},
      'source_specialisations':[{'profile':'sabsa','ref':f'sabsa:{eid}'}],
      'valid_from':m.get('valid_from') or None,'valid_to':m.get('valid_until') or None
    }


def project_entries(entries: dict, repository: dict, project_id: str, project_name: str, owner: str, source_library: str='') -> dict:
    mp=mapping(); rules=mp['rules']; missing=sorted({m.get('_dirtype') for m in entries.values()}-set(rules))
    if missing: raise ValueError('unmapped SABSA types: '+', '.join(missing))
    # deterministic replacement of prior projections for this target project/bridge
    old_ids={e['id'] for e in repository.get('elements',[]) if e.get('project_id')==project_id and (e.get('projection') or {}).get('bridge') in ({BRIDGE} | LEGACY_BRIDGES)}
    repository['elements']=[e for e in repository.get('elements',[]) if e.get('id') not in old_ids]
    repository['relationships']=[r for r in repository.get('relationships',[]) if r.get('source') not in old_ids and r.get('target') not in old_ids and not str(r.get('id','')).startswith('sabsa-rel-')]
    repository['views']=[v for v in repository.get('views',[]) if not (v.get('project_ids')==[project_id] and v.get('properties',{}).get('projection_bridge') in ({BRIDGE} | LEGACY_BRIDGES))]
    ps=repo_tool.index_by(repository.setdefault('projects',[])); project=ps.get(project_id)
    if not project:
        repository['projects'].append({'id':project_id,'name':project_name,'owner':owner,'status':'delivery','benefits':[],'artifacts':[]})
    else:
        project.update({'name':project_name,'owner':owner})
    idmap={eid:ea_id(eid) for eid in entries}
    elems=[]; rels=[]
    for eid,m in sorted(entries.items()): elems.append(element_from(eid,m,rules[m['_dirtype']],project_id,mp['mapping_version']))
    for eid,m in sorted(entries.items()):
        rule=rules[m['_dirtype']]; spec=sabsa.TYPES[m['_dirtype']]
        for field in spec.get('links',{}):
            for target in sabsa.ids(m.get(field)):
                if target not in idmap: continue
                rels.append({'id':rel_id(eid,field,target),'type':rule.get('relationship_rules',{}).get(field,'Association'),'source':idmap[eid],'target':idmap[target],
                             'project_id':project_id,'owner':owner,'lifecycle_state':'active','name':field.replace('_',' '),'description':f'SABSA relation {eid}.{field} -> {target}',
                             'properties':{'SABSA.SourceStableId':eid,'SABSA.RelationField':field,'SABSA.TargetStableId':target,'SABSA.MappingVersion':mp['mapping_version']}})
    repository.setdefault('elements',[]).extend(elems); repository.setdefault('relationships',[]).extend(rels)
    view={'id':f'sabsa-view-{project_id}','name':f'{project_name} — SABSA projection','viewpoint':'Custom','purpose':'EA domain projection of SABSA semantic objects under JAI global semantic identity',
          'audience':['Architecture stakeholders'],'project_ids':[project_id],'element_refs':[e['id'] for e in elems],'relationship_refs':[r['id'] for r in rels],'include_retired':True,
          'properties':{'projection_bridge':BRIDGE,'mapping_version':mp['mapping_version']}}
    repository.setdefault('views',[]).append(view)
    manifest={'id':f'sabsa-projection-{project_id}','profile':'sabsa-to-jai-ea-profile','source_model':'SABSA','source_library':source_library,'project_id':project_id,
              'source_snapshot_hash':projected_snapshot(entries),'mapping_registry_hash':mapping_hash(mp),'mapping_version':mp['mapping_version'],'object_count':len(elems),'relationship_count':len(rels),'status':'current'}
    manifests=[x for x in repository.get('projection_manifests',[]) if x.get('id')!=manifest['id']]; manifests.append(manifest); repository['projection_manifests']=manifests
    repo_tool.touch(repository); return manifest


def check_projection(entries: dict, repository: dict, project_id: str) -> dict:
    expected={eid:semantic_hash(m) for eid,m in entries.items()}
    projected={e.get('source',{}).get('stable_id'):e for e in repository.get('elements',[]) if e.get('project_id')==project_id and e.get('source',{}).get('model')=='SABSA'}
    missing=sorted(set(expected)-set(projected)); orphan=sorted(set(projected)-set(expected)); stale=[]
    for sid in sorted(set(expected)&set(projected)):
        if projected[sid].get('projection',{}).get('source_hash')!=expected[sid]: stale.append(sid)
    mp=mapping(); mapping_stale=sorted(sid for sid,e in projected.items() if e.get('projection',{}).get('mapping_version')!=mp['mapping_version'])
    manifests=[x for x in repository.get('projection_manifests',[]) if x.get('project_id')==project_id and x.get('source_model')=='SABSA']
    manifest_ok=bool(manifests and manifests[-1].get('source_snapshot_hash')==projected_snapshot(entries) and manifests[-1].get('mapping_registry_hash')==mapping_hash(mp))
    return {'project_id':project_id,'expected_objects':len(expected),'projected_objects':len(projected),'missing':missing,'orphan':orphan,'stale':stale,'mapping_stale':mapping_stale,'manifest_current':manifest_ok,
            'valid':not (missing or orphan or stale or mapping_stale) and manifest_ok}


def validate_mapping() -> list[str]:
    mp=mapping(); et=sabsa.TYPES; rules=mp.get('rules',{}); problems=[]
    if set(rules)!=set(et):
        problems += [f'missing mapping {x}' for x in sorted(set(et)-set(rules))]+[f'unknown mapping {x}' for x in sorted(set(rules)-set(et))]
    cells={(r.get('sabsa_layer'),r.get('sabsa_question')) for r in rules.values()}
    if len(cells)!=36: problems.append(f'mapping covers {len(cells)}/36 SABSA cells')
    for typ,r in rules.items():
        if r.get('archimate_type') not in repo_tool.ARCHIMATE_ELEMENT_TYPES: problems.append(f'{typ}: invalid ArchiMate type {r.get("archimate_type")}')
        for fld,rt in r.get('relationship_rules',{}).items():
            if rt not in repo_tool.ARCHIMATE_RELATIONSHIP_TYPES: problems.append(f'{typ}.{fld}: invalid relationship type {rt}')
    return problems


def cmd_project(a):
    entries,errors=sabsa.load(a.lib)
    if errors: [print('FAIL',x) for x in errors]; return 1
    rp=repo_tool.resolve_repo(a.repo); repository=repo_tool.load_json(rp) if rp.is_file() else repo_tool.empty_repository(a.repository_id or 'enterprise-architecture',a.repository_name or 'Enterprise Architecture Repository')
    manifest=project_entries(entries,repository,a.project_id,a.project_name,a.owner,str(Path(a.lib).resolve()))
    repo_tool.save_repo(rp,repository); print(json.dumps(manifest,indent=2)); return 0


def cmd_check(a):
    problems=validate_mapping(); entries,errors=sabsa.load(a.lib); problems += errors
    if problems: [print('FAIL',x) for x in problems]; return 1
    _,repository=repo_tool.load_repo(a.repo); report=check_projection(entries,repository,a.project_id); print(json.dumps(report,indent=2)); return 0 if report['valid'] else 1


def cmd_mapping(a):
    problems=validate_mapping(); print(json.dumps({'mapping_version':mapping().get('mapping_version'),'rules':len(mapping().get('rules',{})),'cells':len({(x['sabsa_layer'],x['sabsa_question']) for x in mapping()['rules'].values()}),'problems':problems},indent=2)); return 1 if problems else 0


def self_test()->int:
    tests=[]
    def ok(n,v): tests.append((n,bool(v)))
    ok('mapping-39-types',len(mapping()['rules'])==39); ok('mapping-36-cells',not validate_mapping())
    entries={}
    for i,(t,spec) in enumerate(sabsa.TYPES.items(),1):
        eid=f'{spec["prefix"]}-{i:03d}'; entries[eid]={'id':eid,'title':f'Test {t}','owner':'Test Owner','_dirtype':t,'_path':f'{spec["dir"]}/{eid}.md','_origin_library':'/test'}
    repository=repo_tool.empty_repository('test-repo','Test Repository'); project_entries(entries,repository,'P-SABSA','SABSA Test','EA Owner','/test')
    errs,warns=repo_tool.validate_repository(repository); ok('projected-repo-valid',not errs); ok('projected-39',len([e for e in repository['elements'] if e['project_id']=='P-SABSA'])==39)
    ok('stable-id-preserved',all(e.get('source',{}).get('stable_id') for e in repository['elements']))
    report=check_projection(entries,repository,'P-SABSA'); ok('projection-current',report['valid'])
    first=next(iter(entries)); entries2=copy.deepcopy(entries); entries2[first]['title']='Changed title'; report2=check_projection(entries2,repository,'P-SABSA'); ok('change-invalidates',first in report2['stale'] and not report2['valid'])
    entries3=copy.deepcopy(entries); removed=next(iter(entries3)); entries3.pop(removed); report3=check_projection(entries3,repository,'P-SABSA'); ok('orphan-detected',removed in report3['orphan'])
    with tempfile.TemporaryDirectory() as td:
        xp=Path(td)/'model.xml'; repo_tool.export_open_exchange(repository,xp); imported=repo_tool.empty_repository('imported','Imported'); repo_tool.import_open_exchange(xp,imported,project_id='P-SABSA',project_name='SABSA Test')
        src_ids={e.get('source',{}).get('stable_id') for e in imported.get('elements',[]) if e.get('source')}; ok('roundtrip-stable-id',src_ids==set(entries))
    for n,v in tests: print(('PASS' if v else 'FAIL'),n)
    passed=sum(v for _,v in tests); print(f'{passed}/{len(tests)} PASS'); return 0 if passed==len(tests) else 1


def main():
    ap=argparse.ArgumentParser(); sp=ap.add_subparsers(dest='cmd',required=True)
    p=sp.add_parser('project'); p.add_argument('lib'); p.add_argument('--repo',required=True); p.add_argument('--project-id',required=True); p.add_argument('--project-name',required=True); p.add_argument('--owner',required=True); p.add_argument('--repository-id'); p.add_argument('--repository-name'); p.set_defaults(fn=cmd_project)
    p=sp.add_parser('check'); p.add_argument('lib'); p.add_argument('--repo',required=True); p.add_argument('--project-id',required=True); p.set_defaults(fn=cmd_check)
    p=sp.add_parser('mapping-check'); p.set_defaults(fn=cmd_mapping)
    sp.add_parser('self-test').set_defaults(fn=lambda a:self_test())
    a=ap.parse_args(); raise SystemExit(a.fn(a) or 0)
if __name__=='__main__': main()
