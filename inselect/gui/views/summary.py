import locale
from PySide import QtCore
from PySide.QtGui import QAbstractItemView, QHBoxLayout, QLabel, QWidget

from inselect.lib.utils import debug_print


class SummaryView(QAbstractItemView):
    """View that provides a summary of the model
    """
    def __init__(self, parent=None):
        # This view is not visible
        super(SummaryView, self).__init__(None)

        self.n_boxes = QLabel()
        self.n_selected = QLabel()
        self.selected_label = QLabel()

        # Last item has stretch greater than zero to force all labels to be
        # left-aligned
        layout = QHBoxLayout()
        layout.addWidget(self.n_boxes)
        layout.addWidget(self.n_selected)
        layout.addWidget(self.selected_label, stretch=1)

        self.widget = QWidget(parent)
        self.widget.setLayout(layout)

    def _n_boxes(self, n):
        self.n_boxes.setText(
            '{0} boxes'.format(locale.format("%d", n, grouping=True))
        )

    def _n_selected(self, n):
        self.n_selected.setText(
            '{0} selected'.format(locale.format("%d", n, grouping=True))
        )

    def _selected_label(self, selected):
        if 1 == len(selected):
            self.selected_label.setText(selected[0].data(QtCore.Qt.DisplayRole))
        else:
            self.selected_label.setText('')

    def reset(self):
        """QAbstractItemView virtual
        """
        debug_print('SummaryView.reset')
        super(SummaryView, self).reset()
        self._n_boxes(self.model().rowCount())
        self._n_selected(0)
        self._selected_label([])

    def setModel(self, model):
        """QAbstractItemView virtual
        """
        debug_print('SummaryView.setModel', model, model.rowCount(),
                    model.columnCount())
        super(SummaryView, self).setModel(model)

    def dataChanged(self, topLeft, bottomRight):
        """QAbstractItemView virtual
        """
        debug_print('SummaryView.dataChanged')
        self._n_boxes(self.model().rowCount())
        self._selected_label(self.selectionModel().selectedIndexes())

    def selectionChanged(self, selected, deselected):
        """QAbstractItemView slot
        """
        debug_print('SummaryView.selectionChanged')
        selected = self.selectionModel().selectedIndexes()
        self._n_selected(len(selected))
        self._selected_label(selected)

    def rowsAboutToBeRemoved(self, parent, start, end):
        """QAbstractItemView slot
        """
        debug_print('SummaryView.rowsAboutToBeRemoved')
        self._n_boxes(self.model().rowCount() - (end - start))
