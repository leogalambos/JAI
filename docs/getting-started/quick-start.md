# 20-minute quick start

This tour is intentionally practical. It shows how the system behaves in realistic work rather than only describing features.

## Before you begin

Complete [installation](install.md), then start a fresh Claude Code or Codex
session so the installed commands or skills are available. This tour uses
fictional local inputs; it does not require a client system or customer data.

The demo setup creates `~/it-role-demo/`. After setup, open that directory as
your provider workspace and start a new session there before continuing with
step 2. The relative paths in this tour, such as `invoice-service` and
`acme-pay/client-material`, are relative to `~/it-role-demo/`.

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

**Run the examples inside your Claude Code or Codex CLI session**; do not paste
them into a system shell. Run step 1 from a session permitted to create
`~/it-role-demo/`, then use that directory as the workspace for the remaining
steps. Choose the Claude Code or Codex CLI tab for each example; both variants
express the same intent. The provider agent calls the internal Python helpers.
Manual host work covers installation and maintenance, restricted operator tasks
and external signed **L0 human-authority** decisions in either provider. Native
tool approval is separate; see [the interaction model](../using/interaction-model.md).

| User intent | Claude command | Codex skill |
| --- | --- | --- |
| Analyse a repository | `/analyse invoice-service` | `$workflow-analyse invoice-service` |
| Establish review criteria | `/criteria invoice-service` | `$workflow-criteria invoice-service` |
| Review the result | `/review invoice-service` | `$workflow-review invoice-service` |
| Diagnose a defect | `/diagnose <symptom>` | `$workflow-diagnose <symptom>` |
| Manage SABSA | `/sabsa ...` | `$workflow-sabsa ...` |
| Open consequential engagement | `/layered <intent>` | `$workflow-layered <intent>` |
| Request an independent trace | `/fabric-report` | `$workflow-fabric-report` |


## 1. Create the demo estate

=== "Claude Code"

    ```text
    /demo setup
    ```

=== "Codex CLI"

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

=== "Claude Code"

    ```text
    /analyse invoice-service
    ```

=== "Codex CLI"

    ```text
    $workflow-analyse invoice-service
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

=== "Claude Code"

    ```text
    /criteria invoice-service
    /review invoice-service
    ```

=== "Codex CLI"

    ```text
    $workflow-criteria invoice-service
    $workflow-review invoice-service
    ```

### What to expect

- explicit criteria categories;
- a review boundary separate from code changes;
- findings recorded into `.findings/`;
- severity and remediation guidance;
- a clear route to `/rework`.

## 4. Diagnose an intermittent defect

=== "Claude Code"

    ```text
    /diagnose test_charge_is_approved in tests/test_payments.py fails now and then.
    ```

=== "Codex CLI"

    ```text
    $workflow-diagnose test_charge_is_approved in tests/test_payments.py fails now and then.
    ```

The defect workflow compares the last known good state, a working analogue and
timing or ordering effects. Its findings should identify the evidence supporting
the diagnosis before a repair is proposed.

## 5. Build and inspect a SABSA library

=== "Claude Code"

    ```text
    /sabsa prepare acme-pay/sabsa -- source material is in acme-pay/client-material
    /sabsa create acme-pay/sabsa
    /sabsa questions acme-pay/sabsa
    ```

=== "Codex CLI"

    ```text
    $workflow-sabsa prepare acme-pay/sabsa -- source material is in acme-pay/client-material
    $workflow-sabsa create acme-pay/sabsa
    $workflow-sabsa questions acme-pay/sabsa
    ```

### What to expect

- traceability from business drivers to operations;
- explicit coverage of all 36 SABSA matrix cells;
- open questions identified separately from settled architecture elements.

Markdown is the SABSA workflow's default document format. When you need a publication, ask in the same conversation: “Generate the Logical Security Architecture in English as LaTeX and PDF from the reviewed sources; keep unresolved gaps visible.” Use `/sabsa document acme-pay/sabsa` in Claude or `$workflow-sabsa document acme-pay/sabsa` in Codex before that instruction. Ask for DOCX or editable CSV catalogues explicitly when useful. These are existing format choices, not a new global default setting.

The six viewpoint documents include authored narrative, full specifications and typed business paths. Write and review their semantic chapter files before rendering; generated files cannot substitute for missing architecture decisions. See [publication prerequisites](../configuration/publication-stack.md) and the [How to use JAI tutorials](../examples/how-to-use-JAI/index.md) for a fuller security-assessment or Android-development walkthrough. Those tutorials distinguish source reports, adapted instructions and work still to be performed.

## 6. Run a consequential decision

=== "Claude Code"

    ```text
    /layered Decide whether invoice-service is ready to be exposed to external partners. It must be secure enough for partner traffic and its money calculations must be exact.
    ```

=== "Codex CLI"

    ```text
    $workflow-layered Decide whether invoice-service is ready to be exposed to external partners. It must be secure enough for partner traffic and its money calculations must be exact.
    ```

Then request an independent report **in the same provider conversation** (not a Fabric shell invocation):

=== "Claude Code"

    ```text
    /fabric-report
    ```

=== "Codex CLI"

    ```text
    $workflow-fabric-report
    ```

This is the fastest way to experience what makes the Justifiable Fabric different from a normal AI-generated recommendation. The report should cite actual engagement IDs, evidence and blockers; if a risk/authority escalation reaches L0, Codex cannot perform the guarded approval for you. A trusted human action may be required before the result becomes releasable.

## Current operator boundary

For JAI {{ JAI_VERSION }}, use the maintained
[execution routes and boundaries](../security/product-operations.md) and
[operator walkthrough](../operations/operator-walkthrough.md).
Role-authorised local work runs automatically when the effective sandbox and
required tools permit it. Actual Office QA follows that same rule: use the
permitted Office renderer locally, or request an exact operator host action when
it is unavailable. A PDF rendered from HTML does not inspect Office bytes.

A provider permission prompt or host execution handoff is distinct from a
reserved L0 decision. Only the human signs such a decision through the external
operator procedure; the returned proof must match its exact request and effects.

## Local QA and human intervention

Use A / AUTO for role-authorized local work inside the actual sandbox. B is
an observed native permission request; C is an exact operator host task. Neither
is Fabric L0. D is a separately signed consequential decision; it may precede C.
Every B/C/D request must include the complete action and reason inline before
linking details. See [execution routes and boundaries](../security/product-operations.md)
and the [full operator guide](../operations/operator-walkthrough.md).
