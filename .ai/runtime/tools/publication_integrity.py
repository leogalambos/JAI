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
    """Validate projected publication hash, mappings and optional rendered hash.

    Args:
        pub: Publication model dictionary.
        man: Projection manifest dictionary.
        rendered: Optional rendered file path.
    Returns:
        Integrity errors, including structured evidence mapping failures.
    """
    probs=[]
    if man.get('projection_hash')!=sha(pub): probs.append('publication model does not match projection_hash')
    if man.get('mandatory_coverage')!=100: probs.append('mandatory publication coverage is not 100%')
    claims={c.get('id') for c in pub.get('claims',[]) if c.get('id')}; evidence={str(e.get('id',e.get('ref',''))) if isinstance(e,dict) else str(e) for e in pub.get('evidence',[])}
    for c in pub.get('claims',[]): evidence.update(str(e.get('id',e.get('ref',''))) if isinstance(e,dict) else str(e) for e in c.get('evidence',[]))
    for mapping in man.get('mappings',[]):
        src=mapping.get('source','')
        if src.startswith('claim:') and src.split(':',1)[1] not in claims: probs.append(f'mapped claim missing: {src}')
        if src.startswith('evidence:') and src.split(':',1)[1] not in evidence: probs.append(f'mapped evidence missing: {src}')
    if rendered:
        expected=(man.get('render') or {}).get('render_hash')
        if expected and expected!=file_sha(rendered): probs.append('render hash mismatch')
    return probs
def verify_content(pub, man, directory, trusted_executions=None, authority=None):
    """Verify current QA, canonical source and exact mandatory-unit fidelity.

    Args:
        pub: Publication-model dictionary.
        man: Version-four projection manifest dictionary.
        directory: Manifest directory containing fixed local immutable sidecars.
        trusted_executions: Optional host runtime attestation verifier.
        authority: Optional existing JAI L0 authority verifier.
    Returns:
        Error strings; an empty list permits a draft render, never release.
    """
    import content_spec, content_lint
    probs=[]
    if man.get('schema_version')!='4.0.0': return ['new renders require a DCS-bound v4 projection; rebuild with explicit contract_id']
    expected={'content_qa_ref':'content-qa.json','source_ref':'semantic-source.json','compiled_spec_ref':'compiled-content-spec.json'}
    if any(man.get(k)!=v for k,v in expected.items()): return ['invalid local content QA sidecar reference']
    base=Path(directory)
    for name in expected.values():
        path=base/name
        if path.is_symlink() or not path.is_file(): return ['content QA sidecars must be regular local files: '+name]
    try:
        source=load(base/'semantic-source.json'); report=load(base/'content-qa.json'); saved_spec=load(base/'compiled-content-spec.json')
        if not source.get('contract_id'): return ['missing explicit contract_id in canonical source']
        spec=content_spec.ContentSpec(Path(__file__).resolve().parents[1]).resolve(source['contract_id'],source.get('context',{}))
        if spec!=saved_spec: probs.append('compiled specification is stale or tampered')
        if sha(source)!=man.get('source_semantic_hash'): probs.append('canonical semantic source hash mismatch')
        if sha(report)!=man.get('content_qa_hash'): probs.append('content QA hash mismatch')
        if spec['compiled_spec_hash']!=man.get('compiled_spec_hash') or spec['context_hash']!=man.get('context_hash'): probs.append('content specification/context hash mismatch')
        probs.extend(content_lint.verify_report(report,source,spec,trusted_executions=trusted_executions,authority=authority))
        if report.get('gate_verdict')!=man.get('content_status'): probs.append('content verdict mismatch')
        if any(f.get('blocking') for f in report.get('findings',[])): probs.append('blocking content QA findings')
        mappings={m['source']:m for m in man.get('semantic_unit_mappings',[])}
        for unit in spec['blueprint']['semantic_units']:
            if unit.get('category') not in ('required_information','conditional_information') or unit.get('applicability') is False: continue
            for field in unit.get('semantic_fields',[]):
                value=source.get('semantic_units',{}).get(field)
                if value is None:
                    value=source
                    for part in field.split('.'): value=value.get(part) if isinstance(value,dict) else None
                # Missing units remain explicit draft findings, but must not acquire an invented destination.
                mapping=mappings.get(field)
                if value is None:
                    if mapping: probs.append('invented semantic mapping: '+field)
                    continue
                if not mapping: probs.append('mandatory semantic mapping missing: '+field); continue
                destination=mapping.get('destination','')
                expected_value=pub.get('semantic_units',{}).get(field) if destination=='semantic_units.'+field else pub.get('semantic_fields',{}).get(field) if destination=='semantic_fields.'+field else None
                if value!=expected_value or sha(value)!=mapping.get('value_hash'): probs.append('mandatory semantic fidelity mismatch: '+field)
                section_index=mapping.get('rendered_section')
                sections=pub.get('sections',[])
                if not isinstance(section_index,int) or not 0<=section_index<len(sections) or sections[section_index].get('body')!=json.dumps(value,sort_keys=True,ensure_ascii=False,indent=2): probs.append('mandatory rendered semantic fidelity mismatch: '+field)
        if pub.get('contract_id')!=source['contract_id'] or pub.get('context')!=source.get('context'): probs.append('publication binding/context mismatch')
        probs.extend(check(pub,man))
    except (OSError,ValueError,KeyError,TypeError) as exc:
        probs.append('content QA verification failed: '+str(exc))
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
    pub=load(a.publication_model); man=load(a.manifest)
    probs=check(pub,man,a.rendered)
    if man.get('schema_version')=='4.0.0': probs+=verify_content(pub,man,Path(a.manifest).parent)
    [print('FAIL',p) for p in probs]; print('PASS' if not probs else 'FAILED'); raise SystemExit(bool(probs))
if __name__=='__main__': main()
