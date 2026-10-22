# Prepare an AI system approval decision

Owner: JAI documentation maintainers. Updated: 2026-10-20.

ACME Insurance wants an assistant that drafts answers for human claims
handlers. Alice owns the service, Bob owns the data platform and John
Doe coordinates assurance. This illustrative fiction draws on a common
human-in-the-loop use case. It establishes no model accuracy, fairness,
regulatory classification or permission to deploy.

The outcome is a bounded approval package describing intended use,
prohibited use, evaluated behaviour and remaining uncertainty. A vendor
model card and a working demonstration are useful inputs, but neither
proves the proposed service is acceptable.

## Prepare the project

Create a new `acme-ai-approval/` directory with `inputs/`, `working/`
and `output/` beneath it. Keep received source files in `inputs/` and
proposed work separate from material ready for handoff.

Collect the intended-use statement, user journey, data-flow map, model
and supplier information, organisational AI policy, evaluation plan,
available results, human-review procedure and incident/rollback
arrangements. Include excluded uses and an owner for post-release
monitoring.

Use names such as `inputs/intended-use.md`, `inputs/data-flow.md`,
`inputs/evaluation-results.json` and `inputs/human-review.md`. Keep source
dates, versions and owners in `inputs/source-register.md`. If the
available evaluation uses synthetic examples only, preserve that
limitation. Do not describe it as production accuracy or professional
acceptance.

Complete the [installation](../getting-started/install.md), then start
Claude Code or Codex in `acme-ai-approval/`. Confirm the installed JAI
commands or skills are available. All paths below are relative to that
project directory; do not run the example against the JAI library
itself.

## Run this scenario in the provider CLI

Use layered delivery because deployment joins business purpose, data
rights, controls, system design and evidence. The workflow organises the
approval question; it does not itself make the human approval.

Enter these instructions in the provider conversation, not a shell. The
Claude slash command and Codex skill request the same work. They are
workflow entry points, not a claim that routing or artefact creation is
universally automatic. Inspect the actual output locations and use those
paths if the workflow reports a different location from `working/`.

### 1. Bound the proposed use

=== "Claude Code"

    ```text
    /analyse inputs/ for the claims-drafting assistant. Separate intended and excluded uses, actual evaluation evidence, assumptions and missing owner decisions.
    ```

=== "Codex CLI"

    ```text
    $workflow-analyse inputs/ for the claims-drafting assistant. Separate intended and excluded uses, actual evaluation evidence, assumptions and missing owner decisions.
    ```

Inspect whether the system merely drafts text or can take actions. A
change from suggestion to automatic claim disposition changes the
decision boundary. Identify where personal data enters and what the
human reviewer can realistically verify.

### 2. Prepare the approval package

=== "Claude Code"

    ```text
    /layered Prepare the AI service decision from inputs/. Include control objectives, evaluation limitations, human oversight, release conditions and monitoring; use working/ for proposed material.
    ```

=== "Codex CLI"

    ```text
    $workflow-layered Prepare the AI service decision from inputs/. Include control objectives, evaluation limitations, human oversight, release conditions and monitoring; use working/ for proposed material.
    ```

Inspect the trace from use constraints to technical and operational
controls. A statement that a human is in the loop needs a feasible
review process. Test results should identify the evaluated system and
dataset rather than imply all models behave alike.

### 3. Challenge the documented claims

When review presents the criteria and their hash, inspect them and
answer YES only if they match this task. The review then proceeds; that
confirmation authorises the review, not the deliverable or a risk.

=== "Claude Code"

    ```text
    /review working/ against inputs/intended-use.md and the supplied AI policy; check unsupported accuracy claims, excluded uses and operational accountability.
    ```

=== "Codex CLI"

    ```text
    $workflow-review working/ against inputs/intended-use.md and the supplied AI policy; check unsupported accuracy claims, excluded uses and operational accountability.
    ```

Look for claims extending beyond the actual evidence. A successful
benchmark may leave harmful edge cases unresolved. This documentation
review complements technical evaluation and accountable domain
assessment; it does not confer independent human approval.

### 4. Escalate an unsupported use expansion

Replace `<reported-ledger>` with the findings ledger identifier or path
returned by the preceding review. Keep this same ledger through rework
and independent verification; do not invent one or mark findings closed
without verification.

=== "Claude Code"

    ```text
    /rework <reported-ledger>
    Use the current findings ledger to preserve the conflict between drafting support and the requested automatic claim decision. Prepare the additional requirements and evidence needs.
    ```

=== "Codex CLI"

    ```text
    $workflow-rework <reported-ledger>
    Use the current findings ledger to preserve the conflict between drafting support and the requested automatic claim decision. Prepare the additional requirements and evidence needs.
    ```

The illustrative request is to remove the human check to save time.
Alice replies: "Keep the deployment limited to drafting; do not
implement automatic disposition." That clarification narrows scope
without signing an approval. Any formal authority act follows the
runtime's exact emitted human procedure.

### 5. Prepare the decision reading pack

Publication requires an approved, stable semantic snapshot and a
registered publication profile. Use the actual approved snapshot returned
by the workflow, then follow its manifest and rendering steps. If those
prerequisites are absent, stop before rendering. Approval for publication
does not itself approve the business, deployment or risk decision.

=== "Claude Code"

    ```text
    /publish Prepare a publication from the reviewed semantic AI service artefact in working/ for output/. Keep evaluation scope, residual risks and actual approval state visible.
    ```

=== "Codex CLI"

    ```text
    $workflow-publish Prepare a publication from the reviewed semantic AI service artefact in working/ for output/. Keep evaluation scope, residual risks and actual approval state visible.
    ```

If a supplier swaps the model version or retrieval source, record the
changed input and reassess the affected evidence before continuing the
same engagement. Inspect the final summary for a clear distinction
between readiness for review and authorisation to deploy.

## Finish and hand off

The service owner receives the bounded use statement, evidence register,
review findings, conditions, monitoring plan and pending decisions.
Deployment and risk acceptance require actual authorised decisions. A
synthetic evaluation or AI editorial report must remain labelled as
such.

For the wider role chain, required handoffs and blocking decisions, see
the [workflow catalogue](../reference/workflows.md). For handling an
actual authority request, follow [human
authority](../operations/human-authority.md).
