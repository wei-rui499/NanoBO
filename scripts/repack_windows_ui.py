"""Update the interface over the exact, user-tested Windows 0.2.4 runtime.

This publisher script compiles Python UI modules on native Windows CPython 3.10.
It never starts the application, its models, or the generated installer. Every
unchanged file and frozen module is checked against the published baseline.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import sys
import zipfile

from repack_windows_hotfix import rebuild_executable, sha256
from build_support import app_version

ROOT = Path(__file__).resolve().parents[1]
BASE_SHA256 = '07905f83af0ff4c8586dba1be83e363fb4a70bc61073cc083bf4a91ce3ee8be5'
BASE_SOURCE_COMMIT = 'f86b11dce9491adcc94d3b490c08dab49e08edd1'
PATCHES = {name: ROOT / path for name, path in {
    'chembo': 'src/chembo/__init__.py',
    'chembo.app': 'src/chembo/app.py',
    'chembo.analysis_view': 'src/chembo/analysis_view.py',
    'chembo.recipe_dialog': 'src/chembo/recipe_dialog.py',
    'chembo.verification': 'src/chembo/verification.py',
}.items()}
ADDITIONS = {'chembo.i18n': ROOT / 'src/chembo/i18n.py'}
SCIENTIFIC_SOURCES = (
    'src/chembo/engine.py', 'src/chembo/modeling.py',
    'src/chembo/modern_worker.py', 'src/chembo/space.py', 'src/chembo/table_io.py',
    'src/chembo/worker.py',
)


def digest_stream(stream):
    result = hashlib.sha256()
    for chunk in iter(lambda: stream.read(1024 * 1024), b''):
        result.update(chunk)
    return result.hexdigest()


def safe_extract(archive, destination):
    destination = destination.resolve()
    for member in archive.infolist():
        path = (destination / member.filename).resolve()
        if not path.is_relative_to(destination) or '\\' in member.filename:
            raise RuntimeError('Unsafe baseline member: ' + member.filename)
    archive.extractall(destination)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base', type=Path, required=True)
    parser.add_argument('--base-source', type=Path, required=True)
    parser.add_argument('--output', type=Path, default=ROOT / 'dist')
    args = parser.parse_args()
    if sys.platform != 'win32' or sys.version_info[:2] != (3, 10):
        raise SystemExit('Run with native Windows CPython 3.10; no application execution is performed.')
    if sha256(args.base) != BASE_SHA256:
        raise SystemExit('Baseline portable ZIP digest mismatch')
    if sha256(args.base_source) != 'a760178231e95c34a30c66877d401f930cfd548ab1a39fe86a8b59eec7c21c47':
        raise SystemExit('Baseline source ZIP digest mismatch')
    with zipfile.ZipFile(args.base_source) as source:
        for name in SCIENTIFIC_SOURCES:
            expected = source.read('NanoBO/' + name).replace(b'\r\n', b'\n')
            if (ROOT / name).read_bytes().replace(b'\r\n', b'\n') != expected:
                raise SystemExit('Scientific source differs from the tested baseline: ' + name)
    destination = args.output.resolve()
    if destination.exists() and any(destination.iterdir()):
        raise SystemExit('Use an empty destination')
    destination.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(args.base) as archive:
        safe_extract(archive, destination)
    original = destination / 'NanoBO'
    bundle = destination / 'SynthBO'
    original.rename(bundle)
    executable = bundle / 'NanoBO.exe'
    modules = rebuild_executable(executable, PATCHES, ADDITIONS)
    executable.rename(bundle / 'SynthBO.exe')
    changed = {'SynthBO.exe'}
    resources = bundle / '_internal'
    # Documentation/legal resources change, not the science environment.
    for folder in ('docs/html', 'examples/tutorial'):
        target = resources / folder
        if target.exists():
            for path in target.rglob('*'):
                if path.is_file():
                    changed.add(path.relative_to(bundle).as_posix())
            shutil.rmtree(target)
        shutil.copytree(ROOT / folder, target)
        changed.update(path.relative_to(bundle).as_posix() for path in target.rglob('*') if path.is_file())
    for filename in ('LICENSE', 'ACKNOWLEDGMENTS.md', 'THIRD_PARTY_NOTICES.md', 'CITATION.cff', 'REFERENCES.bib'):
        shutil.copy2(ROOT / filename, resources / filename)
        changed.add('_internal/' + filename)
    preserved = []
    modern_files = 0
    with zipfile.ZipFile(args.base) as archive:
        for member in archive.infolist():
            if member.is_dir():
                continue
            relative = member.filename.removeprefix('NanoBO/')
            relative = 'SynthBO.exe' if relative == 'NanoBO.exe' else relative
            if relative in changed:
                continue
            target = bundle / relative
            with archive.open(member) as stream:
                expected = digest_stream(stream)
            if not target.is_file() or sha256(target) != expected:
                raise RuntimeError('Unrelated runtime file changed: ' + relative)
            preserved.append((relative, expected))
            if relative.startswith('_internal/engines/modern/'):
                modern_files += 1
    # Include the actual Windows dependency metadata in corresponding source.
    for kind in ('classic', 'modern'):
        target = ROOT / 'licenses' / kind
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(resources / 'licenses' / kind, target)
    inventory = hashlib.sha256(json.dumps(preserved, separators=(',', ':')).encode()).hexdigest()
    report = {
        'product': 'SynthBO', 'version': app_version(ROOT),
        'created_utc': datetime.now(timezone.utc).isoformat(),
        'baseline': {'release': 'v0.2.4', 'source_commit': BASE_SOURCE_COMMIT,
                     'portable_zip_sha256': BASE_SHA256, 'runtime_pass_reported_by_user': True},
        'scientific_sources_match_baseline': list(SCIENTIFIC_SOURCES),
        'patched_frozen_modules': list(PATCHES), 'new_frozen_modules': list(ADDITIONS),
        'original_frozen_module_count': modules,
        'unrelated_frozen_modules': 'Compressed byte-for-byte match with baseline',
        'preserved_runtime_files': len(preserved), 'preserved_modern_worker_files': modern_files,
        'preserved_file_inventory_sha256': inventory,
        'changed_presentation_files': sorted(changed),
        'executable_sha256': sha256(bundle / 'SynthBO.exe'),
        'status': 'UI_UPDATE_OVER_USER_TESTED_RUNTIME',
        'application_started': False, 'models_executed': False,
        'new_ui_windows_runtime_verified': False,
    }
    (bundle / 'WINDOWS_UI_UPDATE.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({key: report[key] for key in ('product', 'version', 'preserved_runtime_files', 'preserved_modern_worker_files', 'status')}, indent=2))


if __name__ == '__main__':
    main()
