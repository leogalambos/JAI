#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Generate release inventory/documentation from canonical package sources."""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path

START='<!-- GENERATED-INVENTORY:START -->'
END='<!-- GENERATED-INVENTORY:END -->'

def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def root_from(root: Path):
    root=root.resolve()
    # Source bundle: canonical surface is <bundle>/.ai and runtime is <bundle>/.ai/runtime.
    if (root/'.ai/runtime/roles.json').is_file():
        return root, root/'.ai/runtime', root/'.ai'
    # A HOME-like root passed by the structural policy checker.
    installed=root/'.ai/it-role-house'
    if (installed/'roles.json').is_file() and (installed/'schema/schema-registry.json').is_file():
        return installed, installed, installed
    # Installed/common runtime: agents, skills, roles and schemas live together under
    # ~/.ai/it-role-house. Keep this path first-class so generated-doc drift can be
    # verified after installation as well as in the source tree.
    if (root/'roles.json').is_file() and (root/'schema/schema-registry.json').is_file():
        return root, root, root
    raise SystemExit('package/runtime root not found')

def inventory(root: Path):
    package,rt,surface=root_from(root)
    roles=load(rt/'roles.json'); workflows=load(rt/'workflows.json'); taxonomy=load(rt/'artifacts/schema/artifact-types.json'); schemas=load(rt/'schema/schema-registry.json')
    agents=sorted(p.stem for p in (surface/'agents').glob('*.md'))
    skills=sorted(p.parent.name for p in (surface/'skills').glob('*/SKILL.md'))
    adapter_dir=surface/'adapters'
    if adapter_dir.is_dir():
        adapters=sorted(p.name for p in adapter_dir.iterdir() if p.is_dir())
    elif (rt/'install-state.json').is_file():
        adapters=sorted(load(rt/'install-state.json').get('providers',[]))
    elif (rt/'_meta/release-manifest.json').is_file():
        adapters=sorted(load(rt/'_meta/release-manifest.json').get('provider_adapters',[]))
    else:
        adapters=[]
    renderers=sorted({str(v.get('renderer')) for v in taxonomy.get('artifact_types',{}).values() if v.get('renderer')})
    tests=[]
    self_tests=('fabric/fabric.py','tools/publication.py','tools/projection.py','tools/publication_integrity.py','tools/visual_qa.py','tools/agent_runtime.py','tools/repository.py','tools/sabsa_ea.py','tools/ea_conformance.py','tools/schema_check.py','tools/behavioral_eval.py','tools/integration_adapters.py','tools/execution_record.py','tools/supply_chain.py','tools/model_router.py','tools/service_levels.py','tools/release_policy.py')
    for name in self_tests:
        if (rt/name).is_file(): tests.append(name+' self-test')
    if (rt/'tools/provider_parity.py').is_file(): tests.append('tools/provider_parity.py')
    tests += ['tools/docs_contract.py --root .','tools/schema_resolver.py self-test','tools/architecture_claim_lint.py','tools/native_enforcement_26103.py','tools/artifacts.py check','tools/artifacts.py golden-test','tools/license_check.py','tools/human_text_width.py --root .','tools/performance_budget.py --profile fast','tools/qualification_regression.py regression','tools/qualification_core.py A-G qualification','tools/release_ga.py qualify','tools/release_bundle.py build','tools/generate_docs.py --check']
    version=(package/'VERSION').read_text().strip()
    return {
      'manifest_version':'1.0.0','release':version,
      'counts':{'roles':len(roles.get('roles',[])),'agents':len(agents),'skills':len(skills),'workflows':len(workflows.get('workflows',[])),'artifact_types':len(taxonomy.get('artifact_types',{})),'schemas':len(schemas.get('schemas',[])),'renderers':len(renderers),'tests':len(tests),'provider_adapters':len(adapters)},
      'roles_source':'runtime/roles.json','workflows_source':'runtime/workflows.json','artifact_taxonomy_source':'runtime/artifacts/schema/artifact-types.json','schema_registry_source':'runtime/schema/schema-registry.json',
      'agents':agents,'skills':skills,'provider_adapters':adapters,'renderers':renderers,'tests':tests,
      'compatibility':[
        {'component':'Claude Code','minimum':'provider-supported','tested':'adapter contract','supported':'yes'},
        {'component':'Codex CLI','minimum':'provider-supported','tested':'adapter contract','supported':'yes'},
        {'component':'Python','minimum':'3.10','tested':'3.12 release CI target','supported':'yes'},
        {'component':'Pandoc','minimum':'optional','tested':'publication tool detects at runtime','supported':'optional'},
        {'component':'LibreOffice','minimum':'optional','tested':'publication tool detects at runtime','supported':'publication'},
        {'component':'lxml','minimum':'5.x','tested':'XSD conformance suite','supported':'EA conformance'},
        {'component':'jsonschema','minimum':'4.x','tested':'Draft 2020-12','supported':'semantic schemas'},
        {'component':'Pillow','minimum':'runtime-supported','tested':'visual QA fixture rendering','supported':'visual QA'},
        {'component':'GitHub Actions','minimum':'release workflow','tested':'tag, A-H gates, ZIP SHA-256, CI publication','supported':'automatic release publication'}
      ]
    }

def md_block(inv):
    c=inv['counts']
    count_lines='\n'.join(
        f"- {k.replace('_',' ').title()}: **{v}**"
        for k,v in c.items()
    )
    compat_lines=[]
    for item in inv['compatibility']:
        compat_lines.extend([
            f"- **{item['component']}**",
            f"  - Minimum: {item['minimum']}",
            f"  - Tested: {item['tested']}",
            f"  - Supported: {item['supported']}",
        ])
    compat='\n'.join(compat_lines)
    return f"""{START}
## Current generated release inventory

This block is generated from canonical package sources by
`.ai/runtime/tools/generate_docs.py`. Manual count edits are not
authoritative.

{count_lines}

### Compatibility matrix

{compat}
{END}"""

def replace_block(text,block):
    if START in text and END in text:
        return text[:text.index(START)] + block + text[text.index(END)+len(END):]
    # Place after first top-level heading/lede area.
    lines=text.splitlines(); at=1
    for i,line in enumerate(lines[1:],1):
        if line.startswith('## '): at=i; break
    return '\n'.join(lines[:at]).rstrip()+'\n\n'+block+'\n\n'+'\n'.join(lines[at:]).lstrip()

def validation_doc(inv):
    release=inv['release']
    return f"""# Validation — AI IT House {release}

## Production boundary

{release} uses the six-layer Justifiable AI core as its single normative
architecture. Artifact Contract v3 is the native production write model.
Artifact Contract v2 is read/migration-only and is hash-frozen by the
Native Write Policy.

## Enterprise qualification

```sh
python3 .ai/runtime/tools/release_ga.py qualify
```

The independent release gates are:

- **A — Structural:** Native JAI enforcement, schemas, v3 artifact
  contracts, generated documentation and policy.
- **B — Semantic:** SABSA, scoped EA projection, ArchiMate
  interoperability and repository consistency.
- **C — Governance:** authorities/workflows, v3 governance contracts,
  immutable execution records and service objectives.
- **D — Runtime Security:** authority enforcement, model routing,
  provider parity, adapter mutation controls and regression tests.
- **E — Publication:** JAI-lineaged ProjectionManifest v3, enterprise
  renderers and publication integrity.
- **F — Visual:** render-based visual QA.
- **G — Behavioral:** enterprise scenarios, deterministic thresholds,
  adversarial checks and a hard fixture/live-evidence boundary. The
  universal package does not claim qualification of a mutable external
  provider/model; live qualification requires captured results plus a
  typed evidence manifest.
- **H — Supply Chain:** licence policy, SPDX SBOM, digest provenance,
  distribution archive checksums and automated GitHub release policy.

`QUALIFICATION-A-H.json` is the authoritative qualification result.

## Automated production release

```sh
# Change VERSION and synchronize product metadata before committing the tag.
# Only VERSION is edited manually; no global string replacement.
python3 scripts/versioning.py sync
# Commit the result, push main, then publish this exact source version.
git tag -a 'release@{release}' -m 'JAI {release}'
git push origin 'release@{release}'
```

The root `VERSION` is the authoritative product version.
The synchronization script updates installation mirrors, current
catalog metadata and generated documentation. GitHub Actions rejects
tags that disagree with the committed `VERSION` and never changes
its source identity. Independent JAI/schema contract versions and
historical migrations remain unchanged. After A-H
qualification it generates a production distribution ZIP and `.sha256`
checksum and publishes GitHub Release `YY.MM.VV` automatically. GitHub
OIDC attestations protect eligible builds; a private GitHub Free/Pro
repository may publish using digest provenance only.

## Compatibility

- 26.10.0 Artifact Contract v2: read/migrate only.
- 26.10.1 JAI/v3: read/migrate only.
- 26.10.2 JAI/v3: read/migrate only.
- 26.10.3 JAI/v3: read/migrate only.
- Native writes: `ArtifactContract-v3` (independent of product release).

Verified carry-over reviews are recorded in:

- `.ai/runtime/_meta/26.10.1-carryover-audit.json`
- `.ai/runtime/_meta/26.10.2-carryover-audit.json`
- `.ai/runtime/_meta/26.10.3-carryover-audit.json`
"""

def outputs(root: Path):
    package,rt,_surface=root_from(root); inv=inventory(root); manifest=json.dumps(inv,indent=2,ensure_ascii=False)+'\n'; block=md_block(inv)
    readmes={package/'README.md',rt/'README.md'}
    readme_text={p:replace_block(p.read_text(encoding='utf-8'),block) for p in readmes if p.is_file()}
    return package,rt,inv,manifest,readme_text,validation_doc(inv)

def run(root: Path,check=False):
    package,rt,inv,manifest,readmes,validation=outputs(root); mismatches=[]
    targets={rt/'_meta/release-manifest.json':manifest,package/'VALIDATION.md':validation,**readmes}
    # The CLI-facing GUIDE.md is a generated Markdown deployment projection.
    # Its only maintained source is the canonical main-documentation page.
    guide_source=package/'docs/reference/installed-cli-guide.md'
    if guide_source.is_file():
        targets[rt/'GUIDE.md']=guide_source.read_text(encoding='utf-8')
    if check:
        for p,content in targets.items():
            if not p.is_file() or p.read_text(encoding='utf-8')!=content: mismatches.append(str(p))
        if mismatches:
            print('FAILED generated documentation drift:'); [print(' -',x) for x in mismatches]; return 1
        print(f"OK: generated docs match canonical manifest ({inv['counts']['roles']} roles, {inv['counts']['artifact_types']} artifact types, {inv['counts']['schemas']} schemas)"); return 0
    for p,content in targets.items(): p.parent.mkdir(parents=True,exist_ok=True); p.write_text(content,encoding='utf-8')
    print(f"wrote generated manifest/docs for {inv['release']}: {inv['counts']}"); return 0

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--root',default='.'); ap.add_argument('--check',action='store_true'); a=ap.parse_args(); raise SystemExit(run(Path(a.root),a.check))
if __name__=='__main__': main()
