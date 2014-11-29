from PySide import QtGui, QtCore

class SpecimenCropGrid(QtGui.QListWidget):
    """A grid of cropped specimen images
    """
    def __init__(self, parent=None):
        super(SpecimenCropGrid, self).__init__(parent)

        self.setIconSize(QtCore.QSize(100, 100))
        self.setViewMode(QtGui.QListView.IconMode)
        self.setDragEnabled(False)
        self.setResizeMode(QtGui.QListView.Adjust)
        self.setMovement(QtGui.QListView.Static)
        self.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.setMinimumWidth(100)

    def refresh(self, items):
        list_item = QtGui.QListWidgetItem()
        self.insertItem(index, list_item)
