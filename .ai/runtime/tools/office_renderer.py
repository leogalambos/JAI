#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Strict, isolated native Office conversion; unavailable prerequisites fail closed.

LibreOffice requires local IPC even for headless conversion. A version query is
not evidence that conversion works. This helper does not change host policy,
retry outside isolation, replace rendering with fabricated pixels, or qualify a
provider boundary. Its private user profile prevents shared-profile interference.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import socket
import subprocess
import sys
import tempfile


class RendererUnavailable(RuntimeError):
    """Required native conversion prerequisite is unavailable on this runner."""


def prerequisites() -> dict:
    """Check the Linux native converter's local IPC prerequisite without binding.

    Returns:
        A bounded availability/reason/errno mapping. A successful socket creation
        proves only this prerequisite, never a successful render or sandbox.
        Other platforms require their native converter checks rather than a
        fabricated Linux socket result.
    """
    if not sys.platform.startswith('linux'):
        return {'available': True, 'scope': 'Linux IPC probe not applicable; native render still required'}
    try:
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM):
            pass
    except OSError as exc:
        return {'available': False, 'reason': 'AF_UNIX_IPC_DENIED', 'errno': exc.errno}
    return {'available': True, 'scope': 'AF_UNIX socket creation only'}


def convert_office(source, output_directory, timeout=90, executable=None) -> Path:
    """Convert one local Office/HTML source to a fresh, verified PDF.

    Args:
        source: Existing DOCX, PPTX, XLSX or HTML file selected for native render.
        output_directory: Caller-selected generated-output directory; an existing
            PDF is replaced only after a new conversion produces valid PDF bytes.
        timeout: Positive bounded seconds, at most 300; no retries are performed.
        executable: Optional explicit absolute LibreOffice/soffice executable;
            otherwise the installed executable is resolved from the host PATH.
    Returns:
        Generated PDF path after successful native conversion in a fresh private
        profile and output directory. No stale PDF can satisfy the result check.
    Raises:
        ValueError: Unsupported source, timeout or nonabsolute executable.
        RendererUnavailable: Renderer or Linux IPC prerequisite is unavailable.
        RuntimeError: Nonzero process status, missing or invalid new PDF.
        subprocess.TimeoutExpired: Native conversion exceeds the finite timeout.
        OSError: Inputs, temporary profile or destination cannot be accessed.
    """
    if type(timeout) not in {int, float} or not 0 < timeout <= 300:
        raise ValueError('positive bounded renderer timeout required')
    source = Path(source).resolve(strict=True)
    if source.suffix.lower() not in {'.docx', '.pptx', '.xlsx', '.html'} or not source.is_file():
        raise ValueError('supported regular Office/HTML source required')
    executable = executable or shutil.which('libreoffice') or shutil.which('soffice')
    if not executable:
        raise RendererUnavailable('RENDERER_UNAVAILABLE: LibreOffice/soffice is required')
    if not Path(executable).is_absolute():
        raise ValueError('absolute native renderer executable required')
    readiness = prerequisites()
    if not readiness['available']:
        raise RendererUnavailable('RENDERER_PREREQUISITE_UNAVAILABLE: ' + json.dumps(readiness, sort_keys=True))
    output_directory = Path(output_directory)
    output_directory.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='jai-office-render-') as directory:
        temporary = Path(directory)
        converted = temporary / 'converted'; converted.mkdir()
        environment = {'PATH': os.defpath, 'LANG': 'C.UTF-8', 'LC_ALL': 'C.UTF-8',
            'XDG_CONFIG_HOME': str(temporary / 'config'), 'XDG_CACHE_HOME': str(temporary / 'cache')}
        if 'HOME' in os.environ:
            environment['HOME'] = os.environ['HOME']
        command = [str(executable), '-env:UserInstallation=' + (temporary / 'profile').as_uri(),
                   '--headless', '--convert-to', 'pdf', '--outdir', str(converted), str(source)]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                text=True, timeout=timeout, env=environment)
        pdf = converted / (source.stem + '.pdf')
        valid = pdf.is_file() and not pdf.is_symlink() and pdf.read_bytes().startswith(b'%PDF-')
        if result.returncode or not valid:
            redact = lambda text: str(text or '').replace(str(temporary), '<render-temp>').replace(str(source), '<source>')[-1000:]
            raise RuntimeError('NATIVE_RENDER_FAILED: exit=' + str(result.returncode)
                + '; new_pdf=' + str(valid) + '; stdout=' + json.dumps(redact(result.stdout), ensure_ascii=True)
                + '; stderr=' + json.dumps(redact(result.stderr), ensure_ascii=True))
        target = output_directory / pdf.name
        shutil.copyfile(pdf, target)
        return target


def _process_error(exc):
    """Preserve bounded subprocess failure streams, including byte timeout output."""
    details={'type':type(exc).__name__,'message':str(exc)}
    for stream in ('stdout','stderr'):
        value=getattr(exc,stream,None) or ''
        if isinstance(value,bytes):value=value.decode('utf-8',errors='replace')
        details[stream]=value[:8000]
        details[stream+'_truncated']=len(value)>8000
    return json.dumps(details,ensure_ascii=True)


def _html_pdf_cli(source, out):
    """Use WeasyPrint 70 CLI with a deny-all resource fetcher and fresh output."""
    import hashlib,re
    executable=shutil.which('weasyprint')
    if not executable:raise RendererUnavailable('WeasyPrint CLI absent from PATH')
    try:
        probe=subprocess.run([executable,'--version'],capture_output=True,text=True,timeout=10)
    except (OSError,subprocess.SubprocessError) as exc:
        raise RendererUnavailable('WeasyPrint CLI version probe failed: '+_process_error(exc)) from exc
    version=re.fullmatch(r'WeasyPrint(?: version)?\s+(70(?:\.[0-9]+)*)',probe.stdout.strip())
    if probe.returncode or version is None:
        raise RendererUnavailable('WeasyPrint CLI unavailable or unqualified; exit='+str(probe.returncode)
            +'; stdout='+probe.stdout[:2000]+'; stderr='+probe.stderr[:2000])
    text=source.read_text(encoding='utf-8')
    with tempfile.TemporaryDirectory(prefix='jai-cli-html-') as directory:
        temporary=Path(directory)
        stylesheet=temporary/'policy.css'
        stylesheet.write_text('body { font-family: "DejaVu Sans", sans-serif; }')
        pdf=temporary/'result.pdf'
        command=[executable,'--allowed-protocols','','--no-http-redirects',
                 '--fail-on-http-errors','--base-url','file:///__jai_resource_denied__/','--stylesheet',str(stylesheet),'-',str(pdf)]
        try:
            result=subprocess.run(command,input=text,capture_output=True,text=True,timeout=20)
        except (OSError,subprocess.SubprocessError) as exc:
            raise RuntimeError('WeasyPrint CLI conversion failed: '+_process_error(exc)) from exc
        if result.returncode:
            message='WeasyPrint CLI conversion exit='+str(result.returncode)+'; stderr='+result.stderr[-8000:]+'; stdout='+result.stdout[-2000:]
            if 'FatalURLFetchingError' in result.stderr:raise ValueError(message)
            raise RuntimeError(message)
        if not pdf.is_file() or pdf.is_symlink() or not pdf.read_bytes().startswith(b'%PDF-'):
            raise RuntimeError('WeasyPrint CLI produced no valid fresh PDF; stderr='+result.stderr[-2000:])
        target=out/(source.stem+'.pdf')
        data=pdf.read_bytes()
        evidence={'backend':'WeasyPrint','version':version.group(1),'execution':'cli',
            'executable':executable,'python':None,'pyphen':None,
            'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
            'output_sha256':hashlib.sha256(data).hexdigest(),
            'resources':'deny all URL fetches; no custom font-face; system DejaVu Sans',
            'office_visual_evidence':False}
        shutil.copyfile(pdf,target)
        target.with_suffix('.renderer.json').write_text(json.dumps(evidence,indent=2)+'\n')
        return target


def html_pdf(source, output_directory, backend='auto'):
    """Render HTML with constrained WeasyPrint, then optional Office fallback.

    Args:
        source: Existing local HTML file; external resources are denied.
        output_directory: Destination for a freshly rendered PDF and evidence.
        backend: auto, weasyprint or libreoffice. Explicit LibreOffice bypasses
            discovery. All OSes try the WeasyPrint 70 CLI on PATH first, then
            the current Python module if the CLI is absent/unqualified or its
            version probe cannot start. Only unavailable backends permit fallback.
    Returns:
        Path to a new PDF. CLI rendering denies all URL protocols, redirects,
        external CSS and custom font loading; conversion has a 20-second budget.
        CLI evidence reports its executable; interpreter/dependency versions are
        unknown because caller Python packages need not match the CLI runtime.
    Raises:
        ValueError: Invalid input or denied resource; never triggers fallback.
        RendererUnavailable: Neither CLI nor current-Python WeasyPrint can run.
        RuntimeError, OSError: Conversion/output fails; no fabricated PDF accepted.
        subprocess.TimeoutExpired: Office fallback exceeds its conversion budget.
    """
    source = Path(source).resolve(strict=True)
    out = Path(output_directory);out.mkdir(parents=True, exist_ok=True)
    if backend not in {'auto','weasyprint','libreoffice'} or source.suffix.lower()!='.html':
        raise ValueError('explicit HTML backend required')
    if backend == 'libreoffice':return convert_office(source,out)
    import re
    if re.search(r'@import|@font-face|<!ENTITY',source.read_text(encoding='utf-8'),re.I):
        raise ValueError('external CSS, custom fonts and entities denied')
    try:
        return _html_pdf_cli(source,out)
    except RendererUnavailable as cli_error:
        try:return _html_pdf_local(source,out)
        except RendererUnavailable as module_error:
            if backend == 'auto':return convert_office(source,out)
            raise module_error from cli_error


def _html_pdf_local(source,output_directory):
    """Render actual HTML independently of Office when WeasyPrint is installed.

    Only embedded content and protected system fonts are supported. All resource
    fetches and custom font loads deny; an attempted fetch fails the render rather
    than silently replacing content. HTML PDF is never Office visual evidence.
    """
    import importlib.util,importlib.metadata,re,hashlib
    source=Path(source).resolve(strict=True);out=Path(output_directory);out.mkdir(parents=True,exist_ok=True)
    if source.suffix.lower()!='.html':raise ValueError('HTML source required')
    try:
        compatible=(importlib.metadata.version('weasyprint').split('.')[0]=='70'
                    and importlib.util.find_spec('weasyprint') is not None)
    except importlib.metadata.PackageNotFoundError:
        compatible=False
    if not compatible:raise RendererUnavailable('WeasyPrint unavailable or version not qualified; supported major is 70')
    if importlib.util.find_spec('weasyprint') is None:raise RendererUnavailable('WeasyPrint unavailable; operator dependency action required')
    try:
        from weasyprint import HTML,CSS,__version__
    except (ImportError,OSError) as exc:
        raise RendererUnavailable('WeasyPrint dependencies unavailable in this interpreter') from exc
    text=source.read_text(encoding='utf-8')
    from weasyprint.urls import URLFetcher
    from weasyprint.urls import FatalURLFetchingError
    if __version__.split('.')[0]!='70':raise RendererUnavailable('WeasyPrint version not qualified; supported major is 70')
    if re.search(r'@import|@font-face|<!ENTITY',text,re.I):raise ValueError('external CSS, custom fonts and entities denied')
    fetcher=URLFetcher(allowed_protocols=(),allow_redirects=False,fail_on_errors=True)
    with tempfile.TemporaryDirectory(prefix='jai-html-pdf-') as directory:
        result=Path(directory)/'result.pdf'
        try:
            HTML(string=text,base_url='file:///__jai_resource_denied__/',url_fetcher=fetcher).write_pdf(result,stylesheets=[CSS(string='body { font-family: "DejaVu Sans", sans-serif; }')])
        except FatalURLFetchingError as exc:raise ValueError('render attempted an unapproved resource fetch') from exc
        if not result.read_bytes().startswith(b'%PDF-'):raise RuntimeError('native HTML renderer produced no PDF')
        target=out/(source.stem+'.pdf');shutil.copyfile(result,target)
    try:pyphen_version=importlib.metadata.version('pyphen')
    except importlib.metadata.PackageNotFoundError:pyphen_version='metadata unavailable'
    evidence={'backend':'WeasyPrint','version':__version__,'python':sys.executable,'pyphen':pyphen_version,'execution':'in-process','source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'output_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'resources':'deny all URL fetches; no custom font-face; system DejaVu Sans','office_visual_evidence':False}
    target.with_suffix('.renderer.json').write_text(json.dumps(evidence,indent=2)+'\n')
    return target


def validate_svg(source):
    """Reject SVG external resources/entities before a local rasterizer sees them."""
    import re,xml.etree.ElementTree as ET
    text=Path(source).read_text(encoding='utf-8')
    if re.search(r'<!DOCTYPE|<!ENTITY',text,re.I):raise ValueError('SVG declarations/entities denied')
    root=ET.fromstring(text)
    for node in root.iter():
        for key,value in node.attrib.items():
            if key.rsplit('}',1)[-1] in {'href','src'} and not value.startswith('#'):raise ValueError('SVG external resource denied')
        styles=[node.text or ''] if node.tag.rsplit('}',1)[-1]=='style' else []
        styles+=[value for key,value in node.attrib.items() if key=='style' or 'url' in value.lower()]
        for css in styles:
            if '\\' in css or re.search(r'@import|@font-face',css,re.I):raise ValueError('SVG external styling denied')
            for url in re.findall(r'url\s*\((.*?)\)',css,re.I):
                if not url.strip(' \t\r\n\'"').startswith('#'):raise ValueError('SVG URL denied')
    return True
