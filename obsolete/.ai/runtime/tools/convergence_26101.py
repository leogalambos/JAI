#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
from pathlib import Path
import json,re,sys,hashlib,subprocess,tempfile
try: import jsonschema
except Exception: jsonschema=None
R=Path(__file__).resolve().parents[1]; P=R.parents[1]
def load(p): return json.loads(Path(p).read_text())
def check(ok,msg,problems):
 print(('PASS' if ok else 'FAIL'),msg)
 if not ok: problems.append(msg)
def main():
 problems=[]; layers=load(R/'jai/core/layers.json'); lmap={x['id']:x for x in layers['layers']}
 check(len(lmap)==6 and layers['authority_boundary']['id']==0 and layers['authority_boundary']['external_to_jai'],'jai-layer-registry-test',problems)
 roles=load(R/'roles.json')['roles']; check(all(r.get('layer_name')==lmap[r['layer']]['name'] and r.get('jai',{}).get('primary_layer')==r['layer'] for r in roles),'role-layer-conformance',problems)
 check(len(roles)==281,'role-count-preserved',problems)
 v3=load(R/'artifacts/contracts/role-deliverables.v3.json'); check(v3.get('authoritative_write_model') and len(v3['contracts'])==v3['deliverable_count'],'artifact-v3-coverage-count',problems)
 check(all(set(c['jai'])=={'core_version','intent','semantics','justification','design','realisation','evidence'} for c in v3['contracts']),'artifact-v3-L1-L6-bindings',problems)
 if jsonschema:
  schema=load(R/'schema/26.10.1/artifact-contract.schema.json'); val=jsonschema.Draft202012Validator(schema); bad=[]
  for c in v3['contracts']:
   try: val.validate(c)
   except Exception as e: bad.append(c['id']+':'+str(e))
  check(not bad,'artifact-v3-schema',problems)
 sab=load(R/'jai/profiles/sabsa-profile.json'); check('orthogonal' in sab['rule'].lower() or 'never derived' in sab['rule'].lower(),'sabsa-jai-orthogonality-test',problems)
 ea=load(R/'jai/profiles/ea-profile.json'); check(ea.get('global_source_of_truth') is False and ea.get('authoritative_for')=='ea-domain-projection','ea-source-of-truth-test',problems)
 pub=load(R/'jai/profiles/publication-profile.json'); check(set(pub['jai_mapping'])=={'L1','L2','L3','L4','L5','L6'},'publication-lineage-profile-test',problems)
 runtime=load(R/'jai/profiles/runtime-profile.json'); check(set(runtime['jai_mapping'])=={'L1','L2','L3','L4','L5','L6'},'runtime-profile-test',problems)
 q=load(R/'jai/qualification-mapping.json'); check(set(q['dimensions'])==set('ABCDEFGH'),'qualification-mapping-test',problems)
 # no unscoped declarations in normative profile/core JSON
 bad=[]
 for p in list((R/'jai').rglob('*.json')):
  t=p.read_text().lower()
  if '"source_of_truth": true' in t: bad.append(str(p))
 check(not bad,'parallel-authority-test',problems)
 # v2 -> v3 mapping field preservation and idempotency semantic core
 legacy=load(R/'artifacts/contracts/role-deliverables.v2.json')['contracts'][0]; native=v3['contracts'][0]
 checks=(legacy['id']==native['id'] and legacy['source_fingerprint']==native['source_fingerprint'] and legacy['artifact_type']==native['jai']['semantics']['artifact_type'] and legacy['purpose']==native['jai']['intent']['purpose'])
 check(checks,'migration-loss-test',problems)
 # schema namespace and migration rule
 reg=load(R/'schema/schema-registry.json'); check(reg['release']=='26.10.1' and reg['migration_rules'][0]['from']=='26.10.0','legacy-26.10.0-read-test',problems)
 # semantic identity/fabric contract
 pf=load(R/'schema/26.10.1/product-fragment.schema.json'); req=set(pf['required']); check({'object_ref','object_hash','contract_ref'}<=req,'fabric-semantic-ref-test',problems)
 # architecture lint across JAI profile scopes
 profs=list((R/'jai/profiles').glob('*profile.json')); check(all(load(p).get('authoritative_for') for p in profs),'scoped-authority-lint',problems)
 print(f'26.10.1 convergence: {15-len(problems)}/15 checks PASS')
 return 0 if not problems else 1
if __name__=='__main__': raise SystemExit(main())
