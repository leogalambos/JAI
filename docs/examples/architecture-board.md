# Example: Architecture Review Board pack

<img class="ai-example-photo" src="../../assets/images/example-architecture-board.jpg" alt="Example: Architecture Review Board pack">

## Scenario

A solution architect has completed the design model and ADR set for an integration platform. The Architecture Review Board now needs a concise, controlled decision pack covering scope, key decisions, options, dependencies, risks and the approval request.

## Starting material

Provide the reviewed semantic architecture, ADRs, requirements, open risks, dependency model, roadmap and the exact decision requested from the board. Do not begin from an empty slide deck.

## Run this scenario in the provider CLI

Paste the following as a **request in Claude Code or Codex CLI**. It is not a terminal command, and it does not automatically authorise tool execution or a business decision:

```text
Prepare an Architecture Review Board decision pack for our integration platform from the supplied ADRs, risk register and reviewed model. Use semantic-to-enterprise-publication, show mandatory claims and omissions, and identify which board decisions remain pending.
```

**You:** provide the starting material listed above, identify the accountable owners, inspect the evidence and respond to real approval gates. For material decisions, explicitly initiate `/layered <intent>` in Claude or `$workflow-layered <intent>` in Codex rather than assuming a natural-language router enforced Fabric. **Codex cannot execute protected L0 authority commands:** it must show the exact command for you to run separately in a trusted terminal.

**Behind the scenes:** The agent routes architecture review and publication, creates a traceable projection and renders requested artefacts. It does not exercise the Architecture Board's authority or manufacture an approved decision. A named workflow or domain tool is *invoked by the provider* within its available permissions; its presence in the package is not execution evidence. Ask for exact artefact IDs, failed gates, source references and unresolved decisions.

## End-to-end AI IT House process

<div class="ai-example-process">
<div class="ai-example-step"><b>1. Analyse</b><span>Confirm the decision, audience and source-of-truth artefacts.</span></div>
<div class="ai-example-step"><b>2. Criteria</b><span>Fix the ARB acceptance criteria and mandatory sections.</span></div>
<div class="ai-example-step"><b>3. Review</b><span>Independently review semantic completeness and unresolved risks.</span></div>
<div class="ai-example-step"><b>4. Project</b><span>Create a projection manifest for the ARB audience.</span></div>
<div class="ai-example-step"><b>5. Publish</b><span>Render DOCX/PPTX/HTML and pass publication + visual QA.</span></div>
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
/analyse architecture-review.json
/criteria architecture-review.json
/review architecture-review.json
/publish architecture-review.json architecture-review-pack docx,pptx,html
```

## Illustrative checkpoints and expected output

```text
Semantic review: PASS WITH 2 OPEN DECISIONS
Projection mandatory coverage: 100%
Omissions: 0

Rendered
- out/ARB-INT-042.docx
- out/ARB-INT-042.pptx
- out/ARB-INT-042.html

Publication gate: PASS
Visual QA: PASS
```

## Expected artefacts

- Architecture Review Board decision pack
- projection manifest
- semantic / projection / render hashes
- decision and risk appendix
- final approval record

## Why this example matters

This demonstrates the difference between governed publication and “make me a PowerPoint”: presentation can improve, but the approved semantic content remains authoritative.
<!-- AI-PAGE-NAV -->
<div class="ai-page-nav">
  <a class="ai-prev" href="../cloud-migration/"><small>← Previous · Examples</small><strong>Regulated cloud migration</strong></a>
  <a class="ai-next" href="../cyber-incident/"><small>Next · Examples →</small><strong>Cyber incident to recovery</strong></a>
</div>
<!-- /AI-PAGE-NAV -->
