# Prepare a sourcing and contract decision

Owner: JAI documentation maintainers. Updated: 2026-10-20.

ACME Engineering is selecting a managed network service. Alice owns
sourcing, Bob owns network operations and John Doe coordinates the
contract decision. This illustrative fiction uses a familiar
supplier-selection problem; it does not represent a real tender,
negotiated agreement or legal opinion.

The useful outcome is a defensible recommendation with explicit contract
issues and an operating model. Comparing headline prices alone can hide
transition cost, exclusions, exit constraints and unassigned service
responsibilities.

## Prepare the project

Create a new `acme-sourcing-contract/` directory with `inputs/`,
`working/` and `output/` beneath it. Keep received source files in
`inputs/` and proposed work separate from material ready for handoff.

Collect the approved sourcing scope, service requirements, evaluation
criteria, supplier responses, pricing schedules, draft agreements and
current service baseline. Include transition, access, incident,
reporting and exit needs and identify the procurement and legal
authorities.

Use names such as `inputs/service-requirements.md`,
`inputs/evaluation-criteria.md`, `inputs/supplier-responses/ and
inputs/contract-issues.csv`. Keep source dates, versions and owners in
`inputs/source-register.md`. If a supplier omits an exit price, record
it as an unresolved commercial dependency. Do not invent a favourable
number to make bids comparable.

Complete the [installation](../getting-started/install.md), then start
Claude Code or Codex in `acme-sourcing-contract/`. Confirm the installed
JAI commands or skills are available. All paths below are relative to
that project directory; do not run the example against the JAI library
itself.

## Run this scenario in the provider CLI

Use layered delivery to coordinate the sourcing recommendation and
accountable contract decisions. The supplier-side commercial profile is
for ACME's offers to clients; this buyer-side scenario follows sourcing
and contract responsibilities.

Enter these instructions in the provider conversation, not a shell. The
Claude slash command and Codex skill request the same work. They are
workflow entry points, not a claim that routing or artefact creation is
universally automatic. Inspect the actual output locations and use those
paths if the workflow reports a different location from `working/`.

### 1. Establish a comparable evidence base

**Claude**

```text
/analyse inputs/ for the managed-network sourcing decision. Separate mandatory requirements, evaluation criteria, supplier assertions and missing responses.
```

**Codex**

```text
$workflow-analyse inputs/ for the managed-network sourcing decision. Separate mandatory requirements, evaluation criteria, supplier assertions and missing responses.
```

Inspect whether each bid covers the same estate, hours and transition
scope. Preserve the original responses and distinguish clarification
from a revised offer. A supplier's claim of compliance should retain its
supporting evidence and qualifications.

### 2. Prepare sourcing options

**Claude**

```text
/layered Prepare the sourcing and contract recommendation from inputs/. Compare service coverage, lifecycle cost, delivery risk, responsibilities and unresolved terms in working/.
```

**Codex**

```text
$workflow-layered Prepare the sourcing and contract recommendation from inputs/. Compare service coverage, lifecycle cost, delivery risk, responsibilities and unresolved terms in working/.
```

Inspect the recommendation for exclusions and dependencies, including
what ACME must provide. Distinguish estimated transition cost from
supplier-quoted charges. A proposed contract clause is not agreed merely
because it appears in a well-structured draft.

### 3. Challenge the decision package

When review presents the criteria and their hash, inspect them and
answer YES only if they match this task. The review then proceeds; that
confirmation authorises the review, not the deliverable or a risk.

**Claude**

```text
/review working/ against inputs/evaluation-criteria.md and inputs/service-requirements.md; check fairness, pricing scope, exit and operational responsibilities.
```

**Codex**

```text
$workflow-review working/ against inputs/evaluation-criteria.md and inputs/service-requirements.md; check fairness, pricing scope, exit and operational responsibilities.
```

Read findings against the actual schedules. A low unit price may coexist
with expensive mandatory changes. Ensure the service owner can see how
incidents cross supplier boundaries and who is accountable for
coordinating restoration.

### 4. Escalate an unacceptable contract term

Replace `<reported-ledger>` with the findings ledger identifier or path
returned by the preceding review. Keep this same ledger through rework
and independent verification; do not invent one or mark findings closed
without verification.

**Claude**

```text
/rework <reported-ledger>
Use the current findings ledger to retain the disputed liability and exit terms and prepare bounded negotiation or alternative-supplier options.
```

**Codex**

```text
$workflow-rework <reported-ledger>
Use the current findings ledger to retain the disputed liability and exit terms and prepare bounded negotiation or alternative-supplier options.
```

The illustrative preferred supplier refuses a required exit-assistance
commitment. Alice replies: "Keep award pending and obtain a qualified
legal view; compare the alternative with its complete transition costs."
Do not simulate a lawyer's approval. Formal award or risk acceptance
remains a human authority act through the applicable emitted procedure.

### 5. Prepare the award recommendation

Publication requires an approved, stable semantic snapshot and a
registered publication profile. Use the actual approved snapshot returned
by the workflow, then follow its manifest and rendering steps. If those
prerequisites are absent, stop before rendering. Approval for publication
does not itself approve the business, deployment or risk decision.

**Claude**

```text
/publish Prepare a publication from the reviewed semantic sourcing artefact in working/ for output/. Preserve negotiation issues, conditions and actual award state.
```

**Codex**

```text
$workflow-publish Prepare a publication from the reviewed semantic sourcing artefact in working/ for output/. Preserve negotiation issues, conditions and actual award state.
```

If a supplier changes a price or subcontracts service operations,
register the revision and reopen affected comparisons. Inspect the final
recommendation for transparent unresolved terms; presentation must not
turn a conditional preference into a signed award.

## Finish and hand off

The handoff includes the evaluation record, evidence and clarification
register, lifecycle-cost comparison, contract issues and actual
decisions. Procurement, legal and service owners retain their respective
responsibilities. Contract signature and production access are distinct
authorised actions.

For the wider role chain, required handoffs and blocking decisions, see
the [workflow catalogue](../reference/workflows.md). For handling an
actual authority request, follow [human
authority](../operations/human-authority.md).
