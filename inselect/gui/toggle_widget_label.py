from PySide.QtCore import Qt
from PySide.QtGui import QLabel


class ToggleWidgetLabel(QLabel):
    """A QLabel that, when clicked, toggles the visibility of a widget
    """
    def __init__(self, label, widget, parent=None, flags=0):
        super(ToggleWidgetLabel, self).__init__(label, parent, flags)
        self.widget = widget
        self.setCursor(Qt.PointingHandCursor)

    def mouseReleaseEvent(self, event):
        """QLabel virtual
        """
        self.toggle()

    def toggle(self):
        """Toggle the visible state of self.widget
        """
        visible = self.widget.isVisible()
        self.widget.setVisible(not visible)
