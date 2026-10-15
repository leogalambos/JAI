# SABSA narrative publication authoring contract

English publication profiles define six distinct documents: business context and
security governance; security concept and control objectives; logical security
architecture; physical security design; component engineering specification; and
service operations and assurance. Their chapter structures follow each SABSA
viewpoint's semantics. Controlled typography and document metadata support those
views without imposing organisational policy or conflating document governance
levels with architecture layers.

## Author the semantic document before rendering

```sh
python3 .ai/runtime/tools/sabsa.py narrative-init LIB --layer logical
python3 .ai/runtime/tools/sabsa.py check LIB
python3 .ai/runtime/tools/sabsa.py document LIB --layer logical --out logical.md
python3 .ai/runtime/tools/sabsa.py document LIB --layer logical --out logical.tex
python3 .ai/runtime/tools/sabsa.py document LIB --layer logical --out logical.docx
python3 .ai/runtime/tools/sabsa.py document LIB --layer logical --out logical.pdf --latex
```

`narrative-init` creates missing chapter skeletons, preserving existing files. Each
profile under `profiles/` defines its chapter keys and typed specification groups.
Authors write paragraphs in `LIB/narratives/LAYER/CHAPTER.md`, with this front matter:

```yaml
---
basis: stated
source: 00-sources/brief.md#decision
author: Architecture working group
language: en
---
```

The body is authored
Markdown prose without a duplicate chapter heading. Explain purpose, scope, decisions,
alternatives, constraints and consequences using the cited sources. State proposed
requirements as proposals until the relevant authority approves them. Do not copy
normative claims or legal applicability from example documents. `basis` is `stated`,
`inferred` or `assumed`; stated/inferred material requires an existing in-library
source. Unconfirmed assumptions remain warnings. Record the responsible author.

All publication prose is authored in professional English. The deterministic renderer
does not translate or rewrite authoritative content. Retain original-language sources
in `00-sources/`; authors produce and review English architecture entries and chapters,
citing the originals. `language: en` declares the author's reviewed English text.
Explicit non-English declarations produce visible edition gaps rather than silent
translation. Proper names, identifiers and quoted terms retain their meaning.

Element Markdown bodies carry complete design rationale, operating procedures and
verification instructions. Publications reproduce those bodies, every public metadata
field, typed dependency targets, and business justification paths with relationship
names. Supporting dependencies remain distinct from business justification. Missing
required references, type mismatches, cycles, missing prose and source scaffolding
remain visible authoring gaps. No requirement, implementation result, exception or
approval is inferred from a blank field.

Narrative files are semantic inputs: `check` validates provenance; source registers
include their citations; snapshot hashes and approval cover their exact bytes. Adding,
editing or deleting authored prose invalidates a prior approval. Publication profiles
and typography remain projections of this source. Missing viewpoint narrative or
unreviewed language prevents an approved publication presentation, even where an older
architecture approval exists.

## Publication and limitations

LaTeX/PDF requires Pandoc, XeLaTeX, its normal article/font/table packages and DejaVu
Serif. Word generation requires Pandoc and produces a controlled cover and a populated,
clickable contents list without invented page numbers. LibreOffice or Word can render
and independently inspect the resulting DOCX. English boilerplate is generated;
authored facts are never fabricated. The source register wraps citations as individual
items. Trace presentation is bounded at 128 paths per specification and reports the
limit explicitly; canonical dependencies remain available for further analysis.

The reusable fictional example is `example.json`; generate it in a fresh directory:

```sh
python3 .ai/runtime/tools/sabsa_publication_demo.py --out build/sabsa-publication-example --render
```

The six documents contain chapter prose, complete specifications, rationale and trace
paths. They explicitly describe a proposed, invented service. They make no claim of
real deployment, successful testing, legal compliance or owner approval.
