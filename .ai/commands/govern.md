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
