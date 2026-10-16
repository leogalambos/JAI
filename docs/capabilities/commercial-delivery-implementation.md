# Commercial delivery implementation status

This page describes source capabilities and their acceptance boundaries. It is not a deployment certificate. Source validation, operational qualification and human approval are separate decisions; a passing local test does not establish that a live Codex or Claude deployment enforces the required isolation.

**Owner:** JAI maintainers. **Last reviewed:** 16 October 2026.

Start with [commercial delivery](commercial-delivery.md) for practical usage and [methodical workflows](../using/methodical-workflows.md) for the distinction between domain workflows and six-layer execution. Private conversations, internal review ledgers and unpublished implementation archives are not prerequisites for understanding this page.

## Source capabilities and acceptance boundaries

Source paths below are relative to `.ai/runtime/`. An implementation entry identifies where a capability is provided; it does not establish acceptance of a particular engagement.

| Capability | Source entry point | Acceptance boundary |
| --- | --- | --- |
| Lifecycle and discovery | `tools/commercial_core.py`, `tools/commercial_lifecycle.py` | Stage gates check required inputs. Accountable owners review business meaning, assumptions and contractual commitments. |
| Estimates and progressive learning | `commercial_economics.validate_estimate`, `learning_update` | Estimates retain provenance and uncertainty. Public benchmarks require relevance review. Delivery observations support revised estimates; humans approve scope and contractual changes. |
| Pricing and financial scenarios | `commercial_economics.price_quote`, `uncertainty_analysis`, `cashflow` | Decimal calculations support decisions. Finance and legal owners approve accounting, tax, payment and contractual assumptions. Unsupported distributions must not be presented as calibrated confidence levels. |
| Resource and service planning | `capacity_plan`, `service_sizing`, `tools/commercial_scheduler.py` | Calendar and roster checks depend on realistic demand, availability and skills. SLA and queue assumptions need calibration. Structural validity does not establish operational sufficiency. |
| Change and run economics | `classify_quantity`, `map_classification`, `forecast` | Effort and money can use mapped classifications. Accounting-master integration requires controlled identifiers and reconciliation. |
| Customer and internal information | `commercial_core.project` | The supported customer projection is allowlisted JSON with mandatory disclosure. Other surfaces are rejected. Disclosure suitability and inference risk still require review. |
| Traceability and change impact | `trace`, `impact`, `SnapshotStore`, profile bindings | Claims require specific source and fragment bindings and an actual Fabric resolver. Report references are insufficient. Standalone `/sabsa` work does not create a six-layer execution history retroactively. |
| Independent review and readiness | `readiness`, `incorporate_response`, execution gate | Maker/checker identities and execution boundaries require host authentication. Different identity strings supplied in a document are insufficient evidence of independence. |
| Snapshot approval | `commercial_lifecycle.assess_axes`, `approve_snapshot`, `transition` | Review and approval bind to a particular snapshot. Changes can invalidate readiness. The runtime cannot manufacture a human authority act. |
| Routing and consultations | `tools/commercial_router.py`, root catalog and domain shards | Lazy routing selects task-relevant material and supports bounded cross-domain consultation. Smoke tests do not establish independent benchmark quality, provider costs or context isolation. |
| Provider capabilities | Commercial capability registry and readiness checks | A capability declaration is not qualified enforcement. Live provider and negative tests are needed before claiming equivalent execution guarantees. |
| Monitoring and recovery | Monitoring, forecast, snapshot and archive APIs | Stop-loss, exit and risk acceptance remain human decisions. Archive restoration does not establish operational recovery readiness or recovery objectives. |

## Specialist responsibility

Five dedicated supplier-side specialisations complement the wider library: Bid / Proposal Manager, Commercial Pricing / Deal Finance Specialist, Estimation / Cost Engineering Specialist, Independent Commercial Assurance Reviewer and Supplier Commercial / Deal Manager. These are professional knowledge and responsibility contracts served by role operators, not five additional agent processes. Review remains separate from authorship.

Use the [release inventory](../reference/inventory.md) and [coverage matrix](../overview/coverage-matrix.md) for current totals and identifiers. The `/commercial` installation surface is distinct from the canonical workflow-chain registry. Model selection uses the existing model registry.

## Maintainer implementation plan

The shipped `.ai/runtime/commercial/implementation-plan.json` and `tools/commercial_plan.py` describe implementation of the **JAI extension itself**. They are not a client's proposal, project schedule or delivery estimate. The checker tests plan structure and acyclicity, not completeness, implementation quality or release acceptance.

The plan covers activation, lifecycle, discovery, estimates, economics, scheduling, traceability, snapshots, acceptance gates, projections, monitoring, routing, provider capabilities, tests and documentation. Its task and requirement identifiers are maintainer cross-references. The capability descriptions above provide the public explanation without requiring an unpublished specification.

## Reproducing source checks

From a repository checkout with the project's development prerequisites installed, run:

```bash
python3 -m unittest discover -s tests -p 'test_commercial*.py' -v
python3 -m mkdocs build --strict
```

These are repeatable checks, not a report of a test run performed for this page. Record the checkout revision, command, exit code and skipped or blocked checks when reporting results. See the [runtime tools reference](../reference/runtime-tools-detailed.md) for wider validation and qualification tooling.

## Operational qualification

Treat live Codex/Claude execution, context/tool/mount isolation, host-authenticated maker/checker separation, deployment recovery and customer acceptance as **NOT_RUN until supported by evidence from the target environment**. Local fixtures and mock-provider results do not replace those observations. Missing evidence leaves the affected gate unqualified.

Source checks establish bounded software behaviour. Business correctness, source licensing, semantic relevance, financial policy, legal commitments and authority acceptance require their respective accountable owners. This applies equally to a proposal and to its subsequent delivery.
