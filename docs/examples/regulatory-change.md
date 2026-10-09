# Example: Regulatory change to assurance

<img class="ai-example-photo" src="../../assets/images/example-regulatory-change.jpg" alt="Example: Regulatory change to assurance">

## Scenario

A new regulatory interpretation changes expected logging, retention and access-control evidence for a business-critical service. Several teams are involved and the organisation must connect changed obligations to implemented controls and assurance evidence.

## Starting material

Provide the regulatory source/change note, applicability criteria, current control catalogue, architecture/service inventory, existing evidence, assurance findings and remediation ownership.

## Run this scenario in the provider CLI

Paste the following as a **request in Claude Code or Codex CLI**. It is not a terminal command, and it does not automatically authorise tool execution or a business decision:

```text
Assess the change to logging, retention and access-control obligations using regulatory-change-to-assurance. Identify affected services, requirements, control deltas, evidence gaps and the named compliance acceptance owner.
```

**You:** provide the starting material listed above, identify the accountable owners, inspect the evidence and respond to real approval gates. For material decisions, explicitly initiate `/layered <intent>` in Claude or `$workflow-layered <intent>` in Codex rather than assuming a natural-language router enforced Fabric. **Codex cannot execute protected L0 authority commands:** it must show the exact command for you to run separately in a trusted terminal.

**Behind the scenes:** The agent connects source obligations, requirements, controls and evidence with role-specific reviews. Legal applicability and final acceptance remain accountable organisational decisions. A named workflow or domain tool is *invoked by the provider* within its available permissions; its presence in the package is not execution evidence. Ask for exact artefact IDs, failed gates, source references and unresolved decisions.

## End-to-end AI IT House process

<div class="ai-example-process">
<div class="ai-example-step"><b>1. Applicability</b><span>Determine which services, data and control domains are actually in scope.</span></div>
<div class="ai-example-step"><b>2. Translate</b><span>Map obligations to requirements and control changes.</span></div>
<div class="ai-example-step"><b>3. Impact</b><span>Trace architecture, process and operational impact.</span></div>
<div class="ai-example-step"><b>4. Remediate</b><span>Create owned actions and evidence expectations.</span></div>
<div class="ai-example-step"><b>5. Assure</b><span>Review evidence, residual gaps and closure decision.</span></div>
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
Use the regulatory-change-to-assurance workflow.
Show applicability analysis, impacted controls, architecture implications, remediation actions, evidence and closure criteria.

/research What changed and what evidence is authoritative?
/review assurance-pack/
/publish regulatory-assurance.json audit-compliance-evidence-pack pdf,docx
```

## Illustrative checkpoints and expected output

```text
Applicability
- services in scope: 4
- control domains impacted: identity, logging, retention, monitoring

Gaps
- retention evidence incomplete for 2 services
- break-glass access review not evidenced quarterly
- architecture standard update required

Closure gate
PENDING until remediation evidence is independently reviewed.
```

## Expected artefacts

- applicability record
- obligation-to-control mapping
- architecture/control impact assessment
- remediation backlog
- assurance evidence pack
- residual-risk / closure record

## Why this example matters

This closes the gap between “we read the regulation” and “we can demonstrate that affected services are designed, operated and evidenced accordingly”.
<!-- AI-PAGE-NAV -->
<div class="ai-page-nav">
  <a class="ai-prev" href="../justifiable-decision/"><small>← Previous · Examples</small><strong>Justifiable consequential decision</strong></a>
  <a class="ai-next" href="../service-onboarding/"><small>Next · Examples →</small><strong>Service introduction</strong></a>
</div>
<!-- /AI-PAGE-NAV -->
