<!-- JAI:OUTPUT-CONTRACTS:START -->
# Design to operational readiness: source-owned handoff contracts

[Catalogue](index.md)

<a id="output-handoff-design-to-operational-readiness-1"></a>

## solution architecture and decision records

**Handoff content contract:** `handoff/design-to-operational-readiness:1`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_operable_solution_design`**: For solution architecture and decision records, supply the actual versioned operable solution design record, including design_revision, decisions, quality_attributes, failure_modes, verification_criteria. Independently assess the evidence against this exact criterion: Quality attributes and failure modes are explicit and testable. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `design_revision`, `decisions`, `quality_attributes`, `failure_modes`, `verification_criteria`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `new-service`.

**Producer:** `solution-architect`; **receiver:** `security-architect`.

**Receiving condition:** Quality attributes and failure modes are explicit and testable

**Next:** Step 2.

**Role output contracts:** `solution-architect:1`, `solution-architect:4`.

- **`handoff_operable_solution_design`**: For solution architecture and decision records, supply the actual versioned operable solution design record, including design_revision, decisions, quality_attributes, failure_modes, verification_criteria. Independently assess the evidence against this exact criterion: Quality attributes and failure modes are explicit and testable. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `design_revision`, `decisions`, `quality_attributes`, `failure_modes`, `verification_criteria`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `existing-service-delta`.

**Producer:** `solution-architect`; **receiver:** `security-architect`.

**Receiving condition:** Quality attributes and failure modes are explicit and testable

**Next:** Step 2.

**Role output contracts:** `solution-architect:1`, `solution-architect:4`.

- **`handoff_operable_solution_design`**: For solution architecture and decision records, supply the actual versioned operable solution design record, including design_revision, decisions, quality_attributes, failure_modes, verification_criteria. Independently assess the evidence against this exact criterion: Quality attributes and failure modes are explicit and testable. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `design_revision`, `decisions`, `quality_attributes`, `failure_modes`, `verification_criteria`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `zero-trust-migration`.

**Producer:** `network-architect`; **receiver:** `security-architect`.

**Receiving condition:** Record the exact existing estate, observations, ownership and unresolved dependencies before design.

**Next:** Step 2.

**Role output contracts:** `network-architect:1`.

- **`handoff_network_baseline`**: Record the exact existing estate, observations, ownership and unresolved dependencies before design.
  Required fields: `estate_id`, `identities`, `devices`, `workloads`, `resources`, `observed_flows`, `dependencies`, `owners`, `observation_limits`, `verification_scope`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `zero-trust-greenfield`.

**Producer:** `network-architect`; **receiver:** `identity-and-access-management-architect`.

**Receiving condition:** Derive candidate design criteria from accountable service and access requirements.

**Next:** Step 2.

**Role output contracts:** `network-architect:1`.

- **`handoff_zero_trust_requirements`**: Derive candidate design criteria from accountable service and access requirements.
  Required fields: `estate_id`, `requirements`, `identity_population`, `service_dependencies`, `measurable_criteria`, `owners`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `zero-trust-assessment`.

**Producer:** `network-architect`; **receiver:** `security-assurance-and-measurement-architect`.

**Receiving condition:** Record the commissioned scope, actual topology and evidence coverage.

**Next:** Step 2.

**Role output contracts:** `network-architect:1`.

- **`handoff_zero_trust_assessment_baseline`**: Record the commissioned scope, actual topology and evidence coverage.
  Required fields: `estate_id`, `commission_ref`, `scope`, `intended_controls`, `observed_topology`, `observation_window`, `limitations`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `terraform-readiness`.

**Producer:** `cloud-architect`; **receiver:** `infrastructure-as-code-engineer`.

**Receiving condition:** Bind the IaC request to the intended environment, state owner and measurable recovery criteria.

**Next:** Step 2.

**Role output contracts:** `cloud-architect:1`.

- **`handoff_infrastructure_target`**: Bind the IaC request to the intended environment, state owner and measurable recovery criteria.
  Required fields: `target_id`, `environment`, `state_owner`, `requirements`, `constraints`, `recovery_criteria`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `aws-greenfield`.

**Producer:** `cloud-architect`; **receiver:** `cloud-architect`.

**Receiving condition:** Pin the exact organization, organizational unit, account and Region. Establish requirements and placement constraints, service eligibility and placement.

**Next:** Step 2.

**Role output contracts:** `cloud-architect:1`.

- **`handoff_cloud_scope`**: Pin the exact organization, organizational unit, account and Region. Establish requirements and placement constraints, service eligibility and placement.
  Required fields: `provider`, `target_id`, `environment`, `hierarchy`, `region`, `applicability_ref`, `requirements`, `accountable_owners`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `aws-migration`.

**Producer:** `cloud-architect`; **receiver:** `cloud-architect`.

**Receiving condition:** Pin the exact organization, organizational unit, account and Region. Establish on-premises inventory, dependency observations and migration constraints, service eligibility and placement.

**Next:** Step 2.

**Role output contracts:** `cloud-architect:1`.

- **`handoff_cloud_scope`**: Pin the exact organization, organizational unit, account and Region. Establish on-premises inventory, dependency observations and migration constraints, service eligibility and placement.
  Required fields: `provider`, `target_id`, `environment`, `hierarchy`, `region`, `applicability_ref`, `requirements`, `accountable_owners`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `aws-assessment`.

**Producer:** `cloud-architect`; **receiver:** `security-assurance-and-measurement-architect`.

**Receiving condition:** Pin the exact organization, organizational unit, account and Region. Establish independent commission, exact current inventory and evidence coverage, service eligibility and placement.

**Next:** Step 2.

**Role output contracts:** `cloud-architect:1`.

- **`handoff_cloud_scope`**: Pin the exact organization, organizational unit, account and Region. Establish independent commission, exact current inventory and evidence coverage, service eligibility and placement.
  Required fields: `provider`, `target_id`, `environment`, `hierarchy`, `region`, `applicability_ref`, `requirements`, `accountable_owners`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `azure-greenfield`.

**Producer:** `cloud-architect`; **receiver:** `cloud-architect`.

**Receiving condition:** Pin the exact tenant, management group, subscription and region. Establish requirements and placement constraints, service eligibility and placement.

**Next:** Step 2.

**Role output contracts:** `cloud-architect:1`.

- **`handoff_cloud_scope`**: Pin the exact tenant, management group, subscription and region. Establish requirements and placement constraints, service eligibility and placement.
  Required fields: `provider`, `target_id`, `environment`, `hierarchy`, `region`, `applicability_ref`, `requirements`, `accountable_owners`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `azure-migration`.

**Producer:** `cloud-architect`; **receiver:** `cloud-architect`.

**Receiving condition:** Pin the exact tenant, management group, subscription and region. Establish on-premises inventory, dependency observations and migration constraints, service eligibility and placement.

**Next:** Step 2.

**Role output contracts:** `cloud-architect:1`.

- **`handoff_cloud_scope`**: Pin the exact tenant, management group, subscription and region. Establish on-premises inventory, dependency observations and migration constraints, service eligibility and placement.
  Required fields: `provider`, `target_id`, `environment`, `hierarchy`, `region`, `applicability_ref`, `requirements`, `accountable_owners`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `azure-assessment`.

**Producer:** `cloud-architect`; **receiver:** `security-assurance-and-measurement-architect`.

**Receiving condition:** Pin the exact tenant, management group, subscription and region. Establish independent commission, exact current inventory and evidence coverage, service eligibility and placement.

**Next:** Step 2.

**Role output contracts:** `cloud-architect:1`.

- **`handoff_cloud_scope`**: Pin the exact tenant, management group, subscription and region. Establish independent commission, exact current inventory and evidence coverage, service eligibility and placement.
  Required fields: `provider`, `target_id`, `environment`, `hierarchy`, `region`, `applicability_ref`, `requirements`, `accountable_owners`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `google-cloud-greenfield`.

**Producer:** `cloud-architect`; **receiver:** `cloud-architect`.

**Receiving condition:** Pin the exact organization, folder, project and location. Establish requirements and placement constraints, service eligibility and placement.

**Next:** Step 2.

**Role output contracts:** `cloud-architect:1`.

- **`handoff_cloud_scope`**: Pin the exact organization, folder, project and location. Establish requirements and placement constraints, service eligibility and placement.
  Required fields: `provider`, `target_id`, `environment`, `hierarchy`, `region`, `applicability_ref`, `requirements`, `accountable_owners`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `google-cloud-migration`.

**Producer:** `cloud-architect`; **receiver:** `cloud-architect`.

**Receiving condition:** Pin the exact organization, folder, project and location. Establish on-premises inventory, dependency observations and migration constraints, service eligibility and placement.

**Next:** Step 2.

**Role output contracts:** `cloud-architect:1`.

- **`handoff_cloud_scope`**: Pin the exact organization, folder, project and location. Establish on-premises inventory, dependency observations and migration constraints, service eligibility and placement.
  Required fields: `provider`, `target_id`, `environment`, `hierarchy`, `region`, `applicability_ref`, `requirements`, `accountable_owners`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `google-cloud-assessment`.

**Producer:** `cloud-architect`; **receiver:** `security-assurance-and-measurement-architect`.

**Receiving condition:** Pin the exact organization, folder, project and location. Establish independent commission, exact current inventory and evidence coverage, service eligibility and placement.

**Next:** Step 2.

**Role output contracts:** `cloud-architect:1`.

- **`handoff_cloud_scope`**: Pin the exact organization, folder, project and location. Establish independent commission, exact current inventory and evidence coverage, service eligibility and placement.
  Required fields: `provider`, `target_id`, `environment`, `hierarchy`, `region`, `applicability_ref`, `requirements`, `accountable_owners`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-design-to-operational-readiness-2"></a>

## security architecture and control requirements

**Handoff content contract:** `handoff/design-to-operational-readiness:2`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_risk_traced_security_design`**: For security architecture and control requirements, supply the actual versioned risk traced security design record, including risk_scenarios, objectives, controls, requirements, validation_methods. Independently assess the evidence against this exact criterion: Controls trace to risks and objectives. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `risk_scenarios`, `objectives`, `controls`, `requirements`, `validation_methods`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `new-service`.

**Producer:** `security-architect`; **receiver:** `operational-and-technology-resilience-architect`.

**Receiving condition:** Controls trace to risks and objectives

**Next:** Step 3.

**Role output contracts:** `security-architect:1`, `security-architect:4`.

- **`handoff_risk_traced_security_design`**: For security architecture and control requirements, supply the actual versioned risk traced security design record, including risk_scenarios, objectives, controls, requirements, validation_methods. Independently assess the evidence against this exact criterion: Controls trace to risks and objectives. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `risk_scenarios`, `objectives`, `controls`, `requirements`, `validation_methods`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `existing-service-delta`.

**Producer:** `security-architect`; **receiver:** `operational-and-technology-resilience-architect`.

**Receiving condition:** Controls trace to risks and objectives

**Next:** Step 3.

**Role output contracts:** `security-architect:1`, `security-architect:4`.

- **`handoff_risk_traced_security_design`**: For security architecture and control requirements, supply the actual versioned risk traced security design record, including risk_scenarios, objectives, controls, requirements, validation_methods. Independently assess the evidence against this exact criterion: Controls trace to risks and objectives. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `risk_scenarios`, `objectives`, `controls`, `requirements`, `validation_methods`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `zero-trust-migration`.

**Producer:** `security-architect`; **receiver:** `network-engineer`.

**Receiving condition:** Trace requirements and enforcement decisions to the accepted inventory and observed dependencies.

**Next:** Step 3.

**Role output contracts:** `security-architect:1`.

- **`handoff_zero_trust_target`**: Trace requirements and enforcement decisions to the accepted inventory and observed dependencies.
  Required fields: `estate_id`, `baseline_ref`, `requirements`, `trust_assumptions`, `policy_decisions`, `enforcement_points`, `access_criteria`, `verification_scope`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `zero-trust-greenfield`.

**Producer:** `identity-and-access-management-architect`; **receiver:** `security-assurance-and-measurement-architect`.

**Receiving condition:** Trace intended access decisions and failure behavior to exact requirements.

**Next:** Step 3.

**Role output contracts:** `identity-and-access-management-architect:3`.

- **`handoff_zero_trust_greenfield_design`**: Trace intended access decisions and failure behavior to exact requirements.
  Required fields: `estate_id`, `requirements_ref`, `trust_assumptions`, `identity_lifecycle`, `policy_decisions`, `enforcement_points`, `verification_plan`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `zero-trust-assessment`.

**Producer:** `security-assurance-and-measurement-architect`; **receiver:** `it-service-owner`.

**Receiving condition:** Ground control findings in observations, locate unresolved gaps and prioritize owned remediation.

**Next:** Step 3.

**Role output contracts:** `security-assurance-and-measurement-architect:3`.

- **`handoff_zero_trust_estate_assessment`**: Ground control findings in observations, locate unresolved gaps and prioritize owned remediation.
  Required fields: `estate_id`, `baseline_ref`, `observed_controls`, `supported_findings`, `evidence_gaps`, `residual_classic_paths`, `exceptions`, `remediation_priorities`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `terraform-readiness`.

**Producer:** `infrastructure-as-code-engineer`; **receiver:** `service-transition-and-operational-readiness-manager`.

**Receiving condition:** Submit the reviewed plan digest, validated state boundary and applicable provider and tool versions.

**Next:** Step 3.

**Role output contracts:** `infrastructure-as-code-engineer:3`.

- **`handoff_immutable_iac_plan`**: Submit the reviewed plan digest, validated state boundary and applicable provider and tool versions.
  Required fields: `target_id`, `environment`, `target_ref`, `source_revision`, `tool_version`, `lockfile_digest`, `state_identity`, `plan_digest`, `validated_plan`, `drift_checks`, `sensitive_data_handling`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `aws-greenfield`.

**Producer:** `cloud-architect`; **receiver:** `cloud-engineer`.

**Receiving condition:** Trace landing-zone decisions to placement, service requirements and accountable operations.

**Next:** Step 3.

**Role output contracts:** `cloud-architect:1`.

- **`handoff_cloud_landing_zone`**: Trace landing-zone decisions to placement, service requirements and accountable operations.
  Required fields: `provider`, `target_id`, `environment`, `scope_ref`, `hierarchy`, `identity`, `connectivity`, `policy`, `logging`, `residency`, `recovery`, `operating_model`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `aws-migration`.

**Producer:** `cloud-architect`; **receiver:** `cloud-engineer`.

**Receiving condition:** Trace landing-zone decisions to placement, service requirements and accountable operations.

**Next:** Step 3.

**Role output contracts:** `cloud-architect:1`.

- **`handoff_cloud_landing_zone`**: Trace landing-zone decisions to placement, service requirements and accountable operations.
  Required fields: `provider`, `target_id`, `environment`, `scope_ref`, `hierarchy`, `identity`, `connectivity`, `policy`, `logging`, `residency`, `recovery`, `operating_model`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `aws-assessment`.

**Producer:** `security-assurance-and-measurement-architect`; **receiver:** `it-service-owner`.

**Receiving condition:** Independently assess identity, connectivity, policy, logging, data residency, recovery and operational evidence.

**Next:** Step 3.

**Role output contracts:** `security-assurance-and-measurement-architect:3`.

- **`handoff_cloud_estate_assessment`**: Independently assess identity, connectivity, policy, logging, data residency, recovery and operational evidence.
  Required fields: `provider`, `target_id`, `environment`, `scope_ref`, `observed_controls`, `supported_findings`, `evidence_gaps`, `remediation_priorities`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `azure-greenfield`.

**Producer:** `cloud-architect`; **receiver:** `cloud-engineer`.

**Receiving condition:** Trace landing-zone decisions to placement, service requirements and accountable operations.

**Next:** Step 3.

**Role output contracts:** `cloud-architect:1`.

- **`handoff_cloud_landing_zone`**: Trace landing-zone decisions to placement, service requirements and accountable operations.
  Required fields: `provider`, `target_id`, `environment`, `scope_ref`, `hierarchy`, `identity`, `connectivity`, `policy`, `logging`, `residency`, `recovery`, `operating_model`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `azure-migration`.

**Producer:** `cloud-architect`; **receiver:** `cloud-engineer`.

**Receiving condition:** Trace landing-zone decisions to placement, service requirements and accountable operations.

**Next:** Step 3.

**Role output contracts:** `cloud-architect:1`.

- **`handoff_cloud_landing_zone`**: Trace landing-zone decisions to placement, service requirements and accountable operations.
  Required fields: `provider`, `target_id`, `environment`, `scope_ref`, `hierarchy`, `identity`, `connectivity`, `policy`, `logging`, `residency`, `recovery`, `operating_model`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `azure-assessment`.

**Producer:** `security-assurance-and-measurement-architect`; **receiver:** `it-service-owner`.

**Receiving condition:** Independently assess identity, connectivity, policy, logging, data residency, recovery and operational evidence.

**Next:** Step 3.

**Role output contracts:** `security-assurance-and-measurement-architect:3`.

- **`handoff_cloud_estate_assessment`**: Independently assess identity, connectivity, policy, logging, data residency, recovery and operational evidence.
  Required fields: `provider`, `target_id`, `environment`, `scope_ref`, `observed_controls`, `supported_findings`, `evidence_gaps`, `remediation_priorities`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `google-cloud-greenfield`.

**Producer:** `cloud-architect`; **receiver:** `cloud-engineer`.

**Receiving condition:** Trace landing-zone decisions to placement, service requirements and accountable operations.

**Next:** Step 3.

**Role output contracts:** `cloud-architect:1`.

- **`handoff_cloud_landing_zone`**: Trace landing-zone decisions to placement, service requirements and accountable operations.
  Required fields: `provider`, `target_id`, `environment`, `scope_ref`, `hierarchy`, `identity`, `connectivity`, `policy`, `logging`, `residency`, `recovery`, `operating_model`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `google-cloud-migration`.

**Producer:** `cloud-architect`; **receiver:** `cloud-engineer`.

**Receiving condition:** Trace landing-zone decisions to placement, service requirements and accountable operations.

**Next:** Step 3.

**Role output contracts:** `cloud-architect:1`.

- **`handoff_cloud_landing_zone`**: Trace landing-zone decisions to placement, service requirements and accountable operations.
  Required fields: `provider`, `target_id`, `environment`, `scope_ref`, `hierarchy`, `identity`, `connectivity`, `policy`, `logging`, `residency`, `recovery`, `operating_model`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `google-cloud-assessment`.

**Producer:** `security-assurance-and-measurement-architect`; **receiver:** `it-service-owner`.

**Receiving condition:** Independently assess identity, connectivity, policy, logging, data residency, recovery and operational evidence.

**Next:** Step 3.

**Role output contracts:** `security-assurance-and-measurement-architect:3`.

- **`handoff_cloud_estate_assessment`**: Independently assess identity, connectivity, policy, logging, data residency, recovery and operational evidence.
  Required fields: `provider`, `target_id`, `environment`, `scope_ref`, `observed_controls`, `supported_findings`, `evidence_gaps`, `remediation_priorities`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-design-to-operational-readiness-3"></a>

## resilience architecture and validation scenarios

**Handoff content contract:** `handoff/design-to-operational-readiness:3`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_resilience_validation_design`**: For resilience architecture and validation scenarios, supply the actual versioned resilience validation design record, including dependencies, failure_domains, recovery_targets, assumptions, exercise_scenarios. Independently assess the evidence against this exact criterion: Resilience claims identify dependencies, failure domains and validation method. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `dependencies`, `failure_domains`, `recovery_targets`, `assumptions`, `exercise_scenarios`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `new-service`.

**Producer:** `operational-and-technology-resilience-architect`; **receiver:** `site-reliability-engineer`.

**Receiving condition:** Resilience claims identify dependencies, failure domains and validation method

**Next:** Step 4.

**Role output contracts:** `operational-and-technology-resilience-architect:1`, `operational-and-technology-resilience-architect:2`, `operational-and-technology-resilience-architect:4`.

- **`handoff_resilience_validation_design`**: For resilience architecture and validation scenarios, supply the actual versioned resilience validation design record, including dependencies, failure_domains, recovery_targets, assumptions, exercise_scenarios. Independently assess the evidence against this exact criterion: Resilience claims identify dependencies, failure domains and validation method. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `dependencies`, `failure_domains`, `recovery_targets`, `assumptions`, `exercise_scenarios`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `existing-service-delta`.

**Producer:** `operational-and-technology-resilience-architect`; **receiver:** `site-reliability-engineer`.

**Receiving condition:** Resilience claims identify dependencies, failure domains and validation method

**Next:** Step 4.

**Role output contracts:** `operational-and-technology-resilience-architect:1`, `operational-and-technology-resilience-architect:2`, `operational-and-technology-resilience-architect:4`.

- **`handoff_resilience_validation_design`**: For resilience architecture and validation scenarios, supply the actual versioned resilience validation design record, including dependencies, failure_domains, recovery_targets, assumptions, exercise_scenarios. Independently assess the evidence against this exact criterion: Resilience claims identify dependencies, failure domains and validation method. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `dependencies`, `failure_domains`, `recovery_targets`, `assumptions`, `exercise_scenarios`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `zero-trust-migration`.

**Producer:** `network-engineer`; **receiver:** `security-assurance-and-measurement-architect`.

**Receiving condition:** Supply a staged candidate with named exception owners and expiry, halt thresholds and scoped reversal.

**Next:** Step 4.

**Role output contracts:** `network-engineer:2`.

- **`handoff_transition_candidate`**: Supply a staged candidate with named exception owners and expiry, halt thresholds and scoped reversal.
  Required fields: `estate_id`, `baseline_ref`, `design_ref`, `waves`, `coexistence`, `exceptions`, `continuity_limits`, `reversal`, `change_scope`, `verification_scope`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `zero-trust-greenfield`.

**Producer:** `security-assurance-and-measurement-architect`; **receiver:** `engagement:named-authority`.

**Receiving condition:** Independently assess design evidence against requirements and state limits on actual assurance.

**Next:** Terminal disposition; no downstream step.

**Role output contracts:** `security-assurance-and-measurement-architect:2`.

- **`handoff_zero_trust_design_assessment`**: Independently assess design evidence against requirements and state limits on actual assurance.
  Required fields: `estate_id`, `design_ref`, `criteria`, `evidence_coverage`, `unresolved_requirements`, `disposition`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `zero-trust-assessment`.

**Producer:** `it-service-owner`; **receiver:** `engagement:named-authority`.

**Receiving condition:** Receive independent findings and assign disposition, owners and follow-up.

**Next:** Terminal disposition; no downstream step.

**Role output contracts:** `it-service-owner:1`.

- **`handoff_zero_trust_assessment_disposition`**: Receive independent findings and assign disposition, owners and follow-up.
  Required fields: `estate_id`, `assessment_ref`, `accountable_owner`, `remediation_commitments`, `risk_route`, `follow_up`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `terraform-readiness`.

**Producer:** `service-transition-and-operational-readiness-manager`; **receiver:** `engagement:named-authority`.

**Receiving condition:** Review exact plan and recovery evidence and identify required production authority.

**Next:** Terminal disposition; no downstream step.

**Role output contracts:** `service-transition-and-operational-readiness-manager:1`.

- **`handoff_iac_plan_readiness`**: Review exact plan and recovery evidence and identify required production authority.
  Required fields: `target_id`, `environment`, `plan_ref`, `plan_digest`, `recovery_observation`, `monitoring`, `change_authority`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `aws-greenfield`.

**Producer:** `cloud-engineer`; **receiver:** `service-transition-and-operational-readiness-manager`.

**Receiving condition:** Record declarative build, validation, recovery and operating constraints.

**Next:** Step 4.

**Role output contracts:** `cloud-engineer:1`.

- **`handoff_cloud_candidate`**: Record declarative build, validation, recovery and operating constraints.
  Required fields: `provider`, `target_id`, `environment`, `design_ref`, `implementation_digest`, `validation`, `recovery`, `limits`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `aws-migration`.

**Producer:** `cloud-engineer`; **receiver:** `service-transition-and-operational-readiness-manager`.

**Receiving condition:** Record staged migration waves, dependency continuity and reversal evidence.

**Next:** Step 4.

**Role output contracts:** `cloud-engineer:1`.

- **`handoff_cloud_candidate`**: Record staged migration waves, dependency continuity and reversal evidence.
  Required fields: `provider`, `target_id`, `environment`, `design_ref`, `implementation_digest`, `validation`, `recovery`, `limits`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `aws-assessment`.

**Producer:** `it-service-owner`; **receiver:** `engagement:named-authority`.

**Receiving condition:** Receive independent findings and assign disposition and follow-up.

**Next:** Terminal disposition; no downstream step.

**Role output contracts:** `it-service-owner:1`.

- **`handoff_cloud_assessment_disposition`**: Receive independent findings and assign disposition and follow-up.
  Required fields: `provider`, `target_id`, `environment`, `assessment_ref`, `remediation_owners`, `risk_route`, `monitoring`, `follow_up`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `azure-greenfield`.

**Producer:** `cloud-engineer`; **receiver:** `service-transition-and-operational-readiness-manager`.

**Receiving condition:** Record declarative build, validation, recovery and operating constraints.

**Next:** Step 4.

**Role output contracts:** `cloud-engineer:1`.

- **`handoff_cloud_candidate`**: Record declarative build, validation, recovery and operating constraints.
  Required fields: `provider`, `target_id`, `environment`, `design_ref`, `implementation_digest`, `validation`, `recovery`, `limits`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `azure-migration`.

**Producer:** `cloud-engineer`; **receiver:** `service-transition-and-operational-readiness-manager`.

**Receiving condition:** Record staged migration waves, dependency continuity and reversal evidence.

**Next:** Step 4.

**Role output contracts:** `cloud-engineer:1`.

- **`handoff_cloud_candidate`**: Record staged migration waves, dependency continuity and reversal evidence.
  Required fields: `provider`, `target_id`, `environment`, `design_ref`, `implementation_digest`, `validation`, `recovery`, `limits`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `azure-assessment`.

**Producer:** `it-service-owner`; **receiver:** `engagement:named-authority`.

**Receiving condition:** Receive independent findings and assign disposition and follow-up.

**Next:** Terminal disposition; no downstream step.

**Role output contracts:** `it-service-owner:1`.

- **`handoff_cloud_assessment_disposition`**: Receive independent findings and assign disposition and follow-up.
  Required fields: `provider`, `target_id`, `environment`, `assessment_ref`, `remediation_owners`, `risk_route`, `monitoring`, `follow_up`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `google-cloud-greenfield`.

**Producer:** `cloud-engineer`; **receiver:** `service-transition-and-operational-readiness-manager`.

**Receiving condition:** Record declarative build, validation, recovery and operating constraints.

**Next:** Step 4.

**Role output contracts:** `cloud-engineer:1`.

- **`handoff_cloud_candidate`**: Record declarative build, validation, recovery and operating constraints.
  Required fields: `provider`, `target_id`, `environment`, `design_ref`, `implementation_digest`, `validation`, `recovery`, `limits`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `google-cloud-migration`.

**Producer:** `cloud-engineer`; **receiver:** `service-transition-and-operational-readiness-manager`.

**Receiving condition:** Record staged migration waves, dependency continuity and reversal evidence.

**Next:** Step 4.

**Role output contracts:** `cloud-engineer:1`.

- **`handoff_cloud_candidate`**: Record staged migration waves, dependency continuity and reversal evidence.
  Required fields: `provider`, `target_id`, `environment`, `design_ref`, `implementation_digest`, `validation`, `recovery`, `limits`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `google-cloud-assessment`.

**Producer:** `it-service-owner`; **receiver:** `engagement:named-authority`.

**Receiving condition:** Receive independent findings and assign disposition and follow-up.

**Next:** Terminal disposition; no downstream step.

**Role output contracts:** `it-service-owner:1`.

- **`handoff_cloud_assessment_disposition`**: Receive independent findings and assign disposition and follow-up.
  Required fields: `provider`, `target_id`, `environment`, `assessment_ref`, `remediation_owners`, `risk_route`, `monitoring`, `follow_up`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-design-to-operational-readiness-4"></a>

## SLO/monitoring design and runbook requirements

**Handoff content contract:** `handoff/design-to-operational-readiness:4`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_service_observation_design`**: For SLO/monitoring design and runbook requirements, supply the actual versioned service observation design record, including slo_definitions, data_sources, actionable_alerts, runbook_requirements, ownership. Independently assess the evidence against this exact criterion: Alerts are actionable and every SLO has a data source. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `slo_definitions`, `data_sources`, `actionable_alerts`, `runbook_requirements`, `ownership`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `new-service`.

**Producer:** `site-reliability-engineer`; **receiver:** `service-transition-and-operational-readiness-manager`.

**Receiving condition:** Alerts are actionable and every SLO has a data source

**Next:** Step 5.

**Role output contracts:** `site-reliability-engineer:1`.

- **`handoff_service_observation_design`**: For SLO/monitoring design and runbook requirements, supply the actual versioned service observation design record, including slo_definitions, data_sources, actionable_alerts, runbook_requirements, ownership. Independently assess the evidence against this exact criterion: Alerts are actionable and every SLO has a data source. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `slo_definitions`, `data_sources`, `actionable_alerts`, `runbook_requirements`, `ownership`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `existing-service-delta`.

**Producer:** `site-reliability-engineer`; **receiver:** `service-transition-and-operational-readiness-manager`.

**Receiving condition:** Alerts are actionable and every SLO has a data source

**Next:** Step 5.

**Role output contracts:** `site-reliability-engineer:1`.

- **`handoff_service_observation_design`**: For SLO/monitoring design and runbook requirements, supply the actual versioned service observation design record, including slo_definitions, data_sources, actionable_alerts, runbook_requirements, ownership. Independently assess the evidence against this exact criterion: Alerts are actionable and every SLO has a data source. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `slo_definitions`, `data_sources`, `actionable_alerts`, `runbook_requirements`, `ownership`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `zero-trust-migration`.

**Producer:** `security-assurance-and-measurement-architect`; **receiver:** `service-transition-and-operational-readiness-manager`.

**Receiving condition:** Independently observe permitted and denied flows, establish mandatory dependency coverage and prove recovery.

**Next:** Step 5.

**Role output contracts:** `security-assurance-and-measurement-architect:3`.

- **`handoff_transition_observations`**: Independently observe permitted and denied flows, establish mandatory dependency coverage and prove recovery.
  Required fields: `estate_id`, `baseline_ref`, `candidate_ref`, `allowed_paths`, `denied_paths`, `mandatory_dependencies`, `readiness`, `reversal`, `verification_scope`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `aws-greenfield`.

**Producer:** `service-transition-and-operational-readiness-manager`; **receiver:** `engagement:named-authority`.

**Receiving condition:** Independently verify readiness for the exact target and candidate. Locate blocking gaps and change authority.

**Next:** Terminal disposition; no downstream step.

**Role output contracts:** `service-transition-and-operational-readiness-manager:1`.

- **`handoff_cloud_readiness`**: Independently verify readiness for the exact target and candidate. Locate blocking gaps and change authority.
  Required fields: `provider`, `target_id`, `environment`, `candidate_ref`, `implementation_digest`, `independent_verdict`, `observed_controls`, `evidence_limits`, `support_owner`, `change_route`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `aws-migration`.

**Producer:** `service-transition-and-operational-readiness-manager`; **receiver:** `engagement:named-authority`.

**Receiving condition:** Independently verify readiness for the exact target and candidate. Locate blocking gaps and change authority.

**Next:** Terminal disposition; no downstream step.

**Role output contracts:** `service-transition-and-operational-readiness-manager:1`.

- **`handoff_cloud_readiness`**: Independently verify readiness for the exact target and candidate. Locate blocking gaps and change authority.
  Required fields: `provider`, `target_id`, `environment`, `candidate_ref`, `implementation_digest`, `independent_verdict`, `observed_controls`, `evidence_limits`, `support_owner`, `change_route`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `azure-greenfield`.

**Producer:** `service-transition-and-operational-readiness-manager`; **receiver:** `engagement:named-authority`.

**Receiving condition:** Independently verify readiness for the exact target and candidate. Locate blocking gaps and change authority.

**Next:** Terminal disposition; no downstream step.

**Role output contracts:** `service-transition-and-operational-readiness-manager:1`.

- **`handoff_cloud_readiness`**: Independently verify readiness for the exact target and candidate. Locate blocking gaps and change authority.
  Required fields: `provider`, `target_id`, `environment`, `candidate_ref`, `implementation_digest`, `independent_verdict`, `observed_controls`, `evidence_limits`, `support_owner`, `change_route`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `azure-migration`.

**Producer:** `service-transition-and-operational-readiness-manager`; **receiver:** `engagement:named-authority`.

**Receiving condition:** Independently verify readiness for the exact target and candidate. Locate blocking gaps and change authority.

**Next:** Terminal disposition; no downstream step.

**Role output contracts:** `service-transition-and-operational-readiness-manager:1`.

- **`handoff_cloud_readiness`**: Independently verify readiness for the exact target and candidate. Locate blocking gaps and change authority.
  Required fields: `provider`, `target_id`, `environment`, `candidate_ref`, `implementation_digest`, `independent_verdict`, `observed_controls`, `evidence_limits`, `support_owner`, `change_route`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `google-cloud-greenfield`.

**Producer:** `service-transition-and-operational-readiness-manager`; **receiver:** `engagement:named-authority`.

**Receiving condition:** Independently verify readiness for the exact target and candidate. Locate blocking gaps and change authority.

**Next:** Terminal disposition; no downstream step.

**Role output contracts:** `service-transition-and-operational-readiness-manager:1`.

- **`handoff_cloud_readiness`**: Independently verify readiness for the exact target and candidate. Locate blocking gaps and change authority.
  Required fields: `provider`, `target_id`, `environment`, `candidate_ref`, `implementation_digest`, `independent_verdict`, `observed_controls`, `evidence_limits`, `support_owner`, `change_route`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `google-cloud-migration`.

**Producer:** `service-transition-and-operational-readiness-manager`; **receiver:** `engagement:named-authority`.

**Receiving condition:** Independently verify readiness for the exact target and candidate. Locate blocking gaps and change authority.

**Next:** Terminal disposition; no downstream step.

**Role output contracts:** `service-transition-and-operational-readiness-manager:1`.

- **`handoff_cloud_readiness`**: Independently verify readiness for the exact target and candidate. Locate blocking gaps and change authority.
  Required fields: `provider`, `target_id`, `environment`, `candidate_ref`, `implementation_digest`, `independent_verdict`, `observed_controls`, `evidence_limits`, `support_owner`, `change_route`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-design-to-operational-readiness-5"></a>

## operational readiness assessment and evidence pack

**Handoff content contract:** `handoff/design-to-operational-readiness:5`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_operational_readiness`**: For operational readiness assessment and evidence pack, supply the actual versioned operational readiness record, including readiness_criteria, evidence, status, gaps, owners, permitted_waivers. Independently assess the evidence against this exact criterion: Every readiness criterion is pass/fail/waived with evidence and owner. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `readiness_criteria`, `evidence`, `status`, `gaps`, `owners`, `permitted_waivers`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `new-service`.

**Producer:** `service-transition-and-operational-readiness-manager`; **receiver:** `change-manager`.

**Receiving condition:** Every readiness criterion is pass/fail/waived with evidence and owner

**Next:** Step 6.

**Role output contracts:** `service-transition-and-operational-readiness-manager:1`, `service-transition-and-operational-readiness-manager:3`.

- **`handoff_operational_readiness`**: For operational readiness assessment and evidence pack, supply the actual versioned operational readiness record, including readiness_criteria, evidence, status, gaps, owners, permitted_waivers. Independently assess the evidence against this exact criterion: Every readiness criterion is pass/fail/waived with evidence and owner. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `readiness_criteria`, `evidence`, `status`, `gaps`, `owners`, `permitted_waivers`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `existing-service-delta`.

**Producer:** `service-transition-and-operational-readiness-manager`; **receiver:** `change-manager`.

**Receiving condition:** Every readiness criterion is pass/fail/waived with evidence and owner

**Next:** Step 6.

**Role output contracts:** `service-transition-and-operational-readiness-manager:1`, `service-transition-and-operational-readiness-manager:3`.

- **`handoff_operational_readiness`**: For operational readiness assessment and evidence pack, supply the actual versioned operational readiness record, including readiness_criteria, evidence, status, gaps, owners, permitted_waivers. Independently assess the evidence against this exact criterion: Every readiness criterion is pass/fail/waived with evidence and owner. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `readiness_criteria`, `evidence`, `status`, `gaps`, `owners`, `permitted_waivers`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `zero-trust-migration`.

**Producer:** `service-transition-and-operational-readiness-manager`; **receiver:** `change-manager`.

**Receiving condition:** Accept readiness only after reviewing candidate observations and establishing accountable support.

**Next:** Step 6.

**Role output contracts:** `service-transition-and-operational-readiness-manager:1`.

- **`handoff_transition_readiness`**: Accept readiness only after reviewing candidate observations and establishing accountable support.
  Required fields: `estate_id`, `baseline_ref`, `observations_ref`, `continuity_verdict`, `unresolved_items`, `support_owner`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-design-to-operational-readiness-6"></a>

## change authorisation decision

**Handoff content contract:** `handoff/design-to-operational-readiness:6`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_readiness_change_decision`**: For change authorisation decision, supply the actual versioned readiness change decision record, including change_scope, risk_class, readiness_refs, approval_route, actual_authority_decision. Independently assess the evidence against this exact criterion: Change risk and readiness evidence match the approval route. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `change_scope`, `risk_class`, `readiness_refs`, `approval_route`, `actual_authority_decision`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `new-service`.

**Producer:** `change-manager`; **receiver:** `it-service-owner`.

**Receiving condition:** Change risk and readiness evidence match the approval route

**Next:** Step 7.

**Role output contracts:** `change-manager:1`.

- **`handoff_readiness_change_decision`**: For change authorisation decision, supply the actual versioned readiness change decision record, including change_scope, risk_class, readiness_refs, approval_route, actual_authority_decision. Independently assess the evidence against this exact criterion: Change risk and readiness evidence match the approval route. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `change_scope`, `risk_class`, `readiness_refs`, `approval_route`, `actual_authority_decision`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `existing-service-delta`.

**Producer:** `change-manager`; **receiver:** `it-service-owner`.

**Receiving condition:** Change risk and readiness evidence match the approval route

**Next:** Step 7.

**Role output contracts:** `change-manager:1`.

- **`handoff_readiness_change_decision`**: For change authorisation decision, supply the actual versioned readiness change decision record, including change_scope, risk_class, readiness_refs, approval_route, actual_authority_decision. Independently assess the evidence against this exact criterion: Change risk and readiness evidence match the approval route. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `change_scope`, `risk_class`, `readiness_refs`, `approval_route`, `actual_authority_decision`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `zero-trust-migration`.

**Producer:** `change-manager`; **receiver:** `it-service-owner`.

**Receiving condition:** Identify the change and its exact approval route, scope and halt criteria. Apply production authority in the governed change path.

**Next:** Step 7.

**Role output contracts:** `change-manager:1`.

- **`handoff_transition_change_route`**: Identify the change and its exact approval route, scope and halt criteria. Apply production authority in the governed change path.
  Required fields: `estate_id`, `baseline_ref`, `readiness_ref`, `change_record`, `authority_scope`, `window`, `stop_conditions`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-design-to-operational-readiness-7"></a>

## service acceptance

**Handoff content contract:** `handoff/design-to-operational-readiness:7`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_operational_service_acceptance`**: For service acceptance, supply the actual versioned operational service acceptance record, including service_scope, support_owner, agreed_slos, residual_risks, receiving_decision. Independently assess the evidence against this exact criterion: Support ownership, SLOs and residual risks are explicitly accepted. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `service_scope`, `support_owner`, `agreed_slos`, `residual_risks`, `receiving_decision`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `new-service`.

**Producer:** `it-service-owner`; **receiver:** `engagement:named-authority`.

**Receiving condition:** Support ownership, SLOs and residual risks are explicitly accepted

**Next:** Terminal disposition; no downstream step.

**Role output contracts:** `it-service-owner:1`.

- **`handoff_operational_service_acceptance`**: For service acceptance, supply the actual versioned operational service acceptance record, including service_scope, support_owner, agreed_slos, residual_risks, receiving_decision. Independently assess the evidence against this exact criterion: Support ownership, SLOs and residual risks are explicitly accepted. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `service_scope`, `support_owner`, `agreed_slos`, `residual_risks`, `receiving_decision`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `existing-service-delta`.

**Producer:** `it-service-owner`; **receiver:** `engagement:named-authority`.

**Receiving condition:** Support ownership, SLOs and residual risks are explicitly accepted

**Next:** Terminal disposition; no downstream step.

**Role output contracts:** `it-service-owner:1`.

- **`handoff_operational_service_acceptance`**: For service acceptance, supply the actual versioned operational service acceptance record, including service_scope, support_owner, agreed_slos, residual_risks, receiving_decision. Independently assess the evidence against this exact criterion: Support ownership, SLOs and residual risks are explicitly accepted. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `service_scope`, `support_owner`, `agreed_slos`, `residual_risks`, `receiving_decision`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `zero-trust-migration`.

**Producer:** `it-service-owner`; **receiver:** `engagement:named-authority`.

**Receiving condition:** Receive the qualified transition package, ownership, monitoring, exceptions and reversal responsibilities.

**Next:** Terminal disposition; no downstream step.

**Role output contracts:** `it-service-owner:1`.

- **`handoff_transition_operational_handover`**: Receive the qualified transition package, ownership, monitoring, exceptions and reversal responsibilities.
  Required fields: `estate_id`, `baseline_ref`, `change_route_ref`, `named_owner`, `monitoring`, `recovery_obligations`, `exceptions`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.
<!-- JAI:OUTPUT-CONTRACTS:END -->
