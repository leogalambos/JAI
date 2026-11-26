<!-- JAI:OUTPUT-CONTRACTS:START -->
# Technical security evidence assessment: source-owned handoff contracts

[Catalogue](index.md)

<a id="output-handoff-technical-security-evidence-assessment-1"></a>

## assessment scope record

**Handoff content contract:** `handoff/technical-security-evidence-assessment:1`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_technical_assessment_scope`**: For assessment scope record, supply the actual versioned technical assessment scope record, including scope_ref, intended_use, subjects, accountable_duties, policy_ref, custody_scope, evidence_availability. Independently assess the evidence against this exact criterion: Scope identifies the exact subjects, intended use, applicable policy, evidence custody limits and available input revisions. Intake is limited to supplied evidence. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `scope_ref`, `intended_use`, `subjects`, `accountable_duties`, `policy_ref`, `custody_scope`, `evidence_availability`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `supplied-evidence`.

**Producer:** `solution-architect`; **receiver:** `security-architect`.

**Receiving condition:** Scope identifies the exact subjects, intended use, applicable policy, evidence custody limits and available input revisions. Intake is limited to supplied evidence

**Next:** Step 2.

**Role output contracts:** Source-owned handoff only.

- **`handoff_technical_assessment_scope`**: For assessment scope record, supply the actual versioned technical assessment scope record, including scope_ref, intended_use, subjects, accountable_duties, policy_ref, custody_scope, evidence_availability. Independently assess the evidence against this exact criterion: Scope identifies the exact subjects, intended use, applicable policy, evidence custody limits and available input revisions. Intake is limited to supplied evidence. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `scope_ref`, `intended_use`, `subjects`, `accountable_duties`, `policy_ref`, `custody_scope`, `evidence_availability`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-technical-security-evidence-assessment-1"></a>

## assessment scope record

**Producer:** Solution Architect.

**Basis:** JAI-authored source handoff practice; supplements the existing workflow gate without granting authority.

### Required information (MUST)

- Identify the exact subjects, system boundary, intended use and accountable platform or application duties.
- Record available evidence revisions, custody and gaps relevant to assessment planning.

### Conditionally required information


### Optional information (MAY)


**Receiving condition:** Scope identifies the exact subjects, intended use, applicable policy, evidence custody limits and available input revisions. Intake is limited to supplied evidence

Unknown applicability and missing evidence remain explicit gaps. A proposed contract, a drafted decision or a successful rendition grants no acceptance or release permission.

<a id="output-handoff-technical-security-evidence-assessment-2"></a>

## assessment plan

**Handoff content contract:** `handoff/technical-security-evidence-assessment:2`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_technical_assessment_plan`**: For assessment plan, supply the actual versioned technical assessment plan record, including plan_ref, scope_ref, assessment_objectives, examination_objects, criteria_refs, method_refs, evidence_requirements, independence_requirements. Independently assess the evidence against this exact criterion: The plan binds each objective to an applicable criterion revision, scope and evidence requirement. Missing method or protocol applicability is recorded as pending for the affected criterion. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `plan_ref`, `scope_ref`, `assessment_objectives`, `examination_objects`, `criteria_refs`, `method_refs`, `evidence_requirements`, `independence_requirements`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `supplied-evidence`.

**Producer:** `security-architect`; **receiver:** `application-security-engineer`.

**Receiving condition:** The plan binds each objective to an applicable criterion revision, scope and evidence requirement. Missing method or protocol applicability is recorded as pending for the affected criterion

**Next:** Step 3.

**Role output contracts:** Source-owned handoff only.

- **`handoff_technical_assessment_plan`**: For assessment plan, supply the actual versioned technical assessment plan record, including plan_ref, scope_ref, assessment_objectives, examination_objects, criteria_refs, method_refs, evidence_requirements, independence_requirements. Independently assess the evidence against this exact criterion: The plan binds each objective to an applicable criterion revision, scope and evidence requirement. Missing method or protocol applicability is recorded as pending for the affected criterion. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `plan_ref`, `scope_ref`, `assessment_objectives`, `examination_objects`, `criteria_refs`, `method_refs`, `evidence_requirements`, `independence_requirements`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-technical-security-evidence-assessment-2"></a>

## assessment plan

**Producer:** Security Architect.

**Basis:** JAI-authored source handoff practice; supplements the existing workflow gate without granting authority.

### Required information (MUST)

- Identify scoped assessment objectives, approved method and criterion revisions, and required evidence objects.
- Include mandatory controls even without an ATT&CK mapping. Record intended coverage and limits.

### Conditionally required information

- **When:** The assessment requires an independent assessor. **Required:** Specify the applicable independence requirement and how it will be validated.

### Optional information (MAY)


**Receiving condition:** The plan binds each objective to an applicable criterion revision, scope and evidence requirement. Missing method or protocol applicability is recorded as pending for the affected criterion

Unknown applicability and missing evidence remain explicit gaps. A proposed contract, a drafted decision or a successful rendition grants no acceptance or release permission.

<a id="output-handoff-technical-security-evidence-assessment-3"></a>

## assessment report

**Handoff content contract:** `handoff/technical-security-evidence-assessment:3`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_technical_assessment_report`**: For assessment report, supply the actual versioned technical assessment report record, including report_ref, plan_ref, scope_ref, evidence_refs, attribution, criterion_outcomes, coverage, limitations, assessed_impact. Independently assess the evidence against this exact criterion: The report identifies the exact plan, method and evidence revisions. Unsupported or missing evidence leaves the affected conclusion indeterminate. Impact is stated only where supported. Assessors meet independence requirements where applicable. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `report_ref`, `plan_ref`, `scope_ref`, `evidence_refs`, `attribution`, `criterion_outcomes`, `coverage`, `limitations`, `assessed_impact`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `supplied-evidence`.

**Producer:** `application-security-engineer`; **receiver:** `control-owner`.

**Receiving condition:** The report identifies the exact plan, method and evidence revisions. Unsupported or missing evidence leaves the affected conclusion indeterminate. Impact is stated only where supported. Assessors meet independence requirements where applicable

**Next:** Step 4.

**Role output contracts:** Source-owned handoff only.

- **`handoff_technical_assessment_report`**: For assessment report, supply the actual versioned technical assessment report record, including report_ref, plan_ref, scope_ref, evidence_refs, attribution, criterion_outcomes, coverage, limitations, assessed_impact. Independently assess the evidence against this exact criterion: The report identifies the exact plan, method and evidence revisions. Unsupported or missing evidence leaves the affected conclusion indeterminate. Impact is stated only where supported. Assessors meet independence requirements where applicable. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `report_ref`, `plan_ref`, `scope_ref`, `evidence_refs`, `attribution`, `criterion_outcomes`, `coverage`, `limitations`, `assessed_impact`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-technical-security-evidence-assessment-3"></a>

## assessment report

**Producer:** Application Security Engineer.

**Basis:** JAI-authored source handoff practice; supplements the existing workflow gate without granting authority.

### Required information (MUST)

- Bind each reported observation and outcome to the exact assessment plan, criterion, method and evidence revisions.
- Report scope, demonstrated coverage, indeterminate criteria and evidentiary limitations. Claim impact only where supported by observation.

### Conditionally required information


### Optional information (MAY)


**Receiving condition:** The report identifies the exact plan, method and evidence revisions. Unsupported or missing evidence leaves the affected conclusion indeterminate. Impact is stated only where supported. Assessors meet independence requirements where applicable

Unknown applicability and missing evidence remain explicit gaps. A proposed contract, a drafted decision or a successful rendition grants no acceptance or release permission.

<a id="output-handoff-technical-security-evidence-assessment-4"></a>

## assessment response record

**Handoff content contract:** `handoff/technical-security-evidence-assessment:4`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_technical_assessment_response`**: For assessment response record, supply the actual versioned technical assessment response record, including report_ref, intended_use, finding_dispositions, accountable_receivers, authority_applicability, referral_outcomes. Independently assess the evidence against this exact criterion: The response identifies the exact report revision, permitted intended use, decisions and accountable recipients. When required, record human disposition and confirm current scoped permission before transfer. Record acknowledgment or a held transfer. Remediation remains with the receiving workflow. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `report_ref`, `intended_use`, `finding_dispositions`, `accountable_receivers`, `authority_applicability`, `referral_outcomes`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `supplied-evidence`.

**Producer:** `control-owner`; **receiver:** `engagement:named-authority`.

**Receiving condition:** The response identifies the exact report revision, permitted intended use, decisions and accountable recipients. When required, record human disposition and confirm current scoped permission before transfer. Record acknowledgment or a held transfer. Remediation remains with the receiving workflow

**Next:** Terminal disposition; no downstream step.

**Role output contracts:** Source-owned handoff only.

- **`handoff_technical_assessment_response`**: For assessment response record, supply the actual versioned technical assessment response record, including report_ref, intended_use, finding_dispositions, accountable_receivers, authority_applicability, referral_outcomes. Independently assess the evidence against this exact criterion: The response identifies the exact report revision, permitted intended use, decisions and accountable recipients. When required, record human disposition and confirm current scoped permission before transfer. Record acknowledgment or a held transfer. Remediation remains with the receiving workflow. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `report_ref`, `intended_use`, `finding_dispositions`, `accountable_receivers`, `authority_applicability`, `referral_outcomes`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-technical-security-evidence-assessment-4"></a>

## assessment response record

**Producer:** Control Owner.

**Basis:** JAI-authored source handoff practice; supplements the existing workflow gate without granting authority.

### Required information (MUST)

- Record response dispositions against the exact assessment report and intended use. Name the receiving duty for each action.
- Retain the attributed acknowledgement or held transfer for each referral.

### Conditionally required information

- **When:** A referral transfers supplied evidence. **Required:** Check current permission for the exact named recipient and scope before transfer. Record a blocked disposition if permission is absent, ambiguous or denied.
- **When:** Engagement policy reserves the disposition to a human. **Required:** Reference the human decision for the exact report and intended use.

### Optional information (MAY)


**Receiving condition:** The response identifies the exact report revision, permitted intended use, decisions and accountable recipients. When required, record human disposition and confirm current scoped permission before transfer. Record acknowledgment or a held transfer. Remediation remains with the receiving workflow

Unknown applicability and missing evidence remain explicit gaps. A proposed contract, a drafted decision or a successful rendition grants no acceptance or release permission.
<!-- JAI:OUTPUT-CONTRACTS:END -->
