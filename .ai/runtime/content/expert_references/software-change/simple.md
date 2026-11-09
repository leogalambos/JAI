---
reference_id: example:software-change:simple
schema_version: '1.0.0'
document_kind: software-change
complexity: simple
language: en
classification: public-synthetic
provenance: ai-authored-proposed
fictional_context: true
applicable_dcs: kind/software-change
approval_status: not-human-approved
content_revision: 1.0.0
---

# Software Change — Harbor Stock Service

**PUBLIC SYNTHETIC TEACHING CASE.** All entities, revisions, values and observations below are invented. Tests are not executed and no professional or human approval is established.

**Boundary:** one service, one team and one bounded change. **Illustrative evaluation population:** 100 synthetic records or requests; this is a proposed scope, not a measured production sample.

<a id="dcs-proposed-software-change.reference_change_baseline"></a>
## Change Baseline

Requirement R-17 permits one stock reservation per order key. Revision src-42 replaces a read-then-write check with a unique order-key constraint and transactional insert. A duplicate returns the existing reservation ID, not another decrement.

**Acceptance question:** Identify the exact source revision, changed behaviour and requirement.

**Context application:** Use one source revision and one receiving owner. Confirm the bounded normal case and a meaningful failure before expanding scope.

<a id="dcs-proposed-software-change.reference_change_verification"></a>
## Change Verification

The illustrative oracle starts with stock 10, submits the same order twice, and expects stock 9 and one reservation. A second transaction with a different order expects stock 8. Record database version, exact source/test revisions and actual results when run; this example supplies only expected results.

**Acceptance question:** Distinguish actual implementation, test evidence, review and deployment status.

**Context application:** Use one source revision and one receiving owner. Confirm the bounded normal case and a meaningful failure before expanding scope.

<a id="dcs-proposed-software-change.reference_change_recovery"></a>
## Change Recovery

A migration must quarantine existing duplicate keys before adding the constraint. Reverting the application does not restore legitimately reserved stock. The database owner must approve the reconciliation plan; operations receives conflict-rate monitoring and the forward-recovery procedure.

**Acceptance question:** Explain compatibility, recovery limits and receiving responsibilities.

**Context application:** Use one source revision and one receiving owner. Confirm the bounded normal case and a meaningful failure before expanding scope.

## Evidence and alternatives

`SYN-INPUT-01` is the fictional requirements and source-revision record. `SYN-TEST-01` is a proposed verification record with status **NOT_EXECUTED**. `SYN-REVIEW-01` is a review request, not a completed review. In a real task, replace these with attributable permitted inputs and observed results.

Compare the bounded baseline with the proposed change using the same business invariant. Retaining the baseline avoids transition exposure but leaves the stated problem unresolved; adopting the change before verification creates an unsupported confidence claim.

## Plausible but incorrect conclusion

All green unit tests prove the release safe although they ran against src-41 and mocked the database.

**Why it fails:** the conclusion skips an evidence or semantic boundary identified in the information sections. A dated, polished artifact cannot repair the missing observation or change the meaning of an interface.

## Reasoned disposition and downstream action

Defer release until integration results for src-42 demonstrate the uniqueness invariant with concurrent transactions. The reviewer must inspect source/test identity and reconcile migration exceptions; a code summary is not the source change.

The source owner supplies missing evidence; an independent competent reviewer assesses the exact revision. The receiving owner records acceptance or required rework. Human approval and release remain separate existing authority acts.

## Professional basis and limitations

Resolve the linked DCS foundation and its professional-source records. Record the source edition, applicability, interpretation, method and evidence for the real engagement. This case is a JAI-authored illustration, not a quotation from or certification against an external standard. Complexity changes the required evidence boundary, not the truth status of fictional facts.
