# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Authored professional information requirements for all enterprise handoffs.

Each tuple is an editorial selection of a bounded work-product record and its
subject-specific fields. Exact workflow/step IDs select these definitions; titles
and role names never classify runtime work. Requirements supplement existing
source gates and do not establish external-standard conformance or approval.
"""

HANDOFF_REQUIREMENTS = {
    'idea-to-production': [
        ('demand_outcome', 'demand_id outcome owner source urgency'),
        ('product_opportunity', 'problem evidence target_users success_measure roadmap_scope'),
        ('requirements_baseline', 'baseline_id requirements source_links priorities verification_criteria'),
        ('solution_architecture', 'baseline boundaries decisions quality_targets failure_modes operational_review'),
        ('security_design', 'threat_scenarios business_risks controls requirement_links residual_exposure'),
        ('delivery_readiness', 'work_items acceptance_criteria dependency_refs technical_owners readiness_gaps'),
        ('reviewed_source_change', 'source_revision changed_behaviour peer_review test_results telemetry rollback_path'),
        ('release_test_evidence', 'tested_revision predeclared_exit_criteria actual_results exclusions residual_risk_disposition'),
        ('release_manifest', 'release_id artifact_versions target_environments provenance rollback_rehearsal'),
        ('change_authorisation', 'change_id exact_scope risk_class authority decision window emergency_record'),
        ('deployment_observations', 'approved_change_ref deployed_revision health_thresholds actual_results reversal_observations'),
        ('service_objective_status', 'service_id measurement_window indicators objectives budget_consumption policy_action'),
        ('benefit_observations', 'success_measure baseline observation_period effect_size method uncertainty')],
    'new-service-onboarding': [
        ('platform_design', 'service_boundary target_platform resilience_targets residency failure_scenario_evidence'),
        ('infrastructure_baseline', 'module_revisions reviewed_plan state_locking guardrails clean_apply_evidence'),
        ('image_supply_chain', 'image_digests base_lineage signatures sbom runtime_privileges secret_handling'),
        ('pipeline_baseline', 'pipeline_revision identity_federation provenance signing_checks credential_boundary'),
        ('credential_lifecycle', 'service_identity secret_references issuance expiry revocation_test exceptions'),
        ('environment_baseline', 'environments owners refresh_schedule data_classification masking_evidence'),
        ('promotion_model', 'desired_state_revision promoted_digest environment_sequence approval_points rollback_route'),
        ('monitoring_baseline', 'service_indicators dashboards alert_conditions alert_owners runbook_refs'),
        ('service_objectives', 'indicator_definitions objectives data_sources error_budget decision_thresholds policy_owners'),
        ('support_handover', 'runbook_revision known_errors support_owner rehearsal_evidence escalation'),
        ('configuration_records', 'configuration_ids relationships owner lifecycle verified_at reconciliation_source'),
        ('service_definition', 'service_boundary business_contact service_owner agreed_levels cost_risk_ownership')],
    'production-change': [
        ('reviewed_change', 'source_revision change_scope review_result review_size recovery_plan'),
        ('reviewed_infrastructure_plan', 'plan_digest target_assets destructive_actions reviewer actual_apply_identity'),
        ('change_test_evidence', 'tested_revision coverage actual_results residual_risks named_risk_disposition'),
        ('release_provenance', 'manifest_revision artifacts source_commits signatures target_scope'),
        ('change_record', 'change_id risk_class authorisation_ref schedule preauthorisation_basis measurement'),
        ('rollout_readiness', 'artifact_revision rollout_steps reversal_triggers rehearsal_evidence permitted_scope'),
        ('release_health_decision', 'observation_window signals thresholds decision actual_reversal_evidence'),
        ('configuration_reconciliation', 'changed_assets actual_revision record_revision effective_date reconciliation_gaps')],
    'incident-to-problem': [
        ('incident_report', 'incident_id observed_symptoms business_impact affected_service urgency observed_at'),
        ('incident_coordination', 'priority impact_basis working_hypothesis incident_owner communications_cadence'),
        ('restoration_evidence', 'restored_service restoration_actions authorisation_ref preserved_evidence observed_health residual_impact'),
        ('incident_command_log', 'timeline decisions stakeholder_updates notification_clocks accountable_command'),
        ('root_cause_record', 'problem_id causal_chain competing_hypotheses evidence known_error'),
        ('causal_fix_design', 'cause_ref design_options selected_response effort dependencies verification_plan'),
        ('candidate_fix', 'candidate_revision permitted_test_scope actual_test_results rollback_rehearsal unresolved_findings'),
        ('fix_authorisation', 'candidate_revision readiness_evidence exact_effect_scope authority prior_decision emergency_record'),
        ('fix_execution', 'authorisation_ref executed_revision actual_actions stop_go_results rollback_observations'),
        ('independent_fix_validation', 'validator_independence executed_revision regression_results service_results residual_defects'),
        ('detection_improvement', 'alert_revision change_authorisation failure_replay_result threshold runbook'),
        ('recurrence_measurement', 'prechange_baseline postchange_period recurrence_definition observed_rate uncertainty next_action')],
    'vulnerability-to-remediation': [
        ('vulnerability_priorities', 'finding_ids affected_assets exposure exploitability owners remediation_targets'),
        ('threat_assessment', 'threat_sources reliability targeting_evidence exploitability analytic_confidence'),
        ('remediation_guidance', 'finding_id validated_condition false_positive_disposition proposed_fix verification_method'),
        ('candidate_images', 'candidate_digests base_image_owner update_cadence validation_results production_boundary'),
        ('patch_authorisation', 'change_id affected_versions risk_of_action risk_of_delay prior_authority window rollback_conditions'),
        ('patched_system_evidence', 'authorisation_ref patched_revision actual_execution verification_result rollback_status'),
        ('authorised_retest', 'signed_scope_ref tested_target finding_ids retest_method observed_results'),
        ('residual_risk_acceptance', 'risk_id accountable_risk_owner decision compensating_controls expiry review_trigger')],
    'codebase-takeover': [
        ('takeover_review', 'fixed_criteria_ref reviewed_revision located_findings measurements limitations'),
        ('architecture_boundaries', 'system_boundary dependency_map violations enforcement_checks refactoring_increments'),
        ('takeover_test_strategy', 'product_risks test_levels environments lawful_data_basis exit_criteria'),
        ('characterisation_suite', 'source_revision captured_behaviour executable_cases observed_results uncertain_requirements'),
        ('reproducible_environment', 'definition_revision dependencies clean_apply_result drift_detection recovery_path'),
        ('observability_baseline', 'instrumented_revision signals measurement_window baseline_values known_blind_spots'),
        ('incremental_delivery', 'increments dependencies acceptance_criteria sequencing recovery_boundaries'),
        ('takeover_service_ownership', 'service_definition accountable_owner service_levels risk_profile ungoverned_gaps')],
    'access-request-to-review': [
        ('access_request', 'request_id subject entitlement purpose request_type approval_path'),
        ('individual_access_decision', 'subject entitlement purpose decision authority validity policy_ref'),
        ('access_provisioning', 'decision_ref subject entitlement actual_provisioning evidence revocation_event_evidence'),
        ('privileged_account_controls', 'account_id vault_ref session_monitoring break_glass_test use_review'),
        ('access_certification', 'campaign_scope reviewer_knowledge entitlement_decisions evidence exceptions revocation_followup'),
        ('access_assurance', 'assessed_period criteria sample control_evidence findings auditor_independence')],
    'data-product-delivery': [
        ('governed_data_definitions', 'element_ids definitions owner steward quality_tolerances'),
        ('data_privacy_position', 'processing_scope applicable_obligations impact_assessment lawful_basis competent_review timing'),
        ('data_flow_design', 'model_revision domain_owners flows trust_jurisdiction_boundaries boundary_controls'),
        ('pipeline_results', 'pipeline_revision sources transformations freshness_checks completeness_checks failure_signals'),
        ('analytics_model_results', 'model_revision metric_definitions lineage uniqueness_results integrity_results freshness_results'),
        ('data_quality_observations', 'population quality_dimensions measurements tolerances intended_use fitness_conclusion'),
        ('metric_dashboard', 'dashboard_revision metric_definition_ref source_query measurement_period discrepancies actions'),
        ('stewardship_decisions', 'issue_ids disputed_definitions affected_users decision_owner resolution escalation')],
    'ai-system-approval': [
        ('ai_inventory_classification', 'system_id intended_use risk_class classification_basis accountable_human inventory_revision'),
        ('ai_impact_position', 'processing_scope data_population privacy_impacts fairness_assessment preuse_review unresolved_obligations'),
        ('candidate_model_evidence', 'model_revision permitted_data test_scope heldout_results failure_modes excluded_populations limitations'),
        ('ai_serving_design', 'serving_revision interfaces data_lineage drift_monitoring degradation_thresholds harm_monitoring rollback_design'),
        ('ai_adversarial_findings', 'candidate_configuration permitted_test_scope offensive_authorisation findings severity owners'),
        ('ai_human_decision', 'candidate_revision data_users_environment_scope evidence_refs authority actual_decision conditions validity'),
        ('authorised_model_deployment', 'prior_decision_ref deployed_version training_run data_lineage actual_environment actual_scope'),
        ('model_operating_evidence', 'prior_decision_ref monitored_revision signals thresholds observed_breaches rollback_route'),
        ('ai_periodic_review', 'operated_scope review_evidence challenge_route expiry material_changes renewal_decision')],
    'supplier-onboarding': [
        ('supplier_tender_evaluation', 'requirements evaluation_criteria responses security_privacy_requirements continuity_exit_requirements recommendation'),
        ('supplier_risk_tier', 'supplier_id criticality dependencies assessed_risks exit_substitution_test residual_disposition'),
        ('supplier_security_requirements', 'threats business_risks control_requirements evidence_expectations exception_owners'),
        ('contract_obligations', 'executed_version parties obligations owners measures due_dates'),
        ('vendor_governance', 'supplier_scorecard measurement_sources governance_cadence renewal_deadline viable_alternatives'),
        ('underpinned_service_levels', 'customer_commitments supplier_commitments internal_olas coverage_gaps accountable_owners'),
        ('supplier_continuity_exercise', 'exercise_scope exit_steps observed_results recovery_objectives unresolved_dependencies')],
    'business-case-to-benefits': [
        ('investment_context', 'initiative_id sponsor decision_scope thresholds source_basis'),
        ('outcome_requirements', 'requirements source_refs outcomes baseline measures'),
        ('benefit_realisation_plan', 'benefit_ids owners baseline targets measurement_sources timing dependencies'),
        ('benefit_linked_roadmap', 'roadmap_revision increments benefit_refs success_measures dependencies'),
        ('adoption_dependencies', 'cohorts behaviour_changes benefit_refs adoption_measures owners readiness'),
        ('benefit_results', 'benefit_ref preagreed_method observation_period measured_effect attribution uncertainty'),
        ('benefit_review', 'expected_actual_variance disbenefits causes corrective_actions owners investment_decision')],
    'design-to-operational-readiness': [
        ('operable_solution_design', 'design_revision decisions quality_attributes failure_modes verification_criteria'),
        ('risk_traced_security_design', 'risk_scenarios objectives controls requirements validation_methods'),
        ('resilience_validation_design', 'dependencies failure_domains recovery_targets assumptions exercise_scenarios'),
        ('service_observation_design', 'slo_definitions data_sources actionable_alerts runbook_requirements ownership'),
        ('operational_readiness', 'readiness_criteria evidence status gaps owners permitted_waivers'),
        ('readiness_change_decision', 'change_scope risk_class readiness_refs approval_route actual_authority_decision'),
        ('operational_service_acceptance', 'service_scope support_owner agreed_slos residual_risks receiving_decision')],
    'migration-and-cutover': [
        ('migration_data_boundary', 'source_target_domains accountable_owners target_definitions classification mappings'),
        ('migration_cutover_plan', 'object_inventory mappings wave_sequence acceptance_criteria rollback_restore_semantics'),
        ('migration_rehearsal', 'permitted_data_scope rehearsal_revision throughput error_handling repeatability exceptions'),
        ('rehearsal_test_conclusion', 'predeclared_exit_criteria actual_results residual_risks scoped_exception_authority blocking_findings'),
        ('cutover_operational_constraints', 'readiness_criteria operational_limits receiving_evidence critical_gaps owners'),
        ('cutover_release_candidate', 'artifact_versions rehearsal_results deployment_steps rollback_steps production_boundary'),
        ('cutover_authorisation', 'rehearsal_refs reconciliation_design readiness_refs exact_effect_scope authority window rollback_boundaries'),
        ('actual_cutover', 'prior_authorisation_ref actual_versions actual_actions reconciliation stop_go_results rollback_observations'),
        ('independent_cutover_validation', 'prior_authorisation_ref validator_independence actual_cases observed_results reconciliation defects untested_scope'),
        ('production_validation_conclusion', 'validation_evidence predeclared_criteria residual_defects risk_disposition blocking_status'),
        ('migrated_service_acceptance', 'service_validation data_reconciliation ownership_acceptance residual_issues legacy_retirement_conditions')],
    'organisational-change-and-adoption': [
        ('change_business_context', 'business_outcome sponsor affected_stakeholders sources scope'),
        ('cohort_adoption_strategy', 'cohorts impacts readiness behaviour_changes owners support_measures'),
        ('task_training_evidence', 'changed_tasks training_assets proficiency_checks observed_proficiency coverage_gaps'),
        ('release_adoption_alignment', 'cohorts release_waves available_capabilities stability_constraints readiness_actions'),
        ('adoption_observations', 'behaviour_measures outcome_measures cohort_segments observation_period baseline results'),
        ('adoption_benefit_review', 'adoption_targets benefit_targets observed_variance reinforcement_actions owners reforecast')],
    'semantic-to-enterprise-publication': [
        ('semantic_publication_source', 'semantic_revision purpose audience claims evidence decisions unresolved_items'),
        ('semantic_review', 'reviewed_revision criteria reviewer_independence located_findings verdict required_source_approval'),
        ('rendered_publication', 'semantic_hash rendered_files manifest document_control projection_limits'),
        ('publication_review', 'inspected_files methods reviewer_independence located_findings blocking_disposition verdict'),
        ('publication_release_decision', 'exact_version files audience release_scope prior_reviews authority actual_decision')],
    'architecture-model-to-repository-governance': [
        ('project_architecture_source', 'model_revision source_artifacts stable_element_ids stable_relation_ids evidence_basis'),
        ('canonical_project_model', 'canonical_revision source_mapping semantic_preservation unresolved_mismatches ownership'),
        ('repository_revision', 'repository_id revision source_revision identity_preservation validation_evidence'),
        ('model_consistency_result', 'reviewed_revision invariants checked_scope located_findings blocking_disposition reviewer_independence'),
        ('enterprise_model_decisions', 'model_revision cross_project_dependencies reusable_elements accountable_owners actual_decisions'),
        ('repository_release_decision', 'exact_repository_revision evidence_refs decision_authority decision exceptions residual_risks review_expiry')],
    'service-retirement-and-decommission': [
        ('retirement_mandate', 'service_assets scope accountable_authority actual_mandate target_date'),
        ('retirement_dependencies', 'dependency_inventory consumers impact planned_disposition owners scoped_waivers'),
        ('retirement_data_disposition', 'data_inventory classification retention_obligations archive_delete_plan prior_authority'),
        ('retirement_change_authorisation', 'dependency_plan data_disposition rehearsal_evidence exact_credential_service_effects prior_human_decision'),
        ('retirement_access_transition', 'authorisation_ref transferred_removed_access observations retained_shutdown_access purpose expiry final_revocation_owner'),
        ('retirement_execution', 'prior_authorisation_ref actual_shutdown data_checks dependency_checks final_credential_reconciliation verified_state'),
        ('retired_asset_reconciliation', 'technical_state_ref asset_records configuration_records reconciliation_gaps closure_owner'),
        ('repository_retirement', 'repository_revision retired_element_ids active_dependency_checks owners retained_evidence'),
        ('retirement_benefit_review', 'benefit_baseline realised_benefits disbenefits variance accountable_owner')],
    'cyber-incident-breach-to-recovery': [
        ('security_incident_record', 'event_id source observed_at affected_scope observations false_positive_basis'),
        ('incident_triage', 'confirmed_scope severity evidence incident_lead containment_objectives'),
        ('containment_observations', 'authorised_scope actual_actions observations evidence_preservation destructive_action_authority residual_exposure'),
        ('forensic_record', 'evidence_ids collection_method integrity time_source custody timeline'),
        ('incident_impact', 'affected_services_data business_impacts applicable_obligations confirmed_facts inferences uncertainty'),
        ('notification_decision_basis', 'jurisdiction_obligations trigger_assessment clock decision_authority evidence actual_decision'),
        ('eradication_results', 'persistence_checks exploited_gaps actual_actions validation_results residual_risks owners'),
        ('trusted_recovery', 'trusted_state data_integrity restore_actions recovery_targets actual_results service_status'),
        ('business_recovery_acceptance', 'service_owner validation_signals observed_results residual_limits actual_decision'),
        ('incident_communications', 'approved_messages recipients regulatory_actions authority evidence_versions timing'),
        ('systemic_incident_findings', 'causes failed_controls supporting_evidence recurrence_risks improvement_findings'),
        ('control_remediation', 'finding_ids control_owners actions due_dates verification_methods'),
        ('incident_closure_assurance', 'independent_assessor assessed_evidence critical_findings disposition residual_limits closure_recommendation')],
    'resilience-validation': [
        ('business_criticality', 'business_services impact_tolerances criticality business_owners source_basis'),
        ('failure_domain_model', 'critical_paths dependency_ids failure_domains owners unknown_dependencies'),
        ('recovery_objectives', 'business_targets end_to_end_dependencies feasibility_evidence gaps accountable_owners'),
        ('resilience_design', 'design_revision single_shared_failure_modes assumptions design_responses measurable_outcomes'),
        ('exercise_plan', 'testable_claims scenarios permitted_scope safety_controls stop_conditions approval_ref'),
        ('resilience_exercise_evidence', 'approved_plan_ref actual_execution observations timestamps deviations evidence_refs'),
        ('resilience_findings', 'criterion observation impact evidence finding_owner severity_rationale'),
        ('resilience_remediation', 'finding_ids design_response action_owners due_dates acceptance_tests'),
        ('resilience_retest', 'original_findings changed_revision executed_cases observed_results closure_evidence'),
        ('resilience_acceptance', 'reviewed_scope evidence_ref residual_risks actual_acceptance next_validation')],
    'demand-to-portfolio-to-funding': [
        ('qualified_demand_record', 'demand_id business_outcome accountable_owner source urgency'),
        ('demand_disposition', 'demand_ref qualification_evidence reject_redirect_discover_assess decision_owner rationale'),
        ('capability_fit', 'capability_baseline reuse_options service_fit strategic_conflicts evidence'),
        ('application_portfolio_impact', 'affected_applications lifecycle_posture duplication dependencies accountable_owners'),
        ('demand_architecture_impact', 'affected_domains dependencies constraints options owners'),
        ('risk_value_assessment', 'risk_scenarios regulatory_basis incremental_value urgency uncertainty double_count_checks'),
        ('estimate_capacity', 'work_scope estimate_range assumptions constrained_skills available_capacity sources'),
        ('portfolio_prioritisation', 'candidate_set declared_criteria scoring_evidence constraints exceptions decision_authority'),
        ('funding_economics', 'cost_boundary periods currency capex_opex transition_costs reconciliation'),
        ('portfolio_commitment', 'approved_scope authority funding_basis capacity_basis conditions review_trigger')],
    'source-to-contract-to-service': [
        ('sourcing_requirements', 'business_need testable_requirements acceptance_criteria preferred_solution_constraints sources'),
        ('procurement_comparison', 'rfp_revision evaluation_criteria comparable_responses evidence procurement_rules'),
        ('supplier_assessment', 'supplier_id capability_claims evidence material_assumptions dependency_risks'),
        ('supplier_control_risk', 'security_privacy_obligations critical_risks controls mitigation_evidence residual_authority'),
        ('sourcing_architecture_fit', 'candidate_solution target_architecture integration_dependencies contradictions disposition'),
        ('supplier_selection', 'options declared_criteria evaluation_evidence decision_authority actual_decision'),
        ('contract_control_schedule', 'mandatory_controls enforceable_clauses measurements evidence obligations remedies_exit'),
        ('supplier_implementation', 'implementation_baseline milestones actual_results deviations prior_variation_authority'),
        ('sourced_service_acceptance', 'service_scope operational_owners readiness_evidence critical_gaps actual_acceptance'),
        ('vendor_governance_baseline', 'contract_obligations service_measures data_sources responsible_owners review_cadence')],
    'siam-multi-supplier': [
        ('siam_operating_model', 'customer_outcomes integration_processes accountable_owners supplier_boundaries decision_rights'),
        ('service_level_matrix', 'customer_slas underpinning_olas measures suppliers owners coverage_gaps'),
        ('supplier_dependency_model', 'dependency_ids service_supplier_endpoints owners source_revision views'),
        ('cross_supplier_incident_model', 'severity_rules incident_command restoration_owner escalation communication'),
        ('cross_supplier_problem_model', 'problem_scope causal_evidence end_to_end_owner supplier_actions verification'),
        ('integrated_change_calendar', 'release_ids dependencies windows blackout_constraints collision_resolution authority'),
        ('supplier_escalation', 'issue_types accountable_contact escalation_levels response_targets ownership_dispute_route'),
        ('integrated_service_acceptance', 'end_to_end_service evidence supplier_dependencies residual_gaps service_owner actual_acceptance')],
    'enterprise-release-orchestration': [
        ('enterprise_release_calendar', 'release_ids business_windows blackouts milestones accountable_owners'),
        ('release_dependencies', 'dependency_ids predecessor_successor sequence criticality accountable_owners'),
        ('business_release_readiness', 'affected_cohorts changed_tasks readiness_actions owners evidence'),
        ('cutover_readiness', 'critical_transitions cutover_plan reconciliation_rehearsal rollback_constraints gaps'),
        ('supplier_release_readiness', 'critical_dependencies supplier_commitments coverage_windows contingency evidence'),
        ('technical_release_readiness', 'artifact_versions provenance deployment_plan rollback_rehearsal feasibility'),
        ('secure_delivery_readiness', 'critical_controls provenance evidence deviations owners expiry'),
        ('independent_release_assurance', 'criteria assessed_evidence reviewer_independence findings critical_gate_disposition'),
        ('release_go_no_go', 'candidate_scope evidence_refs waivers residual_risks abort_triggers actual_authority_decision'),
        ('enterprise_release_execution', 'prior_approval_ref actual_artifacts actual_plan actual_actions deviations evidence'),
        ('post_release_validation', 'observed_revision signals thresholds actual_results reversal_trigger_actions'),
        ('enterprise_release_acceptance', 'business_outcome impact residual_issues owners actual_service_owner_acceptance')],
    'regulatory-change-to-assurance': [
        ('regulatory_source_change', 'source_reference jurisdiction publication_effective_dates exact_version change_summary'),
        ('regulatory_applicability', 'scope in_out_rationale affected_entities competent_authority evidence'),
        ('regulatory_obligations', 'obligation_ids source_citations context applicable_scope accountable_owner'),
        ('regulatory_requirements', 'requirement_ids obligation_refs preserved_intent testable_criteria traceability'),
        ('obligation_control_mapping', 'requirement_refs controls effectiveness_evidence gaps accountable_owners'),
        ('regulatory_architecture_impact', 'affected_domains model_revisions dependencies required_changes constraints'),
        ('regulatory_remediation_roadmap', 'mandatory_deadlines work_packages dependencies funding owners escalation'),
        ('implemented_control_evidence', 'control_version operating_period attributable_evidence population exceptions'),
        ('regulatory_assurance', 'independent_assessor scope criteria procedures observations exceptions limitations'),
        ('regulatory_closure', 'obligation_scope verification_refs remaining_exceptions actual_authority_decision review_triggers')],
}

# Intake is selected once and carried as versioned evidence. Each workflow has
# distinct entry questions, normal variants and failure/exit semantics.
# Tuple: required inputs; variant -> mechanism/evidence; rework; stop; exit.
WORKFLOW_PROFILES = {
    'idea-to-production': (
        ['Business outcome and accountable sponsor', 'Problem evidence and intended users', 'Existing service and change constraints'],
        [('new-product', 'Discover and test the product hypothesis before committing build scope', 'Problem evidence, options and success baseline'), ('existing-service-change', 'Reuse current service controls and assess only changed dependencies', 'Current baseline, change impact and receiving acceptance')],
        'Return unmet requirements or failed verification to the accountable requirement/design/change owner; retain accepted unchanged work.',
        'Stop production effects without current scoped change authority or on failed rollout health criteria.',
        'Reject/defer the demand with rationale, or close delivery after observed outcome and receiving service acceptance.'),
    'new-service-onboarding': (
        ['Service outcome and accountable owner', 'Platform/service sourcing context', 'Data classification and service-level needs'],
        [('cloud-native', 'Apply owned landing-zone, infrastructure, image and pipeline controls where used', 'Versioned configuration and observed deployment/recovery evidence'), ('saas-cots', 'Assess supplier service, identity, configuration, data export and support obligations', 'Supplier controls, tenancy configuration and tested continuity/exit evidence'), ('existing-platform', 'Reuse the approved platform baseline and assess service-specific deltas', 'Compatibility, capacity and operating handover evidence'), ('data-ai', 'Add lineage, quality and model-risk duties relevant to the service', 'Permitted data, evaluated quality/model limits and monitoring'), ('critical-regulated', 'Apply explicit obligations and business impact tolerances', 'Competent applicability review, recovery validation and correct authority')],
        'Return missing readiness evidence to its service/platform/supplier owner; reuse valid platform evidence by version.',
        'Stop service activation for an unowned critical dependency, missing mandatory control or absent applicable change authority.',
        'Accept the supported service, or cancel onboarding with owned data/access and supplier exit disposition.'),
    'production-change': (
        ['Exact candidate scope and current baseline', 'Change risk and eligible authority route', 'Verification and recovery criteria'],
        [('standard', 'Use a current preauthorised standard change only within its measured bounds', 'Applicable standard model/version and observed change results'), ('normal', 'Obtain the risk-appropriate decision before deployment', 'Reviewed candidate, test evidence and exact authority decision'), ('emergency', 'Use the prior authorised emergency route and explicit scope', 'Urgency, eligible authority, emergency record and later review')],
        'Return failed review/tests to the source owner before seeking another decision; a changed plan needs corresponding review.',
        'Stop on scope drift, absent authority, failed health gate or unsafe recovery condition.',
        'Close with actual health and configuration reconciliation, or execute the previously authorised reversal/forward recovery route.'),
    'incident-to-problem': (
        ['Affected service and observed business impact', 'Current incident/restoration authority', 'Evidence preservation and communication needs'],
        [('ordinary', 'Coordinate proportionate restoration and later causal work', 'Incident observations, authorised restoration and service validation'), ('major', 'Use declared command and stakeholder cadence', 'Command log, business-impact priority and notification-clock assessment'), ('suspected-security', 'Hand security handling to the incident response scope while preserving service coordination', 'Preserved evidence, scoped security handoff and authorised restoration')],
        'Return disproved hypotheses to the problem owner with their evidence; new fix revisions follow readiness and change review.',
        'Stop destructive recovery without evidence preservation and the required scope authority; stop deployment at failed health criteria.',
        'Close restoration separately from causal resolution; permanent closure needs independent fix validation and recurrence measures.'),
    'vulnerability-to-remediation': (
        ['Affected assets and finding evidence', 'Exposure/exploitability and business criticality', 'Current remediation and test authority'],
        [('planned', 'Prioritise exposure and remediate through normal change controls', 'Validated finding, candidate and retest evidence'), ('urgent-exploited', 'Use the authorised emergency route and compensating safeguards', 'Targeting/exploitation evidence, prior authority and recovery conditions'), ('risk-acceptance', 'Request a bounded residual-risk decision from the owner carrying the risk', 'Treatment options, compensating controls and expiry')],
        'Return failed fixes or retests to the finding/remediation owner with exact affected versions.',
        'Stop production change or offensive retest outside current written scope; do not turn scanner silence into closure.',
        'Close only verified remediation or correctly authorised time-bound residual risk, with owner and review trigger.'),
    'codebase-takeover': (
        ['Repository/source revision and permitted access', 'Review criteria fixed before reading', 'Service business purpose and known owners'],
        [('maintain', 'Stabilise ownership, environments and observability before incremental changes', 'Reproduction, baseline findings and receiving service definition'), ('modernise', 'Characterise behaviour and change enforced boundaries incrementally', 'Characterisation tests, architecture constraints and staged plan')],
        'Return unverified assumptions and failed characterisation to the owning analysis/engineering step.',
        'Stop access or data use without permission and production changes without applicable authority.',
        'Accept a governed service baseline or report an explicitly ungoverned/unknown scope with accountable escalation.'),
    'access-request-to-review': (
        ['Subject identity and requested entitlement', 'Justified use purpose and asset policy', 'Approval path and identity lifecycle event'],
        [('ordinary', 'Apply least-privilege decisions and integrated provisioning', 'Specific decision, actual grant/refusal and revocation evidence'), ('privileged', 'Apply vaulting, session monitoring and reviewed break-glass arrangements', 'Privileged decision, monitoring and exercised emergency access'), ('leaver-transfer', 'Revoke or transfer entitlements at the actual lifecycle event', 'Event, actual revocations, residual access owner and expiry')],
        'Return purpose-free or ambiguous requests to the requester/data owner; failed provisioning returns to IAM with actual observations.',
        'Stop granting access without a valid individual decision, required identity proof or current privileged-access scope.',
        'Close on evidenced grant/refusal/revocation; retain certification and independent audit findings with owners.'),
    'data-product-delivery': (
        ['Intended data use and accountable data owner', 'Source definitions and access/processing permissions', 'Quality tolerances and receiving consumer needs'],
        [('nonpersonal', 'Apply governed definitions, lineage and fit-for-purpose quality measurement', 'Source access, tested transforms and agreed metric definitions'), ('personal-regulated', 'Resolve privacy/jurisdiction obligations before processing and test controls', 'Competent impact/applicability position and permitted processing scope')],
        'Return definition conflicts to the data owner/steward and failed quality checks to the producing transform owner.',
        'Stop processing outside authorised purpose or when mandatory privacy/control prerequisites are unresolved.',
        'Accept the product for its bounded use or withdraw it with consumer notification and owned correction/retention actions.'),
    'ai-system-approval': (
        ['Intended use, users and accountable human', 'Permitted data and evaluation scope', 'Risk classification and applicable model obligations'],
        [('candidate-only', 'Develop and evaluate without production or pilot effects', 'Held-out performance, harms, exclusions and adversarial test scope'), ('bounded-pilot', 'Operate only after exact prior human pilot approval', 'Pilot users/data/environment, safeguards, monitoring and stop conditions'), ('production', 'Operate the exact authorised version with lineage, thresholds and challenge route', 'Prior production decision, actual deployment and monitoring evidence')],
        'Return failed evaluations or material changes to model/data/design owners, then seek the necessary renewed decision.',
        'Stop pilot/production effects without current exact human approval or when harmful-output/expiry triggers require it.',
        'Reject, retire or continue a bounded approved scope with review dates, challenge route and accountable data/model disposition.'),
    'supplier-onboarding': (
        ['Sourcing requirements and owner', 'Supplier/service criticality and data use', 'Procurement rules and contract decision rights'],
        [('ordinary', 'Assess comparable offers and proportionate service obligations', 'Declared criteria, supplier responses and owned contract measures'), ('critical', 'Exercise continuity/substitution and test enforceable exit', 'Dependency risks, recovery/exit evidence and residual decisions')],
        'Return noncomparable responses, unowned obligations or failed exit tests to procurement/contract/supplier owners.',
        'Stop commitments beyond authority or activation with unresolved mandatory supplier/security/privacy obligations.',
        'Accept the governed supplier service or terminate selection/exit with retained obligations and data/access disposition.'),
    'business-case-to-benefits': (
        ['Investment decision boundary and sponsor', 'Outcome baseline and measurement sources', 'Cost/benefit horizon and capacity assumptions'],
        [('new-investment', 'Compare feasible options including the baseline before committing benefits', 'Reconciled costs, benefit owners and sensitivity'), ('continuation-review', 'Use actual observations and revise forecasts transparently', 'Preagreed method, variance, disbenefits and continued-investment decision')],
        'Return unsupported benefit assumptions or double-counted value to the financial/benefit owner.',
        'Stop an unsupported funding claim or commitment outside actual portfolio authority.',
        'Approve/defer/reject investment or close a benefits period with owned corrective actions and a review condition.'),
    'design-to-operational-readiness': (
        ['Versioned solution and measurable quality requirements', 'Receiving service owner and support model', 'Risk, resilience and readiness criteria'],
        [('new-service', 'Establish complete receiving operations evidence', 'Runbooks, monitoring, access, recovery and support rehearsal'), ('existing-service-delta', 'Assess affected readiness and dependencies while reusing unchanged approved evidence', 'Exact design delta, impact and current evidence references')],
        'Return failed readiness criteria to the accountable design/platform/support owner before the change decision.',
        'Stop go-live for unowned critical readiness gaps or absent required change authority.',
        'Accept operational responsibility with explicit residual risks or defer activation with owned remediation.'),
    'migration-and-cutover': (
        ['Source/target inventory and data owners', 'Mapping, reconciliation and recovery semantics', 'Permitted rehearsal and production cutover boundaries'],
        [('rehearsal', 'Exercise permitted data and environments without production cutover effects', 'Throughput, error handling, repeatability and rollback observations'), ('cutover', 'Execute only the exact prior authorised production plan/window', 'Authority, actual actions, reconciliation and independent validation')],
        'Return failed rehearsal/reconciliation to migration or data/design owners; preserve valid unchanged evidence.',
        'Stop at failed predeclared criteria, changed scope or missing exact production/data authority.',
        'Accept migrated service/data/ownership or execute the previously authorised restore/forward-recovery branch before legacy retirement.'),
    'organisational-change-and-adoption': (
        ['Business outcome and named sponsor', 'Affected cohorts and changed tasks', 'Release capability/stability and measurement baseline'],
        [('single-cohort', 'Use task-specific readiness and proficiency checks', 'Cohort impact, training results and observed behaviour'), ('multi-wave', 'Align each cohort with available stable capability and reinforcement', 'Wave dependencies, readiness gates and segmented adoption results')],
        'Return low readiness/proficiency or unavailable capability to the adoption/product owner before the next wave.',
        'Stop forcing adoption of unavailable/unstable functionality or making unsupported realised-benefit claims.',
        'Close the wave with behavioural/outcome observations or reforecast benefits and assign reinforcement.'),
    'semantic-to-enterprise-publication': (
        ['Exact semantic source and intended audience', 'Disclosure/classification constraints', 'Required review, source approval and publication formats'],
        [('draft', 'Render a clearly labelled draft without granting acceptance or release', 'Exact semantic binding, draft status and disclosed limitations'), ('release-candidate', 'Require applicable semantic/source and publication gates before effects', 'Independent review, resolved blocking defects and exact human release decision')],
        'Return meaning changes to the semantic owner and rendition defects to the publication owner; preserve exact findings.',
        'Stop editing/release when mandatory source approval, disclosure or publication gates are missing.',
        'Release only the exact permitted package/audience after human decision, or retain an explicitly unapproved draft.'),
    'architecture-model-to-repository-governance': (
        ['Exact source model and project boundary', 'Stable identifier namespace and evidence', 'Selected notation/exchange profile and ownership rules'],
        [('native-model', 'Maintain source semantics and governed canonical identities', 'Exact revisions, ownership and integrity results'), ('interchange', 'Assess supported format and observable losses without inventing tool qualification', 'Export/import artifacts, exact format profile and loss disposition')],
        'Return inconsistent source facts to their owner and exchange losses to the mapping/repository owner.',
        'Stop publication/release with blocking identity/reference errors, unsupported semantic reinterpretation or missing authority.',
        'Publish an explicitly bounded reviewed revision or reject/defer release with owned exceptions and review dates.'),
    'service-retirement-and-decommission': (
        ['Actual retirement mandate and exact service/assets', 'Owned dependency and data-disposition plans', 'Rehearsal and prior production-change authority'],
        [('reversible-preparation', 'Prepare archives, dependency changes and bounded shutdown access without premature retirement', 'Plan/rehearsal evidence and scope-specific access ownership'), ('authorised-retirement', 'Execute exact approved shutdown/data/credential effects and reconcile state', 'Prior decisions, actual execution, final access revocation and records reconciliation')],
        'Return unresolved dependencies, archive failures or unowned retained access to their owners before destructive action.',
        'Stop irreversible effects outside exact authority or on failed dependency, data, credential or recovery criteria.',
        'Complete final credential/asset/model reconciliation and benefit closure, or use the authorised recovery/deferral route.'),
    'cyber-incident-breach-to-recovery': (
        ['Observed event, time and affected scope', 'Current response authority and evidence handling', 'Business priorities and notification obligations'],
        [('suspected', 'Triage hypotheses and preserve evidence before drawing conclusions', 'Observed event, reliability, scope confidence and lead'), ('confirmed-breach', 'Coordinate containment, notification and trusted recovery under exact authority', 'Custody/timeline, impact, clock assessment and actual decisions')],
        'Return disproved hypotheses, incomplete impact evidence or failed recovery to the responsible response/forensic/service owner.',
        'Stop unauthorised destructive handling, unsupported notification claims or recovery from untrusted state.',
        'Close on independent assurance of actual recovery and owned control remediation; retain justified false-positive disposition separately.'),
    'resilience-validation': (
        ['Business-owned criticality and impact tolerances', 'Dependency/failure-domain baseline', 'Falsifiable claims, recovery targets and permitted exercise scope'],
        [('isolated-exercise', 'Test representative failure conditions in permitted nonproduction scope', 'Scenario relevance, actual observations and extrapolation limits'), ('production-exercise', 'Use prior scoped authority, safeguards and enforced stop criteria', 'Actual approval, operating safeguards, observations and recovery status')],
        'Return falsified design assumptions or failed retests to the resilience/control owner with located evidence.',
        'Stop exercise effects outside approved scope or when safety/availability limits are breached.',
        'Accept bounded demonstrated resilience with residual risk and next review, or retain failed claims and owned remediation.'),
    'demand-to-portfolio-to-funding': (
        ['Named demand owner and business outcome', 'Capability/application baseline and constraints', 'Decision criteria, cost horizon and available capacity'],
        [('discovery', 'Reject, redirect or investigate uncertain need before detailed commitment', 'Qualification evidence, alternatives and next decision'), ('funding', 'Compare risk/value, lifecycle, cost and capacity against declared criteria', 'Reconstructible prioritisation and actual funding/commitment authority')],
        'Return unsupported value, lifecycle or estimate assumptions to their accountable owners.',
        'Stop anonymous/outcome-free prioritisation and commitments lacking eligible authority, funding or capacity basis.',
        'Record reject/redirect/discover/defer/commit with rationale and accountable review condition.'),
    'source-to-contract-to-service': (
        ['Testable need and sourcing scope', 'Procurement/contract authority and rules', 'Architecture, risk and receiving-service constraints'],
        [('competitive', 'Compare offers against declared criteria and preserve procurement evidence', 'Comparable responses, evaluation and selection decision'), ('direct-award', 'Apply the actual permitted exception route without fabricating competition', 'Authority, rationale, applicable rules and assessed risk/value')],
        'Return noncomparable responses, control wording gaps or implementation deviations to procurement/contract/delivery owners.',
        'Stop unauthorised commitment or service acceptance with unresolved critical control/ownership gaps.',
        'Accept the contracted service and measured vendor governance, or terminate selection/implementation under the actual contract route.'),
    'siam-multi-supplier': (
        ['Customer outcomes and service boundary', 'Supplier contracts, SLAs/OLAs and dependency owners', 'Integration decision and escalation rights'],
        [('steady-state', 'Govern end-to-end measures and shared responsibilities', 'Underpinning levels, ownership and service results'), ('cross-supplier-disruption', 'Use one incident/problem/escalation owner across contractual boundaries', 'Command/restoration ownership, supplier actions and customer impact')],
        'Return ownership gaps, level mismatches or collisions to the integration/service owner rather than bouncing between suppliers.',
        'Stop unsupported end-to-end acceptance or cross-supplier effects outside actual authority.',
        'Accept the integrated outcome with owned residual issues, or escalate unresolved contract boundaries to the entitled authority.'),
    'enterprise-release-orchestration': (
        ['Integrated release scope/calendar and business windows', 'Owned application/data/supplier dependencies', 'Readiness criteria and go/no-go authority'],
        [('coordinated', 'Sequence dependent releases and validate integrated readiness', 'Dependency register, business/supplier/technical/security readiness'), ('staged', 'Use bounded waves with evidence-driven continuation and recovery', 'Wave criteria, actual results, abort triggers and remaining exposure')],
        'Return failed independent gates to producer owners; changed artifacts/readiness need corresponding renewed review.',
        'Stop execution without exact go/no-go authority or when approved abort/reversal triggers fire.',
        'Close with actual end-to-end outcome, residual issues and service-owner acceptance, or execute the authorised recovery branch.'),
    'regulatory-change-to-assurance': (
        ['Attributable source/version/jurisdiction and dates', 'Competent applicability authority', 'Affected services, controls and obligation owners'],
        [('applicable', 'Trace obligations to testable requirements, implemented controls and independent assurance', 'Source-context mapping, actual control evidence and exceptions'), ('not-applicable', 'Record a competent bounded exclusion with its source/context rationale', 'Actual applicability decision and change/review trigger')],
        'Return ambiguous interpretation to the competent obligation owner and ineffective controls to control/design owners.',
        'Stop unsupported compliance claims or closure with unresolved mandatory obligations and absent authorised disposition.',
        'Close only the assessed scope with explicit exceptions, actual authority and future review triggers.'),
}

# These guards reuse the existing typed DCS condition language. Other mechanism
# choices require professional context evidence rather than invented booleans.
WORKFLOW_VARIANT_CONDITIONS = {
    ('data-product-delivery', 'nonpersonal'): {
        'field': 'processes_personal_data', 'op': 'eq', 'value': False},
    ('regulatory-change-to-assurance', 'not-applicable'): {
        'field': 'regulatory_requirement', 'op': 'eq', 'value': False},
}

# Approval/risk variants and technical mechanisms are different decisions. These
# explicit choices prevent a standard change or an urgent finding from silently
# selecting an infrastructure/container mechanism.
WORKFLOW_MECHANISMS = {
    'production-change': ['application', 'infrastructure-as-code', 'configuration'],
    'vulnerability-to-remediation': ['container', 'host', 'application-dependency'],
}
ONBOARDING_OVERLAYS = {'data-ai', 'critical-regulated'}
ONBOARDING_MECHANISMS = ['cloud-native', 'saas-cots', 'existing-platform']
WORKFLOW_PATH_STEPS = {
    ('regulatory-change-to-assurance', 'not-applicable'): [1, 2],
    ('ai-system-approval', 'candidate-only'): [1, 2, 3, 4, 5],
    ('demand-to-portfolio-to-funding', 'discovery'): [1, 2],
    ('vulnerability-to-remediation', 'risk-acceptance'): [1, 2, 3, 8],
    ('migration-and-cutover', 'rehearsal'): [1, 2, 3, 4, 5, 6],
    ('semantic-to-enterprise-publication', 'draft'): [1, 2, 3],
    ('service-retirement-and-decommission', 'reversible-preparation'): [1, 2, 3],
    ('access-request-to-review', 'ordinary'): [1, 2, 3, 5, 6],
    ('access-request-to-review', 'leaver-transfer'): [1, 2, 3, 5, 6],
}

# Tuple: semantic record, fields, effective criterion, exact eligible output IDs,
# functional producing duty. A duty is a host-assigned responsibility, not a
# restriction on which professional a layer/entity may choose to perform it.
VARIANT_HANDOFF_REQUIREMENTS = {
    ('supplier-onboarding', 2, 'ordinary'): (
        'ordinary_supplier_risk', 'supplier_id criticality classification_evidence assessed_risks continuity_exit_disposition residual_owner review_trigger',
        'Evidence supports supplier criticality and proportionate continuity/exit treatment; a noncritical classification does not fabricate an exercised exit or waive an applicable obligation.',
        ['third-party-risk-manager:1'], 'third-party-risk-manager'),
    ('source-to-contract-to-service', 2, 'direct-award'): (
        'direct_award_basis', 'sourcing_requirement permitted_route prior_exception_authority supplier_evidence value_risk_comparison limitations',
        'The actual permitted direct-award route, eligible authority and supplier/value-risk evidence are attributable; no competitive responses or tender process are invented.',
        ['it-procurement-specialist:3'], 'it-procurement-specialist'),
    ('architecture-model-to-repository-governance', 3, 'native-model'): (
        'native_repository_revision', 'repository_id revision source_revision stable_id_mapping lifecycle_preservation validation_evidence',
        'The exact native repository revision preserves source semantics, identities and lifecycle with structural validation; no interchange files or target-tool qualification are claimed.',
        ['architecture-repository-and-modelling-lead:4'], 'engagement:repository-maintenance-owner'),
    ('new-service-onboarding', 1, 'saas-cots'): (
        'supplier_service_design', 'service_boundary supplier_responsibilities customer_responsibilities residency resilience_targets supplier_test_evidence validation_limits',
        'Service boundaries and resilience/residency claims trace to actual supplier/customer evidence; unverified critical claims remain explicit gaps.',
        ['solution-architect:1'], 'engagement:service-design-owner'),
    ('new-service-onboarding', 2, 'saas-cots'): (
        'service_configuration_baseline', 'service_tenant configuration_revision approved_settings change_identity configuration_verification supplier_customer_guardrails',
        'Tenant/service settings are versioned, reviewed and verified against the permitted service baseline; configuration ownership and guardrails are explicit.',
        ['implementation-consultant:3'], 'engagement:service-configuration-owner'),
    ('new-service-onboarding', 3, 'saas-cots'): (
        'supplier_service_assurance', 'supplier_service critical_dependencies supplier_control_evidence privilege_boundary data_handling assurance_scope limitations',
        'Critical supplied-service dependencies, privilege and data-handling controls have accountable owners and attributable assurance evidence; do not invent customer-owned images or build results.',
        ['third-party-risk-manager:1', 'third-party-risk-manager:3'], 'engagement:supplier-assurance-owner'),
    ('new-service-onboarding', 4, 'saas-cots'): (
        'supplier_change_control', 'customer_supplier_changes identity_controls approval_path release_notifications provenance verification_recovery',
        'Customer and supplier changes have controlled identities, an applicable authorisation path, traceability and observable verification/recovery; no uncontrolled static shared credential is accepted.',
        ['change-manager:4'], 'engagement:service-change-owner'),
    ('new-service-onboarding', 5, 'saas-cots'): (
        'service_identity_lifecycle', 'service_identities supplier_customer_owners credential_references expiry_or_rotation revocation_evidence privileged_access exceptions',
        'Service identities and credentials have accountable ownership, bounded validity or rotation, tested revocation and controlled privileged access; any permitted exception needs its actual authority and expiry.',
        ['identity-and-access-management-engineer:1', 'identity-and-access-management-engineer:2'], 'engagement:service-identity-owner'),
    ('new-service-onboarding', 6, 'saas-cots'): (
        'supplier_service_validation', 'validation_scope tenant_or_sandbox data_classification permitted_data supplier_test_evidence customer_test_results limitations',
        'Validation uses permitted tenant/sandbox/data scope and distinguishes supplier evidence from customer observations; no unmasked production personal data is copied into test scope.',
        ['environment-manager:1', 'environment-manager:3'], 'engagement:service-validation-owner'),
    ('new-service-onboarding', 7, 'saas-cots'): (
        'supplier_release_recovery', 'service_release configuration_revision supplier_change_notifications customer_promotion verification recovery_escalation_evidence limitations',
        'Supplier releases and customer configuration changes retain exact identity, controlled sequence, verification and an evidenced recovery/escalation route; unavailable supplier rollback is disclosed rather than fabricated.',
        ['release-engineer:1', 'release-engineer:4'], 'engagement:service-change-owner'),
    ('new-service-onboarding', 1, 'existing-platform'): (
        'platform_service_design', 'service_boundary platform_baseline retained_controls changed_dependencies residency resilience_evidence',
        'The service design identifies the existing platform baseline, actual changed dependencies and applicable resilience/residency evidence; unchanged valid controls are reused by version.',
        ['solution-architect:1'], 'engagement:service-design-owner'),
    ('new-service-onboarding', 2, 'existing-platform'): (
        'inherited_configuration_baseline', 'platform_revision service_settings delta_review inherited_guardrails verification ownership',
        'Service-specific configuration deltas are reviewed and verified against a versioned owned platform baseline; the service does not recreate unchanged platform provisioning.',
        ['implementation-consultant:3'], 'engagement:service-configuration-owner'),
    ('new-service-onboarding', 3, 'existing-platform'): (
        'platform_dependency_assurance', 'platform_revision dependencies provenance controls privileged_access assurance_evidence residual_limits',
        'Actual platform dependencies have provenance, controlled privilege and attributable assurance; container-specific evidence applies only when that mechanism is actually used.',
        ['third-party-risk-manager:1', 'configuration-manager:3'], 'engagement:platform-assurance-owner'),
    ('new-service-onboarding', 4, 'existing-platform'): (
        'platform_change_path', 'platform_revision service_changes identity_controls approval_path provenance verification_recovery',
        'The service reuses the approved platform change path with current identity, provenance and verification/recovery evidence; no separate CI system is asserted without one.',
        ['change-manager:4'], 'engagement:service-change-owner'),
    ('new-service-onboarding', 7, 'existing-platform'): (
        'platform_service_promotion', 'platform_revision release_revision configuration_deltas promotion_sequence verification rollback_forward_recovery',
        'Actual release/configuration revisions are promoted in a controlled sequence with an evidenced recovery route; GitOps repositories are required only for the GitOps mechanism.',
        ['release-engineer:1', 'release-engineer:4'], 'engagement:service-change-owner'),
    ('data-product-delivery', 2, 'nonpersonal'): (
        'nonpersonal_data_use_classification', 'data_scope classification_evidence personal_data_exclusion permitted_purpose accountable_owner residual_obligations review_trigger',
        'Evidence establishes that this bounded scope contains no personal data; identify permitted use and any other applicable obligations without inventing a privacy legal basis or DPIA. Changed classification returns to competent privacy review.',
        ['data-owner:1', 'data-steward:4'], 'engagement:data-use-classification-owner'),
    ('regulatory-change-to-assurance', 2, 'not-applicable'): (
        'bounded_nonapplicability_decision', 'source_revision jurisdiction assessed_scope exclusion_evidence competent_authority actual_decision change_trigger',
        'A competent exact-scope decision establishes non-applicability from attributable source/context evidence and defines a review trigger; this closes only the assessed scope and does not fabricate implemented controls.',
        ['compliance-officer-technology:2'], 'engagement:regulatory-applicability-owner'),
    ('production-change', 1, 'configuration'): (
        'reviewed_configuration_change', 'configuration_revision affected_settings approved_baseline review_evidence verification_plan recovery_plan',
        'The exact settings change and recovery plan are reviewed against the owned baseline; no source-code change is fabricated.',
        ['implementation-consultant:3'], 'engagement:configuration-change-owner'),
    ('production-change', 2, 'configuration'): (
        'configuration_change_plan', 'reviewed_plan target_assets exact_settings destructive_effects reviewer execution_identity',
        'The actual applied configuration plan is the reviewed plan; destructive effects and applicable authority are explicit.',
        ['implementation-consultant:3'], 'engagement:configuration-change-owner'),
    ('production-change', 2, 'application'): (
        'application_infrastructure_impact', 'change_revision affected_assets infrastructure_delta retained_baseline compatibility_evidence owner',
        'Assess the application change against infrastructure dependencies; evidence supports any unchanged-infrastructure conclusion rather than claiming an IaC apply that did not occur.',
        ['configuration-manager:3'], 'engagement:change-impact-owner'),
    ('production-change', 4, 'configuration'): (
        'configuration_release_manifest', 'manifest_revision configuration_versions source_baseline change_identity verification_provenance',
        'Every applied setting/version is traceable to the exact reviewed configuration baseline and change, with attributable verification provenance.',
        ['release-engineer:2'], 'engagement:release-control-owner'),
    ('production-change', 6, 'configuration'): (
        'controlled_configuration_rollout', 'approved_change configuration_revision execution_steps health_thresholds reversal_triggers recovery_evidence',
        'The authorised settings rollout has observed health criteria and an exercised reversal or explicitly authorised forward-recovery path.',
        ['release-engineer:4'], 'engagement:configuration-execution-owner'),
    ('vulnerability-to-remediation', 4, 'host'): (
        'host_patch_candidate', 'affected_hosts candidate_versions package_provenance platform_owner validation_results production_boundary',
        'Candidate host packages/versions have provenance, an accountable platform owner and actual validation evidence; preparation does not deploy to production.',
        ['software-engineer:1'], 'engagement:remediation-candidate-owner'),
    ('vulnerability-to-remediation', 4, 'application-dependency'): (
        'dependency_remediation_candidate', 'affected_application dependency_versions source_provenance accountable_owner validation_results production_boundary',
        'Candidate dependency revisions have attributable provenance, an accountable application owner and actual validation evidence; preparation does not deploy to production.',
        ['software-engineer:1'], 'engagement:remediation-candidate-owner'),
}

# Every variant was assessed for whether its mechanism changes the information
# needed at a boundary. Unlisted combinations share actual outcome information;
# a scope-limited variant terminates before work it does not authorise or require.
VARIANT_SCOPE_ASSESSMENTS = {
    'idea-to-production': 'New and changed products share requirement/design/execution/outcome evidence; current baseline and changed scope differ in values, not schema.',
    'new-service-onboarding': 'SaaS and inherited-platform mechanisms replace owned IaC/image/pipeline records with configuration, dependency assurance and governed change evidence; overlays select a base mechanism explicitly.',
    'production-change': 'Approval class is separate from application/IaC/settings mechanism; exact authored alternatives prevent fabricated code or IaC evidence.',
    'incident-to-problem': 'Ordinary, major and suspected-security contexts retain actual observations, authority and evidence preservation; command intensity and the referenced response scope differ.',
    'vulnerability-to-remediation': 'Urgency is separate from container/host/dependency target mechanism; risk acceptance follows an explicit path without asserting unperformed deployment/retest.',
    'codebase-takeover': 'Maintenance and modernisation both need measured baselines, characterisation and owned increments; neither implies a completed rewrite.',
    'access-request-to-review': 'Ordinary/privileged/lifecycle requests require the actual decision, identity lifecycle evidence and applicable privileged-control disposition; no access event is inferred.',
    'data-product-delivery': 'Nonpersonal use replaces privacy/DPIA work with evidenced classification and bounded permitted-use decision; personal/regulated use retains competent impact review.',
    'ai-system-approval': 'Candidate-only scope terminates after candidate/adversarial evidence and cannot pass into deployment; pilot and production retain exact prior human scope.',
    'supplier-onboarding': 'Criticality changes continuity/exit depth; all suppliers retain accountable obligations and proportionate assurance.',
    'business-case-to-benefits': 'Investment and continuation share evidenced options, baselines and accountability; future benefits stay forecasts until actually observed.',
    'design-to-operational-readiness': 'New-service and changed-service readiness share evidence types; unchanged valid platform evidence is referenced rather than re-executed.',
    'migration-and-cutover': 'Rehearsal cannot satisfy actual production execution gates; a rehearsal-only scope stops before production authorisation and cutover.',
    'organisational-change-and-adoption': 'Single/multi-cohort cases share task readiness and observed behaviour; waves and denominators remain explicit.',
    'semantic-to-enterprise-publication': 'Drafts terminate at rendering and cannot enter a release-approval route; release candidates retain all applicable gates.',
    'architecture-model-to-repository-governance': 'Native and interchange paths share semantic integrity; native-only scope does not assert exported files or external-tool qualification.',
    'service-retirement-and-decommission': 'Reversible preparation terminates before authorisation for destructive execution; retirement retains actual credential/data/asset reconciliation.',
    'cyber-incident-breach-to-recovery': 'Suspected and confirmed events retain evidence confidence and authority; unobserved breach/notification actions cannot be inferred from suspicion.',
    'resilience-validation': 'Isolated and production exercises both require actual scoped observations; production additionally retains prior authority and safety limits.',
    'demand-to-portfolio-to-funding': 'Discovery terminates after qualification; a funding commitment requires the downstream evidence and eligible authority.',
    'source-to-contract-to-service': 'Direct award requires the actual permitted exception and cannot fabricate competitive tender responses.',
    'siam-multi-supplier': 'Steady-state/disruption share accountable service outcomes, dependencies and escalation; incident actions require actual scope.',
    'enterprise-release-orchestration': 'Coordinated/staged release share readiness, authority and actual observation requirements, with explicit wave boundaries.',
    'regulatory-change-to-assurance': 'Verified non-applicability closes at step2 under exact authority; it cannot require fabricated control implementation or compliance evidence.',
}

ONBOARDING_OVERLAY_REQUIREMENTS = {
    ('data-ai', 1): ('data_model_service_scope', 'data_model_versions permitted_use lineage boundaries quality_risk_requirements approval_dependencies',
        'The selected hosting design identifies actual data/model scope, permitted uses, lineage and quality/model-risk requirements; any separate pilot/production authority remains required.'),
    ('data-ai', 6): ('data_model_validation', 'scope_ref data_model_versions permitted_test_scope observed_evaluation population_limits unresolved_risks',
        'Validation identifies actual evaluated data/model versions, permitted scope, observed quality/performance/harms and excluded populations; synthetic or supplier results are labelled accurately.'),
    ('data-ai', 8): ('data_model_monitoring', 'scope_ref operating_version quality_drift_signals thresholds accountable_owner withdrawal_retraining_route',
        'The operating model defines owned quality/drift monitoring, meaningful thresholds and an authorised withdrawal/retraining route for the exact data/model scope.'),
    ('critical-regulated', 1): ('critical_service_obligations', 'service_scope business_impact_tolerances source_obligations applicability_basis control_objectives accountable_owners',
        'The design traces business-owned impact tolerances and actually applicable obligations to control objectives and owners; no clause or legal applicability is invented.'),
    ('critical-regulated', 3): ('critical_dependency_assurance', 'scope_ref critical_dependencies control_evidence recovery_validation supplier_limits residual_disposition',
        'Critical platform/supplier dependencies have attributable control/recovery evidence with explicit limitations and correctly owned residual exposure.'),
    ('critical-regulated', 10): ('critical_service_handover', 'scope_ref recovery_objectives retention_access_controls segregation_evidence observed_rehearsal receiving_owner unresolved_gaps',
        'Support handover includes actual recovery, retention/access and segregation evidence appropriate to the scope; critical unresolved readiness gaps cannot be closed by choosing another hosting mechanism.'),
}
