# Runtime tools and command-line reference

> **Example compatibility.** This detailed material originated in the 26.10.0 runtime handbook and is retained in the maintained Markdown documentation for its hands-on examples and technical references. AI IT House 26.10.4 has additional capabilities; treat the installed `GUIDE.md`, current `.ai/commands/` contracts, runtime tool `--help`, and versioned schemas as the authoritative behavior. Examples may require adaptation to the deployment context. These notes are not a separate release or documentation system.

## Intended reader and invocation boundary

This is the **developer/maintainer API reference**, not the default user journey. In normal work, the user enters `/layered`, `/review`, `/sabsa`, etc. in Claude Code, or `$workflow-layered`, `$workflow-review`, `$workflow-sabsa`, etc. in Codex CLI. The provider agent then selects supported helpers and executes authorised operations. The commands and help output preserved below explain the actual implementation and allow reproducible diagnosis; they are **not a mandatory series of manual operator steps**. A runtime self-test only verifies its own invariants, not the correctness or release approval of a particular enterprise artefact.

The important exception is L0: Codex intentionally cannot execute guarded human authority acts; those are performed by the human in a separate trusted terminal after examining the dossier. Claude may use a real interactive approval prompt when supported. Agents must not bypass the boundary to make an example "work". See [interaction patterns](../using/interaction-model.md), [human authority](../operations/human-authority.md) and [CLI guide](installed-cli-guide.md). Runtime usage/help and current contracts take precedence over historical examples.

## Agent contract reference


### Agents

Who does the work, and with which tools.

The current runtime includes **33 agent contracts** (see `docs/using/roles.md` and `.ai/agents/` for authoritative definitions). The following **28-entry table is an explanatory earlier-release subset**, including historical model selectors. It must not be used as the current provider tool allowlist: native Agent/Policy Contracts, model routing and runtime enforcement determine effective permissions. Commands and skills dispatch agents; they are not a bypass around those controls.

#### Tiers

| Tier | Tools |
| --- | --- |
| advise | `Read, Grep, Glob, WebSearch` |
| inspect | `Read, Grep, Glob, WebSearch, Bash` |
| author | `Read, Grep, Glob, WebSearch, Write, Edit` |
| execute | `Read, Grep, Glob, WebSearch, Write, Edit, Bash` |
| route | `Read, Grep, Glob` |
| orchestrate | `Read, Grep, Glob, Bash, Task, Agent` |
| research | `Read, Grep, Glob, WebSearch, WebFetch` |

#### Agent examples from the earlier CLI guide (28-entry subset)

| Agent | Tier | Model | Tools | Purpose |
| --- | --- | --- | --- | --- |
| `artefact-governor` | inspect | sonnet | `Read, Grep, Glob, WebSearch, Bash` | Assesses and designs the governance of a software product or document library: ownership, review cycles, versioning and release practice, change approval trail, changelog, CODEOWNERS, retention and the policy that holds it together. Produces a governance assessment with located findings and a proposed governance model. Use for 'who owns this', 'is our documentation governed', 'set up change control for this repository', or governance audits. Reads git history and files; never changes them. |
| `authority-liaison` | route | haiku | `Read, Grep, Glob` | Prepares an escalation packet for the human authority in layered justifiable delivery: the conflict, the chain of layers it passed through, the options, the evidence each rests on, and the exact fabric.py command the human must run. Never decides and cannot record an authority act. Use when an escalation has relayed to Layer 1 or a product awaits authority acceptance. |
| `codebase-reviewer` | inspect | sonnet | `Read, Grep, Glob, WebSearch, Bash` | Performs a deep review of an existing codebase and reports prioritised findings: architecture conformance, coupling and change hotspots, test coverage against risk, dependency and supply-chain exposure, security patterns, operability gaps. Use for inherited systems, technical due diligence, pre-rewrite assessment, recurring-defect investigation, or any request to "review this repository", "audit our code" or "tell us what to fix first". Reads and measures only; never edits the code. |
| `defect-analyst` | inspect | opus | `Read, Grep, Glob, WebSearch, Bash` | Analyses a defect to its root cause before anyone fixes it: reproduces it as a command, measures whether it is intermittent, then compares against the last known good state (bisecting in a separate worktree), against a working analogue (the same code elsewhere, a sibling function, another input or environment) and against timing (timeouts, async completion, ordering, clocks, schedules, expiry). Tests competing hypotheses and returns a validated analysis. Use for 'why does this fail', 'it worked last week', 'it fails sometimes', 'works here but not there'. Diagnoses and verifies; never fixes. |
| `docs-author` | author | sonnet | `Read, Grep, Glob, WebSearch, Write, Edit` | Writes and edits standalone documentation: guides, references, tutorials, articles, books, website and wiki content. Writes into the documentation tree only (docs/, site/, content/, \*.md, \*.mdx, \*.rst, \*.adoc) and never into source files. Use for Technical Writer, Content Designer, Developer Advocate and Knowledge Manager work. In-source comments such as JavaDoc or docstrings are not this agent's. |
| `document-reviewer` | inspect | sonnet | `Read, Grep, Glob, WebSearch, Bash` | Analyses and reviews a document library — books, articles, guides, policies, wikis, websites as source — for accuracy, consistency, structure, terminology, cross-references, ownership and currency. Records located findings in a findings ledger and verifies rework by others. Use for 'review our docs', 'audit this policy set', 'is this documentation still right', or before publishing. Reads and measures only; never edits the documents. |
| `engagement-authorisation-guard` | route | sonnet | `Read, Grep` | Mandatory gate before any offensive-security role skill is used. Verifies that written authorisation, signed scope, rules of engagement, testing window, emergency stop procedure and named contacts exist and are current. Use for penetration testing, red teaming, social engineering, physical intrusion, adversary emulation and vulnerability research requests. Blocks the work if authorisation is absent or ambiguous. |
| `experiment-engineer` | execute | sonnet | `Read, Grep, Glob, WebSearch, Write, Edit, Bash` | Runs research and development experiments: writes a pre-registered plan with hypothesis and success criteria before anything runs, builds a deliberately disposable prototype or benchmark in an experiments/ workspace, executes it reproducibly, and records results including negative ones. Use for proof-of-concept, benchmark, spike or feasibility work in R&D. Prototypes never leave the experiments folder as production code. |
| `fabric-auditor` | inspect | haiku | `Read, Grep, Glob, WebSearch, Bash` | Independently audits a traceability fabric produced by layered justifiable delivery. Verifies the hash chain, authority signatures, well-typedness, adjacency, forward acyclicity and evidence-file integrity, and reports which fragments are justifiable under the published definition and under strict mode, with the rule that fired for each failure. Use before any fragment is treated as an authorised product, and whenever someone asks why the system is entitled to use an output. |
| `gate-auditor` | inspect | sonnet | `Read, Grep, Glob, WebSearch, Bash` | Verifies that a deliverable satisfies the output gates of the role skill that produced it, using the bundled check\_gates.py script. Use before releasing any consequential deliverable, and whenever a gate check has been asserted rather than demonstrated. Reports pass, fail or waiver problems; never fixes the deliverable itself. |
| `l1-intent` | route | opus | `Read, Grep, Glob` | Layer 1 (Intent and Context) agent for layered justifiable engagements. Establishes why the work exists, for whom, the success criteria, risk boundary and authority; issues the contract to Layer 2; reviews Layer 2 fragments; and answers the engagement's requirement upward to the human authority. Use only when the layered-justifiable-delivery skill dispatches this layer, never for a single-step task. |
| `l2-meaning` | advise | sonnet | `Read, Grep, Glob, WebSearch` | Layer 2 (Meaning and Domain Model) agent for layered justifiable engagements. Interprets the intent contract into concepts, scope, terminology and domain rules; derives contracts for Layer 3; reviews Layer 3 fragments. Use only when the layered-justifiable-delivery skill dispatches this layer. |
| `l3-policy` | advise | opus | `Read, Grep, Glob, WebSearch` | Layer 3 (Reasoning, Policy and Control) agent for layered justifiable engagements. Applies policies, controls, constraints, risk logic and acceptance criteria; derives design contracts for Layer 4; reviews Layer 4 fragments. Cannot delete a requirement: an infeasible control becomes a derived requirement for a compensating control plus a conflict. Use only when the layered-justifiable-delivery skill dispatches this layer. |
| `l4-design` | advise | sonnet | `Read, Grep, Glob, WebSearch` | Layer 4 (Solution Design) agent for layered justifiable engagements. Transforms rules and constraints into process, technical, analytical or architectural design; derives realisation contracts for Layer 5; reviews Layer 5 fragments. Returns a conflict when no feasible design satisfies the contract. Use only when the layered-justifiable-delivery skill dispatches this layer. |
| `l5-realisation` | author | opus | `Read, Grep, Glob, WebSearch, Write, Edit` | Layer 5 (Realisation and Tooling) agent for layered justifiable engagements. Builds or configures the concrete artefacts a design calls for: code, infrastructure as code, pipeline definitions, container builds, prompts, configuration. The only layer agent that writes, and it writes only in the workspace. Derives evidence contracts for Layer 6 and reviews Layer 6 fragments. Use only when the layered-justifiable-delivery skill dispatches this layer. |
| `l6-evidence` | inspect | sonnet | `Read, Grep, Glob, WebSearch, Bash` | Layer 6 (Execution and Evidence) agent for layered justifiable engagements. Executes deterministic checks and collects evidence: tests, scans, plans, queries, logs, configuration exports. Holds Bash but no Write or Edit: it has no file-editing tool, and the hooks and its instructions cover the shell. Returns observations with files the runtime hashes; never conclusions or recommendations. Use only when the layered-justifiable-delivery skill dispatches this layer. |
| `library-approver` | inspect | sonnet | `Read, Grep, Glob, WebSearch, Bash` | Reviews a staged change to the IS/IT role library and approves or rejects it. Holds no Write or Edit, so it cannot alter the proposal it is judging. Use after library-author stages a change and before library-release applies it. Checks Agent Skills compliance, the tier model, the blast radius and the reversal path, then records a decision. |
| `library-author` | author | sonnet | `Read, Grep, Glob, WebSearch, Write, Edit` | Drafts changes to the IS/IT role library: new or edited roles, archetypes, agents and generator code. Writes only into it-role-library/staging/, never into the live skills/ or agents/ directories. Use for any proposed change to the library itself. Produces the staged change, a blast-radius statement and a validator run against the staged tree, for library-approver to review. |
| `library-release` | execute | sonnet | `Read, Grep, Glob, Write, Edit, Bash` | Applies an approved staged change to the live IS/IT role library, mechanically. Use only after library-approver has approved and a human has recorded the approval. Rebuilds from the generator, re-runs the validator, updates the changelog, and reports what moved. Exercises no judgement about whether the change was a good idea. |
| `research-analyst` | research | opus | `Read, Grep, Glob, WebSearch, WebFetch` | Researches a problem: frames the question and the decision it informs, surveys prior art and current practice from primary sources, grades source reliability, lays out competing hypotheses and the evidence for each, and recommends adopt, trial, assess or hold. Also assesses experiment results against their pre-registered criteria. Use for 'research how to…', 'what is the state of the art in…', 'evaluate options for…', or the research phase of R&D. Reads and cites; never builds. |
| `role-advisor` | advise | sonnet | `Read, Grep, Glob, WebSearch` | Operates advise-tier role skills: executive, governance, assurance, audit, risk, compliance, privacy and offensive-security roles. Use when the selected role's skill declares allowed-tools of Read, Grep, Glob, WebSearch. Produces analysis, assessments, findings, option sets and recommendations in the response, never as changes to a system. |
| `role-author` | author | sonnet | `Read, Grep, Glob, WebSearch, Write, Edit` | Operates author-tier role skills: analysis, architecture, design, practice management and enablement roles. Use when the selected role's skill declares allowed-tools including Write and Edit but not Bash. Produces specifications, architectures, plans, models, designs and documentation as files. |
| `role-engineer` | execute | sonnet | `Read, Grep, Glob, WebSearch, Write, Edit, Bash` | Operates execute-tier role skills: software engineering, infrastructure, cloud, operations, testing and research roles. Use when the selected role's skill declares allowed-tools including Bash. Implements changes, runs builds and tests, and produces operational evidence. |
| `role-router` | route | haiku | `Read, Grep, Glob` | Selects which IS/IT role skill applies to a request and returns the routing decision with its reasoning. Use this first, before any role work begins, whenever a request could be handled by more than one role, names no role at all, or spans a boundary between two. Also use it to answer "who owns this?" questions about an IT operating model. |
| `sabsa-architect` | author | opus | `Read, Grep, Glob, WebSearch, Write, Edit` | Prepares, creates and updates a SABSA security architecture library: business drivers, measurable business attributes, risks and opportunities, control objectives, domains and trust, logical services, physical mechanisms, components and the service-management operations that measure them — every element traced upward to the business. Use for building a SABSA library from scratch, extending it, or updating it after a change in the business or the estate. Writes library entries; never reviews its own work. |
| `sabsa-reviewer` | inspect | sonnet | `Read, Grep, Glob, WebSearch, Bash` | Reviews a SABSA security architecture library and suggests improvements: runs the structural checks (traceability to business drivers, measurability of attributes, link integrity, matrix coverage), then judges whether each element is right and not merely present. Records located findings in a findings ledger, verifies rework, and produces ranked suggestions. Use for 'review our SABSA architecture', 'what is missing', 'is this traceable', or before a library version is approved. |
| `sod-reviewer` | route | sonnet | `Read, Grep, Glob` | Reviews a proposed set of role assignments for segregation-of-duties conflicts, using section 13 of each role skill. Use when designing a team, writing a RACI, combining roles in a small organisation, assigning someone a second hat, or investigating why a control keeps failing. Produces conflict findings and compensating-control recommendations. |
| `source-docs-engineer` | execute | sonnet | `Read, Grep, Glob, WebSearch, Write, Edit, Bash` | Adds or corrects documentation inside source files: JavaDoc, Python docstrings, XML doc comments, OpenAPI and schema annotations, README files inside modules. Use when documentation must live in the code rather than in a documentation tree. Treats every edit as a code change subject to review, build and the change path, because it is one. |

## Skill and workflow reference


### Skills

What Claude knows, and when it uses it.

The 23 skills. Claude loads a skill when a request matches its description — you do not invoke them
by name. The role-category skills route to 273 role definitions; the others orchestrate workflows.

| Skill | Roles | Allowed tools | When it is used |
| --- | --- | --- | --- |
| `defect-analysis` | — | `Read, Grep, Glob, Bash, Task, Agent` | Diagnoses a defect to its root cause before it is fixed, by three mandatory comparisons: against the last known good state (bisecting to the first bad change, without touching the working tree), against a working analogue (where the same kind of code works) and against timing (timeouts, async completion, ordering, clocks, schedules, expiry, intermittency). Then fixes it with a regression test, through the findings ledger, verified by the analyst. Use for 'why does this fail', 'this broke after the upgrade', 'it fails sometimes', 'works on staging but not production', 'fix this bug'. |
| `it-role-workflows` | — | `Read, Grep, Glob` | Enterprise workflow chains across the IS/IT role library: idea to production; new service onboarding; production change; incident to permanent fix; vulnerability to remediation; inherited codebase takeover; access request to periodic review; data product delivery; ai system from idea to approved production use; supplier onboarding to exit. Use when a request spans more than one role, when someone asks who does what next, what the hand-off is, where a delivery or incident process breaks down, or how to sequence work end to end. Each chain names the role per step, what it hands over, and the gate that must hold before the hand-off. Read the matching file in references/ before answering. |
| `it-roles-analysis` | 11 | `Read, Grep, Glob` | Analysis role skills: 11 defined roles covering business analyst; systems analyst; requirements engineer; process analyst; enterprise business analyst; data analyst; business intelligence analyst; finops analyst; and more. Use when the request involves any of these roles, their deliverables, or the design of the function itself — job descriptions, RACI, segregation of duties, maturity assessment or hiring scorecards within analysis. Read the matching file in references/ before answering. |
| `it-roles-architecture` | 12 | `Read, Grep, Glob` | Architecture role skills: 12 defined roles covering enterprise architect; business architect; solution architect; application architect; domain architect; data architect; integration architect; cloud architect; and more. Use when the request involves any of these roles, their deliverables, or the design of the function itself — job descriptions, RACI, segregation of duties, maturity assessment or hiring scorecards within architecture. Read the matching file in references/ before answering. |
| `it-roles-commercial-sourcing-and-enablement` | 14 | `Read, Grep, Glob` | Commercial, Sourcing and Enablement role skills: 14 defined roles covering it procurement specialist; vendor manager; contract manager; software licence compliance specialist; pre-sales solution consultant; sales engineer; customer success engineer; implementation consultant; and more. Use when the request involves any of these roles, their deliverables, or the design of the function itself — job descriptions, RACI, segregation of duties, maturity assessment or hiring scorecards within commercial, sourcing and enablement. Read the matching file in references/ before answering. |
| `it-roles-data-analytics-and-ai` | 21 | `Read, Grep, Glob` | Data, Analytics and AI role skills: 21 defined roles covering data engineer; analytics engineer; database administrator; database reliability engineer; data modeller; data steward; data owner; data custodian; and more. Use when the request involves any of these roles, their deliverables, or the design of the function itself — job descriptions, RACI, segregation of duties, maturity assessment or hiring scorecards within data, analytics and ai. Read the matching file in references/ before answering. |
| `it-roles-design-and-user-experience` | 11 | `Read, Grep, Glob` | Design and User Experience role skills: 11 defined roles covering ux designer; ui designer; product designer; ux researcher; usability tester; interaction designer; service designer; information architect; and more. Use when the request involves any of these roles, their deliverables, or the design of the function itself — job descriptions, RACI, segregation of duties, maturity assessment or hiring scorecards within design and user experience. Read the matching file in references/ before answering. |
| `it-roles-executive-and-leadership` | 11 | `Read, Grep, Glob` | Executive and Leadership role skills: 11 defined roles covering chief information officer; chief technology officer; chief information security officer; chief data officer; chief digital officer; chief product officer; chief ai officer; it chief of staff; and more. Use when the request involves any of these roles, their deliverables, or the design of the function itself — job descriptions, RACI, segregation of duties, maturity assessment or hiring scorecards within executive and leadership. Read the matching file in references/ before answering. |
| `it-roles-governance-risk-compliance-audit-and-privacy` | 17 | `Read, Grep, Glob` | Governance, Risk, Compliance, Audit and Privacy role skills: 17 defined roles covering it governance manager; grc analyst; it risk manager; information security officer (local); compliance officer (technology); internal it auditor; external auditor and assessor; control owner; and more. Use when the request involves any of these roles, their deliverables, or the design of the function itself — job descriptions, RACI, segregation of duties, maturity assessment or hiring scorecards within governance, risk, compliance, audit and privacy. Read the matching file in references/ before answering. |
| `it-roles-infrastructure-cloud-and-operations` | 21 | `Read, Grep, Glob` | Infrastructure, Cloud and Operations role skills: 21 defined roles covering linux systems administrator; windows systems administrator; cloud engineer; cloud operations engineer; platform engineer; devops engineer; site reliability engineer; kubernetes platform engineer; and more. Use when the request involves any of these roles, their deliverables, or the design of the function itself — job descriptions, RACI, segregation of duties, maturity assessment or hiring scorecards within infrastructure, cloud and operations. Read the matching file in references/ before answering. |
| `it-roles-network-and-telecommunications` | 9 | `Read, Grep, Glob` | Network and Telecommunications role skills: 9 defined roles covering network engineer; network administrator; network operations centre analyst; wireless and rf engineer; unified communications engineer; sd-wan and edge engineer; firewall and perimeter engineer; dns dhcp and ipam specialist; and more. Use when the request involves any of these roles, their deliverables, or the design of the function itself — job descriptions, RACI, segregation of duties, maturity assessment or hiring scorecards within network and telecommunications. Read the matching file in references/ before answering. |
| `it-roles-offensive-security-and-adversarial-testing` | 21 | `Read, Grep, Glob` | Offensive Security and Adversarial Testing role skills: 21 defined roles covering penetration tester (network and infrastructure); penetration tester (web application); penetration tester (mobile); penetration tester (api); penetration tester (cloud); penetration tester (wireless); penetration tester (thick client); red team operator; and more. Use when the request involves any of these roles, their deliverables, or the design of the function itself — job descriptions, RACI, segregation of duties, maturity assessment or hiring scorecards within offensive security and adversarial testing. Read the matching file in references/ before answering. |
| `it-roles-product-delivery-and-agile` | 17 | `Read, Grep, Glob` | Product, Delivery and Agile role skills: 17 defined roles covering product manager; product owner; technical product manager; scrum master; agile coach; delivery manager; release train engineer; epic owner; and more. Use when the request involves any of these roles, their deliverables, or the design of the function itself — job descriptions, RACI, segregation of duties, maturity assessment or hiring scorecards within product, delivery and agile. Read the matching file in references/ before answering. |
| `it-roles-quality-and-testing` | 11 | `Read, Grep, Glob` | Quality and Testing role skills: 11 defined roles covering test analyst; test automation engineer; performance test engineer; test manager; test architect; user acceptance test coordinator; accessibility tester; localisation qa analyst; and more. Use when the request involves any of these roles, their deliverables, or the design of the function itself — job descriptions, RACI, segregation of duties, maturity assessment or hiring scorecards within quality and testing. Read the matching file in references/ before answering. |
| `it-roles-research-innovation-and-specialist-engineering` | 9 | `Read, Grep, Glob` | Research, Innovation and Specialist Engineering role skills: 9 defined roles covering research engineer; innovation lead; technology scout; standards body representative; ethics and responsible technology lead; systems engineer (incose); simulation engineer; high performance computing engineer; and more. Use when the request involves any of these roles, their deliverables, or the design of the function itself — job descriptions, RACI, segregation of duties, maturity assessment or hiring scorecards within research, innovation and specialist engineering. Read the matching file in references/ before answering. |
| `it-roles-sabsa-security-architecture` | 12 | `Read, Grep, Glob` | SABSA Security Architecture role skills: 12 defined roles covering chief security architect (sabsa practice lead); business security architect (sabsa contextual layer); business attribute profiler; conceptual security architect (sabsa architect's view); logical security designer (sabsa designer's view); physical security solution builder (sabsa builder's view); security component specialist (sabsa tradesman's view); security service manager (sabsa service management view); and more. Use when the request involves any of these roles, their deliverables, or the design of the function itself — job descriptions, RACI, segregation of duties, maturity assessment or hiring scorecards within sabsa security architecture. Read the matching file in references/ before answering. |
| `it-roles-security-operations-and-defensive-security` | 24 | `Read, Grep, Glob` | Security Operations and Defensive Security role skills: 24 defined roles covering security analyst tier 1; security analyst tier 2; security analyst tier 3; soc manager; threat hunter; incident responder; digital forensics examiner; malware analyst; and more. Use when the request involves any of these roles, their deliverables, or the design of the function itself — job descriptions, RACI, segregation of duties, maturity assessment or hiring scorecards within security operations and defensive security. Read the matching file in references/ before answering. |
| `it-roles-service-management-and-support` | 17 | `Read, Grep, Glob` | Service Management and Support role skills: 17 defined roles covering service desk analyst; desktop support engineer; application support analyst; incident manager; major incident manager; problem manager; change manager; request fulfilment manager; and more. Use when the request involves any of these roles, their deliverables, or the design of the function itself — job descriptions, RACI, segregation of duties, maturity assessment or hiring scorecards within service management and support. Read the matching file in references/ before answering. |
| `it-roles-software-development-and-engineering` | 27 | `Read, Grep, Glob` | Software Development and Engineering role skills: 27 defined roles covering software engineer; senior software engineer; staff engineer; backend engineer; frontend engineer; full-stack engineer; mobile engineer; embedded firmware engineer; and more. Use when the request involves any of these roles, their deliverables, or the design of the function itself — job descriptions, RACI, segregation of duties, maturity assessment or hiring scorecards within software development and engineering. Read the matching file in references/ before answering. |
| `layered-justifiable-delivery` | — | `Read, Grep, Glob, Bash, Task, Agent` | Runs a consequential task through six layers of agents after Galambos, Towards Justifiable AI Systems (2026): requirements are transformed top-down from intent to evidence through typed contracts, products are reviewed bottom-up, unsupported work is sent back for bounded rework, conflicts escalate layer by layer to a human, and every step lands in a hash-chained traceability fabric that decides which outputs the system is entitled to use. Use for architecture decisions, infrastructure and pipeline changes, compliance evidence, security assessments, SDLC adaptation, release readiness, or any output someone will act on and must be able to justify. Also use when asked why an AI output can be trusted, to trace it, or to audit it. Not for trivial edits. |
| `library-lifecycle` | — | `Read, Grep, Glob, Bash, Task, Agent` | Runs the full lifecycle of a software product or a document library: analysis, review, development, rework and governance. Routes each activity to the right agent — codebase-reviewer or document-reviewer to analyse and review, the engineering or documentation agents to develop and rework, artefact-governor for governance — and drives review, rework and verification through a findings ledger until every finding is verified, withdrawn or accepted by you. Use for 'analyse this repository', 'review our documentation', 'rework the findings', 'improve this codebase', 'govern this library', or any multi-step work on an existing body of code or documents. For SABSA libraries use sabsa-library; for research use research-and-development. |
| `research-and-development` | — | `Read, Grep, Glob, Bash, Task, Agent` | Runs problem research and development to a decision: frames the question and the decision it informs, researches prior art from primary sources, pre-registers hypotheses and success criteria, runs disposable experiments, assesses the results against the criteria they were registered with, and ends with adopt, trial, assess or hold — or a sharper next question. Uses research-analyst for research and assessment and experiment-engineer for experiments, so whoever designs the test is not whoever wants it to pass. Use for 'research how to…', 'is it feasible to…', 'compare approaches to…', proofs of concept, benchmarks and spikes. |
| `sabsa-library` | — | `Read, Grep, Glob, Bash, Task, Agent` | Prepares, creates, updates, reviews and improves a SABSA security architecture library: business drivers, measurable business attributes, risks and opportunities, control objectives, domains, logical services, physical mechanisms, components and service-management operations, every element traced to the business. sabsa-architect writes entries, sabsa-reviewer checks traceability and measurability and judges quality, and suggestions come ranked with the next concrete step. Use for 'build a SABSA architecture for…', 'update our SABSA library', 'review our security architecture against SABSA', 'what is missing from our attribute profile', or traceability and coverage questions. |

## Runtime tool commands and options


### Tools

Everything the commands rely on, as plain tools you can run yourself. The help below is each tool's own.

Everything the commands rely on is a plain Python tool you can run
yourself, in any terminal. On Windows, write `py -3` instead
of `python3` (the installed copy of this guide already
does).

| Tool | Main commands |
| --- | --- |
| `~/.ai/it-role-house/tools/criteria.py` | `init <project>` · `show <path>` · `check <file>` |
| `~/.ai/it-role-house/tools/findings.py` | `status <ledger>` · `list <ledger>` · `report <ledger>` |
| `~/.ai/it-role-house/tools/doc_survey.py` | `<docs folder>` |
| `~/.ai/it-role-house/tools/doc_check.py` | `<source files or folders>` — documentation against the standard |
| `~/.ai/it-role-house/tools/test_check.py` | `<source files or folders>` — tests against the standard |
| `~/.ai/it-role-house/tools/defect.py` | `repeat` · `bisect` · `changes` · `compare` · `timing` · `analysis validate|render|findings` |
| `~/.ai/it-role-house/skills/it-roles-quality-and-testing/scripts/repo_survey.py` | `<repository>` |
| `~/.ai/it-role-house/tools/sabsa.py` | `init` · `new` · `check` · `matrix` · `suggest` · `trace` · `questions` · `sources` · `document` · `template` · `migrate` |
| `~/.ai/it-role-house/fabric/fabric.py` | `status` · `verify` · `justify` · `report` · `dossier` |
| `~/.ai/it-role-house/demo/demo.py` | `setup` · `reset` · `check` · `list` |

Each tool has `--help`. For example:

```
python3 ~/.ai/it-role-house/tools/doc_survey.py ~/it-role-demo/policy-docs
python3 ~/.ai/it-role-house/tools/sabsa.py matrix ~/it-role-demo/acme-pay/sabsa
```

---

#### `doc_check.py`

`~/.ai/it-role-house/tools/doc_check.py`

```
usage: doc_check.py [-h] [--json] [--errors-only] paths [paths ...]

Check source documentation against the standard.

positional arguments:
  paths

options:
  -h, --help     show this help message and exit
  --json
  --errors-only
```

#### `test_check.py`

`~/.ai/it-role-house/tools/test_check.py`

```
usage: test_check.py [-h] [--json] [--errors-only] paths [paths ...]

Check that code is accompanied by tests.

positional arguments:
  paths

options:
  -h, --help     show this help message and exit
  --json
  --errors-only
```

#### `defect.py`

`~/.ai/it-role-house/tools/defect.py`

```
usage: defect.py [-h]
                 {repeat,bisect,changes,compare,timing,analysis,selftest} ...

Defect analysis tools: last known good, working analogue, timing.

positional arguments:
  {repeat,bisect,changes,compare,timing,analysis,selftest}

options:
  -h, --help            show this help message and exit
```

##### `defect.py repeat`

```
usage: defect.py repeat [-h] [-n N] [--parallel PARALLEL] [--timeout TIMEOUT]
                        [--cwd CWD] [--json]
                        command

positional arguments:
  command

options:
  -h, --help           show this help message and exit
  -n N
  --parallel PARALLEL
  --timeout TIMEOUT
  --cwd CWD
  --json
```

##### `defect.py bisect`

```
usage: defect.py bisect [-h] --good GOOD [--bad BAD] --cmd CMD [--with WITH_]
                        [--repo REPO] [--timeout TIMEOUT] [--json]

options:
  -h, --help         show this help message and exit
  --good GOOD
  --bad BAD
  --cmd CMD
  --with WITH_
  --repo REPO
  --timeout TIMEOUT
  --json
```

##### `defect.py changes`

```
usage: defect.py changes [-h] --good GOOD [--bad BAD] [--repo REPO]

options:
  -h, --help   show this help message and exit
  --good GOOD
  --bad BAD
  --repo REPO
```

##### `defect.py compare`

```
usage: defect.py compare [-h] working failing

positional arguments:
  working
  failing

options:
  -h, --help  show this help message and exit
```

##### `defect.py timing`

```
usage: defect.py timing [-h] paths [paths ...]

positional arguments:
  paths

options:
  -h, --help  show this help message and exit
```

##### `defect.py analysis`

```
usage: defect.py analysis [-h] [--reviewer REVIEWER]
                          [--severity {critical,high,medium,low}]
                          {validate,render,findings} file

positional arguments:
  {validate,render,findings}
  file

options:
  -h, --help            show this help message and exit
  --reviewer REVIEWER
  --severity {critical,high,medium,low}
```

#### `criteria.py`

`~/.ai/it-role-house/tools/criteria.py`

```
usage: criteria.py [-h] {init,show,check,selftest} ...

Review criteria: create, resolve, check.

positional arguments:
  {init,show,check,selftest}

options:
  -h, --help            show this help message and exit
```

##### `criteria.py init`

```
usage: criteria.py init [-h] [--type {software,documents,sabsa}] project

positional arguments:
  project

options:
  -h, --help            show this help message and exit
  --type {software,documents,sabsa}
```

##### `criteria.py show`

```
usage: criteria.py show [-h] [--full] target

positional arguments:
  target

options:
  -h, --help  show this help message and exit
  --full
```

##### `criteria.py check`

```
usage: criteria.py check [-h] file

positional arguments:
  file

options:
  -h, --help  show this help message and exit
```

#### `findings.py`

`~/.ai/it-role-house/tools/findings.py`

```
usage: findings.py [-h]
                   {add,list,resolve,verify,withdraw,accept-risk,status,report,selftest}
                   ...

Findings ledger for review -> rework -> verification.

positional arguments:
  {add,list,resolve,verify,withdraw,accept-risk,status,report,selftest}

options:
  -h, --help            show this help message and exit
```

##### `findings.py add`

```
usage: findings.py add [-h] ledger file

positional arguments:
  ledger
  file

options:
  -h, --help  show this help message and exit
```

##### `findings.py list`

```
usage: findings.py list [-h] [--state STATE] ledger

positional arguments:
  ledger

options:
  -h, --help     show this help message and exit
  --state STATE
```

##### `findings.py resolve`

```
usage: findings.py resolve [-h] --by BY --note NOTE [--ref REF] ledger id

positional arguments:
  ledger
  id

options:
  -h, --help   show this help message and exit
  --by BY
  --note NOTE
  --ref REF
```

##### `findings.py verify`

```
usage: findings.py verify [-h] --by BY (--ok | --reopen) --note NOTE ledger id

positional arguments:
  ledger
  id

options:
  -h, --help   show this help message and exit
  --by BY
  --ok
  --reopen
  --note NOTE
```

##### `findings.py withdraw`

```
usage: findings.py withdraw [-h] --by BY --note NOTE ledger id

positional arguments:
  ledger
  id

options:
  -h, --help   show this help message and exit
  --by BY
  --note NOTE
```

##### `findings.py accept-risk`

```
usage: findings.py accept-risk [-h] --by BY --rationale RATIONALE --expires
                               EXPIRES
                               ledger id

positional arguments:
  ledger
  id

options:
  -h, --help            show this help message and exit
  --by BY
  --rationale RATIONALE
  --expires EXPIRES
```

##### `findings.py status`

```
usage: findings.py status [-h] ledger

positional arguments:
  ledger

options:
  -h, --help  show this help message and exit
```

##### `findings.py report`

```
usage: findings.py report [-h] ledger

positional arguments:
  ledger

options:
  -h, --help  show this help message and exit
```

#### `doc_survey.py`

`~/.ai/it-role-house/tools/doc_survey.py`

```
usage: doc_survey.py [-h] [--stale-days STALE_DAYS] [--top TOP] [--json] root

Read-only survey of a document library.

positional arguments:
  root

options:
  -h, --help            show this help message and exit
  --stale-days STALE_DAYS
  --top TOP
  --json
```

#### `sabsa.py`

`~/.ai/it-role-house/tools/sabsa.py`

```
usage: sabsa.py [-h]
                {init,new,check,suggest,report,trace,migrate,matrix,sources,questions,approval,approve,document,template,selftest}
                ...

SABSA library tool.

positional arguments:
  {init,new,check,suggest,report,trace,migrate,matrix,sources,questions,approval,approve,document,template,selftest}

options:
  -h, --help            show this help message and exit
```

##### `sabsa.py init`

```
usage: sabsa.py init [-h] --name NAME --organisation ORGANISATION --scope
                     SCOPE --owner OWNER
                     lib

positional arguments:
  lib

options:
  -h, --help            show this help message and exit
  --name NAME
  --organisation ORGANISATION
  --scope SCOPE
  --owner OWNER
```

##### `sabsa.py new`

```
usage: sabsa.py new [-h] --title TITLE [--set SET]
                    lib
                    {attribute,component,domain,driver,mechanism,objective,operation,risk,service}

positional arguments:
  lib
  {attribute,component,domain,driver,mechanism,objective,operation,risk,service}

options:
  -h, --help            show this help message and exit
  --title TITLE
  --set SET
```

##### `sabsa.py check`

```
usage: sabsa.py check [-h] [--json] lib

positional arguments:
  lib

options:
  -h, --help  show this help message and exit
  --json
```

##### `sabsa.py suggest`

```
usage: sabsa.py suggest [-h] lib

positional arguments:
  lib

options:
  -h, --help  show this help message and exit
```

##### `sabsa.py report`

```
usage: sabsa.py report [-h] lib

positional arguments:
  lib

options:
  -h, --help  show this help message and exit
```

##### `sabsa.py trace`

```
usage: sabsa.py trace [-h] lib id

positional arguments:
  lib
  id

options:
  -h, --help  show this help message and exit
```

##### `sabsa.py migrate`

```
usage: sabsa.py migrate [-h] lib

positional arguments:
  lib

options:
  -h, --help  show this help message and exit
```

##### `sabsa.py matrix`

```
usage: sabsa.py matrix [-h] [--scaffold] lib

positional arguments:
  lib

options:
  -h, --help  show this help message and exit
  --scaffold
```

##### `sabsa.py sources`

```
usage: sabsa.py sources [-h] lib

positional arguments:
  lib

options:
  -h, --help  show this help message and exit
```

##### `sabsa.py questions`

```
usage: sabsa.py questions [-h] lib

positional arguments:
  lib

options:
  -h, --help  show this help message and exit
```

##### `sabsa.py approval`

```
usage: sabsa.py approval [-h] lib

positional arguments:
  lib

options:
  -h, --help  show this help message and exit
```

##### `sabsa.py approve`

```
usage: sabsa.py approve [-h] --by BY [--note NOTE] lib

positional arguments:
  lib

options:
  -h, --help   show this help message and exit
  --by BY
  --note NOTE  approval note / decision reference
```

##### `sabsa.py document`

```
usage: sabsa.py document [-h] [--out OUT] [--template-name TEMPLATE_NAME]
                         [--template TEMPLATE] [--reference REFERENCE]
                         lib

positional arguments:
  lib

options:
  -h, --help            show this help message and exit
  --out OUT             output file; its extension sets the format (.md .html
                        .docx .odt .pdf)
  --template-name TEMPLATE_NAME
                        which template: architecture, client-questions, ...
  --template TEMPLATE   use this template file instead of resolving one
  --reference REFERENCE
                        a .docx whose styles a Word output should use (the
                        client's template)
```

##### `sabsa.py template`

```
usage: sabsa.py template [-h] [--name NAME] [--init] [--fields] [--check FILE]
                         lib

positional arguments:
  lib

options:
  -h, --help    show this help message and exit
  --name NAME
  --init        copy the package default into <lib>/templates/ to edit
  --fields      list every field a template can use
  --check FILE  render FILE against the library and report unknown fields
```

#### `fabric.py`

`~/.ai/it-role-house/fabric/fabric.py`

```
usage: fabric.py [-h] [--version]
                 {init,req,contract,render-contract,ingest,answer,release,render-review,ingest-reviews,evidence,review,consolidate,conflict,escalate,reformulate,propose,dossier,authorise,keygen,verify,status,report,justify,selftest}
                 ...

Traceability fabric for layered justifiable engagements.

positional arguments:
  {init,req,contract,render-contract,ingest,answer,release,render-review,ingest-reviews,evidence,review,consolidate,conflict,escalate,reformulate,propose,dossier,authorise,keygen,verify,status,report,justify,selftest}

options:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
```

##### `fabric.py init`

```
usage: fabric.py init [-h] --intent INTENT --owner OWNER [--success SUCCESS]
                      [--boundary BOUNDARY]
                      engagement

positional arguments:
  engagement

options:
  -h, --help           show this help message and exit
  --intent INTENT
  --owner OWNER
  --success SUCCESS
  --boundary BOUNDARY
```

##### `fabric.py req`

```
usage: fabric.py req [-h] --layer LAYER --from FROM --label {derives,refines}
                     --text TEXT
                     engagement

positional arguments:
  engagement

options:
  -h, --help            show this help message and exit
  --layer LAYER
  --from FROM
  --label {derives,refines}
  --text TEXT
```

##### `fabric.py contract`

```
usage: fabric.py contract [-h] --from FROM [--what WHAT] [--why WHY]
                          [--who WHO] [--where WHERE] [--when WHEN]
                          [--how HOW] [--evidence EVIDENCE]
                          [--escalate-if ESCALATE_IF] [--sanitise SANITISE]
                          [--rework-of REWORK_OF]
                          engagement

positional arguments:
  engagement

options:
  -h, --help            show this help message and exit
  --from FROM
  --what WHAT
  --why WHY
  --who WHO
  --where WHERE
  --when WHEN
  --how HOW
  --evidence EVIDENCE
  --escalate-if ESCALATE_IF
  --sanitise SANITISE
  --rework-of REWORK_OF
```

##### `fabric.py render-contract`

```
usage: fabric.py render-contract [-h] engagement contract

positional arguments:
  engagement
  contract

options:
  -h, --help  show this help message and exit
```

##### `fabric.py ingest`

```
usage: fabric.py ingest [-h] --contract CONTRACT engagement result

positional arguments:
  engagement
  result               JSON file returned by the layer agent, or - for stdin

options:
  -h, --help           show this help message and exit
  --contract CONTRACT
```

##### `fabric.py answer`

```
usage: fabric.py answer [-h] --requirement REQUIREMENT --text TEXT
                        [--supported-by SUPPORTED_BY [SUPPORTED_BY ...]]
                        engagement

positional arguments:
  engagement

options:
  -h, --help            show this help message and exit
  --requirement REQUIREMENT
  --text TEXT
  --supported-by SUPPORTED_BY [SUPPORTED_BY ...]
```

##### `fabric.py release`

```
usage: fabric.py release [-h] engagement fragment

positional arguments:
  engagement
  fragment

options:
  -h, --help  show this help message and exit
```

##### `fabric.py render-review`

```
usage: fabric.py render-review [-h] engagement contract

positional arguments:
  engagement
  contract

options:
  -h, --help  show this help message and exit
```

##### `fabric.py ingest-reviews`

```
usage: fabric.py ingest-reviews [-h] --layer LAYER --reviewer REVIEWER --model
                                MODEL
                                engagement result

positional arguments:
  engagement
  result

options:
  -h, --help           show this help message and exit
  --layer LAYER
  --reviewer REVIEWER
  --model MODEL
```

##### `fabric.py evidence`

```
usage: fabric.py evidence [-h] --layer LAYER [--supports [SUPPORTS ...]]
                          [--contradicts [CONTRADICTS ...]] --source SOURCE
                          --confidence
                          {deterministic,observation,interpretation,ai_derived}
                          [--file FILE]
                          engagement

positional arguments:
  engagement

options:
  -h, --help            show this help message and exit
  --layer LAYER
  --supports [SUPPORTS ...]
  --contradicts [CONTRADICTS ...]
  --source SOURCE
  --confidence {deterministic,observation,interpretation,ai_derived}
  --file FILE
```

##### `fabric.py review`

```
usage: fabric.py review [-h] --layer LAYER --state
                        {accepts,accepts_with_constraints,correlates,resonates,insufficient,out_of_scope,conflicts,escalate}
                        --rationale RATIONALE --reviewer REVIEWER --model
                        MODEL [--constraints CONSTRAINTS]
                        engagement fragment

positional arguments:
  engagement
  fragment

options:
  -h, --help            show this help message and exit
  --layer LAYER
  --state {accepts,accepts_with_constraints,correlates,resonates,insufficient,out_of_scope,conflicts,escalate}
  --rationale RATIONALE
  --reviewer REVIEWER
  --model MODEL
  --constraints CONSTRAINTS
```

##### `fabric.py consolidate`

```
usage: fabric.py consolidate [-h] --layer LAYER engagement fragment

positional arguments:
  engagement
  fragment

options:
  -h, --help     show this help message and exit
  --layer LAYER
```

##### `fabric.py conflict`

```
usage: fabric.py conflict [-h] --from FROM --layer LAYER --text TEXT
                          engagement

positional arguments:
  engagement

options:
  -h, --help     show this help message and exit
  --from FROM
  --layer LAYER
  --text TEXT
```

##### `fabric.py escalate`

```
usage: fabric.py escalate [-h] [--layer LAYER] --reason REASON --code
                          {exhausted,no_viable_reformulation,outside_authority,relay,budget}
                          [--to-top]
                          engagement from

positional arguments:
  engagement
  from

options:
  -h, --help            show this help message and exit
  --layer LAYER
  --reason REASON
  --code {exhausted,no_viable_reformulation,outside_authority,relay,budget}
  --to-top              relay all the way to L1 (budget exhaustion)
```

##### `fabric.py reformulate`

```
usage: fabric.py reformulate [-h] --text TEXT --change CHANGE [--what WHAT]
                             [--why WHY] [--who WHO] [--where WHERE]
                             [--when WHEN] [--how HOW] [--evidence EVIDENCE]
                             [--escalate-if ESCALATE_IF] [--sanitise SANITISE]
                             engagement escalation

positional arguments:
  engagement
  escalation

options:
  -h, --help            show this help message and exit
  --text TEXT
  --change CHANGE
  --what WHAT
  --why WHY
  --who WHO
  --where WHERE
  --when WHEN
  --how HOW
  --evidence EVIDENCE
  --escalate-if ESCALATE_IF
  --sanitise SANITISE
```

##### `fabric.py propose`

```
usage: fabric.py propose [-h] --requirement REQUIREMENT --text TEXT --tradeoff
                         TRADEOFF
                         engagement

positional arguments:
  engagement

options:
  -h, --help            show this help message and exit
  --requirement REQUIREMENT
  --text TEXT
  --tradeoff TRADEOFF
```

##### `fabric.py dossier`

```
usage: fabric.py dossier [-h] [--examples EXAMPLES] engagement escalation

positional arguments:
  engagement
  escalation

options:
  -h, --help           show this help message and exit
  --examples EXAMPLES
```

##### `fabric.py authorise`

```
usage: fabric.py authorise [-h] --decision
                           {accept,exception,revise,reject,terminate} --signer
                           SIGNER [--rationale RATIONALE] [--expires EXPIRES]
                           [--revise-text REVISE_TEXT]
                           [--supersedes SUPERSEDES] [--adopt ADOPT]
                           [--beyond-round-limit]
                           engagement escalation

positional arguments:
  engagement
  escalation

options:
  -h, --help            show this help message and exit
  --decision {accept,exception,revise,reject,terminate}
  --signer SIGNER
  --rationale RATIONALE
  --expires EXPIRES
  --revise-text REVISE_TEXT
  --supersedes SUPERSEDES
  --adopt ADOPT
  --beyond-round-limit
```

##### `fabric.py keygen`

```
usage: fabric.py keygen [-h]

options:
  -h, --help  show this help message and exit
```

##### `fabric.py verify`

```
usage: fabric.py verify [-h] engagement

positional arguments:
  engagement

options:
  -h, --help  show this help message and exit
```

##### `fabric.py status`

```
usage: fabric.py status [-h] engagement

positional arguments:
  engagement

options:
  -h, --help  show this help message and exit
```

##### `fabric.py report`

```
usage: fabric.py report [-h] engagement

positional arguments:
  engagement

options:
  -h, --help  show this help message and exit
```

##### `fabric.py justify`

```
usage: fabric.py justify [-h] [--strict] [--json] engagement [fragment]

positional arguments:
  engagement
  fragment

options:
  -h, --help  show this help message and exit
  --strict
  --json
```

#### `demo.py`

`~/.ai/it-role-house/demo/demo.py`

```
usage: demo.py [-h] {list,setup,reset,check,selftest} ...

Demo kit for the IS/IT role library.

positional arguments:
  {list,setup,reset,check,selftest}

options:
  -h, --help            show this help message and exit
```

##### `demo.py list`

```
usage: demo.py list [-h]

options:
  -h, --help  show this help message and exit
```

##### `demo.py setup`

```
usage: demo.py setup [-h] [--to TO] [--force]

options:
  -h, --help  show this help message and exit
  --to TO
  --force
```

##### `demo.py reset`

```
usage: demo.py reset [-h] [--to TO] name

positional arguments:
  name

options:
  -h, --help  show this help message and exit
  --to TO
```

##### `demo.py check`

```
usage: demo.py check [-h]

options:
  -h, --help  show this help message and exit
```

#### `repo_survey.py`

`~/.ai/it-role-house/skills/it-roles-quality-and-testing/scripts/repo_survey.py`

```
usage: repo_survey.py [-h] [--since SINCE] [--top TOP] [--json] repo

Read-only survey of a repository.

positional arguments:
  repo

options:
  -h, --help     show this help message and exit
  --since SINCE  git history window, e.g. 6.months
  --top TOP
  --json
```
