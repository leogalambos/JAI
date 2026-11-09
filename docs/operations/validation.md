# Review and release readiness

Review a particular output against its actual requirements, governing input
versions and relevant evidence. A previous positive result or a release label
does not establish the correctness of a changed candidate.

## Independent assessment

Set criteria before reviewing, retain located findings and keep the reviewer
independent from the author. After a repair, verify the affected boundary.
Reuse still-applicable evidence for unchanged mechanisms rather than repeating
the entire history or every workflow combination.

Evidence must describe what actually happened. A controlled example, simulated
response, rendered page, declared capability and live professional execution
are different observations. None should be presented as another.

## Professional content adjudication

The existing content evaluation tooling can prepare a blinded professional
review package for exact output contracts and complexity levels. It reuses the
registered DCS, effective output form and bundled illustrative references.
Shared materials are identified by digest rather than copied for every role.
Reviewer materials omit author identities and seeded-answer labels; keep the
coordinator key separate from reviewer delivery.

For a bounded source-checkout example:

```bash
python3 .ai/runtime/tools/content_eval.py prepare-adjudication --root . \
  --contract software-engineer:1 --complexity medium \
  --output ./review-packets/reviewer.json \
  --coordinator-output ./review-packets/coordinator.json
```

The native parent supplies the actual scoped materials and existing host
verification. Normal operators do not construct workers or runtime bootstrap
records. Select a bounded contract/domain scope for an actual review assignment;
a complete inventory is not permission to exceed the host's context limits.

Each reviewer records scores from zero to four against C1 accuracy, C2
consistency, C3 fitness, C4 completeness, C5 navigation, C6 ownership/currency,
C7 clarity/accessibility, C8 evidence/independence and C9 professional-source
applicability. Every score needs rationale and evidence; material findings need
locations. An acceptable verdict cannot coexist with deficient scores or
critical/major findings.

The `content_adjudication.assess_adjudication()` API consumes existing native
review attestations, host-owned domain-competence assignments and known author
identities. The existing host verifier establishes identity and exact material,
specification and context binding. Names or scores supplied in JSON do not
establish an independent review. Unknown author identities keep independence
pending. The native parent reuses its existing action-local snapshot when
measuring a review batch. The offline `assess-adjudication` CLI therefore
retains pending status; the native host passes its verifier through the API.

The report measures seeded critical-defect recall, reviewer agreement,
reference challenges and independently reviewed coverage by domain, output
and complexity. A pair requires distinct attributable reviewers. Reference
examples are not human-adjudicated gold, so a challenge is not automatically a
false positive; the report does not invent a false-positive rate. Synthetic
measurements, professional acceptance, human-gold classification and policy
activation remain separate. Only existing entitled human authority can grant
the latter decisions.

## Separate decisions

Authorisation to continue, acceptance of an exact output and permission to
release it are separate. Missing required current evidence blocks the affected
acceptance or release. An obsolete record unrelated to that output does not
block every operation.

Only the entitled human performs reserved decisions through the
[signing procedure](human-authority.md). A successful build or checksum grants
no acceptance or release permission.

## Publication and installation

The maintainer selects the release candidate and follows the
[version and release procedure](../reference/versioning.md). Operators use
[deployment and recovery](gen2-deployment-recovery.md) to install reviewed
software while preserving current engagement data and public trust.

Source availability, a completed package build, an installed projection and a
live provider session are distinct states. Describe the actual state instead of
claiming activation from a copy or configuration file alone.
