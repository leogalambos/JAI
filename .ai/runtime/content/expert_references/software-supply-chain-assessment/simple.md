---
reference_id: example:software-supply-chain-assessment:simple
schema_version: '1.0.0'
content_revision: 2.2.0
document_kind: software-supply-chain-assessment
complexity: simple
language: en
classification: public-synthetic
provenance: ai-authored-proposed
fictional_context: true
applicable_dcs: proposed/kind/software-supply-chain-assessment
dcs_status: proposed-not-mapped
approval_status: not-human-approved
case_id: HFS-FAR
methodology_context: "SLSA v1.2 provenance and software supply-chain risk; NIST SSDF practices"
---

# Software supply-chain risk and provenance assessment — Field Appointment Reliability

> **SYNTHETIC EXPERT REFERENCE / NOT AN APPROVED PROJECT RECORD.** All organisations, measurements, contracts, test results, approvals and evidence IDs are invented. Narrative is illustrative, not proof of implementation or statutory compliance. Do not copy synthetic values into a real deliverable as verified facts.

**Entity of interest:** technician appointment scheduling. **Context:** Harborline Field Services. **Complexity:** simple. **Status:** proposed pilot; no exercised build or customer evidence. **Decision authority:** Field Operations Manager, subject to separate competent security, finance and operational authority.

**Evidence rule:** distinguish proposed design, expected test, observed result and human approval. In this document observed execution = none; every run-specific status remains `NOT_EXECUTED` or `OPEN`.

<a id="dcs-proposed-software-supply-chain-assessment.supply_chain_scope"></a>
## 1. Supply chain scope

Scope the supply chain for repository `field-booking-adapter` through source contributors, dependencies, build tools, runner, registry, signing and deployment for **technician appointment scheduling**. The protected object is the exact deployable artifact, not a repository branch label. Threats include unreviewed dependencies, compromised build credentials, mutable binary tags, poisoned caches and untrusted supplier components. Record the supplier and subprocess boundaries for **one business unit, managed scheduling SaaS, a dispatch adapter and corporate identity**; do not treat a contract claim as a provenance verification.

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

The matrix is a proposed verification instrument for **technician appointment scheduling**. Its displayed rows are not actual enterprise observations. Evidence must be source-bound and independently interpreted before a finding or green status can support a project decision.

<a id="dcs-proposed-software-supply-chain-assessment.publisher_integrity"></a>
## 4. Publisher integrity

Publisher control includes release tagging authority, signing identity protections, registry immutability, restricted package promotion, artifact retention and approved download/consumption policies. Ensure untrusted PR jobs cannot publish or access signing credentials. Verify consumers reject untrusted publishers and altered digests; do not rely on a matching package name or latest version string. Observe deployment fingerprint against the validated release artifact and capture provenance chain to the operating environment.

<a id="dcs-proposed-software-supply-chain-assessment.supplier_risks"></a>
## 5. Supplier risks

Material supplier risk is **SaaS API availability and idempotent webhook delivery** with possible exposure **service outage and unwanted appointment duplication**. Prioritize unknown dependency origin, privileged installer scripts, unpatched reachable libraries and lack of supplier exit or security notification obligation. Compensating mitigations include isolation, pinned versions, controlled substitutions and negative testing; these do not automatically make an unverified critical dependency acceptable. Track risk owner Head of Operations, reassessment dates and effective remedial tests.

<a id="dcs-proposed-software-supply-chain-assessment.release_conditions"></a>
## 6. Release conditions

Recommendation: require verified provenance and dependency review before promotion; open risks stay unaccepted. Final package acceptance must include source/material manifest, SBOM, signature verification result, builder policy and release authority linked to the same immutable digest. A signed PDF approval of a build is not a cryptographic attestation of its origin. This reference is an educational evaluation, not proof that real software met SLSA or ISO criteria.

## Evidence register, validation and handoff

| Example evidence ID | Required underlying record | Status |
|---|---|---|
| HFS-FAR-E-SCOPE | Verifiable operating baseline, applicable entity/data obligations | PROPOSED / NOT OBSERVED |
| HFS-FAR-E-DESIGN | Versioned architecture/contract and independent review | PROPOSED |
| HFS-FAR-E-TEST | Executed test inputs, output, toolchain and build digest | NOT EXECUTED |
| HFS-FAR-E-OPS | Receiving service acceptance and live owner | PENDING |

**Minimum acceptance conditions:** authoritative requirement `HFS-FAR-REQ-01` traced to business owner; exact build `HFS-FAR-BUILD-01` and change `HFS-FAR-CHG-01` evidenced by immutable identifiers; critical controls evaluated on the intended trust boundary; explicit mitigation and verification of **a duplicated callback creates two technician assignments**; completed handoff acknowledged by Service Desk Lead. An unsupported assumption remains OPEN and may justify deferral.

**Handoff graph:** HFS-FAR-REQ → HFS-FAR-ARCH → HFS-FAR-SEC → HFS-FAR-BUILD → HFS-FAR-TEST → HFS-FAR-OPS. These IDs are illustrative and must not be mistaken for existing documents.

**Methodological reference:** SLSA v1.2 provenance and software supply-chain risk; NIST SSDF practices. These frameworks inform professional coverage and challenge questions; this reference does not assert compliance or quote normative control clauses.

**Professional review disposition:** OPEN. No actual implementation, live provider validation, signed security assessment, executive approval or legal determination occurred.
