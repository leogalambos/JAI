# SABSA-related delivery profile


**JAI governed architecture delivery, version 1** is a local delivery profile
informed by the identified SABSA publications below. It is not an official SABSA
specification, a complete transcription of proprietary material, or a
certification claim. The [layer model](../architecture/sabsa-layer-model.md)
defines process and authority. The
[content contract](../architecture/governed-sabsa-content.md) specifies its
semantic representation, and the [operator guide](../operations/sabsa-content.md)
explains versioned authoring, assessment, and documentary views. Structural
completeness does not widen the external-source or conformity claims below.

## 1. Normative source and applicability gate

Distinguish three sources of obligation:

1. The engagement's attributable L0 requirements define the requested outcome and reserved constraints.
2. An identified external source defines the SABSA method/content obligations actually requested. Record its publisher, title, edition/revision, accessible authoritative location, permitted use, and the clauses or information units adopted. An independently checked authoritative copy or approved source record is required; a remembered framework description is insufficient.
3. This versioned JAI profile defines additional delivery, traceability, assurance, and publication rules. Its requirements are local JAI decisions and must not be attributed to SABSA without source support.

The selected method sources are:

- **S1**, SABSA Institute Academic Board, *SABSA Matrices 2018 Release Notes*, TSI-R101, Release 1.0, June 2018: [version-pinned mirror](https://github.com/yasenstar/ArchiMate_SABSA/blob/f2df225396a8c00e6cb3c5f9b3fae52038996742/Docs/TSI-R101-SABSA-Matrices-2018-Release-Notes.pdf). This governs matrix terminology and the architecture-artefact versus management-activity distinction in this profile.
- **S2**, John Sherwood, Andrew Clark, and David Lynas, *Enterprise Security Architecture*, TSI-W100, copyright 1995–2009 SABSA Limited: [version-pinned mirror](https://github.com/yasenstar/ArchiMate_SABSA/blob/0bb1023ad1f2f6f006e5b460c593eb3aebf43a2b/Docs/TSI-W100-SABSA-White-Paper.pdf). This supplies introductory layer, lifecycle, business-attribute, and assurance explanations; S1 takes precedence where it updates the matrix.

These citations identify the publications and the exact copies referenced by
this profile. Primary authorship concerns their content; the mirrors are not
represented as publisher-authorized distribution or as an assertion that no
later edition exists.

| Source location, printed pages | Supported method distinction | JAI-specific decision, not attributed to the source |
| --- | --- | --- |
| S1, 2–3 | Management Architecture broadens the older service-management name; the architecture matrix describes artefacts and the management matrix describes activities. | L6 is a governed crosscutting processing identity, with explicit activity definitions and observations. |
| S1, 4–5; S2, 10–13, 15 | Business/risk/value/process justification, six-question perspectives, and bidirectional traceability. | Local setter/author/reviewer assignments, integration review, protocol, and authority checks. |
| S2, 8–9, 14, 16–17 | The service-management/Inspector perspective is pervasive across the other five views. | Management feedback is neighbor-relayed without making L6 a terminal evidence-only stage. |
| S2, 18 | Contextual/conceptual signoff precedes productive detailed work; operational design begins early and lifecycle feedback continues. | Exact versioned baselines, pause/speculation policy, and bounded revision gates. |
| S2, 19 | A tailored Business Attributes Profile belongs to conceptual architecture; example attributes are not an exhaustive mandatory taxonomy. | A required versioned profile and measures in the selected JAI engagement scope. |
| S2, 22–23 | Risk/opportunity and assurance concern the architecture across its views and stages. | Exact evidence/review roles, completeness reporting, and release eligibility. |

These sources support the distinctions above. They do not establish an
exhaustive current SABSA deliverable standard or completeness of the local
nineteen-view catalogue. This profile supplies explicit JAI delivery obligations;
independent subject review assesses their sufficiency for the selected engagement.

Use bibliographic attribution, links, and original paraphrased design. Do not
vendor source PDFs, reproduce figures/templates, or infer unrestricted
redistribution rights from access to a mirror. Reproduction requires a recorded
permitted-use basis. This profile makes no legal conclusion about mirror
distribution rights.

**Source adequacy is scope-specific.** An engagement may select the cited matrix
and white paper together with this local profile after independent subject
review and entitled scope acceptance. If it requests a fuller, newer,
proprietary, or certification-specific SABSA obligation, obtain the additional
authorized source before claiming completeness. Missing source material blocks
that claim; the local matrix or catalogue cannot silently replace it. Narrowing
the requested scope requires an explicit entitled decision.

The source register stores public bibliographic references where suitable; confidential sources and their identifying provenance remain in private records. Public documentation must not expose private input identifiers. The profile selects source requirements by stable reference without publishing licensed source content unnecessarily.

## 2. Engagement profile

Before substantive work, the entitled setter records a versioned engagement profile containing:

- requested architecture scope, stakeholders, decision purpose, and lifecycle horizon;
- selected external method sources and JAI profile versions;
- included layers and question coverage, required detail, evidence, and quality criteria;
- required information units, relationships, views, documents, and operational outputs;
- boundaries, dependencies, approved exclusions, and their entitled decision owners;
- publication audiences, confidentiality, source-use restrictions, and acceptance/release authority.

A general JAI engagement may select a proportionate subset. An engagement requesting SABSA deliverables must satisfy its selected method requirements and agreed scope; it cannot silently use a lighter generic profile. All six questions remain accounted for, even where a justified exclusion is permitted. The word "complete" always names the profile, source scope, and output versions against which it was assessed.

## 3. Required information-unit baseline

The following is the **JAI minimum** for this profile. It does not attribute this
exact document list to SABSA. Source mapping and substantive sufficiency require
independent subject review for the engagement's adopted scope.

| Layer | What / Why | How / Who | Where / When |
| --- | --- | --- | --- |
| Contextual | Assets, business information, drivers, opportunities, constraints, required business qualities, measurable outcomes. | Business activities, stakeholders, accountable owners, authority and risk boundaries. | Business environments, jurisdictions, locations, time horizons, events, and critical periods. |
| Conceptual | Architecture concepts, objectives, protection needs, principles, a tailored Business Attributes Profile with targets, and their business justification. | Strategies, domains, trust, policy concepts, ownership, and governance responsibilities. | Conceptual boundaries, inter-domain relationships, lifecycle stages, and relevant timing principles. |
| Logical | Logical information structures, service needs, control objectives, and traceable requirements. | Technology-independent services, functions, interactions, actors, and authorization responsibilities. | Logical placement and trust boundaries, event flows, ordering, schedules, and timing constraints. |
| Physical | Realization choices, information/resource arrangements, mechanisms, and selection rationale. | Concrete processes, technologies, integrations, organizational arrangements, and operating responsibilities. | Deployment topology, physical/organizational locations, environments, sequencing, and timing mechanisms. |
| Component | Components, interfaces, configurations, dependencies, implementation specifications, and requirement satisfaction. | Detailed realization, build/configuration procedures, component ownership, and verifiable behavior. | Packaging/placement, execution environments, release dependencies, initialization, schedules, and interface timing. |
| Management, including operational/service management | Managed architecture/service assets, required attributes, governance and service objectives, measures, and improvement needs. | Governance, assurance, operation, monitoring, support, incidents, change, maintenance, resilience, accountable teams, and escalation. | Coverage across the other five layers, operating locations, lifecycle stages, service windows, review/recovery periods, events, and feedback cadence. |

For each required information unit, retain its semantic owner, exact version, governing requirement, rationale, dependencies, evidence obligations, review, and applicability. A heading or populated field does not demonstrate an adequate answer. Missing evidence or an unresolved conflict remains visible.

## 4. Relationships and documentary views

Every selected realization must have an explicit justification path through the applicable architecture levels to a business driver, required attribute, or entitled obligation. Include contextual requirements → conceptual objectives → logical services/controls → physical mechanisms → components → operational controls/measures, with evidence and decisions at the appropriate points. Preserve legitimate many-to-many mappings rather than forcing one document per cell.

Backward traceability answers why an element exists; forward traceability answers where an obligation is realized and measured. Required but unrealized obligations, unjustified controls, missing measures, contradictory assumptions, and changed dependencies appear in the completeness report. A dependency on an existing version is distinct from a proposed design relationship to a future element.

The local catalogue `.ai/runtime/sabsa/schema/documents.json` groups its views
into these families:

| Family | Views and purpose |
| --- | --- |
| Architecture and audience views | Architecture, executive summary, current state, target state, transition architecture, client questions. |
| Policy, risk, and trust | Risk treatment plan, policy architecture, trust model, information/access model. |
| Realization and assurance | Security service catalogue, component realization, assurance plan. |
| Governance and lifecycle | Governance register, transition roadmap, lifecycle register, reuse register. |
| External relationship views | Framework mapping and compliance gap analysis. |

These grouped names inventory the nineteen-view catalogue; they do not establish
its completeness or make every view mandatory for every engagement. The selected
engagement profile maps each required information unit and relationship to one
or more views, with required audience and detail. Requested source-specific
products absent from the catalogue require an additional governed view or an
explicit entitled scope decision.

The tailored Business Attributes Profile is a required conceptual information product under this JAI profile, whether rendered as its own view or as an explicitly identifiable part of another approved publication. Do not lose it merely because the current local catalogue lacks a standalone view name.

Management activities are accounted for across the contextual, conceptual, logical, physical, and component perspectives, not only production operation. Each required activity has an objective, responsible actor, inputs/outputs, applicable scope, trigger/timing, controls, and evidence obligation. Activity definitions and their execution observations are distinct records.

Management/operational content is represented throughout those views and, where needed, by additional governance/assurance procedures, service responsibilities, monitoring/measurement definitions, incident/change/recovery arrangements, and review schedules. Actual execution and effectiveness require observations; design documents alone do not establish them.

Documents are deterministic or controlled editorial views of governed semantic versions. Publication cannot create a second source of authority or introduce unsupported claims. A changed document that alters meaning must return to its semantic owner and review route. Preserve evidence links and constraints in audience-appropriate form without exposing confidential source material.

## 5. Optional ArchiMate representation

ArchiMate is a selectable representation profile for engagements that require it, not a mandatory implementation language for every JAI task. Native semantic records retain the authoritative information and provenance; a representation cannot silently redefine the source's meaning.

A project may select ArchiMate as its default when its recipients use the notation,
the views answer explicit stakeholder concerns, a governed source model supplies
stable identities, and the exact edition, mapping and renderer have an evidenced
qualification scope, including the receiving tool when one is used.
Independently assess semantics and visual
notation for the published version. An explicit request activates this selection
process; it does not make an unqualified draft conformant. A generic repository
graph is labelled as such and is not presented as an ArchiMate notation view.

Choose the representation to serve the decision: an ADR or principle register
does not require an EA diagram, and executive, operational and software views
may use text, tables or other suitable notations. ISO/IEC/IEEE 42010:2022 does
not prescribe a particular notation or tool.

Edition qualification is explicit. The portable implementation targets language
3.2 and exchange schema 3.1; publication of ArchiMate 4 does not establish
support for its changed metamodel or exchange format. No external EA
application or virtual display is a prerequisite for the portable JAI
workflow. Optional external-tool qualification
must identify the exact tool and supported edition. Internal exchange tests do
not establish vendor interoperability, and a successful 3.2 import cannot qualify
version 4. Follow the maintained [portable ArchiMate procedure](../capabilities/sabsa-ea.md#portable-archimate-32)
for explicit requests, helper operations and separate validation boundaries.

The selected mapping reference is **S3**, Steven Bradley, *Modelling SABSA with ArchiMate*, TSI-T100, Release 1.0, October 2019, SABSA Press, approved by the SABSA Institute Trustees: [version-pinned mirror](https://github.com/yasenstar/ArchiMate_SABSA/blob/55eff9fcc67ab022fcec27093990fb85dbeb509a/Docs/TSI-T100-Modelling-SABSA-with-ArchiMate.pdf). Its declared target is ArchiMate 3.0; do not infer conformance to another edition from that mapping.

The engagement selects an exact ArchiMate edition and mapping version. Independently validate native SABSA content and legal ArchiMate concepts/relationships for that edition. Preserve stable cross-references, documented mapping decisions, loss/unrepresented-information reports, and evidence links. A required information unit that cannot be represented in a chosen diagram must appear in an authorized complementary view, or remain a blocking gap. Diagram validity is not business or SABSA completeness.

The practitioner site [ArchiMate SABSA](https://yasenstar.github.io/ArchiMate_SABSA/) is informative discovery/practice material. It is not the source of authority for the method. A later Open Group guide, G24B, is discoverable through publisher metadata, but its full content has not been assessed for this profile. It is not silently substituted for S3; an engagement requiring it must supply and assess an authorized copy and its applicability.

## 6. Content acceptance and evidence

Independent subject review assesses whether the chosen source obligations and information-unit catalogue are appropriate and sufficient for the requested scope. Record the reviewer's assigned competence and any limitations; a role label or schema pass does not establish expertise.

For each delivered scope, the completeness report records:

1. Selected source/profile versions and the entitled scope decision.
2. Required information units, relationships, and publication views, including their layer/question assignments.
3. Exact current semantic versions and the local professional/integration review evidence.
4. Forward/backward traceability, evidence sufficiency, contradictions, and unresolved gaps.
5. Explicit exclusions with authority, rationale, consequences, and expiry/review condition where applicable.
6. Receiving-use acceptance, required human acceptance, and release permission as separate statuses.

Reject a requested product when required source content, unit, relationship, review, evidence, or publication is missing. Do not replace this assessment with a cell count, filenames, smooth narrative, or agreement between agents. An unverified operating assumption must remain distinguishable from measured service performance.

Review challenges unjustified realization, unrealized obligations, inconsistent
question answers, unsupported exclusions, absent operational measures, changed
required inputs, and documents that disagree with their semantic source.
Required source obligations remain binding throughout delivery.
