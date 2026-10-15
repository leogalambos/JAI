# {{library.name}}

## {{publication_title}}

**Audience:** {{publication_audience}}

{{publication_purpose}}

**Document owner:** {{library.owner}} · **Version:** {{library.version}} · **Scope:** {{library.scope}}

{{#draft}}
> **DRAFT — publication readiness is not established.** {{approval_reason}}. Any missing authored narrative, unresolved architecture issues or incomplete matrix coverage are reported below. Rendering does not grant approval.
{{/draft}}
{{^draft}}
> Architecture snapshot approved by {{approval.approved_by}} at {{approval.approved_at}}.
{{/draft}}

{{#publication_chapters}}
## {{heading}}

{{#missing}}
**Publication gap:** the architecture author has not supplied this chapter. Complete `{{path}}` from cited source material before release.
{{/missing}}
{{#english_gap}}
**English edition gap:** this chapter is declared {{language}}. An author-reviewed English version is required; the source text below is reproduced without automatic translation.
{{/english_gap}}
{{prose}}

{{^missing}}
*Provenance: {{basis}} · Source: {{source}} · Author: {{author}} · Language: {{language}} · Canonical chapter: {{path}}.*
{{/missing}}

{{/publication_chapters}}


## Architecture specifications and design rationale

The following specifications reproduce the complete recorded fields and narrative of this viewpoint. Identifiers and relationship names retain their canonical meaning.

{{#publication_groups}}
### {{heading}}

{{#empty}}
**Coverage gap:** no architecture entries are recorded for this part of the viewpoint. Applicability requires an explicit author decision.
{{/empty}}
{{#records}}
#### {{id}} — {{title}}

**Element type:** {{type}} · **Canonical source:** {{path}}
{{#external}}
**Reused source library:** {{origin}} · **Origin identifier:** {{origin_id}}. Amend this element in its source library.
{{/external}}
{{#english_gap}}
**English edition gap:** source language is {{language}}; author-reviewed translation is required. Source meaning is preserved below.
{{/english_gap}}

{{#fields}}
**{{name}}:** {{value}}


{{/fields}}

{{#missing_body}}
**Publication gap:** detailed rationale and design narrative have not been authored for this element.
{{/missing_body}}
{{body}}

##### Typed dependencies

{{^has_edges}}
No typed dependencies are recorded for this element.
{{/has_edges}}
{{#edges}}
- **{{field}}** → **{{target}}** ({{target_type}}): {{title}}. {{#business}}Business justification relationship.{{/business}}{{^business}}Supporting dependency; does not substitute for business justification.{{/business}}
{{/edges}}

##### Business justification paths

{{#paths}}
- {{text}}
{{/paths}}


{{/records}}


{{/publication_groups}}


## SABSA viewpoint coverage

{{#layers}}
{{#cells}}
### {{interrogative}} — {{question}}

Status: {{status}} · Basis: {{basis}} · Source: {{source}}

{{answer}}
{{#not_applicable}}
Applicability decision: {{reason}}
{{/not_applicable}}
{{#open}}
**Coverage gap:** this viewpoint question is not yet resolved.
{{/open}}

{{/cells}}

{{/layers}}

## Source register and publication gaps

{{#publication_sources}}
### {{file}}

Cited by:

{{#citations}}
- `{{path}}`

{{/citations}}
{{/publication_sources}}
{{#publication_gaps}}
- {{text}}
{{/publication_gaps}}
