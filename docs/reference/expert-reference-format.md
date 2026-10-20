# Expert reference format

Owner: JAI maintainers · Last reviewed: 2026-10-20

Expert references are UTF-8 Markdown documents with YAML front matter.
The separate runtime schema is `content/schema/expert-reference.schema.json`;
this format does not alter Artifact Contract v3 or the DCS specification schema.

## Required metadata

| Field | Meaning |
| --- | --- |
| `reference_id` | Stable reference identifier, preserved for bundled documents. |
| `schema_version` | Literal string `1.0.0`. |
| `document_kind` | Supported reference family, for example `decision-paper`. |
| `complexity` | `simple`, `medium` or `complex`. |
| `language` | Currently `en`. |
| `classification` | `public-synthetic`, `internal`, `confidential` or `restricted`. |
| `provenance` | `ai-authored-proposed` or `user-supplied-proposed`. |
| `fictional_context` | Boolean identifying illustrative rather than actual context. |
| `applicable_dcs` | Preserved source binding, resolved through the registered mapping. |
| `approval_status` | `not-human-approved`; import cannot grant JAI L0 approval. |

A valid bundled example has metadata equivalent to:

```yaml
---
reference_id: example:decision-paper:medium
schema_version: '1.0.0'
document_kind: decision-paper
complexity: medium
language: en
classification: public-synthetic
provenance: ai-authored-proposed
fictional_context: true
applicable_dcs: kind/decision-paper
approval_status: not-human-approved
---
```

The body must also meet the checks below. This metadata snippet alone is not
a valid complete reference. Setting `approval_status: approved`, using a
string instead of a Boolean, or mismatching the selected family is invalid.
A plausible reference identifier does not establish authority.

The complete library also carries supported `content_revision`, `dcs_status`
and proposal-pack metadata where supplied. A proposed source binding may use
`proposed/kind/<family>` and `dcs-proposed-*` anchors. These declarations remain
proposed after import. The maintained
`content/expert-reference-bindings.json` maps reference families and source
anchors to actual registered JAI kinds and information units. Unknown or
inconsistent mappings fail; import cannot approve or activate a rule.

| Optional field | Meaning |
| --- | --- |
| `content_revision` | Supplied content revision, independent of the product version. |
| `dcs_status` | Source binding status; proposed values never grant approval. |
| `proposal_pack_id` | Synthetic pack association, not a customer engagement identity. |
| `target_audiences` | Explicit audience constraints for an override. |
| `applicability_context` | Explicit flat scalar constraints for reference selection. |
| `case_id` | Synthetic case association, never a real engagement or evidence identity. |
| `methodology_context` | Illustrative professional methods, not a compliance attestation. |

Bundled index entries also carry `review_version` and `review_status` for
the v2.3.0 editorial revision. These are manifest metadata, not required new
front-matter fields or an authority record. The recorded status is
`tri-lens-ai-review-applied-not-human-approved`. All three lenses used the
same AI system; neither this status nor a successful integrity check proves
independent human review. See the [review guide](../validation/expert-reference-review.md).

## Stable DCS anchors

Content sections identify DCS information units directly or through an
explicit registered mapping for preserved proposed anchors. Human-readable
headings and visual presentation may vary. Preserve the supplied anchor
syntax and identifiers when editing; consult the registered mapping rather
than inventing identifiers. Duplicate, missing, unknown and inconsistent anchors
are findings with the affected document and rule.

Validation distinguishes four levels:

1. Structural coverage: identifiers link sections to the required units.
2. Content presence and adequacy: empty or placeholder sections do not pass.
3. Evidence and rationale: deterministic diagnostics identify detectable
   unsupported material; unverified professional reasoning remains pending.
4. Professional acceptance: independent competent review and existing JAI
   authority are separate from automatic validation.

**An anchor identifies content; it does not prove its truth or correctness.**
Schema validation and plausible narrative cannot confer professional approval.
The bundled index records public synthetic reference identities and integrity
metadata; private overrides receive sanitized diagnostics.

## Validate a document

```bash
python3 .ai/runtime/tools/expert_references.py validate --root . \
  --source my-medium.md --kind decision-paper --complexity medium
```

See [override configuration](../configuration/expert-document-overrides.md)
for selection and restoration behavior.

## Registered family mappings

The reference family is a library slot; the document kind is the explicit
DCS selection. All new registrations remain proposed and advisory. Source
anchors are preserved and translated by the maintained binding map;
inherited global, type, domain and role obligations remain additional
authoring requirements. Reference coverage is not complete project approval.

| Reference family | Registered document kind | Registration |
| --- | --- | --- |
| `decision-paper` | `decision-paper` | Existing priority kind |
| `adr` | `adr` | Existing priority kind |
| `business-case` | `business-case` | Existing priority kind |
| `risk-assessment` | `risk-assessment` | Existing priority kind |
| `assurance-report` | `assurance-report` | Existing priority kind |
| `architecture-definition` | `architecture-definition` | Existing priority kind |
| `hld` | `hld` | Existing priority kind |
| `operational-handover` | `operational-handover` | Existing priority kind |
| `runbook` | `runbook` | Existing priority kind |
| `test-report` | `test-report` | Existing priority kind |
| `it-digital-strategy` | `strategy` | Proposed specialization |
| `requirements-specification` | `requirements-specification` | Proposed specialization |
| `policy-standard` | `policy-standard` | Proposed specialization |
| `implementation-specification-lld` | `implementation-specification` | Proposed specialization |
| `migration-cutover-plan` | `migration-cutover-plan` | Proposed specialization |
| `test-strategy-plan` | `test-strategy` | Proposed specialization |
| `operational-readiness-assessment` | `operational-readiness-assessment` | Proposed specialization |
| `service-design-sla` | `service-design` | Proposed specialization |
| `incident-postmortem` | `incident-postmortem` | Proposed specialization |
| `compliance-gap-analysis` | `compliance-gap-analysis` | Proposed specialization |
| `benefits-realisation-review` | `benefits-review` | Proposed specialization |
| `transformation-roadmap` | `roadmap` | Proposed specialization |
| `client-proposal` | `client-proposal` | Proposed specialization |
| `executive-proposal` | `executive-proposal` | Proposed specialization |
| `technical-proposal` | `technical-proposal` | Proposed specialization |
| `delivery-proposal` | `delivery-proposal` | Proposed specialization |
| `commercial-proposal` | `commercial-proposal` | Proposed specialization |
| `statement-of-work` | `statement-of-work` | Proposed specialization |
| `rfp-response` | `rfp-response` | Proposed specialization |
| `proposal-compliance-matrix` | `proposal-compliance-matrix` | Proposed specialization |
| `cybersecurity-transformation-proposal` | `cybersecurity-transformation-proposal` | Proposed specialization |
| `managed-security-services-proposal` | `managed-security-services-proposal` | Proposed specialization |
| `software-engineering-plan` | `software-engineering-plan` | Proposed specialization |
| `api-interface-contract` | `api-interface-contract` | Proposed specialization |
| `release-readiness-review` | `release-readiness-review` | Proposed specialization |
| `transformation-baseline-assessment` | `transformation-baseline-assessment` | Proposed specialization |
| `target-operating-model` | `target-operating-model` | Proposed specialization |
| `transformation-execution-plan` | `transformation-execution-plan` | Proposed specialization |
| `security-architecture-assessment` | `security-architecture-assessment` | Proposed specialization |
| `threat-model` | `threat-model` | Proposed specialization |
| `security-control-assessment` | `security-control-assessment` | Proposed specialization |
| `devsecops-pipeline-design` | `devsecops-pipeline-design` | Proposed specialization |
| `cicd-pipeline-assurance` | `cicd-pipeline-assurance` | Proposed specialization |
| `appsec-verification-report` | `appsec-verification-report` | Proposed specialization |
| `software-supply-chain-assessment` | `software-supply-chain-assessment` | Proposed specialization |

The 13 engineering, transformation and security additions preserve source
`proposed-not-mapped` declarations. JAI supplies explicit advisory mappings;
it does not rewrite those declarations into approval. Their standalone
`kind/<document-kind>` selectors are opt-in authoring blueprints, not new
obligations on existing role contracts or permission to perform security tests.
