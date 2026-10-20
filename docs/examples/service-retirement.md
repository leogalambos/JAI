# Retire a service without losing obligations

Owner: JAI maintainers. Last reviewed: 2026-10-20.

This walkthrough illustrates the `service-retirement-and-decommission` workflow recipe.
It is not an additional native slash command.

ACME wants to retire a legacy reporting service after its replacement becomes available. Alice owns the service and Bob coordinates records and integrations. Turning off the server is the last technical step, not evidence that users, data retention and downstream consumers are ready.

These names and circumstances are fictional. They illustrate common public
operating practices, not an account of an actual ACME engagement.

## Prepare a project workspace

Create a new directory named `acme-legacy-reporting-retirement/` with `input/`,
`working/` and `output/` subdirectories. Keep source material in `input/`;
use `working/` for drafts and `output/` for the reviewed handoff. These are
your chosen locations, not filenames JAI guarantees to generate.

Supply:

- service-inventory.md — components, owners, consumers and costs
- replacement-status.md — migration evidence and known functional gaps
- data-obligations.md — retention, deletion and retrieval requirements
- retirement-brief.md — proposed date, responsibilities and constraints

Add `PROJECT.md` with the question, accountable owner, scope exclusions and
confidentiality constraints. Do not fabricate missing records. List absent
inputs and ask the relevant owner for them; narrow the conclusion while
they remain unavailable.

## Run this scenario in the provider CLI

Install the appropriate JAI adapter using the [installation guide](../getting-started/install.md).
Start Claude Code or Codex in the new project directory. The prompts below
are conversational inputs to that provider, not shell commands. Choose
one provider column and continue in the same project conversation.

Use analysis to discover dependencies and the layered path to prepare the retirement decision. Review the exit evidence before any shutdown. JAI should not infer authorization to delete data from an instruction to reduce service costs.

The command pairs are equivalent entry points; they do not imply identical
provider tools. Ask JAI to report actual output paths and any engagement,
snapshot or findings identifiers. Read those results before proceeding. Replace `<reported-review-target>`
with the actual draft path reported by the preceding stage.
In a rework prompt, replace `<reported-ledger>` with the ledger the review
actually reported. Never invent its identifier or erase open findings.

### 1. Identify what still depends on the service

**Claude Code**

```text
/analyse input/ for the reporting-service retirement. Identify consumers, scheduled integrations, retained records and uncertain ownership. Do not operate or delete the service.
```

**Codex**

```text
$workflow-analyse input/ for the reporting-service retirement. Identify consumers, scheduled integrations, retained records and uncertain ownership. Do not operate or delete the service.
```

Inspect whether the inventory includes monthly and annual reporting jobs. A quiet week of traffic does not establish that no one needs a quarterly export. Ask Bob to obtain owner responses for infrequent consumers and preserve nonresponses as open dependencies.

### 2. Prepare the retirement decision

**Claude Code**

```text
/layered Prepare a bounded retirement decision with dependency closure, data handling, rollback or recovery limits and the proposed shutdown sequence.
```

**Codex**

```text
$workflow-layered Prepare a bounded retirement decision with dependency closure, data handling, rollback or recovery limits and the proposed shutdown sequence.
```

Check whether the plan distinguishes disabling access, stopping compute and deleting records. Those actions have different reversal paths. The draft should explain when recovery would require rebuilding infrastructure or restoring archived data, and who is entitled to accept that limitation.

### 3. Set exit criteria

**Claude Code**

```text
/criteria .
```

**Codex**

```text
$workflow-criteria .
```

This displays or initializes the project criteria. Then ask:

> Set retirement review criteria from the service inventory, replacement evidence and data obligations. Require actual consumer and records-owner evidence where applicable.

Confirm the criteria shown by review before allowing assessment to start.

Read the criteria before reviewing the closure pack. A replacement demo is not confirmation that every required report migrated. Define how a consumer's unresolved objection is escalated, rather than treating a missed response deadline as implied agreement.

### 4. Review the closure evidence

**Claude Code**

```text
/review <reported-review-target> the proposed retirement pack against the fixed criteria. Locate missing migration evidence, retention controls and unresolved contracts.
```

**Codex**

```text
$workflow-review <reported-review-target> the proposed retirement pack against the fixed criteria. Locate missing migration evidence, retention controls and unresolved contracts.
```

Inspect a sample of report mappings and retrieval instructions. An archive that nobody can decrypt or search may not satisfy the stated obligation. If a retrieval rehearsal has not happened, record NOT_EXECUTED and request an authorized exercise instead of describing the archive as usable.

### 5. Rework and hand over the shutdown plan

**Claude Code**

```text
/rework <reported-ledger> Rework retirement findings and prepare the proposed shutdown and observation handoff under output/. Preserve deletion and execution as pending human-controlled actions.
```

**Codex**

```text
$workflow-rework <reported-ledger> Rework retirement findings and prepare the proposed shutdown and observation handoff under output/. Preserve deletion and execution as pending human-controlled actions.
```

Inspect who monitors for late consumer failures, how long rollback remains possible and what evidence closes the service record. A cost saving can be proposed from the inventory; realized savings require actual billing or accounting evidence after retirement.

## Handle an escalation or changed evidence

Suppose the records owner says that historical reports must remain retrievable for seven years, but the replacement does not support them. Alice's example reply is: “Remove deletion from this scope. Prepare an archive-access option and its operating owner; shutdown remains conditional on retrieval evidence.” Resume with `/layered` or `$workflow-layered` to revise the retirement boundary without inventing a retention waiver.

Continue the existing engagement where one is active, with its actual
identifiers and unresolved conditions. The example reply clarifies work;
it is not a signed L0 authority act. If the runtime requires such an act,
the authorized human must follow the exact instruction it emits through
the trusted authority path. Do not substitute conversational consent.

If review reveals an overlooked finance export, use `/rework` or `$workflow-rework` after the consumer supplies its requirements. If the business asks to delete the archive as well, reopen scope and the data-obligation decision first. The earlier retirement review does not authorize irreversible disposal.

## Know when to stop

Finish with a reviewed proposed retirement plan, dependency responses, records handling evidence, unresolved conditions and an execution handoff. Keep actual shutdown, deletion, recovery tests and realized cost changes separate. Only supplied execution evidence can establish that the service was retired successfully.

Use the **Service retirement** chain in the
[enterprise workflow catalogue](../reference/workflows.md) to check roles
and handoffs. Review and verification must remain separate from authoring;
a revised draft does not verify itself. The examples above have not been
executed as part of this guide, and their outcomes are not evidence.
