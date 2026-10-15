---
owner: JAI documentation maintainers
review_due: 2027-01-16
---

# Assess a deployed system with SABSA

Imagine that an organisation relies on a monitoring platform with privileged access to production systems. Its owner wants to know whether the deployed security is adequate and which changes deserve priority. A checklist of settings alone cannot answer that question: you first need to establish the business exposure, required outcomes and evidence that would demonstrate them.

This fictional tutorial uses JAI's SABSA workflow to build that foundation. You will derive technology-independent requirements, develop a reference realisation, compare it with the observed deployment, and turn supported gaps into a transformation roadmap. The result is an assessable chain from business need to proposed change, with unresolved questions kept visible.

## Prepare the engagement

Create `PROJECT.md` with the intended decision, systems in and out of scope, stakeholders, known constraints and available evidence. Identify the assessment owner and the permissions for using supplied material. Begin with documents and agreed read-only evidence; this tutorial does not authorise probing a live system.

Use SABSA because it connects security mechanisms to business drivers and measurable attributes. JAI's architect authors the model; an independent reviewer judges its suitability and evidence; the owner decides unresolved business and risk matters. Structural tools help them find broken links and missing fields, while substantive assessment still requires judgement.

Keep these records distinct throughout:

| Record | Purpose | What supports it |
| --- | --- | --- |
| Requirements and reference architecture | Define what should be true and why | Reviewed sources, business decisions and justified design |
| As-built baseline | Describe what is deployed and operated | Dated configuration, architecture and operational evidence |
| Findings and roadmap | Explain supported gaps and proposed changes | Located comparisons, business impact and acceptance criteria |

## Run this scenario in the provider CLI

Use the prompts in your existing provider conversation. Each tab is a complete request. **Operator:** supply the sources, scope each stage and respond to actual decision requests. **Behind the scenes:** JAI routes authoring and independent review, runs permitted checks and reports artefact locations and unresolved matters. The prompts do not substitute for evidence or human authority.

## 1. Establish the business question

Preparation inventories what is known before proposing controls. A monitoring platform can affect the systems it manages, so administrative reach and operational consequences belong in the brief. Public product documentation can explain capability; it does not establish the customer's settings.

The SABSA `prepare` activity should produce a source register, contextual business drivers and questions. A useful driver might require that a platform compromise cannot enable uncontrolled actions across managed systems. Its provenance must show whether that is stated, inferred or assumed.

**Checkpoint:** the assessment owner can explain the purpose and boundary in business terms. If those remain unclear, refine the brief before deriving controls.

=== "Claude Code"

    ```text
    /sabsa prepare assessment/sabsa — use PROJECT.md and the supplied
    documents. Establish the business question for assessing the monitoring
    management plane, including dependable operations and bounded privileged
    access. Inventory sources, derive contextual drivers and distinguish
    stated facts, inferences and assumptions. Do not infer deployed settings
    from vendor defaults or public descriptions.
    ```

=== "Codex"

    ```text
    $workflow-sabsa prepare assessment/sabsa — use PROJECT.md and the supplied
    documents. Establish the business question for assessing the monitoring
    management plane, including dependable operations and bounded privileged
    access. Inventory sources, derive contextual drivers and distinguish
    stated facts, inferences and assumptions. Do not infer deployed settings
    from vendor defaults or public descriptions.
    ```

## 2. Define the technology-independent upper three viewpoints

Build **Contextual, Conceptual and Logical** requirements before choosing a particular implementation. Contextual work explains business assets and dependencies. Conceptual work defines measurable attributes, risks, objectives and authority boundaries. Logical work defines services, policies, entities, privileges and information flows.

Use bounded `create` requests because typed dependencies matter. An attribute needs a driver; objectives link attributes and risks; a logical service addresses objectives. A component standard remains a Component concern even if you can research it early.

For example, “privileged actions are attributable” needs a measurement method and an agreed or explicitly unresolved target. The logical service can require authenticated, authorised and logged administration without naming a vendor agent. Do not invent retention or recovery numbers to make fields look complete.

**Expected output:** source-backed upper-viewpoint specifications, matrix answers and unresolved targets. **Checkpoint:** a reviewer can explain each requirement without relying on the installed product's features.

=== "Claude Code"

    ```text
    /sabsa create assessment/sabsa — develop only the Contextual, Conceptual
    and Logical requirements in dependency order. Describe business assets and
    dependencies; derive measurable attributes, threats and opportunities,
    risks and objectives; then define security services, policies, entities,
    privileges and flows. Keep requirements independent of the installed
    product, identify targets requiring owner agreement, and review each
    dependency stage before advancing.
    ```

=== "Codex"

    ```text
    $workflow-sabsa create assessment/sabsa — develop only the Contextual,
    Conceptual and Logical requirements in dependency order. Describe business
    assets and dependencies; derive measurable attributes, threats and
    opportunities, risks and objectives; then define security services,
    policies, entities, privileges and flows. Keep requirements independent of
    the installed product, identify targets requiring owner agreement, and
    review each dependency stage before advancing.
    ```

## 3. Resolve assumptions and review the requirements

An element-linked question has a clear closure condition. “Who may authorise remote administrative actions, and where is that delegation recorded?” can resolve an authority assumption. A generic request for all security documentation cannot do that as precisely.

Use `questions` to prepare discovery, then `review` for independent judgement. The reviewer should challenge unsupported legal applicability, vague measures and duplicated objectives as well as missing fields. The architect reworks findings; someone else verifies the changes.

**Expected output:** a discovery agenda and reviewed requirements with unresolved decisions identified. **Checkpoint:** do not treat missing discovery as observed deployment. Reference design may remain provisional while those facts are unavailable.

=== "Claude Code"

    ```text
    /sabsa questions assessment/sabsa — prepare discovery questions linked to
    the assumptions and elements they resolve. Identify required owner
    decisions, evidence needed and which work can proceed provisionally
    without inventing deployment facts.
    ```

=== "Codex"

    ```text
    $workflow-sabsa questions assessment/sabsa — prepare discovery questions
    linked to the assumptions and elements they resolve. Identify required
    owner decisions, evidence needed and which work can proceed provisionally
    without inventing deployment facts.
    ```

After inspecting that agenda, request the independent review:

=== "Claude Code"

    ```text
    /sabsa review assessment/sabsa — review provenance, business relevance,
    measurable attributes and logical coverage independently. Record located
    findings, have the architect rework them, and have the reviewer verify the
    rework. Keep unresolved owner decisions explicit.
    ```

=== "Codex"

    ```text
    $workflow-sabsa review assessment/sabsa — review provenance, business
    relevance, measurable attributes and logical coverage independently.
    Record located findings, have the architect rework them, and have the
    reviewer verify the rework. Keep unresolved owner decisions explicit.
    ```

## 4. Develop the reference realisation

The reference realisation turns reviewed logical requirements into the assessment yardstick. **Physical** design describes mechanisms and placement. **Component** design specifies products, configuration expectations and engineering standards. **Service Management** defines operation, measurement and assurance evidence.

For example, the reference might mediate privileged action execution, specify an identity integration and require an attributable decision record. These are target/reference choices until supported and agreed. They must not be presented as observed deployment. Framework mappings describe design coverage, not proved operating compliance; applicability and mapping rationale need review.

**Expected output:** reference mechanisms, component requirements, operational measures and a control/evidence matrix. **Checkpoint:** current, target and transition states remain distinguishable, and each design choice traces to a logical service and business need.

=== "Claude Code"

    ```text
    /sabsa create assessment/sabsa — derive the reference Physical, Component
    and Service Management viewpoints from the reviewed logical requirements.
    Define proposed mechanisms, component requirements, operational measures
    and evidence. Explain alternatives and dependencies, mark these as
    reference/target design rather than observed deployment, and retain the
    business trace. Use standards identifiers and justified interpretations
    without copying licensed text.
    ```

=== "Codex"

    ```text
    $workflow-sabsa create assessment/sabsa — derive the reference Physical,
    Component and Service Management viewpoints from the reviewed logical
    requirements. Define proposed mechanisms, component requirements,
    operational measures and evidence. Explain alternatives and dependencies,
    mark these as reference/target design rather than observed deployment, and
    retain the business trace. Use standards identifiers and justified
    interpretations without copying licensed text.
    ```

## 5. Establish criteria and the as-built baseline

Fix comparison criteria before interpreting deployment evidence. A criterion states the expected condition, why it matters, the evidence needed and how uncertainty is handled. A technician's collection runbook is more specific: it needs actual versions, interfaces and deployment facts.

The as-built baseline records configuration and operating practices with evidence dates and scope. An interview may explain a process; configuration and representative records can support narrower claims about enforcement. Unavailable evidence means **not demonstrated**, rather than automatically compliant or noncompliant.

**Expected output:** fixed criteria and a separate current baseline. **Checkpoint:** each observed claim cites evidence, and evidence gaps are distinguishable from adverse findings.

=== "Claude Code"

    ```text
    /sabsa review assessment/sabsa — establish comparison criteria for the
    agreed reference before assessing deployment evidence. For each criterion
    identify its objective, expected condition, evidence, assessment method
    and uncertainty handling. Use only supplied or explicitly authorised
    discovery evidence to establish the separate current baseline, recording
    dates, deployment scope and limitations.
    ```

=== "Codex"

    ```text
    $workflow-sabsa review assessment/sabsa — establish comparison criteria
    for the agreed reference before assessing deployment evidence. For each
    criterion identify its objective, expected condition, evidence, assessment
    method and uncertainty handling. Use only supplied or explicitly
    authorised discovery evidence to establish the separate current baseline,
    recording dates, deployment scope and limitations.
    ```

## 6. Assess mismatches and verify rework

A defensible finding connects a justified requirement to a supported observation. Suppose a dated configuration export permits a shared administrative identity. That can support a configuration finding; it does not alone establish which actions used that identity. The next assessment step may need effective access-path and action-record evidence.

Trace the affected component through its mechanism, service, objective and attribute to the business driver. Explain impact and priority using that chain. The reviewer records the finding, the relevant author proposes correction, and an independent reviewer verifies it. A clean matrix or an overlay marked “covered” cannot replace that evidence.

**Expected output:** located, prioritised findings with uncertainty and traceability. **Checkpoint:** the report distinguishes design coverage from actual operating effectiveness.

=== "Claude Code"

    ```text
    /sabsa review assessment/sabsa — compare the current baseline with the
    agreed reference and record located gaps. For each finding show the
    requirement, observed evidence, scope, typed business trace, uncertainty,
    impact and priority rationale. Separate design coverage from operating
    effectiveness. Have the appropriate author rework findings and an
    independent reviewer verify the result.
    ```

=== "Codex"

    ```text
    $workflow-sabsa review assessment/sabsa — compare the current baseline
    with the agreed reference and record located gaps. For each finding show
    the requirement, observed evidence, scope, typed business trace,
    uncertainty, impact and priority rationale. Separate design coverage from
    operating effectiveness. Have the appropriate author rework findings and
    an independent reviewer verify the result.
    ```

## 7. Turn gaps into a transformation roadmap

The roadmap links changes to the objectives they will satisfy and the evidence that will demonstrate closure. “Improve access” is not assessable. Replacing shared privileged access through an agreed identity mechanism, then verifying actor attribution for the agreed paths, has a clear acceptance boundary.

Use dependency tracing before changing model entries. Preserve the observed baseline while proposing target and transition changes. Distinguish containment, design, implementation and effectiveness verification. Dates, ownership commitments and risk acceptance belong to the actual decision owners.

**Expected output:** transition actions linked to findings, objectives and acceptance evidence. **Checkpoint:** each action can be assessed, dependencies are explicit and pending decisions are not disguised as commitments.

=== "Claude Code"

    ```text
    /sabsa update assessment/sabsa — trace affected elements and propose
    target and transition changes for the reviewed findings. Preserve the
    current baseline. For each gap identify a proposed owner, dependencies,
    containment or implementation action, acceptance evidence and decision
    needed. Keep dates, ownership commitments and risk acceptance pending
    until the actual owner decides them.
    ```

=== "Codex"

    ```text
    $workflow-sabsa update assessment/sabsa — trace affected elements and
    propose target and transition changes for the reviewed findings. Preserve
    the current baseline. For each gap identify a proposed owner,
    dependencies, containment or implementation action, acceptance evidence
    and decision needed. Keep dates, ownership commitments and risk acceptance
    pending until the actual owner decides them.
    ```

## 8. Publish the assessment and check authority status

Different readers need different views of the same reviewed model. The six SABSA publications provide authored chapters, complete specifications, provenance and typed paths. Start with Markdown for content review, then request the actual formats needed. Missing narrative remains a publication gap.

CSV is useful for maintaining structured catalogues: export, retain IDs and schema, validate edits, import them into canonical entries and re-review. It does not replace narrative or become a separate authority. Source and authored-narrative changes invalidate prior snapshot approval.

**Expected output:** assessment publications, catalogue exports, actual QA evidence and explicit draft/approval status. **Checkpoint:** rendering success is not interpreted as owner approval or permission for a production change.

=== "Claude Code"

    ```text
    /sabsa document assessment/sabsa — prepare the six English viewpoint
    documents and an assessment summary from reviewed sources and authored
    narrative. Produce Markdown for content review, then the Logical viewpoint
    as LaTeX and PDF, and export editable CSV catalogues with the
    validate/import instructions. Report template, output paths, remaining
    gaps, snapshot status and actual rendered-QA evidence. Keep human approval
    pending where required.
    ```

=== "Codex"

    ```text
    $workflow-sabsa document assessment/sabsa — prepare the six English
    viewpoint documents and an assessment summary from reviewed sources and
    authored narrative. Produce Markdown for content review, then the Logical
    viewpoint as LaTeX and PDF, and export editable CSV catalogues with the
    validate/import instructions. Report template, output paths, remaining
    gaps, snapshot status and actual rendered-QA evidence. Keep human approval
    pending where required.
    ```

When the required reviews are ready, JAI can prepare the exact owner command. In Codex, the actual human reviews and executes that protected action in a trusted terminal. This illustrative form is for the human, using real owner and decision values:

```sh
python3 ~/.ai/it-role-house/tools/sabsa.py approve assessment/sabsa --by "ACTUAL OWNER" --note "ACTUAL REVIEW DECISION REFERENCE"
```

After the human action, check whether the recorded snapshot still matches the model before regenerating approved publications:

=== "Claude Code"

    ```text
    /sabsa approval assessment/sabsa — verify that the recorded owner approval
    matches the current semantic snapshot and report any changes requiring
    fresh review or approval.
    ```

=== "Codex"

    ```text
    $workflow-sabsa approval assessment/sabsa — verify that the recorded owner
    approval matches the current semantic snapshot and report any changes
    requiring fresh review or approval.
    ```

## Carry the result forward

You should now have requirements and a reference design, a distinct evidence-backed current baseline, supported findings and a transformation roadmap. Open discovery, funding or risk decisions can remain legitimate outputs. Continue through implementation and effectiveness verification rather than assuming that a roadmap closes the exposure.

This page is a fictional teaching exercise, not an executed assessment or provider transcript. See the [series validation status](index.md#teaching-and-validation-status), [deliverables](../../using/deliverables.md) and [publication prerequisites](../../configuration/publication-stack.md).
