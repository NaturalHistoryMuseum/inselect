from PySide.QtCore import Qt
from PySide.QtGui import QGroupBox, QVBoxLayout

from .toggle_widget_label import ToggleWidgetLabel


class PopupPanel(QGroupBox):
    """A ToggleWidgetLabel and a widget contained within a QGroupBox
    """
    def __init__(self, label, widget, parent=None, flags=0):
        super(PopupPanel, self).__init__(parent, flags)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        layout.addWidget(ToggleWidgetLabel(label, widget))
        layout.addWidget(widget)
        self.setLayout(layout)
