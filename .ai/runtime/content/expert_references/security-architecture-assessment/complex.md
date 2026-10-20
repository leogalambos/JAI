---
reference_id: example:security-architecture-assessment:complex
schema_version: '1.0.0'
content_revision: 2.2.0
document_kind: security-architecture-assessment
complexity: complex
language: en
classification: public-synthetic
provenance: ai-authored-proposed
fictional_context: true
applicable_dcs: proposed/kind/security-architecture-assessment
dcs_status: proposed-not-mapped
approval_status: not-human-approved
case_id: OPG-RSM
methodology_context: "NIST SP 800-53A Rev. 5 methodology; business-driven security architecture consistent with SABSA concepts"
---

# Security architecture design assessment — Regulated Settlement Modernisation

> **SYNTHETIC EXPERT REFERENCE / NOT AN APPROVED PROJECT RECORD.** All organisations, measurements, contracts, test results, approvals and evidence IDs are invented. Narrative is illustrative, not proof of implementation or statutory compliance. Do not copy synthetic values into a real deliverable as verified facts.

**Entity of interest:** cross-border settlement instruction processing and finality reconciliation. **Context:** Orion Payments Group. **Complexity:** complex. **Status:** proposed transformation; no enacted jurisdictional approval or production evidence. **Decision authority:** Group Payments Executive, subject to separate competent security, finance and operational authority.

**Evidence rule:** distinguish proposed design, expected test, observed result and human approval. In this document observed execution = none; every run-specific status remains `NOT_EXECUTED` or `OPEN`.

<a id="dcs-proposed-security-architecture-assessment.scope_and_trust"></a>
## 1. Scope and trust

Assessment target is the security architecture of **cross-border settlement instruction processing and finality reconciliation** across **fourteen jurisdictions, three failure domains, regional connectors, dual-run ledger, evidence store**. Business assets include correct transactions, service availability and trustworthy operator decisions; protected data include **payer/payee identifiers, transaction metadata, finality state and restricted audit records**. Assess against business obligations, approved risk appetite, threat scenarios and applicable security requirements. The critical boundary is **channel boundary → policy decision → immutable journal → regulated ledger and regional processors**; a supplier architecture claim does not prove control operation in the customer's environment. Scope excludes undetermined legal requirements and unprovided service internals.

<a id="dcs-proposed-security-architecture-assessment.security_requirements"></a>
## 2. Security requirements

Key requirements: validated identity for every crossing, least-privilege authorization, segregation of operational duties, integrity of authoritative state, data classification/residency, event traceability, recoverability to **30 minutes/5 minutes** and alert routing to a staffed owner. Maintain a requirement-to-control map, and tag each obligation as legal, organizational or proposed. Explain who can waive a discretionary design preference versus who cannot waive a statutory obligation. Each control needs a testable security property, not simply 'use encryption'.

<a id="dcs-proposed-security-architecture-assessment.architecture_findings"></a>
## 3. Architecture findings

Findings are categorized as design gap, unsupported assertion, control weakness and unknown applicability. For **a privileged policy change enables unauthorised cross-jurisdiction routing**, assess whether authorization is enforced at the receiving service, whether stale trust metadata is rejected, whether audit evidence is immutable and whether business state can be corrupted on replay. Distinguish a plausible failure path from an observed vulnerability; no penetration test took place. Severity depends on impact and preconditions, not a copied CVSS score.

### Worked assessment matrix (synthetic)

| Security concern | Expected control | Evidence | Current state |
|---|---|---|---|
| Cross-boundary privilege | Deny unauthorized actor | Negative policy test | NOT EXECUTED |
| Business integrity | each authorised instruction has immutable lineage and zero unexplained unmatched finality amounts | Reconciliation and replay | NOT EXECUTED |
| Protected data | Scoped retention and jurisdiction | Data-flow and policy owner | PROPOSED |
| Recovery | 30 minutes / 5 minutes | Timed restore | NOT EXECUTED |

The matrix is a proposed verification instrument for **cross-border settlement instruction processing and finality reconciliation**. Its displayed rows are not actual enterprise observations. Evidence must be source-bound and independently interpreted before a finding or green status can support a project decision.

<a id="dcs-proposed-security-architecture-assessment.control_recommendations"></a>
## 4. Control recommendations

Propose prevention, detection and recovery controls that jointly contain **unexplained ledger imbalance or illegal cross-region failover invalidates settlement finality**. The recommended architectural change is **append-only instruction lineage and jurisdiction-aware orchestration with parallel ledger checkpoints**, protected by scoped workload identities, signed state checkpoints, independent authorization and reconciliation. Evaluate cost, operational maintainability, correlated failure domains and residual risk. Reject compensating controls that only improve logging while leaving an unauthorised write path open.

<a id="dcs-proposed-security-architecture-assessment.verification_evidence"></a>
## 5. Verification evidence

Verification requires threat-based negative authorization tests, tampered-schema rejection, replay idempotency, key rotation/scope tests, observation of evidence integrity and timed recovery. Planned assertion: **each authorised instruction has immutable lineage and zero unexplained unmatched finality amounts** under **2.4 million synthetic instructions daily across fourteen jurisdictions**. Record source revision, test method, environmental representativeness and reviewer independence. An absent test is NOT EXECUTED; a management interview does not establish operating effectiveness. Compare observed configuration to approved architecture, not just to a vendor reference diagram.

### Dependency and challenge analysis

For OPG-RSM, a release or transformation claim is invalid if **legal applicability by entity, immutable evidence, HSM policy, finality and regional cut-off controls** remains unresolved. Check the counterfactual: what would break if the preferred technology were removed while user behavior and business service demand stayed constant? An independent reviewer should challenge the alleged root cause, hidden vendor commitments, failures spanning channel boundary → policy decision → immutable journal → regulated ledger and regional processors, and who accepts an unsuccessful delivery when the sponsor and implementer disagree.

<a id="dcs-proposed-security-architecture-assessment.risk_disposition"></a>
## 6. Risk disposition

Suggested disposition: **CONDITIONAL / NOT APPROVED FOR PRODUCTION** until relevant trust-boundary tests, regulatory applicability and operational evidence exist. Assign risk owner Enterprise Financial Risk Officer; record residual concerns and countermeasures with expiry/retest gates. Independently reviewed architecture advice is not itself a financial, legal or operational approval. References to ISO/NIST/SABSA are methodological context, not proof of compliance.

## Enterprise-level adversarial review and exceptional paths

**Compound failure exercise:** independently simulate supplier unavailability, revocation of a privileged deployment identity and loss of trustworthy state observations. The safety response must be bounded: freeze new acceptance and perform authorised compensating reconciliation; never reverse finalised ledgers as a generic rollback. The test never permits bypassing jurisdictional or risk authority; every state-changing activity needs a decision owner, reversible boundary, observed invariant and auditable approval.

**Jurisdiction and third-party boundary:** do not assume an authorization in one market extends to another or that a supplier statement covers the entire fourteen jurisdictions, three failure domains, regional connectors, dual-run ledger, evidence store. A transition must preserve retention and finality duties, business data ownership, security of pipeline credentials and a record of exceptions with expiry.

**Contested decision:** compare the recommended approach **append-only instruction lineage and jurisdiction-aware orchestration with parallel ledger checkpoints** with maintaining the baseline and an aggressive fast-cutover alternative. Ask what evidence would invalidate the preference and estimate the operational consequence of an unplanned halt during **an eighteen-month phased programme with parallel-run cut-offs**. Neither an attractive ROI nor a technically green build overrides a critical missing control or competent stakeholder approval.

## Example decision register

| Decision | Alternatives / objections | Evidence needed | Owner and status |
|---|---|---|---|
| DR-01 — approve scoped approach | append-only instruction lineage and jurisdiction-aware orchestration with parallel ledger checkpoints vs controlled baseline | Business invariant and dependency mapping | Group Payments Executive — OPEN |
| DR-02 — permit protected integration | Deny or quarantine unknown actor/entity vs permissive routing | Independent negative authorization and reconciliation | Enterprise Financial Risk Officer — OPEN |
| DR-03 — accept operations handover | Reversible pilot vs direct cutover | 30 minutes/5 minutes timed recovery, staffed on-call | Critical Service Operations Director — OPEN |

All decision IDs above are local worked-example identifiers; they are not proof that any person approved or that underlying evidence exists.

## Evidence register, validation and handoff

| Example evidence ID | Required underlying record | Status |
|---|---|---|
| OPG-RSM-E-SCOPE | Verifiable operating baseline, applicable entity/data obligations | PROPOSED / NOT OBSERVED |
| OPG-RSM-E-DESIGN | Versioned architecture/contract and independent review | PROPOSED |
| OPG-RSM-E-TEST | Executed test inputs, output, toolchain and build digest | NOT EXECUTED |
| OPG-RSM-E-OPS | Receiving service acceptance and live owner | PENDING |

**Minimum acceptance conditions:** authoritative requirement `OPG-RSM-REQ-01` traced to business owner; exact build `OPG-RSM-BUILD-01` and change `OPG-RSM-CHG-01` evidenced by immutable identifiers; critical controls evaluated on the intended trust boundary; explicit mitigation and verification of **unexplained ledger imbalance or illegal cross-region failover invalidates settlement finality**; completed handoff acknowledged by Critical Service Operations Director. An unsupported assumption remains OPEN and may justify deferral.

**Handoff graph:** OPG-RSM-REQ → OPG-RSM-ARCH → OPG-RSM-SEC → OPG-RSM-BUILD → OPG-RSM-TEST → OPG-RSM-OPS. These IDs are illustrative and must not be mistaken for existing documents.

**Methodological reference:** NIST SP 800-53A Rev. 5 methodology; business-driven security architecture consistent with SABSA concepts. These frameworks inform professional coverage and challenge questions; this reference does not assert compliance or quote normative control clauses.

**Professional review disposition:** OPEN. No actual implementation, live provider validation, signed security assessment, executive approval or legal determination occurred.
