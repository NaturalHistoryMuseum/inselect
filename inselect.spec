# -*- mode: python -*-
import os
import sys

from pathlib import Path

from pylibdmtx import pylibdmtx
from pyzbar import pyzbar


block_cipher = None

# See https://github.com/pyinstaller/pyinstaller/wiki/Recipe-remove-tkinter-tcl
# for details of excluding all of the tcl, tk, tkinter shat
sys.modules['FixTk'] = None


a = Analysis(
    ['inselect/scripts/inselect.py'],
    pathex=[str(Path('.').absolute())],
    binaries=[],
    datas=[
        ('inselect/gui/inselect.qss', ''),
    ],
    hiddenimports=['sklearn.neighbors.typedefs'],
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


ICON = 'icons/inselect.icns'

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    exclude_binaries=True,
    name='inselect',
    debug=False,
    strip=False,
    upx=False,
    console=False,
    icon=ICON
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    name='inselect',
    icon=ICON
)


app = BUNDLE(
    coll,
    name='inselect.app',
    icon=ICON,
    bundle_identifier=None
)
