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
<!-- JAI:OUTPUT-CONTRACTS:END -->
