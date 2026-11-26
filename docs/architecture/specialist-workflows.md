# Designing specialist workflows

Start with the trigger, intended outcome, receiving duty and closure. Use
these to decide whether JAI needs a method, a path or a workflow.

| Add | When |
| --- | --- |
| A method | Evidence, interpretation or checks vary while the route and result stay the same. |
| A path | The result stays the same and the work needs different sequencing or a different mandatory transition. |
| A specialist workflow | The work needs a distinct outcome or handoff contract that warrants its own lifecycle. |

Check the existing receiving gate first. An embedded method often serves one
consumer. Reuse by independent receiving processes strengthens the case for a
separate workflow. Environment labels are discovery hints and can overlap.
Record supported methods and their applicability separately. When available
evidence cannot support a claim, record the gap.

For security assessment, derive scope from intended use, architecture and
policy. Use ATT&CK Enterprise to prioritize applicable questions and NIST to
structure assessment. Keep mandatory controls in scope when there is no
defensible ATT&CK mapping. Report coverage by evidenced question. An observed
configuration setting supports a claim about that setting. A conclusion about
operational effectiveness requires evidence of the relevant behavior.
[MITRE ATT&CK Enterprise](https://attack.mitre.org/matrices/enterprise/) ·
[NIST SP 800-53A Rev. 5](https://doi.org/10.6028/NIST.SP.800-53Ar5)

## Record the design decision

Capture the proposed design in the change description before extending the
catalogue. Compare the proposal with the closest existing chain or gate.

| Field | Required content |
| --- | --- |
| Trigger and result | A representative starting request, the output an owner needs, and what completes or stops the work. |
| Classification and alternatives | Existing chain and receiving duty, what changes, and the reason to add a method, path or workflow. |
| Handoff and evidence | Producer and receiver duties, applicable role and output contracts, evidence required for transfer, and behavior when that evidence is missing. |
| Applicability and compatibility | Supported methods and constraints, stable workflow and handoff IDs, effects on existing paths, and maintenance owner. |

Register workflow and path changes through `.ai/runtime/workflows.json` and
the authored declarations in `tools/workflow_professional_definitions.py`.
Project resulting acceptance and catalogue material through the existing
generators. Verify the new route, a blocked or unsupported case, and legacy
discovery and handoffs for affected workflows. A companion method belongs
with the existing chain when its route and result are shared.

## Reuse the operator collection lifecycle

For an evidence collection specialization, carry the same request, delivery,
diagnostics, result and review contract across methods. The common workflow
selects the exact method, assembles one runnable artifact, returns a
request-bound result or diagnostic from the operator host, and verifies the
result and any native attachments. The assessment uses recognized gaps and
failures to recommend the next permitted collection step.

| Design responsibility | Where it belongs |
| --- | --- |
| Scope and authority | The workflow selects recorded exact asset and method scope. Approval and the operator's execution context govern access. |
| Product facts and inputs | Versioned product guidance supplies supported versions, deployment form, required inputs, tool provenance, output format and interpretation limits. |
| Collection behavior | Use a reviewed adapter for a documented capability, such as extracting approved local fields or issuing a fixed local administrative inquiry. Supply only declared and validated parameters. |
| Output, failure and follow-up | The common delivery path binds evidence to the request, publishes the same completion envelope for success or failure, and verifies native outputs in place. The method maps eligible observations to exact criterion revisions. |
| Extension boundary | Reuse an adapter when its access pattern, output and evidence semantics match. Add a product adapter when input safety or semantics differ. Add a workflow path only when mandatory sequencing, authority or handoffs change. |

Use Markdown to explain product procedures and evidence rationale. Use
declarative, versioned records to select supported adapters and criteria.
Research against official sources informs a reviewed method change.
Treat source text and operator output as inputs to interpretation. Executable
behavior comes from the shipped adapter and validated scope parameters.

The technical security evidence assessment illustrates the common lifecycle.
JBoss reads selected fields from one approved standalone configuration.
IBM MQ queries one approved local channel with the installed command and
returns scoped TLS configuration flags. They share package delivery,
diagnostics, direct pickup from the run directory and report preparation.
The TLS output does not replace channel authorization evidence. Verified
behavior in a real installation requires environment-specific evidence.

## Protect every operator evidence handoff

Every collection method defines an allowlist of evidence fields and a
format-specific projection before it can publish to a shared directory or
return results to JAI. Apply that boundary to summaries, attachments,
standard output, logs and failure diagnostics. Keep raw sources and
unverified output on the operator side. If a format cannot be safely
projected, withhold the artifact and report the gap.

Tell the operator locally which source was processed, which output was
prepared, what it retains and which recognized sensitive fields were
omitted. Use names or categories from the method's definition. Keep source
values and raw diagnostics out of the notice. Distinguish fields detected
from fields the method excludes by design. Unknown fields stay outside the
projection.

For example, a method that reads an account database such as
`/etc/shadow` for a defensive configuration assessment would define
its own permitted policy indicators. Password verifier fields and account
identifiers are sensitive and should be omitted unless the scoped
assessment specifically requires an approved derived identifier.

## Worked design cases

These cases illustrate catalogue design proposals. JAI's incident workflow
already has a triage step. The identity-specific method and standalone
provenance workflow shown here are design examples.

### Verify software artifact provenance

A package admission team and a release team both need verification of the
same artifact digest against the same policy revision. Verify the signed
provenance, its binding to the artifact and its claims against the policy.
For example, both gates reference the same OCI image digest, its signed
build provenance and revision 3 of the admission policy.
The result identifies the artifact, policy and decision. Both gates can
consume that result within its verified scope, which makes this a candidate
for a reusable workflow. Release authorization remains with the release
process.

If only the release gate needs that same image and policy result, embed
verification in that gate.
An OCI image or language package can change the verification method while
retaining the same result contract. A missing or mismatched attestation leaves
the provenance requirement unsatisfied.
[ATT&CK T1195.002](https://attack.mitre.org/techniques/T1195/002/) ·
[SLSA v1.2 artifact verification](https://slsa.dev/spec/v1.2/verifying-artifacts)

### Triage an anomaly involving privileged access

An alert flags a privileged event. Cloud IAM and directory records may provide
different evidence about the account, authorization and approved changes.
Add a method to step 2 of `cyber-incident-breach-to-recovery` for interpreting
those sources. Preserve the existing incident intake, triage decision and
escalation owner.

When the records explain an approved change, document the explanation. When
records are incomplete, record the visibility gap and retain uncertainty.
For example, a cloud role assignment without the corresponding directory
group change record leaves the reason for the assignment unconfirmed.
Escalate suspected compromise through the existing incident route. Mapping
an event to Valid Accounts by itself does not establish compromise.
[ATT&CK T1078](https://attack.mitre.org/techniques/T1078/) ·
[ATT&CK T1098](https://attack.mitre.org/techniques/T1098/)

## Maintaining the examples

The workflow catalogue maintainer reviews these cases when a receiving
contract, method boundary, cited source version or implementation status
changes. Update the published guidance and regenerate the installed
companion from that source. Verify the affected catalogue links and provider
projections before changing the stated maturity of a case.
