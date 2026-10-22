# Build a business case and benefits review

Owner: JAI documentation maintainers. Updated: 2026-10-20.

ACME Transport is considering a scheduling system intended to reduce
manual coordination. Alice sponsors the investment, Bob estimates
delivery and John Doe owns benefits tracking. This illustrative fiction
reflects a familiar investment decision; no saving, return or forecast
is a real ACME result.

The task is to prepare a decision-worthy business case and an explicit
way to revisit benefits. Investment approval, a delivery forecast and
measured benefits are different records with different evidence.

## Prepare the project

Create a new `acme-business-case/` directory with `inputs/`, `working/`
and `output/` beneath it. Keep received source files in `inputs/` and
proposed work separate from material ready for handoff.

Collect the current operating process, available cost records, activity
volumes, options, supplier estimates, internal effort assumptions and
investment policy. Include proposed benefit owners, measurement sources,
baseline dates and dependencies such as process adoption or staffing
changes.

Use names such as `inputs/current-costs.xlsx`, `inputs/options.md`,
`inputs/estimate-basis.md` and `inputs/benefit-measures.md`. Keep source
dates, versions and owners in `inputs/source-register.md`. If the
current baseline is unavailable, show the uncertainty and required
measurement. Do not convert hypothetical hours saved into an assured
cash reduction.

Complete the [installation](../getting-started/install.md), then start
Claude Code or Codex in `acme-business-case/`. Confirm the installed JAI
commands or skills are available. All paths below are relative to that
project directory; do not run the example against the JAI library
itself.

## Run this scenario in the provider CLI

Use layered delivery because the recommendation affects investment and
benefit accountability. A financial specialist should challenge
assumptions separately from the sponsor's desire to approve the project.

Enter these instructions in the provider conversation, not a shell. The
Claude slash command and Codex skill request the same work. They are
workflow entry points, not a claim that routing or artefact creation is
universally automatic. Inspect the actual output locations and use those
paths if the workflow reports a different location from `working/`.

### 1. Understand the baseline and choices

=== "Claude Code"

    ```text
    /analyse inputs/ for the scheduling investment. Separate actual costs, estimates, benefit hypotheses and missing baseline evidence.
    ```

=== "Codex CLI"

    ```text
    $workflow-analyse inputs/ for the scheduling investment. Separate actual costs, estimates, benefit hypotheses and missing baseline evidence.
    ```

Inspect units, dates, currencies and whether figures describe cash,
accounting expense or capacity. Releasing staff time can improve service
without reducing payroll. Treat supplier estimates as estimates with a
scope and validity period.

### 2. Prepare the business case

=== "Claude Code"

    ```text
    /layered Prepare the scheduling business case using inputs/. Compare options, costs, sensitivity, dependencies and benefit ownership; keep proposed artefacts in working/.
    ```

=== "Codex CLI"

    ```text
    $workflow-layered Prepare the scheduling business case using inputs/. Compare options, costs, sensitivity, dependencies and benefit ownership; keep proposed artefacts in working/.
    ```

Inspect the assumptions behind totals and the treatment of recurring
cost. A single return number should not hide uncertainty. Benefits need
a proposed measurement method and owner, while the authority must be
able to see the consequences of doing nothing.

### 3. Challenge financial consistency

When review presents the criteria and their hash, inspect them and
answer YES only if they match this task. The review then proceeds; that
confirmation authorises the review, not the deliverable or a risk.

=== "Claude Code"

    ```text
    /review working/ against inputs/estimate-basis.md and the investment criteria; check totals, time horizons, baseline evidence and double-counted benefits.
    ```

=== "Codex CLI"

    ```text
    $workflow-review working/ against inputs/estimate-basis.md and the investment criteria; check totals, time horizons, baseline evidence and double-counted benefits.
    ```

Read the findings alongside the workbook. Check that narrative savings
match the actual model and do not combine capacity and cash benefits
twice. An AI review does not replace finance approval or establish that
projected benefits will occur.

### 4. Escalate an unsupported saving

Replace `<reported-ledger>` with the findings ledger identifier or path
returned by the preceding review. Keep this same ledger through rework
and independent verification; do not invent one or mark findings closed
without verification.

=== "Claude Code"

    ```text
    /rework <reported-ledger>
    Use the current findings ledger to retain the unsupported payroll-saving claim as a finding and revise the options and sensitivity accordingly.
    ```

=== "Codex CLI"

    ```text
    $workflow-rework <reported-ledger>
    Use the current findings ledger to retain the unsupported payroll-saving claim as a finding and revise the options and sensitivity accordingly.
    ```

Suppose the case assumes staff reduction while operations plans to
redeploy the same people. Alice replies: "Present capacity improvement
separately; remove the cash claim until finance supplies a defensible
basis." This changes an assumption, not the formal investment authority.
A required authority act belongs to the human using the emitted
procedure.

### 5. Continue the existing benefits decision

=== "Claude Code"

    ```text
    /layered Continue the existing investment engagement using the measured follow-up inputs when available. Compare actual results with the recorded baseline without rewriting the original approved case.
    ```

=== "Codex CLI"

    ```text
    $workflow-layered Continue the existing investment engagement using the measured follow-up inputs when available. Compare actual results with the recorded baseline without rewriting the original approved case.
    ```

If adoption is delayed, add the new observation and update the forecast
and corrective options. Do not retrospectively alter the signed baseline
to make variance disappear. Inspect whether the benefits owner can
explain each variance and its evidence.

## Finish and hand off

The handoff includes the business case, assumption and source register,
financial model, benefit measures, reviewer findings and actual
investment decision where available. Later reviews distinguish original
baseline, current forecast and actual measurements. A proposed business
case may legitimately remain deferred.

For the wider role chain, required handoffs and blocking decisions, see
the [workflow catalogue](../reference/workflows.md). For handling an
actual authority request, follow [human
authority](../operations/human-authority.md).
