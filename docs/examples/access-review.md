# Review access to a business service

Owner: JAI maintainers. Last reviewed: 2026-10-20.

This walkthrough illustrates the `access-request-to-review` workflow recipe.
It is not an additional native slash command.

ACME reviews access to its purchasing service before a periodic control review. Alice is the service owner and Bob administers identity groups. The work is an evidence-based access assessment; it does not authorize JAI to remove accounts or certify that all activity was legitimate.

These names and circumstances are fictional. They illustrate common public
operating practices, not an account of an actual ACME engagement.

## Prepare a project workspace

Create a new directory named `acme-access-review/` with `input/`,
`working/` and `output/` subdirectories. Keep source material in `input/`;
use `working/` for drafts and `output/` for the reviewed handoff. These are
your chosen locations, not filenames JAI guarantees to generate.

Supply:

- access-export.csv — accounts, roles, groups and extraction date
- joiner-mover-leaver.csv — authorized employment or supplier status snapshot
- role-rules.md — permitted duties and incompatible role combinations
- review-scope.md — systems, period, reviewers and sensitive-data handling

Add `PROJECT.md` with the question, accountable owner, scope exclusions and
confidentiality constraints. Do not fabricate missing records. List absent
inputs and ask the relevant owner for them; narrow the conclusion while
they remain unavailable.

## Run this scenario in the provider CLI

Install the appropriate JAI adapter using the [installation guide](../getting-started/install.md).
Start Claude Code or Codex in the new project directory. The prompts below
are conversational inputs to that provider, not shell commands. Choose
one provider column and continue in the same project conversation.

Use the assessment sequence to compare evidence with agreed rules. A material exception or remediation decision should use the layered path. The agent may identify a suspected conflict; the accountable reviewer decides whether the access remains justified.

The command pairs are equivalent entry points; they do not imply identical
provider tools. Ask JAI to report actual output paths and any engagement,
snapshot or findings identifiers. Read those results before proceeding.
Replace `<reported-review-target>` with the actual access-population input
path you selected for review; analysis and criteria creation do not produce
an assessment draft automatically.
In a rework prompt, replace `<reported-ledger>` with the ledger the review
actually reported. Never invent its identifier or erase open findings.

### 1. Check the review population

=== "Claude Code"

    ```text
    /analyse input/ for the purchasing-service access review. Identify population gaps, extraction dates and identifiers that cannot be reconciled. Keep personal data within this project.
    ```

=== "Codex CLI"

    ```text
    $workflow-analyse input/ for the purchasing-service access review. Identify population gaps, extraction dates and identifiers that cannot be reconciled. Keep personal data within this project.
    ```

Inspect whether service accounts, privileged groups and indirect memberships are represented. An export of direct application roles may omit privileges inherited from a directory group. Ask Bob for the missing export rather than letting an apparently empty comparison imply that no elevated access exists.

### 2. Fix the comparison rules

=== "Claude Code"

    ```text
    /criteria .
    ```

=== "Codex CLI"

    ```text
    $workflow-criteria .
    ```

This displays or initializes the project criteria. Then ask:

> Set access-review criteria from input/role-rules.md and input/review-scope.md. Separate factual reconciliation from business-owner decisions and formal approval.

Confirm the criteria shown by review before allowing assessment to start.

Review how stale accounts, privileged access and incompatible duties will be assessed. A manager name in an export is not proof that a current review occurred. Define which evidence is enough to resolve an identity mismatch and which exceptions need an accountable human response.

### 3. Review the evidence

=== "Claude Code"

    ```text
    /review <reported-review-target> the access population against the fixed criteria. Locate each exception by a safe internal identifier and cite the supporting records. Do not change access.
    ```

=== "Codex CLI"

    ```text
    $workflow-review <reported-review-target> the access population against the fixed criteria. Locate each exception by a safe internal identifier and cite the supporting records. Do not change access.
    ```

Inspect several exception rows yourself. A missing employment match could indicate a supplier identity, a changed identifier or a real leaver account. Keep those alternatives visible until confirmed. Avoid copying personal details into general examples or a public report.

### 4. Resolve a disputed exception

=== "Claude Code"

    ```text
    /layered Prepare the decision on the purchasing service's conflicting requester and approver roles. Include the service owner's rationale, alternatives and missing transaction evidence.
    ```

=== "Codex CLI"

    ```text
    $workflow-layered Prepare the decision on the purchasing service's conflicting requester and approver roles. Include the service owner's rationale, alternatives and missing transaction evidence.
    ```

Check whether the decision distinguishes a technical role combination from demonstrated misuse. Compensating controls need actual owners and evidence; a proposed monthly check is not an operating control. The resulting packet should allow Alice to accept, reject or ask for stronger controls.

### 5. Rework and prepare the review record

=== "Claude Code"

    ```text
    /rework <reported-ledger> Rework the open access-review findings using the supplied owner responses. Preserve unresolved exceptions and prepare a proposed review record under output/.
    ```

=== "Codex CLI"

    ```text
    $workflow-rework <reported-ledger> Rework the open access-review findings using the supplied owner responses. Preserve unresolved exceptions and prepare a proposed review record under output/.
    ```

Inspect whether owner responses actually answer each exception. 'Still needed' without purpose, scope or expiry is weak evidence. Keep a separate action for Bob to execute any approved entitlement changes and obtain a fresh export afterward; the report itself does not revoke access.

## Handle an escalation or changed evidence

Suppose Alice wants one employee to retain both purchasing roles during a vacancy. Her example reply is: “Record this as an exception request for two weeks. Ask finance to identify a separate transaction checker; until that control is evidenced, do not mark the conflict resolved.” Resume with `/layered` or `$workflow-layered` to evaluate that bounded exception. The agent must not manufacture an independent reviewer or infer formal acceptance from the conversational reply.

Continue the existing engagement where one is active, with its actual
identifiers and unresolved conditions. The example reply clarifies work;
it is not a signed L0 authority act. If the runtime requires such an act,
the authorized human must follow the exact instruction it emits through
the trusted authority path. Do not substitute conversational consent.

If the reviewer finds that indirect group membership was omitted, use `/rework` or `$workflow-rework` after Bob supplies the export. If scope expands to all corporate systems, revise the review scope and population through `/criteria` or `$workflow-criteria` before restarting review. A purchasing-service sample cannot stand in for an enterprise certification.

## Know when to stop

Deliver a reconciled population, located exceptions, owner responses, evidence limitations and a proposed action register. Mark entitlement changes and post-change checks NOT_EXECUTED until actual records exist. Human certification, if required, remains a separate act by the named accountable person.

Use the **Access review** chain in the
[enterprise workflow catalogue](../reference/workflows.md) to check roles
and handoffs. Review and verification must remain separate from authoring;
a revised draft does not verify itself. The examples above have not been
executed as part of this guide, and their outcomes are not evidence.
