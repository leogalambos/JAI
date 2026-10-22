# Publish an enterprise decision document

Owner: JAI maintainers. Last reviewed: 2026-10-20.

This walkthrough illustrates the `semantic-to-enterprise-publication` workflow recipe.
It is not an additional native slash command.

ACME must turn an architecture decision into a readable management publication. Alice owns the semantic decision and Bob prepares the publication. The decision concerns consolidating internal reporting platforms; the publication must communicate the approved meaning without inventing a stronger business case.

These names and circumstances are fictional. They illustrate common public
operating practices, not an account of an actual ACME engagement.

## Prepare a project workspace

Create a new directory named `acme-decision-publication/` with `input/`,
`working/` and `output/` subdirectories. Keep source material in `input/`;
use `working/` for drafts and `output/` for the reviewed handoff. These are
your chosen locations, not filenames JAI guarantees to generate.

Supply:

- decision.md — source decision and its actual review status
- evidence-register.md — sources, limitations and unresolved assumptions
- audience-brief.md — management questions, accessibility and format needs
- publication-rules.md — required document control, distribution and reviewers

Add `PROJECT.md` with the question, accountable owner, scope exclusions and
confidentiality constraints. Do not fabricate missing records. List absent
inputs and ask the relevant owner for them; narrow the conclusion while
they remain unavailable.

## Run this scenario in the provider CLI

Install the appropriate JAI adapter using the [installation guide](../getting-started/install.md).
Start Claude Code or Codex in the new project directory. The prompts below
are conversational inputs to that provider, not shell commands. Choose
one provider column and continue in the same project conversation.

Use publication for transforming an existing semantic artifact. If the source decision is still contested, resolve that issue through the layered or review path first. Publication quality and approval of the decision are separate concerns.

The command pairs are equivalent entry points; they do not imply identical
provider tools. Ask JAI to report actual output paths and any engagement,
snapshot or findings identifiers. Read those results before proceeding. Replace `<reported-review-target>`
with the actual draft path reported by the preceding stage.
In a rework prompt, replace `<reported-ledger>` with the ledger the review
actually reported. Never invent its identifier or erase open findings.

### 1. Inspect source readiness

=== "Claude Code"

    ```text
    /analyse input/ for publication readiness. Identify the decision's actual status, evidence boundaries and unresolved semantic questions before choosing presentation treatments.
    ```

=== "Codex CLI"

    ```text
    $workflow-analyse input/ for publication readiness. Identify the decision's actual status, evidence boundaries and unresolved semantic questions before choosing presentation treatments.
    ```

Inspect whether statements such as 'approved' identify a real authority record. A draft labelled final by its author is still insufficient. Ask Alice to clarify status and the exact source version; Bob must not use layout work to settle a disputed option. If the semantic snapshot is not approved or the profile is not registered, stop before publication and return to the semantic owner. A Markdown filename alone is not a publication-ready snapshot.

### 2. Set the audience and publication contract

=== "Claude Code"

    ```text
    /criteria .
    ```

=== "Codex CLI"

    ```text
    $workflow-criteria .
    ```

This displays or initializes the project criteria. Then ask:

> Set publication review criteria from input/audience-brief.md and input/publication-rules.md. Cover source fidelity, visible limitations, document control and readability.

Confirm the criteria shown by review before allowing assessment to start.

Read what the management audience needs to decide or understand. If the brief asks for a one-page summary, define what must remain accessible in the supporting material. Brevity does not permit deleting a material assumption or making an uncertain saving look committed.

### 3. Prepare the publication set

=== "Claude Code"

    ```text
    /publish Prepare publication from the approved semantic snapshot reported for this project, using its registered publication profile. Preserve its meaning, evidence links and unresolved status. Report the manifest and draft output paths.
    ```

=== "Codex CLI"

    ```text
    $workflow-publish Prepare publication from the approved semantic snapshot reported for this project, using its registered publication profile. Preserve its meaning, evidence links and unresolved status. Report the manifest and draft output paths.
    ```

Inspect the proposed source-to-publication mapping and draft outputs. File destinations depend on the actual publication workflow and should be reported by the run. The illustrative output/ directory is your handoff location, not a promise that the command creates a specific PDF or slide deck.

### 4. Review meaning and presentation

=== "Claude Code"

    ```text
    /review <reported-review-target> the publication set against the fixed criteria and source decision. Check whether financial caveats, rejected alternatives and evidence limitations survived transformation.
    ```

=== "Codex CLI"

    ```text
    $workflow-review <reported-review-target> the publication set against the fixed criteria and source decision. Check whether financial caveats, rejected alternatives and evidence limitations survived transformation.
    ```

Inspect text, tables and any generated graphics together. A red status rendered only through colour may be inaccessible, while a reordered table can change the perceived recommendation. If renderers are unavailable, retain visual checks as NOT_EXECUTED rather than accepting the Markdown preview as equivalent.

### 5. Rework and release the proposed set

=== "Claude Code"

    ```text
    /rework <reported-ledger> Rework the publication findings without changing the source decision. Prepare the reviewed files and their actual check results for the publication owner.
    ```

=== "Codex CLI"

    ```text
    $workflow-rework <reported-ledger> Rework the publication findings without changing the source decision. Prepare the reviewed files and their actual check results for the publication owner.
    ```

Check that a presentational fix has not quietly become a semantic amendment. If Alice changes the decision itself, establish a new source identity and repeat affected checks. Distribution authorization remains with the named owner; a successful render does not authorize sending the files.

## Handle an escalation or changed evidence

Suppose Bob discovers that the requested executive headline removes the condition on projected savings. Alice's example reply is: “Keep the condition visible in the headline or adjacent sentence. If the page budget cannot accommodate it, propose a different layout; do not publish an unconditional saving.” Resume with `/publish` or `$workflow-publish` using that bounded instruction, then review the revised rendering.

Continue the existing engagement where one is active, with its actual
identifiers and unresolved conditions. The example reply clarifies work;
it is not a signed L0 authority act. If the runtime requires such an act,
the authorized human must follow the exact instruction it emits through
the trusted authority path. Do not substitute conversational consent.

If review finds a table clipped in the PDF, use `/rework` or `$workflow-rework` with the visual finding and rerender the affected output where available. If the audience changes from internal management to customers, revisit confidentiality, claims and distribution scope before reusing the publication. A change of audience can invalidate an otherwise readable document.

## Know when to stop

Deliver a publication set tied to the actual semantic source, a review record and explicit renderer results. Mark unavailable visual or accessibility checks NOT_EXECUTED. AI editorial review, actual independent review and human publication authorization must remain distinct statuses throughout.

Use the **Enterprise publication** chain in the
[enterprise workflow catalogue](../reference/workflows.md) to check roles
and handoffs. Review and verification must remain separate from authoring;
a revised draft does not verify itself. The examples above have not been
executed as part of this guide, and their outcomes are not evidence.
