# Example: Justifiable consequential decision

<img class="ai-example-photo" src="../../assets/images/example-justifiable-decision.jpg" alt="Example: Justifiable consequential decision">

## Scenario

An organisation must decide whether to expose a legacy invoice service to external partners before a major rewrite. Revenue pressure is high, but security defects and money-correctness risks are known.

## Starting material

Provide the business objective, exposure scope, code/review evidence, known risks, partner access model, correctness tests, compensating-control options and the human authority who can accept residual risk.

## Run this scenario in the provider CLI

Paste the following as a **request in Claude Code or Codex CLI**. It is not a terminal command, and it does not automatically authorise tool execution or a business decision:

```text
Decide whether the legacy invoice service is ready for external partner exposure. Preserve the original intent, independently verify security and money correctness, record alternatives and escalate any acceptance of residual risk to me.
```

**You:** provide the starting material listed above, identify the accountable owners, inspect the evidence and respond to real approval gates. For material decisions, explicitly initiate `/layered <intent>` in Claude or `$workflow-layered <intent>` in Codex rather than assuming a natural-language router enforced Fabric. **Codex cannot execute protected L0 authority commands:** it must show the exact command for you to run separately in a trusted terminal.

**Behind the scenes:** The layered orchestrator manages contracts and Fabric, separates L5 build from L6 measurement, reviews evidence and compiles a human authority dossier. A positive AI judgement is not an L0 approval. A named workflow or domain tool is *invoked by the provider* within its available permissions; its presence in the package is not execution evidence. Ask for exact artefact IDs, failed gates, source references and unresolved decisions.

## End-to-end AI IT House process

<div class="ai-example-process">
<div class="ai-example-step"><b>1. Intent</b><span>State the consequential decision and success conditions.</span></div>
<div class="ai-example-step"><b>2. Decompose</b><span>Translate intent into adjacent-layer requirements and contracts.</span></div>
<div class="ai-example-step"><b>3. Evidence</b><span>Collect deterministic/observed evidence for material claims.</span></div>
<div class="ai-example-step"><b>4. Conflict</b><span>Record contradictions, failed attempts and unresolved proposals.</span></div>
<div class="ai-example-step"><b>5. Authority</b><span>Present a mechanically compiled dossier for human decision.</span></div>
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
/layered Decide whether invoice-service is ready to be exposed to external partners. It must be secure enough for partner traffic and its money calculations must be exact.

/fabric-report

python3 ~/.ai/it-role-house/fabric/fabric.py verify <engagement>
python3 ~/.ai/it-role-house/fabric/fabric.py justify <engagement> --strict
```

## Illustrative checkpoints and expected output

```text
Fabric integrity: VERIFIED
Open conflicts: 1

Strictly justifiable findings
✓ SQL injection exists — deterministic evidence
✓ partner authorization gap exists — observed/test evidence
✓ money boundary defect exists — deterministic regression evidence

Authority dossier
A fix before exposure
B read-only exposure with compensating controls
C time-bound risk exception

Not releasable until conflict is resolved/authorised and L1 acceptance is recorded.
```

## Expected artefacts

- append-only Fabric JSONL record
- evidence links/hashes
- review and conflict records
- authority dossier
- final human acceptance / exception / rejection record

## Why this example matters

A later reviewer can inspect how the outcome earned release eligibility instead of trusting a polished retrospective explanation.
