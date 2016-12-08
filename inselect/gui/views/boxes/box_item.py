import sys

from itertools import chain

from qtpy.QtCore import Qt, QRect, QRectF
from qtpy.QtGui import QPen, QBrush
from qtpy.QtWidgets import QGraphicsItem, QGraphicsRectItem

from inselect.lib.utils import debug_print
from inselect.gui.colours import colour_scheme_choice
from inselect.gui.utils import painter_state

from .resize_handle import ResizeHandle
from .reticle import Reticle


class BoxItem(QGraphicsRectItem):
    # Might be some relevant stuff here:
    # http://stackoverflow.com/questions/10590881/events-and-signals-in-qts-qgraphicsitem-how-is-this-supposed-to-work

    # The width of the box (in pixels) drawn around the box.
    # A width of 1 on Mac OS X is too thin. 1.5 on Windows causes artefacts -
    # the top and left edges might appear thicker than the bottom and right
    # edges.
    BOX_WIDTH = 1.5 if 'darwin' == sys.platform else 1

    def __init__(self, x, y, w, h, isvalid, parent=None):
        super(BoxItem, self).__init__(x, y, w, h, parent)
        self.setFlags(QGraphicsItem.ItemIsFocusable |
                      QGraphicsItem.ItemIsSelectable |
                      QGraphicsItem.ItemSendsGeometryChanges |
                      QGraphicsItem.ItemIsMovable)

        self.setCursor(Qt.OpenHandCursor)
        self.setAcceptHoverEvents(True)

        # True if the box has valid metadata
        self._isvalid = isvalid

        # Points of interest as represented by instances of Reticle
        self._pois = []

        # Resize handles
        positions = (Qt.TopLeftCorner, Qt.TopRightCorner, Qt.BottomLeftCorner,
                     Qt.BottomRightCorner)
        self._handles = []
        self._handles = [self._create_handle(pos) for pos in positions]
        self._layout_children()

        self._set_z_index()

    def paint(self, painter, option, widget=None):
        """QGraphicsRectItem virtual
        """
        # TODO LH Is there a way to clip to overlapping
        # QAbstractGraphicsItems with a larger zorder

        # TODO LH Get pixmap without tight coupling to scene
        if not self.has_mouse():
            painter.drawPixmap(self.boundingRect(),
                               self.scene().pixmap,
                               self.sceneBoundingRect())

        with painter_state(painter):
            outline_colour, fill_colour = self.colours

            # Cosmetic pens "...draw strokes that have a constant width
            # regardless of any transformations applied to the QPainter they are
            # used with."
            pen = QPen(outline_colour, self.BOX_WIDTH, Qt.SolidLine)
            pen.setCosmetic(True)
            painter.setPen(pen)

            r = self.boundingRect()
            painter.drawRect(r)

            if fill_colour:
                painter.fillRect(r, fill_colour)

    def has_mouse(self):
        """True if self or self._handles has grabbed the mouse
        """
        return self.scene().mouseGrabberItem() in chain([self], self._handles)

    @property
    def colours(self):
        """Tuple of two QColors to use for the box's border and fill
        respectively. Fill might be None.
        """
        colours = colour_scheme_choice().current['Colours']
        has_mouse = self.has_mouse()
        if has_mouse:
            outline = colours['Resizing']
        elif self.isSelected():
            outline = colours['Selected']
        elif self._isvalid:
            outline = colours['Valid']
        else:
            outline = colours['Invalid']

        if not self._isvalid and not has_mouse:
            fill = colours['InvalidFill']
        else:
            fill = None

        return outline, fill

    def update(self, rect=QRectF()):
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
        self._set_handles_visible(True)
        self._set_z_index()
        self.update()

    def hoverLeaveEvent(self, event):
        """QGraphicsRectItem virtual
        """
        debug_print('BoxItem.hoverLeaveEvent')
        super(BoxItem, self).hoverLeaveEvent(event)
        self._set_handles_visible(False)
        self._set_z_index()
        self.update()

    def _set_handles_visible(self, visible):
        for handle in self._handles:
            handle.setVisible(visible)

    def _create_handle(self, corner):
        # Creates and returns a new ResizeHandle at the given Qt.Corner
        handle = ResizeHandle(corner, self)
        handle.setVisible(False)
        handle.setFlags(QGraphicsItem.ItemStacksBehindParent |
                        QGraphicsItem.ItemIgnoresTransformations)
        return handle

    def _layout_children(self):
        """Moves child graphics items to the appropriate positions
        """
        bounding = self.boundingRect()
        for child in chain(self._handles, self._pois):
            child.layout(bounding)

    def setRect(self, rect):
        """QGraphicsRectItem function
        """
        debug_print('BoxItem.setRect')
        super(BoxItem, self).setRect(rect)
        self._set_z_index()
        self._layout_children()

    def mousePressEvent(self, event):
        """QGraphicsRectItem virtual
        """
        debug_print('BoxItem.mousePressEvent')
        super(BoxItem, self).mousePressEvent(event)
        self._set_z_index()

        if Qt.ShiftModifier == event.modifiers():
            # Add a point of interest
            self.append_point_of_interest(event.pos())
        else:
            # Starting a move
            self.setCursor(Qt.ClosedHandCursor)

        self.update()

    def mouseReleaseEvent(self, event):
        """QGraphicsRectItem virtual
        """
        debug_print('BoxItem.mouseReleaseEvent')
        super(BoxItem, self).mouseReleaseEvent(event)
        self.setCursor(Qt.OpenHandCursor)
        self._set_z_index()
        self.update()

    def itemChange(self, change, value):
        """QGraphicsItem virtual
        """
        if change == self.ItemSelectedHasChanged:
            # Clear points of interest
            scene = self.scene()
            while self._pois:
                scene.removeItem(self._pois.pop())

            # Item has gained or lost selection
            self._set_z_index()
        return super(BoxItem, self).itemChange(change, value)

    def set_rect(self, new_rect):
        """Sets a new QRect in integer coordinates
        """

        # Cumbersome conversion to ints
        current = self.sceneBoundingRect()
        current = QRect(current.left(), current.top(),
                        current.width(), current.height())
        if current != new_rect:
            msg = 'Update rect for [{0}] from [{1}] to [{2}]'
            debug_print(msg.format(self, current, new_rect))
            self.prepareGeometryChange()

            # setrect() expects floating point rect
            self.setRect(QRectF(new_rect))

    def set_isvalid(self, isvalid):
        """Sets a new 'is valid'
        """
        if isvalid != self._isvalid:
            self._isvalid = isvalid
            self.update()

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
        else:
            # Newly created items have zero width and height
            pass
        self.setZValue(z)

    def adjust_rect(self, dx1, dy1, dx2, dy2):
        """Adjusts rect
        """
        r = self.rect()
        r.adjust(dx1, dy1, dx2, dy2)
        if r.width() > 1.0 and r.height() > 1.0:
            self.prepareGeometryChange()
            self.setRect(r)

    def append_point_of_interest(self, pos):
        """Appends pos (a QPoint relative to the top-left of this box) to the
        list of points of interest
        """
        debug_print('New point of interest at [{0}]'.format(pos))
        self._pois.append(Reticle(pos - self.boundingRect().topLeft(), self))
        self._pois[-1].layout(self.boundingRect())
        self._pois[-1].setFlags(QGraphicsItem.ItemIgnoresTransformations)

    @property
    def points_of_interest(self):
        """An iterable of QPointFs in item coordinates
        """
        return [poi.offset for poi in self._pois]
