#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Release-blocking convergence carry-over + Unified Lifecycle Hardening suite for 26.10.3."""
from __future__ import annotations
import hashlib, importlib.util, json, re, tempfile
from pathlib import Path
try:
    import jsonschema
except Exception:
    jsonschema=None

R=Path(__file__).resolve().parents[1]
P=R.parents[1]
RELEASE=((P/'VERSION') if (P/'VERSION').is_file() else R/'VERSION').read_text().strip()

def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def h(v): return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
CHECKS=[]
def check(ok,msg,problems):
    CHECKS.append((msg,bool(ok)))
    print(('PASS' if ok else 'FAIL'),msg)
    if not ok: problems.append(msg)
def module_from(path,name):
    spec=importlib.util.spec_from_file_location(name,path); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

def material_v2_equals_v3(old,new):
    j=new['jai']; i=j['intent']; s=j['semantics']; q=j['justification']; d=j['design']; r=j['realisation']; e=j['evidence']
    mapping={
      'id':new['id'],'role_slug':new['role_slug'],'deliverable_number':new['deliverable_number'],'source_fingerprint':new['source_fingerprint'],
      'owner_role':i['owner_role'],'artifact_type':s['artifact_type'],'purpose':i['purpose'],'audience':i['audience'],'decision_supported':i['decision_supported'],
      'schema_ref':s['schema_ref'],'required_inputs':s['required_inputs'],'required_evidence':q['required_evidence'],'required_relations':s['required_relations'],
      'mandatory_sections':d['mandatory_sections'],'producer':r['producer'],'reviewers':q['reviewers'],'approver':q['approver'],'renderer':r['renderer'],
      'output_formats':r['output_formats'],'publication_profile':d['publication_profile'],'acceptance_profile':q['acceptance_profile'],'evidence_profile':q['evidence_profile'],
      'system_of_record':r['system_of_record'],'external_handoff_adapter':r['external_handoff_adapter'],'classification':i['classification'],
      'lifecycle':{**{k:v for k,v in new['lifecycle'].items() if k not in ('retention','version')},'version':old.get('lifecycle',{}).get('version')},'retention':new['lifecycle'].get('retention'),'traceability':new['traceability'],
      'production_mode':r['production_mode'],'semantic_gate':q['semantic_policy'],'publication_gate':e['publication_gate'],'repository_gate':q['repository_policy'],
      'portfolio_traceability':e['portfolio_traceability']
    }
    # version and classification_source are intentionally version-governance fields, not semantic payload.
    return all(old.get(k)==mapping.get(k) for k in mapping)

def main():
    problems=[]
    layers=load(R/'jai/core/layers.json'); lmap={x['id']:x for x in layers['layers']}
    check(RELEASE=='26.10.3','release-identity',problems)
    check(len(lmap)==6 and layers['authority_boundary']['id']==0 and layers['authority_boundary']['external_to_jai'],'jai-layer-registry-test',problems)
    roles=load(R/'roles.json')['roles']
    check(len(roles)==281 and all(r.get('layer_name')==lmap[r['layer']]['name'] and r.get('jai',{}).get('primary_layer')==r['layer'] for r in roles),'role-layer-conformance',problems)

    policy=load(R/'jai/core/native-write-policy.json')
    frozen=(R/'artifacts/contracts/role-deliverables.v2.json').read_bytes()
    check(policy['release']==RELEASE and policy['rules']['legacy_write_forbidden'] and policy['rules']['production_write_requires_jai'],'native-write-policy',problems)
    check(policy['legacy_read_only'][0]['sha256']==hashlib.sha256(frozen).hexdigest(),'legacy-v2-immutability-hash',problems)

    v2=load(R/'artifacts/contracts/role-deliverables.v2.json'); v3=load(R/'artifacts/contracts/role-deliverables.v3.json')
    old={x['id']:x for x in v2['contracts']}; new={x['id']:x for x in v3['contracts']}
    check(v3.get('release')==RELEASE and v3.get('authoritative_write_model') and v3.get('native_write_enforced') and len(new)==1124,'artifact-v3-native-authority',problems)
    check(set(old)==set(new),'artifact-contract-identity-coverage',problems)
    check(all(set(c['jai'])=={'core_version','intent','semantics','justification','design','realisation','evidence'} for c in new.values()),'artifact-v3-L1-L6-bindings',problems)
    check(all(c['compatibility']['writes']=='26.10.3/ArtifactContract-v3' for c in new.values()),'artifact-native-write-target',problems)
    check(all(c.get('migration',{}).get('source_hash')==h(old[cid]) and c['migration'].get('source_id')==cid for cid,c in new.items()),'migration-source-hash-coverage-1124',problems)
    check(all(material_v2_equals_v3(old[cid],c) for cid,c in new.items()),'migration-loss-test-all-material-fields-1124',problems)

    if jsonschema:
        schema=load(R/'schema/26.10.3/artifact-contract.schema.json'); val=jsonschema.Draft202012Validator(schema)
        check(not any(next(val.iter_errors(c),None) for c in new.values()),'artifact-v3-schema-1124',problems)

    mig0=module_from(R/'jai/migrations/migrate-26.10.0.py','mig26100')
    migrated={cid:mig0.migrate(c) for cid,c in old.items()}
    check(all(migrated[cid]==new[cid] for cid in new),'legacy-26.10.0-migration-exact-1124',problems)
    check(all(mig0.migrate(mig0.migrate(c))==mig0.migrate(c) for c in list(old.values())[:50]),'migration-idempotency-test',problems)
    mig2=module_from(R/'jai/migrations/migrate-26.10.2.py','mig26102to26103')
    source26102=module_from(R/'jai/migrations/migrate-26.10.0.py','source26102builder')
    # Reconstruct the material 26.10.2 v3 form from frozen v2, then prove deterministic 26.10.3 migration.
    rows26102=[]
    for c in old.values():
        x=source26102.migrate(c); x['compatibility']['reads']=[r for r in x['compatibility']['reads'] if not r.startswith('26.10.2/')]; x['compatibility']['writes']='26.10.2/ArtifactContract-v3'; rows26102.append(x)
    migrated2={x['id']:mig2.migrate(x) for x in rows26102}
    check(all(migrated2[cid]==new[cid] for cid in new),'legacy-26.10.2-migration-exact-1124',problems)

    reg=load(R/'schema/schema-registry.json')
    check(reg['release']==RELEASE and {x['from'] for x in reg['migration_rules']}=={'26.10.0','26.10.1','26.10.2'} and all(x['to']==RELEASE for x in reg['migration_rules']),'schema-registry-native-namespace',problems)
    check(all('/26.10.3/' in x['path'] for x in reg['schemas']),'schema-path-native-namespace',problems)

    gen=load(R/'artifacts/role-deliverables.json')
    check(gen.get('source')=='contracts/role-deliverables.v3.json' and gen.get('schema_version')=='3.0.0','generated-registry-native-v3-source',problems)

    sab=load(R/'jai/profiles/sabsa-profile.json'); ea=load(R/'jai/profiles/ea-profile.json'); pub=load(R/'jai/profiles/publication-profile.json'); runtime=load(R/'jai/profiles/runtime-profile.json')
    check('orthogonal' in sab['rule'].lower() or 'never derived' in sab['rule'].lower(),'sabsa-jai-orthogonality-test',problems)
    check(ea.get('global_source_of_truth') is False and ea.get('authoritative_for')=='ea-domain-projection','ea-source-of-truth-test',problems)
    check(set(pub['jai_mapping'])=={'L1','L2','L3','L4','L5','L6'} and pub.get('release')==RELEASE,'publication-profile-JAI-lineage',problems)
    check(set(runtime['jai_mapping'])=={'L1','L2','L3','L4','L5','L6'} and runtime.get('release')==RELEASE,'runtime-profile-test',problems)

    contracts=load(R/'agents/agent-contracts.json')['contracts']; bindings=load(R/'jai/profiles/runtime-agent-bindings.json')
    check(bindings.get('release')==RELEASE and {x['id'] for x in contracts}==set(bindings['bindings']),'agent-contract-JAI-binding-coverage',problems)
    check(load(R/'jai/profiles/runtime-policy-binding.json').get('release')==RELEASE,'policy-contract-JAI-binding',problems)

    # Fabric runtime must persist ProductFragment identity rather than merely declaring a schema.
    fabric=module_from(R/'fabric/fabric.py','fabric26103')
    with tempfile.TemporaryDirectory() as td:
        fabric.FABRIC_DIR=td
        fb=fabric.Fabric('native-check',[])
        frag=fb.add_node('frag',3,'material claim',kind='claim',contract='ctr-0001')
        evd=fb.add_node('evd',3,'source record',confidence='observation',contract='ctr-0001')
        needed={'version_id','object_ref','object_hash','contract_ref','context_digest'}
        ok=all(needed<=set(x) and x['object_ref']=='lifecycle:'+x['id']
               and x['object_hash']=='sha256:'+x['version_id']
               and fabric.lifecycle.version_id(fb.lifecycle.versions[x['version_id']])==x['version_id']
               for x in (frag,evd))
        check(ok,'fabric-semantic-ref-runtime-test',problems)

    projection=module_from(R/'tools/projection.py','projection26103')
    profile={'id':'decision-paper','audience':['ARB'],'mandatory_sections':['Context'],'mandatory_semantic_fields':['claims','evidence']}
    model={'artifact_id':'A','claims':[{'id':'C','evidence':['E1']}],'sections':[{'heading':'Context','body':'x'}]}
    _,man=projection.select_sections(model,profile)
    check(not projection.validate_manifest(man) and set(man['jai'])=={'intent_ref','semantic_snapshot_ref','policy_ref','design_ref','realisation_ref','evidence_refs'},'publication-lineage-test',problems)

    resolver=module_from(R/'tools/schema_resolver.py','schema_resolver26103')
    check(resolver.self_test()==0,'current-release-schema-resolver-test',problems)
    architecture_lint=module_from(R/'tools/architecture_claim_lint.py','architecture_claim_lint26103')
    check(architecture_lint.main()==0,'architecture-claim-lint-test',problems)
    repository=module_from(R/'tools/repository.py','repository26103')
    rr=repository.empty_repository('R','Scoped EA'); repository.save_repo(Path(tempfile.gettempdir())/'aiithouse-26103-native-repo.json',rr)
    check(rr.get('schema_version')==RELEASE and rr.get('repository',{}).get('authoritative_for')=='ea-domain-projection' and rr.get('repository',{}).get('global_source_of_truth') is False and rr.get('repository',{}).get('semantic_identity_authority')=='JAI','ea-profile-native-write-test',problems)
    bridge=module_from(R/'tools/sabsa_ea.py','sabsa_ea26103')
    sample={'driver:x':{'id':'driver:x','title':'X','owner':'Owner','_dirtype':'driver','_path':'drivers/x.json'}}
    elem=bridge.element_from('driver:x',sample['driver:x'],bridge.mapping()['rules']['driver'],'P',bridge.mapping()['mapping_version'])
    check(bool(elem.get('canonical_ref')) and elem.get('jai',{}).get('layer')==2 and elem.get('source_specialisations')==[{'profile':'sabsa','ref':'sabsa:driver:x'}] and elem.get('projection',{}).get('bridge')=='sabsa-ea-jai-profile','sabsa-ea-profile-native-projection-test',problems)

    q=load(R/'jai/qualification-mapping.json'); check(set(q['dimensions'])==set('ABCDEFGH'),'qualification-mapping-test',problems)
    bad=[]
    for p in (R/'jai').rglob('*.json'):
        if '"source_of_truth": true' in p.read_text(encoding='utf-8').lower(): bad.append(str(p))
    check(not bad,'parallel-authority-test',problems)

    # Production validation/orchestration may mention v2 only in explicit compatibility/migration code.
    allowed={'artifacts.py','native_enforcement_26102.py','native_enforcement_26103.py','convergence_26101.py'}
    refs=[]
    for p in (R/'tools').glob('*.py'):
        if p.name in allowed: continue
        if 'role-deliverables.v2.json' in p.read_text(encoding='utf-8'): refs.append(p.name)
    if 'role-deliverables.v2.json' in (R/'scripts/check_agent_policy.py').read_text(encoding='utf-8'): refs.append('scripts/check_agent_policy.py')
    check(not refs,'no-legacy-v2-production-authority',problems)

    print(f'26.10.3 Unified Lifecycle Hardening: {sum(ok for _,ok in CHECKS)}/{len(CHECKS)} checks PASS')
    return 0 if not problems else 1
if __name__=='__main__': raise SystemExit(main())
