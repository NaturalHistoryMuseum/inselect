# For PyInstaller build on Mac

import sys

from pathlib import Path

from pylibdmtx import pylibdmtx
from pyzbar import pyzbar


block_cipher = None

a = Analysis(['inselect.py'],
             pathex=[str(Path('.').absolute())],
             binaries=[],
             datas=[('inselect/inselect.qss', '')],
             hiddenimports=['sklearn.neighbors.typedefs'],
             hookspath=[],
             runtime_hooks=[],
             excludes=['Tkinter'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)


# dylibs not detected because they are loaded by ctypes
a.binaries += TOC([
    (Path(dep._name).name, dep._name, 'BINARY')
    for dep in pylibdmtx.EXTERNAL_DEPENDENCIES + pyzbar.EXTERNAL_DEPENDENCIES
])


# PyInstaller does not detect some dylibs, in some cases (I think) because they
# are symlinked.
# See Stack Overflow post http://stackoverflow.com/a/17595149 for example
# of manipulating Analysis.binaries.
MISSING_DYLIBS = (
    'libiomp5.dylib',
    'libmkl_intel_lp64.dylib',
    'libmkl_intel_thread.dylib',
    'libmkl_core.dylib',
    'libQtCore.4.dylib',
    'libQtGui.4.dylib',
    'libpng16.16.dylib',
    'libz.1.dylib',
    'libopencv_contrib.2.4.dylib',
    'libopencv_nonfree.2.4.dylib',
    'libopencv_gpu.2.4.dylib',
    'libopencv_legacy.2.4.dylib',
    'libopencv_photo.2.4.dylib',
    'libopencv_ocl.2.4.dylib',
    'libopencv_calib3d.2.4.dylib',
    'libopencv_features2d.2.4.dylib',
    'libopencv_flann.2.4.dylib',
    'libopencv_ml.2.4.dylib',
    'libopencv_video.2.4.dylib',
    'libopencv_objdetect.2.4.dylib',
    'libopencv_highgui.2.4.dylib',
    'libopencv_imgproc.2.4.dylib',
    'libopencv_core.2.4.dylib',
)

# The lib directory associated with this environment
LIB = Path(sys.argv[0]).parent.parent.joinpath('lib')

# Find the source for each library and add it to the list of binaries
a.binaries += TOC([
    (lib, str(LIB.joinpath(lib).resolve()), 'BINARY') for lib in MISSING_DYLIBS
])
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
              upx=False,
              console=False,
              icon='icons/inselect.icns')
else:
    # A folder
    exe = EXE(pyz,
              a.scripts,
              exclude_binaries=True,
              name='inselect',
              debug=False,
              strip=False,
              upx=False,
              console=False,
              icon='icons/inselect.icns')

    coll = COLLECT(exe,
                   a.binaries,
                   a.zipfiles,
                   a.datas,
                   strip=False,
                   upx=False,
                   name='inselect')


app = BUNDLE(coll,
             name='inselect.app',
             icon='icons/inselect.icns',
             bundle_identifier=None)
