# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Exact professional output refinements, separate from frozen storage identities.

These authored JAI requirements interpret cited public professional guidance.
They do not quote licensed clauses, certify conformance or grant approval.
Keys are stable contract IDs; no title-based production classifier is used.
"""

OUTPUT_REFINEMENTS = {
    'accessibility-tester:1': 'assurance-report',
    'enterprise-architect:2': 'register',
}

OUTPUT_REQUIREMENTS = {
    'accessibility-tester:1': [
        ('accessibility_target', 'object',
         'Identify the assessed product and exact revision, WCAG edition and target level, '
         'applicable additional requirements, complete-process boundaries, evaluation date '
         'and permitted conformance claim; distinguish adopted requirements from advice.'),
        ('accessibility_sample', 'object',
         'Define the population, representative and additional sampling rationale, '
         'included pages/states/complete processes, exclusions, technologies, browser '
         'and assistive-technology versions and manual versus automated methods.'),
        ('accessibility_results', 'array',
         'For each applicable success criterion and evaluated sample, record stable '
         'criterion and sample IDs, expected and observed result, passed/failed/blocked/'
         'not-tested/not-applicable status, method, reproducible evidence and defect '
         'reference. Justify non-applicability; tool scores alone cannot establish conformance.'),
        ('accessibility_conclusion', 'object',
         'Reconcile criterion outcomes, sample coverage and unresolved failures with '
         'the target and applicable conformance conditions; bound the conclusion by '
         'untested states, inaccessible dependencies and uncertainty. Identify remediation '
         'and retest owners; a sampled result is not an unrestricted whole-product claim.')],
    'enterprise-architect:2': [
        ('principle_records', 'array',
         'For each principle, record stable ID, normative statement, scope, business '
         'driver, rationale, practical implications, accountable owner, adoption status '
         'and source version; distinguish a proposed principle from an adopted obligation.'),
        ('principle_conflicts', 'array',
         'Record conflicts, precedence and justified tradeoffs between principles '
         'and existing policies. Define exception authority, required justification, '
         'expiry and review; explicitly record when no conflicts or exceptions are known.'),
        ('principle_verification', 'array',
         'For each principle, define observable architecture/design checks, evidence, '
         'responsible reviewer and change trigger. Carry principle records in a governed '
         'register or document; an EA diagram is optional and cannot replace the rationale.')],
}

OUTPUT_REFERENCES = {
    'accessibility-tester:1': ['accessibility', 'accessibility-evaluation'],
    'enterprise-architect:2': ['architecture-description', 'it-governance'],
}

ADDITIONAL_REFERENCES = {
    'accessibility-evaluation': {
        'title': 'W3C WCAG Evaluation Methodology (WCAG-EM) 2.0',
        'url': 'https://www.w3.org/TR/wcag-em-2/',
        'scope': 'Evaluation scope, representative sample, evaluation and reporting; '
                 'W3C Group Note, informative methodology rather than a conformance standard.'},
}

DELIVERY_FORMS = {
    'enterprise-architect:1': {
        'primary_artifact': 'architecture-description',
        'representation': 'Concern-driven architecture description with linked views; '
                          'notation chosen for audience and qualified project profile.',
        'evidence': ['versioned architecture baseline', 'cross-view review results']},
    'enterprise-architect:2': {
        'primary_artifact': 'principle-register',
        'representation': 'Governed principle records with rationale, implications and exceptions.',
        'evidence': ['principle-to-driver traceability', 'independent principle review']},
    'enterprise-architect:4': {
        'primary_artifact': 'architecture-decision-record',
        'representation': 'Versioned ADR; an EA tool representation is optional.',
        'evidence': ['option evaluation', 'actual decision status and supersession links']},
    'software-engineer:1': {
        'primary_artifact': 'versioned-source-change',
        'representation': 'Actual version-controlled source change, separate from its review summary.',
        'evidence': ['exact source revision', 'observed tests and independent code review',
                     'merge and deployment status supported by actual records']},
    'software-engineer:2': {
        'primary_artifact': 'executable-test-suite',
        'representation': 'Executable tests in version control with reproducible invocation.',
        'evidence': ['exact suite and tested revision', 'observed execution results',
                     'risk/requirement coverage and exclusions']},
    'software-engineer:3': {
        'primary_artifact': 'change-documentation',
        'representation': 'Versioned maintenance/user documentation appropriate to the change.',
        'evidence': ['changed interface/behaviour references', 'documentation review']},
    'software-engineer:4': {
        'primary_artifact': 'deployment-and-recovery-procedure',
        'representation': 'Versioned operational procedure with exact targets and recovery branches.',
        'evidence': ['verification checkpoints', 'actual rehearsal or explicit untested status']},
}

for _form in DELIVERY_FORMS.values():
    _form['legacy_type_is_compatibility_only'] = True
    _form['authority'] = 'Content guidance only; existing execution and human authority boundaries remain.'

# Exact-ID corrections from the full catalogue inventory. Legacy storage types
# stay immutable; these assignments govern the professional work product.
OUTPUT_REFINEMENTS.update({
    'chief-information-officer:2': 'register',
    'chief-product-officer:2': 'register',
    'chief-ai-officer:4': 'document',
    'vp-of-engineering:4': 'roadmap',
    'it-service-owner:2': 'dataset',
    'technical-product-manager:3': 'dashboard',
    'product-owner:3': 'requirements-specification',
    'scrum-master:3': 'dashboard',
    'scrum-master:4': 'register',
    'safe-system-architect:3': 'requirements-specification',
    'safe-system-architect:4': 'requirements-specification',
    'portfolio-manager:1': 'register',
    'portfolio-manager:2': 'dataset',
    'portfolio-manager:4': 'decision-paper',
    'pmo-analyst:4': 'register',
    'technical-lead:4': 'roadmap',
    'transformation-manager:3': 'dashboard',
    'requirements-engineer:2': 'register',
    'process-analyst:3': 'model',
    'process-analyst:4': 'business-case',
    'enterprise-business-analyst:3': 'model',
    'data-analyst:1': 'software-change',
    'data-analyst:4': 'register',
    'business-intelligence-analyst:4': 'model',
    'finops-analyst:1': 'dataset',
    'service-level-analyst:2': 'service-design',
    'configuration-analyst:1': 'catalogue',
    'configuration-analyst:2': 'model',
    'configuration-analyst:3': 'assurance-report',
    'business-architect:1': 'model',
    'business-architect:2': 'model',
    'business-architect:3': 'dashboard',
    'business-architect:4': 'roadmap',
    'application-architect:1': 'hld',
    'application-architect:2': 'requirements-specification',
    'data-architect:1': 'model',
    'cloud-architect:3': 'dataset',
    'cloud-architect:4': 'model',
    'technical-design-authority-member:3': 'adr',
    'technical-design-authority-member:4': 'test-strategy',
    'full-stack-engineer:3': 'software-change',
    'full-stack-engineer:4': 'configuration-baseline',
    'mobile-engineer:2': 'software-change',
    'mobile-engineer:4': 'hld',
    'low-code-and-rpa-developer:2': 'implementation-specification',
    'low-code-and-rpa-developer:4': 'configuration-baseline',
    'quantitative-developer:4': 'document',
    'ci-cd-platform-engineer:2': 'hld',
    'gitops-and-continuous-delivery-engineer:1': 'deployment-automation',
    'developer-experience-engineer:2': 'dashboard',
    'test-analyst:1': 'test-strategy',
    'test-manager:2': 'test-report',
    'test-manager:3': 'risk-assessment',
    'test-architect:4': 'dashboard',
    'user-acceptance-test-coordinator:2': 'test-strategy',
    'accessibility-tester:2': 'test-report',
    'accessibility-tester:3': 'register',
    'localisation-qa-analyst:3': 'register',
    'chaos-and-resilience-engineer:1': 'test-strategy',
    'chaos-and-resilience-engineer:2': 'test-report',
    'chaos-and-resilience-engineer:3': 'test-report',
    'chaos-and-resilience-engineer:4': 'test-strategy',
    'codebase-reviewer:1': 'assurance-report',
    'codebase-reviewer:3': 'assurance-report',
    'release-quality-gatekeeper:2': 'decision-paper',
    'release-quality-gatekeeper:4': 'register',
    'data-engineer:2': 'model',
    'analytics-engineer:1': 'software-change',
    'analytics-engineer:2': 'model',
    'analytics-engineer:3': 'catalogue',
    'database-administrator:4': 'roadmap',
    'data-modeller:1': 'model',
    'data-modeller:2': 'catalogue',
    'data-modeller:3': 'document',
    'data-steward:1': 'catalogue',
    'data-steward:2': 'requirements-specification',
    'data-owner:3': 'requirements-specification',
    'internal-it-auditor:2': 'assurance-report',
    'internal-it-auditor:4': 'assurance-report',
    'external-auditor-and-assessor:3': 'assurance-report',
    'control-tester:1': 'test-strategy',
    'control-tester:3': 'assurance-report',
    'records-manager:1': 'register',
    'records-manager:3': 'register',
    'business-continuity-manager:3': 'test-report',
    'business-continuity-manager:4': 'requirements-specification',
    'ux-designer:1': 'document',
    'ux-designer:2': 'model',
    'ux-designer:4': 'test-report',
    'product-designer:2': 'document',
    'product-designer:4': 'test-report',
    'usability-tester:3': 'test-report',
    'usability-tester:4': 'test-report',
    'interaction-designer:4': 'document',
    'service-designer:1': 'model',
    'service-designer:4': 'test-report',
    'information-architect:1': 'model',
    'information-architect:3': 'catalogue',
    'information-architect:4': 'test-report',
    'design-system-engineer:4': 'assurance-report',
    'content-designer:3': 'catalogue',
    'content-designer:4': 'test-report',
    'sales-engineer:3': 'configuration-baseline',
    'contract-manager:3': 'assurance-report',
    'technical-recruiter:3': 'register',
    'research-engineer:2': 'test-report',
    'innovation-lead:1': 'register',
    'innovation-lead:3': 'decision-paper',
    'technology-scout:3': 'document',
    'technology-scout:4': 'register',
    'systems-engineer-incose:3': 'test-strategy',
    'systems-engineer-incose:4': 'decision-paper',
    'simulation-engineer:1': 'model',
    'simulation-engineer:2': 'test-report',
    'simulation-engineer:4': 'document',
    'chief-security-architect-sabsa-practice-lead:4': 'roadmap',
    'security-component-specialist-sabsa-tradesman-s-view:4': 'test-report',
    'security-service-manager-sabsa-service-management-view:3': 'assurance-report',
    'security-domain-authority:3': 'decision-paper',
    'security-domain-authority:4': 'assurance-report',
    'security-risk-and-opportunity-architect:1': 'risk-assessment',
    'security-risk-and-opportunity-architect:2': 'risk-assessment',
    'security-risk-and-opportunity-architect:3': 'risk-assessment',
    'security-assurance-and-measurement-architect:3': 'assurance-report',
    'architecture-repository-and-modelling-lead:4': 'assurance-report',
    'independent-commercial-assurance-reviewer:1': 'assurance-report',
    'independent-commercial-assurance-reviewer:2': 'assurance-report',
})

# A second complete inventory review distinguishes reporting/investigation from
# requested decisions. These are authored exact IDs, not runtime title rules.
for _cid in '''
chief-information-security-officer:4 head-of-platform:4 agile-coach:1 agile-coach:4
delivery-manager:3 epic-owner:4 project-manager:4 portfolio-manager:3 pmo-analyst:1
pmo-analyst:3 pmo-lead:3 engineering-manager:2 engineering-manager:4 transformation-manager:1
business-analyst:3 business-analyst:4 systems-analyst:3 requirements-engineer:3
requirements-engineer:4 process-analyst:2 enterprise-business-analyst:1
enterprise-business-analyst:2 data-analyst:2 finops-analyst:2 product-analyst:3
product-analyst:4 service-level-analyst:1 service-level-analyst:3 service-level-analyst:4
senior-software-engineer:4 embedded-firmware-engineer:3 real-time-systems-engineer:2
systems-programmer:2 integration-developer:4 erp-and-crm-consultant-developer:3
graphics-and-engine-engineer:2 build-engineer:2 open-source-program-office-engineer:4
performance-test-engineer:3 localisation-qa-analyst:4 database-administrator:3
data-quality-analyst:3 data-quality-analyst:4 data-scientist:2 data-scientist:4
research-scientist:3 llmops-and-ai-platform-engineer:4 virtualisation-engineer:2
storage-engineer:2 availability-manager:2 availability-manager:3 sustainable-it-engineer:3
network-engineer:4 network-operations-centre-analyst:4 unified-communications-engineer:3
application-support-analyst:4 incident-manager:3 major-incident-manager:4
problem-manager:4 change-manager:3 request-fulfilment-manager:3 service-level-manager:2
continual-improvement-manager:3 knowledge-manager:2 it-asset-manager:2
software-asset-manager:1 software-asset-manager:4 end-user-computing-engineer:4
business-relationship-manager:3 security-analyst-tier-2:2 security-analyst-tier-3:1
security-analyst-tier-3:4 soc-manager:2 soc-manager:3 incident-responder:4
digital-forensics-examiner:2 malware-analyst:1 malware-analyst:3
threat-intelligence-analyst:4 detection-engineer:4 vulnerability-management-analyst:4
identity-governance-specialist:4 insider-threat-analyst:2
penetration-tester-network-and-infrastructure:3 penetration-tester-wireless:4
red-team-lead:3 exploit-developer:2 binary-reverse-engineer:1
social-engineering-specialist:4 physical-intrusion-specialist:4
open-source-intelligence-investigator:3 hardware-and-iot-security-researcher:2
hardware-and-iot-security-researcher:4 it-governance-manager:4 grc-analyst:4
information-security-officer-local:1 business-continuity-manager:1 crisis-manager:4
ux-researcher:4 pre-sales-solution-consultant:4 sales-engineer:1
customer-success-engineer:1 customer-success-engineer:4 implementation-consultant:4
technical-account-manager:4 it-trainer:1 it-trainer:4 technical-recruiter:4
resource-manager:2 research-engineer:3 innovation-lead:2 technology-scout:2
standards-body-representative:3 ethics-and-responsible-technology-lead:2
simulation-engineer:3 high-performance-computing-engineer:2
high-performance-computing-engineer:4 quantum-computing-engineer:2
organisational-change-and-adoption-manager:1 technology-lifecycle-and-decommission-manager:4
demand-and-intake-manager:2 commercial-pricing-deal-finance-specialist:3
estimation-cost-engineering-specialist:3
cloud-operations-engineer:4 data-modeller:3 security-analyst-tier-1:3
security-analyst-tier-1:4 security-analyst-tier-2:4 threat-hunter:2 threat-hunter:4
application-security-engineer:3 security-champion:3 data-protection-officer:2
data-protection-officer:3 privacy-analyst:3 disaster-recovery-coordinator:3
product-designer:3 ux-researcher:2 developer-advocate:3 technology-scout:3
service-designer:3 simulation-engineer:4 quantum-computing-engineer:4
business-security-architect-sabsa-contextual-layer:3
'''.split():
    OUTPUT_REFINEMENTS[_cid] = 'analysis-report'

OUTPUT_REFINEMENTS.update({
    'network-operations-centre-analyst:2': 'register',
    'network-operations-centre-analyst:3': 'register',
    'senior-software-engineer:3': 'assurance-report',
    'test-analyst:3': 'test-report',
    'localisation-qa-analyst:2': 'test-report',
    'firewall-and-perimeter-engineer:2': 'assurance-report',
    'knowledge-manager:3': 'runbook',
    'compliance-officer-technology:2': 'assurance-report',
    'ai-governance-officer:2': 'assurance-report',
    'control-owner:3': 'assurance-report',
    'ethics-and-responsible-technology-lead:1': 'test-strategy',
    'vulnerability-disclosure-coordinator:2': 'register',
    'standards-body-representative:1': 'document',
    'bid-proposal-manager:4': 'register',
    'release-quality-gatekeeper:2': 'register',
    'bug-bounty-triage-analyst:2': 'analysis-report',
    'data-protection-officer:4': 'analysis-report',
    'software-licence-compliance-specialist:2': 'assurance-report',
    'security-domain-authority:3': 'register',
    'systems-analyst:2': 'model',
    'systems-analyst:4': 'implementation-specification',
    'head-of-platform:3': 'service-design',
    'systems-programmer:4': 'register',
    'data-custodian:2': 'register',
    'master-data-management-specialist:1': 'implementation-specification',
    'master-data-management-specialist:4': 'dashboard',
    'product-analyst:2': 'test-report',
    'research-scientist:1': 'test-strategy',
    'research-scientist:2': 'test-report',
    'mlops-engineer:2': 'configuration-baseline',
    'ai-safety-and-model-red-team-specialist:1': 'automated-tests',
    'ai-safety-and-model-red-team-specialist:3': 'test-report',
    'ai-governance-officer:3': 'register',
    'cloud-operations-engineer:3': 'deployment-automation',
    'platform-engineer:1': 'software-change',
    'platform-engineer:3': 'service-design',
    'virtualisation-engineer:4': 'test-report',
    'storage-engineer:4': 'test-report',
    'backup-and-recovery-engineer:3': 'test-report',
    'datacentre-technician:2': 'register',
    'datacentre-technician:3': 'dataset',
    'availability-manager:4': 'register',
    'observability-engineer:3': 'configuration-baseline',
    'middleware-administrator:2': 'configuration-baseline',
    'finops-engineer:3': 'configuration-baseline',
    'finops-engineer:4': 'register',
    'network-administrator:3': 'register',
    'wireless-and-rf-engineer:1': 'test-report',
    'unified-communications-engineer:4': 'configuration-baseline',
    'sd-wan-and-edge-engineer:4': 'configuration-baseline',
    'network-field-technician:3': 'register',
    'network-field-technician:4': 'register',
    'service-desk-analyst:2': 'register',
    'service-desk-analyst:4': 'register',
    'desktop-support-engineer:2': 'register',
    'desktop-support-engineer:4': 'register',
    'application-support-analyst:3': 'register',
    'incident-manager:4': 'register',
    'major-incident-manager:3': 'register',
    'problem-manager:2': 'register',
    'service-level-manager:1': 'service-design',
    'service-level-manager:4': 'service-design',
    'continual-improvement-manager:2': 'analysis-report',
    'configuration-manager:2': 'assurance-report',
    'configuration-manager:3': 'model',
    'it-asset-manager:4': 'analysis-report',
    'end-user-computing-engineer:2': 'configuration-baseline',
    'security-analyst-tier-1:2': 'register',
    'security-analyst-tier-2:3': 'register',
    'threat-hunter:3': 'software-change',
    'incident-responder:2': 'register',
    'incident-responder:3': 'test-report',
    'digital-forensics-examiner:3': 'register',
    'malware-analyst:2': 'dataset',
    'malware-analyst:4': 'software-change',
    'threat-intelligence-analyst:1': 'requirements-specification',
    'threat-intelligence-analyst:3': 'dataset',
    'detection-engineer:1': 'software-change',
    'detection-engineer:2': 'automated-tests',
    'detection-engineer:3': 'register',
    'security-engineer:2': 'configuration-baseline',
    'security-engineer:4': 'software-change',
    'vulnerability-management-analyst:1': 'test-report',
    'vulnerability-management-analyst:2': 'register',
    'identity-and-access-management-engineer:2': 'software-change',
    'identity-governance-specialist:1': 'assurance-report',
    'identity-governance-specialist:3': 'register',
    'privileged-access-management-administrator:3': 'configuration-baseline',
    'cloud-security-engineer:2': 'test-report',
    'cloud-security-engineer:4': 'register',
    'operational-technology-security-engineer:3': 'configuration-baseline',
    'operational-technology-security-engineer:4': 'control-design',
    'security-awareness-and-training-manager:2': 'test-report',
    'security-awareness-and-training-manager:4': 'analysis-report',
    'insider-threat-analyst:3': 'register',
    'purple-team-lead:2': 'test-report',
    'purple-team-lead:3': 'register',
    'purple-team-lead:4': 'test-strategy',
    'red-team-operator:3': 'analysis-report',
    'red-team-operator:4': 'test-report',
    'red-team-lead:2': 'test-strategy',
    'exploit-developer:1': 'prototype',
    'vulnerability-researcher:1': 'test-strategy',
    'adversary-emulation-engineer:3': 'test-report',
    'breach-and-attack-simulation-engineer:2': 'test-report',
    'breach-and-attack-simulation-engineer:3': 'test-report',
    'bug-bounty-programme-manager:2': 'register',
    'bug-bounty-programme-manager:4': 'analysis-report',
    'bug-bounty-triage-analyst:3': 'test-report',
    'bug-bounty-triage-analyst:4': 'register',
    'vulnerability-disclosure-coordinator:4': 'register',
    'grc-analyst:3': 'register',
    'it-risk-manager:3': 'dashboard',
    'information-security-officer-local:2': 'register',
    'information-security-officer-local:4': 'assurance-report',
    'control-owner:2': 'register',
    'control-owner:4': 'register',
    'ui-designer:2': 'configuration-baseline',
    'ui-designer:3': 'implementation-specification',
    'ui-designer:4': 'software-change',
    'interaction-designer:2': 'implementation-specification',
    'interaction-designer:3': 'requirements-specification',
    'business-attribute-profiler:1': 'register',
    'business-attribute-profiler:2': 'requirements-specification',
    'business-attribute-profiler:3': 'requirements-specification',
    'business-attribute-profiler:4': 'register',
    'conceptual-security-architect-sabsa-architect-s-view:3': 'register',
    'security-service-manager-sabsa-service-management-view:2': 'service-design',
    'security-assurance-and-measurement-architect:1': 'requirements-specification',
    'sabsa-and-togaf-integration-architect:2': 'register',
    'research-scientist:4': 'analysis-report',
    'capacity-manager:2': 'analysis-report',
    'capacity-manager:4': 'dataset',
    'ai-solutions-engineer:2': 'configuration-baseline',
    'metadata-manager:2': 'model',
    'metadata-manager:3': 'catalogue',
    'metadata-manager:4': 'analysis-report',
    'kubernetes-platform-engineer:1': 'configuration-baseline',
    'infrastructure-as-code-engineer:3': 'software-change',
    'backup-and-recovery-engineer:1': 'configuration-baseline',
    'network-engineer:3': 'model',
    'firewall-and-perimeter-engineer:1': 'configuration-baseline',
    'dns-dhcp-and-ipam-specialist:3': 'register',
    'wireless-and-rf-engineer:2': 'implementation-specification',
    'secrets-and-configuration-management-engineer:4': 'configuration-baseline',
    'privileged-access-management-administrator:2': 'configuration-baseline',
    'security-analyst-tier-3:2': 'test-strategy',
    'threat-hunter:1': 'test-strategy',
    'insider-threat-analyst:1': 'control-design',
    'ui-designer:4': 'catalogue',
    'game-developer:3': 'assurance-report',
    'codebase-reviewer:2': 'analysis-report',
    'pre-sales-solution-consultant:3': 'test-report',
    'continual-improvement-manager:1': 'register',
    'commercial-pricing-deal-finance-specialist:1': 'dataset',
    'estimation-cost-engineering-specialist:1': 'dataset',
    'chief-data-officer:4': 'register',
})

for _cid in '''
penetration-tester-web-application:2 penetration-tester-mobile:2
penetration-tester-mobile:3 penetration-tester-api:2 penetration-tester-api:3
penetration-tester-cloud:2 penetration-tester-cloud:3 penetration-tester-wireless:2
penetration-tester-wireless:3 penetration-tester-thick-client:2
penetration-tester-thick-client:3 vulnerability-researcher:2
binary-reverse-engineer:3 social-engineering-specialist:3
physical-intrusion-specialist:3 open-source-intelligence-investigator:2
hardware-and-iot-security-researcher:3
'''.split():
    OUTPUT_REFINEMENTS[_cid] = 'analysis-report'

for _cid in ('digital-forensics-examiner:2', 'malware-analyst:1',
             'security-analyst-tier-3:1', 'insider-threat-analyst:2'):
    OUTPUT_REQUIREMENTS.setdefault(_cid, []).append((
        'investigation_evidence_trace', 'array',
        'For every reported finding, identify the authorised case/scope, evidence item ID '
        'and integrity/custody record, acquisition and analysis timestamps, tool/method '
        'versions, observed artefacts, alternative explanations and confidence. '
        'Distinguish analyst inference from directly observed behaviour and do not '
        'claim acquisition, detonation or examination that was not actually performed.'))

for _cid in ('test-analyst:3', 'localisation-qa-analyst:2'):
    OUTPUT_REQUIREMENTS.setdefault(_cid, []).append((
        'reproducible_defect_records', 'array',
        'Record each defect ID, exact build/environment/locale, requirement or expected '
        'behaviour, reproduction inputs and steps, actual observation/evidence, business '
        'impact, severity rationale, accountable owner and fix/retest status. '
        'A defect report is not an investment or architecture option appraisal.'))

OUTPUT_REQUIREMENTS['network-operations-centre-analyst:2'] = [(
    'incident_ticket_records', 'array',
    'For each incident ticket, record stable ID, observed start/detection time, affected '
    'service and scope, impact/priority rationale, observed symptoms/evidence, actions '
    'and escalation history, accountable owner and current status; retain unknowns.')]
OUTPUT_REQUIREMENTS['network-operations-centre-analyst:3'] = [(
    'shift_handover_records', 'array',
    'Record shift window and outgoing/incoming accountable operators, affected service '
    'state, open incident/change IDs, actions already taken, unresolved risks, required '
    'next actions and their deadlines, supporting records and actual acknowledgement '
    'status. Do not invent acknowledgement or replace the handover with option scoring.')]
OUTPUT_REQUIREMENTS['incident-responder:4'] = [(
    'incident_timeline_and_lessons', 'object',
    'Link the incident timeline and affected assets/outcomes to observations, actual '
    'containment/recovery actions and their authority, verification evidence, competing '
    'causal hypotheses, unresolved uncertainties and lessons with named owners and '
    'follow-up verification; recommendations are distinct from recorded decisions.')]
OUTPUT_REQUIREMENTS['research-scientist:3'] = [(
    'research_reproducibility', 'object',
    'Identify hypothesis/question, protocol and deviations, data/sample provenance, '
    'methods/software versions, reproducible analysis, uncertainty/effect sizes, negative '
    'results, citations and limitations. Separate observed results from speculation and '
    'do not imply peer-review acceptance, ethics approval or execution without evidence.')]

# Primary representation and observable evidence are authored for every semantic
# family used by the catalogue. A visual projection is never the native payload
# of code, a dataset, a decision record or a procedure.
FAMILY_DELIVERY_FORMS = {
    'analysis-report': ('evidence-based-analysis-report', 'Source-linked analytical, operational or investigative report with an explicit question, method, observed findings and bounded conclusions; no fabricated decision request.', ['versioned source/period/population and reproducible method', 'observations, uncertainty, counterevidence and accountable follow-up']),
    'architecture-definition': ('architecture-description', 'Concern-driven description with a versioned model and views selected for stakeholder questions.', ['stakeholder/concern coverage', 'cross-view consistency and known gaps']),
    'adr': ('architecture-decision-record', 'Versioned decision record with context, alternatives, consequences, status and supersession.', ['comparable option evaluation', 'actual decision status and owner']),
    'hld': ('solution-design', 'Versioned solution design with component responsibilities, interfaces and measurable quality responses.', ['requirements-to-design traceability', 'independent design review']),
    'decision-paper': ('decision-paper', 'Bounded decision paper with consistent option comparison and a clear authority/decision request.', ['baseline and feasible alternatives', 'cost/benefit/uncertainty and consequences']),
    'business-case': ('investment-appraisal', 'Reconciled investment appraisal with dated financial model and accountable benefits.', ['source cash flows and calculations', 'scenario sensitivity and benefit ownership']),
    'risk-assessment': ('risk-assessment', 'Scenario-based risk assessment using explicit evaluation criteria and treatment accountability.', ['likelihood/impact rationale and uncertainty', 'current/residual exposure and treatment evidence']),
    'assurance-report': ('assurance-assessment', 'Evidence-linked assessment with criteria, population/sample, observed findings and bounded conclusion.', ['criterion-to-test-to-observation traceability', 'independent reviewer and limitations']),
    'control-design': ('control-specification', 'Control specification with objectives, trigger, actor, actions, failure paths and effectiveness measures.', ['risk/obligation traceability', 'measurable operating effectiveness checks']),
    'implementation-specification': ('implementation-specification', 'Typed implementation specification with exact target versions, interfaces and verification/recovery conditions.', ['parameter/schema constraints', 'reproducible acceptance and recovery procedure']),
    'migration-plan': ('migration-plan', 'Versioned migration inventory, mappings and sequenced waves with reconciliation and fallback criteria.', ['source/target and ownership inventory', 'integrity/reconciliation and recovery checkpoints']),
    'cutover-plan': ('cutover-runbook', 'Timed operational cutover procedure with decision points, operators, rollback and safe-state checks.', ['go/no-go evidence and latest safe reversal point', 'actual rehearsal or explicit untested status']),
    'operational-readiness-assessment': ('readiness-assessment', 'Service acceptance criteria and observed readiness evidence with receiving-operations disposition.', ['support/security/recovery/capacity evidence', 'open actions and receiving acceptance status']),
    'service-design': ('service-definition', 'Service definition with consumers, outcomes, responsibilities and measurable service commitments.', ['indicator/target/window definitions', 'support, dependency and recovery arrangements']),
    'runbook': ('operational-procedure', 'Executable-by-operator procedure with prerequisites, exact targets, expected observations and recovery branches.', ['versioned verification checkpoints', 'rehearsal environment/results or explicit untested scope']),
    'test-strategy': ('test-specification', 'Risk-based test specification with cases/techniques, expected outcomes, environments and entry/exit criteria.', ['requirement/risk-to-case coverage', 'data/sample rationale and untested risks']),
    'test-report': ('test-results', 'Observed test results against a named baseline with passed, failed, blocked and unexecuted cases.', ['expected/actual observations and execution references', 'coverage denominators and residual defects']),
    'benefits-review': ('benefits-evaluation', 'Observed benefits compared to committed baseline/counterfactual with attribution and variance analysis.', ['dated outcome measurements', 'double-counting control and corrective ownership']),
    'roadmap': ('outcome-roadmap', 'Sequenced outcomes/work packages with accountable owners, dependencies, dates and measurable milestones.', ['current/target baseline and planning assumptions', 'resource/funding constraints and decision triggers']),
    'register': ('governed-register', 'Purpose-specific structured records with stable IDs, schema, owner, status and lifecycle rules.', ['actual source-attributed records', 'uniqueness, completeness and relationship reconciliation']),
    'dashboard': ('measured-dashboard', 'Dashboard or scorecard with metric definitions, observations, source queries and interpretation.', ['units, denominators and measurement windows', 'dated values, thresholds and actionable exceptions']),
    'presentation': ('audience-presentation', 'Audience-specific presentation with a supported ask and sequenced evidence-linked argument.', ['claim/evidence links', 'accessible visuals and source navigation']),
    'dataset': ('typed-dataset-or-calculation-model', 'Typed data or calculation model with units, keys/formulas, lineage and quality constraints.', ['versioned inputs and reproducible transformations', 'reconciliation, quality measures and permitted use']),
    'catalogue': ('governed-catalogue', 'Structured entity definitions/entries with stable identifiers, metadata, ownership and relationships.', ['source reconciliation and lifecycle state', 'duplicate/reference integrity checks']),
    'document': ('professional-document', 'Purpose-specific professional document with source analysis, reasoning, conclusions and recipient actions.', ['attributable subject-specific findings and limitations', 'reviewable sources and verifiable follow-up actions']),
    'diagram': ('model-derived-view', 'Concern-specific diagram with declared notation, legend, typed relationships and source-element links.', ['endpoint/meaning/coverage checks', 'legibility and explicit projection limitations']),
    'model': ('typed-semantic-model', 'Versioned typed model with stable entities, relations, constraints, provenance and selected views.', ['metamodel/reference/cross-view checks', 'source baseline and unresolved semantic gaps']),
    'prototype': ('disposable-prototype', 'Bounded non-production prototype or executable/design experiment with predeclared question and success criteria.', ['reproducible inputs and execution/interaction', 'observed outcomes and applicability limits']),
    'configuration-baseline': ('versioned-configuration', 'Typed desired-state configuration with exact targets, versioned values and controlled secret references.', ['reproduction/drift observations', 'verification and recovery to a known baseline']),
    'strategy': ('strategy', 'Evidenced strategic choices with target outcomes, alternatives, investment assumptions and execution accountability.', ['baseline and rejected options', 'outcome measures, dependencies and review triggers']),
    'release-notes': ('release-change-record', 'Release-specific changes, compatibility impacts, known limitations and recipient upgrade/recovery actions.', ['exact release/predecessor revisions', 'source change and issue references']),
    'requirements-specification': ('requirements-specification', 'Uniquely identified verifiable requirements with rationale, priority, sources and acceptance conditions.', ['forward/backward traceability', 'conflict, interface and change-impact checks']),
    'software-change': ('versioned-source-change', 'Actual version-controlled implementation or analysis code, separate from its explanatory report.', ['exact source and dependency revision', 'observed checks and independent review']),
    'automated-tests': ('executable-test-suite', 'Executable automated checks with deterministic setup, expected assertions and reproducible invocation.', ['exact suite and tested revision', 'risk/requirement coverage and actual run results']),
    'deployment-automation': ('executable-deployment-automation', 'Versioned executable build/provision/deploy automation with controlled targets and failure/recovery gates.', ['reproducible invocation and target versions', 'observed idempotency, health and rollback checks']),
    'operational-handover': ('service-handover', 'Versioned service boundary, operational inventory and receiving responsibilities with readiness disposition.', ['actual monitoring/recovery/security/support readiness', 'recipient acceptance and unresolved obligations']),
}


def delivery_form_for(family, contract_id=None):
    """Return a fresh primary-artifact/evidence contract for an exact family.

    Args:
        family: Authored registered semantic family; never inferred from a title.
        contract_id: Optional exact role-output ID with a specialist override.
    Returns:
        Copy of the explicit representation contract with unchanged authority limits.
    Raises:
        KeyError: The family is not covered by an authored representation.
    """
    import copy
    if contract_id in DELIVERY_FORMS:
        return copy.deepcopy(DELIVERY_FORMS[contract_id])
    artifact, representation, evidence = FAMILY_DELIVERY_FORMS[family]
    return {'primary_artifact': artifact, 'representation': representation,
            'evidence': list(evidence), 'legacy_type_is_compatibility_only': True,
            'authority': 'Content guidance only; existing execution and human authority boundaries remain.'}


for _cid, _artifact, _representation, _evidence in (
    ('detection-engineer:1', 'versioned-detection-rules',
     'Actual executable detection queries/rules in version control with engine/schema versions, scope and deployment status.',
     ['exact rule revision and required data sources', 'positive/negative replay results, false-positive exclusions and coverage limits']),
    ('malware-analyst:4', 'versioned-yara-and-detection-rules',
     'Actual version-controlled YARA or equivalent detection rules with syntax/engine compatibility and controlled sample references.',
     ['rule revision, matching rationale and scope', 'observed positive/negative sample tests and limitations']),
    ('exploit-developer:1', 'controlled-proof-of-concept-code',
     'Actual non-production proof-of-concept code under the current authorised scope and controlled-access handling; descriptive prose cannot replace the code.',
     ['exact source revision, environment and reproducible bounded invocation', 'observed success/failure conditions, reliability limits and handling restrictions']),
    ('cloud-operations-engineer:3', 'drift-remediation-change-and-execution-record',
     'Actual versioned remediation configuration/script or controlled change, linked to the observed drift and execution outcome.',
     ['desired/observed baseline, exact authorised change and target scope', 'actual apply/verification/rollback outcomes or explicit not-executed status']),
    ('ui-designer:4', 'versioned-design-assets',
     'Actual exported design assets/icons in declared editable/runtime formats with versioned source and usage constraints.',
     ['asset manifest, formats, dimensions and source revision', 'render/accessibility review and licensing/usage boundaries']),
    ('infrastructure-as-code-engineer:3', 'versioned-policy-as-code',
     'Actual executable policy rules and rule-engine configuration in version control; the control-design rationale accompanies the rules.',
     ['exact rule/engine revision and enforcement scope', 'observed allow/deny and exception-path tests']),
    ('kubernetes-platform-engineer:1', 'cluster-design-and-configuration-code',
     'Actual versioned cluster configuration/deployment code with linked architecture, dependency and ownership definitions.',
     ['configuration/schema/target revisions', 'actual plan/apply/isolation/recovery checks or explicit not-executed state']),
    ('firewall-and-perimeter-engineer:1', 'versioned-firewall-rulebase-and-change-records',
     'Actual versioned rulebase or controlled configuration export with rule/change identities and authorised target scope.',
     ['exact rules, order, objects and platform version', 'change authorisation, observed validation and rollback status']),
    ('game-developer:3', 'release-build-and-certification-artifacts',
     'Actual versioned release build artefacts and platform-certification evidence, with build identity and qualification status kept distinct.',
     ['immutable build/package manifest and source provenance', 'applicable platform criteria, actual test outcomes and unresolved certification gaps']),
    ('pre-sales-solution-consultant:1', 'solution-proposal-and-demonstration-package',
     'Solution proposal with the actual authorised demonstration environment or versioned reproducible demo package where that portion is in scope.',
     ['proposal assumptions, scope and source references', 'demo/environment revision, setup/access constraints and actual observations or explicit not-executed status']),
    ('commercial-pricing-deal-finance-specialist:1', 'versioned-deal-financial-model',
     'Actual versioned financial/cash-flow model with formulas, dated rate/cost assumptions and scenario results; a funding approval paper is not the model.',
     ['reconciled revenue/cost/cash-flow inputs and calculation lineage', 'margin, timing and sensitivity results with explicit uncertainty']),
    ('estimation-cost-engineering-specialist:1', 'versioned-basis-of-estimate-model',
     'Actual work/cost breakdown and estimate model with estimation method, quantities, units, rates, assumptions and uncertainty; narrative accompanies the reproducible model.',
     ['scope/WBS-to-quantity/rate/formula traceability', 'reconciliation, calibration evidence, exclusions and estimate confidence range']),
):
    DELIVERY_FORMS[_cid] = {'primary_artifact': _artifact, 'representation': _representation,
        'evidence': _evidence, 'legacy_type_is_compatibility_only': True,
        'authority': 'Content guidance only; existing execution and human authority boundaries remain.'}

for _cid in ('detection-engineer:1', 'malware-analyst:4'):
    OUTPUT_REQUIREMENTS.setdefault(_cid, []).append((
        'detection_rule_payload_and_validation', 'object',
        'Identify and supply the actual versioned rule/query payload and engine/schema '
        'version, targeted behaviour and source-data requirements. Link observed positive '
        'and negative tests, false-positive assumptions, deployment status, ownership and '
        'review trigger; a report describing a proposed rule is not a delivered rule.'))

OUTPUT_REQUIREMENTS['game-developer:3'] = [(
    'release_build_and_certification_manifest', 'array',
    'Supply actual release-build/package references with immutable identity/hash, '
    'target platform/version, build/source provenance and handling constraints; '
    'link applicable platform certification criteria, observed results and unresolved '
    'conditions. A descriptive certification report cannot replace the requested build artefacts.')]
OUTPUT_REQUIREMENTS['continual-improvement-manager:1'] = [(
    'improvement_business_case_links', 'array',
    'For each improvement record, link its actual business-case version or explicit '
    'pending status, evidenced problem, expected measurable benefit, cost assumptions, '
    'priority, owner and funding/approval state. Maintain the register as actual records '
    'rather than replacing it with one unrelated investment paper.')]


# Interaction prototypes are native design artefacts, not executable code experiments.
for _cid in ('ux-designer:1', 'product-designer:2', 'interaction-designer:4'):
    DELIVERY_FORMS[_cid] = {
        'primary_artifact': 'interactive-design-prototype',
        'representation': 'Actual editable design/prototype assets or interaction-tool project '
                          'with linked screens, transitions and loading, empty, error states; '
                          'implementation code is required only when explicitly in scope.',
        'evidence': ['exact design revision, tool/version, access and export constraints',
                     'state/flow coverage and observed evaluation findings or explicit not-tested status'],
        'legacy_type_is_compatibility_only': True,
        'authority': 'Content guidance only; existing execution and human authority boundaries remain.'}
    OUTPUT_REQUIREMENTS.setdefault(_cid, []).extend([
        ('interaction_prototype_assets', 'object',
         'Supply the actual editable prototype/design assets or interaction-tool project '
         'with exact revision, tool/version, access/export constraints and links between '
         'screens and flows. A narrative description cannot replace requested prototype assets; '
         'do not require an executable code experiment for a noncoding design.'),
        ('interaction_state_coverage', 'array',
         'Map intended user tasks to screens, inputs, transitions and feedback. Cover loading, '
         'empty, error, permission and success states, keyboard/focus behaviour and recovery '
         'where applicable; explain exclusions and unresolved design questions.'),
        ('interaction_evaluation_evidence', 'array',
         'Link actual review/usability/accessibility evaluation observations to the exact '
         'prototype revision, task/state and remediation decision. Distinguish observed results '
         'from planned evaluation and explicit not-tested states; never invent participant findings.')])
