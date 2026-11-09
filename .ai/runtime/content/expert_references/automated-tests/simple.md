---
reference_id: example:automated-tests:simple
schema_version: '1.0.0'
document_kind: automated-tests
complexity: simple
language: en
classification: public-synthetic
provenance: ai-authored-proposed
fictional_context: true
applicable_dcs: kind/automated-tests
approval_status: not-human-approved
content_revision: 1.0.0
---

# Automated Tests — Harbor Stock Service

**PUBLIC SYNTHETIC TEACHING CASE.** All entities, revisions, values and observations below are invented. Tests are not executed and no professional or human approval is established.

**Boundary:** one service, one team and one bounded change. **Illustrative evaluation population:** 100 synthetic records or requests; this is a proposed scope, not a measured production sample.

<a id="dcs-proposed-automated-tests.reference_test_oracles"></a>
## Test Oracles

R-17 is represented by duplicate-order, independent-order, concurrent-duplicate and rejected-negative-quantity cases. The duplicate oracle checks stored stock and reservation count, rather than merely HTTP 200. Each fixture resets stock to 10.

**Acceptance question:** Trace executable cases to behaviour and meaningful expected outcomes.

**Context application:** Use one source revision and one receiving owner. Confirm the bounded normal case and a meaningful failure before expanding scope.

<a id="dcs-proposed-automated-tests.reference_test_execution"></a>
## Test Execution

Suite tests-18 targets src-42 with a disposable real database. Pin schema and dependency versions and inject the clock. A failure record includes invocation, seed, expected stock 9, observed stock and captured reservation IDs. No invocation was executed for this illustration.

**Acceptance question:** Specify reproducible environment, revision and observed-result evidence.

**Context application:** Use one source revision and one receiving owner. Confirm the bounded normal case and a meaningful failure before expanding scope.

<a id="dcs-proposed-automated-tests.reference_test_coverage_limits"></a>
## Test Coverage Limits

Unit tests cover validation; database integration covers atomicity. Broker redelivery and multi-region recovery are separate risks with explicit owners. Repeating a flaky test until it passes discards evidence and cannot satisfy an exit criterion.

**Acceptance question:** Identify excluded risks and prevent unsupported confidence claims.

**Context application:** Use one source revision and one receiving owner. Confirm the bounded normal case and a meaningful failure before expanding scope.

## Evidence and alternatives

`SYN-INPUT-01` is the fictional requirements and source-revision record. `SYN-TEST-01` is a proposed verification record with status **NOT_EXECUTED**. `SYN-REVIEW-01` is a review request, not a completed review. In a real task, replace these with attributable permitted inputs and observed results.

Compare the bounded baseline with the proposed change using the same business invariant. Retaining the baseline avoids transition exposure but leaves the stated problem unresolved; adopting the change before verification creates an unsupported confidence claim.

## Plausible but incorrect conclusion

100% statement coverage proves that duplicate orders cannot decrement stock twice.

**Why it fails:** the conclusion skips an evidence or semantic boundary identified in the information sections. A dated, polished artifact cannot repair the missing observation or change the meaning of an interface.

## Reasoned disposition and downstream action

Require a failure-sensitive concurrency oracle and a real constraint-boundary test. Track untested recovery risk separately; coverage percentage describes execution, not the correctness of the business invariant.

The source owner supplies missing evidence; an independent competent reviewer assesses the exact revision. The receiving owner records acceptance or required rework. Human approval and release remain separate existing authority acts.

## Professional basis and limitations

Resolve the linked DCS foundation and its professional-source records. Record the source edition, applicability, interpretation, method and evidence for the real engagement. This case is a JAI-authored illustration, not a quotation from or certification against an external standard. Complexity changes the required evidence boundary, not the truth status of fictional facts.
