<!-- JAI:OUTPUT-CONTRACTS:START -->
# Service retirement and decommission: source-owned handoff contracts

[Catalogue](index.md)

<a id="output-handoff-service-retirement-and-decommission-1"></a>

## retirement mandate and target date

**Handoff content contract:** `handoff/service-retirement-and-decommission:1`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_retirement_mandate`**: For retirement mandate and target date, supply the actual versioned retirement mandate record, including service_assets, scope, accountable_authority, actual_mandate, target_date. Independently assess the evidence against this exact criterion: Scope and authority are explicit. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `service_assets`, `scope`, `accountable_authority`, `actual_mandate`, `target_date`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `reversible-preparation`.

**Producer:** `it-service-owner`; **receiver:** `technology-lifecycle-and-decommission-manager`.

**Receiving condition:** Scope and authority are explicit

**Next:** Step 2.

**Role output contracts:** `it-service-owner:1`.

- **`handoff_retirement_mandate`**: For retirement mandate and target date, supply the actual versioned retirement mandate record, including service_assets, scope, accountable_authority, actual_mandate, target_date. Independently assess the evidence against this exact criterion: Scope and authority are explicit. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `service_assets`, `scope`, `accountable_authority`, `actual_mandate`, `target_date`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `authorised-retirement`.

**Producer:** `it-service-owner`; **receiver:** `technology-lifecycle-and-decommission-manager`.

**Receiving condition:** Scope and authority are explicit

**Next:** Step 2.

**Role output contracts:** `it-service-owner:1`.

- **`handoff_retirement_mandate`**: For retirement mandate and target date, supply the actual versioned retirement mandate record, including service_assets, scope, accountable_authority, actual_mandate, target_date. Independently assess the evidence against this exact criterion: Scope and authority are explicit. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `service_assets`, `scope`, `accountable_authority`, `actual_mandate`, `target_date`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-service-retirement-and-decommission-2"></a>

## dependency impact and retirement plan

**Handoff content contract:** `handoff/service-retirement-and-decommission:2`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_retirement_dependencies`**: For dependency impact and retirement plan, supply the actual versioned retirement dependencies record, including dependency_inventory, consumers, impact, planned_disposition, owners, scoped_waivers. Independently assess the evidence against this exact criterion: Every material dependency has an owned disposition or named waiver. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `dependency_inventory`, `consumers`, `impact`, `planned_disposition`, `owners`, `scoped_waivers`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `reversible-preparation`.

**Producer:** `technology-lifecycle-and-decommission-manager`; **receiver:** `data-protection-officer`.

**Receiving condition:** Every material dependency has an owned disposition or named waiver

**Next:** Step 3.

**Role output contracts:** `technology-lifecycle-and-decommission-manager:1`, `technology-lifecycle-and-decommission-manager:2`.

- **`handoff_retirement_dependencies`**: For dependency impact and retirement plan, supply the actual versioned retirement dependencies record, including dependency_inventory, consumers, impact, planned_disposition, owners, scoped_waivers. Independently assess the evidence against this exact criterion: Every material dependency has an owned disposition or named waiver. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `dependency_inventory`, `consumers`, `impact`, `planned_disposition`, `owners`, `scoped_waivers`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `authorised-retirement`.

**Producer:** `technology-lifecycle-and-decommission-manager`; **receiver:** `data-protection-officer`.

**Receiving condition:** Every material dependency has an owned disposition or named waiver

**Next:** Step 3.

**Role output contracts:** `technology-lifecycle-and-decommission-manager:1`, `technology-lifecycle-and-decommission-manager:2`.

- **`handoff_retirement_dependencies`**: For dependency impact and retirement plan, supply the actual versioned retirement dependencies record, including dependency_inventory, consumers, impact, planned_disposition, owners, scoped_waivers. Independently assess the evidence against this exact criterion: Every material dependency has an owned disposition or named waiver. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `dependency_inventory`, `consumers`, `impact`, `planned_disposition`, `owners`, `scoped_waivers`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-service-retirement-and-decommission-3"></a>

## data disposition position

**Handoff content contract:** `handoff/service-retirement-and-decommission:3`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_retirement_data_disposition`**: For data disposition position, supply the actual versioned retirement data disposition record, including data_inventory, classification, retention_obligations, archive_delete_plan, prior_authority. Independently assess the evidence against this exact criterion: Regulated/personal data disposition is authorised before irreversible action. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `data_inventory`, `classification`, `retention_obligations`, `archive_delete_plan`, `prior_authority`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `reversible-preparation`.

**Producer:** `data-protection-officer`; **receiver:** `engagement:named-authority`.

**Receiving condition:** Regulated/personal data disposition is authorised before irreversible action

**Next:** Terminal disposition; no downstream step.

**Role output contracts:** `data-protection-officer:1`, `data-protection-officer:2`.

- **`handoff_retirement_data_disposition`**: For data disposition position, supply the actual versioned retirement data disposition record, including data_inventory, classification, retention_obligations, archive_delete_plan, prior_authority. Independently assess the evidence against this exact criterion: Regulated/personal data disposition is authorised before irreversible action. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `data_inventory`, `classification`, `retention_obligations`, `archive_delete_plan`, `prior_authority`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `authorised-retirement`.

**Producer:** `data-protection-officer`; **receiver:** `change-manager`.

**Receiving condition:** Regulated/personal data disposition is authorised before irreversible action

**Next:** Step 4.

**Role output contracts:** `data-protection-officer:1`, `data-protection-officer:2`.

- **`handoff_retirement_data_disposition`**: For data disposition position, supply the actual versioned retirement data disposition record, including data_inventory, classification, retention_obligations, archive_delete_plan, prior_authority. Independently assess the evidence against this exact criterion: Regulated/personal data disposition is authorised before irreversible action. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `data_inventory`, `classification`, `retention_obligations`, `archive_delete_plan`, `prior_authority`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-service-retirement-and-decommission-4"></a>

## prior scoped human production-change authorisation

**Handoff content contract:** `handoff/service-retirement-and-decommission:4`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_retirement_change_authorisation`**: For prior scoped human production-change authorisation, supply the actual versioned retirement change authorisation record, including dependency_plan, data_disposition, rehearsal_evidence, exact_credential_service_effects, prior_human_decision. Independently assess the evidence against this exact criterion: Dependency and data-disposition plans and rehearsal evidence are available before destructive action; approval covers exact credential and service changes, not a completed retirement. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `dependency_plan`, `data_disposition`, `rehearsal_evidence`, `exact_credential_service_effects`, `prior_human_decision`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `authorised-retirement`.

**Producer:** `change-manager`; **receiver:** `identity-and-access-management-engineer`.

**Receiving condition:** Dependency and data-disposition plans and rehearsal evidence are available before destructive action; approval covers exact credential and service changes, not a completed retirement

**Next:** Step 5.

**Role output contracts:** `change-manager:1`.

- **`handoff_retirement_change_authorisation`**: For prior scoped human production-change authorisation, supply the actual versioned retirement change authorisation record, including dependency_plan, data_disposition, rehearsal_evidence, exact_credential_service_effects, prior_human_decision. Independently assess the evidence against this exact criterion: Dependency and data-disposition plans and rehearsal evidence are available before destructive action; approval covers exact credential and service changes, not a completed retirement. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `dependency_plan`, `data_disposition`, `rehearsal_evidence`, `exact_credential_service_effects`, `prior_human_decision`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-service-retirement-and-decommission-5"></a>

## access-transfer evidence and the exact owned, time-bounded shutdown-access list

**Handoff content contract:** `handoff/service-retirement-and-decommission:5`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_retirement_access_transition`**: For access-transfer evidence and the exact owned, time-bounded shutdown-access list, supply the actual versioned retirement access transition record, including authorisation_ref, transferred_removed_access, observations, retained_shutdown_access, purpose, expiry, final_revocation_owner. Independently assess the evidence against this exact criterion: Prior exact human change approval covers each removal or transfer; retain only explicitly owned bounded shutdown credentials needed for the approved shutdown, with purpose, expiry and final revocation owner. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `authorisation_ref`, `transferred_removed_access`, `observations`, `retained_shutdown_access`, `purpose`, `expiry`, `final_revocation_owner`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `authorised-retirement`.

**Producer:** `identity-and-access-management-engineer`; **receiver:** `site-reliability-engineer`.

**Receiving condition:** Prior exact human change approval covers each removal or transfer; retain only explicitly owned bounded shutdown credentials needed for the approved shutdown, with purpose, expiry and final revocation owner

**Next:** Step 6.

**Role output contracts:** `identity-and-access-management-engineer:3`.

- **`handoff_retirement_access_transition`**: For access-transfer evidence and the exact owned, time-bounded shutdown-access list, supply the actual versioned retirement access transition record, including authorisation_ref, transferred_removed_access, observations, retained_shutdown_access, purpose, expiry, final_revocation_owner. Independently assess the evidence against this exact criterion: Prior exact human change approval covers each removal or transfer; retain only explicitly owned bounded shutdown credentials needed for the approved shutdown, with purpose, expiry and final revocation owner. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `authorisation_ref`, `transferred_removed_access`, `observations`, `retained_shutdown_access`, `purpose`, `expiry`, `final_revocation_owner`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-service-retirement-and-decommission-6"></a>

## actual shutdown, final credential revocation and reconciliation evidence, and verified technical state

**Handoff content contract:** `handoff/service-retirement-and-decommission:6`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_retirement_execution`**: For actual shutdown, final credential revocation and reconciliation evidence, and verified technical state, supply the actual versioned retirement execution record, including prior_authorisation_ref, actual_shutdown, data_checks, dependency_checks, final_credential_reconciliation, verified_state. Independently assess the evidence against this exact criterion: Prior exact human change and data-disposition authorisation covers every effect; stop on changed scope or failed dependency/archive checks; the assigned IAM actor closes retained shutdown access and verifies final credential reconciliation before asset reconciliation. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `prior_authorisation_ref`, `actual_shutdown`, `data_checks`, `dependency_checks`, `final_credential_reconciliation`, `verified_state`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `authorised-retirement`.

**Producer:** `site-reliability-engineer`; **receiver:** `it-asset-manager`.

**Receiving condition:** Prior exact human change and data-disposition authorisation covers every effect; stop on changed scope or failed dependency/archive checks; the assigned IAM actor closes retained shutdown access and verifies final credential reconciliation before asset reconciliation

**Next:** Step 7.

**Role output contracts:** `site-reliability-engineer:3`.

- **`handoff_retirement_execution`**: For actual shutdown, final credential revocation and reconciliation evidence, and verified technical state, supply the actual versioned retirement execution record, including prior_authorisation_ref, actual_shutdown, data_checks, dependency_checks, final_credential_reconciliation, verified_state. Independently assess the evidence against this exact criterion: Prior exact human change and data-disposition authorisation covers every effect; stop on changed scope or failed dependency/archive checks; the assigned IAM actor closes retained shutdown access and verifies final credential reconciliation before asset reconciliation. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `prior_authorisation_ref`, `actual_shutdown`, `data_checks`, `dependency_checks`, `final_credential_reconciliation`, `verified_state`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-service-retirement-and-decommission-7"></a>

## asset/configuration closure

**Handoff content contract:** `handoff/service-retirement-and-decommission:7`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_retired_asset_reconciliation`**: For asset/configuration closure, supply the actual versioned retired asset reconciliation record, including technical_state_ref, asset_records, configuration_records, reconciliation_gaps, closure_owner. Independently assess the evidence against this exact criterion: Systems of record match the retired technical state. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `technical_state_ref`, `asset_records`, `configuration_records`, `reconciliation_gaps`, `closure_owner`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `authorised-retirement`.

**Producer:** `it-asset-manager`; **receiver:** `architecture-repository-and-modelling-lead`.

**Receiving condition:** Systems of record match the retired technical state

**Next:** Step 8.

**Role output contracts:** `it-asset-manager:1`, `it-asset-manager:3`.

- **`handoff_retired_asset_reconciliation`**: For asset/configuration closure, supply the actual versioned retired asset reconciliation record, including technical_state_ref, asset_records, configuration_records, reconciliation_gaps, closure_owner. Independently assess the evidence against this exact criterion: Systems of record match the retired technical state. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `technical_state_ref`, `asset_records`, `configuration_records`, `reconciliation_gaps`, `closure_owner`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-service-retirement-and-decommission-8"></a>

## repository retirement revision

**Handoff content contract:** `handoff/service-retirement-and-decommission:8`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_repository_retirement`**: For repository retirement revision, supply the actual versioned repository retirement record, including repository_revision, retired_element_ids, active_dependency_checks, owners, retained_evidence. Independently assess the evidence against this exact criterion: Repository has no unowned active dependency into the retired element. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `repository_revision`, `retired_element_ids`, `active_dependency_checks`, `owners`, `retained_evidence`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `authorised-retirement`.

**Producer:** `architecture-repository-and-modelling-lead`; **receiver:** `benefits-realisation-manager`.

**Receiving condition:** Repository has no unowned active dependency into the retired element

**Next:** Step 9.

**Role output contracts:** `architecture-repository-and-modelling-lead:3`, `architecture-repository-and-modelling-lead:4`.

- **`handoff_repository_retirement`**: For repository retirement revision, supply the actual versioned repository retirement record, including repository_revision, retired_element_ids, active_dependency_checks, owners, retained_evidence. Independently assess the evidence against this exact criterion: Repository has no unowned active dependency into the retired element. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `repository_revision`, `retired_element_ids`, `active_dependency_checks`, `owners`, `retained_evidence`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-service-retirement-and-decommission-9"></a>

## benefits closure result

**Handoff content contract:** `handoff/service-retirement-and-decommission:9`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_retirement_benefit_review`**: For benefits closure result, supply the actual versioned retirement benefit review record, including benefit_baseline, realised_benefits, disbenefits, variance, accountable_owner. Independently assess the evidence against this exact criterion: Benefit or disbenefit variance has an accountable owner. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `benefit_baseline`, `realised_benefits`, `disbenefits`, `variance`, `accountable_owner`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `authorised-retirement`.

**Producer:** `benefits-realisation-manager`; **receiver:** `engagement:named-authority`.

**Receiving condition:** Benefit or disbenefit variance has an accountable owner

**Next:** Terminal disposition; no downstream step.

**Role output contracts:** `benefits-realisation-manager:4`.

- **`handoff_retirement_benefit_review`**: For benefits closure result, supply the actual versioned retirement benefit review record, including benefit_baseline, realised_benefits, disbenefits, variance, accountable_owner. Independently assess the evidence against this exact criterion: Benefit or disbenefit variance has an accountable owner. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `benefit_baseline`, `realised_benefits`, `disbenefits`, `variance`, `accountable_owner`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.
<!-- JAI:OUTPUT-CONTRACTS:END -->
