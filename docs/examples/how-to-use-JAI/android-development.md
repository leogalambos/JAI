---
owner: JAI documentation maintainers
review_due: 2027-01-16
---

# Keep Android development aligned with SABSA

Owner: JAI maintainers. Last reviewed: 2026-10-20.

## Set up the development workspace

ACME is building an Android personal check-in application. Alice owns the
product and Bob develops the application. Users may choose to notify a
trusted contact when a check-in is missed; consent and contact information
therefore matter to the business design. This familiar mobile setting is
fictional; identities and business requirements must come from your
actual project inputs.

Create a new project directory named `acme-safety-app/` with `input/`,
`working/` and `output/`. Place the real application checkout under
`app/`; do not treat an empty directory as an implemented application.
The existing `app/sabsa` prompts below refer to architecture material
associated with that checkout. Ask JAI to report actual artifact paths
instead of assuming a command creates a particular file.

Supply:

- `input/product-brief.md`: user tasks, supported devices, notification
  behavior and the business reason for the application.
- `input/data-map.md`: contact information stored on the device,
  notification history, retention and the backend boundary.
- `input/platform-constraints.md`: Android support policy, identity
  integration, device management and available test environments.
- `input/acceptance-cases.md`: observable outcomes, including failed
  notifications, consent withdrawal, shared devices and account changes.
- `app/`: source, dependency definitions and maintained build/test
  instructions for the existing application or agreed starter project.

Put scope, accountable ownership and handling rules in `PROJECT.md`.
If a backend API contract is absent, request it and keep integration
claims provisional. A synthetic API fixture can support local tests;
it cannot establish compatibility with a deployed backend. Do not use
real contact or customer records merely to make a tutorial realistic.

Install the appropriate adapter using the
[installation guide](../../getting-started/install.md), then start Claude
Code or Codex in `acme-safety-app/`. Enter the command pairs below in the
provider conversation. Choose one provider and keep the same project
conversation as you move between business analysis, SABSA and development.
Check the reported scope and outputs between steps. Neither adapter
automatically turns a product brief into an approved security design.

Consider a fictional Android app that helps a user keep a personal check-in routine. The user may choose to notify a contact when a check-in is missed. The team needs to protect contact information, make consent understandable and explain what happens when the phone, process or network is unavailable.

You will use JAI to connect those needs to security architecture, implement a bounded increment, review discrepancies and prepare an evidence-based release decision. This is an architecture-and-development exercise, not a complete Android coding course. The goal is to keep requirements, code and evidence consistent as the product changes.

## Choose the assurance arrangement

This case uses **domain work followed by a layered decision**, as explained in [the methodical workflow guide](../../using/methodical-workflows.md). Steps 1–6 establish and reconcile the architecture and one code increment using `/sabsa` and `/develop`. Step 7 explicitly uses `/layered` for a different question: whether a named candidate is ready for release. Step 8 publishes architecture views; publication does not replace the release decision.

Unlike the [security-assessment case](security-assessment.md), which stops at assessment, this exercise includes a release-readiness question. That is why `/layered` appears later here. It is neither an omitted architecture command nor a universal final check for every SABSA activity. The domain workflows already require separate authors and reviewers; the layered decision adds contracts, upward review, bounded recovery and escalation for its own scope.

If the creation process must itself have a six-layer history, choose this alternative **before** step 1:

=== "Claude Code"

    ```text
    /layered Create the security architecture and realise the bounded consent
    increment using sabsa-library and the development workflow. Preserve
    adjacent contracts, independent author/reviewer roles and actual test
    evidence. Reserve product claims, risk acceptance and release authority
    for the named human owners.
    ```

=== "Codex"

    ```text
    $workflow-layered Create the security architecture and realise the bounded
    consent increment using sabsa-library and the development workflow.
    Preserve adjacent contracts, independent author/reviewer roles and actual
    test evidence. Reserve product claims, risk acceptance and release
    authority for the named human owners.
    ```

The orchestrator then uses the activities below as checkpoints inside that engagement. Do not start duplicate domain engagements. The default two-stage exercise below remains useful when its scope meets your assurance policy.

## Understand the workflows before you start

The **SABSA workflow** establishes business drivers, measurable attributes, risks, objectives and security services, then maps them into physical mechanisms, components and operational assurance. Its architect authors the model and an independent reviewer checks suitability and provenance.

The **development workflow** turns a reviewed implementation plan into code and tests. Its author and reviewer have different responsibilities. The **layered workflow** addresses a consequential decision using the architecture and actual implementation evidence, escalating matters that require human authority.

Keep a project brief, the app repository and permitted supporting material available. Name the product owner and the people accountable for privacy, safety-related claims and release. Describe intended users, data flows, failure consequences and the next increment. A check-in app must not acquire a life-critical promise merely because the architecture sounds reassuring; real claims and legal applicability need appropriate assessment.

## Run this scenario in the provider CLI

Use the prompts in your existing Claude Code or Codex project conversation. Each tab contains one complete request for that provider. **Operator:** define the increment, supply decisions and inspect evidence. **Behind the scenes:** JAI routes architecture, implementation and independent review, invokes permitted checks and reports unavailable prerequisites or unresolved decisions. An unperformed device test remains missing evidence.

## 1. Derive business drivers from the brief

Begin with the user outcome rather than an implementation preference. “Protect the contact details entrusted to the app” describes a business need; “use an encrypted database” chooses a mechanism before its context is understood. Notification dependability also needs a failure model, including power loss, process suspension and network unavailability.

The SABSA `prepare` activity inventories the brief, current code, documentation and relevant platform sources. These sources support different claims: documentation describes intent; code and tests can demonstrate narrower implementation behaviour.

**Expected output:** a source register, business drivers and questions for the owner. **Checkpoint:** product claims, known behaviour and assumptions are distinguishable before security requirements are derived.

=== "Claude Code"

    ```text
    /sabsa prepare app/sabsa — use PROJECT.md, the app repository and supplied
    documentation. Identify intended users, benefits, failure consequences,
    privacy expectations and permitted product claims. Inventory sources,
    derive business drivers and distinguish intended behaviour, observed
    implementation and assumptions. Turn unsupported safety, legal and
    platform claims into explicit questions.
    ```

=== "Codex"

    ```text
    $workflow-sabsa prepare app/sabsa — use PROJECT.md, the app repository and
    supplied documentation. Identify intended users, benefits, failure
    consequences, privacy expectations and permitted product claims. Inventory
    sources, derive business drivers and distinguish intended behaviour,
    observed implementation and assumptions. Turn unsupported safety, legal
    and platform claims into explicit questions.
    ```

## 2. Make security outcomes measurable

Create attributes and objectives before selecting Android mechanisms. A notification-timeliness measure needs a defined start event, delivery boundary and operating conditions. Successfully queuing a message is not evidence that its recipient received it. Targets require a justified owner decision, not an invented number.

Logical services translate those outcomes into technology-independent responsibilities. A consent service might prevent optional monitoring from starting before the required choices are recorded. A contact-data service might limit which actors can read stored contact details. Neither yet prescribes a screen, storage API or server product.

**Expected output:** measurable attributes, risks, objectives, policies and services with typed business links. **Checkpoint:** the reviewer can identify how each outcome would be tested and which targets remain undecided.

=== "Claude Code"

    ```text
    /sabsa create app/sabsa — derive the attributes, risks, objectives and
    logical services for the next increment in dependency order. Explain
    notification failure modes, consent, contact-data protection and user
    control. Propose metrics and evidence sources without inventing achieved
    values or agreed targets. Keep requirements technology independent and
    independently review each dependency stage.
    ```

=== "Codex"

    ```text
    $workflow-sabsa create app/sabsa — derive the attributes, risks,
    objectives and logical services for the next increment in dependency
    order. Explain notification failure modes, consent, contact-data
    protection and user control. Propose metrics and evidence sources without
    inventing achieved values or agreed targets. Keep requirements technology
    independent and independently review each dependency stage.
    ```

## 3. Define one implementable increment

Use consent as the first teaching increment. The physical design explains the mechanism; the component design identifies screens, stored state, interfaces and configuration; operational design identifies evidence and support needs. The precise choices depend on the real product and platform constraints.

Connect model IDs to code locations, normal behaviour, failure cases and acceptance evidence. “Implement privacy” is too broad. Preventing monitoring from starting when required choices are absent, and checking persistence and revocation behaviour, gives engineering and review a bounded task.

**Expected output:** a realisation plan and proposed target specifications. **Checkpoint:** existing code is not marked as implementing the target until supporting evidence is inspected.

=== "Claude Code"

    ```text
    /sabsa create app/sabsa — propose the Physical, Component and Service
    Management design for the consent increment. Map the reviewed consent
    service to app components, persisted state, interfaces and operational
    evidence. Identify affected model IDs, code locations, normal and failure
    cases, and acceptance evidence. Separate the proposed target from observed
    current code and identify decisions needed before implementation.
    ```

=== "Codex"

    ```text
    $workflow-sabsa create app/sabsa — propose the Physical, Component and
    Service Management design for the consent increment. Map the reviewed
    consent service to app components, persisted state, interfaces and
    operational evidence. Identify affected model IDs, code locations, normal
    and failure cases, and acceptance evidence. Separate the proposed target
    from observed current code and identify decisions needed before
    implementation.
    ```

## 4. Implement and review the increment

Switch to the development workflow when the implementation plan is ready. The SABSA architect maintains meaning and traceability; the engineering author changes code and tests. An independent reviewer assesses the implementation and its evidence.

A UI test can support a consent-flow claim, and a persistence test can support a stored-choice claim. Neither proves behaviour under every device power-management policy. Request the actual checks appropriate to the acceptance criteria, and keep unavailable build or device evidence explicit.

**Expected output:** scoped code changes, API documentation where appropriate, meaningful tests, execution results and independent review findings. **Checkpoint:** the reported results identify what actually ran and what remains unverified.

=== "Claude Code"

    ```text
    /develop Implement the reviewed consent increment in the app repository
    using its realisation plan and SABSA IDs. Preserve the agreed scope,
    document changed API contracts, add meaningful normal, boundary and
    failure tests, and run the available relevant build and checks. Report
    actual results, unavailable prerequisites and evidence locations. Have a
    different reviewer assess the change before proposing it as complete.
    ```

=== "Codex"

    ```text
    $workflow-develop Implement the reviewed consent increment in the app
    repository using its realisation plan and SABSA IDs. Preserve the agreed
    scope, document changed API contracts, add meaningful normal, boundary and
    failure tests, and run the available relevant build and checks. Report
    actual results, unavailable prerequisites and evidence locations. Have a
    different reviewer assess the change before proposing it as complete.
    ```

## 5. Reconcile a product decision across model and code

Suppose the owner decides that optional monitoring should be opt-in and default-off. First record that decision and its rationale. Trace dependencies before editing so a policy change does not leave services, mechanisms, components, tests and operating guidance inconsistent.

The architecture update identifies affected requirements and the realisation plan; the development workflow implements any necessary code changes. If the owner changes the target, preserve that history instead of presenting the new target as though it had always been the requirement.

**Expected output:** a recorded decision, impacted-element list and reconciled requirements/implementation plan. **Checkpoint:** use an actual owner decision in a real project; the fictional decision here is not an approval for your app.

=== "Claude Code"

    ```text
    /sabsa update app/sabsa — trace the monitoring and consent dependencies
    before editing. For this teaching scenario, record the proposed owner
    decision that optional monitoring is opt-in and default-off, with its
    rationale and pending authority status. In an actual project use the real
    decision source. Update affected requirements and the realisation plan,
    identify code and tests needing change, and preserve current versus target
    status until implementation evidence is checked.
    ```

=== "Codex"

    ```text
    $workflow-sabsa update app/sabsa — trace the monitoring and consent
    dependencies before editing. For this teaching scenario, record the
    proposed owner decision that optional monitoring is opt-in and
    default-off, with its rationale and pending authority status. In an actual
    project use the real decision source. Update affected requirements and the
    realisation plan, identify code and tests needing change, and preserve
    current versus target status until implementation evidence is checked.
    ```

## 6. Review drift independently

An architecture can become stale even when it was once correct. For example, a model may describe a configurable interval while code uses a fixed value, or documentation may name an old dependency or build target. Inspect the actual repository rather than copying a convenient version number from an example.

The reviewer identifies the discrepancy. The appropriate owner decides the intended behaviour. The relevant author fixes the design, implementation or documentation, and an independent reviewer verifies the result. Fix semantic entries and narrative before regenerating publications; editing only a generated PDF cannot reconcile the model with code.

**Expected output:** located inconsistencies, independently verified rework and current evidence. **Checkpoint:** distinguish design defects, implementation defects, stale documentation and missing evidence; a structural pass alone cannot demonstrate code conformance.

=== "Claude Code"

    ```text
    /sabsa review app/sabsa — independently compare the architecture with the
    supplied current code and execution evidence. Check product claims,
    configured behaviour, dependency/build facts and implemented controls.
    Record located inconsistencies, distinguishing design defects,
    implementation defects, stale documentation and missing evidence. Have the
    relevant authors rework them, then independently verify the changes.
    ```

=== "Codex"

    ```text
    $workflow-sabsa review app/sabsa — independently compare the architecture
    with the supplied current code and execution evidence. Check product
    claims, configured behaviour, dependency/build facts and implemented
    controls. Record located inconsistencies, distinguishing design defects,
    implementation defects, stale documentation and missing evidence. Have the
    relevant authors rework them, then independently verify the changes.
    ```

## 7. Prepare a bounded release decision

This starts a decision scope against the exact candidate and architecture snapshot. It does not retrospectively establish L1–L6 contracts or reviews for steps 1–6. Require the orchestrator to identify those snapshots and report the new decision engagement ID before assessing readiness.

A defensible architecture is one input to release readiness. The decision also needs a defined candidate, actual test and operational evidence, relevant conditions and an assessment of remaining exposure. Use layered delivery for that consequential judgement rather than treating the SABSA model as an automatic release verdict.

A legitimate result may be “not ready” or a proposal conditional on further device, notification, consent or accessibility evidence. The actual criteria determine the conditions. JAI prepares an escalation dossier where human authority is required; in Codex, the human inspects and executes the protected action in a trusted terminal.

**Expected output:** an evidence-based readiness assessment, explicit limitations and any required decision dossier. **Checkpoint:** unperformed work remains a condition, not a successful result, and a conversational agreement is not a recorded authority act.

=== "Claude Code"

    ```text
    /layered Assess release readiness for the identified app candidate using
    the reviewed SABSA model and actual implementation evidence. State the
    decision scope, separate observed results from planned tests and
    assumptions, and identify missing acceptance evidence. Escalate safety,
    privacy and risk matters beyond agent authority. Do not label the
    candidate ready to ship when conditions remain; prepare the exact human
    authority actions where required.
    ```

=== "Codex"

    ```text
    $workflow-layered Assess release readiness for the identified app
    candidate using the reviewed SABSA model and actual implementation
    evidence. State the decision scope, separate observed results from planned
    tests and assumptions, and identify missing acceptance evidence. Escalate
    safety, privacy and risk matters beyond agent authority. Do not label the
    candidate ready to ship when conditions remain; prepare the exact human
    authority actions where required.
    ```

## 8. Publish views for implementation and operations

The component engineer and service owner need different details. The six SABSA profiles combine authored chapters with complete fields, bodies, provenance and typed paths. Authors supply reviewed English prose; the deterministic renderer presents it without inventing decisions or translating authoritative text automatically.

Start with Markdown for content review, then request LaTeX/PDF or Word for the intended audience. Editable CSV catalogues support managed changes to existing local entries: preserve IDs and schema, validate and import into canonical sources, then re-review. CSV does not replace narrative or test evidence.

**Expected output:** useful viewpoint documents, structured catalogue exports and actual QA/status evidence. **Checkpoint:** architecture snapshot approval, rendered quality and the product release decision remain separate.

=== "Claude Code"

    ```text
    /sabsa document app/sabsa — prepare English viewpoint documents from the
    reviewed entries and authored narrative. Produce Markdown for content
    review, then the Component Engineering Specification and
    Operations/Assurance viewpoint as LaTeX and PDF. Generate Word only if
    requested for the audience. Export editable CSV catalogues with
    validate/import instructions and report actual draft, snapshot-approval
    and rendered-QA status separately from product release readiness.
    ```

=== "Codex"

    ```text
    $workflow-sabsa document app/sabsa — prepare English viewpoint documents
    from the reviewed entries and authored narrative. Produce Markdown for
    content review, then the Component Engineering Specification and
    Operations/Assurance viewpoint as LaTeX and PDF. Generate Word only if
    requested for the audience. Export editable CSV catalogues with
    validate/import instructions and report actual draft, snapshot-approval
    and rendered-QA status separately from product release readiness.
    ```

When required reviews are complete, JAI can prepare the exact architecture-owner command. The actual human executes it using real decision values; this illustrative form is not an agent instruction:

```sh
python3 ~/.ai/it-role-house/tools/sabsa.py approve app/sabsa --by "ACTUAL OWNER" --note "ACTUAL REVIEW DECISION REFERENCE"
```

This records hash-bound SABSA owner approval, not a Fabric release authority act. Check its current state after the human action:

=== "Claude Code"

    ```text
    /sabsa approval app/sabsa — verify that the recorded architecture-owner
    approval matches the current semantic snapshot. Identify changes requiring
    fresh review or approval and keep architecture status distinct from the
    release decision.
    ```

=== "Codex"

    ```text
    $workflow-sabsa approval app/sabsa — verify that the recorded
    architecture-owner approval matches the current semantic snapshot.
    Identify changes requiring fresh review or approval and keep architecture
    status distinct from the release decision.
    ```

## Handle a failed check or a changed product request

Suppose review finds that signing out leaves another user's contact
information visible in a device cache. A successful notification test
does not close this finding. Alice's example reply is: “Preserve the
authorized notification behavior, but isolate cached data by identity. Keep the
sign-out finding open until the account-switching case is verified.”

Use the actual review ledger for the bounded correction:

**Claude Code**

```text
/rework <reported-ledger> Correct the account-switching finding in app/. Preserve authorized notification behavior and add a local regression for access to cached contact data after sign-out. Report checks actually executed.
```

**Codex**

```text
$workflow-rework <reported-ledger> Correct the account-switching finding in app/. Preserve authorized notification behavior and add a local regression for access to cached contact data after sign-out. Report checks actually executed.
```

Replace the placeholder with the reported ledger. Have the reviewer
verify the original account-switching condition, including failure and
recovery behavior. If an emulator or managed device is unavailable, mark
those checks NOT_EXECUTED. A JVM unit test does not demonstrate all
Android lifecycle or device-management behavior.

If the product owner adds continuous location tracking, pause the
assumption that this is merely another screen. Return to the domain
requirements and SABSA steps to establish purpose, data handling,
affected business attributes and the consequences for users. If the
choice needs formal justification, open the bounded layered extension
with the changed intent. Preserve earlier findings and identifiers; a
new request must not erase an unresolved cache defect.

Conversational permission to explore an option is not a signed L0 act.
If the runtime requires human authority, the authorized person follows
the exact emitted instruction through the trusted authority path. An
agent's draft or favorable review does not become human approval.

Before handing off, reconcile the implemented behavior, architecture
description, acceptance cases and actual test results. Keep device,
backend and release checks pending until evidence exists. The
[idea-to-production chain](../../reference/workflows.md) explains the
wider handoffs; this walkthrough does not execute a store release or
full release qualification merely by naming that workflow.

## Continue the development loop

You should be able to trace a user outcome through an attribute, objective, service and component to the evidence supporting its behaviour. You should also be able to name what is unimplemented, unverified or awaiting a decision. Repeat that loop for the next bounded increment, updating semantic sources and regenerating publications when meaning changes.

This is a fictional teaching exercise; no app build, device test, provider conversation or authority action is claimed. See [validation status](index.md#teaching-and-validation-status), [deliverables](../../using/deliverables.md) and [publication dependencies](../../configuration/publication-stack.md).
