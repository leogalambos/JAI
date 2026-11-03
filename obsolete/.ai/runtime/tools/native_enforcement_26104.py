#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Release-blocking Unified Lifecycle GA suite for stable ArtifactContract v3."""
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

def catalogue_problems(roles_catalog, v2, v3, layers, runtime):
    """Return active catalogue and frozen migration integrity failures.

    Args:
        roles_catalog: Canonical role manifest, including its declared count.
        v2: Immutable legacy contract catalogue (1124 original contracts).
        v3: Current authoritative catalogue, including native additions.
        layers: Canonical JAI layer registry.
        runtime: Runtime directory containing schema and provenance evidence.

    Returns:
        A list of failures. Validation reads JSON evidence only, never role
        bodies; the separate artifact gate verifies source deliverable drift.
        Native provenance is a content binding, never human approval.
    """
    import artifacts
    problems = []
    roles = roles_catalog.get('roles', [])
    old_rows = v2.get('contracts', [])
    rows = v3.get('contracts', [])
    by_role = {row.get('slug'): row for row in roles}
    old = {row.get('id'): row for row in old_rows}
    new = {row.get('id'): row for row in rows}
    layer_map = {row['id']: row for row in layers['layers']}
    if not roles or len(by_role) != len(roles) or None in by_role or roles_catalog.get('count') != len(roles):
        problems.append('canonical role identities/count mismatch')
    for role in roles:
        layer = layer_map.get(role.get('layer'))
        if not layer or role.get('layer_name') != layer['name'] or role.get('jai', {}).get('primary_layer') != role.get('layer'):
            problems.append(f"{role.get('slug')}: invalid role layer binding")
    if len(old_rows) != 1124 or len(old) != len(old_rows) or None in old:
        problems.append('immutable legacy contract cohort must contain 1124 unique identities')
    if not rows or len(new) != len(rows) or None in new:
        problems.append('duplicate, empty or missing authoritative contract identities')
    if v3.get('deliverable_count') != len(rows) or v3.get('role_count') != len(by_role):
        problems.append('active catalogue declared counts mismatch')
    expected_ids = {f"{role.get('slug')}:{number}" for role in roles
                    for number in range(1, len(role.get('primary_deliverables', [])) + 1)}
    if set(new) != expected_ids:
        problems.append('canonical role deliverable identity coverage mismatch')
    if {row.get('role_slug') for row in rows} != set(by_role):
        problems.append('active contract role coverage mismatch')
    if not set(old) <= set(new):
        problems.append('immutable legacy contract identity coverage lost')
    if not jsonschema:
        return problems + ['jsonschema required for native release qualification']
    validator = jsonschema.Draft202012Validator(_load(Path(runtime) / 'schema/contracts/artifact-v3.schema.json'))
    for row in rows:
        cid = row.get('id')
        errors = list(validator.iter_errors(row))
        if errors:
            problems.append(f'{cid}: invalid ArtifactContract v3 schema: {errors[0].message}')
            continue
        role = by_role.get(row.get('role_slug'))
        problems.extend(artifacts._origin_problems(row, old, {'role': role} if role else None, Path(runtime)))
        if cid in old and not _material_v2_equals_v3(old[cid], row):
            problems.append(f'{cid}: immutable legacy material fields changed')
    return problems

def main():
    """Run release checks; return one on any failed catalogue or runtime gate."""
    CHECKS.clear()
    problems=[]
    layers=_load(R/'jai/core/layers.json'); lmap={x['id']:x for x in layers['layers']}
    _check(len(lmap)==6 and layers['authority_boundary']['id']==0 and layers['authority_boundary']['external_to_jai'],'jai-layer-registry-test',problems)
    roles_catalog=_load(R/'roles.json'); workflows_catalog=_load(R/'workflows.json')
    roles=roles_catalog['roles']
    _check(bool(roles_catalog.get('version')) and bool(workflows_catalog.get('version')),'catalogue-release-metadata-conformance',problems)
    _check(len(roles)==roles_catalog.get('count') and all(r.get('layer') in lmap and r.get('layer_name')==lmap[r['layer']]['name'] and r.get('jai',{}).get('primary_layer')==r['layer'] for r in roles),'role-layer-conformance',problems)

    policy=_load(R/'jai/core/native-write-policy.json')
    frozen=(R/'artifacts/contracts/role-deliverables.v2.json').read_bytes()
    _check(bool(policy.get('release')) and policy['rules']['legacy_write_forbidden'] and policy['rules']['production_write_requires_jai'],'native-write-policy',problems)
    _check(policy['legacy_read_only'][0]['sha256']==hashlib.sha256(frozen).hexdigest(),'legacy-v2-immutability-hash',problems)

    v2=_load(R/'artifacts/contracts/role-deliverables.v2.json'); v3=_load(R/'artifacts/contracts/role-deliverables.v3.json')
    catalogue_errors = catalogue_problems(roles_catalog, v2, v3, layers, R)
    _check(not catalogue_errors, 'active-and-immutable-contract-cohorts', problems)
    if catalogue_errors:
        for error in catalogue_errors:
            print('FAIL', error)
        return 1
    old={x['id']:x for x in v2['contracts']}; new={x['id']:x for x in v3['contracts']}
    legacy = {cid: new[cid] for cid in old}
    _check(bool(v3.get('release')) and v3.get('authoritative_write_model') and v3.get('native_write_enforced') and len(new)==v3.get('deliverable_count'),'artifact-v3-native-authority',problems)
    _check(set(old)<=set(new),'artifact-contract-identity-coverage',problems)
    _check(all(set(c['jai'])=={'core_version','intent','semantics','justification','design','realisation','evidence'} for c in new.values()),'artifact-v3-L1-L6-bindings',problems)
    _check(all(c['compatibility']['writes']=='ArtifactContract-v3' for c in new.values()),'artifact-native-write-target',problems)
    _check(all(c.get('migration',{}).get('source_hash')==_h(old[cid]) and c['migration'].get('source_id')==cid for cid,c in legacy.items()),'migration-source-hash-coverage-1124',problems)
    _check(all(_material_v2_equals_v3(old[cid],c) for cid,c in legacy.items()),'migration-loss-test-all-material-fields-1124',problems)

    if jsonschema:
        schema=_load(R/'schema/contracts/artifact-v3.schema.json'); val=jsonschema.Draft202012Validator(schema)
        _check(not any(next(val.iter_errors(c),None) for c in new.values()),'artifact-v3-schema-current',problems)

    mig0=_module_from(R/'jai/migrations/migrate-26.10.0.py','mig26100')
    migrated={cid:mig0.migrate(c) for cid,c in old.items()}
    _check(all({**migrated[cid], "compatibility": {**migrated[cid]["compatibility"], "writes":"ArtifactContract-v3"}}==new[cid] for cid in legacy),'legacy-26.10.0-migration-exact-1124',problems)
    _check(all(mig0.migrate(mig0.migrate(c))==mig0.migrate(c) for c in list(old.values())[:50]),'migration-idempotency-test',problems)
    mig2=_module_from(R/'jai/migrations/migrate-26.10.2.py','mig26102to26104')
    source26102=_module_from(R/'jai/migrations/migrate-26.10.0.py','source26102builder')
    # Reconstruct the material 26.10.2 v3 form from frozen v2, then prove deterministic 26.10.3 migration.
    rows26102=[]
    for c in old.values():
        x=source26102.migrate(c); x['compatibility']['reads']=[r for r in x['compatibility']['reads'] if not r.startswith('26.10.2/')]; x['compatibility']['writes']='26.10.2/ArtifactContract-v3'; rows26102.append(x)
    migrated2={x['id']:mig2.migrate(x) for x in rows26102}
    _check(all({**migrated2[cid], "compatibility": {**migrated2[cid]["compatibility"], "writes":"ArtifactContract-v3"}}==new[cid] for cid in legacy),'legacy-26.10.2-migration-exact-1124',problems)
    mig3=_module_from(R/'jai/migrations/migrate-26.10.3.py','mig26103to26104')
    source3={cid:json.loads(json.dumps(c)) for cid,c in legacy.items()}
    for c in source3.values():
        c['compatibility']['writes']='26.10.3/ArtifactContract-v3'; c['compatibility']['reads']=[x for x in c['compatibility']['reads'] if x!='26.10.3/ArtifactContract-v3']
    migrated3={cid:mig3.migrate(c) for cid,c in source3.items()}
    _check(all({**migrated3[cid], "compatibility": {**migrated3[cid]["compatibility"], "writes":"ArtifactContract-v3"}}==new[cid] for cid in legacy),'legacy-26.10.3-migration-exact-1124',problems)

    reg=_load(R/'schema/schema-registry.json')
    _check(bool(reg.get('release')) and {x['from'] for x in reg['migration_rules']}=={'26.10.0','26.10.1','26.10.2','26.10.3'} and all(x['to']==reg['release'] for x in reg['migration_rules']),'schema-registry-native-namespace',problems)
    _check(all((R/x['path']).is_file() and x['path'].startswith('schema/') for x in reg['schemas']),'schema-registry-paths-resolve',problems)
    stale_current_schema=[]
    for sp in (R/'schema'/reg['release']).glob('*.json'):
        try: sd=_load(sp)
        except Exception: continue
        if '26.10.3' in str(sd.get('title','')): stale_current_schema.append(sp.name)
    _check(not stale_current_schema,'current-schema-title-release-conformance',problems)
    operator_docs=[P/'.ai/agents/architecture-repository-engineer.md',P/'.ai/commands/repository.md']
    _check(all('26.10.3' not in p.read_text(encoding='utf-8') for p in operator_docs),'operator-current-release-reference-conformance',problems)

    gen=_load(R/'artifacts/role-deliverables.json')
    _check(gen.get('source')=='contracts/role-deliverables.v3.json' and gen.get('schema_version')=='3.0.0','generated-registry-native-v3-source',problems)

    sab=_load(R/'jai/profiles/sabsa-profile.json'); ea=_load(R/'jai/profiles/ea-profile.json'); pub=_load(R/'jai/profiles/publication-profile.json'); runtime=_load(R/'jai/profiles/runtime-profile.json')
    _check('orthogonal' in sab['rule'].lower() or 'never derived' in sab['rule'].lower(),'versioned-sabsa-catalogue-classification-test',problems)
    _check(ea.get('global_source_of_truth') is False and ea.get('authoritative_for')=='ea-domain-projection','ea-source-of-truth-test',problems)
    _check(set(pub['jai_mapping'])=={'L1','L2','L3','L4','L5','L6'} and bool(pub.get('release')),'publication-profile-JAI-lineage',problems)
    _check(set(runtime['jai_mapping'])=={'L1','L2','L3','L4','L5','L6'} and bool(runtime.get('release')),'runtime-profile-test',problems)

    contracts=_load(R/'agents/agent-contracts.json')['contracts']; bindings=_load(R/'jai/profiles/runtime-agent-bindings.json')
    _check(bool(bindings.get('release')) and {x['id'] for x in contracts}==set(bindings['bindings']),'agent-contract-JAI-binding-coverage',problems)
    _check(bool(_load(R/'jai/profiles/runtime-policy-binding.json').get('release')),'policy-contract-JAI-binding',problems)
    embedded={c['id']:c.get('jai',{}) for c in contracts}
    _check(all(j.get('profile')=='runtime' and j.get('layer')==bindings['bindings'][cid]['primary_layer'] for cid,j in embedded.items()),'runtime-agent-profile-native-contracts',problems)
    managed=_load(R/'policy/managed-policy.json')
    _check(managed.get('jai_profile',{}).get('profile')=='runtime' and managed.get('jai_profile',{}).get('layers')==[1,2,3,4,5,6],'runtime-policy-profile-native-contract',problems)

    # Pre-cutover catalogue validation is not format-3 authority or confinement.
    from governed_probe import governed_record_probe
    _check(governed_record_probe(),'fabric-governed-identity-and-origin-test',problems)

    projection=_module_from(R/'tools/projection.py','projection26104')
    profile={'id':'decision-paper','audience':['ARB'],'mandatory_sections':['Context'],'mandatory_semantic_fields':['claims','evidence']}
    model={'artifact_id':'A','claims':[{'id':'C','evidence':['E1']}],'sections':[{'heading':'Context','body':'x'}]}
    _,man=projection.select_sections(model,profile)
    _check(not projection.validate_manifest(man) and set(man['jai'])=={'intent_ref','semantic_snapshot_ref','policy_ref','design_ref','realisation_ref','evidence_refs'},'publication-lineage-test',problems)

    resolver=_module_from(R/'tools/schema_resolver.py','schema_resolver26104')
    _check(resolver.self_test()==0,'current-release-schema-resolver-test',problems)
    architecture_lint=_module_from(R/'tools/architecture_claim_lint.py','architecture_claim_lint26104')
    _check(architecture_lint.main()==0,'architecture-claim-lint-test',problems)
    repository=_module_from(R/'tools/repository.py','repository26104')
    rr=repository.empty_repository('R','Scoped EA'); repository.save_repo(Path(tempfile.gettempdir())/'aiithouse-26104-native-repo.json',rr)
    _check(bool(rr.get('schema_version')) and rr.get('repository',{}).get('authoritative_for')=='ea-domain-projection' and rr.get('repository',{}).get('global_source_of_truth') is False and rr.get('repository',{}).get('semantic_identity_authority')=='JAI','ea-profile-native-write-test',problems)
    bridge=_module_from(R/'tools/sabsa_ea.py','sabsa_ea26104')
    sample={'driver:x':{'id':'driver:x','title':'X','owner':'Owner','_dirtype':'driver','_path':'drivers/x.json'}}
    elem=bridge.element_from('driver:x',sample['driver:x'],bridge.mapping()['rules']['driver'],'P',bridge.mapping()['mapping_version'])
    _check(bool(elem.get('canonical_ref')) and elem.get('jai',{}).get('layer')==2 and elem.get('source_specialisations')==[{'profile':'sabsa','ref':'sabsa:driver:x'}] and elem.get('projection',{}).get('bridge')=='sabsa-ea-jai-profile','sabsa-ea-profile-native-projection-test',problems)
    # Native SABSA authoring must persist JAI identity at the source, not only at EA projection time.
    sabsa_tool=_module_from(R/'tools/sabsa.py','sabsa26104')
    with tempfile.TemporaryDirectory() as td:
        lib=Path(td)/'lib'; ns=type('N',(),{})(); ns.lib=str(lib); ns.name='Native'; ns.organisation='Org'; ns.scope='Scope'; ns.owner='Owner'
        sabsa_tool.cmd_init(ns)
        nn=type('N',(),{})(); nn.lib=str(lib); nn.type='driver'; nn.title='Native driver'; nn.set=['statement=Need','owner=Owner','basis=assumed']
        sabsa_tool.cmd_new(nn)
        meta=sabsa_tool.parse(str(lib/'01-contextual/drivers/BD-001.md'))
        lmeta=sabsa_tool.parse(str(lib/'library.md'))
        _check(meta.get('canonical_ref')=='semantic:sabsa:BD-001' and meta.get('jai_profile')=='sabsa' and str(meta.get('jai_layer'))=='2' and bool(meta.get('jai_release')) and lmeta.get('semantic_identity_authority')=='JAI','sabsa-profile-native-write-test',problems)
    execution=_module_from(R/'tools/execution_record.py','execution26104'); rec=execution.make(provider='codex',model='qualification',agent='gate-auditor')
    _check(rec.get('release')==RELEASE and rec.get('profile')=='runtime' and rec.get('jai',{}).get('layer')==6 and rec.get('jai',{}).get('profile')=='runtime','execution-record-JAI-L6-native-test',problems)
    behavior=_module_from(R/'tools/behavioral_eval.py','behavior26104')
    refused,_=behavior.qualify(behavior.REFS,fixture_mode=False)
    fixture_problems,_=behavior.qualify(behavior.REFS,fixture_mode=True)
    _check(bool(refused) and 'evaluator fixtures' in refused[0] and not fixture_problems,'behavioral-live-fixture-boundary-test',problems)

    q=_load(R/'jai/qualification-mapping.json'); _check(set(q['dimensions'])==set('ABCDEFGH'),'qualification-mapping-test',problems)
    bad=[]
    for p in (R/'jai').rglob('*.json'):
        if '"source_of_truth": true' in p.read_text(encoding='utf-8').lower(): bad.append(str(p))
    _check(not bad,'parallel-authority-test',problems)

    # Production validation/orchestration may mention v2 only in explicit compatibility/migration code.
    allowed={'artifacts.py','native_enforcement_26102.py','native_enforcement_26103.py','native_enforcement_26104.py','convergence_26101.py'}
    refs=[]
    for p in (R/'tools').glob('*.py'):
        if p.name in allowed: continue
        if 'role-deliverables.v2.json' in p.read_text(encoding='utf-8'): refs.append(p.name)
    if 'role-deliverables.v2.json' in (R/'scripts/check_agent_policy.py').read_text(encoding='utf-8'): refs.append('scripts/check_agent_policy.py')
    _check(not refs,'no-legacy-v2-production-authority',problems)

    print(f'{RELEASE} Unified Lifecycle GA: {sum(ok for _,ok in CHECKS)}/{len(CHECKS)} checks PASS')
    return 0 if not problems else 1
if __name__=='__main__': raise SystemExit(main())
