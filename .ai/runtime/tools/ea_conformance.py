#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""EA/Open Exchange conformance suite for AI IT House.

L1 syntactic: offline Open Group authored exchange 3.1 XSD validation.
L2 structural: identifiers, known types, references and canonical repository consistency.
Metamodel: ArchiMate 3.2 permitted triples and explicit portable-profile rules.
L3 fidelity: source-file -> export comparison and a canonical round-trip loss report.

Language edition 3.2 and exchange-schema edition 3.1 are distinct. Schema and
permitted-table checks establish bounded implementation results, not Open Group
certification, semantic or visual adequacy, or external-tool interoperability.
Those remain separate qualification duties.
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
    """Load the Python file at ``path`` as ``name``; propagate loader/file errors."""
    spec=importlib.util.spec_from_file_location(name,path); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod
repo_tool=load_module('aiithouse_repository_conformance',REPO_TOOL)
profile=load_module('aiithouse_archimate_profile',HERE/'archimate_profile.py')

def q(name):
    """Return the supported exchange-namespace qualified XML ``name``."""
    return f'{{{NS}}}{name}'

def load_json(p):
    """Read JSON from ``p``; propagate filesystem and JSON decoding errors."""
    return json.loads(Path(p).read_text(encoding='utf-8'))

def canonical(x):
    """Return stable JSON text for ``x``; raise TypeError for unsupported values."""
    return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False)

def l1(xml_path: Path):
    """Return a parsed tree and official pinned exchange-XSD errors for xml_path.

    The language profile is 3.2; the Open Group authored exchange XSD is 3.1.
    Parsing is offline, with external entity resolution disabled.
    """
    errors=[]
    try: doc=etree.parse(str(xml_path),etree.XMLParser(no_network=True,resolve_entities=False))
    except Exception as exc: return None,[f'XML parse error: {exc}']
    errors.extend(profile.exchange_schema_errors(xml_path))
    return doc,errors

def l2(doc):
    """Return structural errors and warnings for a parsed exchange document.

    ``doc`` is an lxml tree. Known type and reference checks do not certify the
    legality of every concept/relationship combination or the selected viewpoint.
    """
    errors=[]; warnings=[]; root=doc.getroot()
    if root.tag!=q('model'): errors.append('root element is not ArchiMate model')
    ids={}; elements={}
    for node in root.xpath('.//*[@identifier]'):
        ident=node.get('identifier')
        if ident in ids: errors.append(f'duplicate identifier {ident}')
        ids[ident]=node.tag
        if node.tag==q('element'):
            elements[ident]=node
            concept=node.get(f'{{{XSI}}}type', '').split(':')[-1]
            if concept not in repo_tool.ARCHIMATE_ELEMENT_TYPES:
                errors.append(f'element {ident} has unknown concept type {concept}')
    relationship_nodes=root.findall('.//'+q('relationship'))
    relationship_ids={r.get('identifier') for r in relationship_nodes}
    for r in relationship_nodes:
        rid=r.get('identifier'); src=r.get('source'); tgt=r.get('target')
        relation=r.get(f'{{{XSI}}}type', '').split(':')[-1]
        if relation not in repo_tool.ARCHIMATE_RELATIONSHIP_TYPES:
            errors.append(f'relationship {rid} has unknown relationship type {relation}')
        endpoints=elements.keys() | relationship_ids if relation=='Association' else elements.keys()
        if src not in endpoints: errors.append(f'relationship {rid} missing source concept {src}')
        if tgt not in endpoints: errors.append(f'relationship {rid} missing target concept {tgt}')
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
    """Return unqualified constructs, including foreign-namespace extensions.

    ``doc`` is a parsed lxml tree. The returned lists are explicit dispositions,
    not a claim that content ignored by the supported envelope was preserved.
    """
    root=doc.getroot(); known={'model','name','documentation','elements','element','relationships','relationship','views','diagrams','view','node','connection','properties','property','value','propertyDefinitions','propertyDefinition','organizations','item','label'}
    nodes=[x for x in root.iter() if isinstance(x.tag,str)]
    unknown=sorted({x.tag for x in nodes if etree.QName(x).namespace!=NS or etree.QName(x).localname not in known})
    attrs=[]
    allowed={'identifier','identifierRef','version','source','target','propertyDefinitionRef','elementRef','relationshipRef','x','y','w','h','type','viewpoint','accessType','modifier'}
    for x in nodes:
        for a in x.attrib:
            qn=etree.QName(a)
            if a in (f'{{{XSI}}}type','{http://www.w3.org/XML/1998/namespace}lang'): continue
            if qn.namespace or qn.localname not in allowed: attrs.append(f'{etree.QName(x).localname}@{a}')
    return {'unknown_elements':unknown,'unknown_attributes':sorted(set(attrs))}

def snapshot(repo):
    """Return stable material-content tuples from a canonical repository.

    ``repo`` is a repository dictionary. Snapshot values include names,
    documentation, properties, relationship attributes and view metadata; volatile
    repository timestamps and project bookkeeping are intentionally excluded.
    """
    fields={
      'elements':('type','name','description','project_id','owner','lifecycle_state','horizon','properties','source','projection','artifact_refs','benefit_refs','source_refs','valid_from','valid_to','review_due'),
      'relationships':('type','source','target','project_id','owner','lifecycle_state','name','description','properties','access_type','influence_strength'),
      'views':('name','description','viewpoint','purpose','audience','project_ids','element_refs','relationship_refs','include_retired','notation','selection_profile','selection_status','viewpoint_contract','properties'),
    }
    return {key:sorted((item.get('id'), canonical({field:item.get(field) for field in names})) for item in repo.get(key,[])) for key,names in fields.items()}

def compare(a,b):
    """Return added/lost material records between two ``snapshot`` results.

    ``a`` and ``b`` have hashable record tuples in elements/relationships/views.
    Changed records appear as a lost and an added value; inputs are not mutated.
    """
    losses=[]
    for key in ('elements','relationships','views'):
        sa=set(map(tuple,a[key])); sb=set(map(tuple,b[key]))
        for x in sorted(sa-sb): losses.append({'category':key,'direction':'lost','value':x})
        for x in sorted(sb-sa): losses.append({'category':key,'direction':'added','value':x})
    return losses


def _exchange_records(doc):
    """Normalize portable XML objects before import can discard information."""
    root=doc.getroot()
    definitions={item.get('identifier'):item.findtext(q('name')) for item in root.findall('.//'+q('propertyDefinition'))}
    records={}
    def value(node):
        if node.tag==q('properties'):
            props=[]
            for item in node.findall(q('property')):
                name=definitions.get(item.get('propertyDefinitionRef'),item.get('propertyDefinitionRef'))
                values=[(part.get('{http://www.w3.org/XML/1998/namespace}lang',''),repo_tool.parse_maybe_json(part.text or '')) for part in item.findall(q('value'))]
                props.append((name,values))
            return sorted(props,key=canonical)
        return {'tag':node.tag,'attributes':dict(sorted(node.attrib.items())),
                'text':(node.text or '').strip(),'children':[value(child) for child in node if isinstance(child.tag,str)]}
    for tag in ('element','relationship','view'):
        for node in root.findall('.//'+q(tag)):
            material={'attributes':dict(node.attrib),'content':{}}
            for child in node:
                if isinstance(child.tag,str):
                    material['content'].setdefault(child.tag,[]).append(value(child))
            records[f'{tag}:{node.get("identifier")}']=material
    organizations=root.find(q('organizations'))
    if organizations is not None:
        records['organizations']=value(organizations)
    for definition in root.findall('.//'+q('propertyDefinition')):
        name=definition.findtext(q('name'),definition.get('identifier',''))
        normalized=value(definition)
        normalized['attributes'].pop('identifier',None)
        records.setdefault('property-definition:'+name,[]).append(normalized)
    return records


def _first_import_losses(source, emitted):
    """Compare source obligations against output without treating added metadata as loss."""
    before,after=_exchange_records(source),_exchange_records(emitted)
    losses=[]
    for ident,record in before.items():
        candidate=after.get(ident)
        if candidate is None:
            losses.append({'category':'first-import','direction':'lost','location':ident,'value':record})
            continue
        if ident=='organizations' or ident.startswith('property-definition:'):
            if record!=candidate:
                losses.append({'category':'first-import','direction':'changed','location':ident,'before':record,'after':candidate})
            continue
        for attr,expected in record['attributes'].items():
            if candidate['attributes'].get(attr)!=expected:
                losses.append({'category':'first-import','direction':'changed','location':ident+'/@'+attr,'before':expected,'after':candidate['attributes'].get(attr)})
        for tag,expected in record['content'].items():
            observed=candidate['content'].get(tag,[])
            if tag==q('properties'):
                expected=[entry for container in expected for entry in container]
                observed=[entry for container in observed for entry in container]
                mismatch=any(entry not in observed for entry in expected)
            else:
                mismatch=expected!=observed
            if mismatch:
                losses.append({'category':'first-import','direction':'changed','location':ident+'/'+etree.QName(tag).localname,'before':expected,'after':observed})
    return losses

def conform(xml_path: Path):
    """Return bounded schema, structure, metamodel and fidelity checks for xml_path.

    Uses the offline exchange 3.1 XSD and the selected language 3.2 permission
    table/profile rules. Reads a source file and uses an automatically removed
    temporary round-trip file. Unsupported constructs or lost input information
    prevent ``valid``. A valid result does not grant Open Group certification,
    semantic/visual approval or external-tool interoperability qualification.
    """
    report={'file':str(xml_path),'l1':{},'l2':{},'l3':{},'metamodel':{},'unsupported':{},'valid':False,
            'qualification':{'standard_conformance':'not-established','metamodel_legality':'not-established','visual_notation':'not-assessed','external_tool_interoperability':'not-exercised'}}
    doc,e1=l1(xml_path); report['l1']={'valid':not e1,'errors':e1,'scope':'open-group-authored-exchange-3.1-xsd','language_edition':'3.2'}
    if doc is None: return report
    e2,w2=l2(doc); report['l2']={'valid':not e2,'errors':e2,'warnings':w2}; report['unsupported']=unsupported_constructs(doc)
    losses=[]; first_losses=[]; repo_errors=[]
    try:
        r1=repo_tool.empty_repository('conformance-import','Conformance Import'); repo_tool.import_open_exchange(xml_path,r1,project_id='P-IMP',project_name='Imported',merge=False)
        report['metamodel']=profile.validate(r1)
        report['qualification']['metamodel_legality']='permitted-triples-and-profile-rules-checked' if report['metamodel']['valid'] else 'failed'
        repo_errors.extend(report['metamodel']['errors'])
        ce,cw=repo_tool.validate_repository(r1); repo_errors.extend(ce)
        with tempfile.TemporaryDirectory() as td:
            out=Path(td)/'roundtrip.xml'
            repo_tool.export_open_exchange(r1,out)
            # Check generated output against the same exchange 3.1 XSD and L2
            # structural rules so reimport cannot hide invalid emitted content.
            generated_doc, generated_l1_errors = l1(out)
            generated_l2_errors, generated_l2_warnings = l2(generated_doc) if generated_doc is not None else (['generated export could not be parsed'], [])
            report['l3']['generated_export_l1']={'valid':not generated_l1_errors,'errors':generated_l1_errors}
            report['l3']['generated_export_l2']={'valid':not generated_l2_errors,'errors':generated_l2_errors,'warnings':generated_l2_warnings}
            if generated_l1_errors or generated_l2_errors:
                repo_errors.extend(['generated export conformance: '+x for x in generated_l1_errors+generated_l2_errors])
            if generated_doc is not None:
                first_losses=_first_import_losses(doc,generated_doc)
            r2=repo_tool.empty_repository('conformance-roundtrip','Conformance Roundtrip')
            repo_tool.import_open_exchange(out,r2,project_id='P-IMP',project_name='Imported',merge=False)
            losses=compare(snapshot(r1),snapshot(r2))
            report['l3']['roundtrip_sha256']=hashlib.sha256(out.read_bytes()).hexdigest()
    except Exception as exc: repo_errors.append(str(exc))
    report['l3'].update({'valid':not repo_errors and not losses and not first_losses,'repository_errors':repo_errors,'losses':losses,'first_import_losses':first_losses,'scope':'element/relationship/view content, attributes, properties and definitions, diagram layout and organizations; repository envelope metadata excluded'})
    report['valid']=report['l1']['valid'] and report['l2']['valid'] and report['l3']['valid'] and not any(report['unsupported'].values())
    return report

def cmd_check(a):
    """Print ``a.xml`` checks, optionally write ``a.report``, and return zero only if valid."""
    r=conform(Path(a.xml)); text=json.dumps(r,indent=2,ensure_ascii=False)
    if a.report: Path(a.report).write_text(text+'\n',encoding='utf-8')
    print(text); return 0 if r['valid'] else 1

def self_test():
    """Check packaged positive fixtures and return zero only if all bounded checks pass."""
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
    """Import exchange fixture ``f`` and return its material canonical snapshot."""
    r=repo_tool.empty_repository('fixture','Fixture'); repo_tool.import_open_exchange(f,r,project_id='P-IMP',project_name='Imported',merge=False); return snapshot(r)

def main():
    """Parse CLI arguments and exit with the selected check's status."""
    ap=argparse.ArgumentParser(); sp=ap.add_subparsers(dest='cmd',required=True)
    p=sp.add_parser('check'); p.add_argument('xml'); p.add_argument('--report'); p.set_defaults(fn=cmd_check)
    sp.add_parser('self-test').set_defaults(fn=lambda a:self_test())
    a=ap.parse_args(); raise SystemExit(a.fn(a) or 0)
if __name__=='__main__': main()
