---
reference_id: example:devsecops-pipeline-design:complex
schema_version: '1.0.0'
content_revision: 2.2.0
document_kind: devsecops-pipeline-design
complexity: complex
language: en
classification: public-synthetic
provenance: ai-authored-proposed
fictional_context: true
applicable_dcs: proposed/kind/devsecops-pipeline-design
dcs_status: proposed-not-mapped
approval_status: not-human-approved
case_id: OPG-RSM
methodology_context: "NIST SSDF SP 800-218 v1.1 (final); OWASP ASVS 5.0; SLSA v1.2 supply-chain framework"
---

# DevSecOps delivery pipeline and policy-as-code design — Regulated Settlement Modernisation

> **SYNTHETIC EXPERT REFERENCE / NOT AN APPROVED PROJECT RECORD.** All organisations, measurements, contracts, test results, approvals and evidence IDs are invented. Narrative is illustrative, not proof of implementation or statutory compliance. Do not copy synthetic values into a real deliverable as verified facts.

**Entity of interest:** cross-border settlement instruction processing and finality reconciliation. **Context:** Orion Payments Group. **Complexity:** complex. **Status:** proposed transformation; no enacted jurisdictional approval or production evidence. **Decision authority:** Group Payments Executive, subject to separate competent security, finance and operational authority.

**Evidence rule:** distinguish proposed design, expected test, observed result and human approval. In this document observed execution = none; every run-specific status remains `NOT_EXECUTED` or `OPEN`.

<a id="dcs-proposed-devsecops-pipeline-design.pipeline_scope"></a>
## 1. Pipeline scope

Pipeline purpose: produce verifiable software for **cross-border settlement instruction processing and finality reconciliation** from repository `settlement-modernisation` through isolated build and controlled release. Quality objective is not maximum deployment frequency: it is a trustworthy artifact whose provenance and tests support **each authorised instruction has immutable lineage and zero unexplained unmatched finality amounts**. Define trust boundaries for developer workstation, source control, CI runner, package registry, deployment agent and production environment. Repository ownership and build service identity must be accountable and separable from release approval.

<a id="dcs-proposed-devsecops-pipeline-design.stages_and_protection"></a>
## 2. Stages and protection

Stages: source revision/PR review → unit and contract tests → SAST and secret detection → dependency and license review → reproducible dependency resolution → build in controlled runner → SBOM/provenance → artifact publication → policy-approved deployment → post-deploy business checks. Place security checks where they can still stop promotion. Make test output explicit PASS/FAIL/NOT_EXECUTED. A passing linter cannot override a critical authorization test failure. Environments use pinned tool versions and no live customer secrets in tests.

<a id="dcs-proposed-devsecops-pipeline-design.security_quality_gates"></a>
## 3. Security quality gates

Quality/security thresholds are versioned proposed policies: any confirmed critical vulnerability in reachable code, invalid signature/provenance, exposed secret or failing business-integrity test blocks promotion; other findings require risk-ranked disposition. SAST and SCA detectors need documented scope and suppressions with reviewer, reason and expiry. Dynamic security checks target **a privileged policy change enables unauthorised cross-jurisdiction routing** and negative authorization across **channel boundary → policy decision → immutable journal → regulated ledger and regional processors**. If a scanner is missing, record NOT EXECUTED, not an invented zero-finding result.

### Worked design matrix (synthetic)

| Stage | Required decision | Fail-closed condition | Illustrative result |
|---|---|---|---|
| Pull request | Independent review + policy | Unreviewed privileged change | NOT EXECUTED |
| Build | Pinned dependencies + isolated runner | Unsigned source or toolchain | NOT EXECUTED |
| Verify | SAST/SCA + business negative tests | Confirmed critical finding | NOT EXECUTED |
| Publish | Attestation tied to digest | Subject/signature mismatch | NOT EXECUTED |
| Deploy | Provenance + authorized change | Unapproved environment | NOT EXECUTED |

The matrix is a proposed verification instrument for **cross-border settlement instruction processing and finality reconciliation**. Its displayed rows are not actual enterprise observations. Evidence must be source-bound and independently interpreted before a finding or green status can support a project decision.

<a id="dcs-proposed-devsecops-pipeline-design.artifact_provenance"></a>
## 4. Artifact provenance

Artifacts are addressable by immutable digest. Record source commit, builder identity, dependency lockfile, SBOM, attestation and signature references. Compare deployed digest with tested digest; no mutable `latest` tag as a release identity. Use SLSA v1.2 concepts to reason about provenance but do not declare a specific achieved SLSA level without evidence that all relevant requirements hold. The release metadata must survive log expiry in a suitably controlled evidence store.

<a id="dcs-proposed-devsecops-pipeline-design.secrets_and_identity"></a>
## 5. Secrets and identity

Build and deployment credentials use short-lived least-privileged workload identity where feasible, are scoped to source branch/environment and cannot be printed into logs. Protect PR workflows from untrusted contributions acquiring release tokens; separate untrusted test execution from privileged publishing. Enforce approval for policy, branch and workflow changes. Document two-person exception review for risk-increasing changes and a safe route to revoke compromised runners and rotate tokens.

### Dependency and challenge analysis

For OPG-RSM, a release or transformation claim is invalid if **legal applicability by entity, immutable evidence, HSM policy, finality and regional cut-off controls** remains unresolved. Check the counterfactual: what would break if the preferred technology were removed while user behavior and business service demand stayed constant? An independent reviewer should challenge the alleged root cause, hidden vendor commitments, failures spanning channel boundary → policy decision → immutable journal → regulated ledger and regional processors, and who accepts an unsuccessful delivery when the sponsor and implementer disagree.

<a id="dcs-proposed-devsecops-pipeline-design.operating_acceptance"></a>
## 6. Operating acceptance

Acceptance: prove the pipeline rejects tampered artifacts, unauthorized promotion, unsigned releases and altered dependency manifests; demonstrate clean recovery from runner compromise without losing traceability. Human security authority verifies exception policy; operations accepts alert routing. No nested Codex/Claude calls belong to mandatory CI. The pipeline is proposed; there is no claim that these gates executed or that a managed CI service was configured.

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

**Methodological reference:** NIST SSDF SP 800-218 v1.1 (final); OWASP ASVS 5.0; SLSA v1.2 supply-chain framework. These frameworks inform professional coverage and challenge questions; this reference does not assert compliance or quote normative control clauses.

**Professional review disposition:** OPEN. No actual implementation, live provider validation, signed security assessment, executive approval or legal determination occurred.
