# Interaction patterns

Owner: JAI maintainers · Last reviewed: 2026-10-16

AI IT House exposes several working modes because not every task needs the same assurance intensity.

Start with [Choosing and running a methodical workflow](methodical-workflows.md) for the decision between direct domain work, layered creation and a separate layered decision after domain work. Then follow the [worked security, Android or proposal case](../examples/how-to-use-JAI/index.md#2-work-through-a-complete-case). These are distinct assurance boundaries, not a mandatory sequence of `/sabsa` or `/commercial` followed by `/layered`.

## First: choose the interface, not a Python script

**Operator in Claude Code:** type a native command such as `/layered <intent>`, `/review <target>` or ask in natural language. **Operator in Codex CLI:** invoke the corresponding skill, for example `$workflow-layered <intent>`, `$workflow-review <target>`, or ask in natural language and explicitly request the workflow. The `$workflow-*` prefix is a Codex skill name, **not** a shell variable or Python program. In either provider, work from the relevant project directory and provide the files, constraints and decision owner.

| Responsibility | What you do in the provider conversation | What is carried out behind the scenes |
| --- | --- | --- |
| Start | State purpose, intended outcome, scope, constraints and acceptance conditions; select `/layered` or `$workflow-layered` for consequential work. | Provider command/skill invokes the orchestrator, routes specialist agents and uses approved runtime tools. |
| Observe | Ask for current status, blocked gates, findings and required evidence; examine actual artefacts. | Agent obtains tool results, performs allowed checks and records contract, review and evidence references. |
| Decide | Clarify intent and make real organisational decisions; do not approve an exception by accepting a plausible narrative. | Fabric/approval controls distinguish proposed decisions from authorised ones; Codex requires a separately executed human authority command. |
| Verify | Ask `/fabric-report` (Claude) or `$workflow-fabric-report` (Codex), and request exact unresolved record IDs. | Audit agent queries/verifies the append-only fabric; reporting is not an approval or release operation. |

**Important limit:** provider commands guide model-driven orchestration; they do not constitute a wholly deterministic workflow engine. Agent tool calls must actually execute and succeed. If delegation, tools, permissions or evidence are unavailable, the assistant must report the gap rather than claim a completed gate. The direct Python API is documented in [runtime tools](../reference/runtime-tools-detailed.md) for developers and recovery, **not** as a prerequisite for a normal operator session. Human L0 decisions remain outside agent authority; see [Human authority](../operations/human-authority.md).

## 1. Ask for an outcome

This is often the best starting point for ordinary multi-role work.

> We are replacing an on-prem ERP with SaaS. Define the architecture work, the security and privacy assessments, the migration and cutover deliverables, the operational-readiness gates and the decision owners.

The role/workflow router can choose the relevant specialist capabilities.

## 2. Invoke a named workflow command

Example:

```text
/review path/to/repository
```

Use this when you want the canonical procedure rather than a free-form answer.

## 3. Work directly with a specialist capability

Examples include SABSA, publication and the scoped EA repository.

This is appropriate when the user already knows which controlled subsystem owns the task.

## 4. Use `/layered` for consequential work

Use `/layered` when the output may be acted on and the organisation must preserve why that use was allowed.

Typical triggers include:

- architecture decisions with material risk/cost consequences;
- infrastructure, pipeline or production changes;
- security assessments and residual-risk decisions;
- compliance/assurance evidence;
- release-readiness decisions;
- SDLC/control adaptation;
- any product for which evidence, dissent and human authority must be reconstructed later.

A layered engagement records the original intent, transforms requirements downward through typed contracts, reviews products upward, bounds rework/reformulation and escalates unresolved authority matters to the operator.

See [Running a layered justifiable engagement](layered-engagement.md) for the operational cycle.

## Choosing the control intensity

| Situation | Recommended path |
| --- | --- |
| Typo, rename, low-risk quick question | direct answer/tool path |
| Clear single-discipline analysis or authoring | role-router → specialist operator |
| Standard repeatable enterprise process | named workflow |
| Creation itself requires six-layer justification | `/layered` with the domain explicitly named |
| Existing domain model needs a justified readiness/risk decision | domain workflow, then `/layered` for the new decision against an exact snapshot |
| Need to inspect why a layered output is entitled to be used | `/fabric-report` or `$workflow-fabric-report`; `fabric.py` is a maintainer-level API |

## Important runtime boundary

The JAI core is normative across the product, but the current entry point does **not** deterministically intercept every possible direct role invocation and force it into `/layered`.

Therefore organisations should distinguish:

- **layered-capable** — supported runtime behavior;
- **layered-by-policy** — organisational procedure says consequential tasks must use `/layered`;
- **layered-by-construction** — host/runtime entry control technically prevents consequential tasks from bypassing the layered route.

The current runtime provides the first two when deployed with an appropriate operating policy. The third requires an additional entry-routing/enforcement control in the deployment.

## Implementation details

[Execution and context assembly](../overview/execution-context-algorithm.md) describes the inspected implementation.
Follow the complete operating flow, including where automatic enforcement ends.
