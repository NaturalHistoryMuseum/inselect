from PySide import QtCore, QtGui
from PySide.QtCore import Qt

from inselect.lib.utils import debug_print
from inselect.gui.roles import MetadataRole


class MetadataView(QtGui.QAbstractItemView):
    def __init__(self, parent=None):
        # This view is not visible
        super(MetadataView, self).__init__(None)

        self.layout = QtGui.QFormLayout()
        self.specimen_number = UpdateModelLineEdit('Specimen number', self.model())
        self.layout.addRow("&Specimen number:", self.specimen_number)

        self.widget = QtGui.QWidget(parent)
        self.widget.setLayout(self.layout)
        # self.setItemDelegate(LineEditDelegate())

    def selectionChanged(self, selected, deselected):
        """QAbstractItemView slot
        """
        debug_print('MetadataView.selectionChanged')
        sn = {}
        for index in self.selectionModel().selectedIndexes():
            sn = {i.get('Specimen number','') for i in index.data(MetadataRole)}
        print(sn)


class UpdateModelLineEdit(QtGui.QLineEdit):
    """Updates the relevant model field when the control looses focus
    """
    def __init__(self, field, parent=None):
        super(UpdateModelLineEdit, self).__init__(parent)
        self._field = field

    def focusOutEvent(self, event):
        if QtCore.QEvent.FocusOut == event.type():
            debug_print('UpdateModelFilter.eventFilter', self._field,
                        self, self.isModified())
            self.setModified(False)
        return False

