from itertools import chain

from PySide import QtCore, QtGui
from PySide.QtCore import Qt

from inselect.lib.utils import debug_print
from inselect.gui.utils import PaintState

from .resize_handle import ResizeHandle


class BoxItem(QtGui.QGraphicsRectItem):
    # Might be some relevant stuff here:
    # http://stackoverflow.com/questions/10590881/events-and-signals-in-qts-qgraphicsitem-how-is-this-supposed-to-work

    DRAW_INNER = False

    if True:
        # Blue unselected, red selected
        UNSELECTED = Qt.blue
        SELECTED =   Qt.red
        RESIZING =   QtGui.QColor(0xff, 0x00, 0x00, 0x50)

        INNER =         Qt.black
        INNER_RESIZE =  QtGui.QColor(0x00, 0x00, 0x00, 0x30)
    else:
        # Light outer, dark inner
        UNSELECTED = Qt.lightGray
        SELECTED =   Qt.white
        RESIZING =   QtGui.QColor(0xff, 0xff, 0xff, 0xa0)

        INNER =         Qt.black
        INNER_RESIZE =  QtGui.QColor(0x00, 0x00, 0x00, 0x30)

    def __init__(self, x, y, w, h, parent=None, scene=None):
        super(BoxItem, self).__init__(x, y, w, h, parent, scene)
        self.setFlags(QtGui.QGraphicsItem.ItemIsFocusable |
                      QtGui.QGraphicsItem.ItemIsSelectable |
                      QtGui.QGraphicsItem.ItemSendsGeometryChanges |
                      QtGui.QGraphicsItem.ItemIsMovable)

        self.setCursor(Qt.ArrowCursor)
        self.setAcceptHoverEvents(True)

        self._mouse_hover = False

        self._handles = []

        positions = (Qt.TopLeftCorner, Qt.TopRightCorner, Qt.BottomLeftCorner,
                     Qt.BottomRightCorner)
        self._handles = [self._create_handle(pos) for pos in positions]
        self._layout_handles()
        self._set_z_index()

    def paint(self, painter, option, widget=None):
        """QGraphicsRectItem virtual
        """
        # TODO LH Is there a way to clip to overlapping
        # QAbstractGraphicsItems with a larger zorder

        # TODO LH Get pixmap without tight coupling to scene
        # pixmap = next((i for i in self.scene().items() if type(i)==QtGui.QGraphicsPixmapItem))
        painter.drawPixmap(self.boundingRect(),
                           self.scene().pixmap,
                           self.sceneBoundingRect())

        with PaintState(painter):
            painter.setPen(QtGui.QPen(self.colour, 1, Qt.SolidLine))
            r = self.boundingRect()
            painter.drawRect(r)

            if self.DRAW_INNER:
                painter.setPen(QtGui.QPen(self.inner_colour, 1, Qt.SolidLine))
                r.adjust(1, 1, -1, -1)
                painter.drawRect(r)

    @property
    def colour(self):
        """QtGui.QColor to use for drawing the order
        """
        # TODO LH Transparency on resize better handled by setOpacity()?
        if self.scene().mouseGrabberItem() in chain([self], self._handles):
            return self.RESIZING
        else:
            return self.SELECTED if self.isSelected() else self.UNSELECTED

    @property
    def inner_colour(self):
        """QtGui.QColor to use for drawing the rectangle within the box's border
        """
        if self.scene().mouseGrabberItem() in chain([self], self._handles):
            return self.INNER_RESIZE
        else:
            return self.INNER


    def update(self, rect=QtCore.QRectF()):
        """QGraphicsRectItem function
        """
        # TODO LH QGraphicsRectItem::update is not a virtual function - is it
        # OK to implement this function and call the base class's
        # implementation?
        super(BoxItem, self).update(rect)
        for item in self._handles:
            item.update()

    def hoverEnterEvent(self, event):
        """QGraphicsRectItem virtual
        """
        debug_print('BoxItem.hoverEnterEvent')
        super(BoxItem, self).hoverEnterEvent(event)
        self._mouse_hover = True
        self._set_handles_visible(True)
        self._set_z_index()
        self.update()

    def hoverLeaveEvent(self, event):
        """QGraphicsRectItem virtual
        """
        debug_print('BoxItem.hoverLeaveEvent')
        super(BoxItem, self).hoverLeaveEvent(event)
        self._mouse_hover = False
        self._set_handles_visible(False)
        self._set_z_index()
        self.update()

    def _set_handles_visible(self, visible):
        map(lambda i: i.setVisible(visible), self._handles)

    def _create_handle(self, corner):
        # Creates and returns a new ResizeHandle at the given Qt.Corner
        handle = ResizeHandle(corner, self)
        handle.setVisible(False)
        handle.setFlags(QtGui.QGraphicsItem.ItemStacksBehindParent)
        return handle

    def _layout_handles(self):
        """Moves handles to the appropriate positions
        """
        map(lambda i: i.relayout(self.boundingRect()), self._handles)

    def setRect(self, rect):
        """QGraphicsRectItem function
        """
        debug_print('BoxItem.setRect')
        super(BoxItem, self).setRect(rect)
        self._set_z_index()
        self._layout_handles()

    def mousePressEvent(self, event):
        """QGraphicsRectItem virtual
        """
        debug_print('BoxItem.mousePressEvent')
        super(BoxItem, self).mousePressEvent(event)
        self._set_z_index()
        self.update()

    def mouseReleaseEvent(self, event):
        """QGraphicsRectItem virtual
        """
        debug_print('BoxItem.mouseReleaseEvent')
        super(BoxItem, self).mousePressEvent(event)
        self._set_z_index()
        self.update()

    def itemChange(self, change, value):
        if change == self.ItemSelectedHasChanged:
            # Item has gained or lost selection
            self._set_z_index()
        return super(BoxItem, self).itemChange(change, value)

    def _set_z_index(self):
        """Updates the Z-index of the box

        This sorts the boxes such that the bigger the area of a box, the lower
        it's Z-index is; and boxes that are selected and have mouse or keyboard
        focus are always above other boxes.
        """
        rect = self.rect()
        # Smaller items have a higher z
        z = 1.0
        if rect.width() and rect.height():
            z += + 1.0 / float(rect.width() * rect.height())
            if self.isSelected():
                z += 1.0
            if self._mouse_hover or self.hasFocus():
                z += 1.0
        else:
            # Newly created items have zero width and height
            pass
        self.setZValue(z)
 