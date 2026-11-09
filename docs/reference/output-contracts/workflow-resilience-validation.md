<!-- JAI:OUTPUT-CONTRACTS:START -->
# Resilience validation: source-owned handoff contracts

[Catalogue](index.md)

<a id="output-handoff-resilience-validation-1"></a>

## business criticality baseline

**Handoff content contract:** `handoff/resilience-validation:1`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_business_criticality`**: For business criticality baseline, supply the actual versioned business criticality record, including business_services, impact_tolerances, criticality, business_owners, source_basis. Independently assess the evidence against this exact criterion: Criticality and tolerances have business ownership. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `business_services`, `impact_tolerances`, `criticality`, `business_owners`, `source_basis`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `isolated-exercise`.

**Producer:** `business-continuity-manager`; **receiver:** `operational-and-technology-resilience-architect`.

**Receiving condition:** Criticality and tolerances have business ownership

**Next:** Step 2.

**Role output contracts:** `business-continuity-manager:1`, `business-continuity-manager:4`.

- **`handoff_business_criticality`**: For business criticality baseline, supply the actual versioned business criticality record, including business_services, impact_tolerances, criticality, business_owners, source_basis. Independently assess the evidence against this exact criterion: Criticality and tolerances have business ownership. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `business_services`, `impact_tolerances`, `criticality`, `business_owners`, `source_basis`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `production-exercise`.

**Producer:** `business-continuity-manager`; **receiver:** `operational-and-technology-resilience-architect`.

**Receiving condition:** Criticality and tolerances have business ownership

**Next:** Step 2.

**Role output contracts:** `business-continuity-manager:1`, `business-continuity-manager:4`.

- **`handoff_business_criticality`**: For business criticality baseline, supply the actual versioned business criticality record, including business_services, impact_tolerances, criticality, business_owners, source_basis. Independently assess the evidence against this exact criterion: Criticality and tolerances have business ownership. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `business_services`, `impact_tolerances`, `criticality`, `business_owners`, `source_basis`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-resilience-validation-2"></a>

## dependency/failure-domain model

**Handoff content contract:** `handoff/resilience-validation:2`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_failure_domain_model`**: For dependency/failure-domain model, supply the actual versioned failure domain model record, including critical_paths, dependency_ids, failure_domains, owners, unknown_dependencies. Independently assess the evidence against this exact criterion: No critical path has an unknown/unowned dependency. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `critical_paths`, `dependency_ids`, `failure_domains`, `owners`, `unknown_dependencies`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `isolated-exercise`.

**Producer:** `operational-and-technology-resilience-architect`; **receiver:** `disaster-recovery-coordinator`.

**Receiving condition:** No critical path has an unknown/unowned dependency

**Next:** Step 3.

**Role output contracts:** `operational-and-technology-resilience-architect:2`.

- **`handoff_failure_domain_model`**: For dependency/failure-domain model, supply the actual versioned failure domain model record, including critical_paths, dependency_ids, failure_domains, owners, unknown_dependencies. Independently assess the evidence against this exact criterion: No critical path has an unknown/unowned dependency. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `critical_paths`, `dependency_ids`, `failure_domains`, `owners`, `unknown_dependencies`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `production-exercise`.

**Producer:** `operational-and-technology-resilience-architect`; **receiver:** `disaster-recovery-coordinator`.

**Receiving condition:** No critical path has an unknown/unowned dependency

**Next:** Step 3.

**Role output contracts:** `operational-and-technology-resilience-architect:2`.

- **`handoff_failure_domain_model`**: For dependency/failure-domain model, supply the actual versioned failure domain model record, including critical_paths, dependency_ids, failure_domains, owners, unknown_dependencies. Independently assess the evidence against this exact criterion: No critical path has an unknown/unowned dependency. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `critical_paths`, `dependency_ids`, `failure_domains`, `owners`, `unknown_dependencies`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-resilience-validation-3"></a>

## validated recovery objectives

**Handoff content contract:** `handoff/resilience-validation:3`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_recovery_objectives`**: For validated recovery objectives, supply the actual versioned recovery objectives record, including business_targets, end_to_end_dependencies, feasibility_evidence, gaps, accountable_owners. Independently assess the evidence against this exact criterion: Objectives are feasible end to end, not only per component. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `business_targets`, `end_to_end_dependencies`, `feasibility_evidence`, `gaps`, `accountable_owners`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `isolated-exercise`.

**Producer:** `disaster-recovery-coordinator`; **receiver:** `operational-and-technology-resilience-architect`.

**Receiving condition:** Objectives are feasible end to end, not only per component

**Next:** Step 4.

**Role output contracts:** `disaster-recovery-coordinator:2`, `disaster-recovery-coordinator:3`.

- **`handoff_recovery_objectives`**: For validated recovery objectives, supply the actual versioned recovery objectives record, including business_targets, end_to_end_dependencies, feasibility_evidence, gaps, accountable_owners. Independently assess the evidence against this exact criterion: Objectives are feasible end to end, not only per component. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `business_targets`, `end_to_end_dependencies`, `feasibility_evidence`, `gaps`, `accountable_owners`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `production-exercise`.

**Producer:** `disaster-recovery-coordinator`; **receiver:** `operational-and-technology-resilience-architect`.

**Receiving condition:** Objectives are feasible end to end, not only per component

**Next:** Step 4.

**Role output contracts:** `disaster-recovery-coordinator:2`, `disaster-recovery-coordinator:3`.

- **`handoff_recovery_objectives`**: For validated recovery objectives, supply the actual versioned recovery objectives record, including business_targets, end_to_end_dependencies, feasibility_evidence, gaps, accountable_owners. Independently assess the evidence against this exact criterion: Objectives are feasible end to end, not only per component. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `business_targets`, `end_to_end_dependencies`, `feasibility_evidence`, `gaps`, `accountable_owners`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-resilience-validation-4"></a>

## resilience design with failure assumptions

**Handoff content contract:** `handoff/resilience-validation:4`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_resilience_design`**: For resilience design with failure assumptions, supply the actual versioned resilience design record, including design_revision, single_shared_failure_modes, assumptions, design_responses, measurable_outcomes. Independently assess the evidence against this exact criterion: Design addresses single/shared failure modes and measurable outcomes. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `design_revision`, `single_shared_failure_modes`, `assumptions`, `design_responses`, `measurable_outcomes`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `isolated-exercise`.

**Producer:** `operational-and-technology-resilience-architect`; **receiver:** `test-manager`.

**Receiving condition:** Design addresses single/shared failure modes and measurable outcomes

**Next:** Step 5.

**Role output contracts:** `operational-and-technology-resilience-architect:1`, `operational-and-technology-resilience-architect:3`.

- **`handoff_resilience_design`**: For resilience design with failure assumptions, supply the actual versioned resilience design record, including design_revision, single_shared_failure_modes, assumptions, design_responses, measurable_outcomes. Independently assess the evidence against this exact criterion: Design addresses single/shared failure modes and measurable outcomes. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `design_revision`, `single_shared_failure_modes`, `assumptions`, `design_responses`, `measurable_outcomes`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `production-exercise`.

**Producer:** `operational-and-technology-resilience-architect`; **receiver:** `test-manager`.

**Receiving condition:** Design addresses single/shared failure modes and measurable outcomes

**Next:** Step 5.

**Role output contracts:** `operational-and-technology-resilience-architect:1`, `operational-and-technology-resilience-architect:3`.

- **`handoff_resilience_design`**: For resilience design with failure assumptions, supply the actual versioned resilience design record, including design_revision, single_shared_failure_modes, assumptions, design_responses, measurable_outcomes. Independently assess the evidence against this exact criterion: Design addresses single/shared failure modes and measurable outcomes. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `design_revision`, `single_shared_failure_modes`, `assumptions`, `design_responses`, `measurable_outcomes`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-resilience-validation-5"></a>

## approved exercise plan

**Handoff content contract:** `handoff/resilience-validation:5`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_exercise_plan`**: For approved exercise plan, supply the actual versioned exercise plan record, including testable_claims, scenarios, permitted_scope, safety_controls, stop_conditions, approval_ref. Independently assess the evidence against this exact criterion: Test design can falsify the resilience claims and protects production safety. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `testable_claims`, `scenarios`, `permitted_scope`, `safety_controls`, `stop_conditions`, `approval_ref`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `isolated-exercise`.

**Producer:** `test-manager`; **receiver:** `chaos-and-resilience-engineer`.

**Receiving condition:** Test design can falsify the resilience claims and protects production safety

**Next:** Step 6.

**Role output contracts:** `test-manager:1`.

- **`handoff_exercise_plan`**: For approved exercise plan, supply the actual versioned exercise plan record, including testable_claims, scenarios, permitted_scope, safety_controls, stop_conditions, approval_ref. Independently assess the evidence against this exact criterion: Test design can falsify the resilience claims and protects production safety. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `testable_claims`, `scenarios`, `permitted_scope`, `safety_controls`, `stop_conditions`, `approval_ref`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `production-exercise`.

**Producer:** `test-manager`; **receiver:** `chaos-and-resilience-engineer`.

**Receiving condition:** Test design can falsify the resilience claims and protects production safety

**Next:** Step 6.

**Role output contracts:** `test-manager:1`.

- **`handoff_exercise_plan`**: For approved exercise plan, supply the actual versioned exercise plan record, including testable_claims, scenarios, permitted_scope, safety_controls, stop_conditions, approval_ref. Independently assess the evidence against this exact criterion: Test design can falsify the resilience claims and protects production safety. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `testable_claims`, `scenarios`, `permitted_scope`, `safety_controls`, `stop_conditions`, `approval_ref`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-resilience-validation-6"></a>

## exercise evidence

**Handoff content contract:** `handoff/resilience-validation:6`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_resilience_exercise_evidence`**: For exercise evidence, supply the actual versioned resilience exercise evidence record, including approved_plan_ref, actual_execution, observations, timestamps, deviations, evidence_refs. Independently assess the evidence against this exact criterion: Execution matches approved scope and evidence is attributable. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `approved_plan_ref`, `actual_execution`, `observations`, `timestamps`, `deviations`, `evidence_refs`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `isolated-exercise`.

**Producer:** `chaos-and-resilience-engineer`; **receiver:** `control-tester`.

**Receiving condition:** Execution matches approved scope and evidence is attributable

**Next:** Step 7.

**Role output contracts:** `chaos-and-resilience-engineer:1`, `chaos-and-resilience-engineer:2`.

- **`handoff_resilience_exercise_evidence`**: For exercise evidence, supply the actual versioned resilience exercise evidence record, including approved_plan_ref, actual_execution, observations, timestamps, deviations, evidence_refs. Independently assess the evidence against this exact criterion: Execution matches approved scope and evidence is attributable. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `approved_plan_ref`, `actual_execution`, `observations`, `timestamps`, `deviations`, `evidence_refs`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `production-exercise`.

**Producer:** `chaos-and-resilience-engineer`; **receiver:** `control-tester`.

**Receiving condition:** Execution matches approved scope and evidence is attributable

**Next:** Step 7.

**Role output contracts:** `chaos-and-resilience-engineer:1`, `chaos-and-resilience-engineer:2`.

- **`handoff_resilience_exercise_evidence`**: For exercise evidence, supply the actual versioned resilience exercise evidence record, including approved_plan_ref, actual_execution, observations, timestamps, deviations, evidence_refs. Independently assess the evidence against this exact criterion: Execution matches approved scope and evidence is attributable. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `approved_plan_ref`, `actual_execution`, `observations`, `timestamps`, `deviations`, `evidence_refs`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-resilience-validation-7"></a>

## findings register

**Handoff content contract:** `handoff/resilience-validation:7`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_resilience_findings`**: For findings register, supply the actual versioned resilience findings record, including criterion, observation, impact, evidence, finding_owner, severity_rationale. Independently assess the evidence against this exact criterion: Findings distinguish observation, criterion, impact and evidence. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `criterion`, `observation`, `impact`, `evidence`, `finding_owner`, `severity_rationale`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `isolated-exercise`.

**Producer:** `control-tester`; **receiver:** `operational-and-technology-resilience-architect`.

**Receiving condition:** Findings distinguish observation, criterion, impact and evidence

**Next:** Step 8.

**Role output contracts:** `control-tester:3`.

- **`handoff_resilience_findings`**: For findings register, supply the actual versioned resilience findings record, including criterion, observation, impact, evidence, finding_owner, severity_rationale. Independently assess the evidence against this exact criterion: Findings distinguish observation, criterion, impact and evidence. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `criterion`, `observation`, `impact`, `evidence`, `finding_owner`, `severity_rationale`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `production-exercise`.

**Producer:** `control-tester`; **receiver:** `operational-and-technology-resilience-architect`.

**Receiving condition:** Findings distinguish observation, criterion, impact and evidence

**Next:** Step 8.

**Role output contracts:** `control-tester:3`.

- **`handoff_resilience_findings`**: For findings register, supply the actual versioned resilience findings record, including criterion, observation, impact, evidence, finding_owner, severity_rationale. Independently assess the evidence against this exact criterion: Findings distinguish observation, criterion, impact and evidence. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `criterion`, `observation`, `impact`, `evidence`, `finding_owner`, `severity_rationale`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-resilience-validation-8"></a>

## remediation plan

**Handoff content contract:** `handoff/resilience-validation:8`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_resilience_remediation`**: For remediation plan, supply the actual versioned resilience remediation record, including finding_ids, design_response, action_owners, due_dates, acceptance_tests. Independently assess the evidence against this exact criterion: Every material finding has owner/date/design response. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `finding_ids`, `design_response`, `action_owners`, `due_dates`, `acceptance_tests`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `isolated-exercise`.

**Producer:** `operational-and-technology-resilience-architect`; **receiver:** `test-manager`.

**Receiving condition:** Every material finding has owner/date/design response

**Next:** Step 9.

**Role output contracts:** `operational-and-technology-resilience-architect:4`.

- **`handoff_resilience_remediation`**: For remediation plan, supply the actual versioned resilience remediation record, including finding_ids, design_response, action_owners, due_dates, acceptance_tests. Independently assess the evidence against this exact criterion: Every material finding has owner/date/design response. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `finding_ids`, `design_response`, `action_owners`, `due_dates`, `acceptance_tests`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `production-exercise`.

**Producer:** `operational-and-technology-resilience-architect`; **receiver:** `test-manager`.

**Receiving condition:** Every material finding has owner/date/design response

**Next:** Step 9.

**Role output contracts:** `operational-and-technology-resilience-architect:4`.

- **`handoff_resilience_remediation`**: For remediation plan, supply the actual versioned resilience remediation record, including finding_ids, design_response, action_owners, due_dates, acceptance_tests. Independently assess the evidence against this exact criterion: Every material finding has owner/date/design response. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `finding_ids`, `design_response`, `action_owners`, `due_dates`, `acceptance_tests`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-resilience-validation-9"></a>

## retest result

**Handoff content contract:** `handoff/resilience-validation:9`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_resilience_retest`**: For retest result, supply the actual versioned resilience retest record, including original_findings, changed_revision, executed_cases, observed_results, closure_evidence. Independently assess the evidence against this exact criterion: Critical findings are demonstrated fixed, not administratively closed. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `original_findings`, `changed_revision`, `executed_cases`, `observed_results`, `closure_evidence`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `isolated-exercise`.

**Producer:** `test-manager`; **receiver:** `it-service-owner`.

**Receiving condition:** Critical findings are demonstrated fixed, not administratively closed

**Next:** Step 10.

**Role output contracts:** `test-manager:2`.

- **`handoff_resilience_retest`**: For retest result, supply the actual versioned resilience retest record, including original_findings, changed_revision, executed_cases, observed_results, closure_evidence. Independently assess the evidence against this exact criterion: Critical findings are demonstrated fixed, not administratively closed. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `original_findings`, `changed_revision`, `executed_cases`, `observed_results`, `closure_evidence`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `production-exercise`.

**Producer:** `test-manager`; **receiver:** `it-service-owner`.

**Receiving condition:** Critical findings are demonstrated fixed, not administratively closed

**Next:** Step 10.

**Role output contracts:** `test-manager:2`.

- **`handoff_resilience_retest`**: For retest result, supply the actual versioned resilience retest record, including original_findings, changed_revision, executed_cases, observed_results, closure_evidence. Independently assess the evidence against this exact criterion: Critical findings are demonstrated fixed, not administratively closed. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `original_findings`, `changed_revision`, `executed_cases`, `observed_results`, `closure_evidence`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-resilience-validation-10"></a>

## resilience acceptance

**Handoff content contract:** `handoff/resilience-validation:10`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_resilience_acceptance`**: For resilience acceptance, supply the actual versioned resilience acceptance record, including reviewed_scope, evidence_ref, residual_risks, actual_acceptance, next_validation. Independently assess the evidence against this exact criterion: Acceptance states evidence, residual risk and next validation date. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `reviewed_scope`, `evidence_ref`, `residual_risks`, `actual_acceptance`, `next_validation`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `isolated-exercise`.

**Producer:** `it-service-owner`; **receiver:** `engagement:named-authority`.

**Receiving condition:** Acceptance states evidence, residual risk and next validation date

**Next:** Terminal disposition; no downstream step.

**Role output contracts:** `it-service-owner:1`.

- **`handoff_resilience_acceptance`**: For resilience acceptance, supply the actual versioned resilience acceptance record, including reviewed_scope, evidence_ref, residual_risks, actual_acceptance, next_validation. Independently assess the evidence against this exact criterion: Acceptance states evidence, residual risk and next validation date. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `reviewed_scope`, `evidence_ref`, `residual_risks`, `actual_acceptance`, `next_validation`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `production-exercise`.

**Producer:** `it-service-owner`; **receiver:** `engagement:named-authority`.

**Receiving condition:** Acceptance states evidence, residual risk and next validation date

**Next:** Terminal disposition; no downstream step.

**Role output contracts:** `it-service-owner:1`.

- **`handoff_resilience_acceptance`**: For resilience acceptance, supply the actual versioned resilience acceptance record, including reviewed_scope, evidence_ref, residual_risks, actual_acceptance, next_validation. Independently assess the evidence against this exact criterion: Acceptance states evidence, residual risk and next validation date. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `reviewed_scope`, `evidence_ref`, `residual_risks`, `actual_acceptance`, `next_validation`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.
<!-- JAI:OUTPUT-CONTRACTS:END -->
