---
reference_id: example:control-design:medium
schema_version: '1.0.0'
document_kind: control-design
complexity: medium
language: en
classification: public-synthetic
provenance: ai-authored-proposed
fictional_context: true
applicable_dcs: kind/control-design
approval_status: not-human-approved
content_revision: 1.0.0
---

# Control Design — Meridian Order Integration

**PUBLIC SYNTHETIC TEACHING CASE.** All entities, revisions, values and observations below are invented. Tests are not executed and no professional or human approval is established.

**Boundary:** three services, two teams and a phased cutover. **Illustrative evaluation population:** 1000 synthetic records or requests; this is a proposed scope, not a measured production sample.

<a id="dcs-proposed-control-design.reference_control_objective"></a>
## Control Objective

Risk CR-4 is unauthorised privileged production access. Control CD-4 requires a time-bounded grant tied to a ticket and accountable approver, owned by the identity service owner. It does not authorise access by itself.

**Acceptance question:** Trace the control objective to a risk, obligation and owner.

**Context application:** Separate producer and consumer revisions. Test cross-service failure and reconciliation; one team's success does not establish the next team's acceptance.

<a id="dcs-proposed-control-design.reference_control_mechanics"></a>
## Control Mechanics

A grant request carries subject, entitlement, purpose and expiry. Approval and provisioning identities differ. Missing expiry rejects the request; revocation failure raises an owned alert and blocks extension until disposition.

**Acceptance question:** Define triggers, actors, conditions and failure handling.

**Context application:** Separate producer and consumer revisions. Test cross-service failure and reconciliation; one team's success does not establish the next team's acceptance.

<a id="dcs-proposed-control-design.reference_control_effectiveness_test"></a>
## Control Effectiveness Test

Test an expired grant, a self-approved request and a revocation-service outage. For each, specify expected rejection or escalation and capture actual logs when executed. The design document is neither an operating sample nor a passed control test.

**Acceptance question:** Separate design adequacy from observed operating effectiveness.

**Context application:** Separate producer and consumer revisions. Test cross-service failure and reconciliation; one team's success does not establish the next team's acceptance.

## Evidence and alternatives

`SYN-INPUT-01` is the fictional requirements and source-revision record. `SYN-TEST-01` is a proposed verification record with status **NOT_EXECUTED**. `SYN-REVIEW-01` is a review request, not a completed review. In a real task, replace these with attributable permitted inputs and observed results.

Compare the bounded baseline with the proposed change using the same business invariant. Retaining the baseline avoids transition exposure but leaves the stated problem unresolved; adopting the change before verification creates an unsupported confidence claim.

## Plausible but incorrect conclusion

An approved policy and a screenshot of the request form demonstrate operating effectiveness.

**Why it fails:** the conclusion skips an evidence or semantic boundary identified in the information sections. A dated, polished artifact cannot repair the missing observation or change the meaning of an interface.

## Reasoned disposition and downstream action

Accept the design only as a proposal until the required negative paths are demonstrated. An independent assessor samples actual grants and revocations before concluding that the control operates effectively.

The source owner supplies missing evidence; an independent competent reviewer assesses the exact revision. The receiving owner records acceptance or required rework. Human approval and release remain separate existing authority acts.

## Professional basis and limitations

Resolve the linked DCS foundation and its professional-source records. Record the source edition, applicability, interpretation, method and evidence for the real engagement. This case is a JAI-authored illustration, not a quotation from or certification against an external standard. Complexity changes the required evidence boundary, not the truth status of fictional facts.
