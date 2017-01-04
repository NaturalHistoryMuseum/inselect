# -*- mode: python -*-
import os

from pathlib import Path

from pylibdmtx import pylibdmtx
from pyzbar import pyzbar


block_cipher = None


a = Analysis(
    ['inselect/scripts/read_barcodes.py'],
    pathex=[str(Path('.').absolute())],
    binaries=[],
    datas=[],
    hiddenimports=['numpy'],
    hookspath=[],
    runtime_hooks=[],
    excludes=os.getenv('EXCLUDE_MODULES', '').split(' '),
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher
)


# dylibs not detected because they are loaded by ctypes
a.binaries += TOC([
    (Path(dep._name).name, dep._name, 'BINARY')
    for dep in pylibdmtx.EXTERNAL_DEPENDENCIES + pyzbar.EXTERNAL_DEPENDENCIES
])

# A dependency of libzbar.dylib that PyInstaller does not detect
MISSING_DYLIBS = (
    Path('/usr/local/lib/libjpeg.8.dylib'),
)
a.binaries += TOC([
    (lib.name, str(lib.resolve()), 'BINARY') for lib in MISSING_DYLIBS
])


pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    name='read_barcodes',
    debug=False,
    strip=False,
    upx=True,
    console=True
)
