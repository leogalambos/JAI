# HISTORICAL: imported 26.10.4 qualification

This record is not current release authorization.

# Validation and release controls

AI IT House {{ JAI_VERSION }} ships with machine-readable release qualification in `QUALIFICATION-A-H.json`.

## Imported baseline qualification snapshot

The status below is the **historical qualification snapshot** shipped in the
incoming 26.10.4 integrated baseline; it is not a new A–H run over the
consolidated tree. Source changes, documentation generation and publication-policy
changes require a new qualification. For the current distribution, read
`QUALIFICATION-A-H.json` in the **exact candidate ZIP** and verify its status
against the tree that was actually qualified. Do not treat a historical PASS
as current release authorization.

- release: **26.10.4**
- generated at: **2026-10-06T23:27:09.112594Z**
- all pass: **True**
- publication state: **ready-for-release-owner-signature**

| Gate | Status | Main 26.10.4 checks |
| --- | --- | --- |
| A — Structural | PASS | 26.10.4 Unified Lifecycle native enforcement; current schema resolver; architecture authority/write-path lint; schema/referential integrity; artifact contracts/golden corpus; generated docs; policy; performance; release/version rules |
| B — Semantic | PASS | SABSA semantic runtime; SABSA→JAI-scoped EA profile; EA interoperability; EA domain-projection repository |
| C — Governance | PASS | authorities/workflow governance; immutable execution record; service objectives/reference SLA |
| D — Runtime Security | PASS | agent authority enforcement; provider parity; adapter mutation enforcement; GA regression; workload/model routing |
| E — Publication | PASS | projection contract; renderers; publication integrity |
| F — Visual | PASS | render-based visual QA |
| G — Behavioral | PASS | adversarial harness; golden-corpus threshold conformance **as fixture qualification** |
| H — Supply Chain | PASS | SPDX SBOM; compatibility; digest provenance; external-signing readiness; license; integrity self-test; final release policy |

## Gate G: what PASS does and does not mean

26.10.4 corrects an important ambiguity from the earlier baseline.

The universal release qualification asserts:

```text
harness + golden corpus + thresholds + adversarial evaluator
```

It explicitly records:

```text
provider_model_claim = false
```

Therefore **Gate G PASS is not a claim that a specific live Claude/Codex/OpenAI model currently achieves the thresholds**. A deployment that wants that statement must run the behavioral evaluation against captured live provider/model outputs and retain the typed qualification evidence manifest with provider/model identity and result hashes.

This distinction prevents reference fixtures from being presented as measured live-model evidence.

## Who initiates validation?

| Scope | Operator in Codex/Claude | Engineer/CI behind the scenes |
| --- | --- | --- |
| One consequential engagement | Ask `/fabric-report` (Claude) or `$workflow-fabric-report` (Codex) for evidence IDs, strict state, unresolved issues and authority actions. | Auditor executes `fabric.py status/report/verify/justify` as permitted; re-evaluates evidence drift and release eligibility. |
| Runtime regression after an upgrade | Ask an administrator for a validated installation or a failed-gate report. | Maintainer executes the Fabric self-test and the appropriate runtime checks in a system terminal. |
| Entire GA candidate | Maintainer pushes `release@YY.MM.VV`; no manual release approval follows. | Repository CI executes A–H, builds the ZIP and automatically publishes the Release. |
| Documentation publication | Reader follows the MkDocs Pages site or installed `GUIDE.md`. | CI checks Markdown links, generated guide synchronization and strict site build. |

**Separation of claims:** structural checks do not prove a model's domain correctness; fixture qualification does not prove live provider behaviour; a Fabric report does not itself grant human authority. Ordinary CLI work does not require manually launching the scripts in this release engineering page.

## Layered runtime validation

The Fabric has a separate **maintainer/CI self-test** (not a step for an end user in a layered session):

```bash
python3 ~/.ai/it-role-house/fabric/fabric.py selftest
```

The current self-test contains **45 checks**. It covers, among other things:

- typing and adjacency;
- review direction;
- strict evidence requirements;
- hash-chain tamper detection;
- rework exhaustion;
- reformulation uniqueness/ownership/budgets;
- upward-only escalation;
- sticky authority matters;
- human revision round behavior;
- context-digest mismatch;
- dependency invalidation;
- bounded worst-case termination.

A self-test passing proves the tested runtime invariants under the test fixtures. It does not establish the truth of arbitrary domain claims or non-bypassability of every external deployment path.

## Re-run enterprise qualification

For a developer or release engineer **in a system terminal**, from an extracted release tree:

```bash
python3 .ai/runtime/tools/release_ga.py qualify
```

## Machine-readable evidence and source-of-truth boundaries

For a release decision use the **authoritative files inside the published ZIP**, not hand-maintained documentation mirrors:

| Question | Authoritative evidence in the package |
| --- | --- |
| Did gates A–H pass? | `QUALIFICATION-A-H.json` (validate scope/date as well as flags) |
| What dependency/runtime versions are declared? | `COMPATIBILITY.json`, `.ai/runtime/models/model-registry.json` |
| What is the JAI normative layer set? | `.ai/runtime/jai/core/layers.json` |
| Who may authorize consequential actions? | `.ai/runtime/jai/core/authority-model.json` and the current managed policy |
| How does supervision escalate? | `.ai/runtime/fabric/supervision-policy.json` |
| What was corrected in this release? | `.ai/runtime/_meta/26.10.4-corrective-audit.json` and the controlled release qualification evidence |

Do not copy mutable release evidence into `docs/assets/`: archived duplicates can drift out of sync with the source-of-truth records and make source digests circular. Verify the ZIP against its published SHA-256 and the GitHub Release source tag. Where supported, verify its OIDC/Sigstore provenance attestation. A checksum without a signed attestation proves integrity only, not publisher identity. No manual release-owner signing step is required.

## Prior documentation QA results and their limitations

For context only, an earlier documentation assembly recorded these **historical** checks:
Fabric supervision self-test 45/45 PASS; native runtime enforcement 42/42 PASS;
74/74 MkDocs navigation entries resolved; 211 links/assets inspected;
six documentation evidence JSONs inspected; and 33 SVGs parsed.
Its strict MkDocs build and live browser screenshots were explicitly
**NOT EXECUTED** in that offline environment. Those records are a historical
baseline, **not** results of running the newly consolidated project tests.
Temporary PNG/browser QA previews are not runtime inputs. The published documentation retains its production SVG diagrams in `docs/assets/`; qualification must be rerun on the delivered source tree.

For changes verify maintained Markdown sources and the published-site build:

```bash
python3 .ai/runtime/tools/docs_contract.py --root .
python3 .ai/runtime/tools/generate_docs.py --check --root .
python3 -m mkdocs build --strict
python3 .ai/runtime/scripts/check_agent_policy.py --fast .
```

The internal schema/object/Fabric hashes enforce identity, change detection
and traceability, while an optional CI attestation authenticates the
**whole final ZIP**. They serve different purposes; removing the checksum-list
file does not disable internal integrity enforcement. A recorded gate PASS on
an earlier release tree should be requalified after source changes.

## Supply-chain separation

The release workflow builds a ZIP after A-H qualification and publishes it with a `.sha256` checksum. GitHub Actions produces a keyless OIDC-signed attestation where the repository plan supports it; otherwise release assets retain SHA-256 and embedded SBOM/digest provenance. No operator signature or secret signing key is needed.

## Implementation details

[Current hooks and Gate A implementation](../configuration/hooks-gates-verification.md) describes the inspected implementation.
See the sequential modular Gate A, report validation limits and current source/full-release workflow boundary.
