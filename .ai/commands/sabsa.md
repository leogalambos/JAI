---
description: Build a SABSA security architecture from client material, or update, review, improve or document one
argument-hint: <prepare|create|update ID|review|suggest|questions|lifecycle|overlays|reuse|documents|approve|approval|document|template> [library path]
allowed-tools: Read, Grep, Glob, Bash, Task, Agent
---

SABSA work: $ARGUMENTS. Use the `sabsa-library` skill. For prepare, follow *From client material to an architecture*: initialise the library, ask me what material exists about the client and the environment and have it placed in `00-sources/`, research the public context, then derive drivers citing their sources and stating their basis. For update, run `sabsa.py trace` before any change. For review, record findings in a ledger. For suggest, give ranked suggestions with the next step. For questions, list the open assumptions as questions for the client. For approve, run the structural/review gates first and only then use `sabsa.py approve --by ...` on the owner's explicit instruction; for approval, verify whether the current snapshot still matches the recorded approval. For document, generate the document with `sabsa.py document` — Markdown by default, or the format I ask for, such as .docx — and tell me which template was used and what still makes it a draft. For template, show which template applies and help me adapt it, or set up the client's own template or reference.docx in the library.

For lifecycle, show or maintain current/transition/target and lifecycle state using the 3.2 lifecycle commands. For overlays, create/validate external framework mappings without reproducing licensed standards. For reuse, prefer namespaced references to approved shared SABSA libraries over copying architecture elements. For documents, list the specialist views and generate the requested one from the single source model.


## Operational specification — SABSA methodology fidelity

**Preconditions and boundary.** Identify business drivers, assets, attributes, threats, risks and decision scope before selecting contextual/conceptual/logical/physical/component/service-management viewpoints.

**Execution and required evidence.** Maintain stable model IDs and the 6×6 SABSA questions independently from JAI L1–L6; demonstrate cross-layer traceability, owner and evidence.

**Acceptance and escalation.** Treat incomplete typed semantics, orphan relations or unsupported ArchiMate mappings as findings, not as a complete architecture.

**Documentation.** The current product manual is authored in repository `docs/` (see `docs/reference/commands.md` and `docs/reference/command-walkthroughs.md`). For installed offline assistance use `~/.ai/it-role-house/GUIDE.md` or `/guide`. Provider commands and skills are native runtime contracts; no separate runtime HTML help site is required.
