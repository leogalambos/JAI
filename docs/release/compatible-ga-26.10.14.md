# JAI 26.10.14 — Human-Governed AI Delivery

**AI handles the work. Humans retain authority.**

JAI helps teams analyse, design and document enterprise IS/IT solutions using specialist AI roles, structured workflows and traceable evidence. Version 26.10.14 makes collaboration between AI agents and human operators more practical without giving agents unrestricted access to the host system.

## Highlights

- **Autonomous work within permissions.** Agents can analyse information, create deliverables, edit authorised project files and run permitted local tools. Routine development and quality checks do not require formal human approval.
- **Human decisions remain human (L0).** When a consequential decision requires formal approval, JAI prepares a request tied to the relevant artefact and its state. An operator signs the decision outside the agent's environment; JAI verifies the signed response before accepting it. A normal Codex or Claude tool-permission prompt is **not** an L0 decision.
- **Work can continue across sandbox boundaries.** If an agent cannot run a required tool, it can explain the limitation and provide a precise action for the operator to perform separately. The result is returned for verification and workflow continuation. This technical handoff does **not** itself require formal L0 approval.
- **Flexible document publication.** JAI produces editable Office artefacts and supports optional HTML-to-PDF rendering with WeasyPrint 70. Visual inspection of actual DOCX, PPTX or XLSX files still requires an Office-compatible renderer, which the operator may run outside the agent sandbox.
- **Traceable delivery.** The six-layer JAI model (L1–L6), SABSA/EA capabilities and Fabric records connect analysis, decisions, deliverables and supporting evidence.

## Example: completing an architecture review

JAI prepares a security architecture report and generates its deliverables. If the agent cannot render the DOCX for visual inspection inside its sandbox, it asks the operator to run a specific conversion command. JAI then checks the returned output and continues the review.

If the architecture also requires formal acceptance of residual risk, that is a **separate L0 decision** signed by the responsible human.

## What do I need to install?

Start with the normal JAI installation and a supported AI provider. Add optional tools only for the capabilities you use:

| Capability | Additional setup |
| --- | --- |
| HTML-to-PDF publication | WeasyPrint 70 |
| Visual review of DOCX, PPTX and XLSX | LibreOffice (can be run by the operator outside the sandbox) |
| Formal signed L0 decisions | Separately protected operator signing key and trusted verification configuration |

See [Installation](../getting-started/install.md) for prerequisites and [Operator walkthrough](../operations/operator-walkthrough.md) for step-by-step examples.

## Security boundaries

JAI does **not** autonomously perform privileged host or external-system mutations. Agent permissions complement, but do not replace, the actual Codex/Claude sandbox and host operating-system controls.

A locally signed L0 decision is not a substitute for enterprise identity management or independently protected audit storage.

For details, see [Security and operator workflows](../security/product-operations.md).
