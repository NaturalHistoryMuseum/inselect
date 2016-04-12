from itertools import chain

from PySide import QtCore
from PySide.QtCore import Qt, QRect, QRectF
from PySide.QtGui import (QBrush, QColor, QFontMetrics, QGraphicsItem,
                          QGraphicsRectItem, QPainter, QPen, QTransform)

from inselect.lib.utils import debug_print
from inselect.gui.colours import colour_scheme_choice
from inselect.gui.utils import painter_state

from .resize_handle import ResizeHandle


def generate_translation_only_transform(original_transform, target_point):
    """To draw the unscaled icons, we desire a transform with scaling factors
    of 1 and shearing factors of 0 and the appropriate translation such that
    our icon center ends up at the same point. According to the
    documentation, QTransform transforms a point in the plane to another
    point using the following formulas:
    x' = m11*x + m21*y + dx
    y' = m22*y + m12*x + dy

    For our new transform, m11 and m22 (scaling) are 1, and m21 and m12
    (shearing) are 0. Since we want x' and y' to be the same, we have the
    following equations:
    m11*x + m21*y + dx = x + dx[new]
    m22*y + m12*x + dy = y + dy[new]

    Thus,
    dx[new] = m11*x - x + m21*y + dx
    dy[new] = m22*y - y + m12*x + dy
    """
    # http://stackoverflow.com/a/11459832

    dx = (original_transform.m11() * target_point.x()
          - target_point.x()
          + original_transform.m21() * target_point.y()
          + original_transform.m31())

    dy = (original_transform.m22() * target_point.y()
          - target_point.y()
          + original_transform.m12() * target_point.x()
          + original_transform.m32())

    return QTransform.fromTranslate(dx, dy)


class BoxItem(QGraphicsRectItem):
    # Might be some relevant stuff here:
    # http://stackoverflow.com/questions/10590881/events-and-signals-in-qts-qgraphicsitem-how-is-this-supposed-to-work

    TRANSPARENT_GREY = QBrush(QColor(0x80, 0x80, 0x80, 0x80))

    def __init__(self, x, y, w, h, parent=None, scene=None):
        super(BoxItem, self).__init__(x, y, w, h, parent, scene)
        self.setFlags(QGraphicsItem.ItemIsFocusable |
                      QGraphicsItem.ItemIsSelectable |
                      QGraphicsItem.ItemSendsGeometryChanges |
                      QGraphicsItem.ItemIsMovable)

        self.setCursor(Qt.OpenHandCursor)
        self.setAcceptHoverEvents(True)

        # Sub-segmentation seed points - QPointF objects in item coordinates
        self._seeds = []

        # Resize handles
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
        if not self.has_mouse():
            painter.drawPixmap(self.boundingRect(),
                               self.scene().pixmap,
                               self.sceneBoundingRect())

        with painter_state(painter):
            # Zero thickness indicates a cosmetic pen, which is drawn with the
            # same thickness regardless of the view's scale factor
            outline_colour, fill_colour = self.colours
            painter.setPen(QPen(outline_colour, 0, Qt.SolidLine))
            bounding = self.boundingRect()
            painter.drawRect(bounding)

            if self._seeds:
                # Draw sub-segmentation seed points
                painter.setBrush(QBrush(Qt.black))
                painter.setPen(QPen(Qt.white, 5, Qt.SolidLine))
                for point in self._seeds:
                    painter.drawEllipse(point, 5, 5)

            if fill_colour:
                painter.fillRect(bounding, fill_colour)

        with painter_state(painter):
            font = painter.font()
            font.setPointSize(14)  # TODO LH Arbitrary font size
            painter.setFont(font)

            # Clip to box
            painter.setClipRect(self.rect())

            # Constant size of text regardless of zoom level
            painter.setTransform(
                generate_translation_only_transform(painter.transform(),
                                                    bounding.topLeft())
            )

            title = self.scene().source.item_display_title(self)

            # Transparent grey rect behind text
            fm = QFontMetrics(font, painter.device())
            width, height = fm.width(title), fm.height()
            text_rect = QRect(bounding.left(), bounding.top(),
                              width, height)
            # Padding around text
            h_padding, v_padding = 4, 1

            painter.fillRect(
                text_rect.adjusted(0, 0, h_padding * 2, v_padding * 2),
                self.TRANSPARENT_GREY
            )

            # The label itself. Need to specify TextDontClip to prevent
            # truncated text on Windows.
            painter.drawText(
                text_rect.adjusted(h_padding, v_padding, h_padding, v_padding),
                Qt.AlignTop | Qt.AlignLeft | Qt.TextDontClip, title
            )

    @property
    def is_valid(self):
        return self.scene().source.item_is_valid(self)

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
        elif self.is_valid:
            outline = colours['Valid']
        else:
            outline = colours['Invalid']

        if not self.is_valid and not has_mouse:
            fill = colours['InvalidFill']
        else:
            fill = None

        return outline, fill

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
        map(lambda i: i.setVisible(visible), self._handles)

    def _create_handle(self, corner):
        # Creates and returns a new ResizeHandle at the given Qt.Corner
        handle = ResizeHandle(corner, self)
        handle.setVisible(False)
        handle.setFlags(QGraphicsItem.ItemStacksBehindParent)
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

        if Qt.ShiftModifier == event.modifiers():
            # Add sub-segmentation seed point
            self.append_subsegmentation_seed_point(event.pos())
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
            # Clear sub-segmentatation seed points
            self._seeds = []

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

    def append_subsegmentation_seed_point(self, pos):
        "Appends pos (a QPoint) to the list of subsegmentation seeds points"
        debug_print('New subsegmentation seed point at [{0}]'.format(pos))
        self._seeds.append(pos)

    @property
    def subsegmentation_seed_points(self):
        """An iterable of sub-segmentatation seed points in item coordinates
        """
        return self._seeds
