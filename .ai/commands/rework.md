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
