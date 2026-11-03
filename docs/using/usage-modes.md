# Choose how to use JAI

JAI supports three ways of working. Choose the smallest arrangement that matches
the task, required independence and consequences of an error.

| Mode | Use it for | What JAI coordinates |
| --- | --- | --- |
| A specialist role | A bounded question, analysis or deliverable | The professional viewpoint and tools appropriate to that role |
| A workflow | A recognisable process involving several responsibilities | Roles, ordered handoffs, required artefacts and review gates |
| A layered matrix | A consequential solution requiring traceability from business intent to realisation and management | Six content perspectives, six questions per perspective, local independent review and explicit versioned handoffs |

## 1. Ask a specialist

Name the responsibility and the result you need, or ask JAI to select a suitable
specialist. Give it the relevant sources, constraints and expected output.

> Act as a Requirements Engineer. Review the attached service requirements for
> ambiguity, missing acceptance criteria and conflicting obligations. Return
> located findings; do not rewrite the requirements yet.

The [complete role catalogue](../reference/roles.md) lists every available role
under its professional category. The [category guide](roles.md) explains the
disciplines and role-selection process. A role is a body of professional
knowledge, not a human identity or permission to approve its own work.

If the result needs independent review, request a separate reviewer. Direct
role work does not silently create a full layered engagement.

## 2. Follow a workflow

Choose a maintained process or describe the business situation and ask JAI to
recommend one. For example:

> Use the inherited codebase takeover workflow for this repository. First
> establish review criteria and assess its condition; propose repairs only after
> the independent assessment.

The [workflow catalogue](../reference/workflows.md) lists all 24 enterprise
chains, their outcomes and detailed procedures. Each procedure selects relevant
specialists from the same [complete role catalogue](../reference/roles.md).
The [command reference](../reference/commands.md) separately lists the 17
provider-facing command entry points: commands and enterprise workflow chains
are related, but they are not interchangeable lists.

A workflow coordinates a particular process. It can produce a useful review,
design, publication or change without requiring every cell of the layered matrix.
When a workflow produces consequential material requiring layered justification,
JAI can hand the exact task, criteria and input references into a layered engagement.

## 3. Develop a layered solution

Use `/layered` in Claude Code or the `$workflow-layered` skill in Codex. Describe
the intended outcome, actual inputs, constraints, exclusions and the decisions
reserved to you. You do not prepare runtime bootstrap JSON or create workers.

> Run this service design as a layered engagement. Preserve the attached business
> requirements, show unresolved assumptions, and obtain my decision before
> changing any requirement I have explicitly reserved.

The matrix covers contextual, conceptual, logical, physical, component and
management perspectives. Each addresses What, Why, How, Who, Where and When.
A setter formulates the local question, an author proposes its answer and an
independent reviewer assesses it against the stated criteria. Each local entity
can choose appropriate specialties from the complete catalogue.

Work progresses through reviewed question answers, layer integration and
acceptance of the exact handoff by its neighbour. A review of one answer is not
acceptance of an entire layer or permission to release the final product.

### Work incrementally and resume

The full matrix is a structured process, not one indivisible prompt. JAI advances
through bounded work steps and can pause at a recorded boundary, show its current
checkpoint and resume the same engagement. Ask for a progress report or pause
after an agreed stage; completed work need not be regenerated just to continue.

Progress follows dependencies. A partial answer, one completed layer or a
recorded checkpoint does not establish that the remaining matrix is complete.
There is no implied right to skip required layers or accept an incomplete
solution. Management concerns are crosscutting and inform the other perspectives.

When an escalation may change shared assumptions, the affected layer pauses by
default. The operator may explicitly accept bounded speculative continuation.
Timeouts report the interrupted stage and completed work; they do not turn
uncertainty into a positive result.

Continue with [the layered operating guide](layered-engagement.md) and the
[layer model](../architecture/sabsa-layer-model.md).

## Permissions stay separate

All three modes use the effective provider sandbox and tool permissions. A role
name, workflow instruction or well-written answer grants no extra authority.
Ordinary work records are unsigned. Only explicit reserved human decisions use
the [host signing procedure](../operations/human-authority.md). Authorisation to
continue, acceptance of a particular result and permission to release it remain
separate decisions.

