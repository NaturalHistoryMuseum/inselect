from PySide import QtGui, QtCore

from inselect.gui.annotator import AnnotateDialog


class SegmentListItem(QtGui.QListWidgetItem):
    def __init__(self, icon, text, parent=None, box=None):
        super(SegmentListItem, self).__init__(icon, text, parent)
        self.original_icon = icon
        self.original_text = text
        self.box = box
        self.fields = {}


class SegmentListWidget(QtGui.QListWidget):
    def __init__(self, parent=None):
        super(SegmentListWidget, self).__init__(parent)
        self.setIconSize(QtCore.QSize(100, 100))
        self.setViewMode(QtGui.QListView.IconMode)
        self.setDragEnabled(False)
        self.setResizeMode(QtGui.QListView.Adjust)
        self.setMovement(QtGui.QListView.Static)
        self.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.itemDoubleClicked.connect(self.on_item_double_clicked)
        self.setMinimumWidth(100)
        self.enable = True
        self.parent = parent

    def selectionChanged(self, selected_items, deselected_items):
        for i in range(self.count()):
            item = self.item(i)
            selected = item.isSelected()
            item.box.setSelected(selected)
        QtGui.QListWidget.selectionChanged(self, selected_items,
                                           deselected_items)

    def keyPressEvent(self, event):
        if event.key() in [QtCore.Qt.Key_Delete, QtCore.Qt.Key_Return,
                           ord('Z')]:
            self.parent.view.keyPressEvent(event)
        QtGui.QListWidget.keyPressEvent(self, event)

    def on_item_double_clicked(self, item):
        dialog = AnnotateDialog(item.box, parent=self.parent)
        dialog.exec_()


