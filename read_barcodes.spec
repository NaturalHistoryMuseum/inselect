import sys

from pathlib import Path

block_cipher = None


a = Analysis(['inselect/scripts/read_barcodes.py'],
             pathex=[str(Path('.').absolute())],
             binaries=[],
             datas=None,
             hiddenimports=['numpy', 'libdmtx'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)


# libdmtx dylib is not detected because it is loaded by a ctypes call
a.binaries += TOC([
    ('libdmtx.dylib', '/usr/local/Cellar/libdmtx/0.7.4/lib/libdmtx.dylib', 'BINARY'),
])

# PyInstaller does not detect some dylibs, I think in some cases because they
# are symlinked.
# See Stack Overflow post http://stackoverflow.com/a/17595149 for example
# of manipulating Analysis.binaries.
MISSING_DYLIBS = (
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

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='read_barcodes',
          debug=False,
          strip=False,
          upx=True,
          console=True )
