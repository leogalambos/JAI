# Running a layered justifiable engagement

Owner: JAI maintainers · Last reviewed: 2026-10-16

First choose the assurance boundary using [the methodical workflow guide](methodical-workflows.md). `/layered` can govern creation with an explicitly named domain such as `sabsa-library` or `commercial-delivery`, or justify a new decision using an existing domain model as evidence. A later decision does not retroactively establish the model's creation history. Standalone domain workflows remain valid for their own scope.

Use a layered engagement when the output is consequential: somebody may act on it, approve it, publish it, change a production system because of it, or later need to defend why it was allowed.

Choose the high-level entry point for your provider:

=== "Claude Code"

    ```text
    /layered <consequential intent>
    ```

=== "Codex CLI"

    ```text
    $workflow-layered <consequential intent>
    ```

Enter the selected command in the provider conversation, not in a system shell.

The runtime then uses six JAI responsibility layers plus the external L0 Human Authority boundary. The layers are not six mandatory LLM calls: deterministic checks, several agents or human specialists may exist inside a layer. What is mandatory inside a layered engagement is preservation of the relevant contracts, evidence, review and authority boundaries.

<div class="ai-diagram ai-diagram-inline">
  <img src="../../assets/diagrams/layered-runtime-cycle.svg" alt="Requirements descend through the JAI layers while evidence, review and escalation ascend to human authority">
</div>

## Operator journey: starting a layered engagement

Start **inside the target workspace** (the Fabric lives under that workspace unless `FABRIC_HOME` is configured). You do not initialise `.fabric/`, call `fabric.py`, construct JSON contracts or invoke L1–L6 agents yourself.

=== "Claude Code"

    ```text
    /layered Assess whether invoice-service can be exposed to external partners. Explain the material risks, gather evidence, challenge the proposal and escalate any residual-risk acceptance to me.
    ```

=== "Codex CLI"

    ```text
    $workflow-layered Assess whether invoice-service can be exposed to external partners. Explain the material risks, gather evidence, challenge the proposal and escalate any residual-risk acceptance to me.
    ```

The operator and the provider have different responsibilities:

| Phase | You (the human operator) | Claude/Codex and the installed AI IT House runtime |
| --- | --- | --- |
| Scope | Specify the original intent, project files, constraints, success conditions and accountable authority. | Preserve intent verbatim; initialise the engagement; derive the first L1 requirement. |
| Decompose | Answer questions about missing inputs; approve only the tool permissions you intend to grant. | Issue adjacent-layer typed contracts and context packets; delegate within the available tool/agent boundaries. |
| Execute and test | Make required workspaces and evidence accessible; do not substitute a verbal success claim for a test result. | Separate L5 authoring from L6 checking; record observations, failures, hashes and upward reviews. |
| Resolve failure | Clarify desired outcome when asked; decide whether a business/policy constraint may change. | Apply bounded rework or owner-controlled reformulation; relay matters outside authority upward without hiding failed attempts. |
| L0 authority | Examine the exact decision dossier and make the decision yourself. In either provider, review/sign the exact request externally; Fabric verifies the Ed25519 receipt and current state. Native permission prompts are not L0. | Prepare dossier and proposal; **never** forge approval, run a denied Codex authority operation, or silently bypass the gate. |
| Review result | Inspect outputs and request an independent report, then decide on their use. | Run strict eligibility checks and preserve the distinction between produced, evidenced, reviewed and authorised outputs. |

After the engagement, ask for the assurance record:

=== "Claude Code"

    ```text
    /fabric-report
    ```

=== "Codex CLI"

    ```text
    $workflow-fabric-report
    ```

Ask the assistant to report **engagement ID, artefact/fragment IDs, failing or accepted gates, evidence references, open conflicts, pending human authority acts and release eligibility**. The report must not conceal uncertainty or present an unaccepted draft as a released product. Use [the installed CLI guide](../reference/installed-cli-guide.md) for general provider syntax and [Human authority](../operations/human-authority.md) for the exceptional human-only operation.

**Execution boundary:** `/layered` and `$workflow-layered` are **agent-orchestrated** capabilities. They instruct the provider to call the runtime tools; they are not a guarantee that a tool actually ran. If the provider cannot call an agent, collect evidence or obtain approval, the process must stop at the relevant gate and report why. Organisation-wide automatic routing of *every* consequential request into the layered path is not enforced by the current release; deployments requiring that must apply an entry policy/control.

## Behind the scenes: implementation and diagnostic trace

The remaining sections explain **what the installed agent and Fabric runtime do**, using the actual Python CLI interface so engineers can reproduce and diagnose the state transitions. **The `python3` examples are not additional steps required of a normal Codex/Claude user.** Do not run example commands with literal `<engagement>` or `<contract-id>` placeholders. External operator steps use the same signed-receipt flow in both providers; native approval UI is not Fabric authority. See the [operator walkthrough](../operations/operator-walkthrough.md).

### 1. Start with the operator's intent

The **orchestrating agent**, not the operator, records the human intent verbatim before decomposition using the runtime API:

```bash
python3 ~/.ai/it-role-house/fabric/fabric.py init <engagement> \
  --intent "<operator intent verbatim>" --owner "<operator>"

python3 ~/.ai/it-role-house/fabric/fabric.py req <engagement> \
  --layer 1 --from intent-0001 --label derives --text "<top requirement>"
```

The verbatim intent matters because later reformulations must not silently rewrite the original purpose.

### 2. Requirements descend through typed contracts

Each adjacent downward hop is a contract. A production contract contains all of these fields:

- `what` — required result;
- `why` — purpose that must be preserved;
- `who` — responsible or participating roles;
- `where` — scope/environment;
- `when` — timing or lifecycle condition;
- `how` — permitted transformation approach;
- `evidence` — what would establish the result;
- `escalate_if` — conditions outside the local authority or recovery path;
- `sanitise` — context/data restrictions.

The runtime renders a canonical context packet and computes a SHA-256 context digest. An agent result must echo the matching digest; `fabric.py` rejects a result bound to another packet.

```bash
python3 ~/.ai/it-role-house/fabric/fabric.py render-contract <engagement> <contract-id>
python3 ~/.ai/it-role-house/fabric/fabric.py context-packet <engagement> <contract-id>
```

Layer agents do not delegate to arbitrary other layers. The orchestrator mediates each hop and the fabric rejects illegal non-adjacent transformation edges.

### 3. Making and measuring are separated

The production/evidence split is deliberate:

- **L5 Realisation and Tooling** can create or modify implementation artefacts but does not run the evidence checks that prove its own work;
- **L6 Execution and Evidence** performs permitted checks and captures observations but has no normal Write/Edit capability for the artefact being measured.

This is the required segregation-of-duties design. Its actual strength depends on the host enforcing tool and workspace boundaries; different role names or prompt instructions alone do not prove isolation. Report which controls were tested for the deployed provider and which are unavailable or unverified.

When L6 references an evidence file, `fabric.py` records its digest. Later evidence drift makes the dependent release ineligible until it is re-evaluated.

### 4. Products are reviewed upward

The return path is not summarisation. Each receiving layer reviews the child product against its own obligation before using it.

```bash
python3 ~/.ai/it-role-house/fabric/fabric.py render-review <engagement> <contract-id>
python3 ~/.ai/it-role-house/fabric/fabric.py ingest-reviews <engagement> \
  --layer <n> --reviewer <reviewer> --model <resolved-model-or-class> reviews.json
```

A layer may answer its parent only from child fragments it has accepted. Unsupported or rejected child work cannot simply be promoted upward by a persuasive summary.

The [complete ordinary CLI example](../operations/normal-layered-workflow.md)
shows explicit relevant input obligations, exact source bindings and the
full six-layer path. Missing obligations or bindings remain ineligible.

#### Review states

| State | Strict release meaning | Typical response |
| --- | --- | --- |
| `accepts` | qualifying | continue upward |
| `accepts_with_constraints` | qualifying only with carried conditions | continue with constraints |
| `correlates` | not enough for strict release | rework for direct support |
| `resonates` | not enough for strict release | obtain direct evidence |
| `insufficient` | blocking | rework |
| `out_of_scope` | blocking | route/rescope |
| `conflicts` | blocking | conflict, then rework/reformulate/escalate |
| `escalate` | blocking | escalate |

Paper-mode justifiability exists to inspect the published formal definition. **Strict mode is the release mode.**

### 5. Failures are first-class records

A failed provider call, tool call or evidence collection is not an invisible retry. Record it:

```bash
python3 ~/.ai/it-role-house/fabric/fabric.py failure <engagement> \
  --contract <contract-id> --state timeout \
  --actor <layer-agent> --model '<model>' --reason '<reason>'
```

Retryable states include `failed`, `unavailable`, `timeout`, `ambiguous` and `insufficient`. Contradiction states are `contradicted` and `conflicting`.

The deterministic supervision policy decides the legal recovery category. The model does not grant itself a new retry budget.

### 6. Rework, reformulation and escalation are different

These mechanisms are intentionally not interchangeable.

| Mechanism | Meaning | Who may do it | Bound |
| --- | --- | --- | ---: |
| **Rework** | better attempt at the **same** requirement | orchestrated local producer path | 3 per contract lineage |
| **Reformulation** | issue a **different** requirement because the current one is infeasible or inadequate | layer that **issued/owns** the requirement | 2 per layer per round |
| **Escalation** | move an unresolved or authority-sensitive matter upward | current layer/orchestrator | one layer per hop |

Rework is not allowed to change `what`, `why`, the evidence obligation or `escalate_if`. Changing those fields requires a formal reformulation by the owning layer.

Authority matters are sticky. Risk acceptance, scope change, removal of a mandatory control or reinterpretation of intent cannot be repaired by a lower layer rewriting the requirement. They climb toward L0 Human Authority.

<div class="ai-diagram ai-diagram-inline">
  <img src="../../assets/diagrams/layered-state-machine.svg" alt="State machine for review, rework, reformulation, escalation and human authority">
</div>

### 7. The episode is bounded

Default limits are:

| Control | Default |
| --- | ---: |
| Rework attempts | 3 per contract lineage |
| Reformulations | 2 per layer per round |
| Contracts | 40 per round |
| Human revision rounds | 5 before explicit override |
| Shared episode steps | 120 |

All continuation-capable transitions consume the shared `FABRIC_MAX_STEPS` budget. Exhaustion stops autonomous continuation but **must not block escalation to the operator**.

This prevents the apparently harmless failure mode where an agent keeps retrying, rephrasing or spawning delegated work indefinitely.

### 8. Human escalation is a real boundary

When an escalation reaches L1 and cannot be resolved within its authority, the system creates a dossier. `authority-liaison` may explain the options, but it cannot decide or record the authority act. The agent normally invokes the following read-only command; the human receives its result in the provider conversation.

```bash
python3 ~/.ai/it-role-house/fabric/fabric.py dossier <engagement> <escalation-id>
```

The operator may decide:

- `accept`;
- `exception` with rationale/expiry;
- `revise`;
- `reject`;
- `terminate`.

A `revise` decision creates a new L1 generation and starts a new round. It does not overwrite the earlier intent, attempts or reviews.

See [Human authority and escalation](../operations/human-authority.md) for provider-specific enforcement details.

### 9. Release is a separate act

Finishing L1 does not make a product releasable. The release gate checks strict justifiability, current review/authority state, fabric integrity and evidence-file hashes.

```bash
python3 ~/.ai/it-role-house/fabric/fabric.py justify <engagement> <fragment-id> --strict
python3 ~/.ai/it-role-house/fabric/fabric.py verify <engagement>
python3 ~/.ai/it-role-house/fabric/fabric.py release <engagement> <fragment-id>
```

If a depended-on observation is superseded, revoked or otherwise invalidated:

```bash
python3 ~/.ai/it-role-house/fabric/fabric.py invalidate <engagement> \
  --changed <record-id> --reason '<reason>' --request-out invalidation-plan.json
```

This only prepares a pending lifecycle plan. The external human signs with
`lifecycle-update` capability and performs protected `lifecycle-apply` with its
exact request and returned receipt. Applied effects cancel dependent conclusions,
reviews, acceptance and permissions across scopes. Obtain fresh verification,
independent review and new separate human acceptance before later use. See
[lifecycle recovery](../operations/lifecycle-recovery.md) for commands and receipt
paths; no cancelled proof or historical acceptance is inherited.

### 10. Inspect and audit

The following are **developer/maintainer diagnostics**. Ordinary users should request `/fabric-report` or `$workflow-fabric-report` from the provider rather than type these commands themselves.

```bash
python3 ~/.ai/it-role-house/fabric/fabric.py status <engagement>
python3 ~/.ai/it-role-house/fabric/fabric.py report <engagement>
python3 ~/.ai/it-role-house/fabric/fabric.py justify <engagement> --strict
python3 ~/.ai/it-role-house/fabric/fabric.py verify <engagement>
python3 ~/.ai/it-role-house/fabric/fabric.py selftest
```

The shipped runtime self-test exercises adjacency, review direction, evidence requirements, bounded rework, reformulation ownership, upward-only escalation, sticky authority matters, human revision, termination and evidence invalidation.

## Enforcement scope

The JAI core is the normative architecture of the product, and the controls above are enforced **inside a layered engagement**. However, the product still exposes direct role/workflow surfaces for ordinary work. The current `role-router` does not deterministically force every consequential request into `/layered` before any other operator path can run.

Therefore the accurate deployment statement is:

> **AI IT House is layered-capable and strongly enforced once a layered engagement is opened; organisations that require layered-by-construction for every consequential task must add an entry-routing policy/control that makes `/layered` mandatory for those task classes.**

Do not describe the presence of JAI metadata alone as proof that every possible invocation path passed through a supervised layered episode.
