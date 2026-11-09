---
reference_id: example:diagram:medium
schema_version: '1.0.0'
document_kind: diagram
complexity: medium
language: en
classification: public-synthetic
provenance: ai-authored-proposed
fictional_context: true
applicable_dcs: kind/diagram
approval_status: not-human-approved
content_revision: 1.0.0
---

# Diagram — Meridian Order Integration

**PUBLIC SYNTHETIC TEACHING CASE.** All entities, revisions, values and observations below are invented. Tests are not executed and no professional or human approval is established.

**Boundary:** three services, two teams and a phased cutover. **Illustrative evaluation population:** 1000 synthetic records or requests; this is a proposed scope, not a measured production sample.

<a id="dcs-proposed-diagram.reference_diagram_question"></a>
## Diagram Question

The operations view answers which dependency can prevent order acceptance. It includes Order API, Stock API and their synchronous call; finance reporting is explicitly outside the view. The legend distinguishes dependency direction from event-flow direction.

**Acceptance question:** Identify audience, concern, boundary and notation so readers can judge whether the view answers its stated question.

**Context application:** Separate producer and consumer revisions. Test cross-service failure and reconciliation; one team's success does not establish the next team's acceptance.

<a id="dcs-proposed-diagram.reference_diagram_source"></a>
## Diagram Source

Node n1 represents svc-orders and n2 represents svc-stock from repository revision ea-12. Relation r1 is a dependency from orders to stock. Reversing an arrow for easier layout must not reverse the model relationship.

**Acceptance question:** Link symbols and relations to stable source facts so reviewers can detect unsupported or stale model statements.

**Context application:** Separate producer and consumer revisions. Test cross-service failure and reconciliation; one team's success does not establish the next team's acceptance.

<a id="dcs-proposed-diagram.reference_diagram_review"></a>
## Diagram Review

A reviewer traces every displayed endpoint to its model ID, checks the declared concern and reads labels at publication scale. A generic graph remains labelled repository-graph unless a qualified notation profile was actually applied.

**Acceptance question:** Assess semantic fidelity, coverage and visual readability.

**Context application:** Separate producer and consumer revisions. Test cross-service failure and reconciliation; one team's success does not establish the next team's acceptance.

## Evidence and alternatives

`SYN-INPUT-01` is the fictional requirements and source-revision record. `SYN-TEST-01` is a proposed verification record with status **NOT_EXECUTED**. `SYN-REVIEW-01` is a review request, not a completed review. In a real task, replace these with attributable permitted inputs and observed results.

Compare the bounded baseline with the proposed change using the same business invariant. Retaining the baseline avoids transition exposure but leaves the stated problem unresolved; adopting the change before verification creates an unsupported confidence claim.

## Plausible but incorrect conclusion

Two coloured boxes connected by an arrow constitute a validated ArchiMate model.

**Why it fails:** the conclusion skips an evidence or semantic boundary identified in the information sections. A dated, polished artifact cannot repair the missing observation or change the meaning of an interface.

## Reasoned disposition and downstream action

Review source semantics, chosen notation and readability separately. Supply missing dependency evidence or a clearer legend before using the view for an operational decision.

The source owner supplies missing evidence; an independent competent reviewer assesses the exact revision. The receiving owner records acceptance or required rework. Human approval and release remain separate existing authority acts.

## Professional basis and limitations

Resolve the linked DCS foundation and its professional-source records. Record the source edition, applicability, interpretation, method and evidence for the real engagement. This case is a JAI-authored illustration, not a quotation from or certification against an external standard. Complexity changes the required evidence boundary, not the truth status of fictional facts.
