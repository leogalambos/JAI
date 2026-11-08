---
description: Assess and propose the governance of a repository or document library
argument-hint: <path>
allowed-tools: Read, Grep, Glob, Bash, Task, Agent
---
> **Agents named here** are subagents: delegate them through the active provider's operator/delegation mechanism — `artefact-governor`.

Assess the governance of $ARGUMENTS with `artefact-governor`: ownership, change control from the git history, versioning and release, currency, and policy. Record gaps in a findings ledger and propose a governance model sized to it. Change nothing.


## Operational specification — Governance and accountability

**Preconditions and boundary.** Identify decision owner, affected assurance dimensions, applicable policy, human authority at L0 and required separation of duties.

**Execution and required evidence.** Tie decisions to traceable claims, risk acceptance, review records, and release conditions.

**Acceptance and escalation.** Do not treat agent output, passing technical tests or an advisory recommendation as a human approval.

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
