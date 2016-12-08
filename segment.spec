# -*- mode: python -*-
from pathlib import Path

block_cipher = None


a = Analysis(
    ['inselect/scripts/segment.py'],
    pathex=[str(Path('.').absolute())],
    binaries=[],
    datas=[],
    hiddenimports=['numpy', 'sklearn.neighbors.typedefs'],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    name='segment',
    debug=False,
    strip=False,
    upx=True,
    console=True
)
