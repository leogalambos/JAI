#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Typed human handoff data, constrained render helper and local attestations.

No daemon, shell evaluator, elevation, Git mutation or external-system executor.
Signing is an explicit host operator action with a key outside agent mounts.
"""
from __future__ import annotations
import argparse, base64, hashlib, json, os, re, shlex, stat, subprocess, sys, tempfile, time, uuid
from pathlib import Path

CRYPTO='/usr/bin/openssl'
CRYPTO_ENV={'PATH':'/usr/bin:/bin','LANG':'C.UTF-8','OPENSSL_CONF':'/dev/null'}

KINDS={'render','fabric-authorise','fabric-review','dependency-install','git-maintenance'}
ASSURANCE='LOCAL_OPERATOR_ATTESTATION'

def canonical(value):
    """Encode finite, deterministic request/receipt data."""
    return json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()

def sha(data):
    """Return an exact byte digest."""
    return hashlib.sha256(data).hexdigest()

def regular(path):
    """Read a bounded nonsymlink regular file without following the final link."""
    p=Path(path).absolute()
    if '..' in p.parts:raise ValueError('path traversal denied')
    if not hasattr(os,'O_NOFOLLOW') or os.open not in os.supports_dir_fd:raise ValueError('secure local file adapter unavailable on this OS')
    directory=os.open(p.anchor,os.O_RDONLY|os.O_DIRECTORY)
    try:
        for part in p.parts[1:-1]:
            child=os.open(part,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=directory)
            os.close(directory);directory=child
        fd=os.open(p.name,os.O_RDONLY|os.O_NOFOLLOW,dir_fd=directory)
    finally:os.close(directory)
    try:
        info=os.fstat(fd)
        if not stat.S_ISREG(info.st_mode) or info.st_nlink!=1 or info.st_size>32*1024*1024:raise ValueError('bounded single-link regular file required')
        with os.fdopen(fd,'rb',closefd=False) as stream:return stream.read()
    finally:os.close(fd)


def request(kind,purpose,source,target,parameters,permissions='normal user',risk='local output only',ttl=1800):
    """Create immutable typed handoff data; creation grants no execution authority."""
    if kind not in KINDS or not 1<=ttl<=3600:raise ValueError('unsupported operation or lifetime')
    p=Path(source).absolute();now=time.time()
    value={'schema_version':1,'request_id':str(uuid.uuid4()),'kind':kind,'purpose':purpose,
        'source':{'path':str(p),'sha256':sha(regular(p))},'target':str(target),'parameters':parameters,
        'permissions':permissions,'risk':risk,'created_at':now,'expires_at':now+ttl}
    value['request_hash']=sha(canonical(value));return value

def validate(value,live=True):
    """Validate exact schema, digest and bounded lifetime; unknown operations deny."""
    keys={'schema_version','request_id','kind','purpose','source','target','parameters','permissions','risk','created_at','expires_at','request_hash'}
    if not isinstance(value,dict) or set(value)!=keys or value['schema_version']!=1 or value['kind'] not in KINDS:raise ValueError('invalid operator request')
    if str(uuid.UUID(value['request_id']))!=value['request_id']:raise ValueError('invalid request identity')
    body=dict(value);body.pop('request_hash')
    if sha(canonical(body))!=value['request_hash']:raise ValueError('request modified')
    if not 0<value['expires_at']-value['created_at']<=3600:raise ValueError('invalid lifetime')
    if live and not value['created_at']-5<=time.time()<value['expires_at']:raise ValueError('request expired or not yet valid')
    return value

def operation_plan(agent_id,effect,target,workspace,*,sandbox='unknown',observed_error='',trust='approved-project',qa_output=None):
    """Describe an execution route, never grant permissions or execute a command.

    Args:
        agent_id: Registered actor contract; lookup is not caller authentication.
        effect: Known semantic effect, not an executable-name allowlist.
        target: Exact resource; local effects must remain inside workspace.
        workspace: Owner-authorized project root, not a sandbox configuration.
        sandbox: Observed available/blocked/provider-requested, or unknown to try.
        observed_error: Required actual evidence for a blocked/provider request.
        trust: Approved project or untrusted input; never an OS trust credential.
        qa_output: Optional explicitly native-writable diagnostic output location.
    Returns:
        Advisory route A/B/C, separate D authority requirement, or DENIED.
        Native containment remains mandatory and is not established by this data.
    """
    result={'schema_version':1,'agent_id':agent_id,'effect':effect,'execution_route':None,'formal_l0_required':False,'state':'DENIED','reason':'unknown actor/effect or unsupported mutation','host_verified':False}
    try:
        import agent_runtime
        contracts=agent_runtime.contracts();actor=contracts.get(agent_id)
    except (ImportError,OSError,ValueError,KeyError):return {**result,'reason':'required role/contract validation unavailable'}
    if actor is None or effect not in {'read','local-qa','workspace-edit','system-install','owner-git','formal-decision'}:return result
    if effect=='formal-decision':return {**result,'execution_route':'C','formal_l0_required':True,'state':'FORMAL_L0_REQUIRED','reason':'External signed exact-state decision required; never agent self-approval'}
    if effect=='system-install':return {**result,'execution_route':'C','state':'OPERATOR_ACTION_REQUIRED','reason':'System installation is an independent host operator action, not automatically L0'}
    root=Path(workspace).resolve();path=Path(target).absolute()
    if not path.resolve().is_relative_to(root) or '..' in path.parts:return {**result,'reason':'target outside authorized workspace'}
    if any(p.is_symlink() for p in [path,*path.parents] if p!=root.parent):return {**result,'reason':'ambiguous symlink target'}
    protected={'.git','.ssh','.gnupg','.codex','.claude','policy','policies','approvals','keys','secrets','.fabric','.findings'}
    if set(path.relative_to(root).parts)&{'.ssh','.gnupg','keys','secrets'} or path.name in {'.env','auth.json'}:return {**result,'reason':'credential/private resource is not an ordinary workspace target'}
    if effect in {'workspace-edit','local-qa'} and set(path.relative_to(root).parts)&protected:return {**result,'reason':'protected target; operator execution is not an override'}
    if effect=='owner-git':return {**result,'execution_route':'C','state':'OPERATOR_ACTION_REQUIRED','reason':'Owner-controlled Git; no agent metadata-write or release authorization grant'}
    operation='write' if effect=='workspace-edit' else 'validate' if effect=='local-qa' else 'read'
    allowed,reason=agent_runtime.authorize(actor,operation,'Bash' if effect=='local-qa' else None)
    if not allowed:return {**result,'reason':reason}
    if qa_output is not None:
        output=Path(qa_output).absolute()
        if any(p.is_symlink() for p in [output,*output.parents] if p!=root.parent):return {**result,'reason':'ambiguous QA output symlink'}
        scoped=output.resolve().is_relative_to(root/'build') if output.resolve().is_relative_to(root) else output.resolve().is_relative_to(Path(tempfile.gettempdir()))
        if not scoped or set(output.parts)&protected:return {**result,'reason':'QA output is not scoped build/temporary evidence'}
    if trust!='approved-project':return {**result,'execution_route':'C','state':'OPERATOR_ACTION_REQUIRED','reason':'Untrusted input needs separate containment/review; do not run active content as ordinary local QA'}
    if sandbox not in {'unknown','available','blocked','provider-requested'}:return {**result,'reason':'unknown effective sandbox status'}
    if sandbox in {'blocked','provider-requested'}:
        if not observed_error:raise ValueError('observed denial/provider requirement required; do not invent one')
        return {**result,'execution_route':'B' if sandbox=='provider-requested' else 'C','state':'PROVIDER_APPROVAL_REQUIRED' if sandbox=='provider-requested' else 'OPERATOR_ACTION_REQUIRED','reason':observed_error}
    return {**result,'execution_route':'A','state':'WITHIN_SANDBOX' if sandbox=='available' else 'TRY_EXISTING_SANDBOX','reason':'Role-authorized local operation; native sandbox decides actual capabilities, with no automatic escalation'}

def intervention_message(plan,*,purpose,reason,workdir,inputs,outputs,privileges,risks,afterwards,commands=(),attempted='None recorded',alternative='No safe alternative established',missing=''):
    """Render a complete conversation request; command data is NEVER executed.

    Args:
        plan: operation_plan result or request-derived route/authority view.
        purpose: Necessary objective, not an authority assertion.
        reason: Observed restriction or explicit host/authority requirement.
        workdir: Exact operator working directory.
        inputs: Exact inputs and hashes where available.
        outputs: Expected concrete artifacts.
        privileges: Required user/admin privileges, not an escalation grant.
        risks: Sensitive/external access, side effects and reversibility.
        afterwards: Returned evidence, verification and resumption instructions.
        commands: Reviewed argv lists for DISPLAY ONLY; never shell strings.
        attempted: Actual prior attempts or an explicit none.
        alternative: Safe alternative considered, or unknown.
        missing: Required explanation if a complete command is not ready.
    Returns:
        Inline human-facing summary independent of optional detail files.
    Raises:
        ValueError: For AUTO/denied plans, incomplete fields or unsafe formatting.
    """
    route=plan.get('execution_route');formal=plan.get('formal_l0_required') is True
    if route not in {'B','C'} or plan.get('state')=='DENIED':raise ValueError('no human request for AUTO or denied operation')
    if formal and (route!='C' or not (plan.get('effect')=='formal-decision' or plan.get('request_kind') in {'fabric-authorise','fabric-review'})):raise ValueError('formal L0 requires an explicit domain decision, not an execution permission')
    if not all(str(x).strip() for x in [purpose,reason,workdir,inputs,outputs,privileges,risks,afterwards]):raise ValueError('self-contained intervention fields required')
    rendered=[]
    for argv in commands:
        if not isinstance(argv,(list,tuple)) or not argv or any(not isinstance(x,str) or any(ord(c)<32 for c in x) for x in argv):raise ValueError('display commands require exact non-control argv data')
        rendered.append(shlex.join(argv))
    if not rendered and not missing:raise ValueError('missing executable command must be explained')
    label='D — FORMAL_L0' if formal else 'B — PROVIDER_APPROVAL' if route=='B' else 'C — OPERATOR_EXECUTION'
    lines=[f'CATEGORY: {label}',f'FORMAL L0: {"YES" if formal else "NO"}',f'EXECUTION ROUTE: {route}',f'STATE: {plan.get("state","OPERATOR_ACTION_REQUIRED")}', 'ACTOR: '+json.dumps(plan.get('agent_id','external human operator; requester identity is not authenticated by this display'))]
    for key,value in [('PURPOSE',purpose),('WHY YOU',reason),('ALREADY TRIED',attempted),('ALTERNATIVE',alternative),('WORKDIR',workdir),('INPUT',inputs),('OUTPUT',outputs),('PRIVILEGES',privileges),('RISK / EXTERNAL ACCESS / EFFECT / REVERSIBILITY',risks),('AFTERWARDS',afterwards)]:lines.append(key+': '+json.dumps(str(value),ensure_ascii=True))
    lines.extend('COMMAND: '+c for c in rendered)
    if not rendered:lines.append('COMMAND: NOT READY — '+json.dumps(missing,ensure_ascii=True))
    return '\n'.join(lines)

def request_message(req,request_path,*,reason='Explicit host route requested; no sandbox denial is inferred',workdir=None):
    """Present an existing hash-bound request without changing its signed schema.

    Args:
        req: Existing validated render/decision request, not approval evidence.
        request_path: Actual written request; detail is secondary to inline text.
        reason: Actual restriction or intentional operator route, never guessed.
        workdir: Actual project directory; defaults to caller working directory.
    Returns:
        Complete C render request or D decision request with C signing route.
        Unknown external signing paths are explicitly NOT READY, never invented.
    """
    validate(req);formal=req['kind'] in {'fabric-authorise','fabric-review'};cwd=str(Path(workdir or Path.cwd()).resolve());path=str(Path(request_path).absolute())
    commands=[] if formal else [[sys.executable,str(Path(__file__).resolve()),'render',path,'--workspace',cwd]] if req['kind']=='render' else []
    context={'source':req['source'],'target':req['target'],'parameters':req['parameters']}
    effect='exact signed ledger effect only' if formal else 'actual PDF/page evidence under '+str(Path(req['target'])/req['request_id']) if req['kind']=='render' else 'operator-returned effect/output evidence for '+req['target']
    text=intervention_message({'execution_route':'C','formal_l0_required':formal,'request_kind':req['kind'],'state':'OPERATOR_ACTION_REQUIRED'},purpose=req['purpose'],reason='Formal consequential decision requires external signed authority; provider/chat approval is not proof' if formal else reason,workdir=cwd,inputs=json.dumps(context),outputs='Public receipt/observation under '+str(Path(path).parent/'receipts'/f"{req['request_id']}.json")+'; '+effect,privileges='Normal host user with existing signing key outside agent access; no agent enrollment' if formal else req['permissions'],risks=req['risk']+'; review/freeze helper code before host execution; no provider credentials required; no external access authorized; local output creation is reversible, signed decisions remain auditable',afterwards='Return only public receipt path/hash; runtime verifies signature, expiry, policy, exact state and replay before apply; chat is never authority' if formal else 'Return exit status/output paths; JAI verifies concrete evidence and resumes only after matching the request; observations are not cryptographic execution attestations',commands=commands,missing='Select the reviewed host signer and private key in the HOST console; do not share the key with the agent' if formal else 'An exact supported host command is not available for this operation')
    return text+'\nDETAIL (secondary): '+path+'\nREQUEST ID: '+req['request_id']+'\nREQUEST SHA-256: '+req['request_hash']+'\nHELPER SHA-256 (review before host execution): '+sha(Path(__file__).read_bytes())

def trust_path():
    """Locate the protected account pin; its path alone is never authority."""
    if sys.platform!='linux':raise ValueError('local trust adapter NOT VERIFIED on this OS')
    import pwd
    try:home=Path(pwd.getpwuid(os.getuid()).pw_dir)
    except KeyError:home=Path.home()  # mapped sandbox UID; location is not authority
    return home/'.ai/jai-operator-trust.json'

def trusted_key():
    """Load root-owned public trust outside the agent workspace; no private key."""
    p=trust_path();fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
    try:
        info=os.fstat(fd)
        owner_ok=info.st_uid==0
        if not owner_ok:
            # A user namespace may expose host-root files as overflowuid. Do not
            # confuse that with agent ownership: require unmapped ownership AND
            # actual inability to write either the pin or its containing directory.
            overflow=int(Path('/proc/sys/kernel/overflowuid').read_text())
            mappings=[tuple(map(int,line.split())) for line in Path('/proc/self/uid_map').read_text().splitlines()]
            unmapped=not any(start<=info.st_uid<start+count for start,outside,count in mappings)
            owner_ok=(info.st_uid==overflow and info.st_uid!=os.getuid() and unmapped
                and not os.access(p,os.W_OK) and not os.access(p.parent,os.W_OK))
        if not stat.S_ISREG(info.st_mode) or info.st_nlink!=1 or not owner_ok or info.st_mode&0o022 or info.st_size>65536:raise ValueError('protected administrator-enrolled trust pin required')
        raw=os.read(fd,65537)
    finally:os.close(fd)
    d=json.loads(raw)
    if set(d)!={'schema_version','policy_version','key_id','public_key'} or d['schema_version']!=1 or d['policy_version']!='local-operator-attestation/1':raise ValueError('invalid trust schema')
    if sha(d['public_key'].encode())!=d['key_id']:raise ValueError('public key pin mismatch')
    der=base64.b64decode(''.join(line for line in d['public_key'].splitlines() if not line.startswith('---')),validate=True)
    if len(der)!=44 or not der.startswith(bytes.fromhex('302a300506032b6570032100')):raise ValueError('Ed25519 public key required')
    return d

def verify_receipt(req,receipt,live=True):
    """Verify an external Ed25519 receipt against protected trust and exact request."""
    validate(req,live);trust=trusted_key();body=dict(receipt);signature=body.pop('signature',None)
    if set(body)!={'schema_version','request_id','request_hash','accepted','performed','issued_at','expires_at','key_id','assurance','outputs'}:raise ValueError('invalid receipt schema')
    if (body['schema_version']!=1 or body['request_id']!=req['request_id'] or body['request_hash']!=req['request_hash'] or body['key_id']!=trust['key_id'] or body['assurance']!=ASSURANCE or type(body['accepted']) is not bool or type(body['performed']) is not bool or body['expires_at']!=req['expires_at'] or not req['created_at']<=body['issued_at']<req['expires_at']):raise ValueError('receipt binding mismatch')
    with tempfile.TemporaryDirectory(prefix='jai-public-verify-') as directory:
        p=Path(directory);(p/'key.pem').write_text(trust['public_key']);(p/'body').write_bytes(canonical(body));(p/'sig').write_bytes(base64.b64decode(signature,validate=True))
        result=subprocess.run([CRYPTO,'pkeyutl','-verify','-pubin','-inkey',str(p/'key.pem'),'-rawin','-in',str(p/'body'),'-sigfile',str(p/'sig')],capture_output=True,timeout=15,env=CRYPTO_ENV)
        if result.returncode:raise ValueError('operator signature invalid')
    return body

def response(req,accepted,performed=False,outputs=()):
    """Create an observation response; unsigned responses are never L0 credentials."""
    return {'schema_version':1,'request_id':req['request_id'],'request_hash':req['request_hash'],'accepted':accepted,'performed':performed,'issued_at':time.time(),'expires_at':req['expires_at'],'key_id':None,'assurance':'OBSERVATION_ONLY','outputs':list(outputs)}

def verify_outputs(req,receipt):
    """Verify exact returned files against the still-current source; never rerun work."""
    validate(req,live=False)
    if sha(regular(req['source']['path']))!=req['source']['sha256']:raise ValueError('source changed')
    if receipt['request_id']!=req['request_id'] or receipt['request_hash']!=req['request_hash']:raise ValueError('cross-request response')
    if not receipt['accepted']:return 'DENIED'
    if not receipt['performed']:return 'UNAVAILABLE'
    if receipt.get('qa')=='FAIL':return 'DENIED'
    if not receipt.get('outputs'):return 'UNAVAILABLE'
    output_root=(Path(req['target'])/req['request_id']).resolve()
    for item in receipt['outputs']:
        if not Path(item['path']).resolve().is_relative_to(output_root):raise ValueError('output outside approved request directory')
        if sha(regular(item['path']))!=item['sha256']:raise ValueError('returned output modified')
    return 'COMPLETED'

def perform_render(req,request_path,workspace):
    """Render one exact workspace input into a request-specific output directory."""
    validate(req);workspace=Path(workspace).resolve();source=Path(req['source']['path'])
    if req['kind']!='render' or set(req['parameters']) not in ({'backend'},{'backend','completion_target'}) or req['parameters']['backend'] not in {'libreoffice','html-auto'}:raise ValueError('only allowlisted rendering supported')
    if not source.is_relative_to(workspace) or sha(regular(source))!=req['source']['sha256']:raise ValueError('source outside workspace or stale')
    if source.suffix.lower() in {'.docx','.pptx','.xlsx'}:
        import zipfile,xml.etree.ElementTree as ET
        with zipfile.ZipFile(source) as package:
            if len(package.infolist())>10000 or sum(i.file_size for i in package.infolist())>128*1024*1024:raise ValueError('bounded Office package required')
            for member in package.namelist():
                if 'vba' in member.lower() or '..' in Path(member).parts or member.startswith('/'):raise ValueError('active/unsafe Office content denied')
                if member.endswith('.rels'):
                    for relation in ET.fromstring(package.read(member)):
                        if relation.get('TargetMode','').lower()=='external':raise ValueError('external Office relationships denied')
    parent=Path(request_path).resolve().parent
    if not parent.is_relative_to(workspace):raise ValueError('request outside workspace')
    output=parent/'outputs'/req['request_id']
    if {p.casefold() for p in output.parts}&{'.git','.ai','.agents','.codex','.claude','policy','policies','approvals','.ssh','.gnupg','keys'}:raise ValueError('protected output path denied')
    if source.suffix.lower() not in {'.html','.docx','.pptx','.xlsx','.pdf','.svg'}:raise ValueError('unsupported render input')
    output.mkdir(parents=True,exist_ok=False)
    import visual_qa
    pages=visual_qa.render_to_images(source,output,backend='libreoffice' if req['parameters']['backend']=='libreoffice' else 'auto')
    findings=[(str(p),visual_qa.image_findings(p)) for p in pages]
    receipt=response(req,True,True,[{'path':str(p.resolve()),'sha256':sha(regular(p))} for p in sorted(output.rglob('*')) if p.is_file()])
    if source.suffix.lower()=='.svg':
        import cairosvg
        selected='CairoSVG';version=cairosvg.__version__
    elif source.suffix.lower()=='.pdf':
        selected='Poppler';probe=subprocess.run(['pdftoppm','-v'],capture_output=True,text=True,timeout=15);version=(probe.stdout+probe.stderr).strip()
    elif source.suffix.lower() in {'.docx','.pptx','.xlsx'} or req['parameters']['backend']=='libreoffice':
        selected='LibreOffice';version=subprocess.run(['libreoffice','--version'],capture_output=True,text=True,timeout=15).stdout.strip()
    else:
        import importlib.util
        if importlib.util.find_spec('weasyprint'):
            import weasyprint
            selected='WeasyPrint';version=weasyprint.__version__
        else:selected='LibreOffice';version=subprocess.run(['libreoffice','--version'],capture_output=True,text=True,timeout=15).stdout.strip()
    receipt['tool_evidence']={'backend':selected,'tool_version':version,
        'profile':'fresh profile or deny-all resource fetcher; external Office relationships denied',
        'input_sha256':req['source']['sha256'],'pages':[str(p) for p in pages],'findings':findings,
        'command':['operator_actions.py','render',str(request_path),'--workspace',str(workspace)],
        'libreoffice_version':version if selected=='LibreOffice' else None}
    if any(sev=='critical' for _,items in findings for _,sev,_ in items):receipt['qa']='FAIL'
    else:receipt['qa']='PASS'
    return receipt

def sign(req,key):
    """Sign only an exact reviewed Fabric request in an interactive host console."""
    validate(req)
    if req['kind'] not in {'fabric-authorise','fabric-review'}:raise ValueError('not a Fabric authority request')
    if not sys.stdin.isatty():raise ValueError('host operator console required; stdin/flags cannot approve')
    if sha(regular(req['source']['path']))!=req['source']['sha256']:raise ValueError('stale ledger')
    print(json.dumps(req,indent=2,ensure_ascii=False));print('Assurance:',ASSURANCE,'; private key must be outside all agent-accessible mounts.')
    answer=input('Type APPROVE '+req['request_id']+' or DENY '+req['request_id']+': ')
    if answer not in {'APPROVE '+req['request_id'],'DENY '+req['request_id']}:raise ValueError('cancelled; no signature issued')
    trust=trusted_key();body=response(req,answer.startswith('APPROVE'));body.update(key_id=trust['key_id'],assurance=ASSURANCE)
    with tempfile.TemporaryDirectory(prefix='jai-operator-sign-') as directory:
        p=Path(directory);(p/'body').write_bytes(canonical(body))
        result=subprocess.run([CRYPTO,'pkeyutl','-sign','-inkey',str(Path(key).resolve()),'-rawin','-in',str(p/'body'),'-out',str(p/'sig')],capture_output=True,timeout=30,env=CRYPTO_ENV)
        if result.returncode:raise ValueError('operator signer failed')
        body['signature']=base64.b64encode((p/'sig').read_bytes()).decode()
    verify_receipt(req,body);return body

def tool_inventory():
    """Discover optional executables with bounded offline version probes.

    Returns a fresh observation, never permission or persisted configuration.
    Version success proves discovery only; each real operation must still run
    inside its effective sandbox. No tool is installed or host policy changed.
    """
    import shutil
    tools = {
        'office': ('libreoffice', 'soffice'), 'pdf_pages': ('pdftoppm',),
        'document_conversion': ('pandoc',), 'latex': ('xelatex',),
        'browser': ('chromium', 'chromium-browser', 'google-chrome', 'msedge'),
        'openssl': ('openssl',), 'codex': ('codex',), 'claude': ('claude',),
        'tests': ('pytest',), 'documentation': ('mkdocs',),
    }
    result = {}
    for capability, names in tools.items():
        executable = next((path for name in names if (path := shutil.which(name))), None)
        item = {'executable': executable, 'status': 'UNAVAILABLE',
                'functional_readiness': 'NOT_VERIFIED', 'sandbox_access': 'NOT_VERIFIED',
                'operator_alternative': 'C: independently execute on a suitably equipped host; not formal L0'}
        if executable:
            try:
                argument = {'pdf_pages':'-v', 'openssl':'version'}.get(capability,'--version')
                probe = subprocess.run([executable, argument],
                                       capture_output=True, text=True, timeout=2)
                item['status'] = 'AVAILABLE' if probe.returncode == 0 else 'UNAVAILABLE'
                item['version'] = (probe.stdout or probe.stderr).strip()[:300]
            except (OSError, subprocess.SubprocessError) as exc:
                item['reason'] = type(exc).__name__
        else:
            item['reason'] = 'Optional tool absent from this interpreter process PATH'
        result[capability] = item
    return result


def configure(previous=None):
    """Refresh current capabilities without writing settings or cached authority.

    Run doctor in a bounded child so optional renderer imports/conversion cannot
    indefinitely block installation. Automatic selection remains point-of-use;
    explicit API backend/executable arguments are preserved. No snapshot is
    persisted. Args: previous is an optional explicit earlier JSON observation,
    used only to explain changes, never to select tools or grant permission.
    Returns fresh discovery with optional availability differences. Invalid
    comparison files raise ValueError or OSError before probing.
    """
    import schema_resolver
    baseline = None
    if previous is not None:
        baseline = json.loads(regular(previous))
        if not isinstance(baseline,dict) or baseline.get('schema_version') != 1 or not isinstance(baseline.get('tools'),dict):
            raise ValueError('previous capability observation required')
    scope = schema_resolver.release_scope()
    try:
        probe = subprocess.run([sys.executable, str(Path(__file__).resolve()), 'doctor'],
                               capture_output=True, text=True, timeout=25)
        capabilities = json.loads(probe.stdout) if probe.returncode == 0 else {'status': 'UNAVAILABLE', 'reason': 'doctor failed'}
    except (OSError, ValueError, subprocess.SubprocessError):
        capabilities = {'status': 'UNAVAILABLE', 'reason': 'bounded doctor unavailable or timed out'}
    tools = tool_inventory()
    changes = None if baseline is None else {
        'newly_available': [name for name,item in tools.items() if item['status']=='AVAILABLE' and baseline['tools'].get(name,{}).get('status')!='AVAILABLE'],
        'became_unavailable': [name for name,item in tools.items() if item['status']!='AVAILABLE' and baseline['tools'].get(name,{}).get('status')=='AVAILABLE']}
    return {'schema_version': 1, 'scope': scope['scope'], 'python': sys.executable,
            'platform': sys.platform, 'configuration_changed': False,
            'selection': 'automatic at point of use; explicit backend arguments take precedence',
            'capabilities': capabilities, 'tools': tools, 'changes': changes,
            'refresh': 'Re-run configure --refresh after PATH, interpreter or tool changes; no previous readiness is trusted'}


def doctor():
    """Report prerequisites and actual rendering without asserting confinement.

    Returns:
        Existing capability strings plus renderer_dependencies version metadata.
        Only the supported optional Pyphen series is imported for a PDF probe;
        a legacy/missing dependency requests an isolated renderer environment.
        No warnings are filtered, packages installed or host settings changed.
    """
    import importlib.util,importlib.metadata,shutil
    try:trusted_key();l0='READY for receipt verification; signing separation NOT VERIFIED'
    except (OSError,ValueError):l0='OPERATOR_ACTION_REQUIRED: enroll protected public trust'
    try:
        import agent_runtime
        contracts=agent_runtime.contracts()
        base_state='READY: contract/schema and author/reviewer denial checks' if agent_runtime.authorize(contracts['artifact-author'],'write','Write')[0] and not agent_runtime.authorize(contracts['codebase-reviewer'],'write','Write')[0] else 'UNAVAILABLE'
    except (OSError,ValueError,KeyError):base_state='UNAVAILABLE: core contract validation failed'
    html_state='OPERATOR_ACTION_REQUIRED: install optional WeasyPrint or use host LibreOffice'
    dependencies={'python':sys.executable}
    try:
        dependencies['pyphen']=importlib.metadata.version('pyphen')
        release=re.match(r'^(\d+)\.(\d+)',dependencies['pyphen'])
        clean_pyphen=bool(release and tuple(map(int,release.groups()))==(0,17))
    except importlib.metadata.PackageNotFoundError:
        dependencies['pyphen']='not installed';clean_pyphen=False
    if importlib.util.find_spec('weasyprint') and not clean_pyphen:
        html_state='OPERATOR_ACTION_REQUIRED: use the optional renderer environment (WeasyPrint 70, Pyphen 0.17.x); legacy/missing Pyphen is not imported or render-tested'
    elif importlib.util.find_spec('weasyprint'):
        try:
            from office_renderer import html_pdf
            with tempfile.TemporaryDirectory(prefix='jai-doctor-') as directory:
                source=Path(directory)/'doctor.html';source.write_text('<html><h1>JAI renderer capability check</h1><p>Local deterministic rendering.</p></html>')
                result=html_pdf(source,Path(directory)/'pdf',backend='weasyprint')
                html_state='READY: actual WeasyPrint PDF conversion verified' if regular(result).startswith(b'%PDF-') else 'UNAVAILABLE'
        except (OSError,RuntimeError,ValueError):html_state='UNAVAILABLE: actual HTML conversion failed'
    office_present=bool(shutil.which('libreoffice') or shutil.which('soffice'))
    office_state='NOT VERIFIED: binary present; actual document conversion required' if office_present else 'UNAVAILABLE: optional Office renderer absent here; a host renderer may provide C'
    if office_present:
        from office_renderer import prerequisites
        if not prerequisites()['available']:
            office_state='OPERATOR_ACTION_REQUIRED: observed local IPC prerequisite denial; use C host rendering, not formal L0'
    return {'base_workflow':base_state,'html_pdf':html_state,
        'local_shell':'role-engineer contract permits local QA; actual native sandbox determines A/B/C',
        'office_visual':office_state,
        'libreoffice_binary_present':office_present,'local_l0':l0,'host_provider_confinement':'NOT VERIFIED','privileged_external_mutation':'NOT SUPPORTED','renderer_dependencies':dependencies}


def check_acceptance(path):
    """Verify completed reference-host receipts with current crypto and pixel checks.

    This consumes observations, never executes an operator action or treats a
    stored PASS label as proof. Missing per-format or accepted/declined evidence
    denies reference-host acceptance. It is not a universal host certification.
    """
    manifest=json.loads(regular(path));formats=set();decisions=set()
    import visual_qa,importlib.util
    runtime=Path(__file__).resolve().parents[1]
    spec=importlib.util.spec_from_file_location('operator_acceptance_fabric',runtime/'fabric/fabric.py');fabric=importlib.util.module_from_spec(spec);spec.loader.exec_module(fabric)
    for item in manifest['l0']:
        req=json.loads(regular(item['request']));receipt=json.loads(regular(item['receipt']));body=verify_receipt(req,receipt,live=False)
        if body['accepted']!=item['accepted']:raise ValueError('unexpected actual operator decision')
        decisions.add(body['accepted']);raw=regular(req['source']['path'])
        if body['accepted']:
            entries=[json.loads(line) for line in raw.splitlines() if line.strip()];graph=fabric.Fabric(req['parameters']['engagement'],entries)
            problems,warnings=graph.verify()
            if problems or warnings:raise ValueError('actual approved ledger invalid')
            if not any(e.get('operator_authority',{}).get('request',{}).get('request_id')==req['request_id'] for e in entries):raise ValueError('approved effect absent')
        elif sha(raw)!=req['source']['sha256']:raise ValueError('declined ledger changed')
    for item in manifest['render']:
        req=json.loads(regular(item['request']));receipt=json.loads(regular(item['receipt']))
        if verify_outputs(req,receipt)!='COMPLETED':raise ValueError('render action not completed')
        ext=Path(req['source']['path']).suffix;formats.add(ext)
        pages=[x for x in receipt['outputs'] if Path(x['path']).suffix=='.png']
        if not pages or not receipt.get('tool_evidence',{}).get('libreoffice_version'):raise ValueError('actual format pages/tool evidence required')
        for page in pages:
            if any(severity=='critical' for code,severity,message in visual_qa.image_findings(page['path'])):raise ValueError('actual rendered page failed QA')
    if decisions!={True,False} or not {'.html','.docx','.pptx','.xlsx'}<=formats:raise ValueError('incomplete positive/negative or actual-format coverage')
    return {'state':'PASS','scope':'observed Fedora operator-assisted reference acceptance','manifest_sha256':sha(regular(path)),'assurance':ASSURANCE,'host_confinement':'NOT VERIFIED'}


def main():
    """Dispatch typed operator verbs; never evaluate supplied commands."""
    p=argparse.ArgumentParser(description=__doc__);sp=p.add_subparsers(dest='cmd',required=True)
    sp.add_parser('doctor')
    a=sp.add_parser('configure',help='Refresh optional tool discovery; never install tools or alter provider settings')
    a.add_argument('--refresh',action='store_true',help='Re-detect the current environment (always performed)')
    a.add_argument('--dry-run',action='store_true',help='Preview discovery; no persistent settings are written in either mode')
    a.add_argument('--compare',help='Compare with an explicitly saved earlier configure JSON report (advisory only)')
    a=sp.add_parser('check-acceptance');a.add_argument('manifest')
    a=sp.add_parser('prepare-render');a.add_argument('source');a.add_argument('--out',required=True);a.add_argument('--backend',choices=['libreoffice','html-auto'],default='libreoffice');a.add_argument('--reason',default='Explicit host rendering requested; no in-sandbox denial has been established')
    a=sp.add_parser('decline');a.add_argument('request')
    for name in ('render','sign'):
        a=sp.add_parser(name);a.add_argument('request');a.add_argument('--workspace',required=True)
        if name=='sign':a.add_argument('--key',required=True)
    a=sp.add_parser('verify');a.add_argument('request');a.add_argument('receipt')
    a=sp.add_parser('resume-render');a.add_argument('request');a.add_argument('receipt');a.add_argument('--workspace',required=True)
    args=p.parse_args()
    if args.cmd=='doctor':print(json.dumps(doctor(),indent=2));return 0
    if args.cmd=='configure':print(json.dumps(configure(args.compare),indent=2));return 0
    if args.cmd=='check-acceptance':print(json.dumps(check_acceptance(args.manifest),indent=2));return 0
    if args.cmd=='prepare-render':
        output=Path(args.out).absolute();req=request('render','Render exact produced file and inspect its actual pages',args.source,output.parent/'outputs',{'backend':args.backend})
        output.parent.mkdir(parents=True,exist_ok=True)
        with output.open('x') as stream:json.dump(req,stream,indent=2);stream.write('\n')
        print(request_message(req,output,reason=args.reason));return 3
    req=json.loads(regular(args.request))
    if args.cmd in {'verify','resume-render'}:
        receipt=json.loads(regular(args.receipt));state=verify_outputs(req,receipt)
        if args.cmd=='resume-render' and state=='COMPLETED':
            import shutil,execution_record
            target=Path(req['parameters']['completion_target']).absolute();workspace=Path(args.workspace).resolve()
            if not target.is_relative_to(workspace) or {part.casefold() for part in target.parts}&{'.git','.ai','.agents','.codex','.claude','policy','policies','approvals','keys','.ssh'}:raise ValueError('completion target not authorized')
            pdfs=[Path(item['path']) for item in receipt['outputs'] if Path(item['path']).suffix=='.pdf']
            if len(pdfs)!=1:raise ValueError('one actual PDF output required')
            data=regular(pdfs[0])
            if not data.startswith(b'%PDF-'):raise ValueError('not a PDF')
            if target.exists() and regular(target)!=data:raise ValueError('completion target changed; explicit reconciliation required')
            record=execution_record.make(agent='operator-action-observer',provider='operator-host',input_refs=[req['source']['path']],source_hashes={req['source']['path']:req['source']['sha256']},tools_used=['typed-render'],outputs=[str(target)],render_hash=sha(data))
            if not target.exists():
                with target.open('xb') as stream:stream.write(data)
            evidence=Path(args.request).with_suffix('.execution.json')
            if not evidence.exists():evidence.write_text(json.dumps(record,indent=2)+'\n')
        print(state);return 0
    if args.cmd=='decline':
        output=Path(args.request).parent/'receipts'/f"{req['request_id']}.json";output.parent.mkdir(exist_ok=True)
        with output.open('x') as stream:json.dump(response(req,False),stream,indent=2)
        print('DENIED',output);return 0
    if not Path(req['source']['path']).is_relative_to(Path(args.workspace).resolve()):raise ValueError('input outside explicitly selected workspace')
    if args.cmd=='sign' and Path(args.key).resolve().is_relative_to(Path(args.workspace).resolve()):raise ValueError('signing key must be outside the agent workspace and mounts')
    result=perform_render(req,args.request,args.workspace) if args.cmd=='render' else sign(req,args.key)
    output=Path(args.request).resolve().parent/'receipts'/f"{req['request_id']}.json";output.parent.mkdir(exist_ok=True)
    with output.open('x') as stream:json.dump(result,stream,indent=2);stream.write('\n')
    print(output);return 0

if __name__=='__main__':
    try:raise SystemExit(main())
    except (OSError,ValueError,KeyError,subprocess.SubprocessError) as exc:print('DENIED / UNAVAILABLE:',str(exc),'— not a request to override validation or grant L0.',file=sys.stderr);raise SystemExit(2)
