# Engineering and security references

Owner: JAI maintainers · Last reviewed: 2026-10-20

Library v2.2.0 adds 39 English synthetic examples across 13 families to the
96 established references. Each family has `simple`, `medium` and `complex`
documents. Existing proposal references and production commands remain
unchanged. These examples are authoring inputs, not a second semantic record,
security assessment, release approval or record of executed tests.

## Choose a family and audience

Select the deliverable first, then complexity, professional domain, intended
reader and explicit project context. Complexity reflects dependencies, trust
boundaries and delivery risk rather than a target page count.

| Domain | Families | Typical intended readers |
| --- | --- | --- |
| Engineering and delivery | `software-engineering-plan`, `api-interface-contract`, `release-readiness-review` | Engineers, interface owners, test leads, receiving operations and change authority |
| Transformation | `transformation-baseline-assessment`, `target-operating-model`, `transformation-execution-plan` | Sponsors, process owners, architects, delivery and adoption leads |
| Security assessment | `security-architecture-assessment`, `threat-model`, `security-control-assessment` | Security architects, control owners and independent assessors |
| DevSecOps and AppSec | `devsecops-pipeline-design`, `cicd-pipeline-assurance`, `appsec-verification-report`, `software-supply-chain-assessment` | Platform engineers, AppSec reviewers, release and supply-chain assurance owners |

From the source checkout, inspect and resolve the shared reference library:

```bash
python3 .ai/runtime/tools/expert_references.py list --root .
python3 .ai/runtime/tools/expert_references.py resolve --root . \
  --kind api-interface-contract --complexity medium --audience interface-owner
python3 .ai/runtime/tools/expert_references.py inspect --root . \
  --kind threat-model --complexity complex --audience security-review
```

Use `--context ./reference-context.json` for explicit flat scalar business
qualifiers. Constrained overrides can specify `target_audiences` and
`applicability_context`; bundled examples are unconstrained defaults.
The resolver does not infer domain fitness, security authority or customer
facts from an audience label. Existing agents and workflows use the same
resolver and registered kinds, with no extra reference engine.

## DCS and existing role contracts

The [mapping table](../reference/expert-reference-format.md#registered-family-mappings)
records each family and its registered kind. New standalone specializations
are proposed and advisory. Source `dcs-proposed-*` anchors remain unchanged;
their explicit mapping identifies information units without approving them.
No new family automatically reclassifies an existing role deliverable or
activates normative production enforcement.

Create an unfilled blueprint through the existing shared authoring command:

```bash
python3 .ai/runtime/tools/content_spec.py outline --root . \
  --artifact-id kind/api-interface-contract --reference-complexity medium \
  --reference-audience interface-owner
```

An explicit `kind/` selector grants no role authority. For an existing role
deliverable, use its actual registered artifact ID and retain its binding,
security restrictions and receiving contract. Reference structure covers
kind-owned units; inherited obligations still apply. Publication continues
through existing semantic QA, independent review and projection controls.
See [working with deliverables](deliverables.md).

Overrides retain `engagement > organisation > user > bundled` precedence.
An invalid selected override is an error, without silent fallback; missing
higher levels continue normally. See [paths, installation and restoration](../configuration/expert-document-overrides.md).
Overrides cannot change DCS obligations or human approval authority.

## Synthetic casebook

The new examples share three fictional cases with earlier references.
Every numerical value below is an illustrative design target, not an observed
customer baseline or achieved result.

| Case | Modelled context | Invariant and illustrative targets | Failure to challenge |
| --- | --- | --- | --- |
| `HFS-FAR` | Field appointment reliability; 2,100 weekly appointments and 240 technicians | Reconcile dispatch and booking IDs to the authoritative SaaS record; 99.5% monthly availability, p95 acknowledgement below 2 seconds, RTO 8 hours, RPO 24 hours | Duplicate scheduling after webhook replay |
| `MRG-OEI` | Order/ERP integration; 180,000 peak daily orders across twelve markets | Each accepted order has one explainable final ERP state; 99.9% monthly availability, p95 visibility below 5 minutes, RTO 2 hours, RPO 15 minutes | Country-routing errors or privileged event replay |
| `OPG-RSM` | Settlement modernisation; 2.4 million synthetic daily instructions across fourteen jurisdictions | Immutable instruction lineage and zero unexplained unmatched finality amounts; 99.95% critical-processing availability, p95 acknowledgement below 450 ms excluding external network, RTO 30 minutes, RPO 5 minutes | Privileged policy changes enabling unauthorised jurisdiction routing |

The conceptual chain `CASE-REQ → CASE-ARCH → CASE-SEC → CASE-BUILD →
CASE-TEST → CASE-OPS` is illustrative. Before producing real work, resolve
every required node to an authoritative project record or mark it absent.
Do not create apparent evidence by copying the example identifiers.

## Methods and acceptance questions

- Engineering: define business keys, state transitions, tenancy and
  authorization, interface versions, errors, idempotency and reconciliation.
- CI/CD: distinguish reviewed source, isolated builder identity, materials,
  immutable artifact digest, provenance and deployed-digest verification.
- AppSec: establish scope and consent; derive tests from threats; distinguish
  SAST, SCA, secret scanning, authorization negatives, triage, fixes and retests.
- Security assessment: define criteria and population before sampling;
  distinguish design from operating effectiveness, exceptions and retesting.
  Missing evidence can prevent any conclusion about effectiveness.
- Transformation: verify the current baseline, transition dependencies,
  cutover rehearsal, rollback or compensation, ownership and adoption measures.

Methodological pointers are [NIST SSDF SP 800-218 v1.1](https://csrc.nist.gov/pubs/sp/800/218/final),
[OWASP ASVS 5.0](https://github.com/OWASP/ASVS/tree/master/5.0/en),
[SLSA 1.2](https://slsa.dev/spec/v1.2/) and
[NIST SP 800-53A Rev. 5](https://csrc.nist.gov/pubs/sp/800/53/a/r5/final).
These pointers require no download during qualification. Using an example
does not establish statutory applicability, certification, an ASVS level,
SLSA attainment or an approved risk appetite.

## Evidence and qualification boundaries

Planned tests remain `NOT_EXECUTED`; unresolved decisions remain `OPEN`.
A generated threat scenario is not evidence of exploitation or a verified
vulnerability. Synthetic targets are not measured performance; control
matrices are not achieved compliance. Neither a passing structural check
nor a proposed release review grants JAI L0 authority.

Run local structural and integrity validation with:

```bash
python3 .ai/runtime/tools/expert_references.py validate --root . --all
```

Mandatory [offline qualification](../validation/offline-content-qualification.md)
uses fixtures and mocks, without live LLMs. Obtain optional competent feedback
using the [engineering and security review rubric](../validation/engineering-security-review.md).
