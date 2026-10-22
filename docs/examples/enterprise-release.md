# Prepare an enterprise release decision

Owner: JAI documentation maintainers. Updated: 2026-10-20.

ACME Commerce is coordinating a portal update across application,
identity and support teams. Alice owns release coordination, Bob owns
operations and John Doe represents the change authority. This
illustrative fiction reflects a common enterprise release, not JAI's own
software-release qualification or a real successful deployment.

The outcome is a coordinated release decision package with an
evidence-based go/no-go and operational handoff. Passing an
application's tests is one input; service readiness, dependencies,
rollout and recovery also matter.

## Prepare the project

Create a new `acme-enterprise-release/` directory with `inputs/`,
`working/` and `output/` beneath it. Keep received source files in
`inputs/` and proposed work separate from material ready for handoff.

Collect the release scope, component versions, dependency map, actual
test and security results, change requirements, rollout and recovery
procedures, support readiness and known defects. Include the release
authority and the receiving service owner's acceptance criteria.

Use names such as `inputs/release-scope.md`,
`inputs/component-evidence/`, `inputs/rollout-plan.md and
inputs/readiness-criteria.md`. Keep source dates, versions and owners in
`inputs/source-register.md`. Missing rehearsal evidence stays missing.
Do not infer operational readiness from a generated checklist or an
unrelated component's passing test.

Complete the [installation](../getting-started/install.md), then start
Claude Code or Codex in `acme-enterprise-release/`. Confirm the
installed JAI commands or skills are available. All paths below are
relative to that project directory; do not run the example against the
JAI library itself.

## Run this scenario in the provider CLI

Use layered delivery to coordinate the release decision and domain
handoffs. This does not invoke JAI A–H qualification: those gates
qualify the JAI package, whereas this scenario concerns ACME's service
release.

Enter these instructions in the provider conversation, not a shell. The
Claude slash command and Codex skill request the same work. They are
workflow entry points, not a claim that routing or artefact creation is
universally automatic. Inspect the actual output locations and use those
paths if the workflow reports a different location from `working/`.

### 1. Understand the release boundary

=== "Claude Code"

    ```text
    /analyse inputs/ for the portal release. Identify component versions, dependencies, evidence scope, unresolved defects and required authorities.
    ```

=== "Codex CLI"

    ```text
    $workflow-analyse inputs/ for the portal release. Identify component versions, dependencies, evidence scope, unresolved defects and required authorities.
    ```

Inspect whether the evidence belongs to the versions actually proposed
for release. A test report from an earlier build is not current evidence
merely because the component name matches. Keep planned work separate
from completed checks.

### 2. Prepare the coordinated decision

=== "Claude Code"

    ```text
    /layered Prepare the portal release decision using inputs/. Include rollout sequencing, go/no-go criteria, rollback ownership, service readiness and evidence gaps in working/.
    ```

=== "Codex CLI"

    ```text
    $workflow-layered Prepare the portal release decision using inputs/. Include rollout sequencing, go/no-go criteria, rollback ownership, service readiness and evidence gaps in working/.
    ```

Inspect cross-team dependencies and the point after which reversal
changes data or customer behaviour. A rollback plan should identify who
decides and which observations trigger action. Do not let an attractive
release date silently override a mandatory control.

### 3. Challenge the release pack

When review presents the criteria and their hash, inspect them and
answer YES only if they match this task. The review then proceeds; that
confirmation authorises the review, not the deliverable or a risk.

=== "Claude Code"

    ```text
    /review working/ against inputs/readiness-criteria.md; check evidence identity, unmet prerequisites, recovery and operational handoff.
    ```

=== "Codex CLI"

    ```text
    $workflow-review working/ against inputs/readiness-criteria.md; check evidence identity, unmet prerequisites, recovery and operational handoff.
    ```

Read the findings with the component owners. Distinguish a known defect
with an authorised disposition from one merely mentioned in a status
meeting. AI review can identify inconsistencies; actual service
acceptance remains with the accountable receiving owner.

### 4. Escalate an unmet release prerequisite

Replace `<reported-ledger>` with the findings ledger identifier or path
returned by the preceding review. Keep this same ledger through rework
and independent verification; do not invent one or mark findings closed
without verification.

=== "Claude Code"

    ```text
    /rework <reported-ledger>
    Use the current findings ledger to preserve the failed identity-service rehearsal and prepare resequencing or deferral options for the release authority.
    ```

=== "Codex CLI"

    ```text
    $workflow-rework <reported-ledger>
    Use the current findings ledger to preserve the failed identity-service rehearsal and prepare resequencing or deferral options for the release authority.
    ```

The illustrative sponsor asks to proceed despite the failure. Alice
replies: "Keep the go decision pending; obtain a corrected rehearsal or
remove the affected scope through change control." A request to continue
preparation is not deployment approval. Formal authority actions follow
the exact trusted procedure emitted by the runtime where applicable.

### 5. Prepare the operational reading pack

Publication requires an approved, stable semantic snapshot and a
registered publication profile. Use the actual approved snapshot returned
by the workflow, then follow its manifest and rendering steps. If those
prerequisites are absent, stop before rendering. Approval for publication
does not itself approve the business, deployment or risk decision.

=== "Claude Code"

    ```text
    /publish Prepare a publication from the reviewed semantic release artefact in working/ for output/. Preserve actual readiness, defects, pending decisions and rollback conditions.
    ```

=== "Codex CLI"

    ```text
    $workflow-publish Prepare a publication from the reviewed semantic release artefact in working/ for output/. Preserve actual readiness, defects, pending decisions and rollback conditions.
    ```

If a component is rebuilt, register its new identity and reassess
affected evidence before continuing the same engagement. Inspect the
final go/no-go table and handoff. The publication must not relabel a
failed or unexecuted check as passed.

## Finish and hand off

The handoff contains the release scope, version-specific evidence,
decisions, rollout and recovery procedures, communications ownership and
operational acceptance state. Actual deployment requires the applicable
human change and release authority. This guide does not certify
production readiness or run the full JAI release pipeline.

For the wider role chain, required handoffs and blocking decisions, see
the [workflow catalogue](../reference/workflows.md). For handling an
actual authority request, follow [human
authority](../operations/human-authority.md).
