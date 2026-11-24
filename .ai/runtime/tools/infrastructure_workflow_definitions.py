# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Source-owned infrastructure paths for the existing governed workflows."""

READINESS = 'design-to-operational-readiness'
PRODUCTION = 'production-change'

# A scoped rehearsal leads to the existing readiness, change and service
# receiving duties. Production execution uses its separately governed workflow.
VARIANTS = {
    READINESS: [
        ('zero-trust-migration', 'Existing hybrid network transition',
         'Versioned inventory, observed dependencies, policy and independently measured reversal evidence.'),
    ],
}
PATH_STEPS = {}
MECHANISMS = {}
REQUIREMENTS = {}
EVIDENCE = {}

def _register(workflow, selector, stages):
    for step, role, outputs, record, fields, criterion, identity, predecessor in stages:
        REQUIREMENTS[workflow, step, selector] = (
            record, fields, criterion, [f'{role}:{number}' for number in outputs], role)
        path = 'normal/' + selector if workflow == PRODUCTION else selector
        EVIDENCE[workflow, path, step] = ('handoff_' + record, identity.split(), predecessor)


_register(READINESS, 'zero-trust-migration', [
    (1, 'network-architect', (1,), 'network_baseline',
     'estate_id identities devices workloads resources observed_flows dependencies owners observation_limits verification_scope',
     'Record the exact existing estate, observations, ownership and unresolved dependencies before design.', 'estate_id verification_scope', None),
    (2, 'security-architect', (1,), 'zero_trust_target',
     'estate_id baseline_ref requirements trust_assumptions policy_decisions enforcement_points access_criteria verification_scope',
     'Trace requirements and enforcement decisions to the accepted inventory and observed dependencies.', 'estate_id baseline_ref verification_scope', 'baseline_ref'),
    (3, 'network-engineer', (2,), 'transition_candidate',
     'estate_id baseline_ref design_ref waves coexistence exceptions continuity_limits reversal change_scope verification_scope',
     'Supply a staged candidate with named exception owners and expiry, halt thresholds and scoped reversal.', 'estate_id baseline_ref verification_scope', 'design_ref'),
    (4, 'security-assurance-and-measurement-architect', (3,), 'transition_observations',
     'estate_id baseline_ref candidate_ref allowed_paths denied_paths mandatory_dependencies readiness reversal verification_scope',
     'Independently observe permitted and denied flows, establish mandatory dependency coverage and prove recovery.', 'estate_id baseline_ref verification_scope', 'candidate_ref'),
    (5, 'service-transition-and-operational-readiness-manager', (1,), 'transition_readiness',
     'estate_id baseline_ref observations_ref continuity_verdict unresolved_items support_owner',
     'Accept readiness only after reviewing candidate observations and establishing accountable support.', 'estate_id baseline_ref', 'observations_ref'),
    (6, 'change-manager', (1,), 'transition_change_route',
     'estate_id baseline_ref readiness_ref change_record authority_scope window stop_conditions',
     'Identify the change and its exact approval route, scope and halt criteria. Apply production authority in the governed change path.', 'estate_id baseline_ref', 'readiness_ref'),
    (7, 'it-service-owner', (1,), 'transition_operational_handover',
     'estate_id baseline_ref change_route_ref named_owner monitoring recovery_obligations exceptions',
     'Receive the qualified transition package, ownership, monitoring, exceptions and reversal responsibilities.', 'estate_id baseline_ref', 'change_route_ref'),
])

VARIANTS[READINESS] += [
    ('zero-trust-greenfield', 'Requirements-led Zero Trust design',
     'Attributable requirements, candidate enforcement design and independent verification of design coverage.'),
    ('zero-trust-assessment', 'Independent existing Zero Trust or hybrid estate assessment',
     'Commissioned scope, actual control observations, evidence gaps and prioritized remediation.'),
]
PATH_STEPS[READINESS, 'zero-trust-greenfield'] = [1, 2, 3]
PATH_STEPS[READINESS, 'zero-trust-assessment'] = [1, 2, 3]

_register(READINESS, 'zero-trust-greenfield', [
    (1, 'network-architect', (1,), 'zero_trust_requirements',
     'estate_id requirements identity_population service_dependencies measurable_criteria owners',
     'Derive candidate design criteria from accountable service and access requirements.', 'estate_id', None),
    (2, 'identity-and-access-management-architect', (3,), 'zero_trust_greenfield_design',
     'estate_id requirements_ref trust_assumptions identity_lifecycle policy_decisions enforcement_points verification_plan',
     'Trace intended access decisions and failure behavior to exact requirements.', 'estate_id', 'requirements_ref'),
    (3, 'security-assurance-and-measurement-architect', (2,), 'zero_trust_design_assessment',
     'estate_id design_ref criteria evidence_coverage unresolved_requirements disposition',
     'Independently assess design evidence against requirements and state limits on actual assurance.',
     'estate_id', 'design_ref'),
])
_register(READINESS, 'zero-trust-assessment', [
    (1, 'network-architect', (1,), 'zero_trust_assessment_baseline',
     'estate_id commission_ref scope intended_controls observed_topology observation_window limitations',
     'Record the commissioned scope, actual topology and evidence coverage.', 'estate_id', None),
    (2, 'security-assurance-and-measurement-architect', (3,), 'zero_trust_estate_assessment',
     'estate_id baseline_ref observed_controls supported_findings evidence_gaps residual_classic_paths exceptions remediation_priorities',
     'Ground control findings in observations, locate unresolved gaps and prioritize owned remediation.',
     'estate_id', 'baseline_ref'),
    (3, 'it-service-owner', (1,), 'zero_trust_assessment_disposition',
     'estate_id assessment_ref accountable_owner remediation_commitments risk_route follow_up',
     'Receive independent findings and assign disposition, owners and follow-up.',
     'estate_id', 'assessment_ref'),
])

VARIANTS[READINESS].append(
    ('terraform-readiness', 'Terraform implementation and promotion readiness',
     'Versioned configuration, state topology, reviewed immutable plan and bounded recovery evidence.'))
PATH_STEPS[READINESS, 'terraform-readiness'] = [1, 2, 3]
_register(READINESS, 'terraform-readiness', [
    (1, 'cloud-architect', (1,), 'infrastructure_target',
     'target_id environment state_owner requirements constraints recovery_criteria',
     'Bind the IaC request to the intended environment, state owner and measurable recovery criteria.',
     'target_id environment', None),
    (2, 'infrastructure-as-code-engineer', (3,), 'immutable_iac_plan',
     'target_id environment target_ref source_revision tool_version lockfile_digest state_identity plan_digest validated_plan drift_checks sensitive_data_handling',
     'Submit the reviewed plan digest, validated state boundary and applicable provider and tool versions.',
     'target_id environment', 'target_ref'),
    (3, 'service-transition-and-operational-readiness-manager', (1,), 'iac_plan_readiness',
     'target_id environment plan_ref plan_digest recovery_observation monitoring change_authority',
     'Review exact plan and recovery evidence and identify required production authority.',
     'target_id environment plan_digest', 'plan_ref'),
])

PROVIDERS = {
    'aws': ('AWS', 'organization, organizational unit, account and Region'),
    'azure': ('Microsoft Azure', 'tenant, management group, subscription and region'),
    'google-cloud': ('Google Cloud', 'organization, folder, project and location'),
}

for provider, (name, hierarchy) in PROVIDERS.items():
    for intent, description in (
        ('greenfield', 'requirements and placement constraints'),
        ('migration', 'on-premises inventory, dependency observations and migration constraints'),
        ('assessment', 'independent commission, exact current inventory and evidence coverage'),
    ):
        variant = f'{provider}-{intent}'
        VARIANTS[READINESS].append((variant, f'{name} infrastructure {intent}',
            f'Validate the {hierarchy} against {description} and record independent receiving evidence.'))
        PATH_STEPS[READINESS, variant] = [1, 2, 3] if intent == 'assessment' else [1, 2, 3, 4]
        scope = 'provider target_id environment'
        stages = [
            (1, 'cloud-architect', (1,), 'cloud_scope',
             scope + ' hierarchy region applicability_ref requirements accountable_owners',
             f'Pin the exact {hierarchy}. Establish {description}, service eligibility and placement.',
             scope, None),
        ]
        if intent == 'assessment':
            stages += [
                (2, 'security-assurance-and-measurement-architect', (3,), 'cloud_estate_assessment',
                 scope + ' scope_ref observed_controls supported_findings evidence_gaps remediation_priorities',
                 'Independently assess identity, connectivity, policy, logging, data residency, recovery and operational evidence.',
                 scope, 'scope_ref'),
                (3, 'it-service-owner', (1,), 'cloud_assessment_disposition',
                 scope + ' assessment_ref remediation_owners risk_route monitoring follow_up',
                 'Receive independent findings and assign disposition and follow-up.',
                 scope, 'assessment_ref'),
            ]
        else:
            stages += [
                (2, 'cloud-architect', (1,), 'cloud_landing_zone',
                 scope + ' scope_ref hierarchy identity connectivity policy logging residency recovery operating_model',
                 'Trace landing-zone decisions to placement, service requirements and accountable operations.',
                 scope, 'scope_ref'),
                (3, 'cloud-engineer', (1,), 'cloud_candidate',
                 scope + ' design_ref implementation_digest validation recovery limits',
                 ('Record staged migration waves, dependency continuity and reversal evidence.'
                  if intent == 'migration' else 'Record declarative build, validation, recovery and operating constraints.'),
                 scope, 'design_ref'),
                (4, 'service-transition-and-operational-readiness-manager', (1,), 'cloud_readiness',
                 scope + ' candidate_ref implementation_digest independent_verdict observed_controls evidence_limits support_owner change_route',
                 'Independently verify readiness for the exact target and candidate. Locate blocking gaps and change authority.',
                 scope + ' implementation_digest', 'candidate_ref'),
            ]
        _register(READINESS, variant, stages)

DELIVERY = {
    'aws': ('CodePipeline and CodeBuild', 'Amazon ECS rolling deployment',
            ('codecommit', 'codeconnections'), 'ecr', 'ecs-rolling'),
    'azure': ('Azure DevOps Services and Azure Pipelines', 'Azure Container Apps revisions',
              ('azure-repos',), 'acr', 'container-apps-revisions'),
    'google-cloud': ('Cloud Build and Cloud Deploy', 'Cloud Run revision rollout',
                     ('secure-source-manager', 'cloud-build-connection', 'cloud-source-repositories'),
                     'artifact-registry', 'cloud-run'),
}
MECHANISMS[PRODUCTION, 'normal'] = [
    'application', 'infrastructure-as-code', 'configuration', 'abap-cloud', *DELIVERY,
]

for provider, (pipeline, deployment, _, _, _) in DELIVERY.items():
    target = 'provider target_id environment'
    promotion = target + ' artifact_digest'
    _register(PRODUCTION, provider, [
        (1, 'devops-engineer', (1,), 'delivery_source',
         target + ' repository integration source_revision region applicability_ref backlog_and_test_management',
         f'Identify the exact repository and source revision used by {pipeline}. Record applicable auxiliary management tools.',
         target + ' source_revision', None),
        (2, 'ci-cd-platform-engineer', (4,), 'delivery_build',
         promotion + ' source_ref source_revision build_run pipeline_digest artifact_store provenance test_results credential_scope',
         'Build and test the exact source, attest immutable output and scope short-lived build credentials.',
         promotion + ' source_revision', 'source_ref'),
        (3, 'test-analyst', (4,), 'delivery_test',
         promotion + ' build_ref independent_verdict quality_evidence limitations',
         'Independently assess the exact artifact, tests and unresolved findings.',
         promotion, 'build_ref'),
        (4, 'release-engineer', (2,), 'delivery_promotion',
         promotion + ' test_ref release_id deployment_action region applicability_ref deployment_identity rollback_target monitoring_criteria',
         f'Prepare a promotion of the immutable artifact to {deployment} with bounded deployment identity and recovery target.',
         promotion + ' release_id rollback_target', 'test_ref'),
        (5, 'change-manager', (1,), 'delivery_authority',
         promotion + ' promotion_ref release_id rollback_target change_record approval_scope change_window expiry stop_conditions',
         'Require the exact existing human authority for this artifact, environment and reviewed promotion before effect.',
         promotion + ' release_id rollback_target', 'promotion_ref'),
        (6, 'gitops-and-continuous-delivery-engineer', (4,), 'delivery_rollout',
         promotion + ' approval_ref release_id rollback_target deployment_run deployment_identity rollout_observations rollback_record',
         f'Capture {deployment} rollout and actual reversal disposition against the authorized promotion.',
         promotion + ' release_id rollback_target', 'approval_ref'),
        (7, 'site-reliability-engineer', (1,), 'delivery_health',
         promotion + ' rollout_ref release_id rollback_target independent_verdict monitoring_observations recovery_observations limitations',
         'Independently assess the exact rollout, service objectives, recovery and any evidence gaps.',
         promotion + ' release_id rollback_target', 'rollout_ref'),
        (8, 'configuration-manager', (3,), 'delivery_reconciliation',
         promotion + ' health_ref release_id observed_revision updated_baseline exceptions operational_owner',
         'Reconcile observed configuration to the effective revision and hand over ownership.',
         promotion + ' release_id', 'health_ref'),
    ])
