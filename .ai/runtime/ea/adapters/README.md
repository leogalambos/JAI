# Repository adapters — 26.10.4

AI IT House 26.10.4 uses the JSON repository as the authoritative
architecture-domain projection store. JAI remains the global semantic
identity authority. Repository adapters move governed model facts across
tool boundaries and must not silently create, rename or reinterpret
architecture facts.

The built-in adapter is **Open Exchange file interchange** through
`tools/repository.py`:

- `export-open-exchange` produces portable ArchiMate 3.x Model Exchange
  XML with elements, relationships, properties and diagram views;
- `import-open-exchange` ingests that exchange into the governed EA
  projection repository and retains unknown/custom properties;
- `generate-views` creates deterministic published view sets (JSON +
  SVG) from governed EA projection facts;
- `validate`, `impact` and `portfolio` apply repository and portfolio
  consistency rules before release.

Vendor APIs remain explicit extension points. A future adapter may call
a particular repository product, but it must preserve stable IDs,
evidence/provenance and lifecycle state and must report any semantics it
cannot round-trip.
