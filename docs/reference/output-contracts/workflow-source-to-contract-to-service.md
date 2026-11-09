<!-- JAI:OUTPUT-CONTRACTS:START -->
# Source to contract to service: source-owned handoff contracts

[Catalogue](index.md)

<a id="output-handoff-source-to-contract-to-service-1"></a>

## sourcing requirement baseline

**Handoff content contract:** `handoff/source-to-contract-to-service:1`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_sourcing_requirements`**: For sourcing requirement baseline, supply the actual versioned sourcing requirements record, including business_need, testable_requirements, acceptance_criteria, preferred_solution_constraints, sources. Independently assess the evidence against this exact criterion: Requirements are testable and distinguish need from preferred solution. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `business_need`, `testable_requirements`, `acceptance_criteria`, `preferred_solution_constraints`, `sources`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `competitive`.

**Producer:** `business-analyst`; **receiver:** `it-procurement-specialist`.

**Receiving condition:** Requirements are testable and distinguish need from preferred solution

**Next:** Step 2.

**Role output contracts:** `business-analyst:1`.

- **`handoff_sourcing_requirements`**: For sourcing requirement baseline, supply the actual versioned sourcing requirements record, including business_need, testable_requirements, acceptance_criteria, preferred_solution_constraints, sources. Independently assess the evidence against this exact criterion: Requirements are testable and distinguish need from preferred solution. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `business_need`, `testable_requirements`, `acceptance_criteria`, `preferred_solution_constraints`, `sources`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `direct-award`.

**Producer:** `business-analyst`; **receiver:** `it-procurement-specialist`.

**Receiving condition:** Requirements are testable and distinguish need from preferred solution

**Next:** Step 2.

**Role output contracts:** `business-analyst:1`.

- **`handoff_sourcing_requirements`**: For sourcing requirement baseline, supply the actual versioned sourcing requirements record, including business_need, testable_requirements, acceptance_criteria, preferred_solution_constraints, sources. Independently assess the evidence against this exact criterion: Requirements are testable and distinguish need from preferred solution. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `business_need`, `testable_requirements`, `acceptance_criteria`, `preferred_solution_constraints`, `sources`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-source-to-contract-to-service-2"></a>

## RFI/RFP pack and response evidence

**Handoff content contract:** `handoff/source-to-contract-to-service:2`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_procurement_comparison`**: For RFI/RFP pack and response evidence, supply the actual versioned procurement comparison record, including rfp_revision, evaluation_criteria, comparable_responses, evidence, procurement_rules. Independently assess the evidence against this exact criterion: Supplier responses are comparable and procurement rules are followed. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `rfp_revision`, `evaluation_criteria`, `comparable_responses`, `evidence`, `procurement_rules`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `competitive`.

**Producer:** `it-procurement-specialist`; **receiver:** `vendor-manager`.

**Receiving condition:** Supplier responses are comparable and procurement rules are followed

**Next:** Step 3.

**Role output contracts:** `it-procurement-specialist:1`, `it-procurement-specialist:2`.

- **`handoff_procurement_comparison`**: For RFI/RFP pack and response evidence, supply the actual versioned procurement comparison record, including rfp_revision, evaluation_criteria, comparable_responses, evidence, procurement_rules. Independently assess the evidence against this exact criterion: Supplier responses are comparable and procurement rules are followed. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `rfp_revision`, `evaluation_criteria`, `comparable_responses`, `evidence`, `procurement_rules`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `direct-award`.

**Producer:** `it-procurement-specialist`; **receiver:** `vendor-manager`.

**Receiving condition:** The actual permitted direct-award route, eligible authority and supplier/value-risk evidence are attributable; no competitive responses or tender process are invented.

**Next:** Step 3.

**Role output contracts:** `it-procurement-specialist:3`.

- **`handoff_direct_award_basis`**: The actual permitted direct-award route, eligible authority and supplier/value-risk evidence are attributable; no competitive responses or tender process are invented.
  Required fields: `sourcing_requirement`, `permitted_route`, `prior_exception_authority`, `supplier_evidence`, `value_risk_comparison`, `limitations`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-source-to-contract-to-service-3"></a>

## supplier assessment

**Handoff content contract:** `handoff/source-to-contract-to-service:3`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_supplier_assessment`**: For supplier assessment, supply the actual versioned supplier assessment record, including supplier_id, capability_claims, evidence, material_assumptions, dependency_risks. Independently assess the evidence against this exact criterion: Material supplier assumptions and dependency risks are evidenced. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `supplier_id`, `capability_claims`, `evidence`, `material_assumptions`, `dependency_risks`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `competitive`.

**Producer:** `vendor-manager`; **receiver:** `third-party-risk-manager`.

**Receiving condition:** Material supplier assumptions and dependency risks are evidenced

**Next:** Step 4.

**Role output contracts:** `vendor-manager:1`.

- **`handoff_supplier_assessment`**: For supplier assessment, supply the actual versioned supplier assessment record, including supplier_id, capability_claims, evidence, material_assumptions, dependency_risks. Independently assess the evidence against this exact criterion: Material supplier assumptions and dependency risks are evidenced. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `supplier_id`, `capability_claims`, `evidence`, `material_assumptions`, `dependency_risks`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `direct-award`.

**Producer:** `vendor-manager`; **receiver:** `third-party-risk-manager`.

**Receiving condition:** Material supplier assumptions and dependency risks are evidenced

**Next:** Step 4.

**Role output contracts:** `vendor-manager:1`.

- **`handoff_supplier_assessment`**: For supplier assessment, supply the actual versioned supplier assessment record, including supplier_id, capability_claims, evidence, material_assumptions, dependency_risks. Independently assess the evidence against this exact criterion: Material supplier assumptions and dependency risks are evidenced. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `supplier_id`, `capability_claims`, `evidence`, `material_assumptions`, `dependency_risks`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-source-to-contract-to-service-4"></a>

## security/privacy/supplier risk assessment

**Handoff content contract:** `handoff/source-to-contract-to-service:4`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_supplier_control_risk`**: For security/privacy/supplier risk assessment, supply the actual versioned supplier control risk record, including security_privacy_obligations, critical_risks, controls, mitigation_evidence, residual_authority. Independently assess the evidence against this exact criterion: Critical risks/obligations are resolved, mitigated or accepted by correct authority. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `security_privacy_obligations`, `critical_risks`, `controls`, `mitigation_evidence`, `residual_authority`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `competitive`.

**Producer:** `third-party-risk-manager`; **receiver:** `enterprise-applications-architect`.

**Receiving condition:** Critical risks/obligations are resolved, mitigated or accepted by correct authority

**Next:** Step 5.

**Role output contracts:** `third-party-risk-manager:1`, `third-party-risk-manager:3`.

- **`handoff_supplier_control_risk`**: For security/privacy/supplier risk assessment, supply the actual versioned supplier control risk record, including security_privacy_obligations, critical_risks, controls, mitigation_evidence, residual_authority. Independently assess the evidence against this exact criterion: Critical risks/obligations are resolved, mitigated or accepted by correct authority. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `security_privacy_obligations`, `critical_risks`, `controls`, `mitigation_evidence`, `residual_authority`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `direct-award`.

**Producer:** `third-party-risk-manager`; **receiver:** `enterprise-applications-architect`.

**Receiving condition:** Critical risks/obligations are resolved, mitigated or accepted by correct authority

**Next:** Step 5.

**Role output contracts:** `third-party-risk-manager:1`, `third-party-risk-manager:3`.

- **`handoff_supplier_control_risk`**: For security/privacy/supplier risk assessment, supply the actual versioned supplier control risk record, including security_privacy_obligations, critical_risks, controls, mitigation_evidence, residual_authority. Independently assess the evidence against this exact criterion: Critical risks/obligations are resolved, mitigated or accepted by correct authority. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `security_privacy_obligations`, `critical_risks`, `controls`, `mitigation_evidence`, `residual_authority`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-source-to-contract-to-service-5"></a>

## architecture-fit decision

**Handoff content contract:** `handoff/source-to-contract-to-service:5`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_sourcing_architecture_fit`**: For architecture-fit decision, supply the actual versioned sourcing architecture fit record, including candidate_solution, target_architecture, integration_dependencies, contradictions, disposition. Independently assess the evidence against this exact criterion: Selection does not create hidden target-state or integration contradictions. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `candidate_solution`, `target_architecture`, `integration_dependencies`, `contradictions`, `disposition`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `competitive`.

**Producer:** `enterprise-applications-architect`; **receiver:** `it-procurement-specialist`.

**Receiving condition:** Selection does not create hidden target-state or integration contradictions

**Next:** Step 6.

**Role output contracts:** `enterprise-applications-architect:2`, `enterprise-applications-architect:4`.

- **`handoff_sourcing_architecture_fit`**: For architecture-fit decision, supply the actual versioned sourcing architecture fit record, including candidate_solution, target_architecture, integration_dependencies, contradictions, disposition. Independently assess the evidence against this exact criterion: Selection does not create hidden target-state or integration contradictions. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `candidate_solution`, `target_architecture`, `integration_dependencies`, `contradictions`, `disposition`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `direct-award`.

**Producer:** `enterprise-applications-architect`; **receiver:** `it-procurement-specialist`.

**Receiving condition:** Selection does not create hidden target-state or integration contradictions

**Next:** Step 6.

**Role output contracts:** `enterprise-applications-architect:2`, `enterprise-applications-architect:4`.

- **`handoff_sourcing_architecture_fit`**: For architecture-fit decision, supply the actual versioned sourcing architecture fit record, including candidate_solution, target_architecture, integration_dependencies, contradictions, disposition. Independently assess the evidence against this exact criterion: Selection does not create hidden target-state or integration contradictions. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `candidate_solution`, `target_architecture`, `integration_dependencies`, `contradictions`, `disposition`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-source-to-contract-to-service-6"></a>

## selection decision

**Handoff content contract:** `handoff/source-to-contract-to-service:6`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_supplier_selection`**: For selection decision, supply the actual versioned supplier selection record, including options, declared_criteria, evaluation_evidence, decision_authority, actual_decision. Independently assess the evidence against this exact criterion: Decision is traceable to declared criteria, evidence and authority. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `options`, `declared_criteria`, `evaluation_evidence`, `decision_authority`, `actual_decision`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `competitive`.

**Producer:** `it-procurement-specialist`; **receiver:** `contract-manager`.

**Receiving condition:** Decision is traceable to declared criteria, evidence and authority

**Next:** Step 7.

**Role output contracts:** `it-procurement-specialist:2`, `it-procurement-specialist:3`.

- **`handoff_supplier_selection`**: For selection decision, supply the actual versioned supplier selection record, including options, declared_criteria, evaluation_evidence, decision_authority, actual_decision. Independently assess the evidence against this exact criterion: Decision is traceable to declared criteria, evidence and authority. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `options`, `declared_criteria`, `evaluation_evidence`, `decision_authority`, `actual_decision`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `direct-award`.

**Producer:** `it-procurement-specialist`; **receiver:** `contract-manager`.

**Receiving condition:** Decision is traceable to declared criteria, evidence and authority

**Next:** Step 7.

**Role output contracts:** `it-procurement-specialist:2`, `it-procurement-specialist:3`.

- **`handoff_supplier_selection`**: For selection decision, supply the actual versioned supplier selection record, including options, declared_criteria, evaluation_evidence, decision_authority, actual_decision. Independently assess the evidence against this exact criterion: Decision is traceable to declared criteria, evidence and authority. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `options`, `declared_criteria`, `evaluation_evidence`, `decision_authority`, `actual_decision`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-source-to-contract-to-service-7"></a>

## contract control schedule

**Handoff content contract:** `handoff/source-to-contract-to-service:7`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_contract_control_schedule`**: For contract control schedule, supply the actual versioned contract control schedule record, including mandatory_controls, enforceable_clauses, measurements, evidence, obligations, remedies_exit. Independently assess the evidence against this exact criterion: Every mandatory control has enforceable wording, evidence/measurement and remedy/exit path. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `mandatory_controls`, `enforceable_clauses`, `measurements`, `evidence`, `obligations`, `remedies_exit`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `competitive`.

**Producer:** `contract-manager`; **receiver:** `implementation-consultant`.

**Receiving condition:** Every mandatory control has enforceable wording, evidence/measurement and remedy/exit path

**Next:** Step 8.

**Role output contracts:** `contract-manager:1`.

- **`handoff_contract_control_schedule`**: For contract control schedule, supply the actual versioned contract control schedule record, including mandatory_controls, enforceable_clauses, measurements, evidence, obligations, remedies_exit. Independently assess the evidence against this exact criterion: Every mandatory control has enforceable wording, evidence/measurement and remedy/exit path. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `mandatory_controls`, `enforceable_clauses`, `measurements`, `evidence`, `obligations`, `remedies_exit`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `direct-award`.

**Producer:** `contract-manager`; **receiver:** `implementation-consultant`.

**Receiving condition:** Every mandatory control has enforceable wording, evidence/measurement and remedy/exit path

**Next:** Step 8.

**Role output contracts:** `contract-manager:1`.

- **`handoff_contract_control_schedule`**: For contract control schedule, supply the actual versioned contract control schedule record, including mandatory_controls, enforceable_clauses, measurements, evidence, obligations, remedies_exit. Independently assess the evidence against this exact criterion: Every mandatory control has enforceable wording, evidence/measurement and remedy/exit path. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `mandatory_controls`, `enforceable_clauses`, `measurements`, `evidence`, `obligations`, `remedies_exit`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-source-to-contract-to-service-8"></a>

## implementation plan and evidence

**Handoff content contract:** `handoff/source-to-contract-to-service:8`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_supplier_implementation`**: For implementation plan and evidence, supply the actual versioned supplier implementation record, including implementation_baseline, milestones, actual_results, deviations, prior_variation_authority. Independently assess the evidence against this exact criterion: Implementation deviations are approved, not silently normalised. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `implementation_baseline`, `milestones`, `actual_results`, `deviations`, `prior_variation_authority`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `competitive`.

**Producer:** `implementation-consultant`; **receiver:** `service-transition-and-operational-readiness-manager`.

**Receiving condition:** Implementation deviations are approved, not silently normalised

**Next:** Step 9.

**Role output contracts:** `implementation-consultant:1`, `implementation-consultant:3`.

- **`handoff_supplier_implementation`**: For implementation plan and evidence, supply the actual versioned supplier implementation record, including implementation_baseline, milestones, actual_results, deviations, prior_variation_authority. Independently assess the evidence against this exact criterion: Implementation deviations are approved, not silently normalised. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `implementation_baseline`, `milestones`, `actual_results`, `deviations`, `prior_variation_authority`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `direct-award`.

**Producer:** `implementation-consultant`; **receiver:** `service-transition-and-operational-readiness-manager`.

**Receiving condition:** Implementation deviations are approved, not silently normalised

**Next:** Step 9.

**Role output contracts:** `implementation-consultant:1`, `implementation-consultant:3`.

- **`handoff_supplier_implementation`**: For implementation plan and evidence, supply the actual versioned supplier implementation record, including implementation_baseline, milestones, actual_results, deviations, prior_variation_authority. Independently assess the evidence against this exact criterion: Implementation deviations are approved, not silently normalised. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `implementation_baseline`, `milestones`, `actual_results`, `deviations`, `prior_variation_authority`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-source-to-contract-to-service-9"></a>

## service acceptance

**Handoff content contract:** `handoff/source-to-contract-to-service:9`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_sourced_service_acceptance`**: For service acceptance, supply the actual versioned sourced service acceptance record, including service_scope, operational_owners, readiness_evidence, critical_gaps, actual_acceptance. Independently assess the evidence against this exact criterion: No production acceptance with missing critical operational ownership/evidence. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `service_scope`, `operational_owners`, `readiness_evidence`, `critical_gaps`, `actual_acceptance`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `competitive`.

**Producer:** `service-transition-and-operational-readiness-manager`; **receiver:** `vendor-manager`.

**Receiving condition:** No production acceptance with missing critical operational ownership/evidence

**Next:** Step 10.

**Role output contracts:** `service-transition-and-operational-readiness-manager:3`, `service-transition-and-operational-readiness-manager:4`.

- **`handoff_sourced_service_acceptance`**: For service acceptance, supply the actual versioned sourced service acceptance record, including service_scope, operational_owners, readiness_evidence, critical_gaps, actual_acceptance. Independently assess the evidence against this exact criterion: No production acceptance with missing critical operational ownership/evidence. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `service_scope`, `operational_owners`, `readiness_evidence`, `critical_gaps`, `actual_acceptance`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `direct-award`.

**Producer:** `service-transition-and-operational-readiness-manager`; **receiver:** `vendor-manager`.

**Receiving condition:** No production acceptance with missing critical operational ownership/evidence

**Next:** Step 10.

**Role output contracts:** `service-transition-and-operational-readiness-manager:3`, `service-transition-and-operational-readiness-manager:4`.

- **`handoff_sourced_service_acceptance`**: For service acceptance, supply the actual versioned sourced service acceptance record, including service_scope, operational_owners, readiness_evidence, critical_gaps, actual_acceptance. Independently assess the evidence against this exact criterion: No production acceptance with missing critical operational ownership/evidence. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `service_scope`, `operational_owners`, `readiness_evidence`, `critical_gaps`, `actual_acceptance`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-source-to-contract-to-service-10"></a>

## vendor governance baseline

**Handoff content contract:** `handoff/source-to-contract-to-service:10`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_vendor_governance_baseline`**: For vendor governance baseline, supply the actual versioned vendor governance baseline record, including contract_obligations, service_measures, data_sources, responsible_owners, review_cadence. Independently assess the evidence against this exact criterion: Contractual obligations map to measured service/vendor governance. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `contract_obligations`, `service_measures`, `data_sources`, `responsible_owners`, `review_cadence`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `competitive`.

**Producer:** `vendor-manager`; **receiver:** `engagement:named-authority`.

**Receiving condition:** Contractual obligations map to measured service/vendor governance

**Next:** Terminal disposition; no downstream step.

**Role output contracts:** `vendor-manager:1`, `vendor-manager:2`.

- **`handoff_vendor_governance_baseline`**: For vendor governance baseline, supply the actual versioned vendor governance baseline record, including contract_obligations, service_measures, data_sources, responsible_owners, review_cadence. Independently assess the evidence against this exact criterion: Contractual obligations map to measured service/vendor governance. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `contract_obligations`, `service_measures`, `data_sources`, `responsible_owners`, `review_cadence`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `direct-award`.

**Producer:** `vendor-manager`; **receiver:** `engagement:named-authority`.

**Receiving condition:** Contractual obligations map to measured service/vendor governance

**Next:** Terminal disposition; no downstream step.

**Role output contracts:** `vendor-manager:1`, `vendor-manager:2`.

- **`handoff_vendor_governance_baseline`**: For vendor governance baseline, supply the actual versioned vendor governance baseline record, including contract_obligations, service_measures, data_sources, responsible_owners, review_cadence. Independently assess the evidence against this exact criterion: Contractual obligations map to measured service/vendor governance. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `contract_obligations`, `service_measures`, `data_sources`, `responsible_owners`, `review_cadence`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.
<!-- JAI:OUTPUT-CONTRACTS:END -->
