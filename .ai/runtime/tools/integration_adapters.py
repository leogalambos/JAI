#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Provider-neutral enterprise adapter contract and mutation-enforcement self-test."""
from __future__ import annotations
import argparse, hashlib, json, re, tempfile
from pathlib import Path
try: import jsonschema
except Exception: jsonschema=None
RUNTIME=Path(__file__).resolve().parents[1]
import schema_resolver
DIR=RUNTIME/'integrations/adapters'; SCHEMA_NAME='EnterpriseAdapterContract'
REGISTRY=RUNTIME/'integrations/adapter-registry.json'
PRIORITY=['itsm-cmdb','backlog-project','grc','ea-repository','ci-cd','identity','observability','financial-tbm']
OPS=['discover','read','query','create-draft','validate','propose-change','execute-approved-change','verify','rollback']
def load(p): return json.loads(Path(p).read_text())
def digest(change): return hashlib.sha256(json.dumps(change,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def build_registry():
    adapters=[]
    for priority,category in enumerate(PRIORITY,1):
        path=DIR/f'{category}.json'
        data=load(path)
        adapters.append({
            'priority':priority,
            'category':category,
            'contract':f'adapters/{path.name}',
            'operations':data.get('operations',[]),
            'authority':data.get('authority'),
        })
    return {
        'schema_version':'1.0.0',
        # The adapter model is independent of the product distribution.
        'generated_from':'integrations/adapters/*.json',
        'default_mode':'read-only/dry-run',
        'adapters':adapters,
    }

def validate_contracts():
    if jsonschema is None: return ['enterprise adapter schema validator unavailable']
    probs=[]; schema=schema_resolver.schema(SCHEMA_NAME); files=sorted(DIR.glob('*.json')); cats=set()
    for p in files:
        d=load(p)
        try:
            jsonschema.Draft202012Validator(schema).validate(d)
        except Exception as e: probs.append(f'{p.name}: {e}')
        cats.add(d.get('category'))
    expected=set(PRIORITY)
    if cats!=expected: probs.append(f'categories {sorted(cats)} != {sorted(expected)}')
    expected_registry=build_registry()
    if not REGISTRY.is_file():
        probs.append('adapter-registry.json missing')
    else:
        recorded = load(REGISTRY)
        baseline = recorded.pop('release', None)
        if not isinstance(baseline, str) or not re.fullmatch(
                r'\d{2}\.(?:0[1-9]|1[0-2])\.\d+', baseline):
            probs.append('adapter-registry.json invalid model origin release')
        if recorded != expected_registry:
            probs.append('adapter-registry.json drift from canonical adapter contracts')
    return probs


class ReferenceAdapter:
    """Dry-run reference model, without production mutation or approval authority.

    Args:
        category: Adapter category used only for draft simulation. Production
            mutations are unavailable here; an exact operator action is required.
    """
    def __init__(self,category): self.category=category; self.drafts={}; self.audit=[]
    def discover(self): return {'category':self.category,'capabilities':OPS}
    def read(self,key): return self.drafts.get(key)
    def query(self,_q): return list(self.drafts.values())
    def create_draft(self,change):
        d=digest(change); self.drafts[d]={'digest':d,'change':change,'status':'draft'}; return self.drafts[d]
    def validate(self,d): return bool(d in self.drafts and self.drafts[d]['status']=='draft')
    def propose_change(self,d):
        if not self.validate(d): raise ValueError('unknown/invalid draft')
        return {'digest':d,'scope':self.drafts[d]['change'].get('scope'),'status':'proposed'}
    def execute_approved_change(self,d,approval=None):
        """Refuse mutation: local approval dictionaries are not external authority.

        Args:
            d: Draft identifier; no target is changed.
            approval: Untrusted legacy value; never accepted as authorization.
        Raises:
            PermissionError: Always; configure a trusted host integration instead.
        """
        self.audit.append({'operation':'execute-approved-change','decision':'DENY','reason':'HOST_BROKER_REQUIRED'})
        raise PermissionError('external mutation not supported; exact operator action required')
    def verify(self,d): return self.drafts.get(d,{}).get('status')=='executed'
    def rollback(self,d,approval=None):
        """Refuse rollback through an untrusted local approval dictionary.

        Args:
            d: Draft identifier; no target is changed.
            approval: Legacy untrusted approval value.
        Raises:
            PermissionError: Always; rollback is an independently approved mutation.
        """
        self.audit.append({'operation':'rollback','decision':'DENY','reason':'HOST_BROKER_REQUIRED'})
        raise PermissionError('external mutation not supported; exact operator action required')

def self_test():
    probs=validate_contracts()
    a=ReferenceAdapter('itsm-cmdb'); assert a.discover()['category']=='itsm-cmdb'; ch={'scope':'service:PAYMENTS','operation':'update-cmdb','payload':{'state':'active'}}; draft=a.create_draft(ch); d=draft['digest']; assert a.validate(d); a.propose_change(d)
    try: a.execute_approved_change(d); probs.append('mutation succeeded without approval')
    except PermissionError: pass
    try: a.execute_approved_change(d,{'id':'A-bad','approver':'owner','scope':'wrong','digest':d}); probs.append('scope mismatch accepted')
    except PermissionError: pass
    try: a.execute_approved_change(d,{'id':'A-1','approver':'service-owner','scope':'service:PAYMENTS','digest':d}); probs.append('forged approval accepted')
    except PermissionError: pass
    if a.read(d)['status']!='draft': probs.append('dry-run draft was mutated')
    if not a.audit: probs.append('local denial event missing')
    if probs: [print('FAIL',x) for x in probs]; return 1
    print('PASS adapters: 8 categories, dry-run only; local approval dictionaries denied; production host integration NOT VERIFIED'); return 0

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('command',choices=['check','self-test']); a=ap.parse_args()
    if a.command=='self-test': return self_test()
    probs=validate_contracts(); [print('FAIL',x) for x in probs]; print(('PASS' if not probs else 'FAIL'),'adapter contracts'); return 1 if probs else 0
if __name__=='__main__': raise SystemExit(main())
