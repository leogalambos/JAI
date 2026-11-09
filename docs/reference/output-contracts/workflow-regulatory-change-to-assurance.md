<!-- JAI:OUTPUT-CONTRACTS:START -->
# Regulatory change to assurance: source-owned handoff contracts

[Catalogue](index.md)

<a id="output-handoff-regulatory-change-to-assurance-1"></a>

## regulatory change record

**Handoff content contract:** `handoff/regulatory-change-to-assurance:1`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_regulatory_source_change`**: For regulatory change record, supply the actual versioned regulatory source change record, including source_reference, jurisdiction, publication_effective_dates, exact_version, change_summary. Independently assess the evidence against this exact criterion: Source, jurisdiction, dates and version are attributable. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `source_reference`, `jurisdiction`, `publication_effective_dates`, `exact_version`, `change_summary`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `applicable`.

**Producer:** `compliance-officer-technology`; **receiver:** `compliance-officer-technology`.

**Receiving condition:** Source, jurisdiction, dates and version are attributable

**Next:** Step 2.

**Role output contracts:** `compliance-officer-technology:1`.

- **`handoff_regulatory_source_change`**: For regulatory change record, supply the actual versioned regulatory source change record, including source_reference, jurisdiction, publication_effective_dates, exact_version, change_summary. Independently assess the evidence against this exact criterion: Source, jurisdiction, dates and version are attributable. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `source_reference`, `jurisdiction`, `publication_effective_dates`, `exact_version`, `change_summary`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `not-applicable`.

**Producer:** `compliance-officer-technology`; **receiver:** `engagement:regulatory-applicability-owner`.

**Receiving condition:** Source, jurisdiction, dates and version are attributable

**Next:** Step 2.

**Role output contracts:** `compliance-officer-technology:1`.

- **`handoff_regulatory_source_change`**: For regulatory change record, supply the actual versioned regulatory source change record, including source_reference, jurisdiction, publication_effective_dates, exact_version, change_summary. Independently assess the evidence against this exact criterion: Source, jurisdiction, dates and version are attributable. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `source_reference`, `jurisdiction`, `publication_effective_dates`, `exact_version`, `change_summary`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-regulatory-change-to-assurance-2"></a>

## applicability decision

**Handoff content contract:** `handoff/regulatory-change-to-assurance:2`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_regulatory_applicability`**: For applicability decision, supply the actual versioned regulatory applicability record, including scope, in_out_rationale, affected_entities, competent_authority, evidence. Independently assess the evidence against this exact criterion: In/out-of-scope rationale and authority are explicit. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `scope`, `in_out_rationale`, `affected_entities`, `competent_authority`, `evidence`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `applicable`.

**Producer:** `compliance-officer-technology`; **receiver:** `grc-analyst`.

**Receiving condition:** In/out-of-scope rationale and authority are explicit

**Next:** Step 3.

**Role output contracts:** `compliance-officer-technology:2`.

- **`handoff_regulatory_applicability`**: For applicability decision, supply the actual versioned regulatory applicability record, including scope, in_out_rationale, affected_entities, competent_authority, evidence. Independently assess the evidence against this exact criterion: In/out-of-scope rationale and authority are explicit. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `scope`, `in_out_rationale`, `affected_entities`, `competent_authority`, `evidence`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `not-applicable`.

**Producer:** `engagement:regulatory-applicability-owner`; **receiver:** `engagement:named-authority`.

**Receiving condition:** A competent exact-scope decision establishes non-applicability from attributable source/context evidence and defines a review trigger; this closes only the assessed scope and does not fabricate implemented controls.

**Next:** Terminal disposition; no downstream step.

**Role output contracts:** `compliance-officer-technology:2`.

- **`handoff_bounded_nonapplicability_decision`**: A competent exact-scope decision establishes non-applicability from attributable source/context evidence and defines a review trigger; this closes only the assessed scope and does not fabricate implemented controls.
  Required fields: `source_revision`, `jurisdiction`, `assessed_scope`, `exclusion_evidence`, `competent_authority`, `actual_decision`, `change_trigger`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-regulatory-change-to-assurance-3"></a>

## obligations register

**Handoff content contract:** `handoff/regulatory-change-to-assurance:3`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_regulatory_obligations`**: For obligations register, supply the actual versioned regulatory obligations record, including obligation_ids, source_citations, context, applicable_scope, accountable_owner. Independently assess the evidence against this exact criterion: Each obligation retains source citation/context and applicability owner. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `obligation_ids`, `source_citations`, `context`, `applicable_scope`, `accountable_owner`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `applicable`.

**Producer:** `grc-analyst`; **receiver:** `business-analyst`.

**Receiving condition:** Each obligation retains source citation/context and applicability owner

**Next:** Step 4.

**Role output contracts:** `grc-analyst:1`, `grc-analyst:3`.

- **`handoff_regulatory_obligations`**: For obligations register, supply the actual versioned regulatory obligations record, including obligation_ids, source_citations, context, applicable_scope, accountable_owner. Independently assess the evidence against this exact criterion: Each obligation retains source citation/context and applicability owner. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `obligation_ids`, `source_citations`, `context`, `applicable_scope`, `accountable_owner`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-regulatory-change-to-assurance-4"></a>

## requirements baseline

**Handoff content contract:** `handoff/regulatory-change-to-assurance:4`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_regulatory_requirements`**: For requirements baseline, supply the actual versioned regulatory requirements record, including requirement_ids, obligation_refs, preserved_intent, testable_criteria, traceability. Independently assess the evidence against this exact criterion: Requirements preserve obligation intent and are testable. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `requirement_ids`, `obligation_refs`, `preserved_intent`, `testable_criteria`, `traceability`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `applicable`.

**Producer:** `business-analyst`; **receiver:** `control-owner`.

**Receiving condition:** Requirements preserve obligation intent and are testable

**Next:** Step 5.

**Role output contracts:** `business-analyst:1`.

- **`handoff_regulatory_requirements`**: For requirements baseline, supply the actual versioned regulatory requirements record, including requirement_ids, obligation_refs, preserved_intent, testable_criteria, traceability. Independently assess the evidence against this exact criterion: Requirements preserve obligation intent and are testable. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `requirement_ids`, `obligation_refs`, `preserved_intent`, `testable_criteria`, `traceability`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-regulatory-change-to-assurance-5"></a>

## control mapping and gap register

**Handoff content contract:** `handoff/regulatory-change-to-assurance:5`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_obligation_control_mapping`**: For control mapping and gap register, supply the actual versioned obligation control mapping record, including requirement_refs, controls, effectiveness_evidence, gaps, accountable_owners. Independently assess the evidence against this exact criterion: Every requirement maps to effective control evidence or an owned gap. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `requirement_refs`, `controls`, `effectiveness_evidence`, `gaps`, `accountable_owners`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `applicable`.

**Producer:** `control-owner`; **receiver:** `enterprise-architect`.

**Receiving condition:** Every requirement maps to effective control evidence or an owned gap

**Next:** Step 6.

**Role output contracts:** `control-owner:1`, `control-owner:3`.

- **`handoff_obligation_control_mapping`**: For control mapping and gap register, supply the actual versioned obligation control mapping record, including requirement_refs, controls, effectiveness_evidence, gaps, accountable_owners. Independently assess the evidence against this exact criterion: Every requirement maps to effective control evidence or an owned gap. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `requirement_refs`, `controls`, `effectiveness_evidence`, `gaps`, `accountable_owners`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-regulatory-change-to-assurance-6"></a>

## architecture impact assessment

**Handoff content contract:** `handoff/regulatory-change-to-assurance:6`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_regulatory_architecture_impact`**: For architecture impact assessment, supply the actual versioned regulatory architecture impact record, including affected_domains, model_revisions, dependencies, required_changes, constraints. Independently assess the evidence against this exact criterion: Cross-domain impacts and affected governed models are explicit. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `affected_domains`, `model_revisions`, `dependencies`, `required_changes`, `constraints`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `applicable`.

**Producer:** `enterprise-architect`; **receiver:** `portfolio-manager`.

**Receiving condition:** Cross-domain impacts and affected governed models are explicit

**Next:** Step 7.

**Role output contracts:** `enterprise-architect:1`.

- **`handoff_regulatory_architecture_impact`**: For architecture impact assessment, supply the actual versioned regulatory architecture impact record, including affected_domains, model_revisions, dependencies, required_changes, constraints. Independently assess the evidence against this exact criterion: Cross-domain impacts and affected governed models are explicit. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `affected_domains`, `model_revisions`, `dependencies`, `required_changes`, `constraints`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-regulatory-change-to-assurance-7"></a>

## remediation roadmap

**Handoff content contract:** `handoff/regulatory-change-to-assurance:7`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_regulatory_remediation_roadmap`**: For remediation roadmap, supply the actual versioned regulatory remediation roadmap record, including mandatory_deadlines, work_packages, dependencies, funding, owners, escalation. Independently assess the evidence against this exact criterion: Mandatory deadlines and dependencies are funded/owned or escalated. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `mandatory_deadlines`, `work_packages`, `dependencies`, `funding`, `owners`, `escalation`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `applicable`.

**Producer:** `portfolio-manager`; **receiver:** `control-owner`.

**Receiving condition:** Mandatory deadlines and dependencies are funded/owned or escalated

**Next:** Step 8.

**Role output contracts:** `portfolio-manager:1`, `portfolio-manager:2`.

- **`handoff_regulatory_remediation_roadmap`**: For remediation roadmap, supply the actual versioned regulatory remediation roadmap record, including mandatory_deadlines, work_packages, dependencies, funding, owners, escalation. Independently assess the evidence against this exact criterion: Mandatory deadlines and dependencies are funded/owned or escalated. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `mandatory_deadlines`, `work_packages`, `dependencies`, `funding`, `owners`, `escalation`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-regulatory-change-to-assurance-8"></a>

## evidence pack

**Handoff content contract:** `handoff/regulatory-change-to-assurance:8`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_implemented_control_evidence`**: For evidence pack, supply the actual versioned implemented control evidence record, including control_version, operating_period, attributable_evidence, population, exceptions. Independently assess the evidence against this exact criterion: Evidence is attributable to implemented control version and period. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `control_version`, `operating_period`, `attributable_evidence`, `population`, `exceptions`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `applicable`.

**Producer:** `control-owner`; **receiver:** `internal-it-auditor`.

**Receiving condition:** Evidence is attributable to implemented control version and period

**Next:** Step 9.

**Role output contracts:** `control-owner:2`.

- **`handoff_implemented_control_evidence`**: For evidence pack, supply the actual versioned implemented control evidence record, including control_version, operating_period, attributable_evidence, population, exceptions. Independently assess the evidence against this exact criterion: Evidence is attributable to implemented control version and period. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `control_version`, `operating_period`, `attributable_evidence`, `population`, `exceptions`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-regulatory-change-to-assurance-9"></a>

## assurance report

**Handoff content contract:** `handoff/regulatory-change-to-assurance:9`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_regulatory_assurance`**: For assurance report, supply the actual versioned regulatory assurance record, including independent_assessor, scope, criteria, procedures, observations, exceptions, limitations. Independently assess the evidence against this exact criterion: Assurance is independent and reports exceptions/limitations. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `independent_assessor`, `scope`, `criteria`, `procedures`, `observations`, `exceptions`, `limitations`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `applicable`.

**Producer:** `internal-it-auditor`; **receiver:** `compliance-officer-technology`.

**Receiving condition:** Assurance is independent and reports exceptions/limitations

**Next:** Step 10.

**Role output contracts:** `internal-it-auditor:3`.

- **`handoff_regulatory_assurance`**: For assurance report, supply the actual versioned regulatory assurance record, including independent_assessor, scope, criteria, procedures, observations, exceptions, limitations. Independently assess the evidence against this exact criterion: Assurance is independent and reports exceptions/limitations. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `independent_assessor`, `scope`, `criteria`, `procedures`, `observations`, `exceptions`, `limitations`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-handoff-regulatory-change-to-assurance-10"></a>

## closure decision

**Handoff content contract:** `handoff/regulatory-change-to-assurance:10`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_regulatory_closure`**: For closure decision, supply the actual versioned regulatory closure record, including obligation_scope, verification_refs, remaining_exceptions, actual_authority_decision, review_triggers. Independently assess the evidence against this exact criterion: Closure states remaining exceptions, authority and future review triggers. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `obligation_scope`, `verification_refs`, `remaining_exceptions`, `actual_authority_decision`, `review_triggers`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `applicable`.

**Producer:** `compliance-officer-technology`; **receiver:** `engagement:named-authority`.

**Receiving condition:** Closure states remaining exceptions, authority and future review triggers

**Next:** Terminal disposition; no downstream step.

**Role output contracts:** `compliance-officer-technology:2`.

- **`handoff_regulatory_closure`**: For closure decision, supply the actual versioned regulatory closure record, including obligation_scope, verification_refs, remaining_exceptions, actual_authority_decision, review_triggers. Independently assess the evidence against this exact criterion: Closure states remaining exceptions, authority and future review triggers. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `obligation_scope`, `verification_refs`, `remaining_exceptions`, `actual_authority_decision`, `review_triggers`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.
<!-- JAI:OUTPUT-CONTRACTS:END -->
