import json

from PySide import QtCore, QtGui
from PySide.QtCore import Qt, QAbstractItemModel, QModelIndex

from inselect.lib.utils import debug_print
from .utils import qimage_of_bgr
from .roles import RectRole, PixmapRole, RotationRole, MetadataRole


class Model(QAbstractItemModel):
    """
    """

    def __init__(self, parent=None):
        super(Model, self).__init__(parent)
        # TODO LH Placeholder metadata fields
        self._metadata_fields = ('Specimen number', 'Taxonomic group',)
        self._clear_model_data()

    def _clear_model_data(self):
        """Clear data structures
        """
        self._modified = False
        self._data = [] # A list of dicts
        self._image_array = None    # np.nd_array, for segmentation
        self._pixmap = None    # QPixmap, for display

    def clear(self):
        """Empty data
        """
        self.beginResetModel()
        self._clear_model_data()
        self.endResetModel ()

    def set_new_boxes(self, rects):
        """Replace all boxes with rects. All box information is replaced
        """
        self.removeRows(0, self.rowCount())
        if rects:
            # TODO LH Validation
            self.beginInsertRows(QModelIndex(), 0, len(rects)-1)
            self._data = [{"metadata": {}, "rect": r, "rotation": 0} for r in rects]
            self.endInsertRows()
            self.dataChanged.emit(self.index(0, 0),
                                  self.index(len(rects)-1, 0))

    def from_document(self, document):
        """Load data from document
        """
        # Load the new data
        if document.thumbnail:
            debug_print('Model will work on thumbnail')
            image_array = document.thumbnail.array
        else:
            debug_print('Model will work on full-res scan')
            image_array = document.scanned.array

        pixmap = QtGui.QPixmap.fromImage(qimage_of_bgr(image_array))
        data = []
        for item in document.items:
            rect = item['rect']
            rect = QtCore.QRect(rect[0]*pixmap.width(),
                                rect[1]*pixmap.height(),
                                rect[2]*pixmap.width(),
                                rect[3]*pixmap.height())
            data.append({"metadata": item['fields'],
                         "rect": rect,
                         "rotation": item.get('rotation', 0),
                        }
                       )

        # Inform views
        self.beginResetModel()
        self._data, self._image_array, self._pixmap = data, image_array, pixmap
        self.endResetModel()

    @property
    def image_array(self):
        """np.nd_array
        """
        return self._image_array

    @property
    def modified(self):
        """bool - True if the model has been modified
        """
        return self._modified

    def clear_modified(self):
        """Clears modified
        """
        self._modified = False

    def to_document(self, document):
        """Write data to document
        """
        # Convert to normalised boxes
        items = []
        w, h = float(self._pixmap.width()), float(self._pixmap.height())
        for box in self._data:
            # TODO LH Better to use InselectImage to convert to normalised?
            rect = box['rect']
            items.append({'rect': (rect.left()/w,
                                   rect.top()/h,
                                   rect.width()/w,
                                   rect.height()/h),
                          'fields': box['metadata'],
                          'rotation': box['rotation'],
                        })
        document.set_items(items)

    def flags(self, index):
        """QAbstractItemModel virtual
        """
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def index(self, row, column, parent=QModelIndex()):
        """QAbstractItemModel virtual
        """
        if self.hasIndex(row, column, parent):
            return self.createIndex(row, column, self._data[row])
        else:
            return QModelIndex()

    def parent(self, child):
        """QAbstractItemModel virtual
        """
        return QModelIndex()

    def rowCount(self, parent=QModelIndex()):
        """QAbstractItemModel virtual
        """
        return len(self._data)

    def columnCount(self, parent=QModelIndex()):
        """QAbstractItemModel virtual
        """
        return 1

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        """QAbstractItemModel virtual
        """
        if Qt.DisplayRole==role:
            if Qt.Vertical==orientation:
                return str(1+section)
            else:
                return 'Specimen crop'

    def data(self, index, role=Qt.DisplayRole):
        """QAbstractItemModel virtual
        """
        if PixmapRole == role:
            # This role applies to the document as a whole
            return self._pixmap
        elif not index.isValid():
            return None
        else:
            item = index.internalPointer()
            # TODO LH use a dict for this?
            if role in (Qt.DisplayRole, Qt.ToolTipRole):
                return '{0:03} {1}'.format(1+index.row(),
                                           item['metadata'].get('Specimen number', ''))
            elif Qt.WhatsThisRole == role:
                return 'Cropped specimen image'
            elif RectRole == role:
                return item['rect']
            elif RotationRole == role:
                return item['rotation']
            elif MetadataRole == role:
                return item['metadata']

    def setData(self, index, value, role):
        """QAbstractItemModel virtual
        """
        # TODO LH Validation?
        if RectRole == role:
            # value is a QRectF
            current = self._data[index.row()]['rect']

            msg = 'Model.setData rect for [{0}] from [{1}] to [{2}]'
            debug_print(msg.format(index.row(), current, value))

            self._data[index.row()]['rect'] = value
            self.dataChanged.emit(index, index)
            self._modified = True
            return True
        elif RotationRole == role:
            # value is an integer that is a multiple of 90
            current = self._data[index.row()]['rotation']

            # Constrain angle to be in range 0:360
            value = (value+360) % 360

            msg = 'Model.setData rotation for [{0}] from [{1}] to [{2}]'
            debug_print(msg.format(index.row(), current, value))

            self._data[index.row()]['rotation'] = value
            self.dataChanged.emit(index, index)
            self._modified = True
            return True
        elif MetadataRole == role:
            # value is a dict containing one or more fields
            msg = 'Model.setData for [{0}] update [{1}]'
            debug_print(msg.format(index.row(), value))

            current = self._data[index.row()]['metadata']
            current.update(value)
            self._data[index.row()]['metadata'] = current
            self.dataChanged.emit(index, index)
            self._modified = True
            return True
        else:
            return super(Model, self).setData(index, value, role)


    def insertRow(self, row, parent=QModelIndex()):
        """QAbstractItemModel virtual
        """
        debug_print('Model.insertRow row [{0}]'.format(row))

        self.beginInsertRows(QModelIndex(), row, row)
        self._data.insert(row, {"metadata": {},
                                "rect": QtCore.QRect(0, 0, 1, 1),
                                "rotation": 0})
        self._modified = True
        self.endInsertRows()
        self.dataChanged.emit(self.index(row, 0), self.index(row, 0))

        return True

    def removeRows(self, row, count, parent=QModelIndex()):
        """QAbstractItemModel virtual
        """
        debug_print('Model.removeRows row [{0}] count [{1}]'.format(row, count))

        first, last = row, row+count

        self.beginRemoveRows(parent, first, last)
        del self._data[first:last]
        self._modified = True
        self.endRemoveRows()

        return True

    def removeRows(self, row, count, parent=QModelIndex()):
        """QAbstractItemModel virtual
        """
        debug_print('Model.removeRows row [{0}] count [{1}]'.format(row, count))

        first, last = row, row+count

        self.beginRemoveRows(parent, first, last)
        del self._data[first:last]
        self._modified = True
        self.endRemoveRows()

        return True
