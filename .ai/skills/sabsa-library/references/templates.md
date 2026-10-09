# Document templates

`sabsa.py document` renders a document from the library through a template. The package ships a default, and you
can replace it for one library, for all your work, or for one run — for example because a client wants the
document in their own structure or house style.

## Which template is used

The first of these that exists, for the template name asked for (default `architecture`):

| | Where | Use it for |
| --- | --- | --- |
| 1 | `--template FILE` on the command line | a one-off |
| 2 | `<lib>/templates/<name>.<ext>` | this client's structure, kept with the library |
| 3 | `~/.ai/sabsa-templates/<name>.<ext>` | your own house template for every library |
| 4 | the package default | if you have set nothing |

The package provides a catalogue of specialised 3.2 views. Run `sabsa.py documents <lib>` to list them. In addition to `architecture`, `client-questions`, `executive-summary`, `assurance-plan`, `governance-register` and `transition-roadmap`, 3.2 adds `risk-treatment-plan`, `policy-architecture`, `trust-model`, `information-access-model`, `security-service-catalogue`, `component-realisation`, `current-state`, `target-state`, `transition-architecture`, `lifecycle-register`, `framework-mapping`, `compliance-gap-analysis`, and `reuse-register`. Any other name works if you create a template for it.

```bash
sabsa.py documents <lib>                       # list package document views and audiences
sabsa.py template <lib> --init                 # copy the default architecture template into <lib>/templates/
sabsa.py template <lib> --name client-questions --init
sabsa.py template <lib>                        # which template applies, and from where
sabsa.py template <lib> --fields               # every field a template can use, as this library provides them
sabsa.py template <lib> --check FILE           # render FILE against the library; report unknown fields
```

Folders 2 and 3 are yours: the package never writes them, and upgrades leave them alone.

## Output formats and the client's house style

The format follows the extension of `--out`:

- **The template's own format** is written directly. A template can be Markdown, HTML, AsciiDoc, LaTeX or any
  other text format: the engine does not care. A client's HTML template with their CSS and logo works as it is.
- **`.docx`, `.odt`, `.pdf`, `.html` from a Markdown template** go through pandoc (https://pandoc.org).
  - For Word, put the **client's own `.docx`** at `<lib>/templates/reference.docx`, or pass `--reference FILE`.
    Pandoc takes its styles from it — fonts, colours, heading and table styles, margins — so the output is in the
    client's design. Use a document in their style, not a `.dotx`: open the template and save it as `.docx`.
  - For HTML, a `<lib>/templates/style.css` is applied and embedded.
  - PDF needs a LaTeX engine; usually it is easier to produce `.docx` and export PDF from Word.

```bash
sabsa.py document <lib> --out ARCHITECTURE.md
sabsa.py document <lib> --out ACME-Security-Architecture.docx          # styled by templates/reference.docx
sabsa.py document <lib> --template-name client-questions --out questions.docx
sabsa.py document <lib> --template-name executive-summary --out executive-summary.docx
sabsa.py document <lib> --template-name assurance-plan --out assurance-plan.docx
sabsa.py document <lib> --template-name governance-register --out governance-register.md
sabsa.py document <lib> --template-name transition-roadmap --out roadmap.md
sabsa.py document <lib> --template-name current-state --out current.md
sabsa.py document <lib> --template-name target-state --out target.md
sabsa.py document <lib> --template-name transition-architecture --out transition.md
sabsa.py document <lib> --template-name framework-mapping --out framework-mapping.docx
sabsa.py document <lib> --template-name reuse-register --out reuse-register.md
sabsa.py document <lib> --template client-portal.html --out architecture.html
```

## Syntax

A small subset of Mustache, the widely used logic-less template language:

| Tag | Meaning |
| --- | --- |
| `{{name}}` · `{{library.name}}` | insert a value; dots reach inside a group |
| `{{#list}} … {{/list}}` | repeat for each item of a list; inside, the item's fields are available |
| `{{#flag}} … {{/flag}}` | show only if the value is present and not empty, false or zero |
| `{{^flag}} … {{/flag}}` | show only if the value is empty, false or zero |
| `{{! comment }}` | removed from the output; must not itself contain a pair of closing braces |

A section tag alone on its line leaves no blank line behind. Values are inserted as they are, with no HTML escaping.
A field the library does not provide renders as empty **and is reported as a warning**, so a misspelt field in a
client template is caught rather than silently blank.

## Fields

`sabsa.py template <lib> --fields` lists them all for a real library. The main ones:

- `library.name`, `.organisation`, `.scope`, `.owner`, `.version`, `.status`, `.summary` (the body of `library.md`)
- `generated` (today's date), `draft` (the current snapshot is not clean and owner-approved), `has_errors`, `has_warnings`, `open_cells`, `settled_cells`, `approved`, `approval_reason`, `approval.*`
- `counts.elements`, `.reused_elements`, `.errors`, `.warnings`, `.questions`, `.frameworks`, `.framework_mappings`; `basis.stated`, `.inferred`, `.assumed`, `.unstated`
- `layers` — six items, in order: `key`, `name` (Contextual …), `view` (Business view …), `purpose`, `number` (1–6),
  `section` (4–9, the default template's numbering), and `cells` — six items each:
  `interrogative` (What …), `column` (Assets …), `question`, `guidance`, `answer`, `basis`, `source`, `reason`,
  `answered` / `not_applicable` / `open` (flags), and `elements` — what lives in the cell: `id`, `title`,
  `summary`, `basis`, `source`, plus every field of the element
- typed element collections: `drivers`, `attributes`, `risks`, `strategies`, `objectives`, `domains`, `trusts`, `decisions`, `policies`, `entities`, `privileges`, `information_flows`, `services`, `mechanisms`, `standards`, `components`, `measures`, `evidence`, `operations`, `exceptions`, `roadmap` — each with all fields and typed relations declared by the 3.2 metamodel, plus common lifecycle/horizon fields
- `traceability` — component realisation rows; `assurance_traceability`, `policy_traceability`, `trust_traceability`, `roadmap_traceability` and corresponding `has_*` flags
- lifecycle/horizon collections: `current_elements`, `transition_elements`, `target_elements`, `reference_elements`, `unspecified_horizon`, `current_target_transitions`, `lifecycle_states`, `unspecified_lifecycle`
- external framework fields: `frameworks`, `framework_mappings`, `framework_gaps`, `has_frameworks`
- cross-library reuse: `reuse_libraries`, `reused_elements`, `has_reuse`; reused element IDs are namespaced and include origin metadata
- `matrix` — six rows of `name` and `marks` (each with `mark` ✓ / n/a / · and `count`); `interrogatives`
- `questions` — `n`, `id`, `title`, `layer`, `assumption`, `is_attribute`, `target`, `metric`
- `sources` — `file`, `cited_by`; `errors`, `warnings` — each with `text`

## Example: one cell, the client's way

```markdown
{{#layers}}
# {{name}} ({{view}})
{{#cells}}
## {{interrogative}}: {{question}}
{{#answered}}{{answer}}{{/answered}}{{#not_applicable}}Not applicable — {{reason}}{{/not_applicable}}
{{#open}}**Open.**{{/open}}
{{/cells}}
{{/layers}}
```
