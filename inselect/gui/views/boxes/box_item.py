from PySide import QtCore, QtGui
from PySide.QtCore import Qt

from inselect.lib.utils import debug_print
from inselect.gui.utils import PaintState

from .resize_handle import ResizeHandle


class BoxItem(QtGui.QGraphicsRectItem):
    # Might be some relevant stuff here:
    # http://stackoverflow.com/questions/10590881/events-and-signals-in-qts-qgraphicsitem-how-is-this-supposed-to-work

    UNSELECTED = QtGui.QColor(0x00, 0x00, 0xff, 0xcc)
    SELECTED =   QtGui.QColor(0xff, 0x00, 0x00, 0xcc)
    RESIZING =   QtGui.QColor(0xff, 0x00, 0x00, 0x50)

    def __init__(self, x, y, w, h, parent=None, scene=None):
        super(BoxItem, self).__init__(x, y, w, h, parent, scene)
        self.setFlags(QtGui.QGraphicsItem.ItemIsFocusable |
                      QtGui.QGraphicsItem.ItemIsSelectable |
                      QtGui.QGraphicsItem.ItemSendsGeometryChanges |
                      QtGui.QGraphicsItem.ItemIsMovable)

        self.setCursor(Qt.ArrowCursor)
        self.setAcceptHoverEvents(True)

        self._handles_visible = False
        self._handles = []

        positions = (Qt.TopLeftCorner, Qt.TopRightCorner, Qt.BottomLeftCorner,
                     Qt.BottomRightCorner)
        self._handles = [self._create_handle(pos) for pos in positions]
        self._layout_handles()

    def paint(self, painter, option, widget=None):
        """QGraphicsRectItem virtual
        """
        # Thick red border is selected
        # Think blue border if not
        thickness = 3 if self.isSelected() else 1
        with PaintState(painter):
            painter.setPen(QtGui.QPen(self.colour, thickness, Qt.SolidLine))
            painter.drawRect(self.boundingRect())

    @property
    def colour(self):
        """QtGui.QColor
        """
        if self.scene().mouseGrabberItem() in self._handles:
            return self.RESIZING
        else:
            return self.SELECTED if self.isSelected() else self.UNSELECTED

    def hoverEnterEvent(self, event):
        """QGraphicsRectItem virtual
        """
        debug_print('BoxItem.hoverEnterEvent')
        super(BoxItem, self).hoverEnterEvent(event)
        self._set_handles_visible(True)

    def hoverLeaveEvent(self, event):
        """QGraphicsRectItem virtual
        """
        debug_print('BoxItem.hoverLeaveEvent')
        super(BoxItem, self).hoverLeaveEvent(event)
        self._set_handles_visible(False)

    def _set_handles_visible(self, visible):
        self._handles_visible = visible
        map(lambda i: i.setVisible(visible), self._handles)

    def _create_handle(self, corner):
        # Creates and returns a new ResizeHandle at the given Qt.Corner
        handle = ResizeHandle(corner, self)
        handle.setZValue(2.0)
        handle.setVisible(self._handles_visible)
        return handle

    def _layout_handles(self):
        """Moves handles to the appropriate positions
        """
        map(lambda i: i.relayout(self.boundingRect()), self._handles)

    def update_handles(self):
        """Updates handles
        """
        for item in self._handles + [self]:
            item.update()

    def setRect(self, rect):
        """QGraphicsRectItem function
        """
        debug_print('setRect')
        super(BoxItem, self).setRect(rect)
        self._layout_handles()

    def mousePressEvent(self, event):
        """QGraphicsRectItem virtual
        """
        debug_print('mousePressEvent')
        super(BoxItem, self).mousePressEvent(event)
        self.update_handles()
