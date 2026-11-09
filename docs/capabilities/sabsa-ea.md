# SABSA and enterprise architecture

For an end-to-end operator journey, read the [security-assessment case](../examples/how-to-use-JAI/security-assessment.md) or [Android architecture/development case](../examples/how-to-use-JAI/android-development.md). This capability page explains model structure, supported operations and interchange. Choose direct domain work or layered creation using [Methodical workflows](../using/methodical-workflows.md) before beginning; `/sabsa` does not automatically open a complete `/layered` episode.

## SABSA support

The SABSA capability treats the architecture as a structured, traceable library rather than one monolithic report.

<div class="ai-diagram ai-diagram-inline" role="img" aria-label="Architecture and delivery diagram">
<img src="../../assets/diagrams/sabsa-chain.svg" alt="SABSA traceability chain from business drivers through attributes, risk, controls, services, mechanisms and operational measures">
</div>

The release supports all **36 SABSA matrix cells** as projection-capable architecture content and maintains structured semantic types for the runtime.

## SABSA domain metadata and Gen2 perspectives

SABSA is a **profile of the JAI semantic core**, not a parallel global truth hierarchy.

The 26.10.4 domain-profile model introduced persisted semantic references and
profile metadata. The retained SABSA reader and migration path continue to
support that metadata. A persisted field such as `jai_layer` is domain-profile
metadata; it must not be used to infer the current Gen2 content perspective.

Gen2 work uses L1 Contextual, L2 Conceptual, L3 Logical, L4 Physical,
L5 Component and L6 Management. Each perspective addresses What, Why, How, Who,
Where and When, with management concerns applying across the other perspectives.
Use the [canonical layer model](../architecture/sabsa-layer-model.md) to classify
current work. Earlier examples that treated SABSA coordinates and JAI layer
responsibilities as separate taxonomies describe the historical model.

Legacy domain libraries remain readable and can be upgraded on write or
migration. This domain compatibility does not migrate Gen1 engagement history
or carry forward acceptance or release permission; see
[compatibility](../reference/compatibility.md).

## Operator request and implementation boundary

In a **Claude Code** session use the `/sabsa` and `/repository` commands shown below; in **Codex CLI** use `$workflow-sabsa` and `$workflow-repository` with the equivalent arguments. For example, ask for the `acme-pay` SABSA coverage questions and a traceable EA projection. These names are provider commands/skills, **not Python shell calls**. The provider performs permitted `sabsa.py`, `repository.py` and EA bridge operations and should report the resulting object IDs, validation status and open architecture questions. Approval remains bound to the current snapshot and authorised owner; asking the assistant to "approve" does not supply that authority by itself.

## Main commands

=== "Claude Code"

    ```text
    /sabsa prepare <library>
    /sabsa create <library>
    /sabsa update <element> <library>
    /sabsa review <library>
    /sabsa suggest <library>
    /sabsa questions <library>
    /sabsa approve <library>
    /sabsa approval <library>
    /sabsa document <library> [as docx]
    /sabsa template <library>
    ```

=== "Codex CLI"

    ```text
    $workflow-sabsa prepare <library>
    $workflow-sabsa create <library>
    $workflow-sabsa update <element> <library>
    $workflow-sabsa review <library>
    $workflow-sabsa suggest <library>
    $workflow-sabsa questions <library>
    $workflow-sabsa approve <library>
    $workflow-sabsa approval <library>
    $workflow-sabsa document <library> [as docx]
    $workflow-sabsa template <library>
    ```

## Enterprise architecture repository

The EA repository is JSON-based, with ArchiMate/Open Exchange used as an interoperability boundary.

The domain-projection boundary introduced in 26.10.4 distinguishes the EA
repository from the JAI semantic identity authority:

```text
authoritative_for: ea-domain-projection
global_source_of_truth: false
semantic_identity_authority: JAI
```

That means the repository is authoritative for architecture-domain projection state, lifecycle, views, relationships and related EA governance; it does not create a second global identity for an object that already exists in JAI/SABSA semantics.

=== "Claude Code"

    ```text
    /repository validate architecture-repository.json
    /repository views architecture-repository.json all
    /repository portfolio architecture-repository.json
    /repository export architecture-repository.json model.xml
    ```

=== "Codex CLI"

    ```text
    $workflow-repository validate architecture-repository.json
    $workflow-repository views architecture-repository.json all
    $workflow-repository portfolio architecture-repository.json
    $workflow-repository export architecture-repository.json model.xml
    ```

Legacy repository versions `26.10`, `26.10.1`, `26.10.2` and `26.10.3` are accepted for read/migrate; current writes use the JAI-scoped profile-native model.

## Portable ArchiMate 3.2

Owner: architecture repository maintainers. Reviewed for current source
behavior on 2026-11-09. The procedure below describes the portable
implementation; professional acceptance remains a separate assessment.

### Request the representation

ArchiMate is opt-in. Ask for it in ordinary language through the existing
repository workflow; the request selects a representation and its checks,
not approval. For example:

=== "Claude Code"

    ```text
    /repository Prepare an ArchiMate 3.2 application view from the governed model in working/ for the service owner. Use the portable profile, preserve source IDs and report semantic, visual and exchange limitations. Keep unreviewed notation draft.
    ```

=== "Codex CLI"

    ```text
    $workflow-repository Prepare an ArchiMate 3.2 application view from the governed model in working/ for the service owner. Use the portable profile, preserve source IDs and report semantic, visual and exchange limitations. Keep unreviewed notation draft.
    ```

A project may make ArchiMate its default only through an explicit profile
whose recipients understand the notation, whose views answer named
stakeholder concerns, and whose governed source model has stable facts
and identities. Record the exact edition, mapping and renderer scope;
require independent semantic and visual review of the delivered revision.
Qualify a receiving tool separately when one is used. Without these
conditions, choose suitable text, tables or other views. See the
[representation policy](../reference/sabsa-delivery-profile.md#5-optional-archimate-representation).

### Run the portable checks

The supported profile uses ArchiMate language **3.2** and Model Exchange
schema **3.1**. The exchange namespace ends in `/3.0/`; that URI does not
select a different language edition. A model's own revision is also
distinct from either edition. This profile does not claim version 4
support or external-tool interoperability. No Archi application,
graphical display or virtual-display package is required.

For an installed runtime, a maintainer or the provider can invoke the
following helpers against an existing repository and view. Substitute its
actual path and view ID; these Python operations are not additional
slash-command verbs:

```bash
python3 ~/.ai/it-role-house/tools/repository.py validate-archimate ./ea-repo --edition 3.2
python3 ~/.ai/it-role-house/tools/repository.py render-archimate ./ea-repo --view VIEW-ID --out architecture.svg
python3 ~/.ai/it-role-house/tools/ea_conformance.py check enterprise.xml --report conformance.json
```

Create `enterprise.xml` using the existing Open Exchange export operation
before its conformance check. In a source checkout, use the corresponding
tools under `.ai/runtime/tools/`. Keep these checks distinct:

- Metamodel validation checks permitted concept/relation triples and
  profile constraints. The pinned permission matrix combines direct and
  derived relationships; permission alone proves no derivation or
  business rationale.
- Offline exchange validation checks the pinned XSD schema and nested
  model/diagram content. It is not Open Group certification.
- Preservation checks compare source and export content, including
  properties, relationships, views and layout. A stable second round
  trip cannot hide a loss on first import; unresolved loss remains an
  explicit limitation.
- Independent semantic and visual review assesses the actual stakeholder
  concern, source fidelity, completeness and rendered notation. Neither
  schema validation nor a successful render establishes that review.
- External-tool qualification, when requested, identifies the actual
  application, version and observed import/export results. Internal
  checks cannot establish that evidence.

The explicit renderer produces **DRAFT_NOTATION**: typed boxes, concept
labels and relationship-specific lines/markers. It does not claim every
specialist concept icon is qualified. Generic `generate-views` output
remains a **repository graph**, not verified ArchiMate graphical notation.
Retain draft/heuristic status and viewpoint exclusions until the exact
revision has its required reviews; a populated local status field grants
no acceptance or release permission.

The pinned matrix and exchange-schema resources retain their upstream
MIT notices; see [licensing](../about/license-attribution.md). Their availability
does not certify the model or authorize a restricted standard publication.

## SABSA → EA projection

The intended direction is:

```text
JAI canonical semantic identity
        │
        ├── SABSA specialisation / coordinates
        │
        └── EA-domain projection
               │
               └── ArchiMate/Open Exchange interchange
```

The bridge preserves source specialisation and canonical references so that EA views remain traceable to the semantic origin rather than becoming an independent copy of the truth.

## LaTeX documents and editable CSV catalogues

The SABSA conversation workflow uses **Markdown by default**. Ask for a different format in ordinary language when the audience needs it; this does not change the canonical source or approval rules. For example:

The document workflow selects a viewpoint and presents its reviewed semantic content for the requested audience. Expect output paths, the selected template, source provenance and remaining publication gaps before treating a rendered document as ready for use.

=== "Claude Code"

    ```text
    /sabsa document project/sabsa — generate the Logical Security Architecture
    in English as LaTeX and PDF from the reviewed entries and authored
    narrative. Preserve source provenance, report the template and output
    paths, show publication gaps, and keep snapshot approval and rendered-QA
    status explicit.
    ```

=== "Codex CLI"

    ```text
    $workflow-sabsa document project/sabsa — generate the Logical Security
    Architecture in English as LaTeX and PDF from the reviewed entries and
    authored narrative. Preserve source provenance, report the template and
    output paths, show publication gaps, and keep snapshot approval and
    rendered-QA status explicit.
    ```

Ask for Word explicitly for a Word-based review, or request editable CSV catalogues when managing structured entries. The provider should report the chosen viewpoint/template, output paths, actual validation and remaining draft reasons. A format request does not authorise an owner approval.

The following are implementation examples for a maintainer or for inspecting the commands JAI reports; normal users can make the conversation request above:

```sh
python3 .ai/runtime/tools/sabsa.py document LIB --out architecture.tex
python3 .ai/runtime/tools/sabsa.py document LIB --layer logical --out logical.tex
python3 .ai/runtime/tools/sabsa.py document LIB --out architecture.pdf --latex
python3 .ai/runtime/tools/sabsa.py document LIB --template-name security-service-catalogue --out services.docx
```

Writing `.tex` requires Pandoc. Compiling the controlled LaTeX/PDF edition additionally requires XeLaTeX, its installed packages and DejaVu Serif. Word generation uses Pandoc; LibreOffice or Word is used when independently rendering Word output for visual review. These Office tools are not part of the SABSA TeX/PDF renderer. See [publication stack](../configuration/publication-stack.md) and [sandbox prerequisites](../getting-started/sandbox-prerequisites.md) for format-specific prerequisites. The shared LaTeX template provides a
controlled cover (owner, version, status, scope, approval), contents, running header,
page totals and landscape long tables. Markdown raw TeX is disabled during conversion.
The controlled layout is shared across document views, while each viewpoint's
authored content preserves its own architectural purpose. All existing document
views can use this template.
Word tables receive explicit proportional widths; tables with five or more columns
use landscape sections, with a narrower identifier column and more room for prose.

```sh
python3 .ai/runtime/tools/sabsa.py catalogues LIB export --directory CSV
# Edit CSV values, retaining IDs, headers and schema.json.
python3 .ai/runtime/tools/sabsa.py catalogues LIB validate --directory CSV
python3 .ai/runtime/tools/sabsa.py catalogues LIB import --directory CSV
```

Markdown entries remain authoritative. CSV is an editable exchange projection with
versioned schema, UTF-8 encoding, comma delimiter, LF records, fixed columns per type,
stable ID sorting and SHA-256 export manifest. Relation columns retain canonical
comma-separated IDs; CSV quoting preserves commas and quotation marks. Reused entries
are managed in their source library and are excluded from editable exports. Imports
update existing local IDs only; use `new` to create entries and export again. Missing,
new or duplicate IDs, changed schemas and multiline metadata are rejected. Validation
checks a temporary library before any source mutation. Import preserves entry bodies
and native metadata, rolls back write failures, and invalidates prior snapshot approval
through the existing content hash. The export manifest fingerprints the original
export; it is not an approval of subsequent CSV edits.

Rollback: restore changed canonical entries from version control; generated CSV,
LaTeX, PDF and DOCX can be regenerated. No owner approval or publication gate is implied
by successful rendering or CSV validation.

Use `--layer contextual|conceptual|logical|physical|component|service-management`
for an individual matrix layer; `operational` aliases `service-management`.
The retained `service-management` and `operational` CLI identifiers select
L6 Management; they do not introduce additional Gen2 perspectives. Each layer
document includes its six matrix questions, local elements, source/basis,
whole-library approval status and business traceability context.

## Authored English viewpoint documents

Each SABSA layer has its own document profile with substantial authored chapters,
complete element specifications and source bodies, responsibilities, evidence, review
and typed business justification paths. The logical viewpoint describes services,
policy and information access; the component viewpoint describes engineering and
verification; operations describes measurement and assurance. These are semantic
viewpoints rather than a shared questionnaire dressed as a publication.

| Viewpoint | Publication focus |
| --- | --- |
| Contextual | Business context, dependencies and security governance |
| Conceptual | Measurable attributes, security concepts, objectives and trust |
| Logical | Security services, policies, information and access |
| Physical | Mechanisms, deployment boundaries and control execution |
| Component | Component specifications, configuration and verification |
| Service Management | Operations, measurement, evidence and improvement |

Run `sabsa.py narrative-init LIB --layer logical`, write the chapter files under
`narratives/logical/` with basis/source/author/language provenance, then use `document
--layer logical`. Missing prose, source scaffolding and unresolved traceability stay
visible as authoring gaps. Narratives participate in source citations, validation and
snapshot approval; changing them invalidates prior approval. Authors supply reviewed
professional English text, preserve original sources and cite translations. The
renderer preserves canonical meaning and does not automatically translate content.

The complete contract is in `.ai/runtime/sabsa/publication/README.md`. Generate the
populated fictional six-viewpoint example with
`python3 .ai/runtime/tools/sabsa_publication_demo.py --out DIR --render`.

For guided use, follow [assessing a deployed system](../examples/how-to-use-JAI/security-assessment.md) or [keeping Android development aligned](../examples/how-to-use-JAI/android-development.md). Both explain why to take each step and how to distinguish source-backed results from proposed next work.

## Why this matters

Organisations often struggle to keep security architecture, enterprise
architecture and published documents aligned. Domain-profile boundaries define
each subsystem's scope, while Gen2's six SABSA perspectives organise current
work and its justification. Stable identity and traceability connect those
scopes without treating historical profile metadata as a current layer model.


## Independent review model prerequisite

For SABSA AI-authored work, the reviewer must use a different explicit model from
the corresponding author. Different effort alone is insufficient. This retained
professional requirement cannot be waived by an execution profile. When a named
profile would select the same model for both, choose a compatible different model
and disclose the deviation, or keep the review pending with its inline recovery
instructions. A profile command changes future runs, not an already pinned run.

The governed admission check binds the exact candidate's producer context and
captured selection, rather than a later mutable author plan. It applies to captured
SABSA professional categories/operators and admitted SABSA semantic/domain markers;
choosing a generic profession does not bypass an explicitly marked SABSA subject.
Checks run on review selection, new work admission and new assessment registration.
Immutable pair results are reused; historical replay does not rewrite or reapprove
past records. Independent actors and physical contexts remain mandatory.

Native Claude/Codex execution is AI. A process resource label is not automatically
an AI model: a captured `model_kind: deterministic` declaration for a model-free
process exempts its author output from AI model-pair diversity, while other review
requirements remain. Process-wrapped AI declares `model_kind: ai`, its actual
`model_provider` and `model_identity` separately from the executable resource label.
An affected process with unspecified kind or model identity is an unavailable
prerequisite, not permission to guess. A deterministic checker can provide evidence
but cannot replace the required different-model review of AI-authored SABSA work.
These administrative declarations do not prove what arbitrary process code did.

For ordinary `/sabsa` and `$workflow-sabsa`, the native parent runs the same shared
read-only pair check before actual native author/reviewer delegation. It pins the
explicit requested controls and uses the helper's ordinary-model recovery help;
no layered engagement or parallel journal is required. If those controls are
unavailable, the parent must explain the host barrier and stop the affected review.
This mechanically checks the supplied pair; parent compliance is not OS-level
interception of arbitrary calls, and requested selectors do not attest served
backend identity. Registry alternatives are not observed host/account availability.

See [execution profiles and actual routing](../configuration/execution-profiles.md#routing-deviations-and-professional-requirements)
and the [context operation glossary](../configuration/execution-profiles.md#what-each-operation-means).
