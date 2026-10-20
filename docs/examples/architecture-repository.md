# Update an enterprise architecture repository

Owner: JAI documentation maintainers. Updated: 2026-10-20.

ACME Group is replacing a shared identity service used by several
business units. Alice owns the architecture repository, Bob owns the
platform and John Doe coordinates model review. This illustrative
fiction uses a common architecture-maintenance problem and supplies no
actual model facts or retirement approval.

The outcome is a validated repository change with stable identity and a
reviewable impact view. A diagram is a projection of a model; editing an
interchange file is not a substitute for governing the canonical model.

## Prepare the project

Create a new `acme-architecture-repository/` directory with `inputs/`,
`working/` and `output/` beneath it. Keep received source files in
`inputs/` and proposed work separate from material ready for handoff.

Collect the current governed repository or authorised export, the source
change request, service ownership information, affected project
decisions and known dependency evidence. Record the scope and authority
for modifying model facts.

Use names such as `inputs/change-request.md`, `inputs/current-model/`,
`inputs/service-owners.csv` and `inputs/dependency-evidence.md`. Keep
source dates, versions and owners in `inputs/source-register.md`. A
missing relationship is not proof that no dependency exists. Keep
uncertain facts proposed and identify the person who can confirm them.

Complete the [installation](../getting-started/install.md), then start
Claude Code or Codex in `acme-architecture-repository/`. Confirm the
installed JAI commands or skills are available. All paths below are
relative to that project directory; do not run the example against the
JAI library itself.

## Run this scenario in the provider CLI

Use the repository workflow for model operations and independent
consistency review. Use layered delivery when the underlying retirement
or transition decision needs an evidence and authority path; model
validation alone cannot authorise decommissioning.

Enter these instructions in the provider conversation, not a shell. The
Claude slash command and Codex skill request the same work. They are
workflow entry points, not a claim that routing or artefact creation is
universally automatic. Inspect the actual output locations and use those
paths if the workflow reports a different location from `working/`.

### 1. Understand and validate the baseline

**Claude**

```text
/repository Inspect and validate the current model in inputs/current-model/ before proposing changes. Identify canonical repository identity and affected identity-service elements.
```

**Codex**

```text
$workflow-repository Inspect and validate the current model in inputs/current-model/ before proposing changes. Identify canonical repository identity and affected identity-service elements.
```

Inspect the validation findings and existing identifiers before any
mutation. Confirm whether the supplied material is the canonical
repository or an interchange representation. Do not create a second
element simply because a display name changed.

### 2. Prepare the bounded model update

**Claude**

```text
/repository Prepare the identity-service transition change in working/ using the validated baseline and inputs/change-request.md. Preserve stable identifiers and source traceability.
```

**Codex**

```text
$workflow-repository Prepare the identity-service transition change in working/ using the validated baseline and inputs/change-request.md. Preserve stable identifiers and source traceability.
```

Inspect changed elements and relationships, ownership and lifecycle
states. Proposed facts need a source and review status. A generated
replacement view must remain consistent with the model rather than
become an independent source of truth.

### 3. Request independent consistency review

**Claude**

```text
/repository Review the proposed repository change in working/ independently for broken references, ownership gaps, affected projects and premature retirement.
```

**Codex**

```text
$workflow-repository Review the proposed repository change in working/ independently for broken references, ownership gaps, affected projects and premature retirement.
```

Read the findings before accepting the visual result. A valid model can
still miss an affected project; compare the impact view with the
available service dependency evidence. The model author should not close
their own review findings as independently verified.

### 4. Resolve a retirement conflict

**Claude**

```text
/layered Prepare the decision on retiring the old identity service using inputs/ and the repository review findings. Preserve unresolved consumer dependencies.
```

**Codex**

```text
$workflow-layered Prepare the decision on retiring the old identity service using inputs/ and the repository review findings. Preserve unresolved consumer dependencies.
```

Suppose a business unit still depends on the old authentication
endpoint. Alice replies: "Keep the service in transition; identify a
verified migration path for that consumer." This is direction for
further work, not a retirement approval. Any protected authority record
must be made by the named human using the emitted trusted procedure.

### 5. Reconcile and exchange the reviewed model

**Claude**

```text
/repository Update only the affected model facts after the recorded decision and independent review. Validate and prepare the required Open Exchange export and views in output/.
```

**Codex**

```text
$workflow-repository Update only the affected model facts after the recorded decision and independent review. Validate and prepare the required Open Exchange export and views in output/.
```

If a new consumer is discovered, register its evidence and reopen the
impact analysis. Inspect exported identity and relationships against the
canonical model. An exchange file is an interchange artefact; it does
not silently become persistent truth.

## Finish and hand off

Hand over the validated change, independent findings, impact view,
source references and requested exchange artefact. Identify proposed or
unresolved facts explicitly. A service lifecycle label reflects a
justified decision; it must not be used to manufacture permission to
retire a live dependency.

For the wider role chain, required handoffs and blocking decisions, see
the [workflow catalogue](../reference/workflows.md). For handling an
actual authority request, follow [human
authority](../operations/human-authority.md).
