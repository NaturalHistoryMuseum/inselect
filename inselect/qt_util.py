from skimage import io, img_as_ubyte
import matplotlib.pyplot as plt
from PySide import QtGui
import numpy as np

def read_qt_image(filename):
    """Read image in QT format from file.

    """
    image = img_as_ubyte(io.imread(filename, plugin='matplotlib'))[..., :3]
    image = np.ascontiguousarray(image)
    qt_image = QtGui.QImage(image.data,
                            image.shape[1], image.shape[0],
                            image.strides[0], QtGui.QImage.Format_RGB888)

    # Attach the array to the QtImage so that it doesn't go out of scope
    # before the QtImage is used
    qt_image.array = image

    return qt_image
