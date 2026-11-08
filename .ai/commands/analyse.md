---
description: Analyse a code repository, a document library or a SABSA library — understand it, no verdicts
argument-hint: <path or description>
allowed-tools: Read, Grep, Glob, Bash, Task, Agent
---

Analyse $ARGUMENTS. Work out whether it is a software product, a document library or a SABSA library. Use the `library-lifecycle` skill (or `sabsa-library` for a SABSA library) in analysis mode: run the survey tool first, then the analysis agent. Report what it is, how it is organised, who it serves and where it is thin. No verdicts and no changes.


## Operational specification — Analysis boundary

**Preconditions and boundary.** Classify the target before selecting the survey path; declare the source baseline, repository or document coverage, tool access, and observations versus hypotheses.

**Execution and required evidence.** Inventory structure, ownership, dependencies, interfaces, version information, decision and evidence stores; link every identified gap to an inspectable location.

**Acceptance and escalation.** Return an evidence-indexed inventory and a clearly bounded list of uncertainties. Do not issue approvals, implement changes, or turn hypotheses into findings.

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
