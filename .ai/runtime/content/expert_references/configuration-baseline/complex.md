---
reference_id: example:configuration-baseline:complex
schema_version: '1.0.0'
document_kind: configuration-baseline
complexity: complex
language: en
classification: public-synthetic
provenance: ai-authored-proposed
fictional_context: true
applicable_dcs: kind/configuration-baseline
approval_status: not-human-approved
content_revision: 1.0.0
---

# Configuration Baseline — Orion Settlement Platform

**PUBLIC SYNTHETIC TEACHING CASE.** All entities, revisions, values and observations below are invented. Tests are not executed and no professional or human approval is established.

**Boundary:** multiple jurisdictions, suppliers and irreversible business effects. **Illustrative evaluation population:** 10000 synthetic records or requests; this is a proposed scope, not a measured production sample.

<a id="dcs-proposed-configuration-baseline.reference_baseline_contract"></a>
## Baseline Contract

Baseline cfg-12 sets max_connections to integer 80, request_timeout_ms to integer 2500, and a secret-manager reference rather than a password. Targets are the two order-service instances in the test environment; production is excluded.

**Acceptance question:** Specify desired values, types, units and authorised target versions.

**Context application:** Partition evidence by jurisdiction, supplier and irreversible boundary. Do not aggregate away a failed cohort; legal applicability and residual risk decisions require their actual competent owners.

<a id="dcs-proposed-configuration-baseline.reference_baseline_observations"></a>
## Baseline Observations

A hypothetical readback reports 80 on node-a and 120 on node-b. This is one conforming and one drifting target, not a 100% compliant baseline. Capture actual readback time and tool version before drawing an operational conclusion.

**Acceptance question:** Distinguish desired configuration from observed state and explain drift.

**Context application:** Partition evidence by jurisdiction, supplier and irreversible boundary. Do not aggregate away a failed cohort; legal applicability and residual risk decisions require their actual competent owners.

<a id="dcs-proposed-configuration-baseline.reference_baseline_change_recovery"></a>
## Baseline Change Recovery

Review the diff, apply to one target, verify connection saturation and error-rate bounds, then proceed. Restore cfg-11 if saturation worsens, subject to the authorised change window. A successful configuration parse does not prove safe runtime behaviour.

**Acceptance question:** Define controlled application, verification and recovery.

**Context application:** Partition evidence by jurisdiction, supplier and irreversible boundary. Do not aggregate away a failed cohort; legal applicability and residual risk decisions require their actual competent owners.

## Evidence and alternatives

`SYN-INPUT-01` is the fictional requirements and source-revision record. `SYN-TEST-01` is a proposed verification record with status **NOT_EXECUTED**. `SYN-REVIEW-01` is a review request, not a completed review. In a real task, replace these with attributable permitted inputs and observed results.

Compare the bounded baseline with the proposed change using the same business invariant. Retaining the baseline avoids transition exposure but leaves the stated problem unresolved; adopting the change before verification creates an unsupported confidence claim.

## Plausible but incorrect conclusion

The desired-state file validates, so every managed instance is compliant.

**Why it fails:** the conclusion skips an evidence or semantic boundary identified in the information sections. A dated, polished artifact cannot repair the missing observation or change the meaning of an interface.

## Reasoned disposition and downstream action

Require target-by-target observed-state reconciliation. A baseline describes intended state; the operational owner accepts only the measured disposition and explicit untested conditions.

The source owner supplies missing evidence; an independent competent reviewer assesses the exact revision. The receiving owner records acceptance or required rework. Human approval and release remain separate existing authority acts.

## Professional basis and limitations

Resolve the linked DCS foundation and its professional-source records. Record the source edition, applicability, interpretation, method and evidence for the real engagement. This case is a JAI-authored illustration, not a quotation from or certification against an external standard. Complexity changes the required evidence boundary, not the truth status of fictional facts.
