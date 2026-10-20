# Prepare supplier onboarding

Owner: JAI documentation maintainers. Updated: 2026-10-20.

ACME Health Services wants to onboard a supplier that will process
appointment messages. Alice owns procurement, Bob owns the service and
John Doe coordinates security due diligence. This illustrative fiction
reflects ordinary supplier assurance; it does not assert that a real
supplier is safe, certified or contractually acceptable.

The outcome is a justified onboarding recommendation with explicit
dependencies and residual risks. A supplier questionnaire is a statement
by the supplier, not automatic evidence that every control operates.

## Prepare the project

Create a new `acme-supplier-onboarding/` directory with `inputs/`,
`working/` and `output/` beneath it. Keep received source files in
`inputs/` and proposed work separate from material ready for handoff.

Collect the proposed service scope, data-flow description, supplier
responses, available assurance reports, draft agreement, service levels,
subprocessor information and exit requirements. Include ACME's
classification and outsourcing policies and the identity of the actual
contract and risk owners.

Use names such as `inputs/supplier-scope.md`,
`inputs/questionnaire.xlsx`, `inputs/data-flow.pdf and
inputs/contract-draft.docx`. Keep source dates, versions and owners in
`inputs/source-register.md`. Record evidence dates and coverage. If an
assurance report excludes the proposed service, state the gap instead of
borrowing its badge.

Complete the [installation](../getting-started/install.md), then start
Claude Code or Codex in `acme-supplier-onboarding/`. Confirm the
installed JAI commands or skills are available. All paths below are
relative to that project directory; do not run the example against the
JAI library itself.

## Run this scenario in the provider CLI

Use layered delivery to coordinate procurement, security, privacy,
operational acceptance and contract decisions. An internal supplier
decision is distinct from the supplier commercial-delivery profile used
to prepare ACME's own offers.

Enter these instructions in the provider conversation, not a shell. The
Claude slash command and Codex skill request the same work. They are
workflow entry points, not a claim that routing or artefact creation is
universally automatic. Inspect the actual output locations and use those
paths if the workflow reports a different location from `working/`.

### 1. Understand the service and evidence

**Claude**

```text
/analyse inputs/ for appointment-message supplier onboarding. Describe information flows, service dependencies, assurance coverage and missing evidence.
```

**Codex**

```text
$workflow-analyse inputs/ for appointment-message supplier onboarding. Describe information flows, service dependencies, assurance coverage and missing evidence.
```

Inspect the scope before scoring the questionnaire. A supplier may
provide satisfactory evidence for one product and none for the product
being purchased. Check whether subcontractors and support access appear
in the service description.

### 2. Prepare the onboarding decision

**Claude**

```text
/layered Assess the supplier using inputs/. Prepare risk, contractual, privacy and operational acceptance needs, including exit and monitoring, in working/.
```

**Codex**

```text
$workflow-layered Assess the supplier using inputs/. Prepare risk, contractual, privacy and operational acceptance needs, including exit and monitoring, in working/.
```

Inspect how each concern affects a concrete decision or contract
requirement. Avoid a single unexplained risk score. The proposed
recommendation should identify conditional acceptance, deferral or
rejection options without impersonating the human risk owner.

### 3. Review the decision package

When review presents the criteria and their hash, inspect them and
answer YES only if they match this task. The review then proceeds; that
confirmation authorises the review, not the deliverable or a risk.

**Claude**

```text
/review working/ against the supplied onboarding policies; check evidence scope, unresolved contract clauses and receiving-service responsibilities.
```

**Codex**

```text
$workflow-review working/ against the supplied onboarding policies; check evidence scope, unresolved contract clauses and receiving-service responsibilities.
```

Read located findings and compare contract schedules with the technical
scope. A statement that encryption is available does not establish how
this service will use it. Independent review should remain separate from
procurement negotiation pressure.

### 4. Escalate a missing assurance dependency

Replace `<reported-ledger>` with the findings ledger identifier or path
returned by the preceding review. Keep this same ledger through rework
and independent verification; do not invent one or mark findings closed
without verification.

**Claude**

```text
/rework <reported-ledger>
Use the current findings ledger to keep the supplier's unverified support-access controls open and prepare evidence and contract options for the responsible owners.
```

**Codex**

```text
$workflow-rework <reported-ledger>
Use the current findings ledger to keep the supplier's unverified support-access controls open and prepare evidence and contract options for the responsible owners.
```

The illustrative supplier declines to disclose support-access evidence
before signature. Alice replies: "Do not treat the questionnaire as
verification; seek alternative assurance or defer onboarding." The next
rework should preserve that dependency. The actual authority, if needed,
records its act using the exact runtime-emitted trusted command.

### 5. Reassess onboarding conditions

**Claude**

```text
/layered Reassess the supplier after the new evidence or negotiated terms in inputs/. Update conditions, monitoring ownership and operational handoff before a recommendation.
```

**Codex**

```text
$workflow-layered Reassess the supplier after the new evidence or negotiated terms in inputs/. Update conditions, monitoring ownership and operational handoff before a recommendation.
```

If a new subprocessor appears, register it as a changed input and
revisit privacy, trust and exit implications. Inspect whether conditions
have been fulfilled or merely promised; an unresolved promise must
remain visible at the decision.

## Finish and hand off

Procurement and the service owner receive the evidence register,
assessment, contract issues, actual decisions and onboarding conditions.
Contract signature, risk acceptance and access provisioning remain
separately authorised actions. JAI does not grant supplier approval
because the dossier has no formatting errors.

For the wider role chain, required handoffs and blocking decisions, see
the [workflow catalogue](../reference/workflows.md). For handling an
actual authority request, follow [human
authority](../operations/human-authority.md).
