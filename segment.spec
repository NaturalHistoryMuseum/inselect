# -*- mode: python -*-
import sys

from pathlib import Path

block_cipher = None


a = Analysis(['inselect/scripts/segment.py'],
             pathex=['/Users/lawrence/projects/inselect'],
             binaries=None,
             datas=None,
             hiddenimports=['numpy', 'sklearn.neighbors.typedefs'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

# PyInstaller does not detect some dylibs, I think in some cases because they
# are symlinked.
# See Stack Overflow post http://stackoverflow.com/a/17595149 for example
# of manipulating Analysis.binaries.
MISSING_DYLIBS = (
    'libiomp5.dylib',
    'libmkl_intel_lp64.dylib',
    'libmkl_intel_thread.dylib',
    'libmkl_core.dylib',
)

# The lib directory associated with this environment
LIB = Path(sys.argv[0]).parent.parent.joinpath('lib')

# Find the source for each library and add it to the list of binaries
a.binaries += TOC([
    (lib, str(LIB.joinpath(lib).resolve()), 'BINARY') for lib in MISSING_DYLIBS
])

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='segment',
          debug=False,
          strip=False,
          upx=True,
          console=True )
