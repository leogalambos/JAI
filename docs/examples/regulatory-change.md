# Assess and plan a regulatory change

Owner: JAI documentation maintainers. Updated: 2026-10-20.

ACME Finance receives a new reporting obligation affecting an existing
customer service. Alice owns compliance coordination, Bob owns the
service and John Doe represents change delivery. This illustrative
fiction uses a common regulatory-change setting; it makes no claim that
a particular law applies or that a system is compliant.

The outcome is a traceable impact assessment and delivery proposal for
qualified human interpretation. The text of an obligation, the
organisation's interpretation and evidence that a control works are
different things.

## Prepare the project

Create a new `acme-regulatory-change/` directory with `inputs/`,
`working/` and `output/` beneath it. Keep received source files in
`inputs/` and proposed work separate from material ready for handoff.

Collect the applicable published text, any authoritative internal legal
interpretation, current control descriptions, service and data flows,
reporting arrangements and the effective-date notice. Include the scope
statement defining affected entities, products and jurisdictions.

Use names such as `inputs/obligation-text.pdf`,
`inputs/legal-interpretation.md`, `inputs/current-controls.csv and
inputs/applicability.md`. Keep source dates, versions and owners in
`inputs/source-register.md`. An absent legal interpretation must stay a
question for the responsible adviser. A generated explanation cannot
silently become an authoritative interpretation.

Complete the [installation](../getting-started/install.md), then start
Claude Code or Codex in `acme-regulatory-change/`. Confirm the installed
JAI commands or skills are available. All paths below are relative to
that project directory; do not run the example against the JAI library
itself.

## Run this scenario in the provider CLI

Use layered delivery because interpretation, policy, design and
implementation evidence cross accountable boundaries. Use document
review to challenge completeness; it cannot provide a legal opinion or
regulatory acceptance.

Enter these instructions in the provider conversation, not a shell. The
Claude slash command and Codex skill request the same work. They are
workflow entry points, not a claim that routing or artefact creation is
universally automatic. Inspect the actual output locations and use those
paths if the workflow reports a different location from `working/`.

### 1. Inventory obligations and sources

=== "Claude Code"

    ```text
    /analyse inputs/ for the reporting change. Separate quoted obligations, internal interpretations, assumptions and missing applicability decisions.
    ```

=== "Codex CLI"

    ```text
    $workflow-analyse inputs/ for the reporting change. Separate quoted obligations, internal interpretations, assumptions and missing applicability decisions.
    ```

Inspect source dates and amendments before making an impact list. Record
where the meaning is uncertain and who can resolve it. A familiar
control catalogue is useful for comparison, but does not establish that
an obligation is satisfied.

### 2. Trace the impact into proposed changes

=== "Claude Code"

    ```text
    /layered Assess the reporting change using inputs/. Map affected services, controls, owners, delivery dependencies and required evidence. Keep proposed material in working/.
    ```

=== "Codex CLI"

    ```text
    $workflow-layered Assess the reporting change using inputs/. Map affected services, controls, owners, delivery dependencies and required evidence. Keep proposed material in working/.
    ```

Check whether each proposed change traces to an applicable requirement.
Inspect dependencies on supplier data and operational reporting
deadlines. Estimated implementation effort should have an owner and
basis rather than appear as a factual commitment.

### 3. Challenge the impact assessment

When review presents the criteria and their hash, inspect them and
answer YES only if they match this task. The review then proceeds; that
confirmation authorises the review, not the deliverable or a risk.

=== "Claude Code"

    ```text
    /review working/ against inputs/applicability.md and the recorded interpretation; check omissions, evidence claims and control ownership.
    ```

=== "Codex CLI"

    ```text
    $workflow-review working/ against inputs/applicability.md and the recorded interpretation; check omissions, evidence claims and control ownership.
    ```

Inspect the findings for entities or data flows left out of scope. A
complete-looking matrix can still carry an unsupported interpretation.
Keep independent assurance separate from the delivery team's desire to
close all rows.

### 4. Handle conflicting interpretations

Replace `<reported-ledger>` with the findings ledger identifier or path
returned by the preceding review. Keep this same ledger through rework
and independent verification; do not invent one or mark findings closed
without verification.

=== "Claude Code"

    ```text
    /rework <reported-ledger>
    Use the current findings ledger to preserve the disputed retention requirement and prepare alternatives for the qualified legal and policy owners.
    ```

=== "Codex CLI"

    ```text
    $workflow-rework <reported-ledger>
    Use the current findings ledger to preserve the disputed retention requirement and prepare alternatives for the qualified legal and policy owners.
    ```

Suppose the draft assumes a retention period that conflicts with the
existing privacy schedule. Alice replies: "Keep both constraints visible
and obtain an authorised interpretation before selecting a design." Do
not delete the inconvenient requirement. Any formal authority action
must be performed by the designated human through the runtime's emitted
trusted command.

### 5. Resume the delivery proposal

=== "Claude Code"

    ```text
    /layered Update the impact and delivery proposal using the authorised interpretation now recorded in inputs/. Reassess affected controls and evidence requirements before handoff.
    ```

=== "Codex CLI"

    ```text
    $workflow-layered Update the impact and delivery proposal using the authorised interpretation now recorded in inputs/. Reassess affected controls and evidence requirements before handoff.
    ```

A later amendment is a changed input, not a clerical update to the
conclusion. Reopen the relevant interpretation, policy and design steps.
Inspect whether the acceptance evidence can actually demonstrate
reporting completeness and timeliness.

## Finish and hand off

Hand over the applicability record, interpretation references, impact
matrix, proposed delivery work, evidence plan and remaining decisions.
The responsible compliance and legal owners decide whether the
organisation can rely on the assessment. A successful JAI check is not a
declaration of legal compliance.

For the wider role chain, required handoffs and blocking decisions, see
the [workflow catalogue](../reference/workflows.md). For handling an
actual authority request, follow [human
authority](../operations/human-authority.md).
