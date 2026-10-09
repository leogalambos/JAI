---
description: Create or show the review criteria for this project
argument-hint: "[project path]"
allowed-tools: Read, Grep, Glob, Bash, Task, Agent
---

Review criteria for $ARGUMENTS (or the current project). Run `python3 ~/.ai/it-role-house/tools/criteria.py show <path>`. If the criteria come from a package default, offer to create the project's own file with `criteria.py init <path>` — choosing the type (software, documents or sabsa) with me — so I can edit it. Then show me the file, explain the format in two sentences, and offer to tailor it to what I tell you about the project.


## Operational specification — Criteria management

**Preconditions and boundary.** Resolve the selected review criteria from the declared precedence chain, record their exact source and digest, and show their scope before review.

**Execution and required evidence.** Separate mandatory release controls, project-specific criteria, objective evidence requirements and advisory quality signals.

**Acceptance and escalation.** Never silently alter criteria after examining the target; changed criteria require a newly recorded baseline and applicable authority approval.

**Documentation.** The current product manual is authored in repository `docs/` (see `docs/reference/commands.md` and `docs/reference/command-walkthroughs.md`). For installed offline assistance use `~/.ai/it-role-house/GUIDE.md` or `/guide`. Provider commands and skills are native runtime contracts; no separate runtime HTML help site is required.
