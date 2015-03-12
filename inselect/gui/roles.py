from PySide.QtCore import Qt

RectRole = Qt.UserRole               # tuple (x, y, w, h)
PixmapRole = 1+Qt.UserRole           # QPixmap of the entire scanned image
RotationRole = 2+Qt.UserRole         # integer rotation in degrees
MetadataRole = 3+Qt.UserRole         # dict mapping name:value for each field
MetadataValidRole = 4+Qt.UserRole    # False if any metadata field values do not
                                     # validate against the currently selected
                                     # metadata template
