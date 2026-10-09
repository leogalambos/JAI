{{! ===================================================================================================
    Default SABSA architecture document. To change it for one library:   sabsa.py template LIB --init
    then edit LIB/templates/architecture.md. For all your libraries, put it in ~/.ai/sabsa-templates/.
    Every field this template can use is listed by:   sabsa.py template LIB --fields
    Syntax is a Mustache subset - see the sabsa-library skill, references/templates.md.
    (A comment like this one must not contain double braces: it ends at the first pair.)
    =================================================================================================== }}
# {{library.name}}

**Security architecture — {{library.organisation}}**

{{#draft}}
> **DRAFT.** This architecture is not releasable. {{#has_errors}}It has {{counts.errors}} consistency error(s). {{/has_errors}}{{#has_warnings}}It has {{counts.warnings}} unresolved warning(s)/assumption(s). {{/has_warnings}}{{open_cells}} of 36 matrix questions are not yet settled. Approval gate: {{approval_reason}}.
{{/draft}}

| | |
| --- | --- |
| Organisation | {{library.organisation}} |
| Scope | {{library.scope}} |
| Owner | {{library.owner}} |
| Version | {{library.version}} ({{library.status}}) |
| Generated | {{generated}} |
| Approval | {{#approved}}APPROVED — {{approval.approved_by}} at {{approval.approved_at}}{{/approved}}{{^approved}}NOT APPROVED — {{approval_reason}}{{/approved}} |

## 1. Executive summary

{{#library.summary}}{{library.summary}}{{/library.summary}}
{{^library.summary}}_To be written: the purpose of this architecture, the main business drivers it serves, and the decisions it asks for. Write it in the body of `library.md`._{{/library.summary}}

## 2. Scope and approach

This architecture covers **{{library.scope}}** for {{library.organisation}}. It follows the SABSA method: security
requirements are derived from business drivers, expressed as measurable business attributes, and carried through
six layers — from the business's own view down to the components — with each layer answering six questions:
what, why, how, who, where and when. Every element traces upward to a business driver, so nothing is included
without a business reason.

## 3. Basis of this document

Of {{counts.elements}} architecture elements, **{{basis.stated}}** are stated by {{library.organisation}},
**{{basis.inferred}}** are inferred from the material below, and **{{basis.assumed}}** are assumptions awaiting
confirmation (section 13){{#basis.unstated}}; {{basis.unstated}} do not yet state their basis{{/basis.unstated}}.

| Source | Cited by |
| --- | --- |
{{#sources}}
| {{file}} | {{cited_by}} |
{{/sources}}
{{^sources}}
| _No source material recorded yet_ | |
{{/sources}}

{{#layers}}
## {{section}}. {{name}} layer — {{view}}

This layer describes {{purpose}}.

{{#cells}}
### {{interrogative}} — {{column}}

**{{question}}**

{{#answered}}
{{answer}}

_Basis: {{basis}} · Source: {{source}}_
{{/answered}}
{{#not_applicable}}
_Not applicable: {{reason}}_
{{/not_applicable}}
{{#open}}
> _Not yet answered._ {{guidance}}
{{/open}}

{{#has_elements}}
| ID | Element | Description | Basis |
| --- | --- | --- | --- |
{{#elements}}
| {{id}} | {{title}} | {{summary}} | {{basis}} |
{{/elements}}

{{/has_elements}}
{{/cells}}
{{/layers}}
## 10. Business attribute profile

| ID | Attribute | Definition | Metric | Measurement | Target | Owner | Drivers |
| --- | --- | --- | --- | --- | --- | --- | --- |
{{#attributes}}
| {{id}} | {{title}} | {{definition}} | {{metric}} | {{measurement}} | {{target}} | {{owner}} | {{drivers}} |
{{/attributes}}

## 11. Traceability — from component to business driver

{{#has_traceability}}
| Component | Mechanism | Service | Control objective | Attribute | Driver |
| --- | --- | --- | --- | --- | --- |
{{#traceability}}
| {{component}} | {{mechanism}} | {{service}} | {{objective}} | {{attribute}} | {{driver}} |
{{/traceability}}
{{/has_traceability}}
{{^has_traceability}}
_No components defined yet, so there is no end-to-end chain to show._
{{/has_traceability}}

## 12. The SABSA matrix at a glance

✓ answered · n/a not applicable · · open — the number is how many elements sit in the cell.

| Layer | What | Why | How | Who | Where | When |
| --- | --- | --- | --- | --- | --- | --- |
{{#matrix}}
| {{name}} |{{#marks}} {{mark}}{{#count}} {{count}}{{/count}} |{{/marks}}
{{/matrix}}

## 13. Open assumptions — questions for {{library.organisation}}

{{#has_questions}}
{{#questions}}
{{n}}. **{{title}}** ({{layer}}, {{id}}) — we assumed: {{assumption}}{{#is_attribute}} Is the target *{{target}}* for *{{metric}}* right?{{/is_attribute}}
{{/questions}}
{{/has_questions}}
{{^has_questions}}
None: every element is stated by {{library.organisation}} or inferred from cited material.
{{/has_questions}}

## Annex A. Element register

{{#drivers}}
- **{{id}} {{title}}** (driver) — {{summary}} _[{{basis}}; {{source}}]_
{{/drivers}}
{{#risks}}
- **{{id}} {{title}}** ({{kind}}) — {{summary}} _[{{basis}}]_
{{/risks}}
{{#objectives}}
- **{{id}} {{title}}** (control objective) — {{summary}}
{{/objectives}}
{{#domains}}
- **{{id}} {{title}}** (domain) — {{scope}}; authority: {{authority}}
{{/domains}}
{{#services}}
- **{{id}} {{title}}** (service) — {{summary}}
{{/services}}
{{#mechanisms}}
- **{{id}} {{title}}** (mechanism) — {{summary}}
{{/mechanisms}}
{{#components}}
- **{{id}} {{title}}** (component) — {{product}}
{{/components}}
{{#operations}}
- **{{id}} {{title}}** (operation) — {{metric}}, {{frequency}}; owner {{owner}}
{{/operations}}

## Annex B. Consistency check

{{counts.errors}} error(s) and {{counts.warnings}} warning(s) from `sabsa.py check`.

{{#errors}}
- **error:** {{text}}
{{/errors}}

## Annex C. Governance, policy and trust register

### Security strategies
{{#strategies}}
- **{{id}} {{title}}** — {{statement}}; rationale: {{rationale}}; owner: {{owner}}.
{{/strategies}}

### Architecture decisions
{{#decisions}}
- **{{id}} {{title}}** — {{decision}}; rationale: {{rationale}}; owner: {{owner}}.
{{/decisions}}

### Policies
{{#policies}}
- **{{id}} {{title}}** — {{statement}}; owner: {{owner}}; objectives: {{objectives}}.
{{/policies}}

### Trust relationships
{{#trusts}}
- **{{id}} {{title}}** — {{source_domain}} → {{target_domain}}; purpose: {{purpose}}; basis: {{trust_basis}}; assurance: {{assurance_requirement}}.
{{/trusts}}

### Exceptions
{{#exceptions}}
- **{{id}} {{title}}** — {{rationale}}; risk acceptance: {{risk_acceptance}}; owner: {{owner}}; expires: {{expires}}.
{{/exceptions}}

## Annex D. Logical information and access model

{{#entities}}
- **{{id}} {{title}}** (entity) — {{population}}; owner: {{owner}}.
{{/entities}}
{{#privileges}}
- **{{id}} {{title}}** (privilege profile) — {{privileges}}; conditions: {{conditions}}; entities: {{entities}}.
{{/privileges}}
{{#information_flows}}
- **{{id}} {{title}}** (information flow) — {{information}}; classification: {{classification}}; protection: {{protection}}.
{{/information_flows}}

## Annex E. Assurance evidence and transition

### Measures and evidence
{{#measures}}
- **{{id}} {{title}}** — {{metric}}; target {{target}}; source {{data_source}}; {{frequency}}; owner {{owner}}; breach action: {{threshold_action}}.
{{/measures}}
{{#evidence}}
- **{{id}} {{title}}** — {{evidence_type}}; collected by {{collector}}; location {{location}}; measures {{measures}}.
{{/evidence}}

{{#has_assurance_traceability}}
| Evidence | Measure | Attribute | Driver |
| --- | --- | --- | --- |
{{#assurance_traceability}}
| {{evidence}} | {{measure}} | {{attribute}} | {{driver}} |
{{/assurance_traceability}}
{{/has_assurance_traceability}}

### Standards
{{#standards}}
- **{{id}} {{title}}** — {{authority}} {{version}}: {{requirement}}.
{{/standards}}

### Roadmap
{{#roadmap}}
- **{{id}} {{title}}** — {{current_state}} → {{target_state}}; owner {{owner}}; target {{target_date}}; acceptance evidence: {{acceptance_evidence}}.
{{/roadmap}}
