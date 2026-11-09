---
reference_id: example:register:medium
schema_version: '1.0.0'
document_kind: register
complexity: medium
language: en
classification: public-synthetic
provenance: ai-authored-proposed
fictional_context: true
applicable_dcs: kind/register
approval_status: not-human-approved
content_revision: 1.0.0
---

# Register — Meridian Order Integration

**PUBLIC SYNTHETIC TEACHING CASE.** All entities, revisions, values and observations below are invented. Tests are not executed and no professional or human approval is established.

**Boundary:** three services, two teams and a phased cutover. **Illustrative evaluation population:** 1000 synthetic records or requests; this is a proposed scope, not a measured production sample.

<a id="dcs-proposed-register.reference_register_schema"></a>
## Register Schema

Risk register rows have risk ID, cause-event-impact, owner, assessment date, treatment and next review. Example R-4 is open pending privileged-access evidence; a blank owner cannot be replaced with an invented person.

**Acceptance question:** Define purpose-specific records, identifiers and allowed lifecycle states.

**Context application:** Separate producer and consumer revisions. Test cross-service failure and reconciliation; one team's success does not establish the next team's acceptance.

<a id="dcs-proposed-register.reference_register_records"></a>
## Register Records

R-4 points to control proposal CD-4 and an unexecuted negative-access test. An expired exception remains expired until the named authority issues a new decision; copying its old approval into a new row does not renew it.

**Acceptance question:** Populate attributable records with meaningful status and evidence.

**Context application:** Separate producer and consumer revisions. Test cross-service failure and reconciliation; one team's success does not establish the next team's acceptance.

<a id="dcs-proposed-register.reference_register_integrity"></a>
## Register Integrity

Detect duplicate risk IDs and dangling treatment links. At review, identify which observations changed and preserve prior assessments. The recipient needs an actionable owner and evidence gap, not merely an attractive register count.

**Acceptance question:** Reconcile duplicates, references, dates and receiving actions.

**Context application:** Separate producer and consumer revisions. Test cross-service failure and reconciliation; one team's success does not establish the next team's acceptance.

## Evidence and alternatives

`SYN-INPUT-01` is the fictional requirements and source-revision record. `SYN-TEST-01` is a proposed verification record with status **NOT_EXECUTED**. `SYN-REVIEW-01` is a review request, not a completed review. In a real task, replace these with attributable permitted inputs and observed results.

Compare the bounded baseline with the proposed change using the same business invariant. Retaining the baseline avoids transition exposure but leaves the stated problem unresolved; adopting the change before verification creates an unsupported confidence claim.

## Plausible but incorrect conclusion

Every row has a closed status, therefore all risks were accepted.

**Why it fails:** the conclusion skips an evidence or semantic boundary identified in the information sections. A dated, polished artifact cannot repair the missing observation or change the meaning of an interface.

## Reasoned disposition and downstream action

Require disposition evidence and the appropriate authority for closure or risk acceptance. Reopen inconsistent rows through their owner, preserving the previous record and rationale.

The source owner supplies missing evidence; an independent competent reviewer assesses the exact revision. The receiving owner records acceptance or required rework. Human approval and release remain separate existing authority acts.

## Professional basis and limitations

Resolve the linked DCS foundation and its professional-source records. Record the source edition, applicability, interpretation, method and evidence for the real engagement. This case is a JAI-authored illustration, not a quotation from or certification against an external standard. Complexity changes the required evidence boundary, not the truth status of fictional facts.
