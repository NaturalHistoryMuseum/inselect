# For PyInstaller build on Mac

import sys
from pathlib import Path

block_cipher = None

a = Analysis(['inselect.py'],
             pathex=[str(Path('.').absolute())],
             binaries=None,
             datas=None,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=['Tkinter'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)


# PyInstaller does not detect some dylibs, I think because they are symlinked.
# See Stack Overflow post http://stackoverflow.com/a/17595149 for example
# of manipulating Analysis.binaries.

# Tuples (name, source)
MISSING_DYLIBS = (
    ('libQtCore.4.dylib', 'libQtCore.4.8.7.dylib'),
    ('libQtGui.4.dylib', 'libQtGui.4.8.7.dylib'),
    ('libpng16.16.dylib', 'libpng16.16.dylib'),
    ('libz.1.dylib', 'libz.1.dylib'),
)

# The lib directory associated with this environment
LIB = Path(sys.argv[0]).parent.parent.joinpath('lib')

a.binaries += TOC([(name, str(LIB.joinpath(source)), 'BINARY') for name, source in MISSING_DYLIBS])

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# Prefer to freeze to a folder rather than a single file. The choice makes no
# practical difference to the user but makes it easier to diagnose broken freezes
SINGLE_FILE = False

if SINGLE_FILE:
    # A single file
    exe = EXE(pyz,
              a.scripts,
              a.binaries,
              a.zipfiles,
              a.datas,
              name='inselect',
              debug=False,
              strip=False,
              upx=True,
              console=False,
              icon='data/inselect.icns')
else:
    # A folder
    exe = EXE(pyz,
              a.scripts,
              exclude_binaries=True,
              name='inselect',
              debug=False,
              strip=False,
              upx=True,
              console=False,
              icon='data/inselect.icns')

    coll = COLLECT(exe,
                   a.binaries,
                   a.zipfiles,
                   a.datas,
                   strip=False,
                   upx=True,
                   name='inselect')


app = BUNDLE(coll,
             name='inselect.app',
             icon='data/inselect.icns',
             bundle_identifier=None)
