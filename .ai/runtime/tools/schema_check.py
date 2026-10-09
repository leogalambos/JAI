#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""26.10 GA semantic schema and cross-file referential-integrity validator."""
from __future__ import annotations
import argparse, json, subprocess, sys
import artifacts as artifact_registry
from pathlib import Path
try:
    import jsonschema
except Exception as exc:
    raise SystemExit(f'jsonschema is required for schema qualification: {exc}')


def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))

def runtime(root: Path)->Path:
    for p in (root/'.ai/runtime',root/'it-role-library',root/'.ai/it-role-house',root):
        if (p/'schema/schema-registry.json').is_file(): return p
    raise SystemExit('runtime schema registry not found')

def check(root: Path):
    rt=runtime(root.resolve()); problems=[]; reg=load(rt/'schema/schema-registry.json')
    if not reg.get('backward_compatibility_policy'): problems.append('schema registry missing backward compatibility policy')
    if 'migration_rules' not in reg or not isinstance(reg.get('migration_rules'), list): problems.append('schema registry migration_rules must be a list')
    names=set()
    for item in reg.get('schemas',[]):
        name=item.get('name'); path=rt/item.get('path','')
        if name in names: problems.append(f'duplicate schema name {name}')
        names.add(name)
        if not path.is_file(): problems.append(f'{name}: schema path missing {path}'); continue
        try:
            doc=load(path); jsonschema.Draft202012Validator.check_schema(doc)
            expected_id='https://ai-it-house.local/'+item.get('path','')
            if doc.get('$id')!=expected_id:
                problems.append(f"{name}: $id {doc.get('$id')!r} != {expected_id!r}")
            if item.get('critical') and doc.get('additionalProperties') is not False: problems.append(f'{name}: critical schema must set additionalProperties=false')
        except Exception as exc: problems.append(f'{name}: invalid schema: {exc}')
    required={'NativeWritePolicy','ArtifactContract','SABSAElement','EAElement','Relationship','Decision','Claim','Evidence','Risk','Approval','ProjectionManifest','Workflow','WorkflowStep','AgentContract','PolicyContract','PublicationProfile','EvaluationCase','EvaluationResult','EnterpriseAdapterContract','ExecutionRecord','ModelRegistry','ServiceLevels','ReleasePolicy'}
    for x in sorted(required-names): problems.append(f'missing required schema {x}')
    taxonomy=load(rt/'artifacts/schema/artifact-types.json')
    for t,spec in taxonomy.get('artifact_types',{}).items():
        ref=spec.get('schema_ref')
        if ref!='external' and not (rt/ref).is_file(): problems.append(f'artifact type {t}: schema_ref missing {ref}')
        if spec.get('production_mode')=='internal':
            for k in ('producer','renderer'):
                token=str(spec.get(k,'')).split()[0]
                if token and not token.startswith('external:') and not (rt/token).exists(): problems.append(f'artifact type {t}: {k} missing {token}')
    # Authoritative v3 contract references must resolve to taxonomy/profile/archetype definitions.
    src=load(rt/'artifacts/contracts/role-deliverables.v3.json'); profiles=load(rt/'artifacts/profiles/acceptance-evidence.json')
    types=taxonomy.get('artifact_types',{}); acc=profiles.get('acceptance_profiles',{}); ev=profiles.get('evidence_profiles',{})
    artifact_schema=next((load(rt/x['path']) for x in reg.get('schemas',[]) if x.get('name')=='ArtifactContract'),None)
    artifact_validator=jsonschema.Draft202012Validator(artifact_schema) if artifact_schema else None
    for raw in src.get('contracts',[]):
        if artifact_validator:
            for err in artifact_validator.iter_errors(raw): problems.append(f"{raw.get('id')}: ArtifactContract schema: {err.message}")
        c=artifact_registry.flatten_v3(raw)
        if c.get('artifact_type') not in types: problems.append(f"{c.get('id')}: artifact type ref unresolved")
        if c.get('acceptance_profile') not in acc: problems.append(f"{c.get('id')}: acceptance profile ref unresolved")
        if c.get('evidence_profile') not in ev: problems.append(f"{c.get('id')}: evidence profile ref unresolved")
        pp=c.get('publication_profile')
        if pp and types.get(c.get('artifact_type'),{}).get('production_mode')=='internal' and c.get('artifact_type')!='model':
            if not (rt/f'publication/archetypes/{pp}.json').is_file(): problems.append(f"{c.get('id')}: publication profile/archetype missing {pp}")
    # Runtime workflow, behavioral, integration and audit objects are validated against the release schemas.
    schema_by_name={x['name']: load(rt/x['path']) for x in reg.get('schemas',[]) if (rt/x.get('path','')).is_file()}
    nwp_schema=schema_by_name.get('NativeWritePolicy')
    if nwp_schema:
        p=rt/'jai/core/native-write-policy.json'
        if not p.is_file(): problems.append('native write policy missing')
        else:
            for err in jsonschema.Draft202012Validator(nwp_schema).iter_errors(load(p)): problems.append(f'native write policy: {err.message}')
    wf_schema=schema_by_name.get('Workflow')
    if wf_schema:
        wf_validator=jsonschema.Draft202012Validator(wf_schema)
        for wf in load(rt/'workflows.json').get('workflows',[]):
            for err in wf_validator.iter_errors(wf): problems.append(f"workflow {wf.get('key')}: schema: {err.message}")
    case_schema=schema_by_name.get('EvaluationCase')
    if case_schema:
        v=jsonschema.Draft202012Validator(case_schema)
        for p in sorted((rt/'evals/scenarios').glob('*.json')):
            for err in v.iter_errors(load(p)): problems.append(f"evaluation case {p.name}: {err.message}")
    result_schema=schema_by_name.get('EvaluationResult')
    if result_schema:
        v=jsonschema.Draft202012Validator(result_schema)
        for p in sorted((rt/'evals/reference-results').glob('*.json')):
            for err in v.iter_errors(load(p)): problems.append(f"evaluation result {p.name}: {err.message}")
    adapter_schema=schema_by_name.get('EnterpriseAdapterContract')
    if adapter_schema:
        v=jsonschema.Draft202012Validator(adapter_schema)
        for p in sorted((rt/'integrations/adapters').glob('*.json')):
            for err in v.iter_errors(load(p)): problems.append(f"adapter {p.name}: {err.message}")
    model_schema=schema_by_name.get('ModelRegistry')
    if model_schema:
        v=jsonschema.Draft202012Validator(model_schema)
        for err in v.iter_errors(load(rt/'models/model-registry.json')):
            problems.append(f"model registry: {err.message}")
    service_schema=schema_by_name.get('ServiceLevels')
    if service_schema:
        v=jsonschema.Draft202012Validator(service_schema)
        for err in v.iter_errors(load(rt/'operations/service-levels.json')):
            problems.append(f"service levels: {err.message}")
    release_schema=schema_by_name.get('ReleasePolicy')
    if release_schema:
        v=jsonschema.Draft202012Validator(release_schema)
        for err in v.iter_errors(load(rt/'release/release-policy.json')):
            problems.append(f"release policy: {err.message}")
    # SABSA mapping references must be total over the declarative semantic type registry.
    elements=load(rt/'sabsa/schema/elements.json').get('element_types',{}); mapping=load(rt/'ea/sabsa-mapping.json').get('rules',{})
    if set(elements)!=set(mapping):
        for x in sorted(set(elements)-set(mapping)): problems.append(f'SABSA mapping missing type {x}')
        for x in sorted(set(mapping)-set(elements)): problems.append(f'SABSA mapping unknown type {x}')
    cells={(r.get('sabsa_layer'),r.get('sabsa_question')) for r in mapping.values()}
    if len(cells)!=36: problems.append(f'SABSA mapping covers {len(cells)}/36 cells')
    return problems,rt,reg

def self_test(root: Path):
    problems,rt,reg=check(root)
    if problems:
        print(f'FAILED ({len(problems)} problems)'); [print(' -',x) for x in problems[:100]]; return 1
    print(f"OK: {len(reg['schemas'])} versioned schemas valid; critical schemas closed; taxonomy/contracts/mapping references resolve")
    return 0

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('cmd',choices=['check','self-test']); ap.add_argument('--root',default='.'); a=ap.parse_args(); raise SystemExit(self_test(Path(a.root)))
if __name__=='__main__': main()
