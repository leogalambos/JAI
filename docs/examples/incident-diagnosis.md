# Example: Intermittent production defect

<img class="ai-example-photo" src="../../assets/images/example-incident-diagnosis.jpg" alt="Example: Intermittent production defect">

## Scenario

A payments API occasionally reports an approved payment as declined. The defect is intermittent, commercially important and difficult to reproduce; an undisciplined response would be to increase a timeout and hope.

## Starting material

Provide the failing test, recent code/config changes, logs with timestamps, client and gateway timeout settings, a last-known-good revision and a working analogue if one exists.

## Run this scenario in the provider CLI

Paste the following as a **request in Claude Code or Codex CLI**. It is not a terminal command, and it does not automatically authorise tool execution or a business decision:

```text
Diagnose the intermittent payments-API approval/decline defect. Reproduce it, compare last-known-good and a working analogue, test timing hypotheses and present evidence before proposing any code change.
```

**You:** provide the starting material listed above, identify the accountable owners, inspect the evidence and respond to real approval gates. For material decisions, explicitly initiate `/layered <intent>` in Claude or `$workflow-layered <intent>` in Codex rather than assuming a natural-language router enforced Fabric. **Codex cannot execute protected L0 authority commands:** it must show the exact command for you to run separately in a trusted terminal.

**Behind the scenes:** The diagnostic agent may call `defect.py`, repository/test helpers and read-only inspection tools. It must distinguish hypotheses from observations; an accepted production fix still needs an authorised delivery/change workflow. A named workflow or domain tool is *invoked by the provider* within its available permissions; its presence in the package is not execution evidence. Ask for exact artefact IDs, failed gates, source references and unresolved decisions.

## End-to-end AI IT House process

<div class="ai-example-process">
<div class="ai-example-step"><b>1. Reproduce</b><span>Quantify frequency and capture timing/ordering evidence.</span></div>
<div class="ai-example-step"><b>2. Compare</b><span>Check last-known-good and a working analogue.</span></div>
<div class="ai-example-step"><b>3. Hypothesise</b><span>Maintain at least two competing explanations.</span></div>
<div class="ai-example-step"><b>4. Prove</b><span>Use a deterministic regression test to establish root cause.</span></div>
<div class="ai-example-step"><b>5. Fix & review</b><span>Implement the smallest supported change and independently review it.</span></div>
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
/analyse invoice-service
/diagnose payment authorization is reported as declined intermittently; test_charge_is_approved fails roughly one run in three.
/develop fix the confirmed defect without changing business-decline semantics
/review invoice-service
```

## Illustrative checkpoints and expected output

```text
Reproduction
- 30 runs / 11 failures

Timing evidence
- client timeout 100 ms
- gateway latency 35–150 ms
- failure follows latency >100 ms

Hypotheses
H1 gateway declines transaction      REJECTED
H2 client maps timeout to declined   CONFIRMED

Regression contract
- controlled gateway delay fails before fix
- timeout and decline become distinct states
- full suite passes after final code change
```

## Expected artefacts

- diagnosis record with competing hypotheses
- timing evidence
- deterministic regression test
- minimal code/config change
- review findings and closure evidence

## Why this example matters

The important output is not a clever guess. It is a reproducible explanation and a regression contract that prevents the defect class from returning.
<!-- AI-PAGE-NAV -->
<div class="ai-page-nav">
  <a class="ai-prev" href="../cyber-incident/"><small>← Previous · Examples</small><strong>Cyber incident to recovery</strong></a>
  <a class="ai-next" href="../supplier-onboarding/"><small>Next · Examples →</small><strong>Supplier onboarding</strong></a>
</div>
<!-- /AI-PAGE-NAV -->
