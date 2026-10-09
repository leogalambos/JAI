# Example: Cyber incident to recovery

<img class="ai-example-photo" src="../../assets/images/cyber-incident.jpg" alt="Example: Cyber incident to recovery">

## Scenario

Monitoring identifies suspicious privileged access followed by abnormal data transfer. The organisation needs containment, evidence preservation, impact assessment, legal/privacy evaluation, safe recovery and control remediation.

## Starting material

Provide the alert/event sources, affected asset inventory, identity logs, network telemetry, known data classifications, incident severity model, recovery objectives and notification obligations.

## Run this scenario in the provider CLI

Paste the following as a **request in Claude Code or Codex CLI**. It is not a terminal command, and it does not automatically authorise tool execution or a business decision:

```text
Coordinate analysis of the suspected privileged-access/data-transfer incident using cyber-incident-breach-to-recovery. Show verified evidence, containment options, legal/privacy questions, recovery gates and human authorisation needed before any irreversible action.
```

**You:** provide the starting material listed above, identify the accountable owners, inspect the evidence and respond to real approval gates. For material decisions, explicitly initiate `/layered <intent>` in Claude or `$workflow-layered <intent>` in Codex rather than assuming a natural-language router enforced Fabric. **Codex cannot execute protected L0 authority commands:** it must show the exact command for you to run separately in a trusted terminal.

**Behind the scenes:** The agent can triage available logs, prepare incident artefacts and propose response steps within its allowed tools. Actual containment, notification, risk acceptance and restoration require the responsible authorised human and external operational controls. A named workflow or domain tool is *invoked by the provider* within its available permissions; its presence in the package is not execution evidence. Ask for exact artefact IDs, failed gates, source references and unresolved decisions.

## End-to-end AI IT House process

<div class="ai-example-process">
<div class="ai-example-step"><b>1. Triage</b><span>Establish scope without prematurely asserting breach impact.</span></div>
<div class="ai-example-step"><b>2. Contain</b><span>Coordinate containment while preserving forensic evidence.</span></div>
<div class="ai-example-step"><b>3. Assess</b><span>Separate technical impact from legal/privacy applicability.</span></div>
<div class="ai-example-step"><b>4. Recover</b><span>Validate eradication, service recovery and business acceptance.</span></div>
<div class="ai-example-step"><b>5. Remediate</b><span>Close control gaps, lessons learned and residual risk.</span></div>
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
Use the cyber-incident-breach-to-recovery workflow.
Keep the evidence timeline separate from conclusions.
Show the next gate, owner, required artefact and escalation condition.

/layered Decide whether the current evidence supports external breach notification.
/fabric-report
```

## Illustrative checkpoints and expected output

```text
Current state: assess impact
Completed: triage, containment, evidence preservation

Open blocker B-03
Scope of data exfiltration is not yet evidenced.
Do not assert breach scope; continue evidence acquisition.

Authority decisions required
- legal/privacy applicability
- business recovery acceptance
- residual-control acceptance
```

## Expected artefacts

- incident record and evidence register
- immutable timeline
- technical impact assessment
- legal/privacy decision record
- recovery acceptance
- lessons learned and remediation plan
- Justifiable Fabric record for consequential notification decisions

## Why this example matters

The workflow keeps evidence, containment, legal/privacy judgement, recovery and risk acceptance distinct even under incident pressure.
<!-- AI-PAGE-NAV -->
<div class="ai-page-nav">
  <a class="ai-prev" href="../architecture-board/"><small>← Previous · Examples</small><strong>Architecture Review Board pack</strong></a>
  <a class="ai-next" href="../incident-diagnosis/"><small>Next · Examples →</small><strong>Intermittent production defect</strong></a>
</div>
<!-- /AI-PAGE-NAV -->
