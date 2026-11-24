<!-- JAI:OUTPUT-CONTRACTS:START -->
# DAST integration and control assurance for containerised delivery: source-owned handoff contracts

[Catalogue](index.md)

<a id="output-handoff-dast-control-assurance-1"></a>

## readiness and deployment decision

**Handoff content contract:** `handoff/dast-control-assurance:1`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_dast_readiness`**: For readiness and deployment decision, supply the actual versioned dast readiness record, including mandate_ref, application_scope, owners, policy_ref, interface_inventory, topology_decision, feasibility_evidence. Independently assess the evidence against this exact criterion: The application owner, policy and scope are identified. The deployment decision records feasibility evidence, trust boundaries, gateway and backend perspectives, and limitations.. Do not substitute a related policy, plan or claimed execution for the required work product and observations. Apply the relevant requirements and evidence criteria in dast-methodology.md: Implementation lifecycle and Deployment patterns and fidelity. Record each unmet or inapplicable obligation and its disposition.
  Required fields: `mandate_ref`, `application_scope`, `owners`, `policy_ref`, `interface_inventory`, `topology_decision`, `feasibility_evidence`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `integration`.

**Producer:** `solution-architect`; **receiver:** `security-architect`.

**Receiving condition:** The application owner, policy and scope are identified. The deployment decision records feasibility evidence, trust boundaries, gateway and backend perspectives, and limitations.

**Next:** Step 2.

**Role output contracts:** `solution-architect:4`.

- **`handoff_dast_readiness`**: For readiness and deployment decision, supply the actual versioned dast readiness record, including mandate_ref, application_scope, owners, policy_ref, interface_inventory, topology_decision, feasibility_evidence. Independently assess the evidence against this exact criterion: The application owner, policy and scope are identified. The deployment decision records feasibility evidence, trust boundaries, gateway and backend perspectives, and limitations.. Do not substitute a related policy, plan or claimed execution for the required work product and observations. Apply the relevant requirements and evidence criteria in dast-methodology.md: Implementation lifecycle and Deployment patterns and fidelity. Record each unmet or inapplicable obligation and its disposition.
  Required fields: `mandate_ref`, `application_scope`, `owners`, `policy_ref`, `interface_inventory`, `topology_decision`, `feasibility_evidence`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `qualification`.

**Producer:** `solution-architect`; **receiver:** `security-architect`.

**Receiving condition:** The application owner, policy and scope are identified. The deployment decision records feasibility evidence, trust boundaries, gateway and backend perspectives, and limitations.

**Next:** Step 2.

**Role output contracts:** `solution-architect:4`.

- **`handoff_dast_readiness`**: For readiness and deployment decision, supply the actual versioned dast readiness record, including mandate_ref, application_scope, owners, policy_ref, interface_inventory, topology_decision, feasibility_evidence. Independently assess the evidence against this exact criterion: The application owner, policy and scope are identified. The deployment decision records feasibility evidence, trust boundaries, gateway and backend perspectives, and limitations.. Do not substitute a related policy, plan or claimed execution for the required work product and observations. Apply the relevant requirements and evidence criteria in dast-methodology.md: Implementation lifecycle and Deployment patterns and fidelity. Record each unmet or inapplicable obligation and its disposition.
  Required fields: `mandate_ref`, `application_scope`, `owners`, `policy_ref`, `interface_inventory`, `topology_decision`, `feasibility_evidence`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-dast-control-assurance-2"></a>

## security architecture and traceability baseline

**Handoff content contract:** `handoff/dast-control-assurance:2`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_dast_security_baseline`**: For security architecture and traceability baseline, supply the actual versioned dast security baseline record, including risk_refs, security_requirements, architecture_ref, coverage_matrix, acceptance_criteria, authority_matrix. Independently assess the evidence against this exact criterion: Each mandatory scenario traces to a versioned requirement, expected evidence and accountable control. Gaps have an owner and disposition.. Do not substitute a related policy, plan or claimed execution for the required work product and observations. Apply the relevant requirements and evidence criteria in dast-methodology.md: Security requirements catalogue and Qualification and coverage. Record each unmet or inapplicable obligation and its disposition.
  Required fields: `risk_refs`, `security_requirements`, `architecture_ref`, `coverage_matrix`, `acceptance_criteria`, `authority_matrix`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `integration`.

**Producer:** `security-architect`; **receiver:** `solution-architect`.

**Receiving condition:** Each mandatory scenario traces to a versioned requirement, expected evidence and accountable control. Gaps have an owner and disposition.

**Next:** Step 10.

**Role output contracts:** `security-architect:1`.

- **`handoff_dast_security_baseline`**: For security architecture and traceability baseline, supply the actual versioned dast security baseline record, including risk_refs, security_requirements, architecture_ref, coverage_matrix, acceptance_criteria, authority_matrix. Independently assess the evidence against this exact criterion: Each mandatory scenario traces to a versioned requirement, expected evidence and accountable control. Gaps have an owner and disposition.. Do not substitute a related policy, plan or claimed execution for the required work product and observations. Apply the relevant requirements and evidence criteria in dast-methodology.md: Security requirements catalogue and Qualification and coverage. Record each unmet or inapplicable obligation and its disposition.
  Required fields: `risk_refs`, `security_requirements`, `architecture_ref`, `coverage_matrix`, `acceptance_criteria`, `authority_matrix`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `qualification`.

**Producer:** `security-architect`; **receiver:** `control-owner`.

**Receiving condition:** Each mandatory scenario traces to a versioned requirement, expected evidence and accountable control. Gaps have an owner and disposition.

**Next:** Step 3.

**Role output contracts:** `security-architect:1`.

- **`handoff_dast_security_baseline`**: For security architecture and traceability baseline, supply the actual versioned dast security baseline record, including risk_refs, security_requirements, architecture_ref, coverage_matrix, acceptance_criteria, authority_matrix. Independently assess the evidence against this exact criterion: Each mandatory scenario traces to a versioned requirement, expected evidence and accountable control. Gaps have an owner and disposition.. Do not substitute a related policy, plan or claimed execution for the required work product and observations. Apply the relevant requirements and evidence criteria in dast-methodology.md: Security requirements catalogue and Qualification and coverage. Record each unmet or inapplicable obligation and its disposition.
  Required fields: `risk_refs`, `security_requirements`, `architecture_ref`, `coverage_matrix`, `acceptance_criteria`, `authority_matrix`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-dast-control-assurance-3"></a>

## control qualification dossier

**Handoff content contract:** `handoff/dast-control-assurance:3`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_dast_qualification`**: For control qualification dossier, supply the actual versioned dast qualification record, including qualified_scope, implementation_refs, qualification_results, coverage, fitness_gaps, gate_negative_results, operations_runbook. Independently assess the evidence against this exact criterion: The dossier records actual positive and negative observations, identity and session evidence, independent coverage denominators, cleanup and concurrency, and a protected release path. Unmet requirements remain visible.. Do not substitute a related policy, plan or claimed execution for the required work product and observations. Apply the relevant requirements and evidence criteria in dast-methodology.md: Qualification and coverage and Example and completion. Record each unmet or inapplicable obligation and its disposition.
  Required fields: `qualified_scope`, `implementation_refs`, `qualification_results`, `coverage`, `fitness_gaps`, `gate_negative_results`, `operations_runbook`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `integration`.

**Producer:** `control-owner`; **receiver:** `internal-it-auditor`.

**Receiving condition:** The dossier records actual positive and negative observations, identity and session evidence, independent coverage denominators, cleanup and concurrency, and a protected release path. Unmet requirements remain visible.

**Next:** Step 4.

**Role output contracts:** `control-owner:2`.

- **`handoff_dast_qualification`**: For control qualification dossier, supply the actual versioned dast qualification record, including qualified_scope, implementation_refs, qualification_results, coverage, fitness_gaps, gate_negative_results, operations_runbook. Independently assess the evidence against this exact criterion: The dossier records actual positive and negative observations, identity and session evidence, independent coverage denominators, cleanup and concurrency, and a protected release path. Unmet requirements remain visible.. Do not substitute a related policy, plan or claimed execution for the required work product and observations. Apply the relevant requirements and evidence criteria in dast-methodology.md: Qualification and coverage and Example and completion. Record each unmet or inapplicable obligation and its disposition.
  Required fields: `qualified_scope`, `implementation_refs`, `qualification_results`, `coverage`, `fitness_gaps`, `gate_negative_results`, `operations_runbook`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `qualification`.

**Producer:** `control-owner`; **receiver:** `internal-it-auditor`.

**Receiving condition:** The dossier records actual positive and negative observations, identity and session evidence, independent coverage denominators, cleanup and concurrency, and a protected release path. Unmet requirements remain visible.

**Next:** Step 4.

**Role output contracts:** `control-owner:2`.

- **`handoff_dast_qualification`**: For control qualification dossier, supply the actual versioned dast qualification record, including qualified_scope, implementation_refs, qualification_results, coverage, fitness_gaps, gate_negative_results, operations_runbook. Independently assess the evidence against this exact criterion: The dossier records actual positive and negative observations, identity and session evidence, independent coverage denominators, cleanup and concurrency, and a protected release path. Unmet requirements remain visible.. Do not substitute a related policy, plan or claimed execution for the required work product and observations. Apply the relevant requirements and evidence criteria in dast-methodology.md: Qualification and coverage and Example and completion. Record each unmet or inapplicable obligation and its disposition.
  Required fields: `qualified_scope`, `implementation_refs`, `qualification_results`, `coverage`, `fitness_gaps`, `gate_negative_results`, `operations_runbook`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-dast-control-assurance-4"></a>

## independent security assessment

**Handoff content contract:** `handoff/dast-control-assurance:4`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_dast_independent_review`**: For independent security assessment, supply the actual versioned dast independent review record, including reviewer, independence, source_versions, criteria_refs, findings, verdict. Independently assess the evidence against this exact criterion: The reviewer is independent of design and implementation. Findings cite criteria and observed evidence, including qualification and release enforcement limitations.. Do not substitute a related policy, plan or claimed execution for the required work product and observations. Apply the relevant requirements and evidence criteria in dast-methodology.md: Accountability and decision rights, Qualification and coverage, and Output Security Gate and exceptions. Record each unmet or inapplicable obligation and its disposition.
  Required fields: `reviewer`, `independence`, `source_versions`, `criteria_refs`, `findings`, `verdict`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `integration`.

**Producer:** `internal-it-auditor`; **receiver:** `engagement:named-authority`.

**Receiving condition:** The reviewer is independent of design and implementation. Findings cite criteria and observed evidence, including qualification and release enforcement limitations.

**Next:** Step 5.

**Role output contracts:** `internal-it-auditor:3`.

- **`handoff_dast_independent_review`**: For independent security assessment, supply the actual versioned dast independent review record, including reviewer, independence, source_versions, criteria_refs, findings, verdict. Independently assess the evidence against this exact criterion: The reviewer is independent of design and implementation. Findings cite criteria and observed evidence, including qualification and release enforcement limitations.. Do not substitute a related policy, plan or claimed execution for the required work product and observations. Apply the relevant requirements and evidence criteria in dast-methodology.md: Accountability and decision rights, Qualification and coverage, and Output Security Gate and exceptions. Record each unmet or inapplicable obligation and its disposition.
  Required fields: `reviewer`, `independence`, `source_versions`, `criteria_refs`, `findings`, `verdict`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `qualification`.

**Producer:** `internal-it-auditor`; **receiver:** `engagement:named-authority`.

**Receiving condition:** The reviewer is independent of design and implementation. Findings cite criteria and observed evidence, including qualification and release enforcement limitations.

**Next:** Step 5.

**Role output contracts:** `internal-it-auditor:3`.

- **`handoff_dast_independent_review`**: For independent security assessment, supply the actual versioned dast independent review record, including reviewer, independence, source_versions, criteria_refs, findings, verdict. Independently assess the evidence against this exact criterion: The reviewer is independent of design and implementation. Findings cite criteria and observed evidence, including qualification and release enforcement limitations.. Do not substitute a related policy, plan or claimed execution for the required work product and observations. Apply the relevant requirements and evidence criteria in dast-methodology.md: Accountability and decision rights, Qualification and coverage, and Output Security Gate and exceptions. Record each unmet or inapplicable obligation and its disposition.
  Required fields: `reviewer`, `independence`, `source_versions`, `criteria_refs`, `findings`, `verdict`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-dast-control-assurance-5"></a>

## formal security acceptance record

**Handoff content contract:** `handoff/dast-control-assurance:5`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_dast_operational_acceptance`**: For formal security acceptance record, supply the actual versioned dast operational acceptance record, including qualified_scope, review_ref, security_decision, exception_disposition, effective_conditions. Independently assess the evidence against this exact criterion: The decision binds the exact independently reviewed qualification, scope and conditions. Missing or rejected authority blocks acceptance.. Do not substitute a related policy, plan or claimed execution for the required work product and observations. Apply the relevant requirements and evidence criteria in dast-methodology.md: Accountability and decision rights and Implementation lifecycle (A6). Record each unmet or inapplicable obligation and its disposition.
  Required fields: `qualified_scope`, `review_ref`, `security_decision`, `exception_disposition`, `effective_conditions`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `integration`.

**Producer:** `engagement:named-authority`; **receiver:** `engagement:named-authority`.

**Receiving condition:** The decision binds the exact independently reviewed qualification, scope and conditions. Missing or rejected authority blocks acceptance.

**Next:** Step 19.

**Role output contracts:** Source-owned handoff only.

- **`handoff_dast_operational_acceptance`**: For formal security acceptance record, supply the actual versioned dast operational acceptance record, including qualified_scope, review_ref, security_decision, exception_disposition, effective_conditions. Independently assess the evidence against this exact criterion: The decision binds the exact independently reviewed qualification, scope and conditions. Missing or rejected authority blocks acceptance.. Do not substitute a related policy, plan or claimed execution for the required work product and observations. Apply the relevant requirements and evidence criteria in dast-methodology.md: Accountability and decision rights and Implementation lifecycle (A6). Record each unmet or inapplicable obligation and its disposition.
  Required fields: `qualified_scope`, `review_ref`, `security_decision`, `exception_disposition`, `effective_conditions`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `qualification`.

**Producer:** `engagement:named-authority`; **receiver:** `engagement:named-authority`.

**Receiving condition:** The decision binds the exact independently reviewed qualification, scope and conditions. Missing or rejected authority blocks acceptance.

**Next:** Step 19.

**Role output contracts:** Source-owned handoff only.

- **`handoff_dast_operational_acceptance`**: For formal security acceptance record, supply the actual versioned dast operational acceptance record, including qualified_scope, review_ref, security_decision, exception_disposition, effective_conditions. Independently assess the evidence against this exact criterion: The decision binds the exact independently reviewed qualification, scope and conditions. Missing or rejected authority blocks acceptance.. Do not substitute a related policy, plan or claimed execution for the required work product and observations. Apply the relevant requirements and evidence criteria in dast-methodology.md: Accountability and decision rights and Implementation lifecycle (A6). Record each unmet or inapplicable obligation and its disposition.
  Required fields: `qualified_scope`, `review_ref`, `security_decision`, `exception_disposition`, `effective_conditions`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-dast-control-assurance-5"></a>

## formal security acceptance record

**Producer:** Named authority.

**Basis:** JAI-authored source handoff practice; supplements the existing workflow gate without granting authority.

### Required information (MUST)

- Bind formal security acceptance to the exact qualification, independent review, policy and application scope.
- Record the named security authority decision and effective conditions before operational takeover.

### Conditionally required information

- **When:** A permitted exception is relied upon. **Required:** Reference the exact current governance decision and separate risk acceptance.

### Optional information (MAY)


**Receiving condition:** The decision binds the exact independently reviewed qualification, scope and conditions. Missing or rejected authority blocks acceptance.

Unknown applicability and missing evidence remain explicit gaps. A proposed contract, a drafted decision or a successful rendition grants no acceptance or release permission.

<a id="output-handoff-dast-control-assurance-6"></a>

## release evidence assessment

**Handoff content contract:** `handoff/dast-control-assurance:6`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_dast_release_evidence`**: For release evidence assessment, supply the actual versioned dast release evidence record, including qualification_ref, candidate_manifest, observed_deployment, run_refs, evidence_integrity, validity, coverage, policy_compliance, findings. Independently assess the evidence against this exact criterion: Evidence must bind the observed deployment, approved profile, identity, run and policy to the exact candidate. Missing, stale, out-of-scope or untrusted evidence cannot support ordinary promotion.. Do not substitute a related policy, plan or claimed execution for the required work product and observations. Apply the relevant requirements and evidence criteria in dast-methodology.md: Recurring execution and evidence handoff and Qualification and coverage. Record each unmet or inapplicable obligation and its disposition.
  Required fields: `qualification_ref`, `candidate_manifest`, `observed_deployment`, `run_refs`, `evidence_integrity`, `validity`, `coverage`, `policy_compliance`, `findings`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `release-evidence`.

**Producer:** `control-owner`; **receiver:** `engagement:named-authority`.

**Receiving condition:** Evidence must bind the observed deployment, approved profile, identity, run and policy to the exact candidate. Missing, stale, out-of-scope or untrusted evidence cannot support ordinary promotion.

**Next:** Step 7.

**Role output contracts:** `control-owner:2`.

- **`handoff_dast_release_evidence`**: For release evidence assessment, supply the actual versioned dast release evidence record, including qualification_ref, candidate_manifest, observed_deployment, run_refs, evidence_integrity, validity, coverage, policy_compliance, findings. Independently assess the evidence against this exact criterion: Evidence must bind the observed deployment, approved profile, identity, run and policy to the exact candidate. Missing, stale, out-of-scope or untrusted evidence cannot support ordinary promotion.. Do not substitute a related policy, plan or claimed execution for the required work product and observations. Apply the relevant requirements and evidence criteria in dast-methodology.md: Recurring execution and evidence handoff and Qualification and coverage. Record each unmet or inapplicable obligation and its disposition.
  Required fields: `qualification_ref`, `candidate_manifest`, `observed_deployment`, `run_refs`, `evidence_integrity`, `validity`, `coverage`, `policy_compliance`, `findings`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-dast-control-assurance-7"></a>

## DAST gate and release authority record

**Handoff content contract:** `handoff/dast-control-assurance:7`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_dast_release_decision`**: For DAST gate and release authority record, supply the actual versioned dast release decision record, including candidate_manifest, evidence_ref, policy_ref, gate_result, exception_disposition, release_authority_ref. Independently assess the evidence against this exact criterion: Untrusted evidence and non-waivable failures block. Any permitted exception is exact, current and sufficient. Promotion requires the verified release decision and all mandatory controls.. Do not substitute a related policy, plan or claimed execution for the required work product and observations. Apply the relevant requirements and evidence criteria in dast-methodology.md: Output Security Gate and exceptions. Record each unmet or inapplicable obligation and its disposition.
  Required fields: `candidate_manifest`, `evidence_ref`, `policy_ref`, `gate_result`, `exception_disposition`, `release_authority_ref`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `release-evidence`.

**Producer:** `engagement:named-authority`; **receiver:** `engagement:named-authority`.

**Receiving condition:** Untrusted evidence and non-waivable failures block. Any permitted exception is exact, current and sufficient. Promotion requires the verified release decision and all mandatory controls.

**Next:** Terminal disposition; no downstream step.

**Role output contracts:** Source-owned handoff only.

- **`handoff_dast_release_decision`**: For DAST gate and release authority record, supply the actual versioned dast release decision record, including candidate_manifest, evidence_ref, policy_ref, gate_result, exception_disposition, release_authority_ref. Independently assess the evidence against this exact criterion: Untrusted evidence and non-waivable failures block. Any permitted exception is exact, current and sufficient. Promotion requires the verified release decision and all mandatory controls.. Do not substitute a related policy, plan or claimed execution for the required work product and observations. Apply the relevant requirements and evidence criteria in dast-methodology.md: Output Security Gate and exceptions. Record each unmet or inapplicable obligation and its disposition.
  Required fields: `candidate_manifest`, `evidence_ref`, `policy_ref`, `gate_result`, `exception_disposition`, `release_authority_ref`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-dast-control-assurance-7"></a>

## DAST gate and release authority record

**Producer:** Named authority.

**Basis:** JAI-authored source handoff practice; supplements the existing workflow gate without granting authority.

### Required information (MUST)

- Reference the exact release manifest, assessed evidence and protected gate decision under the applicable policy revision.
- Record the actual release authority decision and confirm the other mandatory release controls. Untrusted evidence or a non-waivable failure blocks promotion.

### Conditionally required information

- **When:** The gate relies on an exception. **Required:** Show authority, scope and validity for each affected finding or control requirement; retain the original technical status.

### Optional information (MAY)


**Receiving condition:** Untrusted evidence and non-waivable failures block. Any permitted exception is exact, current and sufficient. Promotion requires the verified release decision and all mandatory controls.

Unknown applicability and missing evidence remain explicit gaps. A proposed contract, a drafted decision or a successful rendition grants no acceptance or release permission.

<a id="output-handoff-dast-control-assurance-8"></a>

## continuous assurance disposition

**Handoff content contract:** `handoff/dast-control-assurance:8`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_dast_assurance`**: For continuous assurance disposition, supply the actual versioned dast assurance record, including qualification_ref, review_period, operating_metrics, drift_events, remediation_owners, requalification_scope, disposition. Independently assess the evidence against this exact criterion: Material changes invalidate affected evidence where required and return impacted scope to qualification. Follow-up has accountable owners and review dates.. Do not substitute a related policy, plan or claimed execution for the required work product and observations. Apply the relevant requirements and evidence criteria in dast-methodology.md: Remediation and operating assurance. Record each unmet or inapplicable obligation and its disposition.
  Required fields: `qualification_ref`, `review_period`, `operating_metrics`, `drift_events`, `remediation_owners`, `requalification_scope`, `disposition`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `continuous-assurance`.

**Producer:** `control-owner`; **receiver:** `engagement:named-authority`.

**Receiving condition:** Material changes invalidate affected evidence where required and return impacted scope to qualification. Follow-up has accountable owners and review dates.

**Next:** Terminal disposition; no downstream step.

**Role output contracts:** `control-owner:2`.

- **`handoff_dast_assurance`**: For continuous assurance disposition, supply the actual versioned dast assurance record, including qualification_ref, review_period, operating_metrics, drift_events, remediation_owners, requalification_scope, disposition. Independently assess the evidence against this exact criterion: Material changes invalidate affected evidence where required and return impacted scope to qualification. Follow-up has accountable owners and review dates.. Do not substitute a related policy, plan or claimed execution for the required work product and observations. Apply the relevant requirements and evidence criteria in dast-methodology.md: Remediation and operating assurance. Record each unmet or inapplicable obligation and its disposition.
  Required fields: `qualification_ref`, `review_period`, `operating_metrics`, `drift_events`, `remediation_owners`, `requalification_scope`, `disposition`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-dast-control-assurance-9"></a>

## integration mandate

**Handoff content contract:** `handoff/dast-control-assurance:9`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_dast_mandate`**: For integration mandate, supply the actual versioned dast mandate record, including application_scope, pipeline_revision, mandate_ref, resources, policy_ref, accountable_owners. Independently assess the evidence against this exact criterion: A named application owner authorises the bounded change. Policy, scope, risk ownership and available resources are explicit.. Do not substitute a related policy, plan or claimed execution for the required work product and observations. Apply the relevant requirements and evidence criteria in dast-methodology.md: Accountability and decision rights and Implementation lifecycle (A0). Record each unmet or inapplicable obligation and its disposition.
  Required fields: `application_scope`, `pipeline_revision`, `mandate_ref`, `resources`, `policy_ref`, `accountable_owners`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `integration`.

**Producer:** `engagement:named-authority`; **receiver:** `solution-architect`.

**Receiving condition:** A named application owner authorises the bounded change. Policy, scope, risk ownership and available resources are explicit.

**Next:** Step 1.

**Role output contracts:** Source-owned handoff only.

- **`handoff_dast_mandate`**: For integration mandate, supply the actual versioned dast mandate record, including application_scope, pipeline_revision, mandate_ref, resources, policy_ref, accountable_owners. Independently assess the evidence against this exact criterion: A named application owner authorises the bounded change. Policy, scope, risk ownership and available resources are explicit.. Do not substitute a related policy, plan or claimed execution for the required work product and observations. Apply the relevant requirements and evidence criteria in dast-methodology.md: Accountability and decision rights and Implementation lifecycle (A0). Record each unmet or inapplicable obligation and its disposition.
  Required fields: `application_scope`, `pipeline_revision`, `mandate_ref`, `resources`, `policy_ref`, `accountable_owners`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-dast-control-assurance-9"></a>

## integration mandate

**Producer:** Named authority.

**Basis:** JAI-authored source handoff practice; supplements the existing workflow gate without granting authority.

### Required information (MUST)

- Record exact application and existing pipeline scope, the named application owner mandate, delivery ownership, funding and capacity.
- Identify applicable policy, accountable authorities and integration bounds.

### Conditionally required information


### Optional information (MAY)


**Receiving condition:** A named application owner authorises the bounded change. Policy, scope, risk ownership and available resources are explicit.

Unknown applicability and missing evidence remain explicit gaps. A proposed contract, a drafted decision or a successful rendition grants no acceptance or release permission.

<a id="output-handoff-dast-control-assurance-10"></a>

## reviewed integration design and implementation backlog

**Handoff content contract:** `handoff/dast-control-assurance:10`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_dast_integration_design`**: For reviewed integration design and implementation backlog, supply the actual versioned dast integration design record, including readiness_ref, requirements_ref, topology_decision, feasibility_evidence, design_review, implementation_backlog, qualification_plan. Independently assess the evidence against this exact criterion: The design binds readiness and requirements to a deployment decision, representative test environment, specific implementation changes and qualification plan. Critical uncertainties have observed feasibility evidence.. Do not substitute a related policy, plan or claimed execution for the required work product and observations. Apply the relevant requirements and evidence criteria in dast-methodology.md: Deployment patterns and fidelity and Qualification and coverage. Record each unmet or inapplicable obligation and its disposition.
  Required fields: `readiness_ref`, `requirements_ref`, `topology_decision`, `feasibility_evidence`, `design_review`, `implementation_backlog`, `qualification_plan`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `integration`.

**Producer:** `solution-architect`; **receiver:** `software-engineer`.

**Receiving condition:** The design binds readiness and requirements to a deployment decision, representative test environment, specific implementation changes and qualification plan. Critical uncertainties have observed feasibility evidence.

**Next:** Step 11.

**Role output contracts:** `solution-architect:4`.

- **`handoff_dast_integration_design`**: For reviewed integration design and implementation backlog, supply the actual versioned dast integration design record, including readiness_ref, requirements_ref, topology_decision, feasibility_evidence, design_review, implementation_backlog, qualification_plan. Independently assess the evidence against this exact criterion: The design binds readiness and requirements to a deployment decision, representative test environment, specific implementation changes and qualification plan. Critical uncertainties have observed feasibility evidence.. Do not substitute a related policy, plan or claimed execution for the required work product and observations. Apply the relevant requirements and evidence criteria in dast-methodology.md: Deployment patterns and fidelity and Qualification and coverage. Record each unmet or inapplicable obligation and its disposition.
  Required fields: `readiness_ref`, `requirements_ref`, `topology_decision`, `feasibility_evidence`, `design_review`, `implementation_backlog`, `qualification_plan`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-dast-control-assurance-11"></a>

## reviewed application changes

**Handoff content contract:** `handoff/dast-control-assurance:11`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_dast_application_change`**: For reviewed application changes, supply the actual versioned dast application change record, including design_ref, application_revision, change_disposition, readiness_tests, fixture_isolation, peer_review. Independently assess the evidence against this exact criterion: Application revision and tests are recorded. Release authentication and authorisation remain effective and test fixtures are isolated.. Do not substitute a related policy, plan or claimed execution for the required work product and observations. Apply the relevant requirements and evidence criteria in dast-methodology.md: Implementation lifecycle (Application workstream) and Typical testability changes. Record each unmet or inapplicable obligation and its disposition.
  Required fields: `design_ref`, `application_revision`, `change_disposition`, `readiness_tests`, `fixture_isolation`, `peer_review`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `integration`.

**Producer:** `software-engineer`; **receiver:** `network-engineer`.

**Receiving condition:** Application revision and tests are recorded. Release authentication and authorisation remain effective and test fixtures are isolated.

**Next:** Step 12.

**Role output contracts:** `software-engineer:1`.

- **`handoff_dast_application_change`**: For reviewed application changes, supply the actual versioned dast application change record, including design_ref, application_revision, change_disposition, readiness_tests, fixture_isolation, peer_review. Independently assess the evidence against this exact criterion: Application revision and tests are recorded. Release authentication and authorisation remain effective and test fixtures are isolated.. Do not substitute a related policy, plan or claimed execution for the required work product and observations. Apply the relevant requirements and evidence criteria in dast-methodology.md: Implementation lifecycle (Application workstream) and Typical testability changes. Record each unmet or inapplicable obligation and its disposition.
  Required fields: `design_ref`, `application_revision`, `change_disposition`, `readiness_tests`, `fixture_isolation`, `peer_review`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-dast-control-assurance-12"></a>

## isolated environment evidence

**Handoff content contract:** `handoff/dast-control-assurance:12`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_dast_environment`**: For isolated environment evidence, supply the actual versioned dast environment record, including design_ref, environment_revision, network_controls, isolation_results, teardown_results. Independently assess the evidence against this exact criterion: The environment revision identifies approved connectivity, blocked destinations, resource limits, concurrency isolation and teardown results.. Do not substitute a related policy, plan or claimed execution for the required work product and observations. Apply the relevant requirements and evidence criteria in dast-methodology.md: Deployment patterns and fidelity and the isolation and concurrency qualification cases. Record each unmet or inapplicable obligation and its disposition.
  Required fields: `design_ref`, `environment_revision`, `network_controls`, `isolation_results`, `teardown_results`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `integration`.

**Producer:** `network-engineer`; **receiver:** `identity-and-access-management-engineer`.

**Receiving condition:** The environment revision identifies approved connectivity, blocked destinations, resource limits, concurrency isolation and teardown results.

**Next:** Step 13.

**Role output contracts:** `network-engineer:2`.

- **`handoff_dast_environment`**: For isolated environment evidence, supply the actual versioned dast environment record, including design_ref, environment_revision, network_controls, isolation_results, teardown_results. Independently assess the evidence against this exact criterion: The environment revision identifies approved connectivity, blocked destinations, resource limits, concurrency isolation and teardown results.. Do not substitute a related policy, plan or claimed execution for the required work product and observations. Apply the relevant requirements and evidence criteria in dast-methodology.md: Deployment patterns and fidelity and the isolation and concurrency qualification cases. Record each unmet or inapplicable obligation and its disposition.
  Required fields: `design_ref`, `environment_revision`, `network_controls`, `isolation_results`, `teardown_results`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-dast-control-assurance-13"></a>

## test identity lifecycle evidence

**Handoff content contract:** `handoff/dast-control-assurance:13`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_dast_identities`**: For test identity lifecycle evidence, supply the actual versioned dast identities record, including design_ref, identity_revision, role_mapping, protected_delivery, lifecycle_results. Independently assess the evidence against this exact criterion: Required identities and roles are scoped, credential material stays out of records, and issue, expiry and revocation have observed evidence.. Do not substitute a related policy, plan or claimed execution for the required work product and observations. Apply the relevant requirements and evidence criteria in dast-methodology.md: Implementation lifecycle (IAM workstream) and identity qualification criteria AC-03 and AC-04. Record each unmet or inapplicable obligation and its disposition.
  Required fields: `design_ref`, `identity_revision`, `role_mapping`, `protected_delivery`, `lifecycle_results`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `integration`.

**Producer:** `identity-and-access-management-engineer`; **receiver:** `container-platform-engineer`.

**Receiving condition:** Required identities and roles are scoped, credential material stays out of records, and issue, expiry and revocation have observed evidence.

**Next:** Step 14.

**Role output contracts:** `identity-and-access-management-engineer:1`.

- **`handoff_dast_identities`**: For test identity lifecycle evidence, supply the actual versioned dast identities record, including design_ref, identity_revision, role_mapping, protected_delivery, lifecycle_results. Independently assess the evidence against this exact criterion: Required identities and roles are scoped, credential material stays out of records, and issue, expiry and revocation have observed evidence.. Do not substitute a related policy, plan or claimed execution for the required work product and observations. Apply the relevant requirements and evidence criteria in dast-methodology.md: Implementation lifecycle (IAM workstream) and identity qualification criteria AC-03 and AC-04. Record each unmet or inapplicable obligation and its disposition.
  Required fields: `design_ref`, `identity_revision`, `role_mapping`, `protected_delivery`, `lifecycle_results`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-dast-control-assurance-14"></a>

## approved scanner platform baseline

**Handoff content contract:** `handoff/dast-control-assurance:14`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_dast_platform`**: For approved scanner platform baseline, supply the actual versioned dast platform record, including design_ref, image_digest, dependency_inventory, provenance, hardening_evidence, lifecycle_owner. Independently assess the evidence against this exact criterion: The recorded platform is reproducible and isolated. Its immutable identity and lifecycle ownership are explicit.. Do not substitute a related policy, plan or claimed execution for the required work product and observations. Apply the relevant requirements and evidence criteria in dast-methodology.md: Deployment patterns and fidelity and Remediation and operating assurance (platform lifecycle). Record each unmet or inapplicable obligation and its disposition.
  Required fields: `design_ref`, `image_digest`, `dependency_inventory`, `provenance`, `hardening_evidence`, `lifecycle_owner`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `integration`.

**Producer:** `container-platform-engineer`; **receiver:** `control-owner`.

**Receiving condition:** The recorded platform is reproducible and isolated. Its immutable identity and lifecycle ownership are explicit.

**Next:** Step 15.

**Role output contracts:** `container-platform-engineer:1`.

- **`handoff_dast_platform`**: For approved scanner platform baseline, supply the actual versioned dast platform record, including design_ref, image_digest, dependency_inventory, provenance, hardening_evidence, lifecycle_owner. Independently assess the evidence against this exact criterion: The recorded platform is reproducible and isolated. Its immutable identity and lifecycle ownership are explicit.. Do not substitute a related policy, plan or claimed execution for the required work product and observations. Apply the relevant requirements and evidence criteria in dast-methodology.md: Deployment patterns and fidelity and Remediation and operating assurance (platform lifecycle). Record each unmet or inapplicable obligation and its disposition.
  Required fields: `design_ref`, `image_digest`, `dependency_inventory`, `provenance`, `hardening_evidence`, `lifecycle_owner`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-dast-control-assurance-15"></a>

## control profile and evidence interface baseline

**Handoff content contract:** `handoff/dast-control-assurance:15`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_dast_control_interface`**: For control profile and evidence interface baseline, supply the actual versioned dast control interface record, including design_ref, profile_ref, coverage_matrix, validity_rules, evidence_schema, complementary_controls. Independently assess the evidence against this exact criterion: Approved profile and scope revisions are traceable to mandatory scenarios, qualified measurement and complementary controls. Missing coverage has an explicit disposition.. Do not substitute a related policy, plan or claimed execution for the required work product and observations. Apply the relevant requirements and evidence criteria in dast-methodology.md: Qualification and coverage and Recurring execution and evidence handoff. Record each unmet or inapplicable obligation and its disposition.
  Required fields: `design_ref`, `profile_ref`, `coverage_matrix`, `validity_rules`, `evidence_schema`, `complementary_controls`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `integration`.

**Producer:** `control-owner`; **receiver:** `ci-cd-platform-engineer`.

**Receiving condition:** Approved profile and scope revisions are traceable to mandatory scenarios, qualified measurement and complementary controls. Missing coverage has an explicit disposition.

**Next:** Step 16.

**Role output contracts:** `control-owner:1`.

- **`handoff_dast_control_interface`**: For control profile and evidence interface baseline, supply the actual versioned dast control interface record, including design_ref, profile_ref, coverage_matrix, validity_rules, evidence_schema, complementary_controls. Independently assess the evidence against this exact criterion: Approved profile and scope revisions are traceable to mandatory scenarios, qualified measurement and complementary controls. Missing coverage has an explicit disposition.. Do not substitute a related policy, plan or claimed execution for the required work product and observations. Apply the relevant requirements and evidence criteria in dast-methodology.md: Qualification and coverage and Recurring execution and evidence handoff. Record each unmet or inapplicable obligation and its disposition.
  Required fields: `design_ref`, `profile_ref`, `coverage_matrix`, `validity_rules`, `evidence_schema`, `complementary_controls`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-dast-control-assurance-16"></a>

## reviewed pipeline evidence integration

**Handoff content contract:** `handoff/dast-control-assurance:16`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_dast_pipeline_integration`**: For reviewed pipeline evidence integration, supply the actual versioned dast pipeline integration record, including design_ref, prerequisite_revisions, pipeline_revision, candidate_binding, report_intake, cleanup_results, integration_tests, peer_review. Independently assess the evidence against this exact criterion: Versioned pipeline changes bind evidence to the actual candidate and observed deployment. Synthetic tests demonstrate error handling, cleanup and tamper rejection. The intake is tested against the exact environment, identity, platform and control interface revisions.. Do not substitute a related policy, plan or claimed execution for the required work product and observations. Apply the relevant requirements and evidence criteria in dast-methodology.md: Recurring execution and evidence handoff and Implementation lifecycle (Pipeline workstream). Record each unmet or inapplicable obligation and its disposition.
  Required fields: `design_ref`, `prerequisite_revisions`, `pipeline_revision`, `candidate_binding`, `report_intake`, `cleanup_results`, `integration_tests`, `peer_review`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `integration`.

**Producer:** `ci-cd-platform-engineer`; **receiver:** `release-engineer`.

**Receiving condition:** Versioned pipeline changes bind evidence to the actual candidate and observed deployment. Synthetic tests demonstrate error handling, cleanup and tamper rejection. The intake is tested against the exact environment, identity, platform and control interface revisions.

**Next:** Step 17.

**Role output contracts:** `ci-cd-platform-engineer:1`.

- **`handoff_dast_pipeline_integration`**: For reviewed pipeline evidence integration, supply the actual versioned dast pipeline integration record, including design_ref, prerequisite_revisions, pipeline_revision, candidate_binding, report_intake, cleanup_results, integration_tests, peer_review. Independently assess the evidence against this exact criterion: Versioned pipeline changes bind evidence to the actual candidate and observed deployment. Synthetic tests demonstrate error handling, cleanup and tamper rejection. The intake is tested against the exact environment, identity, platform and control interface revisions.. Do not substitute a related policy, plan or claimed execution for the required work product and observations. Apply the relevant requirements and evidence criteria in dast-methodology.md: Recurring execution and evidence handoff and Implementation lifecycle (Pipeline workstream). Record each unmet or inapplicable obligation and its disposition.
  Required fields: `design_ref`, `prerequisite_revisions`, `pipeline_revision`, `candidate_binding`, `report_intake`, `cleanup_results`, `integration_tests`, `peer_review`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-dast-control-assurance-17"></a>

## protected release gate implementation

**Handoff content contract:** `handoff/dast-control-assurance:17`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_dast_gate_implementation`**: For protected release gate implementation, supply the actual versioned dast gate implementation record, including pipeline_ref, gate_revision, policy_ref, enforcement_tests, exception_checks, release_boundary. Independently assess the evidence against this exact criterion: The gate evidence shows exact candidate binding, blocked promotion for failed prerequisites, validated exceptions and separate release authority.. Do not substitute a related policy, plan or claimed execution for the required work product and observations. Apply the relevant requirements and evidence criteria in dast-methodology.md: Output Security Gate and exceptions and the enforcement qualification cases. Record each unmet or inapplicable obligation and its disposition.
  Required fields: `pipeline_ref`, `gate_revision`, `policy_ref`, `enforcement_tests`, `exception_checks`, `release_boundary`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `integration`.

**Producer:** `release-engineer`; **receiver:** `test-manager`.

**Receiving condition:** The gate evidence shows exact candidate binding, blocked promotion for failed prerequisites, validated exceptions and separate release authority.

**Next:** Step 18.

**Role output contracts:** `release-engineer:3`.

- **`handoff_dast_gate_implementation`**: For protected release gate implementation, supply the actual versioned dast gate implementation record, including pipeline_ref, gate_revision, policy_ref, enforcement_tests, exception_checks, release_boundary. Independently assess the evidence against this exact criterion: The gate evidence shows exact candidate binding, blocked promotion for failed prerequisites, validated exceptions and separate release authority.. Do not substitute a related policy, plan or claimed execution for the required work product and observations. Apply the relevant requirements and evidence criteria in dast-methodology.md: Output Security Gate and exceptions and the enforcement qualification cases. Record each unmet or inapplicable obligation and its disposition.
  Required fields: `pipeline_ref`, `gate_revision`, `policy_ref`, `enforcement_tests`, `exception_checks`, `release_boundary`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-dast-control-assurance-18"></a>

## system and negative integration qualification

**Handoff content contract:** `handoff/dast-control-assurance:18`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_dast_system_qualification`**: For system and negative integration qualification, supply the actual versioned dast system qualification record, including plan_ref, workstream_refs, tested_versions, positive_results, negative_results, traceability, verdict. Independently assess the evidence against this exact criterion: Every applicable workstream has completion evidence and applicable requirements trace to tests. Unresolved integration failures block acceptance.. Do not substitute a related policy, plan or claimed execution for the required work product and observations. Apply the relevant requirements and evidence criteria in dast-methodology.md: Qualification and coverage and Security requirements catalogue. Record each unmet or inapplicable obligation and its disposition.
  Required fields: `plan_ref`, `workstream_refs`, `tested_versions`, `positive_results`, `negative_results`, `traceability`, `verdict`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `integration`.

**Producer:** `test-manager`; **receiver:** `control-owner`.

**Receiving condition:** Every applicable workstream has completion evidence and applicable requirements trace to tests. Unresolved integration failures block acceptance.

**Next:** Step 3.

**Role output contracts:** `test-manager:2`.

- **`handoff_dast_system_qualification`**: For system and negative integration qualification, supply the actual versioned dast system qualification record, including plan_ref, workstream_refs, tested_versions, positive_results, negative_results, traceability, verdict. Independently assess the evidence against this exact criterion: Every applicable workstream has completion evidence and applicable requirements trace to tests. Unresolved integration failures block acceptance.. Do not substitute a related policy, plan or claimed execution for the required work product and observations. Apply the relevant requirements and evidence criteria in dast-methodology.md: Qualification and coverage and Security requirements catalogue. Record each unmet or inapplicable obligation and its disposition.
  Required fields: `plan_ref`, `workstream_refs`, `tested_versions`, `positive_results`, `negative_results`, `traceability`, `verdict`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-dast-control-assurance-19"></a>

## operational takeover decision and lifecycle handoff

**Handoff content contract:** `handoff/dast-control-assurance:19`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_dast_takeover`**: For operational takeover decision and lifecycle handoff, supply the actual versioned dast takeover record, including acceptance_ref, takeover_decision, qualified_scope, runbook_ref, owner_register, monitoring_plan, requalification_plan. Independently assess the evidence against this exact criterion: The signed takeover binds the accepted scope to runbooks, support ownership, metrics, remediation and requalification triggers.. Do not substitute a related policy, plan or claimed execution for the required work product and observations. Apply the relevant requirements and evidence criteria in dast-methodology.md: Implementation lifecycle (A7), Remediation and operating assurance, and Example and completion. Record each unmet or inapplicable obligation and its disposition.
  Required fields: `acceptance_ref`, `takeover_decision`, `qualified_scope`, `runbook_ref`, `owner_register`, `monitoring_plan`, `requalification_plan`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `integration`.

**Producer:** `engagement:named-authority`; **receiver:** `engagement:named-authority`.

**Receiving condition:** The signed takeover binds the accepted scope to runbooks, support ownership, metrics, remediation and requalification triggers.

**Next:** Terminal disposition; no downstream step.

**Role output contracts:** Source-owned handoff only.

- **`handoff_dast_takeover`**: For operational takeover decision and lifecycle handoff, supply the actual versioned dast takeover record, including acceptance_ref, takeover_decision, qualified_scope, runbook_ref, owner_register, monitoring_plan, requalification_plan. Independently assess the evidence against this exact criterion: The signed takeover binds the accepted scope to runbooks, support ownership, metrics, remediation and requalification triggers.. Do not substitute a related policy, plan or claimed execution for the required work product and observations. Apply the relevant requirements and evidence criteria in dast-methodology.md: Implementation lifecycle (A7), Remediation and operating assurance, and Example and completion. Record each unmet or inapplicable obligation and its disposition.
  Required fields: `acceptance_ref`, `takeover_decision`, `qualified_scope`, `runbook_ref`, `owner_register`, `monitoring_plan`, `requalification_plan`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `qualification`.

**Producer:** `engagement:named-authority`; **receiver:** `engagement:named-authority`.

**Receiving condition:** The signed takeover binds the accepted scope to runbooks, support ownership, metrics, remediation and requalification triggers.

**Next:** Terminal disposition; no downstream step.

**Role output contracts:** Source-owned handoff only.

- **`handoff_dast_takeover`**: For operational takeover decision and lifecycle handoff, supply the actual versioned dast takeover record, including acceptance_ref, takeover_decision, qualified_scope, runbook_ref, owner_register, monitoring_plan, requalification_plan. Independently assess the evidence against this exact criterion: The signed takeover binds the accepted scope to runbooks, support ownership, metrics, remediation and requalification triggers.. Do not substitute a related policy, plan or claimed execution for the required work product and observations. Apply the relevant requirements and evidence criteria in dast-methodology.md: Implementation lifecycle (A7), Remediation and operating assurance, and Example and completion. Record each unmet or inapplicable obligation and its disposition.
  Required fields: `acceptance_ref`, `takeover_decision`, `qualified_scope`, `runbook_ref`, `owner_register`, `monitoring_plan`, `requalification_plan`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-dast-control-assurance-19"></a>

## operational takeover decision and lifecycle handoff

**Producer:** Named authority.

**Basis:** JAI-authored source handoff practice; supplements the existing workflow gate without granting authority.

### Required information (MUST)

- Reference the accepted control baseline and versioned runbook, support responsibilities, follow-up and requalification triggers.
- Record the named application owner decision for the exact qualified scope before closing the integration.

### Conditionally required information


### Optional information (MAY)


**Receiving condition:** The signed takeover binds the accepted scope to runbooks, support ownership, metrics, remediation and requalification triggers.

Unknown applicability and missing evidence remain explicit gaps. A proposed contract, a drafted decision or a successful rendition grants no acceptance or release permission.
<!-- JAI:OUTPUT-CONTRACTS:END -->
