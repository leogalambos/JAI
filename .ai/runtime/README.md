# AI IT House runtime

This directory is the provider-neutral common runtime for AI IT House.
Canonical roles, schemas, policies and workflows are shared by Claude
Code and Codex adapters.

<!-- GENERATED-INVENTORY:START -->
## Current generated release inventory

This block is generated from canonical package sources by
`.ai/runtime/tools/generate_docs.py`. Manual count edits are not
authoritative.

- Roles: **286**
- Agents: **34**
- Skills: **24**
- Workflows: **24**
- Artifact Types: **28**
- Schemas: **33**
- Renderers: **4**
- Tests: **32**
- Provider Adapters: **2**

### Compatibility matrix

- **Claude Code**
  - Minimum: provider-supported
  - Tested: adapter contract
  - Supported: yes
- **Codex CLI**
  - Minimum: provider-supported
  - Tested: adapter contract
  - Supported: yes
- **Python**
  - Minimum: 3.10
  - Tested: 3.12 release CI target
  - Supported: yes
- **Pandoc**
  - Minimum: optional
  - Tested: publication tool detects at runtime
  - Supported: optional
- **LibreOffice**
  - Minimum: optional
  - Tested: publication tool detects at runtime
  - Supported: publication
- **lxml**
  - Minimum: 5.x
  - Tested: XSD conformance suite
  - Supported: EA conformance
- **jsonschema**
  - Minimum: 4.x
  - Tested: Draft 2020-12
  - Supported: semantic schemas
- **Pillow**
  - Minimum: runtime-supported
  - Tested: visual QA fixture rendering
  - Supported: visual QA
- **GitHub Actions**
  - Minimum: release workflow
  - Tested: tag, A-H gates, ZIP SHA-256, CI publication
  - Supported: automatic release publication
<!-- GENERATED-INVENTORY:END -->

## Runtime contract

The runtime treats skills as knowledge/capability and agents as
authority/execution boundaries. Production correctness is enforced by
contracts, schemas, managed policy and tests rather than prompt wording
alone.

Artifact Contract v3/JAI binds each governed deliverable to its artifact
type, schema, required evidence and relations,
producer/reviewer/approver roles, renderer or external handoff,
acceptance profile and lifecycle.

## Provider and model abstraction

Canonical agent frontmatter uses `model_class`. The effective provider
selector is resolved by `tools/model_router.py` from
`models/model-registry.json` plus an optional organisation/user
override. The base classes are `light`, `standard`, `heavy` and
`research`; the registry can add classes without rewriting role
semantics.

Installed Claude agents receive native selectors produced by the Claude
adapter. Codex receives project-managed model plus reasoning settings
for each workload class, with an ordered fallback chain ending in the
active host/session model. The strategy labels are AI IT House policy
values, not provider-native API enums.

## Release and operational policy

- Root `VERSION` is the sole current-product version authority.
  Run `python3 scripts/versioning.py sync` after changing it.
  The release tag must match the committed `VERSION`.
- `release/release-policy.json` defines `YY.MM.VV`, the first production
  release, required A–H gates and automatic tag-triggered publication
  policy.
- `operations/service-levels.json` defines measurable GA service
  objectives, an error-budget policy and a non-contractual reference
  support SLA for deploying organisations.
- `schema/schema-registry.json` resolves the active versioned contracts;
  Historical schema namespaces remain intact, including
  `schema/26.10.4/`.

## Validation

From the package root:

```sh
python3 .ai/runtime/tools/release_ga.py qualify
```

All A–H gates must pass. Gate G qualifies the behavioral harness and
golden enterprise corpus without claiming that a mutable external model
has passed; provider/model qualification is captured separately with a
typed evidence manifest. Gate H validates digest provenance and
readiness for automated CI publication. `release_bundle.py` creates a
distribution ZIP and its SHA-256 checksum. GitHub Actions publishes the
release after successful checks. Eligible repositories also receive
a keyless OIDC-signed attestation.

## Workflows and publication

The workflow catalogue spans demand/funding, design/delivery,
onboarding, change, cyber recovery, security remediation, data/AI,
sourcing/SIAM, migration/cutover, operational readiness, adoption,
resilience, enterprise release, regulatory assurance, architecture
publication and retirement. Publication is projected from the canonical
semantic layer and visually checked after rendering.

## Auditability

Significant executions can be recorded as immutable Execution Records
including provider, resolved model, agent, skills, source hashes,
policies, approvals, external calls, outputs and
semantic/projection/render hashes. This supports audit, incident
analysis and reproducibility.
