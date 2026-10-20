# Architecture security assessment and recurring findings management

Owner: JAI documentation maintainers  
Review date: 2026-10-20

ACME Corp operates a shared monitoring platform. Bob owns the platform;
Alice performs the assessment. They need an architecture assessment and
a repeatable way to detect changes, address findings and verify corrections.
The situation is fictional and reflects common enterprise practice. The
commands below are illustrative prompts, not executed traces or approval
records.

This combines the maintained [security-assessment example](how-to-use-JAI/security-assessment.md)
with an adapted recurring-review procedure. The recurring process design is
a project proposal: neither the example nor `/hint` installs monitoring or
schedules future work. This walkthrough chooses layered assurance for the
combined deliverable. The maintained SABSA assessment route is an alternative;
do not start a second engagement simply to duplicate the same assessment.
This is an additional combined walkthrough, not a new bundled scenario ID
or demo pack. The maintained catalog still contains 29 scenario packs.

## Prepare one project and its evidence boundary

Create a new project directory, such as `acme-monitoring-assessment`, and
place authorised source material under `inputs/`. Use a separate `outputs/`
directory for drafts. A suitable input inventory is:

| File | Purpose |
| --- | --- |
| `inputs/architecture.md` | Components, trust boundaries, data flows, integrations and privileged administration paths. |
| `inputs/security-requirements.md` | Applicable requirements, scope exclusions and the source of each requirement. |
| `inputs/control-evidence-register.csv` | Evidence IDs, dates, owners, locations and access constraints; explicitly identify missing or stale evidence. |
| `inputs/change-and-incident-history.md` | Relevant changes and incidents, with observation sources and unresolved questions. |
| `inputs/service-responsibilities.md` | Proposed owners, review participants, escalation contacts and decision authority. |

Do not invent control effectiveness or incident history to complete the
inventory. Record unknowns and request the missing evidence. Fictional demo
inputs are useful for practice, but are not evidence about a real platform.
Start the provider in this project and confirm which files it may read.

## Run this scenario in the provider CLI

### 1. Ask for a starting procedure

Claude:

```text
/hint Assess the security architecture of ACME's monitoring platform and propose a recurring process for detecting changes, resolving findings and verifying corrections. Use only authorised project inputs. Identify missing evidence and any unsupported parts of the recommendation.
```

Codex:

```text
$workflow-hint Assess the security architecture of ACME's monitoring platform and propose a recurring process for detecting changes, resolving findings and verifying corrections. Use only authorised project inputs. Identify missing evidence and any unsupported parts of the recommendation.
```

Check the English interpretation, source examples and unmatched goals.
A selected assessment example may cover only the first outcome. Ask the
operator to label the recurring-process portion as adapted or proposed,
rather than pretending that a single maintained example covers everything.

### 2. Understand the sources before judging them

Claude:

```text
/analyse .
```

Codex:

```text
$workflow-analyse .
```

Inspect the source inventory and scope description. The desired result is a
map of what is known and missing, not an early assertion that the platform
is secure. If privileged access is undocumented, request that information
before treating its controls as assessed. Keep the gap visible if work
continues with a bounded scope.

### 3. Establish review criteria

Claude:

```text
/criteria .
```

Codex:

```text
$workflow-criteria .
```

Have the responsible owner confirm applicable requirements and criteria
through the project's actual process. Include traceability, evidence
currency, trust boundaries, privileged access, finding ownership and closure
verification. A generated criterion is not automatically an approved
organisational standard. Resolve conflicting requirements before assessment.

### 4. Produce the assessment and recurring-process proposal

Claude:

```text
/layered Assess the monitoring platform using the authorised inputs and confirmed criteria. Produce a traceable architecture security assessment and a proposed recurring findings process. Distinguish observations, assumptions and recommendations. Define triggers, owners, evidence refresh, escalation and independent closure verification; do not claim monitoring or scheduling has been installed.
```

Codex:

```text
$workflow-layered Assess the monitoring platform using the authorised inputs and confirmed criteria. Produce a traceable architecture security assessment and a proposed recurring findings process. Distinguish observations, assumptions and recommendations. Define triggers, owners, evidence refresh, escalation and independent closure verification; do not claim monitoring or scheduling has been installed.
```

Retain the actual engagement and output identifiers returned by the runtime.
Inspect the finding-to-evidence links and the proposed hand-offs. If a
required authority act is requested, the named human performs it using the
actual supplied instructions; a chat response cannot substitute for a
signature. Do not restart an engagement merely to erase an unresolved gate.

### 5. Review and correct the outputs

Layered delivery already includes its own review hand-offs. First inspect
those results. Use the following separate review only when the project
requires an additional assessment of the combined outputs against its
criteria, or the proposed operating procedure needs a distinct review scope;
do not repeat an already completed review merely to run another command.

Claude:

```text
/review <actual-assessment-and-process-output>
/rework <actual-findings-ledger>
```

Codex:

```text
$workflow-review <actual-assessment-and-process-output>
$workflow-rework <actual-findings-ledger>
```

Replace both placeholders with observed paths or identifiers. Run review
first, inspect its findings and use the ledger it actually reports for
rework. Preserve reviewer/author separation. An AI editorial review is not
independent human acceptance. If a proposed correction lacks operational
evidence, keep the finding open and assign evidence collection rather than
marking it resolved on the basis of a rewritten paragraph.

## Make recurrence an owned operating procedure

The proposal should specify observable triggers and accountable people:

| Trigger or activity | Proposed responsibility and check |
| --- | --- |
| Material architecture, access or integration change | Bob supplies the change record and updated architecture; Alice identifies affected criteria. |
| New vulnerability, incident or control failure | The assigned operational owner supplies observations; the review coordinator assesses scope and urgency. |
| Periodic review date | A named service owner arranges the review and refreshes evidence. The interval is explicitly agreed for the project. |
| Remediation | The assigned implementer records the change and its evidence against the actual finding. |
| Closure | A distinct verifier checks the evidence against the criterion; unresolved residual risk follows the actual authority process. |

For the next cycle, refresh the inventory and review the changed scope;
retain unresolved findings and link new evidence to them. Reuse relevant
criteria after checking their currency. New business scope may require new
criteria, an updated engagement contract and human decisions rather than
mechanical repetition of the prior prompts.

If the organisation wants automatic detection, specify the actual telemetry,
integrations, access permissions, alert ownership and scheduler separately.
Until implemented and tested, a calendar promise or process document is not
working monitoring. Confirm who initiates each cycle before calling the
procedure operational.

## Finish with a clear status

Report which areas were assessed, which evidence was missing, which findings
remain open, who owns the next action and which decisions await authority.
Keep the maintained example, project adaptation and proposed operating
procedure distinguishable. Publication and acceptance use their existing
gates; a useful hint is neither release qualification nor approval.
