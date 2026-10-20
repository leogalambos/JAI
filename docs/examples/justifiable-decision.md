# Make a consequential decision with traceability

Owner: JAI documentation maintainers. Updated: 2026-10-20.

ACME Utilities must choose how to replace an ageing field-service
application. Alice is the business sponsor, Bob owns operations and John
Doe coordinates the decision. This illustrative fiction supplies a
familiar investment and service-risk problem, not a real recommendation
or accepted risk.

The objective is a decision whose reasoning and evidence can be
inspected. The six JAI execution layers transform intent through
meaning, policy, design, realisation and evidence. External L0 human
authority remains outside those layers.

## Prepare the project

Create a new `acme-justifiable-decision/` directory with `inputs/`,
`working/` and `output/` beneath it. Keep received source files in
`inputs/` and proposed work separate from material ready for handoff.

Collect the business problem, decision remit, current service
description, constraints, candidate options, cost assumptions and
available operational evidence. Include who can authorise expenditure
and who can accept service risk; those may be different people.

Use names such as `inputs/intent.md`, `inputs/authority.md`,
`inputs/options.md` and `inputs/evidence-register.csv`. Keep source dates,
versions and owners in `inputs/source-register.md`. Write unknowns
explicitly. An absence of failure reports does not establish
reliability, and a reference document does not prove ACME's readiness.

Complete the [installation](../getting-started/install.md), then start
Claude Code or Codex in `acme-justifiable-decision/`. Confirm the
installed JAI commands or skills are available. All paths below are
relative to that project directory; do not run the example against the
JAI library itself.

## Run this scenario in the provider CLI

Use the layered workflow directly because this is a consequential
decision. Do not start with a stack of unrelated role prompts and later
claim that their outputs form a verified traceability chain.

Enter these instructions in the provider conversation, not a shell. The
Claude slash command and Codex skill request the same work. They are
workflow entry points, not a claim that routing or artefact creation is
universally automatic. Inspect the actual output locations and use those
paths if the workflow reports a different location from `working/`.

### 1. Clarify the starting point

**Claude**

```text
/analyse inputs/ for the field-service replacement. Describe the decision boundary, stakeholders, evidence gaps and competing objectives.
```

**Codex**

```text
$workflow-analyse inputs/ for the field-service replacement. Describe the decision boundary, stakeholders, evidence gaps and competing objectives.
```

Inspect whether the summary expresses a decision rather than an already
selected product. If the sponsor's preferred option is a constraint,
record who established it and why. Keep that distinct from a comparative
conclusion.

### 2. Establish the governed decision

**Claude**

```text
/layered Prepare the field-service replacement decision from inputs/. Preserve L0 authority, independent review and explicit uncertainty. Keep proposed deliverables in working/.
```

**Codex**

```text
$workflow-layered Prepare the field-service replacement decision from inputs/. Preserve L0 authority, independent review and explicit uncertainty. Keep proposed deliverables in working/.
```

Inspect the contracts and fragments produced by the engagement.
Requirements should remain traceable as they pass through layers; an
infeasible requirement becomes a visible conflict or compensation need,
not a silently deleted condition. File presence alone does not establish
entitlement to use its conclusions.

### 3. Inspect justifiability independently

**Claude**

```text
/fabric-report Independently report on the traceability fabric for this engagement. Explain supported fragments, failures and the effect of missing evidence without recording authority acts.
```

**Codex**

```text
$workflow-fabric-report Independently report on the traceability fabric for this engagement. Explain supported fragments, failures and the effect of missing evidence without recording authority acts.
```

Read the report's scope and rule failures. Integrity and well-typedness
are different from the truth of every business claim. Do not translate a
structurally valid chain into human acceptance or assume an unsigned
record is equivalent to an authority signature.

### 4. Handle the escalation

**Claude**

```text
/layered Continue the existing replacement engagement with the unresolved conflict between the required outage boundary and the proposed migration approach. Prepare options for the appropriate authority.
```

**Codex**

```text
$workflow-layered Continue the existing replacement engagement with the unresolved conflict between the required outage boundary and the proposed migration approach. Prepare options for the appropriate authority.
```

The illustrative reply from Alice is: "Keep the outage requirement;
compare a phased transition and an interim operating procedure before a
decision." That reply directs further work. Where the runtime requires
an authority act, the named human must use its exact emitted trusted
command. The agent must not manufacture the act.

### 5. Prepare the decision for its audience

Publication requires an approved, stable semantic snapshot and a
registered publication profile. Use the actual approved snapshot returned
by the workflow, then follow its manifest and rendering steps. If those
prerequisites are absent, stop before rendering. Approval for publication
does not itself approve the business, deployment or risk decision.

**Claude**

```text
/publish Prepare a publication from the reviewed semantic decision artefact in working/ for output/. Preserve source references, alternatives, uncertainty and actual authority state.
```

**Codex**

```text
$workflow-publish Prepare a publication from the reviewed semantic decision artefact in working/ for output/. Preserve source references, alternatives, uncertainty and actual authority state.
```

If new cost or service evidence changes the recommendation, return to
the affected engagement work and independent review. Do not patch only
the executive summary. Inspect the publication against its semantic
source, especially qualifications omitted by a shorter presentation.

## Finish and hand off

The handoff contains the decision package, evidence and assumption
register, independent fabric report, unresolved conflicts and genuine
authority record where available. A pending decision is an honest
outcome. Neither an AI review nor a polished publication substitutes for
the accountable human decision.

For the wider role chain, required handoffs and blocking decisions, see
the [workflow catalogue](../reference/workflows.md). For handling an
actual authority request, follow [human
authority](../operations/human-authority.md).
