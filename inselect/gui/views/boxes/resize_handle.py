from PySide.QtGui import QGraphicsItem
from PySide.QtCore import Qt, QRectF

from inselect.lib.utils import debug_print


class ResizeHandle(QGraphicsItem):
    """A resize handle
    """

    # Ideas taken from QT Fotowall application
    # http://qt-apps.org/content/show.php?content=71316
    def __init__(self, corner, parent=None):
        super(ResizeHandle, self).__init__(parent)

        if corner not in list(Qt.Corner.values.values()):
            raise ValueError('Bad corner [{0}]'.format(corner))
        else:
            self._corner = corner
            self.setAcceptsHoverEvents(True)
            if corner in (Qt.TopLeftCorner, Qt.BottomRightCorner):
                self.setCursor(Qt.SizeFDiagCursor)
            else:
                self.setCursor(Qt.SizeBDiagCursor)

    def layout(self, parent_rect):
        """Sets position in parent coordinates
        """
        # Map Qt.Corner to the appropriate method of QRectF
        if Qt.TopLeftCorner == self._corner:
            location = parent_rect.topLeft()
        elif Qt.TopRightCorner == self._corner:
            location = parent_rect.topRight()
        elif Qt.BottomLeftCorner == self._corner:
            location = parent_rect.bottomLeft()
        else:
            # Qt.BottomRightCorner
            location = parent_rect.bottomRight()

        self.setPos(location)

    def boundingRect(self):
        """QGraphicsItem virtual
        """
        size = 20   # Local coordinate units
        return QRectF(-size/2, -size/2, size, size)

    def mousePressEvent(self, event):
        """QGraphicsItem virtual
        """
        debug_print('ResizeHandle.mousePressEvent')
        event.accept()  # Grab the mouse

        # Select parent and deselect everything else
        parent = self.parentItem()
        selected = set(self.scene().selectedItems())
        for deselect in selected.difference([parent]):
            deselect.setSelected(False)

        if parent not in selected:
            parent.setSelected(True)

        # Redraw parent and corners
        parent.update()

    def mouseMoveEvent(self, event):
        """QGraphicsItem virtual
        """
        debug_print('ResizeHandle.mouseMoveEvent')

        # Vector difference between the mouse's position and current position,
        # both in client coordinates
        parent = self.parentItem()
        v = event.pos() - self.mapFromItem(parent, self.pos())
        if v.isNull():
            debug_print('v.isNull')
        else:
            # Compute adjustments to parent item's rect
            dx1 = dy1 = dx2 = dy2 = 0.0
            if Qt.TopLeftCorner == self._corner:
                dx1, dy1 = v.x(), v.y()
            elif Qt.TopRightCorner == self._corner:
                dx2, dy1 = v.x(), v.y()
            elif Qt.BottomLeftCorner == self._corner:
                dx1, dy2 = v.x(), v.y()
            else:
                dx2, dy2 = v.x(), v.y()

            rect = parent.rect().adjusted(dx1, dy1, dx2, dy2)

            if not rect.isValid():
                # A valid rectangle has a width() > 0 and height() > 0
                # rect will be invalid if the user has attempted to drag the box
                # inside out - prevent this
                pass
            else:
                parent.prepareGeometryChange()
                parent.setRect(rect)

    def mouseReleaseEvent(self, event):
        """QGraphicsItem virtual
        """
        debug_print('ResizeHandle.mouseReleaseEvent')

        # Redraw parent and corners
        self.parentItem().update()

    def paint(self, painter, option, widget):
        """QGraphicsItem virtual
        """
        painter.fillRect(self.boundingRect(), self.parentItem().colours[0])
