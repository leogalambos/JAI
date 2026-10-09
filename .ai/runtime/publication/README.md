# Enterprise Publication — 26.10.4

AI IT House 26.10.4 separates **semantic truth**, **audience
projection**, and **rendered publication**.

`semantic model → publication profile → ProjectionManifest v3 →
publication model → renderer → render-based visual QA → approval →
release`

## Integrity model

Three independent SHA-256 values are used: the **semantic hash**
identifies the canonical truth model, the **projection hash** identifies
the audience-specific publication model, and the **render hash**
identifies the exact published file. `tools/projection.py` enforces 100%
mandatory coverage unless every omission is explicitly justified;
`tools/publication_integrity.py` validates the publication model against
that manifest.

## Enterprise profiles

Thirteen first-class profiles are provided: Executive One-Pager,
Decision Paper, Architecture Review Board Pack, Architecture Definition,
Solution Design/HLD, Detailed Design/LLD, Risk & Assurance Pack,
Implementation Specification, Migration & Cutover Pack, Operational
Handover, Roadmap, Benefits Review and Audit/Compliance Evidence Pack.
Profiles define audience, maximum detail, mandatory sections and
semantic fields, diagrams, tables, document control, classification,
approval, branding, accessibility and output formats.


## Unified Lifecycle production boundary

A production render is no longer permitted from an arbitrary publication
model. `tools/projection.py build` first creates a JAI-lineaged
`publication-model.json` and `projection-manifest.json`;
`tools/publication.py render` requires that manifest, verifies the
projection hash and L1–L6 lineage, and writes `render-evidence.json`
with per-format SHA-256 hashes and QA results. Legacy material remains
readable, but it is not a production write path.

## Native outputs

`tools/publication.py` produces HTML, DOCX, PDF, PPTX, XLSX and SVG. PDF
is a first-class renderer using LibreOffice/soffice.

## Render-based Visual QA v2

`tools/visual_qa.py` renders DOCX/PPTX/XLSX/HTML/PDF/SVG into visible
page images and checks release-critical conditions including blank
output, clipping/edge overflow, broken rendering and excessive density.
The acceptance corpus contains 120 valid and 120 seeded-defect cases;
the deterministic critical-defect gate requires ≥95% recall and ≤10%
false positives. Source/package checks in `publication.py` remain
complementary.

## Runtime enforcement

Publication reviewers and authors are governed by Agent Contract v2 and
managed enterprise policy. Reviewer mutation, self-approval, unapproved
policy mutation and restricted-MCP shell bypass are negative-test cases
in the release qualification suite.
