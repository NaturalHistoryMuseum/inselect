from PySide import QtCore, QtGui
from PySide.QtCore import QSettings


class AnnotateDialog(QtGui.QDialog):
    """ Dialog that handles annotation of a segment. """
    def __init__(self, boxes, parent=None):
        super(AnnotateDialog, self).__init__(parent)
        self.fields = QSettings('NHM', 'Inselect').value('annotation_fields')
        if isinstance(boxes, list):
            self.list_items = [box.list_item for box in boxes] 
        else:
            self.list_items = [boxes.list_item]
        self.parent = parent
        # set size and placement
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Popup)
        self.resize(max(500, int(0.66 * self.parent.width())),
                    max(500, int(0.66 * self.parent.height())))
        screen_rect = self.parent.app.desktop().availableGeometry()
        self.move(screen_rect.center() - self.rect().center())

        self.layout = QtGui.QGridLayout(self)
        self.setWindowTitle('Annotate Segment')
        label = QtGui.QLabel(self)
        if len(self.list_items) == 1:
            icon = self.parent.get_icon(self.list_items[0].box)
            pixmap = icon.pixmap(icon.availableSizes()[0])
            label.setPixmap(pixmap)
        self.num_fields = len(self.fields)
        self.table = QtGui.QTableWidget(self.num_fields, 1)
        self.table.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.table.setVerticalHeaderLabels(self.fields)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().hide()
        self.table.itemChanged.connect(self._item_changed)

        self.layout.addWidget(label, 0, 0)
        self.layout.addWidget(self.table, 0, 1)
        self.setLayout(self.layout)

        if len(self.list_items) == 1:
            # load data from list item
            for row, field in enumerate(self.fields):
                if field in self.list_items[0].fields:
                    item = QtGui.QTableWidgetItem()
                    item.setData(QtCore.Qt.EditRole, 
                                 self.list_items[0].fields[field])
                    self.table.setItem(row, 0, item)

        self.table.setFocus()

    def _item_changed(self, item):
        row = item.row()
        field = self.fields[row]
        for list_item in self.list_items:
            list_item.fields[field] = item.text()
