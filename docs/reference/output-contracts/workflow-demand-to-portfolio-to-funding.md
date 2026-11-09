<!-- JAI:OUTPUT-CONTRACTS:START -->
# Demand to portfolio to funding: source-owned handoff contracts

[Catalogue](index.md)

<a id="output-handoff-demand-to-portfolio-to-funding-1"></a>

## demand record

**Handoff content contract:** `handoff/demand-to-portfolio-to-funding:1`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_qualified_demand_record`**: For demand record, supply the actual versioned qualified demand record record, including demand_id, business_outcome, accountable_owner, source, urgency. Independently assess the evidence against this exact criterion: No anonymous or outcome-free demand enters prioritisation. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `demand_id`, `business_outcome`, `accountable_owner`, `source`, `urgency`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `discovery`.

**Producer:** `demand-and-intake-manager`; **receiver:** `demand-and-intake-manager`.

**Receiving condition:** No anonymous or outcome-free demand enters prioritisation

**Next:** Step 2.

**Role output contracts:** `demand-and-intake-manager:1`.

- **`handoff_qualified_demand_record`**: For demand record, supply the actual versioned qualified demand record record, including demand_id, business_outcome, accountable_owner, source, urgency. Independently assess the evidence against this exact criterion: No anonymous or outcome-free demand enters prioritisation. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `demand_id`, `business_outcome`, `accountable_owner`, `source`, `urgency`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `funding`.

**Producer:** `demand-and-intake-manager`; **receiver:** `demand-and-intake-manager`.

**Receiving condition:** No anonymous or outcome-free demand enters prioritisation

**Next:** Step 2.

**Role output contracts:** `demand-and-intake-manager:1`.

- **`handoff_qualified_demand_record`**: For demand record, supply the actual versioned qualified demand record record, including demand_id, business_outcome, accountable_owner, source, urgency. Independently assess the evidence against this exact criterion: No anonymous or outcome-free demand enters prioritisation. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `demand_id`, `business_outcome`, `accountable_owner`, `source`, `urgency`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-demand-to-portfolio-to-funding-2"></a>

## qualification assessment

**Handoff content contract:** `handoff/demand-to-portfolio-to-funding:2`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_demand_disposition`**: For qualification assessment, supply the actual versioned demand disposition record, including demand_ref, qualification_evidence, reject_redirect_discover_assess, decision_owner, rationale. Independently assess the evidence against this exact criterion: Disposition is explicit: reject, redirect, discover or assess. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `demand_ref`, `qualification_evidence`, `reject_redirect_discover_assess`, `decision_owner`, `rationale`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `discovery`.

**Producer:** `demand-and-intake-manager`; **receiver:** `engagement:named-authority`.

**Receiving condition:** Disposition is explicit: reject, redirect, discover or assess

**Next:** Terminal disposition; no downstream step.

**Role output contracts:** `demand-and-intake-manager:2`.

- **`handoff_demand_disposition`**: For qualification assessment, supply the actual versioned demand disposition record, including demand_ref, qualification_evidence, reject_redirect_discover_assess, decision_owner, rationale. Independently assess the evidence against this exact criterion: Disposition is explicit: reject, redirect, discover or assess. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `demand_ref`, `qualification_evidence`, `reject_redirect_discover_assess`, `decision_owner`, `rationale`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `funding`.

**Producer:** `demand-and-intake-manager`; **receiver:** `enterprise-architect`.

**Receiving condition:** Disposition is explicit: reject, redirect, discover or assess

**Next:** Step 3.

**Role output contracts:** `demand-and-intake-manager:2`.

- **`handoff_demand_disposition`**: For qualification assessment, supply the actual versioned demand disposition record, including demand_ref, qualification_evidence, reject_redirect_discover_assess, decision_owner, rationale. Independently assess the evidence against this exact criterion: Disposition is explicit: reject, redirect, discover or assess. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `demand_ref`, `qualification_evidence`, `reject_redirect_discover_assess`, `decision_owner`, `rationale`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-demand-to-portfolio-to-funding-3"></a>

## capability-fit assessment

**Handoff content contract:** `handoff/demand-to-portfolio-to-funding:3`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_capability_fit`**: For capability-fit assessment, supply the actual versioned capability fit record, including capability_baseline, reuse_options, service_fit, strategic_conflicts, evidence. Independently assess the evidence against this exact criterion: Existing capability/service reuse and strategic conflicts are explicit. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `capability_baseline`, `reuse_options`, `service_fit`, `strategic_conflicts`, `evidence`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `funding`.

**Producer:** `enterprise-architect`; **receiver:** `application-portfolio-manager`.

**Receiving condition:** Existing capability/service reuse and strategic conflicts are explicit

**Next:** Step 4.

**Role output contracts:** `enterprise-architect:1`.

- **`handoff_capability_fit`**: For capability-fit assessment, supply the actual versioned capability fit record, including capability_baseline, reuse_options, service_fit, strategic_conflicts, evidence. Independently assess the evidence against this exact criterion: Existing capability/service reuse and strategic conflicts are explicit. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `capability_baseline`, `reuse_options`, `service_fit`, `strategic_conflicts`, `evidence`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-demand-to-portfolio-to-funding-4"></a>

## application portfolio impact assessment

**Handoff content contract:** `handoff/demand-to-portfolio-to-funding:4`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_application_portfolio_impact`**: For application portfolio impact assessment, supply the actual versioned application portfolio impact record, including affected_applications, lifecycle_posture, duplication, dependencies, accountable_owners. Independently assess the evidence against this exact criterion: Impacted applications have an explicit lifecycle posture, duplication/dependency view and accountable owner. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `affected_applications`, `lifecycle_posture`, `duplication`, `dependencies`, `accountable_owners`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `funding`.

**Producer:** `application-portfolio-manager`; **receiver:** `solution-architect`.

**Receiving condition:** Impacted applications have an explicit lifecycle posture, duplication/dependency view and accountable owner

**Next:** Step 5.

**Role output contracts:** `application-portfolio-manager:1`, `application-portfolio-manager:2`.

- **`handoff_application_portfolio_impact`**: For application portfolio impact assessment, supply the actual versioned application portfolio impact record, including affected_applications, lifecycle_posture, duplication, dependencies, accountable_owners. Independently assess the evidence against this exact criterion: Impacted applications have an explicit lifecycle posture, duplication/dependency view and accountable owner. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `affected_applications`, `lifecycle_posture`, `duplication`, `dependencies`, `accountable_owners`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-demand-to-portfolio-to-funding-5"></a>

## architecture impact assessment

**Handoff content contract:** `handoff/demand-to-portfolio-to-funding:5`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_demand_architecture_impact`**: For architecture impact assessment, supply the actual versioned demand architecture impact record, including affected_domains, dependencies, constraints, options, owners. Independently assess the evidence against this exact criterion: Material cross-domain dependencies and constraints are identified. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `affected_domains`, `dependencies`, `constraints`, `options`, `owners`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `funding`.

**Producer:** `solution-architect`; **receiver:** `it-risk-manager`.

**Receiving condition:** Material cross-domain dependencies and constraints are identified

**Next:** Step 6.

**Role output contracts:** `solution-architect:1`.

- **`handoff_demand_architecture_impact`**: For architecture impact assessment, supply the actual versioned demand architecture impact record, including affected_domains, dependencies, constraints, options, owners. Independently assess the evidence against this exact criterion: Material cross-domain dependencies and constraints are identified. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `affected_domains`, `dependencies`, `constraints`, `options`, `owners`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-demand-to-portfolio-to-funding-6"></a>

## risk/value assessment

**Handoff content contract:** `handoff/demand-to-portfolio-to-funding:6`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_risk_value_assessment`**: For risk/value assessment, supply the actual versioned risk value assessment record, including risk_scenarios, regulatory_basis, incremental_value, urgency, uncertainty, double_count_checks. Independently assess the evidence against this exact criterion: Regulatory/risk urgency is evidence-based and not double-counted as value. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `risk_scenarios`, `regulatory_basis`, `incremental_value`, `urgency`, `uncertainty`, `double_count_checks`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `funding`.

**Producer:** `it-risk-manager`; **receiver:** `resource-manager`.

**Receiving condition:** Regulatory/risk urgency is evidence-based and not double-counted as value

**Next:** Step 7.

**Role output contracts:** `it-risk-manager:2`.

- **`handoff_risk_value_assessment`**: For risk/value assessment, supply the actual versioned risk value assessment record, including risk_scenarios, regulatory_basis, incremental_value, urgency, uncertainty, double_count_checks. Independently assess the evidence against this exact criterion: Regulatory/risk urgency is evidence-based and not double-counted as value. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `risk_scenarios`, `regulatory_basis`, `incremental_value`, `urgency`, `uncertainty`, `double_count_checks`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-demand-to-portfolio-to-funding-7"></a>

## estimate and capacity view

**Handoff content contract:** `handoff/demand-to-portfolio-to-funding:7`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_estimate_capacity`**: For estimate and capacity view, supply the actual versioned estimate capacity record, including work_scope, estimate_range, assumptions, constrained_skills, available_capacity, sources. Independently assess the evidence against this exact criterion: Uncertainty ranges and constrained skills/capacity are explicit. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `work_scope`, `estimate_range`, `assumptions`, `constrained_skills`, `available_capacity`, `sources`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `funding`.

**Producer:** `resource-manager`; **receiver:** `portfolio-manager`.

**Receiving condition:** Uncertainty ranges and constrained skills/capacity are explicit

**Next:** Step 8.

**Role output contracts:** `resource-manager:1`.

- **`handoff_estimate_capacity`**: For estimate and capacity view, supply the actual versioned estimate capacity record, including work_scope, estimate_range, assumptions, constrained_skills, available_capacity, sources. Independently assess the evidence against this exact criterion: Uncertainty ranges and constrained skills/capacity are explicit. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `work_scope`, `estimate_range`, `assumptions`, `constrained_skills`, `available_capacity`, `sources`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-demand-to-portfolio-to-funding-8"></a>

## prioritisation decision

**Handoff content contract:** `handoff/demand-to-portfolio-to-funding:8`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_portfolio_prioritisation`**: For prioritisation decision, supply the actual versioned portfolio prioritisation record, including candidate_set, declared_criteria, scoring_evidence, constraints, exceptions, decision_authority. Independently assess the evidence against this exact criterion: Prioritisation can be reconstructed from declared criteria and exceptions. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `candidate_set`, `declared_criteria`, `scoring_evidence`, `constraints`, `exceptions`, `decision_authority`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `funding`.

**Producer:** `portfolio-manager`; **receiver:** `it-financial-management-tbm-manager`.

**Receiving condition:** Prioritisation can be reconstructed from declared criteria and exceptions

**Next:** Step 9.

**Role output contracts:** `portfolio-manager:1`, `portfolio-manager:4`.

- **`handoff_portfolio_prioritisation`**: For prioritisation decision, supply the actual versioned portfolio prioritisation record, including candidate_set, declared_criteria, scoring_evidence, constraints, exceptions, decision_authority. Independently assess the evidence against this exact criterion: Prioritisation can be reconstructed from declared criteria and exceptions. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `candidate_set`, `declared_criteria`, `scoring_evidence`, `constraints`, `exceptions`, `decision_authority`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-demand-to-portfolio-to-funding-9"></a>

## funding economics and cost profile

**Handoff content contract:** `handoff/demand-to-portfolio-to-funding:9`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_funding_economics`**: For funding economics and cost profile, supply the actual versioned funding economics record, including cost_boundary, periods, currency, capex_opex, transition_costs, reconciliation. Independently assess the evidence against this exact criterion: Cost boundaries, CAPEX/OPEX and transition costs reconcile to the cost model. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `cost_boundary`, `periods`, `currency`, `capex_opex`, `transition_costs`, `reconciliation`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `funding`.

**Producer:** `it-financial-management-tbm-manager`; **receiver:** `portfolio-manager`.

**Receiving condition:** Cost boundaries, CAPEX/OPEX and transition costs reconcile to the cost model

**Next:** Step 10.

**Role output contracts:** `it-financial-management-tbm-manager:1`, `it-financial-management-tbm-manager:2`.

- **`handoff_funding_economics`**: For funding economics and cost profile, supply the actual versioned funding economics record, including cost_boundary, periods, currency, capex_opex, transition_costs, reconciliation. Independently assess the evidence against this exact criterion: Cost boundaries, CAPEX/OPEX and transition costs reconcile to the cost model. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `cost_boundary`, `periods`, `currency`, `capex_opex`, `transition_costs`, `reconciliation`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-demand-to-portfolio-to-funding-10"></a>

## portfolio commitment

**Handoff content contract:** `handoff/demand-to-portfolio-to-funding:10`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_portfolio_commitment`**: For portfolio commitment, supply the actual versioned portfolio commitment record, including approved_scope, authority, funding_basis, capacity_basis, conditions, review_trigger. Independently assess the evidence against this exact criterion: Commitment has authority, funding/capacity basis and review condition. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `approved_scope`, `authority`, `funding_basis`, `capacity_basis`, `conditions`, `review_trigger`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `funding`.

**Producer:** `portfolio-manager`; **receiver:** `engagement:named-authority`.

**Receiving condition:** Commitment has authority, funding/capacity basis and review condition

**Next:** Terminal disposition; no downstream step.

**Role output contracts:** `portfolio-manager:2`.

- **`handoff_portfolio_commitment`**: For portfolio commitment, supply the actual versioned portfolio commitment record, including approved_scope, authority, funding_basis, capacity_basis, conditions, review_trigger. Independently assess the evidence against this exact criterion: Commitment has authority, funding/capacity basis and review condition. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `approved_scope`, `authority`, `funding_basis`, `capacity_basis`, `conditions`, `review_trigger`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.
<!-- JAI:OUTPUT-CONTRACTS:END -->
