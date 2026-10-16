# Roles and disciplines

The current working catalogue contains **{{ JAI_ROLE_COVERAGE }}**.

| Discipline | Roles | Representative roles |
| --- | ---: | --- |
| Analysis | 11 | Business Analyst, Systems Analyst, Requirements Engineer, Process Analyst |
| Architecture | 18 | Enterprise Architect, Business Architect, Solution Architect, Application Architect |
| Commercial, Sourcing and Enablement | 20 | Bid / Proposal Manager, Commercial Pricing / Deal Finance Specialist, Estimation / Cost Engineering Specialist, Independent Commercial Assurance Reviewer |
| Data, Analytics and AI | 21 | Data Engineer, Analytics Engineer, Database Administrator, Database Reliability Engineer |
| Design and User Experience | 11 | UX Designer, UI Designer, Product Designer, UX Researcher |
| Executive and Leadership | 11 | Chief Information Officer, Chief Technology Officer, Chief Information Security Officer, Chief Data Officer |
| Governance, Risk, Compliance, Audit and Privacy | 18 | IT Governance Manager, GRC Analyst, IT Risk Manager, Information Security Officer (Local) |
| Infrastructure, Cloud and Operations | 21 | Linux Systems Administrator, Windows Systems Administrator, Cloud Engineer, Cloud Operations Engineer |
| Network and Telecommunications | 9 | Network Engineer, Network Administrator, Network Operations Centre Analyst, Wireless and RF Engineer |
| Offensive Security and Adversarial Testing | 21 | Penetration Tester (Network and Infrastructure), Penetration Tester (Web Application), Penetration Tester (Mobile), Penetration Tester (API) |
| Product, Delivery and Agile | 22 | Product Manager, Product Owner, Technical Product Manager, Scrum Master |
| Quality and Testing | 11 | Test Analyst, Test Automation Engineer, Performance Test Engineer, Test Manager |
| Research, Innovation and Specialist Engineering | 9 | Research Engineer, Innovation Lead, Technology Scout, Standards Body Representative |
| SABSA Security Architecture | 12 | Chief Security Architect (SABSA Practice Lead), Business Security Architect (SABSA Contextual Layer), Business Attribute Profiler, Conceptual Security Architect (SABSA Architect's View) |
| Security Operations and Defensive Security | 24 | Security Analyst Tier 1, Security Analyst Tier 2, Security Analyst Tier 3, SOC Manager |
| Service Management and Support | 20 | Service Desk Analyst, Desktop Support Engineer, Application Support Analyst, Incident Manager |
| Software Development and Engineering | 27 | Software Engineer, Senior Software Engineer, Staff Engineer, Backend Engineer |

## Using roles in a provider session

You can ask in plain language: "Have the Solution Architect and Security Architect evaluate this SaaS integration; show their respective deliverables, evidence and the independent reviewer." You do not instantiate all registered roles as separate processes or run a Python role catalogue command. Claude/Codex uses the installed `role-router`, knowledge skills and provider delegation (where supported) to select a relevant specialist with the appropriate author/reviewer boundary. Ask for the selected role and its limits to be shown; role choice is not itself approval or enforcement of host tool permissions.

For high-impact outcomes, explicitly start `/layered` (Claude) or `$workflow-layered` (Codex) so typed contracts and supervision are part of the engagement. Role routing alone is not a substitute for that release evidence.

## Why the role model matters

The role catalogue is not just a list of personas. Roles encode:

- mission and purpose;
- expected deliverables;
- related frameworks and methods;
- upstream and downstream relationships;
- tool or execution tier;
- out-of-scope boundaries.

This is one of the reasons the system is more useful than asking a general model to “act as an architect” or “act as a security analyst”.

## Example

If you ask for a migration strategy, a good answer may involve solution architecture, data migration, service transition, security architecture, test leadership, operational readiness and release/change governance — not only one job title.
