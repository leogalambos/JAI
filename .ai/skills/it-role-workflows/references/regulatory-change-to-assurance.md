# Regulatory change to assurance

**Trigger.** A new or changed law, regulation, supervisory expectation or contractual compliance obligation may affect IS/IT services, controls or architecture.

**Outcome.** Applicability and obligations are translated into traceable requirements/controls, architecture and remediation changes are implemented, evidence is independently assured, and closure is authorised.

## Mandatory artefacts

- Regulatory change record
- Applicability decision
- Obligations register
- Requirements baseline
- Control mapping
- Architecture impact assessment
- Remediation roadmap
- Evidence pack
- Assurance report
- Closure decision

## Chain

| Step | Accountable role | Does | Hands over | Mandatory artefact | Gate |
| ---: | --- | --- | --- | --- | --- |
| 1 | [Compliance Officer (Technology)](../../it-roles-governance-risk-compliance-audit-and-privacy/references/compliance-officer-technology.md) | records authoritative regulatory change source, effective dates and scope hypotheses | regulatory change record | Source, jurisdiction, dates and version are attributable |
| 2 | [Compliance Officer (Technology)](../../it-roles-governance-risk-compliance-audit-and-privacy/references/compliance-officer-technology.md) | determines technology applicability with legal/business input where needed | applicability decision | In/out-of-scope rationale and authority are explicit |
| 3 | [GRC Analyst](../../it-roles-governance-risk-compliance-audit-and-privacy/references/grc-analyst.md) | decomposes applicable obligations into traceable obligation records | obligations register | Each obligation retains source citation/context and applicability owner |
| 4 | [Business Analyst](../../it-roles-analysis/references/business-analyst.md) | translates obligations into atomic/testable business/technology requirements | requirements baseline | Requirements preserve obligation intent and are testable |
| 5 | [Control Owner](../../it-roles-governance-risk-compliance-audit-and-privacy/references/control-owner.md) | maps requirements to existing/new controls and identifies gaps | control mapping and gap register | Every requirement maps to effective control evidence or an owned gap |
| 6 | [Enterprise Architect](../../it-roles-architecture/references/enterprise-architect.md) | assesses architecture/process/data/service impact and target-state changes | architecture impact assessment | Cross-domain impacts and affected governed models are explicit |
| 7 | [Portfolio Manager](../../it-roles-product-delivery-and-agile/references/portfolio-manager.md) | prioritises/funds time-bound remediation according to effective dates and risk | remediation roadmap | Mandatory deadlines and dependencies are funded/owned or escalated |
| 8 | [Control Owner](../../it-roles-governance-risk-compliance-audit-and-privacy/references/control-owner.md) | coordinates implementation evidence and control operating proof | evidence pack | Evidence is attributable to implemented control version and period |
| 9 | [Internal IT Auditor](../../it-roles-governance-risk-compliance-audit-and-privacy/references/internal-it-auditor.md) | independently tests design/operating evidence against obligation/control criteria | assurance report | Assurance is independent and reports exceptions/limitations |
| 10 | [Compliance Officer (Technology)](../../it-roles-governance-risk-compliance-audit-and-privacy/references/compliance-officer-technology.md) | authorises or routes closure based on assurance and residual exceptions | closure decision | Closure states remaining exceptions, authority and future review triggers |

## Control semantics

- A gate is blocking unless a named authority with the required decision right records an explicit waiver, rationale, expiry/review date and residual risk.
- A handoff is not complete because a document exists; the receiving role must be able to verify the acceptance condition from attributable evidence.
- Producer, approver and independent assurance responsibilities remain separated where the decision is consequential.
- Workflow order may branch or loop, but skipped steps and their unmet gates remain visible.
- Material claims/decisions use stable IDs and trace to evidence so Behavioral Quality evaluation can measure coverage and unsupported claims.

<!-- BEGIN workflow-applicability -->
## Context and mechanism applicability

Use the actual bounded request, current environment and decision rights to select one applicable mechanism variant. Unknown applicability remains pending; the routing record grants no authority.

**Invariant outcomes:**

- Applicability and obligations are translated into traceable requirements/controls, architecture and remediation changes are implemented, evidence is independently assured, and closure is authorised.
- Retain source-version traceability, accountable receiving duties and every applicable existing gate.

| Context | Mechanisms | Required evidence |
| --- | --- | --- |
| applicable | Trace obligations to testable requirements, implemented controls and independent assurance | Source-context mapping, actual control evidence and exceptions |
| not-applicable | Record a competent bounded exclusion with its source/context rationale | Actual applicability decision and change/review trigger |

Return ambiguous interpretation to the competent obligation owner and ineffective controls to control/design owners. Stop unsupported compliance claims or closure with unresolved mandatory obligations and absent authorised disposition. Close only the assessed scope with explicit exceptions, actual authority and future review triggers. Mechanism selection is not a waiver of security, legal or acceptance obligations.

**Entry information (selected once per actual context version):**

- Attributable source/version/jurisdiction and dates
- Competent applicability authority
- Affected services, controls and obligation owners

Select intake and mechanism variant once per actual context version. Carry the reviewed record by versioned evidence reference. Reuse unchanged evidence; recheck mutable prerequisites only at the action they govern. A new context version requires its own relevant review, not reconstruction of historical work.

**Continuation, rework, stop and exit:**

- **continue** — The current handoff criteria and applicable prerequisites are satisfied. Continue to the registered receiving duty with exact output and evidence references.
- **rework** — A current criterion fails or required information changes. Return ambiguous interpretation to the competent obligation owner and ineffective controls to control/design owners.
- **stop** — An applicable authority, legal, safety or mandatory-control boundary forbids the effect. Stop unsupported compliance claims or closure with unresolved mandatory obligations and absent authorised disposition.
- **exit** — The bounded outcome is accepted or the entitled owner rejects, cancels or defers the scope. Close only the assessed scope with explicit exceptions, actual authority and future review triggers.

**Bounded paths and scope:**

Verified non-applicability closes at step2 under exact authority; it cannot require fabricated control implementation or compliance evidence.

| Selected path | Applicable stages | Terminal stage |
| --- | --- | ---: |
| applicable | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 | 10 |
| not-applicable | 1, 2 | 2 |

A path with a separate mechanism requires that explicit mechanism selection in the versioned intake record. Unknown selection remains pending. Later out-of-scope stages cannot claim acceptance; a terminal exit still needs the registered exact-scope authority.

**Context guards:**

- **not-applicable** requires evidence that the statement "a regulatory requirement applies" is false; unknown applicability remains pending.
<!-- END workflow-applicability -->
