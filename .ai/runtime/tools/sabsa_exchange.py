# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Deterministic CSV exchange and safe document layout for SABSA projections.

CSV is an editable projection of canonical Markdown, never a second authority.
"""
import csv
import hashlib
import io
import json
import re
from pathlib import Path
import zipfile
import xml.etree.ElementTree as ET

VERSION = "1"


def catalogue_schema(types):
    """Return versioned ordered per-type columns from the active metamodel.

    Args:
        types: Mapping of element types to field and relation specifications.
    Returns:
        JSON-compatible schema with fixed UTF-8, comma and LF serialization.
    """
    return {"schema_version": VERSION, "metamodel_version": json.loads((Path(__file__).resolve().parents[1] / "sabsa/schema/elements.json").read_text(encoding="utf-8"))["schema_version"],
            "relations": {t: {field: {"target_type": target, "required": required, "separator": ","}
                               for field, (target, required) in spec["links"].items()} for t, spec in sorted(types.items())}, "encoding": "utf-8", "delimiter": ",", "newline": "LF",
            "types": {t: list(dict.fromkeys(["id", "title", *s["fields"], *s["links"], "basis", "source"]))
                      for t, s in sorted(types.items())}}


def export_catalogues(entries, types, out):
    """Write sorted CSV catalogues, schema and source fingerprint to a directory.

    Args:
        entries: Canonical loaded entries, including read-only reused entries.
        types: Active metamodel mapping.
        out: Destination directory; existing named projections are replaced.
    Returns:
        The written schema dictionary.
    Raises:
        OSError: If output cannot be written.
    """
    out = Path(out); out.mkdir(parents=True, exist_ok=True)
    schema = catalogue_schema(types)
    hashes = {}
    for typ, columns in schema["types"].items():
        stream = io.StringIO(newline="")
        writer = csv.DictWriter(stream, fieldnames=columns, lineterminator="\n")
        writer.writeheader()
        for eid, entry in sorted(entries.items()):
            if entry["_dirtype"] == typ and not entry.get("_external"):
                writer.writerow({c: entry.get(c, "") for c in columns})
        data = stream.getvalue().encode("utf-8")
        (out / (typ + ".csv")).write_bytes(data)
        hashes[typ + ".csv"] = hashlib.sha256(data).hexdigest()
    (out / "schema.json").write_text(json.dumps(schema, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (out / "manifest.json").write_text(json.dumps({"schema_version": VERSION, "sha256": hashes}, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    return schema


def read_catalogues(directory, types, entries):
    """Validate edited CSV structure and stable identity; return proposed field updates.

    Args:
        directory: Export directory containing schema.json and all type CSVs.
        types: Active metamodel mapping.
        entries: Current canonical entries used to enforce stable IDs and types.
    Returns:
        Mapping of local IDs to CSV field dictionaries; no files are changed.
    Raises:
        ValueError: For schema drift, duplicate/missing/new IDs or unsafe metadata.
        OSError: For unreadable files.
    """
    directory = Path(directory)
    schema = catalogue_schema(types)
    if json.loads((directory / "schema.json").read_text(encoding="utf-8")) != schema:
        raise ValueError("CSV schema does not match the active metamodel/version")
    proposed = {}
    for typ, columns in schema["types"].items():
        with (directory / (typ + ".csv")).open(encoding="utf-8", newline="") as stream:
            reader = csv.DictReader(stream)
            if reader.fieldnames != columns:
                raise ValueError(f"{typ}: unexpected CSV columns/order")
            for row in reader:
                eid = row.get("id")
                if None in row or any(v is None for v in row.values()):
                    raise ValueError(f"{typ}: malformed CSV row")
                if eid in proposed or eid not in entries or entries[eid]["_dirtype"] != typ or entries[eid].get("_external"):
                    raise ValueError(f"{typ}: duplicate, new or nonlocal ID {eid}")
                if any(v != v.strip() or "\n" in v or "\r" in v or "\x00" in v or re.search(r"\s+#\s", v) for v in row.values()):
                    raise ValueError(f"{eid}: metadata must be single-line without inline-comment syntax")
                proposed[eid] = row
    expected = {eid for eid, e in entries.items() if not e.get("_external")}
    if set(proposed) != expected:
        raise ValueError("CSV must contain every local ID exactly once; deletion/creation uses sabsa new")
    return proposed


def format_docx(path):
    """Give Word tables explicit proportional widths and landscape wide-table sections.

    Args:
        path: Existing DOCX package to update in place.
    Returns:
        None. Text and all unrelated ZIP parts are preserved.
    Raises:
        OSError: For file failures.
        ValueError: For malformed Word XML.
    """
    ns = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
    ET.register_namespace("w", ns)
    q = lambda name: "{" + ns + "}" + name
    with zipfile.ZipFile(path) as archive:
        parts = {name: archive.read(name) for name in archive.namelist()}
    root = ET.fromstring(parts["word/document.xml"])
    body = root.find(q("body"))
    original_section = body.find(q("sectPr"))
    original_size = original_section.find(q("pgSz")) if original_section is not None else None
    original_margin = original_section.find(q("pgMar")) if original_section is not None else None
    page_width = int(original_size.get(q("w"), "11906")) if original_size is not None else 11906
    page_height = int(original_size.get(q("h"), "16838")) if original_size is not None else 16838
    margins = {side: original_margin.get(q(side), "1420") if original_margin is not None else "1420" for side in ("top", "bottom", "left", "right")}
    for table in list(body.iter(q("tbl"))):
        rows = table.findall(q("tr"))
        if not rows:
            continue
        cells = rows[0].findall(q("tc")); count = len(cells)
        wide = count >= 5
        width = (max(page_width, page_height) if wide else min(page_width, page_height)) - int(margins["left"]) - int(margins["right"])
        weights = []
        for index, cell in enumerate(cells):
            heading = " ".join(cell.itertext()).lower()
            values = [" ".join(r.findall(q("tc"))[index].itertext()) for r in rows if len(r.findall(q("tc"))) > index]
            weights.append(1 if heading.strip() in ("id", "identifier") else min(5, max(1.5, max(map(len, values), default=0) / 22)))
        widths = [int(width * weight / sum(weights)) for weight in weights]
        widths[-1] += width - sum(widths)
        grid = table.find(q("tblGrid"))
        if grid is not None: table.remove(grid)
        grid = ET.Element(q("tblGrid"))
        table.insert(list(table).index(rows[0]), grid)
        for value in widths: ET.SubElement(grid, q("gridCol"), {q("w"): str(value)})
        for row in rows:
            for index, cell in enumerate(row.findall(q("tc"))):
                props = cell.find(q("tcPr"))
                if props is None: props = ET.SubElement(cell, q("tcPr"))
                current = props.find(q("tcW"))
                if current is not None: props.remove(current)
                ET.SubElement(props, q("tcW"), {q("w"): str(widths[min(index, count-1)]), q("type"): "dxa"})
        if wide and table in list(body):
            def boundary(landscape):
                paragraph = ET.Element(q("p")); props = ET.SubElement(paragraph, q("pPr")); section = ET.SubElement(props, q("sectPr"))
                ET.SubElement(section, q("type"), {q("val"): "nextPage"})
                ET.SubElement(section, q("pgSz"), {q("w"): str(max(page_width, page_height) if landscape else min(page_width, page_height)), q("h"): str(min(page_width, page_height) if landscape else max(page_width, page_height)), q("orient"): "landscape" if landscape else "portrait"})
                ET.SubElement(section, q("pgMar"), {q(side): value for side, value in margins.items()})
                return paragraph
            index = list(body).index(table)
            body.insert(index, boundary(False)); body.insert(index + 2, boundary(True))
    parts["word/document.xml"] = ET.tostring(root, encoding="utf-8", xml_declaration=True)
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as archive:
        for name, data in parts.items(): archive.writestr(name, data)


def format_narrative_docx(path, metadata):
    """Add a controlled cover and populated clickable contents to a narrative Word document.

    Args:
        path: Existing Pandoc DOCX package updated in place.
        metadata: String title, viewpoint, organisation, owner, version, scope and approval values.
    Returns:
        None; source paragraphs and architecture content are preserved.
    Raises:
        OSError: If the package cannot be read or written.
        ValueError: If Word XML is malformed.
    """
    ns = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
    q = lambda name: '{' + ns + '}' + name
    with zipfile.ZipFile(path) as archive:
        parts = {name: archive.read(name) for name in archive.namelist()}
    root = ET.fromstring(parts['word/document.xml']); body = root.find(q('body'))
    headings = []
    for paragraph in body.findall(q('p')):
        style = paragraph.find(q('pPr') + '/' + q('pStyle'))
        if style is not None and style.get(q('val')) in ('Heading1', 'Heading2'):
            label = ''.join(paragraph.itertext())
            bookmark = paragraph.find(q('bookmarkStart'))
            headings.append((label, bookmark.get(q('name')) if bookmark is not None else None))
    for child in list(body):
        if child.tag == q('sdt') and child.find('.//' + q('docPartGallery')) is not None:
            body.remove(child)
    def paragraph(text, style=None, page_break=False):
        p = ET.Element(q('p'))
        if style:
            properties = ET.SubElement(p, q('pPr')); ET.SubElement(properties, q('pStyle'), {q('val'): style})
        run = ET.SubElement(p, q('r'))
        if page_break: ET.SubElement(run, q('br'), {q('type'): 'page'})
        else: ET.SubElement(run, q('t')).text = text
        return p
    front = [paragraph(metadata['title'], 'Title'), paragraph(metadata['viewpoint'], 'Subtitle'),
             paragraph(metadata['organisation']), paragraph('Document owner: ' + metadata['owner']),
             paragraph('Version: ' + metadata['version']), paragraph('Scope: ' + metadata['scope']),
             paragraph('Status: ' + metadata['approval']), paragraph('Publication language: English'),
             paragraph('', page_break=True), paragraph('Contents', 'Heading1')]
    for label, anchor in headings:
        p = paragraph(label)
        if anchor:
            run = list(p)[0]; p.remove(run)
            ET.SubElement(p, q('hyperlink'), {q('anchor'): anchor, q('history'): '1'}).append(run)
        front.append(p)
    front.append(paragraph('', page_break=True))
    for index, item in enumerate(front): body.insert(index, item)
    parts['word/document.xml'] = ET.tostring(root, encoding='utf-8', xml_declaration=True)
    with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as archive:
        for name, data in parts.items(): archive.writestr(name, data)
