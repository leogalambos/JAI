#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Generate release inventory/documentation from canonical package sources."""
from __future__ import annotations
import argparse, json, re, sys, textwrap
from schema_resolver import release_scope
from pathlib import Path

START='<!-- GENERATED-INVENTORY:START -->'
END='<!-- GENERATED-INVENTORY:END -->'

def load(p):
    """Read canonical JSON; malformed or missing input raises without fallback."""
    return json.loads(Path(p).read_text(encoding='utf-8'))
def root_from(root: Path):
    """Resolve a source or installed runtime; reject unknown layouts."""
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
    """Derive the canonical release inventory and compatibility claims.

    Args:
        root: Source package or installed runtime root accepted by root_from.
    Returns:
        Fresh manifest mapping, including CLI-first WeasyPrint compatibility and
        informational Pyphen metadata; generated projections must use these claims.
    Raises:
        OSError, ValueError: Required resources are missing or malformed.
        SystemExit: The root does not identify a supported package/runtime layout.
    """
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
      'release_scope':release_scope(package),
      'counts':{'roles':len(roles.get('roles',[])),'agents':len(agents),'skills':len(skills),'workflows':len(workflows.get('workflows',[])),'artifact_types':len(taxonomy.get('artifact_types',{})),'schemas':len(schemas.get('schemas',[])),'renderers':len(renderers),'tests':len(tests),'provider_adapters':len(adapters)},
      'roles_source':'runtime/roles.json','workflows_source':'runtime/workflows.json','artifact_taxonomy_source':'runtime/artifacts/schema/artifact-types.json','schema_registry_source':'runtime/schema/schema-registry.json',
      'agents':agents,'skills':skills,'provider_adapters':adapters,'renderers':renderers,'tests':tests,
      'compatibility':[
        {'component':'Claude Code','minimum':'provider-supported strict sandbox','tested':'not installed on reference host; projections only, live NOT_VERIFIED','supported':'contract-scoped tools; reviewer shell unavailable without read-only isolation'},
        {'component':'Codex CLI','minimum':'provider-supported','tested':'0.164.0 host CLI help confirms sandbox/on-request values; live role confinement NOT_VERIFIED','supported':'role-authorized local QA in effective native sandbox'},
        {'component':'Python','minimum':'3.10','tested':'3.12 release CI target','supported':'yes'},
        {'component':'Pandoc','minimum':'optional','tested':'publication tool detects at runtime','supported':'optional'},
        {'component':'WeasyPrint','minimum':'70.x optional','tested':'actual HTML/PDF conversion; constrained resource fetching; uniform CLI-first/current-Python fallback covered by real CLI subprocess tests','supported':'SUPPORTED optional HTML/PDF; not Office fidelity'},
        {'component':'Pyphen','minimum':'determined by the installed WeasyPrint dependency requirements','tested':'metadata reported; actual HTML/PDF conversion determines readiness','supported':'WeasyPrint transitive dependency; optional pip recipe selects 0.17.x in requirements-rendering.txt, without rejecting working OS packages'},
        {'component':'LibreOffice','minimum':'Office-compatible host renderer','tested':'actual DOCX/PPTX/XLSX operator renders on Fedora','supported':'AUTO when native sandbox permits; otherwise OPERATOR_ASSISTED actual Office QA'},
        {'component':'Poppler','minimum':'pdftoppm on PATH','tested':'actual PDF page rasterization','supported':'visual QA raster prerequisite'},
        {'component':'OpenSSL','minimum':'Ed25519 pkeyutl -rawin','tested':'external receipts verified with fixed /usr/bin/openssl on Linux','supported':'OPERATOR_ASSISTED local L0; other trust adapters NOT_VERIFIED'},
        {'component':'Fonts/system libraries','minimum':'DejaVu Sans; renderer-native text/layout libraries','tested':'Fedora reference glyph/layout corpus','supported':'host prerequisite; other platforms NOT_VERIFIED'},
        {'component':'lxml','minimum':'5.x','tested':'XSD conformance suite','supported':'EA conformance'},
        {'component':'jsonschema','minimum':'4.x','tested':'Draft 2020-12','supported':'semantic schemas'},
        {'component':'Pillow','minimum':'runtime-supported','tested':'visual QA fixture rendering','supported':'visual QA'},
        {'component':'GitHub Actions','minimum':'release workflow','tested':'tag, A-H gates, ZIP SHA-256, CI publication','supported':'automatic release publication'}
      ]
    }

def md_block(inv):
    """Render the canonical inventory as a bounded generated Markdown block."""
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
    features=textwrap.fill('Enabled features: '+', '.join('`'+name+'`' for name in inv['release_scope']['enabled'])+'.',width=70,break_long_words=False,break_on_hyphens=False)
    compat='\n'.join(textwrap.fill(line,width=72,subsequent_indent='    ',break_long_words=False,break_on_hyphens=False) for line in compat_lines)
    return f"""{START}
## Current generated release inventory

This block is generated from canonical package sources by
`.ai/runtime/tools/generate_docs.py`. Manual count edits are not
authoritative.

Supported scope: **{inv['release_scope']['scope']}**.

{features}

{count_lines}

### Compatibility matrix

{compat}
{END}"""

def replace_block(text,block):
    """Replace marked generated content, or insert it without losing prose."""
    if START in text and END in text:
        return text[:text.index(START)] + block + text[text.index(END)+len(END):]
    # Place after first top-level heading/lede area.
    lines=text.splitlines(); at=1
    for i,line in enumerate(lines[1:],1):
        if line.startswith('## '): at=i; break
    return '\n'.join(lines[:at]).rstrip()+'\n\n'+block+'\n\n'+'\n'.join(lines[at:]).lstrip()

def validation_doc(inv):
    """Describe current qualification commands without asserting gate results."""
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
  content-hashed execution records and service objectives
  (not immutable custody).
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
    """Prepare generated resources from canonical inputs without writing them."""
    package,rt,_surface=root_from(root); inv=inventory(root); manifest=json.dumps(inv,indent=2,ensure_ascii=False)+'\n'; block=md_block(inv)
    readmes={package/'README.md',rt/'README.md'}
    readme_text={p:replace_block(p.read_text(encoding='utf-8'),block) for p in readmes if p.is_file()}
    return package,rt,inv,manifest,readme_text,validation_doc(inv)

def run(root: Path,check=False):
    """Generate projections or return nonzero on any exact-byte drift."""
    package,rt,inv,manifest,readmes,validation=outputs(root); mismatches=[]
    targets={rt/'_meta/release-manifest.json':manifest,package/'VALIDATION.md':validation,**readmes}
    # The CLI-facing GUIDE.md is a generated Markdown deployment projection.
    # Its only maintained source is the canonical main-documentation page.
    guide_source=package/'docs/reference/installed-cli-guide.md'
    if guide_source.is_file():
        targets[rt/'GUIDE.md']=guide_source.read_text(encoding='utf-8')
    compatibility_source=package/'docs/reference/compatibility.md'
    if compatibility_source.is_file():
        targets[compatibility_source]=replace_block(compatibility_source.read_text(encoding='utf-8'),md_block(inv))
    if check:
        for p,content in targets.items():
            if not p.is_file() or p.read_text(encoding='utf-8')!=content: mismatches.append(str(p))
        if mismatches:
            print('FAILED generated documentation drift:'); [print(' -',x) for x in mismatches]; return 1
        print(f"OK: generated docs match canonical manifest ({inv['counts']['roles']} roles, {inv['counts']['artifact_types']} artifact types, {inv['counts']['schemas']} schemas)"); return 0
    for p,content in targets.items(): p.parent.mkdir(parents=True,exist_ok=True); p.write_text(content,encoding='utf-8')
    print(f"wrote generated manifest/docs for {inv['release']}: {inv['counts']}"); return 0

def main():
    """Dispatch the source/installed documentation generation CLI."""
    ap=argparse.ArgumentParser(); ap.add_argument('--root',default='.'); ap.add_argument('--check',action='store_true'); a=ap.parse_args(); raise SystemExit(run(Path(a.root),a.check))
if __name__=='__main__': main()
