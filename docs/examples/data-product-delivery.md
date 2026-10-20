# Deliver a governed data product

Owner: JAI documentation maintainers. Updated: 2026-10-20.

ACME Retail wants a daily inventory-availability dataset for store
replenishment. Alice owns the business definition, Bob engineers the
pipelines and John Doe represents the receiving analytics team. This
illustrative fiction uses a common data-product pattern and provides no
measured data quality or delivery guarantee.

The useful outcome is a data product with agreed meaning, accountable
ownership, tested transformations and an operating handoff. A dataset
that loads successfully can still be wrong if stores disagree about what
available inventory means.

## Prepare the project

Create a new `acme-data-product/` directory with `inputs/`, `working/`
and `output/` beneath it. Keep received source files in `inputs/` and
proposed work separate from material ready for handoff.

Collect the consumer use cases, source-system descriptions, sample
schemas, business definitions, classification, quality expectations,
transformation rules and current operational schedules. Use authorised
sample data and describe its representativeness. Include the receiving
team's acceptance criteria and the data owner's authority.

Use names such as `inputs/consumer-needs.md`,
`inputs/source-schema.json`, `inputs/definitions.md and
inputs/quality-expectations.md`. Keep source dates, versions and owners
in `inputs/source-register.md`. If reserved stock is not defined
consistently across systems, record the semantic conflict before
choosing a calculation. A reference example is not a source of ACME's
inventory facts.

Complete the [installation](../getting-started/install.md), then start
Claude Code or Codex in `acme-data-product/`. Confirm the installed JAI
commands or skills are available. All paths below are relative to that
project directory; do not run the example against the JAI library
itself.

## Run this scenario in the provider CLI

Use layered delivery for the product because business semantics, access
rules, transformation design and acceptance evidence must agree. Use the
development workflow for bounded implementation after those decisions
are established.

Enter these instructions in the provider conversation, not a shell. The
Claude slash command and Codex skill request the same work. They are
workflow entry points, not a claim that routing or artefact creation is
universally automatic. Inspect the actual output locations and use those
paths if the workflow reports a different location from `working/`.

### 1. Understand consumers and sources

**Claude**

```text
/analyse inputs/ for the inventory data product. Identify consumers, source limitations, disputed definitions and required freshness.
```

**Codex**

```text
$workflow-analyse inputs/ for the inventory data product. Identify consumers, source limitations, disputed definitions and required freshness.
```

Inspect whether the source schema actually contains the fields needed
for the proposed measure. Separate source-system timestamps from
business event time. An extract arriving daily does not establish that
every record is current.

### 2. Define the product and evidence

**Claude**

```text
/layered Prepare the inventory data-product delivery from inputs/. Trace definitions, quality rules, access constraints, ownership and acceptance evidence into proposed material in working/.
```

**Codex**

```text
$workflow-layered Prepare the inventory data-product delivery from inputs/. Trace definitions, quality rules, access constraints, ownership and acceptance evidence into proposed material in working/.
```

Inspect the contract between producer and consumer. It should make
exclusions and latency visible and say who handles a broken feed. Avoid
pretending a syntactic schema check establishes semantic correctness or
complete source coverage.

### 3. Implement the bounded change

**Claude**

```text
/develop Implement the agreed inventory transformation and checks using the reviewed design in working/ and authorised sample inputs. Keep unapproved definition choices explicit.
```

**Codex**

```text
$workflow-develop Implement the agreed inventory transformation and checks using the reviewed design in working/ and authorised sample inputs. Keep unapproved definition choices explicit.
```

Inspect the actual changed code and evidence returned by the development
workflow. The intended checks should expose duplicate items, missing
locations and inconsistent totals. A mock fixture demonstrates a
specified case, not production quality across all stores.

### 4. Review the deliverable and its claims

When review presents the criteria and their hash, inspect them and
answer YES only if they match this task. The review then proceeds; that
confirmation authorises the review, not the deliverable or a risk.

**Claude**

```text
/review working/ against inputs/definitions.md and inputs/quality-expectations.md; check traceability, consumer meaning and evidence limitations.
```

**Codex**

```text
$workflow-review working/ against inputs/definitions.md and inputs/quality-expectations.md; check traceability, consumer meaning and evidence limitations.
```

The illustrative escalation is that two systems count transferred stock
differently. Alice replies: "Keep transfer stock separate until the data
owner resolves the definition; do not conceal it in available stock." If
an authority record is needed, the human follows the exact emitted
trusted command.

### 5. Close findings and prepare the handoff

Replace `<reported-ledger>` with the findings ledger identifier or path
returned by the preceding review. Keep this same ledger through rework
and independent verification; do not invent one or mark findings closed
without verification.

**Claude**

```text
/rework <reported-ledger>
Use the current findings ledger to revise the inventory product documentation and implementation as appropriate. Preserve the unresolved transfer definition and request independent verification.
```

**Codex**

```text
$workflow-rework <reported-ledger>
Use the current findings ledger to revise the inventory product documentation and implementation as appropriate. Preserve the unresolved transfer definition and request independent verification.
```

If a source adds a new reservation state, register the schema revision
and revisit definitions, transformations and checks. Inspect the updated
findings and actual evidence before claiming closure. Continue the
existing engagement rather than treating a new source as automatically
accepted.

## Finish and hand off

Hand over the versioned product definition, transformation and test
evidence, source lineage, access ownership, monitoring and support
procedure. Identify pending semantic decisions and quality limits. The
receiving data owner accepts actual fitness for use; publication does
not create that acceptance.

For the wider role chain, required handoffs and blocking decisions, see
the [workflow catalogue](../reference/workflows.md). For handling an
actual authority request, follow [human
authority](../operations/human-authority.md).
