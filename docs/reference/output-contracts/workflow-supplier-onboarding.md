<!-- JAI:OUTPUT-CONTRACTS:START -->
# Supplier onboarding to exit: source-owned handoff contracts

[Catalogue](index.md)

<a id="output-handoff-supplier-onboarding-1"></a>

## tender, evaluation and recommendation

**Handoff content contract:** `handoff/supplier-onboarding:1`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_supplier_tender_evaluation`**: For tender, evaluation and recommendation, supply the actual versioned supplier tender evaluation record, including requirements, evaluation_criteria, responses, security_privacy_requirements, continuity_exit_requirements, recommendation. Independently assess the evidence against this exact criterion: Security, privacy, exit and continuity requirements in the tender, not added after. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `requirements`, `evaluation_criteria`, `responses`, `security_privacy_requirements`, `continuity_exit_requirements`, `recommendation`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `ordinary`.

**Producer:** `it-procurement-specialist`; **receiver:** `third-party-risk-manager`.

**Receiving condition:** Security, privacy, exit and continuity requirements in the tender, not added after

**Next:** Step 2.

**Role output contracts:** `it-procurement-specialist:1`, `it-procurement-specialist:2`, `it-procurement-specialist:3`.

- **`handoff_supplier_tender_evaluation`**: For tender, evaluation and recommendation, supply the actual versioned supplier tender evaluation record, including requirements, evaluation_criteria, responses, security_privacy_requirements, continuity_exit_requirements, recommendation. Independently assess the evidence against this exact criterion: Security, privacy, exit and continuity requirements in the tender, not added after. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `requirements`, `evaluation_criteria`, `responses`, `security_privacy_requirements`, `continuity_exit_requirements`, `recommendation`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `critical`.

**Producer:** `it-procurement-specialist`; **receiver:** `third-party-risk-manager`.

**Receiving condition:** Security, privacy, exit and continuity requirements in the tender, not added after

**Next:** Step 2.

**Role output contracts:** `it-procurement-specialist:1`, `it-procurement-specialist:2`, `it-procurement-specialist:3`.

- **`handoff_supplier_tender_evaluation`**: For tender, evaluation and recommendation, supply the actual versioned supplier tender evaluation record, including requirements, evaluation_criteria, responses, security_privacy_requirements, continuity_exit_requirements, recommendation. Independently assess the evidence against this exact criterion: Security, privacy, exit and continuity requirements in the tender, not added after. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `requirements`, `evaluation_criteria`, `responses`, `security_privacy_requirements`, `continuity_exit_requirements`, `recommendation`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-supplier-onboarding-2"></a>

## risk assessment and tier

**Handoff content contract:** `handoff/supplier-onboarding:2`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_supplier_risk_tier`**: For risk assessment and tier, supply the actual versioned supplier risk tier record, including supplier_id, criticality, dependencies, assessed_risks, exit_substitution_test, residual_disposition. Independently assess the evidence against this exact criterion: Critical suppliers have a tested exit or substitution plan. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `supplier_id`, `criticality`, `dependencies`, `assessed_risks`, `exit_substitution_test`, `residual_disposition`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `ordinary`.

**Producer:** `third-party-risk-manager`; **receiver:** `security-architect`.

**Receiving condition:** Evidence supports supplier criticality and proportionate continuity/exit treatment; a noncritical classification does not fabricate an exercised exit or waive an applicable obligation.

**Next:** Step 3.

**Role output contracts:** `third-party-risk-manager:1`.

- **`handoff_ordinary_supplier_risk`**: Evidence supports supplier criticality and proportionate continuity/exit treatment; a noncritical classification does not fabricate an exercised exit or waive an applicable obligation.
  Required fields: `supplier_id`, `criticality`, `classification_evidence`, `assessed_risks`, `continuity_exit_disposition`, `residual_owner`, `review_trigger`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `critical`.

**Producer:** `third-party-risk-manager`; **receiver:** `security-architect`.

**Receiving condition:** Critical suppliers have a tested exit or substitution plan

**Next:** Step 3.

**Role output contracts:** `third-party-risk-manager:1`.

- **`handoff_supplier_risk_tier`**: For risk assessment and tier, supply the actual versioned supplier risk tier record, including supplier_id, criticality, dependencies, assessed_risks, exit_substitution_test, residual_disposition. Independently assess the evidence against this exact criterion: Critical suppliers have a tested exit or substitution plan. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `supplier_id`, `criticality`, `dependencies`, `assessed_risks`, `exit_substitution_test`, `residual_disposition`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-supplier-onboarding-3"></a>

## supplier control requirements

**Handoff content contract:** `handoff/supplier-onboarding:3`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_supplier_security_requirements`**: For supplier control requirements, supply the actual versioned supplier security requirements record, including threats, business_risks, control_requirements, evidence_expectations, exception_owners. Independently assess the evidence against this exact criterion: Requirements traced to threats, not copied from a questionnaire. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `threats`, `business_risks`, `control_requirements`, `evidence_expectations`, `exception_owners`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `ordinary`.

**Producer:** `security-architect`; **receiver:** `contract-manager`.

**Receiving condition:** Requirements traced to threats, not copied from a questionnaire

**Next:** Step 4.

**Role output contracts:** `security-architect:4`.

- **`handoff_supplier_security_requirements`**: For supplier control requirements, supply the actual versioned supplier security requirements record, including threats, business_risks, control_requirements, evidence_expectations, exception_owners. Independently assess the evidence against this exact criterion: Requirements traced to threats, not copied from a questionnaire. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `threats`, `business_risks`, `control_requirements`, `evidence_expectations`, `exception_owners`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `critical`.

**Producer:** `security-architect`; **receiver:** `contract-manager`.

**Receiving condition:** Requirements traced to threats, not copied from a questionnaire

**Next:** Step 4.

**Role output contracts:** `security-architect:4`.

- **`handoff_supplier_security_requirements`**: For supplier control requirements, supply the actual versioned supplier security requirements record, including threats, business_risks, control_requirements, evidence_expectations, exception_owners. Independently assess the evidence against this exact criterion: Requirements traced to threats, not copied from a questionnaire. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `threats`, `business_risks`, `control_requirements`, `evidence_expectations`, `exception_owners`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-supplier-onboarding-4"></a>

## contract and obligation register

**Handoff content contract:** `handoff/supplier-onboarding:4`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_contract_obligations`**: For contract and obligation register, supply the actual versioned contract obligations record, including executed_version, parties, obligations, owners, measures, due_dates. Independently assess the evidence against this exact criterion: Obligations on both sides tracked with owners. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `executed_version`, `parties`, `obligations`, `owners`, `measures`, `due_dates`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `ordinary`.

**Producer:** `contract-manager`; **receiver:** `vendor-manager`.

**Receiving condition:** Obligations on both sides tracked with owners

**Next:** Step 5.

**Role output contracts:** `contract-manager:1`.

- **`handoff_contract_obligations`**: For contract and obligation register, supply the actual versioned contract obligations record, including executed_version, parties, obligations, owners, measures, due_dates. Independently assess the evidence against this exact criterion: Obligations on both sides tracked with owners. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `executed_version`, `parties`, `obligations`, `owners`, `measures`, `due_dates`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `critical`.

**Producer:** `contract-manager`; **receiver:** `vendor-manager`.

**Receiving condition:** Obligations on both sides tracked with owners

**Next:** Step 5.

**Role output contracts:** `contract-manager:1`.

- **`handoff_contract_obligations`**: For contract and obligation register, supply the actual versioned contract obligations record, including executed_version, parties, obligations, owners, measures, due_dates. Independently assess the evidence against this exact criterion: Obligations on both sides tracked with owners. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `executed_version`, `parties`, `obligations`, `owners`, `measures`, `due_dates`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-supplier-onboarding-5"></a>

## scorecards and governance cadence

**Handoff content contract:** `handoff/supplier-onboarding:5`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_vendor_governance`**: For scorecards and governance cadence, supply the actual versioned vendor governance record, including supplier_scorecard, measurement_sources, governance_cadence, renewal_deadline, viable_alternatives. Independently assess the evidence against this exact criterion: Renewal started early enough for a real alternative to exist. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `supplier_scorecard`, `measurement_sources`, `governance_cadence`, `renewal_deadline`, `viable_alternatives`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `ordinary`.

**Producer:** `vendor-manager`; **receiver:** `service-level-manager`.

**Receiving condition:** Renewal started early enough for a real alternative to exist

**Next:** Step 6.

**Role output contracts:** `vendor-manager:1`, `vendor-manager:2`.

- **`handoff_vendor_governance`**: For scorecards and governance cadence, supply the actual versioned vendor governance record, including supplier_scorecard, measurement_sources, governance_cadence, renewal_deadline, viable_alternatives. Independently assess the evidence against this exact criterion: Renewal started early enough for a real alternative to exist. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `supplier_scorecard`, `measurement_sources`, `governance_cadence`, `renewal_deadline`, `viable_alternatives`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `critical`.

**Producer:** `vendor-manager`; **receiver:** `service-level-manager`.

**Receiving condition:** Renewal started early enough for a real alternative to exist

**Next:** Step 6.

**Role output contracts:** `vendor-manager:1`, `vendor-manager:2`.

- **`handoff_vendor_governance`**: For scorecards and governance cadence, supply the actual versioned vendor governance record, including supplier_scorecard, measurement_sources, governance_cadence, renewal_deadline, viable_alternatives. Independently assess the evidence against this exact criterion: Renewal started early enough for a real alternative to exist. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `supplier_scorecard`, `measurement_sources`, `governance_cadence`, `renewal_deadline`, `viable_alternatives`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-supplier-onboarding-6"></a>

## aligned SLAs and OLAs

**Handoff content contract:** `handoff/supplier-onboarding:6`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_underpinned_service_levels`**: For aligned SLAs and OLAs, supply the actual versioned underpinned service levels record, including customer_commitments, supplier_commitments, internal_olas, coverage_gaps, accountable_owners. Independently assess the evidence against this exact criterion: No internal commitment exceeding what the supply chain can deliver. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `customer_commitments`, `supplier_commitments`, `internal_olas`, `coverage_gaps`, `accountable_owners`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `ordinary`.

**Producer:** `service-level-manager`; **receiver:** `business-continuity-manager`.

**Receiving condition:** No internal commitment exceeding what the supply chain can deliver

**Next:** Step 7.

**Role output contracts:** `service-level-manager:1`, `service-level-manager:4`.

- **`handoff_underpinned_service_levels`**: For aligned SLAs and OLAs, supply the actual versioned underpinned service levels record, including customer_commitments, supplier_commitments, internal_olas, coverage_gaps, accountable_owners. Independently assess the evidence against this exact criterion: No internal commitment exceeding what the supply chain can deliver. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `customer_commitments`, `supplier_commitments`, `internal_olas`, `coverage_gaps`, `accountable_owners`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `critical`.

**Producer:** `service-level-manager`; **receiver:** `business-continuity-manager`.

**Receiving condition:** No internal commitment exceeding what the supply chain can deliver

**Next:** Step 7.

**Role output contracts:** `service-level-manager:1`, `service-level-manager:4`.

- **`handoff_underpinned_service_levels`**: For aligned SLAs and OLAs, supply the actual versioned underpinned service levels record, including customer_commitments, supplier_commitments, internal_olas, coverage_gaps, accountable_owners. Independently assess the evidence against this exact criterion: No internal commitment exceeding what the supply chain can deliver. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `customer_commitments`, `supplier_commitments`, `internal_olas`, `coverage_gaps`, `accountable_owners`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-supplier-onboarding-7"></a>

## exercised continuity and exit plan

**Handoff content contract:** `handoff/supplier-onboarding:7`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_supplier_continuity_exercise`**: For exercised continuity and exit plan, supply the actual versioned supplier continuity exercise record, including exercise_scope, exit_steps, observed_results, recovery_objectives, unresolved_dependencies. Independently assess the evidence against this exact criterion: Exit tested, not described. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `exercise_scope`, `exit_steps`, `observed_results`, `recovery_objectives`, `unresolved_dependencies`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `ordinary`.

**Producer:** `business-continuity-manager`; **receiver:** `engagement:named-authority`.

**Receiving condition:** Exit tested, not described

**Next:** Terminal disposition; no downstream step.

**Role output contracts:** `business-continuity-manager:2`, `business-continuity-manager:3`.

- **`handoff_supplier_continuity_exercise`**: For exercised continuity and exit plan, supply the actual versioned supplier continuity exercise record, including exercise_scope, exit_steps, observed_results, recovery_objectives, unresolved_dependencies. Independently assess the evidence against this exact criterion: Exit tested, not described. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `exercise_scope`, `exit_steps`, `observed_results`, `recovery_objectives`, `unresolved_dependencies`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `critical`.

**Producer:** `business-continuity-manager`; **receiver:** `engagement:named-authority`.

**Receiving condition:** Exit tested, not described

**Next:** Terminal disposition; no downstream step.

**Role output contracts:** `business-continuity-manager:2`, `business-continuity-manager:3`.

- **`handoff_supplier_continuity_exercise`**: For exercised continuity and exit plan, supply the actual versioned supplier continuity exercise record, including exercise_scope, exit_steps, observed_results, recovery_objectives, unresolved_dependencies. Independently assess the evidence against this exact criterion: Exit tested, not described. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `exercise_scope`, `exit_steps`, `observed_results`, `recovery_objectives`, `unresolved_dependencies`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.
<!-- JAI:OUTPUT-CONTRACTS:END -->
