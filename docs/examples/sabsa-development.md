# Develop a SABSA security architecture

Owner: JAI documentation maintainers. Updated: 2026-10-20.

ACME Distribution is opening an online ordering channel. Alice sponsors
the business service, Bob operates the warehouse systems, and John Doe
coordinates security architecture. This illustrative fiction uses a
common retail problem: orders must remain trustworthy and the service
must recover from disruption. It does not supply real risks, accepted
controls or measured resilience.

The task is to build a traceable security architecture, not to choose a
catalogue of products. A useful library connects business purposes and
attributes to risks, control objectives, services and operating
measures. The [SABSA workflow](../capabilities/sabsa-ea.md) provides the
domain path.

## Prepare the project

Create `acme-sabsa/` containing `inputs/`, `working/` and `output/`.
Collect the business plan, service description, process maps,
information classification, dependency inventory and existing security
policies in `inputs/`. Add available incident history, continuity
requirements and interviews identifying accountable business owners.
Keep factual documents separate from workshop ideas.

Useful names include `inputs/business-drivers.md`,
`inputs/order-process.pdf`, `inputs/dependencies.csv` and
`inputs/known-controls.md`. A missing recovery objective is a business
question, not permission to invent a convenient number. Record gaps,
document dates and authority in `inputs/source-register.md`.

After [installation](../getting-started/install.md), start Claude Code
or Codex in `acme-sabsa/`. Confirm JAI is available before entering the
following conversation instructions. They are not shell commands.

## Run this scenario in the provider CLI

Use the direct SABSA workflow for an architecture library. Introduce
layered delivery when a consequential decision needs the six-layer
evidence and authority path; the SABSA architectural layers are not the
JAI L1–L6 execution layers.

### 1. Prepare sources before designing controls

=== "Claude Code"

    ```text
    /sabsa prepare working/security-library using inputs/ for the online
    ordering service. Identify source gaps and business owners.
    ```

=== "Codex CLI"

    ```text
    $workflow-sabsa prepare working/security-library using inputs/ for the
    online ordering service. Identify source gaps and business owners.
    ```

Inspect the prepared source area and inventory, including the workflow's
`00-sources` convention. Check that received facts retain their origins
and that workshop assumptions are recognisable. Preparation does not
mean every source has been accepted as current or authoritative.

### 2. Build from business drivers

=== "Claude Code"

    ```text
    /sabsa create working/security-library from the prepared sources.
    Trace online-ordering drivers through attributes, risks and control
    objectives; leave unsupported values pending.
    ```

=== "Codex CLI"

    ```text
    $workflow-sabsa create working/security-library from the prepared sources.
    Trace online-ordering drivers through attributes, risks and control
    objectives; leave unsupported values pending.
    ```

Read the resulting entries from the business layer downward. A proposed
attribute such as availability needs a business owner and an observable
meaning. Inspect whether a logical security service addresses a control
objective before discussing its physical product implementation.
Examples in bundled references provide structure, not ACME evidence.

### 3. Review completeness and meaning separately

=== "Claude Code"

    ```text
    /sabsa review working/security-library for upward traceability,
    measurable attributes, ownership and unsupported security claims.
    ```

=== "Codex CLI"

    ```text
    $workflow-sabsa review working/security-library for upward traceability,
    measurable attributes, ownership and unsupported security claims.
    ```

The independent reviewer should record located findings rather than edit
the design. Inspect both broken links and substantive questions: a
syntactically valid control can still address the wrong risk. Read
coverage findings as gaps to resolve, not proof that a service is
secure.

### 4. Resolve a business conflict explicitly

Suppose sales requests uninterrupted ordering while operations says the
warehouse integration has no failover. John Doe cannot accept the
business risk merely by choosing a shorter outage target. Alice's
illustrative reply is: "Prepare the cost and service-impact options;
keep the continuity target pending until the service owner decides."

=== "Claude Code"

    ```text
    /layered Resolve the continuity conflict recorded in
    working/security-library. Compare degraded operation and integration
    resilience using inputs/; preserve the pending business decision.
    ```

=== "Codex CLI"

    ```text
    $workflow-layered Resolve the continuity conflict recorded in
    working/security-library. Compare degraded operation and integration
    resilience using inputs/; preserve the pending business decision.
    ```

Inspect the conflict, alternatives, evidence limitations and named human
authority. L0 is external to the six execution layers. If a protected
authority action is required, the human uses the exact command emitted
by the runtime; a chat reply must not be converted into a fabricated
act.

### 5. Update only after the decision is available

=== "Claude Code"

    ```text
    /sabsa update <affected-entry-id> working/security-library using the
    recorded continuity decision. Preserve stable identifiers and request
    independent review of the changed traceability.
    ```

=== "Codex CLI"

    ```text
    $workflow-sabsa update <affected-entry-id> working/security-library using
    the recorded continuity decision. Preserve stable identifiers and request
    independent review of the changed traceability.
    ```

Replace `<affected-entry-id>` with a concrete identifier observed in the
library; repeat for each affected entry instead of inventing an ID.
Inspect the changes and review findings before treating the library as a
baseline. If the business channel changes to include a marketplace
partner, register that new source and reassess affected trust, ownership
and operational measures.

## Finish and hand off

Hand over the architecture library, source register, traceability and
unresolved decisions to the security and service owners. State which
entries remain proposed and which decisions have actual human evidence.
A library review is not penetration testing or operational acceptance.
Publish audience-specific documents only from the appropriately reviewed
semantic material.
