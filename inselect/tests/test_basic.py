from inselect.image_viewer import ImageViewer

import os
import sys

from PySide import QtGui

import numpy as np
from skimage import data_dir


def test_main():
    app = QtGui.QApplication(sys.argv)
    window = ImageViewer(app)
    window.open(os.path.join(data_dir, 'chelsea.png'))
    window.segment()
