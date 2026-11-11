"""Exercise archive patching without starting any Windows executable."""
import importlib.util
from pathlib import Path
import struct
import zipfile

import pytest


@pytest.fixture
def repacker(monkeypatch):
    scripts = Path(__file__).resolve().parents[1] / 'scripts'
    monkeypatch.syspath_prepend(str(scripts))
    import repack_windows_ui
    return repack_windows_ui


def test_added_translation_module_preserves_every_other_archive_entry(repacker, tmp_path):
    from PyInstaller.archive.writers import CArchiveWriter, ZlibArchiveWriter
    from PyInstaller.archive.readers import CArchiveReader
    import repack_windows_hotfix as patcher
    entries, code = [], {}
    for name, text in {'interface': 'label = "旧界面"', 'scientific_engine': 'constant = 3.141592653589793'}.items():
        source = tmp_path / (name + '.py')
        source.write_text(text)
        entries.append((name, str(source), 'PYMODULE'))
        code[name] = compile(text, str(source), 'exec')
    pyz = tmp_path / 'base.pyz'
    ZlibArchiveWriter(str(pyz), entries, code)
    native = tmp_path / 'native.dll'
    native.write_bytes(b'UNCHANGED-NATIVE-LIBRARY\x00\x01')
    archive = tmp_path / 'base.pkg'
    CArchiveWriter(str(archive), [('PYZ.pyz', str(pyz), False, 'z'), ('native.dll', str(native), True, 'b')], 'python310.dll')
    executable = tmp_path / 'fixture.exe'
    prefix = b'MZ-SYNTHETIC-BOOTLOADER-NOT-EXECUTABLE'
    executable.write_bytes(prefix + archive.read_bytes())
    before = CArchiveReader(str(executable))
    science = before.open_embedded_archive('PYZ.pyz').extract('scientific_engine')
    replacement = tmp_path / 'interface.py'
    replacement.write_text('label = "SynthBO"')
    added = tmp_path / 'translation.py'
    added.write_text('languages = ("zh-CN", "en")')
    assert patcher.rebuild_executable(executable, {'interface': replacement}, {'translation': added}) == 2
    after = CArchiveReader(str(executable))
    new_pyz = after.open_embedded_archive('PYZ.pyz')
    assert set(new_pyz.toc) == {'interface', 'scientific_engine', 'translation'}
    assert new_pyz.extract('scientific_engine') == science
    assert after.extract('native.dll') == native.read_bytes()
    assert executable.read_bytes().startswith(prefix)
    assert new_pyz.extract('interface').co_consts[0] == 'SynthBO'
    assert new_pyz.extract('translation').co_consts[0] == ('zh-CN', 'en')


def test_unsafe_zip_cannot_escape_destination(repacker, tmp_path):
    archive = tmp_path / 'unsafe.zip'
    with zipfile.ZipFile(archive, 'w') as target:
        target.writestr('../outside.txt', 'not allowed')
    destination = tmp_path / 'destination'
    destination.mkdir()
    with zipfile.ZipFile(archive) as source, pytest.raises(RuntimeError, match='Unsafe'):
        repacker.safe_extract(source, destination)
    assert not (tmp_path / 'outside.txt').exists()
