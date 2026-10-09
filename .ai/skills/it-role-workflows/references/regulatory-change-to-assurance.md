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
| 1 | **Compliance Officer (Technology)** | records authoritative regulatory change source, effective dates and scope hypotheses | regulatory change record | Regulatory change record | Source, jurisdiction, dates and version are attributable |
| 2 | **Compliance Officer (Technology)** | determines technology applicability with legal/business input where needed | applicability decision | Applicability decision | In/out-of-scope rationale and authority are explicit |
| 3 | **GRC Analyst** | decomposes applicable obligations into traceable obligation records | obligations register | Obligations register | Each obligation retains source citation/context and applicability owner |
| 4 | **Business Analyst** | translates obligations into atomic/testable business/technology requirements | requirements baseline | Requirements baseline | Requirements preserve obligation intent and are testable |
| 5 | **Control Owner** | maps requirements to existing/new controls and identifies gaps | control mapping and gap register | Control mapping | Every requirement maps to effective control evidence or an owned gap |
| 6 | **Enterprise Architect** | assesses architecture/process/data/service impact and target-state changes | architecture impact assessment | Architecture impact assessment | Cross-domain impacts and affected governed models are explicit |
| 7 | **Portfolio Manager** | prioritises/funds time-bound remediation according to effective dates and risk | remediation roadmap | Remediation roadmap | Mandatory deadlines and dependencies are funded/owned or escalated |
| 8 | **Control Owner** | coordinates implementation evidence and control operating proof | evidence pack | Evidence pack | Evidence is attributable to implemented control version and period |
| 9 | **Internal IT Auditor** | independently tests design/operating evidence against obligation/control criteria | assurance report | Assurance report | Assurance is independent and reports exceptions/limitations |
| 10 | **Compliance Officer (Technology)** | authorises or routes closure based on assurance and residual exceptions | closure decision | Closure decision | Closure states remaining exceptions, authority and future review triggers |

## Control semantics

- A gate is blocking unless a named authority with the required decision right records an explicit waiver, rationale, expiry/review date and residual risk.
- A handoff is not complete because a document exists; the receiving role must be able to verify the acceptance condition from attributable evidence.
- Producer, approver and independent assurance responsibilities remain separated where the decision is consequential.
- Workflow order may branch or loop, but skipped steps and their unmet gates remain visible.
- Material claims/decisions use stable IDs and trace to evidence so Behavioral Quality evaluation can measure coverage and unsupported claims.
