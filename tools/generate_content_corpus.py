#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Generate reproducible synthetic DCS development examples, never human gold.

Variants are explicit mutations with expected rule IDs and observable defects.
These fixtures qualify the foundation test harness, not production content QA.
"""
import argparse
import sys
import copy
import json
from pathlib import Path
from generate_content_catalog import BINDINGS, FAMILIES, ROOT

sys.path.insert(0, str(ROOT / '.ai/runtime/tools'))
from content_mutations import apply_variant

SCENARIOS = {
 'simple':{'name':'Inventory service recovery','scope':'One internal inventory service, a PostgreSQL database and twelve authorised warehouse operators.','drivers':'Restore warehouse inventory updates within 30 minutes; data loss must remain below five minutes.','design':'One application instance and a standby database in the existing managed platform.','cost':'EUR 18000 implementation and EUR 6000 annual operation; one-year benefit EUR 32000, with a 25 percent adoption uncertainty.','risk':'Database replication delay can lose updates; lag alert at 60 seconds and hourly recovery-point checks reduce likelihood.','operations':'Warehouse operations owns support from 06:00 to 22:00; the platform duty engineer handles recovery escalation.','regulatory':False,'privacy':False},
 'medium':{'name':'Regional order integration','scope':'Three regional order services, ERP integration, identity management and two operations teams.','drivers':'Reconcile regional orders within 15 minutes with 99.9 percent monthly availability and no duplicated financial postings.','design':'An idempotent event gateway connects three regional services to ERP using versioned schemas and a dead-letter queue.','cost':'EUR 420000 implementation and EUR 90000 annual operation; three-year avoided handling cost EUR 810000, sensitive to order volume by 30 percent.','risk':'Replayed events can duplicate postings; deduplication keys and reconciled ledger totals reduce exposure but require weekly evidence review.','operations':'Regional service owners retain customer support; the integration team owns gateway recovery and ERP reconciliation escalation.','regulatory':False,'privacy':True},
 'complex':{'name':'Regulated payment platform transition','scope':'A payment platform across two jurisdictions, legacy ledger migration, external settlement and 24-hour incident response.','drivers':'Preserve reconciled balances and a 15-minute recovery objective while retaining auditable transaction evidence within approved jurisdictions.','design':'A staged migration uses immutable event IDs, dual reconciliation and approved regional failover; outbound settlement remains gated by ledger equality.','cost':'EUR 8400000 transition and EUR 1900000 annual operation; five-year benefits EUR 16000000, sensitive to delay and compliance cost by 35 percent.','risk':'Cross-border failover can violate approved data-location constraints; regional routing and policy checks reduce exposure, with legal interpretation remaining reviewable.','operations':'The payment service owner authorises cutover; independent control assurance and round-the-clock operations review reconciliation before traffic migration.','regulatory':True,'privacy':True},
}
def populated_units(family, complexity, scenario):
    """Return concrete fictional semantic units for one reference document.

    family selects an authored FAMILIES contract; complexity selects simple,
    medium or complex constants; scenario supplies the fictional business scope.
    Raises KeyError or ValueError for unsupported authored identifiers.
    """
    index=['simple','medium','complex'].index(complexity)
    capex=[18000,420000,8400000][index];opex=[6000,90000,1900000][index]
    years=[1,3,5][index];benefit=[32000,270000,3200000][index]
    uncertainty=[.25,.30,.35][index]
    owner=['Morgan Lee','Alex Chen','Sam Rivera'][index]
    prefix=['INV','ORD','PAY'][index];recovery=[30,15,15][index]
    horizon_cost=capex+opex*years;gross=benefit*years
    cost={'currency':'EUR','horizon_years':years,'transition':capex,'annual_operation':opex,'total_cost':horizon_cost,'annual_avoided_manual_cost':benefit,'gross_benefit':gross,'net_benefit':gross-horizon_cost,'benefit_basis':'Avoided manual processing only; no revenue uplift counted.','benefit_owner':owner}
    options=[{'id':'BASE','name':'Retain current service','transition':0,'annual_operation':opex+benefit,'recovery_minutes':recovery+18,'criterion_result':'Fails recovery objective'}, {'id':'TARGET','name':'Managed recovery deployment','transition':capex,'annual_operation':opex,'recovery_minutes':recovery-3,'criterion_result':'Meets proposed recovery objective'}]
    risk={'id':prefix+'-R1','cause':'Recovery checkpoint lags active transaction state','event':'Replay duplicates a committed transaction','consequence':'Ledger imbalance delays service restoration','owner':owner,'inherent':{'likelihood':3,'impact':4,'score':12},'residual':{'likelihood':2,'impact':4,'score':8},'control_ref':prefix+'-C1','evidence_ref':'SYN-01'}
    controls=[{'id':prefix+'-C1','criterion':'Repeated event IDs must not create a second ledger entry','procedure':'Submit the same transaction ID twice and compare the ledger total','sample_size':[10,100,1000][index],'observed_duplicates':0,'result':'met in synthetic rehearsal','evidence_ref':'SYN-01'}]
    entities=[{'id':prefix+'-APP','type':'application','name':scenario['name'],'responsibility':'Accept authorised transaction requests and return durable IDs'}, {'id':prefix+'-DB','type':'data-store','name':'PostgreSQL ledger','responsibility':'Persist unique event IDs and reconciled balances'}, {'id':prefix+'-OPS','type':'operational-role','name':owner,'responsibility':'Own restore rehearsal and incident escalation'}]
    interfaces=[{'id':prefix+'-IF1','source':prefix+'-APP','target':prefix+'-DB','protocol':'PostgreSQL TLS','contract_version':'1.0','fields':['event_id','amount','status'],'failure':'Timeout after 5 seconds; retry twice with same event_id; then reject and alert','trust_boundary':'Application service identity to restricted database role'}]
    evidence={'id':'SYN-01','status':'synthetic-assumption','date':'2026-10-19','environment':prefix.lower()+'-rehearsal','build':'candidate-1.0','owner':owner}
    acceptance={'status':'pending-human-approval','receiving_owner':owner,'open_item':prefix+'-DEF1','approval_ref':None,'condition':'Independent operations authority reviews pending load retest before acceptance.'}
    results=[{'id':prefix+'-EX1','requirement':prefix+'-REC1','started':'2026-10-19T09:00:00Z','finished':f'2026-10-19T09:{recovery-3:02d}:00Z','expected_max_minutes':recovery,'actual_minutes':recovery-3,'result':'PASS','evidence_ref':'SYN-01'}, {'id':prefix+'-EX2','requirement':prefix+'-INT1','started':'2026-10-19T10:00:00Z','finished':'2026-10-19T10:02:00Z','expected_ledger_count':[10,100,1000][index],'actual_ledger_count':[10,100,1000][index],'result':'PASS','evidence_ref':'SYN-01'}]
    defects=[{'id':prefix+'-DEF1','severity':'material','description':'Retry queue drain under peak load remains untested','status':'retest-pending','owner':owner,'due':'2026-11-05','impact':'Peak-load recovery claim remains outside demonstrated scope'}]
    treatment=[{'risk_ref':risk['id'],'action':'Enable unique event_id constraint and rehearse restored-ledger reconciliation','owner':owner,'due':'2026-11-05','verification_ref':prefix+'-EX2','acceptance_authority':'Independent service risk owner','approval_status':'pending'}]
    decision={'question':'Approve TARGET managed recovery design or retain BASE?','owner':owner,'authority':'Service investment board','deadline':'2026-11-12','status':'proposed'}
    records={
      'decision-paper':[decision,{'problem':'Synthetic rehearsal missed the recovery objective by 18 minutes','current_recovery_minutes':recovery+18,'objective_minutes':recovery,'evidence_ref':'SYN-01'},options,{'financial_model':cost,'risk':risk,'criteria':['recovery time','lifetime cost','operator effort'],'uncertainty':f'Benefit adoption may be {uncertainty*100:g} percent below plan','adoption_uncertainty_fraction':uncertainty}, {'option_ref':'TARGET','rationale':'TARGET meets the recovery objective; BASE exceeds it by 18 minutes. Additional investment buys a measurable recovery improvement.','condition':'Independent operations acceptance remains pending'}],
      'adr':[{'concern':'Recover service without duplicate committed transactions','scope':scenario['scope'],'status':'proposed'},options,{'choice':'TARGET','owner':owner,'date':'2026-10-19','rationale':'Unique transaction IDs and managed recovery meet the recovery objective while retaining traceable reconciliation.'},{'residual_risk':risk,'technical_debt':'Two supported recovery paths require rehearsals','reversibility':'Drain retry queue and restore previous configuration before reverting traffic'},{'supersedes':[],'reason':'First recovery decision for this fictional service'}],
      'business-case':[{'requested_funding':capex,'currency':'EUR','sponsor':owner,'financial_owner':'Taylor Smith','decision_deadline':'2026-11-12'},options,cost,{'benefit_downside':{'reduction_fraction':uncertainty,'gross_benefit':gross*(1-uncertainty),'net_benefit':gross*(1-uncertainty)-horizon_cost},'six_month_delay':{'lost_benefit':benefit*.5,'net_benefit':gross-horizon_cost-benefit*.5},'interpretation':'Reconsider scope if delayed or reduced benefits do not justify total cost.'},{'measure':'Manual handling cost avoided','baseline_annual_eur':benefit,'target_annual_avoidance_eur':benefit,'owner':owner,'review':'quarterly','risk_ref':risk['id']}],
      'risk-assessment':[{'scope':scenario['scope'],'assets':entities,'risk_owner':owner},{'likelihood_scale':{'1':'rare','2':'unlikely','3':'possible','4':'likely','5':'frequent'},'impact_scale':{'1':'minor','2':'limited','3':'moderate','4':'major','5':'severe'},'calculation':'likelihood * impact','escalation_threshold':12,'authority':'Synthetic proposed method; not enterprise-approved'},[risk],[{'risk_ref':risk['id'],'inherent_score':12,'residual_score':8,'control_ref':prefix+'-C1','uncertainty':'Peak-load recovery not exercised'}],treatment],
      'assurance-report':[{'period':'2026-10-19','scope':scenario['scope'],'criteria':[prefix+'-REC1',prefix+'-INT1'],'exclusions':['Peak-load recovery']},{'assessor':'Independent QA reviewer Jordan Patel','method':'Inspect configuration and replay duplicate event IDs','sample_size':[10,100,1000][index],'limitation':'Synthetic sample only'},controls,[{'finding_ref':prefix+'-DEF1','criterion':prefix+'-REC1','significance':'material','observation':'Peak-load recovery was excluded from the rehearsal','owner':owner,'response':'Schedule load retest by 2026-11-05'}],{'conclusion':'Sampled integrity control met; full recovery assurance remains qualified','basis_refs':[prefix+'-EX1',prefix+'-EX2'],'execution_records':results,'limits':['Synthetic evidence','Peak workload excluded'],'approval_status':'pending'}],
      'architecture-definition':[{'scope':scenario['scope'],'stakeholders':[owner,'Warehouse or payment operations'],'baseline':'Manual restoration misses the recovery objective by 18 minutes'},[{'id':prefix+'-DRV1','driver':scenario['drivers'],'requirement_ref':prefix+'-REC1'}],[{'id':prefix+'-BUS','viewpoint':'business','description':'Service owner delivers reconciled transaction processing','element_refs':[prefix+'-OPS']},{'id':prefix+'-INFO','viewpoint':'information','description':'Ledger records immutable event IDs','element_refs':[prefix+'-DB']},{'id':prefix+'-APPS','viewpoint':'application','description':scenario['design'],'element_refs':[prefix+'-APP']},{'id':prefix+'-TECH','viewpoint':'technology','description':'Managed Linux runtime and PostgreSQL standby','element_refs':[prefix+'-APP',prefix+'-DB']}],interfaces,{'entities':entities,'target':'Managed recovery with durable event IDs','gaps':defects,'transition_owner':owner,'decision_ref':'TARGET'}],
      'hld':[{'boundary':scenario['scope'],'release':'candidate-1.0','external_dependency':'Approved identity provider'},[{'id':prefix+'-REC1','metric':'recovery_minutes','maximum':recovery},{'id':prefix+'-INT1','metric':'duplicate_committed_event_ids','maximum':0}],entities,interfaces,{'deployment':'Restore candidate configuration in isolated rehearsal; reconcile ledger before traffic switch','rollback':'Disable candidate traffic; retain previous primary; restore previous configuration only after queue drain','verification_refs':[r['id'] for r in results],'owner':owner}],
      'operational-handover':[{'service':scenario['name'],'owner':owner,'application_team':'Transaction engineering','platform_team':'Managed platform operations'},[{'criterion':c['criterion'],'result':c['result'],'evidence_ref':'SYN-01'} for c in controls],{'support_hours':['06:00-22:00','06:00-22:00','24x7'][index],'response_minutes':[30,15,5][index],'escalation_owner':owner,'access':'Approved identity group operations-recovery'},[{'id':prefix+'-RB1','version':'1.0','owner':owner,'purpose':'Recovery procedure'},{'id':prefix+'-CFG1','version':'candidate-1.0','owner':'Platform operations','purpose':'Configuration baseline'}],acceptance],
      'runbook':[{'trigger':'Incident commander confirms unavailable transaction API','incident_ref':prefix+'-INC1','operator':owner,'stop_condition':'Environment label differs from rehearsal target'},[{'tool':'kubectl','version':'1.31','context':prefix.lower()+'-rehearsal'},{'permission':'operations-recovery','credential_location':'Existing approved secret store; no credential content included'}],[{'step':1,'command':'kubectl --context '+prefix.lower()+'-rehearsal get deployment transaction-api','expected_output':'transaction-api 0/1 available','stop_on':'Unexpected deployment or environment'},{'step':2,'command':'kubectl --context '+prefix.lower()+'-rehearsal rollout undo deployment/transaction-api','expected_output':'deployment.apps/transaction-api rolled back','stop_on':'Rollback failed'},{'step':3,'command':'kubectl --context '+prefix.lower()+'-rehearsal rollout status deployment/transaction-api --timeout=120s','expected_output':'deployment "transaction-api" successfully rolled out','stop_on':'Timeout; do not enable traffic'}],{'rollback':'Keep external traffic disabled; preserve last consistent database checkpoint; incident commander approves any database restoration','escalation_owner':owner,'escalation_channel':'Incident bridge '+prefix+'-INC1','safe_state':'No new transaction traffic'}, {'rehearsal_date':'2026-10-19','environment':evidence['environment'],'evidence_ref':'SYN-01','next_review':'After deployment or dependency change','owner':owner}],
      'test-report':[{'requirements':[prefix+'-REC1',prefix+'-INT1'],'build':'candidate-1.0','period':'2026-10-19','exclusions':['Peak-load recovery']},evidence,results,defects,{'executed':2,'passed':2,'failed':0,'not_run':1,'requirement_coverage_fraction':2/3,'exit_status':'qualified-pending-retest','limits':['Synthetic evidence only','Peak-load recovery not demonstrated'],'signoff':acceptance}],
    }
    output={}
    for (field,datatype,_),value in zip(FAMILIES[family],records[family]):
        if isinstance(value,dict):value={**value,'knowledge_status':'synthetic-assumption','evidence_refs':['SYN-01']}
        else:value=[{**row,'knowledge_status':'synthetic-assumption','evidence_refs':['SYN-01']} for row in value]
        output[field]=value
    return output



def observe_variant(reference, variant):
    """Return observable rule IDs and review limitations for a seeded variant.

    reference and variant have the contracts accepted by apply_variant.
    This development harness recognises deliberately seeded defects and never
    establishes general semantic validity. Mutation exceptions propagate.
    """
    case=apply_variant(reference,variant);family=reference['document_kind'];units=case['semantic_units'];rules=[]
    required={item[0] for item in FAMILIES[family]}
    for field in sorted(required):
        value=units.get(field)
        if not value or isinstance(value,dict) and value.get('status')=='not_applicable':rules.append(f'{family}.{field}')
    if 'claims' in case and any(c['material'] and not c['evidence_refs'] for c in case['claims']):rules.append(f'{family}.unsupported_material_claim')
    if case.get('repeated_content'):rules.append(f'{family}.duplicate_claim')
    if case.get('irrelevant_annex'):rules.append(f'{family}.irrelevant_detail')
    if case['context'].get('processes_personal_data') is None:rules.append(f'{family}.privacy_analysis')
    regulatory=units.get('regulatory_analysis',{})
    if isinstance(regulatory,dict) and regulatory.get('status')=='waived' and not regulatory.get('authority_ref'):rules.append('global.authority_bypass')
    return {'rule_ids':sorted(rules),'semantic_review_required':True,'scope':'Seeded development-fixture observation only; not production validation.'}


def build():
    """Produce thirty references and deterministic mutation recipes with expectations."""
    result={}
    for family, definitions in FAMILIES.items():
        for complexity,scenario in SCENARIOS.items():
            units=populated_units(family,complexity,scenario)
            contract_id=next(key for key,value in BINDINGS.items() if value==family)
            units['identity']={'artifact_id':f'synthetic/{family}/{complexity}','owner':'Synthetic service owner','source_version':'1','intended_usage':'Development regression only; professional approval pending','knowledge_status':'synthetic-assumption'}
            if scenario['privacy']:
                units['privacy_analysis']={'description':'Transaction identifiers are pseudonymised; access is role-limited, retention is tied to the approved purpose and deletion is verified in rehearsal.','evidence_refs':['SYN-01'],'knowledge_status':'assumption'}
            if scenario['regulatory']:
                units['regulatory_analysis']={'description':'Data-location and transaction-retention obligations require competent jurisdictional interpretation; the fixture does not assert a legal exemption or real compliance approval.','evidence_refs':['SYN-01'],'knowledge_status':'pending'}
            first=definitions[0][0]
            variants=[
              {'id':'headings-only','operation':'headings_only','expected_rule_ids':[f'{family}.{x[0]}' for x in definitions],'expected_category':'critical-content'},
              {'id':'irrelevant','operation':'append_irrelevant','text':'A detailed history of office furniture procurement has no connection to the service decision or operational procedure.','expected_rule_ids':[f'{family}.irrelevant_detail'],'expected_category':'editorial'},
              {'id':'missing-core','operation':'remove','field':first,'expected_rule_ids':[f'{family}.{first}'],'expected_category':'critical-content'},
              {'id':'unsupported','operation':'unsupported_claim','text':'This design guarantees zero incidents forever; no observation or assumption supports this assertion.','expected_rule_ids':[f'{family}.unsupported_material_claim'],'expected_category':'critical-content'},
              {'id':'excessive','operation':'repeat','field':first,'count':200,'expected_rule_ids':[f'{family}.duplicate_claim'],'expected_category':'editorial','must_not_automatically_block':True},
              {'id':'invalid-na','operation':'mark_na','field':first,'reason':'The author omitted this unconditional obligation.','expected_rule_ids':[f'{family}.{first}'],'expected_category':'critical-content'},
              {'id':'unknown-applicability','operation':'unknown_context','field':'processes_personal_data','expected_rule_ids':[f'{family}.privacy_analysis'],'expected_category':'pending-applicability'},
              {'id':'regulatory-exception','operation':'unauthorised_exception','field':'regulatory_analysis','text':'The author claims that schedule pressure waives the applicable legal restriction.','expected_rule_ids':['global.authority_bypass'],'expected_category':'existing-mandatory-gate'},
              {'id':'valid-conditional-na','operation':'justified_conditional_na','field':'privacy_analysis','context':{'processes_personal_data':False},'justification':'Alternative synthetic scope explicitly excludes personal identifiers; SYN-NA documents anonymous stock counts only.','expected_rule_ids':[],'expected_category':'borderline-review'},
            ]
            document={'artifact_id':f'synthetic/{family}/{complexity}','contract_id':contract_id,'document_kind':family,'author':{'principal_id':'synthetic-author'},'title':f'{scenario["name"]}: {family}',
             'context':{'processes_personal_data':scenario['privacy'],'regulatory_requirement':scenario['regulatory']},
             'summary':scenario['scope']+' '+scenario['drivers']+' '+scenario['design'],
             'scenario':scenario,'semantic_units':units,
             'evidence':[{'id':'SYN-01','version':'1','classification':'synthetic','description':'Scenario assumptions and fabricated rehearsal observations for test development only; not real customer evidence.'}],
             'provenance':{'corpus_level':'synthetic-reference','calibration_status':'synthetic-only','human_approval_ref':None},
             'reference_expectation':{'required_units_present':True,'independent_semantic_review_required':True,'production_pass_claim':False},'variants':variants}
            result[ROOT/f'.ai/runtime/evals/content_quality/{family}-{complexity}.json']=document
    groups={'valid':[], 'invalid':[], 'borderline':[]}
    for case_path,case in list(result.items()):
        reference=str(case_path.relative_to(ROOT/'.ai/runtime'))
        groups['valid'].append({'case_ref':reference,'variant_id':None,'role':'synthetic-reference; professional review pending'})
        for variant in case['variants']:
            category='borderline' if variant['id'] in ['excessive','unknown-applicability','valid-conditional-na'] else 'invalid'
            groups[category].append({'case_ref':reference,'variant_id':variant['id'],'expected_category':variant['expected_category']})
    for category,entries in groups.items():
        result[ROOT/f'.ai/runtime/content/fixtures/{category}/index.json']={'schema_version':'1.0.0','category':category,'authority':'Navigation only; canonical examples remain in evals/content_quality.','calibration_status':'synthetic-only','entries':entries}
    result[ROOT/'.ai/runtime/evals/content_quality/manifest.json']={'schema_version':'1.0.0','corpus_level':'synthetic-reference','calibration_status':'synthetic-only','human_gold':False,'professional_approval_ref':None,'reference_count':30,'variants_per_reference':9,'cases':[str(p.relative_to(ROOT/'.ai/runtime')) for p in result if p.parent.name=='content_quality'], 'evaluation_limit':'Mutation integrity and predicate tests support development; no automatic professional or production acceptance.'}
    return result


def main():
    """Write fixtures or check that committed fixtures match the authored definitions."""
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true');args=parser.parse_args();errors=[]
    for path,document in build().items():
        text=json.dumps(document,indent=2)+'\n'
        if args.check:
            if not path.exists() or path.read_text()!=text:errors.append(str(path))
        else:path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text)
    if errors:raise SystemExit('Corpus drift: '+', '.join(errors))
    print('Synthetic corpus is reproducible.' if args.check else 'Generated synthetic development corpus.')

if __name__=='__main__':main()
