# Lifecycle deployment and blocked-engagement recovery

Use format 2 for fresh engagements. Unsupported ledgers belong in private
read-only archival storage under local retention policy. Never execute, rewrite
or import them. Reconstruct requirements from maintained public specifications
and obtain fresh evidence, independent review and new human acceptance.

## Deploy and start fresh

From the extracted release directory, the administrator runs:

```sh
sh ./install.sh --dry-run
sh ./install.sh
```

On Windows use `install.cmd`. Installation copies runtime files, not operator
trust or private keys. Start a new provider session after deployment. See
[installation](../getting-started/install.md) for prerequisites and options.
In a new project directory choose a new engagement name:

```sh
python3 ~/.ai/it-role-house/fabric/fabric.py init recovery-current --intent "Reconstruct current requirements from maintained public specifications" --owner "Project owner"
python3 ~/.ai/it-role-house/fabric/fabric.py verify recovery-current
python3 ~/.ai/it-role-house/fabric/fabric.py lifecycle-status recovery-current --scope default
```

Initialization and integrity checks do not establish completed requirements.
Continue through layered delivery with fresh contracts, public source versions
and independent evidence. Do not copy historical acceptance or permission.

## Continue an integral blocked format-2 engagement

Changed required inputs can leave an integral engagement unjustified. Prepare a
typed `update-spec.json` outside the ledger. All fields below are required;
replace illustrative identities with actual shared-engine version IDs:

```json
{
  "scope": "default",
  "reason": "Maintained public source updated",
  "proposed": [],
  "selections": [],
  "reinstatements": [],
  "verification": [],
  "invalidations": [],
  "proofs": [],
  "allowed_verification_path": "public-source-recheck"
}
```

This skeleton is intentionally incomplete: an empty update is rejected. Each
proposed item contains `manifest` and optional `locator`. A manifest has
`schema: jai.lifecycle.manifest/2`, stable `logical_id`, `kind`, `content`,
`bindings` and `members`. A selection contains `logical_id` and exact `version_id`.
Use the shared lifecycle engine for version IDs and exact-byte blob bindings;
locators do not establish content identity. Required obligations come from the
governing contract/policy, never from caller-written exclusions.

For a disposable fresh-engagement plan smoke check, this complete example adds
a maintained-public-specification reference. It does not establish evidence or
replace a production source; adapt exact manifests and selections to the actual
governed change:

```sh
python3 - <<'PY'
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path.home() / '.ai/it-role-house/tools'))
import lifecycle
value = lifecycle.manifest('public-lifecycle-spec', 'source',
    {'text': 'JAI maintained lifecycle format-2 specification'})
spec = {
    'scope': 'default', 'reason': 'Register maintained public specification',
    'proposed': [{'manifest': value}],
    'selections': [{'logical_id': value['logical_id'],
                    'version_id': lifecycle.version_id(value)}],
    'reinstatements': [], 'verification': [], 'invalidations': [], 'proofs': [],
    'allowed_verification_path': 'public-source-recheck'
}
Path('update-spec.json').write_text(json.dumps(spec, indent=2), encoding='utf-8')
PY
```

```sh
python3 ~/.ai/it-role-house/fabric/fabric.py lifecycle-plan recovery-current --spec update-spec.json --out update-plan.json
```

The pending plan grants nothing. Review exact effects, cross-scope cancellation,
predecessor head, policy and allowed verification path. An integral but unjustified
engagement may be planned; corrupted history cannot be waived. The human operator
must review and sign using the existing operator-signing procedure in an
interactive host console with an externally provisioned key outside agent mounts.
The trusted signer must explicitly have `lifecycle-update` capability.

In the human host console, replace the private-key placeholder with the actual
external key path. The source project must be inside the explicit workspace:

```sh
python3 ~/.ai/it-role-house/tools/operator_actions.py sign update-plan.json --workspace "$PWD" --key /operator/private/lifecycle-ed25519.pem
```

Signing prompts for the exact request ID and writes
`receipts/<request_id>.json` beside the plan, printing that receipt path. It does
not apply the update. Obtain the exact receipt path from the request:

```sh
UPDATE_RECEIPT="$(python3 -c 'import json; from pathlib import Path; p=Path("update-plan.json"); print(p.resolve().parent / "receipts" / (json.loads(p.read_text())["request_id"] + ".json"))')"
```

The human performs protected apply using the exact receipt returned by that step:

```sh
python3 ~/.ai/it-role-house/fabric/fabric.py lifecycle-apply --request update-plan.json --receipt "$UPDATE_RECEIPT"
python3 ~/.ai/it-role-house/fabric/fabric.py verify recovery-current
python3 ~/.ai/it-role-house/fabric/fabric.py lifecycle-status recovery-current --scope default
```

The receipt must be the actual file returned by signing, not a manufactured file.
Agents prepare plans and collect permitted observations; protected human acts
remain external. A changed policy/head/source or expired request requires a new
plan and receipt. Never edit a signed request or receipt.

Execute the allowed fresh verification path and obtain independent exact-version
review proofs. Reinstatement cannot revive cancelled conclusions or acceptance.
Use `contract --obligations FILE` for governed category/evidence/reviewer
obligations and `evidence` / `answer --bindings FILE` for exact category bindings.
Complete ordinary records use fixed, replay-checked verification rules:
byte-bound observations qualify their capture, and adjacent reviews qualify
the exact issuer contract and assessed dependency closure. Missing inputs
remain pending. See the [complete ordinary CLI example](normal-layered-workflow.md).
After a signed source replacement, recapture that same fresh pending source
with `record-input`, using its original logical ID, kind and recorded file.
Different bytes or a different locator require a new governed plan.
Cancelled versions cannot be qualified through this routine path.
`lifecycle-status` reports current manifests, predicates and gate results.
`invalidate` also only
prepares a plan: it requires `--request-out FILE`, with `--changed NODE`,
`--reason TEXT` and optional `--scope default`; it never directly cancels history.
Once the preacceptance closure passes, prepare a new exact-output acceptance
request using `review` with layer 0 and `--request-out`; the human signer must
separately have `accept` capability and apply that exact acceptance request.
Replace `frag-NNNN` with the actual current output fragment ID. These commands
are for the external human operator after fresh verification and review have
made the preacceptance closure eligible; the fresh-init smoke example alone
does not create such an output:

```sh
python3 ~/.ai/it-role-house/fabric/fabric.py review recovery-current frag-NNNN --layer 0 --state accepts --rationale "Exact current output and preacceptance closure reviewed" --reviewer "Human reviewer" --model human --request-out acceptance-plan.json
python3 ~/.ai/it-role-house/tools/operator_actions.py sign acceptance-plan.json --workspace "$PWD" --key /operator/private/acceptance-ed25519.pem
ACCEPTANCE_RECEIPT="$(python3 -c 'import json; from pathlib import Path; p=Path("acceptance-plan.json"); print(p.resolve().parent / "receipts" / (json.loads(p.read_text())["request_id"] + ".json"))')"
python3 ~/.ai/it-role-house/fabric/fabric.py apply-operator acceptance-plan.json "$ACCEPTANCE_RECEIPT"
python3 ~/.ai/it-role-house/fabric/fabric.py release recovery-current frag-NNNN
```

Finally use `release` for the exact output to inspect eligibility. It does not
perform publication or release.

Deployment and synthetic signer tests are independent evidence obligations;
these instructions do not claim production deployment or human acceptance.
See [the lifecycle decision](../reference/lifecycle-format-2.md) for governing rules.
