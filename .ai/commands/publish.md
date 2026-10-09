---
description: Turn an approved semantic artefact into an enterprise-grade publication set and run semantic/publication gates.
---

# Publish

Use the enterprise publication pipeline shipped with the current package.

1. Identify the owning specialist and the approved semantic source. Do not invent missing facts.
2. Build the audience projection from the approved semantic source and a registered publication profile. Do not author a production publication model by hand.
3. Run the Evidence & Rationale Reviewer. Material claims must distinguish stated, inferred and assumed basis and cite evidence.
4. Select the closest profile under `~/.ai/it-role-house/publication/profiles/`.
5. Build the projection and manifest, then render only through that manifest:

```bash
python3 ~/.ai/it-role-house/tools/projection.py build semantic.json \
  --profile ~/.ai/it-role-house/publication/profiles/<profile>.json \
  --out ./projection
python3 ~/.ai/it-role-house/tools/publication.py render \
  ./projection/publication-model.json \
  --manifest ./projection/projection-manifest.json \
  --format all --out ./publication
```

6. Treat `render-evidence.json` as L6 evidence for the concrete publication set.
7. Run format QA on each generated output and route failures to the Enterprise Publication Editor for correction.
8. Run the Visual Quality Reviewer on the actual rendered/output package. A projection/JAI lineage mismatch is a release blocker.
9. Obtain named authority approval where the deliverable is consequential.

The publication layer may restructure or visualise content but may not alter a material claim, decision, assumption, risk acceptance or evidence statement from the semantic source.


## Operational specification — Publication integrity

**Preconditions and boundary.** Require a stable approved semantic snapshot, selected audience profile and complete projection manifest before rendering.

**Execution and required evidence.** Verify mandatory claim/evidence coverage, permitted omissions, semantic/projection/render hashes, actual rendered quality and document control.

**Acceptance and escalation.** Do not invent facts or suppress materially adverse findings; a visually polished artefact cannot override failed semantic or governance gates.

**Documentation.** The current product manual is authored in repository `docs/` (see `docs/reference/commands.md` and `docs/reference/command-walkthroughs.md`). For installed offline assistance use `~/.ai/it-role-house/GUIDE.md` or `/guide`. Provider commands and skills are native runtime contracts; no separate runtime HTML help site is required.
