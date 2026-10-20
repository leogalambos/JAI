# 20-minute quick start

This tour is intentionally practical. It shows how the system behaves in realistic work rather than only describing features.

If you do not yet know which walkthrough fits your task, start with the
[experimental hint guide](../using/experimental-hint.md). `/hint` (Claude)
or `$workflow-hint` (Codex) recommends a starting procedure; `/guide`
explains a selected example and `/demo` prepares fictional practice inputs.

When a task produces a lesson worth reusing, ask JAI to remember that specific
part of the current conversation. It prepares the record and asks for missing
metadata before saving; you do not need to write out the steps again. Follow
[Remember useful knowledge](../using/remembering-knowledge.md) for examples
and the limits of experimental capture.

These are short exercises across the demo estate, not a single governed engagement. For a complete reader journey, continue to [How to use JAI](../examples/how-to-use-JAI/index.md): choose the assurance arrangement, then follow the security-assessment, Android-development or commercial-proposal case. A final `/layered` exercise here does not recreate a layered history for preceding exercises.

**Run the examples inside your Claude Code or Codex CLI session** in the demo workspace; do not paste these into a system shell. Except where shown explicitly, examples below use the **Claude** `/command` notation; Codex uses the corresponding **`$workflow-command`** skill with the same intent. The provider agent is responsible for calling the internal Python helpers. Manual shell work is normally limited to installation/maintenance and the special Codex **L0 human-authority** action; see [the interaction model](../using/interaction-model.md).

| User intent | Claude command | Codex skill |
| --- | --- | --- |
| Analyse a repository | `/analyse invoice-service` | `$workflow-analyse invoice-service` |
| Fix review criteria | `/criteria invoice-service` | `$workflow-criteria invoice-service` |
| Review the result | `/review invoice-service` | `$workflow-review invoice-service` |
| Diagnose a defect | `/diagnose <symptom>` | `$workflow-diagnose <symptom>` |
| Manage SABSA | `/sabsa ...` | `$workflow-sabsa ...` |
| Open consequential engagement | `/layered <intent>` | `$workflow-layered <intent>` |
| Request an independent trace | `/fabric-report` | `$workflow-fabric-report` |


## 1. Create the demo estate

Claude:

```text
/demo setup
```

Codex:

```text
$workflow-demo setup
```

This creates three practice workspaces under `~/it-role-demo/`.

| Demo | Purpose | Useful commands |
| --- | --- | --- |
| `invoice-service` | Small Python billing service with deliberate defects. | `/analyse`, `/criteria`, `/review`, `/rework`, `/diagnose`, `/develop`, `/layered` |
| `policy-docs` | Security policy library with deliberate content and governance defects. | `/analyse`, `/review`, `/rework`, `/govern` |
| `acme-pay` | Fictional client notes and RFP material for SABSA and solution work. | `/sabsa`, `/publish`, `/layered` |

## 2. Analyse before judging

```text
/analyse invoice-service
```

### Expected shape of the answer

```text
Repository profile
- Python billing service
- modules: API, invoice logic, persistence, payments
- external dependencies: SQLite, payment gateway
- tests present but incomplete
- notable hotspots: API authorisation, payment timing, money correctness

Recommended next step
- establish review criteria before issuing findings
```

A good result first explains what the system is and where complexity lies.

## 3. Establish criteria, then review

```text
/criteria invoice-service
/review invoice-service
```

### What to expect

- explicit criteria categories;
- a review boundary separate from code changes;
- findings recorded into `.findings/`;
- severity and remediation guidance;
- a clear route to `/rework`.

## 4. Diagnose an intermittent defect

```text
/diagnose test_charge_is_approved in tests/test_payments.py fails now and then.
```

The defect workflow must compare the last known good state, a working analogue and timing/order effects. That is materially stronger than a shallow “guess a fix” answer.

## 5. Build and inspect a SABSA library

```text
/sabsa prepare acme-pay/sabsa -- source material is in acme-pay/client-material
/sabsa create acme-pay/sabsa
/sabsa questions acme-pay/sabsa
```

### What to expect

- traceability from business drivers to operations;
- explicit coverage of all 36 SABSA matrix cells;
- open questions identified separately from settled architecture elements.

Markdown is the SABSA workflow's default document format. When you need a publication, ask in the same conversation: “Generate the Logical Security Architecture in English as LaTeX and PDF from the reviewed sources; keep unresolved gaps visible.” Use `/sabsa document acme-pay/sabsa` in Claude or `$workflow-sabsa document acme-pay/sabsa` in Codex before that instruction. Ask for DOCX or editable CSV catalogues explicitly when useful. These are existing format choices, not a new global default setting.

The six viewpoint documents include authored narrative, full specifications and typed business paths. Write and review their semantic chapter files before rendering; generated files cannot substitute for missing architecture decisions. See [publication prerequisites](../configuration/publication-stack.md) and the [How to use JAI tutorials](../examples/how-to-use-JAI/index.md) for a fuller security-assessment or Android-development walkthrough. Those tutorials distinguish source reports, adapted instructions and work still to be performed.

## 6. Run a consequential decision

```text
/layered Decide whether invoice-service is ready to be exposed to external partners. It must be secure enough for partner traffic and its money calculations must be exact.
```

Then request an independent report **in the same provider conversation** (not a Fabric shell invocation):

```text
/fabric-report
```

This is the fastest way to experience what makes the Justifiable Fabric different from a normal AI-generated recommendation. In Codex the corresponding call is `$workflow-fabric-report`. The report should cite actual engagement IDs, evidence and blockers; if a risk/authority escalation reaches L0, Codex cannot perform the guarded approval for you. A trusted human action may be required before the result becomes releasable.
