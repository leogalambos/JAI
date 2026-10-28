#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Provider-neutral Agent Contract enforcement with configurable model routing."""
from __future__ import annotations
import argparse,json,tempfile
try: import jsonschema
except Exception: jsonschema=None
from model_router import effective_registry, resolve
from pathlib import Path
import schema_resolver
ROOT=Path(__file__).resolve().parents[1]
CONTRACTS=ROOT/'agents/agent-contracts.json'; POLICY=ROOT/'policy/managed-policy.json'; BINDINGS=ROOT/'jai/profiles/runtime-agent-bindings.json'

def load(p):
    """Read required JSON without permissive fallback."""
    return json.loads(Path(p).read_text(encoding='utf-8'))

def release_scope(root=None):
    """Return validated canonical product metadata, never an execution grant.

    Args:
        root: Trusted package/runtime root; defaults to this runtime.
    Returns:
        The selected RELEASE-SCOPE.json, validated without any generated fallback.
    Raises:
        OSError, ValueError: Missing/malformed resources or unsupported release
            scope schema. This narrow metadata validator uses the standard
            library; runtime Agent/Policy contracts still require jsonschema.
    """
    return schema_resolver.release_scope(ROOT if root is None else root)

def contracts():
    """Load schema-validated canonical contracts; missing validation fails closed."""
    rows=load(CONTRACTS)['contracts']; bindings=load(BINDINGS)['bindings']
    if jsonschema is None: raise ValueError('AgentContract validator unavailable')
    validator=jsonschema.Draft202012Validator(schema_resolver.schema('AgentContract'))
    for row in rows: validator.validate(row)
    for row in rows:
        b=bindings.get(row['id'])
        if not b: raise ValueError(f"{row['id']}: missing runtime JAI binding")
        j=row.get('jai',{})
        if j.get('profile')!='runtime' or j.get('layer')!=b.get('primary_layer') or j.get('authority_ref')!=f"human-authority:{row['authority_boundary']}":
            raise ValueError(f"{row['id']}: embedded JAI binding disagrees with runtime profile")
    return {x['id']:x for x in rows}

def authorize(c,operation,tool=None):
    """Return advisory contract compatibility; never a host execution grant.

    Args:
        c: Exact registered AgentContract, not an agent-generated role definition.
        operation: Known read/write diagnostic operation. Privileged execution
            is unavailable; request an exact operator action instead.
        tool: Optional exact registered tool identifier.
    Returns:
        Boolean and safe reason; lookup/validation failures and unknowns deny.
    """
    try:
        release_scope()
        if contracts().get(c.get('id')) != c: return False,'unknown or altered agent contract'
        policy=load(POLICY)
        if jsonschema is None: return False,'policy validator unavailable'
        jsonschema.Draft202012Validator(schema_resolver.schema('PolicyContract')).validate(policy)
    except Exception: return False,'policy or contract validation unavailable'
    if operation not in {'read','query','discover','validate','verify','write','edit','mutate'}:
        return False,'unknown or privileged operation unavailable; operator action required'
    if operation in set(policy.get('denied_operations',[])): return False,f'{operation} denied by enterprise policy'
    if operation in ('write','edit','mutate') and not c['mutation_allowed']: return False,'reviewer-write denied'
    if operation=='policy-change': return False,'policy mutation requires independent human approval'
    if operation=='self-approve': return False,'self-approval denied'
    if operation=='restricted-mcp-via-shell': return False,'restricted MCP bypass via shell denied'
    if tool and tool in c.get('denied_tools',[]): return False,f'tool {tool} denied'
    if tool and c.get('allowed_tools') and tool not in c['allowed_tools']: return False,f'tool {tool} outside allowlist'
    return True,'allowed'

def provider_config(c,provider,model_config=None):
    """Compile contract intent to conservative native restrictions and host obligations.

    Args:
        c: Validated canonical AgentContract; mutation intent stays in that contract.
        provider: Claude or Codex projection selector.
        model_config: Optional trusted model-routing configuration.
    Returns:
        Role-scoped native workspace settings. These never override the host's
        effective sandbox or confer privileged deployment capabilities.
    Raises:
        ValueError: Unsupported provider or model-routing configuration.
    """
    if provider not in ('claude','codex'):
        raise ValueError('unsupported provider')
    workload_class=c.get('workload_class','standard')
    selector,mapping=resolve(provider,workload_class,model_config)
    registry,_=effective_registry(model_config); pspec=registry['providers'][provider]
    common={'name':c['id'],'provider':provider,'jai':c['jai'],'workload_class':workload_class,'selection_strategy':pspec.get('selection_strategy'),'strategy_scope':pspec.get('strategy_scope','project-internal'),'model_selector':selector}
    content_profile=ROOT/'jai/profiles/content-profile.json'
    extensions=load(content_profile).get('agent_bindings',{}).get(c['id'],{}) if content_profile.exists() else {}
    if extensions:
        if extensions!={'content_profile_ref':'jai/profiles/content-profile.json'}:
            raise ValueError('unsupported or unsafe provider profile extension')
        common.update(extensions)
    scope=release_scope()
    common['runtime_boundary']={'scope':scope['scope'],'live_verified':False,
        'hardened_privileged_enabled':scope['hardened_privileged']['enabled'],'protected_resources':'deny',
        'git_authority':'human','enforcement':'effective-provider-sandbox-and-host'}
    if mapping.get('reasoning_effort'): common['reasoning_effort']=mapping['reasoning_effort']
    if mapping.get('fallbacks'): common['fallbacks']=mapping['fallbacks']
    author=bool(c['mutation_allowed'])
    # A tool name is not containment. Codex reviewers retain its native read-only
    # mode; Claude's default sandbox does not establish a read-only source mount.
    shell_allowed='Bash' in c['allowed_tools'] and 'Bash' not in c['denied_tools'] and (author or provider=='codex')
    permitted={'Read','Grep','Glob'}|({'Write','Edit'} if author else set())|({'Bash'} if shell_allowed else set())
    safe_tools=[tool for tool in c['allowed_tools'] if tool in permitted and tool not in c['denied_tools']]
    denied_tools=sorted(set(c['denied_tools'])|{'Agent','WebFetch'}|(set() if shell_allowed else {'Bash','Shell'})|(set() if author else {'Write','Edit'}))
    common['local_execution']={'requires_effective_native_sandbox':True,'contract_is_host_enforcement':False,
        'reviewer_source_write':False,'qa_output':'only explicitly native-writable scratch; never widen source access',
        'shell_available':shell_allowed,'host_mount_isolation_required':True,'limitation':'Claude reviewer shell requires an independently established read-only boundary' if not author and provider=='claude' else 'Native settings must actually be loaded; no live confinement claim'}
    mode='workspace-write' if author else 'read-only'
    if provider=='codex':
        common.update({'sandbox_mode':mode,'workspace_write':author,'network':False,'allowed_tools':safe_tools,'denied_tools':denied_tools,'approval_required_for':c.get('approval_required_for',[])})
        common['native_codex']={'model':selector if selector!='inherit' else 'inherit-session','model_reasoning_effort':mapping.get('reasoning_effort'),'sandbox_mode':mode,'approval_policy':'on-request'}
        return common
    common.update({'tools':safe_tools,'deny':denied_tools,'sandbox':{'mode':mode,'workspace_write':author,'network':False},'approval_required_for':c.get('approval_required_for',[])})
    common['native_claude']={'permissionMode':'default','allowedTools':safe_tools,'disallowedTools':denied_tools,'sandbox':{'enabled':True,'failIfUnavailable':True,'autoAllowBashIfSandboxed':False,'allowUnsandboxedCommands':False,'excludedCommands':[]}}
    return common

def generate(outdir):
    """Generate detached provider projections; never edit effective user settings."""
    out=Path(outdir); (out/'codex').mkdir(parents=True,exist_ok=True); (out/'claude').mkdir(parents=True,exist_ok=True)
    for c in contracts().values():
        for p in ('codex','claude'):(out/p/f"{c['id']}.json").write_text(json.dumps(provider_config(c,p),indent=2)+'\n')

def self_test():
    """Check enabled contract permissions and disabled privileged release surface."""
    cs=contracts(); tests=[]
    import release_bundle
    tests.append(('validated-release-scope',bool(release_scope())))
    source_layout=(ROOT.parent/'setup/installer.py').is_file()
    # Installed runtime parents may be an operator home: never enumerate them.
    package_root=ROOT.parents[1] if source_layout else ROOT
    if source_layout:
        shipped={str(p.relative_to(package_root)) for p in release_bundle.files(package_root)}
        unavailable=not any(release_bundle.hardened_resource(p) for p in shipped)
    else:
        unavailable=not any((ROOT/'tools'/name).exists() for name in release_bundle.HARDENED_MODULES)
    tests.append(('hardened-code-not-shipped',unavailable))
    for n in ['codebase-reviewer','gate-auditor','sod-reviewer','sabsa-reviewer','visual-quality-reviewer','evidence-rationale-reviewer']:
        if n in cs: tests.append((n+'-write-denied',not authorize(cs[n],'write')[0]))
    if 'role-author' in cs:
        tests += [('author-write',authorize(cs['role-author'],'write')[0]),('author-policy-denied',not authorize(cs['role-author'],'policy-change')[0]),('shell-bypass-denied',not authorize(cs['role-author'],'restricted-mcp-via-shell')[0])]
    with tempfile.TemporaryDirectory() as td:
        generate(td); tests.append(('codex-native-config',(Path(td)/'codex/codebase-reviewer.json').exists())); tests.append(('claude-config',(Path(td)/'claude/codebase-reviewer.json').exists())); tests.append(('model-class-preserved',provider_config(cs['codebase-reviewer'],'claude')['workload_class']==cs['codebase-reviewer']['workload_class'])); tests.append(('jai-binding-propagated',provider_config(cs['codebase-reviewer'],'codex')['jai']['profile']=='runtime'))
    for n,v in tests: print(('PASS' if v else 'FAIL'),n)
    print(f"{sum(v for _,v in tests)}/{len(tests)} PASS"); return 0 if all(v for _,v in tests) else 1

def main():
    """Run public contract diagnostics or detached configuration generation."""
    ap=argparse.ArgumentParser();sp=ap.add_subparsers(dest='cmd',required=True);g=sp.add_parser('generate');g.add_argument('--out',required=True);c=sp.add_parser('check');c.add_argument('agent');c.add_argument('operation');c.add_argument('--tool');sp.add_parser('self-test');a=ap.parse_args()
    if a.cmd=='self-test': raise SystemExit(self_test())
    if a.cmd=='generate': generate(a.out); print(a.out); return
    cc=contracts().get(a.agent)
    if not cc: raise SystemExit('unknown agent')
    ok,why=authorize(cc,a.operation,a.tool); print(('ALLOW' if ok else 'DENY'),why); raise SystemExit(0 if ok else 3)
if __name__=='__main__': main()
