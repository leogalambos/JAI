#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Generate reproducible synthetic DCS development examples, never human gold.

Variants are explicit mutations with expected rule IDs and observable defects.
These fixtures qualify the foundation test harness, not production content QA.
"""
import argparse
import hashlib
import sys
import copy
import json
from pathlib import Path
from generate_content_catalog import BINDINGS, FAMILIES, ROOT

sys.path.insert(0, str(ROOT / '.ai/runtime/tools'))
from content_mutations import apply_variant
from content_spec import ContentSpec, canonical_hash

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



def compiled_case(resolver, contract_id, context, overlays=None):
    """Resolve explicit role identity and optionally strengthen registered overlays.

    Args:
        resolver: ContentSpec instance for the source catalogue.
        contract_id: Exact stable registered role contract identifier.
        context: Explicit typed applicability values.
        overlays: Optional registered strengthening overlay IDs.
    Returns:
        Compiled specification retaining the stable binding identity.
    Raises:
        ValueError: For missing bindings, unknown overlays or policy conflicts.
    """
    resolved = resolver.resolve(contract_id, context)
    if not overlays:
        return resolved
    binding = resolver.bindings[contract_id]
    selected = resolver.compile(binding['content_spec_ref'], context,
                                list(dict.fromkeys([*binding.get('overlays', []), *overlays])))
    for key in ('artifact_id', 'document_kind', 'spec_selection_reason', 'decision_supported'):
        selected[key] = copy.deepcopy(resolved[key])
    return selected


def synthetic_value(unit, scenario, field):
    """Create explicitly fictional data to exercise a typed information obligation.

    unit is a compiled obligation, scenario supplies bounded service assumptions,
    and field identifies the semantic location. Returns JSON-compatible data;
    this tests shape and defect detection, never professional adequacy.
    """
    facts = {
        'design': {'element_id': 'SYN-APP-1', 'responsibility': 'Accept transaction IDs and persist each committed event once', 'interface_ref': 'SYN-IF-1', 'deployment': 'Managed Linux service with PostgreSQL standby', 'failure_handling': 'Retry twice using the same event ID, then reject and alert', 'rollback': 'Drain retries and reconcile the ledger before restoring the previous configuration'},
        'options': {'baseline': {'id': 'BASE', 'restore_minutes': 48, 'transition_eur': 0}, 'candidate': {'id': 'TARGET', 'restore_minutes': 27, 'transition_eur': 18000}, 'criterion': 'Restore within 30 minutes with no duplicate committed event IDs', 'recommendation': 'Propose TARGET subject to peak-load rehearsal; BASE misses the recovery target'},
        'finance': {'currency': 'EUR', 'horizon_years': 1, 'transition': 18000, 'annual_operation': 6000, 'annual_avoided_manual_cost': 32000, 'net_benefit': 8000, 'benefit_downside_fraction': .25, 'downside_net_benefit': 0, 'double_counting_rule': 'Count avoided manual handling only, with no revenue uplift'},
        'risk': {'risk_id': 'SYN-R1', 'cause': 'Recovery checkpoint lags active transaction state', 'event': 'Replay duplicates a committed transaction', 'business_consequence': 'Ledger imbalance delays warehouse updates', 'inherent_score': 12, 'residual_score': 8, 'control_ref': 'SYN-C1', 'treatment': 'Enforce unique event IDs and rehearse ledger reconciliation', 'due': '2026-11-05', 'residual_authority': 'Independent service risk owner; approval pending'},
        'test': {'test_id': 'SYN-T1', 'requirement_ref': 'SYN-REC1', 'build': 'candidate-1.0', 'environment': 'Isolated recovery rehearsal', 'procedure': 'Restore service and submit the same event ID twice; compare durable ledger totals', 'expected_max_minutes': 30, 'observed_minutes': 27, 'expected_duplicate_count': 0, 'observed_duplicate_count': 0, 'sample_size': 10, 'exclusions': ['Peak-load recovery'], 'disposition': 'Bounded synthetic result only; peak-load retest required before acceptance'},
        'operations': {'service_owner': 'Morgan Lee', 'support_team': 'Warehouse platform operations', 'support_hours': '06:00-22:00', 'incident_ref': 'SYN-INC1', 'step': 1, 'command': 'kubectl --context inv-rehearsal rollout status deployment/transaction-api --timeout=120s', 'expected_output': 'deployment transaction-api successfully rolled out', 'stop_condition': 'Environment differs from inv-rehearsal or reconciliation fails', 'safe_state': 'Keep new transaction traffic disabled', 'escalation': 'Incident commander on bridge SYN-INC1'},
        'schedule': {'increment_id': 'SYN-WAVE1', 'start': '2026-11-01', 'finish': '2026-11-05', 'dependency': 'SYN-T1 peak-load retest', 'entry': 'Backup restore rehearsed and rollback configuration retained', 'exit': 'Ledger totals reconcile and operations independently accepts support', 'go_no_go': 'Service owner with independent operations evidence', 'fallback_decision_time': 'Before enabling transaction traffic'},
        'schema': {'schema_version': '1.0', 'entity_id': 'SYN-APP-1', 'columns': [{'name': 'event_id', 'datatype': 'uuid', 'nullable': False}, {'name': 'amount', 'datatype': 'decimal(12,2)', 'unit': 'EUR', 'nullable': False}], 'key': 'event_id', 'record': {'event_id': 'SYN-EVENT-1', 'amount': 125.50}, 'uniqueness_observed': '10 of 10 event IDs unique', 'constraint': 'Every event references one existing service; no orphan event IDs observed in the fabricated sample'},
        'measurement': {'metric_id': 'SYN-M1', 'metric': 'recovery_minutes', 'unit': 'minutes', 'observed': 27, 'target_max': 30, 'sample_numerator': 1, 'sample_denominator': 1, 'period': '2026-10-19', 'source_query': 'rehearsal_end minus rehearsal_start, version 1', 'refresh': 'After each deployment and quarterly', 'interpretation': 'One synthetic rehearsal meets the target; peak-load confidence remains unknown'},
        'lineage': {'source_id': 'SYN-LEDGER-1', 'source_version': '1', 'extracted_at': '2026-10-19T10:00:00Z', 'transformation': 'Group committed records by event_id and compare counts before/after restore', 'input_records': 10, 'output_records': 10, 'classification': 'Synthetic non-customer data', 'retention': 'Delete rehearsal extracts after regression investigation closes', 'permitted_use': 'Development regression only'},
        'business': {'driver_id': 'SYN-DRV1', 'driver': 'Restore warehouse inventory updates within 30 minutes', 'attribute_id': 'SYN-ATTR1', 'attribute': 'Recoverable', 'measure': 'Recovery minutes', 'target_max': 30, 'objective_id': 'SYN-OBJ1', 'control_id': 'SYN-C1', 'service_id': 'SYN-SVC1', 'mechanism_id': 'SYN-MECH1', 'component_id': 'SYN-APP-1', 'source_model_version': 'synthetic-1', 'chain': 'SYN-DRV1 -> SYN-ATTR1 -> SYN-OBJ1 -> SYN-SVC1 -> SYN-MECH1 -> SYN-APP-1 -> SYN-M1'},
    }
    # This authored fixture mapping selects concrete fictional records. It is
    # not a production classifier and never infers a document kind from a title.
    groups = {
        'options': ('decision_record', 'design_alternatives', 'decision_consequences', 'decision_authority', 'option_comparison', 'decision_impacts', 'decision_reader_comparison', 'executive_reader_ask', 'executive_security_choices'),
        'finance': ('investment_boundary', 'investment_cashflows', 'investment_sensitivity', 'benefit_baselines', 'benefit_observations', 'benefit_disposition', 'benefits_reader_comparison'),
        'risk': ('risk_method', 'evaluated_scenarios', 'treatment_accountability', 'control_objectives', 'control_mechanisms', 'security_boundary', 'security_control_trace', 'sabsa_risk_treatments', 'sabsa_residual_acceptance', 'trust_domains', 'trust_relationships', 'risk_reader_exposure', 'governance_exceptions', 'compliance_gaps', 'compliance_gap_treatments'),
        'test': ('design_verification', 'assurance_criteria', 'assurance_observations', 'bounded_conclusion', 'control_effectiveness', 'implementation_acceptance', 'readiness_criteria', 'readiness_observations', 'readiness_disposition', 'test_risk_scope', 'test_approach', 'test_exit_criteria', 'tested_baseline', 'observed_test_results', 'test_release_constraints', 'test_requirement_trace', 'test_evidence_limits', 'prototype_hypothesis', 'prototype_reproduction', 'prototype_results', 'component_verification', 'attribute_assurance', 'assurance_schedule', 'review_disposition', 'audit_evidence_index'),
        'operations': ('execution_boundary', 'verified_steps', 'recovery_and_escalation', 'service_outcomes', 'service_levels', 'service_operating_model', 'operational_ownership', 'operational_recoverability', 'migration_recovery', 'cutover_reversal', 'operations_reader_acceptance'),
        'schedule': ('migration_inventory', 'migration_waves', 'cutover_schedule', 'cutover_decision_points', 'outcome_horizons', 'delivery_increments', 'roadmap_dependencies', 'delivery_accountability', 'delivery_dependencies', 'security_roadmap_items', 'security_roadmap_acceptance', 'transition_mappings', 'transition_controls', 'roadmap_reader_sequence', 'cutover_reader_decisions', 'implementation_reader_sequence', 'document_actions'),
        'schema': ('register_schema', 'register_records', 'register_integrity', 'dataset_schema', 'catalogue_schema', 'catalogue_entries', 'catalogue_integrity', 'diagram_elements', 'diagram_integrity', 'model_metamodel', 'model_entities', 'model_validation', 'baseline_targets', 'baseline_values', 'baseline_verification', 'implementation_parameters', 'architecture_lifecycle', 'lifecycle_transitions', 'reused_elements', 'reuse_dependencies'),
        'measurement': ('dashboard_measures', 'dashboard_values', 'dashboard_interpretation', 'presentation_ask', 'presentation_argument', 'presentation_navigation', 'security_service_measures', 'current_limitations', 'target_feasibility'),
        'lineage': ('dataset_lineage', 'dataset_quality', 'data_accountability', 'data_lineage_quality', 'architecture_source_trace', 'document_scope', 'document_analysis', 'framework_requirements', 'framework_architecture_links', 'confirmation_questions', 'confirmation_accountability', 'information_entities', 'privilege_profiles', 'policy_hierarchy', 'policy_enforcement'),
        'business': ('business_traceability', 'architecture_cells', 'architecture_chain', 'executive_business_attributes', 'logical_security_services', 'security_components', 'current_baseline', 'target_requirements', 'governance_decisions', 'architecture_reader_map'),
    }
    group = next((name for name, fields in groups.items() if field in fields), 'design')
    entry = {**copy.deepcopy(facts[group]),
             'record_id': 'SYN-' + field.upper().replace('_', '-')[:60],
             'service': scenario['name'], 'scope': scenario['scope'],
             'criterion_under_review': unit['acceptance_criteria'][0],
             'accountable_role': 'Synthetic receiving service owner',
             'evidence_refs': ['SYN-01'], 'knowledge_status': 'synthetic-assumption'}
    datatype = unit['datatype']
    if field.endswith('matrix_coverage'):
        return [dict(entry, row=row, column=column,
                     source_element_ref='SYN-ELEMENT-1',
                     applicability='selected',
                     rationale='Fictional recovery service demonstrates this cell; actual architecture facts remain subject to domain review.')
                for row in ('contextual', 'conceptual', 'logical', 'physical', 'component', 'operational')
                for column in ('what', 'why', 'how', 'who', 'where', 'when')]
    if datatype == 'array':
        return [entry]
    if datatype == 'object':
        return entry
    if datatype in ('string', 'reference'):
        return scenario['design'] + ' Synthetic bounded assumption; professional review pending.'
    if datatype in ('integer', 'number'):
        return 1
    if datatype == 'boolean':
        return False
    raise ValueError('Unsupported synthetic datatype: ' + datatype)


def enrich_case(document, compiled):
    """Populate missing inherited units without changing authored priority facts.

    document is mutated in place; compiled is its resolved registry blueprint.
    Only applicable required/conditional information is populated. Returns None.
    """
    for unit in compiled['blueprint']['semantic_units']:
        if unit['category'] not in ('required_information', 'conditional_information') or unit['applicability'] is False:
            continue
        for field in unit['semantic_fields']:
            if field not in document['semantic_units']:
                document['semantic_units'][field] = synthetic_value(unit, document['scenario'], field)


def enterprise_cases(resolver):
    """Build explicit-binding and overlay probes for the full proposed catalogue.

    resolver is the real registered content resolver. Returns canonical case
    paths mapped to synthetic data with positive, negative and borderline
    recipes. Every role kind is exercised; standalone registered kinds and
    overlays each have three complexity scenarios. Professional meaning remains an independent review obligation.
    """
    result = {}
    selections = [(cid, [], 'medium') for cid in sorted(resolver.bindings)
                  if cid not in BINDINGS]
    bound_kinds={row['document_kind'] for row in resolver.bindings.values()}
    selections.extend(('kind/'+kind,[],complexity)
                      for kind in sorted(set(resolver.kinds)-bound_kinds)
                      for complexity in SCENARIOS)
    anchor = 'enterprise-architect:1'
    for category in ('archetypes', 'sabsa_views'):
        for ref in sorted(resolver.registry['mappings'][category].values()):
            if isinstance(ref, dict):
                ref = ref['spec_ref']
            selections.extend((anchor, [ref], complexity) for complexity in SCENARIOS)
    for cid, overlays, complexity in selections:
        scenario = SCENARIOS[complexity]
        context = {'processes_personal_data': scenario['privacy'],
                   'regulatory_requirement': scenario['regulatory']}
        compiled = compiled_case(resolver, cid, context, overlays)
        slug = (overlays[0] if overlays else cid).replace('/', '-').replace(':', '-') + '-' + complexity
        document = {'artifact_id': 'synthetic/enterprise/' + slug,
                    'contract_id': cid, 'document_kind': compiled['document_kind'],
                    'author': {'principal_id': 'synthetic-author'},
                    'title': scenario['name'] + ': ' + slug,
                    'context': context, 'summary': scenario['scope'],
                    'scenario': copy.deepcopy(scenario), 'semantic_units': {},
                    'evaluation_selection': {'overlays': overlays},
                    'structural_probe': True,
                    'evaluation_scope': 'Typed contract/overlay detector probe; professional semantic adequacy is not established by these generated records.',
                    'evidence': [{'id': 'SYN-01', 'version': '1', 'classification': 'synthetic',
                                  'description': 'Fabricated recovery service records; no real customer evidence or human approval.'}],
                    'provenance': {'corpus_level': 'synthetic-reference',
                                   'calibration_status': 'synthetic-only', 'human_approval_ref': None},
                    'reference_expectation': {'independent_semantic_review_required': True,
                                              'production_pass_claim': False}}
        if cid in BINDINGS:
            document['semantic_units'].update(populated_units(BINDINGS[cid], complexity, scenario))
        enrich_case(document, compiled)
        required = [u for u in compiled['blueprint']['semantic_units']
                    if u['category'] == 'required_information']
        first = next((u for u in required if u['source_spec'] == compiled['spec_id']), required[0])
        field = first['semantic_fields'][0]
        # Expectations come from selected obligations; the production detector
        # never receives a recipe ID or uses these expectations as observations.
        document['variants'] = [
            {'id': 'headings-only', 'operation': 'headings_only',
             'expected_rule_ids': sorted(u['id'] for u in required), 'expected_category': 'critical-content'},
            {'id': 'missing-core', 'operation': 'remove', 'field': field,
             'expected_rule_ids': [first['id']], 'expected_category': 'critical-content'},
            {'id': 'invalid-na', 'operation': 'mark_na', 'field': field,
             'reason': 'Author omitted a required obligation without authority.',
             'expected_rule_ids': [first['id']], 'expected_category': 'critical-content'},
            {'id': 'unsupported', 'operation': 'unsupported_claim',
             'text': 'The recovery design guarantees permanent zero incidents without evidence.',
             'expected_rule_ids': [compiled['document_kind'] + '.unsupported_material_claim'], 'expected_category': 'critical-content'},
            {'id': 'irrelevant', 'operation': 'append_irrelevant',
             'text': 'The history of office furniture procurement does not support service recovery or the receiving decision.',
             'expected_rule_ids': [compiled['document_kind'] + '.irrelevant_detail'], 'expected_category': 'editorial'},
            {'id': 'unknown-applicability', 'operation': 'unknown_context', 'field': 'processes_personal_data',
             'expected_rule_ids': [compiled['document_kind'] + '.privacy_analysis'], 'expected_category': 'pending-applicability'},
            {'id': 'regulatory-exception', 'operation': 'unauthorised_exception', 'field': 'regulatory_analysis',
             'text': 'Schedule pressure is claimed to waive the applicable legal restriction without authority.',
             'expected_rule_ids': ['global.authority_bypass'], 'expected_category': 'existing-mandatory-gate'},
            {'id': 'valid-conditional-na', 'operation': 'justified_conditional_na', 'field': 'privacy_analysis',
             'context': {'processes_personal_data': False},
             'justification': 'Alternative synthetic scope excludes personal identifiers; SYN-NA records anonymous stock counts only.',
             'expected_rule_ids': [], 'expected_category': 'borderline-review'},
            {'id': 'excessive', 'operation': 'repeat', 'field': field, 'count': 5,
             'expected_rule_ids': [compiled['document_kind'] + '.duplicate_claim'],
             'expected_category': 'editorial', 'must_not_automatically_block': True},
        ]
        result[ROOT / '.ai/runtime/evals/content_quality/enterprise' / (slug + '.json')] = document
    return result


def build():
    """Produce thirty references and deterministic mutation recipes with expectations."""
    result={}
    resolver=ContentSpec(ROOT)
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
            enrich_case(document, resolver.resolve(contract_id, document['context']))
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
    enterprise = enterprise_cases(resolver)
    result.update(enterprise)
    manifest = result[ROOT/'.ai/runtime/evals/content_quality/manifest.json']
    manifest['enterprise_cases'] = [str(p.relative_to(ROOT/'.ai/runtime')) for p in enterprise]
    manifest['enterprise_reference_count'] = len(enterprise)
    manifest['enterprise_variants_per_reference'] = 9
    manifest['reference_count_scope'] = 'Legacy reference_count and cases identify the thirty priority examples; enterprise_cases are additional typed development probes.'
    manifest['total_reference_count'] = manifest['reference_count'] + len(enterprise)
    manifest['total_mutation_count'] = manifest['reference_count'] * manifest['variants_per_reference'] + sum(len(case['variants']) for case in enterprise.values())
    manifest['evaluation_limit'] += ' Enterprise probes test typed contract coverage; professional meaning remains pending independent domain review.'
    payload = {str(path.relative_to(ROOT / '.ai/runtime')):
               hashlib.sha256((json.dumps(document, indent=2) + '\n').encode()).hexdigest()
               for path, document in enterprise.items()}
    descriptor = {'schema_version': '1.0.0', 'package_kind': 'optional-extended-synthetic-evaluation',
                  'release': (ROOT / 'VERSION').read_text().strip(), 'files': payload,
                  'classification': 'public-synthetic', 'professional_approval': False}
    descriptor['payload_hash'] = canonical_hash(payload)
    result[ROOT / '.ai/runtime/content/evaluation-package.json'] = descriptor
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
