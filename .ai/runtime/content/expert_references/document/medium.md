---
reference_id: example:document:medium
schema_version: '1.0.0'
document_kind: document
complexity: medium
language: en
classification: public-synthetic
provenance: ai-authored-proposed
fictional_context: true
applicable_dcs: kind/document
approval_status: not-human-approved
content_revision: 1.0.0
---

# Document — Meridian Order Integration

**PUBLIC SYNTHETIC TEACHING CASE.** All entities, revisions, values and observations below are invented. Tests are not executed and no professional or human approval is established.

**Boundary:** three services, two teams and a phased cutover. **Illustrative evaluation population:** 1000 synthetic records or requests; this is a proposed scope, not a measured production sample.

<a id="dcs-proposed-document.reference_document_question"></a>
## Document Question

The maintainer needs to know whether interface stock-v2 changes retry behaviour. The source set is API schema v2, change src-42 and the owner supplied requirement R-17; undocumented production behaviour is excluded.

**Acceptance question:** State the reader decision, subject and bounded sources.

**Context application:** Separate producer and consumer revisions. Test cross-service failure and reconciliation; one team's success does not establish the next team's acceptance.

<a id="dcs-proposed-document.reference_document_reasoning"></a>
## Document Reasoning

The schema allows an idempotency key but does not prove atomic storage. Compare client-side suppression with server-side transactional uniqueness; only the latter addresses concurrent requests from different clients. Expected behaviour remains a proposed contract until tested.

**Acceptance question:** Link substantive analysis to evidence and alternatives.

**Context application:** Separate producer and consumer revisions. Test cross-service failure and reconciliation; one team's success does not establish the next team's acceptance.

<a id="dcs-proposed-document.reference_document_action"></a>
## Document Action

Ask the API owner to confirm duplicate-response semantics and the database owner to provide concurrency evidence before release. A dated document review records readability and traceability; it cannot manufacture the missing execution result.

**Acceptance question:** Assign a usable conclusion, limitations and follow-up.

**Context application:** Separate producer and consumer revisions. Test cross-service failure and reconciliation; one team's success does not establish the next team's acceptance.

## Evidence and alternatives

`SYN-INPUT-01` is the fictional requirements and source-revision record. `SYN-TEST-01` is a proposed verification record with status **NOT_EXECUTED**. `SYN-REVIEW-01` is a review request, not a completed review. In a real task, replace these with attributable permitted inputs and observed results.

Compare the bounded baseline with the proposed change using the same business invariant. Retaining the baseline avoids transition exposure but leaves the stated problem unresolved; adopting the change before verification creates an unsupported confidence claim.

## Plausible but incorrect conclusion

A signed, complete and well-formatted document proves that the described implementation works.

**Why it fails:** the conclusion skips an evidence or semantic boundary identified in the information sections. A dated, polished artifact cannot repair the missing observation or change the meaning of an interface.

## Reasoned disposition and downstream action

Limit the conclusion to supported design claims and name the missing operational evidence. Preserve the source version so a later change triggers review of affected claims only.

The source owner supplies missing evidence; an independent competent reviewer assesses the exact revision. The receiving owner records acceptance or required rework. Human approval and release remain separate existing authority acts.

## Professional basis and limitations

Resolve the linked DCS foundation and its professional-source records. Record the source edition, applicability, interpretation, method and evidence for the real engagement. This case is a JAI-authored illustration, not a quotation from or certification against an external standard. Complexity changes the required evidence boundary, not the truth status of fictional facts.
