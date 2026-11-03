#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Shared canonical provider projections, used by installer and native runtime."""
from __future__ import annotations
import copy
import json
import re
from pathlib import Path

def split_frontmatter(text):
    """Return portable scalar frontmatter and the unchanged canonical body."""
    if not text.startswith('---\n'): return {},text
    end=text.find('\n---\n',4)
    if end<0: return {},text
    fm=text[4:end].splitlines(); d={}
    for line in fm:
        m=re.match(r'^([A-Za-z0-9_-]+):\s*(.*)$',line)
        if m: d[m.group(1)]=m.group(2).strip().strip('"')
    return d,text[end+5:]

def model_mapping(registry,provider,workload_class):
    """Copy the explicit captured provider/workload mapping; missing entries fail."""
    try: return copy.deepcopy(registry['providers'][provider]['classes'][workload_class])
    except KeyError as exc: raise SystemExit(f'error: no model mapping for {provider}/{workload_class}') from exc

def model_selector(registry,provider,workload_class):
    """Return the exact selector from the supplied registry, without ambient reads."""
    return model_mapping(registry,provider,workload_class)['model_selector']

def render_claude_agent(src,registry,*,workload_class=None,tool_ceiling=None):
    """Render declared author tools within the inherited native sandbox.

    Args:
        src: Canonical agent source file, preserving its behavioral body.
        registry: Trusted model routing configuration.
        workload_class: Explicit selected workload, otherwise canonical agent class.
        tool_ceiling: Optional common source tool intersection for this assignment.
    Returns:
        UTF-8 agent with role tools; Bash requires a source author/execute tier.
        Reviewer shell stays unavailable without a read-only host boundary.
        This does not
        replace host mount/network isolation or prove live provider enforcement.
    """
    text=Path(src).read_text(encoding='utf-8'); fm,_=split_frontmatter(text)
    workload=workload_class or fm.get('model_class',registry.get('fallback_class','standard')); selector=model_selector(registry,'claude',workload)
    line=re.compile(r'^model_class:\s*[^\n]+$',re.MULTILINE)
    replacement='' if selector=='inherit' else f'model: {selector}'
    text=line.sub(replacement,text)
    declared={tool.strip() for tool in fm.get('tools','').split(',')}
    permitted={'Read','Grep','Glob','Write','Edit'}|({'Bash'} if declared&{'Write','Edit'} else set())
    safe=[tool.strip() for tool in fm.get('tools','').split(',') if tool.strip() in permitted]
    if tool_ceiling is not None: safe=[tool for tool in safe if tool in tool_ceiling]
    text=re.sub(r'^tools:\s*[^\n]+$', 'tools: '+', '.join(safe), text, flags=re.MULTILINE)
    return text.encode()

def skill_doc(name,desc,body,source_kind,source_name,tools=''):
    """Render a source-preserving Codex skill with honest tool-ceiling guidance."""
    desc=desc or f"Universal AI IS/IT house {source_kind}: {source_name}."
    note=(f"> Rendered from the provider-neutral {source_kind} `{source_name}`. The canonical source is under "
          f"`~/.ai/it-role-house/{source_kind}s/`." if source_kind!='command' else
          f"> Rendered from provider-neutral workflow command `/{source_name}`. The canonical source is under `~/.ai/it-role-house/commands/`.")
    if tools:
        note += f"\n> Source tool ceiling: `{tools}`. This is behavioral guidance only: Codex skills do not enforce tools, mounts or network permissions. The effective native sandbox and host access controls enforce permissions; operator actions remain external."
    return f"---\nname: {name}\ndescription: {json.dumps(desc,ensure_ascii=False)}\n---\n\n{note}\n\n{body.lstrip()}".encode()

def render_codex_skill(src,kind,name,registry,*,workload_class=None,tool_ceiling=None):
    """Project canonical agent, skill or command bytes with explicit model policy.

    Args:
        src: Canonical UTF-8 source path.
        kind: Agent, skill or command projection kind.
        name: Stable source identity.
        registry: Explicit effective or captured model registry.
        workload_class: Explicit local selection, otherwise canonical agent class.
        tool_ceiling: Optional common assignment source tool intersection.
    Returns:
        UTF-8 Codex skill bytes preserving the canonical behavioral body.
    Raises:
        OSError, SystemExit: Source or required model mapping unavailable.
    """
    text=Path(src).read_text(encoding='utf-8')
    fm,body=split_frontmatter(text)
    if tool_ceiling is not None:
        for key in ('tools','allowed-tools'):
            if key in fm: fm[key]=', '.join(tool.strip() for tool in fm[key].split(',') if tool.strip() in tool_ceiling)
    if kind=='skill':
        # OpenAI skill frontmatter retains portable identity/description; provider-specific tool declarations stay in the canonical source.
        nm=fm.get('name',name); desc=fm.get('description',f"AI IS/IT house skill {nm}.")
        return skill_doc(nm,desc,body,'skill',name,fm.get('allowed-tools',''))
    if kind=='agent':
        nm='agent-'+name; desc=fm.get('description',f"Provider-neutral operator contract for {name}.")
        workload=workload_class or fm.get('model_class',registry.get('fallback_class','standard')); mapping=model_mapping(registry,'codex',workload); selector=mapping['model_selector']
        effort=mapping.get('reasoning_effort'); behaviour=('the active Codex/session model' if selector=='inherit' else f'the configured Codex model `{selector}`')
        fallbacks=', '.join(x.get('model_selector','?') for x in mapping.get('fallbacks',[])) or 'none'
        extra=(f"\n\n## Provider adaptation\n\nWorkload class: `{workload}`. Project-managed routing selects {behaviour}" + (f" with reasoning effort `{effort}`" if effort else '') + f". Ordered fallbacks: `{fallbacks}`. `selection_strategy` is an AI IT House policy label, not an OpenAI API enum. Change provider/model mappings in the model registry override; do not edit this generated skill.")
        return skill_doc(nm,desc,body+extra,'agent',name,fm.get('tools',''))
    nm='workflow-'+name; desc=fm.get('description',f"Provider-neutral workflow /{name}.")
    body=body.replace('$ARGUMENTS','the user-provided workflow arguments')
    return skill_doc(nm,desc,body,'command',name,fm.get('allowed-tools',''))

