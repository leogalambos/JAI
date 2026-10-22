# Take demand through a funding decision

Owner: JAI documentation maintainers. Updated: 2026-10-20.

ACME Public Services has competing requests for a customer portal, a
resilience upgrade and reporting improvements. Alice manages the demand
portfolio, Bob represents delivery capacity and John Doe chairs funding
discussions. This illustrative fiction reflects ordinary portfolio
prioritisation, with no real budget or commitment.

The outcome is a transparent demand and funding recommendation. A ranked
list is useful only when it exposes dependencies, capacity limits,
decision criteria and proposals that are not yet ready for a commitment.

## Prepare the project

Create a new `acme-demand-funding/` directory with `inputs/`, `working/`
and `output/` beneath it. Keep received source files in `inputs/` and
proposed work separate from material ready for handoff.

Collect the demand submissions, strategic objectives, funding policy,
available budget evidence, delivery-capacity view, existing commitments
and dependency map. Each submission should identify a sponsor, expected
outcome, rough cost basis, timing constraint and consequences of
deferral.

Use names such as `inputs/demand-register.csv`, `inputs/strategy.md`,
`inputs/capacity.md` and `inputs/funding-policy.md`. Keep source dates,
versions and owners in `inputs/source-register.md`. Mark an unestimated
request as unestimated. Do not assign a convenient cost or benefit score
simply to fill the prioritisation table.

Complete the [installation](../getting-started/install.md), then start
Claude Code or Codex in `acme-demand-funding/`. Confirm the installed
JAI commands or skills are available. All paths below are relative to
that project directory; do not run the example against the JAI library
itself.

## Run this scenario in the provider CLI

Use layered delivery for the portfolio recommendation because
prioritisation involves business meaning, policy constraints, feasible
delivery and evidence. It does not replace the actual portfolio or
funding authority.

Enter these instructions in the provider conversation, not a shell. The
Claude slash command and Codex skill request the same work. They are
workflow entry points, not a claim that routing or artefact creation is
universally automatic. Inspect the actual output locations and use those
paths if the workflow reports a different location from `working/`.

### 1. Normalise the incoming demand

=== "Claude Code"

    ```text
    /analyse inputs/ for the funding round. Identify incomplete submissions, dependencies, existing commitments and incomparable assumptions.
    ```

=== "Codex CLI"

    ```text
    $workflow-analyse inputs/ for the funding round. Identify incomplete submissions, dependencies, existing commitments and incomparable assumptions.
    ```

Inspect whether demand is expressed as an outcome or merely a preferred
solution. A mandated deadline differs from a sponsor's desired date.
Keep incomplete requests visible rather than silently assigning low
scores that imply they were fully assessed.

### 2. Prepare feasible portfolio options

=== "Claude Code"

    ```text
    /layered Prepare the funding-round recommendation from inputs/. Compare capacity-constrained options, dependency sequencing, funding conditions and deferred demands in working/.
    ```

=== "Codex CLI"

    ```text
    $workflow-layered Prepare the funding-round recommendation from inputs/. Compare capacity-constrained options, dependency sequencing, funding conditions and deferred demands in working/.
    ```

Inspect scenarios rather than a single artificial optimum. A request may
be valuable and still depend on an unfunded platform change. Make the
consequences of partial funding visible and distinguish provisional
resource estimates from committed capacity.

### 3. Challenge the recommendation

When review presents the criteria and their hash, inspect them and
answer YES only if they match this task. The review then proceeds; that
confirmation authorises the review, not the deliverable or a risk.

=== "Claude Code"

    ```text
    /review working/ against inputs/funding-policy.md and inputs/strategy.md; check criteria consistency, capacity realism and treatment of incomplete demand.
    ```

=== "Codex CLI"

    ```text
    $workflow-review working/ against inputs/funding-policy.md and inputs/strategy.md; check criteria consistency, capacity realism and treatment of incomplete demand.
    ```

Read findings for inconsistent scoring and unrecorded exceptions.
Independent review should challenge how the recommendation was reached,
without voting on behalf of the investment committee. A correct
spreadsheet formula does not establish the validity of its scores.

### 4. Escalate an unfunded prerequisite

Replace `<reported-ledger>` with the findings ledger identifier or path
returned by the preceding review. Keep this same ledger through rework
and independent verification; do not invent one or mark findings closed
without verification.

=== "Claude Code"

    ```text
    /rework <reported-ledger>
    Use the current findings ledger to retain the portal's identity-platform dependency and prepare funding options that do not hide its cost.
    ```

=== "Codex CLI"

    ```text
    $workflow-rework <reported-ledger>
    Use the current findings ledger to retain the portal's identity-platform dependency and prepare funding options that do not hide its cost.
    ```

The illustrative conflict is that the portal is ranked first but its
prerequisite is outside the requested budget. Alice replies: "Show a
combined option and a deferral option; do not label the portal funded in
isolation." Any formal allocation requires the actual human authority,
using the runtime-emitted trusted command where applicable.

### 5. Prepare the funding meeting pack

Publication requires an approved, stable semantic snapshot and a
registered publication profile. Use the actual approved snapshot returned
by the workflow, then follow its manifest and rendering steps. If those
prerequisites are absent, stop before rendering. Approval for publication
does not itself approve the business, deployment or risk decision.

=== "Claude Code"

    ```text
    /publish Prepare a publication from the reviewed semantic recommendation in working/ for output/. Preserve deferred items, conditions and the actual funding status.
    ```

=== "Codex CLI"

    ```text
    $workflow-publish Prepare a publication from the reviewed semantic recommendation in working/ for output/. Preserve deferred items, conditions and the actual funding status.
    ```

If the budget ceiling changes, register the revised source and reassess
feasibility rather than merely changing the first page. Inspect the
decision table for clear boundaries between recommendation, conditional
allocation and authorised commitment.

## Finish and hand off

Hand over the demand register, criteria, option comparison, capacity and
funding assumptions, review findings and real decisions. Every deferred
item retains an owner and reason. Teams should not begin committed
delivery because a proposed portfolio pack has been generated.

For the wider role chain, required handoffs and blocking decisions, see
the [workflow catalogue](../reference/workflows.md). For handling an
actual authority request, follow [human
authority](../operations/human-authority.md).
