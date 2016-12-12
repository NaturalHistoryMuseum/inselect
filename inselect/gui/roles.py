from itertools import count

from PyQt5.QtCore import Qt


_role = count(start=int(Qt.UserRole))
RectRole = next(_role)              # tuple (x, y, w, h)
PixmapRole = next(_role)            # QPixmap of the entire scanned image
RotationRole = next(_role)          # integer rotation in degrees
MetadataRole = next(_role)          # dict mapping name:value for each field
MetadataValidRole = next(_role)     # False if any metadata field values do not
                                    # validate against the currently selected
                                    # metadata template
