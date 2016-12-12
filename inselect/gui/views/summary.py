import locale

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QAbstractItemView, QHBoxLayout, QLabel, QWidget

from inselect.lib.utils import debug_print


class SummaryView(QAbstractItemView):
    """View that provides a summary of the model
    """
    def __init__(self, parent=None):
        # This view is not visible
        super(SummaryView, self).__init__(None)

        self.info = QLabel()

        # Last item has stretch greater than zero to force all labels to be
        # left-aligned
        layout = QHBoxLayout()

        # Smaller margins than the defaults
        layout.setContentsMargins(
            8,  # left
            2,  # top
            0,  # right
            2   # bottom
        )

        layout.addWidget(self.info, stretch=1)

        self.widget = QWidget(parent)
        self.widget.setLayout(layout)

    def _updated(self, n, selected):
        template = '{0} boxes / {1} selected / {2}'
        self.info.setText(template.format(
            locale.format("%d", n, grouping=True),
            locale.format("%d", len(selected), grouping=True),
            selected[0].data(Qt.DisplayRole) if 1 == len(selected) else ''
        ))

    def reset(self):
        """QAbstractItemView virtual
        """
        debug_print('SummaryView.reset')
        super(SummaryView, self).reset()
        self._updated(self.model().rowCount(), [])

    def setModel(self, model):
        """QAbstractItemView virtual
        """
        debug_print('SummaryView.setModel', model, model.rowCount(),
                    model.columnCount())
        super(SummaryView, self).setModel(model)

    def dataChanged(self, topLeft, bottomRight, roles=[]):
        """QAbstractItemView virtual
        """
        debug_print('SummaryView.dataChanged')
        self._updated(
            self.model().rowCount(), self.selectionModel().selectedIndexes()
        )

    def selectionChanged(self, selected, deselected):
        """QAbstractItemView slot
        """
        debug_print('SummaryView.selectionChanged')
        self._updated(
            self.model().rowCount(), self.selectionModel().selectedIndexes()
        )

    def rowsAboutToBeRemoved(self, parent, start, end):
        """QAbstractItemView slot
        """
        debug_print('SummaryView.rowsAboutToBeRemoved')
        self._updated(
            self.model().rowCount() - (end - start),
            self.selectionModel().selectedIndexes()
        )
