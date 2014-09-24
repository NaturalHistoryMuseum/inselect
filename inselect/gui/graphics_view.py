from PySide import QtCore, QtGui

from inselect.lib import utils
from inselect.lib.mouse_handler import MouseHandler, MouseState
from inselect.lib.key_handler import KeyHandler
from inselect.gui.annotator import AnnotateDialog


class GraphicsView(KeyHandler, MouseHandler, QtGui.QGraphicsView):
    """This is the GraphicsView that is used to display the main Graphics
    Scene.

    The data about the segments is held in the SegmentScene, while the
    graphical data (the image and the boxes) are held in the GraphicsScene.
    The GraphicsView is a view on the scene, and handles the user interaction.

    Parameters
    -----------
    graphics_scene : QtGui.GraphicsScene
        The Qt object that holds all the graphics element (image and boxes)
    segment_scene : SegmentScene
        The SegmentScene object which holds the segments for this scene
    parent : object
        the parent widget
    """
    def __init__(self, graphics_scene, segment_scene, parent=None):
        # Call constructors
        QtGui.QGraphicsView.__init__(self, parent)
        MouseHandler.__init__(self, parent_class=QtGui.QGraphicsView)
        KeyHandler.__init__(self, parent_class=QtGui.QGraphicsView)
        # Initialize members
        self._parent = parent
        self._segment_scene = segment_scene
        self._boxes_with_keyboard_focus = []
        # UI setup
        self.scrollBarValuesOnMousePress = QtCore.QPoint()
        self.setDragMode(QtGui.QGraphicsView.RubberBandDrag)
        # Setup navigation
        self._setup_mouse_navigation()
        self._setup_key_navigation()
        # Register the scene
        self.setScene(graphics_scene)

    def _setup_key_navigation(self):
        """Setups the key handlers for this view"""
        self.add_key_handler(QtCore.Qt.Key_Delete, self.delete_boxes)
        self.add_key_handler(QtCore.Qt.Key_Return, self.annotate_boxes)
        self.add_key_handler(QtCore.Qt.Key_Z, self.zoom_to_selection)
        self.add_key_handler(QtCore.Qt.Key_Up, self.move_boxes, [(0, -1)])
        self.add_key_handler(QtCore.Qt.Key_Right, self.move_boxes, [(1, 0)])
        self.add_key_handler(QtCore.Qt.Key_Down, self.move_boxes, [(0, 1)])
        self.add_key_handler(QtCore.Qt.Key_Left, self.move_boxes, [(-1, 0)])
        self.add_key_handler(
            key=(QtCore.Qt.ControlModifier, QtCore.Qt.Key_Up),
            callback=self.move_boxes,
            args=[(0, -1), (0, 0)]
        )
        self.add_key_handler(
            key=(QtCore.Qt.ControlModifier, QtCore.Qt.Key_Right),
            callback=self.move_boxes,
            args=[(1, 0), (0, 0)]
        )
        self.add_key_handler(
            key=(QtCore.Qt.ControlModifier, QtCore.Qt.Key_Down),
            callback=self.move_boxes,
            args=[(0, 1), (0, 0)]
        )
        self.add_key_handler(
            key=(QtCore.Qt.ControlModifier, QtCore.Qt.Key_Left),
            callback=self.move_boxes,
            args=[(-1, 0), (0, 0)]
        )
        self.add_key_handler(
            key=(QtCore.Qt.ShiftModifier, QtCore.Qt.Key_Up),
            callback=self.move_boxes,
            args=[(0, 0), (0, -1)]
        )
        self.add_key_handler(
            key=(QtCore.Qt.ShiftModifier, QtCore.Qt.Key_Right),
            callback=self.move_boxes,
            args=[(0, 0), (1, 0)]
        )
        self.add_key_handler(
            key=(QtCore.Qt.ShiftModifier, QtCore.Qt.Key_Down),
            callback=self.move_boxes,
            args=[(0, 0), (0, 1)]
        )
        self.add_key_handler(
            key=(QtCore.Qt.ShiftModifier, QtCore.Qt.Key_Left),
            callback=self.move_boxes,
            args=[(0, 0), (-1, 0)]
        )
        self.add_key_handler(QtCore.Qt.Key_N, self.select_next)
        self.add_key_handler(QtCore.Qt.Key_P, self.select_previous)

    def _setup_mouse_navigation(self):
        """Setup the mouse handlers for this view"""
        self.add_mouse_handler(
            event='move',
            callback=self._remove_keyboard_focus,
            delegate=True
        )
        self.add_mouse_handler(
            event='double-click',
            callback=self.annotate_boxes
        )
        self.add_mouse_handler(
            event={
                'event': 'move',
                'button': 'middle'
            },
            callback=self.scroll_view,
            args=[MouseState('delta_x'), MouseState('delta_y')]
        )
        self.add_mouse_handler(
            event={
                'event': 'press',
                'button': 'right'
            },
            callback=self._start_new_box,
            args=[MouseState('x'), MouseState('y')]
        )
        self.add_mouse_handler(
            event={
                'event': 'move',
                'button': 'right'
            },
            callback=self._update_new_box,
            args=[MouseState('x'), MouseState('y')]
        )
        self.add_mouse_handler(
            event={
                'event': 'release',
                'button': 'right'
            },
            callback=self._finish_new_box,
            args=[MouseState('x'), MouseState('y')]
        )
        self.add_mouse_handler(
            event={
                'event': 'wheel',
                'button': None,
                'modifier': QtCore.Qt.ControlModifier
            },
            callback=self.zoom,
            args=[MouseState('wheel_delta')]
        )

    def _remove_keyboard_focus(self):
        """Remove the keyboard focus from all the boxes that have it"""
        for box in self._boxes_with_keyboard_focus:
            box.set_keyboard_focus(False)
        self._boxes_with_keyboard_focus = []
        # Return True to delegate when this is invoked as a mouse handler
        return True

    def zoom_to_selection(self):
        """Zoom the view to the current selection"""
        box = self._get_selection_box()
        if box is not None:
            self.fitInView(box[0][0], box[0][1], box[1][0] - box[0][0],
                           box[1][1] - box[0][1], QtCore.Qt.KeepAspectRatio)

    def zoom(self, delta, factor=0.2):
        """Zoom the view in or out.

        Notes
        -----
        Only the sign of the delta is important. This sets the scale to 1 +
        sign(delta) * factor

        Parameters
        ----------
        delta : int
            Positive to zoom in, negative to zoom out
        factor : float
            The factor - should be between 0 and 1 (Exclusive)
        """
        scale_value = 1 + cmp(delta, 0) * factor
        self.scale(scale_value, scale_value)

    def move_boxes(self, top_left_delta, bottom_right_delta=None):
        """Move the currently selected segments

        If only the top left delta is specified, then both the top left and
        bottom right corners are moved equally (so the entire box is moved).
        If two values are specified, then the top left and bottom right corners
        are moved independently.

        Parameters
        ----------
        top_left_delta : tuple
            (x_delta, y_delta)
        bottom_right_delta : tuple, optional
            (x_delta, y_delta)
        """
        selected_boxes = self.scene().selectedItems()
        self._remove_keyboard_focus()
        for box in selected_boxes:
            segment = self._segment_scene.get_associated_segment(box)
            self._segment_scene.move_segment_corners(
                segment, top_left_delta, bottom_right_delta
            )
            box.set_keyboard_focus(True)
            self._boxes_with_keyboard_focus.append(box)

    def annotate_boxes(self):
        """Open the annotation dialog for the currently selected segments"""
        segments = []
        for box in self.scene().selectedItems():
            segment = self._segment_scene.get_associated_segment(box)
            segments.append(segment)
        dialog = AnnotateDialog(self._segment_scene, segments,
                                parent=self._parent)
        dialog.exec_()

    def delete_boxes(self):
        """Delete the currently selected segments"""
        selected_boxes = self.scene().selectedItems()
        self._remove_keyboard_focus()
        for box in selected_boxes:
            segment = self._segment_scene.get_associated_segment(box)
            self._segment_scene.remove(segment)

    def deselect_all(self):
        """Deselect all items in the scene"""
        self._remove_keyboard_focus()
        for box in self.scene().selectedItems():
            box.setSelected(False)

    def select_all(self):
        """Select all items in the scene"""
        self._remove_keyboard_focus()
        for box in self.scene().items():
            box.setSelected(True)

    def select_next(self):
        """Select the next object in the scene"""
        self._remove_keyboard_focus()
        selected = self.scene().selectedItems()
        segment = None
        if len(selected) > 0:
            segment = self._segment_scene.get_associated_segment(selected[0])
        next_segment = self._segment_scene.get_next_segment(segment)
        if next_segment:
            self.deselect_all()
            next_box = self._segment_scene.get_associated_object(
                'boxResizable', next_segment
            )
            next_box.setSelected(True)
            next_box.set_keyboard_focus(True)
            self._boxes_with_keyboard_focus.append(next_box)
            self.ensure_selection_visible()

    def select_previous(self):
        """Select the previous object in the scene"""
        self._remove_keyboard_focus()
        selected = self.scene().selectedItems()
        segment = None
        if len(selected) > 0:
            segment = self._segment_scene.get_associated_segment(selected[0])
        previous_segment = self._segment_scene.get_previous_segment(segment)
        if previous_segment:
            self.deselect_all()
            previous_box = self._segment_scene.get_associated_object(
                'boxResizable', previous_segment
            )
            previous_box.setSelected(True)
            previous_box.set_keyboard_focus(True)
            self._boxes_with_keyboard_focus.append(previous_box)
            self.ensure_selection_visible()

    def ensure_selection_visible(self):
        """Ensure the selected boxes are visible

        Notes
        -----
        Doing on this on a mouse-triggered selection change event might cause
        the box to move.
        """
        box = self._get_selection_box()
        if box is not None:
            self.ensureVisible(box[0][0], box[0][1], box[1][0] - box[0][0],
                               box[1][1] - box[0][1])

    def _get_selection_box(self):
        """Return the bounding box of selected items

        Returns
        --------
        tuple : (top_left, bottom_right) where each tuple is formed of (x,y) or
            None if there is no selection
        """
        tl = None
        br = None
        for item in self.scene().selectedItems():
            box = item.boundingRect()
            if tl is None:
                tl = (box.left(), box.top())
                br = (box.right(), box.bottom())
            else:
                tl = (min(tl[0], box.left()), min(tl[1], box.top()))
                br = (max(br[0], box.right()), max(br[1], box.bottom()))
        if tl is None:
            return None
        return tl, br

    def _start_new_box(self, x, y):
        """Start drawing a new box

        Parameters
        ----------
        x : int
            Screen X coordinate of first corner
        y : int
            Screen Y coordinate of first corner
        """
        s = self.mapToScene(x, y).toPoint()
        r = self.scene().addRect(s.x(), s.y(), 0, 0, QtCore.Qt.DotLine)
        r.setZValue(1E9)
        self._new_box = (s.x(), s.y(), r)

    def _update_new_box(self, x, y):
        """Update the size of the newly created box

        Parameters
        ----------
        x : int
            Screen X coordinate of other corner
        y : int
            Screen Y coordinate of other corner
        """
        u = self.mapToScene(x, y).toPoint()
        x1, y1 = min(self._new_box[0], u.x()), min(self._new_box[1], u.y())
        x2, y2 = max(self._new_box[0], u.x()), max(self._new_box[1], u.y())
        w = x2 - x1
        h = y2 - y1
        self._new_box[2].setRect(x1, y1, w, h)
        self.scene().update()

    def _finish_new_box(self, x, y):
        """Finish drawing a box and add it to the list of objects

        Parameters
        ----------
        x : int
            Screen X coordinate of other corner
        y : int
            Screen Y coordinate of other corner
        """
        u = self.mapToScene(x, y).toPoint()
        ((x1, y1), (x2, y2)) = utils.get_corners(self._new_box[0],
                                                 self._new_box[1],
                                                 u.x(),
                                                 u.y())
        x1 = max(0, x1)
        y1 = max(0, y1)
        x2 = min(x2, self.scene().width())
        y2 = min(y2, self.scene().height())

        w = x2 - x1
        h = y2 - y1

        if w > 5 and h > 5:
            self._segment_scene.add((x1, y1), (x2, y2))

        # Remove the creation box
        self.scene().removeItem(self._new_box[2])
        self._new_box = None

    def scroll_view(self, delta_x, delta_y):
        """ Scroll the view

        Parameters
        ----------
        delta_x : int
        delta_y : int
        """
        h = self.horizontalScrollBar()
        v = self.verticalScrollBar()
        h.setValue(h.value() + delta_x)
        v.setValue(v.value() + delta_y)

    def view_pixel_to_scene_width(self):
        """Return the scene width of a view pixel.

        This allows us to draw elements that are always n pixels apart in the
        view regardless of the scale.

        Returns
        -------
        float
        """
        return (self.mapToScene(1, 0) - self.mapToScene(0, 1)).x()
