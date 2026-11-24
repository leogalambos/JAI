#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
# https://www.egothor.org
"""Generate installable instruction supplements from composed infrastructure modules."""

import argparse
import json
from pathlib import Path

from compose_role_library import compose

_ROOT = Path(__file__).resolve().parents[1]
_OUTPUT = _ROOT / '.ai/runtime/knowledge/infrastructure-role-guidance.json'
_MODULES = {
    'methods/zero-trust/resource-access',
    'products/hashicorp/terraform/governed-plans',
    'domains/cloud/landing-zone-evidence',
    'domains/cloud/delivery-pipelines',
}


def _render():
    compilation = compose(_ROOT)
    overlays, references = {}, {}
    for slug, row in compilation.manifest['roles'].items():
        if row['legacy_anchor'] != slug:
            continue
        if not any(module['id'] in _MODULES for module in row['modules']):
            continue
        relative = row['projection_path']
        baseline = (_ROOT / '.ai' / relative).read_bytes()
        instruction = compilation.instructions[slug]
        if not instruction.startswith(baseline):
            raise ValueError(f'{slug}: infrastructure guidance must preserve the exact legacy instruction')
        deferred = {}
        prefix = '.ai/' + str(Path(relative).parent) + '/'
        for module in row['modules']:
            for section in module['sections']:
                if section['delivery'] != 'optional':
                    continue
                projection = section['projection_path']
                name = projection.removeprefix(prefix)
                deferred[name] = section['reference_sha256']
                references[projection.removeprefix('.ai/')] = compilation.files[projection].decode('utf-8')
        overlays[relative] = {
            'baseline': row['legacy_instruction_sha256'],
            'supplement': instruction[len(baseline):].decode('utf-8'),
            'references': deferred,
        }
    return json.dumps({'schema_version': 1, 'roles': overlays, 'references': references}, ensure_ascii=False, indent=2) + '\n'


def main():
    """Write the canonical supplement or return one if check mode detects drift."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    generated = _render()
    if args.check:
        return int(not _OUTPUT.is_file() or _OUTPUT.read_text(encoding='utf-8') != generated)
    _OUTPUT.write_text(generated, encoding='utf-8')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
