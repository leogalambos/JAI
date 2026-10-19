#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Authoritative Artifact Contract v3 registry for AI IT House.

Production behavior is deliberately non-inferential. Section 6 role deliverables are parsed only to
verify identity/source drift. New writes and generated registries use the JAI-bound v3 contract source;
v2 is an immutable compatibility/migration fixture only.

Commands:
  artifacts.py sync [--root PATH]                 generate compatibility registry from authoritative v3 contracts
  artifacts.py check [--root PATH]                enforce Artifact Contract v3 and native-write integrity
  artifacts.py golden-test [--root PATH]          verify release classification corpus
  artifacts.py show ROLE-SLUG [--root PATH]
  artifacts.py check-handoff CONTRACT-ID [--root PATH]
  artifacts.py propose-migration [--root PATH] [--out FILE]

`propose-migration` is the only command allowed to use keyword inference. Its output is marked proposal-only
and cannot pass `check` until a human/release process turns it into explicit authoritative contracts.
"""
from __future__ import annotations
import argparse, hashlib, json, re, sys
from pathlib import Path

try:
    import jsonschema
except Exception:  # optional at runtime; CI/release environment includes it
    jsonschema = None

ROW = re.compile(r"^\|\s*(\d+)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*$")
INPUT_ROW = ROW
GATE = re.compile(r"^\s*-\s*\[[ xX]\]\s*\*\*(G\d+)\.\*\*\s*(.+?)\s*$")


def locate(root: Path):
    root=root.resolve()
    candidates=[
        (root/'.ai/runtime/roles.json', root/'.ai/skills', root/'.ai/runtime/artifacts', root/'.ai/runtime'),
        (root/'it-role-library/roles.json', root/'skills', root/'it-role-library/artifacts', root/'it-role-library'),
        (root/'.ai/it-role-house/roles.json', root/'.ai/it-role-house/skills', root/'.ai/it-role-house/artifacts', root/'.ai/it-role-house'),
        (root/'roles.json', root/'skills', root/'artifacts', root),
    ]
    for roles, skills, artifacts, runtime in candidates:
        if roles.is_file(): return roles, skills, artifacts, runtime
    raise SystemExit(f"error: cannot find roles.json below {root}")


def sections(text: str):
    out={}; current=None
    for line in text.splitlines():
        m=re.match(r"^##\s+(\d+)\.\s+(.*)$",line)
        if m: current=int(m.group(1)); out[current]=[]
        elif current is not None: out[current].append(line)
    return out


def clean(s): return re.sub(r"\s+"," ",s.replace('**','').replace('`','')).strip()


def parse_role(path: Path):
    sec=sections(path.read_text(encoding='utf-8')); inputs=[]; gates=[]; deliverables=[]
    for line in sec.get(3,[]):
        m=INPUT_ROW.match(line)
        if m and not set(m.group(2).strip()) <= {'-'} and m.group(2).strip().lower()!='input': inputs.append(clean(m.group(2)))
    for line in sec.get(7,[]):
        m=GATE.match(line)
        if m: gates.append({'id':m.group(1),'criterion':clean(m.group(2))})
    for line in sec.get(6,[]):
        m=ROW.match(line)
        if not m or m.group(2).strip().lower()=='artefact' or set(m.group(2).strip()) <= {'-'}: continue
        deliverables.append({'number':int(m.group(1)),'name':clean(m.group(2)),'format':clean(m.group(3)),'acceptance_criterion':clean(m.group(4))})
    return inputs,gates,deliverables


def fingerprint(d: dict) -> str:
    payload={'deliverable':d['name'],'format':d['format'],'acceptance':d['acceptance_criterion']}
    return hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()


def paths(root: Path):
    roles, skills, artifacts, runtime=locate(root)
    return {
        'roles':roles,'skills':skills,'artifacts':artifacts,'runtime':runtime,
        'taxonomy':artifacts/'schema/artifact-types.json',
        'contract_schema':runtime/'schema/contracts/artifact-v3.schema.json',
        'source':artifacts/'contracts/role-deliverables.v3.json',
        'legacy':artifacts/'contracts/role-deliverables.v2.json',
        'golden':artifacts/'contracts/golden-classification.json',
        'profiles':artifacts/'profiles/acceptance-evidence.json',
        'generated':artifacts/'role-deliverables.json',
    }


def load_all(root: Path):
    p=paths(root)
    for key in ('taxonomy','contract_schema','source','golden','profiles'):
        if not p[key].is_file(): raise SystemExit(f"error: missing {p[key]}")
    taxonomy=json.loads(p['taxonomy'].read_text(encoding='utf-8'))
    schema=json.loads(p['contract_schema'].read_text(encoding='utf-8'))
    source=json.loads(p['source'].read_text(encoding='utf-8'))
    profiles=json.loads(p['profiles'].read_text(encoding='utf-8'))
    roles=json.loads(p['roles'].read_text(encoding='utf-8'))['roles']
    return p,taxonomy,schema,source,profiles,roles


def live_deliverables(p, roles):
    out={}
    for role in roles:
        rel=Path(role['path'])
        rp=(p['skills']/Path(*rel.parts[1:])) if rel.parts and rel.parts[0]=='skills' else p['skills']/rel
        if not rp.is_file(): raise SystemExit(f"error: role reference missing: {rp}")
        inputs,gates,ds=parse_role(rp)
        downstream=[x.get('name') for x in role.get('links',{}).get('downstream',[]) if x.get('name')]
        for d in ds:
            cid=f"{role['slug']}:{d['number']}"
            out[cid]={'role':role,'inputs':inputs,'gates':gates,'downstream':downstream,'deliverable':d,'fingerprint':fingerprint(d)}
    return out


def runtime_path_exists(runtime: Path, ref: str) -> bool:
    if not ref or ref=='external' or ref.startswith('external:'): return False
    token=ref.split()[0]
    return (runtime/token).exists()


def flatten_v3(c: dict) -> dict:
    if c.get("version") != "3.0.0" or "jai" not in c: return c
    j=c["jai"]; i=j["intent"]; m=j["semantics"]; q=j["justification"]; d=j["design"]; r=j["realisation"]; e=j["evidence"]
    return {**c, "owner_role":i["owner_role"], "artifact_type":m["artifact_type"], "purpose":i["purpose"], "audience":i["audience"], "decision_supported":i["decision_supported"], "schema_ref":m["schema_ref"], "required_inputs":m["required_inputs"], "required_evidence":q["required_evidence"], "required_relations":m["required_relations"], "mandatory_sections":d["mandatory_sections"], "producer":r["producer"], "reviewers":q["reviewers"], "approver":q["approver"], "renderer":r["renderer"], "output_formats":r["output_formats"], "publication_profile":d["publication_profile"], "acceptance_profile":q["acceptance_profile"], "evidence_profile":q["evidence_profile"], "system_of_record":r["system_of_record"], "external_handoff_adapter":r["external_handoff_adapter"], "classification":i["classification"], "production_mode":r["production_mode"], "semantic_gate":q["semantic_policy"], "repository_gate":q["repository_policy"], "publication_gate":e["publication_gate"], "portfolio_traceability":e["portfolio_traceability"], "classification_source":c["compatibility"]["classification_source"], "retention":c["lifecycle"].get("retention")}


def _record_hash(record: dict) -> str:
    return hashlib.sha256(json.dumps(record, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()).hexdigest()


def _origin_problems(raw: dict, legacy_by: dict, live: dict | None, runtime: Path) -> list[str]:
    """Validate origin without treating authored provenance as approval or signature."""
    cid = raw.get('id')
    problems = []
    migration = raw.get('migration')
    native = raw.get('native_creation')
    compatibility = raw.get('compatibility', {})
    old = legacy_by.get(cid)
    if (migration is None) == (native is None):
        return [f'{cid}: exactly one migration or native_creation origin required']
    if migration is not None and not isinstance(migration, dict) or native is not None and not isinstance(native, dict):
        return [f'{cid}: origin must be an object']
    if old is not None:
        if native is not None:
            return [f'{cid}: legacy contract cannot be relabelled as native creation']
        if migration.get('source_id') != cid or migration.get('source_hash') != _record_hash(old):
            problems.append(f'{cid}: migration provenance/hash mismatch')
        if compatibility.get('migration') != 'forward-only':
            problems.append(f'{cid}: legacy migration must remain forward-only')
        if not str(compatibility.get('classification_source', '')).startswith('explicit-ga-'):
            problems.append(f'{cid}: legacy classification must preserve its GA provenance')
    elif migration is not None:
        problems.append(f'{cid}: legacy migration source missing')
    else:
        if compatibility.get('migration') != 'native-creation-no-legacy-source':
            problems.append(f'{cid}: native origin must declare no legacy source')
        if not str(compatibility.get('classification_source', '')).startswith('explicit-native-'):
            problems.append(f'{cid}: native classification must declare native provenance')
        if live is None or native.get('source_path') != live['role']['path']:
            problems.append(f'{cid}: native origin role source mismatch')
        if native.get('source_kind') != 'reviewed-role-definition':
            problems.append(f'{cid}: unsupported native source kind')
        ref = native.get('evidence_ref', '')
        if not re.fullmatch(r'artifacts/contracts/[a-z0-9-]+\.native-v3\.json', ref):
            return problems + [f'{cid}: invalid native provenance reference']
        path = runtime / ref
        if not path.resolve().is_relative_to(runtime.resolve()):
            return problems + [f'{cid}: native provenance reference escapes runtime']
        try:
            payload = path.read_bytes()
            evidence = json.loads(payload)
        except (OSError, ValueError):
            return problems + [f'{cid}: native provenance evidence missing or invalid']
        if not isinstance(evidence, dict) or not isinstance(evidence.get('contracts'), list) or any(not isinstance(entry, dict) for entry in evidence['contracts']):
            return problems + [f'{cid}: native provenance evidence must contain contract objects']
        if hashlib.sha256(payload).hexdigest() != native.get('evidence_hash'):
            problems.append(f'{cid}: native provenance evidence hash mismatch')
        entries = evidence.get('contracts', [])
        ids = [entry.get('id') for entry in entries]
        if len(ids) != len(set(ids)):
            problems.append(f'{cid}: duplicate native provenance ids')
        matching = [entry for entry in entries if entry.get('id') == cid]
        record = {key: value for key, value in raw.items() if key != 'native_creation'}
        if evidence.get('origin') != 'native-v3-authored' or len(matching) != 1 or matching[0].get('contract_hash') != _record_hash(record):
            problems.append(f'{cid}: native provenance contract binding mismatch')
    if cid != f"{raw.get('role_slug')}:{raw.get('deliverable_number')}":
        problems.append(f'{cid}: contract identity differs from role/deliverable identity')
    return problems

def content_profile_problems(runtime: Path) -> list[str]:
    """Validate an optional DCS sidecar without rewriting historical contracts.

    Args:
        runtime: Canonical runtime directory in a source or installed library.

    Returns:
        Structural DCS errors, or an empty list for compatible unprofiled trees.
        Packaged profiles fail closed if the resolver or referenced data is absent.
    """
    profile = runtime / 'jai/profiles/content-profile.json'
    if not profile.exists():
        return []
    try:
        settings = json.loads(profile.read_text(encoding='utf-8'))
        expected_refs = {
            'registry_ref': 'content/registry.json',
            'binding_map_ref': 'content/migrations/26.10.5-binding-map.json',
            'resolver': 'tools/content_spec.py',
        }
        if not isinstance(settings, dict) or any(settings.get(key) != value for key, value in expected_refs.items()):
            return ['DCS: content profile must reference the canonical registry, bindings and resolver']
        import importlib.util
        spec = importlib.util.spec_from_file_location('jai_content_spec', runtime / 'tools/content_spec.py')
        if spec is None or spec.loader is None:
            return ['DCS: content resolver is unavailable']
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        return ['DCS: ' + problem for problem in module.lint_registry(runtime)]
    except (OSError, ValueError, ImportError, AttributeError, TypeError, KeyError) as exc:
        return [f'DCS: packaged content profile cannot be validated: {exc}']


def validate(root: Path):
    """Return validation problems and loaded state; read all registered role sources.

    Args:
        root: Repository or installed library root containing the canonical registry.

    Returns:
        A pair of problem strings and state used to construct the compatibility view.
        When a DCS sidecar profile is packaged, problems include its structural
        reference and policy-conflict checks. Older unprofiled installations remain readable.

    Raises:
        SystemExit: Required canonical files or role references are missing.
    """
    p,taxonomy,schema,source,profiles,roles=load_all(root); problems=[]
    if taxonomy.get('policy',{}).get('production_inference_forbidden') is not True:
        problems.append('taxonomy policy must forbid production inference')
    types=taxonomy.get('artifact_types',{}); acc=profiles.get('acceptance_profiles',{}); evp=profiles.get('evidence_profiles',{})
    live=live_deliverables(p,roles); rows=source.get('contracts',[]); actual={r.get('id'):flatten_v3(r) for r in rows if r.get('id')}
    if len(actual)!=len(rows): problems.append('duplicate or empty contract ids in authoritative source')
    if set(actual)!=set(live):
        for x in sorted(set(live)-set(actual)): problems.append(f'missing authoritative contract {x}')
        for x in sorted(set(actual)-set(live)): problems.append(f'stale authoritative contract {x}')
    if source.get('deliverable_count')!=len(rows): problems.append('authoritative deliverable_count drift')
    if source.get('role_count')!=len({x['role']['slug'] for x in live.values()}): problems.append('authoritative role_count drift')
    # source['release'] is the baseline in which the contract catalogue was authored,
    # not the release of every later package consuming the same contract version.
    if source.get('authoritative_write_model') is not True or source.get('native_write_enforced') is not True:
        problems.append('authoritative v3 source must declare native write enforcement')
    legacy=json.loads(p['legacy'].read_text(encoding='utf-8')); legacy_by={x['id']:x for x in legacy.get('contracts',[])}
    for cid,c in actual.items():
        if jsonschema:
            try: jsonschema.Draft202012Validator(schema).validate(next(x for x in rows if x.get('id')==cid))
            except Exception as exc: problems.append(f'{cid}: contract schema: {exc.message if hasattr(exc,"message") else exc}')
        if not re.fullmatch(r'explicit-(?:ga|native)-[0-9]{2}\.(0[1-9]|1[0-2])\.[0-9]+', str(c.get('classification_source',''))): problems.append(f'{cid}: non-explicit classification source')
        raw=next(x for x in rows if x.get('id')==cid)
        if raw.get('compatibility',{}).get('writes')!='ArtifactContract-v3': problems.append(f'{cid}: non-native write target')
        problems.extend(_origin_problems(raw, legacy_by, live.get(cid), p['runtime']))
        if not c.get('retention'): problems.append(f'{cid}: retention obligation lost in v3 lifecycle')
        ld=live.get(cid)
        if ld and c.get('source_fingerprint')!=ld['fingerprint']: problems.append(f'{cid}: role Section 6 drift; explicit contract review required')
        at=c.get('artifact_type'); spec=types.get(at)
        if not spec: problems.append(f'{cid}: unknown artifact_type {at}'); continue
        for fld in ('schema_ref','producer','renderer','production_mode','acceptance_profile','evidence_profile'):
            if c.get(fld)!=spec.get(fld): problems.append(f'{cid}: {fld} differs from taxonomy for {at}')
        if c.get('acceptance_profile') not in acc: problems.append(f'{cid}: missing acceptance profile definition')
        if c.get('evidence_profile') not in evp: problems.append(f'{cid}: missing evidence profile definition')
        if spec.get('production_mode')=='internal':
            if c.get('external_handoff_adapter') is not None: problems.append(f'{cid}: internal deliverable declares external handoff adapter')
            for fld in ('schema_ref','producer','validator','renderer'):
                ref=spec.get(fld)
                if not ref or str(ref).startswith('external'): problems.append(f'{cid}: internal {at} lacks internal {fld}')
                elif fld in ('schema_ref','producer','renderer') and not runtime_path_exists(p['runtime'],ref): problems.append(f'{cid}: {fld} path not found: {ref}')
        elif spec.get('production_mode')=='external_handoff':
            if not c.get('external_handoff_adapter'): problems.append(f'{cid}: external deliverable lacks handoff adapter')
        else: problems.append(f'{cid}: invalid production_mode {spec.get("production_mode")}')
    # Golden corpus is release-blocking and tests historically problematic/decision-significant mappings.
    golden=json.loads(p['golden'].read_text(encoding='utf-8'))
    for case in golden.get('cases',[]):
        c=actual.get(case.get('id'))
        if not c: problems.append(f"golden case missing contract {case.get('id')}")
        elif c.get('artifact_type')!=case.get('expected_artifact_type'): problems.append(f"golden {case['id']}: {c.get('artifact_type')} != {case.get('expected_artifact_type')}")
    problems.extend(content_profile_problems(p['runtime']))
    return problems, (p,taxonomy,source,live)


def generated_registry(root: Path):
    problems,state=validate(root)
    if problems: return None,problems
    p,taxonomy,source,live=state; types=taxonomy['artifact_types']; rows=[]
    for raw in source['contracts']:
        c=flatten_v3(raw); ld=live[c['id']]; d=ld['deliverable']; role=ld['role']; spec=types[c['artifact_type']]
        row=dict(c)
        row.update({
          'role':role['name'],'skill':role['skill'],'deliverable':d['name'],'declared_format':d['format'],'acceptance_criterion':d['acceptance_criterion'],
          'schema':c['schema_ref'],'template':'publication/templates/publication-model.example.json' if spec['production_mode']=='internal' and c['artifact_type']!='model' else ('ea/templates/repository.example.json' if c['artifact_type']=='model' else 'external'),
          'validator':spec['validator'],'render_targets':spec.get('render_targets',[]),'owner':c['owner_role'],'review_cycle':c['lifecycle']['review_cycle'],
          'acceptance_gates':[g['id']+': '+g['criterion'] for g in ld['gates']],
        })
        rows.append(row)
    return {'schema_version':'3.0.0','source':'contracts/role-deliverables.v3.json','role_count':source['role_count'],'deliverable_count':source['deliverable_count'],'contracts':rows},[]


def cmd_sync(args):
    reg,problems=generated_registry(Path(args.root))
    if problems:
        print(f'FAILED ({len(problems)} problems)'); [print(' -',x) for x in problems[:100]]; return 1
    p=paths(Path(args.root)); p['generated'].write_text(json.dumps(reg,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(f"wrote {p['generated']}: {reg['deliverable_count']} explicit contracts across {reg['role_count']} roles")
    return 0


def cmd_check(args):
    problems,state=validate(Path(args.root))
    if problems:
        print(f'FAILED ({len(problems)} problems)'); [print(' -',x) for x in problems[:100]]; return 1
    _,taxonomy,source,_=state
    internal=sum(taxonomy['artifact_types'][flatten_v3(x)['artifact_type']]['production_mode']=='internal' for x in source['contracts'])
    external=len(source['contracts'])-internal
    print(f"OK: {len(source['contracts'])} authoritative Artifact Contract v3 records; 0 runtime-inferred types; {internal} internal, {external} external_handoff")
    return 0


def cmd_golden(args):
    problems,state=validate(Path(args.root)); p=paths(Path(args.root))
    golden=json.loads(p['golden'].read_text(encoding='utf-8')); source=json.loads(p['source'].read_text(encoding='utf-8')); by={x['id']:flatten_v3(x) for x in source['contracts']}
    failed=[]
    for case in golden.get('cases',[]):
        got=by.get(case['id'],{}).get('artifact_type')
        if got!=case['expected_artifact_type']: failed.append(f"{case['id']}: {got} != {case['expected_artifact_type']}")
    failed += [x for x in problems if x.startswith('golden ')]
    if failed: print('FAILED'); [print(' -',x) for x in failed]; return 1
    print(f"OK: {len(golden.get('cases',[]))}/{len(golden.get('cases',[]))} golden classifications match explicit contracts")
    return 0


def cmd_show(args):
    p=paths(Path(args.root)); src=json.loads(p['source'].read_text(encoding='utf-8'))
    rows=[flatten_v3(x) for x in src['contracts'] if x['role_slug']==args.role]
    if not rows: raise SystemExit(f'no contracts for {args.role}')
    print(json.dumps(rows,indent=2,ensure_ascii=False)); return 0


def cmd_handoff(args):
    p=paths(Path(args.root)); src=json.loads(p['source'].read_text(encoding='utf-8')); rows={x['id']:flatten_v3(x) for x in src['contracts']}; c=rows.get(args.contract_id)
    if not c: print('FAIL unknown contract'); return 1
    if c.get('production_mode')!='external_handoff': print('FAIL contract is not external_handoff'); return 1
    if not c.get('external_handoff_adapter'): print('FAIL handoff adapter missing'); return 1
    print('PASS',c['contract_id'] if 'contract_id' in c else c['id'],c['external_handoff_adapter']); return 0

# Proposal-only classifier retained solely for migration assistance. Production code never calls this.
def propose_type(name: str, fmt: str) -> str:
    x=(name+' '+fmt).lower()
    if 'benefits review' in x or 'post-implementation benefits review' in x: return 'benefits-review'
    if 'operational readiness' in x: return 'operational-readiness-assessment'
    if 'cutover' in x: return 'cutover-plan'
    if 'business case' in x: return 'business-case'
    if 'architecture decision' in x or re.search(r'\badr(s)?\b',x): return 'architecture-decision'
    if 'ea tool' in x or 'archimate' in x: return 'model'
    if 'diagram' in x: return 'diagram'
    if 'prototype' in x: return 'prototype'
    if 'roadmap' in x or ' plan' in x: return 'roadmap'
    if 'register' in x or ' log' in x: return 'register'
    if 'assessment' in x or 'report' in x or 'review' in x: return 'decision-paper'
    if 'design' in x or 'specification' in x or 'requirements' in x: return 'implementation-specification'
    return 'document'


def cmd_propose(args):
    p,taxonomy,schema,source,profiles,roles=load_all(Path(args.root)); live=live_deliverables(p,roles); rows=[]
    for cid,ld in sorted(live.items()):
        d=ld['deliverable']; rows.append({'id':cid,'proposed_artifact_type':propose_type(d['name'],d['format']),'classification_source':'migration-proposal-inferred','source_fingerprint':ld['fingerprint']})
    out=Path(args.out) if args.out else p['artifacts']/'contracts/migration-proposal.json'; out.write_text(json.dumps({'proposal_only':True,'contracts':rows},indent=2)+'\n',encoding='utf-8')
    print(f'wrote proposal-only migration file {out}; it is not accepted by production validation'); return 0


def main():
    ap=argparse.ArgumentParser(); sp=ap.add_subparsers(dest='cmd',required=True)
    for name,fn in [('sync',cmd_sync),('check',cmd_check),('golden-test',cmd_golden)]:
        p=sp.add_parser(name); p.add_argument('--root',default='.'); p.set_defaults(fn=fn)
    p=sp.add_parser('show'); p.add_argument('role'); p.add_argument('--root',default='.'); p.set_defaults(fn=cmd_show)
    p=sp.add_parser('check-handoff'); p.add_argument('contract_id'); p.add_argument('--root',default='.'); p.set_defaults(fn=cmd_handoff)
    p=sp.add_parser('propose-migration'); p.add_argument('--root',default='.'); p.add_argument('--out'); p.set_defaults(fn=cmd_propose)
    a=ap.parse_args(); raise SystemExit(a.fn(a) or 0)
if __name__=='__main__': main()
