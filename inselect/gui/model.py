import json

from PySide import QtCore, QtGui
from PySide.QtCore import Qt, QAbstractItemModel, QModelIndex

from inselect.lib.utils import debug_print
from .utils import qimage_of_bgr
from .roles import RectRole, ImageRole, RotationRole, MetadataRole


class Model(QAbstractItemModel):
    """
    """

    def __init__(self, parent=None):
        super(Model, self).__init__(parent)
        self._metadata_fields = ('Specimen number', 'Taxonomic group',)
        self._data = []
        self._image = None

    def clear(self):
        self.beginResetModel()
        self._data, self._image = [], None
        self.endResetModel ()

    def from_document(self, document):
        # Load the new data
        if document.thumbnail:
            debug_print('Will display thumbnail')
            image_array = document.thumbnail.array
        else:
            debug_print('Will display full-res scan')
            image_array = document.scanned.array

        image = QtGui.QPixmap.fromImage(qimage_of_bgr(image_array))
        data = []
        for item in document.items:
            rect = item['rect']
            rect = QtCore.QRect(rect[0]*image.width(),
                                rect[1]*image.height(),
                                rect[2]*image.width(),
                                rect[3]*image.height())
            data.append({"metadata": item['fields'],
                         "rect": rect,
                         "rotation": item['rotation'],
                        }
                       )


        # Inform views
        self.beginResetModel()
        self._data, self._image = data, image
        self.endResetModel ()

    def to_document(self, document):
        # Convert to normalised boxes
        items = []
        w, h = float(self._image.width()), float(self._image.height())
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
        """QAbstractItemModel
        """
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def index(self, row, column, parent=QModelIndex()):
        """QAbstractItemModel
        """
        if self.hasIndex(row, column, parent):
            return self.createIndex(row, column, self._data[row])
        else:
            return QModelIndex()

    def parent(self, child):
        """QAbstractItemModel
        """
        return QModelIndex()

    def rowCount(self, parent=QModelIndex()):
        """QAbstractItemModel
        """
        return len(self._data)

    def columnCount(self, parent=QModelIndex()):
        """QAbstractItemModel
        """
        return 1

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if Qt.DisplayRole==role:
            if Qt.Vertical==orientation:
                return str(1+section)
            else:
                return 'Title'

    def data(self, index, role=Qt.DisplayRole):
        """QAbstractItemModel
        """
        if not index.isValid():
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
            elif ImageRole == role:
                return self._image
            elif MetadataRole == role:
                return item['metadata']

    def setData(self, index, value, role):
        # TODO LH Validation?
        if RectRole == role:
            current = self._data[index.row()]['rect']
            debug_print('Model.setData rect for [{0}] from [{1}] to [{2}]'.format(index.row(), current, value))
            self._data[index.row()]['rect'] = value
            self.dataChanged.emit(index, index)
            return True
        elif RotationRole == role:
            current = self._data[index.row()]['rotation']
            value = (value+360) % 360
            debug_print('Model.setData rotation for [{0}] from [{1}] to [{2}]'.format(index.row(), current, value))
            # Constrain angle to be in range 0:360
            self._data[index.row()]['rotation'] = value
            self.dataChanged.emit(index, index)
            return True
        else:
            return super(Model, self).setData(index, value, role)

    def removeRows(self, row, count, parent=QModelIndex()):
        debug_print('Model.removeRows row [{0}] count [{1}]'.format(row, count))

        first, last = row, row+count

        self.beginRemoveRows(parent, first, last)
        del self._data[first:last]
        self.endRemoveRows()

        return True
