#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Release-blocking convergence carry-over + Native JAI Enforcement suite for 26.10.2."""
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

def _load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def _h(v): return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
CHECKS=[]
def _check(ok,msg,problems):
    CHECKS.append((msg,bool(ok)))
    print(('PASS' if ok else 'FAIL'),msg)
    if not ok: problems.append(msg)
def _module_from(path,name):
    spec=importlib.util.spec_from_file_location(name,path); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

def _material_v2_equals_v3(old,new):
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
    """Check this exact archived release without reading another release's catalogue.

    Returns:
        Zero if the exact archive passes; one for an unsupported release or failed gate.
    """
    if RELEASE != '26.10.2':
        print('Unsupported archive-only gate: native_enforcement_26102 requires 26.10.2; active release is ' + RELEASE)
        return 1
    problems=[]
    layers=_load(R/'jai/core/layers.json'); lmap={x['id']:x for x in layers['layers']}
    _check(RELEASE=='26.10.2','release-identity',problems)
    _check(len(lmap)==6 and layers['authority_boundary']['id']==0 and layers['authority_boundary']['external_to_jai'],'jai-layer-registry-test',problems)
    roles=_load(R/'roles.json')['roles']
    _check(len(roles)==281 and all(r.get('layer_name')==lmap[r['layer']]['name'] and r.get('jai',{}).get('primary_layer')==r['layer'] for r in roles),'role-layer-conformance',problems)

    policy=_load(R/'jai/core/native-write-policy.json')
    frozen=(R/'artifacts/contracts/role-deliverables.v2.json').read_bytes()
    _check(policy['release']==RELEASE and policy['rules']['legacy_write_forbidden'] and policy['rules']['production_write_requires_jai'],'native-write-policy',problems)
    _check(policy['legacy_read_only'][0]['sha256']==hashlib.sha256(frozen).hexdigest(),'legacy-v2-immutability-hash',problems)

    v2=_load(R/'artifacts/contracts/role-deliverables.v2.json'); v3=_load(R/'artifacts/contracts/role-deliverables.v3.json')
    old={x['id']:x for x in v2['contracts']}; new={x['id']:x for x in v3['contracts']}
    _check(v3.get('release')==RELEASE and v3.get('authoritative_write_model') and v3.get('native_write_enforced') and len(new)==1124,'artifact-v3-native-authority',problems)
    _check(set(old)==set(new),'artifact-contract-identity-coverage',problems)
    _check(all(set(c['jai'])=={'core_version','intent','semantics','justification','design','realisation','evidence'} for c in new.values()),'artifact-v3-L1-L6-bindings',problems)
    _check(all(c['compatibility']['writes']=='26.10.2/ArtifactContract-v3' for c in new.values()),'artifact-native-write-target',problems)
    _check(all(c.get('migration',{}).get('source_hash')==_h(old[cid]) and c['migration'].get('source_id')==cid for cid,c in new.items()),'migration-source-hash-coverage-1124',problems)
    _check(all(_material_v2_equals_v3(old[cid],c) for cid,c in new.items()),'migration-loss-test-all-material-fields-1124',problems)

    if jsonschema:
        schema=_load(R/'schema/26.10.2/artifact-contract.schema.json'); val=jsonschema.Draft202012Validator(schema)
        _check(not any(next(val.iter_errors(c),None) for c in new.values()),'artifact-v3-schema-1124',problems)

    mig0=_module_from(R/'jai/migrations/migrate-26.10.0.py','mig26100')
    migrated={cid:mig0.migrate(c) for cid,c in old.items()}
    _check(all(migrated[cid]==new[cid] for cid in new),'legacy-26.10.0-migration-exact-1124',problems)
    _check(all(mig0.migrate(mig0.migrate(c))==mig0.migrate(c) for c in list(old.values())[:50]),'migration-idempotency-test',problems)

    reg=_load(R/'schema/schema-registry.json')
    _check(reg['release']==RELEASE and {x['from'] for x in reg['migration_rules']}=={'26.10.0','26.10.1'} and all(x['to']==RELEASE for x in reg['migration_rules']),'schema-registry-native-namespace',problems)
    _check(all('/26.10.2/' in x['path'] for x in reg['schemas']),'schema-path-native-namespace',problems)

    gen=_load(R/'artifacts/role-deliverables.json')
    _check(gen.get('source')=='contracts/role-deliverables.v3.json' and gen.get('schema_version')=='3.0.0','generated-registry-native-v3-source',problems)

    sab=_load(R/'jai/profiles/sabsa-profile.json'); ea=_load(R/'jai/profiles/ea-profile.json'); pub=_load(R/'jai/profiles/publication-profile.json'); runtime=_load(R/'jai/profiles/runtime-profile.json')
    _check('orthogonal' in sab['rule'].lower() or 'never derived' in sab['rule'].lower(),'versioned-sabsa-catalogue-classification-test',problems)
    _check(ea.get('global_source_of_truth') is False and ea.get('authoritative_for')=='ea-domain-projection','ea-source-of-truth-test',problems)
    _check(set(pub['jai_mapping'])=={'L1','L2','L3','L4','L5','L6'} and pub.get('release')==RELEASE,'publication-profile-JAI-lineage',problems)
    _check(set(runtime['jai_mapping'])=={'L1','L2','L3','L4','L5','L6'} and runtime.get('release')==RELEASE,'runtime-profile-test',problems)

    contracts=_load(R/'agents/agent-contracts.json')['contracts']; bindings=_load(R/'jai/profiles/runtime-agent-bindings.json')
    _check(bindings.get('release')==RELEASE and {x['id'] for x in contracts}==set(bindings['bindings']),'agent-contract-JAI-binding-coverage',problems)
    _check(_load(R/'jai/profiles/runtime-policy-binding.json').get('release')==RELEASE,'policy-contract-JAI-binding',problems)

    # Pre-cutover catalogue validation is not format-3 authority or confinement.
    from governed_probe import governed_record_probe
    _check(governed_record_probe(),'fabric-governed-identity-and-origin-test',problems)

    projection=_module_from(R/'tools/projection.py','projection26102')
    profile={'id':'decision-paper','audience':['ARB'],'mandatory_sections':['Context'],'mandatory_semantic_fields':['claims','evidence']}
    model={'artifact_id':'A','claims':[{'id':'C','evidence':['E1']}],'sections':[{'heading':'Context','body':'x'}]}
    _,man=projection.select_sections(model,profile)
    _check(not projection.validate_manifest(man) and set(man['jai'])=={'intent_ref','semantic_snapshot_ref','policy_ref','design_ref','realisation_ref','evidence_refs'},'publication-lineage-test',problems)

    q=_load(R/'jai/qualification-mapping.json'); _check(set(q['dimensions'])==set('ABCDEFGH'),'qualification-mapping-test',problems)
    bad=[]
    for p in (R/'jai').rglob('*.json'):
        if '"source_of_truth": true' in p.read_text(encoding='utf-8').lower(): bad.append(str(p))
    _check(not bad,'parallel-authority-test',problems)

    # Production validation/orchestration may mention v2 only in explicit compatibility/migration code.
    allowed={'artifacts.py','native_enforcement_26102.py','convergence_26101.py'}
    refs=[]
    for p in (R/'tools').glob('*.py'):
        if p.name in allowed: continue
        if 'role-deliverables.v2.json' in p.read_text(encoding='utf-8'): refs.append(p.name)
    if 'role-deliverables.v2.json' in (R/'scripts/check_agent_policy.py').read_text(encoding='utf-8'): refs.append('scripts/check_agent_policy.py')
    _check(not refs,'no-legacy-v2-production-authority',problems)

    print(f'26.10.2 Native JAI Enforcement: {sum(ok for _,ok in CHECKS)}/{len(CHECKS)} checks PASS')
    return 0 if not problems else 1
if __name__=='__main__': raise SystemExit(main())
