<!-- JAI:OUTPUT-CONTRACTS:START -->
# SIAM / multi-supplier service integration: source-owned handoff contracts

[Catalogue](index.md)

<a id="output-handoff-siam-multi-supplier-1"></a>

## SIAM operating model

**Handoff content contract:** `handoff/siam-multi-supplier:1`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_siam_operating_model`**: For SIAM operating model, supply the actual versioned siam operating model record, including customer_outcomes, integration_processes, accountable_owners, supplier_boundaries, decision_rights. Independently assess the evidence against this exact criterion: No customer outcome or integration process is ownerless. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `customer_outcomes`, `integration_processes`, `accountable_owners`, `supplier_boundaries`, `decision_rights`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `steady-state`.

**Producer:** `siam-manager`; **receiver:** `service-level-manager`.

**Receiving condition:** No customer outcome or integration process is ownerless

**Next:** Step 2.

**Role output contracts:** `siam-manager:1`.

- **`handoff_siam_operating_model`**: For SIAM operating model, supply the actual versioned siam operating model record, including customer_outcomes, integration_processes, accountable_owners, supplier_boundaries, decision_rights. Independently assess the evidence against this exact criterion: No customer outcome or integration process is ownerless. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `customer_outcomes`, `integration_processes`, `accountable_owners`, `supplier_boundaries`, `decision_rights`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `cross-supplier-disruption`.

**Producer:** `siam-manager`; **receiver:** `service-level-manager`.

**Receiving condition:** No customer outcome or integration process is ownerless

**Next:** Step 2.

**Role output contracts:** `siam-manager:1`.

- **`handoff_siam_operating_model`**: For SIAM operating model, supply the actual versioned siam operating model record, including customer_outcomes, integration_processes, accountable_owners, supplier_boundaries, decision_rights. Independently assess the evidence against this exact criterion: No customer outcome or integration process is ownerless. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `customer_outcomes`, `integration_processes`, `accountable_owners`, `supplier_boundaries`, `decision_rights`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-siam-multi-supplier-2"></a>

## SLA/OLA matrix

**Handoff content contract:** `handoff/siam-multi-supplier:2`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_service_level_matrix`**: For SLA/OLA matrix, supply the actual versioned service level matrix record, including customer_slas, underpinning_olas, measures, suppliers, owners, coverage_gaps. Independently assess the evidence against this exact criterion: Every SLA has sufficient underpinning measures/owners. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `customer_slas`, `underpinning_olas`, `measures`, `suppliers`, `owners`, `coverage_gaps`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `steady-state`.

**Producer:** `service-level-manager`; **receiver:** `architecture-repository-and-modelling-lead`.

**Receiving condition:** Every SLA has sufficient underpinning measures/owners

**Next:** Step 3.

**Role output contracts:** `service-level-manager:1`, `service-level-manager:4`.

- **`handoff_service_level_matrix`**: For SLA/OLA matrix, supply the actual versioned service level matrix record, including customer_slas, underpinning_olas, measures, suppliers, owners, coverage_gaps. Independently assess the evidence against this exact criterion: Every SLA has sufficient underpinning measures/owners. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `customer_slas`, `underpinning_olas`, `measures`, `suppliers`, `owners`, `coverage_gaps`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `cross-supplier-disruption`.

**Producer:** `service-level-manager`; **receiver:** `architecture-repository-and-modelling-lead`.

**Receiving condition:** Every SLA has sufficient underpinning measures/owners

**Next:** Step 3.

**Role output contracts:** `service-level-manager:1`, `service-level-manager:4`.

- **`handoff_service_level_matrix`**: For SLA/OLA matrix, supply the actual versioned service level matrix record, including customer_slas, underpinning_olas, measures, suppliers, owners, coverage_gaps. Independently assess the evidence against this exact criterion: Every SLA has sufficient underpinning measures/owners. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `customer_slas`, `underpinning_olas`, `measures`, `suppliers`, `owners`, `coverage_gaps`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-siam-multi-supplier-3"></a>

## shared dependency register/view set

**Handoff content contract:** `handoff/siam-multi-supplier:3`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_supplier_dependency_model`**: For shared dependency register/view set, supply the actual versioned supplier dependency model record, including dependency_ids, service_supplier_endpoints, owners, source_revision, views. Independently assess the evidence against this exact criterion: Material supplier/service dependencies have stable IDs and owners. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `dependency_ids`, `service_supplier_endpoints`, `owners`, `source_revision`, `views`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `steady-state`.

**Producer:** `architecture-repository-and-modelling-lead`; **receiver:** `incident-manager`.

**Receiving condition:** Material supplier/service dependencies have stable IDs and owners

**Next:** Step 4.

**Role output contracts:** `architecture-repository-and-modelling-lead:3`.

- **`handoff_supplier_dependency_model`**: For shared dependency register/view set, supply the actual versioned supplier dependency model record, including dependency_ids, service_supplier_endpoints, owners, source_revision, views. Independently assess the evidence against this exact criterion: Material supplier/service dependencies have stable IDs and owners. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `dependency_ids`, `service_supplier_endpoints`, `owners`, `source_revision`, `views`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `cross-supplier-disruption`.

**Producer:** `architecture-repository-and-modelling-lead`; **receiver:** `incident-manager`.

**Receiving condition:** Material supplier/service dependencies have stable IDs and owners

**Next:** Step 4.

**Role output contracts:** `architecture-repository-and-modelling-lead:3`.

- **`handoff_supplier_dependency_model`**: For shared dependency register/view set, supply the actual versioned supplier dependency model record, including dependency_ids, service_supplier_endpoints, owners, source_revision, views. Independently assess the evidence against this exact criterion: Material supplier/service dependencies have stable IDs and owners. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `dependency_ids`, `service_supplier_endpoints`, `owners`, `source_revision`, `views`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-siam-multi-supplier-4"></a>

## cross-supplier incident model

**Handoff content contract:** `handoff/siam-multi-supplier:4`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_cross_supplier_incident_model`**: For cross-supplier incident model, supply the actual versioned cross supplier incident model record, including severity_rules, incident_command, restoration_owner, escalation, communication. Independently assess the evidence against this exact criterion: Severity and service restoration ownership cannot bounce between suppliers. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `severity_rules`, `incident_command`, `restoration_owner`, `escalation`, `communication`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `steady-state`.

**Producer:** `incident-manager`; **receiver:** `problem-manager`.

**Receiving condition:** Severity and service restoration ownership cannot bounce between suppliers

**Next:** Step 5.

**Role output contracts:** `incident-manager:1`.

- **`handoff_cross_supplier_incident_model`**: For cross-supplier incident model, supply the actual versioned cross supplier incident model record, including severity_rules, incident_command, restoration_owner, escalation, communication. Independently assess the evidence against this exact criterion: Severity and service restoration ownership cannot bounce between suppliers. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `severity_rules`, `incident_command`, `restoration_owner`, `escalation`, `communication`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `cross-supplier-disruption`.

**Producer:** `incident-manager`; **receiver:** `problem-manager`.

**Receiving condition:** Severity and service restoration ownership cannot bounce between suppliers

**Next:** Step 5.

**Role output contracts:** `incident-manager:1`.

- **`handoff_cross_supplier_incident_model`**: For cross-supplier incident model, supply the actual versioned cross supplier incident model record, including severity_rules, incident_command, restoration_owner, escalation, communication. Independently assess the evidence against this exact criterion: Severity and service restoration ownership cannot bounce between suppliers. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `severity_rules`, `incident_command`, `restoration_owner`, `escalation`, `communication`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-siam-multi-supplier-5"></a>

## cross-supplier problem model

**Handoff content contract:** `handoff/siam-multi-supplier:5`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_cross_supplier_problem_model`**: For cross-supplier problem model, supply the actual versioned cross supplier problem model record, including problem_scope, causal_evidence, end_to_end_owner, supplier_actions, verification. Independently assess the evidence against this exact criterion: Root causes crossing contracts still receive one end-to-end owner. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `problem_scope`, `causal_evidence`, `end_to_end_owner`, `supplier_actions`, `verification`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `steady-state`.

**Producer:** `problem-manager`; **receiver:** `enterprise-release-manager`.

**Receiving condition:** Root causes crossing contracts still receive one end-to-end owner

**Next:** Step 6.

**Role output contracts:** `problem-manager:1`.

- **`handoff_cross_supplier_problem_model`**: For cross-supplier problem model, supply the actual versioned cross supplier problem model record, including problem_scope, causal_evidence, end_to_end_owner, supplier_actions, verification. Independently assess the evidence against this exact criterion: Root causes crossing contracts still receive one end-to-end owner. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `problem_scope`, `causal_evidence`, `end_to_end_owner`, `supplier_actions`, `verification`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `cross-supplier-disruption`.

**Producer:** `problem-manager`; **receiver:** `enterprise-release-manager`.

**Receiving condition:** Root causes crossing contracts still receive one end-to-end owner

**Next:** Step 6.

**Role output contracts:** `problem-manager:1`.

- **`handoff_cross_supplier_problem_model`**: For cross-supplier problem model, supply the actual versioned cross supplier problem model record, including problem_scope, causal_evidence, end_to_end_owner, supplier_actions, verification. Independently assess the evidence against this exact criterion: Root causes crossing contracts still receive one end-to-end owner. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `problem_scope`, `causal_evidence`, `end_to_end_owner`, `supplier_actions`, `verification`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-siam-multi-supplier-6"></a>

## integrated change/release calendar

**Handoff content contract:** `handoff/siam-multi-supplier:6`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_integrated_change_calendar`**: For integrated change/release calendar, supply the actual versioned integrated change calendar record, including release_ids, dependencies, windows, blackout_constraints, collision_resolution, authority. Independently assess the evidence against this exact criterion: Cross-supplier change collisions and blackout constraints are governed. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `release_ids`, `dependencies`, `windows`, `blackout_constraints`, `collision_resolution`, `authority`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `steady-state`.

**Producer:** `enterprise-release-manager`; **receiver:** `siam-manager`.

**Receiving condition:** Cross-supplier change collisions and blackout constraints are governed

**Next:** Step 7.

**Role output contracts:** `enterprise-release-manager:1`.

- **`handoff_integrated_change_calendar`**: For integrated change/release calendar, supply the actual versioned integrated change calendar record, including release_ids, dependencies, windows, blackout_constraints, collision_resolution, authority. Independently assess the evidence against this exact criterion: Cross-supplier change collisions and blackout constraints are governed. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `release_ids`, `dependencies`, `windows`, `blackout_constraints`, `collision_resolution`, `authority`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `cross-supplier-disruption`.

**Producer:** `enterprise-release-manager`; **receiver:** `siam-manager`.

**Receiving condition:** Cross-supplier change collisions and blackout constraints are governed

**Next:** Step 7.

**Role output contracts:** `enterprise-release-manager:1`.

- **`handoff_integrated_change_calendar`**: For integrated change/release calendar, supply the actual versioned integrated change calendar record, including release_ids, dependencies, windows, blackout_constraints, collision_resolution, authority. Independently assess the evidence against this exact criterion: Cross-supplier change collisions and blackout constraints are governed. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `release_ids`, `dependencies`, `windows`, `blackout_constraints`, `collision_resolution`, `authority`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-siam-multi-supplier-7"></a>

## supplier escalation matrix

**Handoff content contract:** `handoff/siam-multi-supplier:7`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_supplier_escalation`**: For supplier escalation matrix, supply the actual versioned supplier escalation record, including issue_types, accountable_contact, escalation_levels, response_targets, ownership_dispute_route. Independently assess the evidence against this exact criterion: Escalation cannot be blocked by contractual ownership ambiguity. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `issue_types`, `accountable_contact`, `escalation_levels`, `response_targets`, `ownership_dispute_route`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `steady-state`.

**Producer:** `siam-manager`; **receiver:** `it-service-owner`.

**Receiving condition:** Escalation cannot be blocked by contractual ownership ambiguity

**Next:** Step 8.

**Role output contracts:** `siam-manager:3`.

- **`handoff_supplier_escalation`**: For supplier escalation matrix, supply the actual versioned supplier escalation record, including issue_types, accountable_contact, escalation_levels, response_targets, ownership_dispute_route. Independently assess the evidence against this exact criterion: Escalation cannot be blocked by contractual ownership ambiguity. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `issue_types`, `accountable_contact`, `escalation_levels`, `response_targets`, `ownership_dispute_route`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `cross-supplier-disruption`.

**Producer:** `siam-manager`; **receiver:** `it-service-owner`.

**Receiving condition:** Escalation cannot be blocked by contractual ownership ambiguity

**Next:** Step 8.

**Role output contracts:** `siam-manager:3`.

- **`handoff_supplier_escalation`**: For supplier escalation matrix, supply the actual versioned supplier escalation record, including issue_types, accountable_contact, escalation_levels, response_targets, ownership_dispute_route. Independently assess the evidence against this exact criterion: Escalation cannot be blocked by contractual ownership ambiguity. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `issue_types`, `accountable_contact`, `escalation_levels`, `response_targets`, `ownership_dispute_route`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-siam-multi-supplier-8"></a>

## shared service acceptance

**Handoff content contract:** `handoff/siam-multi-supplier:8`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_integrated_service_acceptance`**: For shared service acceptance, supply the actual versioned integrated service acceptance record, including end_to_end_service, evidence, supplier_dependencies, residual_gaps, service_owner, actual_acceptance. Independently assess the evidence against this exact criterion: Service acceptance is end-to-end, not a collection of supplier self-attestations. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `end_to_end_service`, `evidence`, `supplier_dependencies`, `residual_gaps`, `service_owner`, `actual_acceptance`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `steady-state`.

**Producer:** `it-service-owner`; **receiver:** `engagement:named-authority`.

**Receiving condition:** Service acceptance is end-to-end, not a collection of supplier self-attestations

**Next:** Terminal disposition; no downstream step.

**Role output contracts:** `it-service-owner:1`.

- **`handoff_integrated_service_acceptance`**: For shared service acceptance, supply the actual versioned integrated service acceptance record, including end_to_end_service, evidence, supplier_dependencies, residual_gaps, service_owner, actual_acceptance. Independently assess the evidence against this exact criterion: Service acceptance is end-to-end, not a collection of supplier self-attestations. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `end_to_end_service`, `evidence`, `supplier_dependencies`, `residual_gaps`, `service_owner`, `actual_acceptance`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `cross-supplier-disruption`.

**Producer:** `it-service-owner`; **receiver:** `engagement:named-authority`.

**Receiving condition:** Service acceptance is end-to-end, not a collection of supplier self-attestations

**Next:** Terminal disposition; no downstream step.

**Role output contracts:** `it-service-owner:1`.

- **`handoff_integrated_service_acceptance`**: For shared service acceptance, supply the actual versioned integrated service acceptance record, including end_to_end_service, evidence, supplier_dependencies, residual_gaps, service_owner, actual_acceptance. Independently assess the evidence against this exact criterion: Service acceptance is end-to-end, not a collection of supplier self-attestations. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `end_to_end_service`, `evidence`, `supplier_dependencies`, `residual_gaps`, `service_owner`, `actual_acceptance`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.
<!-- JAI:OUTPUT-CONTRACTS:END -->
