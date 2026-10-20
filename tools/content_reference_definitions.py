# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Authored proposed reference-kind obligations and explicit family mappings.

These public definitions describe professional information needs, not approval,
customer facts or executed evidence. Source Markdown anchors remain unchanged;
the generated sidecar maps their full HTML identifiers to registered DCS units.
"""

# Reference family: canonical kind, shared parents, source field -> rationale.
REFERENCE_KINDS = {
 'it-digital-strategy': ('strategy', ['family/strategy'], {
  'strategic_mandate':'Identify sponsor, business outcomes, planning horizon, authority and organisational boundary.',
  'current_capabilities':'Assess capability effectiveness, technical debt, service evidence and constraints against a dated baseline.',
  'target_portfolio':'Compare retain, modernise and replace options against common value, risk and cost criteria.',
  'investment_waves':'Sequence discovery and investment tranches with dependencies, capacity and irreversible commitment points.',
  'governance_measures':'Assign outcome measures, baselines, accountable owners and strategy review triggers.'}),
 'requirements-specification': ('requirements-specification', ['family/requirements-specification'], {
  'business_problem':'Describe actors, observable business problem, normal and exceptional scenarios and source evidence.',
  'functional_requirements':'State uniquely identified triggers, inputs, processing rules, outputs, exception behaviour and acceptance oracles.',
  'quality_constraints':'Quantify quality attributes, measurement windows, operating loads and applicable legal constraints without inventing applicability.',
  'traceability_priorities':'Trace requirements to sources, dependencies, priorities and conflict/change dispositions.',
  'acceptance_model':'Define measurable positive and negative acceptance cases, receiving authority and unresolved decisions.'}),
 'policy-standard': ('policy-standard', ['type/control-design'], {
  'policy_scope':'Identify issuing authority, scope, effective date, precedence and mandatory versus guidance statements.',
  'control_obligations':'Define accountable actors, required and prohibited behaviour, applicability and enforcement points.',
  'implementation_guidance':'Describe conforming implementation patterns and observable evidence without secrets or unsupported defaults.',
  'exceptions':'Define exception authority, risk basis, expiry and compensating controls without bypassing law or security.',
  'lifecycle':'Record authorised publication, supersession, review triggers and affected implementation migration.'}),
 'implementation-specification-lld': ('implementation-specification', ['type/implementation-specification'], {
  'implementation_scope':'Identify exact deployable boundary, approved design, environment baseline, owners and prerequisites.',
  'configuration_contract':'Specify typed configuration, interfaces, error handling, secrets references and least-privilege identities.',
  'deployment_sequence':'Order preflight, authorisation, rollout, data migration verification and safe recovery steps.',
  'technical_validation':'Define reproducible conformance, interface, failure-injection and authorisation-negative checks with expected observations.',
  'handover':'Identify versioned build artifacts, monitoring, recovery references, open defects and receiving operations responsibilities.'}),
 'migration-cutover-plan': ('migration-cutover-plan', ['type/migration-plan','type/cutover-plan'], {
  'migration_scope':'Identify source and target systems, data ownership, business boundaries, constraints and cut-off windows.',
  'mapping_reconciliation':'Define transformation, key/null/time semantics, rejected-record handling and quantitative reconciliation totals.',
  'cutover_schedule':'Assign ordered activities, prerequisites, operators, expected outputs and latest-safe go/no-go points.',
  'rollback_contingency':'Define points of no return, data recovery, replay or forward-fix branches and safe-state criteria.',
  'readiness_acceptance':'Identify rehearsal evidence, readiness disposition, stabilisation measures and accountable business acceptance.'}),
 'test-strategy-plan': ('test-strategy', ['type/test-strategy'], {
  'test_objectives':'Define critical business invariants, release risks, scope and the confidence tests can and cannot provide.',
  'levels_techniques':'Allocate test levels, design techniques and responsibilities against specific risks and interfaces.',
  'environment_data':'Define representative environments, deterministic data, workload, time controls and captured execution evidence.',
  'coverage_metrics':'Trace risks and requirements to cases and distinguish passed, failed, blocked and unexecuted coverage.',
  'execution_governance':'Define sequencing, staffing, triage, retest, blocking exit criteria and authorised deviation handling.'}),
 'operational-readiness-assessment': ('operational-readiness-assessment', ['type/operational-readiness-assessment'], {
  'operating_scope':'Identify service owners, consumers, support windows, criticality and emergency authority.',
  'technical_readiness':'Evaluate monitoring, identity, backup, demonstrated recovery, runbooks and on-call coverage with evidence.',
  'service_dependencies':'Map supplier and cross-service incident/change responsibilities and matching SLA/OLA boundaries.',
  'readiness_findings':'Locate readiness gaps, assess impact and assign remediation, risk owners and gate dispositions.',
  'go_live':'Separate readiness recommendation from deployment permission and define early-life support and exit measures.'}),
 'service-design-sla': ('service-design', ['type/service-design'], {
  'service_value':'Define consumers, service outcomes, eligibility, catalogue boundary and explicit exclusions.',
  'sli_slo':'Define service indicators, numerators, denominators, windows, exclusions and breach-handling measurements.',
  'support_operating_model':'Assign support tiers, incident/problem ownership, escalation, monitoring and change responsibility.',
  'continuity_security':'Define dependencies, recovery objectives, demonstrated verification and authoritative data/security obligations.',
  'service_acceptance':'Specify receiving acceptance, handover, SLA commencement, measurement disputes and change governance.'}),
 'incident-postmortem': ('incident-postmortem', [], {
  'incident_boundary':'Identify affected services, business impact, chronology sources and known, inferred and unknown facts.',
  'contain_recovery':'Record containment and restoration actions, authorisation, observed effects and evidence preservation.',
  'causal_analysis':'Evaluate technical, process and organisational contributing factors and counterfactual control opportunities.',
  'action_plan':'Assign corrective and preventive controls, accountable owners, deadlines and independent verification criteria.',
  'lessons_followup':'Define communications, applicability assessments, recurrence measures and evidence required for closure.'}),
 'compliance-gap-analysis': ('compliance-gap-analysis', ['type/assurance-report'], {
  'applicability':'Identify legal entity, jurisdiction, controlling obligation version, interpretation authority and exclusions.',
  'mapping':'Trace each requirement through control objectives and implemented controls to observed evidence and owners.',
  'gap_analysis':'Locate gaps, distinguish documented intent from operating effectiveness and justify materiality and uncertainty.',
  'remediation':'Prioritise remediation by exposure and dependencies with owners, deadlines and interim controls.',
  'closure':'Require independent verification and retain findings history, residual uncertainty and authorised dispositions.'}),
 'benefits-realisation-review': ('benefits-review', ['type/benefits-review'], {
  'benefit_baseline':'Identify original business-case hypotheses, accountable benefit owners and measured pre-change baselines.',
  'actuals':'Reconcile measured attributable benefits to targets, periods and accounting treatment without double counting.',
  'variance_drivers':'Explain volume, timing, adoption and external effects using an explicit counterfactual and uncertainty.',
  'corrective_actions':'Assign benefit recovery or revised investment actions, decision authorities and measurable review dates.',
  'closure_value':'State realised value, unresolved evidence gaps and continued ownership after programme closure.'}),
 'transformation-roadmap': ('roadmap', ['type/roadmap'], {
  'transformation_objectives':'Trace transformation outcomes and measures to business drivers, scope and accountable sponsors.',
  'current_target':'Identify current and target capabilities, material gaps and explicitly uncertain assumptions.',
  'waves_dependencies':'Sequence work packages, milestones, dependencies, resources and decision checkpoints.',
  'risk_change':'Assess delivery and adoption risks, business continuity, change ownership and mitigation evidence.',
  'investment_governance':'Assign funding tranches, benefits measures, approval boundaries and outcome-based review triggers.'}),
 'client-proposal': ('client-proposal', [], {
  'customer_need':'Identify the customer problem, scope, outcomes, stakeholders and unverified discovery assumptions.',
  'proposed_solution':'Describe the proposed solution and reasoned alternatives with boundaries, dependencies and constraints.',
  'scope_deliverables':'Identify included and excluded deliverables, recipient responsibilities and measurable acceptance.',
  'delivery_plan':'Define delivery stages, milestones, client prerequisites, accountable roles and change controls.',
  'commercial_overview':'Reconcile supplier fees, third-party and client costs, currency, pricing conditions and separately priced options.',
  'decision_request':'Identify the bounded negotiation or mobilisation decision, conditions, authority and next evidence gates.'}),
 'executive-proposal': ('executive-proposal', [], {
  'executive_ask':'State the bounded executive decision, sponsor, authority and permitted commitment level.',
  'business_case':'Explain business outcomes, baseline, benefit assumptions and cost exposure without claiming unmeasured value.',
  'solution_value':'Explain how the recommended operating and technology direction addresses the business need.',
  'alternatives':'Compare viable alternatives and sensitivities against common value, risk and feasibility criteria.',
  'risk_dependencies':'Identify material management risks, dependencies, owners and evidence required for mitigation.',
  'next_decision':'Record conditions to proceed, unresolved questions, decision checkpoints and immediate accountable actions.'}),
 'technical-proposal': ('technical-proposal', [], {
  'architecture_context':'Identify architecture concern, governing requirements, stakeholders, constraints and solution boundary.',
  'solution_design':'Describe component responsibilities, logical interactions, deployment assumptions and design rationale.',
  'interfaces_security':'Specify interface contracts, trust boundaries, identity, data protection and failure behaviour.',
  'nonfunctional_requirements':'State measurable quality objectives with operating conditions and distinguish targets from results.',
  'verification_strategy':'Trace requirements through implementation and functional, negative and recovery checks to receiving acceptance.',
  'technical_assumptions':'Identify design assumptions, exclusions, unresolved decisions and evidence owners.'}),
 'delivery-proposal': ('delivery-proposal', [], {
  'delivery_scope':'Define delivery objectives, included work, contractual boundaries and the proposed delivery approach.',
  'work_packages':'Decompose work into identified outputs with recipient, acceptance evidence and scope traceability.',
  'resources_governance':'Reconcile role effort and person-days independently of elapsed duration and define delivery governance.',
  'schedule_dependencies':'Define sequenced milestones, critical path, capacity and client/supplier prerequisites.',
  'quality_acceptance':'Specify readiness, completion, independent evidence and receiving-role acceptance criteria.',
  'transition_controls':'Define change, risk, recovery and operational transfer responsibilities without inventing acceptance.'}),
 'commercial-proposal': ('commercial-proposal', [], {
  'price_basis':'Define quote status, currency, scope, rate basis, validity and authorised commitment boundary.',
  'cost_breakdown':'Reconcile effort times rates, supplier fees, third-party costs, client costs and total investment.',
  'assumptions_exclusions':'Identify pricing assumptions, dependencies, inclusions and separately priced optional offerings.',
  'payment_terms':'Reconcile milestone payments to supplier services only and state invoicing and acceptance conditions.',
  'commercial_risks':'Evaluate variance, contingency, client delay and optional-service exposure with accountable treatment.',
  'approval_boundary':'Require existing Finance, Legal, Procurement and delegated commercial authority before executable commitment.'}),
 'statement-of-work': ('statement-of-work', [], {
  'parties_scope':'Identify draft status, parties, service boundary, effective-date reservations and included/excluded work.',
  'deliverables':'Specify uniquely identified deliverables, materials, measurable acceptance criteria and receiving owners.',
  'responsibilities':'Assign supplier/client obligations, prerequisites, access, data ownership and accountable authorities.',
  'milestones_acceptance':'Define schedule, acceptance windows, defect handling, checkpoint evidence and exit conditions.',
  'commercial_change':'Reconcile supplier fees with scope and define controlled changes, suspension and commercial dependencies.',
  'legal_reservations':'Identify unresolved legal, privacy, liability and signature conditions without implying an executed agreement.'}),
 'rfp-response': ('rfp-response', [], {
  'response_context':'Identify controlled tender revision, bidder, submission status, scope and unverified assumptions.',
  'requirement_mapping':'Give each requirement a traceable substantive response and truthful proposed, conditional or deviation status.',
  'solution_response':'Reconcile technical, delivery and service responses to the proposed scope and acceptance conditions.',
  'compliance_qualification':'State evidence limitations, mandatory control dependencies and legal/security reservations explicitly.',
  'commercial_schedules':'Reconcile prices, terms and schedule to the accompanying proposal and statement of work.',
  'clarifications':'Assign clarification questions, evidence owners, submission review and existing approval controls.'}),
 'proposal-compliance-matrix': ('proposal-compliance-matrix', [], {
  'requirement_source':'Identify the exact controlled requirement revision, clause locations and response vocabulary.',
  'response_classification':'Record one independently decidable substantive response per requirement with conditions and owner.',
  'evidence_mapping':'Link each claim to actual evidence, current evidence state and receiving review authority.',
  'exceptions_dependencies':'Identify deviations, unmet dependencies, non-negotiable controls and corrective actions.',
  'closure_governance':'Check source completeness, amendment handling and signed disposition without inventing compliance.'}),
 'cybersecurity-transformation-proposal': ('cybersecurity-transformation-proposal', ['domain/security'], {
  'security_baseline':'Identify business risk, current security evidence, transformation scope and mandate limitations.',
  'target_control_architecture':'Trace target control outcomes and trust boundaries to risks, business drivers and alternatives.',
  'transformation_waves':'Sequence security work packages, prerequisites, owners and deployment dependencies.',
  'assurance_roadmap':'Define control verification, measurable outcomes, independent review and residual uncertainty.',
  'resourcing_cost':'Reconcile scope-specific effort and separately priced security options, excluded from base programme totals.',
  'risk_acceptance':'State residual risk, competent acceptance authority and conditions without claiming certification or approval.'}),
 'managed-security-services-proposal': ('managed-security-services-proposal', ['domain/security'], {
  'service_boundary':'Identify entitled services, consumers, support windows, exclusions and required client authority.',
  'service_catalogue':'Define monitoring and response activities, outputs, evidence and actions requiring client approval.',
  'slo_escalation':'Specify measurable service windows, severity, triage targets, exclusions and escalation responsibility.',
  'client_supplier_raci':'Assign incident, privacy and response responsibilities without transferring client decision authority.',
  'commercial_service_model':'Reconcile recurring and onboarding fees, term assumptions and optional scope outside base pricing.',
  'transition_acceptance':'Define onboarding, detection rehearsals, acceptance evidence and controlled exit or handback.'}),
}

REFERENCE_ROLE_LINKS = {
 'client-proposal':['bid-proposal-manager:3'],
 'executive-proposal':['bid-proposal-manager:3'],
 'technical-proposal':['pre-sales-solution-consultant:1'],
 'delivery-proposal':['delivery-manager:1','bid-proposal-manager:4'],
 'commercial-proposal':['commercial-pricing-deal-finance-specialist:2'],
 'statement-of-work':['supplier-commercial-deal-manager:2'],
 'rfp-response':['pre-sales-solution-consultant:2','bid-proposal-manager:1'],
 'proposal-compliance-matrix':['bid-proposal-manager:2'],
 'cybersecurity-transformation-proposal':[],
 'managed-security-services-proposal':[],
}

# Explicit opt-in specializations; these do not change existing role contracts.
ENGINEERING_REFERENCE_KINDS = ('api-interface-contract', 'appsec-verification-report', 'cicd-pipeline-assurance', 'devsecops-pipeline-design', 'release-readiness-review', 'security-architecture-assessment', 'security-control-assessment', 'software-engineering-plan', 'software-supply-chain-assessment', 'target-operating-model', 'threat-model', 'transformation-baseline-assessment', 'transformation-execution-plan')
REFERENCE_KINDS.update({
 'software-engineering-plan': ('software-engineering-plan', ['domain/delivery'], {'delivery_boundary': 'Define delivery boundary, business invariants, authoritative sources and explicit engineering exclusions.', 'design_decomposition': 'Decompose the design into components, interfaces, migrations, failure modes and accountable implementation owners.', 'engineering_controls': 'Specify peer review, least privilege, pinned dependencies and traceable engineering change controls.', 'quality_gates': 'Define positive, negative, recovery and performance assertions with actual execution evidence and blocking outcomes.', 'release_governance': 'Identify promotion authority, rollback boundaries, readiness dependencies and independent release decisions.', 'acceptance_trace': 'Trace requirements through design, implementation, verification and receiving acceptance without inventing execution.'}),
 'api-interface-contract': ('api-interface-contract', ['type/implementation-specification'], {'contract_boundary': 'Identify providers, consumers, protocol version, interface boundary and supported business interactions.', 'schemas_semantics': 'Specify schemas, field meaning, identifiers, units, state transitions and compatibility constraints.', 'auth_and_privacy': 'Define authentication, object authorization, data minimization and applicable privacy responsibilities.', 'failure_contract': 'Specify error semantics, retry limits, idempotency, timeouts and uncertain-completion reconciliation.', 'compatibility_testing': 'Define compatibility windows and reproducible consumer, negative and failure-path contract tests.', 'ownership_acceptance': 'Assign interface ownership, change authority, acceptance conditions and unresolved integration dependencies.'}),
 'release-readiness-review': ('release-readiness-review', ['type/operational-readiness-assessment'], {'release_scope': 'Identify exact release scope, included changes, environments, owners and excluded capabilities.', 'build_provenance': 'Trace source revision, dependency inventory, build digest and attributable provenance to the candidate.', 'verification_summary': 'Distinguish executed verification results, failures, blocked checks and missing mandatory evidence.', 'operability_readiness': 'Assess monitoring, recovery rehearsal, receiving operations, service dependencies and support readiness.', 'open_risks': 'Record unresolved defects, residual risks, compensating controls and competent disposition owners.', 'release_disposition': 'Separate evidence-based release recommendation from human deployment authority and approval.'}),
 'transformation-baseline-assessment': ('transformation-baseline-assessment', ['domain/delivery'], {'baseline_boundary': 'Define dated baseline scope, business entities, value streams and assessment authority limitations.', 'capability_evidence': 'Assess current capabilities using attributable observations, sampling limits and explicitly uncertain measurements.', 'pain_points': 'Locate business pain points, causal hypotheses, impacts and gaps in the supporting evidence.', 'dependency_map': 'Map organizational, system, supplier and data dependencies with accountable ownership and constraints.', 'gap_prioritisation': 'Prioritize gaps using explicit value, risk, feasibility and confidence criteria without invented certainty.', 'baseline_decision': 'Identify decisions supported by the baseline, evidence owners and conditions for independent acceptance.'}),
 'target-operating-model': ('target-operating-model', ['domain/delivery'], {'target_value': 'Define target value, business outcomes, operating boundary and measurable service objectives.', 'capability_ownership': 'Assign capability ownership, service responsibilities and cross-domain accountabilities.', 'process_and_decisions': 'Describe operational processes, decision rights, escalation paths and authority boundaries.', 'organization_skills': 'Define organization, role competencies, capacity assumptions and adoption responsibilities.', 'controls_and_measurement': 'Specify controls, performance measures, evidence sources and independent oversight obligations.', 'transition_acceptance': 'Plan transition states, receiving acceptance, dependencies and unresolved organizational decisions.'}),
 'transformation-execution-plan': ('transformation-execution-plan', ['type/roadmap'], {'outcomes_scope': 'Trace transformation outcomes, scope, measures and delivery authority to agreed business drivers.', 'transition_states': 'Define current, interim and target operating states with continuity and rollback constraints.', 'waves_dependencies': 'Sequence work packages, dependencies, milestones, resource capacity and funding decision checkpoints.', 'change_and_adoption': 'Define stakeholder engagement, training, adoption measures and accountable change ownership.', 'risk_governance': 'Identify delivery risks, control ownership, escalation and authorized residual-risk decisions.', 'decision_gates': 'Specify evidence-based stage entry and exit criteria without converting recommendations into approval.'}),
 'security-architecture-assessment': ('security-architecture-assessment', ['domain/security'], {'scope_and_trust': 'Identify assessed assets, architecture boundaries, data flows, trust assumptions and exclusions.', 'security_requirements': 'Trace security requirements to business risks, applicable obligations and authoritative sources.', 'architecture_findings': 'Locate architecture weaknesses and evaluate abuse paths, uncertainty and business impact.', 'control_recommendations': 'Recommend proportionate preventive, detective and recovery controls with ownership and rationale.', 'verification_evidence': 'Distinguish observed evidence, proposed validation and unavailable execution results.', 'risk_disposition': 'State residual risks, assessment limitations and competent risk acceptance authority.'}),
 'threat-model': ('threat-model', ['domain/security'], {'assets_and_scope': 'Identify valuable assets, business invariants, attacker assumptions and authorized modeling scope.', 'trust_flows': 'Describe components, data flows, trust crossings, identities and security-relevant dependencies.', 'threat_scenarios': 'Enumerate credible misuse scenarios with preconditions, attack paths and business consequences.', 'security_controls': 'Map mitigations to threats, responsible owners and defense limitations without claiming effectiveness.', 'validation_plan': 'Define reproducible abuse-case, authorization and recovery checks with expected evidence.', 'residual_risk': 'Evaluate remaining exposure, uncertain assumptions and the separate human risk disposition.'}),
 'security-control-assessment': ('security-control-assessment', ['domain/security', 'type/assurance-report'], {'assessment_criteria': 'Identify control objectives, authoritative criteria, period, applicability and assessment exclusions.', 'population_and_method': 'Define tested population, sampling, assessor independence and limitations of the method.', 'control_observations': 'Record source-bound control observations and distinguish design from operating effectiveness.', 'exceptions_analysis': 'Analyze exceptions, their significance, affected populations and evidence uncertainty.', 'remediation_retest': 'Assign remediation, deadlines, retest procedures and independent closure evidence.', 'assurance_conclusion': 'Bound assurance conclusions to actual evidence and retain unresolved risks and authorization limits.'}),
 'devsecops-pipeline-design': ('devsecops-pipeline-design', ['domain/security', 'type/solution-design'], {'pipeline_scope': 'Define repository, build, deployment, environment and pipeline trust boundaries.', 'stages_and_protection': 'Specify isolated stages, protected transitions, independent reviews and promotion permissions.', 'security_quality_gates': 'Define security and quality checks, failure behavior and non-waivable evidence requirements.', 'artifact_provenance': 'Trace immutable artifacts through provenance, verification, signing and controlled distribution.', 'secrets_and_identity': 'Specify least-privilege workload identities, secret references, rotation and exposure prevention.', 'operating_acceptance': 'Define pipeline ownership, monitoring, recovery, change control and receiving acceptance.'}),
 'cicd-pipeline-assurance': ('cicd-pipeline-assurance', ['domain/security', 'type/assurance-report'], {'assurance_scope': 'Identify pipeline revision, execution environments, assurance criteria and coverage exclusions.', 'runner_trust': 'Assess runner isolation, identity permissions, untrusted input and protected promotion boundaries.', 'execution_results': 'Record actual check results and retain failed, blocked and unexecuted states without promotion.', 'provenance_checks': 'Verify source-to-build-to-artifact provenance and distinguish integrity from professional approval.', 'exceptions_and_risks': 'Locate exceptions, evidence gaps, supply dependencies and accountable residual-risk owners.', 'release_attestation': 'State bounded release assurance and required independent decisions without fabricating attestation.'}),
 'appsec-verification-report': ('appsec-verification-report', ['domain/security', 'type/test-report'], {'verification_scope': 'Identify application build, authorized test boundary, environments and verification exclusions.', 'threat_requirements': 'Trace security requirements and threat scenarios to risk-based verification procedures.', 'static_dependency_tests': 'Record attributable static, dependency and configuration checks with versions and limitations.', 'dynamic_authorization_tests': 'Document executed dynamic, object-authorization and abuse tests with inputs and observations.', 'findings_and_fixes': 'Locate findings, assess exploitability, record fixes and independently attributable retest evidence.', 'acceptance_disposition': 'State unresolved exposure, execution gaps and competent release or risk disposition authority.'}),
 'software-supply-chain-assessment': ('software-supply-chain-assessment', ['domain/security', 'type/assurance-report'], {'supply_chain_scope': 'Define software products, build systems, suppliers and distribution boundaries under assessment.', 'dependency_inventory': 'Inventory direct and transitive dependencies, versions, origin, licensing and known evidence gaps.', 'build_provenance': 'Assess attributable build provenance, reproducibility, isolated execution and source integrity.', 'publisher_integrity': 'Verify publisher identities, artifact digests, signing trust and controlled acquisition practices.', 'supplier_risks': 'Evaluate supplier exposure, maintenance, compromise paths and uncertainty with accountable owners.', 'release_conditions': 'Define evidence-based release conditions, remediation and competent exception authority.'}),
})
