---
owner: JAI documentation maintainers
review_due: 2027-01-16
---

# Assess a deployed system with SABSA

Owner: JAI maintainers. Last reviewed: 2026-10-20.

## Set up the assessment workspace

Use a fictional starting question: ACME's monitoring platform is already
operating with privileged production reach. Alice needs to understand
whether its security controls support the business service. Bob owns the
platform and can supply dated
records. These are illustrative roles, not evidence about an actual
organisation. Assessment must start from the deployed system and its
business use; a reference document is not a substitute for either.

Create a new project directory named `acme-monitoring-assessment/`. Within it,
create `input/`, `assessment/`, `working/` and `output/`. The subsequent
`assessment/sabsa` examples refer to this project's assessment material.
They do not imply that JAI discovers the production system automatically.
Reserve `working/` for draft analysis and `output/` for a reviewed handoff;
ask the selected workflow to report the paths it actually produces.

Supply a small, coherent initial evidence set:

- `input/business-brief.md`: service purpose, users, business attributes,
  consequences of interruption and the question Alice must answer.
- `input/deployment-map.md`: deployed components, trust boundaries,
  integrations, owners and the date represented by the map.
- `input/control-inventory.md`: controls claimed by Bob, with links to
  available configuration or operating evidence.
- `input/observations/`: authorized, sanitized test results, incident
  records and control observations with their dates and environments.
- `input/assessment-scope.md`: exclusions, allowed evidence handling,
  assessment period, accountable owner and required human reviewers.

Add `PROJECT.md` summarizing that scope. Do not start with a large folder
of unexplained screenshots. Record why each item supports a claim and
which deployment it describes. If restore results or supplier evidence
are missing, list them as requested inputs and narrow the conclusion.
An unanswered request is not a passing control.

Follow the [installation guide](../../getting-started/install.md), then
start Claude Code or Codex in `acme-monitoring-assessment/`. Use the paired
prompts below in the provider conversation, not in a terminal shell. Read
each resulting draft, evidence gap and actual output path before moving
to the next stage. The assessment commands organize work; they do not
authorize live penetration tests or grant access to customer records.

Imagine that an organisation relies on a monitoring platform with privileged access to production systems. Its owner wants to know whether the deployed security is adequate and which changes deserve priority. A checklist of settings alone cannot answer that question: you first need to establish the business exposure, required outcomes and evidence that would demonstrate them.

This fictional tutorial uses JAI's SABSA workflow to build that foundation. You will derive technology-independent requirements, develop a reference realisation, compare it with the observed deployment, and turn supported gaps into a transformation roadmap. The result is an assessable chain from business need to proposed change, with unresolved questions kept visible.

## Choose the assurance arrangement

This case uses the **direct domain workflow** from [the methodical workflow guide](../../using/methodical-workflows.md). The main sequence deliberately stops at a reviewed assessment, transformation roadmap and architecture-owner approval. It does not decide whether a system may be released, accept residual risk or authorise production changes. `/sabsa` is appropriate for that documented scope because it supplies domain authoring, independent review and verified rework without requiring a complete six-layer creation episode.

The absence of `/layered` from the main sequence does not mean that review is optional. It means that the exercise does not claim a Fabric record of its creation process. This explains the tutorial's scope; it is not a claim about why an earlier author or provider chose particular commands.

If your policy requires layered justification of **creation itself**, choose this alternative before step 1:

=== "Claude Code"

    ```text
    /layered Create and independently review the monitoring-platform security
    assessment using sabsa-library, PROJECT.md and the supplied evidence.
    Preserve the distinction between reference design and observed deployment,
    use adjacent contracts and keep owner decisions outside agent authority.
    ```

=== "Codex"

    ```text
    $workflow-layered Create and independently review the monitoring-platform
    security assessment using sabsa-library, PROJECT.md and the supplied
    evidence. Preserve the distinction between reference design and observed
    deployment, use adjacent contracts and keep owner decisions outside agent
    authority.
    ```

Under that arrangement the orchestrator carries out the domain activities below inside the layer contracts. Use them as checkpoints within the existing engagement; do not start a duplicate `/sabsa` engagement for each checkpoint. The [layered operating cycle](../../using/layered-engagement.md) describes the required evidence and recovery paths.

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

## Optional extension: justify a new decision

The assessment can legitimately end here with unresolved funding or risk decisions. Architecture-owner approval records the owner's decision about an exact model snapshot; it is not permission to expose the service or implement the roadmap.

If the next task is a consequential decision, use the reviewed assessment as input to a **new decision scope**. This extension is an additional teaching option, not evidence that the earlier domain work ran through Fabric:

=== "Claude Code"

    ```text
    /layered Assess whether the reviewed monitoring-platform assessment
    snapshot <reference and digest> supports the proposed transformation
    commitment. Use sabsa-library and the actual deployment evidence;
    independently examine gaps, uncertainty, implementation dependencies and
    acceptance conditions. Escalate funding and risk acceptance to the human
    owner. Do not authorise implementation or invent earlier creation records.
    ```

=== "Codex"

    ```text
    $workflow-layered Assess whether the reviewed monitoring-platform
    assessment snapshot <reference and digest> supports the proposed
    transformation commitment. Use sabsa-library and the actual deployment
    evidence; independently examine gaps, uncertainty, implementation
    dependencies and acceptance conditions. Escalate funding and risk
    acceptance to the human owner. Do not authorise implementation or invent
    earlier creation records.
    ```

Request `/fabric-report <decision-engagement-ID>` in Claude or `$workflow-fabric-report <decision-engagement-ID>` in Codex afterwards. A blocked or conditional decision is a valid result. Missing supporting evidence must remain visible; later review cannot recreate an unrecorded creation history.

## Respond to missing evidence and review findings

Suppose Bob supplies a backup schedule but no restoration result. The
assessment should distinguish a configured backup from demonstrated
recoverability. Alice can reply: “Continue the assessment, but leave
recoverability unverified. Request a dated restoration result and its
environment; do not infer that our recovery target has been met.”

Continue the current domain conversation with that evidence request.
If a review ledger already exists, use its actual identifier:

**Claude Code**

```text
/rework <reported-ledger> Incorporate Bob's supplied restoration evidence into the assessment. Preserve the recoverability finding if the evidence does not demonstrate the stated target.
```

**Codex**

```text
$workflow-rework <reported-ledger> Incorporate Bob's supplied restoration evidence into the assessment. Preserve the recoverability finding if the evidence does not demonstrate the stated target.
```

Replace the placeholder with the ledger returned by review. Ask an
independent reviewer to verify the finding against the actual result;
rewriting the assessment is not verification. A tabletop explanation,
an automated backup log and a successful restoration have different
evidential meanings.

If Alice instead asks whether to launch a new payment integration, the
question has changed from assessment to a consequential decision. Keep
the existing assessment intact and use the optional layered extension
above to frame the new intent, scope, alternatives and unresolved risks.
A reply that clarifies the work does not substitute for any signed L0
authority act required by the runtime. Follow its exact human authority
instruction when one is emitted; do not invent an approval command.

Before handoff, check that each conclusion cites available evidence and
that missing checks remain NOT_EXECUTED or otherwise explicitly
unverified. Separate AI editorial review, actual independent assessment
and human acceptance. This guide has not executed the fictional case.

The [enterprise workflow catalogue](../../reference/workflows.md)
provides the related security and assurance handoffs; the scenario does
not create a new `/assessment` command.

## Carry the result forward

You should now have requirements and a reference design, a distinct evidence-backed current baseline, supported findings and a transformation roadmap. Open discovery, funding or risk decisions can remain legitimate outputs. Continue through implementation and effectiveness verification rather than assuming that a roadmap closes the exposure.

This page is a fictional teaching exercise, not an executed assessment or provider transcript. See the [series validation status](index.md#teaching-and-validation-status), [deliverables](../../using/deliverables.md) and [publication prerequisites](../../configuration/publication-stack.md).
