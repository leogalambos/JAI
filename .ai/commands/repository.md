---
description: Build, validate, exchange and govern enterprise architecture models in the governed EA-domain projection repository.
---

# Repository

Use the 26.10 enterprise architecture integration runtime.

1. Identify the owning architecture role and repository/project boundary. Do not infer missing architecture facts.
2. Work on the canonical repository model under the agreed system of record.
3. Validate before mutation:

```bash
python3 ~/.ai/it-role-house/tools/repository.py validate ./ea-repo
```

4. Maintain projects, elements, relationships, views, benefit links and lifecycle state with stable IDs.
5. For EA-tool interchange, use Open Exchange import/export rather than treating the XML as the persistent source of truth:

```bash
python3 ~/.ai/it-role-house/tools/repository.py import-open-exchange model.xml --repo ./ea-repo --merge
python3 ~/.ai/it-role-house/tools/repository.py export-open-exchange ./ea-repo --out enterprise.xml
```

6. Generate governed views and portfolio/impact evidence:

```bash
python3 ~/.ai/it-role-house/tools/repository.py generate-views ./ea-repo --out ./published-views --preset all
python3 ~/.ai/it-role-house/tools/repository.py portfolio ./ea-repo --format md --out portfolio-architecture.md
```

7. Before retirement/decommission, run impact analysis. Do not force a lifecycle transition past active dependencies without a named waiver and retained evidence.
8. Run the Model Consistency Reviewer before architecture/repository release.

For an explicit ArchiMate request, select the portable language 3.2 / exchange
3.1 profile and retain its semantic, preservation and draft-notation limits.
The installed `ea/README.md` describes `validate-archimate` and
`render-archimate`; these are Python helpers, not additional native command
verbs. Use the public manual's `docs/capabilities/sabsa-ea.md` section
"Portable ArchiMate 3.2" for request examples, project-default conditions and
independent QA boundaries. Generic repository graphs do not establish verified
ArchiMate notation, and no external EA application is required.


## Operational specification — Repository integrity

**Preconditions and boundary.** Define the canonical identifier namespace, source-of-truth scope, synchronization direction, lifecycle and project boundaries.

**Execution and required evidence.** Verify reference integrity, provenance, deterministic EA/ArchiMate projection and orphan detection.

**Acceptance and escalation.** A projected EA view must not rewrite the identity or semantics of its canonical source.

Ordinary model maintenance and exchanges retain these routes. When the requested
architecture result requires Gen2 justification, use the canonical
`layered-justifiable-delivery/references/domain-handoff.md` native handoff with
the exact repository snapshot, model-review findings and evidence. Do not replace
the repository engine or infer acceptance/release from a generated view.

**Documentation.** The current product manual is authored in repository `docs/` (see `docs/reference/commands.md` and `docs/reference/command-walkthroughs.md`). For installed offline assistance use `~/.ai/it-role-house/GUIDE.md` or `/guide`. Provider commands and skills are native runtime contracts; no separate runtime HTML help site is required.


## Compact execution feedback

Present the task result first, then a compact one-row Markdown efficiency table.
Use actual recorded host `efficiency.table` when linked to a native governed run.
Otherwise report measurements unavailable in one row; never invent model time,
rework, findings, acceptance or a governed execution record. Detailed history and
advisory comparisons are available through `/jai-stats` / `$workflow-stats` inside
the conversation. Do not append a long efficiency narrative or switch profiles
without an explicit operator selection.
