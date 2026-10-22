# Prepare an architecture board decision

Owner: JAI documentation maintainers. Updated: 2026-10-20.

ACME Retail must decide whether its order service should use a shared
integration platform or direct partner connections. Alice sponsors the
service, Bob maintains the platform and John Doe coordinates the
architecture board. This illustrative fiction reflects a familiar
design-review setting and supplies no actual approval or performance
evidence.

The useful result is a decision package that makes the options and
consequences understandable. The board should be able to distinguish a
mandatory constraint from a preference and a measured fact from an
estimate.

## Prepare the project

Create a new `acme-architecture-board/` directory with `inputs/`,
`working/` and `output/` beneath it. Keep received source files in
`inputs/` and proposed work separate from material ready for handoff.

Collect the business outcome, current application and interface views,
approved architecture principles, relevant security constraints,
service-level needs and the candidate solution descriptions. Include the
actual decision remit: which decisions belong to this board and which
require a different owner.

Use names such as `inputs/decision-remit.md`, `inputs/options.md`,
`inputs/current-interfaces.csv` and `inputs/architecture-principles.md`.
Keep source dates, versions and owners in `inputs/source-register.md`.
If throughput requirements are estimates, identify the estimator and
uncertainty. Do not turn an illustrative reference architecture into an
ACME-approved standard.

Complete the [installation](../getting-started/install.md), then start
Claude Code or Codex in `acme-architecture-board/`. Confirm the
installed JAI commands or skills are available. All paths below are
relative to that project directory; do not run the example against the
JAI library itself.

## Run this scenario in the provider CLI

Use layered delivery for the decision itself. A direct document review
can inspect the resulting paper, but cannot grant the board's authority
or resolve a cross-domain policy conflict.

Enter these instructions in the provider conversation, not a shell. The
Claude slash command and Codex skill request the same work. They are
workflow entry points, not a claim that routing or artefact creation is
universally automatic. Inspect the actual output locations and use those
paths if the workflow reports a different location from `working/`.

### 1. Understand the decision boundary

=== "Claude Code"

    ```text
    /analyse inputs/ for the integration decision. Separate binding constraints, preferences, evidence and unresolved questions.
    ```

=== "Codex CLI"

    ```text
    $workflow-analyse inputs/ for the integration decision. Separate binding constraints, preferences, evidence and unresolved questions.
    ```

Inspect the scope before analysing products. The current platform owner
may be a valuable source and still have a preference that deserves
independent challenge. Confirm that all relevant decision makers and
affected service owners are represented.

### 2. Build an evidence-based option set

=== "Claude Code"

    ```text
    /layered Prepare the integration decision from inputs/. Compare the shared platform and direct connections, including security, operability, cost basis and reversibility. Use working/ for proposed artefacts.
    ```

=== "Codex CLI"

    ```text
    $workflow-layered Prepare the integration decision from inputs/. Compare the shared platform and direct connections, including security, operability, cost basis and reversibility. Use working/ for proposed artefacts.
    ```

Look for a meaningful alternative, explicit assumptions and consequences
over the service lifecycle. An unsupported numerical score should not
conceal a tradeoff. Check that each important conclusion identifies the
source or missing test behind it.

### 3. Review the board paper

When review presents the criteria and their hash, inspect them and
answer YES only if they match this task. The review then proceeds; that
confirmation authorises the review, not the deliverable or a risk.

=== "Claude Code"

    ```text
    /review working/ against inputs/decision-remit.md and inputs/architecture-principles.md; check option fairness and traceable rationale.
    ```

=== "Codex CLI"

    ```text
    $workflow-review working/ against inputs/decision-remit.md and inputs/architecture-principles.md; check option fairness and traceable rationale.
    ```

Inspect the findings and ensure the proposed recommendation remains
visibly proposed. A reviewer should identify gaps without rewriting the
author's reasoning into an apparently independent endorsement. AI
editorial review is not a board vote.

### 4. Handle an unresolved policy conflict

Replace `<reported-ledger>` with the findings ledger identifier or path
returned by the preceding review. Keep this same ledger through rework
and independent verification; do not invent one or mark findings closed
without verification.

=== "Claude Code"

    ```text
    /rework <reported-ledger>
    Use the current findings ledger to revise the decision paper. Keep the data-location exception open and prepare its options for the responsible authority.
    ```

=== "Codex CLI"

    ```text
    $workflow-rework <reported-ledger>
    Use the current findings ledger to revise the decision paper. Keep the data-location exception open and prepare its options for the responsible authority.
    ```

Suppose the preferred partner connection crosses a jurisdiction boundary
prohibited by the existing policy. Alice replies: "Do not waive the
policy; present a compliant option and the exception path separately."
The next rework must preserve the requirement. Human authority acts,
when needed, use only the exact runtime-emitted trusted command.

### 5. Prepare the board reading pack

Publication requires an approved, stable semantic snapshot and a
registered publication profile. Use the actual approved snapshot returned
by the workflow, then follow its manifest and rendering steps. If those
prerequisites are absent, stop before rendering. Approval for publication
does not itself approve the business, deployment or risk decision.

=== "Claude Code"

    ```text
    /publish Prepare a publication from the reviewed semantic artefact in working/ for output/. Preserve alternatives, pending exceptions and the recorded decision status.
    ```

=== "Codex CLI"

    ```text
    $workflow-publish Prepare a publication from the reviewed semantic artefact in working/ for output/. Preserve alternatives, pending exceptions and the recorded decision status.
    ```

If the partner revises its hosting location, register the new source and
reopen affected analysis before publication. Inspect the rendered
comparison table and the prominence of unresolved issues; attractive
slides must not suppress the board's actual choice.

## Finish and hand off

Hand over the decision paper, source and assumption register, option
comparison, reviewer findings and the actual decision record if one
exists. The paper can be ready for a meeting while the decision remains
pending. Implementation must follow the recorded authority and scope.

For the wider role chain, required handoffs and blocking decisions, see
the [workflow catalogue](../reference/workflows.md). For handling an
actual authority request, follow [human
authority](../operations/human-authority.md).
