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


def html_pdf(source,output_directory,backend='auto'):
    """Render actual HTML independently of Office when WeasyPrint is installed.

    Only embedded content and protected system fonts are supported. All resource
    fetches and custom font loads deny; an attempted fetch fails the render rather
    than silently replacing content. HTML PDF is never Office visual evidence.
    """
    import importlib.util,importlib.metadata,re,hashlib
    source=Path(source).resolve(strict=True);out=Path(output_directory);out.mkdir(parents=True,exist_ok=True)
    if backend not in {'auto','weasyprint','libreoffice'} or source.suffix.lower()!='.html':raise ValueError('explicit HTML backend required')
    try:
        compatible=(importlib.metadata.version('weasyprint').split('.')[0]=='70'
                    and importlib.util.find_spec('weasyprint') is not None)
    except importlib.metadata.PackageNotFoundError:
        compatible=False
    if backend=='libreoffice' or (backend=='auto' and not compatible):
        return convert_office(source,out)
    if importlib.util.find_spec('weasyprint') is None:raise RendererUnavailable('WeasyPrint unavailable; operator dependency action required')
    try:
        from weasyprint import HTML,CSS,__version__
    except (ImportError,OSError) as exc:
        if backend=='auto':return convert_office(source,out)
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
            HTML(string=text,url_fetcher=fetcher).write_pdf(result,stylesheets=[CSS(string='body { font-family: "DejaVu Sans", sans-serif; }')])
        except FatalURLFetchingError as exc:raise ValueError('render attempted an unapproved resource fetch') from exc
        if not result.read_bytes().startswith(b'%PDF-'):raise RuntimeError('native HTML renderer produced no PDF')
        target=out/(source.stem+'.pdf');shutil.copyfile(result,target)
    evidence={'backend':'WeasyPrint','version':__version__,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'output_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'resources':'deny all URL fetches; no custom font-face; system DejaVu Sans','office_visual_evidence':False}
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
