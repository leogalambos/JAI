<!-- JAI:OUTPUT-CONTRACTS:START -->
# Production change: source-owned handoff contracts

[Catalogue](index.md)

<a id="output-handoff-production-change-1"></a>

## reviewed change and rollback plan

**Handoff content contract:** `handoff/production-change:1`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_reviewed_change`**: For reviewed change and rollback plan, supply the actual versioned reviewed change record, including source_revision, change_scope, review_result, review_size, recovery_plan. Independently assess the evidence against this exact criterion: Small enough to review in one pass. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `source_revision`, `change_scope`, `review_result`, `review_size`, `recovery_plan`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `standard/application`.

**Producer:** `software-engineer`; **receiver:** `engagement:change-impact-owner`.

**Receiving condition:** Small enough to review in one pass

**Next:** Step 2.

**Role output contracts:** `software-engineer:1`, `software-engineer:4`.

- **`handoff_reviewed_change`**: For reviewed change and rollback plan, supply the actual versioned reviewed change record, including source_revision, change_scope, review_result, review_size, recovery_plan. Independently assess the evidence against this exact criterion: Small enough to review in one pass. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `source_revision`, `change_scope`, `review_result`, `review_size`, `recovery_plan`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `standard/infrastructure-as-code`.

**Producer:** `software-engineer`; **receiver:** `infrastructure-as-code-engineer`.

**Receiving condition:** Small enough to review in one pass

**Next:** Step 2.

**Role output contracts:** `software-engineer:1`, `software-engineer:4`.

- **`handoff_reviewed_change`**: For reviewed change and rollback plan, supply the actual versioned reviewed change record, including source_revision, change_scope, review_result, review_size, recovery_plan. Independently assess the evidence against this exact criterion: Small enough to review in one pass. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `source_revision`, `change_scope`, `review_result`, `review_size`, `recovery_plan`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `standard/configuration`.

**Producer:** `engagement:configuration-change-owner`; **receiver:** `engagement:configuration-change-owner`.

**Receiving condition:** The exact settings change and recovery plan are reviewed against the owned baseline; no source-code change is fabricated.

**Next:** Step 2.

**Role output contracts:** `implementation-consultant:3`.

- **`handoff_reviewed_configuration_change`**: The exact settings change and recovery plan are reviewed against the owned baseline; no source-code change is fabricated.
  Required fields: `configuration_revision`, `affected_settings`, `approved_baseline`, `review_evidence`, `verification_plan`, `recovery_plan`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `normal/application`.

**Producer:** `software-engineer`; **receiver:** `engagement:change-impact-owner`.

**Receiving condition:** Small enough to review in one pass

**Next:** Step 2.

**Role output contracts:** `software-engineer:1`, `software-engineer:4`.

- **`handoff_reviewed_change`**: For reviewed change and rollback plan, supply the actual versioned reviewed change record, including source_revision, change_scope, review_result, review_size, recovery_plan. Independently assess the evidence against this exact criterion: Small enough to review in one pass. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `source_revision`, `change_scope`, `review_result`, `review_size`, `recovery_plan`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `normal/infrastructure-as-code`.

**Producer:** `software-engineer`; **receiver:** `infrastructure-as-code-engineer`.

**Receiving condition:** Small enough to review in one pass

**Next:** Step 2.

**Role output contracts:** `software-engineer:1`, `software-engineer:4`.

- **`handoff_reviewed_change`**: For reviewed change and rollback plan, supply the actual versioned reviewed change record, including source_revision, change_scope, review_result, review_size, recovery_plan. Independently assess the evidence against this exact criterion: Small enough to review in one pass. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `source_revision`, `change_scope`, `review_result`, `review_size`, `recovery_plan`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `normal/configuration`.

**Producer:** `engagement:configuration-change-owner`; **receiver:** `engagement:configuration-change-owner`.

**Receiving condition:** The exact settings change and recovery plan are reviewed against the owned baseline; no source-code change is fabricated.

**Next:** Step 2.

**Role output contracts:** `implementation-consultant:3`.

- **`handoff_reviewed_configuration_change`**: The exact settings change and recovery plan are reviewed against the owned baseline; no source-code change is fabricated.
  Required fields: `configuration_revision`, `affected_settings`, `approved_baseline`, `review_evidence`, `verification_plan`, `recovery_plan`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `emergency/application`.

**Producer:** `software-engineer`; **receiver:** `engagement:change-impact-owner`.

**Receiving condition:** Small enough to review in one pass

**Next:** Step 2.

**Role output contracts:** `software-engineer:1`, `software-engineer:4`.

- **`handoff_reviewed_change`**: For reviewed change and rollback plan, supply the actual versioned reviewed change record, including source_revision, change_scope, review_result, review_size, recovery_plan. Independently assess the evidence against this exact criterion: Small enough to review in one pass. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `source_revision`, `change_scope`, `review_result`, `review_size`, `recovery_plan`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `emergency/infrastructure-as-code`.

**Producer:** `software-engineer`; **receiver:** `infrastructure-as-code-engineer`.

**Receiving condition:** Small enough to review in one pass

**Next:** Step 2.

**Role output contracts:** `software-engineer:1`, `software-engineer:4`.

- **`handoff_reviewed_change`**: For reviewed change and rollback plan, supply the actual versioned reviewed change record, including source_revision, change_scope, review_result, review_size, recovery_plan. Independently assess the evidence against this exact criterion: Small enough to review in one pass. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `source_revision`, `change_scope`, `review_result`, `review_size`, `recovery_plan`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `emergency/configuration`.

**Producer:** `engagement:configuration-change-owner`; **receiver:** `engagement:configuration-change-owner`.

**Receiving condition:** The exact settings change and recovery plan are reviewed against the owned baseline; no source-code change is fabricated.

**Next:** Step 2.

**Role output contracts:** `implementation-consultant:3`.

- **`handoff_reviewed_configuration_change`**: The exact settings change and recovery plan are reviewed against the owned baseline; no source-code change is fabricated.
  Required fields: `configuration_revision`, `affected_settings`, `approved_baseline`, `review_evidence`, `verification_plan`, `recovery_plan`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-production-change-2"></a>

## reviewed plan; destructive operations flagged

**Handoff content contract:** `handoff/production-change:2`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_reviewed_infrastructure_plan`**: For reviewed plan; destructive operations flagged, supply the actual versioned reviewed infrastructure plan record, including plan_digest, target_assets, destructive_actions, reviewer, actual_apply_identity. Independently assess the evidence against this exact criterion: The applied plan is the reviewed plan. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `plan_digest`, `target_assets`, `destructive_actions`, `reviewer`, `actual_apply_identity`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `standard/application`.

**Producer:** `engagement:change-impact-owner`; **receiver:** `test-analyst`.

**Receiving condition:** Assess the application change against infrastructure dependencies; evidence supports any unchanged-infrastructure conclusion rather than claiming an IaC apply that did not occur.

**Next:** Step 3.

**Role output contracts:** `configuration-manager:3`.

- **`handoff_application_infrastructure_impact`**: Assess the application change against infrastructure dependencies; evidence supports any unchanged-infrastructure conclusion rather than claiming an IaC apply that did not occur.
  Required fields: `change_revision`, `affected_assets`, `infrastructure_delta`, `retained_baseline`, `compatibility_evidence`, `owner`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `standard/infrastructure-as-code`.

**Producer:** `infrastructure-as-code-engineer`; **receiver:** `test-analyst`.

**Receiving condition:** The applied plan is the reviewed plan

**Next:** Step 3.

**Role output contracts:** `infrastructure-as-code-engineer:1`, `infrastructure-as-code-engineer:3`.

- **`handoff_reviewed_infrastructure_plan`**: For reviewed plan; destructive operations flagged, supply the actual versioned reviewed infrastructure plan record, including plan_digest, target_assets, destructive_actions, reviewer, actual_apply_identity. Independently assess the evidence against this exact criterion: The applied plan is the reviewed plan. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `plan_digest`, `target_assets`, `destructive_actions`, `reviewer`, `actual_apply_identity`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `standard/configuration`.

**Producer:** `engagement:configuration-change-owner`; **receiver:** `test-analyst`.

**Receiving condition:** The actual applied configuration plan is the reviewed plan; destructive effects and applicable authority are explicit.

**Next:** Step 3.

**Role output contracts:** `implementation-consultant:3`.

- **`handoff_configuration_change_plan`**: The actual applied configuration plan is the reviewed plan; destructive effects and applicable authority are explicit.
  Required fields: `reviewed_plan`, `target_assets`, `exact_settings`, `destructive_effects`, `reviewer`, `execution_identity`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `normal/application`.

**Producer:** `engagement:change-impact-owner`; **receiver:** `test-analyst`.

**Receiving condition:** Assess the application change against infrastructure dependencies; evidence supports any unchanged-infrastructure conclusion rather than claiming an IaC apply that did not occur.

**Next:** Step 3.

**Role output contracts:** `configuration-manager:3`.

- **`handoff_application_infrastructure_impact`**: Assess the application change against infrastructure dependencies; evidence supports any unchanged-infrastructure conclusion rather than claiming an IaC apply that did not occur.
  Required fields: `change_revision`, `affected_assets`, `infrastructure_delta`, `retained_baseline`, `compatibility_evidence`, `owner`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `normal/infrastructure-as-code`.

**Producer:** `infrastructure-as-code-engineer`; **receiver:** `test-analyst`.

**Receiving condition:** The applied plan is the reviewed plan

**Next:** Step 3.

**Role output contracts:** `infrastructure-as-code-engineer:1`, `infrastructure-as-code-engineer:3`.

- **`handoff_reviewed_infrastructure_plan`**: For reviewed plan; destructive operations flagged, supply the actual versioned reviewed infrastructure plan record, including plan_digest, target_assets, destructive_actions, reviewer, actual_apply_identity. Independently assess the evidence against this exact criterion: The applied plan is the reviewed plan. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `plan_digest`, `target_assets`, `destructive_actions`, `reviewer`, `actual_apply_identity`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `normal/configuration`.

**Producer:** `engagement:configuration-change-owner`; **receiver:** `test-analyst`.

**Receiving condition:** The actual applied configuration plan is the reviewed plan; destructive effects and applicable authority are explicit.

**Next:** Step 3.

**Role output contracts:** `implementation-consultant:3`.

- **`handoff_configuration_change_plan`**: The actual applied configuration plan is the reviewed plan; destructive effects and applicable authority are explicit.
  Required fields: `reviewed_plan`, `target_assets`, `exact_settings`, `destructive_effects`, `reviewer`, `execution_identity`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `emergency/application`.

**Producer:** `engagement:change-impact-owner`; **receiver:** `test-analyst`.

**Receiving condition:** Assess the application change against infrastructure dependencies; evidence supports any unchanged-infrastructure conclusion rather than claiming an IaC apply that did not occur.

**Next:** Step 3.

**Role output contracts:** `configuration-manager:3`.

- **`handoff_application_infrastructure_impact`**: Assess the application change against infrastructure dependencies; evidence supports any unchanged-infrastructure conclusion rather than claiming an IaC apply that did not occur.
  Required fields: `change_revision`, `affected_assets`, `infrastructure_delta`, `retained_baseline`, `compatibility_evidence`, `owner`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `emergency/infrastructure-as-code`.

**Producer:** `infrastructure-as-code-engineer`; **receiver:** `test-analyst`.

**Receiving condition:** The applied plan is the reviewed plan

**Next:** Step 3.

**Role output contracts:** `infrastructure-as-code-engineer:1`, `infrastructure-as-code-engineer:3`.

- **`handoff_reviewed_infrastructure_plan`**: For reviewed plan; destructive operations flagged, supply the actual versioned reviewed infrastructure plan record, including plan_digest, target_assets, destructive_actions, reviewer, actual_apply_identity. Independently assess the evidence against this exact criterion: The applied plan is the reviewed plan. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `plan_digest`, `target_assets`, `destructive_actions`, `reviewer`, `actual_apply_identity`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `emergency/configuration`.

**Producer:** `engagement:configuration-change-owner`; **receiver:** `test-analyst`.

**Receiving condition:** The actual applied configuration plan is the reviewed plan; destructive effects and applicable authority are explicit.

**Next:** Step 3.

**Role output contracts:** `implementation-consultant:3`.

- **`handoff_configuration_change_plan`**: The actual applied configuration plan is the reviewed plan; destructive effects and applicable authority are explicit.
  Required fields: `reviewed_plan`, `target_assets`, `exact_settings`, `destructive_effects`, `reviewer`, `execution_identity`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-production-change-3"></a>

## test evidence with coverage and residual risk

**Handoff content contract:** `handoff/production-change:3`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_change_test_evidence`**: For test evidence with coverage and residual risk, supply the actual versioned change test evidence record, including tested_revision, coverage, actual_results, residual_risks, named_risk_disposition. Independently assess the evidence against this exact criterion: Residual risk accepted by a named person. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `tested_revision`, `coverage`, `actual_results`, `residual_risks`, `named_risk_disposition`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `standard/application`.

**Producer:** `test-analyst`; **receiver:** `release-engineer`.

**Receiving condition:** Residual risk accepted by a named person

**Next:** Step 4.

**Role output contracts:** `test-analyst:2`, `test-analyst:4`.

- **`handoff_change_test_evidence`**: For test evidence with coverage and residual risk, supply the actual versioned change test evidence record, including tested_revision, coverage, actual_results, residual_risks, named_risk_disposition. Independently assess the evidence against this exact criterion: Residual risk accepted by a named person. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `tested_revision`, `coverage`, `actual_results`, `residual_risks`, `named_risk_disposition`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `standard/infrastructure-as-code`.

**Producer:** `test-analyst`; **receiver:** `release-engineer`.

**Receiving condition:** Residual risk accepted by a named person

**Next:** Step 4.

**Role output contracts:** `test-analyst:2`, `test-analyst:4`.

- **`handoff_change_test_evidence`**: For test evidence with coverage and residual risk, supply the actual versioned change test evidence record, including tested_revision, coverage, actual_results, residual_risks, named_risk_disposition. Independently assess the evidence against this exact criterion: Residual risk accepted by a named person. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `tested_revision`, `coverage`, `actual_results`, `residual_risks`, `named_risk_disposition`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `standard/configuration`.

**Producer:** `test-analyst`; **receiver:** `engagement:release-control-owner`.

**Receiving condition:** Residual risk accepted by a named person

**Next:** Step 4.

**Role output contracts:** `test-analyst:2`, `test-analyst:4`.

- **`handoff_change_test_evidence`**: For test evidence with coverage and residual risk, supply the actual versioned change test evidence record, including tested_revision, coverage, actual_results, residual_risks, named_risk_disposition. Independently assess the evidence against this exact criterion: Residual risk accepted by a named person. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `tested_revision`, `coverage`, `actual_results`, `residual_risks`, `named_risk_disposition`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `normal/application`.

**Producer:** `test-analyst`; **receiver:** `release-engineer`.

**Receiving condition:** Residual risk accepted by a named person

**Next:** Step 4.

**Role output contracts:** `test-analyst:2`, `test-analyst:4`.

- **`handoff_change_test_evidence`**: For test evidence with coverage and residual risk, supply the actual versioned change test evidence record, including tested_revision, coverage, actual_results, residual_risks, named_risk_disposition. Independently assess the evidence against this exact criterion: Residual risk accepted by a named person. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `tested_revision`, `coverage`, `actual_results`, `residual_risks`, `named_risk_disposition`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `normal/infrastructure-as-code`.

**Producer:** `test-analyst`; **receiver:** `release-engineer`.

**Receiving condition:** Residual risk accepted by a named person

**Next:** Step 4.

**Role output contracts:** `test-analyst:2`, `test-analyst:4`.

- **`handoff_change_test_evidence`**: For test evidence with coverage and residual risk, supply the actual versioned change test evidence record, including tested_revision, coverage, actual_results, residual_risks, named_risk_disposition. Independently assess the evidence against this exact criterion: Residual risk accepted by a named person. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `tested_revision`, `coverage`, `actual_results`, `residual_risks`, `named_risk_disposition`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `normal/configuration`.

**Producer:** `test-analyst`; **receiver:** `engagement:release-control-owner`.

**Receiving condition:** Residual risk accepted by a named person

**Next:** Step 4.

**Role output contracts:** `test-analyst:2`, `test-analyst:4`.

- **`handoff_change_test_evidence`**: For test evidence with coverage and residual risk, supply the actual versioned change test evidence record, including tested_revision, coverage, actual_results, residual_risks, named_risk_disposition. Independently assess the evidence against this exact criterion: Residual risk accepted by a named person. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `tested_revision`, `coverage`, `actual_results`, `residual_risks`, `named_risk_disposition`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `emergency/application`.

**Producer:** `test-analyst`; **receiver:** `release-engineer`.

**Receiving condition:** Residual risk accepted by a named person

**Next:** Step 4.

**Role output contracts:** `test-analyst:2`, `test-analyst:4`.

- **`handoff_change_test_evidence`**: For test evidence with coverage and residual risk, supply the actual versioned change test evidence record, including tested_revision, coverage, actual_results, residual_risks, named_risk_disposition. Independently assess the evidence against this exact criterion: Residual risk accepted by a named person. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `tested_revision`, `coverage`, `actual_results`, `residual_risks`, `named_risk_disposition`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `emergency/infrastructure-as-code`.

**Producer:** `test-analyst`; **receiver:** `release-engineer`.

**Receiving condition:** Residual risk accepted by a named person

**Next:** Step 4.

**Role output contracts:** `test-analyst:2`, `test-analyst:4`.

- **`handoff_change_test_evidence`**: For test evidence with coverage and residual risk, supply the actual versioned change test evidence record, including tested_revision, coverage, actual_results, residual_risks, named_risk_disposition. Independently assess the evidence against this exact criterion: Residual risk accepted by a named person. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `tested_revision`, `coverage`, `actual_results`, `residual_risks`, `named_risk_disposition`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `emergency/configuration`.

**Producer:** `test-analyst`; **receiver:** `engagement:release-control-owner`.

**Receiving condition:** Residual risk accepted by a named person

**Next:** Step 4.

**Role output contracts:** `test-analyst:2`, `test-analyst:4`.

- **`handoff_change_test_evidence`**: For test evidence with coverage and residual risk, supply the actual versioned change test evidence record, including tested_revision, coverage, actual_results, residual_risks, named_risk_disposition. Independently assess the evidence against this exact criterion: Residual risk accepted by a named person. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `tested_revision`, `coverage`, `actual_results`, `residual_risks`, `named_risk_disposition`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-production-change-4"></a>

## release manifest with signed provenance

**Handoff content contract:** `handoff/production-change:4`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_release_provenance`**: For release manifest with signed provenance, supply the actual versioned release provenance record, including manifest_revision, artifacts, source_commits, signatures, target_scope. Independently assess the evidence against this exact criterion: Every artefact traceable to a source commit. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `manifest_revision`, `artifacts`, `source_commits`, `signatures`, `target_scope`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `standard/application`.

**Producer:** `release-engineer`; **receiver:** `change-manager`.

**Receiving condition:** Every artefact traceable to a source commit

**Next:** Step 5.

**Role output contracts:** `release-engineer:2`.

- **`handoff_release_provenance`**: For release manifest with signed provenance, supply the actual versioned release provenance record, including manifest_revision, artifacts, source_commits, signatures, target_scope. Independently assess the evidence against this exact criterion: Every artefact traceable to a source commit. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `manifest_revision`, `artifacts`, `source_commits`, `signatures`, `target_scope`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `standard/infrastructure-as-code`.

**Producer:** `release-engineer`; **receiver:** `change-manager`.

**Receiving condition:** Every artefact traceable to a source commit

**Next:** Step 5.

**Role output contracts:** `release-engineer:2`.

- **`handoff_release_provenance`**: For release manifest with signed provenance, supply the actual versioned release provenance record, including manifest_revision, artifacts, source_commits, signatures, target_scope. Independently assess the evidence against this exact criterion: Every artefact traceable to a source commit. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `manifest_revision`, `artifacts`, `source_commits`, `signatures`, `target_scope`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `standard/configuration`.

**Producer:** `engagement:release-control-owner`; **receiver:** `change-manager`.

**Receiving condition:** Every applied setting/version is traceable to the exact reviewed configuration baseline and change, with attributable verification provenance.

**Next:** Step 5.

**Role output contracts:** `release-engineer:2`.

- **`handoff_configuration_release_manifest`**: Every applied setting/version is traceable to the exact reviewed configuration baseline and change, with attributable verification provenance.
  Required fields: `manifest_revision`, `configuration_versions`, `source_baseline`, `change_identity`, `verification_provenance`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `normal/application`.

**Producer:** `release-engineer`; **receiver:** `change-manager`.

**Receiving condition:** Every artefact traceable to a source commit

**Next:** Step 5.

**Role output contracts:** `release-engineer:2`.

- **`handoff_release_provenance`**: For release manifest with signed provenance, supply the actual versioned release provenance record, including manifest_revision, artifacts, source_commits, signatures, target_scope. Independently assess the evidence against this exact criterion: Every artefact traceable to a source commit. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `manifest_revision`, `artifacts`, `source_commits`, `signatures`, `target_scope`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `normal/infrastructure-as-code`.

**Producer:** `release-engineer`; **receiver:** `change-manager`.

**Receiving condition:** Every artefact traceable to a source commit

**Next:** Step 5.

**Role output contracts:** `release-engineer:2`.

- **`handoff_release_provenance`**: For release manifest with signed provenance, supply the actual versioned release provenance record, including manifest_revision, artifacts, source_commits, signatures, target_scope. Independently assess the evidence against this exact criterion: Every artefact traceable to a source commit. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `manifest_revision`, `artifacts`, `source_commits`, `signatures`, `target_scope`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `normal/configuration`.

**Producer:** `engagement:release-control-owner`; **receiver:** `change-manager`.

**Receiving condition:** Every applied setting/version is traceable to the exact reviewed configuration baseline and change, with attributable verification provenance.

**Next:** Step 5.

**Role output contracts:** `release-engineer:2`.

- **`handoff_configuration_release_manifest`**: Every applied setting/version is traceable to the exact reviewed configuration baseline and change, with attributable verification provenance.
  Required fields: `manifest_revision`, `configuration_versions`, `source_baseline`, `change_identity`, `verification_provenance`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `emergency/application`.

**Producer:** `release-engineer`; **receiver:** `change-manager`.

**Receiving condition:** Every artefact traceable to a source commit

**Next:** Step 5.

**Role output contracts:** `release-engineer:2`.

- **`handoff_release_provenance`**: For release manifest with signed provenance, supply the actual versioned release provenance record, including manifest_revision, artifacts, source_commits, signatures, target_scope. Independently assess the evidence against this exact criterion: Every artefact traceable to a source commit. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `manifest_revision`, `artifacts`, `source_commits`, `signatures`, `target_scope`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `emergency/infrastructure-as-code`.

**Producer:** `release-engineer`; **receiver:** `change-manager`.

**Receiving condition:** Every artefact traceable to a source commit

**Next:** Step 5.

**Role output contracts:** `release-engineer:2`.

- **`handoff_release_provenance`**: For release manifest with signed provenance, supply the actual versioned release provenance record, including manifest_revision, artifacts, source_commits, signatures, target_scope. Independently assess the evidence against this exact criterion: Every artefact traceable to a source commit. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `manifest_revision`, `artifacts`, `source_commits`, `signatures`, `target_scope`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `emergency/configuration`.

**Producer:** `engagement:release-control-owner`; **receiver:** `change-manager`.

**Receiving condition:** Every applied setting/version is traceable to the exact reviewed configuration baseline and change, with attributable verification provenance.

**Next:** Step 5.

**Role output contracts:** `release-engineer:2`.

- **`handoff_configuration_release_manifest`**: Every applied setting/version is traceable to the exact reviewed configuration baseline and change, with attributable verification provenance.
  Required fields: `manifest_revision`, `configuration_versions`, `source_baseline`, `change_identity`, `verification_provenance`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-production-change-5"></a>

## change record and schedule slot

**Handoff content contract:** `handoff/production-change:5`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_change_record`**: For change record and schedule slot, supply the actual versioned change record record, including change_id, risk_class, authorisation_ref, schedule, preauthorisation_basis, measurement. Independently assess the evidence against this exact criterion: Standard changes pre-authorised and measured, not queued for ceremony. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `change_id`, `risk_class`, `authorisation_ref`, `schedule`, `preauthorisation_basis`, `measurement`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `standard/application`.

**Producer:** `change-manager`; **receiver:** `gitops-and-continuous-delivery-engineer`.

**Receiving condition:** Standard changes pre-authorised and measured, not queued for ceremony

**Next:** Step 6.

**Role output contracts:** `change-manager:1`, `change-manager:2`.

- **`handoff_change_record`**: For change record and schedule slot, supply the actual versioned change record record, including change_id, risk_class, authorisation_ref, schedule, preauthorisation_basis, measurement. Independently assess the evidence against this exact criterion: Standard changes pre-authorised and measured, not queued for ceremony. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `change_id`, `risk_class`, `authorisation_ref`, `schedule`, `preauthorisation_basis`, `measurement`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `standard/infrastructure-as-code`.

**Producer:** `change-manager`; **receiver:** `gitops-and-continuous-delivery-engineer`.

**Receiving condition:** Standard changes pre-authorised and measured, not queued for ceremony

**Next:** Step 6.

**Role output contracts:** `change-manager:1`, `change-manager:2`.

- **`handoff_change_record`**: For change record and schedule slot, supply the actual versioned change record record, including change_id, risk_class, authorisation_ref, schedule, preauthorisation_basis, measurement. Independently assess the evidence against this exact criterion: Standard changes pre-authorised and measured, not queued for ceremony. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `change_id`, `risk_class`, `authorisation_ref`, `schedule`, `preauthorisation_basis`, `measurement`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `standard/configuration`.

**Producer:** `change-manager`; **receiver:** `engagement:configuration-execution-owner`.

**Receiving condition:** Standard changes pre-authorised and measured, not queued for ceremony

**Next:** Step 6.

**Role output contracts:** `change-manager:1`, `change-manager:2`.

- **`handoff_change_record`**: For change record and schedule slot, supply the actual versioned change record record, including change_id, risk_class, authorisation_ref, schedule, preauthorisation_basis, measurement. Independently assess the evidence against this exact criterion: Standard changes pre-authorised and measured, not queued for ceremony. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `change_id`, `risk_class`, `authorisation_ref`, `schedule`, `preauthorisation_basis`, `measurement`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `normal/application`.

**Producer:** `change-manager`; **receiver:** `gitops-and-continuous-delivery-engineer`.

**Receiving condition:** Standard changes pre-authorised and measured, not queued for ceremony

**Next:** Step 6.

**Role output contracts:** `change-manager:1`, `change-manager:2`.

- **`handoff_change_record`**: For change record and schedule slot, supply the actual versioned change record record, including change_id, risk_class, authorisation_ref, schedule, preauthorisation_basis, measurement. Independently assess the evidence against this exact criterion: Standard changes pre-authorised and measured, not queued for ceremony. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `change_id`, `risk_class`, `authorisation_ref`, `schedule`, `preauthorisation_basis`, `measurement`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `normal/infrastructure-as-code`.

**Producer:** `change-manager`; **receiver:** `gitops-and-continuous-delivery-engineer`.

**Receiving condition:** Standard changes pre-authorised and measured, not queued for ceremony

**Next:** Step 6.

**Role output contracts:** `change-manager:1`, `change-manager:2`.

- **`handoff_change_record`**: For change record and schedule slot, supply the actual versioned change record record, including change_id, risk_class, authorisation_ref, schedule, preauthorisation_basis, measurement. Independently assess the evidence against this exact criterion: Standard changes pre-authorised and measured, not queued for ceremony. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `change_id`, `risk_class`, `authorisation_ref`, `schedule`, `preauthorisation_basis`, `measurement`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `normal/configuration`.

**Producer:** `change-manager`; **receiver:** `engagement:configuration-execution-owner`.

**Receiving condition:** Standard changes pre-authorised and measured, not queued for ceremony

**Next:** Step 6.

**Role output contracts:** `change-manager:1`, `change-manager:2`.

- **`handoff_change_record`**: For change record and schedule slot, supply the actual versioned change record record, including change_id, risk_class, authorisation_ref, schedule, preauthorisation_basis, measurement. Independently assess the evidence against this exact criterion: Standard changes pre-authorised and measured, not queued for ceremony. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `change_id`, `risk_class`, `authorisation_ref`, `schedule`, `preauthorisation_basis`, `measurement`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `emergency/application`.

**Producer:** `change-manager`; **receiver:** `gitops-and-continuous-delivery-engineer`.

**Receiving condition:** Standard changes pre-authorised and measured, not queued for ceremony

**Next:** Step 6.

**Role output contracts:** `change-manager:1`, `change-manager:2`.

- **`handoff_change_record`**: For change record and schedule slot, supply the actual versioned change record record, including change_id, risk_class, authorisation_ref, schedule, preauthorisation_basis, measurement. Independently assess the evidence against this exact criterion: Standard changes pre-authorised and measured, not queued for ceremony. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `change_id`, `risk_class`, `authorisation_ref`, `schedule`, `preauthorisation_basis`, `measurement`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `emergency/infrastructure-as-code`.

**Producer:** `change-manager`; **receiver:** `gitops-and-continuous-delivery-engineer`.

**Receiving condition:** Standard changes pre-authorised and measured, not queued for ceremony

**Next:** Step 6.

**Role output contracts:** `change-manager:1`, `change-manager:2`.

- **`handoff_change_record`**: For change record and schedule slot, supply the actual versioned change record record, including change_id, risk_class, authorisation_ref, schedule, preauthorisation_basis, measurement. Independently assess the evidence against this exact criterion: Standard changes pre-authorised and measured, not queued for ceremony. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `change_id`, `risk_class`, `authorisation_ref`, `schedule`, `preauthorisation_basis`, `measurement`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `emergency/configuration`.

**Producer:** `change-manager`; **receiver:** `engagement:configuration-execution-owner`.

**Receiving condition:** Standard changes pre-authorised and measured, not queued for ceremony

**Next:** Step 6.

**Role output contracts:** `change-manager:1`, `change-manager:2`.

- **`handoff_change_record`**: For change record and schedule slot, supply the actual versioned change record record, including change_id, risk_class, authorisation_ref, schedule, preauthorisation_basis, measurement. Independently assess the evidence against this exact criterion: Standard changes pre-authorised and measured, not queued for ceremony. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `change_id`, `risk_class`, `authorisation_ref`, `schedule`, `preauthorisation_basis`, `measurement`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-production-change-6"></a>

## rollout with automatic reversal armed

**Handoff content contract:** `handoff/production-change:6`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_rollout_readiness`**: For rollout with automatic reversal armed, supply the actual versioned rollout readiness record, including artifact_revision, rollout_steps, reversal_triggers, rehearsal_evidence, permitted_scope. Independently assess the evidence against this exact criterion: Rollback exercised, not merely documented. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `artifact_revision`, `rollout_steps`, `reversal_triggers`, `rehearsal_evidence`, `permitted_scope`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `standard/application`.

**Producer:** `gitops-and-continuous-delivery-engineer`; **receiver:** `site-reliability-engineer`.

**Receiving condition:** Rollback exercised, not merely documented

**Next:** Step 7.

**Role output contracts:** `gitops-and-continuous-delivery-engineer:3`, `gitops-and-continuous-delivery-engineer:4`.

- **`handoff_rollout_readiness`**: For rollout with automatic reversal armed, supply the actual versioned rollout readiness record, including artifact_revision, rollout_steps, reversal_triggers, rehearsal_evidence, permitted_scope. Independently assess the evidence against this exact criterion: Rollback exercised, not merely documented. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `artifact_revision`, `rollout_steps`, `reversal_triggers`, `rehearsal_evidence`, `permitted_scope`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `standard/infrastructure-as-code`.

**Producer:** `gitops-and-continuous-delivery-engineer`; **receiver:** `site-reliability-engineer`.

**Receiving condition:** Rollback exercised, not merely documented

**Next:** Step 7.

**Role output contracts:** `gitops-and-continuous-delivery-engineer:3`, `gitops-and-continuous-delivery-engineer:4`.

- **`handoff_rollout_readiness`**: For rollout with automatic reversal armed, supply the actual versioned rollout readiness record, including artifact_revision, rollout_steps, reversal_triggers, rehearsal_evidence, permitted_scope. Independently assess the evidence against this exact criterion: Rollback exercised, not merely documented. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `artifact_revision`, `rollout_steps`, `reversal_triggers`, `rehearsal_evidence`, `permitted_scope`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `standard/configuration`.

**Producer:** `engagement:configuration-execution-owner`; **receiver:** `site-reliability-engineer`.

**Receiving condition:** The authorised settings rollout has observed health criteria and an exercised reversal or explicitly authorised forward-recovery path.

**Next:** Step 7.

**Role output contracts:** `release-engineer:4`.

- **`handoff_controlled_configuration_rollout`**: The authorised settings rollout has observed health criteria and an exercised reversal or explicitly authorised forward-recovery path.
  Required fields: `approved_change`, `configuration_revision`, `execution_steps`, `health_thresholds`, `reversal_triggers`, `recovery_evidence`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `normal/application`.

**Producer:** `gitops-and-continuous-delivery-engineer`; **receiver:** `site-reliability-engineer`.

**Receiving condition:** Rollback exercised, not merely documented

**Next:** Step 7.

**Role output contracts:** `gitops-and-continuous-delivery-engineer:3`, `gitops-and-continuous-delivery-engineer:4`.

- **`handoff_rollout_readiness`**: For rollout with automatic reversal armed, supply the actual versioned rollout readiness record, including artifact_revision, rollout_steps, reversal_triggers, rehearsal_evidence, permitted_scope. Independently assess the evidence against this exact criterion: Rollback exercised, not merely documented. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `artifact_revision`, `rollout_steps`, `reversal_triggers`, `rehearsal_evidence`, `permitted_scope`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `normal/infrastructure-as-code`.

**Producer:** `gitops-and-continuous-delivery-engineer`; **receiver:** `site-reliability-engineer`.

**Receiving condition:** Rollback exercised, not merely documented

**Next:** Step 7.

**Role output contracts:** `gitops-and-continuous-delivery-engineer:3`, `gitops-and-continuous-delivery-engineer:4`.

- **`handoff_rollout_readiness`**: For rollout with automatic reversal armed, supply the actual versioned rollout readiness record, including artifact_revision, rollout_steps, reversal_triggers, rehearsal_evidence, permitted_scope. Independently assess the evidence against this exact criterion: Rollback exercised, not merely documented. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `artifact_revision`, `rollout_steps`, `reversal_triggers`, `rehearsal_evidence`, `permitted_scope`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `normal/configuration`.

**Producer:** `engagement:configuration-execution-owner`; **receiver:** `site-reliability-engineer`.

**Receiving condition:** The authorised settings rollout has observed health criteria and an exercised reversal or explicitly authorised forward-recovery path.

**Next:** Step 7.

**Role output contracts:** `release-engineer:4`.

- **`handoff_controlled_configuration_rollout`**: The authorised settings rollout has observed health criteria and an exercised reversal or explicitly authorised forward-recovery path.
  Required fields: `approved_change`, `configuration_revision`, `execution_steps`, `health_thresholds`, `reversal_triggers`, `recovery_evidence`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `emergency/application`.

**Producer:** `gitops-and-continuous-delivery-engineer`; **receiver:** `site-reliability-engineer`.

**Receiving condition:** Rollback exercised, not merely documented

**Next:** Step 7.

**Role output contracts:** `gitops-and-continuous-delivery-engineer:3`, `gitops-and-continuous-delivery-engineer:4`.

- **`handoff_rollout_readiness`**: For rollout with automatic reversal armed, supply the actual versioned rollout readiness record, including artifact_revision, rollout_steps, reversal_triggers, rehearsal_evidence, permitted_scope. Independently assess the evidence against this exact criterion: Rollback exercised, not merely documented. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `artifact_revision`, `rollout_steps`, `reversal_triggers`, `rehearsal_evidence`, `permitted_scope`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `emergency/infrastructure-as-code`.

**Producer:** `gitops-and-continuous-delivery-engineer`; **receiver:** `site-reliability-engineer`.

**Receiving condition:** Rollback exercised, not merely documented

**Next:** Step 7.

**Role output contracts:** `gitops-and-continuous-delivery-engineer:3`, `gitops-and-continuous-delivery-engineer:4`.

- **`handoff_rollout_readiness`**: For rollout with automatic reversal armed, supply the actual versioned rollout readiness record, including artifact_revision, rollout_steps, reversal_triggers, rehearsal_evidence, permitted_scope. Independently assess the evidence against this exact criterion: Rollback exercised, not merely documented. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `artifact_revision`, `rollout_steps`, `reversal_triggers`, `rehearsal_evidence`, `permitted_scope`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `emergency/configuration`.

**Producer:** `engagement:configuration-execution-owner`; **receiver:** `site-reliability-engineer`.

**Receiving condition:** The authorised settings rollout has observed health criteria and an exercised reversal or explicitly authorised forward-recovery path.

**Next:** Step 7.

**Role output contracts:** `release-engineer:4`.

- **`handoff_controlled_configuration_rollout`**: The authorised settings rollout has observed health criteria and an exercised reversal or explicitly authorised forward-recovery path.
  Required fields: `approved_change`, `configuration_revision`, `execution_steps`, `health_thresholds`, `reversal_triggers`, `recovery_evidence`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-production-change-7"></a>

## post-release confirmation or a reversal decision

**Handoff content contract:** `handoff/production-change:7`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_release_health_decision`**: For post-release confirmation or a reversal decision, supply the actual versioned release health decision record, including observation_window, signals, thresholds, decision, actual_reversal_evidence. Independently assess the evidence against this exact criterion: Reversal executed on trigger, not on debate. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `observation_window`, `signals`, `thresholds`, `decision`, `actual_reversal_evidence`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `standard/application`.

**Producer:** `site-reliability-engineer`; **receiver:** `configuration-manager`.

**Receiving condition:** Reversal executed on trigger, not on debate

**Next:** Step 8.

**Role output contracts:** `site-reliability-engineer:1`, `site-reliability-engineer:3`.

- **`handoff_release_health_decision`**: For post-release confirmation or a reversal decision, supply the actual versioned release health decision record, including observation_window, signals, thresholds, decision, actual_reversal_evidence. Independently assess the evidence against this exact criterion: Reversal executed on trigger, not on debate. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `observation_window`, `signals`, `thresholds`, `decision`, `actual_reversal_evidence`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `standard/infrastructure-as-code`.

**Producer:** `site-reliability-engineer`; **receiver:** `configuration-manager`.

**Receiving condition:** Reversal executed on trigger, not on debate

**Next:** Step 8.

**Role output contracts:** `site-reliability-engineer:1`, `site-reliability-engineer:3`.

- **`handoff_release_health_decision`**: For post-release confirmation or a reversal decision, supply the actual versioned release health decision record, including observation_window, signals, thresholds, decision, actual_reversal_evidence. Independently assess the evidence against this exact criterion: Reversal executed on trigger, not on debate. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `observation_window`, `signals`, `thresholds`, `decision`, `actual_reversal_evidence`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `standard/configuration`.

**Producer:** `site-reliability-engineer`; **receiver:** `configuration-manager`.

**Receiving condition:** Reversal executed on trigger, not on debate

**Next:** Step 8.

**Role output contracts:** `site-reliability-engineer:1`, `site-reliability-engineer:3`.

- **`handoff_release_health_decision`**: For post-release confirmation or a reversal decision, supply the actual versioned release health decision record, including observation_window, signals, thresholds, decision, actual_reversal_evidence. Independently assess the evidence against this exact criterion: Reversal executed on trigger, not on debate. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `observation_window`, `signals`, `thresholds`, `decision`, `actual_reversal_evidence`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `normal/application`.

**Producer:** `site-reliability-engineer`; **receiver:** `configuration-manager`.

**Receiving condition:** Reversal executed on trigger, not on debate

**Next:** Step 8.

**Role output contracts:** `site-reliability-engineer:1`, `site-reliability-engineer:3`.

- **`handoff_release_health_decision`**: For post-release confirmation or a reversal decision, supply the actual versioned release health decision record, including observation_window, signals, thresholds, decision, actual_reversal_evidence. Independently assess the evidence against this exact criterion: Reversal executed on trigger, not on debate. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `observation_window`, `signals`, `thresholds`, `decision`, `actual_reversal_evidence`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `normal/infrastructure-as-code`.

**Producer:** `site-reliability-engineer`; **receiver:** `configuration-manager`.

**Receiving condition:** Reversal executed on trigger, not on debate

**Next:** Step 8.

**Role output contracts:** `site-reliability-engineer:1`, `site-reliability-engineer:3`.

- **`handoff_release_health_decision`**: For post-release confirmation or a reversal decision, supply the actual versioned release health decision record, including observation_window, signals, thresholds, decision, actual_reversal_evidence. Independently assess the evidence against this exact criterion: Reversal executed on trigger, not on debate. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `observation_window`, `signals`, `thresholds`, `decision`, `actual_reversal_evidence`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `normal/configuration`.

**Producer:** `site-reliability-engineer`; **receiver:** `configuration-manager`.

**Receiving condition:** Reversal executed on trigger, not on debate

**Next:** Step 8.

**Role output contracts:** `site-reliability-engineer:1`, `site-reliability-engineer:3`.

- **`handoff_release_health_decision`**: For post-release confirmation or a reversal decision, supply the actual versioned release health decision record, including observation_window, signals, thresholds, decision, actual_reversal_evidence. Independently assess the evidence against this exact criterion: Reversal executed on trigger, not on debate. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `observation_window`, `signals`, `thresholds`, `decision`, `actual_reversal_evidence`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `emergency/application`.

**Producer:** `site-reliability-engineer`; **receiver:** `configuration-manager`.

**Receiving condition:** Reversal executed on trigger, not on debate

**Next:** Step 8.

**Role output contracts:** `site-reliability-engineer:1`, `site-reliability-engineer:3`.

- **`handoff_release_health_decision`**: For post-release confirmation or a reversal decision, supply the actual versioned release health decision record, including observation_window, signals, thresholds, decision, actual_reversal_evidence. Independently assess the evidence against this exact criterion: Reversal executed on trigger, not on debate. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `observation_window`, `signals`, `thresholds`, `decision`, `actual_reversal_evidence`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `emergency/infrastructure-as-code`.

**Producer:** `site-reliability-engineer`; **receiver:** `configuration-manager`.

**Receiving condition:** Reversal executed on trigger, not on debate

**Next:** Step 8.

**Role output contracts:** `site-reliability-engineer:1`, `site-reliability-engineer:3`.

- **`handoff_release_health_decision`**: For post-release confirmation or a reversal decision, supply the actual versioned release health decision record, including observation_window, signals, thresholds, decision, actual_reversal_evidence. Independently assess the evidence against this exact criterion: Reversal executed on trigger, not on debate. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `observation_window`, `signals`, `thresholds`, `decision`, `actual_reversal_evidence`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `emergency/configuration`.

**Producer:** `site-reliability-engineer`; **receiver:** `configuration-manager`.

**Receiving condition:** Reversal executed on trigger, not on debate

**Next:** Step 8.

**Role output contracts:** `site-reliability-engineer:1`, `site-reliability-engineer:3`.

- **`handoff_release_health_decision`**: For post-release confirmation or a reversal decision, supply the actual versioned release health decision record, including observation_window, signals, thresholds, decision, actual_reversal_evidence. Independently assess the evidence against this exact criterion: Reversal executed on trigger, not on debate. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `observation_window`, `signals`, `thresholds`, `decision`, `actual_reversal_evidence`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-production-change-8"></a>

## updated configuration items

**Handoff content contract:** `handoff/production-change:8`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_configuration_reconciliation`**: For updated configuration items, supply the actual versioned configuration reconciliation record, including changed_assets, actual_revision, record_revision, effective_date, reconciliation_gaps. Independently assess the evidence against this exact criterion: Record updated the same day the change lands. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `changed_assets`, `actual_revision`, `record_revision`, `effective_date`, `reconciliation_gaps`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `standard/application`.

**Producer:** `configuration-manager`; **receiver:** `engagement:named-authority`.

**Receiving condition:** Record updated the same day the change lands

**Next:** Terminal disposition; no downstream step.

**Role output contracts:** `configuration-manager:1`, `configuration-manager:3`.

- **`handoff_configuration_reconciliation`**: For updated configuration items, supply the actual versioned configuration reconciliation record, including changed_assets, actual_revision, record_revision, effective_date, reconciliation_gaps. Independently assess the evidence against this exact criterion: Record updated the same day the change lands. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `changed_assets`, `actual_revision`, `record_revision`, `effective_date`, `reconciliation_gaps`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `standard/infrastructure-as-code`.

**Producer:** `configuration-manager`; **receiver:** `engagement:named-authority`.

**Receiving condition:** Record updated the same day the change lands

**Next:** Terminal disposition; no downstream step.

**Role output contracts:** `configuration-manager:1`, `configuration-manager:3`.

- **`handoff_configuration_reconciliation`**: For updated configuration items, supply the actual versioned configuration reconciliation record, including changed_assets, actual_revision, record_revision, effective_date, reconciliation_gaps. Independently assess the evidence against this exact criterion: Record updated the same day the change lands. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `changed_assets`, `actual_revision`, `record_revision`, `effective_date`, `reconciliation_gaps`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `standard/configuration`.

**Producer:** `configuration-manager`; **receiver:** `engagement:named-authority`.

**Receiving condition:** Record updated the same day the change lands

**Next:** Terminal disposition; no downstream step.

**Role output contracts:** `configuration-manager:1`, `configuration-manager:3`.

- **`handoff_configuration_reconciliation`**: For updated configuration items, supply the actual versioned configuration reconciliation record, including changed_assets, actual_revision, record_revision, effective_date, reconciliation_gaps. Independently assess the evidence against this exact criterion: Record updated the same day the change lands. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `changed_assets`, `actual_revision`, `record_revision`, `effective_date`, `reconciliation_gaps`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `normal/application`.

**Producer:** `configuration-manager`; **receiver:** `engagement:named-authority`.

**Receiving condition:** Record updated the same day the change lands

**Next:** Terminal disposition; no downstream step.

**Role output contracts:** `configuration-manager:1`, `configuration-manager:3`.

- **`handoff_configuration_reconciliation`**: For updated configuration items, supply the actual versioned configuration reconciliation record, including changed_assets, actual_revision, record_revision, effective_date, reconciliation_gaps. Independently assess the evidence against this exact criterion: Record updated the same day the change lands. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `changed_assets`, `actual_revision`, `record_revision`, `effective_date`, `reconciliation_gaps`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `normal/infrastructure-as-code`.

**Producer:** `configuration-manager`; **receiver:** `engagement:named-authority`.

**Receiving condition:** Record updated the same day the change lands

**Next:** Terminal disposition; no downstream step.

**Role output contracts:** `configuration-manager:1`, `configuration-manager:3`.

- **`handoff_configuration_reconciliation`**: For updated configuration items, supply the actual versioned configuration reconciliation record, including changed_assets, actual_revision, record_revision, effective_date, reconciliation_gaps. Independently assess the evidence against this exact criterion: Record updated the same day the change lands. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `changed_assets`, `actual_revision`, `record_revision`, `effective_date`, `reconciliation_gaps`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `normal/configuration`.

**Producer:** `configuration-manager`; **receiver:** `engagement:named-authority`.

**Receiving condition:** Record updated the same day the change lands

**Next:** Terminal disposition; no downstream step.

**Role output contracts:** `configuration-manager:1`, `configuration-manager:3`.

- **`handoff_configuration_reconciliation`**: For updated configuration items, supply the actual versioned configuration reconciliation record, including changed_assets, actual_revision, record_revision, effective_date, reconciliation_gaps. Independently assess the evidence against this exact criterion: Record updated the same day the change lands. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `changed_assets`, `actual_revision`, `record_revision`, `effective_date`, `reconciliation_gaps`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `emergency/application`.

**Producer:** `configuration-manager`; **receiver:** `engagement:named-authority`.

**Receiving condition:** Record updated the same day the change lands

**Next:** Terminal disposition; no downstream step.

**Role output contracts:** `configuration-manager:1`, `configuration-manager:3`.

- **`handoff_configuration_reconciliation`**: For updated configuration items, supply the actual versioned configuration reconciliation record, including changed_assets, actual_revision, record_revision, effective_date, reconciliation_gaps. Independently assess the evidence against this exact criterion: Record updated the same day the change lands. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `changed_assets`, `actual_revision`, `record_revision`, `effective_date`, `reconciliation_gaps`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `emergency/infrastructure-as-code`.

**Producer:** `configuration-manager`; **receiver:** `engagement:named-authority`.

**Receiving condition:** Record updated the same day the change lands

**Next:** Terminal disposition; no downstream step.

**Role output contracts:** `configuration-manager:1`, `configuration-manager:3`.

- **`handoff_configuration_reconciliation`**: For updated configuration items, supply the actual versioned configuration reconciliation record, including changed_assets, actual_revision, record_revision, effective_date, reconciliation_gaps. Independently assess the evidence against this exact criterion: Record updated the same day the change lands. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `changed_assets`, `actual_revision`, `record_revision`, `effective_date`, `reconciliation_gaps`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `emergency/configuration`.

**Producer:** `configuration-manager`; **receiver:** `engagement:named-authority`.

**Receiving condition:** Record updated the same day the change lands

**Next:** Terminal disposition; no downstream step.

**Role output contracts:** `configuration-manager:1`, `configuration-manager:3`.

- **`handoff_configuration_reconciliation`**: For updated configuration items, supply the actual versioned configuration reconciliation record, including changed_assets, actual_revision, record_revision, effective_date, reconciliation_gaps. Independently assess the evidence against this exact criterion: Record updated the same day the change lands. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `changed_assets`, `actual_revision`, `record_revision`, `effective_date`, `reconciliation_gaps`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.
<!-- JAI:OUTPUT-CONTRACTS:END -->
