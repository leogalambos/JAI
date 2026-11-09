# Architecture model to repository governance

## Trigger

A project/domain architecture needs to become a governed enterprise repository model and published view set.

## Intended outcome

Canonical model facts, cross-project dependencies, Open Exchange interchange and published views are consistent, reviewable and traceable to named owners.


<!-- BEGIN workflow-applicability -->
## Context and mechanism applicability

Use the actual bounded request, current environment and decision rights to select one applicable mechanism variant. Unknown applicability remains pending; the routing record grants no authority.

**Invariant outcomes:**

- Canonical model facts, cross-project dependencies, Open Exchange interchange and published views are consistent, reviewable and traceable to named owners.
- Retain source-version traceability, accountable receiving duties and every applicable existing gate.

| Context | Mechanisms | Required evidence |
| --- | --- | --- |
| native-model | Maintain source semantics and governed canonical identities | Exact revisions, ownership and integrity results |
| interchange | Assess supported format and observable losses without inventing tool qualification | Export/import artifacts, exact format profile and loss disposition |

Return inconsistent source facts to their owner and exchange losses to the mapping/repository owner. Stop publication/release with blocking identity/reference errors, unsupported semantic reinterpretation or missing authority. Publish an explicitly bounded reviewed revision or reject/defer release with owned exceptions and review dates. Mechanism selection is not a waiver of security, legal or acceptance obligations.

**Entry information (selected once per actual context version):**

- Exact source model and project boundary
- Stable identifier namespace and evidence
- Selected notation/exchange profile and ownership rules

Select intake and mechanism variant once per actual context version. Carry the reviewed record by versioned evidence reference. Reuse unchanged evidence; recheck mutable prerequisites only at the action they govern. A new context version requires its own relevant review, not reconstruction of historical work.

**Continuation, rework, stop and exit:**

- **continue** — The current handoff criteria and applicable prerequisites are satisfied. Continue to the registered receiving duty with exact output and evidence references.
- **rework** — A current criterion fails or required information changes. Return inconsistent source facts to their owner and exchange losses to the mapping/repository owner.
- **stop** — An applicable authority, legal, safety or mandatory-control boundary forbids the effect. Stop publication/release with blocking identity/reference errors, unsupported semantic reinterpretation or missing authority.
- **exit** — The bounded outcome is accepted or the entitled owner rejects, cancels or defers the scope. Publish an explicitly bounded reviewed revision or reject/defer release with owned exceptions and review dates.

**Bounded paths and scope:**

Native and interchange paths share semantic integrity; native-only scope does not assert exported files or external-tool qualification.

| Selected path | Applicable stages | Terminal stage |
| --- | --- | ---: |
| native-model | 1, 2, 3, 4, 5, 6 | 6 |
| interchange | 1, 2, 3, 4, 5, 6 | 6 |

A path with a separate mechanism requires that explicit mechanism selection in the versioned intake record. Unknown selection remains pending. Later out-of-scope stages cannot claim acceptance; a terminal exit still needs the registered exact-scope authority.
<!-- END workflow-applicability -->

<!-- JAI:WORKFLOW-DIAGRAM:START -->
<div class="ai-workflow-overview">
<ol class="ai-workflow-steps" role="list" aria-label="Architecture model to repository governance workflow steps">
<li data-step="1"><span class="ai-workflow-step-number" aria-hidden="true">1</span><div><strong>Solution Architect</strong><p>finalises project model facts, decisions and project ownership boundaries</p></div></li>
<li data-step="2"><span class="ai-workflow-step-number" aria-hidden="true">2</span><div><strong>Architecture Repository and Modelling Lead</strong><p>maps model facts into the canonical repository/metamodel and repository conventions</p></div></li>
<li data-step="3"><span class="ai-workflow-step-number" aria-hidden="true">3</span><div><strong>Architecture Repository Engineer</strong><p>imports/updates the canonical repository, preserving IDs, lifecycle and provenance</p></div></li>
<li data-step="4"><span class="ai-workflow-step-number" aria-hidden="true">4</span><div><strong>Model Consistency Reviewer</strong><p>checks references, orphans, cross-project ownership, lifecycle conflicts and view drift</p></div></li>
<li data-step="5"><span class="ai-workflow-step-number" aria-hidden="true">5</span><div><strong>Enterprise Architect</strong><p>resolves enterprise/domain overlap, shared elements and portfolio dependencies</p></div></li>
<li data-step="6"><span class="ai-workflow-step-number" aria-hidden="true">6</span><div><strong>Technical Design Authority Member</strong><p>applies architecture governance to material conformance/exception decisions</p></div></li>
</ol>
</div>

[Open the full-size workflow diagram](../assets/diagrams/workflow-architecture-model-to-repository-governance.svg). Follow the numbered order. The table below specifies the outputs and receiving conditions for each handoff.
<!-- JAI:WORKFLOW-DIAGRAM:END -->

## Workflow steps and gates

| Step | Accountable role | Activity | Handover | Gate |
| ---: | --- | --- | --- | --- |
| 1 | Solution Architect | finalises project model facts, decisions and project ownership boundaries | project architecture model and source artefacts | Elements/relationships have stable identities and evidence basis |
| 2 | Architecture Repository and Modelling Lead | maps model facts into the canonical repository/metamodel and repository conventions | canonical project model | No model fact is silently reinterpreted to fit a tool |
| 3 | Architecture Repository Engineer | imports/updates the canonical repository, preserving IDs, lifecycle and provenance | repository revision plus interchange artefacts | Repository structural validation passes |
| 4 | Model Consistency Reviewer | checks references, orphans, cross-project ownership, lifecycle conflicts and view drift | consistency findings/gate | No blocking integrity error remains |
| 5 | Enterprise Architect | resolves enterprise/domain overlap, shared elements and portfolio dependencies | accepted enterprise model/repository decisions | Cross-project dependencies and reusable/reference elements have owners |
| 6 | Technical Design Authority Member | applies architecture governance to material conformance/exception decisions | approved/rejected repository release | Exceptions and residual risks have named authority and expiry/review |

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

> Apply the `architecture-model-to-repository-governance` workflow to this situation. For each step, identify the current state, accountable role, required evidence, hand-over artefact, gate status and unresolved blocker. Do not skip a gate merely because the implementation is technically complete.

## Operational interpretation

The workflow is most useful when the team keeps each hand-over explicit. The system can help generate or review the artefacts, but the accountable role and approval decision remain organisational responsibilities.
