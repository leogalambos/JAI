# Example: Intermittent production defect

Owner: JAI maintainers. Last reviewed: 2026-10-20.

This walkthrough illustrates the `incident-to-problem` workflow recipe.
It is not an additional native slash command.

ACME's invoice service sometimes rejects a valid payment authorization. Alice maintains the service and Bob represents the payment integration. A local test fails intermittently, but the actual customer impact is still being investigated. This is a debugging walkthrough, not an incident declaration or permission to inspect live customer payments.

The names and circumstances are fictional examples of common operating
practice. They do not describe an actual customer or executed engagement.

## Prepare a project workspace

Create `acme-invoice-diagnosis/` with `input/`, `working/` and `output/`.
Keep supplied records in `input/`, drafts in `working/` and the reviewed
handoff in `output/`. These are chosen destinations; ask JAI to report
its actual file paths rather than assuming fixed generated filenames.

Supply:

- source/ — the invoice-service checkout and dependency lockfiles
- failure-record.md — failing test name, observed frequency and sanitized output
- last-known-good.md — release identities and relevant change history
- payment-contract.md — timeout, retry, approval and business-decline semantics

Add `PROJECT.md` with the question, accountable owner, exclusions and
handling rules. If a record is absent, list the gap and request it from
its owner. Narrow conclusions while it is missing; do not fill gaps with
plausible invented evidence.

## Run this scenario in the provider CLI

Follow the [installation guide](../getting-started/install.md) for the
appropriate JAI adapter, then start Claude Code or Codex in this project.
Enter the prompts below in that provider's conversation, not a shell.
Choose one provider and keep the same project conversation throughout.

Use diagnosis before developing a fix. The analyst must compare the last known good state, a working analogue and timing. A business decline and a technical timeout are different outcomes; merging them to make a test green would change the contract.

Ask for actual report paths, findings ledgers and engagement identifiers.
Inspect them between stages. Use `<reported-review-target>` for the actual
artifact path that JAI reports; do not type that placeholder literally. Replace `<reported-ledger>` below with the
ledger actually returned by review; the placeholder is not a real ledger.

### 1. Understand the service boundary

**Claude Code**

```text
/analyse input/source/ with input/payment-contract.md. Map authorization, retries and decline handling. Identify missing observations; do not contact the live payment provider.
```

**Codex**

```text
$workflow-analyse input/source/ with input/payment-contract.md. Map authorization, retries and decline handling. Identify missing observations; do not contact the live payment provider.
```

Inspect whether the account of the failing path names actual functions and test fixtures. If the sanitized record omits whether the response was late or negative, ask Bob for that distinction. Avoid spending the first session rewriting unrelated payment code.

### 2. Establish the root cause

**Claude Code**

```text
/diagnose Diagnose the intermittent payment authorization failure recorded in input/failure-record.md. Compare last known good, a working authorization path and timeout ordering. Use local evidence only.
```

**Codex**

```text
$workflow-diagnose Diagnose the intermittent payment authorization failure recorded in input/failure-record.md. Compare last known good, a working authorization path and timeout ordering. Use local evidence only.
```

Read the reproduced command, repetitions and competing explanations. One successful run cannot refute an intermittent failure. Timing checks should explain which event wins and under what conditions. If the cause remains uncertain, continue diagnosis rather than describing a plausible race as confirmed.

### 3. Develop only the confirmed correction

**Claude Code**

```text
/develop Develop a local fix for the confirmed authorization defect. Preserve business-decline semantics and add a regression covering the observed ordering.
```

**Codex**

```text
$workflow-develop Develop a local fix for the confirmed authorization defect. Preserve business-decline semantics and add a regression covering the observed ordering.
```

Inspect the change against the diagnosis. A test should fail for the original ordering and pass after correction, while genuine declines stay declines. Check whether retries could charge twice or create duplicate requests. Development evidence must identify which local checks actually ran.

### 4. Review the behavioral change

**Claude Code**

```text
/review <reported-review-target> the authorization change against the payment contract and diagnosis. Check timeout ordering, idempotency, legitimate declines and regression strength.
```

**Codex**

```text
$workflow-review <reported-review-target> the authorization change against the payment contract and diagnosis. Check timeout ordering, idempotency, legitimate declines and regression strength.
```

Read located findings rather than only an overall verdict. Ask whether the regression controls timing deliberately or merely retries a flaky assertion. Keep actual live-provider behavior unverified unless separately authorized evidence exists; mocked approval fixtures are not customer transactions.

### 5. Rework and prepare the change handoff

**Claude Code**

```text
/rework <reported-ledger> Rework the open diagnosis and implementation review findings. Prepare the proposed change handoff under output/, preserving missing production observations.
```

**Codex**

```text
$workflow-rework <reported-ledger> Rework the open diagnosis and implementation review findings. Prepare the proposed change handoff under output/, preserving missing production observations.
```

Inspect the verification against the original failure and the contract. A local fix may be ready for normal release handling while customer-impact analysis remains open. Record both statuses. Do not mark the deployed defect resolved simply because the source test now passes.

## Handle an escalation or changed evidence

Suppose diagnosis finds a race but resolving it requires deciding whether to wait longer for an uncertain payment response. Alice's example reply is: “Preserve the existing customer-visible timeout. Investigate an idempotent reconciliation path; do not turn uncertainty into either approval or decline.” Resume with `/diagnose` or `$workflow-diagnose` to test that alternative. If the contract itself must change, open a bounded `/layered` or `$workflow-layered` decision and retain the current uncertainty.

Resume the existing engagement with its actual identifiers when one is
active. A conversational reply can clarify or restrict work; it does not
replace a signed L0 act. If the runtime requires an authority operation,
the authorized human follows the exact instruction emitted through the
trusted authority path. Do not invent a substitute approval command.

If independent review finds that the test still depends on wall-clock sleep, use `/rework` or `$workflow-rework` with the actual ledger to introduce deterministic ordering. If a second failure appears in refund handling, first record a separate diagnosis scope. Similar symptoms do not establish the same root cause.

## Know when to stop

Stop when the cause is evidenced, the bounded fix preserves the contract, the original failure is covered and review findings have verified outcomes. Record repetition counts honestly and mark live-provider or production checks NOT_EXECUTED. Deployment and customer recovery remain separate operational work.

The **Incident and defect diagnosis** chain in the
[enterprise workflow catalogue](../reference/workflows.md) describes the
roles and handoffs behind this example. It is a workflow recipe, not an
additional slash command. Authors do not verify their own findings. The
example has not been executed as part of this guide.
