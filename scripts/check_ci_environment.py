#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Fail-fast environment contract for both validation and release GitHub Actions jobs.

Never silently skip a required renderer; publication and render-based visual QA
are quality gates, not optional tests. --python-only helps with local diagnostics.
"""
from __future__ import annotations

import argparse
import importlib
import importlib.metadata
import io
import json
import platform
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

PYTHON_DEPENDENCIES = {
    "jsonschema": "jsonschema",
    "lxml": "lxml",
    "PIL": "Pillow",
    "cairosvg": "CairoSVG",
    "mistune": "mistune",
    "mkdocs": "mkdocs",
    "material": "mkdocs-material",
    "pymdownx": "pymdown-extensions",
}
SYSTEM_COMMANDS = ("libreoffice", "pdftoppm")


def run(command: list[str], timeout: int = 45) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          text=True, timeout=timeout, check=True)


def verify(python_only: bool = False) -> dict:
    result: dict = {"python": platform.python_version(), "packages": {},
                    "commands": {}, "smoke_tests": {}, "errors": []}
    if sys.version_info[:2] != (3, 12):
        result["errors"].append("CI requires Python 3.12")

    for module, distribution in PYTHON_DEPENDENCIES.items():
        try:
            importlib.import_module(module)
            result["packages"][distribution] = importlib.metadata.version(distribution)
        except (ImportError, importlib.metadata.PackageNotFoundError) as exc:
            result["errors"].append(f"Python dependency {distribution}: {exc}")

    if result["errors"] or python_only:
        return result

    for name in SYSTEM_COMMANDS:
        result["commands"][name] = shutil.which(name)
        if not result["commands"][name]:
            result["errors"].append(f"System executable missing: {name}")
    if result["errors"]:
        return result

    try:
        result["commands"]["libreoffice_version"] = run(
            ["libreoffice", "--version"], timeout=15).stdout.strip()
        result["commands"]["pdftoppm_version"] = run(
            ["pdftoppm", "-v"], timeout=15).stderr.strip().splitlines()[0]
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            html = folder / "smoke.html"
            html.write_text("<html><body><h1>JAI render smoke test</h1></body></html>",
                            encoding="utf-8")
            run(["libreoffice", "-env:UserInstallation=file://" + str(folder / "profile"),
                 "--headless", "--convert-to", "pdf", "--outdir", str(folder), str(html)],
                timeout=60)
            pdf = folder / "smoke.pdf"
            if not pdf.is_file() or pdf.stat().st_size < 100:
                raise RuntimeError("LibreOffice HTML-to-PDF did not produce a PDF")
            result["smoke_tests"]["office_to_pdf"] = "PASS"
            run(["pdftoppm", "-f", "1", "-l", "1", "-singlefile",
                 "-png", "-r", "72", str(pdf), str(folder / "page")], timeout=30)
            from PIL import Image
            with Image.open(folder / "page.png") as im:
                im.verify()
            result["smoke_tests"]["pdf_rasterisation"] = "PASS"
            import cairosvg
            svg = ('<svg xmlns="http://www.w3.org/2000/svg" width="400" height="400">'
                   '<rect x="10" y="10" width="380" height="380" fill="black"/></svg>')
            png_bytes = cairosvg.svg2png(bytestring=svg.encode("utf-8"))
            with Image.open(io.BytesIO(png_bytes)) as im:
                im.verify()
            result["smoke_tests"]["svg_rasterisation"] = "PASS"
    except (OSError, ValueError, RuntimeError, subprocess.CalledProcessError,
            subprocess.TimeoutExpired) as exc:
        result["errors"].append(f"Renderer smoke test: {exc}")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--python-only", action="store_true")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    report = verify(python_only=args.python_only)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    for package, version in sorted(report["packages"].items()):
        print(f"PASS {package} {version}")
    for test, status in report["smoke_tests"].items():
        print(f"{status} {test}")
    for error in report["errors"]:
        print(f"::error::{error}", file=sys.stderr)
    if not report["errors"]:
        print("PASS JAI qualification environment")
    return 1 if report["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
