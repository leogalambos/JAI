# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Build the explicitly fictional English SABSA publication example and optional native outputs."""
import argparse
from contextlib import redirect_stdout
import io
import json
from pathlib import Path
import subprocess
import sys
from argparse import Namespace
import sabsa
from sabsa_narrative import PROFILE_ROOT

FIXTURE = Path(__file__).resolve().parents[1] / 'sabsa/publication/example.json'


def build_example(destination, render=False):
    """Create the English example library and six viewpoint documents.

    Args:
        destination: Output directory; an existing library is rejected to avoid overwrite.
        render: If true, also render TeX, DOCX and PDF using Pandoc/XeLaTeX.
    Returns:
        Path of the generated canonical example library.
    Raises:
        FileExistsError: If destination/library already exists.
        RuntimeError: If the authored example does not pass architecture validation.
        subprocess.CalledProcessError: If a required external renderer fails.
    """
    destination = Path(destination)
    if destination.exists() and any(destination.iterdir()):
        raise FileExistsError(f'{destination} is not empty; choose a fresh destination')
    destination.mkdir(parents=True, exist_ok=True)
    library = destination / 'library'
    if library.exists(): raise FileExistsError(f'{library} already exists; choose a fresh destination')
    fixture = json.loads(FIXTURE.read_text(encoding='utf-8'))
    with redirect_stdout(io.StringIO()):
        sabsa.cmd_init(Namespace(lib=str(library), **fixture['library']))
        (library / '00-sources/example-brief.md').write_text(fixture['brief'], encoding='utf-8')
        for item in fixture['entries']:
            fields = {**item['fields'], 'basis': 'stated', 'source': '00-sources/example-brief.md', 'horizon': 'target', 'lifecycle_state': 'proposed'}
            sabsa.cmd_new(Namespace(lib=str(library), type=item['type'], title=item['title'], set=[f'{key}={value}' for key, value in fields.items()]))
            path = library / sabsa.TYPES[item['type']]['dir'] / (item['id'] + '.md')
            text = path.read_text(encoding='utf-8')
            for field, value in sabsa.parse(path).items():
                if not field.startswith('_') and sabsa.PLACEHOLDER.search(str(value)):
                    sabsa._frontmatter_set(path, field, '')
            text = path.read_text(encoding='utf-8'); end = text.find('\n---', 3)
            path.write_text(text[:end] + '\nlanguage: en' + text[end:end+4] + '\n\n' + item['body'] + '\n', encoding='utf-8')
        for layer in sabsa.LAYER_KEYS:
            directory = library / 'narratives' / layer; directory.mkdir(parents=True)
            profile = json.loads((PROFILE_ROOT / (layer + '.json')).read_text(encoding='utf-8'))
            for chapter in profile['chapters']:
                prose = fixture['narratives'][layer][chapter['key']]
                (directory / (chapter['key'] + '.md')).write_text('---\nbasis: stated\nsource: 00-sources/example-brief.md\nauthor: Fictional architecture working group\nlanguage: en\n---\n\n' + prose + '\n', encoding='utf-8')
            for aspect in sabsa.INTERROGATIVE:
                path = library / 'matrix' / (layer + '-' + aspect + '.md')
                answer = fixture['matrix'][layer][aspect]
                path.write_text(f'---\nlayer: {layer}\naspect: {aspect}\nstatus: answered\nbasis: stated\nsource: 00-sources/example-brief.md\n---\n\n{answer}\n', encoding='utf-8')
    _, errors, warnings = sabsa.check(str(library))
    if errors: raise RuntimeError('; '.join(errors))
    for layer in sabsa.LAYER_KEYS:
        for extension in (('md', 'tex', 'docx', 'pdf') if render else ('md',)):
            args = [sys.executable, str(Path(sabsa.__file__)), 'document', str(library), '--layer', layer, '--out', str(destination / (layer + '.' + extension))]
            if extension == 'pdf': args += ['--latex']
            subprocess.run(args, check=True)
    subprocess.run([sys.executable, str(Path(sabsa.__file__)), 'catalogues', str(library), 'export', '--directory', str(destination / 'csv')], check=True)
    (destination / 'README.md').write_text('# English SABSA publication example\n\nThis is an explicitly fictional target architecture, not a statement about a real organisation. No implementation, legal applicability, approval or measured result is asserted.\n\nThe six named viewpoint documents are the primary examples. Their authored chapters and complete typed specifications are generated from the adjacent canonical library. CSV files are editable exchange projections.\n\nReproduce in a fresh directory:\n\n```sh\npython3 .ai/runtime/tools/sabsa_publication_demo.py --out build/sabsa-publication-demo-new --render\n```\n\nRendering requires Pandoc, XeLaTeX and DejaVu Serif. Word files can be independently converted with LibreOffice.\n', encoding='utf-8')
    return library


def main():
    """Parse command arguments, build the example, and return success.

    Returns:
        Zero after successful generation; exceptions retain renderer diagnostics.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', required=True)
    parser.add_argument('--render', action='store_true')
    args = parser.parse_args()
    build_example(args.out, args.render)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
