<!-- JAI:OUTPUT-CONTRACTS:START -->
# Incident to permanent fix: source-owned handoff contracts

[Catalogue](index.md)

<a id="output-handoff-incident-to-problem-1"></a>

## incident record with impact and urgency

**Handoff content contract:** `handoff/incident-to-problem:1`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_incident_report`**: For incident record with impact and urgency, supply the actual versioned incident report record, including incident_id, observed_symptoms, business_impact, affected_service, urgency, observed_at. Independently assess the evidence against this exact criterion: Symptom-only records are returned for clarification. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `incident_id`, `observed_symptoms`, `business_impact`, `affected_service`, `urgency`, `observed_at`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `ordinary`.

**Producer:** `service-desk-analyst`; **receiver:** `incident-manager`.

**Receiving condition:** Symptom-only records are returned for clarification

**Next:** Step 2.

**Role output contracts:** `service-desk-analyst:1`.

- **`handoff_incident_report`**: For incident record with impact and urgency, supply the actual versioned incident report record, including incident_id, observed_symptoms, business_impact, affected_service, urgency, observed_at. Independently assess the evidence against this exact criterion: Symptom-only records are returned for clarification. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `incident_id`, `observed_symptoms`, `business_impact`, `affected_service`, `urgency`, `observed_at`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `major`.

**Producer:** `service-desk-analyst`; **receiver:** `incident-manager`.

**Receiving condition:** Symptom-only records are returned for clarification

**Next:** Step 2.

**Role output contracts:** `service-desk-analyst:1`.

- **`handoff_incident_report`**: For incident record with impact and urgency, supply the actual versioned incident report record, including incident_id, observed_symptoms, business_impact, affected_service, urgency, observed_at. Independently assess the evidence against this exact criterion: Symptom-only records are returned for clarification. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `incident_id`, `observed_symptoms`, `business_impact`, `affected_service`, `urgency`, `observed_at`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `suspected-security`.

**Producer:** `service-desk-analyst`; **receiver:** `incident-manager`.

**Receiving condition:** Symptom-only records are returned for clarification

**Next:** Step 2.

**Role output contracts:** `service-desk-analyst:1`.

- **`handoff_incident_report`**: For incident record with impact and urgency, supply the actual versioned incident report record, including incident_id, observed_symptoms, business_impact, affected_service, urgency, observed_at. Independently assess the evidence against this exact criterion: Symptom-only records are returned for clarification. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `incident_id`, `observed_symptoms`, `business_impact`, `affected_service`, `urgency`, `observed_at`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-incident-to-problem-2"></a>

## priority, working hypothesis, comms cadence

**Handoff content contract:** `handoff/incident-to-problem:2`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_incident_coordination`**: For priority, working hypothesis, comms cadence, supply the actual versioned incident coordination record, including priority, impact_basis, working_hypothesis, incident_owner, communications_cadence. Independently assess the evidence against this exact criterion: Priority from business impact, not technical severity. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `priority`, `impact_basis`, `working_hypothesis`, `incident_owner`, `communications_cadence`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `ordinary`.

**Producer:** `incident-manager`; **receiver:** `site-reliability-engineer`.

**Receiving condition:** Priority from business impact, not technical severity

**Next:** Step 3.

**Role output contracts:** `incident-manager:1`, `incident-manager:2`, `incident-manager:4`.

- **`handoff_incident_coordination`**: For priority, working hypothesis, comms cadence, supply the actual versioned incident coordination record, including priority, impact_basis, working_hypothesis, incident_owner, communications_cadence. Independently assess the evidence against this exact criterion: Priority from business impact, not technical severity. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `priority`, `impact_basis`, `working_hypothesis`, `incident_owner`, `communications_cadence`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `major`.

**Producer:** `incident-manager`; **receiver:** `site-reliability-engineer`.

**Receiving condition:** Priority from business impact, not technical severity

**Next:** Step 3.

**Role output contracts:** `incident-manager:1`, `incident-manager:2`, `incident-manager:4`.

- **`handoff_incident_coordination`**: For priority, working hypothesis, comms cadence, supply the actual versioned incident coordination record, including priority, impact_basis, working_hypothesis, incident_owner, communications_cadence. Independently assess the evidence against this exact criterion: Priority from business impact, not technical severity. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `priority`, `impact_basis`, `working_hypothesis`, `incident_owner`, `communications_cadence`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `suspected-security`.

**Producer:** `incident-manager`; **receiver:** `site-reliability-engineer`.

**Receiving condition:** Priority from business impact, not technical severity

**Next:** Step 3.

**Role output contracts:** `incident-manager:1`, `incident-manager:2`, `incident-manager:4`.

- **`handoff_incident_coordination`**: For priority, working hypothesis, comms cadence, supply the actual versioned incident coordination record, including priority, impact_basis, working_hypothesis, incident_owner, communications_cadence. Independently assess the evidence against this exact criterion: Priority from business impact, not technical severity. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `priority`, `impact_basis`, `working_hypothesis`, `incident_owner`, `communications_cadence`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-incident-to-problem-3"></a>

## service restored; evidence preserved

**Handoff content contract:** `handoff/incident-to-problem:3`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_restoration_evidence`**: For service restored; evidence preserved, supply the actual versioned restoration evidence record, including restored_service, restoration_actions, authorisation_ref, preserved_evidence, observed_health, residual_impact. Independently assess the evidence against this exact criterion: Prior applicable standard or emergency change authorisation covers restoration effects; preserve evidence before destructive recovery; stop for named human approval if scope is not already authorised. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `restored_service`, `restoration_actions`, `authorisation_ref`, `preserved_evidence`, `observed_health`, `residual_impact`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `ordinary`.

**Producer:** `site-reliability-engineer`; **receiver:** `major-incident-manager`.

**Receiving condition:** Prior applicable standard or emergency change authorisation covers restoration effects; preserve evidence before destructive recovery; stop for named human approval if scope is not already authorised

**Next:** Step 4.

**Role output contracts:** `site-reliability-engineer:3`.

- **`handoff_restoration_evidence`**: For service restored; evidence preserved, supply the actual versioned restoration evidence record, including restored_service, restoration_actions, authorisation_ref, preserved_evidence, observed_health, residual_impact. Independently assess the evidence against this exact criterion: Prior applicable standard or emergency change authorisation covers restoration effects; preserve evidence before destructive recovery; stop for named human approval if scope is not already authorised. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `restored_service`, `restoration_actions`, `authorisation_ref`, `preserved_evidence`, `observed_health`, `residual_impact`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `major`.

**Producer:** `site-reliability-engineer`; **receiver:** `major-incident-manager`.

**Receiving condition:** Prior applicable standard or emergency change authorisation covers restoration effects; preserve evidence before destructive recovery; stop for named human approval if scope is not already authorised

**Next:** Step 4.

**Role output contracts:** `site-reliability-engineer:3`.

- **`handoff_restoration_evidence`**: For service restored; evidence preserved, supply the actual versioned restoration evidence record, including restored_service, restoration_actions, authorisation_ref, preserved_evidence, observed_health, residual_impact. Independently assess the evidence against this exact criterion: Prior applicable standard or emergency change authorisation covers restoration effects; preserve evidence before destructive recovery; stop for named human approval if scope is not already authorised. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `restored_service`, `restoration_actions`, `authorisation_ref`, `preserved_evidence`, `observed_health`, `residual_impact`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `suspected-security`.

**Producer:** `site-reliability-engineer`; **receiver:** `major-incident-manager`.

**Receiving condition:** Prior applicable standard or emergency change authorisation covers restoration effects; preserve evidence before destructive recovery; stop for named human approval if scope is not already authorised

**Next:** Step 4.

**Role output contracts:** `site-reliability-engineer:3`.

- **`handoff_restoration_evidence`**: For service restored; evidence preserved, supply the actual versioned restoration evidence record, including restored_service, restoration_actions, authorisation_ref, preserved_evidence, observed_health, residual_impact. Independently assess the evidence against this exact criterion: Prior applicable standard or emergency change authorisation covers restoration effects; preserve evidence before destructive recovery; stop for named human approval if scope is not already authorised. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `restored_service`, `restoration_actions`, `authorisation_ref`, `preserved_evidence`, `observed_health`, `residual_impact`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-incident-to-problem-4"></a>

## command log, stakeholder comms, notification assessment

**Handoff content contract:** `handoff/incident-to-problem:4`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_incident_command_log`**: For command log, stakeholder comms, notification assessment, supply the actual versioned incident command log record, including timeline, decisions, stakeholder_updates, notification_clocks, accountable_command. Independently assess the evidence against this exact criterion: Comms on a fixed clock; regulatory clocks assessed. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `timeline`, `decisions`, `stakeholder_updates`, `notification_clocks`, `accountable_command`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `ordinary`.

**Producer:** `major-incident-manager`; **receiver:** `problem-manager`.

**Receiving condition:** Comms on a fixed clock; regulatory clocks assessed

**Next:** Step 5.

**Role output contracts:** `major-incident-manager:1`, `major-incident-manager:2`, `major-incident-manager:3`.

- **`handoff_incident_command_log`**: For command log, stakeholder comms, notification assessment, supply the actual versioned incident command log record, including timeline, decisions, stakeholder_updates, notification_clocks, accountable_command. Independently assess the evidence against this exact criterion: Comms on a fixed clock; regulatory clocks assessed. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `timeline`, `decisions`, `stakeholder_updates`, `notification_clocks`, `accountable_command`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `major`.

**Producer:** `major-incident-manager`; **receiver:** `problem-manager`.

**Receiving condition:** Comms on a fixed clock; regulatory clocks assessed

**Next:** Step 5.

**Role output contracts:** `major-incident-manager:1`, `major-incident-manager:2`, `major-incident-manager:3`.

- **`handoff_incident_command_log`**: For command log, stakeholder comms, notification assessment, supply the actual versioned incident command log record, including timeline, decisions, stakeholder_updates, notification_clocks, accountable_command. Independently assess the evidence against this exact criterion: Comms on a fixed clock; regulatory clocks assessed. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `timeline`, `decisions`, `stakeholder_updates`, `notification_clocks`, `accountable_command`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `suspected-security`.

**Producer:** `major-incident-manager`; **receiver:** `problem-manager`.

**Receiving condition:** Comms on a fixed clock; regulatory clocks assessed

**Next:** Step 5.

**Role output contracts:** `major-incident-manager:1`, `major-incident-manager:2`, `major-incident-manager:3`.

- **`handoff_incident_command_log`**: For command log, stakeholder comms, notification assessment, supply the actual versioned incident command log record, including timeline, decisions, stakeholder_updates, notification_clocks, accountable_command. Independently assess the evidence against this exact criterion: Comms on a fixed clock; regulatory clocks assessed. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `timeline`, `decisions`, `stakeholder_updates`, `notification_clocks`, `accountable_command`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-incident-to-problem-5"></a>

## problem record with root cause and known error

**Handoff content contract:** `handoff/incident-to-problem:5`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_root_cause_record`**: For problem record with root cause and known error, supply the actual versioned root cause record record, including problem_id, causal_chain, competing_hypotheses, evidence, known_error. Independently assess the evidence against this exact criterion: "Human error" alone rejected as a root cause. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `problem_id`, `causal_chain`, `competing_hypotheses`, `evidence`, `known_error`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `ordinary`.

**Producer:** `problem-manager`; **receiver:** `technical-lead`.

**Receiving condition:** "Human error" alone rejected as a root cause

**Next:** Step 6.

**Role output contracts:** `problem-manager:1`, `problem-manager:2`.

- **`handoff_root_cause_record`**: For problem record with root cause and known error, supply the actual versioned root cause record record, including problem_id, causal_chain, competing_hypotheses, evidence, known_error. Independently assess the evidence against this exact criterion: "Human error" alone rejected as a root cause. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `problem_id`, `causal_chain`, `competing_hypotheses`, `evidence`, `known_error`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `major`.

**Producer:** `problem-manager`; **receiver:** `technical-lead`.

**Receiving condition:** "Human error" alone rejected as a root cause

**Next:** Step 6.

**Role output contracts:** `problem-manager:1`, `problem-manager:2`.

- **`handoff_root_cause_record`**: For problem record with root cause and known error, supply the actual versioned root cause record record, including problem_id, causal_chain, competing_hypotheses, evidence, known_error. Independently assess the evidence against this exact criterion: "Human error" alone rejected as a root cause. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `problem_id`, `causal_chain`, `competing_hypotheses`, `evidence`, `known_error`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `suspected-security`.

**Producer:** `problem-manager`; **receiver:** `technical-lead`.

**Receiving condition:** "Human error" alone rejected as a root cause

**Next:** Step 6.

**Role output contracts:** `problem-manager:1`, `problem-manager:2`.

- **`handoff_root_cause_record`**: For problem record with root cause and known error, supply the actual versioned root cause record record, including problem_id, causal_chain, competing_hypotheses, evidence, known_error. Independently assess the evidence against this exact criterion: "Human error" alone rejected as a root cause. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `problem_id`, `causal_chain`, `competing_hypotheses`, `evidence`, `known_error`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-incident-to-problem-6"></a>

## fix approach and effort

**Handoff content contract:** `handoff/incident-to-problem:6`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_causal_fix_design`**: For fix approach and effort, supply the actual versioned causal fix design record, including cause_ref, design_options, selected_response, effort, dependencies, verification_plan. Independently assess the evidence against this exact criterion: The fix addresses the cause, not the latest symptom. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `cause_ref`, `design_options`, `selected_response`, `effort`, `dependencies`, `verification_plan`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `ordinary`.

**Producer:** `technical-lead`; **receiver:** `software-engineer`.

**Receiving condition:** The fix addresses the cause, not the latest symptom

**Next:** Step 7.

**Role output contracts:** `technical-lead:1`, `technical-lead:4`.

- **`handoff_causal_fix_design`**: For fix approach and effort, supply the actual versioned causal fix design record, including cause_ref, design_options, selected_response, effort, dependencies, verification_plan. Independently assess the evidence against this exact criterion: The fix addresses the cause, not the latest symptom. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `cause_ref`, `design_options`, `selected_response`, `effort`, `dependencies`, `verification_plan`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `major`.

**Producer:** `technical-lead`; **receiver:** `software-engineer`.

**Receiving condition:** The fix addresses the cause, not the latest symptom

**Next:** Step 7.

**Role output contracts:** `technical-lead:1`, `technical-lead:4`.

- **`handoff_causal_fix_design`**: For fix approach and effort, supply the actual versioned causal fix design record, including cause_ref, design_options, selected_response, effort, dependencies, verification_plan. Independently assess the evidence against this exact criterion: The fix addresses the cause, not the latest symptom. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `cause_ref`, `design_options`, `selected_response`, `effort`, `dependencies`, `verification_plan`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `suspected-security`.

**Producer:** `technical-lead`; **receiver:** `software-engineer`.

**Receiving condition:** The fix addresses the cause, not the latest symptom

**Next:** Step 7.

**Role output contracts:** `technical-lead:1`, `technical-lead:4`.

- **`handoff_causal_fix_design`**: For fix approach and effort, supply the actual versioned causal fix design record, including cause_ref, design_options, selected_response, effort, dependencies, verification_plan. Independently assess the evidence against this exact criterion: The fix addresses the cause, not the latest symptom. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `cause_ref`, `design_options`, `selected_response`, `effort`, `dependencies`, `verification_plan`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-incident-to-problem-7"></a>

## versioned candidate, pre-production test evidence and rollback rehearsal

**Handoff content contract:** `handoff/incident-to-problem:7`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_candidate_fix`**: For versioned candidate, pre-production test evidence and rollback rehearsal, supply the actual versioned candidate fix record, including candidate_revision, permitted_test_scope, actual_test_results, rollback_rehearsal, unresolved_findings. Independently assess the evidence against this exact criterion: Preparation is confined to permitted code, data and test environments; no production effects before the exact human change decision. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `candidate_revision`, `permitted_test_scope`, `actual_test_results`, `rollback_rehearsal`, `unresolved_findings`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `ordinary`.

**Producer:** `software-engineer`; **receiver:** `change-manager`.

**Receiving condition:** Preparation is confined to permitted code, data and test environments; no production effects before the exact human change decision

**Next:** Step 8.

**Role output contracts:** `software-engineer:1`, `software-engineer:2`, `software-engineer:4`.

- **`handoff_candidate_fix`**: For versioned candidate, pre-production test evidence and rollback rehearsal, supply the actual versioned candidate fix record, including candidate_revision, permitted_test_scope, actual_test_results, rollback_rehearsal, unresolved_findings. Independently assess the evidence against this exact criterion: Preparation is confined to permitted code, data and test environments; no production effects before the exact human change decision. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `candidate_revision`, `permitted_test_scope`, `actual_test_results`, `rollback_rehearsal`, `unresolved_findings`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `major`.

**Producer:** `software-engineer`; **receiver:** `change-manager`.

**Receiving condition:** Preparation is confined to permitted code, data and test environments; no production effects before the exact human change decision

**Next:** Step 8.

**Role output contracts:** `software-engineer:1`, `software-engineer:2`, `software-engineer:4`.

- **`handoff_candidate_fix`**: For versioned candidate, pre-production test evidence and rollback rehearsal, supply the actual versioned candidate fix record, including candidate_revision, permitted_test_scope, actual_test_results, rollback_rehearsal, unresolved_findings. Independently assess the evidence against this exact criterion: Preparation is confined to permitted code, data and test environments; no production effects before the exact human change decision. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `candidate_revision`, `permitted_test_scope`, `actual_test_results`, `rollback_rehearsal`, `unresolved_findings`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `suspected-security`.

**Producer:** `software-engineer`; **receiver:** `change-manager`.

**Receiving condition:** Preparation is confined to permitted code, data and test environments; no production effects before the exact human change decision

**Next:** Step 8.

**Role output contracts:** `software-engineer:1`, `software-engineer:2`, `software-engineer:4`.

- **`handoff_candidate_fix`**: For versioned candidate, pre-production test evidence and rollback rehearsal, supply the actual versioned candidate fix record, including candidate_revision, permitted_test_scope, actual_test_results, rollback_rehearsal, unresolved_findings. Independently assess the evidence against this exact criterion: Preparation is confined to permitted code, data and test environments; no production effects before the exact human change decision. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `candidate_revision`, `permitted_test_scope`, `actual_test_results`, `rollback_rehearsal`, `unresolved_findings`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-incident-to-problem-8"></a>

## change authorisation

**Handoff content contract:** `handoff/incident-to-problem:8`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_fix_authorisation`**: For change authorisation, supply the actual versioned fix authorisation record, including candidate_revision, readiness_evidence, exact_effect_scope, authority, prior_decision, emergency_record. Independently assess the evidence against this exact criterion: Candidate fix design, pre-production test evidence and rollback plan precede the human decision; emergency authorisation is justified and logged before effects. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `candidate_revision`, `readiness_evidence`, `exact_effect_scope`, `authority`, `prior_decision`, `emergency_record`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `ordinary`.

**Producer:** `change-manager`; **receiver:** `software-engineer`.

**Receiving condition:** Candidate fix design, pre-production test evidence and rollback plan precede the human decision; emergency authorisation is justified and logged before effects

**Next:** Step 9.

**Role output contracts:** `change-manager:1`.

- **`handoff_fix_authorisation`**: For change authorisation, supply the actual versioned fix authorisation record, including candidate_revision, readiness_evidence, exact_effect_scope, authority, prior_decision, emergency_record. Independently assess the evidence against this exact criterion: Candidate fix design, pre-production test evidence and rollback plan precede the human decision; emergency authorisation is justified and logged before effects. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `candidate_revision`, `readiness_evidence`, `exact_effect_scope`, `authority`, `prior_decision`, `emergency_record`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `major`.

**Producer:** `change-manager`; **receiver:** `software-engineer`.

**Receiving condition:** Candidate fix design, pre-production test evidence and rollback plan precede the human decision; emergency authorisation is justified and logged before effects

**Next:** Step 9.

**Role output contracts:** `change-manager:1`.

- **`handoff_fix_authorisation`**: For change authorisation, supply the actual versioned fix authorisation record, including candidate_revision, readiness_evidence, exact_effect_scope, authority, prior_decision, emergency_record. Independently assess the evidence against this exact criterion: Candidate fix design, pre-production test evidence and rollback plan precede the human decision; emergency authorisation is justified and logged before effects. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `candidate_revision`, `readiness_evidence`, `exact_effect_scope`, `authority`, `prior_decision`, `emergency_record`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `suspected-security`.

**Producer:** `change-manager`; **receiver:** `software-engineer`.

**Receiving condition:** Candidate fix design, pre-production test evidence and rollback plan precede the human decision; emergency authorisation is justified and logged before effects

**Next:** Step 9.

**Role output contracts:** `change-manager:1`.

- **`handoff_fix_authorisation`**: For change authorisation, supply the actual versioned fix authorisation record, including candidate_revision, readiness_evidence, exact_effect_scope, authority, prior_decision, emergency_record. Independently assess the evidence against this exact criterion: Candidate fix design, pre-production test evidence and rollback plan precede the human decision; emergency authorisation is justified and logged before effects. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `candidate_revision`, `readiness_evidence`, `exact_effect_scope`, `authority`, `prior_decision`, `emergency_record`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-incident-to-problem-9"></a>

## versioned fix, execution evidence and rollback observations

**Handoff content contract:** `handoff/incident-to-problem:9`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_fix_execution`**: For versioned fix, execution evidence and rollback observations, supply the actual versioned fix execution record, including authorisation_ref, executed_revision, actual_actions, stop_go_results, rollback_observations. Independently assess the evidence against this exact criterion: Prior exact human change authorisation covers deployment; stop on scope change or failed stop/go criteria. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `authorisation_ref`, `executed_revision`, `actual_actions`, `stop_go_results`, `rollback_observations`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `ordinary`.

**Producer:** `software-engineer`; **receiver:** `test-analyst`.

**Receiving condition:** Prior exact human change authorisation covers deployment; stop on scope change or failed stop/go criteria

**Next:** Step 10.

**Role output contracts:** `software-engineer:1`, `software-engineer:4`.

- **`handoff_fix_execution`**: For versioned fix, execution evidence and rollback observations, supply the actual versioned fix execution record, including authorisation_ref, executed_revision, actual_actions, stop_go_results, rollback_observations. Independently assess the evidence against this exact criterion: Prior exact human change authorisation covers deployment; stop on scope change or failed stop/go criteria. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `authorisation_ref`, `executed_revision`, `actual_actions`, `stop_go_results`, `rollback_observations`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `major`.

**Producer:** `software-engineer`; **receiver:** `test-analyst`.

**Receiving condition:** Prior exact human change authorisation covers deployment; stop on scope change or failed stop/go criteria

**Next:** Step 10.

**Role output contracts:** `software-engineer:1`, `software-engineer:4`.

- **`handoff_fix_execution`**: For versioned fix, execution evidence and rollback observations, supply the actual versioned fix execution record, including authorisation_ref, executed_revision, actual_actions, stop_go_results, rollback_observations. Independently assess the evidence against this exact criterion: Prior exact human change authorisation covers deployment; stop on scope change or failed stop/go criteria. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `authorisation_ref`, `executed_revision`, `actual_actions`, `stop_go_results`, `rollback_observations`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `suspected-security`.

**Producer:** `software-engineer`; **receiver:** `test-analyst`.

**Receiving condition:** Prior exact human change authorisation covers deployment; stop on scope change or failed stop/go criteria

**Next:** Step 10.

**Role output contracts:** `software-engineer:1`, `software-engineer:4`.

- **`handoff_fix_execution`**: For versioned fix, execution evidence and rollback observations, supply the actual versioned fix execution record, including authorisation_ref, executed_revision, actual_actions, stop_go_results, rollback_observations. Independently assess the evidence against this exact criterion: Prior exact human change authorisation covers deployment; stop on scope change or failed stop/go criteria. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `authorisation_ref`, `executed_revision`, `actual_actions`, `stop_go_results`, `rollback_observations`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-incident-to-problem-10"></a>

## independent regression, service and residual-defect evidence

**Handoff content contract:** `handoff/incident-to-problem:10`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_independent_fix_validation`**: For independent regression, service and residual-defect evidence, supply the actual versioned independent fix validation record, including validator_independence, executed_revision, regression_results, service_results, residual_defects. Independently assess the evidence against this exact criterion: Actual execution and independent validation evidence are required before closure; failed criteria remain blocking. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `validator_independence`, `executed_revision`, `regression_results`, `service_results`, `residual_defects`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `ordinary`.

**Producer:** `test-analyst`; **receiver:** `detection-engineer`.

**Receiving condition:** Actual execution and independent validation evidence are required before closure; failed criteria remain blocking

**Next:** Step 11.

**Role output contracts:** `test-analyst:1`, `test-analyst:2`.

- **`handoff_independent_fix_validation`**: For independent regression, service and residual-defect evidence, supply the actual versioned independent fix validation record, including validator_independence, executed_revision, regression_results, service_results, residual_defects. Independently assess the evidence against this exact criterion: Actual execution and independent validation evidence are required before closure; failed criteria remain blocking. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `validator_independence`, `executed_revision`, `regression_results`, `service_results`, `residual_defects`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `major`.

**Producer:** `test-analyst`; **receiver:** `detection-engineer`.

**Receiving condition:** Actual execution and independent validation evidence are required before closure; failed criteria remain blocking

**Next:** Step 11.

**Role output contracts:** `test-analyst:1`, `test-analyst:2`.

- **`handoff_independent_fix_validation`**: For independent regression, service and residual-defect evidence, supply the actual versioned independent fix validation record, including validator_independence, executed_revision, regression_results, service_results, residual_defects. Independently assess the evidence against this exact criterion: Actual execution and independent validation evidence are required before closure; failed criteria remain blocking. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `validator_independence`, `executed_revision`, `regression_results`, `service_results`, `residual_defects`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `suspected-security`.

**Producer:** `test-analyst`; **receiver:** `detection-engineer`.

**Receiving condition:** Actual execution and independent validation evidence are required before closure; failed criteria remain blocking

**Next:** Step 11.

**Role output contracts:** `test-analyst:1`, `test-analyst:2`.

- **`handoff_independent_fix_validation`**: For independent regression, service and residual-defect evidence, supply the actual versioned independent fix validation record, including validator_independence, executed_revision, regression_results, service_results, residual_defects. Independently assess the evidence against this exact criterion: Actual execution and independent validation evidence are required before closure; failed criteria remain blocking. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `validator_independence`, `executed_revision`, `regression_results`, `service_results`, `residual_defects`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-incident-to-problem-11"></a>

## new or tuned alert with a runbook

**Handoff content contract:** `handoff/incident-to-problem:11`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_detection_improvement`**: For new or tuned alert with a runbook, supply the actual versioned detection improvement record, including alert_revision, change_authorisation, failure_replay_result, threshold, runbook. Independently assess the evidence against this exact criterion: Prior exact change authorisation covers alert changes; prove the alert would have fired earlier for this failure. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `alert_revision`, `change_authorisation`, `failure_replay_result`, `threshold`, `runbook`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `ordinary`.

**Producer:** `detection-engineer`; **receiver:** `continual-improvement-manager`.

**Receiving condition:** Prior exact change authorisation covers alert changes; prove the alert would have fired earlier for this failure

**Next:** Step 12.

**Role output contracts:** `detection-engineer:1`, `detection-engineer:2`.

- **`handoff_detection_improvement`**: For new or tuned alert with a runbook, supply the actual versioned detection improvement record, including alert_revision, change_authorisation, failure_replay_result, threshold, runbook. Independently assess the evidence against this exact criterion: Prior exact change authorisation covers alert changes; prove the alert would have fired earlier for this failure. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `alert_revision`, `change_authorisation`, `failure_replay_result`, `threshold`, `runbook`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `major`.

**Producer:** `detection-engineer`; **receiver:** `continual-improvement-manager`.

**Receiving condition:** Prior exact change authorisation covers alert changes; prove the alert would have fired earlier for this failure

**Next:** Step 12.

**Role output contracts:** `detection-engineer:1`, `detection-engineer:2`.

- **`handoff_detection_improvement`**: For new or tuned alert with a runbook, supply the actual versioned detection improvement record, including alert_revision, change_authorisation, failure_replay_result, threshold, runbook. Independently assess the evidence against this exact criterion: Prior exact change authorisation covers alert changes; prove the alert would have fired earlier for this failure. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `alert_revision`, `change_authorisation`, `failure_replay_result`, `threshold`, `runbook`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `suspected-security`.

**Producer:** `detection-engineer`; **receiver:** `continual-improvement-manager`.

**Receiving condition:** Prior exact change authorisation covers alert changes; prove the alert would have fired earlier for this failure

**Next:** Step 12.

**Role output contracts:** `detection-engineer:1`, `detection-engineer:2`.

- **`handoff_detection_improvement`**: For new or tuned alert with a runbook, supply the actual versioned detection improvement record, including alert_revision, change_authorisation, failure_replay_result, threshold, runbook. Independently assess the evidence against this exact criterion: Prior exact change authorisation covers alert changes; prove the alert would have fired earlier for this failure. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `alert_revision`, `change_authorisation`, `failure_replay_result`, `threshold`, `runbook`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-incident-to-problem-12"></a>

## measured recurrence rate

**Handoff content contract:** `handoff/incident-to-problem:12`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_recurrence_measurement`**: For measured recurrence rate, supply the actual versioned recurrence measurement record, including prechange_baseline, postchange_period, recurrence_definition, observed_rate, uncertainty, next_action. Independently assess the evidence against this exact criterion: Baseline measured before the change, not asserted after. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `prechange_baseline`, `postchange_period`, `recurrence_definition`, `observed_rate`, `uncertainty`, `next_action`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `ordinary`.

**Producer:** `continual-improvement-manager`; **receiver:** `engagement:named-authority`.

**Receiving condition:** Baseline measured before the change, not asserted after

**Next:** Terminal disposition; no downstream step.

**Role output contracts:** `continual-improvement-manager:2`.

- **`handoff_recurrence_measurement`**: For measured recurrence rate, supply the actual versioned recurrence measurement record, including prechange_baseline, postchange_period, recurrence_definition, observed_rate, uncertainty, next_action. Independently assess the evidence against this exact criterion: Baseline measured before the change, not asserted after. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `prechange_baseline`, `postchange_period`, `recurrence_definition`, `observed_rate`, `uncertainty`, `next_action`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `major`.

**Producer:** `continual-improvement-manager`; **receiver:** `engagement:named-authority`.

**Receiving condition:** Baseline measured before the change, not asserted after

**Next:** Terminal disposition; no downstream step.

**Role output contracts:** `continual-improvement-manager:2`.

- **`handoff_recurrence_measurement`**: For measured recurrence rate, supply the actual versioned recurrence measurement record, including prechange_baseline, postchange_period, recurrence_definition, observed_rate, uncertainty, next_action. Independently assess the evidence against this exact criterion: Baseline measured before the change, not asserted after. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `prechange_baseline`, `postchange_period`, `recurrence_definition`, `observed_rate`, `uncertainty`, `next_action`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `suspected-security`.

**Producer:** `continual-improvement-manager`; **receiver:** `engagement:named-authority`.

**Receiving condition:** Baseline measured before the change, not asserted after

**Next:** Terminal disposition; no downstream step.

**Role output contracts:** `continual-improvement-manager:2`.

- **`handoff_recurrence_measurement`**: For measured recurrence rate, supply the actual versioned recurrence measurement record, including prechange_baseline, postchange_period, recurrence_definition, observed_rate, uncertainty, next_action. Independently assess the evidence against this exact criterion: Baseline measured before the change, not asserted after. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `prechange_baseline`, `postchange_period`, `recurrence_definition`, `observed_rate`, `uncertainty`, `next_action`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.
<!-- JAI:OUTPUT-CONTRACTS:END -->
