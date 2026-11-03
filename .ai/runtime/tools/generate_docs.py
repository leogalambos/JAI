#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Generate release inventory/documentation from canonical package sources."""
from __future__ import annotations
import argparse, json, re, sys, textwrap
from schema_resolver import release_scope
from pathlib import Path
from guide_alias import GUIDE_SOURCE, guide_bytes

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
        Fresh public resource manifest and supported tool requirements. Internal
        development results and planning checkpoints are not publication inputs.
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
    version=(package/'VERSION').read_text().strip()
    return {
      'manifest_version':'1.0.0','release':version,
      'release_scope':release_scope(package),
      'counts':{'roles':len(roles.get('roles',[])),'agents':len(agents),'skills':len(skills),'workflows':len(workflows.get('workflows',[])),'artifact_types':len(taxonomy.get('artifact_types',{})),'schemas':len(schemas.get('schemas',[])),'renderers':len(renderers),'provider_adapters':len(adapters)},
      'roles_source':'runtime/roles.json','workflows_source':'runtime/workflows.json','artifact_taxonomy_source':'runtime/artifacts/schema/artifact-types.json','schema_registry_source':'runtime/schema/schema-registry.json',
      'agents':agents,'skills':skills,'provider_adapters':adapters,'renderers':renderers,
      'compatibility':[
        {'component': 'Claude Code', 'minimum': 'provider-supported', 'supported': 'Native role and workflow projections; effective isolation depends on the host sandbox.'},
        {'component': 'Codex CLI', 'minimum': 'provider-supported', 'supported': 'Native role and workflow skills; effective isolation depends on the host sandbox.'},
        {'component': 'Python', 'minimum': '3.10', 'supported': 'Standard-library installation; runtime contract workflows also require their declared dependencies.'},
        {'component': 'Pandoc', 'minimum': 'optional', 'supported': 'Optional document conversion.'},
        {'component': 'WeasyPrint', 'minimum': '70.x optional', 'supported': 'HTML/PDF publication using a CLI-first/current-Python fallback with constrained resource fetching; not Office fidelity.'},
        {'component': 'Pyphen', 'minimum': 'determined by the installed WeasyPrint dependency requirements', 'supported': 'WeasyPrint transitive dependency; the optional pip recipe selects 0.17.x without rejecting working OS packages.'},
        {'component': 'LibreOffice', 'minimum': 'Office-compatible host renderer', 'supported': 'Office document rendering in the native sandbox when available, otherwise through an explicit operator handoff.'},
        {'component': 'Poppler', 'minimum': 'pdftoppm on PATH', 'supported': 'PDF page rasterization for visual inspection.'},
        {'component': 'OpenSSL', 'minimum': 'Ed25519 genpkey and pkeyutl -rawin', 'supported': 'Host-confirmed key creation and explicit human signing; private keys stay outside agent access.'},
        {'component': 'Fonts/system libraries', 'minimum': 'DejaVu Sans and renderer-native layout libraries', 'supported': 'Required by the selected rendering tools.'},
        {'component': 'lxml', 'minimum': '5.x', 'supported': 'Architecture exchange conformance checks.'},
        {'component': 'jsonschema', 'minimum': '>=4.18,<5', 'supported': 'Required for runtime contract validation; not required for installation.'},
        {'component': 'Pillow', 'minimum': 'runtime-supported', 'supported': 'Image inspection and visual QA.'},
        {'component': 'GitHub Actions', 'minimum': 'release@YY.MM.VV tag workflow', 'supported': 'Validated source archives and checksums are published only after a matching release tag is pushed.'}
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

def outputs(root: Path):
    """Prepare generated resources from canonical inputs without writing them."""
    package,rt,_surface=root_from(root); inv=inventory(root); manifest=json.dumps(inv,indent=2,ensure_ascii=False)+'\n'; block=md_block(inv)
    readmes={package/'README.md',rt/'README.md'}
    readme_text={p:replace_block(p.read_text(encoding='utf-8'),block) for p in readmes if p.is_file()}
    return package,rt,inv,manifest,readme_text

def run(root: Path,check=False):
    """Generate projections without rewriting the single-source GUIDE alias.

    Args:
        root: Source package or installed runtime root accepted by root_from.
        check: Report projection drift without changing any output.
    Returns:
        Zero for current/generated projections; one for drift or an invalid
        declared GUIDE relationship. An invalid alias is never repaired by copying.
    Raises:
        OSError, ValueError: Other canonical input or generated output is unavailable.
        SystemExit: The supplied root is not a recognized package layout.
    """
    package,rt,inv,manifest,readmes=outputs(root); mismatches=[]
    targets={rt/'_meta/release-manifest.json':manifest,**readmes}
    # Source GUIDE is a Git alias; only installation and archives materialize it.
    guide_source=package/GUIDE_SOURCE
    if guide_source.is_file():
        try:
            guide_bytes(package)
        except (ValueError, OSError) as error:
            mismatches.append(str(error))
    if mismatches:
        print('FAILED GUIDE alias:'); [print(' -',x) for x in mismatches]; return 1
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
