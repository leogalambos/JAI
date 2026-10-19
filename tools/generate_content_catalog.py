#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Reproduce the proposed DCS foundation from explicit authored family definitions.

The role catalogue remains authoritative. This generator never infers a production
kind from a name: the reviewed mapping below is the only priority classification.
Other contracts receive source-attributed proposals with inherited modality/domain
obligations; authored completeness never means independent professional approval.
"""
from pathlib import Path
import hashlib
import json
import argparse
import importlib.util
from content_catalog_definitions import (TYPE_REQUIREMENTS, DOMAIN_REQUIREMENTS,
    TYPE_DOMAINS, SABSA_REQUIREMENTS, ARCHETYPE_REQUIREMENTS)

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / '.ai/runtime'
CONTENT = RUNTIME / 'content'
# Reviewed actual contract identifiers; legacy types are deliberately preserved.
BINDINGS = {
 'enterprise-applications-architect:2': 'decision-paper',
 'enterprise-architect:4': 'adr',
 'it-financial-management-tbm-manager:2': 'business-case',
 'it-risk-manager:2': 'risk-assessment',
 'secure-delivery-devsecops-architect:3': 'assurance-report',
 'enterprise-architect:1': 'architecture-definition',
 'solution-architect:1': 'hld',
 'implementation-consultant:3': 'operational-handover',
 'linux-systems-administrator:4': 'runbook',
 'test-analyst:2': 'test-report',
}
# Each entry records substantive information, its type and why the reader needs it.
FAMILIES = {
 'decision-paper': [
 ('decision_request','object','Identify the question, accountable authority, decision deadline and permitted outcomes.'),
 ('baseline','object','Explain the evidenced problem and the consequences of taking no action.'),
 ('options','array','Compare at least two feasible options including the baseline using consistent criteria.'),
 ('tradeoffs','object','Explain comparative cost, benefit, dependencies, uncertainty and residual risk.'),
 ('recommendation','object','Identify the proposed choice and link its rationale to the comparative evaluation.')],
 'adr': [
 ('decision_context','object','Identify the architecture concern, constraints, scope and decision status.'),
 ('architecture_options','array','Compare feasible design alternatives and the rejected baseline against drivers.'),
 ('architecture_choice','object','Record the selected design, decision owner and dated rationale.'),
 ('consequences','object','Describe technical debt, reversibility, operational impacts and residual risks.'),
 ('supersession','object','Record predecessor links or explicitly state that no decision is superseded.')],
 'business-case': [
 ('investment_request','object','Identify the investment decision, sponsor, financial owner and funding boundary.'),
 ('investment_options','array','Compare the no-investment baseline and feasible investment options.'),
 ('financial_model','object','Provide dated currency, horizon, TCO, cash flows and non-overlapping benefit assumptions.'),
 ('sensitivity','object','Show how uncertain cost, adoption and benefit assumptions affect the recommendation.'),
 ('benefit_realisation','object','Assign benefit measures, baselines, owners, review dates and residual investment risks.')],
 'risk-assessment': [
 ('assessment_scope','object','Identify assets, business outcomes, boundaries and accountable risk owners.'),
 ('scoring_method','object','Define likelihood, impact, evaluation scales and the applicable risk appetite.'),
 ('risk_scenarios','array','Describe causes, events, consequences and the evidence behind each scenario.'),
 ('risk_evaluation','array','Link inherent and residual scores to scenarios, control effectiveness and uncertainty.'),
 ('risk_treatment','array','Assign response actions, owners, deadlines and residual-risk acceptance authority.')],
 'assurance-report': [
 ('assurance_scope','object','Define assurance objectives, applicable criteria, period and exclusions.'),
 ('assurance_method','object','Identify independent assessor, sampling approach, limitations and evidence collection method.'),
 ('control_tests','array','Link each tested criterion to procedure, evidence, sample and observed outcome.'),
 ('assurance_findings','array','Record located deviations, significance, management response and corrective owners.'),
 ('assurance_conclusion','object','Bound the assurance conclusion by tested scope, evidence and remaining uncertainty.')],
 'architecture-definition': [
 ('architecture_context','object','Define the enterprise concern, stakeholders, system boundary and current baseline.'),
 ('architecture_drivers','array','Trace business drivers, principles and measurable quality requirements to sources.'),
 ('architecture_viewpoints','array','Describe business, information, application and technology views with stable element links.'),
 ('architecture_relations','array','Define cross-view relationships, interfaces, trust boundaries and integrity constraints.'),
 ('architecture_evolution','object','Explain target gaps, architectural decisions, operational implications and transition dependencies.')],
 'hld': [
 ('solution_scope','object','Define the proposed implementation boundary, use cases and external dependencies.'),
 ('quality_requirements','array','State measurable availability, performance, security and operational acceptance targets.'),
 ('solution_components','array','Describe component responsibilities, deployment topology and design rationale.'),
 ('solution_interfaces','array','Specify integration contracts, data flows, trust boundaries and failure behaviour.'),
 ('delivery_strategy','object','Describe deployment, migration, operability, rollback and design verification.')],
 'operational-handover': [
 ('service_boundary','object','Define the service, service owner, support teams, assets and responsibility boundaries.'),
 ('readiness_evidence','array','Link monitoring, backup, recovery, capacity and security readiness criteria to observed evidence.'),
 ('support_arrangements','object','Specify support hours, contacts, escalation paths, service levels and access prerequisites.'),
 ('handover_inventory','array','Identify versioned runbooks, configuration, known errors, training and dependency records.'),
 ('acceptance_decision','object','Record receiving operations acceptance, unresolved risks, action owners and authority status.')],
 'runbook': [
 ('operational_trigger','object','State the trigger, permitted operators, service boundary and stop conditions.'),
 ('prerequisites','array','Identify access permissions, tools, versions, dependencies and safety checks without embedding secrets.'),
 ('procedure_steps','array','Give ordered actions, exact targets, expected outputs and verification at each critical step.'),
 ('failure_recovery','object','Specify failure detection, rollback, safe state and conditions requiring escalation.'),
 ('operational_validation','object','Record last rehearsal environment, evidence, owner and next review trigger.')],
 'test-report': [
 ('test_scope','object','Identify tested requirements, exclusions, build versions and the reporting period.'),
 ('test_environment','object','Record environment, data constraints, tools and reproducible execution configuration.'),
 ('execution_results','array','Link test cases and requirement IDs to execution timestamps, actual outcomes and evidence.'),
 ('defect_analysis','array','Record unresolved defects, severity, retest state and their impact on acceptance.'),
 ('test_conclusion','object','Compare achieved coverage with exit criteria and explain limitations and residual release risk.')],
}
DECISIONS = {
 'decision-paper':'Choose an application platform and rationalisation option against explicit evaluation criteria.',
 'adr':'Accept or reject an architectural design choice and its documented consequences.',
 'business-case':'Approve, defer or reject the proposed technology investment and benefit accountability.',
 'risk-assessment':'Select treatments and decide whether residual change risks are acceptable.',
 'assurance-report':'Determine whether delivery controls provide sufficient evidenced assurance for the stated scope.',
 'architecture-definition':'Accept the architecture baseline and prioritise documented architecture gaps.',
 'hld':'Accept the proposed solution design as the basis for detailed engineering.',
 'operational-handover':'Accept service responsibility or require remediation before operational transfer.',
 'runbook':'Determine whether an authorised operator can safely execute the recovery procedure.',
 'test-report':'Determine whether tested requirements satisfy exit criteria and residual defects permit progression.',
}

def canonical(value):
    """Return canonical UTF-8 JSON bytes for JSON-compatible ``value``.

    Raises TypeError if value cannot be represented as JSON.
    """
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()


def unit(kind, name, datatype, reason, obligation='MUST', when=None):
    """Return a typed attributable information-obligation dictionary.

    kind and name identify the rule; datatype names its JSON value type.
    reason states its justification, obligation sets its strength and optional
    when supplies the structured applicability predicate. Inputs are authored
    catalogue data; this helper does not validate professional correctness.
    """
    value = {'id':f'{kind}.{name}', 'semantic_fields':[name], 'datatype':datatype,
      'obligation':obligation, 'acceptance_predicate':{'op':'review'},
      'acceptance_criteria':[reason,'A title alone is insufficient; values must identify concrete entities, relations and limitations.'],
      'evidence_policy':{'material_claims':'versioned source reference or explicitly labelled assumption', 'unknown':'retain pending status and identify owner; never fabricate', 'knowledge_statuses':['known','assumption','unknown','pending']},
      'rationale':{'basis':'professional-proposal','reason':reason,'source_refs':['artifacts/contracts/role-deliverables.v3.json','content/rules/global-invariants.yaml']},
      'provenance':{'origin':'AI-derived professional proposal','normative_claim':False}, 'jai_layer':'L2'}
    if when: value['when']=when
    return value


def spec(identifier, category, purpose, completeness='skeleton', inherits=None):
    """Return common lifecycle, approval and uncertainty metadata.

    identifier and category locate the specification; purpose states its use.
    completeness marks authored coverage and inherits lists parent IDs.
    Defaults deliberately preserve proposed status and pending human approval.
    """
    return {'license':'SPDX-License-Identifier: BSD-4-Clause','copyright':'Copyright (c) 2026 Leo Galambos and the Egothor team','id':identifier,'version':'1.1.0','owner':'Content Standards Owner','status':'proposed',
      'effective_from':None,'category':category,'completeness':completeness,'inherits':inherits or [],
      'applies_to':{},'purpose':purpose,'target_audience':['competent independent domain reviewer'],
      'decisions_supported':[],'intended_usage':'26.10.8 advisory content contract; professional approval pending',
      'non_goals':['Replace JAI authority','Claim a professional framework requirement without a cited source'],
      'required_information':[],'conditional_information':[],'optional_information':[],
      'forbidden_information':[],'low_value_information':[],
      'size_budget':{'metric':'semantic_units','calibration_basis':'Modality-specific information coverage; numerical envelopes require approved enterprise calibration.','minimum_is_quality_gate':False,'calibration_status':'synthetic-only','allowance_rules':['Document complexity and audience need; excess requires review, not automatic rejection.'],'annex_rules':['Reference canonical detail rather than repeat it.']},
      'sources':{'evidence_grade':'AI-derived proposal','provenance':['Approved implementation direction; content specifics remain proposed.'],'freshness':'review on source or policy change','claim_to_evidence_rules':['Material claims reference dated, versioned evidence or explicit uncertainty.']},
      'overlap':{'excluded_content':['Unrelated material'],'deduplication_rules':['Reference canonical claims by stable ID.'],'canonical_reference_rules':['Preserve source version and hash.']},
      'runtime':{'validators':['content_spec.py lint-registry'],'judge_rubric':['Evaluate actual meaning, applicability, evidence and contradictions.'],'gate':'advisory','reviewer_class':'independent competent domain reviewer','waiver_policy':'Existing JAI L0 authority only; no legal/security bypass.'},
      'lifecycle':{'effective_version':'1.1.0','deprecation':None,'migration':'26.10.5 explicit sidecar binding','golden_case_refs':[],'change_history':['Initial proposed foundation; no professional approval asserted.']},
      'jai':{'L1':'purpose, audience and decision_supported','L2':'typed semantic information units','L3':'global invariants, precedence and acceptance','L4':'content blueprint and profile reference','L5':'canonical artifact source; existing producer','L6':'evidence and independent review; existing fabric authority references','L0':'Human professional approval through existing JAI authority acts; never AI self-approval'},
      'approval':{'status':'pending','authority_ref':None,'independent_of_author':True,'mechanism':'Existing JAI L0 / fabric authority process'},'calibration_status':'synthetic-only'}


def modality(artifact_type):
    """Return the authored size modality for a registered artifact type.

    Args:
        artifact_type: Explicit legacy artifact type, never a guessed title.
    Returns:
        Schema-supported metric; data/configuration outputs avoid prose budgets.
    """
    if artifact_type in ('register','catalogue','dataset','dashboard'):
        return 'rows'
    if artifact_type in ('diagram','model'):
        return 'elements'
    if artifact_type in ('configuration-baseline','prototype','implementation-specification'):
        return 'typed'
    if artifact_type=='presentation':
        return 'slides'
    return 'semantic_units'


def complete_policy(value, prefix):
    """Populate proposed contextual, optional, forbidden and evidence obligations.

    Args:
        value: Mutable authored policy receiving the shared control obligations.
        prefix: Stable rule namespace identifying this policy.
    Returns:
        None; modifies only the supplied policy without granting approval.
    """
    value['conditional_information']=[unit(prefix,'privacy_analysis','object','Identify in-scope personal-data flows, minimisation, authorised handling and competent review evidence.','CONDITIONAL',{'field':'processes_personal_data','op':'eq','value':True}),unit(prefix,'regulatory_analysis','object','Identify applicable obligation IDs, interpretation authority, compliance evidence and unresolved gaps.','CONDITIONAL',{'field':'regulatory_requirement','op':'eq','value':True})]
    value['optional_information']=[unit(prefix,'supporting_annex','object','Include versioned calculations, logs or technical detail only when linked to a specific required claim.','MAY')]
    value['forbidden_information']=[unit(prefix,'unsupported_material_claim','object','Do not assert material conclusions without dated evidence or an explicitly labelled assumption.','MUST NOT')|{'category':'critical-content','severity':'critical'}]
    value['low_value_information']=[unit(prefix,'irrelevant_detail','object','Remove material unrelated to the stated purpose, required input analysis or receiving-role action.','SHOULD NOT')|{'category':'editorial','severity':'minor'}]
    value['applicability_policy']={'unconditional_units':'N/A prohibited','conditional_units':'N/A requires evidenced false applicability and review; unknown remains pending'}
    value['completion_scope']='Authored proposed contract only; evaluated and human-approved coverage must be reported separately.'
    value['lifecycle']['change_history'].append('26.10.8 substantive proposed obligations; no professional approval asserted.')


def contract_units(contract, kind, source):
    """Derive traceable proposed units from one exact unchanged role contract.

    Args:
        contract: Canonical Artifact Contract v3 object with explicit ID and inputs.
        kind: Registered contract-specific kind, not a classifier output.
        source: Exact parsed source role deliverable and gate declarations.
    Returns:
        Typed units requiring analysis of actual inputs and receiving-role needs.
        Copied legacy decision text is explicitly retained as migration debt.
    """
    jai=contract['jai'];cid=contract['id']
    result=[unit(kind,'delivery_scope','object',f"Identify the subject entities, boundaries, outcomes and versioned sources for: {jai['intent']['purpose']}"),unit(kind,'receiving_acceptance','array',f"For each receiving role ({'; '.join(jai['intent']['audience'])}), identify the concrete downstream use, requested action, acceptance measure and accountable recipient."),unit(kind,'contract_relations','array',f"Identify actual entity IDs and relationship instances for: {'; '.join(jai['semantics']['required_relations'])}."),unit(kind,'decision_purpose_correction','object','State the specific choice enabled, alternatives and competent decision authority, or explain why this output supports no decision; copied acceptance boilerplate is not a decision purpose.')]
    delivery=source['deliverable']
    verification=unit(kind,'delivery_verification','array',f"For the specific output '{delivery['name']}', provide verifiable evidence satisfying: {delivery['acceptance_criterion']}. Required delivery form: {delivery['format']}.")
    verification['source_deliverable']={'name':delivery['name'],'format':delivery['format'],'acceptance_criterion':delivery['acceptance_criterion'],'role_path':source['role']['path']}
    gate=unit(kind,'role_gate_observations','array','Evaluate every applicable existing role gate using actual evidence and identified residual gaps; do not infer PASS from headings or DCS advisory status.')
    gate['acceptance_criteria'] += [row['id']+': '+row['criterion'] for row in source['gates']]
    gate['source_role_gate_refs']=[source['role']['path']+'#'+row['id'] for row in source['gates']]
    result += [verification,gate]
    for index,input_name in enumerate(jai['semantics']['required_inputs'],1):
        item=unit(kind,f'contract_input_{index}','object',f'Analyse the specific input "{input_name}" for this deliverable: identify its version, relevant entities/values, constraints, implications and unresolved evidence gaps.')
        item['source_input']={'contract_id':cid,'json_pointer':f'/jai/semantics/required_inputs/{index-1}','value':input_name}
        result.append(item)
    for item in result:
        item['rationale']['source_refs']=[f'artifacts/contracts/role-deliverables.v3.json#{cid}', 'content/types/'+jai['semantics']['artifact_type']+'.yaml']
    return result


def build():
    """Return every reproducible catalogue file without mutating canonical contracts."""
    files={}
    registry={'schema_version':'1.0.0','version':'26.10.8','status':'proposed','calibration_status':'synthetic-only','specifications':[],
      'document_kinds':[],'mappings':{'artifact_types':{},'archetypes':{},'sabsa_views':{},'domains':{}},
      'context_fields':{'processes_personal_data':{'type':'boolean'},'regulatory_requirement':{'type':'boolean'}},
      'priority_document_kinds':list(FAMILIES),'binding_map_ref':'migrations/26.10.5-binding-map.json'}
    def add(value,path):
        files[CONTENT/path]=value
        registry['specifications'].append({k:value[k] for k in ['id','version','category','status','completeness']}|{'path':path})
    glob=spec('global/invariants','global','Preserve evidence, privacy, authority and explicit uncertainty.')
    glob['forbidden_information']=[unit('global',name,'object',reason,'MUST NOT')|{'category':'security-policy' if name=='secret_disclosure' else 'existing-mandatory-gate','severity':'critical'} for name,reason in [
      ('secret_disclosure','Never disclose credentials, restricted personal information or information outside the authorised classification boundary.'),
      ('fabricated_evidence','Do not invent observations, claim unsupported certainty or present synthetic examples as human-approved gold.'),
      ('authority_bypass','Never replace existing JAI human approval or weaken security, evidence and authorisation gates.')]]
    glob['precedence']=['applicable law and classification','binding customer/organisational requirements','approved internal methods','applicable professional frameworks','existing JAI contracts','AI-derived professional proposals']
    glob['conflict_policy']='SPEC_CONFLICT: lower precedence may strengthen but cannot silently weaken applicable obligations.'
    add(glob,'rules/global-invariants.yaml')
    types=json.loads((RUNTIME/'artifacts/schema/artifact-types.json').read_text())['artifact_types']
    for name in types:
        value=spec('type/'+name,'type',f'Common typed foundation for {name}; no substitute for a substantive document kind.','complete',inherits=['global/invariants'])
        value['applies_to']={'artifact_types':[name]}
        value['required_information']=[unit('type/'+name,'identity','object','Identify stable artifact ID, owner, source version and intended usage.')]+[unit('type/'+name,*entry) for entry in TYPE_REQUIREMENTS[name]]
        complete_policy(value, 'type/'+name)
        value['size_budget']['metric']=modality(name)
        value['coverage_note']='Authored proposed modality policy; professional approval and evaluated coverage are separate.'
        registry['mappings']['artifact_types'][name]=value['id'];add(value,f'types/{name}.yaml')
    for name, obligations in DOMAIN_REQUIREMENTS.items():
        value=spec('domain/'+name,'domain',f'Professional {name} obligations supplement the explicitly bound artifact contract.','complete')
        value['applies_to']={'artifact_types':[key for key,domain in TYPE_DOMAINS.items() if domain==name]}
        value['required_information']=[unit('domain/'+name,*entry) for entry in obligations]
        complete_policy(value,'domain/'+name)
        registry['mappings']['domains'][name]=value['id'];add(value,f'domain/{name}.yaml')
    contracts=json.loads((RUNTIME/'artifacts/contracts/role-deliverables.v3.json').read_text())['contracts']
    role_module=importlib.util.spec_from_file_location('catalog_role_sources',RUNTIME/'tools/artifacts.py')
    role_sources=importlib.util.module_from_spec(role_module);role_module.loader.exec_module(role_sources)
    roles=json.loads((RUNTIME/'roles.json').read_text())['roles']
    live=role_sources.live_deliverables({'skills':ROOT/'.ai/skills'},roles)
    for family, obligations in FAMILIES.items():
        legacy=sorted({c['jai']['semantics']['artifact_type'] for c in contracts if BINDINGS.get(c['id'])==family})
        value=spec('kind/'+family,'document_kind',DECISIONS[family],'complete',[])
        value['applies_to']={'document_kind':family,'artifact_types':legacy}
        value['decisions_supported']=[DECISIONS[family]]
        value['required_information']=[unit(family,*o) for o in obligations]
        value['conditional_information']=[unit(family,'privacy_analysis','object','Identify personal-data flows, lawful handling constraints, minimisation and review evidence.','CONDITIONAL',{'field':'processes_personal_data','op':'eq','value':True}),unit(family,'regulatory_analysis','object','Trace each applicable regulatory obligation to scope, evidence and competent interpretation; exceptions cannot waive law.','CONDITIONAL',{'field':'regulatory_requirement','op':'eq','value':True})]
        value['optional_information']=[unit(family,'technical_annex','object','Include deeper calculations or technical detail only when linked to a reader need.','MAY')]
        value['forbidden_information']=[unit(family,'unsupported_material_claim','object','Never state a material conclusion as established without evidence or explicit uncertainty.','MUST NOT')|{'category':'critical-content','severity':'critical'}]
        value['low_value_information']=[unit(family,'irrelevant_detail','object','Remove detail that does not support the stated purpose or a referenced annex.','SHOULD NOT')|{'category':'editorial','severity':'minor'},unit(family,'duplicate_claim','object','Reference an existing claim instead of repeating it without new analytical value.','SHOULD NOT')|{'category':'editorial','severity':'minor'}]
        value['applicability_policy']={'unconditional_units':'N/A prohibited','conditional_units':'N/A requires context evidence, reviewer-visible justification and condition=false; unknown condition remains pending','unknown_context':'Do not silently assume false; request evidence or retain pending review.'}
        budgets={'decision-paper':(3,6,8),'adr':(3,6,8),'business-case':(6,12,16),'risk-assessment':(4,12,16),'assurance-report':(4,12,16),'architecture-definition':(10,30,40),'hld':(10,30,40),'operational-handover':(4,12,16),'runbook':(2,10,14),'test-report':(3,10,14)}
        lower,upper,soft=budgets[family]
        value['size_budget'].update(metric='pages',target=[lower,upper],soft_max=soft,basis='Indicative pilot intervals from approved implementation direction; assurance and handover use proposed evidence-pack intervals requiring calibration.',exclude=['controlled_annexes','source_register'],target_is_informational=True)
        value['lifecycle']['golden_case_refs']=[f'evals/content_quality/{family}-{c}.json' for c in ['simple','medium','complex']]
        value['completion_scope']='Authored information contract and synthetic fixtures only; proposed and not production-qualified.'
        registry['document_kinds'].append({'id':family,'artifact_types':legacy,'spec_ref':value['id'],'completeness':'complete','status':'proposed'})
        add(value,f'document_kinds/{family}.yaml')
    bindings=[]
    for c in contracts:
        cid=c['id'];legacy=c['jai']['semantics']['artifact_type'];kind=BINDINGS.get(cid,'role/'+cid)
        if cid not in BINDINGS:
            value=spec('kind/'+kind,'document_kind',c['jai']['intent']['purpose'],'complete',inherits=['type/'+legacy,'domain/'+TYPE_DOMAINS[legacy]])
            value['applies_to']={'document_kind':kind,'artifact_types':[legacy]}
            value['target_audience']=c['jai']['intent']['audience']
            value['required_information']=contract_units(c,kind,live[cid])
            complete_policy(value,kind)
            value['size_budget']['metric']=modality(legacy)
            value['decisions_supported']=['Determine whether the specific deliverable is fit for its explicit receiving-role use; competent domain confirmation remains pending.']
            value['coverage_note']='Source-attributed contract-specific proposal plus modality/domain obligations; original copied decision purpose remains a mandatory migration review item.'
            value['source_contract']={'id':cid,'source_fingerprint':c['source_fingerprint'],'source_hash':hashlib.sha256(canonical(c)).hexdigest()}
            value['derivation_limits']=['Source inputs identify the subject boundary but do not prove professional sufficiency.','Independent semantic assessment and human L0 approval remain pending.']
            registry['document_kinds'].append({'id':kind,'artifact_types':[legacy],'spec_ref':value['id'],'completeness':'complete','status':'proposed'})
            add(value,f'document_kinds/roles/{cid.replace(":","-")}.yaml')
        purpose=DECISIONS.get(kind)
        bindings.append({'artifact_id':cid,'artifact_type':legacy,'document_kind':kind,'content_spec_ref':'kind/'+kind,'overlays':[],
          'source_id':cid,'source_fingerprint':c['source_fingerprint'],'source_hash':hashlib.sha256(canonical(c)).hexdigest(),
          'decision_supported_copy_detected':True,'decision_supported':{'status':'mapped' if purpose else 'pending-correction','value':purpose,'reason':'Explicitly reviewed priority decision purpose.' if purpose else 'Legacy acceptance text is not a decision purpose; requires contract-specific domain review.'},
          'jai_extension':{'semantics.content_spec_ref':'kind/'+kind,'design.content_profile_ref':'kind/'+kind,'justification.content_acceptance_ref':'kind/'+kind},
          'classification_basis':'Reviewed explicit contract ID; original artifact type preserved.' if purpose else 'Unique explicit legacy contract binding; no name inference.'})
    files[CONTENT/'migrations/26.10.5-binding-map.json']={'schema_version':'1.0.0','source_release':'26.10.5','source_ref':'artifacts/contracts/role-deliverables.v3.json','canonical_contracts_unchanged':True,'bindings':bindings}
    for path in sorted((RUNTIME/'publication/archetypes').glob('*.json')):
        original=json.loads(path.read_text());name=path.stem
        value=spec('archetype/'+name,'archetype',f'Audience and presentation overlay for {name}.','complete')
        value['applies_to']={'publication_archetype':name};value['source_ref']=str(path.relative_to(RUNTIME))
        field,reason=ARCHETYPE_REQUIREMENTS[name]
        value['required_information']=[unit('archetype/'+name,field,'object',reason)]
        complete_policy(value,'archetype/'+name)
        value['target_audience']=original['audience']
        value['presentation_obligations']={'source_profile':original,'preserve_required_information':True,'no_obligation_weakening':True}
        registry['mappings']['archetypes'][name]=value['id'];add(value,f'archetypes/{name}.yaml')
    views=json.loads((RUNTIME/'sabsa/schema/documents.json').read_text())['views']
    for name, original in views.items():
        value=spec('sabsa/'+name,'sabsa',original['purpose'],'complete');value['applies_to']={'sabsa_view':name}
        value['target_audience']=[original['audience']];value['required_information']=[unit('sabsa/'+name,'business_traceability','array','Trace selected security elements to business drivers, measurable attributes and source model IDs.'),unit('sabsa/'+name,'matrix_coverage','array','Account for all 36 SABSA cells through selected source elements or explicit applicability reasons; never invent missing architecture facts.')]
        value['required_information'] += [unit('sabsa/'+name,*entry) for entry in SABSA_REQUIREMENTS[name]]
        complete_policy(value,'sabsa/'+name)
        value['size_budget']['metric']='elements'
        value['coverage_note']='Authored view-specific proposal; all 36 cells require evidenced applicability, not invented facts.'
        if name=='risk-treatment-plan':
            value['inherits']=['kind/risk-assessment','domain/security']
        registry['mappings']['sabsa_views'][name]=value['id'];add(value,f'sabsa/{name}.yaml')
    files[CONTENT/'registry.json']=registry
    return files


def main():
    """Write generated foundation files, or fail if the checked-in projection drifts."""
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true');args=parser.parse_args()
    errors=[]
    for path,value in build().items():
        encoded=json.dumps(value,indent=2,ensure_ascii=False)+'\n'
        if args.check:
            if not path.exists() or path.read_text()!=encoded: errors.append(str(path.relative_to(ROOT)))
        else:
            path.parent.mkdir(parents=True,exist_ok=True);path.write_text(encoded)
    if errors: raise SystemExit('Generated catalogue drift: '+', '.join(errors))
    print('DCS catalogue is reproducible.' if args.check else 'Generated proposed DCS catalogue.')

if __name__=='__main__':main()
