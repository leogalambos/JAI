# Plan a cloud migration

Owner: JAI documentation maintainers. Updated: 2026-10-20.

ACME Manufacturing wants to move its customer portal from a data-centre
virtual machine estate to a managed cloud platform. Alice owns the
service, Bob coordinates operations, and John Doe chairs the migration
decision. This is an illustrative fictional case based on a common
migration problem; no benchmark, cloud saving or outage allowance is
established by the example.

The outcome is a reviewable migration and cutover plan, with a credible
reversal path. Choosing a target platform is only one decision:
dependencies, data transfer, support ownership and the business service
window determine whether migration can proceed.

## Prepare the project

Create a new `acme-cloud-migration/` directory with `inputs/`,
`working/` and `output/` beneath it. Keep received source files in
`inputs/` and proposed work separate from material ready for handoff.

Collect the current architecture, application and database inventory,
interface catalogue, data classification, actual utilisation history,
contract constraints and service-level requirements. Include an existing
backup/restore report if one exists; an inventory claiming backups are
configured is weaker evidence than a successful recovery exercise.

Use names such as `inputs/service-map.md`, `inputs/dependencies.csv`,
`inputs/utilisation.csv` and `inputs/change-window.md`. Keep source dates,
versions and owners in `inputs/source-register.md`. If recovery time or
the maximum tolerable data loss is unknown, ask the service owner. Do
not infer a recovery promise from a cloud product description.

Complete the [installation](../getting-started/install.md), then start
Claude Code or Codex in `acme-cloud-migration/`. Confirm the installed
JAI commands or skills are available. All paths below are relative to
that project directory; do not run the example against the JAI library
itself.

## Run this scenario in the provider CLI

Use layered delivery because the migration joins business constraints,
design, implementation planning and an operational go/no-go. It
preserves the authority boundary while allowing specialists to work on
their own evidence.

Enter these instructions in the provider conversation, not a shell. The
Claude slash command and Codex skill request the same work. They are
workflow entry points, not a claim that routing or artefact creation is
universally automatic. Inspect the actual output locations and use those
paths if the workflow reports a different location from `working/`.

### 1. Read the existing estate

**Claude**

```text
/analyse inputs/ for the portal migration. Describe dependencies, source gaps and constraints without selecting a target solution.
```

**Codex**

```text
$workflow-analyse inputs/ for the portal migration. Describe dependencies, source gaps and constraints without selecting a target solution.
```

Inspect the estate summary against the inventory. Look for a payment
connection, scheduled batch job or identity dependency omitted from the
diagram. Keep the observed estate distinct from an architect's preferred
replacement.

### 2. Develop the migration decision

**Claude**

```text
/layered Plan the portal migration using inputs/. Compare feasible target options, migration waves, cutover, verification and rollback. Keep proposed material in working/.
```

**Codex**

```text
$workflow-layered Plan the portal migration using inputs/. Compare feasible target options, migration waves, cutover, verification and rollback. Keep proposed material in working/.
```

Inspect the derived requirements and acceptance evidence. A wave plan
should say what moves together and why. A rollback plan needs a trigger,
owner and data-consistency consequences; the word rollback is not a
tested procedure.

### 3. Challenge the plan

When review presents the criteria and their hash, inspect them and
answer YES only if they match this task. The review then proceeds; that
confirmation authorises the review, not the deliverable or a risk.

**Claude**

```text
/review working/ against inputs/change-window.md; check dependency coverage, data reconciliation, recovery evidence and receiving-team ownership.
```

**Codex**

```text
$workflow-review working/ against inputs/change-window.md; check dependency coverage, data reconciliation, recovery evidence and receiving-team ownership.
```

Read findings as concrete problems to resolve. Confirm that success
means a working business service, not merely successful infrastructure
deployment. Have reviewers expose untested restoration and ambiguous
supplier responsibilities.

### 4. Respond to the findings

Replace `<reported-ledger>` with the findings ledger identifier or path
returned by the preceding review. Keep this same ledger through rework
and independent verification; do not invent one or mark findings closed
without verification.

**Claude**

```text
/rework <reported-ledger>
Use the current findings ledger to revise working/. Preserve the unresolved data-recovery conflict and identify the evidence needed before cutover.
```

**Codex**

```text
$workflow-rework <reported-ledger>
Use the current findings ledger to revise working/. Preserve the unresolved data-recovery conflict and identify the evidence needed before cutover.
```

The illustrative escalation is that replication lag could exceed the
agreed data-loss boundary. Alice replies: "Keep cutover pending; obtain
a rehearsal and compare the reconciliation results." That is a request
for evidence, not acceptance of the risk. Use the runtime's exact
protected command only through the named human if authority recording is
required.

### 5. Resume with fresh evidence

**Claude**

```text
/layered Reassess the portal migration using the new rehearsal evidence in inputs/. Reopen affected acceptance criteria and prepare the cutover decision for the actual authority.
```

**Codex**

```text
$workflow-layered Reassess the portal migration using the new rehearsal evidence in inputs/. Reopen affected acceptance criteria and prepare the cutover decision for the actual authority.
```

If a supplier changes the database migration method, treat it as a
changed input and repeat the affected design and evidence work. Inspect
source revisions and findings closure; never copy the fictional
example's outcome into a real migration report.

## Finish and hand off

The receiving team has the reviewed wave and cutover plan, dependency
inventory, recovery procedure, evidence references and outstanding
decisions. Production execution requires the organisation's actual
change authority. A document review does not demonstrate that failover,
restore or rollback has succeeded.

For the wider role chain, required handoffs and blocking decisions, see
the [workflow catalogue](../reference/workflows.md). For handling an
actual authority request, follow [human
authority](../operations/human-authority.md).
