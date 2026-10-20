# Coordinate a cyber incident response

Owner: JAI documentation maintainers. Updated: 2026-10-20.

ACME Logistics discovers suspicious access to a supplier account used by
its booking service. Alice is incident commander, Bob operates the
service and John Doe coordinates security analysis. This is an
illustrative fictional response scenario based on common
incident-management practice; there is no real compromise, investigation
result or containment success.

The outcome is a coordinated response plan and evidence-backed incident
record. JAI can help structure facts, decisions and handoffs; it does
not replace the incident commander, emergency procedures or forensic
tools.

## Prepare the project

Create a new `acme-cyber-incident/` directory with `inputs/`, `working/`
and `output/` beneath it. Keep received source files in `inputs/` and
proposed work separate from material ready for handoff.

Collect the declared incident scope, approved response procedure,
service inventory, relevant timestamped alerts, available identity logs
and named contacts. Use authorised, minimised copies of evidence with
appropriate handling. Retain originals through the organisation's
evidence procedures rather than treating an editable narrative as a
forensic source.

Use names such as `inputs/incident-brief.md`, `inputs/timeline.csv`,
`inputs/service-dependencies.md` and `inputs/response-authority.md`. Keep
source dates, versions and owners in `inputs/source-register.md`. Mark
unverified observations as unverified. Missing logging is a limitation,
not proof that no other account was used.

Complete the [installation](../getting-started/install.md), then start
Claude Code or Codex in `acme-cyber-incident/`. Confirm the installed
JAI commands or skills are available. All paths below are relative to
that project directory; do not run the example against the JAI library
itself.

## Run this scenario in the provider CLI

Use layered delivery to coordinate consequential containment and
recovery decisions. This walkthrough does not authorise offensive
testing, account changes or external notifications; those actions
require the actual incident and operational authority.

Enter these instructions in the provider conversation, not a shell. The
Claude slash command and Codex skill request the same work. They are
workflow entry points, not a claim that routing or artefact creation is
universally automatic. Inspect the actual output locations and use those
paths if the workflow reports a different location from `working/`.

### 1. Separate observations from hypotheses

**Claude**

```text
/analyse inputs/ for the supplier-account incident. Describe confirmed observations, hypotheses, missing evidence and immediate decision needs.
```

**Codex**

```text
$workflow-analyse inputs/ for the supplier-account incident. Describe confirmed observations, hypotheses, missing evidence and immediate decision needs.
```

Inspect the timeline for timezone, provenance and source consistency.
Distinguish an alert from a confirmed event and avoid naming a cause
prematurely. The fact that a suspicious login occurred does not
establish which data was accessed.

### 2. Prepare coordinated response options

**Claude**

```text
/layered Coordinate the incident response using inputs/. Prepare bounded containment, business-impact and recovery options, with owners and evidence needs in working/.
```

**Codex**

```text
$workflow-layered Coordinate the incident response using inputs/. Prepare bounded containment, business-impact and recovery options, with owners and evidence needs in working/.
```

Inspect the operational consequences of each option. Disabling the
supplier identity may stop legitimate bookings, so the incident
commander needs the dependency and fallback information. Agent-produced
instructions are proposed work until the responsible operator authorises
execution.

### 3. Review the incident record

When review presents the criteria and their hash, inspect them and
answer YES only if they match this task. The review then proceeds; that
confirmation authorises the review, not the deliverable or a risk.

**Claude**

```text
/review working/ against inputs/response-authority.md; check evidence boundaries, timeline consistency, response ownership and unsupported statements of containment.
```

**Codex**

```text
$workflow-review working/ against inputs/response-authority.md; check evidence boundaries, timeline consistency, response ownership and unsupported statements of containment.
```

Read findings without delaying emergency action mandated by the existing
response procedure. Ensure the report distinguishes actions planned,
actions executed and effects observed. An agent's successful document
check is not evidence that an attacker has been removed.

### 4. Escalate a containment conflict

Replace `<reported-ledger>` with the findings ledger identifier or path
returned by the preceding review. Keep this same ledger through rework
and independent verification; do not invent one or mark findings closed
without verification.

**Claude**

```text
/rework <reported-ledger>
Use the current findings ledger to preserve the booking-service availability conflict and prepare the decision for Alice without weakening the containment requirement.
```

**Codex**

```text
$workflow-rework <reported-ledger>
Use the current findings ledger to preserve the booking-service availability conflict and prepare the decision for Alice without weakening the containment requirement.
```

The illustrative conflict is that disabling the account would interrupt
a critical shipment window. Alice replies: "Use the approved manual
booking fallback while the authorised operator disables the account;
verify effects before recovery." Record who actually executed each
action. If protected authority recording is required, the human uses the
emitted trusted command, not an invented approval.

### 5. Reassess recovery with observed evidence

**Claude**

```text
/layered Reassess recovery using the authorised action results added to inputs/. Keep unverified persistence and data-access questions open and prepare the receiving-team handoff.
```

**Codex**

```text
$workflow-layered Reassess recovery using the authorised action results added to inputs/. Keep unverified persistence and data-access questions open and prepare the receiving-team handoff.
```

If fresh logs show another identity, extend scope through the incident
process and revisit containment. Inspect the updated dependencies and
monitoring criteria. Do not mark recovery complete simply because a
proposed plan was followed or the initial alert stopped.

## Finish and hand off

The handoff includes the evidence-referenced timeline, actual action
record, unresolved hypotheses, recovery criteria and named service
owner. Notification, legal interpretation and business risk acceptance
remain with authorised humans. Lessons learned should distinguish
evidence gaps from demonstrated control failures.

For the wider role chain, required handoffs and blocking decisions, see
the [workflow catalogue](../reference/workflows.md). For handling an
actual authority request, follow [human
authority](../operations/human-authority.md).
