# Example: Supplier onboarding

<img class="ai-example-photo" src="../../assets/images/example-supplier-onboarding.jpg" alt="Example: Supplier onboarding">

## Scenario

A business unit wants to procure a SaaS platform quickly. Procurement has a commercial proposal, but architecture, security, privacy, resilience, exit and service-acceptance concerns are incomplete.

## Starting material

Provide business requirements, supplier proposal/RFP response, DPA/security material, subprocessor list, service commitments, architecture/interface material, pricing/TCO assumptions and intended data classes.

## Run this scenario in the provider CLI

Paste the following as a **request in Claude Code or Codex CLI**. It is not a terminal command, and it does not automatically authorise tool execution or a business decision:

```text
Assess the proposed SaaS supplier using supplier-onboarding and source-to-contract-to-service. Map contractual obligations, security/privacy evidence, exit risks, integrations and the residual decisions for our service and risk owners.
```

**You:** provide the starting material listed above, identify the accountable owners, inspect the evidence and respond to real approval gates. For material decisions, explicitly initiate `/layered <intent>` in Claude or `$workflow-layered <intent>` in Codex rather than assuming a natural-language router enforced Fabric. **Codex cannot execute protected L0 authority commands:** it must show the exact command for you to run separately in a trusted terminal.

**Behind the scenes:** The agent coordinates sourcing, architecture, GRC and service-readiness reviews. Binding commercial commitments, risk exceptions and supplier/service acceptance belong to the authorised business owners. A named workflow or domain tool is *invoked by the provider* within its available permissions; its presence in the package is not execution evidence. Ask for exact artefact IDs, failed gates, source references and unresolved decisions.

## End-to-end AI IT House process

<div class="ai-example-process">
<div class="ai-example-step"><b>1. Qualify</b><span>Clarify business need and mandatory requirements.</span></div>
<div class="ai-example-step"><b>2. Assess</b><span>Run architecture, security, privacy and supplier-risk assessment.</span></div>
<div class="ai-example-step"><b>3. Contract</b><span>Translate unresolved controls into enforceable clauses.</span></div>
<div class="ai-example-step"><b>4. Implement</b><span>Track integration, access, monitoring and operational readiness.</span></div>
<div class="ai-example-step"><b>5. Accept</b><span>Require service-acceptance evidence before declaring onboarding complete.</span></div>
</div>

### 1. Frame the engagement

Before generating deliverables, establish the decision, scope, owners and source material. AI IT House should state what it knows, what it is assuming and what is still missing.

### 2. Route to the correct workflow and roles

Use the named workflow or ask the router to select the relevant specialists. The expected result is not a list of personas, but explicit responsibility for analysis, authoring, review, approval and hand-over.

### 3. Build the semantic work product

Generate or update the structured architecture, risk, design, operational or decision content. Keep claims tied to evidence and retain unresolved questions rather than silently filling them.

### 4. Review and close evidence gaps

Run an independent review before publication or approval. Findings should identify severity, evidence, owner and the condition for closure. If the decision is consequential, use the Justifiable Fabric to preserve the review and authority chain.

### 5. Publish, approve and hand over

Only after semantic review should the output be projected into a stakeholder-facing artefact. Publication may improve communication; it must not invent new decisions.

## Example interaction sequence

```text
Apply the source-to-contract-to-service workflow to this SaaS purchase.
Route each step to the correct role and identify missing evidence.

/review supplier-assessment/
/publish supplier-decision.json decision-paper docx,pdf
```

## Illustrative checkpoints and expected output

```text
Pre-signature gate: FAIL
- subprocessor location evidence missing
- RTO commitment not contractually enforceable
- privileged support access model not accepted

Pre-service-acceptance gate: PENDING
- monitoring integration
- CMDB/service ownership
- tested exit/export procedure
```

## Expected artefacts

- requirement baseline
- architecture fit assessment
- security/privacy assurance
- supplier risk statement
- required contract clauses
- service acceptance checklist
- exit/data-return obligations

## Why this example matters

The process prevents “vendor selected” from being confused with “service safe and operationally accepted”.
<!-- AI-PAGE-NAV -->
<div class="ai-page-nav">
  <a class="ai-prev" href="../incident-diagnosis/"><small>← Previous · Examples</small><strong>Intermittent production defect</strong></a>
  <a class="ai-next" href="../justifiable-decision/"><small>Next · Examples →</small><strong>Justifiable consequential decision</strong></a>
</div>
<!-- /AI-PAGE-NAV -->
