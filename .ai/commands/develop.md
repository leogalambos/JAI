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
