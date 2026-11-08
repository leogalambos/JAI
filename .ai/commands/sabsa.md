---
description: Build a SABSA security architecture from client material, or update, review, improve or document one
argument-hint: <prepare|create|update ID|review|suggest|questions|lifecycle|overlays|reuse|documents|approve|approval|document|template> [library path]
allowed-tools: Read, Grep, Glob, Bash, Task, Agent
---

SABSA work: $ARGUMENTS. Use the `sabsa-library` skill. For prepare, follow *From client material to an architecture*: initialise the library, ask me what material exists about the client and the environment and have it placed in `00-sources/`, research the public context, then derive drivers citing their sources and stating their basis. For update, run `sabsa.py trace` before any change. For review, record findings in a ledger. For suggest, give ranked suggestions with the next step. For questions, list the open assumptions as questions for the client. For approve, run the structural/review gates first and only then use `sabsa.py approve --by ...` on the owner's explicit instruction; for approval, verify whether the current snapshot still matches the recorded approval. For document, generate the document with `sabsa.py document` — Markdown by default, or the format I ask for, such as .docx — and tell me which template was used and what still makes it a draft. For template, show which template applies and help me adapt it, or set up the client's own template or reference.docx in the library.

For lifecycle, show or maintain current/transition/target and lifecycle state using the 3.2 lifecycle commands. For overlays, create/validate external framework mappings without reproducing licensed standards. For reuse, prefer namespaced references to approved shared SABSA libraries over copying architecture elements. For documents, list the specialist views and generate the requested one from the single source model.


## Operational specification — SABSA methodology fidelity

**Preconditions and boundary.** Identify business drivers, assets, attributes, threats, risks and decision scope before selecting contextual/conceptual/logical/physical/component/service-management viewpoints.

**Execution and required evidence.** Maintain stable model IDs and the 6×6 SABSA
content with typed cross-layer traceability, owner and evidence. Governed work
uses the current Gen2 SABSA layer registry; library cell identifiers and runtime
owner coordinates remain distinct identities, not an old fixed author/reviewer
layer scheme. Use the `sabsa-library` skill's native Gen2 handoff when required.

**Acceptance and escalation.** Treat incomplete typed semantics, orphan relations or unsupported ArchiMate mappings as findings, not as a complete architecture.

**Documentation.** The current product manual is authored in repository `docs/` (see `docs/reference/commands.md` and `docs/reference/command-walkthroughs.md`). For installed offline assistance use `~/.ai/it-role-house/GUIDE.md` or `/guide`. Provider commands and skills are native runtime contracts; no separate runtime HTML help site is required.


## Compact execution feedback

Present the task result first, then a compact one-row Markdown efficiency table.
Use actual recorded host `efficiency.table` when linked to a native governed run.
Otherwise report measurements unavailable in one row; never invent model time,
rework, findings, acceptance or a governed execution record. Detailed history and
advisory comparisons are available through `/jai-stats` / `$workflow-stats` inside
the conversation. Do not append a long efficiency narrative or switch profiles
without an explicit operator selection.


## Required model prerequisite before ordinary native delegation

The retained SABSA different-model requirement applies to ordinary bounded work
as well as governed delivery. Do not force ordinary work into six layers to run
this check. Before dispatching a native SABSA author/reviewer pair, the parent must
know and pin the actual explicit author and reviewer provider/model/effort controls.
Use the shared read-only helper internally:

```text
python3 ~/.ai/it-role-house/tools/professional_review.py --project PROJECT --profile PROFILE --author-provider PROVIDER --author-model AUTHOR_MODEL --author-effort AUTHOR_EFFORT --reviewer-provider PROVIDER --reviewer-model REVIEWER_MODEL --reviewer-effort REVIEWER_EFFORT
```

Use the actual project and declared class/profile mappings. These placeholders
are filled by the native parent, not by the user. Keep the authored candidate and
actual requested author controls, then recheck the pair before each review if the
planned controls changed. A different effort on the same model does not qualify.
`inherit`, unknown controls or an unavailable compatible model are blocking
prerequisites: show the helper's inline facts, registry-declared alternatives and
ordinary native-model reselection step. Do not invent a governed assignment,
select_execution decision or journal for this ordinary route. Run the check again
with the actual alternate model before dispatching the pending review.

A model profile expresses preferences and cannot waive this requirement. If a
compatible alternative differs from the preference, report the actual choice.
The helper checks supplied explicit controls; the parent must actually use them.
If the host cannot expose or pin those controls, stop and explain that concrete
capability barrier. Neither this contract nor the helper is an OS interception of
arbitrary provider calls or proof of the served backend model. Human-authored or
explicitly model-free inputs must not be assigned an invented AI producer model.
