from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QWidget


class ToggleWidgetLabel(QWidget):
    """A QLabel that, when clicked, toggles the visibility of a widget
    """

    SIZE = 16

    # Can't create instances of QPixmap until QApplication has been created
    # See classmethods up and down
    UP = None
    DOWN = None

    def __init__(self, label, widget, initially_visible=True, parent=None,
                 flags=Qt.WindowFlags(0)):
        super(ToggleWidgetLabel, self).__init__(parent, flags)
        self.widget = widget

        self.arrow = QLabel()
        self.arrow.setFixedSize(self.SIZE, self.SIZE)
        self.arrow.setPixmap(
            self.down() if initially_visible else self.up()
        )

        layout = QHBoxLayout()
        layout.addWidget(QLabel(label), Qt.AlignLeft)
        layout.addWidget(self.arrow, Qt.AlignRight)
        self.setLayout(layout)

        self.setCursor(Qt.PointingHandCursor)
        self.setContentsMargins(0, 0, 0, 0)

    def mouseReleaseEvent(self, event):
        """QLabel virtual
        """
        self.toggle()

    def toggle(self):
        """Toggle the visible state of self.widget
        """
        current = self.widget.isVisible()
        self.widget.setVisible(not current)
        self.arrow.setPixmap(self.up() if current else self.down())

    @classmethod
    def up(cls):
        # TODO LH recolor arrow images using text color
        # Perhaps using http://stackoverflow.com/a/22152735
        if not cls.UP:
            cls.UP = QPixmap(':/icons/up_arrow.png').scaled(
                cls.SIZE, cls.SIZE, Qt.IgnoreAspectRatio, Qt.FastTransformation
            )
        return cls.UP

    @classmethod
    def down(cls):
        if not cls.DOWN:
            cls.DOWN = QPixmap(':/icons/down_arrow.png').scaled(
                cls.SIZE, cls.SIZE, Qt.IgnoreAspectRatio, Qt.FastTransformation
            )
        return cls.DOWN
