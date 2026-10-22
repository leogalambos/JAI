---
owner: JAI documentation maintainers
review_due: 2027-01-16
---

# Choosing and running a methodical workflow

JAI separates **the discipline used to do the work** from **the process used to justify a result for a particular use**. `/sabsa` supplies security-architecture methods. `/commercial` supplies supplier-side commercial methods. `/layered` supplies six-layer contract, evidence, review and escalation orchestration. Choose the domain and the assurance boundary together.

This is the methodological chapter of [How to use JAI](../examples/how-to-use-JAI/index.md). Read the explanation here, then follow the adjacent worked cases. The cases are instructional sequences, not reports of completed provider executions.

## 1. Choose what the engagement must establish

| Mode | Choose it when | What the record establishes |
| --- | --- | --- |
| **Direct domain workflow** | You need a maintained domain model with its own authoring, checks and independent review. | The domain checks, findings, evidence and snapshot state actually recorded. It does not automatically establish a complete six-layer execution history. |
| **Layered creation with a named domain** | The creation process itself must preserve intent, typed obligations, independent review and escalation through L1–L6. | The work actually recorded in Fabric, subject to evidence, review, authority and deployment controls. |
| **Domain work followed by a layered decision** | A model exists and a new decision must be justified: issue a bid, accept residual risk or release a system. | Justification of the new decision against an exact snapshot and supporting evidence. It does not retrospectively prove how the model was created. |

The decisive question is **whether you need to justify creation, a later decision, or both**. Your organisation may require layered creation for particular classes of work. Starting `/layered` after authoring can assess the available result and reveal deficiencies; it cannot manufacture missing historical contracts, isolation or reviews.

The arrangements are alternatives, not a compulsory `/sabsa` → `/commercial` → `/layered` sequence. `/sabsa` is not a general implementation command: it maintains security architecture. Code and infrastructure realisation use the appropriate delivery workflow. Commercial delivery spans bidding, realisation and service economics; it is not confined to writing a sales document.

### Why the worked cases use different commands

| Case | Chosen arrangement | Why `/layered` appears, or does not |
| --- | --- | --- |
| [Security assessment](../examples/how-to-use-JAI/security-assessment.md) | Direct SABSA workflow | The main exercise ends with assessment, a roadmap and model-owner approval. It makes no formal release/risk-acceptance decision. An optional extension introduces a new decision scope. |
| [Android development](../examples/how-to-use-JAI/android-development.md) | SABSA and development, then a layered decision | Step 7 explicitly assesses release readiness using architecture and implementation evidence. It does not certify the preceding creation history. |
| [Commercial proposal](../capabilities/commercial-delivery.md#worked-proposal-from-discovery-to-bid-decision) | Commercial preparation, then a bid decision | Bid issue is a distinct decision. Alternatively, start layered creation before preparing the proposal if your policy requires it. |

Each case also gives a layered-from-the-start alternative at the relevant entry point. These statements explain the documented teaching scopes. They do not claim to reconstruct an earlier author's motives or an unrecorded provider conversation.

## 2. Use the correct provider interface

| Purpose | Claude Code conversation | Codex conversation |
| --- | --- | --- |
| Commercial domain work | `/commercial <scope>` | `$workflow-commercial <scope>` |
| SABSA domain work | `/sabsa <action> <library>` | `$workflow-sabsa <action> <library>` |
| Controlled implementation | `/develop <scope>` | `$workflow-develop <scope>` |
| Layered engagement | `/layered <intent>` | `$workflow-layered <intent>` |
| Independent Fabric report | `/fabric-report <engagement>` | `$workflow-fabric-report <engagement>` |
| Findings rework | `/rework <ledger>` | `$workflow-rework <ledger>` |

Enter these in the provider conversation, not a shell. The Codex skills are generated from command definitions during installation. A source checkout containing a command does not establish that an older installation exposes it. Report missing installation capabilities rather than silently omitting the procedure.

Commands and skills are behavioural contracts interpreted by the provider. They are not a deterministic interceptor for every request. The orchestrator must actually delegate work and call the runtime; a command name or a fluent completion message is not execution evidence. [Interaction patterns](interaction-model.md) explains the operator/runtime boundary.

## 3. Give the orchestrator a usable starting contract

Identify the workspace, source material, expected outputs, exclusions, decision owner and constraints. For commercial work include the internal/client disclosure boundary and permitted commitment level. For architecture work identify system boundaries, business drivers and evidence-access restrictions.

Before substantial production begins, require the orchestrator to report:

- the selected mode and domain workflow;
- the existing or new engagement ID and canonical model/library location;
- the producer, independent checker and human decision owner;
- the source snapshot, unknowns, output gates and escalation conditions;
- unavailable tools or unqualified controls that block the requested assurance level.

Preserve the original intent; clarifications supplement it. Do not initialise or edit `.fabric/` yourself. The orchestrator uses the supported runtime interfaces. If the request names both `/layered` and a domain, the orchestrator must explicitly use that domain's skills and specialists inside the contracts. Naming `/layered` does not guarantee automatic domain selection or recursive slash-command execution.

## 4. Example: prepare an enterprise proposal

Follow the [worked proposal](../capabilities/commercial-delivery.md#worked-proposal-from-discovery-to-bid-decision) for commands, checkpoints, uncertainty treatments and outputs. It places the commercial method and its example together rather than requiring a separate tutorial and capability manual.

The architectural pattern is:

=== "Claude Code"

    ```text
    Direct creation: /commercial → reviewed proposal snapshot
    New decision:   /layered → readiness to issue that snapshot → human decision

    Alternative chosen before creation:
    /layered with commercial-delivery → controlled proposal creation → decision dossier
    ```

=== "Codex CLI"

    ```text
    Direct creation: $workflow-commercial → reviewed proposal snapshot
    New decision:   $workflow-layered → readiness to issue that snapshot → human decision

    Alternative chosen before creation:
    $workflow-layered with commercial-delivery → controlled proposal creation → decision dossier
    ```

Strict commercial dispatch remains blocked until the deployment supplies current qualification evidence for the required controls. Shipped live capability states are `not_run` for both providers; a teaching sequence does not override them.

## 5. Example: build and maintain a security architecture

Follow [the security assessment](../examples/how-to-use-JAI/security-assessment.md) for direct SABSA work. Follow [Android development](../examples/how-to-use-JAI/android-development.md) to see architecture, implementation and a subsequent layered release question joined into one sequence.

The **SABSA domain matrix** and **JAI execution layers** are different coordinates. The matrix asks six questions across six architectural perspectives. Execution layers assign responsibility for intent, meaning, policy, design, realisation and evidence. Completing 36 matrix cells does not prove six-layer execution; a Fabric trace does not alone prove each matrix answer correct.

## 6. Handle unsuccessful work without losing the reason

| Situation | Required response | Ownership |
| --- | --- | --- |
| The product fails an unchanged requirement | Rework it and obtain independent verification. | Producer repairs; checker verifies. |
| The requirement is ambiguous, inadequate or infeasible | Return it to its issuer for explicit reformulation; preserve the prior obligation and rationale. | Requirement owner, within its authority. |
| Resolution needs scope change, risk acceptance or higher authority | Escalate through adjacent layers, retaining the conflict and options. | Higher layer, ultimately the human where required. |
| Evidence, permissions or execution controls are unavailable | Block the affected gate and report the limitation. | Orchestrator reports; it cannot authorise its own exception. |

Standalone domain workflows have findings/rework procedures. Those are not evidence that adjacent L1–L6 escalation occurred. Inside `/layered`, the Fabric applies bounded rework, owner-controlled reformulation and adjacent escalation. See [the layered operating cycle](layered-engagement.md) for the exact transitions and limits.

## 7. Check what was actually achieved

Require exact object and snapshot identifiers, source/evidence references, actual check results, reviewer records, open findings, constraints and pending human acts. Distinguish produced, structurally valid, evidenced, independently reviewed, owner-approved and authorised-for-use states.

A later decision must identify the exact earlier snapshot it uses. Source changes, new discovery answers or revised implementation can invalidate dependent claims and reviews. Continue against the recorded engagement and version the affected material; do not silently replace history or create a second semantic master.

`Continue engagement <ID>` is natural-language guidance, not an implemented `resume` subcommand. Ask the orchestrator to resolve and report existing state before proceeding.

## 8. What the methodology promises—and what the deployment must prove

JAI provides procedural contracts and runtime checks. Actual provider identity, fresh context, tool restrictions, mounts and evidence custody require host controls. Different role names or a matching context digest do not prove isolation. Report tested, unverified and unavailable controls separately.

The current entry points do not deterministically force every consequential request into `/layered`. Organisations requiring that property need an entry policy/enforcement control. Human scope changes, risk acceptance and release remain external authority acts; see [Human authority and escalation](../operations/human-authority.md).

Continue to [Interaction patterns](interaction-model.md), then [Running a layered engagement](layered-engagement.md) or the [worked cases](../examples/how-to-use-JAI/index.md#2-work-through-a-complete-case).
