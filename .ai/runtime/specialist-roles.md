# Designing specialist roles

Start with the requested deliverable, the accountable professional duty and
the limits of the assignment. Identify the existing base role and read its
scope and output contract before deciding how to represent a specialization.

| Add | When |
| --- | --- |
| Named knowledge for an existing role | Product, platform or practice changes how the role works, while its scope, deliverable and accountability stay the same. |
| A registered specialist extending a base role | A recurring assignment needs a distinctly bounded professional remit and repeatable product-specific methods or evidence. The base role's deliverable and review boundary still apply. |
| A separate professional role | The assignment owns a materially different deliverable or accountability that an existing role cannot express. Check the existing catalogue and separation of duties before adding it. |

Record the retained base role and contract, observable difference in work,
applicability, required evidence and maintenance owner. Where product version
or deployment changes applicability, capture that scope in the assignment.
Environment names can direct discovery. Confirm the actual remit before
choosing the role. Keep cross-product guidance on the applicable base role
when the same professional competence and output suffice.

A registered specialization inherits its professional contract and permitted
work mode. For a governed workflow step, use an existing compatibility
profile only where the workflow supports it and the reviewed enrollment
covers the exact endpoint, variant and scope. The receiving duty and
independent review remain in force. Other steps use their registered role
binding. Professional selection and installation convey no approval or
additional tool access.

## Record the design decision

Record a proposed specialization against the canonical base role before
changing catalogue sources. Include these fields in the change description.

| Field | Required content |
| --- | --- |
| Assignment and alternatives | Representative request, expected deliverable, base role, and why named knowledge, a registered specialization or a separate role fits. |
| Inherited contract | Role identifier, output contract, retained work mode, and who independently reviews or receives the result. |
| Applicability and evidence | Supported product, version and deployment where relevant, what the specialist does differently, and an explicit condition under which the base role or another role should be selected. |
| Catalogue change | Stable identifier and aliases where applicable, authored source, affected projections and maintenance owner. |

Author registered role specializations in the role library under
`.ai/role-library/roles/`. Put reusable product and practice knowledge under
`.ai/role-library/knowledge/` or the existing maintained source for the
applicable role. Check role composition and provider projections, and use two
representative requests to verify selection inside and outside the
specialization. If an eligible governed handoff will use the role, verify its
compatibility separately from basic catalogue discovery.

## Worked examples

### Terraform delivery uses named knowledge

A team requests versioned Terraform modules and evidence for state locking.
Select **Infrastructure as Code Engineer** and its Terraform reference.
The expected work remains reproducible infrastructure code and state
evidence. A different state backend changes implementation guidance and
evidence collection. It does not create a new professional remit.
A request to approve change promotion follows the existing change authority.

### QRadar integration uses a registered specialist

A team needs to design and validate log-source integration for an applicable
on-premises IBM QRadar SIEM deployment. Select **IBM QRadar SIEM Integration
Specialist** (`qradar-siem-specialist`), which extends **Security Engineer**.
The recurring scoped assignment adds collection, parser and normalization
evidence to the inherited security tooling integration deliverable. Confirm
the deployment and scope before applying the product-specific practice. The
maintained method covers on-premises QRadar SIEM 7.6.0. Verify the exact fix
level, deployment support and source parser (DSM) compatibility.

If the request is to triage a live incident from those events, route to the
existing incident duties. The fact that events are stored in QRadar does not
change who owns incident triage. Filling a governed integration handoff
requires the applicable registered role or an eligible enrolled mapping.

### Distinct deliverables retain distinct roles

In a Microsoft Entra ID engagement, an identity architect can own workforce
authentication and federation design. Implementing the approved configuration
and independently reviewing the evidence remain separately scoped assignments.
A shared product label is sufficient context for discovery. Check the design,
implementation and review outputs separately before choosing the roles.

## Maintaining the guidance

The role catalogue maintainer reviews these examples when the professional
contract, product applicability, review boundary or compatibility policy
changes. Update the public guide and regenerate its installed copy. Verify
that the role catalogue and provider routing describe the same scope and
state accurately which capabilities are registered or governed.
