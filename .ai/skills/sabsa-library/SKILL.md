---
name: sabsa-library
description: "Prepares, creates, updates, reviews and improves a SABSA security architecture library: business drivers, measurable business attributes, risks and opportunities, control objectives, domains, logical services, physical mechanisms, components and service-management operations, every element traced to the business. sabsa-architect writes entries, sabsa-reviewer checks traceability and measurability and judges quality, and suggestions come ranked with the next concrete step. Use for 'build a SABSA architecture for…', 'update our SABSA library', 'review our security architecture against SABSA', 'what is missing from our attribute profile', or traceability and coverage questions."
allowed-tools: Read, Grep, Glob, Bash, Task, Agent
---

# SABSA library

> **Agents named here** are subagents: delegate them through the active provider's operator/delegation mechanism — `research-analyst`, `sabsa-architect`, `sabsa-reviewer`.

`tool-tier: orchestrate` (`Read, Grep, Glob, Bash, Task, Agent`) · `version: 1.2.0`

You orchestrate work on a SABSA library — a folder of one-file-per-element entries, laid out by SABSA layer.
`references/structure.md` defines every element and field. The tool:

```bash
# `sabsa` below means:   python3 ~/.ai/it-role-house/tools/sabsa.py   (write it out in full; never store it in a shell variable)
sabsa init <lib> --name … --organisation … --scope … --owner …      # creates 00-sources/ for client material
sabsa metamodel                                                   # active declarative element contract
sabsa new <lib> <type> --title "…" [--set f=v]                     # type list comes from the metamodel
sabsa check <lib>      sabsa suggest <lib>      sabsa trace <lib> <ID>      sabsa report <lib>
sabsa view <lib> <realisation|assurance|policy|trust|roadmap>       # typed relation views
sabsa lifecycle <lib> [ID]     sabsa lifecycle-set <lib> ID ...         # current/transition/target + lifecycle
sabsa overlays <lib>           sabsa overlay-init <lib> --id ...       # external framework mappings
sabsa reuse <lib>              sabsa reuse-add <lib> ALIAS PATH        # cross-library reusable architecture
sabsa documents <lib>                                                   # specialised generated document views
sabsa matrix <lib>     sabsa sources <lib>      sabsa questions <lib>    sabsa migrate <lib>
sabsa approve <lib> --by "<owner/person>" [--note "decision reference"]    sabsa approval <lib>
sabsa document <lib> --out <lib>/ARCHITECTURE.md      (or .docx, .html; see references/templates.md)
sabsa template <lib> [--init | --fields | --check FILE]
```

## The five activities

| Activity | Steps |
| --- | --- |
| **Prepare** | See *From client material to an architecture* below. |
| **Create** | Build in **dependency order**, not a misleading strict layer sequence: drivers → attributes → risks/opportunities → objectives → strategies/domains/trust/decisions → policies/entities/information flows/services → mechanisms → standards/components → measures/evidence/operations/exceptions/roadmap. The 3.2 metamodel is declarative; validate each dependency stage and then review/render by SABSA layer. Scaffold entries with `sabsa new`. |
| **Update** | `sabsa trace <lib> <ID>` first: it lists every element that depends on the one changing. For architectural evolution also inspect `sabsa lifecycle <lib>` so current/transition/target relationships remain explicit. Dispatch `sabsa-architect` with the change and the impact list; each dependent is updated or explicitly confirmed unaffected. Then review. |
| **Review** | Dispatch `sabsa-reviewer` with the library and a ledger name. It runs `check`, `suggest` and `report`, judges whether elements are right and not just present, and records findings. Rework with `sabsa-architect`, verification by `sabsa-reviewer`, until `findings.py status` is COMPLETE — the same bounded loop as `library-lifecycle`. |
| **Suggest** | `sabsa suggest <lib>` gives the structural gaps, ranked: integrity, measurability, coverage, the assurance loop, matrix cells. Dispatch `sabsa-reviewer` to add judgement: which gaps matter for this organisation, and what to do about each. |

## From client material to an architecture

This is the usual way in: a project, some information about the client or the environment, and a SABSA
architecture to produce.

1. **Initialise** the library inside the project: `sabsa init <project>/sabsa --name … --organisation … --scope … --owner …`.
2. **Intake.** Everything known goes into `<lib>/00-sources/` as text files: the brief or RFP, meeting notes,
   the client's website or annual report, organisation chart, regulatory context, existing architecture and
   policies, incidents. Convert PDF and Word files to text first. Ask the user what exists; do not invent material.
3. **Public context.** Dispatch `research-analyst` for what the material implies but does not say — the
   regulations that apply to this sector and country, the threats typical of it — with citations. Have
   `sabsa-architect` save the result as `00-sources/research-<topic>.md`, so it can be cited like the rest.
4. **Drivers.** Dispatch `sabsa-architect` with the sources to propose business drivers. Each cites the file and
   section it comes from and states its basis: `stated` (the client said it), `inferred` (follows from what
   they said, the reasoning in the entry), or `assumed` (needed, but not supported by the material).
   `sabsa check` makes a `stated` or `inferred` driver without a source an error.
5. **Build element dependencies, then complete each layer's six questions.** Create elements in the dependency order above; then for every SABSA layer, Contextual through Service Management:
   - the layer's elements, as in *Create* — for the Contextual layer drivers and risks; Conceptual, the
     attribute profile (each attribute with metric, measurement and target), control objectives and domains;
     Logical, policies, entities, privilege profiles, information flows and services; Physical, mechanisms; Component, standards and components; Service Management, measures, evidence, operations, exceptions and roadmap;
   - **its six matrix cells**: `matrix/<layer>-what|why|how|who|where|when.md`. Each states its question; the
     architect writes the answer for this client, citing `source` and `basis`, or sets `status: not-applicable`
     with a `reason`. Narrative cells remain for client-specific synthesis, and typed artefacts promote the most assurance-critical concepts to first-class typed artefacts. Use prose only for context that genuinely has no reusable typed representation; the matrix is a view, not the primary system of record.

   `sabsa check` clean and `sabsa matrix` reviewed after each layer. When the work distinguishes baseline, interim and target architecture, classify typed elements with `horizon: current|transition|target|reference`, record lifecycle state, connect target elements to same-type `predecessors`, and cite RM roadmap items in `transition_items`.
6. **Review** with `sabsa-reviewer` against the SABSA criteria (`criteria.py show <lib>`).
7. **Deliver:**
   - `sabsa document <lib> --out <lib>/ARCHITECTURE.md` — the complete architecture document, generated from
     the library, so the document and the library cannot disagree: every layer, every one of its six questions
     with its answer and the elements in it, the attribute profile, traceability, the matrix and the open
     questions. It carries a DRAFT banner until `check` has no errors or warnings, all 36 questions are settled, and the current snapshot has a valid owner approval. After review, the owner runs `sabsa approve <lib> --by ...`; `sabsa approval <lib>` proves whether later edits have invalidated it.
   - **In the client's structure or style:** `sabsa template <lib> --init` copies the default into
     `<lib>/templates/` to edit; a client's own template (Markdown, HTML, any text format) goes there too; their
     Word design goes in as `<lib>/templates/reference.docx` and styles `--out …docx`. See `references/templates.md`.
   - `sabsa questions <lib>` — every assumption written as a question for the client. With a potential client,
     this list is often the most valuable output: it is the agenda for the next meeting.
   - `sabsa sources <lib>` — which material was used, and which was not.
   - `sabsa documents <lib>` — the available specialist views. Use policy/trust/information/service/component/current/target/transition/framework/reuse views instead of creating independent hand-maintained deliverables.
   - `sabsa overlays <lib>` — mappings to external frameworks. Store identifiers and mappings; never silently reproduce licensed framework text.
   - `sabsa reuse <lib>` — shared/reference libraries and their approval state. References are namespaced (`enterprise:PL-001`); reused source snapshot changes deliberately invalidate downstream approvals.
8. **Iterate.** When the client answers, add their answers to `00-sources/`, change each answered element's
   basis to `stated` with the new source, and run `sabsa trace` before changing anything that others depend on.

## Rules

- Never present an assumption as a fact. Every driver and attribute says what it rests on; the document shows
  the basis of every element, and the open assumptions are listed as questions.
- Every element traces upward to a driver through **typed business-parent relations** declared in the metamodel; lateral relationships never substitute for justification. An attribute without a metric, measurement and target is an error. Prefer first-class `ME` measures and `EV` evidence to close the operational assurance loop; legacy `SO` operations remain supported for 3.0 libraries.
- Treat current/transition/target as an explicit architecture axis, not prose. `lifecycle_state` describes maturity/operation; `horizon` describes architectural time. Do not conflate the two.
- External frameworks are overlays on the SABSA model, not a second architecture database. Map requirement identifiers to typed elements/evidence/roadmap/exceptions and keep authoritative framework content at its licensed source.
- Prefer cross-library reuse for enterprise/reference policies, standards, strategies and other stable architecture instead of copying them. Reuse is namespaced, source-approval-aware and snapshot-bound.
- The architect writes, the reviewer checks, the owner approves. A text `status: approved` is not release authority: final approval is the hash-bound `.sabsa/approval.json` created by `sabsa approve` after a clean review. Any architecture-input edit invalidates it.
- SABSA is the SABSA Institute's framework. Its attribute taxonomy is not reproduced here; use the
  organisation's own definitions or its licensed material.
- For an architecture decision that must be justified to an audit or a board, run `/layered` with the library
  report as evidence.
