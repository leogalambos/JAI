# Example: Regulated cloud migration

<img class="ai-example-photo" src="../../assets/images/cloud-migration.jpg" alt="Example: Regulated cloud migration">

## Scenario

A European financial-services organisation is moving a customer-facing platform from a private data centre to public cloud. The programme must satisfy resilience, identity, privacy, operational-readiness and cutover expectations, and the sponsor needs outputs that can survive architecture and risk scrutiny.

## Starting material

Provide the business case, current architecture, target constraints, data classification, regulatory obligations, RTO/RPO objectives, identity model, supplier material, migration milestones and known risks. If some are absent, treat them as questions rather than facts.

## Run this scenario in the provider CLI

Paste the following as a **request in Claude Code or Codex CLI**. It is not a terminal command, and it does not automatically authorise tool execution or a business decision:

```text
Assess the proposed regulated cloud migration. Include SABSA and EA traceability, privacy/IAM/resilience review, migration-and-cutover gates, operational acceptance and an Architecture Board decision dossier. Escalate material residual risk.
```

**You:** provide the starting material listed above, identify the accountable owners, inspect the evidence and respond to real approval gates. For material decisions, explicitly initiate `/layered <intent>` in Claude or `$workflow-layered <intent>` in Codex rather than assuming a natural-language router enforced Fabric. **Codex cannot execute protected L0 authority commands:** it must show the exact command for you to run separately in a trusted terminal.

**Behind the scenes:** The agent coordinates the named architecture, migration and readiness workflows, records contract/evidence links and routes unresolved risk to the actual accountable owner. It does not deploy or approve production changes merely because a workflow page lists those stages. A named workflow or domain tool is *invoked by the provider* within its available permissions; its presence in the package is not execution evidence. Ask for exact artefact IDs, failed gates, source references and unresolved decisions.

## End-to-end AI IT House process

<div class="ai-example-process">
<div class="ai-example-step"><b>1. Analyse</b><span>Establish drivers, dependencies, constraints and evidence quality.</span></div>
<div class="ai-example-step"><b>2. SABSA / EA</b><span>Build the security and enterprise architecture model with stable traceability.</span></div>
<div class="ai-example-step"><b>3. Migration</b><span>Apply migration-and-cutover plus operational-readiness workflow gates.</span></div>
<div class="ai-example-step"><b>4. Review</b><span>Challenge resilience, IAM, data, supplier and rollback claims.</span></div>
<div class="ai-example-step"><b>5. Publish</b><span>Produce the ARB / risk pack and approved migration hand-over.</span></div>
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
/analyse cloud-program/source
/sabsa prepare cloud-program/sabsa — source material is under cloud-program/source
/sabsa create cloud-program/sabsa
/sabsa questions cloud-program/sabsa

Use the migration-and-cutover and design-to-operational-readiness workflows.
Show accountable roles, hand-offs, gate status, missing evidence and blockers.

/review cloud-program/sabsa
/publish cloud-program/architecture-review.json architecture-review-pack docx,pptx,html
```

## Illustrative checkpoints and expected output

```text
SABSA
- 36/36 matrix cells addressed
- 0 structural errors
- 3 client questions remain open

Material risks
R-014 privileged cloud administration is not attributable end-to-end
R-019 recovery dependency on one identity plane exceeds stated RTO
R-027 backup-copy residency is assumed, not evidenced

Cutover blockers
- rollback boundary not approved
- recovery exercise evidence missing
- CMDB/service ownership hand-over incomplete
```

## Expected artefacts

- SABSA architecture library and matrix status
- target architecture / EA views
- cloud risk and assurance pack
- migration and cutover plan
- operational-readiness assessment
- Architecture Review Board pack
- open-question and residual-risk register

## Why this example matters

The value is the full chain from business drivers and architecture to cutover and operational evidence — not merely a cloud diagram.
