# Prepare a supplier proposal

Owner: JAI documentation maintainers. Updated: 2026-10-20.

ACME Services is considering a fixed-price bid for a customer support
portal. Alice owns the bid, Bob estimates delivery, and John Doe
represents the customer. This is an illustrative fictional engagement,
based on the familiar practice of responding to an RFP. No customer
requirements, prices, qualifications or approvals in this guide are real
evidence.

The useful outcome is a proposal whose promises can be traced to the
customer request, priced assumptions and delivery capacity. A polished
document alone is insufficient: an unresolved service exclusion can make
an attractive offer impossible to deliver.

## Prepare the project

Create a new project directory named `acme-proposal/`, with `inputs/`,
`working/` and `output/` beneath it. Put the customer RFP, clarification
responses, draft contract, service-level schedule and pricing workbook
in `inputs/`. Add ACME's delivery assumptions, available team capacity
and approved product descriptions. Retain the received originals.

Name files clearly, for example `inputs/customer-rfp.pdf`,
`inputs/clarifications.md` and `inputs/pricing.xlsx`. Record versions
and dates in `inputs/source-register.md`. If the customer has not
specified support hours, list that as a question; do not silently assume
office hours. Remove personal or confidential material that the selected
provider is not authorised to process.

Complete the [installation](../getting-started/install.md) first. Start
Claude Code or Codex with `acme-proposal/` as its working directory,
then confirm that the installed JAI commands or skills are available.
The paths below are relative to that directory.

## Run this scenario in the provider CLI

These are conversation instructions, not terminal commands. Enter the
Claude form in Claude Code or the dollar-prefixed skill form in Codex.
They request a governed workflow; they do not guarantee that every named
output appears automatically. Inspect the returned files and findings.

### 1. Establish the bid engagement

**Claude**

```text
/layered Establish the ACME portal bid engagement from inputs/. Identify
intent, boundaries, human commercial owner and authority. Keep proposed
working material in working/; do not commit an offer.
```

**Codex**

```text
$workflow-layered Establish the ACME portal bid engagement from inputs/.
Identify intent, boundaries, human commercial owner and authority. Keep
proposed working material in working/; do not commit an offer.
```

Use layered delivery because the offer crosses technical, commercial and
approval boundaries. Inspect the returned engagement identifier, scope
and unresolved questions. Keep that engagement active for the next step;
the commercial command extends an existing engagement.

### 2. Add the supplier commercial profile

**Claude**

```text
/commercial Extend the existing portal bid engagement with the supplier
commercial profile. Alice is the proposed human commercial owner.
Scope the bid, estimates, pricing and separate commercial assurance.
Use inputs/ and keep proposed deliverables in working/.
```

**Codex**

```text
$workflow-commercial Extend the existing portal bid engagement with the
supplier commercial profile. Alice is the proposed human commercial
owner. Scope the bid, estimates, pricing and separate commercial
assurance. Use inputs/ and keep proposed deliverables in working/.
```

Use the actual engagement identifier returned in step 1 if prompted.
Inspect the proposed profile change and its required authority before
treating it as active. Check estimate bases, contract exceptions and the
separation of pricing from independent assurance. A reference example
cannot establish ACME's available capacity or the customer's consent.

### 3. Challenge the draft against explicit criteria

When review presents the criteria and their hash, inspect them and
answer YES only if they match this task. The review then proceeds; that
confirmation authorises the review, not the deliverable or a risk.

**Claude**

```text
/review working/ against inputs/customer-rfp.pdf and the recorded bid
criteria; check requirement coverage, financial consistency and the
visibility of unresolved contractual exceptions.
```

**Codex**

```text
$workflow-review working/ against inputs/customer-rfp.pdf and the recorded
bid criteria; check requirement coverage, financial consistency and the
visibility of unresolved contractual exceptions.
```

This document review complements the commercial assurance in the
engagement; it does not substitute for professional or customer
approval. Read located findings, especially disagreements between the
pricing workbook, staffing plan and proposal narrative.

### 4. Rework an exception without concealing it

Suppose the RFP requires continuous support but the estimate covers only
business hours. The escalation should expose the requirement, cost and
options. Alice's illustrative reply is: "Do not offer continuous support
at the current price. Request a customer clarification and keep the bid
pending." That reply narrows the work; it is not a signed authority act.

**Claude**

```text
/rework <reported-ledger>
Use the current findings ledger. Record the support-hours
conflict as unresolved, prepare the clarification and revise the
affected scope and price assumptions without inventing customer consent.
```

**Codex**

```text
$workflow-rework <reported-ledger>
Use the current findings ledger. Record the support-hours
conflict as unresolved, prepare the clarification and revise the
affected scope and price assumptions without inventing customer consent.
```

If JAI emits a protected authority command, the named human runs that
exact command through the documented trusted path. Never ask the agent
to approve its own bid or replace a pending decision with a PASS label.

### 5. Prepare the approved publication

Publication requires an approved, stable semantic snapshot and a
registered publication profile. Use the actual approved snapshot returned
by the workflow, then follow its manifest and rendering steps. If those
prerequisites are absent, stop before rendering. Approval for publication
does not itself approve the business, deployment or risk decision.

**Claude**

```text
/publish Prepare the proposal publication from the reviewed semantic
artefact in working/ for output/. Preserve qualifications, evidence
references and the actual approval state.
```

**Codex**

```text
$workflow-publish Prepare the proposal publication from the reviewed
semantic artefact in working/ for output/. Preserve qualifications,
evidence references and the actual approval state.
```

Use publication only when its input and approval prerequisites are
satisfied. Inspect rendered tables, totals, exception visibility and
document control. If a new customer clarification arrives, add it as a
new input revision, reassess affected estimates and repeat review before
publishing again.

## Finish and hand off

The handoff contains the reviewed proposal, compliance mapping, estimate
basis, explicit exceptions and remaining decisions. Alice can explain
every material promise and identify its approver. A draft may remain
pending; publication does not authorise contract signature.

For the underlying role sequence and handoffs, see the [workflow
library](../reference/workflows.md).
