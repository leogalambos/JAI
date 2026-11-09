<!-- JAI:OUTPUT-CONTRACTS:START -->
# AI system from idea to approved production use: source-owned handoff contracts

[Catalogue](index.md)

<a id="output-handoff-ai-system-approval-1"></a>

## risk classification and inventory entry

**Handoff content contract:** `handoff/ai-system-approval:1`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_ai_inventory_classification`**: For risk classification and inventory entry, supply the actual versioned ai inventory classification record, including system_id, intended_use, risk_class, classification_basis, accountable_human, inventory_revision. Independently assess the evidence against this exact criterion: No production AI without a classification and an accountable human. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `system_id`, `intended_use`, `risk_class`, `classification_basis`, `accountable_human`, `inventory_revision`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `candidate-only`.

**Producer:** `ai-governance-officer`; **receiver:** `data-protection-officer`.

**Receiving condition:** No production AI without a classification and an accountable human

**Next:** Step 2.

**Role output contracts:** `ai-governance-officer:1`.

- **`handoff_ai_inventory_classification`**: For risk classification and inventory entry, supply the actual versioned ai inventory classification record, including system_id, intended_use, risk_class, classification_basis, accountable_human, inventory_revision. Independently assess the evidence against this exact criterion: No production AI without a classification and an accountable human. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `system_id`, `intended_use`, `risk_class`, `classification_basis`, `accountable_human`, `inventory_revision`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `bounded-pilot`.

**Producer:** `ai-governance-officer`; **receiver:** `data-protection-officer`.

**Receiving condition:** No production AI without a classification and an accountable human

**Next:** Step 2.

**Role output contracts:** `ai-governance-officer:1`.

- **`handoff_ai_inventory_classification`**: For risk classification and inventory entry, supply the actual versioned ai inventory classification record, including system_id, intended_use, risk_class, classification_basis, accountable_human, inventory_revision. Independently assess the evidence against this exact criterion: No production AI without a classification and an accountable human. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `system_id`, `intended_use`, `risk_class`, `classification_basis`, `accountable_human`, `inventory_revision`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `production`.

**Producer:** `ai-governance-officer`; **receiver:** `data-protection-officer`.

**Receiving condition:** No production AI without a classification and an accountable human

**Next:** Step 2.

**Role output contracts:** `ai-governance-officer:1`.

- **`handoff_ai_inventory_classification`**: For risk classification and inventory entry, supply the actual versioned ai inventory classification record, including system_id, intended_use, risk_class, classification_basis, accountable_human, inventory_revision. Independently assess the evidence against this exact criterion: No production AI without a classification and an accountable human. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `system_id`, `intended_use`, `risk_class`, `classification_basis`, `accountable_human`, `inventory_revision`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-ai-system-approval-2"></a>

## privacy and fairness position

**Handoff content contract:** `handoff/ai-system-approval:2`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_ai_impact_position`**: For privacy and fairness position, supply the actual versioned ai impact position record, including processing_scope, data_population, privacy_impacts, fairness_assessment, preuse_review, unresolved_obligations. Independently assess the evidence against this exact criterion: Impact assessment before processing, not retrospectively. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `processing_scope`, `data_population`, `privacy_impacts`, `fairness_assessment`, `preuse_review`, `unresolved_obligations`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `candidate-only`.

**Producer:** `data-protection-officer`; **receiver:** `data-scientist`.

**Receiving condition:** Impact assessment before processing, not retrospectively

**Next:** Step 3.

**Role output contracts:** `data-protection-officer:2`.

- **`handoff_ai_impact_position`**: For privacy and fairness position, supply the actual versioned ai impact position record, including processing_scope, data_population, privacy_impacts, fairness_assessment, preuse_review, unresolved_obligations. Independently assess the evidence against this exact criterion: Impact assessment before processing, not retrospectively. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `processing_scope`, `data_population`, `privacy_impacts`, `fairness_assessment`, `preuse_review`, `unresolved_obligations`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `bounded-pilot`.

**Producer:** `data-protection-officer`; **receiver:** `data-scientist`.

**Receiving condition:** Impact assessment before processing, not retrospectively

**Next:** Step 3.

**Role output contracts:** `data-protection-officer:2`.

- **`handoff_ai_impact_position`**: For privacy and fairness position, supply the actual versioned ai impact position record, including processing_scope, data_population, privacy_impacts, fairness_assessment, preuse_review, unresolved_obligations. Independently assess the evidence against this exact criterion: Impact assessment before processing, not retrospectively. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `processing_scope`, `data_population`, `privacy_impacts`, `fairness_assessment`, `preuse_review`, `unresolved_obligations`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `production`.

**Producer:** `data-protection-officer`; **receiver:** `data-scientist`.

**Receiving condition:** Impact assessment before processing, not retrospectively

**Next:** Step 3.

**Role output contracts:** `data-protection-officer:2`.

- **`handoff_ai_impact_position`**: For privacy and fairness position, supply the actual versioned ai impact position record, including processing_scope, data_population, privacy_impacts, fairness_assessment, preuse_review, unresolved_obligations. Independently assess the evidence against this exact criterion: Impact assessment before processing, not retrospectively. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `processing_scope`, `data_population`, `privacy_impacts`, `fairness_assessment`, `preuse_review`, `unresolved_obligations`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-ai-system-approval-3"></a>

## candidate model with held-out performance and stated limits

**Handoff content contract:** `handoff/ai-system-approval:3`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_candidate_model_evidence`**: For candidate model with held-out performance and stated limits, supply the actual versioned candidate model evidence record, including model_revision, permitted_data, test_scope, heldout_results, failure_modes, excluded_populations, limitations. Independently assess the evidence against this exact criterion: Permitted data and test scope are explicit; no production or pilot use before named human approval; failure modes and excluded populations are stated. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `model_revision`, `permitted_data`, `test_scope`, `heldout_results`, `failure_modes`, `excluded_populations`, `limitations`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `candidate-only`.

**Producer:** `data-scientist`; **receiver:** `ai-and-ml-architect`.

**Receiving condition:** Permitted data and test scope are explicit; no production or pilot use before named human approval; failure modes and excluded populations are stated

**Next:** Step 4.

**Role output contracts:** `data-scientist:1`, `data-scientist:2`.

- **`handoff_candidate_model_evidence`**: For candidate model with held-out performance and stated limits, supply the actual versioned candidate model evidence record, including model_revision, permitted_data, test_scope, heldout_results, failure_modes, excluded_populations, limitations. Independently assess the evidence against this exact criterion: Permitted data and test scope are explicit; no production or pilot use before named human approval; failure modes and excluded populations are stated. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `model_revision`, `permitted_data`, `test_scope`, `heldout_results`, `failure_modes`, `excluded_populations`, `limitations`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `bounded-pilot`.

**Producer:** `data-scientist`; **receiver:** `ai-and-ml-architect`.

**Receiving condition:** Permitted data and test scope are explicit; no production or pilot use before named human approval; failure modes and excluded populations are stated

**Next:** Step 4.

**Role output contracts:** `data-scientist:1`, `data-scientist:2`.

- **`handoff_candidate_model_evidence`**: For candidate model with held-out performance and stated limits, supply the actual versioned candidate model evidence record, including model_revision, permitted_data, test_scope, heldout_results, failure_modes, excluded_populations, limitations. Independently assess the evidence against this exact criterion: Permitted data and test scope are explicit; no production or pilot use before named human approval; failure modes and excluded populations are stated. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `model_revision`, `permitted_data`, `test_scope`, `heldout_results`, `failure_modes`, `excluded_populations`, `limitations`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `production`.

**Producer:** `data-scientist`; **receiver:** `ai-and-ml-architect`.

**Receiving condition:** Permitted data and test scope are explicit; no production or pilot use before named human approval; failure modes and excluded populations are stated

**Next:** Step 4.

**Role output contracts:** `data-scientist:1`, `data-scientist:2`.

- **`handoff_candidate_model_evidence`**: For candidate model with held-out performance and stated limits, supply the actual versioned candidate model evidence record, including model_revision, permitted_data, test_scope, heldout_results, failure_modes, excluded_populations, limitations. Independently assess the evidence against this exact criterion: Permitted data and test scope are explicit; no production or pilot use before named human approval; failure modes and excluded populations are stated. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `model_revision`, `permitted_data`, `test_scope`, `heldout_results`, `failure_modes`, `excluded_populations`, `limitations`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-ai-system-approval-4"></a>

## serving and monitoring architecture

**Handoff content contract:** `handoff/ai-system-approval:4`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_ai_serving_design`**: For serving and monitoring architecture, supply the actual versioned ai serving design record, including serving_revision, interfaces, data_lineage, drift_monitoring, degradation_thresholds, harm_monitoring, rollback_design. Independently assess the evidence against this exact criterion: Drift, degradation and harmful-output monitoring designed in. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `serving_revision`, `interfaces`, `data_lineage`, `drift_monitoring`, `degradation_thresholds`, `harm_monitoring`, `rollback_design`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `candidate-only`.

**Producer:** `ai-and-ml-architect`; **receiver:** `ai-safety-and-model-red-team-specialist`.

**Receiving condition:** Drift, degradation and harmful-output monitoring designed in

**Next:** Step 5.

**Role output contracts:** `ai-and-ml-architect:1`, `ai-and-ml-architect:4`.

- **`handoff_ai_serving_design`**: For serving and monitoring architecture, supply the actual versioned ai serving design record, including serving_revision, interfaces, data_lineage, drift_monitoring, degradation_thresholds, harm_monitoring, rollback_design. Independently assess the evidence against this exact criterion: Drift, degradation and harmful-output monitoring designed in. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `serving_revision`, `interfaces`, `data_lineage`, `drift_monitoring`, `degradation_thresholds`, `harm_monitoring`, `rollback_design`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `bounded-pilot`.

**Producer:** `ai-and-ml-architect`; **receiver:** `ai-safety-and-model-red-team-specialist`.

**Receiving condition:** Drift, degradation and harmful-output monitoring designed in

**Next:** Step 5.

**Role output contracts:** `ai-and-ml-architect:1`, `ai-and-ml-architect:4`.

- **`handoff_ai_serving_design`**: For serving and monitoring architecture, supply the actual versioned ai serving design record, including serving_revision, interfaces, data_lineage, drift_monitoring, degradation_thresholds, harm_monitoring, rollback_design. Independently assess the evidence against this exact criterion: Drift, degradation and harmful-output monitoring designed in. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `serving_revision`, `interfaces`, `data_lineage`, `drift_monitoring`, `degradation_thresholds`, `harm_monitoring`, `rollback_design`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `production`.

**Producer:** `ai-and-ml-architect`; **receiver:** `ai-safety-and-model-red-team-specialist`.

**Receiving condition:** Drift, degradation and harmful-output monitoring designed in

**Next:** Step 5.

**Role output contracts:** `ai-and-ml-architect:1`, `ai-and-ml-architect:4`.

- **`handoff_ai_serving_design`**: For serving and monitoring architecture, supply the actual versioned ai serving design record, including serving_revision, interfaces, data_lineage, drift_monitoring, degradation_thresholds, harm_monitoring, rollback_design. Independently assess the evidence against this exact criterion: Drift, degradation and harmful-output monitoring designed in. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `serving_revision`, `interfaces`, `data_lineage`, `drift_monitoring`, `degradation_thresholds`, `harm_monitoring`, `rollback_design`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-ai-system-approval-5"></a>

## adversarial findings with severity and owners

**Handoff content contract:** `handoff/ai-system-approval:5`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_ai_adversarial_findings`**: For adversarial findings with severity and owners, supply the actual versioned ai adversarial findings record, including candidate_configuration, permitted_test_scope, offensive_authorisation, findings, severity, owners. Independently assess the evidence against this exact criterion: Candidate tests use the intended configuration without production or pilot effects; any offensive testing requires prior written authorisation. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `candidate_configuration`, `permitted_test_scope`, `offensive_authorisation`, `findings`, `severity`, `owners`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `candidate-only`.

**Producer:** `ai-safety-and-model-red-team-specialist`; **receiver:** `engagement:named-authority`.

**Receiving condition:** Candidate tests use the intended configuration without production or pilot effects; any offensive testing requires prior written authorisation

**Next:** Terminal disposition; no downstream step.

**Role output contracts:** `ai-safety-and-model-red-team-specialist:1`, `ai-safety-and-model-red-team-specialist:2`, `ai-safety-and-model-red-team-specialist:3`.

- **`handoff_ai_adversarial_findings`**: For adversarial findings with severity and owners, supply the actual versioned ai adversarial findings record, including candidate_configuration, permitted_test_scope, offensive_authorisation, findings, severity, owners. Independently assess the evidence against this exact criterion: Candidate tests use the intended configuration without production or pilot effects; any offensive testing requires prior written authorisation. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `candidate_configuration`, `permitted_test_scope`, `offensive_authorisation`, `findings`, `severity`, `owners`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `bounded-pilot`.

**Producer:** `ai-safety-and-model-red-team-specialist`; **receiver:** `engagement:named-authority`.

**Receiving condition:** Candidate tests use the intended configuration without production or pilot effects; any offensive testing requires prior written authorisation

**Next:** Step 6.

**Role output contracts:** `ai-safety-and-model-red-team-specialist:1`, `ai-safety-and-model-red-team-specialist:2`, `ai-safety-and-model-red-team-specialist:3`.

- **`handoff_ai_adversarial_findings`**: For adversarial findings with severity and owners, supply the actual versioned ai adversarial findings record, including candidate_configuration, permitted_test_scope, offensive_authorisation, findings, severity, owners. Independently assess the evidence against this exact criterion: Candidate tests use the intended configuration without production or pilot effects; any offensive testing requires prior written authorisation. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `candidate_configuration`, `permitted_test_scope`, `offensive_authorisation`, `findings`, `severity`, `owners`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `production`.

**Producer:** `ai-safety-and-model-red-team-specialist`; **receiver:** `engagement:named-authority`.

**Receiving condition:** Candidate tests use the intended configuration without production or pilot effects; any offensive testing requires prior written authorisation

**Next:** Step 6.

**Role output contracts:** `ai-safety-and-model-red-team-specialist:1`, `ai-safety-and-model-red-team-specialist:2`, `ai-safety-and-model-red-team-specialist:3`.

- **`handoff_ai_adversarial_findings`**: For adversarial findings with severity and owners, supply the actual versioned ai adversarial findings record, including candidate_configuration, permitted_test_scope, offensive_authorisation, findings, severity, owners. Independently assess the evidence against this exact criterion: Candidate tests use the intended configuration without production or pilot effects; any offensive testing requires prior written authorisation. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `candidate_configuration`, `permitted_test_scope`, `offensive_authorisation`, `findings`, `severity`, `owners`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-ai-system-approval-6"></a>

## exact scoped human approval or rejection

**Handoff content contract:** `handoff/ai-system-approval:6`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_ai_human_decision`**: For exact scoped human approval or rejection, supply the actual versioned ai human decision record, including candidate_revision, data_users_environment_scope, evidence_refs, authority, actual_decision, conditions, validity. Independently assess the evidence against this exact criterion: Candidate evidence, privacy, safety, lineage, monitoring and rollback readiness are reviewed before any production or pilot effect; an agent cannot approve. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `candidate_revision`, `data_users_environment_scope`, `evidence_refs`, `authority`, `actual_decision`, `conditions`, `validity`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `bounded-pilot`.

**Producer:** `engagement:named-authority`; **receiver:** `machine-learning-engineer`.

**Receiving condition:** Candidate evidence, privacy, safety, lineage, monitoring and rollback readiness are reviewed before any production or pilot effect; an agent cannot approve

**Next:** Step 7.

**Role output contracts:** Source-owned handoff only.

- **`handoff_ai_human_decision`**: For exact scoped human approval or rejection, supply the actual versioned ai human decision record, including candidate_revision, data_users_environment_scope, evidence_refs, authority, actual_decision, conditions, validity. Independently assess the evidence against this exact criterion: Candidate evidence, privacy, safety, lineage, monitoring and rollback readiness are reviewed before any production or pilot effect; an agent cannot approve. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `candidate_revision`, `data_users_environment_scope`, `evidence_refs`, `authority`, `actual_decision`, `conditions`, `validity`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `production`.

**Producer:** `engagement:named-authority`; **receiver:** `machine-learning-engineer`.

**Receiving condition:** Candidate evidence, privacy, safety, lineage, monitoring and rollback readiness are reviewed before any production or pilot effect; an agent cannot approve

**Next:** Step 7.

**Role output contracts:** Source-owned handoff only.

- **`handoff_ai_human_decision`**: For exact scoped human approval or rejection, supply the actual versioned ai human decision record, including candidate_revision, data_users_environment_scope, evidence_refs, authority, actual_decision, conditions, validity. Independently assess the evidence against this exact criterion: Candidate evidence, privacy, safety, lineage, monitoring and rollback readiness are reviewed before any production or pilot effect; an agent cannot approve. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `candidate_revision`, `data_users_environment_scope`, `evidence_refs`, `authority`, `actual_decision`, `conditions`, `validity`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-ai-system-approval-6"></a>

## exact scoped human approval or rejection

**Producer:** Named authority.

**Basis:** JAI-authored source handoff practice; supplements the existing workflow gate without granting authority.

### Required information (MUST)

- Identify the named human authority, exact candidate version, intended use, deployment scope and reviewed risk and assurance evidence.
- Record the actual approval, rejection or conditional decision before the corresponding production effects; an agent recommendation is not authority.
- Identify conditions, unresolved evidence, monitoring obligations, validity and change triggers; reference verified external approval where the governing profile requires it.

### Conditionally required information

- **When:** Evidence requires a bounded pilot before final approval. **Required:** Reference prior authority for that exact pilot scope, safeguards and stop conditions; pilot evidence does not authorise broader production use.

### Optional information (MAY)

- Decision communication within the authorised scope.

**Receiving condition:** Candidate evidence, privacy, safety, lineage, monitoring and rollback readiness are reviewed before any production or pilot effect; an agent cannot approve

Unknown applicability and missing evidence remain explicit gaps. A proposed contract, a drafted decision or a successful rendition grants no acceptance or release permission.

<a id="output-handoff-ai-system-approval-7"></a>

## authorised deployed version and reproducible training lineage

**Handoff content contract:** `handoff/ai-system-approval:7`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_authorised_model_deployment`**: For authorised deployed version and reproducible training lineage, supply the actual versioned authorised model deployment record, including prior_decision_ref, deployed_version, training_run, data_lineage, actual_environment, actual_scope. Independently assess the evidence against this exact criterion: Prior named human approval covers the exact version, data, users, environment and production or pilot scope; every deployed version is traceable to its training run. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `prior_decision_ref`, `deployed_version`, `training_run`, `data_lineage`, `actual_environment`, `actual_scope`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `bounded-pilot`.

**Producer:** `machine-learning-engineer`; **receiver:** `mlops-engineer`.

**Receiving condition:** Prior named human approval covers the exact version, data, users, environment and production or pilot scope; every deployed version is traceable to its training run

**Next:** Step 8.

**Role output contracts:** `machine-learning-engineer:1`, `machine-learning-engineer:2`.

- **`handoff_authorised_model_deployment`**: For authorised deployed version and reproducible training lineage, supply the actual versioned authorised model deployment record, including prior_decision_ref, deployed_version, training_run, data_lineage, actual_environment, actual_scope. Independently assess the evidence against this exact criterion: Prior named human approval covers the exact version, data, users, environment and production or pilot scope; every deployed version is traceable to its training run. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `prior_decision_ref`, `deployed_version`, `training_run`, `data_lineage`, `actual_environment`, `actual_scope`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `production`.

**Producer:** `machine-learning-engineer`; **receiver:** `mlops-engineer`.

**Receiving condition:** Prior named human approval covers the exact version, data, users, environment and production or pilot scope; every deployed version is traceable to its training run

**Next:** Step 8.

**Role output contracts:** `machine-learning-engineer:1`, `machine-learning-engineer:2`.

- **`handoff_authorised_model_deployment`**: For authorised deployed version and reproducible training lineage, supply the actual versioned authorised model deployment record, including prior_decision_ref, deployed_version, training_run, data_lineage, actual_environment, actual_scope. Independently assess the evidence against this exact criterion: Prior named human approval covers the exact version, data, users, environment and production or pilot scope; every deployed version is traceable to its training run. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `prior_decision_ref`, `deployed_version`, `training_run`, `data_lineage`, `actual_environment`, `actual_scope`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-ai-system-approval-8"></a>

## monitored model with defined thresholds and rollback

**Handoff content contract:** `handoff/ai-system-approval:8`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_model_operating_evidence`**: For monitored model with defined thresholds and rollback, supply the actual versioned model operating evidence record, including prior_decision_ref, monitored_revision, signals, thresholds, observed_breaches, rollback_route. Independently assess the evidence against this exact criterion: Prior named human approval covers operation and rollback scope; thresholds and an authorised rollback route exist. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `prior_decision_ref`, `monitored_revision`, `signals`, `thresholds`, `observed_breaches`, `rollback_route`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `bounded-pilot`.

**Producer:** `mlops-engineer`; **receiver:** `ai-governance-officer`.

**Receiving condition:** Prior named human approval covers operation and rollback scope; thresholds and an authorised rollback route exist

**Next:** Step 9.

**Role output contracts:** `mlops-engineer:2`, `mlops-engineer:4`.

- **`handoff_model_operating_evidence`**: For monitored model with defined thresholds and rollback, supply the actual versioned model operating evidence record, including prior_decision_ref, monitored_revision, signals, thresholds, observed_breaches, rollback_route. Independently assess the evidence against this exact criterion: Prior named human approval covers operation and rollback scope; thresholds and an authorised rollback route exist. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `prior_decision_ref`, `monitored_revision`, `signals`, `thresholds`, `observed_breaches`, `rollback_route`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `production`.

**Producer:** `mlops-engineer`; **receiver:** `ai-governance-officer`.

**Receiving condition:** Prior named human approval covers operation and rollback scope; thresholds and an authorised rollback route exist

**Next:** Step 9.

**Role output contracts:** `mlops-engineer:2`, `mlops-engineer:4`.

- **`handoff_model_operating_evidence`**: For monitored model with defined thresholds and rollback, supply the actual versioned model operating evidence record, including prior_decision_ref, monitored_revision, signals, thresholds, observed_breaches, rollback_route. Independently assess the evidence against this exact criterion: Prior named human approval covers operation and rollback scope; thresholds and an authorised rollback route exist. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `prior_decision_ref`, `monitored_revision`, `signals`, `thresholds`, `observed_breaches`, `rollback_route`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-ai-system-approval-9"></a>

## periodic assessment, challenge route and next review trigger

**Handoff content contract:** `handoff/ai-system-approval:9`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_ai_periodic_review`**: For periodic assessment, challenge route and next review trigger, supply the actual versioned ai periodic review record, including operated_scope, review_evidence, challenge_route, expiry, material_changes, renewal_decision. Independently assess the evidence against this exact criterion: The challenge route is published; expired or materially changed scope is not operated without renewed prior human approval. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `operated_scope`, `review_evidence`, `challenge_route`, `expiry`, `material_changes`, `renewal_decision`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `bounded-pilot`.

**Producer:** `ai-governance-officer`; **receiver:** `engagement:named-authority`.

**Receiving condition:** The challenge route is published; expired or materially changed scope is not operated without renewed prior human approval

**Next:** Terminal disposition; no downstream step.

**Role output contracts:** `ai-governance-officer:3`.

- **`handoff_ai_periodic_review`**: For periodic assessment, challenge route and next review trigger, supply the actual versioned ai periodic review record, including operated_scope, review_evidence, challenge_route, expiry, material_changes, renewal_decision. Independently assess the evidence against this exact criterion: The challenge route is published; expired or materially changed scope is not operated without renewed prior human approval. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `operated_scope`, `review_evidence`, `challenge_route`, `expiry`, `material_changes`, `renewal_decision`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `production`.

**Producer:** `ai-governance-officer`; **receiver:** `engagement:named-authority`.

**Receiving condition:** The challenge route is published; expired or materially changed scope is not operated without renewed prior human approval

**Next:** Terminal disposition; no downstream step.

**Role output contracts:** `ai-governance-officer:3`.

- **`handoff_ai_periodic_review`**: For periodic assessment, challenge route and next review trigger, supply the actual versioned ai periodic review record, including operated_scope, review_evidence, challenge_route, expiry, material_changes, renewal_decision. Independently assess the evidence against this exact criterion: The challenge route is published; expired or materially changed scope is not operated without renewed prior human approval. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `operated_scope`, `review_evidence`, `challenge_route`, `expiry`, `material_changes`, `renewal_decision`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.
<!-- JAI:OUTPUT-CONTRACTS:END -->
