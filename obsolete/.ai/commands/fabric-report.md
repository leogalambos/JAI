---
description: Independent justifiability report on a traceability fabric
argument-hint: <engagement> [product fragment]
allowed-tools: Read, Grep, Glob, Bash, Task, Agent
---
> **Agents named here** are subagents: delegate them through the active provider's operator/delegation mechanism — `fabric-auditor`.

Dispatch the `fabric-auditor` agent on engagement `$ARGUMENTS` (fabric under `./.fabric/` unless FABRIC_HOME says otherwise; if no engagement is given, use the newest `.jsonl` there). Report verify, open conflicts and escalations, every fragment with its strict and paper verdicts, and the release verdict for the product if one is named.


## Operational specification — Assurance interpretation

**Preconditions and boundary.** Identify the fabric instance, canonical object references, layer contract, revisions and evidence scope.

**Execution and required evidence.** Show unresolved obligations, escalation, exceptions, invalidations and approvals with exact record IDs, rather than summarizing only favorable status.

**Acceptance and escalation.** Treat a report as assurance evidence, not an authorization to release.

**Documentation.** The current product manual is authored in repository `docs/` (see `docs/reference/commands.md` and `docs/reference/command-walkthroughs.md`). For installed offline assistance use `~/.ai/it-role-house/GUIDE.md` or `/guide`. Provider commands and skills are native runtime contracts; no separate runtime HTML help site is required.
