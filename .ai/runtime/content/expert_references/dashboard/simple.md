---
reference_id: example:dashboard:simple
schema_version: '1.0.0'
document_kind: dashboard
complexity: simple
language: en
classification: public-synthetic
provenance: ai-authored-proposed
fictional_context: true
applicable_dcs: kind/dashboard
approval_status: not-human-approved
content_revision: 1.0.0
---

# Dashboard — Harbor Stock Service

**PUBLIC SYNTHETIC TEACHING CASE.** All entities, revisions, values and observations below are invented. Tests are not executed and no professional or human approval is established.

**Boundary:** one service, one team and one bounded change. **Illustrative evaluation population:** 100 synthetic records or requests; this is a proposed scope, not a measured production sample.

<a id="dcs-proposed-dashboard.reference_measure_definition"></a>
## Measure Definition

Availability is successful eligible requests divided by all eligible requests over the calendar month. The numerator 990 and denominator 1000 yield 99.0%; excluded synthetic probes are disclosed separately. The service owner sets the target, not the chart.

**Acceptance question:** Define metric semantics, units, denominator, window and owner.

**Context application:** Use one source revision and one receiving owner. Confirm the bounded normal case and a meaningful failure before expanding scope.

<a id="dcs-proposed-dashboard.reference_measurement_lineage"></a>
## Measurement Lineage

Query q-7 selects production order requests with a fixed UTC window and documented retry treatment. A join that duplicates requests changes the denominator and must fail reconciliation against distinct request IDs. Mark the latest incomplete hour provisional.

**Acceptance question:** Link displayed values to reproducible queries and source versions.

**Context application:** Use one source revision and one receiving owner. Confirm the bounded normal case and a meaningful failure before expanding scope.

<a id="dcs-proposed-dashboard.reference_decision_thresholds"></a>
## Decision Thresholds

A target of 99.9% means this illustrative period is below target. Display the sample size and missing-data interval. The owned action is incident triage and data validation; a green colour cannot override the arithmetic.

**Acceptance question:** Explain thresholds, uncertainty and the supported action.

**Context application:** Use one source revision and one receiving owner. Confirm the bounded normal case and a meaningful failure before expanding scope.

## Evidence and alternatives

`SYN-INPUT-01` is the fictional requirements and source-revision record. `SYN-TEST-01` is a proposed verification record with status **NOT_EXECUTED**. `SYN-REVIEW-01` is a review request, not a completed review. In a real task, replace these with attributable permitted inputs and observed results.

Compare the bounded baseline with the proposed change using the same business invariant. Retaining the baseline avoids transition exposure but leaves the stated problem unresolved; adopting the change before verification creates an unsupported confidence claim.

## Plausible but incorrect conclusion

The dashboard is green because failed requests were removed before calculating availability.

**Why it fails:** the conclusion skips an evidence or semantic boundary identified in the information sections. A dated, polished artifact cannot repair the missing observation or change the meaning of an interface.

## Reasoned disposition and downstream action

Reject the misleading denominator, reconcile the query and restate the affected period. Keep metric definition and data freshness visible so a reader can reproduce the decision.

The source owner supplies missing evidence; an independent competent reviewer assesses the exact revision. The receiving owner records acceptance or required rework. Human approval and release remain separate existing authority acts.

## Professional basis and limitations

Resolve the linked DCS foundation and its professional-source records. Record the source edition, applicability, interpretation, method and evidence for the real engagement. This case is a JAI-authored illustration, not a quotation from or certification against an external standard. Complexity changes the required evidence boundary, not the truth status of fictional facts.
