# Access request to periodic review

## Trigger

Someone needs access, changes role, or leaves.

## Intended outcome

Access that is appropriate, evidenced, and removed when no longer needed.


<!-- BEGIN workflow-applicability -->
## Context and mechanism applicability

Use the actual bounded request, current environment and decision rights to select one applicable mechanism variant. Unknown applicability remains pending; the routing record grants no authority.

**Invariant outcomes:**

- Access that is appropriate, evidenced, and removed when no longer needed.
- Retain source-version traceability, accountable receiving duties and every applicable existing gate.

| Context | Mechanisms | Required evidence |
| --- | --- | --- |
| ordinary | Apply least-privilege decisions and integrated provisioning | Specific decision, actual grant/refusal and revocation evidence |
| privileged | Apply vaulting, session monitoring and reviewed break-glass arrangements | Privileged decision, monitoring and exercised emergency access |
| leaver-transfer | Revoke or transfer entitlements at the actual lifecycle event | Event, actual revocations, residual access owner and expiry |

Return purpose-free or ambiguous requests to the requester/data owner; failed provisioning returns to IAM with actual observations. Stop granting access without a valid individual decision, required identity proof or current privileged-access scope. Close on evidenced grant/refusal/revocation; retain certification and independent audit findings with owners. Mechanism selection is not a waiver of security, legal or acceptance obligations.

**Entry information (selected once per actual context version):**

- Subject identity and requested entitlement
- Justified use purpose and asset policy
- Approval path and identity lifecycle event

Select intake and mechanism variant once per actual context version. Carry the reviewed record by versioned evidence reference. Reuse unchanged evidence; recheck mutable prerequisites only at the action they govern. A new context version requires its own relevant review, not reconstruction of historical work.

**Continuation, rework, stop and exit:**

- **continue** — The current handoff criteria and applicable prerequisites are satisfied. Continue to the registered receiving duty with exact output and evidence references.
- **rework** — A current criterion fails or required information changes. Return purpose-free or ambiguous requests to the requester/data owner; failed provisioning returns to IAM with actual observations.
- **stop** — An applicable authority, legal, safety or mandatory-control boundary forbids the effect. Stop granting access without a valid individual decision, required identity proof or current privileged-access scope.
- **exit** — The bounded outcome is accepted or the entitled owner rejects, cancels or defers the scope. Close on evidenced grant/refusal/revocation; retain certification and independent audit findings with owners.

**Bounded paths and scope:**

Ordinary/privileged/lifecycle requests require the actual decision, identity lifecycle evidence and applicable privileged-control disposition; no access event is inferred.

| Selected path | Applicable stages | Terminal stage |
| --- | --- | ---: |
| ordinary | 1, 2, 3, 5, 6 | 6 |
| privileged | 1, 2, 3, 4, 5, 6 | 6 |
| leaver-transfer | 1, 2, 3, 5, 6 | 6 |

A path with a separate mechanism requires that explicit mechanism selection in the versioned intake record. Unknown selection remains pending. Later out-of-scope stages cannot claim acceptance; a terminal exit still needs the registered exact-scope authority.
<!-- END workflow-applicability -->

<!-- JAI:WORKFLOW-DIAGRAM:START -->
<div class="ai-workflow-overview">
<ol class="ai-workflow-steps" role="list" aria-label="Access request to periodic review workflow steps">
<li data-step="1"><span class="ai-workflow-step-number" aria-hidden="true">1</span><div><strong>Service Desk Analyst</strong><p>records the request against a catalogue entitlement</p></div></li>
<li data-step="2"><span class="ai-workflow-step-number" aria-hidden="true">2</span><div><strong>Data Owner</strong><p>or application owner decides whether the purpose justifies access</p></div></li>
<li data-step="3"><span class="ai-workflow-step-number" aria-hidden="true">3</span><div><strong>Identity and Access Management Engineer</strong><p>provisions through the identity platform</p></div></li>
<li data-step="4"><span class="ai-workflow-step-number" aria-hidden="true">4</span><div><strong>Privileged Access Management Administrator</strong><p>vaults and monitors anything privileged</p></div></li>
<li data-step="5"><span class="ai-workflow-step-number" aria-hidden="true">5</span><div><strong>Identity Governance Specialist</strong><p>certifies periodically that access is still appropriate</p></div></li>
<li data-step="6"><span class="ai-workflow-step-number" aria-hidden="true">6</span><div><strong>Internal IT Auditor</strong><p>tests the control independently</p></div></li>
</ol>
</div>

[Open the full-size workflow diagram](../assets/diagrams/workflow-access-request-to-review.svg). Follow the numbered order. The table below specifies the outputs and receiving conditions for each handoff.
<!-- JAI:WORKFLOW-DIAGRAM:END -->

## Workflow steps and gates

| Step | Accountable role | Activity | Handover | Gate |
| ---: | --- | --- | --- | --- |
| 1 | Service Desk Analyst | records the request against a catalogue entitlement | request with entitlement and approval path | Entitlement and approval path defined for the request type |
| 2 | Data Owner | or application owner decides whether the purpose justifies access | access decision recorded with its purpose | Purpose-free access grants refused |
| 3 | Identity and Access Management Engineer | provisions through the identity platform | provisioned access, automated where integrated | Leaver revocation evidenced automatically, not attested |
| 4 | Privileged Access Management Administrator | vaults and monitors anything privileged | vaulted account with session monitoring | Break-glass tested on a schedule; every use reviewed |
| 5 | Identity Governance Specialist | certifies periodically that access is still appropriate | certification campaign results | Reviewers have actual knowledge of the access |
| 6 | Internal IT Auditor | tests the control independently | audit finding or assurance | Auditor never operated the control |

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

> Apply the `access-request-to-review` workflow to this situation. For each step, identify the current state, accountable role, required evidence, hand-over artefact, gate status and unresolved blocker. Do not skip a gate merely because the implementation is technically complete.

## Operational interpretation

The workflow is most useful when the team keeps each hand-over explicit. The system can help generate or review the artefacts, but the accountable role and approval decision remain organisational responsibilities.
