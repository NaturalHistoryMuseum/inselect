from PySide.QtCore import Qt
from PySide.QtGui import (QAbstractItemView, QHBoxLayout, QLabel, QSlider,
                          QWidget)

from inselect.lib.utils import debug_print
from inselect.gui.roles import RectRole
from inselect.gui.utils import update_selection_model


class SelectorView(QAbstractItemView):
    """View that sets selection by objects' relative size
    """
    def __init__(self, parent=None):
        # This view is not visible
        super(SelectorView, self).__init__(None)

        layout = QHBoxLayout()
        layout.addWidget(QLabel("Select by size"))

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setTickPosition(QSlider.TicksBothSides)
        self.slider.setMinimum(-1)
        self.slider.setMaximum(1)
        self.slider.setTickInterval(1)
        self.slider.setSingleStep(1)
        self.slider.setEnabled(False)

        self.slider.valueChanged.connect(self._slider_changed)
        self.slider.sliderReleased.connect(self._slider_released)
        self.slider.sliderPressed.connect(self._slider_pressed)

        # Slider has stretch greater than zero to force left-alignment
        layout.addWidget(self.slider, stretch=1)

        self.widget = QWidget(parent)
        self.widget.setLayout(layout)

    def _update_slider(self):
        """Sets the slider range and enabled state
        """
        n = self.model().rowCount()
        self.slider.setEnabled(n > 0)
        if n:
            # Scale runs from -n to + n in steps of 1
            self.slider.setMinimum(-n)
            self.slider.setMaximum(n)
            self.slider.setTickInterval(n)
            self.slider.setSingleStep(1)
        self.slider.setEnabled(n > 0)

    def _slider_changed(self, value):
        """QSlider.valueChanged slot
        """
        debug_print('_slider_changed', value)
        if 0 == value:
            # Do not alter selection if value is 0
            pass
        else:
            # Order items by area and send first / last n
            model = self.model()
            rows = xrange(model.rowCount())

            def box_area(row):
                rect = model.index(row, 0).data(RectRole)
                return rect.width() * rect.height()
            rows = sorted(rows, key=box_area)
            if value > 0:
                select = rows[:value]
            else:
                select = rows[value:]
            update_selection_model(model, self.selectionModel(), select)

    def _slider_released(self):
        """QSlider.sliderReleased slot
        """
        debug_print('_slider_released')
        self.slider.setValue(0)

    def _slider_pressed(self):
        """QSlider.sliderPressed slot
        """
        debug_print('_slider_pressed')
        if 0 == self.slider.value():
            # User clicked on the centre (0) of the slider
            self.selectionModel().clear()

    def reset(self):
        """QAbstractItemView virtual
        """
        debug_print('SelectorView.reset')
        super(SelectorView, self).reset()
        self._update_slider()

    def dataChanged(self, topLeft, bottomRight):
        """QAbstractItemView virtual
        """
        debug_print('SelectorView.dataChanged')
        self._update_slider()

    def rowsAboutToBeRemoved(self, parent, start, end):
        """QAbstractItemView slot
        """
        debug_print('SelectorView.rowsAboutToBeRemoved')
        self._update_slider()
