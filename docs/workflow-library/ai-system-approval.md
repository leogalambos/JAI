# AI system from idea to approved production use

## Trigger

A business area wants to deploy a model or an AI-assisted workflow.

## Intended outcome

An AI system classified, assessed, monitored, and accountable to a named human.


<!-- BEGIN workflow-applicability -->
## Context and mechanism applicability

Use the actual bounded request, current environment and decision rights to select one applicable mechanism variant. Unknown applicability remains pending; the routing record grants no authority.

**Invariant outcomes:**

- An AI system classified, assessed, monitored, and accountable to a named human.
- Retain source-version traceability, accountable receiving duties and every applicable existing gate.

| Context | Mechanisms | Required evidence |
| --- | --- | --- |
| candidate-only | Develop and evaluate without production or pilot effects | Held-out performance, harms, exclusions and adversarial test scope |
| bounded-pilot | Operate only after exact prior human pilot approval | Pilot users/data/environment, safeguards, monitoring and stop conditions |
| production | Operate the exact authorised version with lineage, thresholds and challenge route | Prior production decision, actual deployment and monitoring evidence |

Return failed evaluations or material changes to model/data/design owners, then seek the necessary renewed decision. Stop pilot/production effects without current exact human approval or when harmful-output/expiry triggers require it. Reject, retire or continue a bounded approved scope with review dates, challenge route and accountable data/model disposition. Mechanism selection is not a waiver of security, legal or acceptance obligations.

**Entry information (selected once per actual context version):**

- Intended use, users and accountable human
- Permitted data and evaluation scope
- Risk classification and applicable model obligations

Select intake and mechanism variant once per actual context version. Carry the reviewed record by versioned evidence reference. Reuse unchanged evidence; recheck mutable prerequisites only at the action they govern. A new context version requires its own relevant review, not reconstruction of historical work.

**Continuation, rework, stop and exit:**

- **continue** — The current handoff criteria and applicable prerequisites are satisfied. Continue to the registered receiving duty with exact output and evidence references.
- **rework** — A current criterion fails or required information changes. Return failed evaluations or material changes to model/data/design owners, then seek the necessary renewed decision.
- **stop** — An applicable authority, legal, safety or mandatory-control boundary forbids the effect. Stop pilot/production effects without current exact human approval or when harmful-output/expiry triggers require it.
- **exit** — The bounded outcome is accepted or the entitled owner rejects, cancels or defers the scope. Reject, retire or continue a bounded approved scope with review dates, challenge route and accountable data/model disposition.

**Bounded paths and scope:**

Candidate-only scope terminates after candidate/adversarial evidence and cannot pass into deployment; pilot and production retain exact prior human scope.

| Selected path | Applicable stages | Terminal stage |
| --- | --- | ---: |
| candidate-only | 1, 2, 3, 4, 5 | 5 |
| bounded-pilot | 1, 2, 3, 4, 5, 6, 7, 8, 9 | 9 |
| production | 1, 2, 3, 4, 5, 6, 7, 8, 9 | 9 |

A path with a separate mechanism requires that explicit mechanism selection in the versioned intake record. Unknown selection remains pending. Later out-of-scope stages cannot claim acceptance; a terminal exit still needs the registered exact-scope authority.
<!-- END workflow-applicability -->

<!-- JAI:WORKFLOW-DIAGRAM:START -->
<div class="ai-workflow-overview">
<ol class="ai-workflow-steps" role="list" aria-label="AI system from idea to approved production use workflow steps">
<li data-step="1"><span class="ai-workflow-step-number" aria-hidden="true">1</span><div><strong>AI Governance Officer</strong><p>registers the use case and classifies its risk</p></div></li>
<li data-step="2"><span class="ai-workflow-step-number" aria-hidden="true">2</span><div><strong>Data Protection Officer</strong><p>assesses lawfulness of the data and the decisioning</p></div></li>
<li data-step="3"><span class="ai-workflow-step-number" aria-hidden="true">3</span><div><strong>Data Scientist</strong><p>builds and characterises a candidate model within the explicitly permitted pre-production scope</p></div></li>
<li data-step="4"><span class="ai-workflow-step-number" aria-hidden="true">4</span><div><strong>AI and ML Architect</strong><p>designs serving, monitoring and the human override path</p></div></li>
<li data-step="5"><span class="ai-workflow-step-number" aria-hidden="true">5</span><div><strong>AI Safety and Model Red Team Specialist</strong><p>assesses the candidate deployment configuration for harm and misuse within the authorised test scope</p></div></li>
<li data-step="6"><span class="ai-workflow-step-number" aria-hidden="true">6</span><div><strong>Named authority</strong><p>records the human deployment and operating decision on the reviewed candidate</p></div></li>
<li data-step="7"><span class="ai-workflow-step-number" aria-hidden="true">7</span><div><strong>Machine Learning Engineer</strong><p>deploys the exact approved model and configuration with full lineage</p></div></li>
<li data-step="8"><span class="ai-workflow-step-number" aria-hidden="true">8</span><div><strong>MLOps Engineer</strong><p>operates the approved lifecycle with monitoring and rollback</p></div></li>
<li data-step="9"><span class="ai-workflow-step-number" aria-hidden="true">9</span><div><strong>AI Governance Officer</strong><p>coordinates periodic reassessment and routes material changes for renewed human approval</p></div></li>
</ol>
</div>

[Open the full-size workflow diagram](../assets/diagrams/workflow-ai-system-approval.svg). Follow the numbered order. The table below specifies the outputs and receiving conditions for each handoff.
<!-- JAI:WORKFLOW-DIAGRAM:END -->

## Workflow steps and gates

| Step | Accountable role | Activity | Handover | Gate |
| ---: | --- | --- | --- | --- |
| 1 | AI Governance Officer | registers the use case and classifies its risk | risk classification and inventory entry | No production AI without a classification and an accountable human |
| 2 | Data Protection Officer | assesses lawfulness of the data and the decisioning | privacy and fairness position | Impact assessment before processing, not retrospectively |
| 3 | Data Scientist | builds and characterises a candidate model within the explicitly permitted pre-production scope | candidate model with held-out performance and stated limits | Permitted data and test scope are explicit; no production or pilot use before named human approval; failure modes and excluded populations are stated |
| 4 | AI and ML Architect | designs serving, monitoring and the human override path | serving and monitoring architecture | Drift, degradation and harmful-output monitoring designed in |
| 5 | AI Safety and Model Red Team Specialist | assesses the candidate deployment configuration for harm and misuse within the authorised test scope | adversarial findings with severity and owners | Candidate tests use the intended configuration without production or pilot effects; any offensive testing requires prior written authorisation |
| 6 | Named authority | records the human deployment and operating decision on the reviewed candidate | exact scoped human approval or rejection | Candidate evidence, privacy, safety, lineage, monitoring and rollback readiness are reviewed before any production or pilot effect; an agent cannot approve |
| 7 | Machine Learning Engineer | deploys the exact approved model and configuration with full lineage | authorised deployed version and reproducible training lineage | Prior named human approval covers the exact version, data, users, environment and production or pilot scope; every deployed version is traceable to its training run |
| 8 | MLOps Engineer | operates the approved lifecycle with monitoring and rollback | monitored model with defined thresholds and rollback | Prior named human approval covers operation and rollback scope; thresholds and an authorised rollback route exist |
| 9 | AI Governance Officer | coordinates periodic reassessment and routes material changes for renewed human approval | periodic assessment, challenge route and next review trigger | The challenge route is published; expired or materially changed scope is not operated without renewed prior human approval |

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

> Apply the `ai-system-approval` workflow to this situation. For each step, identify the current state, accountable role, required evidence, hand-over artefact, gate status and unresolved blocker. Do not skip a gate merely because the implementation is technically complete.

## Operational interpretation

The workflow is most useful when the team keeps each hand-over explicit. The system can help generate or review the artefacts, but the accountable role and approval decision remain organisational responsibilities.

Approval and execution are separate handoffs. Candidate preparation stays within explicitly permitted pre-production scope. Every production, pilot, credential or irreversible effect requires prior exact named human authority under the applicable policy. If operational proof is required before a wider approval, obtain separate prior authorisation for the bounded pilot needed to collect it; if no policy route permits collection, stop and consult the authority. Draft rendering and review evidence do not release a publication. An existing policy-permitted waiver must identify the competent human authority, exact gate and scope, and validity period before the gated action; mandatory controls and unsupported factual claims remain blocking.
