import sys

from PySide import QtCore, QtGui

from inselect.gui.utils import get_corners
from inselect.lib.utils import debug_print
from inselect.lib.mouse_handler import MouseHandler, MouseState
from inselect.lib.key_handler import KeyHandler
from .annotator import AnnotateDialog


class GraphicsView(KeyHandler, MouseHandler, QtGui.QGraphicsView):
    """This is the GraphicsView that is used to display the main Graphics
    Scene.

    The GraphicsView handles the view port (zooming, etc.) as well as user
    interactions. Modification of the segments themselves is done via
    the SegmentScene, while the handling of selected segments is done via
    the GraphicsScene

    Parameters
    -----------
    graphics_scene : QtGui.GraphicsScene
        The Qt object that holds all the graphics element (image and boxes)
    parent : object
        the parent widget
    """
    def __init__(self, graphics_scene, parent=None):
        # Call constructors
        QtGui.QGraphicsView.__init__(self, parent)
        MouseHandler.__init__(self, parent_class=QtGui.QGraphicsView)
        KeyHandler.__init__(self, parent_class=QtGui.QGraphicsView)
        # Initialize members
        self._parent = parent
        self._graphics_scene = graphics_scene
        self._segment_scene = self._graphics_scene.segment_scene()
        # UI setup
        self.scrollBarValuesOnMousePress = QtCore.QPoint()
        self.setDragMode(QtGui.QGraphicsView.RubberBandDrag)
        # Setup navigation
        self._setup_mouse_navigation()
        self._setup_key_navigation()
        # Register the scene
        self.setScene(self._graphics_scene)

    def _setup_key_navigation(self):
        """Setups the key handlers for this view"""
        self.add_key_handler(QtCore.Qt.Key_Delete, self.delete_selected)
        if 'darwin'==sys.platform:
            # CMD+backspace is the OS X standard for 'delete objects'. Not all
            # Mac keyboards have a delete key.
            self.add_key_handler((QtCore.Qt.ControlModifier, QtCore.Qt.Key_Backspace),
                                 self.delete_selected)
        self.add_key_handler(QtCore.Qt.Key_Return, self.annotate_segments)
        self.add_key_handler(QtCore.Qt.Key_Z, self.zoom_to_selection)
        self.add_key_handler(QtCore.Qt.Key_Up, self.move_segments, [(0, -1)])
        self.add_key_handler(QtCore.Qt.Key_Right, self.move_segments, [(1, 0)])
        self.add_key_handler(QtCore.Qt.Key_Down, self.move_segments, [(0, 1)])
        self.add_key_handler(QtCore.Qt.Key_Left, self.move_segments, [(-1, 0)])
        self.add_key_handler(
            key=(QtCore.Qt.ControlModifier, QtCore.Qt.Key_Up),
            callback=self.move_segments,
            args=[(0, -1), (0, 0)]
        )
        self.add_key_handler(
            key=(QtCore.Qt.ControlModifier, QtCore.Qt.Key_Right),
            callback=self.move_segments,
            args=[(1, 0), (0, 0)]
        )
        self.add_key_handler(
            key=(QtCore.Qt.ControlModifier, QtCore.Qt.Key_Down),
            callback=self.move_segments,
            args=[(0, 1), (0, 0)]
        )
        self.add_key_handler(
            key=(QtCore.Qt.ControlModifier, QtCore.Qt.Key_Left),
            callback=self.move_segments,
            args=[(-1, 0), (0, 0)]
        )
        self.add_key_handler(
            key=(QtCore.Qt.ShiftModifier, QtCore.Qt.Key_Up),
            callback=self.move_segments,
            args=[(0, 0), (0, -1)]
        )
        self.add_key_handler(
            key=(QtCore.Qt.ShiftModifier, QtCore.Qt.Key_Right),
            callback=self.move_segments,
            args=[(0, 0), (1, 0)]
        )
        self.add_key_handler(
            key=(QtCore.Qt.ShiftModifier, QtCore.Qt.Key_Down),
            callback=self.move_segments,
            args=[(0, 0), (0, 1)]
        )
        self.add_key_handler(
            key=(QtCore.Qt.ShiftModifier, QtCore.Qt.Key_Left),
            callback=self.move_segments,
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
            callback=self.annotate_segments
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
        self._graphics_scene.remove_keyboard_focus()
        # Return True to delegate when this is invoked as a mouse handler
        return True

    def zoom_to_selection(self):
        """Zoom the view to the current selection"""
        box = self._graphics_scene.get_selection_box()
        if box is not None:
            x, y, width, height = box
            self.fitInView(x, y, width, height, QtCore.Qt.KeepAspectRatio)

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

    def move_segments(self, top_left_delta, bottom_right_delta=None):
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
        for segment in self._graphics_scene.selected_segments():
            segment.move_corners(top_left_delta, bottom_right_delta)
            #TODO: we always assume this is triggered by keyboard.
            self._graphics_scene.set_keyboard_focus(segment, True)

    def annotate_segments(self):
        """Open the annotation dialog for the currently selected segments"""
        segments = self._graphics_scene.selected_segments()
        if segments:
            dialog = AnnotateDialog(self._graphics_scene, segments,
                                    parent=self._parent)
            dialog.exec_()

    def delete_items(self, delete):
        self._remove_keyboard_focus()
        for segment in delete:
            self._segment_scene.remove(segment)

    def delete_all_boxes(self):
        all_boxes = self._graphics_scene.boxes()
        self.delete_items(self._graphics_scene.segments_of_boxes(all_boxes))

    def delete_selected(self):
        """Delete the currently selected segments"""
        self.delete_items(self._graphics_scene.selected_segments())

    def select_none(self):
        """Clear selection"""
        self._graphics_scene.remove_keyboard_focus()
        self._graphics_scene.deselect_all_boxes()

    def select_all(self):
        """Select all items in the scene"""
        self._graphics_scene.remove_keyboard_focus()
        self._graphics_scene.select_all_boxes()

    def select_next(self):
        """Select the next object in the scene"""
        self._graphics_scene.remove_keyboard_focus()
        selected = self._graphics_scene.selected_segments()
        segment = None
        if len(selected) > 0:
            segment = selected[0]
        next_segment = self._segment_scene.get_next_segment(segment)
        if next_segment:
            self._graphics_scene.select_segment(next_segment)
            #TODO: we always assume this is triggered by keyboard.
            self._graphics_scene.set_keyboard_focus(next_segment, True)
            self.ensure_selection_visible()

    def select_previous(self):
        """Select the previous object in the scene"""
        self._remove_keyboard_focus()
        selected = self._graphics_scene.selected_segments()
        segment = None
        if len(selected) > 0:
            segment = selected[0]
        previous_segment = self._segment_scene.get_previous_segment(segment)
        if previous_segment:
            self._graphics_scene.select_segment(previous_segment)
            #TODO: we always assume this is triggered by keyboard.
            self._graphics_scene.set_keyboard_focus(previous_segment, True)
            self.ensure_selection_visible()

    def ensure_selection_visible(self):
        """Ensure the selected boxes are visible

        Notes
        -----
        Doing on this on a mouse-triggered selection change event might cause
        the box to move.
        """
        box = self._graphics_scene.get_selection_box()
        if box is not None:
            x, y, width, height = box
            self.ensureVisible(x, y, width, height)

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
