# Source to contract to service

**Trigger.** A capability may be sourced externally and must move from requirement/RFI/RFP through supplier selection and contract controls to implementation and accepted service.

**Outcome.** The selected supplier/service has evidence-backed fit, enforceable contract obligations, approved implementation and operational acceptance, with ongoing vendor governance.

## Mandatory artefacts

- Sourcing requirement baseline
- RFI/RFP pack
- Supplier assessment
- Security/privacy assessment
- Architecture-fit decision
- Selection decision
- Contract control schedule
- Implementation plan
- Service acceptance
- Vendor governance baseline

## Chain

| Step | Accountable role | Does | Hands over | Mandatory artefact | Gate |
| ---: | --- | --- | --- | --- | --- |
| 1 | **Business Analyst** | turns business/service need into outcome, requirement and acceptance baseline | sourcing requirement baseline | Sourcing requirement baseline | Requirements are testable and distinguish need from preferred solution |
| 2 | **IT Procurement Specialist** | creates and runs RFI/RFP process with comparable response structure | RFI/RFP pack and response evidence | RFI/RFP pack | Supplier responses are comparable and procurement rules are followed |
| 3 | **Vendor Manager** | assesses supplier capability, viability, support and governance fit | supplier assessment | Supplier assessment | Material supplier assumptions and dependency risks are evidenced |
| 4 | **Third-Party Risk Manager** | coordinates security/privacy/resilience risk assessment with specialist authorities | security/privacy/supplier risk assessment | Security/privacy assessment | Critical risks/obligations are resolved, mitigated or accepted by correct authority |
| 5 | **Enterprise Applications Architect** | assesses architecture/capability/integration fit and lock-in/exit implications | architecture-fit decision | Architecture-fit decision | Selection does not create hidden target-state or integration contradictions |
| 6 | **IT Procurement Specialist** | runs weighted selection and records rationale/conflicts | selection decision | Selection decision | Decision is traceable to declared criteria, evidence and authority |
| 7 | **Contract Manager** | translates agreed service/security/privacy/resilience/exit controls into enforceable clauses/schedules | contract control schedule | Contract control schedule | Every mandatory control has enforceable wording, evidence/measurement and remedy/exit path |
| 8 | **Implementation Consultant** | coordinates implementation against contract/design acceptance criteria | implementation plan and evidence | Implementation plan | Implementation deviations are approved, not silently normalised |
| 9 | **Service Transition and Operational Readiness Manager** | validates support, monitoring, CMDB, DR, security, ownership and service acceptance | service acceptance | Service acceptance | No production acceptance with missing critical operational ownership/evidence |
| 10 | **Vendor Manager** | establishes ongoing performance, risk, improvement, renewal and exit governance | vendor governance baseline | Vendor governance baseline | Contractual obligations map to measured service/vendor governance |

## Control semantics

- A gate is blocking unless a named authority with the required decision right records an explicit waiver, rationale, expiry/review date and residual risk.
- A handoff is not complete because a document exists; the receiving role must be able to verify the acceptance condition from attributable evidence.
- Producer, approver and independent assurance responsibilities remain separated where the decision is consequential.
- Workflow order may branch or loop, but skipped steps and their unmet gates remain visible.
- Material claims/decisions use stable IDs and trace to evidence so Behavioral Quality evaluation can measure coverage and unsupported claims.
