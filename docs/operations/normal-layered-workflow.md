# Complete an ordinary layered workflow

The example below checks exact bytes of a maintained public specification
through all six layers. It records real source bytes and a reproducible
capture. It makes no claim about the specification's semantic correctness.
Replace the public source with the actual input your requirement concerns.
Never use private inputs in a public example or released output.

Initial input registration occupies an empty logical slot. Changing an
existing governing selection still requires a signed lifecycle plan.
Routine observation and adjacent review qualification grant no human
acceptance, permission or authority continuation.
Replay derives each actual graph edge's exact causal dependency rule and
rejects missing or substituted reliance. A routine capture cannot replace
an existing version's recorded locator; relocation needs governed effects.
Edges touching L0 require exact signed effects, including edges to an
already signed authority decision; its authority cannot be reused by a
new unsigned edge.

Run from a deployed project with a fresh engagement name. The local script
uses ordinary CLI commands; it does not write ledger files. Keep the work
directory and its observation files until retention permits their removal.

```sh
mkdir -p build/normal-layered
python3 - <<'PY'
import hashlib
import json
from pathlib import Path
import subprocess
import sys

runtime = Path.home() / '.ai/it-role-house'
program = runtime / 'fabric/fabric.py'
work = Path('build/normal-layered').resolve()
source = Path('docs/reference/lifecycle-format-2.md').resolve()
eng = 'normal-public-spec'

def run(*args):
    result = subprocess.run(
        [sys.executable, str(program), *args],
        check=True, text=True, capture_output=True)
    return result.stdout

def write(name, value):
    path = work / name
    path.write_text(json.dumps(value), encoding='utf-8')
    return str(path)

run('init', eng, '--intent', 'Trace exact public source bytes',
    '--owner', 'Project owner')
source_id = run('record-input', eng, '--logical-id', 'public-spec',
                '--kind', 'source', '--file', str(source)).strip()
status = json.loads(run('lifecycle-status', eng, '--scope', 'default'))
policy_id = next(row['version_id'] for row in status
                 if row['logical_id'] == 'lifecycle-policy')
obligations = {
    'categories': {
        key: {'minimum': 1, 'allow_exclusion': False}
        for key in ('source', 'contract', 'policy')},
    'evidence_roles': ['evidence'], 'review_roles': ['reviewer']}
fields = dict(
    what='Establish the exact public source capture',
    why='Demonstrate traceable ordinary completion',
    who='Assigned layer role', where='Local project workspace',
    when='Before human acceptance', how='Check exact source digest',
    evidence='Captured SHA-256 observation of source bytes',
    escalate_if='Source or capture cannot be checked',
    sanitise='Maintained public source only')
run('req', eng, '--layer', '1', '--from', 'intent-0001',
    '--label', 'derives', '--text', fields['what'])
flags = [item for key, value in fields.items()
         for item in ('--' + key.replace('_', '-'), value)]
run('contract', eng, '--from', 'req-0001', *flags,
    '--obligations', write('obligations.json', obligations))

def binding(contract):
    rows = json.loads(run('lifecycle-status', eng, '--scope', 'default'))
    contract_id = next(row['version_id'] for row in rows
                       if row['logical_id'] == contract)
    return {key: {'refs': [value]} for key, value in {
        'source': source_id, 'policy': policy_id,
        'contract': contract_id}.items()}

def ingest(contract, **values):
    packet = json.loads(run('context-packet', eng, contract))
    payload = {'context_digest': packet['context_digest'], **values}
    run('ingest', eng, '--contract', contract,
        write('reply.json', payload))

for index in range(1, 5):
    ingest(f'ctr-{index:04}', derived_requirements=[{
        'key': 'child', 'text': fields['what'],
        'contract': {**fields, 'obligations': obligations}}])
capture = work / 'source-capture.txt'
capture.write_text(hashlib.sha256(source.read_bytes()).hexdigest()
                   + '\n', encoding='utf-8')
ingest('ctr-0005', fragments=[{
    'key': 'capture', 'text': 'The exact source digest is captured',
    'bindings': binding('ctr-0005')}], evidence=[{
    'supports': ['capture'], 'source': 'SHA-256 capture of source bytes',
    'confidence': 'deterministic', 'file': str(capture),
    'bindings': binding('ctr-0005')}])
child = 'frag-0001'
for layer in range(5, 0, -1):
    review = {'reviews': [{
        'fragment': child, 'state': 'accepts',
        'rationale': 'Checked exact source, capture and dependency closure'}]}
    run('ingest-reviews', eng, '--layer', str(layer),
        '--reviewer', f'Assigned layer {layer} reviewer',
        '--model', 'record-actual-model', write('review.json', review))
    if layer > 1:
        parent = f'ctr-{layer - 1:04}'
        ingest(parent, fragments=[{
            'key': 'upward', 'text': 'Reviewed child establishes capture',
            'supported_by': [child], 'bindings': binding(parent)}])
        child = f'frag-{7 - layer:04}'
run('answer', eng, '--requirement', 'req-0001',
    '--text', 'The public source capture is established',
    '--supported-by', child,
    '--bindings', write('bindings.json', binding('ctr-0001')))
print(run('status', eng))
print(run('verify', eng))
PY
```

The review loop is an executable interface example. In real delivery the
assigned independent reviewer must assess each packet and supply its actual
verdict, rationale and model. A display name supplies attribution; the
qualifying role comes from the exact contract issuer, adjacent layer and
maintained review profile. Do not accept a packet solely to advance a loop.

The resulting L1 output is `frag-0006`. Preacceptance eligibility does not
grant release. Prepare its exact L0 review request, then have the human sign
and apply it using the [external signing procedure](lifecycle-recovery.md).
`release` reports eligibility and performs no external publication.

After a source change, use a governed selection plan. Old dependent
conclusions, reviews and acceptance remain cancelled. Capture fresh bytes,
produce new fragments through the same contracts where still applicable,
obtain independent reviews, answer again and obtain new exact acceptance.
See [source replacement and recovery](lifecycle-recovery.md).

For the example engagement, prepare the exact source replacement after the
approved edit to the public specification:

```sh
python3 - <<'PY'
import json
from pathlib import Path
import sys

runtime = Path.home() / '.ai/it-role-house'
sys.path.insert(0, str(runtime / 'tools'))
import lifecycle

source = Path('docs/reference/lifecycle-format-2.md').resolve()
value = lifecycle.manifest('public-spec', 'source', {
    'blob': lifecycle.blob(source.read_bytes()),
    'capture_profile': 'jai.byte-observation/1'})
spec = {
    'scope': 'default', 'reason': 'Maintained public source changed',
    'proposed': [{'manifest': value, 'locator': str(source)}],
    'selections': [{'logical_id': 'public-spec',
                    'version_id': lifecycle.version_id(value)}],
    'reinstatements': [], 'verification': [],
    'invalidations': [], 'proofs': [],
    'allowed_verification_path': 'jai.byte-observation/1'}
Path('build/normal-layered/update-spec.json').write_text(
    json.dumps(spec), encoding='utf-8')
PY
python3 ~/.ai/it-role-house/fabric/fabric.py lifecycle-plan \
  normal-public-spec --spec build/normal-layered/update-spec.json \
  --out build/normal-layered/update-plan.json
```

Have the human review, sign and apply `update-plan.json` through the
[source-update signing procedure](lifecycle-recovery.md). After that actual
apply, the following script recaptures the same pending current source and
produces fresh conclusions. Use it only while the existing contracts remain
applicable. Independent workers must supply the actual review verdicts.

```sh
python3 - <<'PY'
import hashlib
import json
from pathlib import Path
import subprocess
import sys

program = Path.home() / '.ai/it-role-house/fabric/fabric.py'
eng = 'normal-public-spec'
work = Path('build/normal-layered').resolve()
source = Path('docs/reference/lifecycle-format-2.md').resolve()

def run(*args):
    return subprocess.run(
        [sys.executable, str(program), *args],
        check=True, text=True, capture_output=True).stdout

def write(name, value):
    path = work / name
    path.write_text(json.dumps(value), encoding='utf-8')
    return str(path)

source_id = run('record-input', eng, '--logical-id', 'public-spec',
                '--kind', 'source', '--file', str(source)).strip()
rows = json.loads(run('lifecycle-status', eng, '--scope', 'default'))
current = {row['logical_id']: row['version_id'] for row in rows}

def binding(contract):
    return {key: {'refs': [value]} for key, value in {
        'source': source_id, 'contract': current[contract],
        'policy': current['lifecycle-policy']}.items()}

def ingest(contract, **values):
    packet = json.loads(run('context-packet', eng, contract))
    reply = {'context_digest': packet['context_digest'], **values}
    run('ingest', eng, '--contract', contract,
        write('fresh-reply.json', reply))

capture = work / 'fresh-source-capture.txt'
capture.write_text(hashlib.sha256(source.read_bytes()).hexdigest()
                   + '\n', encoding='utf-8')
ingest('ctr-0005', fragments=[{
    'key': 'fresh', 'text': 'The changed source digest is captured',
    'bindings': binding('ctr-0005')}], evidence=[{
    'supports': ['fresh'], 'source': 'Fresh exact source digest',
    'confidence': 'deterministic', 'file': str(capture),
    'bindings': binding('ctr-0005')}])
child = 'frag-0007'
for layer in range(5, 0, -1):
    run('review', eng, child, '--layer', str(layer),
        '--state', 'accepts', '--reviewer', f'Layer {layer} reviewer',
        '--model', 'record-actual-model', '--rationale',
        'Checked fresh source, capture and exact dependency closure')
    if layer > 1:
        parent = f'ctr-{layer - 1:04}'
        ingest(parent, fragments=[{
            'key': 'upward', 'text': 'Fresh reviewed child establishes capture',
            'supported_by': [child], 'bindings': binding(parent)}])
        child = f'frag-{13 - layer:04}'
run('answer', eng, '--requirement', 'req-0001',
    '--text', 'The changed public source capture is established',
    '--supported-by', child,
    '--bindings', write('fresh-bindings.json', binding('ctr-0001')))
print(run('status', eng))
print(run('verify', eng))
PY
```

Prepare new human acceptance for `frag-0012`, sign and apply that exact
request, then run `release` for `frag-0012`. The earlier acceptance cannot
authorize this changed output. These identifiers assume only the commands
shown above ran; inspect actual command output if the engagement has other
work. Do not increase the shared step budget to fit an example.
