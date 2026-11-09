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

# These sources are candidate professional methods for the six shared overlays,
# not an assertion that every cited standard applies to every domain task.
DOMAIN_PROFESSIONAL_REFERENCES = {
    'security': ['systems-security-engineering', 'risk-assessment', 'control-assessment'],
    'architecture': ['architecture-description', 'requirements-engineering'],
    'testing': ['software-testing', 'control-assessment'],
    'operations': ['service-management', 'sre-practice', 'contingency-planning'],
    'data': ['data-catalogue', 'data-quality'],
    'delivery': ['it-governance', 'business-appraisal'],
}

# Candidate professional bases for every catalogue domain. The shared
# applicability record selects the actually relevant edition/method per task.
# Candidates are not automatic requirements or assertions of conformance.
ROLE_DOMAIN_PROFESSIONAL_REFERENCES = {
    1: ['it-governance', 'business-appraisal'],
    2: ['it-governance', 'requirements-engineering', 'human-centred-design'],
    3: ['requirements-engineering', 'data-quality'],
    4: ['architecture-description', 'requirements-engineering'],
    5: ['secure-software', 'software-testing'],
    6: ['software-testing', 'control-assessment', 'accessibility'],
    7: ['data-catalogue', 'data-quality', 'ai-risk-management'],
    8: ['sre-practice', 'configuration-management', 'contingency-planning'],
    9: ['internet-standards-process', 'systems-security-engineering'],
    10: ['service-management', 'sre-practice'],
    11: ['systems-security-engineering', 'control-assessment', 'contingency-planning'],
    12: ['control-assessment', 'risk-assessment'],
    13: ['it-governance', 'control-assessment', 'risk-assessment'],
    14: ['human-centred-design', 'accessibility', 'accessibility-evaluation'],
    15: ['business-appraisal', 'it-governance'],
    16: ['research-reproducibility', 'requirements-engineering'],
    17: ['sabsa-overview', 'architecture-description', 'systems-security-engineering'],
}

DOMAIN_ACCEPTANCE_DETAILS = {
    'security': [
        'Use the applicable secure-systems life-cycle method to identify protected outcomes, trust assumptions and threats; distinguish design evidence from operating-effectiveness evidence.',
        'For each selected risk/control method, link scenario, objective, control, assessment procedure, observed result, uncertainty and residual acceptance owner.'],
    'architecture': [
        'Use architecture-description concepts to trace stakeholder, concern, requirement, viewpoint and view; identify correspondence rules and unresolved inconsistencies without mandating a notation.',
        'Use measurable requirement and correspondence checks to assess affected elements, cross-view dependencies, change impact and decisions still needing evidence.'],
    'testing': [
        'Apply a stated test or assessment technique to each scoped requirement/risk; identify expected versus observed outcomes, tested baseline and exact evidence.',
        'Bound conclusions by the evaluated population, sample rationale, exclusions, environment and unresolved defects; absence of execution is not a passing result.'],
    'operations': [
        'Use the adopted service-management and service-objective method to define receiving responsibilities, service indicators, objectives, measurement windows and escalation thresholds.',
        'Compare observed recovery and failure-handling results to agreed objectives, dependency assumptions and rehearsal conditions; an untested recovery procedure remains an open evidence gap.'],
    'data': [
        'Distinguish catalogue identity, access and provenance metadata from lawful-use decisions; identify accountable owners, permitted purposes and restrictions.',
        'Apply explicit quality dimensions, metrics and measurements to lineage transformations; specify population, thresholds, observed results and reconciliation limitations.'],
    'delivery': [
        'Use the applicable governance/appraisal method to separate outcomes, decision rights, funding assumptions, acceptance responsibility and benefit ownership.',
        'Compare credible delivery options and dependencies against a common baseline; identify sensitivity to cost, benefit, timing and residual risk without treating public-sector guidance as universally binding.'],
}

# Catalogue category IDs retain local specialty selection. These method prompts
# sharpen output reasoning; they do not whitelist professions or frameworks.
ROLE_DOMAIN_METHOD_FOCUS = {
    1: 'Connect strategic choices, investment options, measurable outcomes, risk appetite and accountable decisions.',
    2: 'Trace the evidenced problem through product hypotheses, delivery choices, acceptance and observed benefits.',
    3: 'Trace source needs, stakeholders and conflicting constraints into verifiable requirements, models and acceptance criteria.',
    4: 'Trace stakeholder concerns through viewpoints, design alternatives, correspondence rules and evidenced architecture decisions.',
    5: 'Trace required behaviour and security constraints to exact source changes, reproducible checks and independently reviewed results.',
    6: 'Use risk-based test or assessment methods with expected/actual results, coverage, sampling and bounded conclusions.',
    7: 'Trace data provenance, quality, meaning and permitted use; define model evaluation, uncertainty and operational monitoring where applicable.',
    8: 'Define measurable service objectives, capacity and dependency assumptions, failure behaviour, recovery and observed operational evidence.',
    9: 'Identify applicable protocol/technology editions, topology and trust assumptions, measurable network behaviour and compatibility evidence.',
    10: 'Distinguish service restoration, problem resolution, authorised change and receiving service acceptance with measured outcomes.',
    11: 'Separate observed events, detection coverage, analytic hypotheses, confidence and containment/recovery evidence.',
    12: 'Bind authorised scope and methodology to reproducible observations, impact, evidence limitations and retest results.',
    13: 'Separate binding obligation, interpretation, control, evidence, independent test and bounded assurance/risk conclusion.',
    14: 'Trace user research and accessibility requirements to findings, design choices and observed usability/accessibility evaluation.',
    15: 'Expose sourcing/pricing assumptions, obligations, economic sensitivities, acceptance responsibilities and exit conditions.',
    16: 'State hypotheses, success criteria and measurement methods before experiments; distinguish observed results, uncertainty and applicability limits.',
    17: 'Trace business drivers and measurable attributes through risks, control objectives, services, mechanisms and operational measures.',
}

FRAMEWORK_APPLICABILITY_CRITERIA = [
    'Identify only professional sources invoked by the conclusion or materially applicable obligations; a bibliography or a list of framework names is insufficient. Do not require every candidate framework for every task.',
    'For each record, identify source title, exact edition or dated revision and authoritative location; unavailable authoritative text remains pending and cannot support invented clause identifiers or clause-level conformance.',
    'State the basis as a normative legal/contractual requirement, organisational adoption, informative guidance or JAI interpretation; identify jurisdiction, scope and the authority/evidence establishing a binding duty.',
    'Record applicability as applicable, not applicable or pending, with a concrete rationale and context evidence. A record of no applicable external framework must explain the bounded task and its actual professional basis.',
    'Identify adopted concepts or verifiable requirement identifiers, tailoring, exclusions and precedence against law, customer obligations and organisation policy; tailoring cannot silently weaken an applicable mandatory obligation.',
    'Map each adopted concept or requirement to stable output information-unit references, the chosen method or practical procedure, required evidence and a concrete independent reviewer test. Cross-reference shared source records rather than duplicate them.',
    'Distinguish planned evidence from observed evidence and bounded guidance alignment from demonstrated conformance; unsupported conclusions and unavailable evidence remain pending.',
    'Name the accountable owner and change trigger for reassessing applicability, including relevant changes to scope, source edition, organisation policy or evidence. Reuse unchanged verified source records rather than rechecking immutable history at every workflow step.',
]

TYPE_DOMAINS = {
 **dict.fromkeys(['risk-assessment','assurance-report','control-design'],'security'),
 **dict.fromkeys(['architecture-definition','architecture-decision','solution-design','implementation-specification','diagram','model'],'architecture'),
 **dict.fromkeys(['test-strategy','test-report'],'testing'),
 **dict.fromkeys(['runbook','service-design','operational-readiness-assessment','configuration-baseline'],'operations'),
 **dict.fromkeys(['dataset','catalogue','register','dashboard'],'data'),
 **dict.fromkeys(['roadmap','business-case','decision-paper','benefits-review','migration-plan','cutover-plan','prototype','presentation','document'],'delivery'),
}

SABSA_REQUIREMENTS = {
 'architecture': [('architecture_cells','array','Map each selected Contextual/Conceptual/Logical/Physical/Component/Management perspective to its What/Why/How/Who/Where/When cell; Management applies across the other perspectives.'),('architecture_chain','array','Trace business drivers through attributes, objectives, services, mechanisms and operational measures.')],
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
    'analysis-report': [
        ('analysis_baseline', 'object', 'Define the actual analytical question, reporting period, population, source versions, method, measurement/reconciliation rules and exclusions.'),
        ('analysis_observations', 'array', 'Separate observed facts from hypotheses and assumptions; trace each material finding to reproducible evidence, calculations, chronology or source records with uncertainty and counterevidence.'),
        ('analysis_conclusion', 'object', 'Explain what the evidence supports, alternative explanations, limits, impacts and accountable follow-up actions. A factual or status report does not require a fabricated option appraisal or approval request.')],
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

# These references inform JAI's authored information contracts. A reference is
# not a claim of clause-level conformance, certification or permission to act.
PROFESSIONAL_REFERENCES = {
    'architecture-description': {
        'title': 'ISO/IEC/IEEE 42010:2022, Architecture description',
        'url': 'https://www.iso.org/standard/74393.html',
        'scope': 'Stakeholders, concerns, viewpoints, architecture views and correspondence.'},
    'systems-security-engineering': {
        'title': 'NIST SP 800-160 Volume 1 Revision 1, Engineering Trustworthy Secure Systems',
        'url': 'https://doi.org/10.6028/NIST.SP.800-160v1r1',
        'scope': 'Life-cycle requirements, design rationale, verification and assurance of system security.'},
    'risk-assessment': {
        'title': 'NIST SP 800-30 Revision 1, Guide for Conducting Risk Assessments',
        'url': 'https://doi.org/10.6028/NIST.SP.800-30r1',
        'scope': 'Assessment scope, threat events, vulnerabilities, likelihood, impact and uncertainty.'},
    'control-assessment': {
        'title': 'NIST SP 800-53A Revision 5, Assessing Security and Privacy Controls',
        'url': 'https://doi.org/10.6028/NIST.SP.800-53Ar5',
        'scope': 'Assessment objectives, methods, evidence, findings and bounded assessment conclusions.'},
    'secure-software': {
        'title': 'NIST SP 800-218, Secure Software Development Framework Version 1.1',
        'url': 'https://doi.org/10.6028/NIST.SP.800-218',
        'scope': 'Secure development practices, protected source/build inputs, verification and vulnerability response.'},
    'configuration-management': {
        'title': 'NIST SP 800-128, Guide for Security-Focused Configuration Management of Information Systems',
        'url': 'https://doi.org/10.6028/NIST.SP.800-128',
        'scope': 'Configuration baselines, controlled changes, impact analysis and monitoring.'},
    'contingency-planning': {
        'title': 'NIST SP 800-34 Revision 1, Contingency Planning Guide for Federal Information Systems',
        'url': 'https://doi.org/10.6028/NIST.SP.800-34r1',
        'scope': 'Recovery priorities, dependencies, recovery procedures, exercises and maintenance.'},
    'requirements-engineering': {
        'title': 'ISO/IEC/IEEE 29148:2018, Requirements engineering',
        'url': 'https://www.iso.org/standard/72089.html',
        'scope': 'Requirements information items, requirement quality and traceability.'},
    'software-testing': {
        'title': 'ISO/IEC/IEEE 29119-3:2021, Software testing — Test documentation',
        'url': 'https://www.iso.org/standard/79429.html',
        'scope': 'Test planning, test specifications and reporting information needs.'},
    'data-catalogue': {
        'title': 'W3C Data Catalog Vocabulary Version 3 (DCAT 3)',
        'url': 'https://www.w3.org/TR/vocab-dcat-3/',
        'scope': 'Dataset/catalogue identity, distributions, provenance, access and descriptive metadata.'},
    'data-quality': {
        'title': 'W3C Data Quality Vocabulary',
        'url': 'https://www.w3.org/TR/vocab-dqv/',
        'scope': 'Quality dimensions, metrics, measurements and quality annotations; this source is a Working Group Note.'},
    'accessibility': {
        'title': 'W3C Web Content Accessibility Guidelines (WCAG) 2.2',
        'url': 'https://www.w3.org/TR/WCAG22/',
        'scope': 'Perceivable and understandable content, text alternatives and accessible navigation; applicability depends on the delivered medium.'},
    'service-management': {
        'title': 'ISO/IEC 20000-1:2018, Service management system requirements',
        'url': 'https://www.iso.org/standard/70636.html',
        'scope': 'Service requirements, agreements, transition, operation and measurement concepts.'},
    'it-governance': {
        'title': 'COBIT governance and management framework',
        'url': 'https://www.isaca.org/resources/cobit',
        'scope': 'Enterprise information and technology objectives, accountability, performance and governance.'},
    'business-appraisal': {
        'title': 'HM Treasury, The Green Book',
        'url': 'https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government',
        'scope': 'Options, appraisal, costs, benefits, risk, uncertainty and evaluation; used as a practice reference outside its own jurisdiction.'},
    'sre-practice': {
        'title': 'Google Site Reliability Engineering, Service Level Objectives',
        'url': 'https://sre.google/sre-book/service-level-objectives/',
        'scope': 'Service indicators, objectives, measurement and error-budget interpretation; practitioner guidance, not a formal standard.'},
    'jai-practice': {
        'title': 'JAI authored enterprise-delivery practice',
        'url': None,
        'scope': 'Explicit scope, accountable recipients, evidence limits, usable handoffs and independent review.'},
}

TYPE_PROFESSIONAL_REFERENCES = {
    'architecture-definition': ['architecture-description'],
    'architecture-decision': ['architecture-description', 'systems-security-engineering'],
    'solution-design': ['architecture-description', 'systems-security-engineering'],
    'decision-paper': ['business-appraisal', 'it-governance'],
    'business-case': ['business-appraisal'],
    'risk-assessment': ['risk-assessment'],
    'assurance-report': ['control-assessment'],
    'control-design': ['systems-security-engineering', 'control-assessment'],
    'implementation-specification': ['secure-software', 'configuration-management'],
    'migration-plan': ['configuration-management', 'contingency-planning'],
    'cutover-plan': ['configuration-management', 'contingency-planning'],
    'operational-readiness-assessment': ['service-management', 'contingency-planning'],
    'service-design': ['service-management', 'sre-practice'],
    'runbook': ['contingency-planning', 'configuration-management'],
    'test-strategy': ['software-testing'],
    'test-report': ['software-testing'],
    'benefits-review': ['business-appraisal'],
    'roadmap': ['it-governance', 'business-appraisal'],
    'register': ['jai-practice'],
    'dashboard': ['sre-practice', 'data-quality'],
    'presentation': ['accessibility', 'jai-practice'],
    'dataset': ['data-catalogue', 'data-quality'],
    'catalogue': ['data-catalogue'],
    'document': ['jai-practice'],
    'diagram': ['architecture-description'],
    'model': ['architecture-description'],
    'prototype': ['secure-software', 'jai-practice'],
    'configuration-baseline': ['configuration-management'],
}

FAMILY_PROFESSIONAL_REFERENCES = {
    'analysis-report': ['jai-practice'],
    'adr': ['architecture-description', 'systems-security-engineering'],
    'hld': ['architecture-description', 'systems-security-engineering'],
    'operational-handover': ['service-management', 'contingency-planning'],
    'strategy': ['it-governance'],
    'release-notes': ['configuration-management', 'secure-software'],
    'requirements-specification': ['requirements-engineering'],
    'software-change': ['secure-software'],
    'automated-tests': ['software-testing', 'secure-software'],
    'deployment-automation': ['configuration-management', 'secure-software'],
}

# Acceptance statements refine existing semantic units without changing their
# identifiers or requiring a second representation of the same information.
TYPE_ACCEPTANCE_DETAILS = {
    'architecture-definition': [
        'Name the system of interest, boundary exclusions, stakeholder groups, each concern and the versioned current/target baseline.',
        'Identify each viewpoint and its conventions; trace each view to the concerns it addresses and identify cross-view correspondences and unresolved inconsistencies.',
        'For each material gap, identify current and target elements, business impact, owner, proposed response and the decision or evidence needed to close it.'],
    'architecture-decision': [
        'State one bounded decision question, its status, responsible decision maker, governing constraints and the exact design revision affected.',
        'Use the same explicit criteria for credible alternatives; record rejected options and why the no-change baseline is unsuitable or retained.',
        'Record expected consequences, validation needs, reversibility limits and superseded decision IDs; recommendation and recorded approval must remain distinguishable.'],
    'solution-design': [
        'For each component, state responsibility, interfaces, data owned, deployment placement and assumptions about external dependencies.',
        'For each interface, state producer/consumer, data semantics, authentication/trust boundary, failure/timeout behaviour and compatibility expectations.',
        'Link each material quality requirement to a measurable target, design response and planned verification; expose unresolved design tradeoffs.'],
    'decision-paper': [
        'Separate the requested decision from information for noting; state decision scope, eligible authority, deadline and consequences of deferral.',
        'List feasible options with consistent evaluation criteria, evidence, costs, benefits and constraints; justify any unavailable baseline.',
        'State recommendation, implementation dependencies, uncertainty and residual exposure; show which assumptions would change the preferred option.'],
    'business-case': [
        'State sponsor, financial owner, investment boundary, appraisal period and the precise funding or continuation decision requested.',
        'Show source and date of costs/benefits, currency, price basis, cash-flow periods, baseline and incremental treatment; avoid double-counted benefits.',
        'Identify key uncertain variables, sensitivity/scenario results, benefit measures, baseline, accountable realisation owner and review trigger.'],
    'risk-assessment': [
        'Define assessment scope, likelihood/impact scales, time horizon, risk criteria and appetite; explain how qualitative or quantitative ratings are assigned.',
        'For each scenario, record cause, event, affected asset/outcome, consequences, existing controls, evidence, uncertainty and a justified current/residual rating.',
        'For each treatment, record the scenario ID, chosen response, action owner, target date, expected risk change and authority required for residual acceptance.'],
    'assurance-report': [
        'State assessment objectives, criteria versions, scope, period, population, sample rationale and exclusions before drawing conclusions.',
        'For each criterion, identify procedure, sample, observed result, supporting material and located deviations; distinguish absent evidence from demonstrated failure.',
        'Bound the conclusion by coverage and limitations; list findings, severity rationale, management response, remediation owner and verification needed for closure.'],
    'control-design': [
        'Trace each control objective to a risk or obligation and identify accountable owner, protected outcome and operating scope.',
        'Specify trigger, actor/system, required inputs, action, expected observable result, exceptions and response when the control fails.',
        'Define design/operating-effectiveness checks, population or sampling, expected evidence, acceptance threshold and disposition of exceptions.'],
    'implementation-specification': [
        'Identify exact component/environment versions and each required parameter with type, unit, permitted range, default and secret-reference handling.',
        'State interface schemas, input/output semantics, error responses, concurrency/idempotency expectations and external dependency constraints.',
        'Give reproducible build/deploy/verification steps, expected results, stop conditions and recovery path; identify evidence still required before execution.'],
    'migration-plan': [
        'Inventory source/target versions, data classes, owners, interfaces, dependencies and mapping or transformation rules.',
        'For each wave, identify entry criteria, ordered activities, resource/window assumptions, reconciliation measures and receiving acceptance.',
        'State integrity checks, recovery points, fallback decision authority, latest safe reversal point and continuity arrangements for an unsuccessful wave.'],
    'cutover-plan': [
        'For every activity, identify sequence/dependencies, operator, target, window, expected result and completion criterion.',
        'State go/no-go criteria and authority, communications, evidence needed at each checkpoint and any point of no return.',
        'Define reversal or forward-recovery branches, decision deadlines, data reconciliation and observable safe-state criteria; distinguish rehearsed from untested actions.'],
    'operational-readiness-assessment': [
        'Define service boundary and named receiving operations owner; enumerate support, access, monitoring, capacity, resilience and security readiness criteria.',
        'Record evidence and disposition for each applicable criterion, including missing/unexecuted checks, impact and remediation accountability.',
        'Separate readiness recommendation from deployment permission; identify unresolved risks, receiving acceptance conditions and early-life support exit criteria.'],
    'service-design': [
        'State service consumers, business outcomes, eligibility, service boundary, exclusions, accountable owner and demand assumptions.',
        'For every service level, define indicator, unit, measurement source/window, target, exclusions and breach response; label unagreed targets as proposals.',
        'Define support tiers, ownership, supplier/interface dependencies, change/incident escalation, recovery objectives and cost assumptions.'],
    'runbook': [
        'State when the procedure applies, exact targets, permitted operator capability, prerequisites, access dependencies and conditions forbidding execution.',
        'For each step, give the action, parameters, expected observation and a decision on success/failure; do not embed credentials.',
        'Define failure/timeout branches, rollback or safe recovery, escalation conditions and evidence of rehearsal against a named version/environment.'],
    'test-strategy': [
        'Identify product/build scope, critical requirements, quality risks, excluded risks and the confidence the selected tests can and cannot provide.',
        'Map risks to levels, techniques and responsibilities; specify environment, representative data, dependencies and expected evidence.',
        'Define measurable entry/exit criteria, coverage interpretation, triage/retest rules and treatment of blocked or unexecuted cases.'],
    'test-report': [
        'Identify exact tested build, requirements baseline, environment/data versions, test period and deviations from the plan.',
        'State passed, failed, blocked and unexecuted cases with evidence references; give denominators and traceability so counts cannot disguise missing coverage.',
        'Summarise defects by business impact, unmet exit criteria, untested risks and limitations; separate a release recommendation from release authorisation.'],
    'benefits-review': [
        'State each committed benefit, baseline, target, measure, realisation owner and measurement window.',
        'Compare observed results with the baseline/counterfactual, reconcile data sources and attribution, and explain uncertainty and double-counting controls.',
        'Explain material variances, corrective options, decision owners, follow-up dates and accountability for benefits not yet realised.'],
    'roadmap': [
        'State business outcomes, current/target baseline, planning horizons, sponsors and material planning assumptions.',
        'For each increment, identify deliverables, owner, indicative resource/funding requirement, milestone and measurable completion outcome.',
        'Identify dependencies and critical sequence, decision dates, constraints and alternative paths; distinguish committed work from tentative options.'],
    'register': [
        'Define the purpose-specific record type, required fields, datatypes, unique key, allowed states, owner and lifecycle rules.',
        'Populate records with actual subject-specific values, source references, state, accountable owner and relevant review/change trigger; explain an empty population.',
        'Identify duplicate, missing, stale or inconsistent records and unresolved references; report checks and remediation without claiming unsupported completeness.'],
    'dashboard': [
        'For each metric, define question, formula, unit, population/denominator, time window, target/threshold and accountable owner.',
        'Show observation timestamp, source/query version, aggregation, missing-data handling and measurement limitations.',
        'Explain threshold crossings and trends, uncertainty and the action or decision supported; distinguish operational signals from causal explanations.'],
    'presentation': [
        'State intended audience, specific decision or learning objective, scope and requested next action.',
        'Present a coherent argument linking claims to evidence, alternatives, limitations and the recommendation; do not replace analysis with slogans.',
        'Make visuals and reading order understandable; give meaningful labels/text alternatives and links to supporting details appropriate to the delivered medium.'],
    'dataset': [
        'Specify field names, meaning, type, units, code lists, keys, relationships, null semantics and permitted values.',
        'Identify source systems/extract versions, transformations, time coverage, access/licensing conditions and accountable custodian.',
        'Report completeness, validity, consistency and other relevant quality measures with method, population, results and known limitations.'],
    'catalogue': [
        'Define the catalogued entity type, unique identifier, classification, required descriptive fields and inclusion/exclusion rules.',
        'Provide usable entries with owner, state, source/version, discovery/access reference and relevant service or dependency relationships.',
        'Check identifiers, required metadata, broken references, duplicates and lifecycle status; name unresolved gaps and responsible maintainers.'],
    'document': [
        'State the exact subject, intended recipient/use, boundary, source versions and the concrete question the document answers.',
        'Provide subject-specific findings or instructions with supporting facts, assumptions, reasoning, limitations and traceable references; generic background alone is insufficient.',
        'State conclusions, decisions requested or actionable instructions, accountable recipients and completion/acceptance conditions; identify open issues explicitly.'],
    'diagram': [
        'Identify diagram purpose, scope, audience, version and notation/legend, including the meaning of every relationship type.',
        'Use stable element identifiers and meaningful labels; show relevant boundaries, directions, interfaces and external dependencies without invented facts.',
        'Check consistency with source models and related views; distinguish intentional abstraction from omitted or unresolved relationships.'],
    'model': [
        'Define model purpose, boundary, entity/relation types, semantics, constraints and authoritative source versions.',
        'Populate stable identified entities and typed relationships with ownership/provenance; relate each model view to its intended question.',
        'Report referential and constraint checks, cross-view consistency and unresolved modelling assumptions; an attractive diagram alone does not establish validity.'],
    'prototype': [
        'State the hypothesis or feasibility question, experiment boundary, success/failure criteria and limitations of representativeness.',
        'Identify reproducible prototype source/configuration, dependencies, environment and procedure without claiming production readiness.',
        'Record actual observations against criteria, failed/untested conditions and what may or may not be inferred for a production solution.'],
    'configuration-baseline': [
        'Identify managed components, exact versions, environments, approved parameter values, exceptions and configuration owner without exposing secrets.',
        'Describe how the baseline is created/applied, validated and changed, including dependencies and recovery from an unsuccessful change.',
        'Compare observed configuration with the declared baseline, classify drift, identify material impact and record authorised remediation or unresolved exceptions.'],
}

FAMILY_ACCEPTANCE_DETAILS = {
    'analysis-report': [
        'State scope, precise question, method, period and source/population boundaries; disclose missing data, selection bias and the limits of the measurement or investigative method.',
        'For each finding, link source and exact observation or calculation, distinguish event chronology from causal inference, and expose counterevidence, uncertainty and unsupported hypotheses.',
        'Bound conclusions by the observations, specify recipient actions and unresolved questions, and distinguish recommendations from actual decisions. Do not invent a do-nothing baseline or two alternatives merely to package an operational, research or investigative report.'],
    'strategy': [
        'State measurable target outcomes, their baselines, planning horizon, business drivers and the constraints that rule options in or out.',
        'Compare coherent strategic options and no-change consequences with resource, dependency and uncertainty assumptions visible.',
        'Identify sequenced initiatives, decision points, accountable outcome owners and measures/triggers for revisiting the strategy.'],
    'release-notes': [
        'Name exact released and predecessor versions, affected products, applicable installation paths and intended recipients.',
        'Distinguish new features, fixes, breaking changes, compatibility limits and known defects; link each material item to a change record.',
        'State user/operator actions, upgrade prerequisites, data/configuration implications and recovery limitations; distinguish required actions from optional features.'],
    'requirements-specification': [
        'Identify stakeholder/source, need, scope boundary, authoritative baseline and assumptions for each requirement group.',
        'Each requirement has a stable ID, one unambiguous obligation, rationale, priority and observable verification method/threshold; quantify units and operating conditions.',
        'Trace requirements to sources and planned verification, identify dependencies/conflicts and define who resolves gaps or authorises baseline changes.'],
    'software-change': [
        'Identify the exact revision, changed behaviour/interfaces and requirements or defects addressed; distinguish source completion from merge or deployment status.',
        'Reference reproducible checks and actual observed results, independent review findings, test exclusions and unresolved defects.',
        'Define compatibility, telemetry/failure signals and rollback or forward-recovery constraints for the actual changed components.'],
    'automated-tests': [
        'Each executable case identifies the covered behaviour/risk, deterministic setup/data, stimulus, expected assertion and relevant environment assumptions.',
        'Give the command, required dependencies and failure diagnostics; distinguish a case definition from an observed execution result for an exact product revision.',
        'Define test isolation and cleanup, treatment of nondeterminism/flakiness, maintenance responsibilities and explicit gaps that coverage metrics cannot establish.'],
    'deployment-automation': [
        'Identify immutable build inputs, target environments, parameter contracts, prerequisite permissions and externally supplied secret references.',
        'Define stage dependencies, expected postconditions, failure/timeout handling, idempotency or retry constraints and safe recovery.',
        'Reference reproducible checks of target selection, configuration, error/recovery paths and actual execution where performed; planned automation is not evidence of production deployment.'],
}

# Exact authored assignments correct professional meaning where a broad storage
# modality otherwise misrepresents a requirement baseline or executable output.
SEMANTIC_REFINEMENTS.update({
    'systems-analyst:1': 'requirements-specification',
    'requirements-engineer:1': 'requirements-specification',
    'test-manager:1': 'test-strategy',
    'performance-test-engineer:1': 'test-strategy',
    'performance-test-engineer:2': 'test-report',
    'test-analyst:4': 'test-report',
    'linux-systems-administrator:1': 'configuration-baseline',
    'linux-systems-administrator:2': 'assurance-report',
    'linux-systems-administrator:3': 'test-report',
    'windows-systems-administrator:1': 'configuration-baseline',
    'windows-systems-administrator:2': 'assurance-report',
    'windows-systems-administrator:3': 'register',
    'windows-systems-administrator:4': 'test-report',
    'cloud-engineer:1': 'deployment-automation',
    'cloud-engineer:2': 'deployment-automation',
    'cloud-engineer:3': 'configuration-baseline',
    'cloud-engineer:4': 'assurance-report',
    'infrastructure-as-code-engineer:1': 'deployment-automation',
    'infrastructure-as-code-engineer:2': 'configuration-baseline',
    'infrastructure-as-code-engineer:3': 'control-design',
    'infrastructure-as-code-engineer:4': 'assurance-report',
    'site-reliability-engineer:1': 'service-design',
})

# Explicit engineering assignments cover executable products and configuration,
# not a runtime classifier based on words in deliverable names. Research/UX
# prototypes remain feasibility or interaction artefacts unless separately mapped.
SEMANTIC_REFINEMENTS.update({
    'senior-software-engineer:1': 'software-change',
    'backend-engineer:1': 'software-change',
    'backend-engineer:2': 'software-change',
    'backend-engineer:3': 'automated-tests',
    'frontend-engineer:1': 'software-change',
    'frontend-engineer:2': 'automated-tests',
    'frontend-engineer:3': 'test-report',
    'full-stack-engineer:1': 'software-change',
    'full-stack-engineer:2': 'automated-tests',
    'mobile-engineer:1': 'software-change',
    'mobile-engineer:3': 'software-change',
    'embedded-firmware-engineer:1': 'software-change',
    'embedded-firmware-engineer:2': 'software-change',
    'embedded-firmware-engineer:4': 'software-change',
    'real-time-systems-engineer:3': 'test-report',
    'systems-programmer:1': 'software-change',
    'systems-programmer:3': 'test-report',
    'mainframe-developer:1': 'software-change',
    'mainframe-developer:2': 'deployment-automation',
    'mainframe-developer:3': 'software-change',
    'mainframe-developer:4': 'test-report',
    'api-developer:1': 'software-change',
    'api-developer:4': 'automated-tests',
    'integration-developer:1': 'software-change',
    'integration-developer:3': 'implementation-specification',
    'erp-and-crm-consultant-developer:2': 'software-change',
    'erp-and-crm-consultant-developer:4': 'software-change',
    'low-code-and-rpa-developer:1': 'software-change',
    'game-developer:1': 'software-change',
    'game-developer:4': 'software-change',
    'graphics-and-engine-engineer:1': 'software-change',
    'blockchain-and-smart-contract-developer:1': 'software-change',
    'blockchain-and-smart-contract-developer:2': 'test-report',
    'quantitative-developer:1': 'software-change',
    'quantitative-developer:2': 'test-report',
    'quantitative-developer:3': 'test-report',
    'compiler-and-toolchain-engineer:1': 'software-change',
    'compiler-and-toolchain-engineer:2': 'automated-tests',
    'compiler-and-toolchain-engineer:3': 'test-report',
    'build-engineer:1': 'configuration-baseline',
    'build-engineer:4': 'test-report',
    'ci-cd-platform-engineer:1': 'deployment-automation',
    'ci-cd-platform-engineer:4': 'configuration-baseline',
    'gitops-and-continuous-delivery-engineer:2': 'configuration-baseline',
    'gitops-and-continuous-delivery-engineer:4': 'deployment-automation',
    'developer-experience-engineer:1': 'software-change',
    'developer-experience-engineer:3': 'configuration-baseline',
    'software-modernisation-engineer:2': 'automated-tests',
    'software-modernisation-engineer:3': 'software-change',
    'data-engineer:1': 'software-change',
    'data-engineer:3': 'automated-tests',
    'database-administrator:2': 'test-report',
    'database-reliability-engineer:1': 'deployment-automation',
    'database-reliability-engineer:2': 'service-design',
    'data-custodian:3': 'configuration-baseline',
    'master-data-management-specialist:3': 'configuration-baseline',
    'data-scientist:1': 'software-change',
    'machine-learning-engineer:1': 'software-change',
    'machine-learning-engineer:3': 'test-report',
    'mlops-engineer:1': 'deployment-automation',
    'llmops-and-ai-platform-engineer:1': 'configuration-baseline',
    'llmops-and-ai-platform-engineer:2': 'automated-tests',
    'llmops-and-ai-platform-engineer:3': 'configuration-baseline',
    'ai-solutions-engineer:1': 'software-change',
    'ai-solutions-engineer:3': 'test-report',
    'data-privacy-engineer:1': 'software-change',
    'data-privacy-engineer:2': 'software-change',
    'data-privacy-engineer:3': 'deployment-automation',
    'data-privacy-engineer:4': 'assurance-report',
    'platform-engineer:2': 'software-change',
    'platform-engineer:4': 'software-change',
    'site-reliability-engineer:4': 'software-change',
    'container-platform-engineer:3': 'configuration-baseline',
    'storage-engineer:3': 'configuration-baseline',
    'backup-and-recovery-engineer:4': 'configuration-baseline',
    'finops-engineer:2': 'software-change',
    'network-engineer:1': 'configuration-baseline',
    'wireless-and-rf-engineer:3': 'configuration-baseline',
    'unified-communications-engineer:1': 'configuration-baseline',
    'dns-dhcp-and-ipam-specialist:2': 'configuration-baseline',
    'dns-dhcp-and-ipam-specialist:4': 'configuration-baseline',
    'identity-and-access-management-engineer:1': 'configuration-baseline',
    'identity-and-access-management-engineer:3': 'deployment-automation',
    'cloud-security-engineer:3': 'configuration-baseline',
    'application-security-engineer:2': 'configuration-baseline',
    'design-system-engineer:1': 'software-change',
    'developer-advocate:1': 'software-change',
    'privacy-analyst:1': 'risk-assessment',
})

PROFESSIONAL_REFERENCES['eu-gdpr'] = {
    'title': 'Regulation (EU) 2016/679, Article 35 — Data protection impact assessment',
    'url': 'https://eur-lex.europa.eu/eli/reg/2016/679/oj',
    'scope': 'Article 35 assessment content and accountability where EU GDPR applies; engagement-specific legal applicability and competent interpretation must be established.'}

# These obligations refine particular professional outputs whose actual subject
# is not adequately specified by their former broad modality or a generic gate.
CONTRACT_CONTENT_REQUIREMENTS = {
    'privacy-analyst:1': [
        ('processing_description', 'object', 'Describe the envisaged processing operations, purposes, categories of data/subjects, recipients, retention and relevant data flows; identify controller and applicable jurisdiction.'),
        ('necessity_proportionality', 'object', 'Assess necessity and proportionality of processing in relation to its purpose, less intrusive alternatives and data-minimisation/retention choices using the actual proposal.'),
        ('data_subject_risks', 'array', 'Describe risks to the rights and freedoms of affected people, including who may be harmed, likelihood, severity, assumptions and supporting evidence; business risk alone is insufficient.'),
        ('privacy_safeguards', 'array', 'Map each material rights/freedoms risk to proposed safeguards, responsible owner, verification evidence and remaining exposure; record DPO advice where sought and any decision or consultation still required without implying permission to process.')],
    'chief-information-officer:4': [
        ('budget_baseline', 'object', 'State financial year, currency, price/assumption basis, planning scope, accountable budget owner and reconciliation to the current approved baseline.'),
        ('budget_allocation', 'array', 'Identify expenditure lines by service/initiative and accountable owner, distinguishing capital/operating and one-off/recurring cost where relevant; state amount, timing, funding source and material dependencies.'),
        ('budget_reconciliation', 'object', 'Reconcile allocation totals to the requested envelope and financial periods; show forecast/commitment assumptions, material variances, contingency and the decisions needed for an unfunded or over-budget plan.')],
    'contract-manager:3': [
        ('binding_obligation_baseline', 'array', 'Identify the executed contract/version, applicable clause or obligation ID, accountable party, effective/due dates and agreed measurable acceptance or performance threshold; distinguish proposed terms from binding obligations.'),
        ('obligation_observations', 'array', 'For each obligation due in the reporting period, link actual performance/delivery evidence, measurement period and status; separate met, breached, disputed, not yet due and insufficient-evidence cases.'),
        ('obligation_remedies', 'array', 'For each material deviation, identify impact, notice/cure deadlines, contractually available remedies, escalation owner and required legal/commercial decision; do not invent a right, waive an obligation or claim a dispute resolved without authority.')],
    'blockchain-and-smart-contract-developer:2': [
        ('verification_properties', 'array', 'Identify exact contract/source and deployment/compiler assumptions, security or functional properties, threat model, entry conditions and excluded behaviours for the selected verification method.'),
        ('verification_method_limits', 'object', 'For formal verification, state specification, assumptions/axioms, proof obligations, tool/version and unresolved obligations or counterexamples. For property-based testing, state generators, domains, seeds/shrinking, invariant assertions and execution limits; sampled tests do not establish a universal proof.'),
        ('verification_outcome', 'array', 'Link each claimed property to actual proof/check/test output for the exact version, reproducible invocation, failure/counterexample details and residual uncertainty; tool success does not establish correctness beyond the stated model and assumptions.')],
}

CONTRACT_PROFESSIONAL_REFERENCES = {
    'privacy-analyst:1': ['eu-gdpr', 'risk-assessment'],
    'chief-information-officer:4': ['business-appraisal', 'it-governance'],
    'contract-manager:3': ['jai-practice'],
    'blockchain-and-smart-contract-developer:2': ['systems-security-engineering', 'software-testing'],
}

CONTRACT_CONTENT_REQUIREMENTS.update({
    'it-financial-management-tbm-manager:1': [
        ('cost_model_boundary', 'object', 'State model purpose, service/portfolio boundary, accounting period, currency and price basis, source ledger extracts and accountable financial owner; identify actuals, commitments and forecasts separately.'),
        ('cost_allocation_model', 'array', 'Define the selected cost taxonomy, source cost pools, allocation drivers, units, formulas and mappings through resources/services to consuming products or business units; disclose shared, unallocated and excluded costs.'),
        ('cost_reconciliation_sensitivity', 'object', 'Reconcile source totals to allocated outputs without double counting; identify rounding, missing inputs and material assumptions, and show how uncertain volumes/rates affect unit costs and proposed decisions.')],
    'commercial-pricing-deal-finance-specialist:1': [
        ('deal_model_assumptions', 'array', 'Identify the exact deal scenario, term, currency, price/escalation basis, volumes, staffing/productivity, rates, tax/working-capital assumptions where applicable, source and accountable assumption owner.'),
        ('deal_model_calculations', 'array', 'Provide inspectable formulas linking assumptions to delivery costs, supplier/customer cash-flow timing, revenues, margin and funding exposure; identify units, period granularity and calculation dependencies rather than supplying unexplained totals.'),
        ('deal_model_controls', 'object', 'Reconcile detailed schedules and totals, expose formula/input inconsistencies and run sensitivity scenarios for material volume, timing, cost and collection assumptions; separate a modelled outcome from an approved price or commitment.')],
    'contract-manager:1': [
        ('contract_repository_identity', 'array', 'Identify contracting parties, operative signed contract/version, applicable jurisdiction or governing-law reference, effective/expiry dates and authoritative record location; preserve draft and superseded status explicitly.'),
        ('contract_obligation_records', 'array', 'For each tracked obligation, identify contract/clause, responsible party and owner, deliverable or performance measure, due/renewal/notice dates, dependencies, acceptance evidence and current status.'),
        ('contract_lifecycle_integrity', 'object', 'Define access/classification, authorised variation links, renewal/termination triggers and reconciliation of the obligation register with operative contract versions; expose missing documents or unresolved interpretations.')],
    'contract-manager:4': [
        ('dispute_factual_record', 'array', 'Identify dispute/claim ID, parties, operative contract/clause and relevant governing-law reference, asserted event, dated chronology, evidence, amounts/remedies claimed and disputed versus agreed facts.'),
        ('notice_remedy_control', 'array', 'Record applicable contractual notice/cure/escalation deadlines, required delivery method, notices actually issued, rights reserved, proposed remedies and accountable commercial/legal owners; do not fabricate authority or a legal entitlement.'),
        ('dispute_disposition', 'object', 'Record positions, negotiation/decision status, authorised settlement or remedy where actually agreed, outstanding actions, implementation evidence and closure conditions; a recommendation is not an executed settlement.')],
})

CONTRACT_PROFESSIONAL_REFERENCES.update({
    'it-financial-management-tbm-manager:1': ['business-appraisal', 'jai-practice'],
    'commercial-pricing-deal-finance-specialist:1': ['business-appraisal', 'jai-practice'],
    'contract-manager:1': ['jai-practice'],
    'contract-manager:4': ['jai-practice'],
})

# Professional-fit corrections are exact contract assignments; legacy modality
# remains unchanged for compatibility and never selects these obligations.
SEMANTIC_REFINEMENTS.update({
    'accessibility-specialist:1': 'document',
    'accessibility-specialist:2': 'assurance-report',
    'accessibility-tester:2': 'document',
    'ai-governance-officer:3': 'document',
    'ai-safety-and-model-red-team-specialist:4': 'assurance-report',
    'ai-solutions-engineer:4': 'control-design',
    'backup-and-recovery-engineer:2': 'assurance-report',
    'binary-reverse-engineer:4': 'software-change',
    'business-relationship-manager:2': 'register',
    'chaos-and-resilience-engineer:1': 'document',
    'ci-cd-platform-engineer:3': 'hld',
    'ci-cd-platform-engineer:4': 'configuration-baseline',
    'cloud-architect:1': 'hld',
    'cloud-architect:2': 'hld',
    'content-designer:4': 'document',
    'control-owner:1': 'control-design',
    'control-tester:1': 'document',
    'control-tester:2': 'assurance-report',
    'control-tester:4': 'assurance-report',
    'data-architect:3': 'model',
    'data-privacy-engineer:4': 'assurance-report',
    'design-system-engineer:2': 'configuration-baseline',
    'disaster-recovery-coordinator:2': 'assurance-report',
    'environment-manager:3': 'runbook',
    'finops-engineer:1': 'software-change',
    'frontend-engineer:4': 'test-report',
    'game-developer:2': 'test-report',
    'grc-analyst:1': 'register',
    'information-architect:2': 'model',
    'information-architect:4': 'document',
    'integration-developer:2': 'implementation-specification',
    'localisation-qa-analyst:1': 'test-report',
    'low-code-and-rpa-developer:2': 'document',
    'network-architect:1': 'hld',
    'network-architect:3': 'hld',
    'network-engineer:2': 'configuration-baseline',
    'penetration-tester-mobile:4': 'assurance-report',
    'penetration-tester-network-and-infrastructure:2': 'assurance-report',
    'penetration-tester-network-and-infrastructure:4': 'assurance-report',
    'penetration-tester-web-application:4': 'assurance-report',
    'privacy-analyst:4': 'document',
    'privileged-access-management-administrator:4': 'runbook',
    'product-analyst:2': 'document',
    'product-designer:1': 'strategy',
    'product-designer:2': 'document',
    'product-designer:3': 'document',
    'product-designer:4': 'document',
    'project-manager:1': 'roadmap',
    'real-time-systems-engineer:1': 'hld',
    'release-engineer:4': 'runbook',
    'request-fulfilment-manager:4': 'register',
    'requirements-engineer:3': 'document',
    'research-scientist:1': 'document',
    'sd-wan-and-edge-engineer:2': 'hld',
    'secrets-and-configuration-management-engineer:2': 'hld',
    'security-architect:3': 'hld',
    'security-architect:4': 'requirements-specification',
    'security-champion:2': 'assurance-report',
    'security-domain-authority:1': 'document',
    'service-designer:2': 'service-design',
    'solution-architect:2': 'hld',
    'solution-architect:3': 'requirements-specification',
    'staff-engineer:3': 'prototype',
    'standards-body-representative:3': 'document',
    'technical-design-authority-member:1': 'assurance-report',
    'technical-product-manager:4': 'requirements-specification',
    'technical-recruiter:2': 'roadmap',
    'test-architect:2': 'test-strategy',
    'third-party-risk-manager:3': 'document',
    'threat-intelligence-analyst:1': 'document',
    'usability-tester:4': 'document',
    'ux-designer:1': 'document',
    'ux-designer:4': 'document',
    'vulnerability-disclosure-coordinator:1': 'document',
})

# Policies, practice standards and schedules describe governance obligations,
# not component parameters or deployment instructions.
SEMANTIC_REFINEMENTS.update({
    'policy-author:1': 'document',
    'policy-author:2': 'document',
    'policy-author:4': 'roadmap',
    'it-governance-manager:3': 'document',
    'pmo-lead:1': 'document',
    'knowledge-manager:1': 'document',
})

# Complete remaining implementation-family merit review: standards/policies are
# not component build specifications; exact technical products retain their duties.
SEMANTIC_REFINEMENTS.update({
    'ai-governance-officer:4': 'document',
    'api-developer:2': 'requirements-specification',
    'application-security-engineer:1': 'document',
    'bug-bounty-programme-manager:1': 'document',
    'build-engineer:3': 'document',
    'change-manager:4': 'document',
    'chief-information-security-officer:2': 'document',
    'cloud-security-engineer:1': 'configuration-baseline',
    'configuration-manager:1': 'document',
    'container-platform-engineer:2': 'document',
    'container-platform-engineer:4': 'document',
    'cryptography-and-pki-engineer:4': 'document',
    'data-architect:4': 'document',
    'data-governance-lead:2': 'document',
    'data-modeller:4': 'document',
    'data-owner:2': 'document',
    'database-reliability-engineer:3': 'software-change',
    'domain-architect:4': 'document',
    'environment-manager:4': 'document',
    'gitops-and-continuous-delivery-engineer:3': 'document',
    'high-performance-computing-engineer:1': 'configuration-baseline',
    'integration-architect:2': 'document',
    'integration-developer:3': 'requirements-specification',
    'interaction-designer:1': 'requirements-specification',
    'it-procurement-specialist:1': 'document',
    'kubernetes-platform-engineer:2': 'configuration-baseline',
    'network-architect:4': 'document',
    'observability-engineer:1': 'software-change',
    'observability-engineer:4': 'document',
    'open-source-program-office-engineer:1': 'document',
    'performance-test-engineer:4': 'dataset',
    'physical-security-solution-builder-sabsa-builder-s-view:2': 'hld',
    'purple-team-lead:4': 'document',
    'sd-wan-and-edge-engineer:3': 'configuration-baseline',
    'staff-engineer:4': 'document',
    'technical-lead:3': 'document',
    'technical-product-manager:2': 'requirements-specification',
    'vp-of-engineering:3': 'document',
})

# Operational automation and noncoding designs are not research-code experiments.
# Explicit experimental-code products retain the existing prototype foundation.
SEMANTIC_REFINEMENTS.update({
    'adversary-emulation-engineer:2': 'software-change',
    'end-user-computing-engineer:3': 'deployment-automation',
    'interaction-designer:4': 'document',
    'machine-learning-engineer:2': 'configuration-baseline',
    'machine-learning-engineer:4': 'software-change',
    'mlops-engineer:3': 'software-change',
    'mobile-engineer:4': 'document',
    'security-engineer:1': 'configuration-baseline',
    'service-designer:4': 'document',
})

# Exact professional corrections preserve the frozen storage contract while
# choosing the substantive output family used by authors and reviewers.
from professional_output_refinements import (
    OUTPUT_REFINEMENTS, OUTPUT_REQUIREMENTS, OUTPUT_REFERENCES,
    ADDITIONAL_REFERENCES,
)

SEMANTIC_REFINEMENTS.update(OUTPUT_REFINEMENTS)
CONTRACT_CONTENT_REQUIREMENTS.update(OUTPUT_REQUIREMENTS)
CONTRACT_PROFESSIONAL_REFERENCES.update(OUTPUT_REFERENCES)
PROFESSIONAL_REFERENCES.update(ADDITIONAL_REFERENCES)
PROFESSIONAL_REFERENCES.update({
    'human-centred-design': {
        'title': 'ISO 9241-210:2019, Human-centred design for interactive systems',
        'url': 'https://www.iso.org/standard/77520.html',
        'scope': 'Human-centred design principles and life-cycle activities; public abstract is a basis for candidate selection, not clause-level assessment.'},
    'ai-risk-management': {
        'title': 'NIST AI 100-1, Artificial Intelligence Risk Management Framework (AI RMF 1.0)',
        'url': 'https://doi.org/10.6028/NIST.AI.100-1',
        'scope': 'Voluntary GOVERN, MAP, MEASURE and MANAGE functions for AI risks; applicability and adopted practices require explicit contextual selection.'},
    'internet-standards-process': {
        'title': 'IETF RFC 2026, The Internet Standards Process — Revision 3',
        'url': 'https://www.rfc-editor.org/rfc/rfc2026',
        'scope': 'Distinguishing standards-track status and specification maturity; select the actual applicable protocol RFCs and their updates rather than treating the process document as a network design standard.'},
    'research-reproducibility': {
        'title': 'ACM Artifact Review and Badging policy',
        'url': 'https://www.acm.org/publications/policies/artifact-review-and-badging-current',
        'scope': 'Artifact availability, evaluation and reproducibility terminology; informative evidence-pack practice, not proof that an experiment is scientifically sufficient.'},
    'sabsa-overview': {
        'title': 'SABSA Institute, SABSA Executive Summary',
        'url': 'https://sabsa.org/sabsa-executive-summary/',
        'scope': 'Business-driven security architecture and traceability overview; actual SABSA deliveries must select the accessible authoritative method/version and their detailed obligations.'},
})
