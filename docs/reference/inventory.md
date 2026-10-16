---
owner: JAI documentation maintainers
review_due: 2027-01-16
---

# Release inventory

This inventory is rendered from the canonical release manifest at `.ai/runtime/_meta/release-manifest.json` in the source checkout. Counts and agent identifiers are generated together during the documentation build; they are not a separately maintained catalogue. An installed runtime places the corresponding manifest under `~/.ai/it-role-house/_meta/`.

{{ JAI_RELEASE_INVENTORY }}

## How to interpret the inventory

**Agents** are the behavioural/operator definitions shipped by JAI, including specialised coordinators and reviewers. They are distinct from **business roles**, which describe enterprise responsibilities and are selected through role-category skills. A listed agent is not evidence that a provider has instantiated it or qualified its isolation controls.

The qualification-check count identifies checks registered in the release manifest. It is not the total number of unit-test cases, individual assertions, provider executions or passed deployment gates. Source availability and generated configuration likewise do not establish live qualification; consult the [commercial implementation matrix](../capabilities/commercial-delivery-implementation.md) and [validation controls](../operations/validation.md) for those boundaries.

For responsibilities and role selection, use [Roles and disciplines](../using/roles.md) and the [full role catalogue](roles.md). Source behavioural contracts are under `.ai/agents/`; their installed equivalents are under `~/.ai/it-role-house/agents/`. The [agent contract reference](runtime-tools-detailed.md#agent-contract-reference) explains contract/tool-tier concepts and explicitly marks its earlier-release illustrative subset. Current canonical contracts and provider configuration determine effective permissions.

Start with [How to use JAI](../examples/how-to-use-JAI/index.md) for method selection and complete worked cases; use this page for package inventory lookup.
