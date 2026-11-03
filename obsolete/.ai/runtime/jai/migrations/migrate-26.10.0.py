#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path

RELEASE='26.10.4'
MIGRATION_VERSION='2.0.0'
RETENTION_DEFAULT='inherit enterprise records/engagement retention policy'

def canonical_hash(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()

def migrate(c):
    if c.get('version') == '3.0.0' and 'jai' in c:
        out=json.loads(json.dumps(c))
        out.setdefault('lifecycle',{})['retention']=out.get('lifecycle',{}).get('retention',RETENTION_DEFAULT)
        comp=out.setdefault('compatibility',{})
        comp['reads']=sorted(set(comp.get('reads',[])+['26.10.0/ArtifactContract-v2','26.10.1/ArtifactContract-v3','26.10.2/ArtifactContract-v3','26.10.3/ArtifactContract-v3']))
        comp['writes']='26.10.4/ArtifactContract-v3'; comp['migration']='forward-only'
        return out
    return {
      'id':c['id'],'version':'3.0.0','role_slug':c['role_slug'],'deliverable_number':c['deliverable_number'],'source_fingerprint':c['source_fingerprint'],
      'jai':{'core_version':'1.0.0',
        'intent':{'purpose':c['purpose'],'audience':c['audience'],'decision_supported':c['decision_supported'],'owner_role':c['owner_role'],'classification':c['classification']},
        'semantics':{'artifact_type':c['artifact_type'],'schema_ref':c['schema_ref'],'required_inputs':c['required_inputs'],'required_relations':c['required_relations']},
        'justification':{'required_evidence':c['required_evidence'],'acceptance_profile':c['acceptance_profile'],'evidence_profile':c['evidence_profile'],'reviewers':c['reviewers'],'approver':c['approver'],'semantic_policy':c['semantic_gate'],'repository_policy':c['repository_gate']},
        'design':{'mandatory_sections':c['mandatory_sections'],'publication_profile':c['publication_profile']},
        'realisation':{'producer':c['producer'],'renderer':c['renderer'],'output_formats':c['output_formats'],'system_of_record':c['system_of_record'],'external_handoff_adapter':c['external_handoff_adapter'],'production_mode':c['production_mode']},
        'evidence':{'obligations':['semantic validation','projection/publication validation where applicable','render/visual evidence where applicable'],'publication_gate':c['publication_gate'],'portfolio_traceability':c['portfolio_traceability']}},
      'lifecycle':{**c['lifecycle'],'version':'3.0.0','retention':c.get('retention',RETENTION_DEFAULT)},'traceability':c['traceability'],
      'compatibility':{'reads':['26.10.0/ArtifactContract-v2','26.10.1/ArtifactContract-v3','26.10.2/ArtifactContract-v3','26.10.3/ArtifactContract-v3'],'writes':'26.10.4/ArtifactContract-v3','migration':'forward-only','classification_source':'explicit-ga-26.10.1'},
      'migration':{'source_release':'26.10.0','source_schema':'ArtifactContract-v2','source_id':c['id'],'source_hash':canonical_hash(c),'migration_version':MIGRATION_VERSION}
    }

def main():
    p=argparse.ArgumentParser(); p.add_argument('input'); p.add_argument('output'); a=p.parse_args()
    d=json.loads(Path(a.input).read_text()); rows=[migrate(x) for x in d.get('contracts',[d])]
    out={'schema_version':'3.0.0','release':RELEASE,'authoritative_write_model':True,'native_write_enforced':True,'legacy_read_source':'role-deliverables.v2.json','role_count':d.get('role_count',len({x['role_slug'] for x in rows})),'deliverable_count':len(rows),'contracts':rows} if 'contracts' in d else rows[0]
    Path(a.output).write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
if __name__=='__main__': main()
