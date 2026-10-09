---
description: Fix the open findings of a review, with independent verification, until complete
argument-hint: "[ledger]"
allowed-tools: Read, Grep, Glob, Bash, Task, Agent
---

Rework the open findings in ledger $ARGUMENTS (or the newest ledger in .findings/). Follow the review-then-rework loop of `library-lifecycle` (or `sabsa-library`): the author for this library type fixes, the reviewer verifies, repeat until `findings.py status` says COMPLETE. Bring me any stuck finding with its history, and stop there.


## Operational specification — Controlled rework

**Preconditions and boundary.** Reference the rejected deliverable, governing criterion, defect ID and unchanged intent unless reformulation was authorized.

**Execution and required evidence.** Produce a versioned correction preserving the original object/record, and rerun the relevant acceptance and regression checks.

**Acceptance and escalation.** Escalate when resolution needs changed requirements, risk acceptance or higher human authority.

**Documentation.** The current product manual is authored in repository `docs/` (see `docs/reference/commands.md` and `docs/reference/command-walkthroughs.md`). For installed offline assistance use `~/.ai/it-role-house/GUIDE.md` or `/guide`. Provider commands and skills are native runtime contracts; no separate runtime HTML help site is required.
