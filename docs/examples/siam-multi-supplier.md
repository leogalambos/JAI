# Coordinate a service across several suppliers

Owner: JAI maintainers. Last reviewed: 2026-10-20.

This walkthrough illustrates the `siam-multi-supplier` workflow recipe.
It is not an additional native slash command.

ACME's employee portal depends on a hosting supplier, an identity supplier and an application supplier. Alice owns the end-to-end service and Bob coordinates supplier interfaces. Users experience one service even when each supplier reports that its own component is healthy.

These names and circumstances are fictional. They illustrate common public
operating practices, not an account of an actual ACME engagement.

## Prepare a project workspace

Create a new directory named `acme-supplier-service-integration/` with `input/`,
`working/` and `output/` subdirectories. Keep source material in `input/`;
use `working/` for drafts and `output/` for the reviewed handoff. These are
your chosen locations, not filenames JAI guarantees to generate.

Supply:

- service-map.md — end-to-end journeys and supplier boundaries
- supplier-obligations.md — supplied service levels, hours and escalation terms
- handoff-records.csv — anonymized incident transfers and elapsed times
- integration-brief.md — service owner, intended improvements and constraints

Add `PROJECT.md` with the question, accountable owner, scope exclusions and
confidentiality constraints. Do not fabricate missing records. List absent
inputs and ask the relevant owner for them; narrow the conclusion while
they remain unavailable.

## Run this scenario in the provider CLI

Install the appropriate JAI adapter using the [installation guide](../getting-started/install.md).
Start Claude Code or Codex in the new project directory. The prompts below
are conversational inputs to that provider, not shell commands. Choose
one provider column and continue in the same project conversation.

Use analysis to locate interface gaps, then the layered path to design a bounded service-integration improvement. Review the proposed operating agreement against actual supplied obligations. JAI cannot amend a supplier contract or appoint an accountable service owner.

The command pairs are equivalent entry points; they do not imply identical
provider tools. Ask JAI to report actual output paths and any engagement,
snapshot or findings identifiers. Read those results before proceeding. Replace `<reported-review-target>`
with the actual draft path reported by the preceding stage.
In a rework prompt, replace `<reported-ledger>` with the ledger the review
actually reported. Never invent its identifier or erase open findings.

### 1. Map the customer journey and handoffs

=== "Claude Code"

    ```text
    /analyse input/ for employee-portal service integration. Identify ownership gaps between hosting, identity and application suppliers, using actual handoff records.
    ```

=== "Codex CLI"

    ```text
    $workflow-analyse input/ for employee-portal service integration. Identify ownership gaps between hosting, identity and application suppliers, using actual handoff records.
    ```

Inspect whether the map follows a user login through every dependency. Separate measured transfer delays from opinions about supplier performance. If incident clocks use different time zones or pause rules, reconcile them before comparing elapsed times or blaming one supplier.

### 2. Frame the operating improvement

=== "Claude Code"

    ```text
    /layered Prepare a bounded service-integration proposal for incident coordination, shared observations and escalation. Preserve contractual boundaries and identify changes requiring negotiation.
    ```

=== "Codex CLI"

    ```text
    $workflow-layered Prepare a bounded service-integration proposal for incident coordination, shared observations and escalation. Preserve contractual boundaries and identify changes requiring negotiation.
    ```

Check whether one person coordinates the end-to-end incident without pretending to own every supplier's technology. A proposed shared bridge needs participation hours and a fallback when a supplier cannot join. Do not describe a suggested handoff time as an existing contractual commitment.

### 3. Agree review criteria

=== "Claude Code"

    ```text
    /criteria .
    ```

=== "Codex CLI"

    ```text
    $workflow-criteria .
    ```

This displays or initializes the project criteria. Then ask:

> Set review criteria for the proposed multi-supplier operating model: accountability, contactability, evidence exchange, boundary ownership and contractual consistency.

Confirm the criteria shown by review before allowing assessment to start.

Read the criteria against the actual employee service hours. A sequence that waits for a supplier's next business day cannot support an immediate restoration commitment. Decide what minimal sanitized evidence suppliers need to exchange without exposing unrelated customer information.

### 4. Review the proposed agreement

=== "Claude Code"

    ```text
    /review <reported-review-target> the integration proposal against the supplied obligations and fixed criteria. Locate ambiguous ownership, conflicting clocks and unsupported performance claims.
    ```

=== "Codex CLI"

    ```text
    $workflow-review <reported-review-target> the integration proposal against the supplied obligations and fixed criteria. Locate ambiguous ownership, conflicting clocks and unsupported performance claims.
    ```

Inspect examples of a failed login and an infrastructure alarm. Each should identify who coordinates, who investigates and who confirms restoration to the user. If no party can observe the whole journey, retain the gap instead of drawing a dashboard that does not exist.

### 5. Rework and prepare negotiation handoff

=== "Claude Code"

    ```text
    /rework <reported-ledger> Rework open integration findings and prepare a proposed supplier discussion pack under output/. Keep unagreed responsibilities and service levels explicitly proposed.
    ```

=== "Codex CLI"

    ```text
    $workflow-rework <reported-ledger> Rework open integration findings and prepare a proposed supplier discussion pack under output/. Keep unagreed responsibilities and service levels explicitly proposed.
    ```

Read the pack from each supplier's boundary as well as ACME's. A useful draft makes disagreements visible enough to negotiate. Record actual supplier responses separately; the agent's reconstruction of a likely response is not evidence that a supplier accepted the model.

## Handle an escalation or changed evidence

Suppose the identity supplier does not provide support during ACME's overnight operations. Alice's example reply is: “Prepare limited overnight service options and a contract-change request. Do not promise round-the-clock recovery while that support gap remains.” Resume with `/layered` or `$workflow-layered` to compare service limits, retained capability and supplier negotiation. This keeps the business decision visible rather than hiding it in a contact matrix.

Continue the existing engagement where one is active, with its actual
identifiers and unresolved conditions. The example reply clarifies work;
it is not a signed L0 authority act. If the runtime requires such an act,
the authorized human must follow the exact instruction it emits through
the trusted authority path. Do not substitute conversational consent.

If review finds inconsistent severity definitions across suppliers, use `/rework` or `$workflow-rework` to propose an explicit mapping and retain disputed cases. If procurement asks to consolidate all suppliers, open a separate sourcing decision before changing the integration scope. Operating-model review does not establish a supplier-selection outcome.

## Know when to stop

Finish with an end-to-end responsibility map, proposed operating agreement, located contractual gaps and a negotiation register. Treat shared dashboards, exercises and supplier acceptances as NOT_EXECUTED or pending unless actual evidence is supplied. Improvement targets remain targets until measured service results establish progress.

Use the **SIAM and multi-supplier service integration** chain in the
[enterprise workflow catalogue](../reference/workflows.md) to check roles
and handoffs. Review and verification must remain separate from authoring;
a revised draft does not verify itself. The examples above have not been
executed as part of this guide, and their outcomes are not evidence.
