# Concepts, demonstrations and review controls

> **Example compatibility.** This detailed material originated in the 26.10.0 runtime handbook and is retained in the maintained Markdown documentation for its hands-on examples and technical references. AI IT House 26.10.4 has additional capabilities; treat the installed `GUIDE.md`, current `.ai/commands/` contracts, runtime tool `--help`, and versioned schemas as the authoritative behavior. Examples may require adaptation to the deployment context. These notes are not a separate release or documentation system.

## Provider use and the implementation explained

The old walkthroughs use Claude-style slash commands. In **Claude Code** enter `/demo`, `/analyse`, `/review`, etc. in the provider conversation; in **Codex CLI** enter the corresponding `$workflow-demo`, `$workflow-analyse`, `$workflow-review`, etc. (not in a system shell). The orchestrating agent delegates work and calls installed Python utilities as needed. The user supplies evidence, accepts/declines permission requests and makes reserved human decisions, but does not initialise Fabric or execute its everyday API manually. Codex does **not** support agent-driven L0 approval; the human runs that protected command in a separate trusted terminal after reviewing the dossier. See [interaction patterns](interaction-model.md), [the layered user journey](layered-engagement.md), and [Human authority](../operations/human-authority.md).

## Getting started and demonstration tour


### Overview

281 IS/IT roles, specialised agents and workflows for Claude Code and Codex — and how to use every command, with a demo for each.

#### Before you start

1. **Install** the package (`install.cmd` on
   Windows, `bash install.sh` elsewhere) and **start a new
   Claude Code or Codex CLI session**. Nothing else needs setting up.
2. **Create the demo projects:** in Claude Code, type
   `/demo setup`. They are copied to
   `~/it-role-demo/` (on Windows,
   `C:\Users\<you>\it-role-demo\`):

   | Project | What it is | Use it with |
   | --- | --- | --- |
   | `invoice-service` | a small Python billing service, with a short git history, and deliberate flaws | `/analyse` `/criteria` `/review` `/rework` `/develop` `/govern` `/research` `/layered` |
   | `policy-docs` | a security policy library, with deliberate flaws | `/analyse` `/review` `/rework` `/govern` |
   | `acme-pay` | notes and an RFP extract about a fictional potential client | `/sabsa` |
3. **Open Claude Code or Codex CLI in `~/it-role-demo`**
   (`cd ~/it-role-demo` then `claude` or `codex`), so that the
   paths below work as written. Anywhere else, give full paths.

**How to read the demos.** Each command's *Try
it* gives you the exact text to type. *What to expect*
describes a good result. For the review demos it also lists the flaws
that were planted — the answer key. The reviewers never see this guide,
so if they find the flaws, they found them in the code. A good review
finds most of them, and may find others; a review that misses the
high-severity ones is worth reporting.

**Two things you will see often.**

- *Approval prompts.* Some acts are yours alone: accepting a
  finding as a risk instead of fixing it, granting an exception, accepting
  a product. Claude Code may present an interactive permission gate; review
  the exact operation. Codex instead refuses agent-driven L0 commands and
  requires you to execute the exact protected command separately as the human.
- *Confirmation before work starts.* Reviews show you their
  criteria and wait for your yes. That is deliberate: criteria chosen
  after reading cannot be defended.

---

#### A 20-minute tour

The shortest path through the main ideas, all on the demo
projects:

| Step | Type | What you learn |
| --- | --- | --- |
| 1 | `/demo setup` | the demo projects appear in `~/it-role-demo` |
| 2 | `/analyse invoice-service` | the library understands a codebase before judging it |
| 3 | `/criteria invoice-service` | review criteria are a file you own and edit |
| 4 | `/review invoice-service` | located findings, recorded in a ledger |
| 5 | `/rework` | fixes by one agent, verified by another, until complete |
| 6 | `/review policy-docs` | the same discipline for documents |
| 7 | `/diagnose test_charge_is_approved fails now and then` *(in `invoice-service`)* | a defect analysed before it is fixed: last known good, a working analogue, timing |
| 8 | `/sabsa questions acme-pay/sabsa` *(after a short `/sabsa prepare`)* | a SABSA architecture built from client material |

---

## Core concepts


### Concepts

The ideas the commands share.

##### Review criteria

What a review judges against, fixed before reading. They come from
the first of these that exists:

1. criteria in your request —
   `/review docs against docs/style-guide.md`;
2. the project's own file
   `<project>/.claude/review-criteria.md` — created by
   `/criteria`, yours to edit and commit;
3. your personal default
   `~/.ai/review-criteria.md`;
4. the package default for the kind of target: software, documents or
   SABSA.

Each criterion is a `## C<n> <title>` heading
in the file; findings cite it by that ID. Each review records which file
it used and a fingerprint of its contents.

##### The findings ledger

Every review records its findings in
`.findings/<name>.jsonl` in the project. Each finding
is open, resolved, verified, stuck, accepted or withdrawn. The reviewer
never fixes, and the fixer never verifies — the ledger refuses both.
After three failed fixes a finding is stuck and comes to you. The ledger
is append-only and tamper-evident: do not edit it by hand.

##### Approvals

Some acts are reserved for you: accepting a risk, granting an
exception, accepting a product, approving a change to the library
itself. Claude can present the exact approval command interactively; Codex deliberately requires the reserved authority command to be executed explicitly by the human. The action remains fail-closed when that authority cannot be established.

##### SABSA library layout

```
<library>/
├── library.md          name, organisation, scope, owner, version; its text is the executive summary
├── 00-sources/         what is known about the client; every claim cites a file here
├── 01-contextual/ … 06-service-management/    the elements, by SABSA layer
├── matrix/             36 files: each layer's six questions, answered or marked not applicable
├── .sabsa/approval.json hash-bound owner approval of the current architecture snapshot
└── templates/          optional: the client's own document template and reference.docx
```

`~/.ai/it-role-house/skills/sabsa-library/references/structure.md`
describes every element and field; `references/templates.md`
describes templates and every field they can use.

##### Defect analysis

A defect is analysed before it is fixed, following
`~/.ai/it-role-house/standards/defect-analysis.md`:
reproduce it as a command and measure whether it is intermittent; then
compare against the **last known good state** (when did it
work, and what changed?), against a **working analogue**
(where does the same kind of thing work, and what differs?), and against
**timing** (does an operation get the time it needs? do
other timed events — schedules, expiry, ordering, clocks — take part?).
Each comparison is carried out or marked not applicable with a reason.
Hypotheses are tested by experiment; the root cause is distinguished
from the trigger and contributing factors; the fix addresses the root
cause, with a regression test that fails first. `/diagnose`
runs it; the `defect-analyst` agent carries it out;
`defect.py` bisects safely, reports changes, compares code,
scans for timing constructs, repeats runs and validates the
analysis.

##### Source code documentation

All code Claude writes follows
`~/.ai/it-role-house/standards/code-documentation.md`:
a doc comment on every public element in the language's own format —
Javadoc for Java, docstrings for Python, TSDoc, XML doc, KDoc, godoc —
stating its contract (parameters, result, exceptions); comments that say
*why*, never narrate *what*; no commented-out code. It is
enforced in layers:

- a hook checks every source file Claude writes and tells Claude at
  once what is missing — for an edit, only the declarations the edit
  touched, so changing one method never obliges Claude to document a whole
  legacy file;
- Claude cannot finish its turn while public API it wrote is
  undocumented (a second attempt is allowed, and you are told what
  remains, so a problem it cannot solve never traps the session);
- reviews apply it as criterion C8;
- the standard includes CI configurations — javac doclint and
  Checkstyle, Ruff, ESLint, and the equivalents for C#, Kotlin and Go —
  that make it a build failure in your own pipeline.

To switch the hook off for one project, create an empty file
`.ai/no-doc-check` in it.

##### Tests

Code Claude writes is accompanied by its tests, following
`~/.ai/it-role-house/standards/testing.md`:

- **unit tests** for every public behaviour added or
  changed — the normal case, the boundaries, a failure path; for Java,
  JUnit 5 with AssertJ and `@ParameterizedTest`, and Mockito
  for collaborators;
- **integration tests** for every boundary to a database,
  a service, a broker or the file system, against the real thing —
  Testcontainers, `*IT` classes run by Maven Failsafe;
- **mocks only for collaborators** at the edge of the
  unit — never the class under test, never types you do not own;
- **a regression test** for every fixed defect.

Claude then runs the tests. A hook checks that what Claude wrote has
tests, notices every test run and whether it failed, and will not let
Claude finish while its code lacks tests, while the tests have not been
run since its last change, or while the last run failed. Code outside a
project (no `pom.xml`, `package.json`,
`pyproject.toml` …) is exempt, as are prototypes in
`experiments/`. Reviews apply this as criterion C4. The
standard includes CI configurations — Surefire and Failsafe, JaCoCo,
pytest-cov, and the equivalents — for your own pipeline.

To switch the test hooks off for one project, create an empty file
`.ai/no-test-check` in it.

##### Decision records (`/layered`)

`.fabric/<engagement>.jsonl` in the folder where you
ran `/layered`: every requirement, contract, result, review,
escalation and decision, hash-chained. `/fabric-report`
checks it.

---

## Command overview


### Command reference

All commands at a glance.

Every slash command the library adds to Claude Code. Type it in a Claude Code session; arguments in
`<angle brackets>` are required, in `[square brackets]` optional. Each page has the
syntax, what happens, a demo to try, what to expect and how to check it worked. The filter on the left narrows
this table.

| Command | Arguments | What it does |
| --- | --- | --- |
| `/demo` | `<setup|list|reset PROJECT|check>` | Set up, reset or check the demo projects for trying every command |
| `/guide` | `[command or topic]` | Show the user guide for this library, or the section for one command, with its demo |
| `/publish` | `<semantic model> [archetype] [formats]` | Render governed enterprise outputs from one reviewed semantic source |
| `/repository` | `<init|validate|import|export|views|portfolio|impact|decommission> ...` | Govern the canonical EA repository, ArchiMate exchange, views, portfolio dependencies and retirement |
| `/analyse` | `<path or description>` | Analyse a code repository, a document library or a SABSA library — understand it, no verdicts |
| `/criteria` | `[project path]` | Create or show the review criteria for this project |
| `/review` | `<path> [against <criteria or a criteria file>]` | Review code, documents or a SABSA library against criteria fixed before reading, with located findings |
| `/rework` | `[ledger]` | Fix the open findings of a review, with independent verification, until complete |
| `/diagnose` | `<symptom, failing test or issue>` | Find the root cause of a defect before fixing it: last known good, a working analogue, and timing |
| `/develop` | `<what to build or change>` | Develop a change to a software product or document library, reviewed before it is proposed |
| `/govern` | `<path>` | Assess and propose the governance of a repository or document library |
| `/research` | `<question>` | Research a problem to a decision, with experiments if needed |
| `/sabsa` | `<prepare|create|update ID|review|suggest|questions|approve|approval|document|template> [library path]` | Build a SABSA security architecture from client material, or update, review, improve or document one |
| `/layered` | `<intent, stated as you would to an accountable team>` | Run a consequential task through the six-layer justifiable delivery method |
| `/fabric-report` | `<engagement> [product fragment]` | Independent justifiability report on a traceability fabric |

New here? Run `/demo setup`, open Claude Code in `~/it-role-demo`, and follow
the 20-minute tour.

## Troubleshooting


### Troubleshooting

When something does not work as described.

| Symptom | Cause and fix |
| --- | --- |
| A command is not recognised | Start a new Claude Code session after installing or upgrading. |
| "Python 3.10 or newer is required" | Install Python from python.org; on Windows tick "Add python.exe to PATH". |
| An authority act is refused, with a message about the permission mode | You are in auto or bypass mode, where no approval prompt can appear. Switch to the default mode. |
| `/sabsa document … as docx` says pandoc is needed | Install pandoc from pandoc.org, or produce Markdown and convert it yourself. |
| Windows: a note that Git for Windows was not found | Claude Code then uses PowerShell. Most things work; install Git for Windows for the full experience. |
| Claude keeps adding Javadoc or docstrings it was not asked for | That is the documentation standard, applied to code Claude wrote or changed. To switch it off for a project, create an empty file `.ai/no-doc-check` in it. |
| Claude says it cannot finish: tests missing, not run, or failing | That is the testing standard, applied to code Claude wrote. Let it write and run the tests. To switch it off for a project, create an empty file `.ai/no-test-check` in it. |
| A demo went wrong and you want to start again | `/demo reset <project>`. |
| You want to check the installation itself | `/demo check`, or `python3 ~/.ai/it-role-house/scripts/check_agent_policy.py ~/.claude`. |

**Removing everything:**
`bash ~/.ai/it-role-house/uninstall.sh`, or on Windows
`%USERPROFILE%\.claude\it-role-library\uninstall.cmd`. Your
own files, settings and demo projects stay.
