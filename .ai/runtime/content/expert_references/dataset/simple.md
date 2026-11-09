---
reference_id: example:dataset:simple
schema_version: '1.0.0'
document_kind: dataset
complexity: simple
language: en
classification: public-synthetic
provenance: ai-authored-proposed
fictional_context: true
applicable_dcs: kind/dataset
approval_status: not-human-approved
content_revision: 1.0.0
---

# Dataset — Harbor Stock Service

**PUBLIC SYNTHETIC TEACHING CASE.** All entities, revisions, values and observations below are invented. Tests are not executed and no professional or human approval is established.

**Boundary:** one service, one team and one bounded change. **Illustrative evaluation population:** 100 synthetic records or requests; this is a proposed scope, not a measured production sample.

<a id="dcs-proposed-dataset.reference_dataset_contract"></a>
## Dataset Contract

Dataset orders-v3 contains order_id as the unique key, amount_minor as integer cents, currency as an ISO currency code and event_time as a UTC timestamp. Null amount is unknown, not zero; mixed currencies cannot be summed without a dated conversion basis.

**Acceptance question:** Specify field meanings, keys, units, nulls and schema version.

**Context application:** Use one source revision and one receiving owner. Confirm the bounded normal case and a meaningful failure before expanding scope.

<a id="dcs-proposed-dataset.reference_dataset_lineage"></a>
## Dataset Lineage

Extract src-orders revision 17, deduplicate by business key and latest event sequence, and retain quarantined duplicate IDs. The owner must establish permitted use, access and retention. Synthetic row values here do not demonstrate real customer-data authority.

**Acceptance question:** Record source, transformations and permitted handling.

**Context application:** Use one source revision and one receiving owner. Confirm the bounded normal case and a meaningful failure before expanding scope.

<a id="dcs-proposed-dataset.reference_dataset_quality"></a>
## Dataset Quality

The illustrative input has 100 rows, two duplicate IDs and one missing amount. If duplicates are quarantined, record retained and rejected counts explicitly. A completeness metric must use the original population and identify how overlap is handled.

**Acceptance question:** Measure dimensions and disclose rejected and unresolved records.

**Context application:** Use one source revision and one receiving owner. Confirm the bounded normal case and a meaningful failure before expanding scope.

## Evidence and alternatives

`SYN-INPUT-01` is the fictional requirements and source-revision record. `SYN-TEST-01` is a proposed verification record with status **NOT_EXECUTED**. `SYN-REVIEW-01` is a review request, not a completed review. In a real task, replace these with attributable permitted inputs and observed results.

Compare the bounded baseline with the proposed change using the same business invariant. Retaining the baseline avoids transition exposure but leaves the stated problem unresolved; adopting the change before verification creates an unsupported confidence claim.

## Plausible but incorrect conclusion

Replace all missing amounts with zero and call the resulting dataset complete.

**Why it fails:** the conclusion skips an evidence or semantic boundary identified in the information sections. A dated, polished artifact cannot repair the missing observation or change the meaning of an interface.

## Reasoned disposition and downstream action

Preserve the distinction between unknown and zero. Reconcile transformation counts and currency units, publish quality limitations and require the receiving analyst to acknowledge the permitted-use boundary.

The source owner supplies missing evidence; an independent competent reviewer assesses the exact revision. The receiving owner records acceptance or required rework. Human approval and release remain separate existing authority acts.

## Professional basis and limitations

Resolve the linked DCS foundation and its professional-source records. Record the source edition, applicability, interpretation, method and evidence for the real engagement. This case is a JAI-authored illustration, not a quotation from or certification against an external standard. Complexity changes the required evidence boundary, not the truth status of fictional facts.
