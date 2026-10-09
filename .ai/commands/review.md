---
description: Review code, documents or a SABSA library against criteria fixed before reading, with located findings
argument-hint: <path> [against <criteria or a criteria file>]
allowed-tools: Read, Grep, Glob, Bash, Task, Agent
---

Review $ARGUMENTS. If I named criteria or a criteria file, use those. Otherwise run `python3 ~/.ai/it-role-house/tools/criteria.py show <path>` and use what it resolves: the project's `.ai/review-criteria.md`, my `~/.ai/review-criteria.md`, or the package default for this kind of target. Show me the criteria, where they came from and their hash, and wait for my yes before the reviewer reads anything. Then follow `library-lifecycle` (or `sabsa-library` for a SABSA library): dispatch the reviewer, record findings in a ledger named review-<today>, and show me `findings.py report`.


## Operational specification — Independent review

**Preconditions and boundary.** Freeze criteria and their digest before reading the target, and respect reviewer write isolation and owner authority.

**Execution and required evidence.** Use evidence-linked, severity-rated findings with exact locations, impact, reproduction and corrective acceptance tests.

**Acceptance and escalation.** Review status is distinct from approval; record blockers and do not change the reviewed baseline.

**Documentation.** The current product manual is authored in repository `docs/` (see `docs/reference/commands.md` and `docs/reference/command-walkthroughs.md`). For installed offline assistance use `~/.ai/it-role-house/GUIDE.md` or `/guide`. Provider commands and skills are native runtime contracts; no separate runtime HTML help site is required.
