---
reference_id: example:software-supply-chain-assessment:medium
schema_version: '1.0.0'
content_revision: 2.2.0
document_kind: software-supply-chain-assessment
complexity: medium
language: en
classification: public-synthetic
provenance: ai-authored-proposed
fictional_context: true
applicable_dcs: proposed/kind/software-supply-chain-assessment
dcs_status: proposed-not-mapped
approval_status: not-human-approved
case_id: MRG-OEI
methodology_context: "SLSA v1.2 provenance and software supply-chain risk; NIST SSDF practices"
---

# Software supply-chain risk and provenance assessment — Order Event Integration

> **SYNTHETIC EXPERT REFERENCE / NOT AN APPROVED PROJECT RECORD.** All organisations, measurements, contracts, test results, approvals and evidence IDs are invented. Narrative is illustrative, not proof of implementation or statutory compliance. Do not copy synthetic values into a real deliverable as verified facts.

**Entity of interest:** cross-channel order ingestion and ERP fulfilment synchronisation. **Context:** Meridian Retail Group. **Complexity:** medium. **Status:** proposed phased delivery; no live ERP, market or regulatory evidence. **Decision authority:** Digital Commerce Sponsor, subject to separate competent security, finance and operational authority.

**Evidence rule:** distinguish proposed design, expected test, observed result and human approval. In this document observed execution = none; every run-specific status remains `NOT_EXECUTED` or `OPEN`.

<a id="dcs-proposed-software-supply-chain-assessment.supply_chain_scope"></a>
## 1. Supply chain scope

Scope the supply chain for repository `retail-order-integration` through source contributors, dependencies, build tools, runner, registry, signing and deployment for **cross-channel order ingestion and ERP fulfilment synchronisation**. The protected object is the exact deployable artifact, not a repository branch label. Threats include unreviewed dependencies, compromised build credentials, mutable binary tags, poisoned caches and untrusted supplier components. Record the supplier and subprocess boundaries for **twelve European markets with a commerce platform, broker, ERP adapters, and reconciliation**; do not treat a contract claim as a provenance verification.

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

The matrix is a proposed verification instrument for **cross-channel order ingestion and ERP fulfilment synchronisation**. Its displayed rows are not actual enterprise observations. Evidence must be source-bound and independently interpreted before a finding or green status can support a project decision.

<a id="dcs-proposed-software-supply-chain-assessment.publisher_integrity"></a>
## 4. Publisher integrity

Publisher control includes release tagging authority, signing identity protections, registry immutability, restricted package promotion, artifact retention and approved download/consumption policies. Ensure untrusted PR jobs cannot publish or access signing credentials. Verify consumers reject untrusted publishers and altered digests; do not rely on a matching package name or latest version string. Observe deployment fingerprint against the validated release artifact and capture provenance chain to the operating environment.

<a id="dcs-proposed-software-supply-chain-assessment.supplier_risks"></a>
## 5. Supplier risks

Material supplier risk is **country data-handling decisions, broker retention, ERP freeze windows and vendor SLAs** with possible exposure **customer-data misrouting, delayed order promises and incomplete reconciliation**. Prioritize unknown dependency origin, privileged installer scripts, unpatched reachable libraries and lack of supplier exit or security notification obligation. Compensating mitigations include isolation, pinned versions, controlled substitutions and negative testing; these do not automatically make an unverified critical dependency acceptable. Track risk owner Head of Digital Risk, reassessment dates and effective remedial tests.

### Dependency and challenge analysis

For MRG-OEI, a release or transformation claim is invalid if **country data-handling decisions, broker retention, ERP freeze windows and vendor SLAs** remains unresolved. Check the counterfactual: what would break if the preferred technology were removed while user behavior and business service demand stayed constant? An independent reviewer should challenge the alleged root cause, hidden vendor commitments, failures spanning commerce cloud → broker → region-scoped ERP service, and who accepts an unsuccessful delivery when the sponsor and implementer disagree.

<a id="dcs-proposed-software-supply-chain-assessment.release_conditions"></a>
## 6. Release conditions

Recommendation: require verified provenance and dependency review before promotion; open risks stay unaccepted. Final package acceptance must include source/material manifest, SBOM, signature verification result, builder policy and release authority linked to the same immutable digest. A signed PDF approval of a build is not a cryptographic attestation of its origin. This reference is an educational evaluation, not proof that real software met SLSA or ISO criteria.

## Example decision register

| Decision | Alternatives / objections | Evidence needed | Owner and status |
|---|---|---|---|
| DR-01 — approve scoped approach | transactional outbox plus managed broker with a quarantine stream and idempotent consumers vs controlled baseline | Business invariant and dependency mapping | Digital Commerce Sponsor — OPEN |
| DR-02 — permit protected integration | Deny or quarantine unknown actor/entity vs permissive routing | Independent negative authorization and reconciliation | Head of Digital Risk — OPEN |
| DR-03 — accept operations handover | Reversible pilot vs direct cutover | 2 hours/15 minutes timed recovery, staffed on-call | Service Operations Manager — OPEN |

All decision IDs above are local worked-example identifiers; they are not proof that any person approved or that underlying evidence exists.

## Evidence register, validation and handoff

| Example evidence ID | Required underlying record | Status |
|---|---|---|
| MRG-OEI-E-SCOPE | Verifiable operating baseline, applicable entity/data obligations | PROPOSED / NOT OBSERVED |
| MRG-OEI-E-DESIGN | Versioned architecture/contract and independent review | PROPOSED |
| MRG-OEI-E-TEST | Executed test inputs, output, toolchain and build digest | NOT EXECUTED |
| MRG-OEI-E-OPS | Receiving service acceptance and live owner | PENDING |

**Minimum acceptance conditions:** authoritative requirement `MRG-OEI-REQ-01` traced to business owner; exact build `MRG-OEI-BUILD-01` and change `MRG-OEI-CHG-01` evidenced by immutable identifiers; critical controls evaluated on the intended trust boundary; explicit mitigation and verification of **duplicate or out-of-order messages create an incorrect fulfilment state**; completed handoff acknowledged by Service Operations Manager. An unsupported assumption remains OPEN and may justify deferral.

**Handoff graph:** MRG-OEI-REQ → MRG-OEI-ARCH → MRG-OEI-SEC → MRG-OEI-BUILD → MRG-OEI-TEST → MRG-OEI-OPS. These IDs are illustrative and must not be mistaken for existing documents.

**Methodological reference:** SLSA v1.2 provenance and software supply-chain risk; NIST SSDF practices. These frameworks inform professional coverage and challenge questions; this reference does not assert compliance or quote normative control clauses.

**Professional review disposition:** OPEN. No actual implementation, live provider validation, signed security assessment, executive approval or legal determination occurred.
