---
description: Research a problem to a decision, with experiments if needed
argument-hint: <question>
allowed-tools: Read, Grep, Glob, Bash, Task, Agent
---

Research: $ARGUMENTS. Use the `research-and-development` skill: frame the question and the decision it informs with me, research prior art, and only if needed pre-register and run experiments. End with a recommendation — adopt, trial, assess or hold — and what remains unknown.


## Operational specification — Research traceability

**Preconditions and boundary.** Define a question, evidence eligibility, recency constraints and source-quality rules.

**Execution and required evidence.** Record source attribution, date, competing explanations, uncertainty and separation of observation from inference.

**Acceptance and escalation.** Return reproducible references and unresolved gaps; do not imply unverified external evidence was observed.

**Documentation.** The current product manual is authored in repository `docs/` (see `docs/reference/commands.md` and `docs/reference/command-walkthroughs.md`). For installed offline assistance use `~/.ai/it-role-house/GUIDE.md` or `/guide`. Provider commands and skills are native runtime contracts; no separate runtime HTML help site is required.
