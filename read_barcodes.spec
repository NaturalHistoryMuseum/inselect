# For PyInstaller build on Mac
import sys

from pathlib import Path

from pylibdmtx import pylibdmtx
from pyzbar import pyzbar


block_cipher = None


a = Analysis(['inselect/scripts/read_barcodes.py'],
             pathex=[str(Path('.').absolute())],
             binaries=[],
             datas=None,
             hiddenimports=['numpy'],
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


# PyInstaller does not detect some dylibs, in some cases (I think) because they
# are symlinked.
# See Stack Overflow post http://stackoverflow.com/a/17595149 for example
# of manipulating Analysis.binaries.
MISSING_DYLIBS = (
    'libopencv_hdf.3.1.dylib',
    'libopencv_reg.3.1.dylib',
    'libopencv_surface_matching.3.1.dylib',
    'libopencv_dnn.3.1.dylib',
    'libopencv_superres.3.1.dylib',
    'libopencv_xobjdetect.3.1.dylib',
    'libopencv_xphoto.3.1.dylib',
    'libopencv_bgsegm.3.1.dylib',
    'libopencv_bioinspired.3.1.dylib',
    'libopencv_dpm.3.1.dylib',
    'libopencv_line_descriptor.3.1.dylib',
    'libopencv_saliency.3.1.dylib',
    'libopencv_ccalib.3.1.dylib',
    'libopencv_rgbd.3.1.dylib',
    'libopencv_tracking.3.1.dylib',
    'libopencv_videostab.3.1.dylib',
    'libopencv_aruco.3.1.dylib',
    'libopencv_optflow.3.1.dylib',
    'libopencv_stitching.3.1.dylib',
    'libopencv_datasets.3.1.dylib',
    'libopencv_face.3.1.dylib',
    'libopencv_text.3.1.dylib',
    'libopencv_photo.3.1.dylib',
    'libopencv_ximgproc.3.1.dylib',
    'libopencv_objdetect.3.1.dylib',
    'libopencv_xfeatures2d.3.1.dylib',
    'libopencv_shape.3.1.dylib',
    'libopencv_video.3.1.dylib',
    'libopencv_calib3d.3.1.dylib',
    'libopencv_features2d.3.1.dylib',
    'libopencv_flann.3.1.dylib',
    'libopencv_ml.3.1.dylib',
    'libopencv_highgui.3.1.dylib',
    'libopencv_videoio.3.1.dylib',
    'libopencv_imgcodecs.3.1.dylib',
    'libopencv_imgproc.3.1.dylib',
    'libopencv_core.3.1.dylib',
    'libtbb.dylib'
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
