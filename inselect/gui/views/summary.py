from PySide.QtGui import QAbstractItemView, QHBoxLayout, QLabel, QWidget

from inselect.lib.utils import debug_print


class SummaryView(QAbstractItemView):
    """View that provides a summary of the model
    """
    def __init__(self, parent=None):
        # This view is not visible
        super(SummaryView, self).__init__(None)

        layout = QHBoxLayout()

        self.n_boxes = QLabel()
        layout.addWidget(self.n_boxes)

        # Last item has stretch greater than zero to force all labels to be
        # left-aligned
        self.n_selected = QLabel()
        layout.addWidget(self.n_selected, stretch=1)

        self.widget = QWidget(parent)
        self.widget.setLayout(layout)

    def _n_boxes(self, n):
        self.n_boxes.setText('{0} boxes'.format(n))

    def _n_selected(self, n):
        self.n_selected.setText('{0} selected'.format(n))

    def reset(self):
        """QAbstractItemView virtual
        """
        debug_print('SummaryView.reset')
        super(SummaryView, self).reset()
        self._n_boxes(self.model().rowCount())
        self._n_selected(0)

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

    def selectionChanged(self, selected, deselected):
        """QAbstractItemView slot
        """
        debug_print('SummaryView.selectionChanged')
        n = len(self.selectionModel().selectedIndexes())
        self.n_selected.setText('{0} selected'.format(n))

    def rowsAboutToBeRemoved(self, parent, start, end):
        """QAbstractItemView slot
        """
        debug_print('SummaryView.rowsAboutToBeRemoved')
        self._n_boxes(self.model().rowCount() - (end - start))
