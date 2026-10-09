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


def command(name,args,timeout=120): return core.command(name,args,timeout=timeout)

def gate_a():
    return core.gate_a()+[command('GA release/version/changelog policy',[PY,str(TOOLS/'release_policy.py'),'check'])]

def gate_b(): return core.gate_b()

def gate_c():
    return core.gate_c()+[command('GA service objectives and reference SLA',[PY,str(TOOLS/'service_levels.py'),'check'])]

def gate_d():
    return core.gate_d()+[command('provider-neutral workload/model routing',[PY,str(TOOLS/'model_router.py'),'self-test'])]

def gate_e(): return core.gate_e()
def gate_f(): return core.gate_f()
def gate_g(): return core.gate_g()
GATES={'A':gate_a,'B':gate_b,'C':gate_c,'D':gate_d,'E':gate_e,'F':gate_f,'G':gate_g}


def gate_payload(gate,checks):
    return {'release':(PACKAGE/'VERSION').read_text().strip(),'qualification_profile':'enterprise-ga-unified-lifecycle','gate':gate,'generated_at':core.now(),'checks':checks,'pass':all(x['ok'] for x in checks)}

def run_gate(gate,out=None):
    checks=GATES[gate](); payload=gate_payload(gate,checks); target=Path(out) if out else GATE_DIR/f'gate-{gate}.json'; target.parent.mkdir(parents=True,exist_ok=True); target.write_text(json.dumps(payload,indent=2,ensure_ascii=False)+'\n'); print(('PASS' if payload['pass'] else 'FAIL'),f'Gate {gate}'); return 0 if payload['pass'] else 1

def assemble(gate_dir=GATE_DIR,out=AG):
    gate_dir=Path(gate_dir); checks={}; gates={}; problems=[]
    for gate in 'ABCDEFG':
        path=gate_dir/f'gate-{gate}.json'
        if not path.is_file(): problems.append(f'missing {path}'); continue
        data=json.loads(path.read_text())
        if data.get('gate')!=gate: problems.append(f'{path}: wrong gate identity')
        if data.get('release')!=(PACKAGE/'VERSION').read_text().strip(): problems.append(f'{path}: release identity mismatch')
        checks[gate]=data.get('checks',[]); gates[gate]=bool(data.get('pass'))
    payload={'release':(PACKAGE/'VERSION').read_text().strip(),'qualification':'enterprise-ga-gates-A-G','generated_at':core.now(),'gates':gates,'checks':checks,'all_pass':not problems and set(gates)==set('ABCDEFG') and all(gates.values())}
    Path(out).write_text(json.dumps(payload,indent=2,ensure_ascii=False)+'\n')
    for problem in problems: print('FAIL',problem)
    for gate in 'ABCDEFG':
        if gate in gates: print(('PASS' if gates[gate] else 'FAIL'),f'Gate {gate}')
    return 0 if payload['all_pass'] else 1

def prep_check():
    problems=[]
    if not AG.is_file(): problems.append('internal A-G qualification missing')
    else:
        data=json.loads(AG.read_text()); gates=data.get('gates',{})
        if set(gates)!=set('ABCDEFG') or not all(gates.values()): problems.append('A-G qualification is not all PASS')
    for name in ('SBOM.spdx.json','COMPATIBILITY.json','PROVENANCE.json'):
        if not (PACKAGE/name).is_file(): problems.append(f'{name} missing')
    for candidate in PACKAGE.glob('*.sig'):
        problems.append(
            f'{candidate.name} must not be packaged; CI attestation is external to ZIP'
        )
    if problems:
        for problem in problems: print('FAIL supply-chain prerequisite',problem)
        return {'name':'release integrity and automated-publication readiness','ok':False,'detail':'; '.join(problems)}
    print('PASS release integrity material present; ready for CI publication')
    return {'name':'release integrity and automated-publication readiness','ok':True,'detail':''}

def generate_release_evidence():
    return [
      command('generate SPDX SBOM',[PY,str(TOOLS/'supply_chain.py'),'sbom','--root',str(PACKAGE),'--out',str(PACKAGE/'SBOM.spdx.json')]),
      command('generate compatibility manifest',[PY,str(TOOLS/'supply_chain.py'),'compatibility','--root',str(PACKAGE),'--out',str(PACKAGE/'COMPATIBILITY.json')]),
      command('generate digest provenance',[PY,str(TOOLS/'supply_chain.py'),'provenance','--root',str(PACKAGE),'--sbom',str(PACKAGE/'SBOM.spdx.json'),'--qualification',str(AG),'--out',str(PACKAGE/'PROVENANCE.json')]),
    ]

def h_checks(generate=True):
    checks=generate_release_evidence() if generate else []
    checks += [prep_check(),command('BSD-4-Clause license policy',[PY,str(TOOLS/'license_check.py'),str(PACKAGE)]),command('supply-chain integrity self-test',[PY,str(TOOLS/'supply_chain.py'),'self-test']),command('provenance/SBOM/compatibility verification',[PY,str(TOOLS/'supply_chain.py'),'verify','--root',str(PACKAGE),'--sbom',str(PACKAGE/'SBOM.spdx.json'),'--provenance',str(PACKAGE/'PROVENANCE.json'),'--compatibility',str(PACKAGE/'COMPATIBILITY.json')])]
    return checks

def write_final(checks):
    source=json.loads(AG.read_text()); gates=dict(source.get('gates',{})); gates['H']=all(x['ok'] for x in checks)
    payload={'release':(PACKAGE/'VERSION').read_text().strip(),'qualification':'enterprise-ga-gates-A-H','generated_at':core.now(),'gates':gates,'checks':{**source.get('checks',{}),'H':checks},'behavioral_qualification':{'universal_release_scope':'harness + golden corpus + thresholds + adversarial evaluator','provider_model_claim':False,'deployment_requirement':'live provider/model results + qualification evidence manifest'},'archive_signing':'GitHub OIDC attestation when available','build_signing':'keyless-ci','publication_state':'qualified-for-ci-publication' if all(gates.values()) else 'blocked','all_pass':set(gates)==set('ABCDEFGH') and all(gates.values())}
    (PACKAGE/'QUALIFICATION-A-H.json').write_text(json.dumps(payload,indent=2,ensure_ascii=False)+'\n'); return payload

def run_h(generate=True):
    checks=h_checks(generate); final=write_final(checks); policy=command('final GA release-policy completeness',[PY,str(TOOLS/'release_policy.py'),'check','--final']); checks.append(policy); final=write_final(checks); passed=final['all_pass']; print(('PASS' if passed else 'FAIL'),'Gate H'); print(f"{(PACKAGE/'VERSION').read_text().strip()} qualification: {sum(final['gates'].values())}/8 gates PASS"); return 0 if passed else 1

def run_all(through_g=False):
    for gate in 'ABCDEFG':
        if run_gate(gate): return 1
    if assemble(): return 1
    if through_g: print(f"{(PACKAGE/'VERSION').read_text().strip()} qualification A-G: 7/7 gates PASS"); return 0
    return run_h(True)

def main():
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
