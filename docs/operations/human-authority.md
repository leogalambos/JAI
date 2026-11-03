# Human authority and escalation

L0 is external human authority, not another JAI layer. Agents prepare dossiers
and requests; they cannot synthesize approvals or signer credentials.

## What the human does

In Codex CLI and Claude Code, the human inspects and executes host signing.
The agent/runtime prepares requests and verifies returned evidence inside its
existing sandbox. Neither provider approval UI nor chat is an L0 credential.

1. Inspect the verified dossier and actual object IDs.
2. A reserved authority decision produces an exact request and a host signing
   command; it does not silently sign records. A missing public enrollment is
   reported as a readiness gap without inventing a signer.
3. In a HOST console, the human reviews that request using a reviewed signer,
   external Ed25519 private key and protected public trust pin.
4. Type APPROVE or DENY with the exact request ID after inspecting the engagement,
   target, ledger snapshot, policy digest, rationale and consequences.
5. Bind the actual public receipt using the prepared package's `bind-human`
   command, then submit its exact message/proof through the supplied Fabric
   command. Binding alone does not submit. The runtime verifies signature,
   scope, expiry, replay and current state; approved effects commit atomically.
6. Inspect the resulting current basis. Signed acceptance is not proof of all lower-layer
   evidence, professional correctness or release readiness by itself.

Continuation, acceptance and release are separate decisions. Replacing inputs
creates new records and cancels affected applicability without erasing history.
A domain rejection differs from declining an operation.

## Default signing key and host script

Run the normal installer in the operator's host terminal. If
`~/.local/share/jai-operator/private.pem` is absent, it asks whether to create an
Ed25519 key with a `[Y/n]` prompt. Enter, `Y` or `yes` confirms; refusal or EOF
does not create a key. Noninteractive installation reports that confirmation is
still needed; `--dry-run` never prompts or creates material.

An existing key is reported and preserved. To deliberately replace it:

```sh
bash ./install.sh --force-genkey
```

Replacement still asks for confirmation, generates the new key before replacing
the old one and retains the old key in a uniquely named private backup. A
generation failure preserves the existing key. Creation uses a directory mode
of `0700` and private key mode `0600`; an ordinary existing-key skip does not
change its permissions. `--force` concerns managed software conflicts and
does not authorize key replacement. Keep the key and its backups outside agent
access; the host sandbox controls this boundary.

JAI supplies a signing command for the exact prepared request. Its existing
companion script uses the default key:

```sh
python3 "$HOME/.ai/it-role-house/tools/operator_actions.py" sign /private/work/request.json --workspace /private/work
```

To select another key, append `--key /host-only/other-private.pem`. Substitute
the actual request and workspace from JAI's handoff. The script displays the
request and requires `APPROVE REQUEST_ID` or `DENY REQUEST_ID`; there is no
automatic approval flag. Return only the public receipt path to JAI, never the
private key. Host helper code must be reviewed before execution.

Key creation and a signature alone do not grant authority. The public key must
already be enrolled for the exact purpose, engagement and scope. For public-key
export in the host terminal:

```sh
openssl pkey -in "$HOME/.local/share/jai-operator/private.pem" -pubout
```

After replacement, separately enroll the new public key before using it for
decisions. Existing enrollment is never silently replaced. Retain historical
public keys as appropriate for audit; new signatures must match the active key.

## Enrollment and limits

Only public material is enrolled, separately from installation. Purpose-specific
keyrings live under `~/.ai/it-role-house/trust/` as
`jai-delivery-change-trust.json`, `jai-delivery-accept-trust.json` and
`jai-delivery-release-trust.json`. Current JSON uses `schema_version: 3` and
`policy_version: governed-keyring/1`, the exact purpose, approved host authority
and routing policy IDs, and explicit key entries. Each entry records the public
PEM, its SHA-256 key ID, signer, capabilities, state, engagement/scope grants and
validity window. Exactly one key is active per purpose. Capabilities are
`lifecycle-update`, `accept` and `release` respectively; none implies another.
Only external human trust administration assigns them. There is no automatic
enrollment, legacy trust fallback or migration.
Fabric reads only protected public material. Do not return private
keys or treat environment flags, labels, same UID or keypresses alone as proof.

This is LOCAL OPERATOR ATTESTATION. If model tools can read the private key or
replace trusted runtime/pin, leave authority unavailable. Enterprise identity
and rollback-resistant audit custody are not claimed. Unsupported historical
ledgers are archive-only, never executable engagements or imported acceptance.

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
