---
reference_id: example:prototype:simple
schema_version: '1.0.0'
document_kind: prototype
complexity: simple
language: en
classification: public-synthetic
provenance: ai-authored-proposed
fictional_context: true
applicable_dcs: kind/prototype
approval_status: not-human-approved
content_revision: 1.0.0
---

# Prototype — Harbor Stock Service

**PUBLIC SYNTHETIC TEACHING CASE.** All entities, revisions, values and observations below are invented. Tests are not executed and no professional or human approval is established.

**Boundary:** one service, one team and one bounded change. **Illustrative evaluation population:** 100 synthetic records or requests; this is a proposed scope, not a measured production sample.

<a id="dcs-proposed-prototype.reference_prototype_hypothesis"></a>
## Prototype Hypothesis

Hypothesis H-2: transactional uniqueness prevents duplicate reservation under concurrent requests while p95 latency stays below the agreed test target. Specify target load, environment and failure cases before measurement; do not select thresholds after observing results.

**Acceptance question:** Predeclare a bounded feasibility hypothesis and success oracle.

**Context application:** Use one source revision and one receiving owner. Confirm the bounded normal case and a meaningful failure before expanding scope.

<a id="dcs-proposed-prototype.reference_prototype_reproduction"></a>
## Prototype Reproduction

Use experiment revision exp-3, a seeded synthetic workload and a disposable database. Record invocation, dependency versions, clock configuration and raw observations when run. The prototype is isolated from production and contains no customer credentials.

**Acceptance question:** Identify disposable code, dependencies and reproducible workload.

**Context application:** Use one source revision and one receiving owner. Confirm the bounded normal case and a meaningful failure before expanding scope.

<a id="dcs-proposed-prototype.reference_prototype_disposition"></a>
## Prototype Disposition

If correctness passes but latency misses the target, report a mixed result and investigate the bottleneck. A successful limited experiment supports a trial proposal, not an unqualified production claim or merge of disposable prototype code.

**Acceptance question:** Compare observations to criteria and bound the adoption decision.

**Context application:** Use one source revision and one receiving owner. Confirm the bounded normal case and a meaningful failure before expanding scope.

## Evidence and alternatives

`SYN-INPUT-01` is the fictional requirements and source-revision record. `SYN-TEST-01` is a proposed verification record with status **NOT_EXECUTED**. `SYN-REVIEW-01` is a review request, not a completed review. In a real task, replace these with attributable permitted inputs and observed results.

Compare the bounded baseline with the proposed change using the same business invariant. Retaining the baseline avoids transition exposure but leaves the stated problem unresolved; adopting the change before verification creates an unsupported confidence claim.

## Plausible but incorrect conclusion

The demo worked once, so rename the prototype as a production service.

**Why it fails:** the conclusion skips an evidence or semantic boundary identified in the information sections. A dated, polished artifact cannot repair the missing observation or change the meaning of an interface.

## Reasoned disposition and downstream action

Require reproducible correctness and performance observations against the preregistered criteria. Transfer validated requirements and findings to engineering; keep experiment code and production acceptance distinct.

The source owner supplies missing evidence; an independent competent reviewer assesses the exact revision. The receiving owner records acceptance or required rework. Human approval and release remain separate existing authority acts.

## Professional basis and limitations

Resolve the linked DCS foundation and its professional-source records. Record the source edition, applicability, interpretation, method and evidence for the real engagement. This case is a JAI-authored illustration, not a quotation from or certification against an external standard. Complexity changes the required evidence boundary, not the truth status of fictional facts.
