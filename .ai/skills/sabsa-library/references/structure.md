# SABSA library structure

Generated from `sabsa.py`, so it always matches what the tool enforces.

## Folders

```
<lib>/
├── library.md              name, organisation, scope, owner, version; its body is the executive summary
├── 00-sources/             client and environment material, as text files; every claim cites one
├── 01-contextual/ … 06-service-management/   the elements, by layer and type
├── matrix/                 36 files: one per layer × question, answered or marked not-applicable
├── overlays/               optional external framework mapping overlays (identifiers/mappings, not bundled licensed text)
├── reuse.json              optional namespaced dependencies on other SABSA libraries
├── .sabsa/approval.json    owner approval of the exact architecture-input + reused-dependency snapshot
└── templates/              optional: this library's own document templates and reference.docx
```

## Elements

The element catalogue is declarative (`runtime/sabsa/schema/elements.json`). The table below is the 3.2 metamodel; `sabsa.py metamodel` prints the active runtime contract.

| Type | ID | Folder | SABSA layer | Default cell | Required fields | Typed links (✓ required) |
| --- | --- | --- | --- | --- | --- | --- |
| driver | BD-NNN | `01-contextual/drivers/` | Contextual | What | title, statement, owner | — |
| risk | RO-NNN | `01-contextual/risks/` | Contextual | Why | title, kind, statement | `attributes` → attribute ✓ |
| attribute | BA-NNN | `02-conceptual/attributes/` | Conceptual | What | title, definition, metric, measurement, target, owner | `drivers` → driver ✓ |
| strategy | SG-NNN | `02-conceptual/strategies/` | Conceptual | How | title, statement, rationale, owner | `attributes` → attribute ✓, `objectives` → objective |
| objective | CO-NNN | `02-conceptual/control-objectives/` | Conceptual | Why | title, statement | `attributes` → attribute ✓, `risks` → risk ✓ |
| domain | DM-NNN | `02-conceptual/domains/` | Conceptual | Where | title, scope, authority | `objectives` → objective ✓, `trusts` → domain |
| trust | TR-NNN | `02-conceptual/trust-relationships/` | Conceptual | Who | title, purpose, trust_basis, owner | `source_domain` → domain ✓, `target_domain` → domain ✓, `objectives` → objective ✓ |
| decision | AD-NNN | `02-conceptual/decisions/` | Conceptual | Why | title, decision, rationale, owner | `objectives` → objective ✓ |
| policy | PL-NNN | `03-logical/policies/` | Logical | Why | title, statement, owner | `objectives` → objective ✓, `services` → service |
| entity | ET-NNN | `03-logical/entities/` | Logical | Who | title, population, owner | `objectives` → objective ✓, `domains` → domain |
| privilege | PV-NNN | `03-logical/privilege-profiles/` | Logical | Who | title, privileges, owner | `entities` → entity ✓, `policies` → policy ✓, `objectives` → objective ✓ |
| information-flow | IF-NNN | `03-logical/information-flows/` | Logical | What | title, information, protection, owner | `source_entity` → entity ✓, `target_entity` → entity ✓, `objectives` → objective ✓, `services` → service |
| service | SS-NNN | `03-logical/services/` | Logical | How | title, description | `objectives` → objective ✓, `domain` → domain, `policies` → policy |
| mechanism | SM-NNN | `04-physical/mechanisms/` | Physical | How | title, description | `services` → service ✓ |
| standard | ST-NNN | `05-component/standards/` | Component | Why | title, authority, requirement | `policies` → policy ✓, `mechanisms` → mechanism |
| component | SC-NNN | `05-component/components/` | Component | How | title, product | `mechanisms` → mechanism ✓, `standards` → standard |
| measure | ME-NNN | `06-service-management/measures/` | Service Management | How | title, metric, data_source, frequency, target, threshold_action, owner | `attributes` → attribute ✓, `services` → service |
| evidence | EV-NNN | `06-service-management/evidence/` | Service Management | What | title, evidence_type, location, collector | `measures` → measure ✓ |
| operation | SO-NNN | `06-service-management/operations/` | Service Management | How | title, metric, frequency, owner, threshold_action | `attributes` → attribute ✓, `services` → service, `measures` → measure |
| exception | EX-NNN | `06-service-management/exceptions/` | Service Management | Why | title, rationale, risk_acceptance, owner, expires | `objectives` → objective ✓, `policies` → policy |
| roadmap | RM-NNN | `06-service-management/roadmap/` | Service Management | When | title, current_state, target_state, owner, target_date, acceptance_evidence | `objectives` → objective ✓, `components` → component |

Every element carries provenance through `source` and `basis`; missing provenance is a warning and blocks owner approval. The canonical cell comes from the metamodel. Use `aspect` only for a deliberate alternate view, not to change an element's ontology.

### Typed trace views

`runtime/sabsa/schema/views.json` defines reusable, explicit relation paths. `sabsa.py view <lib> realisation|assurance|policy|trust|roadmap` renders them without following unrelated/lateral links. This prevents a structurally valid but semantically wrong relation from appearing in the wrong traceability column.

### Architecture horizon and lifecycle (3.2)

Every typed element also accepts these optional common fields:

- `horizon`: `current | transition | target | reference` — where the element sits in architectural time;
- `lifecycle_state`: `proposed | reviewed | approved | implemented | operational | deprecated | retired` — maturity/operational state;
- `valid_from`, `valid_until` — temporal applicability;
- `predecessors` — same-type element IDs that this transition/target element evolves or replaces;
- `transition_items` — `RM-*` roadmap items implementing the movement.

These two axes are deliberately separate. A target architecture element may be only `approved`; a current element may be `operational` or `deprecated`. `sabsa lifecycle` renders the current/transition/target register and `sabsa lifecycle-set` enforces allowed lifecycle-state transitions.

### Cross-library reuse

`reuse.json` declares source libraries with a short alias. Imported IDs are namespaced (`enterprise:PL-001`). Optional `types` or `ids` selectors limit the import; dependencies needed by selected elements are included automatically. Source approval is required by default. The consuming approval hash includes reused-library snapshot hashes, so source drift invalidates downstream approval and forces impact review.

### External framework overlays

`overlays/*.json` maps external requirement identifiers to typed architecture elements, `EV-*` evidence, `RM-*` treatment and `EX-*` exceptions. Mapping states are `covered`, `partial`, `gap`, and `not-applicable`. Overlays intentionally do not ship copyrighted/licensed framework requirement text; keep authoritative content at the framework source and map by identifier/local label.

## The matrix: six layers, six questions

Each cell is a file `matrix/<layer>-<question>.md`. Answer its question in the body, citing `source` and `basis`, or set `status: not-applicable` with a `reason`. Every answered or not-applicable cell must state a valid `basis`; `stated` and `inferred` cells must cite a source. The document renders every cell.

### Contextual — Business view

_The business itself: what it does, why it needs security, and the constraints it works within._

- **What** — Which business assets, goals and decisions does security protect or enable?
- **Why** — Which business risks — threats and opportunities — matter, and why?
- **How** — Which business processes depend on security, and how?
- **Who** — Who is involved: the organisation, its governance, customers, partners and suppliers?
- **Where** — Where does the business operate: locations, jurisdictions, markets?
- **When** — When: which business cycles, deadlines and time dependencies constrain security?

### Conceptual — Architect's view

_What security must achieve, expressed as attributes, objectives, strategies and domains._

- **What** — What does 'secure' mean for this business — its attribute profile?
- **Why** — Why: which control objectives follow from the risks and attributes?
- **How** — How: which security strategies and architectural layering will meet the objectives?
- **Who** — Who: which entities are trusted, by whom, and on what basis?
- **Where** — Where: which security domains exist, and how do they relate?
- **When** — When: which security lifetimes, deadlines and time limits apply?

### Logical — Designer's view

_The security services, policies, information and entities that deliver the concept._

- **What** — What information needs protecting, and how is it classified?
- **Why** — Why: which security policies govern the information and services?
- **How** — How: which logical security services deliver the objectives?
- **Who** — Who: which entities, roles and privilege profiles exist?
- **Where** — Where: how are the security domains defined and associated with each other?
- **When** — When: what is the security processing cycle?

### Physical — Builder's view

_The mechanisms, rules, infrastructure and data structures that implement the design._

- **What** — What data structures and stores hold the information?
- **Why** — Why: which security rules, practices and procedures apply?
- **How** — How: which security mechanisms implement the services?
- **Who** — Who: which users, applications and interfaces interact with the system?
- **Where** — Where: which platforms and network infrastructure carry the system?
- **When** — When: in what order and at what times do the controls execute?

### Component — Tradesman's view

_The products, standards, identities and protocols that make up the mechanisms._

- **What** — What detailed data structures and formats are used?
- **Why** — Why: which security standards apply to the components?
- **How** — How: which security products and tools are used?
- **Who** — Who: which identities, functions and access rights are configured?
- **Where** — Where: which nodes, addresses, ports and protocols are involved?
- **When** — When: what is the timing and sequencing of each security step?

### Service Management — Service manager's view

_How security is operated, measured, supported and kept current._

- **What** — What assures operational continuity of security?
- **Why** — Why: how is operational security risk managed?
- **How** — How are security services managed and supported?
- **Who** — Who is managed and supported, and how?
- **Where** — Where: how are sites, networks and platforms kept secure in operation?
- **When** — When: what is the security operations schedule?

## Field guidance

- **statement** — One sentence, in business language: what the business needs or what could happen.
- **source** — Which client material this comes from: 00-sources/<file>[#section], or a URL. Comma-separate several.
- **basis** — stated (the client said so) | inferred (follows from what they said) | assumed (to confirm)
- **category** — Your attribute category (e.g. from your licensed SABSA taxonomy, or your own).
- **definition** — What this attribute means in THIS organisation, precisely enough to disagree with.
- **metric** — What is measured.
- **measurement** — How, from which source, how often.
- **target** — The threshold that counts as meeting it.
- **kind** — threat or opportunity
- **likelihood** — low | medium | high
- **impact** — low | medium | high
- **scope** — What this domain covers.
- **authority** — Who sets policy within it.
- **description** — What this provides, in the terms of the layer.
- **policy** — The rule the service enforces.
- **product** — Product, standard or tool, with version where it matters.
- **configuration** — Settings that matter for the mechanism.
- **frequency** — How often it is measured.
- **threshold_action** — What happens when the target is missed.
- **owner** — A named person or role.


## Approval and release state

`status: approved` is not itself an approval. Final approval is created with `sabsa.py approve <lib> --by <person-or-role>` only after `check` is free of both errors and warnings. The command writes `.sabsa/approval.json` containing the approver, UTC timestamp, version and SHA-256 of the complete architecture-input snapshot (`library.md`, sources, matrix cells, element files, framework overlays and `reuse.json`) plus the snapshot hashes of reused libraries. Any local change or reused-source drift invalidates the approval automatically. `sabsa.py approval <lib>` verifies the current snapshot. Generated documents remain **DRAFT** unless the current snapshot is validly approved.
