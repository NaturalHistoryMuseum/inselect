from PySide.QtGui import (QBrush, QPainter, QPen, QSizePolicy, QTabBar,
                          QTabWidget)


class Ribbon(QTabWidget):
    """A QTabWidget with a defined background colour and bottom margin colour.

    I found it impossible to alter the background of a QTabWidget using
    stylesheets, even when using QTabWidget's documentMode.
    """
    def __init__(self, background_colour, bottom_margin_colour, parent=None):
        super(Ribbon, self).__init__(parent)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.setUsesScrollButtons(False)

        self.brush = QBrush(background_colour)
        self.pen = QPen(background_colour)
        self.bottom_margin = QPen(bottom_margin_colour, 1)

    def paintEvent(self, event):
        painter = QPainter(self)

        # Background
        painter.setBrush(self.brush)
        painter.setPen(self.pen)
        rect = self.rect()
        painter.drawRect(rect)

        # Line along bottom
        tab_bar_rect = self.findChild(QTabBar).rect()
        rect.moveBottom(tab_bar_rect.bottom())
        painter.setPen(self.bottom_margin)
        painter.drawLine(rect.bottomLeft(), rect.bottomRight())
