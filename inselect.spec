# -*- mode: python -*-
import sys

from pathlib import Path

from pylibdmtx import pylibdmtx
from pyzbar import pyzbar

block_cipher = None


a = Analysis(['inselect/scripts/inselect.py'],
             pathex=[str(Path('.').absolute())],
             binaries=[],
             datas=[
                 ('inselect/gui/inselect.qss', ''),
             ],
             hiddenimports=['sklearn.neighbors.typedefs'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)


# dylibs not detected because they are loaded by ctypes
a.binaries += TOC([
    (Path(dep._name).name, dep._name, 'BINARY')
    for dep in pylibdmtx.EXTERNAL_DEPENDENCIES + pyzbar.EXTERNAL_DEPENDENCIES
])


ICON = 'icons/inselect.icns'

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='inselect',
          debug=False,
          strip=False,
          upx=False,
          console=False,
          icon=ICON)

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,
               name='inselect',
               icon=ICON)

app = BUNDLE(coll,
             name='inselect.app',
             icon=ICON,
             bundle_identifier=None)
