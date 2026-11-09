<!-- JAI:OUTPUT-CONTRACTS:START -->
# New service onboarding: source-owned handoff contracts

[Catalogue](index.md)

<a id="output-handoff-new-service-onboarding-1"></a>

## target platform design

**Handoff content contract:** `handoff/new-service-onboarding:1`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_platform_design`**: For target platform design, supply the actual versioned platform design record, including service_boundary, target_platform, resilience_targets, residency, failure_scenario_evidence. Independently assess the evidence against this exact criterion: Resilience claims substantiated by a tested failure scenario. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `service_boundary`, `target_platform`, `resilience_targets`, `residency`, `failure_scenario_evidence`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `cloud-native`.

**Producer:** `cloud-architect`; **receiver:** `infrastructure-as-code-engineer`.

**Receiving condition:** Resilience claims substantiated by a tested failure scenario

**Next:** Step 2.

**Role output contracts:** `cloud-architect:1`.

- **`handoff_platform_design`**: For target platform design, supply the actual versioned platform design record, including service_boundary, target_platform, resilience_targets, residency, failure_scenario_evidence. Independently assess the evidence against this exact criterion: Resilience claims substantiated by a tested failure scenario. Do not substitute a related policy, plan or claimed execution for the required work product and observations. Cloud-native mechanism criterion: Resilience claims substantiated by a tested failure scenario.
  Required fields: `service_boundary`, `target_platform`, `resilience_targets`, `residency`, `failure_scenario_evidence`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `saas-cots`.

**Producer:** `engagement:service-design-owner`; **receiver:** `engagement:service-configuration-owner`.

**Receiving condition:** Service boundaries and resilience/residency claims trace to actual supplier/customer evidence; unverified critical claims remain explicit gaps.

**Next:** Step 2.

**Role output contracts:** `solution-architect:1`.

- **`handoff_supplier_service_design`**: Service boundaries and resilience/residency claims trace to actual supplier/customer evidence; unverified critical claims remain explicit gaps.
  Required fields: `service_boundary`, `supplier_responsibilities`, `customer_responsibilities`, `residency`, `resilience_targets`, `supplier_test_evidence`, `validation_limits`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `existing-platform`.

**Producer:** `engagement:service-design-owner`; **receiver:** `engagement:service-configuration-owner`.

**Receiving condition:** The service design identifies the existing platform baseline, actual changed dependencies and applicable resilience/residency evidence; unchanged valid controls are reused by version.

**Next:** Step 2.

**Role output contracts:** `solution-architect:1`.

- **`handoff_platform_service_design`**: The service design identifies the existing platform baseline, actual changed dependencies and applicable resilience/residency evidence; unchanged valid controls are reused by version.
  Required fields: `service_boundary`, `platform_baseline`, `retained_controls`, `changed_dependencies`, `residency`, `resilience_evidence`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `data-ai/cloud-native`.

**Producer:** `cloud-architect`; **receiver:** `infrastructure-as-code-engineer`.

**Receiving condition:** Resilience claims substantiated by a tested failure scenario

**Next:** Step 2.

**Role output contracts:** `cloud-architect:1`.

- **`handoff_platform_design`**: For target platform design, supply the actual versioned platform design record, including service_boundary, target_platform, resilience_targets, residency, failure_scenario_evidence. Independently assess the evidence against this exact criterion: Resilience claims substantiated by a tested failure scenario. Do not substitute a related policy, plan or claimed execution for the required work product and observations. Cloud-native mechanism criterion: Resilience claims substantiated by a tested failure scenario.
  Required fields: `service_boundary`, `target_platform`, `resilience_targets`, `residency`, `failure_scenario_evidence`.
- **`handoff_data_model_service_scope`**: The selected hosting design identifies actual data/model scope, permitted uses, lineage and quality/model-risk requirements; any separate pilot/production authority remains required.
  Required fields: `data_model_versions`, `permitted_use`, `lineage`, `boundaries`, `quality_risk_requirements`, `approval_dependencies`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `data-ai/saas-cots`.

**Producer:** `engagement:service-design-owner`; **receiver:** `engagement:service-configuration-owner`.

**Receiving condition:** Service boundaries and resilience/residency claims trace to actual supplier/customer evidence; unverified critical claims remain explicit gaps.

**Next:** Step 2.

**Role output contracts:** `solution-architect:1`.

- **`handoff_supplier_service_design`**: Service boundaries and resilience/residency claims trace to actual supplier/customer evidence; unverified critical claims remain explicit gaps.
  Required fields: `service_boundary`, `supplier_responsibilities`, `customer_responsibilities`, `residency`, `resilience_targets`, `supplier_test_evidence`, `validation_limits`.
- **`handoff_data_model_service_scope`**: The selected hosting design identifies actual data/model scope, permitted uses, lineage and quality/model-risk requirements; any separate pilot/production authority remains required.
  Required fields: `data_model_versions`, `permitted_use`, `lineage`, `boundaries`, `quality_risk_requirements`, `approval_dependencies`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `data-ai/existing-platform`.

**Producer:** `engagement:service-design-owner`; **receiver:** `engagement:service-configuration-owner`.

**Receiving condition:** The service design identifies the existing platform baseline, actual changed dependencies and applicable resilience/residency evidence; unchanged valid controls are reused by version.

**Next:** Step 2.

**Role output contracts:** `solution-architect:1`.

- **`handoff_platform_service_design`**: The service design identifies the existing platform baseline, actual changed dependencies and applicable resilience/residency evidence; unchanged valid controls are reused by version.
  Required fields: `service_boundary`, `platform_baseline`, `retained_controls`, `changed_dependencies`, `residency`, `resilience_evidence`.
- **`handoff_data_model_service_scope`**: The selected hosting design identifies actual data/model scope, permitted uses, lineage and quality/model-risk requirements; any separate pilot/production authority remains required.
  Required fields: `data_model_versions`, `permitted_use`, `lineage`, `boundaries`, `quality_risk_requirements`, `approval_dependencies`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `critical-regulated/cloud-native`.

**Producer:** `cloud-architect`; **receiver:** `infrastructure-as-code-engineer`.

**Receiving condition:** Resilience claims substantiated by a tested failure scenario

**Next:** Step 2.

**Role output contracts:** `cloud-architect:1`.

- **`handoff_platform_design`**: For target platform design, supply the actual versioned platform design record, including service_boundary, target_platform, resilience_targets, residency, failure_scenario_evidence. Independently assess the evidence against this exact criterion: Resilience claims substantiated by a tested failure scenario. Do not substitute a related policy, plan or claimed execution for the required work product and observations. Cloud-native mechanism criterion: Resilience claims substantiated by a tested failure scenario.
  Required fields: `service_boundary`, `target_platform`, `resilience_targets`, `residency`, `failure_scenario_evidence`.
- **`handoff_critical_service_obligations`**: The design traces business-owned impact tolerances and actually applicable obligations to control objectives and owners; no clause or legal applicability is invented.
  Required fields: `service_scope`, `business_impact_tolerances`, `source_obligations`, `applicability_basis`, `control_objectives`, `accountable_owners`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `critical-regulated/saas-cots`.

**Producer:** `engagement:service-design-owner`; **receiver:** `engagement:service-configuration-owner`.

**Receiving condition:** Service boundaries and resilience/residency claims trace to actual supplier/customer evidence; unverified critical claims remain explicit gaps.

**Next:** Step 2.

**Role output contracts:** `solution-architect:1`.

- **`handoff_supplier_service_design`**: Service boundaries and resilience/residency claims trace to actual supplier/customer evidence; unverified critical claims remain explicit gaps.
  Required fields: `service_boundary`, `supplier_responsibilities`, `customer_responsibilities`, `residency`, `resilience_targets`, `supplier_test_evidence`, `validation_limits`.
- **`handoff_critical_service_obligations`**: The design traces business-owned impact tolerances and actually applicable obligations to control objectives and owners; no clause or legal applicability is invented.
  Required fields: `service_scope`, `business_impact_tolerances`, `source_obligations`, `applicability_basis`, `control_objectives`, `accountable_owners`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `critical-regulated/existing-platform`.

**Producer:** `engagement:service-design-owner`; **receiver:** `engagement:service-configuration-owner`.

**Receiving condition:** The service design identifies the existing platform baseline, actual changed dependencies and applicable resilience/residency evidence; unchanged valid controls are reused by version.

**Next:** Step 2.

**Role output contracts:** `solution-architect:1`.

- **`handoff_platform_service_design`**: The service design identifies the existing platform baseline, actual changed dependencies and applicable resilience/residency evidence; unchanged valid controls are reused by version.
  Required fields: `service_boundary`, `platform_baseline`, `retained_controls`, `changed_dependencies`, `residency`, `resilience_evidence`.
- **`handoff_critical_service_obligations`**: The design traces business-owned impact tolerances and actually applicable obligations to control objectives and owners; no clause or legal applicability is invented.
  Required fields: `service_scope`, `business_impact_tolerances`, `source_obligations`, `applicability_basis`, `control_objectives`, `accountable_owners`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-new-service-onboarding-2"></a>

## controlled service configuration baseline and verification evidence

**Handoff content contract:** `handoff/new-service-onboarding:2`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_infrastructure_baseline`**: For controlled service configuration baseline and verification evidence, supply the actual versioned infrastructure baseline record, including module_revisions, reviewed_plan, state_locking, guardrails, clean_apply_evidence. Independently assess the evidence against this exact criterion: Service configuration is versioned, reviewed and verified against the selected mechanism and applicable guardrails. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `module_revisions`, `reviewed_plan`, `state_locking`, `guardrails`, `clean_apply_evidence`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `cloud-native`.

**Producer:** `infrastructure-as-code-engineer`; **receiver:** `container-platform-engineer`.

**Receiving condition:** Applies idempotently from clean; plan reviewed before apply

**Next:** Step 3.

**Role output contracts:** `infrastructure-as-code-engineer:1`, `infrastructure-as-code-engineer:3`.

- **`handoff_infrastructure_baseline`**: For controlled service configuration baseline and verification evidence, supply the actual versioned infrastructure baseline record, including module_revisions, reviewed_plan, state_locking, guardrails, clean_apply_evidence. Independently assess the evidence against this exact criterion: Service configuration is versioned, reviewed and verified against the selected mechanism and applicable guardrails. Do not substitute a related policy, plan or claimed execution for the required work product and observations. Cloud-native mechanism criterion: Applies idempotently from clean; plan reviewed before apply.
  Required fields: `module_revisions`, `reviewed_plan`, `state_locking`, `guardrails`, `clean_apply_evidence`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `saas-cots`.

**Producer:** `engagement:service-configuration-owner`; **receiver:** `engagement:supplier-assurance-owner`.

**Receiving condition:** Tenant/service settings are versioned, reviewed and verified against the permitted service baseline; configuration ownership and guardrails are explicit.

**Next:** Step 3.

**Role output contracts:** `implementation-consultant:3`.

- **`handoff_service_configuration_baseline`**: Tenant/service settings are versioned, reviewed and verified against the permitted service baseline; configuration ownership and guardrails are explicit.
  Required fields: `service_tenant`, `configuration_revision`, `approved_settings`, `change_identity`, `configuration_verification`, `supplier_customer_guardrails`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `existing-platform`.

**Producer:** `engagement:service-configuration-owner`; **receiver:** `engagement:platform-assurance-owner`.

**Receiving condition:** Service-specific configuration deltas are reviewed and verified against a versioned owned platform baseline; the service does not recreate unchanged platform provisioning.

**Next:** Step 3.

**Role output contracts:** `implementation-consultant:3`.

- **`handoff_inherited_configuration_baseline`**: Service-specific configuration deltas are reviewed and verified against a versioned owned platform baseline; the service does not recreate unchanged platform provisioning.
  Required fields: `platform_revision`, `service_settings`, `delta_review`, `inherited_guardrails`, `verification`, `ownership`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `data-ai/cloud-native`.

**Producer:** `infrastructure-as-code-engineer`; **receiver:** `container-platform-engineer`.

**Receiving condition:** Applies idempotently from clean; plan reviewed before apply

**Next:** Step 3.

**Role output contracts:** `infrastructure-as-code-engineer:1`, `infrastructure-as-code-engineer:3`.

- **`handoff_infrastructure_baseline`**: For controlled service configuration baseline and verification evidence, supply the actual versioned infrastructure baseline record, including module_revisions, reviewed_plan, state_locking, guardrails, clean_apply_evidence. Independently assess the evidence against this exact criterion: Service configuration is versioned, reviewed and verified against the selected mechanism and applicable guardrails. Do not substitute a related policy, plan or claimed execution for the required work product and observations. Cloud-native mechanism criterion: Applies idempotently from clean; plan reviewed before apply.
  Required fields: `module_revisions`, `reviewed_plan`, `state_locking`, `guardrails`, `clean_apply_evidence`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `data-ai/saas-cots`.

**Producer:** `engagement:service-configuration-owner`; **receiver:** `engagement:supplier-assurance-owner`.

**Receiving condition:** Tenant/service settings are versioned, reviewed and verified against the permitted service baseline; configuration ownership and guardrails are explicit.

**Next:** Step 3.

**Role output contracts:** `implementation-consultant:3`.

- **`handoff_service_configuration_baseline`**: Tenant/service settings are versioned, reviewed and verified against the permitted service baseline; configuration ownership and guardrails are explicit.
  Required fields: `service_tenant`, `configuration_revision`, `approved_settings`, `change_identity`, `configuration_verification`, `supplier_customer_guardrails`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `data-ai/existing-platform`.

**Producer:** `engagement:service-configuration-owner`; **receiver:** `engagement:platform-assurance-owner`.

**Receiving condition:** Service-specific configuration deltas are reviewed and verified against a versioned owned platform baseline; the service does not recreate unchanged platform provisioning.

**Next:** Step 3.

**Role output contracts:** `implementation-consultant:3`.

- **`handoff_inherited_configuration_baseline`**: Service-specific configuration deltas are reviewed and verified against a versioned owned platform baseline; the service does not recreate unchanged platform provisioning.
  Required fields: `platform_revision`, `service_settings`, `delta_review`, `inherited_guardrails`, `verification`, `ownership`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `critical-regulated/cloud-native`.

**Producer:** `infrastructure-as-code-engineer`; **receiver:** `container-platform-engineer`.

**Receiving condition:** Applies idempotently from clean; plan reviewed before apply

**Next:** Step 3.

**Role output contracts:** `infrastructure-as-code-engineer:1`, `infrastructure-as-code-engineer:3`.

- **`handoff_infrastructure_baseline`**: For controlled service configuration baseline and verification evidence, supply the actual versioned infrastructure baseline record, including module_revisions, reviewed_plan, state_locking, guardrails, clean_apply_evidence. Independently assess the evidence against this exact criterion: Service configuration is versioned, reviewed and verified against the selected mechanism and applicable guardrails. Do not substitute a related policy, plan or claimed execution for the required work product and observations. Cloud-native mechanism criterion: Applies idempotently from clean; plan reviewed before apply.
  Required fields: `module_revisions`, `reviewed_plan`, `state_locking`, `guardrails`, `clean_apply_evidence`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `critical-regulated/saas-cots`.

**Producer:** `engagement:service-configuration-owner`; **receiver:** `engagement:supplier-assurance-owner`.

**Receiving condition:** Tenant/service settings are versioned, reviewed and verified against the permitted service baseline; configuration ownership and guardrails are explicit.

**Next:** Step 3.

**Role output contracts:** `implementation-consultant:3`.

- **`handoff_service_configuration_baseline`**: Tenant/service settings are versioned, reviewed and verified against the permitted service baseline; configuration ownership and guardrails are explicit.
  Required fields: `service_tenant`, `configuration_revision`, `approved_settings`, `change_identity`, `configuration_verification`, `supplier_customer_guardrails`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `critical-regulated/existing-platform`.

**Producer:** `engagement:service-configuration-owner`; **receiver:** `engagement:platform-assurance-owner`.

**Receiving condition:** Service-specific configuration deltas are reviewed and verified against a versioned owned platform baseline; the service does not recreate unchanged platform provisioning.

**Next:** Step 3.

**Role output contracts:** `implementation-consultant:3`.

- **`handoff_inherited_configuration_baseline`**: Service-specific configuration deltas are reviewed and verified against a versioned owned platform baseline; the service does not recreate unchanged platform provisioning.
  Required fields: `platform_revision`, `service_settings`, `delta_review`, `inherited_guardrails`, `verification`, `ownership`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-new-service-onboarding-3"></a>

## service dependency and supply-chain assurance evidence

**Handoff content contract:** `handoff/new-service-onboarding:3`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_image_supply_chain`**: For service dependency and supply-chain assurance evidence, supply the actual versioned image supply chain record, including image_digests, base_lineage, signatures, sbom, runtime_privileges, secret_handling. Independently assess the evidence against this exact criterion: Critical dependencies have provenance, accountable ownership, controlled privileges and bounded assurance. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `image_digests`, `base_lineage`, `signatures`, `sbom`, `runtime_privileges`, `secret_handling`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `cloud-native`.

**Producer:** `container-platform-engineer`; **receiver:** `ci-cd-platform-engineer`.

**Receiving condition:** Non-root, no build secrets, pinned digests

**Next:** Step 4.

**Role output contracts:** `container-platform-engineer:1`, `container-platform-engineer:4`.

- **`handoff_image_supply_chain`**: For service dependency and supply-chain assurance evidence, supply the actual versioned image supply chain record, including image_digests, base_lineage, signatures, sbom, runtime_privileges, secret_handling. Independently assess the evidence against this exact criterion: Critical dependencies have provenance, accountable ownership, controlled privileges and bounded assurance. Do not substitute a related policy, plan or claimed execution for the required work product and observations. Cloud-native mechanism criterion: Non-root, no build secrets, pinned digests.
  Required fields: `image_digests`, `base_lineage`, `signatures`, `sbom`, `runtime_privileges`, `secret_handling`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `saas-cots`.

**Producer:** `engagement:supplier-assurance-owner`; **receiver:** `engagement:service-change-owner`.

**Receiving condition:** Critical supplied-service dependencies, privilege and data-handling controls have accountable owners and attributable assurance evidence; do not invent customer-owned images or build results.

**Next:** Step 4.

**Role output contracts:** `third-party-risk-manager:1`, `third-party-risk-manager:3`.

- **`handoff_supplier_service_assurance`**: Critical supplied-service dependencies, privilege and data-handling controls have accountable owners and attributable assurance evidence; do not invent customer-owned images or build results.
  Required fields: `supplier_service`, `critical_dependencies`, `supplier_control_evidence`, `privilege_boundary`, `data_handling`, `assurance_scope`, `limitations`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `existing-platform`.

**Producer:** `engagement:platform-assurance-owner`; **receiver:** `engagement:service-change-owner`.

**Receiving condition:** Actual platform dependencies have provenance, controlled privilege and attributable assurance; container-specific evidence applies only when that mechanism is actually used.

**Next:** Step 4.

**Role output contracts:** `third-party-risk-manager:1`, `configuration-manager:3`.

- **`handoff_platform_dependency_assurance`**: Actual platform dependencies have provenance, controlled privilege and attributable assurance; container-specific evidence applies only when that mechanism is actually used.
  Required fields: `platform_revision`, `dependencies`, `provenance`, `controls`, `privileged_access`, `assurance_evidence`, `residual_limits`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `data-ai/cloud-native`.

**Producer:** `container-platform-engineer`; **receiver:** `ci-cd-platform-engineer`.

**Receiving condition:** Non-root, no build secrets, pinned digests

**Next:** Step 4.

**Role output contracts:** `container-platform-engineer:1`, `container-platform-engineer:4`.

- **`handoff_image_supply_chain`**: For service dependency and supply-chain assurance evidence, supply the actual versioned image supply chain record, including image_digests, base_lineage, signatures, sbom, runtime_privileges, secret_handling. Independently assess the evidence against this exact criterion: Critical dependencies have provenance, accountable ownership, controlled privileges and bounded assurance. Do not substitute a related policy, plan or claimed execution for the required work product and observations. Cloud-native mechanism criterion: Non-root, no build secrets, pinned digests.
  Required fields: `image_digests`, `base_lineage`, `signatures`, `sbom`, `runtime_privileges`, `secret_handling`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `data-ai/saas-cots`.

**Producer:** `engagement:supplier-assurance-owner`; **receiver:** `engagement:service-change-owner`.

**Receiving condition:** Critical supplied-service dependencies, privilege and data-handling controls have accountable owners and attributable assurance evidence; do not invent customer-owned images or build results.

**Next:** Step 4.

**Role output contracts:** `third-party-risk-manager:1`, `third-party-risk-manager:3`.

- **`handoff_supplier_service_assurance`**: Critical supplied-service dependencies, privilege and data-handling controls have accountable owners and attributable assurance evidence; do not invent customer-owned images or build results.
  Required fields: `supplier_service`, `critical_dependencies`, `supplier_control_evidence`, `privilege_boundary`, `data_handling`, `assurance_scope`, `limitations`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `data-ai/existing-platform`.

**Producer:** `engagement:platform-assurance-owner`; **receiver:** `engagement:service-change-owner`.

**Receiving condition:** Actual platform dependencies have provenance, controlled privilege and attributable assurance; container-specific evidence applies only when that mechanism is actually used.

**Next:** Step 4.

**Role output contracts:** `third-party-risk-manager:1`, `configuration-manager:3`.

- **`handoff_platform_dependency_assurance`**: Actual platform dependencies have provenance, controlled privilege and attributable assurance; container-specific evidence applies only when that mechanism is actually used.
  Required fields: `platform_revision`, `dependencies`, `provenance`, `controls`, `privileged_access`, `assurance_evidence`, `residual_limits`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `critical-regulated/cloud-native`.

**Producer:** `container-platform-engineer`; **receiver:** `ci-cd-platform-engineer`.

**Receiving condition:** Non-root, no build secrets, pinned digests

**Next:** Step 4.

**Role output contracts:** `container-platform-engineer:1`, `container-platform-engineer:4`.

- **`handoff_image_supply_chain`**: For service dependency and supply-chain assurance evidence, supply the actual versioned image supply chain record, including image_digests, base_lineage, signatures, sbom, runtime_privileges, secret_handling. Independently assess the evidence against this exact criterion: Critical dependencies have provenance, accountable ownership, controlled privileges and bounded assurance. Do not substitute a related policy, plan or claimed execution for the required work product and observations. Cloud-native mechanism criterion: Non-root, no build secrets, pinned digests.
  Required fields: `image_digests`, `base_lineage`, `signatures`, `sbom`, `runtime_privileges`, `secret_handling`.
- **`handoff_critical_dependency_assurance`**: Critical platform/supplier dependencies have attributable control/recovery evidence with explicit limitations and correctly owned residual exposure.
  Required fields: `scope_ref`, `critical_dependencies`, `control_evidence`, `recovery_validation`, `supplier_limits`, `residual_disposition`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `critical-regulated/saas-cots`.

**Producer:** `engagement:supplier-assurance-owner`; **receiver:** `engagement:service-change-owner`.

**Receiving condition:** Critical supplied-service dependencies, privilege and data-handling controls have accountable owners and attributable assurance evidence; do not invent customer-owned images or build results.

**Next:** Step 4.

**Role output contracts:** `third-party-risk-manager:1`, `third-party-risk-manager:3`.

- **`handoff_supplier_service_assurance`**: Critical supplied-service dependencies, privilege and data-handling controls have accountable owners and attributable assurance evidence; do not invent customer-owned images or build results.
  Required fields: `supplier_service`, `critical_dependencies`, `supplier_control_evidence`, `privilege_boundary`, `data_handling`, `assurance_scope`, `limitations`.
- **`handoff_critical_dependency_assurance`**: Critical platform/supplier dependencies have attributable control/recovery evidence with explicit limitations and correctly owned residual exposure.
  Required fields: `scope_ref`, `critical_dependencies`, `control_evidence`, `recovery_validation`, `supplier_limits`, `residual_disposition`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `critical-regulated/existing-platform`.

**Producer:** `engagement:platform-assurance-owner`; **receiver:** `engagement:service-change-owner`.

**Receiving condition:** Actual platform dependencies have provenance, controlled privilege and attributable assurance; container-specific evidence applies only when that mechanism is actually used.

**Next:** Step 4.

**Role output contracts:** `third-party-risk-manager:1`, `configuration-manager:3`.

- **`handoff_platform_dependency_assurance`**: Actual platform dependencies have provenance, controlled privilege and attributable assurance; container-specific evidence applies only when that mechanism is actually used.
  Required fields: `platform_revision`, `dependencies`, `provenance`, `controls`, `privileged_access`, `assurance_evidence`, `residual_limits`.
- **`handoff_critical_dependency_assurance`**: Critical platform/supplier dependencies have attributable control/recovery evidence with explicit limitations and correctly owned residual exposure.
  Required fields: `scope_ref`, `critical_dependencies`, `control_evidence`, `recovery_validation`, `supplier_limits`, `residual_disposition`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-new-service-onboarding-4"></a>

## controlled service change path with identity and provenance evidence

**Handoff content contract:** `handoff/new-service-onboarding:4`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_pipeline_baseline`**: For controlled service change path with identity and provenance evidence, supply the actual versioned pipeline baseline record, including pipeline_revision, identity_federation, provenance, signing_checks, credential_boundary. Independently assess the evidence against this exact criterion: Changes use governed identities, traceable inputs and an authorised observable change path. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `pipeline_revision`, `identity_federation`, `provenance`, `signing_checks`, `credential_boundary`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `cloud-native`.

**Producer:** `ci-cd-platform-engineer`; **receiver:** `secrets-and-configuration-management-engineer`.

**Receiving condition:** No static cloud credentials in the CI system

**Next:** Step 5.

**Role output contracts:** `ci-cd-platform-engineer:1`, `ci-cd-platform-engineer:3`, `ci-cd-platform-engineer:4`.

- **`handoff_pipeline_baseline`**: For controlled service change path with identity and provenance evidence, supply the actual versioned pipeline baseline record, including pipeline_revision, identity_federation, provenance, signing_checks, credential_boundary. Independently assess the evidence against this exact criterion: Changes use governed identities, traceable inputs and an authorised observable change path. Do not substitute a related policy, plan or claimed execution for the required work product and observations. Cloud-native mechanism criterion: No static cloud credentials in the CI system.
  Required fields: `pipeline_revision`, `identity_federation`, `provenance`, `signing_checks`, `credential_boundary`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `saas-cots`.

**Producer:** `engagement:service-change-owner`; **receiver:** `engagement:service-identity-owner`.

**Receiving condition:** Customer and supplier changes have controlled identities, an applicable authorisation path, traceability and observable verification/recovery; no uncontrolled static shared credential is accepted.

**Next:** Step 5.

**Role output contracts:** `change-manager:4`.

- **`handoff_supplier_change_control`**: Customer and supplier changes have controlled identities, an applicable authorisation path, traceability and observable verification/recovery; no uncontrolled static shared credential is accepted.
  Required fields: `customer_supplier_changes`, `identity_controls`, `approval_path`, `release_notifications`, `provenance`, `verification_recovery`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `existing-platform`.

**Producer:** `engagement:service-change-owner`; **receiver:** `secrets-and-configuration-management-engineer`.

**Receiving condition:** The service reuses the approved platform change path with current identity, provenance and verification/recovery evidence; no separate CI system is asserted without one.

**Next:** Step 5.

**Role output contracts:** `change-manager:4`.

- **`handoff_platform_change_path`**: The service reuses the approved platform change path with current identity, provenance and verification/recovery evidence; no separate CI system is asserted without one.
  Required fields: `platform_revision`, `service_changes`, `identity_controls`, `approval_path`, `provenance`, `verification_recovery`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `data-ai/cloud-native`.

**Producer:** `ci-cd-platform-engineer`; **receiver:** `secrets-and-configuration-management-engineer`.

**Receiving condition:** No static cloud credentials in the CI system

**Next:** Step 5.

**Role output contracts:** `ci-cd-platform-engineer:1`, `ci-cd-platform-engineer:3`, `ci-cd-platform-engineer:4`.

- **`handoff_pipeline_baseline`**: For controlled service change path with identity and provenance evidence, supply the actual versioned pipeline baseline record, including pipeline_revision, identity_federation, provenance, signing_checks, credential_boundary. Independently assess the evidence against this exact criterion: Changes use governed identities, traceable inputs and an authorised observable change path. Do not substitute a related policy, plan or claimed execution for the required work product and observations. Cloud-native mechanism criterion: No static cloud credentials in the CI system.
  Required fields: `pipeline_revision`, `identity_federation`, `provenance`, `signing_checks`, `credential_boundary`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `data-ai/saas-cots`.

**Producer:** `engagement:service-change-owner`; **receiver:** `engagement:service-identity-owner`.

**Receiving condition:** Customer and supplier changes have controlled identities, an applicable authorisation path, traceability and observable verification/recovery; no uncontrolled static shared credential is accepted.

**Next:** Step 5.

**Role output contracts:** `change-manager:4`.

- **`handoff_supplier_change_control`**: Customer and supplier changes have controlled identities, an applicable authorisation path, traceability and observable verification/recovery; no uncontrolled static shared credential is accepted.
  Required fields: `customer_supplier_changes`, `identity_controls`, `approval_path`, `release_notifications`, `provenance`, `verification_recovery`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `data-ai/existing-platform`.

**Producer:** `engagement:service-change-owner`; **receiver:** `secrets-and-configuration-management-engineer`.

**Receiving condition:** The service reuses the approved platform change path with current identity, provenance and verification/recovery evidence; no separate CI system is asserted without one.

**Next:** Step 5.

**Role output contracts:** `change-manager:4`.

- **`handoff_platform_change_path`**: The service reuses the approved platform change path with current identity, provenance and verification/recovery evidence; no separate CI system is asserted without one.
  Required fields: `platform_revision`, `service_changes`, `identity_controls`, `approval_path`, `provenance`, `verification_recovery`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `critical-regulated/cloud-native`.

**Producer:** `ci-cd-platform-engineer`; **receiver:** `secrets-and-configuration-management-engineer`.

**Receiving condition:** No static cloud credentials in the CI system

**Next:** Step 5.

**Role output contracts:** `ci-cd-platform-engineer:1`, `ci-cd-platform-engineer:3`, `ci-cd-platform-engineer:4`.

- **`handoff_pipeline_baseline`**: For controlled service change path with identity and provenance evidence, supply the actual versioned pipeline baseline record, including pipeline_revision, identity_federation, provenance, signing_checks, credential_boundary. Independently assess the evidence against this exact criterion: Changes use governed identities, traceable inputs and an authorised observable change path. Do not substitute a related policy, plan or claimed execution for the required work product and observations. Cloud-native mechanism criterion: No static cloud credentials in the CI system.
  Required fields: `pipeline_revision`, `identity_federation`, `provenance`, `signing_checks`, `credential_boundary`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `critical-regulated/saas-cots`.

**Producer:** `engagement:service-change-owner`; **receiver:** `engagement:service-identity-owner`.

**Receiving condition:** Customer and supplier changes have controlled identities, an applicable authorisation path, traceability and observable verification/recovery; no uncontrolled static shared credential is accepted.

**Next:** Step 5.

**Role output contracts:** `change-manager:4`.

- **`handoff_supplier_change_control`**: Customer and supplier changes have controlled identities, an applicable authorisation path, traceability and observable verification/recovery; no uncontrolled static shared credential is accepted.
  Required fields: `customer_supplier_changes`, `identity_controls`, `approval_path`, `release_notifications`, `provenance`, `verification_recovery`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `critical-regulated/existing-platform`.

**Producer:** `engagement:service-change-owner`; **receiver:** `secrets-and-configuration-management-engineer`.

**Receiving condition:** The service reuses the approved platform change path with current identity, provenance and verification/recovery evidence; no separate CI system is asserted without one.

**Next:** Step 5.

**Role output contracts:** `change-manager:4`.

- **`handoff_platform_change_path`**: The service reuses the approved platform change path with current identity, provenance and verification/recovery evidence; no separate CI system is asserted without one.
  Required fields: `platform_revision`, `service_changes`, `identity_controls`, `approval_path`, `provenance`, `verification_recovery`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-new-service-onboarding-5"></a>

## dynamic short-lived credentials and a tested revocation path

**Handoff content contract:** `handoff/new-service-onboarding:5`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_credential_lifecycle`**: For dynamic short-lived credentials and a tested revocation path, supply the actual versioned credential lifecycle record, including service_identity, secret_references, issuance, expiry, revocation_test, exceptions. Independently assess the evidence against this exact criterion: Static credentials only as a time-bound exception. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `service_identity`, `secret_references`, `issuance`, `expiry`, `revocation_test`, `exceptions`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `cloud-native`.

**Producer:** `secrets-and-configuration-management-engineer`; **receiver:** `environment-manager`.

**Receiving condition:** Static credentials only as a time-bound exception

**Next:** Step 6.

**Role output contracts:** `secrets-and-configuration-management-engineer:2`, `secrets-and-configuration-management-engineer:3`.

- **`handoff_credential_lifecycle`**: For dynamic short-lived credentials and a tested revocation path, supply the actual versioned credential lifecycle record, including service_identity, secret_references, issuance, expiry, revocation_test, exceptions. Independently assess the evidence against this exact criterion: Static credentials only as a time-bound exception. Do not substitute a related policy, plan or claimed execution for the required work product and observations. Cloud-native mechanism criterion: Static credentials only as a time-bound exception.
  Required fields: `service_identity`, `secret_references`, `issuance`, `expiry`, `revocation_test`, `exceptions`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `saas-cots`.

**Producer:** `engagement:service-identity-owner`; **receiver:** `engagement:service-validation-owner`.

**Receiving condition:** Service identities and credentials have accountable ownership, bounded validity or rotation, tested revocation and controlled privileged access; any permitted exception needs its actual authority and expiry.

**Next:** Step 6.

**Role output contracts:** `identity-and-access-management-engineer:1`, `identity-and-access-management-engineer:2`.

- **`handoff_service_identity_lifecycle`**: Service identities and credentials have accountable ownership, bounded validity or rotation, tested revocation and controlled privileged access; any permitted exception needs its actual authority and expiry.
  Required fields: `service_identities`, `supplier_customer_owners`, `credential_references`, `expiry_or_rotation`, `revocation_evidence`, `privileged_access`, `exceptions`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `existing-platform`.

**Producer:** `secrets-and-configuration-management-engineer`; **receiver:** `environment-manager`.

**Receiving condition:** Static credentials only as a time-bound exception

**Next:** Step 6.

**Role output contracts:** `secrets-and-configuration-management-engineer:2`, `secrets-and-configuration-management-engineer:3`.

- **`handoff_credential_lifecycle`**: For dynamic short-lived credentials and a tested revocation path, supply the actual versioned credential lifecycle record, including service_identity, secret_references, issuance, expiry, revocation_test, exceptions. Independently assess the evidence against this exact criterion: Static credentials only as a time-bound exception. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `service_identity`, `secret_references`, `issuance`, `expiry`, `revocation_test`, `exceptions`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `data-ai/cloud-native`.

**Producer:** `secrets-and-configuration-management-engineer`; **receiver:** `environment-manager`.

**Receiving condition:** Static credentials only as a time-bound exception

**Next:** Step 6.

**Role output contracts:** `secrets-and-configuration-management-engineer:2`, `secrets-and-configuration-management-engineer:3`.

- **`handoff_credential_lifecycle`**: For dynamic short-lived credentials and a tested revocation path, supply the actual versioned credential lifecycle record, including service_identity, secret_references, issuance, expiry, revocation_test, exceptions. Independently assess the evidence against this exact criterion: Static credentials only as a time-bound exception. Do not substitute a related policy, plan or claimed execution for the required work product and observations. Cloud-native mechanism criterion: Static credentials only as a time-bound exception.
  Required fields: `service_identity`, `secret_references`, `issuance`, `expiry`, `revocation_test`, `exceptions`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `data-ai/saas-cots`.

**Producer:** `engagement:service-identity-owner`; **receiver:** `engagement:service-validation-owner`.

**Receiving condition:** Service identities and credentials have accountable ownership, bounded validity or rotation, tested revocation and controlled privileged access; any permitted exception needs its actual authority and expiry.

**Next:** Step 6.

**Role output contracts:** `identity-and-access-management-engineer:1`, `identity-and-access-management-engineer:2`.

- **`handoff_service_identity_lifecycle`**: Service identities and credentials have accountable ownership, bounded validity or rotation, tested revocation and controlled privileged access; any permitted exception needs its actual authority and expiry.
  Required fields: `service_identities`, `supplier_customer_owners`, `credential_references`, `expiry_or_rotation`, `revocation_evidence`, `privileged_access`, `exceptions`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `data-ai/existing-platform`.

**Producer:** `secrets-and-configuration-management-engineer`; **receiver:** `environment-manager`.

**Receiving condition:** Static credentials only as a time-bound exception

**Next:** Step 6.

**Role output contracts:** `secrets-and-configuration-management-engineer:2`, `secrets-and-configuration-management-engineer:3`.

- **`handoff_credential_lifecycle`**: For dynamic short-lived credentials and a tested revocation path, supply the actual versioned credential lifecycle record, including service_identity, secret_references, issuance, expiry, revocation_test, exceptions. Independently assess the evidence against this exact criterion: Static credentials only as a time-bound exception. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `service_identity`, `secret_references`, `issuance`, `expiry`, `revocation_test`, `exceptions`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `critical-regulated/cloud-native`.

**Producer:** `secrets-and-configuration-management-engineer`; **receiver:** `environment-manager`.

**Receiving condition:** Static credentials only as a time-bound exception

**Next:** Step 6.

**Role output contracts:** `secrets-and-configuration-management-engineer:2`, `secrets-and-configuration-management-engineer:3`.

- **`handoff_credential_lifecycle`**: For dynamic short-lived credentials and a tested revocation path, supply the actual versioned credential lifecycle record, including service_identity, secret_references, issuance, expiry, revocation_test, exceptions. Independently assess the evidence against this exact criterion: Static credentials only as a time-bound exception. Do not substitute a related policy, plan or claimed execution for the required work product and observations. Cloud-native mechanism criterion: Static credentials only as a time-bound exception.
  Required fields: `service_identity`, `secret_references`, `issuance`, `expiry`, `revocation_test`, `exceptions`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `critical-regulated/saas-cots`.

**Producer:** `engagement:service-identity-owner`; **receiver:** `engagement:service-validation-owner`.

**Receiving condition:** Service identities and credentials have accountable ownership, bounded validity or rotation, tested revocation and controlled privileged access; any permitted exception needs its actual authority and expiry.

**Next:** Step 6.

**Role output contracts:** `identity-and-access-management-engineer:1`, `identity-and-access-management-engineer:2`.

- **`handoff_service_identity_lifecycle`**: Service identities and credentials have accountable ownership, bounded validity or rotation, tested revocation and controlled privileged access; any permitted exception needs its actual authority and expiry.
  Required fields: `service_identities`, `supplier_customer_owners`, `credential_references`, `expiry_or_rotation`, `revocation_evidence`, `privileged_access`, `exceptions`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `critical-regulated/existing-platform`.

**Producer:** `secrets-and-configuration-management-engineer`; **receiver:** `environment-manager`.

**Receiving condition:** Static credentials only as a time-bound exception

**Next:** Step 6.

**Role output contracts:** `secrets-and-configuration-management-engineer:2`, `secrets-and-configuration-management-engineer:3`.

- **`handoff_credential_lifecycle`**: For dynamic short-lived credentials and a tested revocation path, supply the actual versioned credential lifecycle record, including service_identity, secret_references, issuance, expiry, revocation_test, exceptions. Independently assess the evidence against this exact criterion: Static credentials only as a time-bound exception. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `service_identity`, `secret_references`, `issuance`, `expiry`, `revocation_test`, `exceptions`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-new-service-onboarding-6"></a>

## environments with owners, refresh cadence and masked data

**Handoff content contract:** `handoff/new-service-onboarding:6`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_environment_baseline`**: For environments with owners, refresh cadence and masked data, supply the actual versioned environment baseline record, including environments, owners, refresh_schedule, data_classification, masking_evidence. Independently assess the evidence against this exact criterion: No unmasked production personal data anywhere. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `environments`, `owners`, `refresh_schedule`, `data_classification`, `masking_evidence`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `cloud-native`.

**Producer:** `environment-manager`; **receiver:** `gitops-and-continuous-delivery-engineer`.

**Receiving condition:** No unmasked production personal data anywhere

**Next:** Step 7.

**Role output contracts:** `environment-manager:1`, `environment-manager:2`, `environment-manager:3`.

- **`handoff_environment_baseline`**: For environments with owners, refresh cadence and masked data, supply the actual versioned environment baseline record, including environments, owners, refresh_schedule, data_classification, masking_evidence. Independently assess the evidence against this exact criterion: No unmasked production personal data anywhere. Do not substitute a related policy, plan or claimed execution for the required work product and observations. Cloud-native mechanism criterion: No unmasked production personal data anywhere.
  Required fields: `environments`, `owners`, `refresh_schedule`, `data_classification`, `masking_evidence`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `saas-cots`.

**Producer:** `engagement:service-validation-owner`; **receiver:** `engagement:service-change-owner`.

**Receiving condition:** Validation uses permitted tenant/sandbox/data scope and distinguishes supplier evidence from customer observations; no unmasked production personal data is copied into test scope.

**Next:** Step 7.

**Role output contracts:** `environment-manager:1`, `environment-manager:3`.

- **`handoff_supplier_service_validation`**: Validation uses permitted tenant/sandbox/data scope and distinguishes supplier evidence from customer observations; no unmasked production personal data is copied into test scope.
  Required fields: `validation_scope`, `tenant_or_sandbox`, `data_classification`, `permitted_data`, `supplier_test_evidence`, `customer_test_results`, `limitations`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `existing-platform`.

**Producer:** `environment-manager`; **receiver:** `engagement:service-change-owner`.

**Receiving condition:** No unmasked production personal data anywhere

**Next:** Step 7.

**Role output contracts:** `environment-manager:1`, `environment-manager:2`, `environment-manager:3`.

- **`handoff_environment_baseline`**: For environments with owners, refresh cadence and masked data, supply the actual versioned environment baseline record, including environments, owners, refresh_schedule, data_classification, masking_evidence. Independently assess the evidence against this exact criterion: No unmasked production personal data anywhere. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `environments`, `owners`, `refresh_schedule`, `data_classification`, `masking_evidence`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `data-ai/cloud-native`.

**Producer:** `environment-manager`; **receiver:** `gitops-and-continuous-delivery-engineer`.

**Receiving condition:** No unmasked production personal data anywhere

**Next:** Step 7.

**Role output contracts:** `environment-manager:1`, `environment-manager:2`, `environment-manager:3`.

- **`handoff_environment_baseline`**: For environments with owners, refresh cadence and masked data, supply the actual versioned environment baseline record, including environments, owners, refresh_schedule, data_classification, masking_evidence. Independently assess the evidence against this exact criterion: No unmasked production personal data anywhere. Do not substitute a related policy, plan or claimed execution for the required work product and observations. Cloud-native mechanism criterion: No unmasked production personal data anywhere.
  Required fields: `environments`, `owners`, `refresh_schedule`, `data_classification`, `masking_evidence`.
- **`handoff_data_model_validation`**: Validation identifies actual evaluated data/model versions, permitted scope, observed quality/performance/harms and excluded populations; synthetic or supplier results are labelled accurately.
  Required fields: `scope_ref`, `data_model_versions`, `permitted_test_scope`, `observed_evaluation`, `population_limits`, `unresolved_risks`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `data-ai/saas-cots`.

**Producer:** `engagement:service-validation-owner`; **receiver:** `engagement:service-change-owner`.

**Receiving condition:** Validation uses permitted tenant/sandbox/data scope and distinguishes supplier evidence from customer observations; no unmasked production personal data is copied into test scope.

**Next:** Step 7.

**Role output contracts:** `environment-manager:1`, `environment-manager:3`.

- **`handoff_supplier_service_validation`**: Validation uses permitted tenant/sandbox/data scope and distinguishes supplier evidence from customer observations; no unmasked production personal data is copied into test scope.
  Required fields: `validation_scope`, `tenant_or_sandbox`, `data_classification`, `permitted_data`, `supplier_test_evidence`, `customer_test_results`, `limitations`.
- **`handoff_data_model_validation`**: Validation identifies actual evaluated data/model versions, permitted scope, observed quality/performance/harms and excluded populations; synthetic or supplier results are labelled accurately.
  Required fields: `scope_ref`, `data_model_versions`, `permitted_test_scope`, `observed_evaluation`, `population_limits`, `unresolved_risks`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `data-ai/existing-platform`.

**Producer:** `environment-manager`; **receiver:** `engagement:service-change-owner`.

**Receiving condition:** No unmasked production personal data anywhere

**Next:** Step 7.

**Role output contracts:** `environment-manager:1`, `environment-manager:2`, `environment-manager:3`.

- **`handoff_environment_baseline`**: For environments with owners, refresh cadence and masked data, supply the actual versioned environment baseline record, including environments, owners, refresh_schedule, data_classification, masking_evidence. Independently assess the evidence against this exact criterion: No unmasked production personal data anywhere. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `environments`, `owners`, `refresh_schedule`, `data_classification`, `masking_evidence`.
- **`handoff_data_model_validation`**: Validation identifies actual evaluated data/model versions, permitted scope, observed quality/performance/harms and excluded populations; synthetic or supplier results are labelled accurately.
  Required fields: `scope_ref`, `data_model_versions`, `permitted_test_scope`, `observed_evaluation`, `population_limits`, `unresolved_risks`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `critical-regulated/cloud-native`.

**Producer:** `environment-manager`; **receiver:** `gitops-and-continuous-delivery-engineer`.

**Receiving condition:** No unmasked production personal data anywhere

**Next:** Step 7.

**Role output contracts:** `environment-manager:1`, `environment-manager:2`, `environment-manager:3`.

- **`handoff_environment_baseline`**: For environments with owners, refresh cadence and masked data, supply the actual versioned environment baseline record, including environments, owners, refresh_schedule, data_classification, masking_evidence. Independently assess the evidence against this exact criterion: No unmasked production personal data anywhere. Do not substitute a related policy, plan or claimed execution for the required work product and observations. Cloud-native mechanism criterion: No unmasked production personal data anywhere.
  Required fields: `environments`, `owners`, `refresh_schedule`, `data_classification`, `masking_evidence`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `critical-regulated/saas-cots`.

**Producer:** `engagement:service-validation-owner`; **receiver:** `engagement:service-change-owner`.

**Receiving condition:** Validation uses permitted tenant/sandbox/data scope and distinguishes supplier evidence from customer observations; no unmasked production personal data is copied into test scope.

**Next:** Step 7.

**Role output contracts:** `environment-manager:1`, `environment-manager:3`.

- **`handoff_supplier_service_validation`**: Validation uses permitted tenant/sandbox/data scope and distinguishes supplier evidence from customer observations; no unmasked production personal data is copied into test scope.
  Required fields: `validation_scope`, `tenant_or_sandbox`, `data_classification`, `permitted_data`, `supplier_test_evidence`, `customer_test_results`, `limitations`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `critical-regulated/existing-platform`.

**Producer:** `environment-manager`; **receiver:** `engagement:service-change-owner`.

**Receiving condition:** No unmasked production personal data anywhere

**Next:** Step 7.

**Role output contracts:** `environment-manager:1`, `environment-manager:2`, `environment-manager:3`.

- **`handoff_environment_baseline`**: For environments with owners, refresh cadence and masked data, supply the actual versioned environment baseline record, including environments, owners, refresh_schedule, data_classification, masking_evidence. Independently assess the evidence against this exact criterion: No unmasked production personal data anywhere. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `environments`, `owners`, `refresh_schedule`, `data_classification`, `masking_evidence`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-new-service-onboarding-7"></a>

## service promotion or supplier-change model and recovery evidence

**Handoff content contract:** `handoff/new-service-onboarding:7`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_promotion_model`**: For service promotion or supplier-change model and recovery evidence, supply the actual versioned promotion model record, including desired_state_revision, promoted_digest, environment_sequence, approval_points, rollback_route. Independently assess the evidence against this exact criterion: Change identity and sequence are traceable; recovery and escalation limits are explicit and validated. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `desired_state_revision`, `promoted_digest`, `environment_sequence`, `approval_points`, `rollback_route`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `cloud-native`.

**Producer:** `gitops-and-continuous-delivery-engineer`; **receiver:** `observability-engineer`.

**Receiving condition:** The same immutable artefact is promoted, never rebuilt

**Next:** Step 8.

**Role output contracts:** `gitops-and-continuous-delivery-engineer:1`.

- **`handoff_promotion_model`**: For service promotion or supplier-change model and recovery evidence, supply the actual versioned promotion model record, including desired_state_revision, promoted_digest, environment_sequence, approval_points, rollback_route. Independently assess the evidence against this exact criterion: Change identity and sequence are traceable; recovery and escalation limits are explicit and validated. Do not substitute a related policy, plan or claimed execution for the required work product and observations. Cloud-native mechanism criterion: The same immutable artefact is promoted, never rebuilt.
  Required fields: `desired_state_revision`, `promoted_digest`, `environment_sequence`, `approval_points`, `rollback_route`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `saas-cots`.

**Producer:** `engagement:service-change-owner`; **receiver:** `observability-engineer`.

**Receiving condition:** Supplier releases and customer configuration changes retain exact identity, controlled sequence, verification and an evidenced recovery/escalation route; unavailable supplier rollback is disclosed rather than fabricated.

**Next:** Step 8.

**Role output contracts:** `release-engineer:1`, `release-engineer:4`.

- **`handoff_supplier_release_recovery`**: Supplier releases and customer configuration changes retain exact identity, controlled sequence, verification and an evidenced recovery/escalation route; unavailable supplier rollback is disclosed rather than fabricated.
  Required fields: `service_release`, `configuration_revision`, `supplier_change_notifications`, `customer_promotion`, `verification`, `recovery_escalation_evidence`, `limitations`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `existing-platform`.

**Producer:** `engagement:service-change-owner`; **receiver:** `observability-engineer`.

**Receiving condition:** Actual release/configuration revisions are promoted in a controlled sequence with an evidenced recovery route; GitOps repositories are required only for the GitOps mechanism.

**Next:** Step 8.

**Role output contracts:** `release-engineer:1`, `release-engineer:4`.

- **`handoff_platform_service_promotion`**: Actual release/configuration revisions are promoted in a controlled sequence with an evidenced recovery route; GitOps repositories are required only for the GitOps mechanism.
  Required fields: `platform_revision`, `release_revision`, `configuration_deltas`, `promotion_sequence`, `verification`, `rollback_forward_recovery`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `data-ai/cloud-native`.

**Producer:** `gitops-and-continuous-delivery-engineer`; **receiver:** `observability-engineer`.

**Receiving condition:** The same immutable artefact is promoted, never rebuilt

**Next:** Step 8.

**Role output contracts:** `gitops-and-continuous-delivery-engineer:1`.

- **`handoff_promotion_model`**: For service promotion or supplier-change model and recovery evidence, supply the actual versioned promotion model record, including desired_state_revision, promoted_digest, environment_sequence, approval_points, rollback_route. Independently assess the evidence against this exact criterion: Change identity and sequence are traceable; recovery and escalation limits are explicit and validated. Do not substitute a related policy, plan or claimed execution for the required work product and observations. Cloud-native mechanism criterion: The same immutable artefact is promoted, never rebuilt.
  Required fields: `desired_state_revision`, `promoted_digest`, `environment_sequence`, `approval_points`, `rollback_route`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `data-ai/saas-cots`.

**Producer:** `engagement:service-change-owner`; **receiver:** `observability-engineer`.

**Receiving condition:** Supplier releases and customer configuration changes retain exact identity, controlled sequence, verification and an evidenced recovery/escalation route; unavailable supplier rollback is disclosed rather than fabricated.

**Next:** Step 8.

**Role output contracts:** `release-engineer:1`, `release-engineer:4`.

- **`handoff_supplier_release_recovery`**: Supplier releases and customer configuration changes retain exact identity, controlled sequence, verification and an evidenced recovery/escalation route; unavailable supplier rollback is disclosed rather than fabricated.
  Required fields: `service_release`, `configuration_revision`, `supplier_change_notifications`, `customer_promotion`, `verification`, `recovery_escalation_evidence`, `limitations`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `data-ai/existing-platform`.

**Producer:** `engagement:service-change-owner`; **receiver:** `observability-engineer`.

**Receiving condition:** Actual release/configuration revisions are promoted in a controlled sequence with an evidenced recovery route; GitOps repositories are required only for the GitOps mechanism.

**Next:** Step 8.

**Role output contracts:** `release-engineer:1`, `release-engineer:4`.

- **`handoff_platform_service_promotion`**: Actual release/configuration revisions are promoted in a controlled sequence with an evidenced recovery route; GitOps repositories are required only for the GitOps mechanism.
  Required fields: `platform_revision`, `release_revision`, `configuration_deltas`, `promotion_sequence`, `verification`, `rollback_forward_recovery`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `critical-regulated/cloud-native`.

**Producer:** `gitops-and-continuous-delivery-engineer`; **receiver:** `observability-engineer`.

**Receiving condition:** The same immutable artefact is promoted, never rebuilt

**Next:** Step 8.

**Role output contracts:** `gitops-and-continuous-delivery-engineer:1`.

- **`handoff_promotion_model`**: For service promotion or supplier-change model and recovery evidence, supply the actual versioned promotion model record, including desired_state_revision, promoted_digest, environment_sequence, approval_points, rollback_route. Independently assess the evidence against this exact criterion: Change identity and sequence are traceable; recovery and escalation limits are explicit and validated. Do not substitute a related policy, plan or claimed execution for the required work product and observations. Cloud-native mechanism criterion: The same immutable artefact is promoted, never rebuilt.
  Required fields: `desired_state_revision`, `promoted_digest`, `environment_sequence`, `approval_points`, `rollback_route`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `critical-regulated/saas-cots`.

**Producer:** `engagement:service-change-owner`; **receiver:** `observability-engineer`.

**Receiving condition:** Supplier releases and customer configuration changes retain exact identity, controlled sequence, verification and an evidenced recovery/escalation route; unavailable supplier rollback is disclosed rather than fabricated.

**Next:** Step 8.

**Role output contracts:** `release-engineer:1`, `release-engineer:4`.

- **`handoff_supplier_release_recovery`**: Supplier releases and customer configuration changes retain exact identity, controlled sequence, verification and an evidenced recovery/escalation route; unavailable supplier rollback is disclosed rather than fabricated.
  Required fields: `service_release`, `configuration_revision`, `supplier_change_notifications`, `customer_promotion`, `verification`, `recovery_escalation_evidence`, `limitations`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `critical-regulated/existing-platform`.

**Producer:** `engagement:service-change-owner`; **receiver:** `observability-engineer`.

**Receiving condition:** Actual release/configuration revisions are promoted in a controlled sequence with an evidenced recovery route; GitOps repositories are required only for the GitOps mechanism.

**Next:** Step 8.

**Role output contracts:** `release-engineer:1`, `release-engineer:4`.

- **`handoff_platform_service_promotion`**: Actual release/configuration revisions are promoted in a controlled sequence with an evidenced recovery route; GitOps repositories are required only for the GitOps mechanism.
  Required fields: `platform_revision`, `release_revision`, `configuration_deltas`, `promotion_sequence`, `verification`, `rollback_forward_recovery`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-new-service-onboarding-8"></a>

## dashboards and owned, actionable alerts

**Handoff content contract:** `handoff/new-service-onboarding:8`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_monitoring_baseline`**: For dashboards and owned, actionable alerts, supply the actual versioned monitoring baseline record, including service_indicators, dashboards, alert_conditions, alert_owners, runbook_refs. Independently assess the evidence against this exact criterion: Every alert has an owner, an action and a runbook. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `service_indicators`, `dashboards`, `alert_conditions`, `alert_owners`, `runbook_refs`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `cloud-native`.

**Producer:** `observability-engineer`; **receiver:** `site-reliability-engineer`.

**Receiving condition:** Every alert has an owner, an action and a runbook

**Next:** Step 9.

**Role output contracts:** `observability-engineer:2`, `observability-engineer:3`.

- **`handoff_monitoring_baseline`**: For dashboards and owned, actionable alerts, supply the actual versioned monitoring baseline record, including service_indicators, dashboards, alert_conditions, alert_owners, runbook_refs. Independently assess the evidence against this exact criterion: Every alert has an owner, an action and a runbook. Do not substitute a related policy, plan or claimed execution for the required work product and observations. Cloud-native mechanism criterion: Every alert has an owner, an action and a runbook.
  Required fields: `service_indicators`, `dashboards`, `alert_conditions`, `alert_owners`, `runbook_refs`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `saas-cots`.

**Producer:** `observability-engineer`; **receiver:** `site-reliability-engineer`.

**Receiving condition:** Every alert has an owner, an action and a runbook

**Next:** Step 9.

**Role output contracts:** `observability-engineer:2`, `observability-engineer:3`.

- **`handoff_monitoring_baseline`**: For dashboards and owned, actionable alerts, supply the actual versioned monitoring baseline record, including service_indicators, dashboards, alert_conditions, alert_owners, runbook_refs. Independently assess the evidence against this exact criterion: Every alert has an owner, an action and a runbook. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `service_indicators`, `dashboards`, `alert_conditions`, `alert_owners`, `runbook_refs`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `existing-platform`.

**Producer:** `observability-engineer`; **receiver:** `site-reliability-engineer`.

**Receiving condition:** Every alert has an owner, an action and a runbook

**Next:** Step 9.

**Role output contracts:** `observability-engineer:2`, `observability-engineer:3`.

- **`handoff_monitoring_baseline`**: For dashboards and owned, actionable alerts, supply the actual versioned monitoring baseline record, including service_indicators, dashboards, alert_conditions, alert_owners, runbook_refs. Independently assess the evidence against this exact criterion: Every alert has an owner, an action and a runbook. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `service_indicators`, `dashboards`, `alert_conditions`, `alert_owners`, `runbook_refs`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `data-ai/cloud-native`.

**Producer:** `observability-engineer`; **receiver:** `site-reliability-engineer`.

**Receiving condition:** Every alert has an owner, an action and a runbook

**Next:** Step 9.

**Role output contracts:** `observability-engineer:2`, `observability-engineer:3`.

- **`handoff_monitoring_baseline`**: For dashboards and owned, actionable alerts, supply the actual versioned monitoring baseline record, including service_indicators, dashboards, alert_conditions, alert_owners, runbook_refs. Independently assess the evidence against this exact criterion: Every alert has an owner, an action and a runbook. Do not substitute a related policy, plan or claimed execution for the required work product and observations. Cloud-native mechanism criterion: Every alert has an owner, an action and a runbook.
  Required fields: `service_indicators`, `dashboards`, `alert_conditions`, `alert_owners`, `runbook_refs`.
- **`handoff_data_model_monitoring`**: The operating model defines owned quality/drift monitoring, meaningful thresholds and an authorised withdrawal/retraining route for the exact data/model scope.
  Required fields: `scope_ref`, `operating_version`, `quality_drift_signals`, `thresholds`, `accountable_owner`, `withdrawal_retraining_route`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `data-ai/saas-cots`.

**Producer:** `observability-engineer`; **receiver:** `site-reliability-engineer`.

**Receiving condition:** Every alert has an owner, an action and a runbook

**Next:** Step 9.

**Role output contracts:** `observability-engineer:2`, `observability-engineer:3`.

- **`handoff_monitoring_baseline`**: For dashboards and owned, actionable alerts, supply the actual versioned monitoring baseline record, including service_indicators, dashboards, alert_conditions, alert_owners, runbook_refs. Independently assess the evidence against this exact criterion: Every alert has an owner, an action and a runbook. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `service_indicators`, `dashboards`, `alert_conditions`, `alert_owners`, `runbook_refs`.
- **`handoff_data_model_monitoring`**: The operating model defines owned quality/drift monitoring, meaningful thresholds and an authorised withdrawal/retraining route for the exact data/model scope.
  Required fields: `scope_ref`, `operating_version`, `quality_drift_signals`, `thresholds`, `accountable_owner`, `withdrawal_retraining_route`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `data-ai/existing-platform`.

**Producer:** `observability-engineer`; **receiver:** `site-reliability-engineer`.

**Receiving condition:** Every alert has an owner, an action and a runbook

**Next:** Step 9.

**Role output contracts:** `observability-engineer:2`, `observability-engineer:3`.

- **`handoff_monitoring_baseline`**: For dashboards and owned, actionable alerts, supply the actual versioned monitoring baseline record, including service_indicators, dashboards, alert_conditions, alert_owners, runbook_refs. Independently assess the evidence against this exact criterion: Every alert has an owner, an action and a runbook. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `service_indicators`, `dashboards`, `alert_conditions`, `alert_owners`, `runbook_refs`.
- **`handoff_data_model_monitoring`**: The operating model defines owned quality/drift monitoring, meaningful thresholds and an authorised withdrawal/retraining route for the exact data/model scope.
  Required fields: `scope_ref`, `operating_version`, `quality_drift_signals`, `thresholds`, `accountable_owner`, `withdrawal_retraining_route`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `critical-regulated/cloud-native`.

**Producer:** `observability-engineer`; **receiver:** `site-reliability-engineer`.

**Receiving condition:** Every alert has an owner, an action and a runbook

**Next:** Step 9.

**Role output contracts:** `observability-engineer:2`, `observability-engineer:3`.

- **`handoff_monitoring_baseline`**: For dashboards and owned, actionable alerts, supply the actual versioned monitoring baseline record, including service_indicators, dashboards, alert_conditions, alert_owners, runbook_refs. Independently assess the evidence against this exact criterion: Every alert has an owner, an action and a runbook. Do not substitute a related policy, plan or claimed execution for the required work product and observations. Cloud-native mechanism criterion: Every alert has an owner, an action and a runbook.
  Required fields: `service_indicators`, `dashboards`, `alert_conditions`, `alert_owners`, `runbook_refs`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `critical-regulated/saas-cots`.

**Producer:** `observability-engineer`; **receiver:** `site-reliability-engineer`.

**Receiving condition:** Every alert has an owner, an action and a runbook

**Next:** Step 9.

**Role output contracts:** `observability-engineer:2`, `observability-engineer:3`.

- **`handoff_monitoring_baseline`**: For dashboards and owned, actionable alerts, supply the actual versioned monitoring baseline record, including service_indicators, dashboards, alert_conditions, alert_owners, runbook_refs. Independently assess the evidence against this exact criterion: Every alert has an owner, an action and a runbook. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `service_indicators`, `dashboards`, `alert_conditions`, `alert_owners`, `runbook_refs`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `critical-regulated/existing-platform`.

**Producer:** `observability-engineer`; **receiver:** `site-reliability-engineer`.

**Receiving condition:** Every alert has an owner, an action and a runbook

**Next:** Step 9.

**Role output contracts:** `observability-engineer:2`, `observability-engineer:3`.

- **`handoff_monitoring_baseline`**: For dashboards and owned, actionable alerts, supply the actual versioned monitoring baseline record, including service_indicators, dashboards, alert_conditions, alert_owners, runbook_refs. Independently assess the evidence against this exact criterion: Every alert has an owner, an action and a runbook. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `service_indicators`, `dashboards`, `alert_conditions`, `alert_owners`, `runbook_refs`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-new-service-onboarding-9"></a>

## SLOs and error budget policy

**Handoff content contract:** `handoff/new-service-onboarding:9`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_service_objectives`**: For SLOs and error budget policy, supply the actual versioned service objectives record, including indicator_definitions, objectives, data_sources, error_budget, decision_thresholds, policy_owners. Independently assess the evidence against this exact criterion: Exhausting the budget changes something, or the SLO is decorative. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `indicator_definitions`, `objectives`, `data_sources`, `error_budget`, `decision_thresholds`, `policy_owners`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `cloud-native`.

**Producer:** `site-reliability-engineer`; **receiver:** `application-support-analyst`.

**Receiving condition:** Exhausting the budget changes something, or the SLO is decorative

**Next:** Step 10.

**Role output contracts:** `site-reliability-engineer:1`.

- **`handoff_service_objectives`**: For SLOs and error budget policy, supply the actual versioned service objectives record, including indicator_definitions, objectives, data_sources, error_budget, decision_thresholds, policy_owners. Independently assess the evidence against this exact criterion: Exhausting the budget changes something, or the SLO is decorative. Do not substitute a related policy, plan or claimed execution for the required work product and observations. Cloud-native mechanism criterion: Exhausting the budget changes something, or the SLO is decorative.
  Required fields: `indicator_definitions`, `objectives`, `data_sources`, `error_budget`, `decision_thresholds`, `policy_owners`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `saas-cots`.

**Producer:** `site-reliability-engineer`; **receiver:** `application-support-analyst`.

**Receiving condition:** Exhausting the budget changes something, or the SLO is decorative

**Next:** Step 10.

**Role output contracts:** `site-reliability-engineer:1`.

- **`handoff_service_objectives`**: For SLOs and error budget policy, supply the actual versioned service objectives record, including indicator_definitions, objectives, data_sources, error_budget, decision_thresholds, policy_owners. Independently assess the evidence against this exact criterion: Exhausting the budget changes something, or the SLO is decorative. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `indicator_definitions`, `objectives`, `data_sources`, `error_budget`, `decision_thresholds`, `policy_owners`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `existing-platform`.

**Producer:** `site-reliability-engineer`; **receiver:** `application-support-analyst`.

**Receiving condition:** Exhausting the budget changes something, or the SLO is decorative

**Next:** Step 10.

**Role output contracts:** `site-reliability-engineer:1`.

- **`handoff_service_objectives`**: For SLOs and error budget policy, supply the actual versioned service objectives record, including indicator_definitions, objectives, data_sources, error_budget, decision_thresholds, policy_owners. Independently assess the evidence against this exact criterion: Exhausting the budget changes something, or the SLO is decorative. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `indicator_definitions`, `objectives`, `data_sources`, `error_budget`, `decision_thresholds`, `policy_owners`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `data-ai/cloud-native`.

**Producer:** `site-reliability-engineer`; **receiver:** `application-support-analyst`.

**Receiving condition:** Exhausting the budget changes something, or the SLO is decorative

**Next:** Step 10.

**Role output contracts:** `site-reliability-engineer:1`.

- **`handoff_service_objectives`**: For SLOs and error budget policy, supply the actual versioned service objectives record, including indicator_definitions, objectives, data_sources, error_budget, decision_thresholds, policy_owners. Independently assess the evidence against this exact criterion: Exhausting the budget changes something, or the SLO is decorative. Do not substitute a related policy, plan or claimed execution for the required work product and observations. Cloud-native mechanism criterion: Exhausting the budget changes something, or the SLO is decorative.
  Required fields: `indicator_definitions`, `objectives`, `data_sources`, `error_budget`, `decision_thresholds`, `policy_owners`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `data-ai/saas-cots`.

**Producer:** `site-reliability-engineer`; **receiver:** `application-support-analyst`.

**Receiving condition:** Exhausting the budget changes something, or the SLO is decorative

**Next:** Step 10.

**Role output contracts:** `site-reliability-engineer:1`.

- **`handoff_service_objectives`**: For SLOs and error budget policy, supply the actual versioned service objectives record, including indicator_definitions, objectives, data_sources, error_budget, decision_thresholds, policy_owners. Independently assess the evidence against this exact criterion: Exhausting the budget changes something, or the SLO is decorative. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `indicator_definitions`, `objectives`, `data_sources`, `error_budget`, `decision_thresholds`, `policy_owners`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `data-ai/existing-platform`.

**Producer:** `site-reliability-engineer`; **receiver:** `application-support-analyst`.

**Receiving condition:** Exhausting the budget changes something, or the SLO is decorative

**Next:** Step 10.

**Role output contracts:** `site-reliability-engineer:1`.

- **`handoff_service_objectives`**: For SLOs and error budget policy, supply the actual versioned service objectives record, including indicator_definitions, objectives, data_sources, error_budget, decision_thresholds, policy_owners. Independently assess the evidence against this exact criterion: Exhausting the budget changes something, or the SLO is decorative. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `indicator_definitions`, `objectives`, `data_sources`, `error_budget`, `decision_thresholds`, `policy_owners`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `critical-regulated/cloud-native`.

**Producer:** `site-reliability-engineer`; **receiver:** `application-support-analyst`.

**Receiving condition:** Exhausting the budget changes something, or the SLO is decorative

**Next:** Step 10.

**Role output contracts:** `site-reliability-engineer:1`.

- **`handoff_service_objectives`**: For SLOs and error budget policy, supply the actual versioned service objectives record, including indicator_definitions, objectives, data_sources, error_budget, decision_thresholds, policy_owners. Independently assess the evidence against this exact criterion: Exhausting the budget changes something, or the SLO is decorative. Do not substitute a related policy, plan or claimed execution for the required work product and observations. Cloud-native mechanism criterion: Exhausting the budget changes something, or the SLO is decorative.
  Required fields: `indicator_definitions`, `objectives`, `data_sources`, `error_budget`, `decision_thresholds`, `policy_owners`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `critical-regulated/saas-cots`.

**Producer:** `site-reliability-engineer`; **receiver:** `application-support-analyst`.

**Receiving condition:** Exhausting the budget changes something, or the SLO is decorative

**Next:** Step 10.

**Role output contracts:** `site-reliability-engineer:1`.

- **`handoff_service_objectives`**: For SLOs and error budget policy, supply the actual versioned service objectives record, including indicator_definitions, objectives, data_sources, error_budget, decision_thresholds, policy_owners. Independently assess the evidence against this exact criterion: Exhausting the budget changes something, or the SLO is decorative. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `indicator_definitions`, `objectives`, `data_sources`, `error_budget`, `decision_thresholds`, `policy_owners`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `critical-regulated/existing-platform`.

**Producer:** `site-reliability-engineer`; **receiver:** `application-support-analyst`.

**Receiving condition:** Exhausting the budget changes something, or the SLO is decorative

**Next:** Step 10.

**Role output contracts:** `site-reliability-engineer:1`.

- **`handoff_service_objectives`**: For SLOs and error budget policy, supply the actual versioned service objectives record, including indicator_definitions, objectives, data_sources, error_budget, decision_thresholds, policy_owners. Independently assess the evidence against this exact criterion: Exhausting the budget changes something, or the SLO is decorative. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `indicator_definitions`, `objectives`, `data_sources`, `error_budget`, `decision_thresholds`, `policy_owners`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-new-service-onboarding-10"></a>

## runbook and known-error entries

**Handoff content contract:** `handoff/new-service-onboarding:10`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_support_handover`**: For runbook and known-error entries, supply the actual versioned support handover record, including runbook_revision, known_errors, support_owner, rehearsal_evidence, escalation. Independently assess the evidence against this exact criterion: A competent on-call engineer who has never seen it can follow it. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `runbook_revision`, `known_errors`, `support_owner`, `rehearsal_evidence`, `escalation`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `cloud-native`.

**Producer:** `application-support-analyst`; **receiver:** `configuration-manager`.

**Receiving condition:** A competent on-call engineer who has never seen it can follow it

**Next:** Step 11.

**Role output contracts:** `application-support-analyst:2`.

- **`handoff_support_handover`**: For runbook and known-error entries, supply the actual versioned support handover record, including runbook_revision, known_errors, support_owner, rehearsal_evidence, escalation. Independently assess the evidence against this exact criterion: A competent on-call engineer who has never seen it can follow it. Do not substitute a related policy, plan or claimed execution for the required work product and observations. Cloud-native mechanism criterion: A competent on-call engineer who has never seen it can follow it.
  Required fields: `runbook_revision`, `known_errors`, `support_owner`, `rehearsal_evidence`, `escalation`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `saas-cots`.

**Producer:** `application-support-analyst`; **receiver:** `configuration-manager`.

**Receiving condition:** A competent on-call engineer who has never seen it can follow it

**Next:** Step 11.

**Role output contracts:** `application-support-analyst:2`.

- **`handoff_support_handover`**: For runbook and known-error entries, supply the actual versioned support handover record, including runbook_revision, known_errors, support_owner, rehearsal_evidence, escalation. Independently assess the evidence against this exact criterion: A competent on-call engineer who has never seen it can follow it. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `runbook_revision`, `known_errors`, `support_owner`, `rehearsal_evidence`, `escalation`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `existing-platform`.

**Producer:** `application-support-analyst`; **receiver:** `configuration-manager`.

**Receiving condition:** A competent on-call engineer who has never seen it can follow it

**Next:** Step 11.

**Role output contracts:** `application-support-analyst:2`.

- **`handoff_support_handover`**: For runbook and known-error entries, supply the actual versioned support handover record, including runbook_revision, known_errors, support_owner, rehearsal_evidence, escalation. Independently assess the evidence against this exact criterion: A competent on-call engineer who has never seen it can follow it. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `runbook_revision`, `known_errors`, `support_owner`, `rehearsal_evidence`, `escalation`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `data-ai/cloud-native`.

**Producer:** `application-support-analyst`; **receiver:** `configuration-manager`.

**Receiving condition:** A competent on-call engineer who has never seen it can follow it

**Next:** Step 11.

**Role output contracts:** `application-support-analyst:2`.

- **`handoff_support_handover`**: For runbook and known-error entries, supply the actual versioned support handover record, including runbook_revision, known_errors, support_owner, rehearsal_evidence, escalation. Independently assess the evidence against this exact criterion: A competent on-call engineer who has never seen it can follow it. Do not substitute a related policy, plan or claimed execution for the required work product and observations. Cloud-native mechanism criterion: A competent on-call engineer who has never seen it can follow it.
  Required fields: `runbook_revision`, `known_errors`, `support_owner`, `rehearsal_evidence`, `escalation`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `data-ai/saas-cots`.

**Producer:** `application-support-analyst`; **receiver:** `configuration-manager`.

**Receiving condition:** A competent on-call engineer who has never seen it can follow it

**Next:** Step 11.

**Role output contracts:** `application-support-analyst:2`.

- **`handoff_support_handover`**: For runbook and known-error entries, supply the actual versioned support handover record, including runbook_revision, known_errors, support_owner, rehearsal_evidence, escalation. Independently assess the evidence against this exact criterion: A competent on-call engineer who has never seen it can follow it. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `runbook_revision`, `known_errors`, `support_owner`, `rehearsal_evidence`, `escalation`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `data-ai/existing-platform`.

**Producer:** `application-support-analyst`; **receiver:** `configuration-manager`.

**Receiving condition:** A competent on-call engineer who has never seen it can follow it

**Next:** Step 11.

**Role output contracts:** `application-support-analyst:2`.

- **`handoff_support_handover`**: For runbook and known-error entries, supply the actual versioned support handover record, including runbook_revision, known_errors, support_owner, rehearsal_evidence, escalation. Independently assess the evidence against this exact criterion: A competent on-call engineer who has never seen it can follow it. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `runbook_revision`, `known_errors`, `support_owner`, `rehearsal_evidence`, `escalation`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `critical-regulated/cloud-native`.

**Producer:** `application-support-analyst`; **receiver:** `configuration-manager`.

**Receiving condition:** A competent on-call engineer who has never seen it can follow it

**Next:** Step 11.

**Role output contracts:** `application-support-analyst:2`.

- **`handoff_support_handover`**: For runbook and known-error entries, supply the actual versioned support handover record, including runbook_revision, known_errors, support_owner, rehearsal_evidence, escalation. Independently assess the evidence against this exact criterion: A competent on-call engineer who has never seen it can follow it. Do not substitute a related policy, plan or claimed execution for the required work product and observations. Cloud-native mechanism criterion: A competent on-call engineer who has never seen it can follow it.
  Required fields: `runbook_revision`, `known_errors`, `support_owner`, `rehearsal_evidence`, `escalation`.
- **`handoff_critical_service_handover`**: Support handover includes actual recovery, retention/access and segregation evidence appropriate to the scope; critical unresolved readiness gaps cannot be closed by choosing another hosting mechanism.
  Required fields: `scope_ref`, `recovery_objectives`, `retention_access_controls`, `segregation_evidence`, `observed_rehearsal`, `receiving_owner`, `unresolved_gaps`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `critical-regulated/saas-cots`.

**Producer:** `application-support-analyst`; **receiver:** `configuration-manager`.

**Receiving condition:** A competent on-call engineer who has never seen it can follow it

**Next:** Step 11.

**Role output contracts:** `application-support-analyst:2`.

- **`handoff_support_handover`**: For runbook and known-error entries, supply the actual versioned support handover record, including runbook_revision, known_errors, support_owner, rehearsal_evidence, escalation. Independently assess the evidence against this exact criterion: A competent on-call engineer who has never seen it can follow it. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `runbook_revision`, `known_errors`, `support_owner`, `rehearsal_evidence`, `escalation`.
- **`handoff_critical_service_handover`**: Support handover includes actual recovery, retention/access and segregation evidence appropriate to the scope; critical unresolved readiness gaps cannot be closed by choosing another hosting mechanism.
  Required fields: `scope_ref`, `recovery_objectives`, `retention_access_controls`, `segregation_evidence`, `observed_rehearsal`, `receiving_owner`, `unresolved_gaps`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `critical-regulated/existing-platform`.

**Producer:** `application-support-analyst`; **receiver:** `configuration-manager`.

**Receiving condition:** A competent on-call engineer who has never seen it can follow it

**Next:** Step 11.

**Role output contracts:** `application-support-analyst:2`.

- **`handoff_support_handover`**: For runbook and known-error entries, supply the actual versioned support handover record, including runbook_revision, known_errors, support_owner, rehearsal_evidence, escalation. Independently assess the evidence against this exact criterion: A competent on-call engineer who has never seen it can follow it. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `runbook_revision`, `known_errors`, `support_owner`, `rehearsal_evidence`, `escalation`.
- **`handoff_critical_service_handover`**: Support handover includes actual recovery, retention/access and segregation evidence appropriate to the scope; critical unresolved readiness gaps cannot be closed by choosing another hosting mechanism.
  Required fields: `scope_ref`, `recovery_objectives`, `retention_access_controls`, `segregation_evidence`, `observed_rehearsal`, `receiving_owner`, `unresolved_gaps`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-new-service-onboarding-11"></a>

## configuration items with verified relationships

**Handoff content contract:** `handoff/new-service-onboarding:11`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_configuration_records`**: For configuration items with verified relationships, supply the actual versioned configuration records record, including configuration_ids, relationships, owner, lifecycle, verified_at, reconciliation_source. Independently assess the evidence against this exact criterion: Owner, lifecycle status and verified-by date present. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `configuration_ids`, `relationships`, `owner`, `lifecycle`, `verified_at`, `reconciliation_source`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `cloud-native`.

**Producer:** `configuration-manager`; **receiver:** `it-service-owner`.

**Receiving condition:** Owner, lifecycle status and verified-by date present

**Next:** Step 12.

**Role output contracts:** `configuration-manager:3`.

- **`handoff_configuration_records`**: For configuration items with verified relationships, supply the actual versioned configuration records record, including configuration_ids, relationships, owner, lifecycle, verified_at, reconciliation_source. Independently assess the evidence against this exact criterion: Owner, lifecycle status and verified-by date present. Do not substitute a related policy, plan or claimed execution for the required work product and observations. Cloud-native mechanism criterion: Owner, lifecycle status and verified-by date present.
  Required fields: `configuration_ids`, `relationships`, `owner`, `lifecycle`, `verified_at`, `reconciliation_source`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `saas-cots`.

**Producer:** `configuration-manager`; **receiver:** `it-service-owner`.

**Receiving condition:** Owner, lifecycle status and verified-by date present

**Next:** Step 12.

**Role output contracts:** `configuration-manager:3`.

- **`handoff_configuration_records`**: For configuration items with verified relationships, supply the actual versioned configuration records record, including configuration_ids, relationships, owner, lifecycle, verified_at, reconciliation_source. Independently assess the evidence against this exact criterion: Owner, lifecycle status and verified-by date present. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `configuration_ids`, `relationships`, `owner`, `lifecycle`, `verified_at`, `reconciliation_source`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `existing-platform`.

**Producer:** `configuration-manager`; **receiver:** `it-service-owner`.

**Receiving condition:** Owner, lifecycle status and verified-by date present

**Next:** Step 12.

**Role output contracts:** `configuration-manager:3`.

- **`handoff_configuration_records`**: For configuration items with verified relationships, supply the actual versioned configuration records record, including configuration_ids, relationships, owner, lifecycle, verified_at, reconciliation_source. Independently assess the evidence against this exact criterion: Owner, lifecycle status and verified-by date present. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `configuration_ids`, `relationships`, `owner`, `lifecycle`, `verified_at`, `reconciliation_source`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `data-ai/cloud-native`.

**Producer:** `configuration-manager`; **receiver:** `it-service-owner`.

**Receiving condition:** Owner, lifecycle status and verified-by date present

**Next:** Step 12.

**Role output contracts:** `configuration-manager:3`.

- **`handoff_configuration_records`**: For configuration items with verified relationships, supply the actual versioned configuration records record, including configuration_ids, relationships, owner, lifecycle, verified_at, reconciliation_source. Independently assess the evidence against this exact criterion: Owner, lifecycle status and verified-by date present. Do not substitute a related policy, plan or claimed execution for the required work product and observations. Cloud-native mechanism criterion: Owner, lifecycle status and verified-by date present.
  Required fields: `configuration_ids`, `relationships`, `owner`, `lifecycle`, `verified_at`, `reconciliation_source`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `data-ai/saas-cots`.

**Producer:** `configuration-manager`; **receiver:** `it-service-owner`.

**Receiving condition:** Owner, lifecycle status and verified-by date present

**Next:** Step 12.

**Role output contracts:** `configuration-manager:3`.

- **`handoff_configuration_records`**: For configuration items with verified relationships, supply the actual versioned configuration records record, including configuration_ids, relationships, owner, lifecycle, verified_at, reconciliation_source. Independently assess the evidence against this exact criterion: Owner, lifecycle status and verified-by date present. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `configuration_ids`, `relationships`, `owner`, `lifecycle`, `verified_at`, `reconciliation_source`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `data-ai/existing-platform`.

**Producer:** `configuration-manager`; **receiver:** `it-service-owner`.

**Receiving condition:** Owner, lifecycle status and verified-by date present

**Next:** Step 12.

**Role output contracts:** `configuration-manager:3`.

- **`handoff_configuration_records`**: For configuration items with verified relationships, supply the actual versioned configuration records record, including configuration_ids, relationships, owner, lifecycle, verified_at, reconciliation_source. Independently assess the evidence against this exact criterion: Owner, lifecycle status and verified-by date present. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `configuration_ids`, `relationships`, `owner`, `lifecycle`, `verified_at`, `reconciliation_source`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `critical-regulated/cloud-native`.

**Producer:** `configuration-manager`; **receiver:** `it-service-owner`.

**Receiving condition:** Owner, lifecycle status and verified-by date present

**Next:** Step 12.

**Role output contracts:** `configuration-manager:3`.

- **`handoff_configuration_records`**: For configuration items with verified relationships, supply the actual versioned configuration records record, including configuration_ids, relationships, owner, lifecycle, verified_at, reconciliation_source. Independently assess the evidence against this exact criterion: Owner, lifecycle status and verified-by date present. Do not substitute a related policy, plan or claimed execution for the required work product and observations. Cloud-native mechanism criterion: Owner, lifecycle status and verified-by date present.
  Required fields: `configuration_ids`, `relationships`, `owner`, `lifecycle`, `verified_at`, `reconciliation_source`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `critical-regulated/saas-cots`.

**Producer:** `configuration-manager`; **receiver:** `it-service-owner`.

**Receiving condition:** Owner, lifecycle status and verified-by date present

**Next:** Step 12.

**Role output contracts:** `configuration-manager:3`.

- **`handoff_configuration_records`**: For configuration items with verified relationships, supply the actual versioned configuration records record, including configuration_ids, relationships, owner, lifecycle, verified_at, reconciliation_source. Independently assess the evidence against this exact criterion: Owner, lifecycle status and verified-by date present. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `configuration_ids`, `relationships`, `owner`, `lifecycle`, `verified_at`, `reconciliation_source`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `critical-regulated/existing-platform`.

**Producer:** `configuration-manager`; **receiver:** `it-service-owner`.

**Receiving condition:** Owner, lifecycle status and verified-by date present

**Next:** Step 12.

**Role output contracts:** `configuration-manager:3`.

- **`handoff_configuration_records`**: For configuration items with verified relationships, supply the actual versioned configuration records record, including configuration_ids, relationships, owner, lifecycle, verified_at, reconciliation_source. Independently assess the evidence against this exact criterion: Owner, lifecycle status and verified-by date present. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `configuration_ids`, `relationships`, `owner`, `lifecycle`, `verified_at`, `reconciliation_source`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-new-service-onboarding-12"></a>

## service definition and service level agreement

**Handoff content contract:** `handoff/new-service-onboarding:12`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_service_definition`**: For service definition and service level agreement, supply the actual versioned service definition record, including service_boundary, business_contact, service_owner, agreed_levels, cost_risk_ownership. Independently assess the evidence against this exact criterion: Named business contact and an agreed SLA exist. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `service_boundary`, `business_contact`, `service_owner`, `agreed_levels`, `cost_risk_ownership`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `cloud-native`.

**Producer:** `it-service-owner`; **receiver:** `engagement:named-authority`.

**Receiving condition:** Named business contact and an agreed SLA exist

**Next:** Terminal disposition; no downstream step.

**Role output contracts:** `it-service-owner:1`.

- **`handoff_service_definition`**: For service definition and service level agreement, supply the actual versioned service definition record, including service_boundary, business_contact, service_owner, agreed_levels, cost_risk_ownership. Independently assess the evidence against this exact criterion: Named business contact and an agreed SLA exist. Do not substitute a related policy, plan or claimed execution for the required work product and observations. Cloud-native mechanism criterion: Named business contact and an agreed SLA exist.
  Required fields: `service_boundary`, `business_contact`, `service_owner`, `agreed_levels`, `cost_risk_ownership`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `saas-cots`.

**Producer:** `it-service-owner`; **receiver:** `engagement:named-authority`.

**Receiving condition:** Named business contact and an agreed SLA exist

**Next:** Terminal disposition; no downstream step.

**Role output contracts:** `it-service-owner:1`.

- **`handoff_service_definition`**: For service definition and service level agreement, supply the actual versioned service definition record, including service_boundary, business_contact, service_owner, agreed_levels, cost_risk_ownership. Independently assess the evidence against this exact criterion: Named business contact and an agreed SLA exist. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `service_boundary`, `business_contact`, `service_owner`, `agreed_levels`, `cost_risk_ownership`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `existing-platform`.

**Producer:** `it-service-owner`; **receiver:** `engagement:named-authority`.

**Receiving condition:** Named business contact and an agreed SLA exist

**Next:** Terminal disposition; no downstream step.

**Role output contracts:** `it-service-owner:1`.

- **`handoff_service_definition`**: For service definition and service level agreement, supply the actual versioned service definition record, including service_boundary, business_contact, service_owner, agreed_levels, cost_risk_ownership. Independently assess the evidence against this exact criterion: Named business contact and an agreed SLA exist. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `service_boundary`, `business_contact`, `service_owner`, `agreed_levels`, `cost_risk_ownership`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `data-ai/cloud-native`.

**Producer:** `it-service-owner`; **receiver:** `engagement:named-authority`.

**Receiving condition:** Named business contact and an agreed SLA exist

**Next:** Terminal disposition; no downstream step.

**Role output contracts:** `it-service-owner:1`.

- **`handoff_service_definition`**: For service definition and service level agreement, supply the actual versioned service definition record, including service_boundary, business_contact, service_owner, agreed_levels, cost_risk_ownership. Independently assess the evidence against this exact criterion: Named business contact and an agreed SLA exist. Do not substitute a related policy, plan or claimed execution for the required work product and observations. Cloud-native mechanism criterion: Named business contact and an agreed SLA exist.
  Required fields: `service_boundary`, `business_contact`, `service_owner`, `agreed_levels`, `cost_risk_ownership`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `data-ai/saas-cots`.

**Producer:** `it-service-owner`; **receiver:** `engagement:named-authority`.

**Receiving condition:** Named business contact and an agreed SLA exist

**Next:** Terminal disposition; no downstream step.

**Role output contracts:** `it-service-owner:1`.

- **`handoff_service_definition`**: For service definition and service level agreement, supply the actual versioned service definition record, including service_boundary, business_contact, service_owner, agreed_levels, cost_risk_ownership. Independently assess the evidence against this exact criterion: Named business contact and an agreed SLA exist. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `service_boundary`, `business_contact`, `service_owner`, `agreed_levels`, `cost_risk_ownership`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `data-ai/existing-platform`.

**Producer:** `it-service-owner`; **receiver:** `engagement:named-authority`.

**Receiving condition:** Named business contact and an agreed SLA exist

**Next:** Terminal disposition; no downstream step.

**Role output contracts:** `it-service-owner:1`.

- **`handoff_service_definition`**: For service definition and service level agreement, supply the actual versioned service definition record, including service_boundary, business_contact, service_owner, agreed_levels, cost_risk_ownership. Independently assess the evidence against this exact criterion: Named business contact and an agreed SLA exist. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `service_boundary`, `business_contact`, `service_owner`, `agreed_levels`, `cost_risk_ownership`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `critical-regulated/cloud-native`.

**Producer:** `it-service-owner`; **receiver:** `engagement:named-authority`.

**Receiving condition:** Named business contact and an agreed SLA exist

**Next:** Terminal disposition; no downstream step.

**Role output contracts:** `it-service-owner:1`.

- **`handoff_service_definition`**: For service definition and service level agreement, supply the actual versioned service definition record, including service_boundary, business_contact, service_owner, agreed_levels, cost_risk_ownership. Independently assess the evidence against this exact criterion: Named business contact and an agreed SLA exist. Do not substitute a related policy, plan or claimed execution for the required work product and observations. Cloud-native mechanism criterion: Named business contact and an agreed SLA exist.
  Required fields: `service_boundary`, `business_contact`, `service_owner`, `agreed_levels`, `cost_risk_ownership`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `critical-regulated/saas-cots`.

**Producer:** `it-service-owner`; **receiver:** `engagement:named-authority`.

**Receiving condition:** Named business contact and an agreed SLA exist

**Next:** Terminal disposition; no downstream step.

**Role output contracts:** `it-service-owner:1`.

- **`handoff_service_definition`**: For service definition and service level agreement, supply the actual versioned service definition record, including service_boundary, business_contact, service_owner, agreed_levels, cost_risk_ownership. Independently assess the evidence against this exact criterion: Named business contact and an agreed SLA exist. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `service_boundary`, `business_contact`, `service_owner`, `agreed_levels`, `cost_risk_ownership`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `critical-regulated/existing-platform`.

**Producer:** `it-service-owner`; **receiver:** `engagement:named-authority`.

**Receiving condition:** Named business contact and an agreed SLA exist

**Next:** Terminal disposition; no downstream step.

**Role output contracts:** `it-service-owner:1`.

- **`handoff_service_definition`**: For service definition and service level agreement, supply the actual versioned service definition record, including service_boundary, business_contact, service_owner, agreed_levels, cost_risk_ownership. Independently assess the evidence against this exact criterion: Named business contact and an agreed SLA exist. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `service_boundary`, `business_contact`, `service_owner`, `agreed_levels`, `cost_risk_ownership`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.
<!-- JAI:OUTPUT-CONTRACTS:END -->
