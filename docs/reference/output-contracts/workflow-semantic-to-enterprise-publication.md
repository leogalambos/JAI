<!-- JAI:OUTPUT-CONTRACTS:START -->
# Semantic artefact to enterprise publication: source-owned handoff contracts

[Catalogue](index.md)

<a id="output-handoff-semantic-to-enterprise-publication-1"></a>

## semantic publication model

**Handoff content contract:** `handoff/semantic-to-enterprise-publication:1`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_semantic_publication_source`**: For semantic publication model, supply the actual versioned semantic publication source record, including semantic_revision, purpose, audience, claims, evidence, decisions, unresolved_items. Independently assess the evidence against this exact criterion: Semantic source is complete enough to review; unresolved items are explicit. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `semantic_revision`, `purpose`, `audience`, `claims`, `evidence`, `decisions`, `unresolved_items`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `draft`.

**Producer:** `engagement:owning-specialist`; **receiver:** `agent:evidence-rationale-reviewer`.

**Receiving condition:** Semantic source is complete enough to review; unresolved items are explicit

**Next:** Step 2.

**Role output contracts:** Source-owned handoff only.

- **`handoff_semantic_publication_source`**: For semantic publication model, supply the actual versioned semantic publication source record, including semantic_revision, purpose, audience, claims, evidence, decisions, unresolved_items. Independently assess the evidence against this exact criterion: Semantic source is complete enough to review; unresolved items are explicit. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `semantic_revision`, `purpose`, `audience`, `claims`, `evidence`, `decisions`, `unresolved_items`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `release-candidate`.

**Producer:** `engagement:owning-specialist`; **receiver:** `agent:evidence-rationale-reviewer`.

**Receiving condition:** Semantic source is complete enough to review; unresolved items are explicit

**Next:** Step 2.

**Role output contracts:** Source-owned handoff only.

- **`handoff_semantic_publication_source`**: For semantic publication model, supply the actual versioned semantic publication source record, including semantic_revision, purpose, audience, claims, evidence, decisions, unresolved_items. Independently assess the evidence against this exact criterion: Semantic source is complete enough to review; unresolved items are explicit. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `semantic_revision`, `purpose`, `audience`, `claims`, `evidence`, `decisions`, `unresolved_items`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-semantic-to-enterprise-publication-1"></a>

## semantic publication model

**Producer:** Owning specialist.

**Basis:** JAI-authored source handoff practice; supplements the existing workflow gate without granting authority.

### Required information (MUST)

- Identify the exact semantic model version, intended audience, purpose, scope and requested publication formats.
- State claims, decisions, alternatives and rationale; link material claims to evidence and distinguish facts, assumptions and unresolved questions.
- Identify acceptance criteria, source references, classification, disclosure limits and the owners of unresolved items.

### Conditionally required information

- **When:** The publication requests a consequential decision. **Required:** Identify the accountable decision authority, exact decision requested and residual risks requiring disposition.

### Optional information (MAY)

- Supporting calculations and detailed source annexes referenced by material claims.

**Receiving condition:** Semantic source is complete enough to review; unresolved items are explicit

Unknown applicability and missing evidence remain explicit gaps. A proposed contract, a drafted decision or a successful rendition grants no acceptance or release permission.

<a id="output-handoff-semantic-to-enterprise-publication-2"></a>

## semantic gate result and located findings

**Handoff content contract:** `handoff/semantic-to-enterprise-publication:2`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_semantic_review`**: For semantic gate result and located findings, supply the actual versioned semantic review record, including reviewed_revision, criteria, reviewer_independence, located_findings, verdict, required_source_approval. Independently assess the evidence against this exact criterion: Semantic Gate PASS and the exact stable semantic snapshot has its required source approval under the governing profile, including verified external human proof where required, before the editor acts; only an existing expressly permitted prior scoped waiver applies, and mandatory controls remain blocking. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `reviewed_revision`, `criteria`, `reviewer_independence`, `located_findings`, `verdict`, `required_source_approval`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `draft`.

**Producer:** `agent:evidence-rationale-reviewer`; **receiver:** `agent:enterprise-publication-editor`.

**Receiving condition:** Semantic Gate PASS and the exact stable semantic snapshot has its required source approval under the governing profile, including verified external human proof where required, before the editor acts; only an existing expressly permitted prior scoped waiver applies, and mandatory controls remain blocking

**Next:** Step 3.

**Role output contracts:** Source-owned handoff only.

- **`handoff_semantic_review`**: For semantic gate result and located findings, supply the actual versioned semantic review record, including reviewed_revision, criteria, reviewer_independence, located_findings, verdict, required_source_approval. Independently assess the evidence against this exact criterion: Semantic Gate PASS and the exact stable semantic snapshot has its required source approval under the governing profile, including verified external human proof where required, before the editor acts; only an existing expressly permitted prior scoped waiver applies, and mandatory controls remain blocking. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `reviewed_revision`, `criteria`, `reviewer_independence`, `located_findings`, `verdict`, `required_source_approval`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `release-candidate`.

**Producer:** `agent:evidence-rationale-reviewer`; **receiver:** `agent:enterprise-publication-editor`.

**Receiving condition:** Semantic Gate PASS and the exact stable semantic snapshot has its required source approval under the governing profile, including verified external human proof where required, before the editor acts; only an existing expressly permitted prior scoped waiver applies, and mandatory controls remain blocking

**Next:** Step 3.

**Role output contracts:** Source-owned handoff only.

- **`handoff_semantic_review`**: For semantic gate result and located findings, supply the actual versioned semantic review record, including reviewed_revision, criteria, reviewer_independence, located_findings, verdict, required_source_approval. Independently assess the evidence against this exact criterion: Semantic Gate PASS and the exact stable semantic snapshot has its required source approval under the governing profile, including verified external human proof where required, before the editor acts; only an existing expressly permitted prior scoped waiver applies, and mandatory controls remain blocking. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `reviewed_revision`, `criteria`, `reviewer_independence`, `located_findings`, `verdict`, `required_source_approval`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-semantic-to-enterprise-publication-2"></a>

## semantic gate result and located findings

**Producer:** Evidence & Rationale Reviewer.

**Basis:** JAI-authored source handoff practice; supplements the existing workflow gate without granting authority.

### Required information (MUST)

- Identify reviewer, independence, exact source version and the criteria and evidence actually assessed.
- Locate each finding against a claim or criterion; record significance, evidence limits and required resolution.
- State a bounded semantic verdict, unresolved findings and any explicit waiver reference without treating missing evidence as a pass.

### Conditionally required information

- **When:** The governing policy permits a waiver and one is relied upon. **Required:** Reference prior explicit authority for that exact criterion, scope, rationale, limits and expiry where specified; a reviewer cannot create permission to waive a mandatory gate.

### Optional information (MAY)

- Comparative recommendations that do not alter the underlying decision.

**Receiving condition:** Semantic Gate PASS and the exact stable semantic snapshot has its required source approval under the governing profile, including verified external human proof where required, before the editor acts; only an existing expressly permitted prior scoped waiver applies, and mandatory controls remain blocking

Unknown applicability and missing evidence remain explicit gaps. A proposed contract, a drafted decision or a successful rendition grants no acceptance or release permission.

<a id="output-handoff-semantic-to-enterprise-publication-3"></a>

## rendered publication set with semantic hash

**Handoff content contract:** `handoff/semantic-to-enterprise-publication:3`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_rendered_publication`**: For rendered publication set with semantic hash, supply the actual versioned rendered publication record, including semantic_hash, rendered_files, manifest, document_control, projection_limits. Independently assess the evidence against this exact criterion: All outputs carry the same semantic SHA-256 and required document control; draft rendering grants no acceptance or release. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `semantic_hash`, `rendered_files`, `manifest`, `document_control`, `projection_limits`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `draft`.

**Producer:** `agent:enterprise-publication-editor`; **receiver:** `engagement:named-authority`.

**Receiving condition:** All outputs carry the same semantic SHA-256 and required document control; draft rendering grants no acceptance or release

**Next:** Terminal disposition; no downstream step.

**Role output contracts:** Source-owned handoff only.

- **`handoff_rendered_publication`**: For rendered publication set with semantic hash, supply the actual versioned rendered publication record, including semantic_hash, rendered_files, manifest, document_control, projection_limits. Independently assess the evidence against this exact criterion: All outputs carry the same semantic SHA-256 and required document control; draft rendering grants no acceptance or release. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `semantic_hash`, `rendered_files`, `manifest`, `document_control`, `projection_limits`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

**Selected path:** `release-candidate`.

**Producer:** `agent:enterprise-publication-editor`; **receiver:** `agent:visual-quality-reviewer`.

**Receiving condition:** All outputs carry the same semantic SHA-256 and required document control; draft rendering grants no acceptance or release

**Next:** Step 4.

**Role output contracts:** Source-owned handoff only.

- **`handoff_rendered_publication`**: For rendered publication set with semantic hash, supply the actual versioned rendered publication record, including semantic_hash, rendered_files, manifest, document_control, projection_limits. Independently assess the evidence against this exact criterion: All outputs carry the same semantic SHA-256 and required document control; draft rendering grants no acceptance or release. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `semantic_hash`, `rendered_files`, `manifest`, `document_control`, `projection_limits`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-semantic-to-enterprise-publication-3"></a>

## rendered publication set with semantic hash

**Producer:** Enterprise Publication Editor.

**Basis:** JAI-authored source handoff practice; supplements the existing workflow gate without granting authority.

### Required information (MUST)

- Identify the approved semantic input version and digest, selected publication archetype, audience and requested formats.
- Supply the actual rendered files with a manifest linking every rendition to the same semantic source; preserve claims, caveats and decisions.
- Record document identity, classification, references, generation limitations and dependencies needed to reproduce the projection.

### Conditionally required information

- **When:** A required renderer or format is unavailable. **Required:** Identify the missing rendition and blocking limitation; do not claim it was produced or inspected.

### Optional information (MAY)

- Additional audience projections whose semantic equivalence is established.

**Receiving condition:** All outputs carry the same semantic SHA-256 and required document control; draft rendering grants no acceptance or release

Unknown applicability and missing evidence remain explicit gaps. A proposed contract, a drafted decision or a successful rendition grants no acceptance or release permission.

<a id="output-handoff-semantic-to-enterprise-publication-4"></a>

## publication gate result and findings

**Handoff content contract:** `handoff/semantic-to-enterprise-publication:4`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_publication_review`**: For publication gate result and findings, supply the actual versioned publication review record, including inspected_files, methods, reviewer_independence, located_findings, blocking_disposition, verdict. Independently assess the evidence against this exact criterion: Publication Gate PASS with blocking defects resolved; any policy-permitted waiver requires prior named human authority for its exact scope before release or other gated effects; mandatory controls remain blocking. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `inspected_files`, `methods`, `reviewer_independence`, `located_findings`, `blocking_disposition`, `verdict`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `release-candidate`.

**Producer:** `agent:visual-quality-reviewer`; **receiver:** `engagement:named-authority`.

**Receiving condition:** Publication Gate PASS with blocking defects resolved; any policy-permitted waiver requires prior named human authority for its exact scope before release or other gated effects; mandatory controls remain blocking

**Next:** Step 5.

**Role output contracts:** Source-owned handoff only.

- **`handoff_publication_review`**: For publication gate result and findings, supply the actual versioned publication review record, including inspected_files, methods, reviewer_independence, located_findings, blocking_disposition, verdict. Independently assess the evidence against this exact criterion: Publication Gate PASS with blocking defects resolved; any policy-permitted waiver requires prior named human authority for its exact scope before release or other gated effects; mandatory controls remain blocking. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `inspected_files`, `methods`, `reviewer_independence`, `located_findings`, `blocking_disposition`, `verdict`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-semantic-to-enterprise-publication-4"></a>

## publication gate result and findings

**Producer:** Visual Quality Reviewer.

**Basis:** JAI-authored source handoff practice; supplements the existing workflow gate without granting authority.

### Required information (MUST)

- Identify reviewer, exact rendered files, source binding, inspected formats and actual viewing or rendering method.
- Record located findings for legibility, hierarchy, density, tables, diagrams, document control and package integrity.
- State the publication verdict and limitations, defect disposition, and any explicit waiver; distinguish static checks from observed visual inspection.

### Conditionally required information

- **When:** An output format or part of the package could not be inspected. **Required:** Record the missing inspection and its impact; retain the blocked state unless the governing policy permits and the exact authority explicitly approves a scoped disposition before release.

### Optional information (MAY)

- Annotated previews and presentation recommendations supporting the findings.

**Receiving condition:** Publication Gate PASS with blocking defects resolved; any policy-permitted waiver requires prior named human authority for its exact scope before release or other gated effects; mandatory controls remain blocking

Unknown applicability and missing evidence remain explicit gaps. A proposed contract, a drafted decision or a successful rendition grants no acceptance or release permission.

<a id="output-handoff-semantic-to-enterprise-publication-5"></a>

## release approval

**Handoff content contract:** `handoff/semantic-to-enterprise-publication:5`.

**Basis:** JAI-authored exact handoff information; complements the source gate and role obligations without granting authority.

These requirements supplement the linked role output contracts. A related policy or published view does not replace the specific decision or repository/interchange records required here.

### Required information (MUST)

- **`handoff_publication_release_decision`**: For release approval, supply the actual versioned publication release decision record, including exact_version, files, audience, release_scope, prior_reviews, authority, actual_decision. Independently assess the evidence against this exact criterion: Explicit exact human approval precedes release; required independence is preserved; agents cannot approve or issue waivers. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `exact_version`, `files`, `audience`, `release_scope`, `prior_reviews`, `authority`, `actual_decision`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

The existing authenticated receiver reviews each required unit against this exact handoff. A content record alone does not grant acceptance or release.

### Context-selected alternatives

Alternative bindings replace the base obligations for the selected path. Select the path from the reviewed intake context and the workflow operating profile; requirements from other paths are not cumulative.

**Selected path:** `release-candidate`.

**Producer:** `engagement:named-authority`; **receiver:** `engagement:named-authority`.

**Receiving condition:** Explicit exact human approval precedes release; required independence is preserved; agents cannot approve or issue waivers

**Next:** Terminal disposition; no downstream step.

**Role output contracts:** Source-owned handoff only.

- **`handoff_publication_release_decision`**: For release approval, supply the actual versioned publication release decision record, including exact_version, files, audience, release_scope, prior_reviews, authority, actual_decision. Independently assess the evidence against this exact criterion: Explicit exact human approval precedes release; required independence is preserved; agents cannot approve or issue waivers. Do not substitute a related policy, plan or claimed execution for the required work product and observations.
  Required fields: `exact_version`, `files`, `audience`, `release_scope`, `prior_reviews`, `authority`, `actual_decision`.
- **`workflow_context`**: Reference the already-reviewed versioned intake context and selected mechanism variant; identify actual input versions and current continue/rework/stop/exit disposition with evidence. Do not reconstruct unchanged intake or historical decisions. Recheck only mutable prerequisites governing this action; a context reference cannot grant approval.
  Required fields: `context_ref`, `route`, `input_refs`, `route_evidence`.

<a id="output-semantic-to-enterprise-publication-5"></a>

## release approval

**Producer:** Named authority.

**Basis:** JAI-authored source handoff practice; supplements the existing workflow gate without granting authority.

### Required information (MUST)

- Identify the actual accountable authority, exact publication version and files, permitted audience and release scope.
- Reference the applicable semantic and publication reviews, unresolved risks and any authorised conditions or waivers.
- Record the explicit decision and its effective conditions using the existing authority mechanism; a drafted request or agent assertion is not approval.

### Conditionally required information

- **When:** The governing decision requires an L0 signature. **Required:** Reference the actual operator-signed decision bound to these effects; do not manufacture a signature or inherit another output approval.

### Optional information (MAY)

- Communication instructions that stay within the approved audience and scope.

**Receiving condition:** Explicit exact human approval precedes release; required independence is preserved; agents cannot approve or issue waivers

Unknown applicability and missing evidence remain explicit gaps. A proposed contract, a drafted decision or a successful rendition grants no acceptance or release permission.
<!-- JAI:OUTPUT-CONTRACTS:END -->
