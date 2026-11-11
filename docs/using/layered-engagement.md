# Running a layered justifiable engagement

Use a layered engagement when the solution needs explicit connections between
business intent, requirements, design, implementation and management, with
independent review and traceable decisions. For smaller tasks,
[choose a specialist or workflow](usage-modes.md).

For the meaning of compaction, main-chat reset and fresh workers, see the
[context operations and handoff boundaries](../configuration/execution-profiles.md#context-boundaries).
One policy is captured for each future run; it does not clear the main chat at
every internal handoff.

## Operator journey: describe, inspect and decide

Invoke `/layered` in Claude Code or `$workflow-layered` in Codex and describe:

- the outcome and deliverables you need;
- the source files and other available evidence;
- constraints, exclusions and requirements reserved to the human;
- the workspace and any relevant operational restrictions.

JAI captures the task and criteria, selects relevant professional resources and
advances through the normal runtime. You do not write bootstrap JSON, invent
worker IDs or supply transport envelopes.

The layered runtime normally records the engagement under the project's
`.fabric/`, including the journal and its referenced immutable materials. This
is not an automatic side effect of every JAI role or workflow. To inspect the
records graphically, follow the
[Fabric Explorer data prerequisites](../fabric-explorer/importing.md#before-you-open-a-project-are-there-records-to-display);
findings can also be viewed independently of a Fabric engagement.

Ask JAI to show its current checkpoint, outstanding questions, review findings
and escalation dossier. Work can pause at a durable boundary and resume using
the same session locator. A partially completed stage remains partial; it does
not imply acceptance of the whole matrix.

The default local iteration window is ten minutes. After the permitted reworks,
unresolved disagreement escalates rather than becoming a positive verdict.
When a window expires, JAI reports the stage, completed work and reworks used;
the operator can permit more time or stop. These local controls are distinct
from a mandatory time limit on the entire task.

If JAI requests a reserved L0 decision, inspect its proposed effects and use the
supplied [host signing command](../operations/human-authority.md). Chat approval,
installation confirmation and provider tool permission are not signed authority.

## Behind the scenes: local work and exact handoffs

Each of the six layers addresses What, Why, How, Who, Where and When. The
[content layer model](../architecture/sabsa-layer-model.md) defines what these
perspectives own. Each question has a setter, author and independent reviewer.
The entities select suitable specialties from the
[complete role catalogue](../reference/roles.md), without a neighbour imposing
their internal staffing or method.

Reviewed answers form a versioned layer bundle. Integration review checks their
interactions before the receiving neighbour accepts the exact handoff for use.
That receiving decision is not a substitute for the producing layer's professional
review. Required dependencies govern progress; an arbitrary layer cannot be
declared complete by skipping its obligations.

The native parent assembles compact task-specific contexts. An author and
reviewer use separate contexts; each receives relevant input sections and
references to supporting material rather than the entire conversational history.
Missing information is requested through the declared interface.

## Revisions and escalation

A lower layer cannot silently edit the meaning supplied by its neighbour.
It requests clarification or an owner-led revision. The owner publishes a new
version and explicitly cancels the affected uses; dependent reviews and
permissions lose applicability together. Unrelated evidence can remain usable
where its declared dependencies are unchanged.

Escalation is aggregated so related conflicts can be resolved together. The
affected layer pauses by default because shared assumptions may change.
Speculative continuation requires an explicit operator decision about its scope
and budget; it does not make speculative results accepted evidence.

## Completion and release

A completed question is not a completed layer; a completed layer is not a
released product. Acceptance assesses an exact output and its relevant current
justification. Release requires its own applicable permission. An obsolete record
outside that justification does not block every output, and missing required
current evidence still blocks the affected result.

Use the independent audit workflow to inspect current justification. Keep the
newest journal, referenced material and session/enrollment files together for
[recovery](../operations/gen2-deployment-recovery.md).
