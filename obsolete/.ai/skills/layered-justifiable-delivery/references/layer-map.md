# Roles by layer

Which roles each layer agent draws on, and which agent operates each role. `layer_operator` is never wider than the narrower of the role's own tool tier and the layer agent's: where a role is narrower than its layer agent, a narrower agent operates it.

## Layer 1 — Intent and Context (15 roles)

Layer agent `l1-intent` · tier `route` · workload class `heavy`

| Role | Role tier | Operated by |
| --- | --- | --- |
| [Business Relationship Manager](../../it-roles-service-management-and-support/references/business-relationship-manager.md) | `author` | `l1-intent` |
| [Business Security Architect (SABSA Contextual Layer)](../../it-roles-sabsa-security-architecture/references/business-security-architect-sabsa-contextual-layer.md) | `author` | `l1-intent` |
| [Chief Data Officer](../../it-roles-executive-and-leadership/references/chief-data-officer.md) | `advise` | `l1-intent` |
| [Chief Digital Officer](../../it-roles-executive-and-leadership/references/chief-digital-officer.md) | `advise` | `l1-intent` |
| [Chief Information Officer](../../it-roles-executive-and-leadership/references/chief-information-officer.md) | `advise` | `l1-intent` |
| [Chief Product Officer](../../it-roles-executive-and-leadership/references/chief-product-officer.md) | `advise` | `l1-intent` |
| [Chief Security Architect (SABSA Practice Lead)](../../it-roles-sabsa-security-architecture/references/chief-security-architect-sabsa-practice-lead.md) | `author` | `l1-intent` |
| [Chief Technology Officer](../../it-roles-executive-and-leadership/references/chief-technology-officer.md) | `advise` | `l1-intent` |
| [Epic Owner](../../it-roles-product-delivery-and-agile/references/epic-owner.md) | `author` | `l1-intent` |
| [IT Service Owner](../../it-roles-executive-and-leadership/references/it-service-owner.md) | `author` | `l1-intent` |
| [Portfolio Manager](../../it-roles-product-delivery-and-agile/references/portfolio-manager.md) | `advise` | `l1-intent` |
| [Product Manager](../../it-roles-product-delivery-and-agile/references/product-manager.md) | `author` | `l1-intent` |
| [Product Owner](../../it-roles-product-delivery-and-agile/references/product-owner.md) | `author` | `l1-intent` |
| [Programme Manager](../../it-roles-product-delivery-and-agile/references/programme-manager.md) | `author` | `l1-intent` |
| [VP of Engineering](../../it-roles-executive-and-leadership/references/vp-of-engineering.md) | `advise` | `l1-intent` |

## Layer 2 — Meaning and Domain Model (34 roles)

Layer agent `l2-meaning` · tier `advise` · workload class `standard`

| Role | Role tier | Operated by |
| --- | --- | --- |
| [Binary Reverse Engineer](../../it-roles-offensive-security-and-adversarial-testing/references/binary-reverse-engineer.md) | `advise` | `l2-meaning` |
| [Business Analyst](../../it-roles-analysis/references/business-analyst.md) | `author` | `l2-meaning` |
| [Business Architect](../../it-roles-architecture/references/business-architect.md) | `author` | `l2-meaning` |
| [Business Attribute Profiler](../../it-roles-sabsa-security-architecture/references/business-attribute-profiler.md) | `author` | `l2-meaning` |
| [Business Intelligence Analyst](../../it-roles-analysis/references/business-intelligence-analyst.md) | `author` | `l2-meaning` |
| [Capacity Manager](../../it-roles-infrastructure-cloud-and-operations/references/capacity-manager.md) | `author` | `l2-meaning` |
| [Configuration Analyst](../../it-roles-analysis/references/configuration-analyst.md) | `author` | `l2-meaning` |
| [Content Designer](../../it-roles-design-and-user-experience/references/content-designer.md) | `author` | `l2-meaning` |
| [Data Analyst](../../it-roles-analysis/references/data-analyst.md) | `author` | `l2-meaning` |
| [Data Modeller](../../it-roles-data-analytics-and-ai/references/data-modeller.md) | `author` | `l2-meaning` |
| [Data Scientist](../../it-roles-data-analytics-and-ai/references/data-scientist.md) | `execute` | `l2-meaning` |
| [Data Steward](../../it-roles-data-analytics-and-ai/references/data-steward.md) | `author` | `l2-meaning` |
| [Enterprise Business Analyst](../../it-roles-analysis/references/enterprise-business-analyst.md) | `author` | `l2-meaning` |
| [Exploit Developer](../../it-roles-offensive-security-and-adversarial-testing/references/exploit-developer.md) | `advise` | `l2-meaning` |
| [FinOps Analyst](../../it-roles-analysis/references/finops-analyst.md) | `author` | `l2-meaning` |
| [Hardware and IoT Security Researcher](../../it-roles-offensive-security-and-adversarial-testing/references/hardware-and-iot-security-researcher.md) | `advise` | `l2-meaning` |
| [Information Architect](../../it-roles-design-and-user-experience/references/information-architect.md) | `author` | `l2-meaning` |
| [Metadata Manager](../../it-roles-data-analytics-and-ai/references/metadata-manager.md) | `author` | `l2-meaning` |
| [Open Source Intelligence Investigator](../../it-roles-offensive-security-and-adversarial-testing/references/open-source-intelligence-investigator.md) | `advise` | `l2-meaning` |
| [PMO Analyst](../../it-roles-product-delivery-and-agile/references/pmo-analyst.md) | `author` | `l2-meaning` |
| [Privacy Analyst](../../it-roles-governance-risk-compliance-audit-and-privacy/references/privacy-analyst.md) | `advise` | `l2-meaning` |
| [Problem Manager](../../it-roles-service-management-and-support/references/problem-manager.md) | `author` | `l2-meaning` |
| [Process Analyst](../../it-roles-analysis/references/process-analyst.md) | `author` | `l2-meaning` |
| [Product Analyst](../../it-roles-analysis/references/product-analyst.md) | `author` | `l2-meaning` |
| [Quantum Computing Engineer](../../it-roles-research-innovation-and-specialist-engineering/references/quantum-computing-engineer.md) | `execute` | `l2-meaning` |
| [Requirements Engineer](../../it-roles-analysis/references/requirements-engineer.md) | `author` | `l2-meaning` |
| [Research Engineer](../../it-roles-research-innovation-and-specialist-engineering/references/research-engineer.md) | `execute` | `l2-meaning` |
| [Research Scientist](../../it-roles-data-analytics-and-ai/references/research-scientist.md) | `execute` | `l2-meaning` |
| [Sustainable IT Engineer](../../it-roles-infrastructure-cloud-and-operations/references/sustainable-it-engineer.md) | `author` | `l2-meaning` |
| [Systems Analyst](../../it-roles-analysis/references/systems-analyst.md) | `author` | `l2-meaning` |
| [Technology Scout](../../it-roles-research-innovation-and-specialist-engineering/references/technology-scout.md) | `author` | `l2-meaning` |
| [Threat Intelligence Analyst](../../it-roles-security-operations-and-defensive-security/references/threat-intelligence-analyst.md) | `author` | `l2-meaning` |
| [UX Researcher](../../it-roles-design-and-user-experience/references/ux-researcher.md) | `author` | `l2-meaning` |
| [Vulnerability Researcher](../../it-roles-offensive-security-and-adversarial-testing/references/vulnerability-researcher.md) | `advise` | `l2-meaning` |

## Layer 3 — Reasoning, Policy and Control (57 roles)

Layer agent `l3-policy` · tier `advise` · workload class `heavy`

| Role | Role tier | Operated by |
| --- | --- | --- |
| [AI Governance Officer](../../it-roles-data-analytics-and-ai/references/ai-governance-officer.md) | `advise` | `l3-policy` |
| [Accessibility Specialist](../../it-roles-design-and-user-experience/references/accessibility-specialist.md) | `advise` | `l3-policy` |
| [Availability Manager](../../it-roles-infrastructure-cloud-and-operations/references/availability-manager.md) | `author` | `l3-policy` |
| [Bug Bounty Programme Manager](../../it-roles-offensive-security-and-adversarial-testing/references/bug-bounty-programme-manager.md) | `advise` | `l3-policy` |
| [Business Continuity Manager](../../it-roles-governance-risk-compliance-audit-and-privacy/references/business-continuity-manager.md) | `advise` | `l3-policy` |
| [Change Manager](../../it-roles-service-management-and-support/references/change-manager.md) | `advise` | `l3-policy` |
| [Chief AI Officer](../../it-roles-executive-and-leadership/references/chief-ai-officer.md) | `advise` | `l3-policy` |
| [Chief Information Security Officer](../../it-roles-executive-and-leadership/references/chief-information-security-officer.md) | `advise` | `l3-policy` |
| [Compliance Officer (Technology)](../../it-roles-governance-risk-compliance-audit-and-privacy/references/compliance-officer-technology.md) | `advise` | `l3-policy` |
| [Conceptual Security Architect (SABSA Architect's View)](../../it-roles-sabsa-security-architecture/references/conceptual-security-architect-sabsa-architect-s-view.md) | `author` | `l3-policy` |
| [Configuration Manager](../../it-roles-service-management-and-support/references/configuration-manager.md) | `author` | `l3-policy` |
| [Continual Improvement Manager](../../it-roles-service-management-and-support/references/continual-improvement-manager.md) | `author` | `l3-policy` |
| [Contract Manager](../../it-roles-commercial-sourcing-and-enablement/references/contract-manager.md) | `author` | `l3-policy` |
| [Control Owner](../../it-roles-governance-risk-compliance-audit-and-privacy/references/control-owner.md) | `author` | `l3-policy` |
| [Data Governance Lead](../../it-roles-data-analytics-and-ai/references/data-governance-lead.md) | `advise` | `l3-policy` |
| [Data Owner](../../it-roles-data-analytics-and-ai/references/data-owner.md) | `advise` | `l3-policy` |
| [Data Protection Officer](../../it-roles-governance-risk-compliance-audit-and-privacy/references/data-protection-officer.md) | `advise` | `l3-policy` |
| [Delivery Manager](../../it-roles-product-delivery-and-agile/references/delivery-manager.md) | `author` | `l3-policy` |
| [Engineering Manager](../../it-roles-product-delivery-and-agile/references/engineering-manager.md) | `author` | `l3-policy` |
| [Ethics and Responsible Technology Lead](../../it-roles-research-innovation-and-specialist-engineering/references/ethics-and-responsible-technology-lead.md) | `advise` | `l3-policy` |
| [GRC Analyst](../../it-roles-governance-risk-compliance-audit-and-privacy/references/grc-analyst.md) | `advise` | `l3-policy` |
| [Head of Platform](../../it-roles-executive-and-leadership/references/head-of-platform.md) | `author` | `l3-policy` |
| [IT Asset Manager](../../it-roles-service-management-and-support/references/it-asset-manager.md) | `author` | `l3-policy` |
| [IT Chief of Staff](../../it-roles-executive-and-leadership/references/it-chief-of-staff.md) | `author` | `l3-policy` |
| [IT Governance Manager](../../it-roles-governance-risk-compliance-audit-and-privacy/references/it-governance-manager.md) | `advise` | `l3-policy` |
| [IT Procurement Specialist](../../it-roles-commercial-sourcing-and-enablement/references/it-procurement-specialist.md) | `author` | `l3-policy` |
| [IT Risk Manager](../../it-roles-governance-risk-compliance-audit-and-privacy/references/it-risk-manager.md) | `advise` | `l3-policy` |
| [Identity Governance Specialist](../../it-roles-security-operations-and-defensive-security/references/identity-governance-specialist.md) | `advise` | `l3-policy` |
| [Information Security Officer (Local)](../../it-roles-governance-risk-compliance-audit-and-privacy/references/information-security-officer-local.md) | `advise` | `l3-policy` |
| [Innovation Lead](../../it-roles-research-innovation-and-specialist-engineering/references/innovation-lead.md) | `author` | `l3-policy` |
| [Knowledge Manager](../../it-roles-service-management-and-support/references/knowledge-manager.md) | `author` | `l3-policy` |
| [Master Data Management Specialist](../../it-roles-data-analytics-and-ai/references/master-data-management-specialist.md) | `author` | `l3-policy` |
| [Open Source Program Office Engineer](../../it-roles-software-development-and-engineering/references/open-source-program-office-engineer.md) | `author` | `l3-policy` |
| [PMO Lead](../../it-roles-product-delivery-and-agile/references/pmo-lead.md) | `author` | `l3-policy` |
| [Policy Author](../../it-roles-governance-risk-compliance-audit-and-privacy/references/policy-author.md) | `advise` | `l3-policy` |
| [Project Manager](../../it-roles-product-delivery-and-agile/references/project-manager.md) | `author` | `l3-policy` |
| [Records Manager](../../it-roles-governance-risk-compliance-audit-and-privacy/references/records-manager.md) | `advise` | `l3-policy` |
| [Red Team Lead](../../it-roles-offensive-security-and-adversarial-testing/references/red-team-lead.md) | `advise` | `l3-policy` |
| [Release Train Engineer](../../it-roles-product-delivery-and-agile/references/release-train-engineer.md) | `author` | `l3-policy` |
| [Request Fulfilment Manager](../../it-roles-service-management-and-support/references/request-fulfilment-manager.md) | `author` | `l3-policy` |
| [Resource Manager](../../it-roles-commercial-sourcing-and-enablement/references/resource-manager.md) | `author` | `l3-policy` |
| [SOC Manager](../../it-roles-security-operations-and-defensive-security/references/soc-manager.md) | `author` | `l3-policy` |
| [Scrum Master](../../it-roles-product-delivery-and-agile/references/scrum-master.md) | `author` | `l3-policy` |
| [Security Domain Authority](../../it-roles-sabsa-security-architecture/references/security-domain-authority.md) | `advise` | `l3-policy` |
| [Security Risk and Opportunity Architect](../../it-roles-sabsa-security-architecture/references/security-risk-and-opportunity-architect.md) | `advise` | `l3-policy` |
| [Service Catalogue Manager](../../it-roles-service-management-and-support/references/service-catalogue-manager.md) | `author` | `l3-policy` |
| [Service Level Manager](../../it-roles-service-management-and-support/references/service-level-manager.md) | `author` | `l3-policy` |
| [Software Asset Manager](../../it-roles-service-management-and-support/references/software-asset-manager.md) | `author` | `l3-policy` |
| [Software Licence Compliance Specialist](../../it-roles-commercial-sourcing-and-enablement/references/software-licence-compliance-specialist.md) | `advise` | `l3-policy` |
| [Technical Product Manager](../../it-roles-product-delivery-and-agile/references/technical-product-manager.md) | `author` | `l3-policy` |
| [Test Manager](../../it-roles-quality-and-testing/references/test-manager.md) | `author` | `l3-policy` |
| [Third-Party Risk Manager](../../it-roles-governance-risk-compliance-audit-and-privacy/references/third-party-risk-manager.md) | `advise` | `l3-policy` |
| [Transformation Manager](../../it-roles-product-delivery-and-agile/references/transformation-manager.md) | `author` | `l3-policy` |
| [User Acceptance Test Coordinator](../../it-roles-quality-and-testing/references/user-acceptance-test-coordinator.md) | `author` | `l3-policy` |
| [Vendor Manager](../../it-roles-commercial-sourcing-and-enablement/references/vendor-manager.md) | `author` | `l3-policy` |
| [Vulnerability Disclosure Coordinator](../../it-roles-offensive-security-and-adversarial-testing/references/vulnerability-disclosure-coordinator.md) | `advise` | `l3-policy` |
| [Vulnerability Management Analyst](../../it-roles-security-operations-and-defensive-security/references/vulnerability-management-analyst.md) | `author` | `l3-policy` |

## Layer 4 — Solution Design (23 roles)

Layer agent `l4-design` · tier `advise` · workload class `standard`

| Role | Role tier | Operated by |
| --- | --- | --- |
| [AI and ML Architect](../../it-roles-architecture/references/ai-and-ml-architect.md) | `author` | `l4-design` |
| [Application Architect](../../it-roles-architecture/references/application-architect.md) | `author` | `l4-design` |
| [Cloud Architect](../../it-roles-architecture/references/cloud-architect.md) | `author` | `l4-design` |
| [Data Architect](../../it-roles-architecture/references/data-architect.md) | `author` | `l4-design` |
| [Domain Architect](../../it-roles-architecture/references/domain-architect.md) | `author` | `l4-design` |
| [Enterprise Architect](../../it-roles-architecture/references/enterprise-architect.md) | `author` | `l4-design` |
| [Integration Architect](../../it-roles-architecture/references/integration-architect.md) | `author` | `l4-design` |
| [Interaction Designer](../../it-roles-design-and-user-experience/references/interaction-designer.md) | `author` | `l4-design` |
| [Logical Security Designer (SABSA Designer's View)](../../it-roles-sabsa-security-architecture/references/logical-security-designer-sabsa-designer-s-view.md) | `author` | `l4-design` |
| [Network Architect](../../it-roles-architecture/references/network-architect.md) | `author` | `l4-design` |
| [Product Designer](../../it-roles-design-and-user-experience/references/product-designer.md) | `author` | `l4-design` |
| [SABSA and TOGAF Integration Architect](../../it-roles-sabsa-security-architecture/references/sabsa-and-togaf-integration-architect.md) | `author` | `l4-design` |
| [SAFe System Architect](../../it-roles-product-delivery-and-agile/references/safe-system-architect.md) | `author` | `l4-design` |
| [Security Architect](../../it-roles-architecture/references/security-architect.md) | `author` | `l4-design` |
| [Service Designer](../../it-roles-design-and-user-experience/references/service-designer.md) | `author` | `l4-design` |
| [Solution Architect](../../it-roles-architecture/references/solution-architect.md) | `author` | `l4-design` |
| [Staff Engineer](../../it-roles-software-development-and-engineering/references/staff-engineer.md) | `author` | `l4-design` |
| [Systems Engineer (INCOSE)](../../it-roles-research-innovation-and-specialist-engineering/references/systems-engineer-incose.md) | `author` | `l4-design` |
| [Technical Design Authority Member](../../it-roles-architecture/references/technical-design-authority-member.md) | `author` | `l4-design` |
| [Technical Lead](../../it-roles-product-delivery-and-agile/references/technical-lead.md) | `author` | `l4-design` |
| [Test Architect](../../it-roles-quality-and-testing/references/test-architect.md) | `author` | `l4-design` |
| [UI Designer](../../it-roles-design-and-user-experience/references/ui-designer.md) | `author` | `l4-design` |
| [UX Designer](../../it-roles-design-and-user-experience/references/ux-designer.md) | `author` | `l4-design` |

## Layer 5 — Realisation and Tooling (66 roles)

Layer agent `l5-realisation` · tier `author` · workload class `heavy`

| Role | Role tier | Operated by |
| --- | --- | --- |
| [AI Solutions Engineer](../../it-roles-data-analytics-and-ai/references/ai-solutions-engineer.md) | `execute` | `l5-realisation` |
| [API Developer](../../it-roles-software-development-and-engineering/references/api-developer.md) | `execute` | `l5-realisation` |
| [Agile Coach](../../it-roles-product-delivery-and-agile/references/agile-coach.md) | `author` | `l5-realisation` |
| [Analytics Engineer](../../it-roles-data-analytics-and-ai/references/analytics-engineer.md) | `execute` | `l5-realisation` |
| [Application Security Engineer](../../it-roles-security-operations-and-defensive-security/references/application-security-engineer.md) | `execute` | `l5-realisation` |
| [Backend Engineer](../../it-roles-software-development-and-engineering/references/backend-engineer.md) | `execute` | `l5-realisation` |
| [Blockchain and Smart Contract Developer](../../it-roles-software-development-and-engineering/references/blockchain-and-smart-contract-developer.md) | `execute` | `l5-realisation` |
| [Build Engineer](../../it-roles-software-development-and-engineering/references/build-engineer.md) | `execute` | `l5-realisation` |
| [CI/CD Platform Engineer](../../it-roles-software-development-and-engineering/references/ci-cd-platform-engineer.md) | `execute` | `l5-realisation` |
| [Cloud Engineer](../../it-roles-infrastructure-cloud-and-operations/references/cloud-engineer.md) | `execute` | `l5-realisation` |
| [Cloud Security Engineer](../../it-roles-security-operations-and-defensive-security/references/cloud-security-engineer.md) | `execute` | `l5-realisation` |
| [Compiler and Toolchain Engineer](../../it-roles-software-development-and-engineering/references/compiler-and-toolchain-engineer.md) | `execute` | `l5-realisation` |
| [Container Platform Engineer](../../it-roles-infrastructure-cloud-and-operations/references/container-platform-engineer.md) | `execute` | `l5-realisation` |
| [Cryptography and PKI Engineer](../../it-roles-security-operations-and-defensive-security/references/cryptography-and-pki-engineer.md) | `execute` | `l5-realisation` |
| [Customer Success Engineer](../../it-roles-commercial-sourcing-and-enablement/references/customer-success-engineer.md) | `author` | `l5-realisation` |
| [Data Engineer](../../it-roles-data-analytics-and-ai/references/data-engineer.md) | `execute` | `l5-realisation` |
| [Data Privacy Engineer](../../it-roles-data-analytics-and-ai/references/data-privacy-engineer.md) | `execute` | `l5-realisation` |
| [Design System Engineer](../../it-roles-design-and-user-experience/references/design-system-engineer.md) | `execute` | `l5-realisation` |
| [Detection Engineer](../../it-roles-security-operations-and-defensive-security/references/detection-engineer.md) | `execute` | `l5-realisation` |
| [DevOps Engineer](../../it-roles-infrastructure-cloud-and-operations/references/devops-engineer.md) | `execute` | `l5-realisation` |
| [Developer Advocate](../../it-roles-commercial-sourcing-and-enablement/references/developer-advocate.md) | `author` | `l5-realisation` |
| [Developer Experience Engineer](../../it-roles-software-development-and-engineering/references/developer-experience-engineer.md) | `execute` | `l5-realisation` |
| [ERP and CRM Consultant Developer](../../it-roles-software-development-and-engineering/references/erp-and-crm-consultant-developer.md) | `execute` | `l5-realisation` |
| [Embedded Firmware Engineer](../../it-roles-software-development-and-engineering/references/embedded-firmware-engineer.md) | `execute` | `l5-realisation` |
| [End-User Computing Engineer](../../it-roles-service-management-and-support/references/end-user-computing-engineer.md) | `execute` | `l5-realisation` |
| [Environment Manager](../../it-roles-infrastructure-cloud-and-operations/references/environment-manager.md) | `author` | `l5-realisation` |
| [FinOps Engineer](../../it-roles-infrastructure-cloud-and-operations/references/finops-engineer.md) | `execute` | `l5-realisation` |
| [Frontend Engineer](../../it-roles-software-development-and-engineering/references/frontend-engineer.md) | `execute` | `l5-realisation` |
| [Full-stack Engineer](../../it-roles-software-development-and-engineering/references/full-stack-engineer.md) | `execute` | `l5-realisation` |
| [Game Developer](../../it-roles-software-development-and-engineering/references/game-developer.md) | `execute` | `l5-realisation` |
| [GitOps and Continuous Delivery Engineer](../../it-roles-software-development-and-engineering/references/gitops-and-continuous-delivery-engineer.md) | `execute` | `l5-realisation` |
| [Graphics and Engine Engineer](../../it-roles-software-development-and-engineering/references/graphics-and-engine-engineer.md) | `execute` | `l5-realisation` |
| [IT Trainer](../../it-roles-commercial-sourcing-and-enablement/references/it-trainer.md) | `author` | `l5-realisation` |
| [Identity and Access Management Engineer](../../it-roles-security-operations-and-defensive-security/references/identity-and-access-management-engineer.md) | `execute` | `l5-realisation` |
| [Implementation Consultant](../../it-roles-commercial-sourcing-and-enablement/references/implementation-consultant.md) | `author` | `l5-realisation` |
| [Infrastructure as Code Engineer](../../it-roles-infrastructure-cloud-and-operations/references/infrastructure-as-code-engineer.md) | `execute` | `l5-realisation` |
| [Integration Developer](../../it-roles-software-development-and-engineering/references/integration-developer.md) | `execute` | `l5-realisation` |
| [Kubernetes Platform Engineer](../../it-roles-infrastructure-cloud-and-operations/references/kubernetes-platform-engineer.md) | `execute` | `l5-realisation` |
| [Low-code and RPA Developer](../../it-roles-software-development-and-engineering/references/low-code-and-rpa-developer.md) | `execute` | `l5-realisation` |
| [Machine Learning Engineer](../../it-roles-data-analytics-and-ai/references/machine-learning-engineer.md) | `execute` | `l5-realisation` |
| [Mainframe Developer](../../it-roles-software-development-and-engineering/references/mainframe-developer.md) | `execute` | `l5-realisation` |
| [Mobile Engineer](../../it-roles-software-development-and-engineering/references/mobile-engineer.md) | `execute` | `l5-realisation` |
| [Observability Engineer](../../it-roles-infrastructure-cloud-and-operations/references/observability-engineer.md) | `execute` | `l5-realisation` |
| [Physical Security Solution Builder (SABSA Builder's View)](../../it-roles-sabsa-security-architecture/references/physical-security-solution-builder-sabsa-builder-s-view.md) | `execute` | `l5-realisation` |
| [Platform Engineer](../../it-roles-infrastructure-cloud-and-operations/references/platform-engineer.md) | `execute` | `l5-realisation` |
| [Pre-Sales Solution Consultant](../../it-roles-commercial-sourcing-and-enablement/references/pre-sales-solution-consultant.md) | `author` | `l5-realisation` |
| [Quantitative Developer](../../it-roles-software-development-and-engineering/references/quantitative-developer.md) | `execute` | `l5-realisation` |
| [Real-time Systems Engineer](../../it-roles-software-development-and-engineering/references/real-time-systems-engineer.md) | `execute` | `l5-realisation` |
| [Release Engineer](../../it-roles-software-development-and-engineering/references/release-engineer.md) | `execute` | `l5-realisation` |
| [SD-WAN and Edge Engineer](../../it-roles-network-and-telecommunications/references/sd-wan-and-edge-engineer.md) | `execute` | `l5-realisation` |
| [Sales Engineer](../../it-roles-commercial-sourcing-and-enablement/references/sales-engineer.md) | `author` | `l5-realisation` |
| [Secrets and Configuration Management Engineer](../../it-roles-security-operations-and-defensive-security/references/secrets-and-configuration-management-engineer.md) | `execute` | `l5-realisation` |
| [Security Awareness and Training Manager](../../it-roles-security-operations-and-defensive-security/references/security-awareness-and-training-manager.md) | `author` | `l5-realisation` |
| [Security Champion](../../it-roles-security-operations-and-defensive-security/references/security-champion.md) | `author` | `l5-realisation` |
| [Security Component Specialist (SABSA Tradesman's View)](../../it-roles-sabsa-security-architecture/references/security-component-specialist-sabsa-tradesman-s-view.md) | `execute` | `l5-realisation` |
| [Security Engineer](../../it-roles-security-operations-and-defensive-security/references/security-engineer.md) | `execute` | `l5-realisation` |
| [Senior Software Engineer](../../it-roles-software-development-and-engineering/references/senior-software-engineer.md) | `execute` | `l5-realisation` |
| [Simulation Engineer](../../it-roles-research-innovation-and-specialist-engineering/references/simulation-engineer.md) | `execute` | `l5-realisation` |
| [Software Engineer](../../it-roles-software-development-and-engineering/references/software-engineer.md) | `execute` | `l5-realisation` |
| [Software Modernisation Engineer](../../it-roles-software-development-and-engineering/references/software-modernisation-engineer.md) | `execute` | `l5-realisation` |
| [Standards Body Representative](../../it-roles-research-innovation-and-specialist-engineering/references/standards-body-representative.md) | `author` | `l5-realisation` |
| [Systems Programmer](../../it-roles-software-development-and-engineering/references/systems-programmer.md) | `execute` | `l5-realisation` |
| [Technical Account Manager](../../it-roles-commercial-sourcing-and-enablement/references/technical-account-manager.md) | `author` | `l5-realisation` |
| [Technical Recruiter](../../it-roles-commercial-sourcing-and-enablement/references/technical-recruiter.md) | `author` | `l5-realisation` |
| [Technical Writer](../../it-roles-commercial-sourcing-and-enablement/references/technical-writer.md) | `author` | `l5-realisation` |
| [Wireless and RF Engineer](../../it-roles-network-and-telecommunications/references/wireless-and-rf-engineer.md) | `execute` | `l5-realisation` |

## Layer 6 — Execution and Evidence (70 roles)

Layer agent `l6-evidence` · tier `inspect` · workload class `standard`

| Role | Role tier | Operated by |
| --- | --- | --- |
| [AI Safety and Model Red Team Specialist](../../it-roles-data-analytics-and-ai/references/ai-safety-and-model-red-team-specialist.md) | `advise` | `role-advisor` |
| [Accessibility Tester](../../it-roles-quality-and-testing/references/accessibility-tester.md) | `execute` | `l6-evidence` |
| [Adversary Emulation Engineer](../../it-roles-offensive-security-and-adversarial-testing/references/adversary-emulation-engineer.md) | `advise` | `role-advisor` |
| [Application Support Analyst](../../it-roles-service-management-and-support/references/application-support-analyst.md) | `execute` | `l6-evidence` |
| [Backup and Recovery Engineer](../../it-roles-infrastructure-cloud-and-operations/references/backup-and-recovery-engineer.md) | `execute` | `l6-evidence` |
| [Breach and Attack Simulation Engineer](../../it-roles-offensive-security-and-adversarial-testing/references/breach-and-attack-simulation-engineer.md) | `advise` | `role-advisor` |
| [Bug Bounty Triage Analyst](../../it-roles-offensive-security-and-adversarial-testing/references/bug-bounty-triage-analyst.md) | `advise` | `role-advisor` |
| [Chaos and Resilience Engineer](../../it-roles-quality-and-testing/references/chaos-and-resilience-engineer.md) | `execute` | `l6-evidence` |
| [Cloud Operations Engineer](../../it-roles-infrastructure-cloud-and-operations/references/cloud-operations-engineer.md) | `execute` | `l6-evidence` |
| [Codebase Reviewer](../../it-roles-quality-and-testing/references/codebase-reviewer.md) | `inspect` | `l6-evidence` |
| [Control Tester](../../it-roles-governance-risk-compliance-audit-and-privacy/references/control-tester.md) | `advise` | `role-advisor` |
| [Crisis Manager](../../it-roles-governance-risk-compliance-audit-and-privacy/references/crisis-manager.md) | `execute` | `l6-evidence` |
| [DNS DHCP and IPAM Specialist](../../it-roles-network-and-telecommunications/references/dns-dhcp-and-ipam-specialist.md) | `execute` | `l6-evidence` |
| [Data Custodian](../../it-roles-data-analytics-and-ai/references/data-custodian.md) | `execute` | `l6-evidence` |
| [Data Quality Analyst](../../it-roles-data-analytics-and-ai/references/data-quality-analyst.md) | `author` | `role-advisor` |
| [Database Administrator](../../it-roles-data-analytics-and-ai/references/database-administrator.md) | `execute` | `l6-evidence` |
| [Database Reliability Engineer](../../it-roles-data-analytics-and-ai/references/database-reliability-engineer.md) | `execute` | `l6-evidence` |
| [Datacentre Technician](../../it-roles-infrastructure-cloud-and-operations/references/datacentre-technician.md) | `execute` | `l6-evidence` |
| [Desktop Support Engineer](../../it-roles-service-management-and-support/references/desktop-support-engineer.md) | `execute` | `l6-evidence` |
| [Digital Forensics Examiner](../../it-roles-security-operations-and-defensive-security/references/digital-forensics-examiner.md) | `inspect` | `l6-evidence` |
| [Disaster Recovery Coordinator](../../it-roles-governance-risk-compliance-audit-and-privacy/references/disaster-recovery-coordinator.md) | `execute` | `l6-evidence` |
| [External Auditor and Assessor](../../it-roles-governance-risk-compliance-audit-and-privacy/references/external-auditor-and-assessor.md) | `advise` | `role-advisor` |
| [Firewall and Perimeter Engineer](../../it-roles-network-and-telecommunications/references/firewall-and-perimeter-engineer.md) | `execute` | `l6-evidence` |
| [High Performance Computing Engineer](../../it-roles-research-innovation-and-specialist-engineering/references/high-performance-computing-engineer.md) | `execute` | `l6-evidence` |
| [Incident Manager](../../it-roles-service-management-and-support/references/incident-manager.md) | `execute` | `l6-evidence` |
| [Incident Responder](../../it-roles-security-operations-and-defensive-security/references/incident-responder.md) | `author` | `role-advisor` |
| [Insider Threat Analyst](../../it-roles-security-operations-and-defensive-security/references/insider-threat-analyst.md) | `advise` | `role-advisor` |
| [Internal IT Auditor](../../it-roles-governance-risk-compliance-audit-and-privacy/references/internal-it-auditor.md) | `advise` | `role-advisor` |
| [LLMOps and AI Platform Engineer](../../it-roles-data-analytics-and-ai/references/llmops-and-ai-platform-engineer.md) | `execute` | `l6-evidence` |
| [Linux Systems Administrator](../../it-roles-infrastructure-cloud-and-operations/references/linux-systems-administrator.md) | `execute` | `l6-evidence` |
| [Localisation QA Analyst](../../it-roles-quality-and-testing/references/localisation-qa-analyst.md) | `execute` | `l6-evidence` |
| [MLOps Engineer](../../it-roles-data-analytics-and-ai/references/mlops-engineer.md) | `execute` | `l6-evidence` |
| [Major Incident Manager](../../it-roles-service-management-and-support/references/major-incident-manager.md) | `execute` | `l6-evidence` |
| [Malware Analyst](../../it-roles-security-operations-and-defensive-security/references/malware-analyst.md) | `inspect` | `l6-evidence` |
| [Middleware Administrator](../../it-roles-infrastructure-cloud-and-operations/references/middleware-administrator.md) | `execute` | `l6-evidence` |
| [Network Administrator](../../it-roles-network-and-telecommunications/references/network-administrator.md) | `execute` | `l6-evidence` |
| [Network Engineer](../../it-roles-network-and-telecommunications/references/network-engineer.md) | `execute` | `l6-evidence` |
| [Network Field Technician](../../it-roles-network-and-telecommunications/references/network-field-technician.md) | `execute` | `l6-evidence` |
| [Network Operations Centre Analyst](../../it-roles-network-and-telecommunications/references/network-operations-centre-analyst.md) | `execute` | `l6-evidence` |
| [Operational Technology Security Engineer](../../it-roles-security-operations-and-defensive-security/references/operational-technology-security-engineer.md) | `author` | `role-advisor` |
| [Penetration Tester (API)](../../it-roles-offensive-security-and-adversarial-testing/references/penetration-tester-api.md) | `advise` | `role-advisor` |
| [Penetration Tester (Cloud)](../../it-roles-offensive-security-and-adversarial-testing/references/penetration-tester-cloud.md) | `advise` | `role-advisor` |
| [Penetration Tester (Mobile)](../../it-roles-offensive-security-and-adversarial-testing/references/penetration-tester-mobile.md) | `advise` | `role-advisor` |
| [Penetration Tester (Network and Infrastructure)](../../it-roles-offensive-security-and-adversarial-testing/references/penetration-tester-network-and-infrastructure.md) | `advise` | `role-advisor` |
| [Penetration Tester (Thick Client)](../../it-roles-offensive-security-and-adversarial-testing/references/penetration-tester-thick-client.md) | `advise` | `role-advisor` |
| [Penetration Tester (Web Application)](../../it-roles-offensive-security-and-adversarial-testing/references/penetration-tester-web-application.md) | `advise` | `role-advisor` |
| [Penetration Tester (Wireless)](../../it-roles-offensive-security-and-adversarial-testing/references/penetration-tester-wireless.md) | `advise` | `role-advisor` |
| [Performance Test Engineer](../../it-roles-quality-and-testing/references/performance-test-engineer.md) | `execute` | `l6-evidence` |
| [Physical Intrusion Specialist](../../it-roles-offensive-security-and-adversarial-testing/references/physical-intrusion-specialist.md) | `advise` | `role-advisor` |
| [Privileged Access Management Administrator](../../it-roles-security-operations-and-defensive-security/references/privileged-access-management-administrator.md) | `execute` | `l6-evidence` |
| [Purple Team Lead](../../it-roles-security-operations-and-defensive-security/references/purple-team-lead.md) | `advise` | `role-advisor` |
| [Red Team Operator](../../it-roles-offensive-security-and-adversarial-testing/references/red-team-operator.md) | `advise` | `role-advisor` |
| [Release Quality Gatekeeper](../../it-roles-quality-and-testing/references/release-quality-gatekeeper.md) | `advise` | `role-advisor` |
| [Security Analyst Tier 1](../../it-roles-security-operations-and-defensive-security/references/security-analyst-tier-1.md) | `author` | `role-advisor` |
| [Security Analyst Tier 2](../../it-roles-security-operations-and-defensive-security/references/security-analyst-tier-2.md) | `author` | `role-advisor` |
| [Security Analyst Tier 3](../../it-roles-security-operations-and-defensive-security/references/security-analyst-tier-3.md) | `author` | `role-advisor` |
| [Security Assurance and Measurement Architect](../../it-roles-sabsa-security-architecture/references/security-assurance-and-measurement-architect.md) | `advise` | `role-advisor` |
| [Security Service Manager (SABSA Service Management View)](../../it-roles-sabsa-security-architecture/references/security-service-manager-sabsa-service-management-view.md) | `author` | `role-advisor` |
| [Service Desk Analyst](../../it-roles-service-management-and-support/references/service-desk-analyst.md) | `execute` | `l6-evidence` |
| [Service Level Analyst](../../it-roles-analysis/references/service-level-analyst.md) | `author` | `role-advisor` |
| [Site Reliability Engineer](../../it-roles-infrastructure-cloud-and-operations/references/site-reliability-engineer.md) | `execute` | `l6-evidence` |
| [Social Engineering Specialist](../../it-roles-offensive-security-and-adversarial-testing/references/social-engineering-specialist.md) | `advise` | `role-advisor` |
| [Storage Engineer](../../it-roles-infrastructure-cloud-and-operations/references/storage-engineer.md) | `execute` | `l6-evidence` |
| [Test Analyst](../../it-roles-quality-and-testing/references/test-analyst.md) | `execute` | `l6-evidence` |
| [Test Automation Engineer](../../it-roles-quality-and-testing/references/test-automation-engineer.md) | `execute` | `l6-evidence` |
| [Threat Hunter](../../it-roles-security-operations-and-defensive-security/references/threat-hunter.md) | `author` | `role-advisor` |
| [Unified Communications Engineer](../../it-roles-network-and-telecommunications/references/unified-communications-engineer.md) | `execute` | `l6-evidence` |
| [Usability Tester](../../it-roles-design-and-user-experience/references/usability-tester.md) | `execute` | `l6-evidence` |
| [Virtualisation Engineer](../../it-roles-infrastructure-cloud-and-operations/references/virtualisation-engineer.md) | `execute` | `l6-evidence` |
| [Windows Systems Administrator](../../it-roles-infrastructure-cloud-and-operations/references/windows-systems-administrator.md) | `execute` | `l6-evidence` |
