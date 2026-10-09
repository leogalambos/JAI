#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Transactional installer/upgrader for the provider-neutral AI IS/IT house.

The package source is canonical under .ai/. Provider-facing Claude/Codex artefacts are
rendered from it. State records SHA-256 for every owned output so upgrades can distinguish
an untouched package file from a locally modified file. Nothing is overwritten or removed
on a conflict unless --force is explicit; forced changes are backed up first.
"""
from __future__ import annotations
import argparse, copy, hashlib, json, os, re, shutil, subprocess, sys, tempfile, time
from pathlib import Path

SCHEMA=1
MARKERS={
 "claude":("<!-- BEGIN ai-it-house:claude -->","<!-- END ai-it-house:claude -->"),
 "codex":("<!-- BEGIN ai-it-house:codex -->","<!-- END ai-it-house:codex -->"),
}
LEGACY_MARKERS=("<!-- BEGIN it-role-library -->","<!-- END it-role-library -->")


def sha_bytes(b): return hashlib.sha256(b).hexdigest()
def sha_file(p):
    try:
        h=hashlib.sha256()
        with open(p,'rb') as f:
            for chunk in iter(lambda:f.read(1024*1024),b''): h.update(chunk)
        return h.hexdigest()
    except OSError: return None

def atomic_write(path,data,mode=None):
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    fd,tmp=tempfile.mkstemp(prefix='.'+path.name+'.',dir=str(path.parent))
    try:
        with os.fdopen(fd,'wb') as f: f.write(data)
        if mode is not None: os.chmod(tmp,mode)
        os.replace(tmp,path)
    except Exception:
        try: os.unlink(tmp)
        except OSError: pass
        raise

def backup_one(path, backup):
    path=Path(path)
    if not path.exists(): return False
    rel=Path(str(path).lstrip('/\\').replace(':','_'))
    dest=Path(backup)/rel; dest.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(path,dest)
    return True

def files_under(root):
    root=Path(root)
    return sorted([p for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts])

def split_frontmatter(text):
    if not text.startswith('---\n'): return {},text
    end=text.find('\n---\n',4)
    if end<0: return {},text
    fm=text[4:end].splitlines(); d={}
    for line in fm:
        m=re.match(r'^([A-Za-z0-9_-]+):\s*(.*)$',line)
        if m: d[m.group(1)]=m.group(2).strip().strip('"')
    return d,text[end+5:]

def deep_merge(base,override):
    if not isinstance(base,dict) or not isinstance(override,dict): return copy.deepcopy(override)
    out=copy.deepcopy(base)
    for k,v in override.items():
        out[k]=deep_merge(out[k],v) if k in out and isinstance(out[k],dict) and isinstance(v,dict) else copy.deepcopy(v)
    return out

def load_model_registry(pkg,override=None):
    base=json_load(pkg/'.ai/runtime/models/model-registry.json',{})
    path=Path(os.path.expanduser(override)).resolve() if override else None
    if path is None:
        env=base.get('configuration',{}).get('override_environment','AI_HOUSE_MODEL_CONFIG')
        configured=os.environ.get(env) or base.get('configuration',{}).get('override_file_default')
        path=Path(os.path.expanduser(configured)).resolve() if configured else None
    reg=deep_merge(base,json_load(path,{}) if path and path.is_file() else {})
    classes=reg.get('workload_classes',{}); providers=reg.get('providers',{})
    if reg.get('fallback_class') not in classes: raise SystemExit('error: invalid model registry fallback_class')
    for provider,spec in providers.items():
        missing=set(classes)-set(spec.get('classes',{}))
        if missing: raise SystemExit(f'error: model registry provider {provider} missing classes {sorted(missing)}')
    for required in ('claude','codex'):
        if required not in providers: raise SystemExit(f'error: model registry missing provider {required}')
    return reg,path if path and path.is_file() else None

def model_mapping(registry,provider,workload_class):
    try: return copy.deepcopy(registry['providers'][provider]['classes'][workload_class])
    except KeyError as exc: raise SystemExit(f'error: no model mapping for {provider}/{workload_class}') from exc

def model_selector(registry,provider,workload_class):
    return model_mapping(registry,provider,workload_class)['model_selector']

def render_claude_agent(src,registry):
    text=Path(src).read_text(encoding='utf-8'); fm,_=split_frontmatter(text)
    workload=fm.get('model_class',registry.get('fallback_class','standard')); selector=model_selector(registry,'claude',workload)
    line=re.compile(r'^model_class:\s*[^\n]+$',re.MULTILINE)
    replacement='' if selector=='inherit' else f'model: {selector}'
    return line.sub(replacement,text).encode()

def provider_contract_config(contract,provider,registry):
    workload=contract.get('workload_class',registry.get('fallback_class','standard')); mapping=model_mapping(registry,provider,workload); selector=mapping['model_selector']
    common={'name':contract['id'],'provider':provider,'workload_class':workload,'selection_strategy':registry['providers'][provider].get('selection_strategy'),'strategy_scope':registry['providers'][provider].get('strategy_scope','project-internal'),'model_selector':selector}
    if mapping.get('reasoning_effort'): common['reasoning_effort']=mapping['reasoning_effort']
    if mapping.get('fallbacks'): common['fallbacks']=copy.deepcopy(mapping['fallbacks'])
    if provider=='codex':
        common.update({'sandbox_mode':contract['sandbox']['mode'],'workspace_write':contract['sandbox']['workspace_write'],'network':contract['sandbox'].get('network'),'allowed_tools':contract['allowed_tools'],'denied_tools':contract['denied_tools'],'approval_required_for':contract.get('approval_required_for',[])})
        common['native_codex']={'model':selector,'model_reasoning_effort':mapping.get('reasoning_effort')} if selector!='inherit' else {'model':'inherit-session','model_reasoning_effort':mapping.get('reasoning_effort')}
        return common
    common.update({'tools':contract['allowed_tools'],'deny':contract['denied_tools'],'sandbox':contract['sandbox'],'approval_required_for':contract.get('approval_required_for',[])})
    return common

def skill_doc(name,desc,body,source_kind,source_name,tools=''):
    desc=desc or f"Universal AI IS/IT house {source_kind}: {source_name}."
    note=(f"> Rendered from the provider-neutral {source_kind} `{source_name}`. The canonical source is under "
          f"`~/.ai/it-role-house/{source_kind}s/`." if source_kind!='command' else
          f"> Rendered from provider-neutral workflow command `/{source_name}`. The canonical source is under `~/.ai/it-role-house/commands/`.")
    if tools:
        note += f"\n> Source tool ceiling: `{tools}`. Treat it as an authority boundary even when the current provider session exposes more tools."
    return f"---\nname: {name}\ndescription: {json.dumps(desc,ensure_ascii=False)}\n---\n\n{note}\n\n{body.lstrip()}".encode()

def render_codex_skill(src,kind,name,registry):
    text=Path(src).read_text(encoding='utf-8')
    fm,body=split_frontmatter(text)
    if kind=='skill':
        # OpenAI skill frontmatter retains portable identity/description; provider-specific tool declarations stay in the canonical source.
        nm=fm.get('name',name); desc=fm.get('description',f"AI IS/IT house skill {nm}.")
        return skill_doc(nm,desc,body,'skill',name,fm.get('allowed-tools',''))
    if kind=='agent':
        nm='agent-'+name; desc=fm.get('description',f"Provider-neutral operator contract for {name}.")
        workload=fm.get('model_class',registry.get('fallback_class','standard')); mapping=model_mapping(registry,'codex',workload); selector=mapping['model_selector']
        effort=mapping.get('reasoning_effort'); behaviour=('the active Codex/session model' if selector=='inherit' else f'the configured Codex model `{selector}`')
        fallbacks=', '.join(x.get('model_selector','?') for x in mapping.get('fallbacks',[])) or 'none'
        extra=(f"\n\n## Provider adaptation\n\nWorkload class: `{workload}`. Project-managed routing selects {behaviour}" + (f" with reasoning effort `{effort}`" if effort else '') + f". Ordered fallbacks: `{fallbacks}`. `selection_strategy` is an AI IT House policy label, not an OpenAI API enum. Change provider/model mappings in the model registry override; do not edit this generated skill.")
        return skill_doc(nm,desc,body+extra,'agent',name,fm.get('tools',''))
    nm='workflow-'+name; desc=fm.get('description',f"Provider-neutral workflow /{name}.")
    body=body.replace('$ARGUMENTS','the user-provided workflow arguments')
    return skill_doc(nm,desc,body,'command',name,fm.get('allowed-tools',''))

def render_placeholders(obj,ai_house):
    if isinstance(obj,str): return obj.replace('{AI_HOUSE}',str(ai_house))
    if isinstance(obj,list): return [render_placeholders(x,ai_house) for x in obj]
    if isinstance(obj,dict): return {k:render_placeholders(v,ai_house) for k,v in obj.items()}
    return obj

def json_load(path,default):
    try: return json.loads(Path(path).read_text(encoding='utf-8'))
    except FileNotFoundError: return copy.deepcopy(default)
    except json.JSONDecodeError as e: raise SystemExit(f"error: {path} is not valid JSON: {e}")

def hook_cmds(entry):
    return {h.get('command') for h in entry.get('hooks',[]) if isinstance(h,dict) and h.get('command')}

def remove_recorded_json(cur,record):
    cur=copy.deepcopy(cur)
    for key,vals in (record.get('permissions') or {}).items():
        have=cur.get('permissions',{}).get(key,[])
        for v in vals:
            while v in have: have.remove(v)
        if not have and 'permissions' in cur: cur['permissions'].pop(key,None)
    if cur.get('permissions')=={}: cur.pop('permissions',None)
    for event,cmds in (record.get('hooks') or {}).items():
        have=cur.get('hooks',{}).get(event,[]); cmds=set(cmds)
        cur['hooks'][event]=[e for e in have if not (hook_cmds(e)&cmds)]
        if not cur['hooks'][event]: cur['hooks'].pop(event,None)
    if cur.get('hooks')=={}: cur.pop('hooks',None)
    return cur

def merge_snippet(cur,snip):
    cur=copy.deepcopy(cur); added={'permissions':{},'hooks':{}}
    for key,vals in snip.get('permissions',{}).items():
        have=cur.setdefault('permissions',{}).setdefault(key,[])
        for v in vals:
            if v not in have: have.append(v); added['permissions'].setdefault(key,[]).append(v)
        if not have: cur['permissions'].pop(key,None)
    if cur.get('permissions')=={}: cur.pop('permissions',None)
    for event,entries in snip.get('hooks',{}).items():
        have=cur.setdefault('hooks',{}).setdefault(event,[])
        for e in entries:
            if e not in have: have.append(e); added['hooks'].setdefault(event,[]).extend(sorted(hook_cmds(e)))
    if cur.get('hooks')=={}: cur.pop('hooks',None)
    return cur,added

def managed_block(existing,begin,end,content,legacy=False):
    block=begin+'\n'+content.strip()+'\n'+end
    text=existing
    if legacy and LEGACY_MARKERS[0] in text and LEGACY_MARKERS[1] in text:
        a,b=text.split(LEGACY_MARKERS[0],1); _,c=b.split(LEGACY_MARKERS[1],1); text=(a+c).strip('\n')
    if begin in text and end in text:
        a,b=text.split(begin,1); _,c=b.split(end,1); return a+block+c
    if not text.strip(): return block+'\n'
    return text.rstrip()+"\n\n"+block+'\n'

def remove_block(text,begin,end):
    if begin not in text or end not in text: return text
    a,b=text.split(begin,1); _,c=b.split(end,1)
    return (a.rstrip()+('\n\n' if a.strip() and c.strip() else '')+c.lstrip()).rstrip()+('\n' if (a.strip() or c.strip()) else '')

def validate_package(pkg):
    errs=[]
    for p in (pkg/'.ai/skills').glob('*/SKILL.md'):
        fm,_=split_frontmatter(p.read_text(encoding='utf-8'))
        if not fm.get('name') or not fm.get('description'): errs.append(f"missing skill identity: {p}")
    names=[]
    for p in (pkg/'.ai/skills').glob('*/SKILL.md'):
        fm,_=split_frontmatter(p.read_text(encoding='utf-8')); names.append(fm.get('name'))
    if len(names)!=len(set(names)): errs.append('duplicate skill names')
    pys=[str(p) for p in files_under(pkg/'.ai/runtime') if p.suffix=='.py']
    if pys:
        r=subprocess.run([sys.executable,'-m','py_compile',*pys],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        if r.returncode: errs.append('python compile failed:\n'+r.stdout)
    if errs: raise SystemExit('error: package validation failed:\n  '+'\n  '.join(errs))

def desired_outputs(pkg,providers,ai_house,claude_home,codex_home,model_registry):
    out={}; modes={}
    # Shared runtime + canonical sources; setup source is not installed into the protected runtime.
    for section in ('runtime','skills','agents','commands'):
        root=pkg/'.ai'/section
        for p in files_under(root):
            rel=p.relative_to(root)
            dest=ai_house/(rel if section=='runtime' else Path(section)/rel)
            out[str(dest)]=p.read_bytes(); modes[str(dest)]=0o755 if p.suffix in ('.py','.sh') else 0o644
    # Install-time effective model routing and provider-native agent configs.
    effective=json.dumps(model_registry,indent=2,ensure_ascii=False)+'\n'
    out[str(ai_house/'models/effective-model-registry.json')]=effective.encode(); modes[str(ai_house/'models/effective-model-registry.json')]=0o644
    contracts=json_load(pkg/'.ai/runtime/agents/agent-contracts.json',{}).get('contracts',[])
    for contract in contracts:
        for provider in ('claude','codex'):
            dest=ai_house/'providers'/provider/(contract['id']+'.json')
            out[str(dest)]=(json.dumps(provider_contract_config(contract,provider,model_registry),indent=2,ensure_ascii=False)+'\n').encode(); modes[str(dest)]=0o644
    # Generated common manifest used by the live-tree guard.
    rels=[]
    for path in out:
        try: rels.append(str(Path(path).relative_to(ai_house)).replace(os.sep,'/'))
        except ValueError: pass
    manifest=(f"# ai-it-house package-owned common files; generated by installer\n"+'\n'.join(sorted(rels))+"\n").encode()
    out[str(ai_house/'MANIFEST')]=manifest; modes[str(ai_house/'MANIFEST')]=0o644
    if 'claude' in providers:
        for section in ('skills','agents','commands'):
            root=pkg/'.ai'/section
            for p in files_under(root):
                rel=p.relative_to(root); dest=claude_home/section/rel
                out[str(dest)]=render_claude_agent(p,model_registry) if section=='agents' and p.suffix=='.md' else p.read_bytes(); modes[str(dest)]=0o755 if p.suffix in ('.py','.sh') else 0o644
    if 'codex' in providers:
        for d in sorted((pkg/'.ai/skills').iterdir()):
            if d.is_dir() and (d/'SKILL.md').is_file():
                for p in files_under(d):
                    rel=p.relative_to(d); dest=codex_home/'skills'/d.name/rel
                    out[str(dest)]=render_codex_skill(p,'skill',d.name,model_registry) if rel.as_posix()=='SKILL.md' else p.read_bytes()
                    modes[str(dest)]=0o755 if p.suffix in ('.py','.sh') else 0o644
        for p in sorted((pkg/'.ai/agents').glob('*.md')):
            name=p.stem; dest=codex_home/'skills'/('agent-'+name)/'SKILL.md'
            out[str(dest)]=render_codex_skill(p,'agent',name,model_registry); modes[str(dest)]=0o644
        for p in sorted((pkg/'.ai/commands').glob('*.md')):
            name=p.stem; dest=codex_home/'skills'/('workflow-'+name)/'SKILL.md'
            out[str(dest)]=render_codex_skill(p,'command',name,model_registry); modes[str(dest)]=0o644
    return out,modes

def main():
    ap=argparse.ArgumentParser(description='Install/update the universal Claude + Codex AI IS/IT house')
    g=ap.add_mutually_exclusive_group(); g.add_argument('--claude-only',action='store_true'); g.add_argument('--codex-only',action='store_true')
    ap.add_argument('--dry-run',action='store_true'); ap.add_argument('--force',action='store_true',help='back up and replace locally modified/colliding managed files')
    ap.add_argument('--no-claude-md',action='store_true'); ap.add_argument('--no-codex-agents',action='store_true'); ap.add_argument('--no-hooks',action='store_true'); ap.add_argument('--model-config',help='JSON override for provider/workload-class model routing')
    a=ap.parse_args()
    pkg=Path(__file__).resolve().parents[2]
    validate_package(pkg)
    model_registry,model_config_source=load_model_registry(pkg,a.model_config)
    providers={'claude','codex'}
    if a.claude_only: providers={'claude'}
    if a.codex_only: providers={'codex'}
    home=Path(os.path.expanduser('~'))
    ai_home=Path(os.path.expanduser(os.environ.get('AI_IT_HOME','~/.ai'))).resolve()
    ai_house=Path(os.path.expanduser(os.environ.get('AI_IT_HOUSE',str(ai_home/'it-role-house')))).resolve()
    claude_home=Path(os.path.expanduser(os.environ.get('CLAUDE_HOME','~/.claude'))).resolve()
    codex_home=Path(os.path.expanduser(os.environ.get('CODEX_HOME','~/.codex'))).resolve()
    state_path=ai_house/'install-state.json'
    state=json_load(state_path,{}) if state_path.exists() else {}
    oldfiles=state.get('files',{}) if state.get('schema')==SCHEMA else {}
    desired,modes=desired_outputs(pkg,providers,ai_house,claude_home,codex_home,model_registry)
    # Preserve outputs of a provider omitted in a partial update; partial install must not uninstall the other provider.
    for path,h in oldfiles.items():
        pp=Path(path)
        if ('claude' not in providers and str(pp).startswith(str(claude_home)+os.sep)) or ('codex' not in providers and str(pp).startswith(str(codex_home)+os.sep)):
            if pp.exists(): desired[path]=pp.read_bytes(); modes[path]=pp.stat().st_mode & 0o777
    conflicts=[]; add=[]; update=[]; same=[]
    for path,data in desired.items():
        actual=sha_file(path); want=sha_bytes(data); prior=oldfiles.get(path)
        if actual is None: add.append(path)
        elif prior:
            if actual==want: same.append(path)
            elif actual==prior: update.append(path)
            else: conflicts.append((path,'locally modified managed file'))
        elif actual==want: same.append(path)
        else: conflicts.append((path,'pre-existing unowned file'))
    stale=[]
    for path,prior in oldfiles.items():
        if path in desired: continue
        actual=sha_file(path)
        if actual is None: continue
        if actual==prior: stale.append(path)
        else: conflicts.append((path,'locally modified obsolete managed file'))
    version=(pkg/'.ai/VERSION').read_text().strip()
    print(f"AI IS/IT house {version}: providers={','.join(sorted(providers))}")
    print(f"  model routing: {model_config_source if model_config_source else 'package defaults'}")
    print(f"  common {ai_house}\n  claude {claude_home}\n  codex  {codex_home}")
    print(f"  delta: {len(add)} new, {len(update)} changed, {len(same)} unchanged, {len(stale)} obsolete, {len(conflicts)} conflict(s)")
    if conflicts:
        print('\nConflicts:')
        for p,why in conflicts[:40]: print(f"  {why}: {p}")
        if not a.force:
            print('\nNothing was written. Re-run with --force to back up and replace/remove conflicting managed paths.')
            return 2
    if a.dry_run:
        print('\nDry run: package validated; nothing written.')
        return 0
    ts=time.strftime('%Y%m%d-%H%M%S'); backup=ai_home/'backups'/ts
    touched=set(update+stale+[p for p,_ in conflicts])
    if touched:
        for pstr in sorted(touched):
            backup_one(pstr, backup)
        print(f"  backup: {backup}")
    # Apply managed-file delta.
    conflict_paths={p for p,_ in conflicts}
    for path in stale:
        try: Path(path).unlink()
        except FileNotFoundError: pass
    for path,data in desired.items():
        if path in same: continue
        atomic_write(path,data,modes.get(path,0o644))
    # Remove forced stale conflicts only if they are truly no longer desired.
    if a.force:
        for path,_ in conflicts:
            if path not in desired:
                try: Path(path).unlink()
                except FileNotFoundError: pass
    oldmutable=state.get('mutable',{}) if state.get('schema')==SCHEMA else {}
    newmutable={}
    # Claude settings merge.
    if 'claude' in providers:
        sp=claude_home/'settings.json'; cur=json_load(sp,{})
        if oldmutable.get('claude_settings'): cur=remove_recorded_json(cur,oldmutable['claude_settings'])
        if not a.no_hooks:
            snip=render_placeholders(json_load(pkg/'.ai/adapters/claude/settings.snippet.json',{}),ai_house); snip.pop('$comment',None)
            cur,rec=merge_snippet(cur,snip); newmutable['claude_settings']=rec
        elif oldmutable.get('claude_settings'): newmutable['claude_settings']={}
        newbytes=(json.dumps(cur,indent=2,ensure_ascii=False)+'\n').encode()
        if (sp.read_bytes() if sp.exists() else b'') != newbytes:
            backup_one(sp,backup); atomic_write(sp,newbytes,0o644)
        if not a.no_claude_md:
            mp=claude_home/'CLAUDE.md'; existing=mp.read_text(encoding='utf-8') if mp.exists() else ''
            b,e=MARKERS['claude']; content=(pkg/'.ai/adapters/claude/CLAUDE.snippet.md').read_text(encoding='utf-8')
            newbytes=managed_block(existing,b,e,content,legacy=True).encode()
            if (mp.read_bytes() if mp.exists() else b'') != newbytes:
                backup_one(mp,backup); atomic_write(mp,newbytes,0o644)
            newmutable['claude_md']=True
    else:
        for k,v in oldmutable.items():
            if k.startswith('claude_'): newmutable[k]=v
    # Codex hooks + AGENTS.
    if 'codex' in providers:
        hp=codex_home/'hooks.json'; cur=json_load(hp,{})
        if oldmutable.get('codex_hooks'): cur=remove_recorded_json(cur,oldmutable['codex_hooks'])
        if not a.no_hooks:
            snip=render_placeholders(json_load(pkg/'.ai/adapters/codex/hooks.snippet.json',{}),ai_house); snip.pop('$comment',None)
            cur,rec=merge_snippet(cur,snip); newmutable['codex_hooks']=rec
            newbytes=(json.dumps(cur,indent=2,ensure_ascii=False)+'\n').encode()
            if (hp.read_bytes() if hp.exists() else b'') != newbytes:
                backup_one(hp,backup); atomic_write(hp,newbytes,0o644)
        elif hp.exists():
            newbytes=(json.dumps(cur,indent=2,ensure_ascii=False)+'\n').encode()
            if hp.read_bytes()!=newbytes:
                backup_one(hp,backup); atomic_write(hp,newbytes,0o644)
        if not a.no_codex_agents:
            mp=codex_home/'AGENTS.md'; existing=mp.read_text(encoding='utf-8') if mp.exists() else ''
            b,e=MARKERS['codex']; content=(pkg/'.ai/adapters/codex/AGENTS.snippet.md').read_text(encoding='utf-8')
            newbytes=managed_block(existing,b,e,content).encode()
            if (mp.read_bytes() if mp.exists() else b'') != newbytes:
                backup_one(mp,backup); atomic_write(mp,newbytes,0o644)
            newmutable['codex_agents']=True
    else:
        for k,v in oldmutable.items():
            if k.startswith('codex_'): newmutable[k]=v
    # Prune empty directories left by obsolete managed outputs.
    prune_roots=[ai_house, claude_home/'it-role-library', claude_home/'skills', claude_home/'agents', claude_home/'commands', codex_home/'skills']
    for root in prune_roots:
        if not root.exists(): continue
        for dp,dirs,fs in os.walk(root,topdown=False):
            try:
                if not os.listdir(dp): os.rmdir(dp)
            except OSError:
                pass

    # Signing key: never rotate during update.
    key=Path(os.path.expanduser(os.environ.get('FABRIC_AUTHORITY_KEY','~/.config/justifiable-fabric/authority.key')))
    key_created=bool(state.get('key_created'))
    if not key.exists():
        key.parent.mkdir(parents=True,exist_ok=True)
        fd=os.open(str(key),os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
        with os.fdopen(fd,'wb') as f: f.write(os.urandom(32))
        key_created=True
    # State is last: if we fail earlier, old state continues to describe the previous owned hashes.
    newstate={
      'schema':SCHEMA,'version':version,'installed_at':ts,'providers':sorted(set(state.get('providers',[])) | providers),
      'files':{p:sha_bytes(d) for p,d in sorted(desired.items())},'mutable':newmutable,
      'key_created':str(key) if key_created else None,'backup_last':str(backup) if backup.exists() else None
    }
    atomic_write(state_path,(json.dumps(newstate,indent=2,ensure_ascii=False)+'\n').encode(),0o600)
    print('\nInstallation/update complete.')
    if 'codex' in providers and not a.no_hooks:
        print('Codex: review/approve the installed hook configuration in Codex before relying on enforcement.')
    return 0

if __name__=='__main__': raise SystemExit(main())
