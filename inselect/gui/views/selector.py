from PySide.QtCore import Qt
from PySide.QtGui import QAbstractItemView, QSizePolicy, QSlider

from inselect.lib.utils import debug_print
from inselect.gui.roles import RectRole
from inselect.gui.utils import update_selection_model


class SelectorView(QAbstractItemView):
    """View that sets selection by objects' relative size
    """
    def __init__(self, parent=None):
        # This view is not visible
        super(SelectorView, self).__init__(None)

        self._updating_selection = False

        self.slider = QSlider(Qt.Horizontal, parent=parent)
        self.slider.setObjectName('viewSelectorSlider')
        self.slider.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.slider.setTickPosition(QSlider.TicksBothSides)
        self.slider.setMinimum(-1)
        self.slider.setMaximum(1)
        self.slider.setTickInterval(1)
        self.slider.setSingleStep(1)
        self.slider.setEnabled(False)
        self.slider.valueChanged.connect(self._slider_changed)

    def _update_slider(self, n):
        """Sets the slider range and enabled state
        """
        self.slider.setEnabled(n > 0)
        if n:
            # Scale runs from -n to + n in steps of 1
            self.slider.setMinimum(-n)
            self.slider.setMaximum(n)
            self.slider.setTickInterval(n)
            self.slider.setSingleStep(1)
            self.slider.setValue(0)

    def _slider_changed(self, value):
        """QSlider.valueChanged slot
        """
        debug_print('SelectorView._slider_changed', value)
        if False and 0 == value:
            # Do not alter selection if value is 0
            pass
        else:
            # Order items by increasing / decreasing area and select the first n
            model = self.model()
            rows = xrange(model.rowCount())

            def box_area(row):
                rect = model.index(row, 0).data(RectRole)
                return rect.width() * rect.height()

            rows = sorted(rows, key=box_area, reverse=value < 0)
            self._updating_selection = True
            try:
                update_selection_model(model, self.selectionModel(), rows[:abs(value)])
            finally:
                self._updating_selection = False

    def single_step(self, larger):
        """Steps the slider up / down
        """
        if self.slider.isEnabled():
            action = QSlider.SliderSingleStepAdd if larger else QSlider.SliderSingleStepSub
            self.slider.triggerAction(action)

    def selectionChanged(self, selected, deselected):
        """QAbstractItemView virtual
        """
        if not self._updating_selection:
            self.slider.setValue(0)

    def reset(self):
        """QAbstractItemView virtual
        """
        debug_print('SelectorView.reset')
        super(SelectorView, self).reset()
        self._update_slider(self.model().rowCount())

    def dataChanged(self, topLeft, bottomRight):
        """QAbstractItemView virtual
        """
        debug_print('SelectorView.dataChanged')
        self._update_slider(self.model().rowCount())

    def rowsAboutToBeRemoved(self, parent, start, end):
        """QAbstractItemView slot
        """
        debug_print('SelectorView.rowsAboutToBeRemoved')
        self._update_slider(self.model().rowCount() - (end - start))
