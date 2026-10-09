# Example: New service onboarding

<img class="ai-example-photo" src="../../assets/images/example-service-onboarding.jpg" alt="Example: New service onboarding">

## Scenario

A product team is introducing a new internally developed service. The technical build is nearly complete, but the organisation still needs a controlled route into production covering infrastructure, pipeline, secrets, observability, support, configuration and service ownership.

## Starting material

Provide the service design, repository, infrastructure model, dependencies, non-functional requirements, support model, SLO proposal, monitoring design, CMDB/service metadata and production target date.

## Run this scenario in the provider CLI

Paste the following as a **request in Claude Code or Codex CLI**. It is not a terminal command, and it does not automatically authorise tool execution or a business decision:

```text
Assess our new service for production onboarding. Apply design-to-operational-readiness and new-service-onboarding gates; show missing support, monitoring, identity, rollback and service-owner acceptance evidence.
```

**You:** provide the starting material listed above, identify the accountable owners, inspect the evidence and respond to real approval gates. For material decisions, explicitly initiate `/layered <intent>` in Claude or `$workflow-layered <intent>` in Codex rather than assuming a natural-language router enforced Fabric. **Codex cannot execute protected L0 authority commands:** it must show the exact command for you to run separately in a trusted terminal.

**Behind the scenes:** The orchestrator can assemble design, service-management and operations artefacts and run permitted technical checks. Live change execution and service acceptance need authorised people and actual provider/tool integrations. A named workflow or domain tool is *invoked by the provider* within its available permissions; its presence in the package is not execution evidence. Ask for exact artefact IDs, failed gates, source references and unresolved decisions.

## End-to-end AI IT House process

<div class="ai-example-process">
<div class="ai-example-step"><b>1. Platform</b><span>Validate landing zone, IaC, image lineage and pipeline identity.</span></div>
<div class="ai-example-step"><b>2. Environment</b><span>Establish secrets, environments and promotion/rollback model.</span></div>
<div class="ai-example-step"><b>3. Operate</b><span>Define observability, SLO/error-budget and support runbook.</span></div>
<div class="ai-example-step"><b>4. Register</b><span>Record configuration relationships and lifecycle ownership.</span></div>
<div class="ai-example-step"><b>5. Accept</b><span>Require IT Service Owner acceptance before onboarding completes.</span></div>
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
Apply the new-service-onboarding workflow.
For each step show current state, accountable role, hand-over artefact, gate status and blocker.

/review service-onboarding/
/publish operational-readiness.json operational-handover docx,pdf
```

## Illustrative checkpoints and expected output

```text
Readiness gates
✓ landing zone and IaC
✓ federated CI/CD identity
✓ immutable promotion model
✗ support rota undefined
✗ service SLO not approved
✗ dependency map incomplete

Production acceptance: NOT READY
```

## Expected artefacts

- target platform / IaC evidence
- signed build/pipeline provenance
- secrets lifecycle and environment evidence
- observability/SLO pack
- support runbook
- CMDB/service record
- operational handover / acceptance

## Why this example matters

The onboarding process makes “deployable” different from “operable and owned”. It connects engineering readiness with service-management acceptance.
<!-- AI-PAGE-NAV -->
<div class="ai-page-nav">
  <a class="ai-prev" href="../regulatory-change/"><small>← Previous · Examples</small><strong>Regulatory change to assurance</strong></a>
  <a class="ai-next" href="../../operations/validation/"><small>Next · Operate and govern →</small><strong>Validation and release controls</strong></a>
</div>
<!-- /AI-PAGE-NAV -->
