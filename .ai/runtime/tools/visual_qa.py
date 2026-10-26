#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Render-based visual QA v2 for DOCX/PPTX/XLSX/HTML/SVG/PDF.

The gate inspects what a human sees. Office formats are converted through LibreOffice,
HTML through native LibreOffice print rendering, SVG through CairoSVG, and PDFs through pdftoppm.
Image checks are deterministic and focus on release-critical rendering defects; package-
level format checks remain complementary in publication.py.
"""
from __future__ import annotations
import argparse, json, math, os, re, shutil, subprocess, tempfile
from pathlib import Path
from PIL import Image, ImageStat
from office_renderer import convert_office, html_pdf, validate_svg

CRITICAL={'blank','edge-clipping','render-failed','tiny-page','broken-diagram'}

def run(cmd,timeout=90):
    """Run an explicit renderer argument vector with bounded execution.

    Args:
        cmd: Renderer executable and arguments; shell evaluation is not used.
        timeout: Maximum seconds before subprocess.TimeoutExpired is raised.
    Returns:
        Completed process including exit code and captured text diagnostics.
    Raises:
        OSError: Executable cannot start.
        subprocess.TimeoutExpired: Native command exceeds its bound.
    """
    return subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,timeout=timeout)

def pdf_pages(pdf,out):
    """Rasterize a real PDF through the installed Poppler renderer.

    Args:
        pdf: Existing PDF selected for visual inspection.
        out: Generated PNG directory.
    Returns:
        Sorted PNG page paths after a successful native conversion.
    Raises:
        RuntimeError: Poppler rejects the input or conversion fails.
        OSError: Renderer or output cannot be accessed.
    """
    Path(out).mkdir(parents=True,exist_ok=True)
    pref=Path(out)/'page'; r=run(['pdftoppm','-png','-r','120',str(pdf),str(pref)])
    if r.returncode: raise RuntimeError(r.stderr[-1000:])
    return sorted(Path(out).glob('page-*.png'))

def render_to_images(path,out,backend="auto"):
    """Render supported content using native Office, Poppler or CairoSVG engines.

    Args:
        path: Local DOCX/PPTX/XLSX/HTML/SVG/PDF source.
        out: Generated render directory; native Office uses a private profile.
    Returns:
        Real raster page paths, never synthetic replacements for a failed engine.
    Raises:
        ValueError: Unsupported format.
        RuntimeError: Native renderer/prerequisite fails.
        OSError: Source or destination is unavailable.
    """
    p=Path(path); ext=p.suffix.lower(); out=Path(out); out.mkdir(parents=True,exist_ok=True)
    if ext=='.pdf': return pdf_pages(p,out)
    if ext in ('.docx','.pptx','.xlsx'):
        pdfdir=out/'lo'; pdfdir.mkdir(exist_ok=True)
        pdf=convert_office(p,pdfdir,timeout=120)
        return pdf_pages(pdf,out/'pages')
    if ext=='.html':
        # LibreOffice provides a deterministic print rendering in CI; browser screenshot may be used by deployments.
        pdfdir=out/'html'; pdfdir.mkdir(exist_ok=True)
        pdf=html_pdf(p,pdfdir,backend=backend)
        return pdf_pages(pdf,out/'pages')
    if ext=='.svg':
        validate_svg(p)
        import cairosvg
        png=out/'page-1.png'; cairosvg.svg2png(url=str(p),write_to=str(png),output_width=1400)
        return [png]
    raise ValueError('unsupported format '+ext)

def image_findings(img_path):
    """Judge visible pixels on white publication paper using unchanged QA limits.

    Args:
        img_path: Existing raster image, possibly with transparent SVG pixels.
    Returns:
        Located quality findings. Alpha is composited onto white paper before
        luminance analysis, so invisible RGB bytes cannot create false clipping
        or hide an actually blank page. Opaque clipping remains critical.
    Raises:
        OSError: Raster image cannot be read.
    """
    with Image.open(img_path) as source:
        rgba=source.convert('RGBA')
        paper=Image.new('RGBA',rgba.size,'white')
        im0=Image.alpha_composite(paper,rgba).convert('L')
    ow,oh=im0.size; f=[]
    if ow<300 or oh<300: f.append(('tiny-page','critical','rendered page is unexpectedly small'))
    scale=min(1.0,500/max(ow,oh)); im=im0.resize((max(1,int(ow*scale)),max(1,int(oh*scale)))) if scale<1 else im0
    w,h=im.size
    stat=ImageStat.Stat(im); mean=stat.mean[0]; std=stat.stddev[0]
    if mean>248 and std<8: f.append(('blank','critical','page is empty or nearly empty'))
    # edge clipping heuristic: significant dark ink touches a 2px outer edge.
    pix=im.load(); threshold=160
    edge=sum(1 for x in range(w) for y in (0,1,h-2,h-1) if pix[x,y]<threshold)+sum(1 for y in range(h) for x in (0,1,w-2,w-1) if pix[x,y]<threshold)
    denom=max(1,4*w+4*h)
    if edge/denom>0.012: f.append(('edge-clipping','critical',f'ink touches outer render edge ({edge/denom:.2%})'))
    # high density is a warning, not a release blocker.
    thumb=im.resize((max(1,w//4),max(1,h//4)))
    pixels=thumb.get_flattened_data() if hasattr(thumb,'get_flattened_data') else thumb.getdata(); ink=sum(1 for v in pixels if v<210)/max(1,thumb.width*thumb.height)
    if ink>0.34: f.append(('excessive-density','warning',f'ink density {ink:.1%}'))
    return f

def source_findings(path):
    """Check source document-control and diagram structure before rendering.

    Args:
        path: Local SVG/HTML or other supported source.
    Returns:
        Code, severity and explanation tuples; no source change is performed.
    Raises:
        OSError: Source cannot be read.
    """
    p=Path(path); ext=p.suffix.lower(); f=[]
    if ext=='.svg':
        t=p.read_text(encoding='utf-8',errors='ignore')
        if '<svg' not in t or '</svg>' not in t: f.append(('broken-diagram','critical','invalid SVG root'))
        if '<text' not in t: f.append(('missing-legend','warning','diagram has no visible labels'))
    if ext=='.html':
        t=p.read_text(encoding='utf-8',errors='ignore')
        if '<title' not in t or '<h1' not in t: f.append(('document-control','critical','HTML title/H1 missing'))
        if 'classification' not in t.lower(): f.append(('missing-classification','critical','classification marker missing'))
    return f

def qa(path,keep=None):
    """Combine source checks and actual rendered-page findings without bypasses.

    Args:
        path: Local publication to inspect.
        keep: Optional caller-selected directory retaining real raster evidence.
    Returns:
        Findings including a critical render-failed record if conversion cannot
        run. Missing rendering is never promoted to visual PASS.
    """
    findings=source_findings(path)
    try:
        if keep:
            pages=render_to_images(path,keep)
            for i,p in enumerate(pages,1):
                for code,sev,msg in image_findings(p): findings.append((code,sev,f'page {i}: {msg}'))
        else:
            with tempfile.TemporaryDirectory() as td:
                pages=render_to_images(path,td)
                for i,p in enumerate(pages,1):
                    for code,sev,msg in image_findings(p): findings.append((code,sev,f'page {i}: {msg}'))
    except Exception as e: findings.append(('render-failed','critical',str(e)))
    return findings

def make_seed(path,kind,valid=True):
    from PIL import Image,ImageDraw
    im=Image.new('RGB',(450,600),'white'); d=ImageDraw.Draw(im)
    if valid:
        d.text((80,80),'Enterprise Architecture Review',fill='black'); d.rectangle((40,80,410,500),outline='black',width=2)
        for y in range(100,470,35): d.text((55,y),'Decision evidence and architecture content',fill='black')
    elif kind=='blank': pass
    elif kind=='edge-clipping': d.rectangle((0,0,449,599),outline='black',width=8); d.text((0,250),'CLIPPED CONTENT',fill='black')
    elif kind=='excessive-density':
        for y in range(0,600,6): d.line((0,y,449,y),fill='black',width=4)
    im.save(path)

def self_test():
    """Execute seeded visual thresholds and required real HTML/SVG render checks.

    Returns:
        Zero only when all checks pass; required unavailable renderers return one.
        Fixtures never establish provider, host or operator qualification.
    """
    tests=[]; tp=fp=fn=tn=0
    with tempfile.TemporaryDirectory() as td:
        td=Path(td)
        # 120 valid + 120 seeded defects: acceptance corpus required by the GA baseline.
        for i in range(120):
            p=td/f'valid-{i}.png'; make_seed(p,'valid',True); fs=image_findings(p); pred=any(s=='critical' for _,s,_ in fs); tn+=not pred; fp+=pred
        kinds=['blank','edge-clipping']
        for i in range(120):
            kind=kinds[i%2]; p=td/f'defect-{i}.png'; make_seed(p,kind,False); fs=image_findings(p); pred=any(s=='critical' for _,s,_ in fs); tp+=pred; fn+=not pred
        recall=tp/(tp+fn); fpr=fp/(fp+tn)
        tests += [('critical-defect-recall>=95%',recall>=.95),('false-positive<=10%',fpr<=.10)]
        # Exercise the shipped publisher with substantive valid content. The old
        # three-line seed really renders nearly empty on A4 and correctly fails
        # the unchanged blank-page detector; it was not a valid positive fixture.
        from publication import render_html, load_json, DEFAULT_THEME
        html=td/'x.html'
        render_html({'title':'Architecture review', 'artifact_id':'VISUAL-POSITIVE',
            'owner':'Fictional service owner', 'classification':'Public synthetic',
            'audience':['Review board'], 'publication_status':'DRAFT_INCOMPLETE',
            'sections':[
                {'heading':'Decision scope', 'body':'This fictional decision paper compares a retained service with a managed recovery design. The board reviews the baseline, proposed operating model, measured recovery objective and remaining uncertainty before any real investment decision. No production approval or privileged execution is granted by this document.'},
                {'heading':'Options and evidence', 'body':'A synthetic rehearsal exceeded the recovery objective. The target design introduces bounded replay and explicit transaction verification. Cost, ownership and deployment readiness remain assumptions pending independent review. The baseline remains available until the service owner accepts tested recovery evidence.',
                 'table':{'headers':['Option','Recovery','Decision'], 'rows':[['Baseline','48 minutes','Retain pending review'],['Target','27 minutes assumed','Independent evidence required']]}},
                {'heading':'Risks and next action', 'body':'The receiving service owner must verify replay integrity, peak load behavior and operator readiness. Rollback preserves the existing service. Evidence and approval are separate from local document production. This public fixture exercises visible headings, text, tables and document control through the actual publication renderer.'}]},html,load_json(DEFAULT_THEME))
        fs=qa(html); tests.append(('html-render',not any(severity=='critical' for _,severity,_ in fs)))
        if any(severity=='critical' for _,severity,_ in fs):
            for finding in fs: print('HTML finding:',*finding)
        # SVG render smoke
        svg=td/'x.svg'; svg.write_text('<svg xmlns="http://www.w3.org/2000/svg" width="800" height="600"><text x="40" y="80">Architecture</text><rect x="40" y="120" width="700" height="400" fill="none" stroke="black"/></svg>')
        fs=qa(svg); tests.append(('svg-render',not any(severity=='critical' for _,severity,_ in fs)))
    for n,v in tests: print(('PASS' if v else 'FAIL'),n)
    print(f'recall={recall:.3f} fpr={fpr:.3f}'); print(f"{sum(v for _,v in tests)}/{len(tests)} PASS")
    return 0 if all(v for _,v in tests) else 1

def main():
    ap=argparse.ArgumentParser();sp=ap.add_subparsers(dest='cmd',required=True);q=sp.add_parser('qa');q.add_argument('path');q.add_argument('--keep-rendered');sp.add_parser('self-test');a=ap.parse_args()
    if a.cmd=='self-test': raise SystemExit(self_test())
    fs=qa(a.path,a.keep_rendered); [print(sev.upper(),code,msg) for code,sev,msg in fs]; critical=[x for x in fs if x[1]=='critical']; print('PASS' if not critical else 'FAILED'); raise SystemExit(1 if critical else 0)
if __name__=='__main__': main()
