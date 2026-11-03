# Cyber incident / breach to recovery

## Trigger

A suspected or confirmed cyber incident may affect systems, data, customers, regulatory obligations or business operations.

## Intended outcome

The incident is contained and eradicated, evidence is preserved, recovery is accepted by the business, notification decisions are traceable, and control remediation is closed or owned.


<!-- JAI:WORKFLOW-DIAGRAM:START -->
<div class="ai-workflow-overview">
<ol class="ai-workflow-steps" role="list" aria-label="Cyber incident / breach to recovery workflow steps">
<li data-step="1"><span class="ai-workflow-step-number" aria-hidden="true">1</span><div><strong>Security Analyst Tier 1</strong><p>detects and records the alert/incident with initial facts and provenance</p></div></li>
<li data-step="2"><span class="ai-workflow-step-number" aria-hidden="true">2</span><div><strong>Incident Responder</strong><p>triages severity, scope, likely attack path and immediate priorities</p></div></li>
<li data-step="3"><span class="ai-workflow-step-number" aria-hidden="true">3</span><div><strong>Incident Responder</strong><p>contains affected assets/accounts while preserving reversibility and evidence</p></div></li>
<li data-step="4"><span class="ai-workflow-step-number" aria-hidden="true">4</span><div><strong>Digital Forensics Examiner</strong><p>preserves and validates forensic evidence, chain of custody and timeline facts</p></div></li>
<li data-step="5"><span class="ai-workflow-step-number" aria-hidden="true">5</span><div><strong>IT Risk Manager</strong><p>assesses business, service, security and regulatory impact using verified facts</p></div></li>
<li data-step="6"><span class="ai-workflow-step-number" aria-hidden="true">6</span><div><strong>Data Protection Officer</strong><p>performs privacy/breach assessment and coordinates legal/regulatory decision inputs</p></div></li>
<li data-step="7"><span class="ai-workflow-step-number" aria-hidden="true">7</span><div><strong>Incident Responder</strong><p>eradicates malicious persistence/root causes and verifies the environment</p></div></li>
<li data-step="8"><span class="ai-workflow-step-number" aria-hidden="true">8</span><div><strong>Disaster Recovery Coordinator</strong><p>coordinates recovery sequencing, integrity validation and rollback/fallback readiness</p></div></li>
<li data-step="9"><span class="ai-workflow-step-number" aria-hidden="true">9</span><div><strong>IT Service Owner</strong><p>validates business/service recovery and accepts restored operating state</p></div></li>
<li data-step="10"><span class="ai-workflow-step-number" aria-hidden="true">10</span><div><strong>Crisis Manager</strong><p>coordinates customer/regulator/executive communications decision and timing where required</p></div></li>
<li data-step="11"><span class="ai-workflow-step-number" aria-hidden="true">11</span><div><strong>Problem Manager</strong><p>runs lessons learned/root-cause analysis across people/process/technology</p></div></li>
<li data-step="12"><span class="ai-workflow-step-number" aria-hidden="true">12</span><div><strong>Control Owner</strong><p>owns control remediation, target dates and evidence of completion</p></div></li>
<li data-step="13"><span class="ai-workflow-step-number" aria-hidden="true">13</span><div><strong>Internal IT Auditor</strong><p>independently verifies closure evidence for material incidents where governance requires</p></div></li>
</ol>
</div>

[Open the full-size workflow diagram](../assets/diagrams/workflow-cyber-incident-breach-to-recovery.svg). Follow the numbered order. The table below specifies the outputs and receiving conditions for each handoff.
<!-- JAI:WORKFLOW-DIAGRAM:END -->

## Workflow steps and gates

| Step | Accountable role | Activity | Handover | Gate |
| ---: | --- | --- | --- | --- |
| 1 | Security Analyst Tier 1 | detects and records the alert/incident with initial facts and provenance | incident record with source/time/scope | A real event or explicit false-positive rationale is recorded |
| 2 | Incident Responder | triages severity, scope, likely attack path and immediate priorities | triage decision and containment objectives | Severity/scope have evidence and an accountable incident lead |
| 3 | Incident Responder | contains affected assets/accounts while preserving reversibility and evidence | containment actions and status | Containment does not destroy material evidence without authority |
| 4 | Digital Forensics Examiner | preserves and validates forensic evidence, chain of custody and timeline facts | evidence register and forensic timeline | Evidence integrity, time source and custody are documented |
| 5 | IT Risk Manager | assesses business, service, security and regulatory impact using verified facts | impact assessment with uncertainty and affected obligations | Critical impact claims distinguish confirmed fact from inference |
| 6 | Data Protection Officer | performs privacy/breach assessment and coordinates legal/regulatory decision inputs | breach/notification decision basis | Notification/non-notification has correct authority, clock and evidence |
| 7 | Incident Responder | eradicates malicious persistence/root causes and verifies the environment | eradication evidence and residual technical risks | Known persistence and exploited control gaps are addressed or explicitly owned |
| 8 | Disaster Recovery Coordinator | coordinates recovery sequencing, integrity validation and rollback/fallback readiness | recovery evidence and service restoration status | Recovery uses trusted state/data and respects RTO/RPO/business priorities |
| 9 | IT Service Owner | validates business/service recovery and accepts restored operating state | business recovery acceptance | Service owner confirms agreed validation signals and residual limitations |
| 10 | Crisis Manager | coordinates customer/regulator/executive communications decision and timing where required | communication/regulatory action record | Communications are authorised, consistent and evidence-based |
| 11 | Problem Manager | runs lessons learned/root-cause analysis across people/process/technology | lessons learned and systemic findings | Findings address causes and failed controls, not only symptoms |
| 12 | Control Owner | owns control remediation, target dates and evidence of completion | control remediation plan | Every material finding has a control owner, due date and verification method |
| 13 | Internal IT Auditor | independently verifies closure evidence for material incidents where governance requires | closure assurance result | No open critical finding is silently closed or self-assured |

## Running this workflow: operator and implementer boundary

Use the next prompt in the provider conversation, not as a shell command.
You supply permitted inputs, actual owners, gate acceptance and authority for
real-system changes. The agent returns evidence and blockers; a listed stage
is not proof of execution, approval or release.

For consequential work, explicitly start `/layered` or `$workflow-layered`;
natural-language routing does not universally enforce Fabric. L0 authority
remains human, and Codex protected authority commands require the human's
trusted terminal. Follow the [interaction model](../using/interaction-model.md),
[layered engagement](../using/layered-engagement.md) and
[human authority](../operations/human-authority.md). Keep the workflow-specific
stop conditions and gates on this page.

## How to use this workflow

A practical prompt pattern is:

> Apply the `cyber-incident-breach-to-recovery` workflow to this situation. For each step, identify the current state, accountable role, required evidence, hand-over artefact, gate status and unresolved blocker. Do not skip a gate merely because the implementation is technically complete.

## Operational interpretation

The workflow is most useful when the team keeps each hand-over explicit. The system can help generate or review the artefacts, but the accountable role and approval decision remain organisational responsibilities.
