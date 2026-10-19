# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Authored proposed modality and domain obligations for the 26.10.8 catalogue.

These are professional proposals derived from JAI's existing artifact purposes,
not quotations from a normative framework. Tuples contain a stable semantic field,
JSON datatype and substantive acceptance instruction. Production selection always
uses registered identifiers; no title classifier consumes these definitions.
"""

TYPE_REQUIREMENTS = {
 'architecture-definition': [('architecture_boundary','object','Identify stakeholders, system boundary, concerns and architecture baseline.'),('viewpoint_consistency','array','Link business, data, application and technology viewpoints using stable source-model IDs.'),('architecture_gaps','array','Identify target gaps, accountable owners and decisions required to close them.')],
 'architecture-decision': [('decision_record','object','Record decision status, owner, date and architecture concern.'),('design_alternatives','array','Compare feasible alternatives against explicit drivers and constraints.'),('decision_consequences','array','Describe rejected options, reversibility, debt and operational consequences.')],
 'solution-design': [('component_design','array','Describe bounded component responsibilities and deployment topology.'),('interface_contracts','array','Define versioned interface inputs, outputs, trust boundaries and failure handling.'),('design_verification','array','Map measurable quality requirements to design verification and acceptance.')],
 'decision-paper': [('decision_authority','object','Identify the specific choice, accountable authority and decision deadline.'),('option_comparison','array','Compare viable options including the do-nothing baseline against common criteria.'),('decision_impacts','object','Explain cost, benefit, dependencies, uncertainty and residual risks of the recommendation.')],
 'business-case': [('investment_boundary','object','Identify sponsor, financial owner, funding decision and appraisal horizon.'),('investment_cashflows','array','Show dated currency, baseline, costs and non-overlapping benefits with assumptions.'),('investment_sensitivity','array','Assess uncertain benefit, cost and timing assumptions and assign realisation owners.')],
 'risk-assessment': [('risk_method','object','Define scope, likelihood, impact scales and applicable risk appetite.'),('evaluated_scenarios','array','Link assets, causes, events, consequences and inherent/residual ratings to evidence.'),('treatment_accountability','array','Assign treatments, deadlines, risk owners and residual acceptance authority.')],
 'assurance-report': [('assurance_criteria','array','Define tested obligations, assurance period, sample and exclusions.'),('assurance_observations','array','Link procedures and observed results to immutable evidence and located deviations.'),('bounded_conclusion','object','Limit the independent conclusion to tested scope, evidence strength and unresolved findings.')],
 'control-design': [('control_objectives','array','Link control objectives to risks, business requirements and accountable owners.'),('control_mechanisms','array','Define preventive/detective/corrective actions, triggers, inputs and failure behaviour.'),('control_effectiveness','array','Define measurable effectiveness tests, evidence collection and exception handling.')],
 'implementation-specification': [('implementation_parameters','array','Define typed configuration values, units, versions and permitted ranges without secrets.'),('implementation_interfaces','array','Specify schemas, error states, concurrency and compatibility requirements.'),('implementation_acceptance','array','Specify deployment, verification, rollback and reproducible acceptance tests.')],
 'migration-plan': [('migration_inventory','array','Identify source/target assets, data owners, versions and dependencies.'),('migration_waves','array','Assign sequencing, capacity, reconciliation checks and acceptance criteria to each wave.'),('migration_recovery','object','Define integrity checks, fallback decision time, rollback and business continuity.')],
 'cutover-plan': [('cutover_schedule','array','Assign ordered timed activities, named operators and entry/exit criteria.'),('cutover_decision_points','array','Specify go/no-go authorities, evidence, communication and irreversible points.'),('cutover_reversal','object','Define tested fallback steps, maximum rollback window and safe-state verification.')],
 'operational-readiness-assessment': [('readiness_criteria','array','Define service acceptance criteria for support, resilience, security, capacity and monitoring.'),('readiness_observations','array','Link each criterion to observed evidence, gaps and accountable remediation owners.'),('readiness_disposition','object','Record receiving operations recommendation, residual risks and pending authority decisions.')],
 'service-design': [('service_outcomes','object','Identify customers, service owner, outcomes, boundaries and demand assumptions.'),('service_levels','array','Define measurable availability, support, capacity and recovery targets.'),('service_operating_model','object','Describe support responsibilities, suppliers, monitoring, continuity and lifecycle costs.')],
 'runbook': [('execution_boundary','object','Define triggers, authorised operators, prerequisites and stop conditions.'),('verified_steps','array','Provide ordered actions, exact targets, expected observations and verification.'),('recovery_and_escalation','object','Define failures, safe-state recovery, rollback and named escalation responsibility.')],
 'test-strategy': [('test_risk_scope','object','Define risk-based test objectives, quality targets, scope and exclusions.'),('test_approach','array','Define test levels, techniques, environments, representative data and responsibilities.'),('test_exit_criteria','array','Define traceable entry/exit criteria, coverage measurement and defect disposition rules.')],
 'test-report': [('tested_baseline','object','Identify build, requirements, environment, reporting period and exclusions.'),('observed_test_results','array','Link test cases and requirements to actual outcomes, timestamps and execution evidence.'),('test_release_constraints','object','Explain defects, untested scope, achieved exit criteria and residual release risk.')],
 'benefits-review': [('benefit_baselines','array','Identify committed benefit measures, baselines, owners and measurement periods.'),('benefit_observations','array','Compare actual attributable outcomes to targets without double counting.'),('benefit_disposition','array','Explain variance, confidence, corrective actions and continued investment decisions.')],
 'roadmap': [('outcome_horizons','array','Describe current and target outcomes, accountable owners and planning assumptions.'),('delivery_increments','array','Define sequenced increments, resources, milestones and measurable acceptance.'),('roadmap_dependencies','array','Link dependencies, funding constraints, risks and decision dates to affected increments.')],
 'register': [('register_schema','object','Define required columns, datatypes, identifiers, allowed states and ownership.'),('register_records','array','Provide actual uniquely identified records with source, owner, status and review date.'),('register_integrity','array','Evidence uniqueness, referential integrity, completeness and lifecycle reconciliation checks.')],
 'dashboard': [('dashboard_measures','array','Define metrics, units, denominators, targets, refresh cadence and accountable owners.'),('dashboard_values','array','Provide dated observations linked to versioned source queries and population scope.'),('dashboard_interpretation','object','Explain thresholds, uncertainty, missing data and actions supported by the view.')],
 'presentation': [('presentation_ask','object','Identify audience, supported decision or learning outcome and requested next action.'),('presentation_argument','array','Provide sequenced claims, evidence, implications and explicit uncertainty.'),('presentation_navigation','array','Map key messages to slides, accessible visuals and referenced source annexes.')],
 'dataset': [('dataset_schema','array','Define fields, datatypes, units, keys, null handling and allowed values.'),('dataset_lineage','object','Record source versions, extraction time, transformations, lawful access and retention.'),('dataset_quality','array','Evidence completeness, uniqueness, consistency, drift and permitted-use limitations.')],
 'catalogue': [('catalogue_schema','object','Define entity classes, stable identifiers, required attributes and relations.'),('catalogue_entries','array','Identify actual governed entities with owners, source, status and lifecycle dates.'),('catalogue_integrity','array','Evidence duplicate detection, relationship integrity and reconciliation against sources.')],
 'document': [('document_scope','object','Identify document purpose, audience, subject boundary and authoritative source versions.'),('document_analysis','array','Provide attributable substantive findings, reasoning and limitations for the specific subject.'),('document_actions','array','Identify decisions or downstream uses, accountable recipients and verifiable next actions.')],
 'diagram': [('diagram_viewpoint','object','Define the concern, viewpoint, system boundary, legend and notation.'),('diagram_elements','array','List stable source-model element IDs, typed relations and labels represented in the view.'),('diagram_integrity','array','Evidence endpoint validity, semantic compatibility, coverage and visual readability.')],
 'model': [('model_metamodel','object','Define entity/relation types, constraints, model boundary and source baseline.'),('model_entities','array','Provide stable identified entities and typed relationships with ownership and provenance.'),('model_validation','array','Evidence referential integrity, constraint checks, cross-view consistency and known gaps.')],
 'prototype': [('prototype_hypothesis','object','Define the feasibility question, explicit non-production boundary and success criteria.'),('prototype_reproduction','object','Identify versioned code, dependencies, representative inputs and reproducible execution.'),('prototype_results','array','Record observed results, limitations, risks and disposition against predeclared criteria.')],
 'configuration-baseline': [('baseline_targets','array','Identify managed assets, tool/schema versions and authorised configuration scope.'),('baseline_values','array','Provide typed desired settings, permitted ranges and secret-manager references.'),('baseline_verification','array','Evidence reproducibility, drift checks, deployment validation and rollback to a known baseline.')],
}

DOMAIN_REQUIREMENTS = {
 'security': [('security_boundary','object','Identify protected business outcomes, trust boundaries and authorised information handling.'),('security_control_trace','array','Trace threat/risk scenarios through control objectives to effectiveness evidence and residual owners.')],
 'architecture': [('architecture_source_trace','array','Link design claims to versioned source elements, stakeholder concerns and measurable requirements.'),('architecture_change_impact','array','Identify cross-domain dependencies, affected owners and compatibility constraints.')],
 'testing': [('test_requirement_trace','array','Map scoped requirements and risks to test procedures, expected observations and evidence.'),('test_evidence_limits','object','Identify sampling, unexecuted cases, environment limits and independent acceptance responsibility.')],
 'operations': [('operational_ownership','object','Identify receiving service owner, support boundaries, escalation and review triggers.'),('operational_recoverability','array','Trace monitoring, failure handling, backup/recovery and rollback requirements to rehearsed evidence.')],
 'data': [('data_accountability','object','Identify data owner, stewardship, lawful use, classification and lifecycle obligations.'),('data_lineage_quality','array','Trace source-to-output transformations, quality constraints and evidenced reconciliation.')],
 'delivery': [('delivery_accountability','array','Assign outcomes, milestones, resource assumptions and acceptance responsibility.'),('delivery_dependencies','array','Link delivery risks, cross-team dependencies and change decisions to accountable owners.')],
}
TYPE_DOMAINS = {
 **dict.fromkeys(['risk-assessment','assurance-report','control-design'],'security'),
 **dict.fromkeys(['architecture-definition','architecture-decision','solution-design','implementation-specification','diagram','model'],'architecture'),
 **dict.fromkeys(['test-strategy','test-report'],'testing'),
 **dict.fromkeys(['runbook','service-design','operational-readiness-assessment','configuration-baseline'],'operations'),
 **dict.fromkeys(['dataset','catalogue','register','dashboard'],'data'),
 **dict.fromkeys(['roadmap','business-case','decision-paper','benefits-review','migration-plan','cutover-plan','prototype','presentation','document'],'delivery'),
}

SABSA_REQUIREMENTS = {
 'architecture': [('architecture_cells','array','Map each selected contextual/conceptual/logical/physical/component/operational element to its What/Why/How/Who/Where/When cell.'),('architecture_chain','array','Trace business drivers through attributes, objectives, services, mechanisms and operational measures.')],
 'executive-summary': [('executive_business_attributes','array','Explain prioritised business attributes, target measures and observed gaps in business language.'),('executive_security_choices','array','Present material risk/opportunity choices, investment consequences and accountable decisions.')],
 'risk-treatment-plan': [('sabsa_risk_treatments','array','Link each risk/opportunity to business attributes, control objectives, treatment owner and due date.'),('sabsa_residual_acceptance','array','Record residual exposure, exception scope/expiry and mandated risk acceptance authority.')],
 'policy-architecture': [('policy_hierarchy','array','Link business strategy and security policy to standards, owners and scope.'),('policy_enforcement','array','Map policy statements to control objectives, mechanisms, exceptions and compliance evidence.')],
 'trust-model': [('trust_domains','array','Identify domain owners, assets, business rationale and explicit trust boundaries.'),('trust_relationships','array','Define directional trust, authentication/authorisation assumptions, permitted interactions and failure handling.')],
 'information-access-model': [('information_entities','array','Identify classified information entities, owners, lifecycle and authorised uses.'),('privilege_profiles','array','Map subjects/roles to privileges, segregation constraints, information flows and access review.')],
 'security-service-catalogue': [('logical_security_services','array','Describe logical services, consumers, interfaces, owners and supported control objectives.'),('security_service_measures','array','Define business attributes, service measures, dependency assumptions and effectiveness evidence.')],
 'component-realisation': [('security_components','array','Map physical mechanisms to versioned components, owners, deployment boundaries and standards.'),('component_verification','array','Trace component configuration and tests to logical services and control objectives.')],
 'assurance-plan': [('attribute_assurance','array','Link measurable business attributes and control objectives to assurance criteria.'),('assurance_schedule','array','Assign test methods, evidence sources, independent reviewers, frequency and escalation thresholds.')],
 'governance-register': [('governance_decisions','array','Record dated decisions, rationale, mandate, owners and source-model effects.'),('governance_exceptions','array','Identify policy/trust exceptions, scope, expiry, compensating controls and acceptance authority.')],
 'current-state': [('current_baseline','array','Identify observed current assets, controls, services and source versions at the assessment date.'),('current_limitations','array','Distinguish evidenced gaps from assumptions and link business consequences to owners.')],
 'target-state': [('target_requirements','array','Link target architecture elements to business attributes, control objectives and measurable acceptance.'),('target_feasibility','array','Record design assumptions, dependencies, residual risks and validation required before adoption.')],
 'transition-architecture': [('transition_mappings','array','Map current elements to target replacements, retained assets and retirement dependencies.'),('transition_controls','array','Define interim control coverage, coexistence risks, entry/exit criteria and accountable owners.')],
 'transition-roadmap': [('security_roadmap_items','array','Link increments to business drivers, risk treatment, target elements and dependency IDs.'),('security_roadmap_acceptance','array','Assign resources, owners, milestones, control readiness and measurable completion criteria.')],
 'lifecycle-register': [('architecture_lifecycle','array','Record source element IDs, lifecycle states, owners and validity horizons.'),('lifecycle_transitions','array','Define authorised transition/retirement conditions, dependencies and review dates.')],
 'framework-mapping': [('framework_requirements','array','Identify exact framework version, requirement identifiers and applicability basis.'),('framework_architecture_links','array','Map requirements to architecture elements and evidence with full/partial/gap status and rationale.')],
 'compliance-gap-analysis': [('compliance_gaps','array','Identify applicable requirement IDs, observed shortfalls and evidence limitations.'),('compliance_gap_treatments','array','Assign remediation/exception decisions, roadmap links, owners and due dates without waiving law.')],
 'reuse-register': [('reused_elements','array','Identify canonical library, stable element ID, version/hash, owner and reuse scope.'),('reuse_dependencies','array','Record dependent consumers, compatibility constraints and change propagation responsibilities.')],
 'client-questions': [('confirmation_questions','array','Identify unresolved assumptions, precise questions, business impact and requested evidence.'),('confirmation_accountability','array','Assign competent respondents, due dates, pending decisions and consequences of no answer.')],
}

ARCHETYPE_REQUIREMENTS = {
 'architecture-definition': ('architecture_reader_map','Map stakeholder concerns to relevant viewpoints, architecture decisions and source-model annexes.'),
 'architecture-review-pack': ('review_disposition','Present review scope, criteria, located findings, accountable responses and decision disposition.'),
 'audit-compliance-evidence-pack': ('audit_evidence_index','Map each scoped requirement to versioned evidence, tested coverage, exceptions and independent conclusions.'),
 'benefits-review': ('benefits_reader_comparison','Present target-versus-observed benefits, attribution limits, variance owners and decisions.'),
 'decision-paper': ('decision_reader_comparison','Present the specific ask, common option criteria, tradeoffs and accountable next decision.'),
 'detailed-design-lld': ('lld_reader_contracts','Locate exact interface/configuration/error contracts, verification procedures and rollback details.'),
 'executive-one-pager': ('executive_reader_ask','Present one clear ask, business outcome, options/risks, accountable owner and next action.'),
 'implementation-specification': ('implementation_reader_sequence','Locate reproducible engineering inputs, parameter constraints, acceptance tests and deployment sequence.'),
 'migration-cutover-pack': ('cutover_reader_decisions','Locate dependencies, timed cutover sequence, go/no-go authority, reconciliation and fallback decision points.'),
 'operational-handover': ('operations_reader_acceptance','Locate service responsibilities, readiness evidence, support/escalation, known issues and receiving acceptance.'),
 'risk-assurance-pack': ('risk_reader_exposure','Present scope, method, material exposures, evidence limits, treatment and residual acceptance responsibility.'),
 'roadmap': ('roadmap_reader_sequence','Present outcome horizons, sequenced increments, critical dependencies, funding and acceptance milestones.'),
 'solution-design-hld': ('hld_reader_boundaries','Locate solution scope, measurable drivers, components/interfaces, trust boundaries and delivery verification.'),
}

# Explicit registered modality-to-family assignments; no runtime title inference.
SEMANTIC_FAMILIES = {
    'architecture-definition': 'architecture-definition', 'architecture-decision': 'adr',
    'solution-design': 'hld', 'decision-paper': 'decision-paper',
    'business-case': 'business-case', 'risk-assessment': 'risk-assessment',
    'assurance-report': 'assurance-report', 'control-design': 'control-design',
    'implementation-specification': 'implementation-specification',
    'migration-plan': 'migration-plan', 'cutover-plan': 'cutover-plan',
    'operational-readiness-assessment': 'operational-readiness-assessment',
    'service-design': 'service-design', 'runbook': 'runbook',
    'test-strategy': 'test-strategy', 'test-report': 'test-report',
    'benefits-review': 'benefits-review', 'roadmap': 'roadmap', 'register': 'register',
    'dashboard': 'dashboard', 'presentation': 'presentation', 'dataset': 'dataset',
    'catalogue': 'catalogue', 'document': 'document', 'diagram': 'diagram',
    'model': 'model', 'prototype': 'prototype',
    'configuration-baseline': 'configuration-baseline',
}

# Bounded authored refinements for semantically distinct prose families whose
# frozen legacy modality is too broad. Keys are exact canonical contract IDs.
SEMANTIC_REFINEMENTS = {
    'chief-information-officer:1': 'strategy',
    'chief-technology-officer:1': 'strategy',
    'chief-data-officer:1': 'strategy',
    'chief-digital-officer:2': 'strategy',
    'chief-product-officer:1': 'strategy',
    'chief-ai-officer:1': 'strategy',
    'staff-engineer:1': 'strategy',
    'product-owner:4': 'release-notes',
    'release-engineer:2': 'release-notes',
    'technical-writer:3': 'release-notes',
    'business-analyst:1': 'requirements-specification',
    'systems-engineer-incose:1': 'requirements-specification',
}

ADDITIONAL_FAMILIES = {
    'strategy': [
        ('strategic_outcomes', 'array', 'Trace target outcomes and measurable success to business direction and baseline constraints.'),
        ('strategic_choices', 'array', 'Compare investment and operating choices, dependencies, resource assumptions and rejected alternatives.'),
        ('strategy_execution', 'array', 'Assign sequenced initiatives, accountable owners, outcome measures and review triggers.')],
    'release-notes': [
        ('release_identity', 'object', 'Identify exact release and predecessor versions, affected products and deployment applicability.'),
        ('release_changes', 'array', 'Link delivered changes, resolved defects, known limitations and compatibility impacts to traceable change records.'),
        ('release_actions', 'array', 'Specify required upgrade actions, configuration changes, rollback constraints and recipient communication.')],
    'requirements-specification': [
        ('requirement_sources', 'array', 'Trace stakeholder needs, authoritative sources, scope and assumptions to requirement identifiers.'),
        ('verifiable_requirements', 'array', 'State uniquely identified testable requirements, priority, rationale, interfaces and measurable acceptance conditions.'),
        ('requirements_consistency', 'array', 'Identify conflicting requirements, dependencies, traceability gaps and change approval responsibility.')],
}

# Semantic purpose comes from the authored refinement, never the legacy storage
# modality. Broad frozen artifact types sometimes describe the wrong activity.
REFINED_PURPOSE_ACTIONS = {
    'strategy': 'Set strategic choices, target outcomes, investment priorities and accountable review triggers',
    'release-notes': 'Inform recipients of release changes, compatibility impacts, known issues and required upgrade actions',
    'requirements-specification': 'Agree testable requirements, resolve stakeholder conflicts and trace acceptance conditions to implementation and verification',
}

CONTRACT_PURPOSE_ACTIONS = {
    'software-engineer:1': 'Integrate reviewed code against the specified behaviour and demonstrate regression and rollback readiness',
    'software-engineer:2': 'Execute automated tests to detect behavioural regressions and expose untested requirements',
    'software-engineer:3': 'Explain changed interfaces, assumptions and operating requirements to maintainers and users',
    'software-engineer:4': 'Execute deployment and rollback actions using documented verification checkpoints and recovery constraints',
    'release-engineer:3': 'Execute versioned deployment automation with controlled targets, verification checkpoints and rollback handling',
    'test-automation-engineer:1': 'Execute automated test suites against risk-based coverage and investigate observed regressions',
    'test-automation-engineer:2': 'Maintain reusable test framework abstractions that enable deterministic, isolated automated checks',
    'test-automation-engineer:3': 'Prioritise remediation of intermittent test failures from measured flakiness and reliability evidence',
    'test-automation-engineer:4': 'Identify untested product risks and prioritise additional test coverage against those risks',
    'devops-engineer:1': 'Execute controlled build, test and deployment pipeline stages with explicit failure and rollback behaviour',
    'devops-engineer:2': 'Provision and deploy consistent environments using versioned automation and verified recovery paths',
    'devops-engineer:3': 'Apply versioned desired configuration and reconcile drift without exposing secrets',
    'devops-engineer:4': 'Measure deployment outcomes and use feedback to prioritise delivery reliability improvements',
}

# These exact engineering source deliverables are not feasibility prototypes or
# option papers, despite their frozen compatibility artifact types.
SEMANTIC_REFINEMENTS.update({
    'software-engineer:1': 'software-change',
    'software-engineer:2': 'automated-tests',
    'software-engineer:3': 'document',
    'software-engineer:4': 'runbook',
    'release-engineer:3': 'deployment-automation',
    'test-automation-engineer:1': 'automated-tests',
    'test-automation-engineer:2': 'automated-tests',
    'test-automation-engineer:3': 'test-report',
    'test-automation-engineer:4': 'test-strategy',
    'devops-engineer:1': 'deployment-automation',
    'devops-engineer:2': 'deployment-automation',
    'devops-engineer:3': 'configuration-baseline',
    'devops-engineer:4': 'dashboard',
})

ADDITIONAL_FAMILIES.update({
    'software-change': [
        ('change_behaviour', 'object', 'Trace implemented behaviour and changed interfaces to requirements, design constraints and the exact reviewed source revision.'),
        ('change_verification', 'array', 'Identify reproducible automated checks, observed results, untested risks and independent review findings without inventing execution.'),
        ('change_recovery', 'object', 'Define deployment compatibility, telemetry, failure detection and rollback or forward recovery constraints.')],
    'automated-tests': [
        ('automated_test_scope', 'array', 'Trace executable cases and reusable test abstractions to requirements, risk coverage, deterministic data and environment assumptions.'),
        ('automated_test_execution', 'array', 'Give reproducible invocation, assertions, expected outcomes and failure diagnostics; distinguish test definitions from evidence of executed runs.'),
        ('automated_test_maintenance', 'object', 'Define isolation, dependency handling, flakiness investigation, coverage limitations and maintenance ownership.')],
    'deployment-automation': [
        ('deployment_targets', 'array', 'Identify exact deployment targets, versioned build inputs, configuration contracts and authorised execution boundaries without secrets.'),
        ('deployment_controls', 'array', 'Define ordered automated stages, verification checkpoints, error handling, stop conditions and rollback or forward recovery paths.'),
        ('deployment_verification', 'array', 'Link reproducible automation checks and observed outcomes to controlled environments; do not claim production execution or authorisation without evidence.')],
})
