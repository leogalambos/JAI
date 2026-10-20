---
reference_id: example:software-supply-chain-assessment:complex
schema_version: '1.0.0'
content_revision: 2.2.0
document_kind: software-supply-chain-assessment
complexity: complex
language: en
classification: public-synthetic
provenance: ai-authored-proposed
fictional_context: true
applicable_dcs: proposed/kind/software-supply-chain-assessment
dcs_status: proposed-not-mapped
approval_status: not-human-approved
case_id: OPG-RSM
methodology_context: "SLSA v1.2 provenance and software supply-chain risk; NIST SSDF practices"
---

# Software supply-chain risk and provenance assessment — Regulated Settlement Modernisation

> **SYNTHETIC EXPERT REFERENCE / NOT AN APPROVED PROJECT RECORD.** All organisations, measurements, contracts, test results, approvals and evidence IDs are invented. Narrative is illustrative, not proof of implementation or statutory compliance. Do not copy synthetic values into a real deliverable as verified facts.

**Entity of interest:** cross-border settlement instruction processing and finality reconciliation. **Context:** Orion Payments Group. **Complexity:** complex. **Status:** proposed transformation; no enacted jurisdictional approval or production evidence. **Decision authority:** Group Payments Executive, subject to separate competent security, finance and operational authority.

**Evidence rule:** distinguish proposed design, expected test, observed result and human approval. In this document observed execution = none; every run-specific status remains `NOT_EXECUTED` or `OPEN`.

<a id="dcs-proposed-software-supply-chain-assessment.supply_chain_scope"></a>
## 1. Supply chain scope

Scope the supply chain for repository `settlement-modernisation` through source contributors, dependencies, build tools, runner, registry, signing and deployment for **cross-border settlement instruction processing and finality reconciliation**. The protected object is the exact deployable artifact, not a repository branch label. Threats include unreviewed dependencies, compromised build credentials, mutable binary tags, poisoned caches and untrusted supplier components. Record the supplier and subprocess boundaries for **fourteen jurisdictions, three failure domains, regional connectors, dual-run ledger, evidence store**; do not treat a contract claim as a provenance verification.

<a id="dcs-proposed-software-supply-chain-assessment.dependency_inventory"></a>
## 2. Dependency inventory

Dependency inventory identifies direct/transitive packages, license, version, digest, maintainer criticality, origin and update cadence; an SBOM is necessary for visibility but cannot alone establish absence of exploitable vulnerabilities. Pin package manager inputs and lockfile, review unexpected provenance shifts and require a disposition for unmaintained high-impact packages. Dependency-risk selection must consider whether a package is actually built into the released binary or merely appears in a development-only graph.

<a id="dcs-proposed-software-supply-chain-assessment.build_provenance"></a>
## 3. Build provenance

Build provenance must bind source revision, builder identity, steps and materials to resulting digest, preferably as verifiable signed attestation under the organization's selected mechanism. Align checks conceptually to SLSA v1.2 without asserting an achieved security level. An artifact digest that differs from the recorded attestation subject is a release blocker. The example provides no actual signature or trusted build platform and thus remains NOT VERIFIED.

### Worked assessment matrix (synthetic)

| Material | Assurance objective | Evidence needed | State |
|---|---|---|---|
| Source | Signed/attributable revision + review | Branch protection + commit identity | NOT VERIFIED |
| Dependencies | Pinned origin and traceable SBOM | Lockfile/SBOM + vulnerability scope | NOT VERIFIED |
| Build | Provenance subject matches artifact | Verifiable attestation/digest | NOT VERIFIED |
| Deployment | Deployed digest equals reviewed binary | Deployment record | NOT VERIFIED |

The matrix is a proposed verification instrument for **cross-border settlement instruction processing and finality reconciliation**. Its displayed rows are not actual enterprise observations. Evidence must be source-bound and independently interpreted before a finding or green status can support a project decision.

<a id="dcs-proposed-software-supply-chain-assessment.publisher_integrity"></a>
## 4. Publisher integrity

Publisher control includes release tagging authority, signing identity protections, registry immutability, restricted package promotion, artifact retention and approved download/consumption policies. Ensure untrusted PR jobs cannot publish or access signing credentials. Verify consumers reject untrusted publishers and altered digests; do not rely on a matching package name or latest version string. Observe deployment fingerprint against the validated release artifact and capture provenance chain to the operating environment.

<a id="dcs-proposed-software-supply-chain-assessment.supplier_risks"></a>
## 5. Supplier risks

Material supplier risk is **legal applicability by entity, immutable evidence, HSM policy, finality and regional cut-off controls** with possible exposure **financial integrity, data-residency breach and loss of transaction finality**. Prioritize unknown dependency origin, privileged installer scripts, unpatched reachable libraries and lack of supplier exit or security notification obligation. Compensating mitigations include isolation, pinned versions, controlled substitutions and negative testing; these do not automatically make an unverified critical dependency acceptable. Track risk owner Enterprise Financial Risk Officer, reassessment dates and effective remedial tests.

### Dependency and challenge analysis

For OPG-RSM, a release or transformation claim is invalid if **legal applicability by entity, immutable evidence, HSM policy, finality and regional cut-off controls** remains unresolved. Check the counterfactual: what would break if the preferred technology were removed while user behavior and business service demand stayed constant? An independent reviewer should challenge the alleged root cause, hidden vendor commitments, failures spanning channel boundary → policy decision → immutable journal → regulated ledger and regional processors, and who accepts an unsuccessful delivery when the sponsor and implementer disagree.

<a id="dcs-proposed-software-supply-chain-assessment.release_conditions"></a>
## 6. Release conditions

Recommendation: require verified provenance and dependency review before promotion; open risks stay unaccepted. Final package acceptance must include source/material manifest, SBOM, signature verification result, builder policy and release authority linked to the same immutable digest. A signed PDF approval of a build is not a cryptographic attestation of its origin. This reference is an educational evaluation, not proof that real software met SLSA or ISO criteria.

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

**Methodological reference:** SLSA v1.2 provenance and software supply-chain risk; NIST SSDF practices. These frameworks inform professional coverage and challenge questions; this reference does not assert compliance or quote normative control clauses.

**Professional review disposition:** OPEN. No actual implementation, live provider validation, signed security assessment, executive approval or legal determination occurred.
