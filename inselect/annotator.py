from PySide import QtCore, QtGui


class AnnotateDialog(QtGui.QDialog):
    """ Dialog that handles annotation of a segment. """
    fields = ["Specimen Number", "Current Taxon Name",
              "Location in Collection"]

    def __init__(self, item, parent=None):
        super(AnnotateDialog, self).__init__(parent)
        self.list_item = item
        self.parent = parent
        # set size and placement
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Popup)
        self.resize(max(500, int(0.66 * self.parent.width())),
                    max(500, int(0.66 * self.parent.height())))
        screen_rect = self.parent.app.desktop().availableGeometry()
        self.move(screen_rect.center() - self.rect().center())

        self.layout = QtGui.QGridLayout(self)
        self.setWindowTitle('Annotate Segment')
        icon = self.parent.get_icon(item.box)
        label = QtGui.QLabel(self)
        pixmap = icon.pixmap(icon.availableSizes()[0])
        self.num_fields = len(self.fields)
        label.setPixmap(pixmap)
        self.table = QtGui.QTableWidget(self.num_fields, 1)
        self.table.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.table.setVerticalHeaderLabels(self.fields)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().hide()
        self.table.itemChanged.connect(self._item_changed)

        self.layout.addWidget(label, 0, 0)
        self.layout.addWidget(self.table, 0, 1)
        self.setLayout(self.layout)

        # load data from list item
        for row, field in enumerate(self.fields):
            if field in self.list_item.fields:
                item = QtGui.QTableWidgetItem()
                item.setData(QtCore.Qt.EditRole, self.list_item.fields[field])
                self.table.setItem(row, 0, item)

        self.table.setFocus()

    def _item_changed(self, item):
        row = item.row()
        field = self.fields[row]
        self.list_item.fields[field] = item.text()
