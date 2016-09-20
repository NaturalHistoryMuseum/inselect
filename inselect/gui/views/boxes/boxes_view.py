from PySide import QtGui
from PySide.QtCore import Qt, QRectF, QSizeF, Signal

from inselect.lib.utils import debug_print
from inselect.gui.utils import unite_rects
from inselect.gui.colours import colour_scheme_choice


class BoxesView(QtGui.QGraphicsView):
    """Zoomable image with bounding boxes
    """

    # self.absolute_zoom limited to be <= MAXIMUM_ZOOM
    # 1.8 was chosen through experimentation to fix #331
    MAXIMUM_ZOOM = 1.8

    viewport_changed = Signal(QRectF)

    def __init__(self, scene, parent=None):
        super(BoxesView, self).__init__(scene, parent)
        self.setCursor(Qt.CrossCursor)
        self.setDragMode(QtGui.QGraphicsView.RubberBandDrag)

        # If 'whole_scene', resizeEvent() will cause the scale to be updated to
        # fit the scene within the view.
        # If 'follow_selection', changes in selection cause the view to scale to
        # encompass the current selection.
        # If 'fixed', changes in selection and size do not alter the viewport.
        self.zoom_mode = 'whole_scene'

        # Will contain a temporary Rect object while the user drag-drop-creates
        # a box
        self._pending_box = None

        colour_scheme_choice().colour_scheme_changed.connect(self.colour_scheme_changed)
        self.verticalScrollBar().valueChanged.connect(self.scrolled)
        self.horizontalScrollBar().valueChanged.connect(self.scrolled)

    def colour_scheme_changed(self):
        """Slot for colour_scheme_changed signal
        """
        # viewport's update rather than self's update - http://stackoverflow.com/a/3318205
        self.viewport().update()

    def updateSceneRect(self, rect):
        """QGraphicsView slot
        """
        debug_print('BoxesView.updateSceneRect')
        # Reset zoom to fit image
        self.zoom_home()

    def resizeEvent(self, event):
        """QGraphicsView virtual
        """
        debug_print('BoxesView.resizeEvent')

        # Check for change in size because many user-interface actions trigger
        # resizeEvent(), even though they do not cause a change in the view's
        # size
        if 'whole_scene' == self.zoom_mode and event.oldSize() != event.size():
            self.fitInView(self.scene().sceneRect(), Qt.KeepAspectRatio)

        super(BoxesView, self).resizeEvent(event)

        self.viewport_changed.emit(self.normalised_scene_rect())

    def mousePressEvent(self, event):
        """QGraphicsView virtual
        """
        debug_print('BoxesView.mousePressEvent')

        if Qt.RightButton == event.button() and not self.scene().is_empty:
            # TODO Rubber-band drag uses dashed black line - difficult to see on
            # images with a dark background
            if self._pending_box:
                debug_print('Expected self._pending_box to be empty')
            else:
                debug_print('Starting a new box')
                # The user is creating a new box
                # Create a temporary box (self._pending_box) that is used only
                # to provide feedback as the user drags the mouse
                # TODO LH Escape key cancels new box
                tl = self.mapToScene(event.pos())
                r = self.scene().addRect(QRectF(tl, QSizeF(0, 0)),
                                         Qt.DotLine)
                r.setZValue(3)  # Above all other items
                r.update()
                self._pending_box = r
        else:
            super(BoxesView, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """QGraphicsView virtual
        """
        if self._pending_box:
            debug_print('BoxesView.mouseMoveEvent Updating pending box')
            r = self._pending_box.rect()
            r.setBottomRight(self.mapToScene(event.pos()))
            self._pending_box.setRect(r)
            self._pending_box.update()

        super(BoxesView, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """QGraphicsView virtual
        """
        debug_print('BoxesView.mouseReleaseEvent')

        if Qt.RightButton == event.button() and not self.scene().is_empty:
            if not self._pending_box:
                debug_print('Expected self._pending_box to be set')
            else:
                pending, self._pending_box = self._pending_box, None

                # Grab the rect of the new box and remove the temporary box
                r = pending.rect()
                self.scene().removeItem(pending)

                # Update the current position and normalise
                r.setBottomRight(self.mapToScene(event.pos()))
                r = r.normalized()

                if r.width() > 0 and r.height() > 0:
                    debug_print('BoxesView.mouseReleaseEvent creating a new box')
                    # Add the box
                    self.scene().user_add_box(r)
                else:
                    # Chances are that the user just clicked the right mouse -
                    # do nothing
                    pass
        else:
            super(BoxesView, self).mouseReleaseEvent(event)

    def wheelEvent(self, event):
        """QGraphicsView virtual
        """

        if Qt.ControlModifier == event.modifiers() and not self.scene().is_empty:
            event.accept()
            # Wheel event delta is in units of 1/8 of a degree
            degrees = 8 * event.delta()

            # Compute a relative scale factor
            # Multiplier determined by experimenting with a mac trackpad and a
            # cheap Logitech wheel mouse
            multiplier = 0.0005
            f = 1.0 + degrees * multiplier
            if 0 < f < 2:
                msg = 'BoxesView.wheelEvent delta degrees [{0}] factor [{1}]'
                debug_print(msg.format(degrees, f))
                self.new_relative_zoom(f)
            else:
                pass
                # Extremely large wheel delta
        else:
            super(BoxesView, self).wheelEvent(event)

    def zoom_in(self):
        """A higher zoom level, if possible
        """
        self.new_relative_zoom(1.1)

    def zoom_out(self):
        """A lower zoom level, if possible
        """
        self.new_relative_zoom(0.9)

    def zoom_home(self):
        """Zooms to show the entire scene and sets zoom_mode to 'whole_scene'
        """
        debug_print('BoxesView.zoom_home')
        self.zoom_mode = 'whole_scene'
        self.fitInView(self.scene().sceneRect(), Qt.KeepAspectRatio)

    @property
    def absolute_zoom(self):
        """The current zoom scale
        """
        return self.transform().m11()

    def new_relative_zoom(self, factor):
        """Sets a new relative zoom, sets zoom_mode to 'fixed' and emits
        viewport_changed.
        """
        # Do not override the follow selection
        self.zoom_mode = 'fixed'
        self.new_absolute_zoom(self.absolute_zoom * factor)

    def zoom_to_items(self, items):
        """Centres view on the centre of the items and, if view is set to
        'fit to view', sets the zoom level to encompass items.
        Emits viewport_changed.
        """
        united = unite_rects(i.sceneBoundingRect() for i in items)
        if 'whole_scene' == self.zoom_mode:
            debug_print('Ensuring [{0}] items visible'.format(len(items)))
            self.ensureVisible(united)
            self.viewport_changed.emit(self.normalised_scene_rect())
        else:
            debug_print('Showing [{0}] items'.format(len(items)))
            # Add some padding around the selection
            padding = 20
            if 'follow_selection' == self.zoom_mode:
                # Update zoom
                united.adjust(-padding, -padding, 2 * padding, 2 * padding)
                self.fitInView(united, Qt.KeepAspectRatio)

                if self.absolute_zoom > self.MAXIMUM_ZOOM:
                    # new_absolute_zoom() emits viewport_changed
                    self.new_absolute_zoom(self.MAXIMUM_ZOOM)
                else:
                    self.viewport_changed.emit(self.normalised_scene_rect())
            else:
                # zoom_mode == fixed
                self.ensureVisible(united, xmargin=padding, ymargin=padding)

    def toggle_zoom_to_selection(self):
        """Toggles between 'whole_scene' and a either 'fixed' with a mild zoom
        (if no boxes are selected) or 'follow_selection' (if one or more boxes
        are selected).
        """
        selected = self.scene().selectedItems()
        if selected and 'follow_selection' != self.zoom_mode:
            # Show the selection
            self.zoom_mode = 'follow_selection'
            self.zoom_to_items(selected)
        elif 'whole_scene' != self.zoom_mode:
            # Either no selection and/or currently in 'fixed' or
            # 'follow_selection' - show the whole image
            self.zoom_home()
        else:
            # Apply a mild fixed zoom
            self.zoom_mode = 'fixed'
            self.new_relative_zoom(4.0)

    def new_absolute_zoom(self, factor):
        """Sets a new absolute zoom and emits viewport_changed.
        """
        f = factor
        scene_rect = self.scene().sceneRect()   # Scene
        view_rect = self.viewport().rect()      # Available space
        # The size of the scene if the new transform is applied
        t_scene_rect = QtGui.QTransform.fromScale(f, f).mapRect(scene_rect)

        if (t_scene_rect.width() < view_rect.width() and
                t_scene_rect.height() < view_rect.height()):
            # The user wants to zoom out so that the image is smaller than the
            # view
            self.zoom_home()
        else:
            f = min(self.MAXIMUM_ZOOM, f)
            msg = 'Change absolute zoom from [{0}] to [{1}]'
            debug_print(msg.format(self.absolute_zoom, f))

            selected = self.scene().selectedItems()
            if not selected:
                # No selection so we want to centre on the mouse cursor, if it
                # is within the view. We need to get the mouse position in
                # scene coords before applying the zoom.
                mouse_pos = self.mapFromGlobal(QtGui.QCursor.pos())
                if self.rect().contains(mouse_pos, proper=True):
                    mouse_pos = self.mapToScene(mouse_pos)
                else:
                    mouse_pos = None

            self.setTransform(QtGui.QTransform.fromScale(f, f))

            if selected:
                # Centre on selected items
                self.centerOn(
                    unite_rects(i.sceneBoundingRect() for i in selected).center()
                )
            elif mouse_pos:
                # Centre on mouse position
                self.centerOn(mouse_pos)
            else:
                # Default behaviour is fine
                pass

        self.viewport_changed.emit(self.normalised_scene_rect())

    def scrolled(self):
        """Slot for scroll bars' valueChanged signals
        """
        self.viewport_changed.emit(self.normalised_scene_rect())

    def normalised_scene_rect(self):
        """QRectF with values between 0 and 1 indicating the current viewport
        """
        if self.scene().is_empty:
            return QRectF(0, 0, 1, 1)
        else:
            visible = self.mapToScene(self.viewport().rect()).boundingRect()
            scene_rect = self.scene().sceneRect()
            return QRectF(
                visible.x() / scene_rect.width(),
                visible.y() / scene_rect.height(),
                visible.width() / scene_rect.width(),
                visible.height() / scene_rect.height()
            )

    def dragEnterEvent(self, event):
        """QWidget virtual
        """
        debug_print('BoxesView.dragEnterEvent')
        # This method overriden to allow file drag-drop. See
        # MainWindow.dragEnterEvent.
