from PySide import QtCore, QtGui
import inselect.settings


class AnnotateDialog(QtGui.QDialog):
    """ Dialog that handles annotation of a segment. """
    def __init__(self, segment_scene, segments, parent=None):
        super(AnnotateDialog, self).__init__(parent)
        self.fields = inselect.settings.get('annotation_fields')
        self.parent = parent
        if isinstance(segments, list):
            self.segments = list(segments)
        else:
            self.segments = [segments]
        # set size and placement
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Popup)
        self.resize(max(500, int(0.66 * self.parent.width())),
                    max(500, int(0.66 * self.parent.height())))
        screen_rect = self.parent.app.desktop().availableGeometry()
        self.move(screen_rect.center() - self.rect().center())

        self.layout = QtGui.QGridLayout(self)
        self.setWindowTitle('Annotate Segment')
        label = QtGui.QLabel(self)
        if len(self.segments) == 1:
            icon = segment_scene.get_segment_icon(self.segments[0])
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

        if len(self.segments) == 1:
            # load data from segments
            segment_values = self.segments[0].fields()
            for row, field in enumerate(self.fields):
                if field in segment_values:
                    item = QtGui.QTableWidgetItem()
                    item.setData(QtCore.Qt.EditRole, 
                                 segment_values[field])
                    self.table.setItem(row, 0, item)

        self.table.setFocus()

    def _item_changed(self, item):
        row = item.row()
        field = self.fields[row]
        for segment in self.segments:
            segment.set_field(field, item.text())
