#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""AI IT House Unified Lifecycle GA qualification, gates A-H."""
from __future__ import annotations

import argparse, json
from pathlib import Path
import qualification_core as core

PACKAGE=Path(__file__).resolve().parents[3]
RUNTIME=PACKAGE/'.ai/runtime'
TOOLS=RUNTIME/'tools'
PY=core.PY
GATE_DIR=RUNTIME/'_meta/gates'
AG=RUNTIME/'_meta/qualification-A-G.json'


def command(name,args,timeout=120):
    """Execute an existing offline-controlled qualification command.

    Args:
        name: Public check label.
        args: Explicit executable argument vector.
        timeout: Maximum execution seconds.
    Returns:
        The actual PASS, FAIL or NOT_EXECUTED check result.
    """
    return core.command(name,args,timeout=timeout)

def gate_a():
    """Return structural/content checks plus the current release policy check."""
    return core.gate_a()+[command('GA release/version/changelog policy',[PY,str(TOOLS/'release_policy.py'),'check'])]

def gate_b():
    """Return the shared semantic qualification checks without waivers."""
    return core.gate_b()

def gate_c():
    """Return governance and service-level qualification checks."""
    return core.gate_c()+[command('GA service objectives and reference SLA',[PY,str(TOOLS/'service_levels.py'),'check'])]

def gate_d():
    """Return runtime security and provider-neutral routing checks."""
    return core.gate_d()+[command('provider-neutral workload/model routing',[PY,str(TOOLS/'model_router.py'),'self-test'])]

def gate_e():
    """Return actual publication checks, including mandatory renderer execution."""
    return core.gate_e()
def gate_f():
    """Return actual render-based visual qualification checks."""
    return core.gate_f()
def gate_g():
    """Return synthetic behavioral checks without live-provider qualification."""
    return core.gate_g()
GATES={'A':gate_a,'B':gate_b,'C':gate_c,'D':gate_d,'E':gate_e,'F':gate_f,'G':gate_g}


def gate_payload(gate,checks):
    """Bind nonempty executed checks to their current release and gate.

    Args:
        gate: Registered gate identity.
        checks: Actual execution results with explicit Boolean ok and state.
    Returns:
        Current-release report; missing or non-passing execution cannot pass.
    Raises:
        KeyError, OSError: If required result fields or release metadata are absent.
    """
    result=core.gate_payload(gate,checks)
    result.update(release=(PACKAGE/'VERSION').read_text().strip(),qualification_profile='enterprise-ga-unified-lifecycle')
    return result

def run_gate(gate,out=None):
    """Execute a registered gate and persist its actual result.

    Args:
        gate: Identifier A through G.
        out: Optional report destination, otherwise the internal gate directory.
    Returns:
        Zero only for successful execution of every required check.
    Raises:
        KeyError, OSError: For unknown gates or unavailable report storage.
    """
    checks=GATES[gate](); payload=gate_payload(gate,checks); target=Path(out) if out else GATE_DIR/f'gate-{gate}.json'; target.parent.mkdir(parents=True,exist_ok=True); target.write_text(json.dumps(payload,indent=2,ensure_ascii=False)+'\n'); print(('PASS' if payload['pass'] else 'FAIL'),f'Gate {gate}'); return 0 if payload['pass'] else 1

def assemble(gate_dir=GATE_DIR,out=AG):
    """Validate and assemble current-release executed gate evidence.

    Args:
        gate_dir: Directory containing the seven gate reports.
        out: Destination summary JSON.
    Returns:
        Zero only for seven matching nonempty executed PASS reports.
    Raises:
        OSError, ValueError: For unreadable or malformed existing JSON.
    """
    gate_dir=Path(gate_dir); checks={}; gates={}; problems=[]
    for gate in 'ABCDEFG':
        path=gate_dir/f'gate-{gate}.json'
        if not path.is_file(): problems.append(f'missing {path}'); continue
        data=json.loads(path.read_text())
        issues=core.gate_report_problems(data,gate,(PACKAGE/'VERSION').read_text().strip())
        problems.extend(f'Gate {gate}: {issue}' for issue in issues)
        checks[gate]=data.get('checks',[]) if isinstance(data,dict) else []; gates[gate]=not issues
    payload={'release':(PACKAGE/'VERSION').read_text().strip(),'qualification':'enterprise-ga-gates-A-G','generated_at':core.now(),'gates':gates,'checks':checks,'all_pass':not problems and set(gates)==set('ABCDEFG') and all(gates.values())}
    Path(out).write_text(json.dumps(payload,indent=2,ensure_ascii=False)+'\n')
    for problem in problems: print('FAIL',problem)
    for gate in 'ABCDEFG':
        if gate in gates: print(('PASS' if gates[gate] else 'FAIL'),f'Gate {gate}')
    return 0 if payload['all_pass'] else 1

def _summary_problems(source):
    """Recheck actual A-G evidence before H can consume an existing summary."""
    if not isinstance(source,dict): return ['qualification summary is not an object']
    release=(PACKAGE/'VERSION').read_text().strip()
    problems=[]
    if source.get('release')!=release: problems.append('qualification release identity mismatch')
    if source.get('all_pass') is not True: problems.append('A-G summary is not all PASS')
    gates=source.get('gates'); checks=source.get('checks')
    if not isinstance(gates,dict) or not isinstance(checks,dict): return problems+['qualification evidence maps missing']
    if set(gates)!=set('ABCDEFG') or set(checks)!=set('ABCDEFG'): problems.append('qualification gate coverage mismatch')
    for gate in 'ABCDEFG':
        report={'gate':gate,'release':source.get('release'),'pass':gates.get(gate),'checks':checks.get(gate)}
        problems.extend(f'Gate {gate}: {issue}' for issue in core.gate_report_problems(report,gate,release))
    return problems


def prep_check():
    """Check current A-G execution evidence and required integrity resources.

    Returns:
        Explicit PASS or FAIL; stale summaries cannot authorize qualification.
    Raises:
        OSError, ValueError: For unreadable or malformed existing evidence.
    """
    problems=[]
    if not AG.is_file(): problems.append('internal A-G qualification missing')
    else:
        problems.extend(_summary_problems(json.loads(AG.read_text())))
    for name in ('SBOM.spdx.json','COMPATIBILITY.json','PROVENANCE.json'):
        if not (PACKAGE/name).is_file(): problems.append(f'{name} missing')
    for candidate in PACKAGE.glob('*.sig'):
        problems.append(
            f'{candidate.name} must not be packaged; CI attestation is external to ZIP'
        )
    if problems:
        for problem in problems: print('FAIL supply-chain prerequisite',problem)
        return {'name':'release integrity and automated-publication readiness','ok':False,'state':'FAIL','detail':'; '.join(problems)}
    print('PASS release integrity material present; ready for CI publication')
    return {'name':'release integrity and automated-publication readiness','ok':True,'state':'PASS','detail':''}

def generate_release_evidence():
    """Execute existing SBOM, compatibility and digest-provenance generators."""
    return [
      command('generate SPDX SBOM',[PY,str(TOOLS/'supply_chain.py'),'sbom','--root',str(PACKAGE),'--out',str(PACKAGE/'SBOM.spdx.json')]),
      command('generate compatibility manifest',[PY,str(TOOLS/'supply_chain.py'),'compatibility','--root',str(PACKAGE),'--out',str(PACKAGE/'COMPATIBILITY.json')]),
      command('generate digest provenance',[PY,str(TOOLS/'supply_chain.py'),'provenance','--root',str(PACKAGE),'--sbom',str(PACKAGE/'SBOM.spdx.json'),'--qualification',str(AG),'--out',str(PACKAGE/'PROVENANCE.json')]),
    ]

def h_checks(generate=True):
    """Run mandatory supply-chain qualification without relaxing prerequisites.

    Args:
        generate: Whether to regenerate integrity resources before verification.
    Returns:
        Actual generation, prerequisite, licensing and integrity check results.
    """
    checks=generate_release_evidence() if generate else []
    checks += [prep_check(),command('BSD-4-Clause license policy',[PY,str(TOOLS/'license_check.py'),str(PACKAGE)]),command('supply-chain integrity self-test',[PY,str(TOOLS/'supply_chain.py'),'self-test']),command('provenance/SBOM/compatibility verification',[PY,str(TOOLS/'supply_chain.py'),'verify','--root',str(PACKAGE),'--sbom',str(PACKAGE/'SBOM.spdx.json'),'--provenance',str(PACKAGE/'PROVENANCE.json'),'--compatibility',str(PACKAGE/'COMPATIBILITY.json')])]
    return checks

def write_final(checks):
    """Persist current qualification only after rechecking source execution.

    Args:
        checks: Actual H results with explicit Boolean ok and execution state.
    Returns:
        Final report; stale or contradictory A-G evidence always blocks success.
    Raises:
        OSError, ValueError: If qualification input/output cannot be processed.
    """
    source=json.loads(AG.read_text())
    if not isinstance(source,dict): source={}
    source_gates=source.get('gates') if isinstance(source.get('gates'),dict) else {}
    source_checks=source.get('checks') if isinstance(source.get('checks'),dict) else {}
    release=(PACKAGE/'VERSION').read_text().strip()
    gates={gate:not core.gate_report_problems({'gate':gate,'release':source.get('release'),'pass':source_gates.get(gate),'checks':source_checks.get(gate)},gate,release) for gate in 'ABCDEFG'}
    gates['H']=not _summary_problems(source) and bool(checks) and all(x.get('ok') is True and x.get('state')=='PASS' for x in checks)
    payload={'release':release,'qualification':'enterprise-ga-gates-A-H','generated_at':core.now(),'gates':gates,'checks':{**source_checks,'H':checks},'behavioral_qualification':{'universal_release_scope':'harness + golden corpus + thresholds + adversarial evaluator','provider_model_claim':False,'deployment_requirement':'live provider/model results + qualification evidence manifest'},'archive_signing':'GitHub OIDC attestation when available','build_signing':'keyless-ci','publication_state':'qualified-for-ci-publication' if all(gates.values()) else 'blocked','all_pass':set(gates)==set('ABCDEFGH') and all(gates.values())}
    (PACKAGE/'QUALIFICATION-A-H.json').write_text(json.dumps(payload,indent=2,ensure_ascii=False)+'\n'); return payload

def run_h(generate=True):
    """Execute H and its final release policy check before claiming success.

    Args:
        generate: Regenerate integrity evidence when true.
    Returns:
        Zero only when all eight gates and final policy pass.
    """
    checks=h_checks(generate); final=write_final(checks); policy=command('final GA release-policy completeness',[PY,str(TOOLS/'release_policy.py'),'check','--final']); checks.append(policy); final=write_final(checks); passed=final['all_pass']; print(('PASS' if passed else 'FAIL'),'Gate H'); print(f"{(PACKAGE/'VERSION').read_text().strip()} qualification: {sum(final['gates'].values())}/8 gates PASS"); return 0 if passed else 1

def run_all(through_g=False):
    """Execute the full release sequence, stopping at any failed prerequisite.

    Args:
        through_g: Stop after A-G without claiming H when true.
    Returns:
        Zero only for the requested fully executed qualification scope.
    """
    for gate in 'ABCDEFG':
        if run_gate(gate): return 1
    if assemble(): return 1
    if through_g: print(f"{(PACKAGE/'VERSION').read_text().strip()} qualification A-G: 7/7 gates PASS"); return 0
    return run_h(True)

def main():
    """Dispatch qualification from process arguments.

    Returns:
        The selected qualification operation's exit status.
    Raises:
        SystemExit: If CLI syntax is invalid.
    """
    ap=argparse.ArgumentParser(); sp=ap.add_subparsers(dest='cmd',required=True)
    q=sp.add_parser('qualify'); q.add_argument('--through-g',action='store_true')
    g=sp.add_parser('gate'); g.add_argument('name',choices=list('ABCDEFG')); g.add_argument('--out')
    a=sp.add_parser('assemble'); a.add_argument('--gate-dir',default=str(GATE_DIR)); a.add_argument('--out',default=str(AG))
    h=sp.add_parser('gate-h'); h.add_argument('--no-generate',action='store_true')
    args=ap.parse_args()
    if args.cmd=='gate': return run_gate(args.name,args.out)
    if args.cmd=='assemble': return assemble(args.gate_dir,args.out)
    if args.cmd=='gate-h': return run_h(not args.no_generate)
    return run_all(args.through_g)

if __name__=='__main__': raise SystemExit(main())
