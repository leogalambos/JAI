> 26.10.1 scope: **EA Repository is authoritative for the
> architecture-domain
> projection only; global semantic identity is governed by the JAI
> core.**

# Enterprise Architecture Integration — 26.10.4

Version 26.10.4 defines the authoritative architecture-domain projection
repository
and adds a deterministic SABSA projection bridge, stable
source/projection traceability and layered Open Exchange conformance
gates.

## Design boundary

The canonical JSON repository is the authoritative architecture-domain
projection
store. The
Open Group ArchiMate Model Exchange File Format is used only as an
interchange boundary. This matches the exchange format's purpose: move
model instance data between ArchiMate-aware tools rather than act as a
vendor-neutral persistent repository.

## Capabilities

- stable enterprise/project element, relationship and view identifiers;
- ArchiMate 3.x Open Exchange import/export for elements, relationships
and diagram views;
- deterministic multi-view generation to JSON and SVG without creating
new model facts;
- cross-project dependency and portfolio traceability;
- lifecycle state, impact analysis, retirement/decommission blockers and
governed waivers;
- benefit records at project level and links from architecture elements
to benefit IDs;
- consistency checks for missing references, orphans, cross-project
ownership, stale retirement dependencies and model/view drift;
- one-way SABSA → canonical EA → ArchiMate projection for all 39 SABSA
semantic types / 36 cells;
- L1 offline Open Group authored exchange-XSD, L2 structural/reference/type and L3 loss-aware
exchange checks, including source-to-export comparison before a lossy first
import can be hidden by a stable second round trip.

## Examples

```bash
python3 ~/.ai/it-role-house/tools/repository.py init ./ea-repo --id enterprise-ea --name "Enterprise EA"
python3 ~/.ai/it-role-house/tools/repository.py validate ./ea-repo
python3 ~/.ai/it-role-house/tools/repository.py import-open-exchange model.xml --repo ./ea-repo --merge
python3 ~/.ai/it-role-house/tools/repository.py generate-views ./ea-repo --out ./published-views --preset all
python3 ~/.ai/it-role-house/tools/repository.py export-open-exchange ./ea-repo --out enterprise.xml
python3 ~/.ai/it-role-house/tools/repository.py portfolio ./ea-repo --format md --out portfolio-architecture.md
```

The portable profile selects ArchiMate language **3.2** and exchange schema
**3.1** explicitly. The namespace remains the standard exchange namespace ending
in `/3.0/`; it is not evidence of a different language edition. The offline XSD
set is Open Group authored and pinned from a publicly distributed MIT-licensed
implementation. It validates nested model/diagram content and datatypes rather
than only a wildcard envelope. This is not certification by The Open Group.

The check report separates permitted-triple/profile-rule validation, exchange
schema validation, preservation, visual review and external-tool interoperability.
Unknown concepts, relationship types and foreign extensions cannot establish a
valid portable result. Source-to-export checks cover element/relationship/view
content, properties and their definitions, relationship attributes, diagram
layout and organizations. Repository-envelope metadata is outside that comparison;
the report states this scope explicitly. Unpreserved information is a reported
loss, not silently accepted interoperability.

Generated SVG files are **repository graphs**. Their shapes and arrows do not
assert ArchiMate graphical notation. Heuristic selections have viewpoint
`Custom` and status `heuristic-unreviewed`; they require review against actual
stakeholder concerns and completeness criteria. Their notation and selection
qualification remain attached through namespaced exchange properties.

ArchiMate edition and tool qualification are separate decisions. Current exchange
output retains the 3.2 profile; this does not establish ArchiMate 4 conformance.
A successful runtime round trip does not establish an external application's
interoperability. No external EA application, graphical display or virtual-display
package is required by the portable workflow.

## Explicit metamodel and notation requests

```bash
python3 ~/.ai/it-role-house/tools/repository.py validate-archimate ./ea-repo --edition 3.2
python3 ~/.ai/it-role-house/tools/repository.py render-archimate ./ea-repo --view VIEW-ID --out architecture.svg
python3 ~/.ai/it-role-house/tools/ea_conformance.py check enterprise.xml --report conformance.json
```

These commands are distinct from generic `generate-views`. Validation uses the
complete pinned 62-concept permission matrix containing 11,569 allowed triples,
including junction and relationship-concept rows. Unknown triples fail. Additional
rules validate Access modes, Influence modifier types, specialization/composition
cycles, composition ownership and homogeneous junction continuity. The upstream
permission table combines direct and derived relationships; a permitted triple
does not establish a derivation proof or a business rationale.

The renderer produces **DRAFT_NOTATION**, a typed-box representation with explicit
concept labels and relationship-specific line/marker semantics. Business actors,
application components and passive-information objects carry differentiating
symbols; the draft does not certify every specialist concept icon. Independent
visual review remains required. The generic graph renderer remains available
for every retained repository concept and is labelled as a repository graph.

Every generated preset now carries an explicit viewpoint contract describing
stakeholders, concern, decision, boundary, selected concept types, completeness
criteria, exclusions and pending review. A populated local review-status string
never grants approval. Viewpoint contracts and heuristic/notation qualification
survive interchange through namespaced properties.

SABSA projections carry language edition, exchange edition and source-mapping
edition in their properties and manifest. TSI-T100's original target is 3.0;
the JAI mapping's 3.2 target is an explicit local adoption requiring independent
semantic review, not an assertion that TSI-T100 specifies 3.2.

## Source provenance

`vendor/archimate-3.2/provenance.json` pins the source repository revision and
SHA-256 of each matrix/schema/licence file. `License.txt` preserves the MIT notice
including the upstream authors and The Open Group. Resources are checked once
when loaded into a process; conformance requests reuse them. There is no network
fetch, historical reconstruction or external-tool launch during productive checks.
