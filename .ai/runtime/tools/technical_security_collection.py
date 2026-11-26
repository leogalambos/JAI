# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Prepare bounded requests and collect selected fields from supplied local copies."""

import argparse
from datetime import datetime, timedelta, timezone
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import sys
import tempfile
from urllib.parse import urlsplit
import xml.etree.ElementTree as ET
import zipfile

import technical_security_evidence
from technical_security_evidence import load_method_manifest

_SCOPE = ('product', 'edition', 'version', 'deployment')
_JBOSS = ('jboss-eap', 'eap', '7.4.0', 'standalone')
_MQ = ('ibm-mq', 'lts', '9.4.0.0', 'distributed-queue-manager')
_JBOSS_COLLECTOR = 'jboss-standalone-management-audit'
_JBOSS_RUNTIME_COLLECTOR = 'jboss-local-identity-role-inquiry'
_JBOSS_DIRECTORY_COLLECTOR = 'jboss-reviewed-directory-membership-export'
_RUNTIME_CRITERION = 'jboss-management-effective-role-policy'
_RUNTIME_CRITERION_REVISION = '2'
_MQ_COLLECTOR = 'ibm-mq-local-channel-tls'
_MQ_CRITERION = 'ibm-mq-channel-client-certificate-required'
_MQ_FIELDS = ('approved_mqsc_path', 'approved_mqsc_sha256', 'queue_manager', 'channel')

_MAX_INPUT_BYTES = 4 * 1024 * 1024
_AUDIT_FIELDS = ('enabled', 'log-boot', 'log-read-only')
_AUDIT_CRITERION = 'jboss-management-audit-explicitly-enabled'
_ROLE_CRITERION = 'jboss-management-direct-role-inclusion'
_AUDIT_FORMAT = 'configuration-observation'
_AUDIT_CRITERION_REVISION = '1'
_AUDIT_FORMAT_REVISION = '1'
_OPERATOR_ENTRY = (
    'from technical_security_collection import run_operator_package\n'
    'raise SystemExit(run_operator_package())\n'
)


_FAILURE_GUIDANCE = {
    'source-in-handoff': (
        'prepare-collection',
        'Remove the raw source from shared access, review its exposure, and reissue the package with an operator-only source path.',
    ),
    'private-workspace-unavailable': (
        'prepare-collection',
        'Set the handoff path to a dedicated directory outside the private temporary workspace.',
    ),
    'publication-contract-violation': (
        'publish-result',
        'Correct the collector output to match the approved handoff contract, then issue a new package for a fresh result path.',
    ),
    'source-missing': ('read-source', 'Confirm the approved configuration path and inventory revision.'),
    'source-permission-denied': ('read-source', 'Ask the platform owner to verify read access under the approved account.'),
    'source-unreadable': ('read-source', 'Ask the platform owner to confirm the source is a readable local file.'),
    'source-invalid': ('validate-source', 'Confirm the approved file is a supported standalone configuration within input limits.'),
    'mq-binary-mismatch': ('verify-tool', 'Confirm the installed MQ binary against the approved inventory.'),
    'mq-inquiry-failed': ('run-inquiry', 'Verify the named local queue manager and inquiry permissions.'),
    'mq-inquiry-timeout': ('run-inquiry', 'Ask the platform owner to verify queue manager readiness.'),
    'form-incomplete': ('operator-input', 'Complete the scoped form with the accountable platform team.'),
    'jboss-cli-mismatch': ('verify-tool', 'Confirm the local management CLI against the approved installation record.'),
    'jboss-inquiry-failed': ('run-inquiry', 'Verify that the approved local management identity can run the inquiry.'),
    'jboss-identity-mismatch': ('validate-source', 'Confirm the approved account and realm of the current local session.'),
    'mq-output-invalid': ('validate-source', 'Confirm the named server-connection channel and supported MQ version.'),
}
_DIAGNOSTIC_SCHEMA = 'jai.technical-security-collection-diagnostic/v1'
_FORM_SCHEMA = 'jai.technical-security-operator-response/v1'
_FORM_CRITERIA = {'application-server-management-account-scope', 'messaging-channel-authorization'}
_FORM_AVAILABILITY = {'available', 'unavailable', 'unknown'}



def _approved_path(asset, field):
    value = asset.get(field)
    if value is None:
        return None
    if (not isinstance(value, str) or not value.startswith('/') or value.startswith('//')
            or '\x00' in value or '\\' in value or '..' in PurePosixPath(value).parts):
        raise ValueError(f'Expected an absolute local POSIX configuration path or result path for {field}')
    return value


def _mq_scope(asset):
    if not any(key in asset for key in _MQ_FIELDS):
        return None
    tool = _approved_path(asset, 'approved_mqsc_path')
    fingerprint = asset.get('approved_mqsc_sha256')
    manager, channel = asset.get('queue_manager'), asset.get('channel')
    if (tool is None or PurePosixPath(tool).name != 'runmqsc' or not isinstance(fingerprint, str)
            or not re.fullmatch(r'[0-9a-f]{64}', fingerprint)
            or not isinstance(manager, str) or not re.fullmatch(r'[A-Z0-9][A-Z0-9._%/-]{0,47}', manager)
            or not isinstance(channel, str) or not re.fullmatch(r'[A-Z0-9][A-Z0-9._%-]{0,19}', channel)):
        raise ValueError('IBM MQ needs an approved binary path and digest, manager and exact channel')
    return {key: asset[key] for key in _MQ_FIELDS}


def _jboss_role_scope(asset):
    value = asset.get('jboss_role_mapping')
    if value is None:
        return None
    if (not isinstance(value, dict) or set(value) != {'id', 'account', 'role'}
            or any(not isinstance(text, str) or not re.fullmatch(r'[A-Za-z0-9$_.@-]{1,128}', text)
                   for text in value.values())):
        raise ValueError('Expected one exact approved JBoss account and role mapping')
    return value


def _jboss_runtime_scope(asset):
    value = asset.get('jboss_runtime_identity')
    if value is None:
        return None
    names = ('identity_scope', 'username', 'realm', 'policy_revision')
    if not isinstance(value, dict) or set(value) != {*names, 'cli_path', 'cli_sha256', 'port', 'expected_roles'}:
        raise ValueError('Expected an exact JBoss runtime identity and policy scope')
    tool = _approved_path(value, 'cli_path')
    digest = value['cli_sha256']
    roles = value['expected_roles']
    if (tool is None or PurePosixPath(tool).name != 'jboss-cli.sh'
            or not isinstance(digest, str) or not re.fullmatch(r'[0-9a-f]{64}', digest)
            or not all(isinstance(value[key], str) and re.fullmatch(r'[A-Za-z0-9$_.@-]{1,128}', value[key])
                       for key in names)
            or type(value['port']) is not int or not 1 <= value['port'] <= 65535
            or not isinstance(roles, list) or len(roles) > 128
            or any(not isinstance(role, str) or not re.fullmatch(r'[A-Za-z0-9_.-]{1,128}', role) for role in roles)
            or len(set(roles)) != len(roles)):
        raise ValueError('Invalid approved JBoss runtime identity parameters')
    return value


def _jboss_directory_scope(asset):
    value = asset.get('jboss_directory_membership')
    if value is None:
        return None
    fields = ('identity_scope', 'policy_revision', 'group_dn', 'member_dn', 'source')
    if (not isinstance(value, dict) or set(value) != {*fields, 'ldif_path'}
            or any(not isinstance(value[key], str) or not value[key].isascii()
                   or not 1 <= len(value[key]) <= 512 or not value[key].isprintable()
                   for key in fields)
            or not _approved_path(value, 'ldif_path')):
        raise ValueError('Expected one exact approved directory membership source')
    return value


def prepare_collection(manifest, asset):
    """Return a digest-bound collection request for one attributable asset.

    Args:
        manifest: Validated method manifest from the assessment workflow.
        asset: Inventory row with product scope, source, identifier and revision.
    Returns:
        A request with applicable assessment questions and available collector.
    Raises:
        ValueError: Asset identifier, inventory source or revision is absent.
    """
    assessment = manifest.assess([asset], [], [])
    if not all(isinstance(asset.get(key), str) and asset[key].strip()
               for key in ('id', 'source', 'revision')):
        raise ValueError('Collection requires an identified asset and inventory revision')
    method = assessment['asset_methods'][asset['id']]
    scope = {key: asset.get(key) for key in _SCOPE}
    product = scope['product']
    if isinstance(product, str):
        scope['product'] = manifest.aliases.get(product.casefold(), product)
    jboss = method == 'application-server' and tuple(scope.values()) == _JBOSS
    role_mapping = _jboss_role_scope(asset) if jboss else None
    runtime = _jboss_runtime_scope(asset) if jboss else None
    if runtime is not None and _RUNTIME_CRITERION not in manifest.methods[method]['criteria']:
        raise ValueError('The installed method does not authorize this runtime evidence route')
    directory = _jboss_directory_scope(asset) if jboss else None
    if directory is not None and _RUNTIME_CRITERION not in manifest.methods[method]['criteria']:
        raise ValueError('The installed method does not support directory evidence')
    if sum(item is not None for item in (runtime, role_mapping, directory)) > 1:
        raise ValueError('Choose one exact JBoss collection scope')
    jboss_criterion = _AUDIT_CRITERION
    if runtime is not None or directory is not None:
        jboss_criterion = _RUNTIME_CRITERION
    elif role_mapping is not None:
        jboss_criterion = _ROLE_CRITERION
    collector = _JBOSS_COLLECTOR
    if runtime is not None:
        collector = _JBOSS_RUNTIME_COLLECTOR
    if directory is not None:
        collector = _JBOSS_DIRECTORY_COLLECTOR
    mq = _mq_scope(asset) if method == 'messaging' and tuple(scope.values()) == _MQ else None
    criteria = [item['criterion'] for item in assessment['missing_mandatory_questions']]
    if jboss and jboss_criterion in manifest.methods[method]['criteria']:
        criteria.append(jboss_criterion)
    if mq is not None and _MQ_CRITERION in manifest.methods[method]['criteria']:
        criteria.append(_MQ_CRITERION)
    result_path = _approved_path(asset, 'approved_result_path') if method is not None else None
    if result_path is not None and PurePosixPath(result_path) == PurePosixPath(
            asset.get('approved_configuration_path') or ''):
        raise ValueError('The result path must differ from the configuration path')
    return {
        **({'jboss_directory_membership': directory} if directory is not None else {}),
        **({'jboss_runtime_identity': runtime} if runtime is not None else {}),
        **({'jboss_role_mapping': role_mapping} if role_mapping is not None else {}),
        **({'mq_scope': mq} if mq is not None else {}),
        **({'approved_result_path': result_path} if result_path is not None else {}),
        'asset': asset['id'],
        'asset_revision': asset['revision'],
        'inventory_source': asset['source'],
        'receiving_duty': 'platform-owner',
        'manifest_sha256': manifest.digest,
        'scope': scope,
        'method': method,
        'collector': collector if jboss else _MQ_COLLECTOR if mq is not None else None,
        'approved_configuration_path': _approved_path(asset, 'approved_configuration_path') if jboss else None,
        'source': ('Approved local directory snapshot' if directory is not None else
                   'Approved local JBoss management identity' if runtime is not None else
                   'Authorized local copy of the standalone server configuration' if jboss else None),
        'pending_conditions': ['Missing inventory provenance', 'Unsupported scope or source format',
                               'Unresolved setting or insufficient evidence for the criterion'],
        'operator_actions': (
            ['Run the supplied package against the pinned directory snapshot.']
            if directory is not None else
            ['Run under the approved local identity for the fixed local management inquiry.']
            if runtime is not None else
            ['Supply the approved local copy of the standalone XML configuration.',
             'Run the collector and retain the generated configuration summary.',
             'Supply separately reviewed management-account role evidence. The audit setting summary does not establish account assignments.']
            if jboss else
            ['Run the supplied package under the approved local MQ inquiry identity.']
            if mq is not None else
            ['Request approved local records from the accountable platform duty. This scope has no packaged collector.']
        ),
        'questions': [
            {'criterion': criterion,
             'question': manifest.criteria[criterion]['question'],
             'required_evidence': manifest.criteria[criterion]['formats'],
             'evidence_request': manifest.criteria[criterion].get('evidence_request')}
            for criterion in criteria
        ],
    }


def _local_path(location):
    path = Path(location)
    if str(path).startswith(('//', '\\\\')):
        raise ValueError('Use a local copy rather than a network share')
    return path


def _open_local(location):
    path = _local_path(location)
    if not stat.S_ISREG(path.lstat().st_mode):
        raise ValueError('Use an explicit regular local file')
    flags = os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0) | getattr(os, 'O_NONBLOCK', 0) | getattr(os, 'O_BINARY', 0)
    source = os.fdopen(os.open(path, flags), 'rb')
    if not stat.S_ISREG(os.fstat(source.fileno()).st_mode):
        source.close()
        raise ValueError('Use an explicit regular local file')
    return source


def _read_local(location):
    with _open_local(location) as source:
        raw = source.read(_MAX_INPUT_BYTES + 1)
    if len(raw) > _MAX_INPUT_BYTES:
        raise ValueError('Input exceeds the collection size limit')
    return raw


def _verify_native_outputs(summary, directory, result_name):
    entries = summary.get('artifacts', [])
    if not isinstance(entries, list):
        raise ValueError('Expected an artifact manifest list')
    verified = {}
    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError('Invalid artifact entry')
        name, media_type = entry.get('filename'), entry.get('media_type')
        digest, size = entry.get('sha256'), entry.get('bytes')
        if (not isinstance(name, str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]*', name)
                or name.casefold() == result_name.casefold() or name.casefold() in verified
                or not isinstance(media_type, str) or not media_type.strip()
                or not isinstance(digest, str) or not re.fullmatch(r'[0-9a-f]{64}', digest)
                or type(size) is not int or size < 0):
            raise ValueError('Invalid or duplicate artifact metadata')
        remaining = size
        with _open_local(directory / name) as source:
            if os.fstat(source.fileno()).st_size != size:
                raise ValueError('Artifact size does not match the manifest')
            computed = hashlib.sha256()
            while remaining:
                chunk = source.read(min(remaining, 1024 * 1024))
                if not chunk:
                    raise ValueError('Artifact ended before its declared size')
                computed.update(chunk)
                remaining -= len(chunk)
            if source.read(1) or computed.hexdigest() != digest:
                raise ValueError('Artifact digest or size does not match the manifest')
        verified[name.casefold()] = {'filename': name, 'media_type': media_type,
                                    'sha256': digest, 'bytes': size}
    return list(verified.values())


def _audit_logger(root, tag):
    parent = root
    for name in ('management', 'audit-log', 'logger'):
        children = [child for child in parent if child.tag.rsplit('}', 1)[-1] == name]
        if not children:
            return None
        if len(children) != 1 or children[0].tag != tag + name:
            raise ValueError('Ambiguous or unexpected management audit configuration')
        parent = children[0]
    return parent


def _direct_role_inclusion(root, tag, scope):
    parent = root
    for name in ('management', 'access-control', 'role-mapping'):
        nodes = [child for child in parent if child.tag.rsplit('}', 1)[-1] == name]
        if len(nodes) != 1 or nodes[0].tag != tag + name:
            return None
        parent = nodes[0]
        if name == 'access-control' and parent.get('provider') != 'rbac':
            return None
    roles = [role for role in parent if role.tag.rsplit('}', 1)[-1] == 'role'
             and role.get('name') == scope['role']]
    if len(roles) != 1 or roles[0].tag != tag + 'role':
        return None
    role = roles[0]
    # Realm-scoped users cannot be identified by account alone.
    matches = {}
    for name in ('include', 'exclude'):
        containers = [child for child in role if child.tag.rsplit('}', 1)[-1] == name]
        if len(containers) > 1 or any(child.tag != tag + name for child in containers):
            return None
        users = [user for child in containers for user in child
                 if user.tag.rsplit('}', 1)[-1] == 'user' and user.get('name') == scope['account']]
        if len(users) > 1 or any(user.tag != tag + 'user' for user in users):
            return None
        if any(set(user.attrib) != {'name'} for user in users):
            return None
        matches[name] = bool(users)
    if matches['exclude']:
        return None
    return matches['include']


def collect_jboss_audit(manifest, asset, export):
    """Extract scoped audit or direct-role settings from a supplied local XML copy.

    Args:
        manifest: Validated method manifest.
        asset: Same attributable inventory row used to prepare the request.
        export: Path to a local regular file containing the authorized copy.
    Returns:
        Selected audit settings and provenance bound to the collection request.
    Raises:
        ValueError: Unsupported scope, unsafe file type or invalid configuration.
        OSError: The local copy could not be opened or read.
    """
    request = prepare_collection(manifest, asset)
    if request['collector'] != _JBOSS_COLLECTOR:
        raise ValueError('No JBoss collector is registered for this exact asset scope')
    raw = _read_local(export)
    if b'\x00' in raw or b'<!DOCTYPE' in raw.upper() or b'<!ENTITY' in raw.upper():
        raise ValueError('Expected an XML export without external declarations')
    try:
        root = ET.fromstring(raw)
    except ET.ParseError as error:
        raise ValueError('Invalid standalone server XML') from error
    namespace = re.fullmatch(r'\{(urn:jboss:domain:\d+\.\d+)\}server', root.tag)
    if namespace is None:
        raise ValueError('Expected a standalone server configuration')
    tag = '{' + namespace[1] + '}'
    if 'jboss_role_mapping' in request:
        return {
            'request': request,
            'export_sha256': hashlib.sha256(raw).hexdigest(),
            'direct_role_inclusion': _direct_role_inclusion(root, tag, request['jboss_role_mapping']),
            'limitations': 'Direct configured inclusion only. Group grants and effective permissions require separate evidence.',
        }
    logger = _audit_logger(root, tag)
    settings = {}
    if logger is not None:
        for key in _AUDIT_FIELDS:
            settings[key] = {'true': True, 'false': False}.get(logger.get(key))
    return {
        'request': request,
        'export_sha256': hashlib.sha256(raw).hexdigest(),
        'audit_logger_present': logger is not None,
        'audit_settings': settings,
        'limitations': 'Configuration only. Effective settings, account assignments and detection require separate evidence.',
    }


class _LocalInquiryError(ValueError):
    def __init__(self, code):
        super().__init__(code)
        self.code = code


def _tool_digest(path):
    digest = hashlib.sha256()
    with _open_local(path) as binary:
        for chunk in iter(lambda: binary.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def _report_sanitization(source, output, retained, omitted):
    """Describe a safe projection locally using collector-defined labels.

    Source and output identify approved locations. Retained and omitted
    describe categories only and must never contain source data values.
    """
    destination = repr(output) if output else 'standard output'
    print(f"Sanitization of {source!r}: prepared {destination} with {retained}. "
          "The source is unchanged.", file=sys.stderr)
    print("Recognized sensitive fields omitted: "
          + (', '.join(sorted(omitted)) if omitted else 'none detected') + '.',
          file=sys.stderr)


def _collect_jboss_directory(request):
    scope = request['jboss_directory_membership']
    location = request.get('approved_result_path')
    if location and Path(scope['ldif_path']).resolve().is_relative_to(Path(location).parent.resolve()):
        raise _LocalInquiryError('source-in-handoff')
    raw = _read_local(scope['ldif_path'])
    try:
        text = raw.decode('utf-8')
    except UnicodeDecodeError as error:
        raise ValueError('The directory snapshot is not UTF-8 LDIF') from error
    text = text.replace('\r\n', '\n')
    groups = []
    ambiguous = bool(re.search(r'[\x00-\x08\x0b-\x1f\x7f-\x9f\u2028\u2029]', text))
    for entry in text.split('\n\n'):
        lines = [line for line in entry.split('\n') if line and not line.startswith('#')]
        identity = [line for line in lines if line.lower().startswith('dn:')]
        if any(not line.lower().startswith('dn: ') for line in identity):
            ambiguous = True
        if any(line[4:] == scope['group_dn'] for line in identity):
            groups.append(lines)
    if len(groups) == 1 and not ambiguous:
        lines = groups[0]
        unsupported = any(line.startswith((' ', '\t')) or line.lower().startswith(
            ('member::', 'member:<', 'member;', 'changetype:', 'control:')) for line in lines)
        plain_dns = [line for line in lines if line.lower().startswith('dn:')]
        observed = not unsupported and len(plain_dns) == 1 and any(
            line.lower().startswith('member: ') and line[8:] == scope['member_dn']
            for line in lines)
    else:
        observed = False
    sensitive_attributes = {
        'password': 'password',
        'userpassword': 'userPassword',
        'nthash': 'NThash',
        'sambantpassword': 'sambaNTPassword',
        'sambalmpassword': 'sambaLMPassword',
        'unicodepwd': 'unicodePwd',
        'supplementalcredentials': 'supplementalCredentials',
    }
    attribute_names = {
        line.partition(':')[0].partition(';')[0].lower()
        for line in text.split('\n')
        if ':' in line and not line.startswith((' ', '\t', '#'))
    }
    omitted = [sensitive_attributes[key] for key in sensitive_attributes.keys() & attribute_names]
    _report_sanitization(scope['ldif_path'], request.get('approved_result_path'),
                         'only the pinned request and membership result', omitted)
    return {
        'request': request,
        'directory_membership_observed': observed,
    }


def _collect_jboss_runtime(request):
    identity = request['jboss_runtime_identity']
    tool = identity['cli_path']
    try:
        digest = _tool_digest(tool)
    except (OSError, ValueError) as error:
        raise _LocalInquiryError('jboss-cli-mismatch') from error
    if digest != identity['cli_sha256']:
        raise _LocalInquiryError('jboss-cli-mismatch')
    args = [tool, '--connect', f"--controller=127.0.0.1:{identity['port']}",
            '--output-json', '--command=:whoami(verbose=true)']
    try:
        raw = _run_private_inquiry(request, args, b'', 'jboss-inquiry-failed')
        document = json.loads(raw)
        observed_identity = document['result']['identity']
        roles = document['result']['mapped-roles']
        if document['outcome'] != 'success' or not isinstance(roles, list) or any(
                not isinstance(role, str) for role in roles):
            raise _LocalInquiryError('jboss-inquiry-failed')
    except (subprocess.TimeoutExpired, OSError, KeyError, TypeError, UnicodeError, json.JSONDecodeError) as error:
        raise _LocalInquiryError('jboss-inquiry-failed') from error
    if not isinstance(observed_identity, dict) or any(
            observed_identity.get(key) != identity[key] for key in ('username', 'realm')):
        raise _LocalInquiryError('jboss-identity-mismatch')
    return {
        'request': request,
        'export_sha256': hashlib.sha256(raw).hexdigest(),
        'runtime_roles_match_policy': set(roles) == set(identity['expected_roles']),
        'limitations': 'Mapped roles in the observed management session only. Operation-level access was not tested.',
    }


def _collect_mq_channel(request):
    scope = request['mq_scope']
    tool = scope['approved_mqsc_path']
    if _tool_digest(tool) != scope['approved_mqsc_sha256']:
        raise _LocalInquiryError('mq-binary-mismatch')
    query = f"DISPLAY CHANNEL({scope['channel']}) CHLTYPE(SVRCONN) SSLCIPH SSLCAUTH\nEND\n"
    try:
        raw = _run_private_inquiry(request, [tool, scope['queue_manager']],
                                   query.encode('ascii'), 'mq-inquiry-failed')
    except subprocess.TimeoutExpired as error:
        raise _LocalInquiryError('mq-inquiry-timeout') from error
    fields = {}
    for key in ('CHANNEL', 'CHLTYPE', 'SSLCIPH', 'SSLCAUTH'):
        values = re.findall(r'(?<![A-Z0-9_.-])' + key + r'\(([^()\r\n]*)\)', raw.decode('ascii', errors='replace'))
        # MQSC may echo the inquiry, which does not contain a value for TLS attributes.
        fields[key] = set(value.strip() for value in values)
    if (fields['CHANNEL'] != {scope['channel']} or fields['CHLTYPE'] != {'SVRCONN'}
            or len(fields['SSLCIPH']) != 1
            or fields['SSLCAUTH'] not in ({'REQUIRED'}, {'OPTIONAL'})):
        raise _LocalInquiryError('mq-output-invalid')
    return {
        'request': request,
        'export_sha256': hashlib.sha256(raw).hexdigest(),
        'mq_tls': {'cipher_configured': bool(fields['SSLCIPH'] - {''}),
                   'client_certificate_required': fields['SSLCAUTH'] == {'REQUIRED'}},
        'limitations': 'Configuration only. Authentication behavior and effective authorization require separate evidence.',
    }


def _run_private_inquiry(request, command, input_bytes, failure_code):
    """Keep tool-created relative files and captured output out of the handoff."""
    scratch_root = Path('/tmp').resolve()
    location = request.get('approved_result_path')
    if location and scratch_root.is_relative_to(Path(location).parent.resolve()):
        raise _LocalInquiryError('private-workspace-unavailable')
    with tempfile.TemporaryDirectory(prefix='jai-collection-', dir=scratch_root) as workspace:
        environment = {'PATH': os.defpath, 'LC_ALL': 'C',
                       'TMPDIR': workspace, 'TMP': workspace, 'TEMP': workspace}
        with tempfile.TemporaryFile(dir=workspace) as output:
            process = subprocess.run(command, input=input_bytes, stdout=output,
                                     stderr=subprocess.DEVNULL, timeout=30, check=False,
                                     cwd=workspace, env=environment)
            if process.returncode or output.tell() > _MAX_INPUT_BYTES:
                raise _LocalInquiryError(failure_code)
            output.seek(0)
            return output.read(_MAX_INPUT_BYTES + 1)


def _next_evidence_requests(assessment, manifest):
    requests = []
    for gap in assessment['missing_mandatory_questions']:
        method = manifest.criteria[gap['criterion']]
        requests.append({**gap, 'reason': 'mandatory-question-not-planned',
                         'receiving_duty': 'assessment-plan-owner',
                         'evidence_request': method.get('evidence_request', method['question'])})
    for identifier, claim in assessment['claims'].items():
        if claim['status'] != 'pending':
            continue
        scope = {key: claim[key] for key in ('channel', 'interface', 'role_mapping', 'identity_scope', 'policy_revision') if claim.get(key)}
        method = manifest.criteria.get(claim['criterion'], {})
        reason = claim['reason']
        if reason == 'unsupported-scope':
            action = 'Confirm the exact inventory and registered method with the assessment-plan owner.'
        elif reason == 'policy-revision-required':
            action = 'Pin the approved policy revision for this identity before selecting evidence.'
        elif reason == 'evidence-route-incomplete':
            action = 'Select an applicable evidence route and obtain its missing inputs.'
            scope['evidence_routes'] = claim['evidence_routes']
            for key in ('policy_roles_sha256', 'mapping_membership_sha256'):
                if key in claim:
                    scope[key] = claim[key]
        elif reason == 'conflicting-evidence':
            action = 'Reconcile the contradictory observations with their sources before collecting again.'
        elif reason in ('claim-scope-required', 'unknown-or-conflicting-interface',
                        'shared-scope-required', 'single-asset-scope-required'):
            action = 'Resolve and record the exact asset, interface or channel scope before collecting again.'
        else:
            action = method.get('evidence_request', 'Resolve the evidence gap with the receiving duty.')
        requests.append({'claim': identifier, 'criterion': claim['criterion'],
                         'assets': claim['assets'], 'receiving_duty': claim['receiving_duty'],
                         'reason': reason, 'evidence_request': action, **scope})
    scoped_assets = {asset for item in requests for asset in item.get('assets', [])}
    for asset, method in assessment['asset_methods'].items():
        if method is None and asset not in scoped_assets:
            requests.append({'asset': asset, 'reason': 'unsupported-scope',
                             'receiving_duty': 'assessment-plan-owner',
                             'evidence_request': 'Confirm the exact inventory and registered method.'})
    if not assessment['claims'] and not assessment['missing_mandatory_questions']:
        requests.append({'assets': list(assessment['asset_methods']), 'reason': 'no-planned-questions',
                         'receiving_duty': 'assessment-plan-owner',
                         'evidence_request': 'Record the scoped questions and required evidence in the assessment plan.'})
    return requests


def report_preparation(assessment):
    """Recommend drafting a report or resolving gaps from a fresh assessment.

    Args:
        assessment: Result of evaluating the supplied normalized intake.
    Returns:
        Recommendation and exact unresolved assets and claims. Readiness is
        limited to the supplied plan and carries no acceptance authority.
    """
    missing = assessment['missing_mandatory_questions']
    unsupported = [asset for asset, method in assessment['asset_methods'].items() if method is None]
    claims = assessment['claims']
    unresolved = [{'claim': key, 'reason': result['reason']}
                  for key, result in claims.items() if result['status'] == 'pending']
    ready = bool(claims) and not (missing or unsupported or unresolved)
    return {
        'recommendation': 'draft-report' if ready else 'collect-or-reconcile-evidence',
        'missing_mandatory_questions': missing,
        'unsupported_assets': unsupported,
        'pending_claims': unresolved,
        'empty_plan': not claims,
    }


def _form_question(request, criterion):
    if criterion not in _FORM_CRITERIA or not request.get('approved_result_path'):
        raise ValueError('An eligible form criterion and approved result path are required')
    question = next((row for row in request['questions'] if row['criterion'] == criterion), None)
    if question is None:
        raise ValueError('The form criterion is outside the current request')
    return question


def build_operator_package(manifest_bytes, asset, output, *, form_criterion=None):
    """Write a standalone Python package for the approved host-local collector.

    Args:
        manifest_bytes: Bounded bytes of the selected method manifest.
        asset: Attributable inventory row with an approved POSIX configuration path.
        output: New archive path. An existing file is never replaced.
        form_criterion: Optional eligible question to capture from the operator.
    Returns:
        Request and SHA-256 of the produced archive.
    Raises:
        ValueError: No registered collector or approved absolute source path.
        OSError: A packaged source or the requested output cannot be accessed.
    """
    manifest = load_method_manifest(manifest_bytes)
    request = prepare_collection(manifest, asset)
    if form_criterion is not None:
        _form_question(request, form_criterion)
    elif (not request['collector'] or (request['collector'] == _JBOSS_COLLECTOR
                                       and not request['approved_configuration_path'])):
        raise ValueError('A registered collector and an approved configuration path are required')
    destination_path = _local_path(output)
    collector_keys = _MQ_FIELDS if request['collector'] == _MQ_COLLECTOR else ('approved_configuration_path',)
    inventory_keys = (*_SCOPE, 'id', 'revision', 'source', *collector_keys)
    inventory = {key: asset[key] for key in inventory_keys if key in asset}
    if 'jboss_directory_membership' in request:
        inventory['jboss_directory_membership'] = request['jboss_directory_membership']
    if 'jboss_runtime_identity' in request:
        inventory['jboss_runtime_identity'] = request['jboss_runtime_identity']
    if 'jboss_role_mapping' in request:
        inventory['jboss_role_mapping'] = request['jboss_role_mapping']
    if 'approved_result_path' in request:
        inventory['approved_result_path'] = request['approved_result_path']
    data = io.BytesIO()
    with zipfile.ZipFile(data, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr('__main__.py', _OPERATOR_ENTRY)
        archive.writestr('technical_security_collection.py', Path(__file__).read_bytes())
        archive.writestr('technical_security_evidence.py',
                         Path(technical_security_evidence.__file__).read_bytes())
        archive.writestr('manifest.json', manifest_bytes)
        archive.writestr('asset.json', json.dumps(inventory, sort_keys=True))
        if form_criterion is not None:
            archive.writestr('form.json', json.dumps(form_criterion))
    raw = data.getvalue()
    with destination_path.open('xb') as destination:
        destination.write(raw)
    return {'request': request, 'package_sha256': hashlib.sha256(raw).hexdigest()}


def _approved_publication(request, result, form_criterion):
    """Check the output fields and value types before crossing the handoff boundary."""
    if not isinstance(result, dict) or result.get('request') != request:
        return False
    fields = result.keys() - {'request'}
    schema = result.get('schema')
    if schema == _DIAGNOSTIC_SCHEMA:
        code = result.get('code')
        return (fields == {'schema', 'code', 'phase'} and isinstance(code, str)
                and code in _FAILURE_GUIDANCE and result['phase'] == _FAILURE_GUIDANCE[code][0])
    if schema == _FORM_SCHEMA:
        return (fields == {'schema', 'criterion', 'availability', 'evidence_reference', 'context'}
                and form_criterion is not None and result['criterion'] == form_criterion
                and isinstance(result['availability'], str)
                and result['availability'] in _FORM_AVAILABILITY
                and isinstance(result['evidence_reference'], str) and len(result['evidence_reference']) <= 240
                and (result['availability'] != 'available' or bool(result['evidence_reference'].strip()))
                and isinstance(result['context'], str) and len(result['context']) <= 480)
    collector = request['collector']
    if collector == _JBOSS_DIRECTORY_COLLECTOR:
        return fields == {'directory_membership_observed'} and type(result['directory_membership_observed']) is bool
    digest = result.get('export_sha256')
    if not isinstance(digest, str) or not re.fullmatch(r'[0-9a-f]{64}', digest):
        return False
    fields -= {'export_sha256'}
    if collector == _MQ_COLLECTOR:
        tls = result.get('mq_tls')
        return (fields == {'mq_tls'} and isinstance(tls, dict)
                and tls.keys() == {'cipher_configured', 'client_certificate_required'}
                and all(type(value) is bool for value in tls.values()))
    if collector == _JBOSS_RUNTIME_COLLECTOR:
        return fields == {'runtime_roles_match_policy'} and type(result['runtime_roles_match_policy']) is bool
    if collector != _JBOSS_COLLECTOR:
        return False
    if 'jboss_role_mapping' in request:
        return (fields == {'direct_role_inclusion'}
                and type(result['direct_role_inclusion']) in (bool, type(None)))
    present, settings = result.get('audit_logger_present'), result.get('audit_settings')
    return (fields == {'audit_logger_present', 'audit_settings'} and type(present) is bool
            and isinstance(settings, dict) and settings.keys() == (set(_AUDIT_FIELDS) if present else set())
            and all(type(value) in (bool, type(None)) for value in settings.values()))


def _safe_partial_result(request, result):
    """Return only independently safe, collector-specific observations."""
    if not isinstance(result, dict) or result.get('request') != request or 'schema' in result:
        return {}
    retained = {}
    collector = request['collector']
    if collector == _JBOSS_DIRECTORY_COLLECTOR:
        flags = ('directory_membership_observed',)
    elif collector == _JBOSS_RUNTIME_COLLECTOR:
        flags = ('runtime_roles_match_policy',)
    elif collector == _JBOSS_COLLECTOR and 'jboss_role_mapping' in request:
        flags = ('direct_role_inclusion',)
    elif collector == _JBOSS_COLLECTOR:
        flags = ('audit_logger_present',)
        settings = result.get('audit_settings')
        if isinstance(settings, dict):
            safe_settings = {key: settings[key] for key in _AUDIT_FIELDS
                             if key in settings and type(settings[key]) is bool}
            if safe_settings:
                retained['audit_settings'] = safe_settings
    elif collector == _MQ_COLLECTOR:
        flags = ()
        tls = result.get('mq_tls')
        if isinstance(tls, dict):
            safe_tls = {key: tls[key] for key in ('cipher_configured', 'client_certificate_required')
                        if type(tls.get(key)) is bool}
            if safe_tls:
                retained['mq_tls'] = safe_tls
    else:
        flags = ()
    retained.update({key: result[key] for key in flags if type(result.get(key)) is bool})
    return retained


def _publish_operator_result(request, result, status, *, form_criterion=None):
    blocked = not _approved_publication(request, result, form_criterion)
    location = request.get('approved_result_path')
    if blocked:
        method = form_criterion if form_criterion is not None else request['collector']
        print(f"Evidence withheld for asset {request['asset']!r}, method {method!r}: the result "
              "violated the approved handoff contract (publication-contract-violation).",
              file=sys.stderr)
        code = 'publication-contract-violation'
        partial = _safe_partial_result(request, result) if form_criterion is None else {}
        result = {'schema': _DIAGNOSTIC_SCHEMA, 'request': request,
                  'phase': _FAILURE_GUIDANCE[code][0], 'code': code}
        if partial:
            result['safe_partial_result'] = partial
        status = 1
    output = json.dumps(result, indent=2, sort_keys=True) + '\n'
    if location is None:
        sys.stdout.write(output)
    else:
        path = Path(location)
        try:
            with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=path.parent) as candidate:
                candidate.write(output)
                candidate.flush()
                os.link(candidate.name, path)
        except OSError:
            print('Could not publish the result at the approved path. Check directory access, '
                  'hard-link support and whether a result already exists.', file=sys.stderr)
            return 2
    if location is not None:
        print(f"Result available at {location!r}. Tell JAI the run has finished as usual. "
              "JAI will read the result from the agreed path.", file=sys.stderr)
    elif blocked:
        print('Safe diagnostic written to standard output. Return it to JAI using '
              'the normal standalone result handoff.', file=sys.stderr)
    return status


def _run_operator_form(request, criterion):
    question = _form_question(request, criterion)
    print(question['question'])
    print('Enter non-secret references only.')
    try:
        availability = input('Evidence availability [available/unavailable/unknown]: ').strip().lower()
        if availability not in _FORM_AVAILABILITY:
            raise ValueError('Invalid availability')
        reference = input('Reference to approved evidence (required if available): ').strip()
        note = input('Short non-secret context (optional): ').strip()
        if len(reference) > 240 or len(note) > 480 or (availability == 'available' and not reference):
            raise ValueError('An available record needs a reference')
    except (EOFError, KeyboardInterrupt, ValueError):
        phase, _ = _FAILURE_GUIDANCE['form-incomplete']
        return _publish_operator_result(request, {
            'schema': _DIAGNOSTIC_SCHEMA, 'request': request,
            'phase': phase, 'code': 'form-incomplete',
        }, 1)
    return _publish_operator_result(request, {
        'schema': _FORM_SCHEMA, 'request': request, 'criterion': criterion,
        'availability': availability, 'evidence_reference': reference, 'context': note,
    }, 0, form_criterion=criterion)


def run_operator_package():
    """Collect one approved local input and publish the result or diagnostic.

    The operator accepts the host and account context by choosing where to run
    the package. Optional command-line arguments cannot override the source.
    Returns:
        Zero on collection, one after a published source failure, or two if
        publication fails.
    Raises:
        SystemExit: Unsupported platform or unexpected command-line arguments.
        ValueError, OSError: The package or its pinned scope is invalid.
    """
    if os.name != 'posix' or len(sys.argv) != 1:
        raise SystemExit('Run the package on the approved POSIX host without arguments')
    with zipfile.ZipFile(sys.argv[0]) as archive:
        manifest = load_method_manifest(archive.read('manifest.json'))
        asset = json.loads(archive.read('asset.json'))
        form = json.loads(archive.read('form.json')) if 'form.json' in archive.namelist() else None
    if form is not None:
        return _run_operator_form(prepare_collection(manifest, asset), form)
    path = _approved_path(asset, 'approved_configuration_path')
    request = prepare_collection(manifest, asset)
    if request['collector'] == _JBOSS_COLLECTOR and path is None:
        raise ValueError('An approved configuration path is required')
    if request['collector'] is None:
        raise ValueError('Invalid operator package scope')
    try:
        if request['collector'] == _MQ_COLLECTOR:
            result = _collect_mq_channel(request)
        elif request['collector'] == _JBOSS_RUNTIME_COLLECTOR:
            result = _collect_jboss_runtime(request)
        elif request['collector'] == _JBOSS_DIRECTORY_COLLECTOR:
            result = _collect_jboss_directory(request)
        else:
            result = collect_jboss_audit(manifest, asset, path)
    except _LocalInquiryError as error:
        code = error.code
    except FileNotFoundError:
        code = 'mq-inquiry-failed' if request['collector'] == _MQ_COLLECTOR else 'source-missing'
    except PermissionError:
        code = 'mq-inquiry-failed' if request['collector'] == _MQ_COLLECTOR else 'source-permission-denied'
    except OSError:
        code = 'mq-inquiry-failed' if request['collector'] == _MQ_COLLECTOR else 'source-unreadable'
    except ValueError:
        code = 'source-invalid'
    else:
        if isinstance(result, dict):
            result.pop('limitations', None)
        return _publish_operator_result(request, result, 0)
    phase, _ = _FAILURE_GUIDANCE[code]
    diagnostic = {'schema': _DIAGNOSTIC_SCHEMA, 'request': request,
                  'phase': phase, 'code': code}
    return _publish_operator_result(request, diagnostic, 1)


def _expected_roles_digest(identity):
    return hashlib.sha256(json.dumps(sorted(identity['expected_roles']),
                                     separators=(',', ':')).encode('ascii')).hexdigest()


def _membership_scope_digest(directory):
    fields = (directory['source'], directory['group_dn'], directory['member_dn'])
    return hashlib.sha256(json.dumps(fields, separators=(',', ':')).encode('ascii')).hexdigest()


def _runtime_policy_route(criterion):
    routes = [route['inputs'] for route in criterion.get('evidence_routes', [])
              if 'runtime' in route['inputs']]
    return (criterion.get('runtime_policy_binding') is True
            and criterion.get('baseline_roles') == ['policy'] and bool(routes)
            and all('policy' in inputs for inputs in routes))


def _normalize_collection(manifest, asset, claims, summary, returned):
    request = prepare_collection(manifest, asset)
    if not isinstance(summary, dict) or summary.get('request') != request:
        raise ValueError('Collection result does not match the current request')
    directory = request['collector'] == _JBOSS_DIRECTORY_COLLECTOR
    if directory and 'artifacts' in summary:
        raise ValueError('Directory collection does not accept attachments')
    digest = hashlib.sha256(returned).hexdigest()
    if summary.get('schema') == _FORM_SCHEMA:
        criterion = summary.get('criterion')
        if not isinstance(criterion, str):
            raise ValueError('Invalid form criterion')
        _form_question(request, criterion)
        availability, reference = summary.get('availability'), summary.get('evidence_reference')
        note = summary.get('context')
        if (not isinstance(availability, str) or availability not in _FORM_AVAILABILITY
                or not isinstance(reference, str) or len(reference) > 240
                or not isinstance(note, str) or len(note) > 480
                or (availability == 'available' and not reference.strip())):
            raise ValueError('Invalid operator form response')
        return [], {'collection_sha256': digest, 'status': 'requires-assessor-review',
                    'operator_response': {'criterion': criterion, 'availability': availability,
                                          'evidence_reference': reference, 'context': note}}
    if 'schema' in summary:
        code = summary.get('code')
        if summary['schema'] != _DIAGNOSTIC_SCHEMA or not isinstance(code, str) or code not in _FAILURE_GUIDANCE:
            raise ValueError('Unsupported collection diagnostic')
        phase, action = _FAILURE_GUIDANCE[code]
        if summary.get('phase') != phase:
            raise ValueError('Collection diagnostic phase does not match its code')
        review = {'collection_sha256': digest, 'status': 'collection-failed',
                  'phase': phase, 'code': code, 'next_action': action}
        if code == 'publication-contract-violation':
            diagnostic = {key: value for key, value in summary.items() if key != 'safe_partial_result'}
            partial = summary.get('safe_partial_result', {})
            if not _approved_publication(request, diagnostic, None) or not isinstance(partial, dict):
                raise ValueError('Invalid publication contract diagnostic')
            verified = _safe_partial_result(request, {**partial, 'request': request})
            if json.dumps(verified, sort_keys=True) != json.dumps(partial, sort_keys=True):
                raise ValueError('Invalid partial publication result')
            if verified:
                review['safe_partial_result'] = verified
        return [], review
    if request['collector'] is None:
        raise ValueError('No collector is registered for this exact request')
    provenance = {}
    if not directory:
        export_digest = summary.get('export_sha256')
        if not isinstance(export_digest, str) or not re.fullmatch(r'[0-9a-f]{64}', export_digest):
            raise ValueError('Invalid returned export digest')
        provenance['export_sha256'] = export_digest
    if request['collector'] == _MQ_COLLECTOR:
        settings = summary.get('mq_tls')
        if (not isinstance(settings, dict)
                or settings.keys() != {'cipher_configured', 'client_certificate_required'}
                or any(type(value) is not bool for value in settings.values())):
            raise ValueError('Invalid returned MQ channel properties')
        criterion = _MQ_CRITERION
        enabled = all(settings.values())
    elif directory:
        criterion = _RUNTIME_CRITERION
        observed = summary.get('directory_membership_observed')
        if summary.keys() != {'request', 'directory_membership_observed'} or type(observed) is not bool:
            raise ValueError('Invalid returned directory membership result')
        enabled = True if observed else None
    elif request['collector'] == _JBOSS_RUNTIME_COLLECTOR:
        criterion = _RUNTIME_CRITERION
        enabled = summary.get('runtime_roles_match_policy')
        if type(enabled) is not bool:
            raise ValueError('Invalid returned runtime role result')
    elif 'jboss_role_mapping' in request:
        criterion = _ROLE_CRITERION
        enabled = summary.get('direct_role_inclusion')
        if ('direct_role_inclusion' not in summary
                or (enabled is not None and type(enabled) is not bool)):
            raise ValueError('Invalid returned direct role inclusion')
    else:
        settings = summary.get('audit_settings')
        present = summary.get('audit_logger_present')
        if (type(present) is not bool or not isinstance(settings, dict)
                or settings.keys() != (set(_AUDIT_FIELDS) if present else set())
                or any(value is not None and type(value) is not bool for value in settings.values())):
            raise ValueError('Invalid returned audit settings')
        criterion = _AUDIT_CRITERION
        enabled = settings.get('enabled')
    matching_claims = [claim for claim in claims
                       if claim.get('criterion') == criterion and claim.get('assets') == [asset['id']]]
    scope = {}
    if criterion == _MQ_CRITERION:
        scope = {'channel': request['mq_scope']['channel']}
    elif criterion == _ROLE_CRITERION:
        scope = {'role_mapping': request['jboss_role_mapping']['id']}
    elif criterion == _RUNTIME_CRITERION:
        identity = request.get('jboss_runtime_identity') or request['jboss_directory_membership']
        scope = {'identity_scope': identity['identity_scope'], 'policy_revision': identity['policy_revision']}
    planned = bool(matching_claims) and all(
        all(claim.get(key) == value for key, value in scope.items()) for claim in matching_claims)
    review = {'collection_sha256': digest, **provenance,
              'status': 'requires-assessor-review'}
    if not planned:
        return [], review
    revision = _RUNTIME_CRITERION_REVISION if criterion == _RUNTIME_CRITERION else _AUDIT_CRITERION_REVISION
    if (manifest.criteria.get(criterion, {}).get('revision') != revision
            or manifest.formats.get(_AUDIT_FORMAT, {}).get('revision') != _AUDIT_FORMAT_REVISION
            or _AUDIT_FORMAT not in manifest.criteria[criterion]['formats']
            or (scope and manifest.criteria[criterion].get('scope_field') != next(iter(scope)))
            or (criterion == _RUNTIME_CRITERION and not _runtime_policy_route(manifest.criteria[criterion]))):
        review['normalization_gap'] = 'unsupported-criterion-or-format-revision'
        return [], review
    if enabled is None:
        review['normalization_gap'] = (
            'directory-membership-unresolved' if request['collector'] == _JBOSS_DIRECTORY_COLLECTOR else
            'direct-role-mapping-unresolved' if criterion == _ROLE_CRITERION else
            'enabled-setting-not-explicit')
        return [], review
    return [{
        'id': f'collection-{digest}',
        'criterion': criterion,
        **scope,
        **({'evidence_role': 'runtime',
            'expected_roles_sha256': _expected_roles_digest(request['jboss_runtime_identity'])}
           if request['collector'] == _JBOSS_RUNTIME_COLLECTOR else {}),
        **({'evidence_role': 'identity',
            'membership_scope_sha256': _membership_scope_digest(request['jboss_directory_membership'])}
           if request['collector'] == _JBOSS_DIRECTORY_COLLECTOR else {}),
        'criterion_revision': revision,
        'assets': [asset['id']],
        'asset_revisions': {asset['id']: asset['revision']},
        'format': _AUDIT_FORMAT,
        'format_revision': _AUDIT_FORMAT_REVISION,
        'source': f'collection-sha256:{digest}',
        'revision': digest,
        'status': 'conforming' if enabled else 'deviation',
    }], review


def _assessment_window(saved, now, extension):
    if saved is None:
        if extension is not None:
            raise ValueError('An extension requires the existing assessment window')
        start, deadline = now, now + timedelta(minutes=30)
    else:
        try:
            start = datetime.fromisoformat(saved['started_at'])
            deadline = datetime.fromisoformat(saved['deadline'])
        except (KeyError, TypeError, ValueError) as error:
            raise ValueError('Invalid assessment window') from error
        if start.utcoffset() is None or deadline.utcoffset() is None or not start <= now or deadline <= start:
            raise ValueError('Invalid assessment window')
        if extension is not None:
            if extension <= 0:
                raise ValueError('Extension minutes must be positive')
            deadline = max(deadline, now) + timedelta(minutes=extension)
    return {'started_at': start.isoformat(), 'deadline': deadline.isoformat()}, now < deadline


def _prepare_follow_up(manifest_bytes, manifest, asset, intake, observations, assessment,
                       review, input_path, output, result_path, form_criterion, corrected):
    advice = assessment['report_preparation']
    requests = [row for row in advice['next_evidence_requests']
                if row.get('asset') == asset['id'] or row.get('assets') == [asset['id']]]
    if advice['recommendation'] == 'draft-report':
        return {'status': 'draft-report'}
    if review is not None and review['status'] == 'collection-failed' and not corrected:
        return {'status': 'confirm-correction', 'next_action': review['next_action']}
    gap = review.get('normalization_gap') if review is not None else None
    if form_criterion is None and gap == 'unsupported-criterion-or-format-revision':
        return {'status': 'resolve-method', 'receiving_duty': 'method-owner',
                'next_action': 'Confirm a supported criterion and observation format revision.'}
    if form_criterion is None and gap == 'enabled-setting-not-explicit':
        return {'status': 'request-different-evidence', 'receiving_duty': 'platform-owner',
                'next_action': 'Supply attributable evidence for the unresolved audit logger setting.'}
    if form_criterion is None and gap == 'directory-membership-unresolved':
        return {'status': 'request-different-evidence', 'receiving_duty': 'identity-owner',
                'next_action': 'Supply attributable evidence for the unresolved directory membership.'}
    if form_criterion is None and gap == 'direct-role-mapping-unresolved':
        return {'status': 'request-different-evidence', 'receiving_duty': 'platform-owner',
                'next_action': 'Supply reviewed evidence for the unresolved direct role mapping.'}
    request = prepare_collection(manifest, asset)
    collector = request['collector']
    if form_criterion is not None:
        candidates = [row for row in requests if row.get('criterion') == form_criterion]
    else:
        criterion = {_JBOSS_COLLECTOR: _AUDIT_CRITERION, _MQ_COLLECTOR: _MQ_CRITERION,
                     _JBOSS_RUNTIME_COLLECTOR: _RUNTIME_CRITERION,
                     _JBOSS_DIRECTORY_COLLECTOR: _RUNTIME_CRITERION}.get(collector)
        if 'jboss_role_mapping' in request:
            criterion = _ROLE_CRITERION
            if any(row['criterion'] == criterion and row['assets'] == [asset['id']]
                   and row.get('role_mapping') != request['jboss_role_mapping']['id']
                   for row in assessment['claims'].values()):
                return {'status': 'resolve-role-scope', 'requests': requests}
        candidates = [row for row in requests
                      if criterion is not None and row.get('criterion') == criterion
                      and (row['reason'] == 'missing-or-conflicting-evidence'
                           or (collector == _JBOSS_RUNTIME_COLLECTOR and row['reason'] == 'evidence-route-incomplete'
                               and row.get('identity_scope') == request['jboss_runtime_identity']['identity_scope']
                               and row.get('policy_revision') == request['jboss_runtime_identity']['policy_revision']
                               and row.get('policy_roles_sha256') == _expected_roles_digest(request['jboss_runtime_identity'])
                               and any(set(option['missing']) == {'runtime'}
                                       for option in row.get('evidence_routes', [])))
                           or (collector == _JBOSS_DIRECTORY_COLLECTOR and row['reason'] == 'evidence-route-incomplete'
                               and row.get('identity_scope') == request['jboss_directory_membership']['identity_scope']
                               and row.get('policy_revision') == request['jboss_directory_membership']['policy_revision']
                               and row.get('mapping_membership_sha256') == _membership_scope_digest(
                                   request['jboss_directory_membership'])
                               and any(set(option['missing']) == {'identity'}
                                       for option in row.get('evidence_routes', []))))
                      and (collector != _MQ_COLLECTOR
                           or row.get('channel') == request['mq_scope']['channel'])]
    if not candidates:
        return {'status': 'ask-in-conversation', 'requests': requests}
    if (form_criterion is None and collector == _MQ_COLLECTOR
            and any(row['criterion'] == _MQ_CRITERION and row['assets'] == [asset['id']]
                    and row.get('channel') != request['mq_scope']['channel']
                    for row in assessment['claims'].values())):
        return {'status': 'resolve-channel-scope', 'requests': requests}
    next_asset = {**asset, 'approved_result_path': str(result_path)}
    next_request = prepare_collection(manifest, next_asset)
    if 'approved_result_path' not in next_request:
        raise ValueError('A registered asset and fresh approved result path are required')
    previous = [path for path in (asset.get('approved_result_path'), input_path) if path is not None]
    if any(Path(result_path).resolve() == Path(path).resolve() for path in previous):
        raise ValueError('The follow-up result path must differ from the previous attempt')
    if Path(result_path).resolve() == Path(output).resolve():
        raise ValueError('The package and result paths must differ')
    package = build_operator_package(manifest_bytes, next_asset, output, form_criterion=form_criterion)
    return {'status': 'package-issued', 'package_sha256': package['package_sha256'],
            'request': package['request'], 'prior_intake_sha256': assessment['intake_sha256'],
            'prior_collection_sha256': review['collection_sha256'] if review is not None else None,
            'next_asset': next_asset,
            'next_intake': {**intake, 'observations': observations,
                            'assets': [next_asset if row == asset else row for row in intake['assets']]}}


def _review_zap_report(raw, scope, asset):
    required = ('application', 'release', 'assessment_ref', 'scope_ref',
                'asset', 'asset_revision', 'site', 'sha256')
    if not isinstance(scope, dict) or any(
            not isinstance(scope.get(key), str) or not scope[key].strip()
            for key in required):
        raise ValueError('ZAP report needs a release-bound application evidence record')
    if scope['asset'] != asset['id'] or scope['asset_revision'] != asset['revision']:
        raise ValueError('ZAP report does not match the assessed asset revision')
    origin = urlsplit(scope['site'])
    if (origin.scheme not in ('http', 'https') or not origin.hostname
            or origin.username is not None or origin.password is not None
            or origin.path not in ('', '/') or origin.query or origin.fragment):
        raise ValueError('ZAP scope needs an HTTP or HTTPS origin without credentials')
    digest = hashlib.sha256(raw).hexdigest()
    if digest != scope['sha256']:
        raise ValueError('ZAP report digest differs from the scoped evidence record')
    report = json.loads(raw)
    if not isinstance(report, dict):
        raise ValueError('Invalid ZAP traditional JSON report')
    sites = report.get('site')
    if (not isinstance(sites, list) or len(sites) != 1 or not isinstance(sites[0], dict)
            or sites[0].get('@name') != scope['site']):
        raise ValueError('ZAP report must contain exactly the scoped site')
    alerts = sites[0].get('alerts')
    if not isinstance(alerts, list):
        raise ValueError('Invalid ZAP alert list')
    counts = {}
    for alert in alerts:
        if not isinstance(alert, dict):
            raise ValueError('Invalid ZAP alert')
        plugin, risk = alert.get('pluginid'), alert.get('riskcode')
        if (not isinstance(plugin, str) or not re.fullmatch(r'[0-9]{1,12}', plugin)
                or not isinstance(risk, str) or risk not in ('0', '1', '2', '3')):
            raise ValueError('Invalid ZAP alert identifier or risk code')
        counts[(plugin, risk)] = counts.get((plugin, risk), 0) + 1
    return {
        **{key: scope[key] for key in required},
        'format': 'zap-traditional-json',
        'status': 'requires-assessor-review',
        'alerts': [{'plugin_id': plugin, 'risk_code': risk, 'entries': count}
                   for (plugin, risk), count in sorted(counts.items())],
        'limitations': 'Reported alerts only. The supplied record binds release and scope; '
                       'the report alone does not establish identity or assessment coverage.',
    }


def main(argv=None):
    """Print a collection request or approved local evidence to standard output.

    Args:
        argv: Optional CLI arguments, otherwise taken from the process.
    Returns:
        Zero after the request or evidence is written.
    Raises:
        ValueError, OSError: Invalid or inaccessible supplied input.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest', type=Path)
    parser.add_argument('asset', type=Path)
    action = parser.add_mutually_exclusive_group()
    action.add_argument('--export', type=Path)
    action.add_argument('--intake', type=Path)
    action.add_argument('--emit-script', type=Path)
    parser.add_argument('--form-criterion')
    parser.add_argument('--emit-follow-up', type=Path)
    parser.add_argument('--follow-up-result', type=Path)
    parser.add_argument('--retry-after-correction', action='store_true')
    parser.add_argument('--extend-minutes', type=int)
    parser.add_argument('--zap-report', type=Path)
    read_result = parser.add_mutually_exclusive_group()
    read_result.add_argument('--collection', type=Path)
    read_result.add_argument('--use-shared-result', action='store_true')
    args = parser.parse_args(argv)
    if (args.collection is not None or args.use_shared_result) and args.intake is None:
        parser.error('Reading a collection result requires --intake')
    if args.zap_report is not None and args.intake is None:
        parser.error('--zap-report requires --intake')
    if args.extend_minutes is not None and args.intake is None:
        parser.error('--extend-minutes requires --intake')
    if args.form_criterion is not None and args.emit_script is None and args.emit_follow_up is None:
        parser.error('--form-criterion requires package preparation')
    if args.emit_follow_up is not None and (args.intake is None or args.follow_up_result is None):
        parser.error('--emit-follow-up requires --intake and --follow-up-result')
    if (args.follow_up_result is not None or args.retry_after_correction) and args.emit_follow_up is None:
        parser.error('Follow-up options require --emit-follow-up')
    manifest_bytes = _read_local(args.manifest)
    asset = json.loads(_read_local(args.asset))
    if args.emit_script is not None:
        result = build_operator_package(manifest_bytes, asset, args.emit_script,
                                        form_criterion=args.form_criterion)
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0
    manifest = load_method_manifest(manifest_bytes)
    if args.intake is not None:
        raw = _read_local(args.intake)
        intake = json.loads(raw)
        saved_window = intake.get('assessment_window')
        window, _ = _assessment_window(saved_window,
                                                 datetime.now(timezone.utc), args.extend_minutes)
        intake['assessment_window'] = window
        if asset not in intake['assets']:
            raise ValueError('Assessment intake must contain the exact inventory row')
        observations = intake['observations']
        review = None
        collection = args.collection
        if args.use_shared_result:
            collection = prepare_collection(manifest, asset).get('approved_result_path')
            if collection is None:
                raise ValueError('The request has no approved shared result path')
        if collection is not None:
            result_path = Path(collection)
            returned = _read_local(result_path)
            summary = json.loads(returned)
            derived, review = _normalize_collection(manifest, asset, intake['claims'], summary, returned)
            artifacts = _verify_native_outputs(summary, result_path.parent, result_path.name)
            if artifacts:
                review['native_artifacts'] = artifacts
            observations = [*observations, *derived]
        result = manifest.assess(intake['assets'], intake['claims'],
                                 observations, intake.get('interfaces', []))
        result['intake_sha256'] = hashlib.sha256(raw).hexdigest()
        result['assessment_window'] = window
        if args.zap_report is not None:
            result['application_evidence'] = _review_zap_report(
                _read_local(args.zap_report), intake.get('zap_report_scope'), asset)
        result['report_preparation'] = report_preparation(result)
        result['report_preparation']['next_evidence_requests'] = _next_evidence_requests(result, manifest)
        if review is not None:
            result['collection_review'] = review
        _, window_open = _assessment_window(window, datetime.now(timezone.utc), None)
        result['assessment_window_status'] = 'open' if window_open else 'elapsed'
        if args.emit_follow_up is not None and saved_window is None:
            result['follow_up'] = {'status': 'persist-assessment-window'}
        elif args.emit_follow_up is not None and not window_open:
            readiness = result['report_preparation']['recommendation']
            result['follow_up'] = {'status': 'draft-report' if readiness == 'draft-report'
                                   else 'assessment-window-elapsed'}
        elif args.emit_follow_up is not None:
            result['follow_up'] = _prepare_follow_up(
                manifest_bytes, manifest, asset, intake, observations, result, review, collection,
                args.emit_follow_up, args.follow_up_result, args.form_criterion,
                args.retry_after_correction,
            )
    elif args.export is not None:
        result = collect_jboss_audit(manifest, asset, args.export)
    else:
        result = prepare_collection(manifest, asset)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
