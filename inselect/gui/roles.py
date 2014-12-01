from PySide.QtCore import Qt

RectRole = Qt.UserRole        # tuple (x, y, w, h)
ImageRole = 1+Qt.UserRole     # np.ndarray containing image data for crop
RotationRole = 2+Qt.UserRole  # integer rotation in degrees
MetadataRole = 3+Qt.UserRole  # dict mapping name:value for each field
