# Human authority and escalation

L0 is external human authority, not another JAI layer. Agents prepare dossiers
and requests; they cannot synthesize approvals or signer credentials.

## What the human does

In Codex CLI and Claude Code, the human inspects and executes host signing.
The agent/runtime prepares requests and verifies returned evidence inside its
existing sandbox. Neither provider approval UI nor chat is an L0 credential.

1. Inspect the verified dossier and actual object IDs.
2. Authority decisions and layer-0 reviews produce an exact request and return
   OPERATOR_ACTION_REQUIRED; they do not silently sign records.
3. In a HOST console, the human reviews that request using a reviewed signer,
   external Ed25519 private key and protected public trust pin.
4. Type APPROVE or DENY with the exact request ID after inspecting the engagement,
   target, ledger snapshot, policy digest, rationale and consequences.
5. apply-operator verifies signature, scope, expiry and current state. Approved
   effects commit atomically; declining leaves the ledger intact.
6. Run Fabric verify/justify. Signed acceptance is not proof of all lower-layer
   evidence, professional correctness or release readiness by itself.

Decisions retain accept, exception, revise, reject and terminate. Exceptions
remain scoped and expiring. Revision creates a new L1 generation without erasing
history. A domain REJECT differs from declining an operation.

## Enrollment and limits

The operator generates the private key outside agent mounts and exports only
the public key. An administrator enrolls `~/.ai/jai-operator-trust.json`.
The installer creates no keys. Copy the reviewed signer outside agent writes
and use isolated Python imports, not workspace-controlled signing code.

Trust JSON uses schema_version 1, policy_version
`local-operator-attestation/1`, public_key (Ed25519 PEM) and key_id (SHA-256 of that
exact PEM). Fabric reads only protected public material. Do not return private
keys or treat environment flags, labels, same UID or keypresses alone as proof.

This is LOCAL OPERATOR ATTESTATION. If model tools can read the private key or
replace trusted runtime/pin, leave authority unavailable. Enterprise identity
and rollback-resistant audit custody are not claimed. Historical HMAC records
remain verification-compatible only.

## Providers and Git

Native tool approval, Fabric L0 and Git/release ownership remain distinct.
Provider prompts and chat cannot replace a signed Fabric receipt. Signing stays
in the human host console; hooks additionally deny agent signing and protected
record/key writes. Agent sandbox permissions never expand through a receipt.

Human Git remains legitimate outside the sandbox. JAI does not relax .git
protection or provide a privileged Git service. Signing, push and publication
require a separate explicit owner action.

See [product boundaries](../security/product-operations.md) for commands,
render/resume behavior, prerequisites and optional hardening.

## Do not confuse execution with authority

Routine role-authorized QA is A inside the effective sandbox. A native
permission request is B; unavailable host execution is C. Neither is formal
L0. Only a consequential signed Fabric decision is D. D can precede a C action,
but a screenshot, package installation or tool prompt never becomes D merely
because a human participates. Agents must explain every B/C/D request fully
inline before linking evidence; use the [operator walkthrough](operator-walkthrough.md).
