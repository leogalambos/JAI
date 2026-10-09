---
description: Show the user guide for this library, or the section for one command, with its demo
argument-hint: "[command or topic]"
allowed-tools: Read, Grep, Glob, Bash, Task, Agent
---

Read `~/.ai/it-role-house/GUIDE.md`. If I named a command or topic ($ARGUMENTS), show me just that section — what it does, its syntax, what happens, the demo to try, what to expect and how to check it worked — and offer to run the demo now. If I named nothing, give me the contents and the 20-minute tour. Do not show the 'what to expect' answer keys of review demos before I have run the review, unless I ask for them. If I ask for the full website/manual, use `docs/index.md` from a source checkout or an actual verified deployment URL from project configuration. Do not invent a Pages address. If only the installed runtime is available, explain that `GUIDE.md` is its offline guide and the full maintained documentation is distributed in the repository `docs/` tree.


## Operational specification — Assisted navigation

**Preconditions and boundary.** Confirm user objective and installed provider/runtime context, then direct users to the canonical command, skill, workflow or documentation section.

**Execution and required evidence.** Prefer a minimal validated path with prerequisites, artifacts, verification and troubleshooting steps.

**Acceptance and escalation.** State capability boundaries and distinguish optional components from mandatory controls.

**Documentation.** The current product manual is authored in repository `docs/` (see `docs/reference/commands.md` and `docs/reference/command-walkthroughs.md`). For installed offline assistance use `~/.ai/it-role-house/GUIDE.md` or `/guide`. Provider commands and skills are native runtime contracts; no separate runtime HTML help site is required.
