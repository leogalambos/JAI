# Governance, policy and approvals

AI IT House {{ JAI_VERSION }} uses layered enforcement. Prompt text may reinforce expected behavior, but the high-value controls are intended to sit in data contracts, tool permissions, provider adapters, deterministic validators and human authority boundaries.

## Enforcement order

<div class="ai-diagram ai-diagram-inline" role="img" aria-label="Architecture and delivery diagram">
<img src="../../assets/diagrams/policy-enforcement.svg" alt="Enterprise policy through sandbox, agent permissions, tool allowlist, managed hooks and prompt instructions">
</div>

The intended precedence is:

```text
Enterprise policy
→ sandbox / host controls
→ agent permission set
→ MCP / tool allowlist
→ managed hooks
→ prompt instructions
```

A prompt is the weakest enforcement tier in that chain.

## JAI policy responsibilities

Gen2 organises policy work through the six SABSA content perspectives:
**L1 Contextual**, **L2 Conceptual**, **L3 Logical**, **L4 Physical**,
**L5 Component** and **L6 Management**. Each addresses What, Why, How, Who,
Where and When at its own level. See the
[canonical layer model](../architecture/sabsa-layer-model.md).

Within each perspective, the local setter establishes criteria and evidence
obligations, the author proposes an answer, and an independent reviewer assesses
that answer. Policy constraints, exceptions, escalation and execution evidence
are handled wherever they apply; they are not exclusive responsibilities of
L3 or L6. L5 Component covers implementation detail. L6 Management covers
governance, assurance and operation, with management concerns applying across
the other perspectives.

**L0** remains the external human authority for reserved consequential
acceptance, exception and revision decisions. A local review does not grant
that authority.

## High-value operating rules

The packaged policy is designed to uphold these principles:

- reviewers do not edit the artefact they are approving;
- authors do not self-approve;
- policy mutation requires controlled approval;
- restricted provider/MCP capabilities should not be bypassed through shell indirection;
- high-consequence authority actions remain human-controlled;
- publication separates semantic ownership, evidence/rationale review, publication editing, visual review and final authority;
- layered rework/reformulation/escalation follows deterministic bounds rather than model-selected retry loops.

## Human authority acts

Examples include:

- accepting a risk instead of fixing it;
- granting a time-bounded exception;
- approving a protected library change;
- accepting a consequential final L1 product;
- choosing `revise`, `reject` or `terminate` for an escalated engagement.

These decisions are not ordinary model outputs. See [Human authority and escalation](../operations/human-authority.md).

## Authority-hook behavior

`guard_authority.py` is an additional string-level denial guard. Neither Claude nor Codex native approval is a Fabric L0 credential. The human signs the exact request externally; Fabric validates its Ed25519 receipt, protected public pin and unchanged state. See [operator actions](../operations/operator-walkthrough.md).

In non-interactive modes that would hide the approval question, authority acts are denied.

## Security boundary of hooks

Managed hooks are useful enforcement but are not the whole sandbox. The authority hook itself describes its protection as a string-level guard. Deployments with stronger threat models should enforce the same rules through operating-system/container permissions, restricted credentials and network controls.

## Data classification and network behavior

The managed policy declares network restrictions; actual enforcement depends on the effective native sandbox and host controls, not this declaration alone. Organisations must adapt classification, network, evidence-retention and provider-use rules for their environment.

## Implementation details

[Tool hooks, runtime controls and release gates](hooks-gates-verification.md) describes the inspected implementation.
Distinguish procedural routing, interactive hooks, semantic validation and release qualification.
