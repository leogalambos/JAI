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
RELEASE=((PACKAGE/'VERSION') if (PACKAGE/'VERSION').is_file() else ROOT/'VERSION').read_text().strip()
PROFILE_DIR=ROOT/'publication/archetypes'
SCHEMA=ROOT/'schema/26.10.4/projection-manifest.schema.json'
CONTENT_SCHEMA=ROOT/'content/schema/projection-manifest-v4.schema.json'

def canonical(x): return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def sha(x): return hashlib.sha256(canonical(x)).hexdigest()
def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))

def field_present(model, field):
    """Return substantive explicit field presence; section headings never count.

    Args:
        model: Canonical semantic model with explicit values.
        field: Exact field name; evidence also accepts claim evidence references.
    Returns:
        Whether an explicit substantive value exists.
    """
    def substantive(value):
        if isinstance(value, str): return bool(value.strip())
        if isinstance(value, dict): return any(substantive(v) for k,v in value.items() if k not in ('heading','id','knowledge_status'))
        if isinstance(value, list): return any(substantive(v) for v in value)
        return value is not None and value is not False
    if field=='evidence': return substantive(model.get('evidence')) or any(substantive(c.get('evidence')) for c in model.get('claims',[]))
    if field=='approvals': return substantive(model.get('approvals') or model.get('approver'))
    return substantive(model.get(field))

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

def section_has_content(section):
    """Return whether a section carries text, data rows or diagram entities.

    Args:
        section: Section mapping; headings and table headers alone do not count.
    Returns:
        True when at least one substantive rendered information value exists.
    """
    if str(section.get('body') or '').strip(): return True
    if any(str(x).strip() for x in section.get('bullets',[])): return True
    table=section.get('table') or {}
    if any(any(str(cell).strip() for cell in row) for row in table.get('rows',[])): return True
    diagram=section.get('diagram') or {}
    return any(str(node.get('label') or '').strip() for node in diagram.get('nodes',[]))


def select_sections(model, profile):
    """Return legacy projection and manifest from explicit model/profile dictionaries.

    This read-compatible helper does not certify DCS quality or persist outputs.
    Args:
        model: Canonical semantic source mapping.
        profile: Registered publication profile mapping.
    Returns:
        Publication-model and legacy manifest pair.
    """
    by={s.get('heading','').strip().lower():s for s in model.get('sections',[])}
    selected=[]; mappings=[]; omitted=[]; just={}
    for req in profile['mandatory_sections']:
        k=req.strip().lower()
        if k in by and section_has_content(by[k]):
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
    """Validate legacy/v4 manifest schema and mandatory publication coverage.

    Args:
        manifest: Projection manifest dictionary.
    Returns:
        Policy, lineage, hash syntax and schema errors.
    """
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
    schema=CONTENT_SCHEMA if manifest.get('schema_version')=='4.0.0' else SCHEMA
    if not schema.is_file(): probs.append('projection schema unavailable')
    if jsonschema and schema.is_file():
        for err in jsonschema.Draft202012Validator(load(schema)).iter_errors(manifest): probs.append('projection schema: '+err.message)
    return probs

def build(model_path,profile_path,outdir,reviewer=None,trusted_executions=None,authority=None):
    """Persist a new DCS-bound projection with immutable source and QA sidecars.

    Args:
        model_path: Canonical JSON with explicit registered contract_id.
        profile_path: Publication profile JSON path.
        outdir: Output directory; immutable sidecars cannot be overwritten.
        reviewer: Independent review claim authenticated by the host.
        trusted_executions: Optional existing runtime attestation verifier.
        authority: Optional existing JAI L0 authority verifier.
    Returns:
        Problems, publication model and manifest. Failed builds write nothing.
    Raises:
        OSError: Filesystem failure or immutable sidecar collision.
    """
    import content_spec, content_lint
    model=load(model_path); profile=load(profile_path)
    pub,man=select_sections(model,profile)
    try:
        if not model.get('contract_id'): raise ValueError('explicit registered contract_id required for new projection')
        spec=content_spec.ContentSpec(ROOT).resolve(model['contract_id'], model.get('context',{}))
        report=content_lint.evaluate(model,spec,reviewer=reviewer,trusted_executions=trusted_executions,authority=authority)
    except (ValueError, content_spec.SpecError) as exc:
        return [str(exc)],pub,man
    # DCS units are carried unchanged rather than reconstructed from presentation headings.
    units=model.get('semantic_units',{})
    pub['semantic_units']=units
    for key in ('contract_id','document_kind','compiled_spec_hash','context'):
        pub[key]=model.get(key)
    unit_mappings=[]
    for unit in spec['blueprint']['semantic_units']:
        if unit.get('category') not in ('required_information','conditional_information') or unit.get('applicability') is False: continue
        for field in unit.get('semantic_fields',[]):
            if field in units:
                value=units[field]; destination='semantic_units.'+field
            else:
                value=model
                for part in field.split('.'):
                    value=value.get(part) if isinstance(value,dict) else None
                if value is None: continue
                pub.setdefault('semantic_fields',{})[field]=value; destination='semantic_fields.'+field
            section_index=len(pub['sections'])
            pub['sections'].append({'heading':'Semantic information: '+field,'body':json.dumps(value,sort_keys=True,ensure_ascii=False,indent=2)})
            unit_mappings.append({'source':field,'destination':destination,'rendered_section':section_index,'value_hash':sha(value),'required':True})
    man.update(schema_version='4.0.0',content_qa_ref='content-qa.json',content_qa_hash=sha(report),
               source_ref='semantic-source.json',compiled_spec_ref='compiled-content-spec.json',
               compiled_spec_hash=spec['compiled_spec_hash'],context_hash=spec['context_hash'],
               semantic_unit_mappings=unit_mappings,content_status=report['gate_verdict'])
    man['projection_hash']=sha(pub)
    probs=validate_manifest(man)
    if man.get('omitted_fields'): probs.append('new projections cannot waive mandatory publication fields through omission text')
    if any(f.get('blocking') for f in report.get('findings',[])): probs.append('blocking content QA findings')
    out=Path(outdir)
    if not probs:
        out.mkdir(parents=True,exist_ok=True)
        payloads={'semantic-source.json':model,'compiled-content-spec.json':spec,'content-qa.json':report,
                  'publication-model.json':pub,'projection-manifest.json':man}
        for name,value in payloads.items():
            path=out/name
            if path.is_symlink(): raise FileExistsError('symlink projection output forbidden: '+str(path))
            if path.exists() and load(path)!=value: raise FileExistsError('immutable projection output differs: '+str(path))
        for name,value in payloads.items():
            path=out/name
            try:
                with path.open('x',encoding='utf-8') as stream: stream.write(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
            except FileExistsError:
                if path.is_symlink() or load(path)!=value: raise FileExistsError('immutable projection output differs: '+str(path))
    return probs,pub,man

def self_test():
    profile={'id':'decision-paper','audience':['ARB'],'mandatory_sections':['Decision required','Context'],'mandatory_semantic_fields':['claims','decisions','evidence']}
    good={'title':'X','artifact_id':'A','owner':'O','classification':'Internal','claims':[{'id':'C','statement':'x','basis':'stated','evidence':['E']}],'decisions':[{'id':'D','question':'Approve recovery design?'}],'sections':[{'heading':'Decision required','body':'Approve'},{'heading':'Context','body':'Context'}]}
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
