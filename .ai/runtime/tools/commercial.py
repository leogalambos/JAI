#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Opt-in commercial CLI joining canonical snapshots, calculation and discovery.

No operation grants authority or invokes an AI provider. JSON supplied by a worker
cannot authorize identity, capability evidence, approval or provider dispatch.
"""
import argparse
import json
from pathlib import Path
import commercial_core as core
import commercial_economics as economics
import commercial_plan as plan
import commercial_router as router
import commercial_lifecycle as lifecycle
import commercial_scheduler as scheduler
import commercial_proposal as proposal


def main(argv=None):
    """Execute one explicit opt-in command and print JSON.

    Args:
        argv: Optional CLI argument sequence.
    Returns:
        Zero on valid output; two on invalid input or blocked readiness.
    Raises:
        SystemExit: Invalid CLI syntax handled by argparse.
    """
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--profile', required=True, choices=['commercial-delivery/1'])
    commands=parser.add_subparsers(dest='command',required=True)
    for name in ('validate','discover','readiness','trace','project','import','calc','evaluate','plan','route','gate','archive','restore','activate','rollback','axes','schedule','roster'):
        sub=commands.add_parser(name)
        sub.add_argument('input',type=Path)
        if name=='gate':sub.add_argument('--phase',required=True,choices=core.PHASES)
        if name in ('archive','restore','rollback'):sub.add_argument('--store',type=Path,required=True)
        if name=='rollback':sub.add_argument('--expected-revision',type=int,required=True)
        if name=='trace':sub.add_argument('--version',required=True)
        if name=='project':
            sub.add_argument('--audience',required=True,choices=['client','internal'])
            sub.add_argument('--policy',type=Path)
        if name=='import':
            sub.add_argument('--store',type=Path,required=True)
            sub.add_argument('--expected-revision',type=int,required=True)
        if name=='calc':sub.add_argument('--operation',required=True,choices=sorted(economics._OPERATIONS))
    for name in ('proposal-plan','proposal-prepare','proposal-validate','proposal-handoff'):
        sub=commands.add_parser(name)
        sub.add_argument('input',type=Path)
        sub.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1])
        if name in ('proposal-prepare','proposal-handoff'):
            sub.add_argument('--output',type=Path,required=True)
        if name=='proposal-handoff':
            sub.add_argument('--kind',required=True,choices=proposal.CORE_KINDS+proposal.OPTIONAL_KINDS)
        if name in ('proposal-plan','proposal-prepare'):
            sub.add_argument('--user-root',type=Path)
            sub.add_argument('--organisation-root',type=Path)
            sub.add_argument('--engagement-root',type=Path)
    args=parser.parse_args(argv)
    try:
        if args.command.startswith('proposal-'):
            if args.command=='proposal-handoff':
                result=proposal.publication_handoff(args.input,args.kind,args.output,root=args.root)
            else:
                data=json.loads(args.input.read_text())
                if args.command=='proposal-validate':
                    result=proposal.validate_prepared(args.input,args.root) if data.get('package_kind')=='proposal-prepared-draft/1' else proposal.validate_package(data)
                else:
                    options={key:getattr(args,key) for key in ('user_root','organisation_root','engagement_root')}
                    result=proposal.plan_package(data,args.root,**options) if args.command=='proposal-plan' else proposal.prepare_package(data,args.output,args.root,**options)
            print(json.dumps(result,ensure_ascii=False,indent=2))
            consistency=result.get('consistency',result)
            return 2 if consistency.get('consistency_pass') is False or result.get('status')=='BLOCKED' else 0
        elif args.command=='plan':
            result={'order':plan.validate_plan(plan.load_plan(args.input, fixture=args.input.suffix=='.json'))}
        elif args.command=='archive':
            result=core.SnapshotStore(args.store).archive(args.input)
        elif args.command=='restore':
            result=core.SnapshotStore(args.store).restore(args.input)
        else:
            data=json.loads(args.input.read_text())
            if args.command=='schedule':result=scheduler.schedule(data)
            elif args.command=='roster':result=scheduler.validate_service_roster(data)
            elif args.command=='activate':
                result={'ready':False,'blockers':['Activation requires a trusted host engagement-owner verifier and current policy digest; JSON cannot authorize scope change.'],'authority_granted':False}
            elif args.command=='rollback':result={'revision':lifecycle.EngagementStore(args.store).rollback(data['activation_digest'],args.expected_revision)}
            elif args.command=='axes':
                result={'axes':{axis:default for axis,(default,_) in lifecycle.AXES.items()},
                        'receipt_ids':{},'presented_receipt_ids':[item.get('id') for item in data.get('receipts',[])],
                        'commitment_ready':False,'ready':False,
                        'blockers':['Trusted host authentication, producer identities and policy digest unavailable in JSON CLI; presented receipts are unverified.']}
            elif args.command=='validate':result={'valid':core.validate_snapshot(data)}
            elif args.command=='gate':result=core.commercial_gate(data,args.phase)
            elif args.command=='discover':result={'valid':core.validate_discovery(data)}
            elif args.command=='readiness':result=core.readiness(data)
            elif args.command=='trace':result=core.trace(data,args.version,reverse=True)
            elif args.command=='project':result=core.project(data,args.audience,json.loads(args.policy.read_text()) if args.policy else {})
            elif args.command=='import':result={'revision':core.SnapshotStore(args.store).commit(data,args.expected_revision)}
            elif args.command=='calc':result=economics._OPERATIONS[args.operation](data)
            elif args.command=='route':result=router.Catalog().route(data['question'],data['contract_ref'],data.get('domain_ids'),data.get('strategy','hierarchical'))
            else:result=router.evaluate_routing(data)
        print(json.dumps(result,ensure_ascii=False,indent=2))
        return 2 if isinstance(result,dict) and (result.get('ready') is False or result.get('complete') is False or result.get('feasible') is False or result.get('roster_ready') is False or result.get('feasible_aggregate_roster') is False or result.get('operational_recovery_verified') is False) else 0
    except (ValueError,KeyError,TypeError,OSError) as exc:
        print(json.dumps({'error':'Proposal command failed: invalid input or local resource.' if args.command.startswith('proposal-') else str(exc)}))
        return 2


if __name__=='__main__':
    raise SystemExit(main())
