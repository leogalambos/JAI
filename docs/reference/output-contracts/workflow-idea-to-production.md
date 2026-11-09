<!-- JAI:OUTPUT-CONTRACTS:START -->
# Idea to production: source-owned handoff contracts

[Catalogue](index.md)

<a id="output-handoff-idea-to-production-1"></a>

## demand record with outcome and owner

**Handoff content contract:** `handoff/idea-to-production:1`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_demand_outcome`**: For demand record with outcome and owner, supply the actual versioned demand outcome record, including demand_id, outcome, owner, source, urgency. Independently assess the evidence against this exact criterion: Demand with no named business outcome does not enter the pipeline. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `demand_id`, `outcome`, `owner`, `source`, `urgency`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `new-product`.

**Producer:** `business-relationship-manager`; **receiver:** `product-manager`.

**Receiving condition:** Demand with no named business outcome does not enter the pipeline

**Next:** Step 2.

**Role output contracts:** `business-relationship-manager:2`.

- **`handoff_demand_outcome`**: For demand record with outcome and owner, supply the actual versioned demand outcome record, including demand_id, outcome, owner, source, urgency. Independently assess the evidence against this exact criterion: Demand with no named business outcome does not enter the pipeline. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `demand_id`, `outcome`, `owner`, `source`, `urgency`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `existing-service-change`.

**Producer:** `business-relationship-manager`; **receiver:** `product-manager`.

**Receiving condition:** Demand with no named business outcome does not enter the pipeline

**Next:** Step 2.

**Role output contracts:** `business-relationship-manager:2`.

- **`handoff_demand_outcome`**: For demand record with outcome and owner, supply the actual versioned demand outcome record, including demand_id, outcome, owner, source, urgency. Independently assess the evidence against this exact criterion: Demand with no named business outcome does not enter the pipeline. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `demand_id`, `outcome`, `owner`, `source`, `urgency`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-idea-to-production-2"></a>

## roadmap item with problem statement and success measure

**Handoff content contract:** `handoff/idea-to-production:2`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_product_opportunity`**: For roadmap item with problem statement and success measure, supply the actual versioned product opportunity record, including problem, evidence, target_users, success_measure, roadmap_scope. Independently assess the evidence against this exact criterion: The customer problem and its evidence are stated. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `problem`, `evidence`, `target_users`, `success_measure`, `roadmap_scope`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `new-product`.

**Producer:** `product-manager`; **receiver:** `business-analyst`.

**Receiving condition:** The customer problem and its evidence are stated

**Next:** Step 3.

**Role output contracts:** `product-manager:1`, `product-manager:3`.

- **`handoff_product_opportunity`**: For roadmap item with problem statement and success measure, supply the actual versioned product opportunity record, including problem, evidence, target_users, success_measure, roadmap_scope. Independently assess the evidence against this exact criterion: The customer problem and its evidence are stated. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `problem`, `evidence`, `target_users`, `success_measure`, `roadmap_scope`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `existing-service-change`.

**Producer:** `product-manager`; **receiver:** `business-analyst`.

**Receiving condition:** The customer problem and its evidence are stated

**Next:** Step 3.

**Role output contracts:** `product-manager:1`, `product-manager:3`.

- **`handoff_product_opportunity`**: For roadmap item with problem statement and success measure, supply the actual versioned product opportunity record, including problem, evidence, target_users, success_measure, roadmap_scope. Independently assess the evidence against this exact criterion: The customer problem and its evidence are stated. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `problem`, `evidence`, `target_users`, `success_measure`, `roadmap_scope`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-idea-to-production-3"></a>

## requirements baseline with traceability

**Handoff content contract:** `handoff/idea-to-production:3`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_requirements_baseline`**: For requirements baseline with traceability, supply the actual versioned requirements baseline record, including baseline_id, requirements, source_links, priorities, verification_criteria. Independently assess the evidence against this exact criterion: Every requirement is atomic, testable and traced to a source. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `baseline_id`, `requirements`, `source_links`, `priorities`, `verification_criteria`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `new-product`.

**Producer:** `business-analyst`; **receiver:** `solution-architect`.

**Receiving condition:** Every requirement is atomic, testable and traced to a source

**Next:** Step 4.

**Role output contracts:** `business-analyst:1`.

- **`handoff_requirements_baseline`**: For requirements baseline with traceability, supply the actual versioned requirements baseline record, including baseline_id, requirements, source_links, priorities, verification_criteria. Independently assess the evidence against this exact criterion: Every requirement is atomic, testable and traced to a source. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `baseline_id`, `requirements`, `source_links`, `priorities`, `verification_criteria`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `existing-service-change`.

**Producer:** `business-analyst`; **receiver:** `solution-architect`.

**Receiving condition:** Every requirement is atomic, testable and traced to a source

**Next:** Step 4.

**Role output contracts:** `business-analyst:1`.

- **`handoff_requirements_baseline`**: For requirements baseline with traceability, supply the actual versioned requirements baseline record, including baseline_id, requirements, source_links, priorities, verification_criteria. Independently assess the evidence against this exact criterion: Every requirement is atomic, testable and traced to a source. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `baseline_id`, `requirements`, `source_links`, `priorities`, `verification_criteria`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-idea-to-production-4"></a>

## solution architecture and ADRs

**Handoff content contract:** `handoff/idea-to-production:4`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_solution_architecture`**: For solution architecture and ADRs, supply the actual versioned solution architecture record, including baseline, boundaries, decisions, quality_targets, failure_modes, operational_review. Independently assess the evidence against this exact criterion: Reviewed by someone who will operate it; failure modes documented. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `baseline`, `boundaries`, `decisions`, `quality_targets`, `failure_modes`, `operational_review`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `new-product`.

**Producer:** `solution-architect`; **receiver:** `security-architect`.

**Receiving condition:** Reviewed by someone who will operate it; failure modes documented

**Next:** Step 5.

**Role output contracts:** `solution-architect:1`, `solution-architect:4`.

- **`handoff_solution_architecture`**: For solution architecture and ADRs, supply the actual versioned solution architecture record, including baseline, boundaries, decisions, quality_targets, failure_modes, operational_review. Independently assess the evidence against this exact criterion: Reviewed by someone who will operate it; failure modes documented. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `baseline`, `boundaries`, `decisions`, `quality_targets`, `failure_modes`, `operational_review`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `existing-service-change`.

**Producer:** `solution-architect`; **receiver:** `security-architect`.

**Receiving condition:** Reviewed by someone who will operate it; failure modes documented

**Next:** Step 5.

**Role output contracts:** `solution-architect:1`, `solution-architect:4`.

- **`handoff_solution_architecture`**: For solution architecture and ADRs, supply the actual versioned solution architecture record, including baseline, boundaries, decisions, quality_targets, failure_modes, operational_review. Independently assess the evidence against this exact criterion: Reviewed by someone who will operate it; failure modes documented. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `baseline`, `boundaries`, `decisions`, `quality_targets`, `failure_modes`, `operational_review`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-idea-to-production-5"></a>

## security requirements and threat model

**Handoff content contract:** `handoff/idea-to-production:5`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_security_design`**: For security requirements and threat model, supply the actual versioned security design record, including threat_scenarios, business_risks, controls, requirement_links, residual_exposure. Independently assess the evidence against this exact criterion: Every control traces to a threat and a business risk. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `threat_scenarios`, `business_risks`, `controls`, `requirement_links`, `residual_exposure`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `new-product`.

**Producer:** `security-architect`; **receiver:** `technical-lead`.

**Receiving condition:** Every control traces to a threat and a business risk

**Next:** Step 6.

**Role output contracts:** `security-architect:2`, `security-architect:4`.

- **`handoff_security_design`**: For security requirements and threat model, supply the actual versioned security design record, including threat_scenarios, business_risks, controls, requirement_links, residual_exposure. Independently assess the evidence against this exact criterion: Every control traces to a threat and a business risk. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `threat_scenarios`, `business_risks`, `controls`, `requirement_links`, `residual_exposure`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `existing-service-change`.

**Producer:** `security-architect`; **receiver:** `technical-lead`.

**Receiving condition:** Every control traces to a threat and a business risk

**Next:** Step 6.

**Role output contracts:** `security-architect:2`, `security-architect:4`.

- **`handoff_security_design`**: For security requirements and threat model, supply the actual versioned security design record, including threat_scenarios, business_risks, controls, requirement_links, residual_exposure. Independently assess the evidence against this exact criterion: Every control traces to a threat and a business risk. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `threat_scenarios`, `business_risks`, `controls`, `requirement_links`, `residual_exposure`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-idea-to-production-6"></a>

## technical breakdown and readiness-checked items

**Handoff content contract:** `handoff/idea-to-production:6`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_delivery_readiness`**: For technical breakdown and readiness-checked items, supply the actual versioned delivery readiness record, including work_items, acceptance_criteria, dependency_refs, technical_owners, readiness_gaps. Independently assess the evidence against this exact criterion: Acceptance criteria and dependencies exist before start. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `work_items`, `acceptance_criteria`, `dependency_refs`, `technical_owners`, `readiness_gaps`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `new-product`.

**Producer:** `technical-lead`; **receiver:** `software-engineer`.

**Receiving condition:** Acceptance criteria and dependencies exist before start

**Next:** Step 7.

**Role output contracts:** `technical-lead:4`.

- **`handoff_delivery_readiness`**: For technical breakdown and readiness-checked items, supply the actual versioned delivery readiness record, including work_items, acceptance_criteria, dependency_refs, technical_owners, readiness_gaps. Independently assess the evidence against this exact criterion: Acceptance criteria and dependencies exist before start. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `work_items`, `acceptance_criteria`, `dependency_refs`, `technical_owners`, `readiness_gaps`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `existing-service-change`.

**Producer:** `technical-lead`; **receiver:** `software-engineer`.

**Receiving condition:** Acceptance criteria and dependencies exist before start

**Next:** Step 7.

**Role output contracts:** `technical-lead:4`.

- **`handoff_delivery_readiness`**: For technical breakdown and readiness-checked items, supply the actual versioned delivery readiness record, including work_items, acceptance_criteria, dependency_refs, technical_owners, readiness_gaps. Independently assess the evidence against this exact criterion: Acceptance criteria and dependencies exist before start. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `work_items`, `acceptance_criteria`, `dependency_refs`, `technical_owners`, `readiness_gaps`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-idea-to-production-7"></a>

## reviewed, merged change with rollback path

**Handoff content contract:** `handoff/idea-to-production:7`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_reviewed_source_change`**: For reviewed, merged change with rollback path, supply the actual versioned reviewed source change record, including source_revision, changed_behaviour, peer_review, test_results, telemetry, rollback_path. Independently assess the evidence against this exact criterion: Peer reviewed; no secrets in source; telemetry present. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `source_revision`, `changed_behaviour`, `peer_review`, `test_results`, `telemetry`, `rollback_path`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `new-product`.

**Producer:** `software-engineer`; **receiver:** `test-analyst`.

**Receiving condition:** Peer reviewed; no secrets in source; telemetry present

**Next:** Step 8.

**Role output contracts:** `software-engineer:1`, `software-engineer:2`, `software-engineer:4`.

- **`handoff_reviewed_source_change`**: For reviewed, merged change with rollback path, supply the actual versioned reviewed source change record, including source_revision, changed_behaviour, peer_review, test_results, telemetry, rollback_path. Independently assess the evidence against this exact criterion: Peer reviewed; no secrets in source; telemetry present. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `source_revision`, `changed_behaviour`, `peer_review`, `test_results`, `telemetry`, `rollback_path`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `existing-service-change`.

**Producer:** `software-engineer`; **receiver:** `test-analyst`.

**Receiving condition:** Peer reviewed; no secrets in source; telemetry present

**Next:** Step 8.

**Role output contracts:** `software-engineer:1`, `software-engineer:2`, `software-engineer:4`.

- **`handoff_reviewed_source_change`**: For reviewed, merged change with rollback path, supply the actual versioned reviewed source change record, including source_revision, changed_behaviour, peer_review, test_results, telemetry, rollback_path. Independently assess the evidence against this exact criterion: Peer reviewed; no secrets in source; telemetry present. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `source_revision`, `changed_behaviour`, `peer_review`, `test_results`, `telemetry`, `rollback_path`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-idea-to-production-8"></a>

## test evidence and residual risk statement

**Handoff content contract:** `handoff/idea-to-production:8`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_release_test_evidence`**: For test evidence and residual risk statement, supply the actual versioned release test evidence record, including tested_revision, predeclared_exit_criteria, actual_results, exclusions, residual_risk_disposition. Independently assess the evidence against this exact criterion: Exit criteria agreed before execution and met or waived. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `tested_revision`, `predeclared_exit_criteria`, `actual_results`, `exclusions`, `residual_risk_disposition`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `new-product`.

**Producer:** `test-analyst`; **receiver:** `release-engineer`.

**Receiving condition:** Exit criteria agreed before execution and met or waived

**Next:** Step 9.

**Role output contracts:** `test-analyst:2`, `test-analyst:4`.

- **`handoff_release_test_evidence`**: For test evidence and residual risk statement, supply the actual versioned release test evidence record, including tested_revision, predeclared_exit_criteria, actual_results, exclusions, residual_risk_disposition. Independently assess the evidence against this exact criterion: Exit criteria agreed before execution and met or waived. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `tested_revision`, `predeclared_exit_criteria`, `actual_results`, `exclusions`, `residual_risk_disposition`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `existing-service-change`.

**Producer:** `test-analyst`; **receiver:** `release-engineer`.

**Receiving condition:** Exit criteria agreed before execution and met or waived

**Next:** Step 9.

**Role output contracts:** `test-analyst:2`, `test-analyst:4`.

- **`handoff_release_test_evidence`**: For test evidence and residual risk statement, supply the actual versioned release test evidence record, including tested_revision, predeclared_exit_criteria, actual_results, exclusions, residual_risk_disposition. Independently assess the evidence against this exact criterion: Exit criteria agreed before execution and met or waived. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `tested_revision`, `predeclared_exit_criteria`, `actual_results`, `exclusions`, `residual_risk_disposition`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-idea-to-production-9"></a>

## release manifest and tested rollback

**Handoff content contract:** `handoff/idea-to-production:9`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_release_manifest`**: For release manifest and tested rollback, supply the actual versioned release manifest record, including release_id, artifact_versions, target_environments, provenance, rollback_rehearsal. Independently assess the evidence against this exact criterion: Manifest states exactly which artefact versions ship where. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `release_id`, `artifact_versions`, `target_environments`, `provenance`, `rollback_rehearsal`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `new-product`.

**Producer:** `release-engineer`; **receiver:** `change-manager`.

**Receiving condition:** Manifest states exactly which artefact versions ship where

**Next:** Step 10.

**Role output contracts:** `release-engineer:2`, `release-engineer:4`.

- **`handoff_release_manifest`**: For release manifest and tested rollback, supply the actual versioned release manifest record, including release_id, artifact_versions, target_environments, provenance, rollback_rehearsal. Independently assess the evidence against this exact criterion: Manifest states exactly which artefact versions ship where. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `release_id`, `artifact_versions`, `target_environments`, `provenance`, `rollback_rehearsal`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `existing-service-change`.

**Producer:** `release-engineer`; **receiver:** `change-manager`.

**Receiving condition:** Manifest states exactly which artefact versions ship where

**Next:** Step 10.

**Role output contracts:** `release-engineer:2`, `release-engineer:4`.

- **`handoff_release_manifest`**: For release manifest and tested rollback, supply the actual versioned release manifest record, including release_id, artifact_versions, target_environments, provenance, rollback_rehearsal. Independently assess the evidence against this exact criterion: Manifest states exactly which artefact versions ship where. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `release_id`, `artifact_versions`, `target_environments`, `provenance`, `rollback_rehearsal`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-idea-to-production-10"></a>

## change authorisation

**Handoff content contract:** `handoff/idea-to-production:10`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_change_authorisation`**: For change authorisation, supply the actual versioned change authorisation record, including change_id, exact_scope, risk_class, authority, decision, window, emergency_record. Independently assess the evidence against this exact criterion: Risk class matched to approval path; emergency changes logged within the window. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `change_id`, `exact_scope`, `risk_class`, `authority`, `decision`, `window`, `emergency_record`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `new-product`.

**Producer:** `change-manager`; **receiver:** `gitops-and-continuous-delivery-engineer`.

**Receiving condition:** Risk class matched to approval path; emergency changes logged within the window

**Next:** Step 11.

**Role output contracts:** `change-manager:1`.

- **`handoff_change_authorisation`**: For change authorisation, supply the actual versioned change authorisation record, including change_id, exact_scope, risk_class, authority, decision, window, emergency_record. Independently assess the evidence against this exact criterion: Risk class matched to approval path; emergency changes logged within the window. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `change_id`, `exact_scope`, `risk_class`, `authority`, `decision`, `window`, `emergency_record`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `existing-service-change`.

**Producer:** `change-manager`; **receiver:** `gitops-and-continuous-delivery-engineer`.

**Receiving condition:** Risk class matched to approval path; emergency changes logged within the window

**Next:** Step 11.

**Role output contracts:** `change-manager:1`.

- **`handoff_change_authorisation`**: For change authorisation, supply the actual versioned change authorisation record, including change_id, exact_scope, risk_class, authority, decision, window, emergency_record. Independently assess the evidence against this exact criterion: Risk class matched to approval path; emergency changes logged within the window. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `change_id`, `exact_scope`, `risk_class`, `authority`, `decision`, `window`, `emergency_record`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-idea-to-production-11"></a>

## deployed change with health gate

**Handoff content contract:** `handoff/idea-to-production:11`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_deployment_observations`**: For deployed change with health gate, supply the actual versioned deployment observations record, including approved_change_ref, deployed_revision, health_thresholds, actual_results, reversal_observations. Independently assess the evidence against this exact criterion: Health gate and automatic rollback defined and exercised. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `approved_change_ref`, `deployed_revision`, `health_thresholds`, `actual_results`, `reversal_observations`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `new-product`.

**Producer:** `gitops-and-continuous-delivery-engineer`; **receiver:** `site-reliability-engineer`.

**Receiving condition:** Health gate and automatic rollback defined and exercised

**Next:** Step 12.

**Role output contracts:** `gitops-and-continuous-delivery-engineer:3`, `gitops-and-continuous-delivery-engineer:4`.

- **`handoff_deployment_observations`**: For deployed change with health gate, supply the actual versioned deployment observations record, including approved_change_ref, deployed_revision, health_thresholds, actual_results, reversal_observations. Independently assess the evidence against this exact criterion: Health gate and automatic rollback defined and exercised. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `approved_change_ref`, `deployed_revision`, `health_thresholds`, `actual_results`, `reversal_observations`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `existing-service-change`.

**Producer:** `gitops-and-continuous-delivery-engineer`; **receiver:** `site-reliability-engineer`.

**Receiving condition:** Health gate and automatic rollback defined and exercised

**Next:** Step 12.

**Role output contracts:** `gitops-and-continuous-delivery-engineer:3`, `gitops-and-continuous-delivery-engineer:4`.

- **`handoff_deployment_observations`**: For deployed change with health gate, supply the actual versioned deployment observations record, including approved_change_ref, deployed_revision, health_thresholds, actual_results, reversal_observations. Independently assess the evidence against this exact criterion: Health gate and automatic rollback defined and exercised. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `approved_change_ref`, `deployed_revision`, `health_thresholds`, `actual_results`, `reversal_observations`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-idea-to-production-12"></a>

## service operating within SLO, or an error-budget decision

**Handoff content contract:** `handoff/idea-to-production:12`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_service_objective_status`**: For service operating within SLO, or an error-budget decision, supply the actual versioned service objective status record, including service_id, measurement_window, indicators, objectives, budget_consumption, policy_action. Independently assess the evidence against this exact criterion: Error budget policy actually enforced. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `service_id`, `measurement_window`, `indicators`, `objectives`, `budget_consumption`, `policy_action`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `new-product`.

**Producer:** `site-reliability-engineer`; **receiver:** `product-analyst`.

**Receiving condition:** Error budget policy actually enforced

**Next:** Step 13.

**Role output contracts:** `site-reliability-engineer:1`.

- **`handoff_service_objective_status`**: For service operating within SLO, or an error-budget decision, supply the actual versioned service objective status record, including service_id, measurement_window, indicators, objectives, budget_consumption, policy_action. Independently assess the evidence against this exact criterion: Error budget policy actually enforced. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `service_id`, `measurement_window`, `indicators`, `objectives`, `budget_consumption`, `policy_action`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `existing-service-change`.

**Producer:** `site-reliability-engineer`; **receiver:** `product-analyst`.

**Receiving condition:** Error budget policy actually enforced

**Next:** Step 13.

**Role output contracts:** `site-reliability-engineer:1`.

- **`handoff_service_objective_status`**: For service operating within SLO, or an error-budget decision, supply the actual versioned service objective status record, including service_id, measurement_window, indicators, objectives, budget_consumption, policy_action. Independently assess the evidence against this exact criterion: Error budget policy actually enforced. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `service_id`, `measurement_window`, `indicators`, `objectives`, `budget_consumption`, `policy_action`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-idea-to-production-13"></a>

## benefit measurement against the success measure

**Handoff content contract:** `handoff/idea-to-production:13`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_benefit_observations`**: For benefit measurement against the success measure, supply the actual versioned benefit observations record, including success_measure, baseline, observation_period, effect_size, method, uncertainty. Independently assess the evidence against this exact criterion: Result reported with effect size, not just direction. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `success_measure`, `baseline`, `observation_period`, `effect_size`, `method`, `uncertainty`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `new-product`.

**Producer:** `product-analyst`; **receiver:** `engagement:named-authority`.

**Receiving condition:** Result reported with effect size, not just direction

**Next:** Terminal disposition; no downstream step.

**Role output contracts:** `product-analyst:1`, `product-analyst:2`.

- **`handoff_benefit_observations`**: For benefit measurement against the success measure, supply the actual versioned benefit observations record, including success_measure, baseline, observation_period, effect_size, method, uncertainty. Independently assess the evidence against this exact criterion: Result reported with effect size, not just direction. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `success_measure`, `baseline`, `observation_period`, `effect_size`, `method`, `uncertainty`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `existing-service-change`.

**Producer:** `product-analyst`; **receiver:** `engagement:named-authority`.

**Receiving condition:** Result reported with effect size, not just direction

**Next:** Terminal disposition; no downstream step.

**Role output contracts:** `product-analyst:1`, `product-analyst:2`.

- **`handoff_benefit_observations`**: For benefit measurement against the success measure, supply the actual versioned benefit observations record, including success_measure, baseline, observation_period, effect_size, method, uncertainty. Independently assess the evidence against this exact criterion: Result reported with effect size, not just direction. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `success_measure`, `baseline`, `observation_period`, `effect_size`, `method`, `uncertainty`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.
<!-- JAI:OUTPUT-CONTRACTS:END -->
