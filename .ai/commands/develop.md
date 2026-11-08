---
description: Develop a change to a software product or document library, reviewed before it is proposed
argument-hint: <what to build or change>
allowed-tools: Read, Grep, Glob, Bash, Task, Agent
---
> **Agents named here** are subagents: delegate them through the active provider's operator/delegation mechanism — `role-router`.

Develop: $ARGUMENTS. Route through `role-router` to the role and its operator agent. Work on a branch. When the change is ready, have it reviewed (as /review does) before proposing it to me for merge.


## Operational specification — Controlled delivery

**Preconditions and boundary.** Record the problem statement, affected stakeholders, acceptance criteria, baseline files and change authority before editing.

**Execution and required evidence.** Use a branch; retain original content; demonstrate unit, integration and negative tests proportionate to the change; request independent review with located findings.

**Acceptance and escalation.** Return the changed file inventory, verified test results, evidence, open risks and a merge proposal. Do not self-approve.

**Documentation.** The current product manual is authored in repository `docs/` (see `docs/reference/commands.md` and `docs/reference/command-walkthroughs.md`). For installed offline assistance use `~/.ai/it-role-house/GUIDE.md` or `/guide`. Provider commands and skills are native runtime contracts; no separate runtime HTML help site is required.

## Consequential Gen2 use

For a result requiring governed layered justification, use the canonical
`layered-justifiable-delivery` skill and its `references/domain-handoff.md`
native handoff with the actual request, exact criteria/candidate and evidence.
Ordinary bounded work keeps this command's scope and independent responsibilities;
the parent handles runtime transport without user-authored JSON. This command
itself grants no human acceptance or release permission.


## Compact execution feedback

Present the task result first, then a compact one-row Markdown efficiency table.
Use actual recorded host `efficiency.table` when linked to a native governed run.
Otherwise report measurements unavailable in one row; never invent model time,
rework, findings, acceptance or a governed execution record. Detailed history and
advisory comparisons are available through `/jai-stats` / `$workflow-stats` inside
the conversation. Do not append a long efficiency narrative or switch profiles
without an explicit operator selection.
