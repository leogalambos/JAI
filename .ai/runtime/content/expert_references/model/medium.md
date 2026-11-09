---
reference_id: example:model:medium
schema_version: '1.0.0'
document_kind: model
complexity: medium
language: en
classification: public-synthetic
provenance: ai-authored-proposed
fictional_context: true
applicable_dcs: kind/model
approval_status: not-human-approved
content_revision: 1.0.0
---

# Model — Meridian Order Integration

**PUBLIC SYNTHETIC TEACHING CASE.** All entities, revisions, values and observations below are invented. Tests are not executed and no professional or human approval is established.

**Boundary:** three services, two teams and a phased cutover. **Illustrative evaluation population:** 1000 synthetic records or requests; this is a proposed scope, not a measured production sample.

<a id="dcs-proposed-model.reference_model_boundary"></a>
## Model Boundary

Repository ea-12 models Order API as an application component and Reserve Stock as an application service in the explicitly selected 3.2 profile. A process and a component are not interchangeable merely because their labels match.

**Acceptance question:** Define metamodel, edition, concern and source baseline.

**Context application:** Separate producer and consumer revisions. Test cross-service failure and reconciliation; one team's success does not establish the next team's acceptance.

<a id="dcs-proposed-model.reference_model_facts"></a>
## Model Facts

Each entity and relation has a stable ID and versioned provenance. The author must check source-concept/relationship/target-concept legality, relation attributes and any junction rules against the selected profile; this narrative does not assert that validation ran.

**Acceptance question:** Provide stable typed entities and legally directed relations.

**Context application:** Separate producer and consumer revisions. Test cross-service failure and reconciliation; one team's success does not establish the next team's acceptance.

<a id="dcs-proposed-model.reference_model_consistency"></a>
## Model Consistency

A proposed dependency cannot support retirement clearance as an observed absence. Reconcile current and target lifecycle states, missing owners and contradictory views; a view is a selection from the model and does not create new facts.

**Acceptance question:** Assess cross-view integrity, lifecycle and open assumptions.

**Context application:** Separate producer and consumer revisions. Test cross-service failure and reconciliation; one team's success does not establish the next team's acceptance.

## Evidence and alternatives

`SYN-INPUT-01` is the fictional requirements and source-revision record. `SYN-TEST-01` is a proposed verification record with status **NOT_EXECUTED**. `SYN-REVIEW-01` is a review request, not a completed review. In a real task, replace these with attributable permitted inputs and observed results.

Compare the bounded baseline with the proposed change using the same business invariant. Retaining the baseline avoids transition exposure but leaves the stated problem unresolved; adopting the change before verification creates an unsupported confidence claim.

## Plausible but incorrect conclusion

A valid XML file proves that all model relationships are meaningful and the architecture is complete.

**Why it fails:** the conclusion skips an evidence or semantic boundary identified in the information sections. A dated, polished artifact cannot repair the missing observation or change the meaning of an interface.

## Reasoned disposition and downstream action

Separate schema validity, metamodel legality and stakeholder-concern completeness. Require explicit review and source evidence before relying on the model for change or retirement.

The source owner supplies missing evidence; an independent competent reviewer assesses the exact revision. The receiving owner records acceptance or required rework. Human approval and release remain separate existing authority acts.

## Professional basis and limitations

Resolve the linked DCS foundation and its professional-source records. Record the source edition, applicability, interpretation, method and evidence for the real engagement. This case is a JAI-authored illustration, not a quotation from or certification against an external standard. Complexity changes the required evidence boundary, not the truth status of fictional facts.
