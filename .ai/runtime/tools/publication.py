#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Enterprise publication pipeline for AI IT House.

Truth layer: a JSON publication model with claims/evidence and structured sections.
Publication layer: deterministic HTML, DOCX, PDF, PPTX, XLSX and SVG outputs.
No renderer may change semantic claims or decisions; a semantic SHA-256 is embedded in outputs.

Commands:
  publication.py validate MODEL.json
  publication.py render MODEL.json --manifest MANIFEST.json --format html|docx|pdf|pptx|xlsx|svg|all --out DIR [--theme FILE]
  publication.py qa PATH [--theme FILE]
  publication.py self-test
"""
from __future__ import annotations
import argparse, hashlib, html, json, math, os, re, shutil, sys, tempfile, textwrap, zipfile
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, tostring

ROOT=Path(__file__).resolve().parents[1]
PACKAGE=ROOT.parents[1]
RELEASE=((PACKAGE/'VERSION') if (PACKAGE/'VERSION').is_file() else ROOT/'VERSION').read_text().strip()
DEFAULT_THEME=ROOT/'publication/themes/enterprise-default.json'


def load_json(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def canonical(obj): return json.dumps(obj,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def semantic_hash(model): return hashlib.sha256(canonical(model)).hexdigest()
def clean_xml(s): return ''.join(c for c in str(s) if c=='\t' or c=='\n' or c=='\r' or ord(c)>=32)
def esc(s): return html.escape(str(s),quote=True)

def validate_model(m):
    """Validate structure and substantive section presence; headings alone are invalid.

    Args:
        m: Publication model dictionary.
    Returns:
        Located structural and existing claim/evidence errors.
    """
    from projection import section_has_content
    probs=[]
    for k in ('title','artifact_id','audience','owner','classification','sections'):
        if not m.get(k): probs.append(f'missing/empty {k}')
    if not isinstance(m.get('audience',[]),list): probs.append('audience must be array')
    if not isinstance(m.get('sections',[]),list): probs.append('sections must be array')
    claims=m.get('claims',[])
    seen=set()
    for i,c in enumerate(claims):
        for k in ('id','statement','basis'):
            if not c.get(k): probs.append(f'claims[{i}] missing {k}')
        if c.get('id') in seen: probs.append(f'duplicate claim id {c.get("id")}')
        seen.add(c.get('id'))
        if c.get('basis') not in ('stated','inferred','assumed'): probs.append(f'claim {c.get("id")} invalid basis')
        if c.get('basis')=='stated' and not c.get('evidence'): probs.append(f'claim {c.get("id")} stated without evidence')
    for i,s in enumerate(m.get('sections',[])):
        if not s.get('heading'): probs.append(f'sections[{i}] missing heading')
        if not section_has_content(s): probs.append(f'sections[{i}] has no substantive content')
        if 'diagram' in s and s['diagram']:
            probs += [f'sections[{i}].diagram: {x}' for x in validate_diagram(s['diagram'])]
    return probs

def validate_native_jai(m):
    probs=[]; j=m.get('jai')
    if not isinstance(j,dict): return ['missing JAI publication lineage']
    for k in ('intent_ref','semantic_snapshot_ref','policy_ref','design_ref','realisation_ref','evidence_refs'):
        if k not in j or (k!='evidence_refs' and not str(j.get(k,'')).strip()): probs.append(f'JAI publication lineage missing {k}')
    if not isinstance(j.get('evidence_refs'),list): probs.append('JAI evidence_refs must be array')
    if not m.get('profile_id'): probs.append('missing publication profile_id')
    return probs

def validate_diagram(d):
    probs=[]; ids=set()
    if not d.get('title'): probs.append('missing title')
    for i,n in enumerate(d.get('nodes',[])):
        if not n.get('id') or not n.get('label'): probs.append(f'node[{i}] needs id,label')
        if n.get('id') in ids: probs.append(f'duplicate node {n.get("id")}')
        ids.add(n.get('id'))
    for i,e in enumerate(d.get('edges',[])):
        if e.get('from') not in ids or e.get('to') not in ids: probs.append(f'edge[{i}] references missing node')
    return probs

def markdown_text(m):
    out=[f"# {m['title']}",'']
    if m.get('subtitle'): out += [m['subtitle'],'']
    out += [f"**Artifact ID:** {m['artifact_id']}",f"**Owner:** {m['owner']}",f"**Classification:** {m['classification']}",f"**Semantic hash:** `{semantic_hash(m)}`",'']
    for s in m['sections']:
        out += [f"## {s['heading']}",'']
        if s.get('body'): out += [s['body'],'']
        for b in s.get('bullets',[]): out.append(f'- {b}')
        if s.get('bullets'): out.append('')
        t=s.get('table') or {}
        if t.get('headers'):
            hs=t['headers']; out += ['| '+' | '.join(map(str,hs))+' |','| '+' | '.join(['---']*len(hs))+' |']
            for r in t.get('rows',[]): out.append('| '+' | '.join(map(str,r))+' |')
            out.append('')
    return '\n'.join(out)

def render_html(m,out,theme):
    h=semantic_hash(m); sections=[]
    for s in m['sections']:
        body=f"<p>{esc(s.get('body',''))}</p>" if s.get('body') else ''
        bullets=''.join(f'<li>{esc(x)}</li>' for x in s.get('bullets',[])); bullets=f'<ul>{bullets}</ul>' if bullets else ''
        table=''; t=s.get('table') or {}
        if t.get('headers'):
            th=''.join(f'<th>{esc(x)}</th>' for x in t['headers'])
            tr=''.join('<tr>'+''.join(f'<td>{esc(x)}</td>' for x in row)+'</tr>' for row in t.get('rows',[]))
            table=f'<table><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>'
        sections.append(f"<section><h2>{esc(s['heading'])}</h2>{body}{bullets}{table}</section>")
    css="""body{font-family:Arial,sans-serif;max-width:1120px;margin:36px auto;padding:0 28px;line-height:1.45;color:#171717}header{border-bottom:2px solid #333;padding-bottom:18px;margin-bottom:26px}.meta{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:6px 20px;font-size:13px}h1{font-size:32px;margin-bottom:6px}h2{font-size:22px;margin-top:30px;border-bottom:1px solid #ddd;padding-bottom:6px}table{border-collapse:collapse;width:100%;font-size:13px}th,td{border:1px solid #bbb;padding:7px;vertical-align:top}th{background:#eee}footer{margin-top:40px;border-top:1px solid #bbb;padding-top:10px;font-size:11px}@media print{body{max-width:none;margin:0}.no-print{display:none}}"""
    doc=f'''<!doctype html><html><head><meta charset="utf-8"><title>{esc(m['title'])}</title><style>{css}</style><meta name="semantic-sha256" content="{h}"></head><body><header><h1>{esc(m['title'])}</h1><div>{esc(m.get('subtitle',''))}</div><div class="meta"><div><b>Artifact:</b> {esc(m['artifact_id'])}</div><div><b>Owner:</b> {esc(m['owner'])}</div><div><b>Audience:</b> {esc(', '.join(m['audience']))}</div><div><b>Classification:</b> {esc(m['classification'])}</div><div><b>Version:</b> {esc(m.get('version',''))}</div><div><b>Semantic hash:</b> {h[:16]}…</div></div></header>{''.join(sections)}<footer>{esc(m['classification'])} · {esc(m['artifact_id'])} · semantic SHA-256 {h}</footer></body></html>'''
    Path(out).write_text(doc,encoding='utf-8')

def xml(tag,attrs=None,text=None):
    e=Element(tag,attrs or {}); e.text=clean_xml(text) if text is not None else None; return e

def docx_para(text,style=None,bold=False):
    p=Element('w:p')
    if style:
        pp=SubElement(p,'w:pPr'); SubElement(pp,'w:pStyle',{'w:val':style})
    r=SubElement(p,'w:r')
    if bold:
        rp=SubElement(r,'w:rPr'); SubElement(rp,'w:b')
    t=SubElement(r,'w:t'); t.text=clean_xml(text)
    return p

def render_docx(m,out,theme):
    h=semantic_hash(m); ns='http://schemas.openxmlformats.org/wordprocessingml/2006/main'
    body=[]; body.append(docx_para(m['title'],'Title')); 
    if m.get('subtitle'): body.append(docx_para(m['subtitle'],'Subtitle'))
    for x in [f"Artifact ID: {m['artifact_id']}",f"Owner: {m['owner']}",f"Audience: {', '.join(m['audience'])}",f"Classification: {m['classification']}",f"Semantic SHA-256: {h}"]:
        body.append(docx_para(x))
    for s in m['sections']:
        body.append(docx_para(s['heading'],'Heading1'))
        if s.get('body'): body.append(docx_para(s['body']))
        for b in s.get('bullets',[]): body.append(docx_para('• '+b))
        t=s.get('table') or {}
        if t.get('headers'):
            tbl=Element('w:tbl'); rows=[t['headers']]+t.get('rows',[])
            for ri,row in enumerate(rows):
                tr=SubElement(tbl,'w:tr')
                for cell in row:
                    tc=SubElement(tr,'w:tc'); tc.append(docx_para(str(cell),bold=(ri==0)))
            body.append(tbl)
    body.append(docx_para(f"{m['classification']} · {m['artifact_id']} · {h}"))
    document=Element('w:document',{'xmlns:w':ns}); b=SubElement(document,'w:body'); [b.append(x) for x in body]; SubElement(b,'w:sectPr')
    types='''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/><Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/></Types>'''
    rels='''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>'''
    docrels='''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/></Relationships>'''
    styles=f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:styles xmlns:w="{ns}"><w:style w:type="paragraph" w:styleId="Normal"><w:name w:val="Normal"/></w:style><w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:rPr><w:b/><w:sz w:val="36"/></w:rPr></w:style><w:style w:type="paragraph" w:styleId="Subtitle"><w:name w:val="Subtitle"/><w:rPr><w:i/><w:sz w:val="24"/></w:rPr></w:style><w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:rPr><w:b/><w:sz w:val="28"/></w:rPr></w:style></w:styles>'''
    with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml',types); z.writestr('_rels/.rels',rels); z.writestr('word/_rels/document.xml.rels',docrels); z.writestr('word/styles.xml',styles); z.writestr('word/document.xml',b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'+tostring(document,encoding='utf-8'))

def slide_xml(title,lines):
    """Build slide XML from an already paginated line sequence.

    Args:
        title: Slide title.
        lines: Text lines; caller paginates for visual density.
    Returns:
        Slide XML string.
    """
    def tx(text,y,size=1800,bold=False):
        return f'''<p:sp><p:nvSpPr><p:cNvPr id="{y}" name="Text {y}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr><p:spPr><a:xfrm><a:off x="685800" y="{y*40000}"/><a:ext cx="10800000" cy="520000"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/></p:spPr><p:txBody><a:bodyPr wrap="square"/><a:lstStyle/><a:p><a:r><a:rPr lang="en-US" sz="{size}" b="{'1' if bold else '0'}"/><a:t>{esc(text)}</a:t></a:r><a:endParaRPr lang="en-US"/></a:p></p:txBody></p:sp>'''
    shapes=tx(title,20,2600,True)
    y=48
    for line in lines: shapes+=tx(line,y,1600,False); y+=13
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"><p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>{shapes}</p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sld>'''

def render_pptx(m,out,theme):
    """Write a draft presentation retaining all section lines across continued slides.

    Args:
        m: Verified draft model.
        out: Destination PPTX path.
        theme: Presentation theme.
    Raises:
        OSError: If the output file cannot be written.
    """
    slides=[]
    cover=[m.get('subtitle',''),f"Owner: {m['owner']}",f"Classification: {m['classification']}",f"Semantic hash: {semantic_hash(m)[:16]}…"]
    slides.append((m['title'],[x for x in cover if x]))
    for s in m['sections']:
        lines=[]
        if s.get('body'): lines += [x.strip() for x in re.split(r'(?<=[.!?])\s+',s['body']) if x.strip()]
        lines += ['• '+x for x in s.get('bullets',[])]
        t=s.get('table') or {}
        if t.get('headers'): lines.append(' | '.join(map(str,t['headers']))); lines += [' | '.join(map(str,r)) for r in t.get('rows',[])]
        lines=[wrapped for line in lines for paragraph in str(line).splitlines() for wrapped in (textwrap.wrap(paragraph,width=80,replace_whitespace=False,drop_whitespace=False) or [''])]
        for start in range(0,max(1,len(lines)),8):
            slides.append((s['heading']+(' (continued)' if start else ''),lines[start:start+8] or ['']))
    n=len(slides)
    types=['''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>''']
    for i in range(1,n+1): types.append(f'<Override PartName="/ppt/slides/slide{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>')
    types.append('</Types>')
    ids=''.join(f'<p:sldId id="{255+i}" r:id="rId{i}"/>' for i in range(1,n+1))
    pres=f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"><p:sldIdLst>{ids}</p:sldIdLst><p:sldSz cx="12192000" cy="6858000"/><p:notesSz cx="6858000" cy="9144000"/></p:presentation>'''
    rootrels='''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/></Relationships>'''
    prels='<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'+''.join(f'<Relationship Id="rId{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide{i}.xml"/>' for i in range(1,n+1))+'</Relationships>'
    with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml',''.join(types)); z.writestr('_rels/.rels',rootrels); z.writestr('ppt/presentation.xml',pres); z.writestr('ppt/_rels/presentation.xml.rels',prels)
        for i,(title,lines) in enumerate(slides,1): z.writestr(f'ppt/slides/slide{i}.xml',slide_xml(title,lines))

def colname(n):
    s=''
    while n: n,r=divmod(n-1,26); s=chr(65+r)+s
    return s

def render_xlsx(m,out,theme):
    """Write a draft workbook retaining prose sections as content worksheets.

    Args:
        m: Verified draft model.
        out: Destination XLSX path.
        theme: Workbook theme.
    Raises:
        OSError: If the output file cannot be written.
    """
    sheets=[]
    # summary sheet plus one sheet per table section
    summary=[['Field','Value'],['Title',m['title']],['Artifact ID',m['artifact_id']],['Owner',m['owner']],['Classification',m['classification']],['Semantic SHA-256',semantic_hash(m)]]
    sheets.append(('Summary',summary))
    for i,s in enumerate(m['sections'],1):
        t=s.get('table') or {}
        if s.get('body'): sheets.append((f'Content {i}',[['Section','Content'],[s['heading'],s['body']]]))
        if t.get('headers'): sheets.append(((s['heading'][:28] or f'Section{i}'),[t['headers']]+t.get('rows',[])))
    types=['''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>''']
    for i in range(1,len(sheets)+1): types.append(f'<Override PartName="/xl/worksheets/sheet{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>')
    types.append('</Types>')
    rootrels='''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>'''
    sh=''.join(f'<sheet name="{esc(name)}" sheetId="{i}" r:id="rId{i}"/>' for i,(name,_) in enumerate(sheets,1))
    wb=f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets>{sh}</sheets></workbook>'''
    wrels='<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'+''.join(f'<Relationship Id="rId{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet{i}.xml"/>' for i in range(1,len(sheets)+1))+'</Relationships>'
    with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml',''.join(types)); z.writestr('_rels/.rels',rootrels); z.writestr('xl/workbook.xml',wb); z.writestr('xl/_rels/workbook.xml.rels',wrels)
        for si,(name,rows) in enumerate(sheets,1):
            rs=[]
            for ri,row in enumerate(rows,1):
                cells=[]
                for ci,val in enumerate(row,1): cells.append(f'<c r="{colname(ci)}{ri}" t="inlineStr"><is><t>{esc(val)}</t></is></c>')
                rs.append(f'<row r="{ri}">'+''.join(cells)+'</row>')
            sx='<?xml version="1.0" encoding="UTF-8" standalone="yes"?><worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetData>'+''.join(rs)+'</sheetData></worksheet>'
            z.writestr(f'xl/worksheets/sheet{si}.xml',sx)

def render_svg_diagram(d,out,theme):
    probs=validate_diagram(d)
    if probs: raise ValueError('; '.join(probs))
    nodes=d.get('nodes',[]); edges=d.get('edges',[]); W=theme['diagram']['node_width']; H=theme['diagram']['node_height']; hg=theme['diagram']['h_gap']; vg=theme['diagram']['v_gap']; cols=max(1,math.ceil(math.sqrt(len(nodes))))
    pos={}
    for i,n in enumerate(nodes):
        x=40+(i%cols)*(W+hg); y=80+(i//cols)*(H+vg); pos[n['id']]=(x,y)
    width=max(800,80+cols*(W+hg)); rows=math.ceil(len(nodes)/cols); height=max(400,140+rows*(H+vg))
    parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}"><defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#444"/></marker></defs><style>text{{font-family:Arial,sans-serif;fill:#111}}.node{{fill:#fff;stroke:#444;stroke-width:1.5}}.edge{{stroke:#555;stroke-width:1.5;marker-end:url(#arrow)}}</style><text x="40" y="35" font-size="24" font-weight="bold">{esc(d["title"])}</text>']
    for e in edges:
        x1,y1=pos[e['from']]; x2,y2=pos[e['to']]; x1+=W/2; y1+=H/2; x2+=W/2; y2+=H/2
        parts.append(f'<line class="edge" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>')
        if e.get('label'): parts.append(f'<text x="{(x1+x2)/2}" y="{(y1+y2)/2-5}" font-size="11">{esc(e["label"])}</text>')
    for n in nodes:
        x,y=pos[n['id']]; parts.append(f'<rect class="node" x="{x}" y="{y}" width="{W}" height="{H}" rx="8"/><text x="{x+12}" y="{y+28}" font-size="14" font-weight="bold">{esc(n["label"])}</text>')
        if n.get('description'): parts.append(f'<text x="{x+12}" y="{y+49}" font-size="11">{esc(n["description"][:45])}</text>')
    parts.append('</svg>'); Path(out).write_text(''.join(parts),encoding='utf-8')

def render_svg(m,out,theme):
    """Write a diagram SVG with complete semantic-unit description metadata.

    Args:
        m: Verified draft model.
        out: Destination SVG path.
        theme: Diagram theme.
    Raises:
        OSError: If the output file cannot be written.
    """
    ds=[s.get('diagram') for s in m['sections'] if s.get('diagram')]
    if not ds:
        ds=[{'title':m['title'],'kind':'relationship','nodes':[{'id':'source','label':'Semantic source'},{'id':'publication','label':'Enterprise publication'}],'edges':[{'from':'source','to':'publication','label':'render'}]}]
    render_svg_diagram(ds[0],out,theme)
    # Mandatory prose is visibly rendered rather than hidden in SVG metadata.
    if m.get('semantic_units'):
        text=Path(out).read_text(encoding='utf-8')
        original_height=int(re.search(r'height="(\d+)"',text).group(1))
        lines=[line for section in m.get('sections',[]) for paragraph in ([section.get('heading','')]+str(section.get('body','')).splitlines()) for line in (textwrap.wrap(paragraph,width=100,replace_whitespace=False,drop_whitespace=False) or [''])]
        height=original_height+50+22*len(lines)
        text=re.sub(r'height="\d+"',f'height="{height}"',text,count=1)
        text=re.sub(r'viewBox="0 0 (\d+) \d+"',lambda match:f'viewBox="0 0 {match.group(1)} {height}"',text,count=1)
        panel=f'<rect x="0" y="{original_height}" width="100%" height="{height-original_height}" fill="white"/>'
        panel+=''.join(f'<text x="30" y="{original_height+35+22*i}" font-size="14">{esc(line)}</text>' for i,line in enumerate(lines))
        Path(out).write_text(text.replace('</svg>',panel+'</svg>'),encoding='utf-8')


def render_pdf(m,out,theme):
    """Convert a DOCX draft using an isolated, writable LibreOffice profile.

    Args:
        m: Verified draft publication model.
        out: PDF destination path.
        theme: Document theme.
    Raises:
        RuntimeError: If LibreOffice is unavailable or conversion fails.
        subprocess.TimeoutExpired: If conversion exceeds ninety seconds.
        OSError: If temporary files or output cannot be written.
    """
    with tempfile.TemporaryDirectory() as td:
        td=Path(td); docx=td/'source.docx'; render_docx(m,docx,theme)
        exe=shutil.which('libreoffice') or shutil.which('soffice')
        if not exe: raise RuntimeError('PDF renderer requires LibreOffice/soffice')
        import subprocess
        r=subprocess.run([exe,'-env:UserInstallation='+(td/'libreoffice-profile').as_uri(),'--headless','--convert-to','pdf','--outdir',str(td),str(docx)],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,timeout=90)
        pdf=td/'source.pdf'
        if r.returncode or not pdf.exists(): raise RuntimeError('PDF render failed: '+r.stderr[-500:])
        shutil.copyfile(pdf,out)

def _render_format(m,fmt,out,theme):
    {'html':render_html,'docx':render_docx,'pdf':render_pdf,'pptx':render_pptx,'xlsx':render_xlsx,'svg':render_svg}[fmt](m,out,theme)


def render(m,fmt,out,theme,manifest=None,directory=None,trusted_executions=None,authority=None):
    """Render only after independently checking the complete local QA bundle.

    Args:
        m: Publication model matching manifest projection hash.
        fmt: Supported output format name.
        out: Destination path.
        theme: Theme dictionary.
        manifest: Required DCS-bound projection manifest.
        directory: Required immutable sidecar directory.
        trusted_executions: Optional host runtime attestation verifier.
        authority: Optional existing JAI L0 authority verifier.
    Raises:
        ValueError: If verification inputs are absent or invalid.
        OSError: If output cannot be written.
    """
    if manifest is None or directory is None: raise ValueError('render requires verified DCS manifest and sidecars')
    return render_verified(m,manifest,directory,fmt,out,theme,trusted_executions=trusted_executions,authority=authority)

def render_verified(m,manifest,directory,fmt,out,theme,trusted_executions=None,authority=None):
    """Verify current immutable QA before rendering a clearly classified draft.

    Args:
        m: Publication model matching manifest hash.
        manifest: DCS-bound v4 projection manifest.
        directory: Directory containing the fixed QA sidecars.
        fmt: Output format.
        out: Destination path.
        theme: Theme dictionary.
        trusted_executions: Optional host runtime attestation verifier.
        authority: Optional existing JAI L0 authority verifier.
    Raises:
        ValueError: If current content QA or projection integrity fails.
        OSError: If rendering fails.
    """
    import publication_integrity
    problems=publication_integrity.verify_content(m,manifest,directory,trusted_executions=trusted_executions,authority=authority)
    if problems: raise ValueError('; '.join(problems))
    rendered=dict(m,publication_status='DRAFT_INCOMPLETE')
    rendered['subtitle']='DRAFT — content specification and professional approval pending. '+str(m.get('subtitle') or '')
    _render_format(rendered,fmt,out,theme)

def qa_file(path,theme):
    p=Path(path); ext=p.suffix.lower(); probs=[]; warnings=[]
    if not p.is_file(): return ['file missing'],[]
    if p.stat().st_size==0: probs.append('empty file')
    try:
        if ext in ('.docx','.pptx','.xlsx'):
            with zipfile.ZipFile(p) as z:
                names=z.namelist()
                if '[Content_Types].xml' not in names: probs.append('OOXML missing [Content_Types].xml')
                xmls=' '.join(z.read(n).decode('utf-8','ignore') for n in names if n.endswith('.xml'))
                if '<script' in xmls.lower(): probs.append('embedded script marker')
                if ext=='.pptx':
                    slides=[n for n in names if re.match(r'ppt/slides/slide\d+\.xml$',n)]
                    for s in slides:
                        txt=' '.join(re.findall(r'<a:t>(.*?)</a:t>',z.read(s).decode('utf-8','ignore')))
                        if len(txt.split())>theme.get('max_slide_words',85): warnings.append(f'{s}: {len(txt.split())} words exceeds slide density target')
                if ext=='.xlsx':
                    sheets=[n for n in names if re.match(r'xl/worksheets/sheet\d+\.xml$',n)]
                    if not sheets: probs.append('workbook has no worksheets')
        elif ext=='.pdf':
            if not p.read_bytes().startswith(b'%PDF-'): probs.append('not PDF')
        elif ext=='.html':
            txt=p.read_text(encoding='utf-8',errors='ignore')
            for tag in ('<title','<h1','semantic-sha256'): 
                if tag not in txt: probs.append(f'HTML missing {tag}')
        elif ext=='.svg':
            txt=p.read_text(encoding='utf-8',errors='ignore')
            if '<svg' not in txt: probs.append('not SVG')
            if len(re.findall(r'<text',txt))<2: warnings.append('diagram contains very little labelled content')
        else: warnings.append('no format-specific QA rule')
    except Exception as e: probs.append(f'cannot inspect: {e}')
    return probs,warnings

def self_test():
    m={'title':'Architecture Review','subtitle':'publication self-test','artifact_id':'TEST-001','profile_id':'architecture-review-board-pack','jai':{'intent_ref':'intent:TEST-001','semantic_snapshot_ref':'semantic-snapshot:test','policy_ref':'policy:publication:test','design_ref':'publication-design:test','realisation_ref':'renderer:publication.py@self-test','evidence_refs':['evidence:source:1']},'audience':['ARB'],'owner':'Solution Architect','approver':'ARB','classification':'Internal','version':'1.0','claims':[{'id':'C1','statement':'A stated fact','basis':'stated','evidence':['source:1']},{'id':'C2','statement':'An assumption','basis':'assumed'}],'sections':[{'heading':'Decision / ask','body':'Approve the target architecture.','bullets':['Option A selected','Residual risk accepted by owner'],'diagram':{'title':'Target flow','kind':'architecture','nodes':[{'id':'a','label':'Client'},{'id':'b','label':'Service'}],'edges':[{'from':'a','to':'b','label':'TLS'}]}},{'heading':'Risk register','table':{'headers':['Risk','Owner','Status'],'rows':[['R1','CISO','Open'],['R2','CIO','Mitigated']]}}],'acceptance_gates':['G1 semantic','G2 publication']}
    tests=[]
    def ok(name,cond): tests.append((name,bool(cond)))
    ok('model-valid',not validate_model(m) and not validate_native_jai(m)); h=semantic_hash(m); ok('hash-64',len(h)==64)
    with tempfile.TemporaryDirectory() as td:
        for fmt in ('html','docx','pdf','pptx','xlsx','svg'):
            p=Path(td)/('out.'+fmt); _render_format(dict(m,publication_status='DRAFT_INCOMPLETE'),fmt,p,load_json(DEFAULT_THEME)); ok(fmt+'-created',p.is_file() and p.stat().st_size>100); pr,w=qa_file(p,load_json(DEFAULT_THEME)); ok(fmt+'-qa',not pr)
        # deterministic HTML
        p1=Path(td)/'a.html'; p2=Path(td)/'b.html'; render_html(m,p1,{}); render_html(m,p2,{}); ok('html-deterministic',p1.read_bytes()==p2.read_bytes())
        # semantic hash embedded
        ok('html-hash-embedded',h in p1.read_text())
    for name,res in tests: print(('PASS' if res else 'FAIL'),name)
    passed=sum(x[1] for x in tests); print(f'{passed}/{len(tests)} PASS'); return 0 if passed==len(tests) else 1

def main():
    ap=argparse.ArgumentParser(); sp=ap.add_subparsers(dest='cmd',required=True)
    v=sp.add_parser('validate'); v.add_argument('model')
    r=sp.add_parser('render'); r.add_argument('model'); r.add_argument('--manifest',required=True,help='ProjectionManifest v3 proving L1-L6 lineage'); r.add_argument('--format',choices=['html','docx','pdf','pptx','xlsx','svg','all'],default='all'); r.add_argument('--out',required=True); r.add_argument('--theme',default=str(DEFAULT_THEME))
    q=sp.add_parser('qa'); q.add_argument('path'); q.add_argument('--theme',default=str(DEFAULT_THEME))
    sp.add_parser('self-test')
    a=ap.parse_args()
    if a.cmd=='self-test': raise SystemExit(self_test())
    theme=load_json(getattr(a,'theme',DEFAULT_THEME))
    if a.cmd=='validate':
        probs=validate_model(load_json(a.model)); print('OK' if not probs else 'FAILED'); [print(' -',p) for p in probs]; raise SystemExit(1 if probs else 0)
    if a.cmd=='qa':
        probs,w=qa_file(a.path,theme); [print('WARN',x) for x in w]; [print('FAIL',x) for x in probs]; print('OK' if not probs else 'FAILED'); raise SystemExit(1 if probs else 0)
    m=load_json(a.model); probs=validate_model(m)+validate_native_jai(m)
    if probs: [print(' -',p,file=sys.stderr) for p in probs]; raise SystemExit(2)
    import projection, publication_integrity
    man=load_json(a.manifest); probs=projection.validate_manifest(man)+publication_integrity.check(m,man)+publication_integrity.verify_content(m,man,Path(a.manifest).parent)
    if probs: [print(' -',p,file=sys.stderr) for p in probs]; raise SystemExit(2)
    if m.get('jai') != man.get('jai'): print(' - publication model JAI lineage differs from manifest',file=sys.stderr); raise SystemExit(2)
    out=Path(a.out); out.mkdir(parents=True,exist_ok=True)
    if (out/'render-evidence.json').exists() or (out/'render-evidence.json').is_symlink(): raise FileExistsError('immutable render evidence already exists; choose a new output directory')
    render_evidence={'release':RELEASE,'artifact_id':m['artifact_id'],'profile_id':m['profile_id'],'projection_hash':man['projection_hash'],'jai':man['jai'],'content_qa_ref':man['content_qa_ref'],'content_qa_hash':man['content_qa_hash'],'content_status':man['content_status'],'publication_status':'DRAFT_INCOMPLETE','render_status':'RENDER_SUCCESS','renders':{}}
    formats=['html','docx','pdf','pptx','xlsx','svg'] if a.format=='all' else [a.format]
    stem=re.sub(r'[^A-Za-z0-9._-]+','-',m['artifact_id']).strip('-').lower() or 'publication'
    for fmt in formats:
        p=out/f'{stem}.{fmt}'
        if p.exists() or p.is_symlink(): raise FileExistsError('render output already exists: '+str(p))
        render_verified(m,man,Path(a.manifest).parent,fmt,p,theme); pr,w=qa_file(p,theme)
        fh=hashlib.sha256(p.read_bytes()).hexdigest()
        render_evidence['renders'][fmt]={'sha256':fh,'qa':'PASS' if not pr else 'FAIL','warnings':w,'critical_defects':pr}
        print(f'{fmt}: {p} sha256={fh} semantic={semantic_hash(m)} qa={"PASS" if not pr else "FAIL"}')
        [print(' WARN',x) for x in w]
        if pr: [print(' FAIL',x) for x in pr]; raise SystemExit(3)
    with (out/'render-evidence.json').open('x',encoding='utf-8') as stream: stream.write(json.dumps(render_evidence,indent=2,ensure_ascii=False)+'\n')
if __name__=='__main__': main()
