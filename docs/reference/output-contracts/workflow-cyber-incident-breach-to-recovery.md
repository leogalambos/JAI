<!-- JAI:OUTPUT-CONTRACTS:START -->
# Cyber incident / breach to recovery: source-owned handoff contracts

[Catalogue](index.md)

<a id="output-handoff-cyber-incident-breach-to-recovery-1"></a>

## incident record with source/time/scope

**Handoff content contract:** `handoff/cyber-incident-breach-to-recovery:1`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_security_incident_record`**: For incident record with source/time/scope, supply the actual versioned security incident record record, including event_id, source, observed_at, affected_scope, observations, false_positive_basis. Independently assess the evidence against this exact criterion: A real event or explicit false-positive rationale is recorded. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `event_id`, `source`, `observed_at`, `affected_scope`, `observations`, `false_positive_basis`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `suspected`.

**Producer:** `security-analyst-tier-1`; **receiver:** `incident-responder`.

**Receiving condition:** A real event or explicit false-positive rationale is recorded

**Next:** Step 2.

**Role output contracts:** `security-analyst-tier-1:1`, `security-analyst-tier-1:2`, `security-analyst-tier-1:3`.

- **`handoff_security_incident_record`**: For incident record with source/time/scope, supply the actual versioned security incident record record, including event_id, source, observed_at, affected_scope, observations, false_positive_basis. Independently assess the evidence against this exact criterion: A real event or explicit false-positive rationale is recorded. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `event_id`, `source`, `observed_at`, `affected_scope`, `observations`, `false_positive_basis`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `confirmed-breach`.

**Producer:** `security-analyst-tier-1`; **receiver:** `incident-responder`.

**Receiving condition:** A real event or explicit false-positive rationale is recorded

**Next:** Step 2.

**Role output contracts:** `security-analyst-tier-1:1`, `security-analyst-tier-1:2`, `security-analyst-tier-1:3`.

- **`handoff_security_incident_record`**: For incident record with source/time/scope, supply the actual versioned security incident record record, including event_id, source, observed_at, affected_scope, observations, false_positive_basis. Independently assess the evidence against this exact criterion: A real event or explicit false-positive rationale is recorded. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `event_id`, `source`, `observed_at`, `affected_scope`, `observations`, `false_positive_basis`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-cyber-incident-breach-to-recovery-2"></a>

## triage decision and containment objectives

**Handoff content contract:** `handoff/cyber-incident-breach-to-recovery:2`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_incident_triage`**: For triage decision and containment objectives, supply the actual versioned incident triage record, including confirmed_scope, severity, evidence, incident_lead, containment_objectives. Independently assess the evidence against this exact criterion: Severity/scope have evidence and an accountable incident lead. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `confirmed_scope`, `severity`, `evidence`, `incident_lead`, `containment_objectives`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `suspected`.

**Producer:** `incident-responder`; **receiver:** `incident-responder`.

**Receiving condition:** Severity/scope have evidence and an accountable incident lead

**Next:** Step 3.

**Role output contracts:** `incident-responder:2`.

- **`handoff_incident_triage`**: For triage decision and containment objectives, supply the actual versioned incident triage record, including confirmed_scope, severity, evidence, incident_lead, containment_objectives. Independently assess the evidence against this exact criterion: Severity/scope have evidence and an accountable incident lead. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `confirmed_scope`, `severity`, `evidence`, `incident_lead`, `containment_objectives`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `confirmed-breach`.

**Producer:** `incident-responder`; **receiver:** `incident-responder`.

**Receiving condition:** Severity/scope have evidence and an accountable incident lead

**Next:** Step 3.

**Role output contracts:** `incident-responder:2`.

- **`handoff_incident_triage`**: For triage decision and containment objectives, supply the actual versioned incident triage record, including confirmed_scope, severity, evidence, incident_lead, containment_objectives. Independently assess the evidence against this exact criterion: Severity/scope have evidence and an accountable incident lead. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `confirmed_scope`, `severity`, `evidence`, `incident_lead`, `containment_objectives`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-cyber-incident-breach-to-recovery-3"></a>

## containment actions and status

**Handoff content contract:** `handoff/cyber-incident-breach-to-recovery:3`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_containment_observations`**: For containment actions and status, supply the actual versioned containment observations record, including authorised_scope, actual_actions, observations, evidence_preservation, destructive_action_authority, residual_exposure. Independently assess the evidence against this exact criterion: Containment does not destroy material evidence without authority. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `authorised_scope`, `actual_actions`, `observations`, `evidence_preservation`, `destructive_action_authority`, `residual_exposure`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `suspected`.

**Producer:** `incident-responder`; **receiver:** `digital-forensics-examiner`.

**Receiving condition:** Containment does not destroy material evidence without authority

**Next:** Step 4.

**Role output contracts:** `incident-responder:1`, `incident-responder:2`.

- **`handoff_containment_observations`**: For containment actions and status, supply the actual versioned containment observations record, including authorised_scope, actual_actions, observations, evidence_preservation, destructive_action_authority, residual_exposure. Independently assess the evidence against this exact criterion: Containment does not destroy material evidence without authority. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `authorised_scope`, `actual_actions`, `observations`, `evidence_preservation`, `destructive_action_authority`, `residual_exposure`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `confirmed-breach`.

**Producer:** `incident-responder`; **receiver:** `digital-forensics-examiner`.

**Receiving condition:** Containment does not destroy material evidence without authority

**Next:** Step 4.

**Role output contracts:** `incident-responder:1`, `incident-responder:2`.

- **`handoff_containment_observations`**: For containment actions and status, supply the actual versioned containment observations record, including authorised_scope, actual_actions, observations, evidence_preservation, destructive_action_authority, residual_exposure. Independently assess the evidence against this exact criterion: Containment does not destroy material evidence without authority. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `authorised_scope`, `actual_actions`, `observations`, `evidence_preservation`, `destructive_action_authority`, `residual_exposure`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-cyber-incident-breach-to-recovery-4"></a>

## evidence register and forensic timeline

**Handoff content contract:** `handoff/cyber-incident-breach-to-recovery:4`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_forensic_record`**: For evidence register and forensic timeline, supply the actual versioned forensic record record, including evidence_ids, collection_method, integrity, time_source, custody, timeline. Independently assess the evidence against this exact criterion: Evidence integrity, time source and custody are documented. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `evidence_ids`, `collection_method`, `integrity`, `time_source`, `custody`, `timeline`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `suspected`.

**Producer:** `digital-forensics-examiner`; **receiver:** `it-risk-manager`.

**Receiving condition:** Evidence integrity, time source and custody are documented

**Next:** Step 5.

**Role output contracts:** `digital-forensics-examiner:1`, `digital-forensics-examiner:2`, `digital-forensics-examiner:3`.

- **`handoff_forensic_record`**: For evidence register and forensic timeline, supply the actual versioned forensic record record, including evidence_ids, collection_method, integrity, time_source, custody, timeline. Independently assess the evidence against this exact criterion: Evidence integrity, time source and custody are documented. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `evidence_ids`, `collection_method`, `integrity`, `time_source`, `custody`, `timeline`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `confirmed-breach`.

**Producer:** `digital-forensics-examiner`; **receiver:** `it-risk-manager`.

**Receiving condition:** Evidence integrity, time source and custody are documented

**Next:** Step 5.

**Role output contracts:** `digital-forensics-examiner:1`, `digital-forensics-examiner:2`, `digital-forensics-examiner:3`.

- **`handoff_forensic_record`**: For evidence register and forensic timeline, supply the actual versioned forensic record record, including evidence_ids, collection_method, integrity, time_source, custody, timeline. Independently assess the evidence against this exact criterion: Evidence integrity, time source and custody are documented. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `evidence_ids`, `collection_method`, `integrity`, `time_source`, `custody`, `timeline`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-cyber-incident-breach-to-recovery-5"></a>

## impact assessment with uncertainty and affected obligations

**Handoff content contract:** `handoff/cyber-incident-breach-to-recovery:5`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_incident_impact`**: For impact assessment with uncertainty and affected obligations, supply the actual versioned incident impact record, including affected_services_data, business_impacts, applicable_obligations, confirmed_facts, inferences, uncertainty. Independently assess the evidence against this exact criterion: Critical impact claims distinguish confirmed fact from inference. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `affected_services_data`, `business_impacts`, `applicable_obligations`, `confirmed_facts`, `inferences`, `uncertainty`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `suspected`.

**Producer:** `it-risk-manager`; **receiver:** `data-protection-officer`.

**Receiving condition:** Critical impact claims distinguish confirmed fact from inference

**Next:** Step 6.

**Role output contracts:** `it-risk-manager:2`.

- **`handoff_incident_impact`**: For impact assessment with uncertainty and affected obligations, supply the actual versioned incident impact record, including affected_services_data, business_impacts, applicable_obligations, confirmed_facts, inferences, uncertainty. Independently assess the evidence against this exact criterion: Critical impact claims distinguish confirmed fact from inference. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `affected_services_data`, `business_impacts`, `applicable_obligations`, `confirmed_facts`, `inferences`, `uncertainty`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `confirmed-breach`.

**Producer:** `it-risk-manager`; **receiver:** `data-protection-officer`.

**Receiving condition:** Critical impact claims distinguish confirmed fact from inference

**Next:** Step 6.

**Role output contracts:** `it-risk-manager:2`.

- **`handoff_incident_impact`**: For impact assessment with uncertainty and affected obligations, supply the actual versioned incident impact record, including affected_services_data, business_impacts, applicable_obligations, confirmed_facts, inferences, uncertainty. Independently assess the evidence against this exact criterion: Critical impact claims distinguish confirmed fact from inference. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `affected_services_data`, `business_impacts`, `applicable_obligations`, `confirmed_facts`, `inferences`, `uncertainty`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-cyber-incident-breach-to-recovery-6"></a>

## breach/notification decision basis

**Handoff content contract:** `handoff/cyber-incident-breach-to-recovery:6`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_notification_decision_basis`**: For breach/notification decision basis, supply the actual versioned notification decision basis record, including jurisdiction_obligations, trigger_assessment, clock, decision_authority, evidence, actual_decision. Independently assess the evidence against this exact criterion: Notification/non-notification has correct authority, clock and evidence. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `jurisdiction_obligations`, `trigger_assessment`, `clock`, `decision_authority`, `evidence`, `actual_decision`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `suspected`.

**Producer:** `data-protection-officer`; **receiver:** `incident-responder`.

**Receiving condition:** Notification/non-notification has correct authority, clock and evidence

**Next:** Step 7.

**Role output contracts:** `data-protection-officer:4`.

- **`handoff_notification_decision_basis`**: For breach/notification decision basis, supply the actual versioned notification decision basis record, including jurisdiction_obligations, trigger_assessment, clock, decision_authority, evidence, actual_decision. Independently assess the evidence against this exact criterion: Notification/non-notification has correct authority, clock and evidence. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `jurisdiction_obligations`, `trigger_assessment`, `clock`, `decision_authority`, `evidence`, `actual_decision`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `confirmed-breach`.

**Producer:** `data-protection-officer`; **receiver:** `incident-responder`.

**Receiving condition:** Notification/non-notification has correct authority, clock and evidence

**Next:** Step 7.

**Role output contracts:** `data-protection-officer:4`.

- **`handoff_notification_decision_basis`**: For breach/notification decision basis, supply the actual versioned notification decision basis record, including jurisdiction_obligations, trigger_assessment, clock, decision_authority, evidence, actual_decision. Independently assess the evidence against this exact criterion: Notification/non-notification has correct authority, clock and evidence. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `jurisdiction_obligations`, `trigger_assessment`, `clock`, `decision_authority`, `evidence`, `actual_decision`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-cyber-incident-breach-to-recovery-7"></a>

## eradication evidence and residual technical risks

**Handoff content contract:** `handoff/cyber-incident-breach-to-recovery:7`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_eradication_results`**: For eradication evidence and residual technical risks, supply the actual versioned eradication results record, including persistence_checks, exploited_gaps, actual_actions, validation_results, residual_risks, owners. Independently assess the evidence against this exact criterion: Known persistence and exploited control gaps are addressed or explicitly owned. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `persistence_checks`, `exploited_gaps`, `actual_actions`, `validation_results`, `residual_risks`, `owners`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `suspected`.

**Producer:** `incident-responder`; **receiver:** `disaster-recovery-coordinator`.

**Receiving condition:** Known persistence and exploited control gaps are addressed or explicitly owned

**Next:** Step 8.

**Role output contracts:** `incident-responder:1`, `incident-responder:2`.

- **`handoff_eradication_results`**: For eradication evidence and residual technical risks, supply the actual versioned eradication results record, including persistence_checks, exploited_gaps, actual_actions, validation_results, residual_risks, owners. Independently assess the evidence against this exact criterion: Known persistence and exploited control gaps are addressed or explicitly owned. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `persistence_checks`, `exploited_gaps`, `actual_actions`, `validation_results`, `residual_risks`, `owners`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `confirmed-breach`.

**Producer:** `incident-responder`; **receiver:** `disaster-recovery-coordinator`.

**Receiving condition:** Known persistence and exploited control gaps are addressed or explicitly owned

**Next:** Step 8.

**Role output contracts:** `incident-responder:1`, `incident-responder:2`.

- **`handoff_eradication_results`**: For eradication evidence and residual technical risks, supply the actual versioned eradication results record, including persistence_checks, exploited_gaps, actual_actions, validation_results, residual_risks, owners. Independently assess the evidence against this exact criterion: Known persistence and exploited control gaps are addressed or explicitly owned. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `persistence_checks`, `exploited_gaps`, `actual_actions`, `validation_results`, `residual_risks`, `owners`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-cyber-incident-breach-to-recovery-8"></a>

## recovery evidence and service restoration status

**Handoff content contract:** `handoff/cyber-incident-breach-to-recovery:8`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_trusted_recovery`**: For recovery evidence and service restoration status, supply the actual versioned trusted recovery record, including trusted_state, data_integrity, restore_actions, recovery_targets, actual_results, service_status. Independently assess the evidence against this exact criterion: Recovery uses trusted state/data and respects RTO/RPO/business priorities. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `trusted_state`, `data_integrity`, `restore_actions`, `recovery_targets`, `actual_results`, `service_status`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `suspected`.

**Producer:** `disaster-recovery-coordinator`; **receiver:** `it-service-owner`.

**Receiving condition:** Recovery uses trusted state/data and respects RTO/RPO/business priorities

**Next:** Step 9.

**Role output contracts:** `disaster-recovery-coordinator:2`.

- **`handoff_trusted_recovery`**: For recovery evidence and service restoration status, supply the actual versioned trusted recovery record, including trusted_state, data_integrity, restore_actions, recovery_targets, actual_results, service_status. Independently assess the evidence against this exact criterion: Recovery uses trusted state/data and respects RTO/RPO/business priorities. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `trusted_state`, `data_integrity`, `restore_actions`, `recovery_targets`, `actual_results`, `service_status`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `confirmed-breach`.

**Producer:** `disaster-recovery-coordinator`; **receiver:** `it-service-owner`.

**Receiving condition:** Recovery uses trusted state/data and respects RTO/RPO/business priorities

**Next:** Step 9.

**Role output contracts:** `disaster-recovery-coordinator:2`.

- **`handoff_trusted_recovery`**: For recovery evidence and service restoration status, supply the actual versioned trusted recovery record, including trusted_state, data_integrity, restore_actions, recovery_targets, actual_results, service_status. Independently assess the evidence against this exact criterion: Recovery uses trusted state/data and respects RTO/RPO/business priorities. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `trusted_state`, `data_integrity`, `restore_actions`, `recovery_targets`, `actual_results`, `service_status`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-cyber-incident-breach-to-recovery-9"></a>

## business recovery acceptance

**Handoff content contract:** `handoff/cyber-incident-breach-to-recovery:9`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_business_recovery_acceptance`**: For business recovery acceptance, supply the actual versioned business recovery acceptance record, including service_owner, validation_signals, observed_results, residual_limits, actual_decision. Independently assess the evidence against this exact criterion: Service owner confirms agreed validation signals and residual limitations. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `service_owner`, `validation_signals`, `observed_results`, `residual_limits`, `actual_decision`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `suspected`.

**Producer:** `it-service-owner`; **receiver:** `crisis-manager`.

**Receiving condition:** Service owner confirms agreed validation signals and residual limitations

**Next:** Step 10.

**Role output contracts:** `it-service-owner:1`, `it-service-owner:4`.

- **`handoff_business_recovery_acceptance`**: For business recovery acceptance, supply the actual versioned business recovery acceptance record, including service_owner, validation_signals, observed_results, residual_limits, actual_decision. Independently assess the evidence against this exact criterion: Service owner confirms agreed validation signals and residual limitations. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `service_owner`, `validation_signals`, `observed_results`, `residual_limits`, `actual_decision`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `confirmed-breach`.

**Producer:** `it-service-owner`; **receiver:** `crisis-manager`.

**Receiving condition:** Service owner confirms agreed validation signals and residual limitations

**Next:** Step 10.

**Role output contracts:** `it-service-owner:1`, `it-service-owner:4`.

- **`handoff_business_recovery_acceptance`**: For business recovery acceptance, supply the actual versioned business recovery acceptance record, including service_owner, validation_signals, observed_results, residual_limits, actual_decision. Independently assess the evidence against this exact criterion: Service owner confirms agreed validation signals and residual limitations. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `service_owner`, `validation_signals`, `observed_results`, `residual_limits`, `actual_decision`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-cyber-incident-breach-to-recovery-10"></a>

## communication/regulatory action record

**Handoff content contract:** `handoff/cyber-incident-breach-to-recovery:10`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_incident_communications`**: For communication/regulatory action record, supply the actual versioned incident communications record, including approved_messages, recipients, regulatory_actions, authority, evidence_versions, timing. Independently assess the evidence against this exact criterion: Communications are authorised, consistent and evidence-based. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `approved_messages`, `recipients`, `regulatory_actions`, `authority`, `evidence_versions`, `timing`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `suspected`.

**Producer:** `crisis-manager`; **receiver:** `problem-manager`.

**Receiving condition:** Communications are authorised, consistent and evidence-based

**Next:** Step 11.

**Role output contracts:** `crisis-manager:2`, `crisis-manager:3`.

- **`handoff_incident_communications`**: For communication/regulatory action record, supply the actual versioned incident communications record, including approved_messages, recipients, regulatory_actions, authority, evidence_versions, timing. Independently assess the evidence against this exact criterion: Communications are authorised, consistent and evidence-based. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `approved_messages`, `recipients`, `regulatory_actions`, `authority`, `evidence_versions`, `timing`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `confirmed-breach`.

**Producer:** `crisis-manager`; **receiver:** `problem-manager`.

**Receiving condition:** Communications are authorised, consistent and evidence-based

**Next:** Step 11.

**Role output contracts:** `crisis-manager:2`, `crisis-manager:3`.

- **`handoff_incident_communications`**: For communication/regulatory action record, supply the actual versioned incident communications record, including approved_messages, recipients, regulatory_actions, authority, evidence_versions, timing. Independently assess the evidence against this exact criterion: Communications are authorised, consistent and evidence-based. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `approved_messages`, `recipients`, `regulatory_actions`, `authority`, `evidence_versions`, `timing`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-cyber-incident-breach-to-recovery-11"></a>

## lessons learned and systemic findings

**Handoff content contract:** `handoff/cyber-incident-breach-to-recovery:11`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_systemic_incident_findings`**: For lessons learned and systemic findings, supply the actual versioned systemic incident findings record, including causes, failed_controls, supporting_evidence, recurrence_risks, improvement_findings. Independently assess the evidence against this exact criterion: Findings address causes and failed controls, not only symptoms. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `causes`, `failed_controls`, `supporting_evidence`, `recurrence_risks`, `improvement_findings`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `suspected`.

**Producer:** `problem-manager`; **receiver:** `control-owner`.

**Receiving condition:** Findings address causes and failed controls, not only symptoms

**Next:** Step 12.

**Role output contracts:** `problem-manager:1`.

- **`handoff_systemic_incident_findings`**: For lessons learned and systemic findings, supply the actual versioned systemic incident findings record, including causes, failed_controls, supporting_evidence, recurrence_risks, improvement_findings. Independently assess the evidence against this exact criterion: Findings address causes and failed controls, not only symptoms. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `causes`, `failed_controls`, `supporting_evidence`, `recurrence_risks`, `improvement_findings`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `confirmed-breach`.

**Producer:** `problem-manager`; **receiver:** `control-owner`.

**Receiving condition:** Findings address causes and failed controls, not only symptoms

**Next:** Step 12.

**Role output contracts:** `problem-manager:1`.

- **`handoff_systemic_incident_findings`**: For lessons learned and systemic findings, supply the actual versioned systemic incident findings record, including causes, failed_controls, supporting_evidence, recurrence_risks, improvement_findings. Independently assess the evidence against this exact criterion: Findings address causes and failed controls, not only symptoms. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `causes`, `failed_controls`, `supporting_evidence`, `recurrence_risks`, `improvement_findings`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-cyber-incident-breach-to-recovery-12"></a>

## control remediation plan

**Handoff content contract:** `handoff/cyber-incident-breach-to-recovery:12`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_control_remediation`**: For control remediation plan, supply the actual versioned control remediation record, including finding_ids, control_owners, actions, due_dates, verification_methods. Independently assess the evidence against this exact criterion: Every material finding has a control owner, due date and verification method. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `finding_ids`, `control_owners`, `actions`, `due_dates`, `verification_methods`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `suspected`.

**Producer:** `control-owner`; **receiver:** `internal-it-auditor`.

**Receiving condition:** Every material finding has a control owner, due date and verification method

**Next:** Step 13.

**Role output contracts:** `control-owner:4`.

- **`handoff_control_remediation`**: For control remediation plan, supply the actual versioned control remediation record, including finding_ids, control_owners, actions, due_dates, verification_methods. Independently assess the evidence against this exact criterion: Every material finding has a control owner, due date and verification method. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `finding_ids`, `control_owners`, `actions`, `due_dates`, `verification_methods`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `confirmed-breach`.

**Producer:** `control-owner`; **receiver:** `internal-it-auditor`.

**Receiving condition:** Every material finding has a control owner, due date and verification method

**Next:** Step 13.

**Role output contracts:** `control-owner:4`.

- **`handoff_control_remediation`**: For control remediation plan, supply the actual versioned control remediation record, including finding_ids, control_owners, actions, due_dates, verification_methods. Independently assess the evidence against this exact criterion: Every material finding has a control owner, due date and verification method. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `finding_ids`, `control_owners`, `actions`, `due_dates`, `verification_methods`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-cyber-incident-breach-to-recovery-13"></a>

## closure assurance result

**Handoff content contract:** `handoff/cyber-incident-breach-to-recovery:13`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_incident_closure_assurance`**: For closure assurance result, supply the actual versioned incident closure assurance record, including independent_assessor, assessed_evidence, critical_findings, disposition, residual_limits, closure_recommendation. Independently assess the evidence against this exact criterion: No open critical finding is silently closed or self-assured. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `independent_assessor`, `assessed_evidence`, `critical_findings`, `disposition`, `residual_limits`, `closure_recommendation`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `suspected`.

**Producer:** `internal-it-auditor`; **receiver:** `engagement:named-authority`.

**Receiving condition:** No open critical finding is silently closed or self-assured

**Next:** Terminal disposition; no downstream step.

**Role output contracts:** `internal-it-auditor:4`.

- **`handoff_incident_closure_assurance`**: For closure assurance result, supply the actual versioned incident closure assurance record, including independent_assessor, assessed_evidence, critical_findings, disposition, residual_limits, closure_recommendation. Independently assess the evidence against this exact criterion: No open critical finding is silently closed or self-assured. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `independent_assessor`, `assessed_evidence`, `critical_findings`, `disposition`, `residual_limits`, `closure_recommendation`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `confirmed-breach`.

**Producer:** `internal-it-auditor`; **receiver:** `engagement:named-authority`.

**Receiving condition:** No open critical finding is silently closed or self-assured

**Next:** Terminal disposition; no downstream step.

**Role output contracts:** `internal-it-auditor:4`.

- **`handoff_incident_closure_assurance`**: For closure assurance result, supply the actual versioned incident closure assurance record, including independent_assessor, assessed_evidence, critical_findings, disposition, residual_limits, closure_recommendation. Independently assess the evidence against this exact criterion: No open critical finding is silently closed or self-assured. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `independent_assessor`, `assessed_evidence`, `critical_findings`, `disposition`, `residual_limits`, `closure_recommendation`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.
<!-- JAI:OUTPUT-CONTRACTS:END -->
