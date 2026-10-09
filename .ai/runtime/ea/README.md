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
- L1 XML/XSD-envelope, L2 semantic and L3 loss-aware round-trip
conformance checks.

## Examples

```bash
python3 ~/.ai/it-role-house/tools/repository.py init ./ea-repo --id enterprise-ea --name "Enterprise EA"
python3 ~/.ai/it-role-house/tools/repository.py validate ./ea-repo
python3 ~/.ai/it-role-house/tools/repository.py import-open-exchange model.xml --repo ./ea-repo --merge
python3 ~/.ai/it-role-house/tools/repository.py generate-views ./ea-repo --out ./published-views --preset all
python3 ~/.ai/it-role-house/tools/repository.py export-open-exchange ./ea-repo --out enterprise.xml
python3 ~/.ai/it-role-house/tools/repository.py portfolio ./ea-repo --format md --out portfolio-architecture.md
```

The runtime performs structural and semantic consistency checks of the
EA projection model and validates the supported Open Exchange envelope
with
the packaged XSD before L2 semantic and L3 round-trip checks. The
packaged schema is a deliberately supported portability envelope, not a
claim of certification by The Open Group or any commercial EA tool.
Vendor-specific certification remains an external qualification step
when required.
