from PySide import QtCore, QtGui
from PySide.QtCore import Qt

from inselect.lib.utils import debug_print
from inselect.gui.roles import MetadataRole


class MetadataView(QtGui.QAbstractItemView):
    def __init__(self, parent=None):
        # This view is not visible
        super(MetadataView, self).__init__(parent)

        # TODO LH Metadata to come from config
        fields = ['Specimen number', 'Taxonomic group', 'Location']

        # A mapping from field name to UpdateModelLineEdit control
        self._edits = {f:UpdateModelLineEdit(f) for f in fields}

        # Show controls stacked vertically
        self.layout = QtGui.QFormLayout()
        self.title = QtGui.QLabel()
        self.layout.addRow(self.title)
        for field, edit in self._edits.items():
            self.layout.addRow(field, edit)

        self.widget = QtGui.QWidget(parent)
        self.widget.setLayout(self.layout)

    def selectionChanged(self, selected, deselected):
        """QAbstractItemView slot
        """
        debug_print('MetadataView.selectionChanged')
        selected = self.selectionModel().selectedIndexes()
        for field, edit in self._edits.items():
            v = {i.data(MetadataRole).get(field,'') for i in selected}
            edit.setText(','.join(sorted(v)))
            edit.selected = selected
            edit.setEnabled(len(selected) > 0)
        if selected:
            self.title.setText('Metadata for {0} boxes'.format(len(selected)))
        else:
            self.title.setText('Metadata')


class UpdateModelLineEdit(QtGui.QLineEdit):
    """Updates the relevant model field when the control looses focus
    """
    def __init__(self, field, parent=None):
        super(UpdateModelLineEdit, self).__init__(parent)
        self.selected = None
        self.setEnabled(False)
        self._field = field

    def focusOutEvent(self, event):
        debug_print('UpdateModelLineEdit.focusOutEvent')
        if QtCore.QEvent.FocusOut == event.type() and self.isModified():
            self.setModified(False)
            new = {self._field : self.text()}
            for i in self.selected:
                i.model().setData(i, new, MetadataRole)

        super(UpdateModelLineEdit, self).focusOutEvent(event)
