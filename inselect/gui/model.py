from copy import deepcopy

from qtpy.QtCore import Qt, QAbstractItemModel, QModelIndex, QRect, Signal
from qtpy.QtGui import QPixmap

from inselect.lib.utils import debug_print

from .roles import (MetadataRole, MetadataValidRole, PixmapRole, RectRole,
                    RotationRole)
from .user_template_choice import user_template_choice
from .utils import qimage_of_bgr


class Model(QAbstractItemModel):
    """
    """

    # TODO LH Model should encapsulate InselectDocument
    # TODO LH Plugins should operate on Model, not InselectDocument

    # Emitted when modified status changes
    modified_changed = Signal()

    DISPLAY_TEMPLATE = '{0} {1}'
    LEADING_ZEROES = '{0:04d}'

    def __init__(self, parent=None):
        super(Model, self).__init__(parent)
        self._modified = False
        self._data = []             # A list of dicts
        self._image_array = None    # np.nd_array, for segmentation
        self._pixmap = None         # Instance of QPixmap

        user_template_choice().template_changed.connect(self.user_template_changed)

    def _clear_model_data(self):
        """Clear data structures
        """
        self.set_modified(False)
        self._data = []
        self._image_array = None
        self._pixmap = None

    def clear(self):
        """Empty data
        """
        self.beginResetModel()
        self._clear_model_data()
        self.endResetModel()

    def from_document(self, document):
        """Load data from document
        """
        # Load the new data
        # Document promises that either the thumbnail or scanned image will be
        # available
        if document.thumbnail.available:
            debug_print('Model will work on thumbnail')
            image_array = document.thumbnail.array
        else:
            debug_print('Model will work on full-res scan')
            image_array = document.scanned.array

        pixmap = QPixmap.fromImage(qimage_of_bgr(image_array))
        data = self._boxes_from_items(
            document.items, pixmap.width(), pixmap.height()
        )

        # Inform views
        self.beginResetModel()
        self._data, self._image_array, self._pixmap = data, image_array, pixmap
        self.endResetModel()

    def _boxes_from_items(self, items, image_width=None, image_height=None):
        """Returns a list of boxes, suitable for use as self._data, created
        from of InselectDocument items
        """
        if not image_width:
            image_width = self._pixmap.width()
            image_height = self._pixmap.height()

        data = [None] * len(items)
        for index, item in enumerate(items):
            # Convert normalised coords to pixel coords for pixmap
            rect = item['rect']
            rect = QRect(int(round(rect[0] * image_width)),
                         int(round(rect[1] * image_height)),
                         int(round(rect[2] * image_width)),
                         int(round(rect[3] * image_height)))
            data[index] = {
                "fields": item.get('fields', {}),
                "rect": rect,
                "rotation": item.get('rotation', 0),
            }
        return data

    def set_new_boxes(self, items):
        """Replaces existing boxes with those in InselectDocument items
        """
        new = self._boxes_from_items(items)

        if self._data:
            self.removeRows(0, self.rowCount())

        if new:
            self.beginInsertRows(QModelIndex(), 0, len(new)-1)
            self._data = new
            self.set_modified(True)
            self.endInsertRows()
            self.dataChanged.emit(self.index(0, 0),
                                  self.index(len(new)-1, 0))

    @property
    def image_array(self):
        """np.nd_array
        """
        return self._image_array

    @property
    def is_modified(self):
        """True if the model has been modified; False if not modified
        """
        return self._modified

    def set_modified(self, modified):
        """Sets modified flag with bool modified. If this changes modified
        flag, also emits self.modified_changed().
        """
        previous, self._modified = self._modified, modified
        if previous != self._modified:
            self.modified_changed.emit()

    def to_document(self, document):
        """Write data to document
        """
        # Convert to normalised boxes
        items = []
        w, h = float(self._pixmap.width()), float(self._pixmap.height())
        for box in self._data:
            # TODO LH Better to use InselectImage to convert to normalised?
            rect = box['rect']
            items.append({
                'rect': (rect.left() / w,
                         rect.top() / h,
                         rect.width() / w,
                         rect.height() / h),
                'fields': box['fields'],
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
            return self.createIndex(row, column)
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

    def data(self, index, role=Qt.DisplayRole):
        """QAbstractItemModel virtual
        """
        if PixmapRole == role:
            # This role applies to the document as a whole
            return self._pixmap
        elif not index.isValid():
            return None
        else:
            item = self._data[index.row()]
            if role in (Qt.DisplayRole, Qt.ToolTipRole):
                # Title generated by the metadata template. Title is prefix with
                # formatted row index, if title and formatted row index are
                # different

                title = user_template_choice().current.format_label(
                    1 + index.row(),
                    item['fields']
                )
                formatted_index = self.LEADING_ZEROES.format(1 + index.row())
                if formatted_index != title:
                    title = self.DISPLAY_TEMPLATE.format(formatted_index, title)
                return title
            elif Qt.WhatsThisRole == role:
                return 'Cropped object image'
            elif RectRole == role:
                return item['rect']
            elif RotationRole == role:
                return item['rotation']
            elif MetadataRole == role:
                return item['fields']
            elif MetadataValidRole == role:
                return user_template_choice().current.validate_metadata(
                    item['fields']
                )

    def setData(self, index, value, role):
        """QAbstractItemModel virtual
        """
        if RectRole == role:
            # A new QRect for index
            if not isinstance(value, QRect):
                raise ValueError('Value is not a QRect')
            else:
                current = self._data[index.row()]['rect']

                msg = 'Model.setData rect for [{0}] from [{1}] to [{2}]'
                debug_print(msg.format(index.row(), current, value))

                if value != self._data[index.row()]['rect']:
                    self._data[index.row()]['rect'] = value
                    self.dataChanged.emit(index, index)
                    self.set_modified(True)
                    return True
        elif RotationRole == role:
            # A new rotation for index
            if not isinstance(value, int) or 0 != value % 90:
                raise ValueError('Value is not an integer multiple of 90')
            else:
                current = self._data[index.row()]['rotation']

                # Constrain angle to be in range 0:360
                value = (value+360) % 360

                msg = 'Model.setData rotation for [{0}] from [{1}] to [{2}]'
                debug_print(msg.format(index.row(), current, value))

                if current != value:
                    self._data[index.row()]['rotation'] = value
                    self.dataChanged.emit(index, index)
                    self.set_modified(True)
                    return True
        elif MetadataRole == role:
            # value is a dict containing one or more fields
            if not isinstance(value, dict):
                raise ValueError('Value is not a dict with recognised keys')
            else:
                msg = 'Model.setData for [{0}] update [{1}]'
                debug_print(msg.format(index.row(), value))

                new = deepcopy(self._data[index.row()]['fields'])
                new.update(value)

                # Only fields that have a value
                new = {k: v for k, v in new.items() if '' != v}

                # Update if only if changed
                if new != self._data[index.row()]['fields']:
                    self._data[index.row()]['fields'] = new
                    self.dataChanged.emit(index, index)
                    self.set_modified(True)
                return True
        else:
            return super(Model, self).setData(index, value, role)

    def insertRow(self, row, parent=QModelIndex()):
        """QAbstractItemModel virtual
        """
        debug_print('Model.insertRow row [{0}]'.format(row))
        return self.insertRows(row, 1, parent)

    def insertRows(self, row, count, parent=QModelIndex()):
        """QAbstractItemModel virtual
        """
        debug_print('Model.insertRows row [{0}] count [{1}]'.format(row, count))

        if row < 0 or row > len(self._data) or count < 1:
            raise ValueError('Bad row [{0}] or count [{1}]'.format(row, count))
        else:
            upper = row + count - 1
            self.beginInsertRows(QModelIndex(), row, upper)

            # Create list of new rows. Cannot use [{whatever}] * count because
            # this will create the same dict instance repeated 'count' times,
            # not 'count' different dict instances
            new_rows = [None] * count
            for i in range(0, count):
                new_rows[i] = {"fields": {},
                               "rect": QRect(0, 0, 0, 0),
                               "rotation": 0}

            self._data[row:row] = new_rows
            self.set_modified(True)
            self.endInsertRows()
            self.dataChanged.emit(self.index(row, 0), self.index(upper, 0))

            return True

    def removeRows(self, row, count, parent=QModelIndex()):
        """QAbstractItemModel virtual
        """
        debug_print('Model.removeRows row [{0}] count [{1}]'.format(row, count))

        if row < 0 or row > len(self._data) or count < 1:
            raise ValueError('Bad row [{0}] or count [{1}]'.format(row, count))
        else:
            first, last = row, row+count

            self.beginRemoveRows(parent, first, last)
            del self._data[first:last]
            self.set_modified(True)
            self.endRemoveRows()

            return True

    def user_template_changed(self):
        """Informs the model that the user's choice of metadata template has
        changed. Informs all views.
        """
        debug_print('Model.user_template_changed')
        if self._data:
            self.dataChanged.emit(self.index(0, 0),
                                  self.index(self.rowCount()-1, 0))
