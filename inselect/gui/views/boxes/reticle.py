from PyQt5.QtCore import QPoint, QRectF, Qt
from PyQt5.QtGui import QBrush, QColor, QPainter, QPen
from PyQt5.QtWidgets import QGraphicsItem

from inselect.gui.utils import painter_state


class Reticle(QGraphicsItem):
    # Local coordinate units
    SIZE = 26
    HALF_SIZE = SIZE / 2

    PEN = QPen(Qt.black, 1, Qt.SolidLine)
    FILL = QBrush(QColor(0xff, 0xff, 0xff, 0x60))

    def __init__(self, offset, parent=None):
        super(Reticle, self).__init__(parent)
        # A QPoint offset from parent object's top-left.
        self.offset = offset

    def layout(self, parent_rect):
        """Sets position in parent coordinates
        """
        # Rect - parent's bounding rect
        self.setPos(parent_rect.topLeft() + self.offset)

    def boundingRect(self):
        """QGraphicsItem virtual
        """
        size = self.SIZE
        return QRectF(-size / 2, -size / 2, size, size)

    def paint(self, painter, option, widget):
        """QGraphicsItem virtual
        """
        with painter_state(painter):
            painter.setRenderHint(QPainter.Antialiasing)
            bounding = self.boundingRect()

            # Black circle, with partially transparent white fill
            painter.setPen(self.PEN)
            painter.setBrush(self.FILL)
            painter.drawEllipse(bounding)

            # Filled black circle at centre
            painter.setBrush(QBrush(Qt.black))
            painter.drawEllipse(bounding.center(), 2, 2)

            # Black crosshair
            size = self.SIZE
            half_size = self.HALF_SIZE
            painter.drawLine(
                bounding.topLeft() + QPoint(0, half_size),
                bounding.topLeft() + QPoint(size, half_size)
            )
            painter.drawLine(
                bounding.topLeft() + QPoint(half_size, 0),
                bounding.topLeft() + QPoint(half_size, size)
            )
