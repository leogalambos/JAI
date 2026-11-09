# Semantic artefact to enterprise publication

`workflow: semantic-to-enterprise-publication`  ·  `steps: 5`  ·  `tool-tier: route`

**Trigger.** A specialist artefact is substantively complete and requires enterprise-grade publication.

**Outcome.** A released audience-specific publication whose semantic content is traceable to the approved source and has passed semantic and publication gates.

## Chain

| # | Role | Does | Hands over | Gate before the hand-off |
| --- | --- | --- | --- | --- |
| 1 | Owning specialist | finalises claims, decisions, assumptions, evidence and acceptance criteria | semantic publication model | Semantic source is complete enough to review; unresolved items are explicit |
| 2 | Evidence & Rationale Reviewer | checks evidence strength, assumptions, alternatives, rationale and residual risk | semantic gate result and located findings | Semantic Gate PASS and the exact stable semantic snapshot has its required source approval under the governing profile, including verified external human proof where required, before the editor acts; only an existing expressly permitted prior scoped waiver applies, and mandatory controls remain blocking |
| 3 | Enterprise Publication Editor | selects the publication archetype and renders audience-specific DOCX/PPTX/XLSX/HTML/SVG outputs from the exact approved semantic snapshot | rendered publication set with semantic hash | All outputs carry the same semantic SHA-256 and required document control; draft rendering grants no acceptance or release |
| 4 | Visual Quality Reviewer | checks density, hierarchy, legibility, tables, diagrams, document control and package integrity | publication gate result and findings | Publication Gate PASS with blocking defects resolved; any policy-permitted waiver requires prior named human authority for its exact scope before release or other gated effects; mandatory controls remain blocking |
| 5 | Named authority | reviews completed semantic, publication and actual visual evidence and records the human release decision | release approval | Explicit exact human approval precedes release; required independence is preserved; agents cannot approve or issue waivers |

## Operating this chain

The truth layer remains authoritative throughout. Publication roles may change layout, hierarchy and visual representation but may not silently add or alter material facts, decisions, risk acceptance or evidence statements.

Preparatory work is limited to its explicitly permitted scope. Named human approval must precede every effect it authorises; neither a role title nor a later review supplies authority retrospectively. All policy-required pre-approval evidence remains mandatory. Collect candidate evidence only within explicitly permitted pre-production scope. If policy requires operational proof, obtain a separate prior named human approval for the bounded pilot needed to collect it, then seek the wider approval; no pilot permission is implied. If no governing route permits the required evidence collection, stop and consult the accountable authority before proceeding. Any policy-permitted waiver must already be issued by the competent named human authority for the exact gate, scope and validity period before the gated action; non-waivable controls remain blocking.

Semantic-source approval precedes publication editing and is distinct from the final publication-release decision after visual review. Professional Semantic Gate PASS does not itself supply human approval. Preparatory draft work may use only an existing separately permitted route; it cannot bypass the editor's approved-source precondition.

<!-- BEGIN workflow-applicability -->
## Context and mechanism applicability

Use the actual bounded request, current environment and decision rights to select one applicable mechanism variant. Unknown applicability remains pending; the routing record grants no authority.

**Invariant outcomes:**

- A released audience-specific publication whose semantic content is traceable to the approved source and has passed semantic and publication gates.
- Retain source-version traceability, accountable receiving duties and every applicable existing gate.

| Context | Mechanisms | Required evidence |
| --- | --- | --- |
| draft | Render a clearly labelled draft without granting acceptance or release | Exact semantic binding, draft status and disclosed limitations |
| release-candidate | Require applicable semantic/source and publication gates before effects | Independent review, resolved blocking defects and exact human release decision |

Return meaning changes to the semantic owner and rendition defects to the publication owner; preserve exact findings. Stop editing/release when mandatory source approval, disclosure or publication gates are missing. Release only the exact permitted package/audience after human decision, or retain an explicitly unapproved draft. Mechanism selection is not a waiver of security, legal or acceptance obligations.

**Entry information (selected once per actual context version):**

- Exact semantic source and intended audience
- Disclosure/classification constraints
- Required review, source approval and publication formats

Select intake and mechanism variant once per actual context version. Carry the reviewed record by versioned evidence reference. Reuse unchanged evidence; recheck mutable prerequisites only at the action they govern. A new context version requires its own relevant review, not reconstruction of historical work.

**Continuation, rework, stop and exit:**

- **continue** — The current handoff criteria and applicable prerequisites are satisfied. Continue to the registered receiving duty with exact output and evidence references.
- **rework** — A current criterion fails or required information changes. Return meaning changes to the semantic owner and rendition defects to the publication owner; preserve exact findings.
- **stop** — An applicable authority, legal, safety or mandatory-control boundary forbids the effect. Stop editing/release when mandatory source approval, disclosure or publication gates are missing.
- **exit** — The bounded outcome is accepted or the entitled owner rejects, cancels or defers the scope. Release only the exact permitted package/audience after human decision, or retain an explicitly unapproved draft.

**Bounded paths and scope:**

Drafts terminate at rendering and cannot enter a release-approval route; release candidates retain all applicable gates.

| Selected path | Applicable stages | Terminal stage |
| --- | --- | ---: |
| draft | 1, 2, 3 | 3 |
| release-candidate | 1, 2, 3, 4, 5 | 5 |

A path with a separate mechanism requires that explicit mechanism selection in the versioned intake record. Unknown selection remains pending. Later out-of-scope stages cannot claim acceptance; a terminal exit still needs the registered exact-scope authority.
<!-- END workflow-applicability -->
