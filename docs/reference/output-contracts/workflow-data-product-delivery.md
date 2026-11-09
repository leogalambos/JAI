<!-- JAI:OUTPUT-CONTRACTS:START -->
# Data product delivery: source-owned handoff contracts

[Catalogue](index.md)

<a id="output-handoff-data-product-delivery-1"></a>

## governed element definitions

**Handoff content contract:** `handoff/data-product-delivery:1`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_governed_data_definitions`**: For governed element definitions, supply the actual versioned governed data definitions record, including element_ids, definitions, owner, steward, quality_tolerances. Independently assess the evidence against this exact criterion: Owner, steward, definition and quality tolerance exist. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `element_ids`, `definitions`, `owner`, `steward`, `quality_tolerances`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `nonpersonal`.

**Producer:** `data-governance-lead`; **receiver:** `engagement:data-use-classification-owner`.

**Receiving condition:** Owner, steward, definition and quality tolerance exist

**Next:** Step 2.

**Role output contracts:** `data-governance-lead:1`, `data-governance-lead:2`.

- **`handoff_governed_data_definitions`**: For governed element definitions, supply the actual versioned governed data definitions record, including element_ids, definitions, owner, steward, quality_tolerances. Independently assess the evidence against this exact criterion: Owner, steward, definition and quality tolerance exist. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `element_ids`, `definitions`, `owner`, `steward`, `quality_tolerances`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `personal-regulated`.

**Producer:** `data-governance-lead`; **receiver:** `data-protection-officer`.

**Receiving condition:** Owner, steward, definition and quality tolerance exist

**Next:** Step 2.

**Role output contracts:** `data-governance-lead:1`, `data-governance-lead:2`.

- **`handoff_governed_data_definitions`**: For governed element definitions, supply the actual versioned governed data definitions record, including element_ids, definitions, owner, steward, quality_tolerances. Independently assess the evidence against this exact criterion: Owner, steward, definition and quality tolerance exist. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `element_ids`, `definitions`, `owner`, `steward`, `quality_tolerances`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-data-product-delivery-2"></a>

## privacy position and DPIA where required

**Handoff content contract:** `handoff/data-product-delivery:2`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_data_privacy_position`**: For privacy position and DPIA where required, supply the actual versioned data privacy position record, including processing_scope, applicable_obligations, impact_assessment, lawful_basis, competent_review, timing. Independently assess the evidence against this exact criterion: DPIA completed before processing begins. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `processing_scope`, `applicable_obligations`, `impact_assessment`, `lawful_basis`, `competent_review`, `timing`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `nonpersonal`.

**Producer:** `engagement:data-use-classification-owner`; **receiver:** `data-architect`.

**Receiving condition:** Evidence establishes that this bounded scope contains no personal data; identify permitted use and any other applicable obligations without inventing a privacy legal basis or DPIA. Changed classification returns to competent privacy review.

**Next:** Step 3.

**Role output contracts:** `data-owner:1`, `data-steward:4`.

- **`handoff_nonpersonal_data_use_classification`**: Evidence establishes that this bounded scope contains no personal data; identify permitted use and any other applicable obligations without inventing a privacy legal basis or DPIA. Changed classification returns to competent privacy review.
  Required fields: `data_scope`, `classification_evidence`, `personal_data_exclusion`, `permitted_purpose`, `accountable_owner`, `residual_obligations`, `review_trigger`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `personal-regulated`.

**Producer:** `data-protection-officer`; **receiver:** `data-architect`.

**Receiving condition:** DPIA completed before processing begins

**Next:** Step 3.

**Role output contracts:** `data-protection-officer:2`.

- **`handoff_data_privacy_position`**: For privacy position and DPIA where required, supply the actual versioned data privacy position record, including processing_scope, applicable_obligations, impact_assessment, lawful_basis, competent_review, timing. Independently assess the evidence against this exact criterion: DPIA completed before processing begins. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `processing_scope`, `applicable_obligations`, `impact_assessment`, `lawful_basis`, `competent_review`, `timing`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-data-product-delivery-3"></a>

## data model and flow design

**Handoff content contract:** `handoff/data-product-delivery:3`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_data_flow_design`**: For data model and flow design, supply the actual versioned data flow design record, including model_revision, domain_owners, flows, trust_jurisdiction_boundaries, boundary_controls. Independently assess the evidence against this exact criterion: Every flow crossing a trust or jurisdiction boundary has a control. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `model_revision`, `domain_owners`, `flows`, `trust_jurisdiction_boundaries`, `boundary_controls`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `nonpersonal`.

**Producer:** `data-architect`; **receiver:** `data-engineer`.

**Receiving condition:** Every flow crossing a trust or jurisdiction boundary has a control

**Next:** Step 4.

**Role output contracts:** `data-architect:1`, `data-architect:3`.

- **`handoff_data_flow_design`**: For data model and flow design, supply the actual versioned data flow design record, including model_revision, domain_owners, flows, trust_jurisdiction_boundaries, boundary_controls. Independently assess the evidence against this exact criterion: Every flow crossing a trust or jurisdiction boundary has a control. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `model_revision`, `domain_owners`, `flows`, `trust_jurisdiction_boundaries`, `boundary_controls`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `personal-regulated`.

**Producer:** `data-architect`; **receiver:** `data-engineer`.

**Receiving condition:** Every flow crossing a trust or jurisdiction boundary has a control

**Next:** Step 4.

**Role output contracts:** `data-architect:1`, `data-architect:3`.

- **`handoff_data_flow_design`**: For data model and flow design, supply the actual versioned data flow design record, including model_revision, domain_owners, flows, trust_jurisdiction_boundaries, boundary_controls. Independently assess the evidence against this exact criterion: Every flow crossing a trust or jurisdiction boundary has a control. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `model_revision`, `domain_owners`, `flows`, `trust_jurisdiction_boundaries`, `boundary_controls`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-data-product-delivery-4"></a>

## pipelines with freshness and completeness checks

**Handoff content contract:** `handoff/data-product-delivery:4`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_pipeline_results`**: For pipelines with freshness and completeness checks, supply the actual versioned pipeline results record, including pipeline_revision, sources, transformations, freshness_checks, completeness_checks, failure_signals. Independently assess the evidence against this exact criterion: Checks fail loudly rather than degrading silently. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `pipeline_revision`, `sources`, `transformations`, `freshness_checks`, `completeness_checks`, `failure_signals`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `nonpersonal`.

**Producer:** `data-engineer`; **receiver:** `analytics-engineer`.

**Receiving condition:** Checks fail loudly rather than degrading silently

**Next:** Step 5.

**Role output contracts:** `data-engineer:1`, `data-engineer:3`.

- **`handoff_pipeline_results`**: For pipelines with freshness and completeness checks, supply the actual versioned pipeline results record, including pipeline_revision, sources, transformations, freshness_checks, completeness_checks, failure_signals. Independently assess the evidence against this exact criterion: Checks fail loudly rather than degrading silently. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `pipeline_revision`, `sources`, `transformations`, `freshness_checks`, `completeness_checks`, `failure_signals`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `personal-regulated`.

**Producer:** `data-engineer`; **receiver:** `analytics-engineer`.

**Receiving condition:** Checks fail loudly rather than degrading silently

**Next:** Step 5.

**Role output contracts:** `data-engineer:1`, `data-engineer:3`.

- **`handoff_pipeline_results`**: For pipelines with freshness and completeness checks, supply the actual versioned pipeline results record, including pipeline_revision, sources, transformations, freshness_checks, completeness_checks, failure_signals. Independently assess the evidence against this exact criterion: Checks fail loudly rather than degrading silently. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `pipeline_revision`, `sources`, `transformations`, `freshness_checks`, `completeness_checks`, `failure_signals`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-data-product-delivery-5"></a>

## tested, documented models with lineage

**Handoff content contract:** `handoff/data-product-delivery:5`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_analytics_model_results`**: For tested, documented models with lineage, supply the actual versioned analytics model results record, including model_revision, metric_definitions, lineage, uniqueness_results, integrity_results, freshness_results. Independently assess the evidence against this exact criterion: Uniqueness, referential integrity and freshness tested. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `model_revision`, `metric_definitions`, `lineage`, `uniqueness_results`, `integrity_results`, `freshness_results`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `nonpersonal`.

**Producer:** `analytics-engineer`; **receiver:** `data-quality-analyst`.

**Receiving condition:** Uniqueness, referential integrity and freshness tested

**Next:** Step 6.

**Role output contracts:** `analytics-engineer:1`, `analytics-engineer:3`.

- **`handoff_analytics_model_results`**: For tested, documented models with lineage, supply the actual versioned analytics model results record, including model_revision, metric_definitions, lineage, uniqueness_results, integrity_results, freshness_results. Independently assess the evidence against this exact criterion: Uniqueness, referential integrity and freshness tested. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `model_revision`, `metric_definitions`, `lineage`, `uniqueness_results`, `integrity_results`, `freshness_results`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `personal-regulated`.

**Producer:** `analytics-engineer`; **receiver:** `data-quality-analyst`.

**Receiving condition:** Uniqueness, referential integrity and freshness tested

**Next:** Step 6.

**Role output contracts:** `analytics-engineer:1`, `analytics-engineer:3`.

- **`handoff_analytics_model_results`**: For tested, documented models with lineage, supply the actual versioned analytics model results record, including model_revision, metric_definitions, lineage, uniqueness_results, integrity_results, freshness_results. Independently assess the evidence against this exact criterion: Uniqueness, referential integrity and freshness tested. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `model_revision`, `metric_definitions`, `lineage`, `uniqueness_results`, `integrity_results`, `freshness_results`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-data-product-delivery-6"></a>

## quality measurement against tolerance

**Handoff content contract:** `handoff/data-product-delivery:6`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_data_quality_observations`**: For quality measurement against tolerance, supply the actual versioned data quality observations record, including population, quality_dimensions, measurements, tolerances, intended_use, fitness_conclusion. Independently assess the evidence against this exact criterion: No bare percentage without a fitness-for-purpose statement. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `population`, `quality_dimensions`, `measurements`, `tolerances`, `intended_use`, `fitness_conclusion`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `nonpersonal`.

**Producer:** `data-quality-analyst`; **receiver:** `business-intelligence-analyst`.

**Receiving condition:** No bare percentage without a fitness-for-purpose statement

**Next:** Step 7.

**Role output contracts:** `data-quality-analyst:1`.

- **`handoff_data_quality_observations`**: For quality measurement against tolerance, supply the actual versioned data quality observations record, including population, quality_dimensions, measurements, tolerances, intended_use, fitness_conclusion. Independently assess the evidence against this exact criterion: No bare percentage without a fitness-for-purpose statement. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `population`, `quality_dimensions`, `measurements`, `tolerances`, `intended_use`, `fitness_conclusion`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `personal-regulated`.

**Producer:** `data-quality-analyst`; **receiver:** `business-intelligence-analyst`.

**Receiving condition:** No bare percentage without a fitness-for-purpose statement

**Next:** Step 7.

**Role output contracts:** `data-quality-analyst:1`.

- **`handoff_data_quality_observations`**: For quality measurement against tolerance, supply the actual versioned data quality observations record, including population, quality_dimensions, measurements, tolerances, intended_use, fitness_conclusion. Independently assess the evidence against this exact criterion: No bare percentage without a fitness-for-purpose statement. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `population`, `quality_dimensions`, `measurements`, `tolerances`, `intended_use`, `fitness_conclusion`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-data-product-delivery-7"></a>

## dashboards on a single agreed metric definition

**Handoff content contract:** `handoff/data-product-delivery:7`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_metric_dashboard`**: For dashboards on a single agreed metric definition, supply the actual versioned metric dashboard record, including dashboard_revision, metric_definition_ref, source_query, measurement_period, discrepancies, actions. Independently assess the evidence against this exact criterion: Two dashboards may not disagree silently. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `dashboard_revision`, `metric_definition_ref`, `source_query`, `measurement_period`, `discrepancies`, `actions`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `nonpersonal`.

**Producer:** `business-intelligence-analyst`; **receiver:** `data-steward`.

**Receiving condition:** Two dashboards may not disagree silently

**Next:** Step 8.

**Role output contracts:** `business-intelligence-analyst:1`, `business-intelligence-analyst:2`.

- **`handoff_metric_dashboard`**: For dashboards on a single agreed metric definition, supply the actual versioned metric dashboard record, including dashboard_revision, metric_definition_ref, source_query, measurement_period, discrepancies, actions. Independently assess the evidence against this exact criterion: Two dashboards may not disagree silently. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `dashboard_revision`, `metric_definition_ref`, `source_query`, `measurement_period`, `discrepancies`, `actions`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `personal-regulated`.

**Producer:** `business-intelligence-analyst`; **receiver:** `data-steward`.

**Receiving condition:** Two dashboards may not disagree silently

**Next:** Step 8.

**Role output contracts:** `business-intelligence-analyst:1`, `business-intelligence-analyst:2`.

- **`handoff_metric_dashboard`**: For dashboards on a single agreed metric definition, supply the actual versioned metric dashboard record, including dashboard_revision, metric_definition_ref, source_query, measurement_period, discrepancies, actions. Independently assess the evidence against this exact criterion: Two dashboards may not disagree silently. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `dashboard_revision`, `metric_definition_ref`, `source_query`, `measurement_period`, `discrepancies`, `actions`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-data-product-delivery-8"></a>

## stewardship decisions and issue log

**Handoff content contract:** `handoff/data-product-delivery:8`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_stewardship_decisions`**: For stewardship decisions and issue log, supply the actual versioned stewardship decisions record, including issue_ids, disputed_definitions, affected_users, decision_owner, resolution, escalation. Independently assess the evidence against this exact criterion: Competing definitions escalated, not averaged. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `issue_ids`, `disputed_definitions`, `affected_users`, `decision_owner`, `resolution`, `escalation`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `nonpersonal`.

**Producer:** `data-steward`; **receiver:** `engagement:named-authority`.

**Receiving condition:** Competing definitions escalated, not averaged

**Next:** Terminal disposition; no downstream step.

**Role output contracts:** `data-steward:3`, `data-steward:4`.

- **`handoff_stewardship_decisions`**: For stewardship decisions and issue log, supply the actual versioned stewardship decisions record, including issue_ids, disputed_definitions, affected_users, decision_owner, resolution, escalation. Independently assess the evidence against this exact criterion: Competing definitions escalated, not averaged. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `issue_ids`, `disputed_definitions`, `affected_users`, `decision_owner`, `resolution`, `escalation`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `personal-regulated`.

**Producer:** `data-steward`; **receiver:** `engagement:named-authority`.

**Receiving condition:** Competing definitions escalated, not averaged

**Next:** Terminal disposition; no downstream step.

**Role output contracts:** `data-steward:3`, `data-steward:4`.

- **`handoff_stewardship_decisions`**: For stewardship decisions and issue log, supply the actual versioned stewardship decisions record, including issue_ids, disputed_definitions, affected_users, decision_owner, resolution, escalation. Independently assess the evidence against this exact criterion: Competing definitions escalated, not averaged. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `issue_ids`, `disputed_definitions`, `affected_users`, `decision_owner`, `resolution`, `escalation`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.
<!-- JAI:OUTPUT-CONTRACTS:END -->
