# SPDX-License-Identifier: BSD-4-Clause
# Copyright (c) 2026 Leo Galambos and the Egothor team
"""Build the disposable canonical reader in a caller-owned scratch directory.

Run with the pinned scratch virtual environment. No package installation or
source mutation is performed by this builder. Native qualification is separate.
"""
from __future__ import annotations

import argparse
import hashlib
from importlib.metadata import distribution
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import sysconfig


def _mac_dependencies(executable, original_main):
    linked = subprocess.run(['otool', '-L', str(executable)], capture_output=True,
                            text=True, check=True, timeout=15).stdout.splitlines()[1:]
    rpaths = subprocess.run(['otool', '-l', str(executable)], capture_output=True,
                            text=True, check=True, timeout=15).stdout.splitlines()
    search = []
    for index, line in enumerate(rpaths):
        if line.strip() == 'cmd LC_RPATH':
            search.append(rpaths[index + 2].strip().split(' (offset', 1)[0].removeprefix('path '))
    def expand(value):
        return value.replace('@loader_path', str(executable.parent)).replace(
            '@executable_path', str(original_main.parent))
    result = []
    for line in linked:
        name = line.strip().split(' (compatibility', 1)[0]
        if name.startswith(('/usr/lib/', '/System/Library/')):
            continue
        candidates = [Path(expand(name))] if not name.startswith('@rpath/') else [
            Path(expand(entry)) / name.removeprefix('@rpath/') for entry in search]
        resolved = next((p.resolve() for p in candidates if p.is_file()), None)
        if resolved is None:
            raise ValueError('Unresolved native macOS verifier dependency: ' + name)
        if resolved != executable.resolve():
            result.append((name, resolved))
    return result


def _verifier_libraries(executable):
    if sys.platform.startswith('linux'):
        result = subprocess.run(['ldd', str(executable)], capture_output=True,
                                text=True, check=True, timeout=15)
        return [Path(line.split('=>', 1)[1].split('(', 1)[0].strip())
                for line in result.stdout.splitlines() if '=>' in line and 'not found' not in line]
    if os.name == 'nt':
        import pefile
        system = Path(os.environ['SystemRoot']) / 'System32'
        pending, result = [executable], {}
        while pending:
            current = pending.pop()
            with pefile.PE(str(current), fast_load=True) as image:
                image.parse_data_directories(directories=[
                    pefile.DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_IMPORT'],
                    pefile.DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_DELAY_IMPORT']])
                imports = [*getattr(image, 'DIRECTORY_ENTRY_IMPORT', []),
                           *getattr(image, 'DIRECTORY_ENTRY_DELAY_IMPORT', [])]
                for entry in imports:
                    name = entry.dll.decode('ascii')
                    if '/' in name or '\\' in name or ':' in name:
                        raise ValueError('Invalid PE dependency name')
                    local = executable.parent / name
                    if local.is_file():
                        if name.lower() not in result:
                            result[name.lower()] = local
                            pending.append(local)
                    elif not (system / name).is_file() and not name.lower().startswith(
                            ('api-ms-win-', 'ext-ms-win-')):
                        raise ValueError('Unresolved native Windows verifier dependency: ' + name)
        return list(result.values())
    if sys.platform == 'darwin':
        pending, found = [executable], {}
        while pending:
            for _, dependency in _mac_dependencies(pending.pop(), executable):
                if dependency not in found:
                    if any(p.name == dependency.name for p in found):
                        raise ValueError('Colliding macOS verifier dependency basenames')
                    found[dependency] = True
                    pending.append(dependency)
        return list(found)
    raise ValueError('Native verifier dependency inspection unavailable')


def _bundle_verifier(source, destination):
    destination.mkdir()
    executable = destination / ('openssl.exe' if os.name == 'nt' else 'openssl')
    shutil.copy2(source, executable)
    libraries = destination if os.name == 'nt' else destination / 'lib'
    libraries.mkdir(exist_ok=True)
    dependencies = _verifier_libraries(source)
    for dependency in dependencies:
        shutil.copy2(dependency.resolve(), libraries / dependency.name)
    if sys.platform == 'darwin':
        for original in [*dependencies, source]:
            copied = executable if original == source else libraries / original.name
            copied.chmod(0o755)
            for name, dependency in _mac_dependencies(original, source):
                replacement = ('@executable_path/lib/' if original == source else '@loader_path/') + dependency.name
                subprocess.run(['install_name_tool', '-change', name, replacement, str(copied)], check=True)
            if original != source:
                subprocess.run(['install_name_tool', '-id', '@loader_path/' + copied.name,
                                str(copied)], check=True)
            subprocess.run(['codesign', '--force', '--sign', '-', str(copied)], check=True)
    return executable


def _notices(root, application, verifier_license):
    notices = application / 'notices'
    notices.mkdir()
    shutil.copyfile(root / 'LICENSE', notices / 'JAI-LICENSE.txt')
    python_license = next((p for p in [Path(sysconfig.get_path('stdlib')) / 'LICENSE.txt',
                                      Path(sys.base_prefix) / 'LICENSE.txt'] if p.is_file()), None)
    if python_license is None:
        raise ValueError('CPython runtime license file must be supplied by the build interpreter')
    shutil.copyfile(python_license, notices / 'CPython-LICENSE.txt')
    shutil.copyfile(verifier_license, notices / 'OpenSSL-LICENSE.txt')
    for name in ['jsonschema', 'referencing', 'attrs', 'rpds-py',
                 'jsonschema-specifications', 'pyinstaller', 'pyinstaller-hooks-contrib']:
        package = distribution(name)
        files = [p for p in package.files or [] if '.dist-info/licenses/' in str(p)]
        if not files:
            raise ValueError('Installed package lacks inspectable license files: ' + name)
        for file in files:
            target = notices / name / str(file).split('.dist-info/licenses/', 1)[1]
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(package.locate_file(file), target)
    (notices / 'EXPERIMENT-STATUS.txt').write_text(
        'Disposable local build, not a redistributable release. Included notices cover '
        'JAI, CPython, OpenSSL and selected Python distributions. A complete native '
        'dependency SBOM, file-level license audit and release distribution approval '
        'remain required; this inventory is not legal clearance.\n')


def main(argv=None):
    """Build one unsigned native probe and inventory its exact resources.

    Args:
        argv: Optional CLI arguments; defaults to the process arguments.
    Returns:
        Zero after a complete unsigned build; errors propagate without claiming
        that a partial directory is qualified.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--verifier', type=Path, required=True)
    parser.add_argument('--verifier-license', type=Path, required=True)
    args = parser.parse_args(argv)
    root = Path(__file__).resolve().parents[4]
    output = args.output.absolute()
    if output.exists() and any(output.iterdir()):
        raise ValueError('Build output must be a new or empty scratch directory')
    expected = json.loads((root / 'apps/fabric-explorer/config/dependency-baseline.json').read_text())
    if '.'.join(map(str, sys.version_info[:3])) != expected['toolchain']['python']['version']:
        raise ValueError('Pinned CPython build version required')
    version = subprocess.run([str(args.verifier), 'version'], capture_output=True,
                             text=True, check=True, timeout=15).stdout
    if not version.startswith('OpenSSL ' + expected['toolchain']['openssl']['version'] + ' '):
        raise ValueError('Pinned OpenSSL verifier version required')
    output.mkdir(parents=True, exist_ok=True)
    command = [sys.executable, '-m', 'PyInstaller', '--noconfirm', '--clean', '--onedir',
               '--name', 'jai-reader-probe', '--distpath', str(output / 'dist'),
               '--workpath', str(output / 'work'), '--specpath', str(output / 'spec'),
               '--paths', str(root / '.ai/runtime/tools'), '--paths', str(root / 'apps/fabric-explorer/reader'),
               '--hidden-import', 'readonly_files', '--hidden-import', 'windows_readonly',
               '--hidden-import', 'semantic_reader', '--hidden-import', 'recorded_projection', '--hidden-import', 'facts_spool', '--copy-metadata', 'jsonschema',
               str(Path(__file__).with_name('probe.py'))]
    environment = {**os.environ, 'PYINSTALLER_CONFIG_DIR': str(output / 'cache')}
    subprocess.run(command, check=True, cwd=output, env=environment)
    application = output / 'dist/jai-reader-probe'
    # Bare frozen modules are located in _internal; their maintained parent-based
    # resource locator therefore expects protocol resources at the app root.
    schemas = application / 'protocol/governed-delivery/v1'
    schemas.mkdir(parents=True)
    for schema in (root / '.ai/runtime/protocol/governed-delivery/v1').glob('*.schema.json'):
        shutil.copyfile(schema, schemas / schema.name)
    _bundle_verifier(args.verifier.resolve(), application / 'verifier')
    _notices(root, application, args.verifier_license)
    inventory = {'format': 'jai.fabric-explorer.probe-inventory/1',
                 'qualified': False, 'licenseAudit': 'selected-notices-only-not-release-cleared',
                 'nativePlatform': sys.platform,
                 'files': {p.relative_to(application).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                           for p in sorted(application.rglob('*')) if p.is_file()}}
    (output / 'inventory.json').write_text(json.dumps(inventory, indent=2) + '\n')
    print(json.dumps({'status': 'built-not-qualified', 'application': str(application)}))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
