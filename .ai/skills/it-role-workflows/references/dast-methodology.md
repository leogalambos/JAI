# DAST integration methodology for existing CI/CD pipelines

Apply this reference to web applications, APIs, modular systems and
microservices deployed in containers or isolated remote test environments.
Use `integration` when the control must be introduced, `qualification` when
an implementation already exists, `release-evidence` for a specific candidate,
and `continuous-assurance` for operating results and change. The organisation
sets mandatory scopes, authorities, thresholds, retention and remediation
targets. DAST complements source, dependency and image analysis, specialised
authorisation and business-logic tests, and independent penetration testing.

JAI can design and implement defensive pipeline components and validate them
with synthetic or recorded evidence. AppSec supplies the approved assessment
profile and real qualification observations through the organisation's
externally operated assessment process. This reference specifies what evidence
JAI must require at that boundary.

## Accountability and decision rights

| Accountable duty | Responsibility and JAI assignment |
| --- | --- |
| Application Owner (AO) | Mandate, funding, application ownership, remediation capacity and operational takeover. Named human authority. |
| Delivery Owner (DEL) | Implementation coordination, dependencies, staffing, escalations and closure. Assign a Delivery Manager. |
| Security Architect (SA) | Requirements, security design, acceptance criteria, fidelity and architecture compliance. |
| Solution Architect (SOL) | Current and target solution, feasibility, deployment decision and technical compliance. |
| DAST Control Owner (DCO) | Measurement, profile approval, qualification, triage, retest evidence and requalification. Assign a Control Owner. |
| AppSec Engineer (ASE) | Scanner expertise, profile and capability evidence, coverage interpretation and finding disposition under DCO. |
| Development Lead (DEV) | Application testability, contracts, fixtures and remediation. Assign Software Engineer for implementation. |
| DevSecOps Lead (DO) | Pipeline, test deployment, readiness, execution evidence and cleanup. Assign CI/CD Platform Engineer. |
| Infrastructure Lead (INF) | Network boundaries, capacity and isolation. Assign the appropriate infrastructure and network specialists. |
| IAM Lead (IAM) | Test identities, certificates and secret delivery. Assign IAM Engineer for implementation. |
| Scanner Platform Owner (DPO) | Approved images, dependencies, availability, hardening and upgrades. Assign Container Platform Engineer for implementation. |
| QA Lead (QA) | System qualification, positive, negative and regression evidence. Assign Test Manager. |
| Release Platform Owner (RPO) | Protected evidence verification and promotion enforcement. Assign Release Engineer for implementation. |
| Security Governance (SG) | Mandatory policy, non-waivable requirements and control exception authority. |
| Independent Security Reviewer (ISR) | Review exact versions and issue a bounded verdict. Assign Internal IT Auditor with relevant competence and independence. |
| Security Approval Authority (SAA) | Formal acceptance of the qualified control scope. Named human authority. |
| Release Authority (RA) | Authorise exact candidate promotion under all mandatory gates. Named human authority. |
| Risk Owner (RO) | Risk classification and residual risk acceptance within mandate. Named human authority. |

Use one accountable owner per deliverable. Record responsible implementers,
consulted specialists, informed stakeholders and named decision principals.
Reviewers must be independent of the work reviewed. Keep implementation,
evidence verification, policy administration and release permissions separated.
ISR may also fulfil SAA only with explicit authority and independence from
design and implementation. The Delivery Owner coordinates without acquiring
risk or approval authority.

### Responsibility assignments

One role is accountable per output. The accountable owner assigns qualified
people and confirms their authority and separation at the start of the project.
The following assignments supplement the gate and workstream ownership above.

| Output or activity | Accountable | Responsible | Consulted | Informed |
| --- | --- | --- | --- | --- |
| Mandate and funding | AO | DEL | RO, SA | DCO, SOL |
| Delivery plan, coordination and escalation | DEL | DEL, team leads | AO, SA, SOL | SG |
| Initial risk classification | RO | RO | AO, SA, SG | DEL |
| Current architecture and readiness | SOL | SOL, DEV, DO, ASE, INF, IAM | SA, QA | DEL |
| Independent interface inventory | SOL | DEV, ASE | SA, DCO, INF | DEL |
| Scanner capability and feasibility observation | DCO | ASE | SOL, SA, DPO, IAM | DEL |
| Security requirements and acceptance criteria | SA | SA | SG, DCO, SOL, RO | DEL |
| Target security architecture | SA | SA | SOL, DCO, INF, IAM, RPO | DEL |
| Target solution and deployment decision | SOL | SOL | SA, DEV, DO, INF, IAM, ASE, DPO | DEL |
| Security adequacy of deployment decision | SA | SA | SOL, DCO, INF | DEL |
| Test deployment specification | SOL | SOL, DO, INF | SA, DEV, QA, IAM | DEL |
| System and integration qualification plan | QA | QA | DO, DEV, INF, IAM, RPO | DEL |
| DAST qualification plan | DCO | ASE, QA | SA, SOL, DO | DEL |
| Application and testability changes | DEV | Developers | SOL, ASE, QA | DEL |
| CI/CD integration | DO | DevSecOps engineers | SOL, SA, ASE, INF, IAM | DEL |
| Profile, coverage and validity | DCO | ASE | SA, DEV, QA, IAM, DO | DEL |
| Test environment networking and isolation | INF | Infrastructure engineers | SOL, SA, DO | DEL |
| Test identities, credentials and certificates | IAM | IAM engineers | SA, ASE, DO | DEL |
| Scanner platform and approved versions | DPO | Platform engineers | DO, DCO, SA | DEL |
| Security Gate policy | SG | Governance specialists | SA, DCO, RO, RPO | RA, AO |
| Gate implementation and enforcement | RPO | Release platform engineers | SA, SG, DO, DCO | RA, DEL |
| Technical integration qualification | DO | DevSecOps, DEV, INF, IAM | QA, SOL, ASE | DEL |
| System and negative qualification | QA | QA engineers | DEV, DO, ASE, RPO | DEL |
| DAST security qualification | DCO | ASE, QA | SA, SOL, DO | ISR, DEL |
| Fidelity and trust boundary assessment | SA | SA, SOL, INF | DCO, DO, IAM | ISR |
| Release enforcement qualification | RPO | Release platform engineers, QA | SA, SG, DCO, DO | ISR |
| Security architecture compliance | SA | SA | SOL, DCO | ISR |
| Solution architecture compliance | SOL | SOL | DEV, DO, INF | ISR |
| Independent security assessment | ISR | ISR | SA, SOL, DCO, QA, RPO | SAA |
| Formal security acceptance | SAA | SAA | ISR, SG | AO, DEL |
| Risk acceptance | RO | RO | SG, SA, DCO, AO | SAA, RA |
| Control exception | SG | Governance specialists | RO, SA, DCO, RPO | AO, RA |
| Operational transition | AO | DEL, DCO, DO, DPO, DEV, RPO | SA, SOL, QA | SG |
| Routine test lifecycle and cleanup | DO | DevSecOps engineers | DCO, DEV, INF, IAM | AO |
| Per-run validity methodology | DCO | ASE | SA, QA, DO, RPO | SG |
| Evidence verification and gate decision | RPO | Release platform engineers | DCO, SG, DO | AO, RA |
| Release authorisation | RA | Release management | SG, RPO | AO |
| Triage and false-positive disposition | DCO | ASE | DEV, QA | AO |
| Remediation SLA and prioritisation | AO | DEV | DCO, SA, RO | SG |
| Remediation changes | DEV | Developers | SOL, ASE, QA | AO |
| Remediation verification | DCO | ASE, QA | DEV | AO |
| Scanner lifecycle | DPO | Platform engineers | DCO, DO | AO |
| Quality monitoring and requalification | DCO | ASE, QA, DO | SA, SOL, DPO, RPO | AO, SG |

## Implementation lifecycle

| Phase and JAI stages | Required work and handoff |
| --- | --- |
| A0 · 9 | AO records the project mandate, resources and scope, DEL records the delivery plan and responsibilities, SG supplies policy, and RO supplies the initial risk classification. |
| A1 · 1 | SOL inventories application modules, UI, API contracts including protocol variants, routes, trust boundaries and dependencies. Review manifests, startup, pipeline, gateway, network, IAM, test data and scanner limitations. Compare independent source-derived inventory to observations supplied by AppSec. Deliver current architecture, readiness and gaps. |
| A2 · 2 | SA maps risks and policy to the requirement catalogue, target security design, acceptance criteria, coverage matrix and requirements traceability. DCO owns measurement design. |
| A3 · 10 | SOL compares topology options and supplies feasibility observations, architecture decisions, environment specification and backlog. Obtain SA's adequacy assessment and QA and DCO qualification plans. Rework requirements or design if infeasible. Escalate remaining conflicts to DEL, SG and RO. |
| A4 · 11–17 | DEL coordinates separately owned workstreams. Bind each change and local test result to the approved design and verify every prerequisite before dependent work. Record evidenced no-change dispositions where existing components suffice. |
| A5 · 18, 3 | QA verifies integration and negative cases. DO, DCO, SA and RPO each provide technical, DAST, fidelity and enforcement qualification for their own scope. Consolidate actual results and unresolved gaps by requirement. |
| A6 · 4, 5 | SOL and SA attest architecture compliance for their scope. ISR reviews exact artefacts, evidence and limitations. SAA records a formal decision. RO and SG separately record risk and permitted control exceptions. Rework rejected scope. |
| A7 · 19 | AO takes over qualified configurations, support, access, metrics, remediation and requalification. DEL closes the delivery mandate. The gate must already be implemented and qualified. |

A1 and A2 may iterate. A4 workstreams may proceed concurrently where
dependencies allow. A5 consumes all applicable outputs. Findings return to the
responsible phase. Technical receipts never replace actual authority.

| Workstream | Accountable owner and completion evidence |
| --- | --- |
| Application · 11 | DEV supplies changes to startup, readiness, API contracts and isolated fixture lifecycle, or a reviewed no-change disposition. Preserve standard access controls and isolate test-only fixtures from shipped artefacts. |
| Pipeline · 16 | DO supplies candidate identity, test deployment and readiness, protected supplied-report intake, time/resource failure handling, evidence retention and teardown. Use synthetic inputs to verify integration. |
| Control interface · 15 | DCO supplies approval, version and scope of the external profile, required perspectives and identities, validity signals, evidence schema and complementary methods. ASE supplies the actual report and capability evidence. |
| Infrastructure · 12 | INF supplies isolated domains, DNS, constrained connectivity and egress, capacity, teardown and concurrency tests. |
| IAM · 13 | IAM supplies scoped identities, issuance, secret delivery, revocation evidence and role checks for required perspectives. |
| Platform · 14 | DPO supplies approved image digest, dependencies and add-ons, hardening, support and change ownership. |
| Enforcement · 17 | RPO supplies protected policy evaluation, evidence and exception verification, promotion permissions and negative enforcement tests. |

### Deployment patterns and fidelity

DAST examines a running application. The pipeline or test platform owns
provisioning and deployment. Choose a topology using the required network
perspectives, trust boundaries, artefact identity, fidelity, concurrent use,
capacity and evidence trust.

| Pattern | Fit and decision evidence |
| --- | --- |
| A · combined runtime | An exceptional bounded feasibility option. Shared process environment and filesystem weaken isolation and can change the artefact under test. Require explicit evidence of acceptable integrity and fidelity. |
| B · separate containers, dedicated network | Starting option for a single service or API. Resources can be independently versioned and cleaned up. Verify actual isolation. A direct backend path provides no evidence about a gateway that it does not traverse. |
| C · ephemeral representative stack | Starting option for integrated microservices. Record exact manifest, dependency and data versions, relevant gateway and IAM behaviour and separate internal and external perspectives. Assess provisioning, concurrency and capacity. |
| D · remote assessment platform | Suitable for established central platforms or unavailable local fidelity. Require evidence of exact deployed identity, environment reservation, authenticated provenance and correlation. Check for target changes and concurrent activity during the assessment. |
| E · separate containers, shared network namespace | Containers can have distinct filesystems while sharing a network identity. Assess shared network trust and relevance to each scenario before accepting evidence. |

The SOL decision records alternatives and observed feasibility. SA assesses
the security impact of deviations in IAM, mTLS, gateway, WAF, routing, feature
flags, data and mocked dependencies. Keep direct and gateway evidence distinct.
A critical unsupported scenario requires a complementary control or permitted
exception. A successful platform startup is insufficient feasibility evidence.

Model the build domain, test environment and protected control domain. Bind
built artefacts to observed deployment and protect scanner provenance, profile,
test identity, evidence collection, policy and promotion permissions. Treat
application responses as untrusted. Use a pinned, approved image and record
add-on versions. Apply least privilege and avoid granting access to the
container-engine socket. Restrict the runner's network scope, handle secrets
through protected delivery, and isolate evidence and policy administration.
Bound alternatives to production promotion using actual permissions and review
the trusted administrator assumptions.

### Typical testability changes

| Readiness issue | Candidate design change |
| --- | --- |
| Deployment needs manual startup | Review Dockerfile, startup, manifests and dependency configuration. |
| URLs or dependencies are hard-coded | Parameterise addresses and runtime configuration. |
| Readiness cannot be determined | Provide health, readiness and functional preconditions. |
| Required application state is absent | Provision controlled seed/reset and isolated fixture state. |
| Contract is incomplete | Maintain versioned API contracts and reconcile them with actual routing. |
| Test identities are unavailable | Provide supported scoped identities and verify standard access controls. |
| Dependencies cannot be replicated | Use controlled test instances or mocks with a fidelity assessment. |
| Concurrent workloads share mutable state | Separate state, identities and networks or reserve an exclusive environment. |
| Required business sequence is missing | Provide controlled initial states or specialised complementary tests. |

## Security requirements catalogue

For each applicable item record the source risk or policy, named owner,
architectural decision, implementation reference, expected test, actual evidence
and disposition. Record a reason for non-applicability and retain every gap.

| ID | Requirement |
| --- | --- |
| SR-01 | Identify independently derived attack surface and approved scope. |
| SR-02 | Measure coverage against the independent inventory and mandatory scenarios. |
| SR-03 | Account for required authenticated and anonymous perspectives and roles. |
| SR-04 | Use a representative test environment with assessed deviations. |
| SR-05 | Isolate test activity from unauthorised systems and production data. |
| SR-06 | Require approved rules of engagement and evidence of bounded effects. |
| SR-07 | Preserve repeatability through versioned execution conditions. |
| SR-08 | Validate each mandatory run and required context. |
| SR-09 | Bind evidence to the candidate, configuration and run. |
| SR-10 | Protect configuration, execution, evidence and decisions against unauthorised change. |
| SR-11 | Maintain evidence authenticity, completeness, availability, auditability and retention. |
| SR-12 | Enforce policy on the protected promotion path. |
| SR-13 | Require exact, authorised and time-limited exceptions. |
| SR-14 | Track uncovered scenarios, alternative testing and permitted dispositions. |
| SR-15 | Requalify periodically and after relevant change. |
| SR-16 | Protect identities, secrets, test data, reports and recorded traffic. |
| SR-17 | Verify scanner image, dependency and add-on provenance. |
| SR-18 | Separate application, runner and protected components. |
| SR-19 | Restrict network reach to approved scope and required supporting services. |
| SR-20 | Minimise privileges and withhold unnecessary host and engine access. |
| SR-21 | Verify tested artefacts match promotion artefacts, or reassess after change. |
| SR-22 | Provision, isolate, remove and revoke temporary resources and credentials. |
| SR-23 | Isolate concurrent runs, identities, state, network names and evidence. |
| SR-24 | Bound compute, time and concurrency and detect incomplete runs. |
| SR-25 | Protect profiles and templates and validate approved runtime scope. |
| SR-26 | Preserve and record the relevant network path and security mechanisms per scenario. |
| SR-27 | Check freshness and binding and reject replay. |
| SR-28 | Retain partial findings and govern triage, false-positive disposition, remediation and retest. |

For example, bind SR-03 and SR-08 to an identity decision, test identity
configuration and normal and expired session observations. Bind SR-19 and
SR-26 to the topology decision and observed permitted and denied connectivity.
Bind SR-09, SR-21 and SR-27 to the candidate manifest and rejection of evidence
from another candidate. Bind SR-12 to promotion policy and evidence that a
missing decision prevents promotion.

## Qualification and coverage

Qualification establishes that the integrated control works within a defined
scope. Each run still requires separate validity evaluation. Record interfaces,
operations, required roles, application states and network perspectives.
For each scenario record required methods, expected results, owner, actual
observations and gaps. Preserve complementary tests for business logic,
authorisation and unsupported protocols.

For example, a coverage matrix can distinguish anonymous external access,
horizontal authorisation across accounts, administrative access, application
input validation and a service-identity internal operation. A single route may
have multiple mandatory scenarios. Track the scenario ID, method and route,
identity, application state, network perspective, expected policy outcome,
required test method and actual evidence. Inventory from a contract or a
successful HTTP response alone does not establish valid coverage.

Use an independent versioned denominator. Interface coverage counts validly
tested operations against all required operations. DAST scenario coverage
counts validly executed DAST scenarios against all required DAST scenarios.
Overall scenario coverage counts scenarios completed using every required
method against the total required. Discovery coverage counts discovered
operations against the independent required inventory. A zero denominator is
N/A with rationale. For example, 75 valid operations out of 100 required is
75% coverage even when the scanner discovered only 80. Coverage measures
execution under the required conditions. Findings measure observed problems.

| ID | Acceptance criterion and evidence |
| --- | --- |
| AC-01 | Approved scope and execution evidence for every mandatory critical scenario. |
| AC-02 | Coverage meets application-specific thresholds using the required denominator. |
| AC-03 | Actual identity and expected role demonstrated for every required authenticated context. |
| AC-04 | Session loss detected. Require valid replacement evidence or record invalidity. |
| AC-05 | Mandatory jobs complete. Interrupted and timed-out work cannot count as valid. |
| AC-06 | Observed deployment, readiness and approved fidelity differences match the qualification. |
| AC-07 | Required evidence has verified origin, integrity, scope, freshness and exact binding. |
| AC-08 | AppSec supplies independent detection qualification from a separate controlled reference target. |
| AC-09 | Isolation tests show approved connectivity and denial of out-of-scope access. |
| AC-10 | Negative gate tests show blocked promotion without trustworthy evidence and authority. |
| AC-11 | Teardown and revocation are evidenced on success and failure. |
| AC-12 | Concurrent runs preserve separate targets, credentials, state and outputs. |

Thresholds are configured under policy. A coverage percentage cannot
compensate for missing critical scenarios. Record exceptions separately and
retain measured coverage.

| Minimum qualification case | Expected outcome / owner |
| --- | --- |
| Correct deployment and complete valid evidence | Valid, traceable result / DCO |
| Wrong deployment, stale evidence or candidate replay | Rejected / RPO |
| Unavailable service or incomplete test state | Readiness failure / DO |
| Failed authentication or expired session | Invalid context unless valid replacement evidence exists / DCO |
| Scanner error, timeout or incomplete jobs | Error or invalid, with retained partial findings / DCO |
| External detection qualification observation | Expected findings in separately controlled evidence supplied by AppSec / DCO |
| Policy violation | Block unless exact policy-permitted disposition is current / RPO |
| Missing, altered or unauthenticated report | Block / RPO |
| Expired, insufficient or absent exception | Block / RPO |
| Mandatory gate missing, profile mismatch or unauthorised promotion path | Block / RPO |
| Out-of-scope connectivity or redirect | Denied and recorded / INF |
| Untrusted application output or evidence modification attempt | Protected evidence and runner boundaries / QA |
| Concurrent or interrupted run | Isolated state and observed cleanup with preserved findings / QA and DO, each for their result |

## Recurring execution and evidence handoff

Separate fast feedback, integration, release qualification and periodic deeper
assurance. Policy specifies when each tier is required. A fast-feedback result
can satisfy a release rule only when policy allows it and candidate identity,
scope, configuration, qualification and freshness all match.

| Tier | Typical trigger | Decision use |
| --- | --- | --- |
| T1 · Fast feedback | Pull request or merge | Early bounded evidence for developers. |
| T2 · Integration | Significant change or scheduled integration | Required application identities, integrated APIs and environment behaviour. |
| T3 · Release qualification | Release candidate or promotion | Mandatory candidate-bound evidence under release policy. |
| T4 · Deeper assurance | Periodic or material risk change | Extended coverage and independently commissioned specialist evidence. |

For every required run the project pipeline prepares the immutable candidate
manifest, provisions isolated resources, verifies observed deployment and
readiness, initialises test data and scoped identities, and hands off the exact
candidate to the approved organisational assessment process. That process
returns scope, identity, job completion, validity, quality signals and findings.
Verify actual deployment identity, context and profile against qualification.
Preserve authenticated reports even when incomplete. Revoke access and remove
temporary resources on failure or cancellation as well as success. If evidence
transfer fails, block promotion and continue safe cleanup. Escalate delayed
cleanup. A remote platform must supply stable job correlation, observed
deployment and evidence of environment stability.

Before accepting external work, require recorded rules of engagement with
exact targets, environments, ownership, allowed operations, prohibited actions,
allowed protocols, ports and identities, redirect, DNS and callback restrictions,
rate, concurrency, resource and time limits, incident contacts, stop conditions,
data protection, third-party permissions, recovery and cleanup. Retain approval and expiry. JAI consumes
the corresponding authorisation and externally supplied results.

| Recurring boundary | Owner | Evidence supplied to the next duty |
| --- | --- | --- |
| Candidate build and identity | DO | Immutable artefacts and release candidate manifest. |
| Environment provisioning | DO | Isolated instance, network boundaries and run identity. |
| Deployment | DO | Observed component identities and security-relevant configuration. |
| Controlled application state | DEV | Fixture, identity and state initialisation evidence. |
| Readiness and fidelity | DO | Functional preconditions and conformance to the qualified environment profile. |
| Scanner platform readiness | DO | Approved platform identity and bounded runtime record. |
| Profile and credential readiness | DO | Approved configuration reference and scoped identity record, with IAM evidence. |
| Target and identity verification | DCO | Observed target, perspective and role evidence from the authorised assessment. |
| External assessment | DO | AppSec-supplied completion, logs, results and partial findings for the exact run. |
| Validity and coverage | DCO | Per-context result, denominator revision and uncovered conditions. |
| Protected evidence transfer | RPO | Verified and auditable candidate/run binding and evidence receipt. |
| Cleanup and revocation | DO | Observed teardown and access revocation, with unresolved failures escalated. |
| Triage and policy inputs | DCO | Normalised findings and traceable dispositions. |
| Gate evaluation and enforcement | RPO | Protected candidate-bound ALLOW, ALLOW_WITH_EXCEPTION or BLOCK record. |
| Release authorisation | RA | Decision for the exact manifest after all applicable controls. |

The evidence and gate assessment can proceed after test resource cleanup.
Triage may happen before or after the initial gate evaluation. Pending triage
cannot be interpreted as compliance. Record any revised decision as a new
evaluation against the same candidate and updated evidence.

| Evidence category | Required content |
| --- | --- |
| Candidate | Application, build/commit, exact manifest, image digests and security-relevant configuration. |
| Runtime | Run and job identity, start/end, authorised runner and actual observed deployment. |
| Control | Scanner build/digest, add-ons, approved profile, tier and qualification. |
| Scope | Inventory and scenario revisions, identities and roles, perspectives and preconditions. |
| Validity | Identity/session signals, completion, coverage, errors and limits. |
| Findings | Raw and normalised results, stable identifiers and auditable dispositions, including partial runs. |
| Integrity | Authenticated provenance, hashes, protected verification and attestation where required. |
| Decision | Exact policy and candidate, applicability, validity, compliance, exception evidence, outcome and audit record. |

Restrict and sanitise reports and recording access according to classification.
Never place credential material in evidence manifests. Preserve the meaning of
sanitised evidence and restrict access to originals.

## Output Security Gate and exceptions

Track validity (`VALID`, `INVALID`, `ERROR`, `MISSING`, `UNTRUSTED`),
policy compliance (`COMPLIANT`, `NON_COMPLIANT`, `UNKNOWN`) and gate
decision separately. `NOT_REQUIRED` is an applicability decision under
authorised policy. Known findings remain visible when overall compliance is
`UNKNOWN`.

| Applicability or validity | Compliance and evidence | Gate result |
| --- | --- | --- |
| VALID | COMPLIANT | ALLOW |
| VALID | NON_COMPLIANT and every affected permitted risk is explicitly accepted | ALLOW_WITH_EXCEPTION |
| VALID | NON_COMPLIANT with absent or insufficient risk acceptance | BLOCK |
| VALID | UNKNOWN | BLOCK unless an exact, explicitly permitted control exception and sufficient known-risk decisions apply |
| INVALID, ERROR or MISSING | UNKNOWN | BLOCK unless policy permits a control exception covering the missing assurance and all known violations have sufficient dispositions |
| UNTRUSTED | Any | BLOCK and obtain trustworthy evidence |
| Any | Mandatory non-waivable requirement failed, exception invalid, or approval insufficient | BLOCK |
| NOT_REQUIRED | Authorised non-applicability | ALLOW for this control and record the reason |

Require all mandatory contexts and tiers. A partial result or process exit
code cannot authorise promotion. A missing, unverifiable or mismatched gate
decision blocks promotion. RA authorises the exact candidate after all required
controls are satisfied. Keep policy evaluation and release authority distinct.

| Disposition | Authority and evidence |
| --- | --- |
| Vulnerability risk acceptance | RO records risk, scope, rationale, expiry and compensating controls, within SG policy. Retain original finding and validity. |
| Control exception | SG approves the exact missing control or evidence, reason, compensating tests, conditions and expiry. RO separately accepts resulting risk. Preserve original status. |
| False positive | DCO records technical evidence and rationale for the original finding, with independent review where policy requires. Preserve raw report. |

Review all applicable dispositions for exact scope, mandate, required coverage,
expiry and conditions at the release boundary. A disposition cannot broaden
the original approval.

## Remediation and operating assurance

DCO normalises and deduplicates both complete and partial findings, preserves
raw evidence, and assigns triage, remediation and retest. AO provides priorities
and remediation capacity. DEV fixes on an identified revision. DCO verifies
retest evidence against the original scenario and coverage. A finding
disappearing with diminished coverage is not closure. Refer confirmed findings
to the registered vulnerability remediation workflow.

| Indicator group | Owner and evaluation |
| --- | --- |
| Platform availability, update and provenance | DPO monitors inventory, digests, runtime add-ons, capacity, upgrades and rollback. |
| Execution reliability and cleanup | DO tracks provisioning, successful execution, leftover resources and revocation. |
| Required completion, validity, scenario coverage and detection | DCO tracks by application, tier and context. Include missing runs in the denominator. Monitor session degradation and requalification. |
| Findings and remediation | DCO monitors triage quality and retest. AO monitors remediation SLA. |
| Exception validity | SG monitors expiry, scope and overdue disposition. |
| Enforcement failures | RPO monitors evidence verification failures and attempted bypass. |

Review on schedule and after changes to application APIs or routing,
authentication or session design, topology or gateway, scanner image or
add-ons, profile or scope, policy or runner permissions. DCO coordinates
coverage and detection changes, SA architecture and fidelity changes, and RPO
release enforcement changes. Determine exactly which qualifications and prior
evidence cease to apply. Return affected scope to implementation or
qualification with any required independent review. Preserve valid unaffected
evidence. DPO manages qualified upgrades and rollback. Digest pinning is
compatible with a planned update process and does not identify runtime
add-ons that can change independently.

### Example and completion

For a stack using OAuth2 and mTLS, record gateway and internal contexts
separately. Qualify exact required identities and scope through AppSec-supplied
observations, and design network and identity isolation through SOL, SA, IAM
and INF. DEV addresses evidenced testability gaps. DO assembles deployment,
evidence intake and cleanup. QA, DCO and RPO submit separate qualifications.
ISR reviews the resulting evidence before SAA decides. Route an unsupported
scenario to a complementary method or authorised exception.

Before takeover confirm the mandate, owners and approval rights, source-derived
inventory, requirements and traceability, reviewed topology and feasibility,
implemented workstreams, approved profile and pinned platform, positive and
negative qualification, identity and isolation evidence, protected and bound
release gate, remediation and exception process, independent review and
formal acceptance. Confirm operational ownership, runbooks, retention,
monitoring, support and requalification triggers. Record deviations as
separate decisions alongside the actual evidence and status.

### Technical references

- [ZAP Docker documentation](https://www.zaproxy.org/docs/docker/about/) and [Automation Framework reference](https://www.zaproxy.org/docs/automate/automation-framework/)
- [Docker Compose networking](https://docs.docker.com/compose/how-tos/networking/) and [Kubernetes Pods](https://kubernetes.io/docs/concepts/workloads/pods/)
- [OWASP Web Security Testing Guide](https://owasp.org/projects/web-security-testing-guide) and [NIST Secure Software Development Framework](https://csrc.nist.gov/pubs/sp/800/218/final)
