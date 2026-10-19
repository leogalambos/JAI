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

## Document Content Specification review

Load the explicitly bound compiled DCS before authoring or review. Use
`content_spec.py outline` for the information blueprint and
`content_lint.py check` for deterministic content QA. A heading does not
satisfy a semantic information unit. Keep unknowns explicit and do not
invent facts, evidence or approvals.

Reviewers must remain independent of the author. Record rule identifiers,
precise source locations, observations and remediation. Bind the review
to the canonical semantic hash and compiled specification hash; changing
either invalidates the review. Principal identities and review execution
must be verified through existing JAI evidence, never accepted solely
from names declared by the document author. Reviewers never repair the
material they assess. Unsupported review predicates remain pending.

Content QA, projection fidelity, publication integrity and visual QA are
separate obligations. Attach the content QA hash to the DCS projection.
A successful render is not a content pass. Pilot content checks remain
advisory; security, evidence and human authority gates remain mandatory.
Production acceptance and human-gold classification require existing JAI
L0 human authority; neither another agent nor a synthetic test grants it.
