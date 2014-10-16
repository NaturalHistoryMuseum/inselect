from PySide import QtCore, QtGui

from inselect.lib.mouse_handler import MouseHandler, MouseState
from inselect.gui.annotator import AnnotateDialog


class BoxResizable(MouseHandler, QtGui.QGraphicsRectItem):
    """Represent a resizable box in the graphics scene

    BoxResizable represents a box that can be added to a graphics scene,
    and is linked to a segment in a segment scene. Note the box is drawn
    _around_ the segment; the edges of the box itself are not part of the
    segment.

    This class handles user input on the box (resize with handles), and listens
    for changes on the segment itself to update or remove itself.

    Notes
    -----
    The coordinates of the rectangles (_segment_rect, _visible_rect,
    _bound_rect) are relative to this object's co-ordinate in the scene, which
    can be changed externally. Use `_map_rect_to_scene` to get the actual
    scene coordinates or the rectangles.

    Parameters
    ----------
    graphics_scene : QtGui.QGraphicsScene
        The graphics scene this box is part of
    segment : Segment
        The segment associated with this box
    parent : object
        The Qt parent widget
    color : QtCore.Qt.*, optional
        The color for the box. Defaults to QtCore.Qt.blue
    transparent : bool, optional
    scene : QGraphicsScene, optional
        The graphics scene this box belongs to
    """
    def __init__(self, graphics_scene, segment,
                 color=QtCore.Qt.blue, transparent=False):
        # Set up members
        self._graphics_scene = graphics_scene
        self._segment = segment
        self._segment_rect = self._segment.get_q_rect_f()
        self._visible_rect = QtCore.QRectF(self._segment_rect)
        self._bounding_rect = None
        self._handles = {
            'top-left': None,
            'top-right': None,
            'bottom-left': None,
            'bottom-right': None
        }
        self._handle_size = 4.0
        self._color = color
        self._transparent = transparent
        self._seeds = []
        self._has_keyboard_focus = False
        # Watch the segment for changes
        self._segment.watch('after-corners-update', self._update_segment)
        # Call constructors
        QtGui.QGraphicsRectItem.__init__(self, self._visible_rect, None,
                                         self._graphics_scene)
        MouseHandler.__init__(self, parent_class=QtGui.QGraphicsRectItem)
        # We store the area that was pressed, and the rectangle at the
        # time the mouse pressed as part of the mouse state.
        self.set_mouse_state('press_area', 'rectangle')
        self.set_mouse_state('press_rect', None)
        # Setup GUI
        self.setFlags(QtGui.QGraphicsItem.ItemIsFocusable)
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable)
        self.setFlag(QtGui.QGraphicsItem.ItemSendsGeometryChanges)
        self._setup_mouse_navigation()
        self._update_graphics()

    def _setup_mouse_navigation(self):
        self.setAcceptsHoverEvents(True)
        self.add_mouse_handler(
            event={
                'event': 'press',
                'button': 'left',
                'modifier': QtCore.Qt.ShiftModifier
            },
            callback=self.add_seed,
            args=[MouseState('x'), MouseState('y')]
        )
        # Box resizing events
        self.add_mouse_handler(
            event={
                'event': 'press',
                'button': 'left',
                'modifier': QtCore.Qt.NoModifier
            },
            callback=self._start_move_resize,
            args=[MouseState('x'), MouseState('y')],
            delegate=True
        )
        self.add_mouse_handler(
            event={
                'event': 'move',
                'button': 'left',
                'modifier': QtCore.Qt.NoModifier
            },
            callback=self._move_resize,
            args=[MouseState('x'), MouseState('y')],
            delegate=True
        )
        self.add_mouse_handler(
            event={
                'event': 'release',
                'button': 'left',
                'modifier': QtCore.Qt.NoModifier
            },
            callback=self._end_move_resize,
            delegate=True
        )
        # Ensure that resize handles are updated when the mouse is active over
        # the element
        self.add_mouse_handler(
            event='enter',
            callback=self._update_graphics,
            args=[MouseState('x'), MouseState('y')],
            delegate=True
        )
        self.add_mouse_handler(
            event='leave',
            callback=self._update_graphics,
            args=[MouseState('x'), MouseState('y')],
            delegate=True
        )
        self.add_mouse_handler(
            event={
                'event': 'move',
                'over': True
            },
            callback=self._update_graphics,
            args=[MouseState('x'), MouseState('y')],
            delegate=True
        )

    def shape(self):
        """Re-implement QGraphicsRectItem.shape to include our boundingBox

        Returns
        -------
        QPainterPath
        """
        path = QtGui.QPainterPath()
        path.addRect(self.boundingRect())
        return path

    def _update_segment(self, segment):
        """Invoked when the segment is changed

        Parameters
        ----------
        segment : Segment
        """
        self._segment = segment
        self._segment_rect = self._segment.get_q_rect_f()
        # Translate this into this item's coordinate system.
        self._segment_rect.translate(-self.pos().x(), -self.pos().y())
        self.prepareGeometryChange()
        self._update_graphics()

    def _update_bounding_box(self):
        """Updates the bounding box (based the visible rect)"""
        graphics_view = self._graphics_scene.views()[0]
        pixel_width = graphics_view.view_pixel_to_scene_width()
        offset = self._handle_size * pixel_width
        self._bounding_rect = self._visible_rect.normalized().adjusted(
            -offset, -offset, offset, offset
        )

    def _update_visible_rect(self):
        """Updates the visible rect (based on the segment rect)"""
        graphics_view = self._graphics_scene.views()[0]
        pixel_width = graphics_view.view_pixel_to_scene_width()
        self._visible_rect = self._segment_rect.adjusted(
            -pixel_width, -pixel_width, pixel_width, pixel_width
        )

    def _update_handles(self):
        """Updates the handle, based on the bounding rect"""
        b = self._bounding_rect
        graphics_view = self._graphics_scene.views()[0]
        pixel_width = graphics_view.view_pixel_to_scene_width()
        offset = self._handle_size * pixel_width
        self._handles['top-left'] = QtCore.QRectF(
            b.topLeft().x(), b.topLeft().y(), 2*offset, 2*offset
        )
        self._handles['top-right'] = QtCore.QRectF(
            b.topRight().x() - 2*offset, b.topRight().y(), 2*offset, 2*offset
        )
        self._handles['bottom-left'] = QtCore.QRectF(
            b.bottomLeft().x(), b.bottomLeft().y() - 2*offset,
            2*offset, 2*offset
        )
        self._handles['bottom-right'] = QtCore.QRectF(
            b.bottomRight().x() - 2*offset, b.bottomRight().y() - 2*offset,
            2*offset, 2*offset
        )

    def _update_cursor(self, x, y):
        """Update the cursor shape."""
        cursor = QtCore.Qt.ArrowCursor
        if (self._handles['top-left'].contains(x, y) or
                self._handles['bottom-right'].contains(x, y)):
            cursor = QtCore.Qt.SizeFDiagCursor
        elif (self._handles['top-right'].contains(x, y) or
              self._handles['bottom-left'].contains(x, y)):
            cursor = QtCore.Qt.SizeBDiagCursor
        self.setCursor(cursor)

    def _update_z_index(self):
        """Update the Z-index of the box

        This sorts the boxes such that the bigger the area of a box, the lower
        it's Z-index is; and boxes that are selected and have mouse or keyboard
        focus are always above other boxes.
        """
        if self.isSelected() and (self.get_mouse_state('over') or
                                  self._has_keyboard_focus):
            self.setZValue(max(
                1E9 + 1000,
                2E9 - self._segment_rect.width() * self._segment_rect.height()
            ))
        else:
            self.setZValue(max(
                1000,
                1E9 - self._segment_rect.width() * self._segment_rect.height()
            ))

    def set_keyboard_focus(self, focus):
        """Un/set the keyboard focus on this box.

        A box with keyboard focus is always on top.
        """
        self._has_keyboard_focus = focus
        self._update_graphics()

    def _update_graphics(self, x=None, y=None):
        """Update all the elements needed for displaying the rectangle and
        handles correctly. This assumes that the segment rectangle is
        correct, and updates the other information based on that.

        Parameters
        ----------
        x, y : int, optional
            Position of the mouse pointer
        """
        self._update_visible_rect()
        self._update_bounding_box()
        self._update_handles()
        if x is not None and y is not None:
            self._update_cursor(x, y)
        self._update_z_index()
        # When called as a mouse handler, propagate the event back to the
        # parent.
        return True

    def add_seed(self, x, y):
        """Add a new see for segmentation

        Parameters
        ----------
        x, y : int
            Screen coordinate of seed
        """
        p = self.mapToScene(x, y).toPoint()
        rect = self._segment_rect
        self._segment.add_seed((p.x() - rect.x() - self.pos().x(),
                                p.y() - rect.y() - self.pos().y()))
        self.prepareGeometryChange()

    def _start_move_resize(self, x, y):
        """Start moving/resizing the box

        Parameters
        ----------
        x, y : int
            Screen coordinates where starting a move/resize operation
        """
        self.set_mouse_state('press_area', 'rectangle')
        self.set_mouse_state('press_rect', QtCore.QRectF(self._segment_rect))
        for area in self._handles:
            if self._handles[area].contains(x, y):
                self.set_mouse_state('press_area', area)
                break
        # Propagate to ensure the box gets selected
        return True

    def _end_move_resize(self):
        """End moving/resizing the box"""
        segment_corners = self._map_rect_to_scene(self._segment_rect)
        self._segment.set_corners(
            (segment_corners.left(), segment_corners.top()),
            (segment_corners.right(), segment_corners.bottom())
        )
        # Propagate to ensure the box gets selected/etc.
        return True

    def _move_resize(self, x, y):
        """Move/resize the box

        Parameters
        ----------
        x, y : int
            Screen coordinates
        """
        press_area = self.get_mouse_state('press_area')
        if press_area == 'rectangle':
            return True  # Propagate - let QRectItem handle this.

        self.prepareGeometryChange()
        delta = QtCore.QPoint(
            x - self.get_mouse_state('pressed_x'),
            y - self.get_mouse_state('pressed_y')
        )
        self._segment_rect = QtCore.QRectF(self.get_mouse_state('press_rect'))
        if press_area == 'top-left':
            self._segment_rect.setTopLeft(
                self._segment_rect.topLeft() + delta
            )
        elif press_area == 'top-right':
            self._segment_rect.setTopRight(
                self._segment_rect.topRight() + delta
            )
        elif press_area == 'bottom-left':
            self._segment_rect.setBottomLeft(
                self._segment_rect.bottomLeft() + delta
            )
        elif press_area == 'bottom-right':
            self._segment_rect.setBottomRight(
                self._segment_rect.bottomRight() + delta
            )
        self._segment_rect = self._segment_rect.normalized()
        return False

    def boundingRect(self):
        """
        Return bounding rectangle
        """
        return self._bounding_rect

    def _map_rect_to_scene(self, map_rect):
        """Change from box coordinate system to view coordinate system.
        Where (0, 0) is the box coordinates at top left corner of the box,
        the position of the box is added to give the view coordinates.
        """
        #TODO: Implement this class separately from QGraphicsRectItem
        #Then we won't need _map_rect_to_scene anymore.
        rect = map_rect
        target_rect = QtCore.QRectF(rect)
        t = rect.topLeft()
        b = rect.bottomRight()
        x1, y1 = t.x() + self.pos().x(), t.y() + self.pos().y()
        x2, y2 = b.x() + self.pos().x(), b.y() + self.pos().y()
        target_rect.setTopLeft(QtCore.QPointF(min(x1, x2), min(y1, y2)))
        target_rect.setBottomRight(QtCore.QPointF(max(x1, x2), max(y1, y2)))
        return target_rect

    def paint(self, painter, option, widget):
        """
        Paint Widget
        """
        # Paint rectangle
        if self.isSelected():
            color = QtCore.Qt.red
            thickness = 3
        else:
            color = self._color
            thickness = 0

        painter.setPen(QtGui.QPen(color, thickness, QtCore.Qt.SolidLine))
        painter.drawRect(self._visible_rect)

        if not self._transparent:
            rect = self._segment_rect
            if rect.width() > 0 and rect.height() > 0:
                target_rect = self._map_rect_to_scene(rect)
                painter.drawPixmap(rect, self._graphics_scene.pixmap(),
                                   target_rect)

        radius = self._graphics_scene.width() / 150
        for seed in self._segment.seeds():
            x, y = seed
            rect = self._segment_rect
            painter.drawEllipse(QtCore.QPointF(x + rect.x(), y + rect.y()),
                                radius, radius)

        painter.setPen(QtGui.QPen(color, 0, QtCore.Qt.SolidLine))
        # If mouse is over, draw handles
        if self.get_mouse_state('over'):
            for area in self._handles:
                painter.drawRect(self._handles[area])