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
