# Take over an inherited codebase

Owner: JAI maintainers. Last reviewed: 2026-10-20.

This walkthrough illustrates the `codebase-takeover` workflow recipe.
It is not an additional native slash command.

ACME has acquired maintenance responsibility for a supplier-built booking portal. Alice is the receiving engineering lead; Bob represents the outgoing supplier. The immediate goal is a trustworthy takeover plan, not a rewrite justified by unfamiliar code.

These names and circumstances are fictional. They illustrate common public
operating practices, not an account of an actual ACME engagement.

## Prepare a project workspace

Create a new directory named `acme-portal-takeover/` with `input/`,
`working/` and `output/` subdirectories. Keep source material in `input/`;
use `working/` for drafts and `output/` for the reviewed handoff. These are
your chosen locations, not filenames JAI guarantees to generate.

Supply:

- source/ — the repository snapshot with its licence information
- handover.md — supplier notes, known defects and contacts
- build-instructions.md — supported toolchain and build commands
- service-map.md — integrations, data stores and deployment ownership

Add `PROJECT.md` with the question, accountable owner, scope exclusions and
confidentiality constraints. Do not fabricate missing records. List absent
inputs and ask the relevant owner for them; narrow the conclusion while
they remain unavailable.

## Run this scenario in the provider CLI

Install the appropriate JAI adapter using the [installation guide](../getting-started/install.md).
Start Claude Code or Codex in the new project directory. The prompts below
are conversational inputs to that provider, not shell commands. Choose
one provider column and continue in the same project conversation.

Start with analysis, then fix review criteria before assessing the implementation. Development begins only for a bounded finding. A broad rewrite would need a separate decision about business value, migration and support.

The command pairs are equivalent entry points; they do not imply identical
provider tools. Ask JAI to report actual output paths and any engagement,
snapshot or findings identifiers. Read those results before proceeding. Replace `<reported-review-target>`
with the actual draft path reported by the preceding stage.
In a rework prompt, replace `<reported-ledger>` with the ledger the review
actually reported. Never invent its identifier or erase open findings.

### 1. Map the system without a verdict

=== "Claude Code"

    ```text
    /analyse input/source/ with input/handover.md and input/service-map.md. Explain entry points, deployment boundaries and unanswered takeover questions in working/.
    ```

=== "Codex CLI"

    ```text
    $workflow-analyse input/source/ with input/handover.md and input/service-map.md. Explain entry points, deployment boundaries and unanswered takeover questions in working/.
    ```

Inspect whether the report identifies real files and build entry points. Ask it to distinguish observed dependencies from integrations merely mentioned in notes. Missing source for a deployed component is a handover gap; it must not be treated as a clean component because no code was available.

### 2. Agree what takeover must establish

=== "Claude Code"

    ```text
    /criteria .
    ```

=== "Codex CLI"

    ```text
    $workflow-criteria .
    ```

This displays or initializes the project criteria. Then ask:

> Set takeover review criteria for reproducible builds, supported dependencies, licence records, recoverability and ownership. Keep an architectural rewrite out of scope.

Confirm the criteria shown by review before allowing assessment to start.

Read these criteria before the review starts. Decide which checks are feasible locally and which require the outgoing supplier or operations team. This prevents a later preference for a different framework from being reported as a defect against requirements nobody agreed.

### 3. Review against the fixed criteria

=== "Claude Code"

    ```text
    /review input/source/ against the takeover criteria and supplied operational records. Locate findings and separate verified failures from unanswered questions.
    ```

=== "Codex CLI"

    ```text
    $workflow-review input/source/ against the takeover criteria and supplied operational records. Locate findings and separate verified failures from unanswered questions.
    ```

Check a sample of findings against their cited source locations. A missing test suite, an unexecuted build and a failing build are different findings. Dependency age alone does not establish a vulnerability; licence uncertainty needs a document request rather than an invented legal conclusion.

### 4. Repair a bounded takeover blocker

=== "Claude Code"

    ```text
    /develop Develop a local fix for the selected reproducible-build finding only. Preserve application behavior and document the supported build invocation.
    ```

=== "Codex CLI"

    ```text
    $workflow-develop Develop a local fix for the selected reproducible-build finding only. Preserve application behavior and document the supported build invocation.
    ```

Inspect the changed files and the recorded build output. A successful build on one workstation still leaves deployment configuration and data recovery to their respective owners. Ask the reviewer to verify the original failure condition rather than merely accept the new instructions.

### 5. Plan ownership and remaining work

=== "Claude Code"

    ```text
    /govern input/source/ Prepare a proposed ownership and maintenance model from the verified takeover findings. Name unresolved supplier inputs and the receiving team's review responsibilities.
    ```

=== "Codex CLI"

    ```text
    $workflow-govern input/source/ Prepare a proposed ownership and maintenance model from the verified takeover findings. Name unresolved supplier inputs and the receiving team's review responsibilities.
    ```

Inspect whether every critical component has a proposed owner and an escalation route. Governance proposals are not automatically accepted assignments. Put the recommended backlog and verified handover evidence under output/ only after reading them for unsupported readiness claims.

## Handle an escalation or changed evidence

Suppose the supplier cannot provide the encryption-key recovery procedure. Alice's example reply is: “Continue code and build review. Mark recoverability as unresolved; do not declare takeover complete. Bob must supply the recovery owner and an authorized rehearsal plan.” Resume with `/review` or `$workflow-review` for the evidence that is available, retaining the recovery finding. A statement that the supplier has always managed keys is not a recovery test.

Continue the existing engagement where one is active, with its actual
identifiers and unresolved conditions. The example reply clarifies work;
it is not a signed L0 authority act. If the runtime requires such an act,
the authorized human must follow the exact instruction it emits through
the trusted authority path. Do not substitute conversational consent.

If review rejects a build fix because it embeds workstation-specific paths, use `/rework` or `$workflow-rework` on that finding. If management then asks to replace the framework, use `/layered` or `$workflow-layered` to open a separately scoped migration decision. Do not hide a rewrite inside takeover cleanup.

## Know when to stop

The useful result is an understandable system map, fixed review criteria, located and verified findings, a bounded fix and an explicitly incomplete handover where evidence is missing. Record commands actually run and keep production-access checks NOT_EXECUTED until an authorized operator supplies results.

Use the **Codebase takeover** chain in the
[enterprise workflow catalogue](../reference/workflows.md) to check roles
and handoffs. Review and verification must remain separate from authoring;
a revised draft does not verify itself. The examples above have not been
executed as part of this guide, and their outcomes are not evidence.
