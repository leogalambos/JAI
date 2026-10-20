# Engineering and security professional review

Owner: JAI maintainers · Last reviewed: 2026-10-20

This optional rubric supports competent peer evaluation of technical and
enterprise outputs. It does not certify the bundled synthetic examples,
replace independent specialist review or grant JAI L0 approval. The existing
[proposal pilot](proposal-pilot.md) remains unchanged.

## Record scope and evidence

In an authorized private record, identify the evaluated output revision,
case, kind, complexity, intended audience, reviewer role and evidence IDs
actually inspected. Record missing inputs and limits of the review.
Public summaries must omit customer names, private paths, confidential
excerpts and identifying fingerprints. Use existing JAI review and authority
records rather than creating another approval mechanism.

Score each criterion from **0 to 4**: **0** missing or false, **1** major gaps,
**2** partial, **3** adequate, **4** professionally strong. Give exact locations,
evidence and proposed corrections; an average alone is insufficient.

| Criterion | Reviewer challenge |
| --- | --- |
| Business intent and boundaries | Is the service outcome attributable, measurable and scoped? |
| Architecture and engineering mechanics | Are state, interfaces, error handling and recovery explained? |
| Traceability and ownership | Do significant decisions link to evidence and competent receiving authority? |
| Risk and threat specificity | Do scenarios identify assets, trust boundaries and business impact? |
| Security assessment method | Are criteria, populations, independence and non-executed tests explicit? |
| CI/CD and supply chain | Are source, builder, materials, artifact digest, signature and deployment identity distinct? |
| AppSec verification | Are tests threat-derived, authorization negatives included, severity and retest defensible? |
| Transformation feasibility | Are dependencies, migration states, adoption and irreversibility addressed? |
| Operating readiness | Could a named receiving team monitor, recover and support the service? |
| Professional presentation | Do concise diagrams and tables clarify the specific decision? |
| Evidence honesty | Are fictional values, planned tests and absent observations unmistakable? |

## Critical blockers and disposition

A critical unsupported security claim, invented release approval or failure
of a material data-integrity invariant blocks a positive disposition,
regardless of aggregate score. Do not average away reviewer disagreement.
Record a responsible owner, correction and required re-evaluation.

Suggested review samples are medium `software-engineering-plan`, complex
`transformation-execution-plan`, medium `security-architecture-assessment`,
complex `threat-model`, medium `devsecops-pipeline-design`, complex
`cicd-pipeline-assurance`, complex `appsec-verification-report` and complex
`software-supply-chain-assessment`. Two independent competent reviewers per
key output are desirable; adjudicate disagreements with the existing
accountable authority.

For each output retain criterion scores, critical blockers, detailed comments,
revised recommendations and its actual proposed, reviewed or approved status
in the existing JAI model. A reviewer recommendation is separate from an
authority act. Never record approved status without the corresponding act.

Challenge at least one negative case: present an unexecuted security test as
PASS, substitute a different deployed digest, omit an interface invariant or
claim a recovery target without a timed drill. Record whether automatic
checks detect it and whether specialist review is still required. The
deterministic validator does not prove arbitrary prose or expert correctness.

See the [reference casebook and selection guide](../using/engineering-security-references.md),
[DCS mappings](../reference/expert-reference-format.md#registered-family-mappings)
and [qualification states](offline-content-qualification.md#what-a-passing-result-establishes).
