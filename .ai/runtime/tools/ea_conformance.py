#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""EA/Open Exchange conformance suite for AI IT House.

L1 syntactic: XML + packaged XSD envelope.
L2 semantic: identifiers, element/relationship/view references + canonical repository validation.
L3 interoperability: import -> canonical -> export -> import round-trip with machine-readable loss report.

The packaged XSD deliberately validates the portable envelope generated/consumed by the runtime; L2 is the
stronger semantic gate. Vendor-specific external tool certification can add fixtures under ea/fixtures/conformance.
"""
from __future__ import annotations
import argparse, hashlib, importlib.util, json, tempfile
from pathlib import Path
from lxml import etree

HERE=Path(__file__).resolve().parent; RUNTIME=HERE.parent
XSD=RUNTIME/'ea/schema/open-exchange-supported.xsd'; REPO_TOOL=HERE/'repository.py'; FIXTURES=RUNTIME/'ea/fixtures/conformance'
NS='http://www.opengroup.org/xsd/archimate/3.0/'
XSI='http://www.w3.org/2001/XMLSchema-instance'

def load_module(name,path):
    spec=importlib.util.spec_from_file_location(name,path); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod
repo_tool=load_module('aiithouse_repository_conformance',REPO_TOOL)

def q(name): return f'{{{NS}}}{name}'
def load_json(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def canonical(x): return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False)

def l1(xml_path: Path):
    errors=[]
    try: doc=etree.parse(str(xml_path))
    except Exception as exc: return None,[f'XML parse error: {exc}']
    try:
        schema=etree.XMLSchema(etree.parse(str(XSD)))
        if not schema.validate(doc): errors.extend(str(x) for x in schema.error_log)
    except Exception as exc: errors.append(f'XSD validation failure: {exc}')
    return doc,errors

def l2(doc):
    errors=[]; warnings=[]; root=doc.getroot()
    if root.tag!=q('model'): errors.append('root element is not ArchiMate model')
    ids={}; elements={}
    for node in root.xpath('.//*[@identifier]'):
        ident=node.get('identifier')
        if ident in ids: errors.append(f'duplicate identifier {ident}')
        ids[ident]=node.tag
        if node.tag==q('element'): elements[ident]=node
    for r in root.findall('.//'+q('relationship')):
        rid=r.get('identifier'); src=r.get('source'); tgt=r.get('target')
        if src not in elements: errors.append(f'relationship {rid} missing source element {src}')
        if tgt not in elements: errors.append(f'relationship {rid} missing target element {tgt}')
    rel_ids={r.get('identifier') for r in root.findall('.//'+q('relationship'))}
    for n in root.findall('.//'+q('node')):
        ref=n.get('elementRef')
        if ref and ref not in elements: errors.append(f'view node references missing element {ref}')
    for c in root.findall('.//'+q('connection')):
        ref=c.get('relationshipRef')
        if ref and ref not in rel_ids: errors.append(f'view connection references missing relationship {ref}')
    # Property definitions and refs.
    pdefs={p.get('identifier') for p in root.findall('.//'+q('propertyDefinition'))}
    for p in root.findall('.//'+q('property')):
        ref=p.get('propertyDefinitionRef')
        if ref and ref not in pdefs: errors.append(f'property references missing definition {ref}')
    return errors,warnings

def unsupported_constructs(doc):
    root=doc.getroot(); known={'model','name','documentation','elements','element','relationships','relationship','views','diagrams','view','node','connection','properties','property','value','propertyDefinitions','propertyDefinition','organizations','item','label'}
    unknown=sorted({etree.QName(x).localname for x in root.iter() if etree.QName(x).namespace==NS and etree.QName(x).localname not in known})
    attrs=[]
    allowed={'identifier','version','source','target','propertyDefinitionRef','elementRef','relationshipRef','x','y','w','h','type','viewpoint','accessType','modifier'}
    for x in root.iter():
        for a in x.attrib:
            qn=etree.QName(a)
            if qn.namespace in (XSI,'http://www.w3.org/XML/1998/namespace'): continue
            if qn.localname not in allowed: attrs.append(f'{etree.QName(x).localname}@{qn.localname}')
    return {'unknown_elements':unknown,'unknown_attributes':sorted(set(attrs))}

def snapshot(repo):
    return {
      'elements':sorted((e.get('id'),e.get('type'),e.get('source',{}).get('stable_id')) for e in repo.get('elements',[])),
      'relationships':sorted((r.get('id'),r.get('type'),r.get('source'),r.get('target')) for r in repo.get('relationships',[])),
      'views':sorted((v.get('id'),tuple(sorted(v.get('element_refs') or [])),tuple(sorted(v.get('relationship_refs') or []))) for v in repo.get('views',[]))
    }

def compare(a,b):
    losses=[]
    for key in ('elements','relationships','views'):
        sa=set(map(tuple,a[key])); sb=set(map(tuple,b[key]))
        for x in sorted(sa-sb): losses.append({'category':key,'direction':'lost','value':x})
        for x in sorted(sb-sa): losses.append({'category':key,'direction':'added','value':x})
    return losses

def conform(xml_path: Path):
    report={'file':str(xml_path),'l1':{},'l2':{},'l3':{},'unsupported':{},'valid':False}
    doc,e1=l1(xml_path); report['l1']={'valid':not e1,'errors':e1}
    if doc is None: return report
    e2,w2=l2(doc); report['l2']={'valid':not e2,'errors':e2,'warnings':w2}; report['unsupported']=unsupported_constructs(doc)
    losses=[]; repo_errors=[]
    try:
        r1=repo_tool.empty_repository('conformance-import','Conformance Import'); repo_tool.import_open_exchange(xml_path,r1,project_id='P-IMP',project_name='Imported',merge=False)
        ce,cw=repo_tool.validate_repository(r1); repo_errors.extend(ce)
        with tempfile.TemporaryDirectory() as td:
            out=Path(td)/'roundtrip.xml'
            repo_tool.export_open_exchange(r1,out)
            # E05 acceptance: the exchange file emitted by the runtime must itself pass
            # the same L1 XSD envelope and L2 semantic checks before it is imported again.
            generated_doc, generated_l1_errors = l1(out)
            generated_l2_errors, generated_l2_warnings = l2(generated_doc) if generated_doc is not None else (['generated export could not be parsed'], [])
            report['l3']['generated_export_l1']={'valid':not generated_l1_errors,'errors':generated_l1_errors}
            report['l3']['generated_export_l2']={'valid':not generated_l2_errors,'errors':generated_l2_errors,'warnings':generated_l2_warnings}
            if generated_l1_errors or generated_l2_errors:
                repo_errors.extend(['generated export conformance: '+x for x in generated_l1_errors+generated_l2_errors])
            r2=repo_tool.empty_repository('conformance-roundtrip','Conformance Roundtrip')
            repo_tool.import_open_exchange(out,r2,project_id='P-IMP',project_name='Imported',merge=False)
            losses=compare(snapshot(r1),snapshot(r2))
            report['l3']['roundtrip_sha256']=hashlib.sha256(out.read_bytes()).hexdigest()
    except Exception as exc: repo_errors.append(str(exc))
    report['l3'].update({'valid':not repo_errors and not losses,'repository_errors':repo_errors,'losses':losses})
    report['valid']=report['l1']['valid'] and report['l2']['valid'] and report['l3']['valid']
    return report

def cmd_check(a):
    r=conform(Path(a.xml)); text=json.dumps(r,indent=2,ensure_ascii=False)
    if a.report: Path(a.report).write_text(text+'\n',encoding='utf-8')
    print(text); return 0 if r['valid'] else 1

def self_test():
    fixtures=sorted(FIXTURES.glob('*.xml')); tests=[]
    tests.append(('xsd-present',XSD.is_file()))
    tests.append(('fixture-present',bool(fixtures)))
    for f in fixtures:
        r=conform(f); tests.append((f'{f.stem}-L1',r['l1']['valid'])); tests.append((f'{f.stem}-L2',r['l2']['valid'])); tests.append((f'{f.stem}-L3',r['l3']['valid']))
        exp=f.with_suffix('.expected.json')
        if exp.is_file():
            e=load_json(exp); tests.append((f'{f.stem}-expected-elements',len(e.get('element_ids',[]))==len({x[0] for x in snapshot_from_fixture(f)['elements']})))
    for n,v in tests: print(('PASS' if v else 'FAIL'),n)
    passed=sum(v for _,v in tests); print(f'{passed}/{len(tests)} PASS'); return 0 if passed==len(tests) else 1

def snapshot_from_fixture(f):
    r=repo_tool.empty_repository('fixture','Fixture'); repo_tool.import_open_exchange(f,r,project_id='P-IMP',project_name='Imported',merge=False); return snapshot(r)

def main():
    ap=argparse.ArgumentParser(); sp=ap.add_subparsers(dest='cmd',required=True)
    p=sp.add_parser('check'); p.add_argument('xml'); p.add_argument('--report'); p.set_defaults(fn=cmd_check)
    sp.add_parser('self-test').set_defaults(fn=lambda a:self_test())
    a=ap.parse_args(); raise SystemExit(a.fn(a) or 0)
if __name__=='__main__': main()
