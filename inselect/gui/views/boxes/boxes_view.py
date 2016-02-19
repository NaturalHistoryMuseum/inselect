from PySide import QtGui
from PySide.QtCore import Qt, QRectF, QSizeF

from inselect.lib.utils import debug_print
from inselect.gui.utils import unite_rects
from inselect.gui.colours import colour_scheme_choice


class BoxesView(QtGui.QGraphicsView):
    """
    """

    MAXIMUM_ZOOM = 3    # User can't zoom in more than 1:3

    def __init__(self, scene, parent=None):
        super(BoxesView, self).__init__(scene, parent)
        self.setCursor(Qt.CrossCursor)
        self.setDragMode(QtGui.QGraphicsView.RubberBandDrag)

        # If True, resizeEvent() will cause the scale to be updated to fit the
        # scene within the view
        self.fit_to_view = True

        # Will contain a temporary Rect object while the user drag-drop-creates
        # a box
        self._pending_box = None

        colour_scheme_choice().colour_scheme_changed.connect(self.colour_scheme_changed)

    def colour_scheme_changed(self):
        """Slot for colour_scheme_changed signal
        """
        self.update()

    def updateSceneRect(self, rect):
        """QGraphicsView slot
        """
        debug_print('BoxesView.updateSceneRect')
        # Reset zoom to fit image
        self.fitInView(self.scene().sceneRect(), Qt.KeepAspectRatio)

    def resizeEvent(self, event):
        """QGraphicsView virtual
        """
        debug_print('BoxesView.resizeEvent')

        # Check for change in size because many user-interface actions trigger
        # resizeEvent(), even though they do not cause a change in the view's
        # size
        if self.fit_to_view and event.oldSize() != event.size():
            self.fitInView(self.scene().sceneRect(), Qt.KeepAspectRatio)

        super(BoxesView, self).resizeEvent(event)

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
                    # Chances are that the user just click the right mouse - do
                    # nothing
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
        """Zoom to show the entire scene
        """
        debug_print('BoxesView.zoom_home')
        self.fitInView(self.scene().sceneRect(), Qt.KeepAspectRatio)
        self.fit_to_view = True

    @property
    def absolute_zoom(self):
        """The current zoom scale
        """
        return self.transform().m11()

    def new_relative_zoom(self, factor):
        """Sets a new relative zoom
        """
        self.new_absolute_zoom(self.absolute_zoom * factor)

    def zoom_to_items(self, items):
        """Centres view on the centre of the items and, if view is set to
        'fit to view', sets the zoom level to encompass items.
        """
        united = unite_rects(i.sceneBoundingRect() for i in items)
        if self.fit_to_view:
            debug_print('Ensuring [{0}] items visible'.format(len(items)))
            self.ensureVisible(united)
        else:
            # Some space
            debug_print('Zooming on [{0}] items'.format(len(items)))
            united.adjust(-20, -20, 40, 40)
            self.fitInView(united, Qt.KeepAspectRatio)

            # TODO LH Need a better solution
            if self.absolute_zoom > self.MAXIMUM_ZOOM:
                self.new_absolute_zoom(self.MAXIMUM_ZOOM)

    def toggle_zoom(self):
        """Toggles between 'fit to screen' and a mild zoom / zoom to selected
        """
        self.fit_to_view = not self.fit_to_view
        if self.fit_to_view:
            self.zoom_home()
        else:
            selected = self.scene().selectedItems()
            if selected:
                self.zoom_to_items(selected)
            else:
                self.new_relative_zoom(4.0)

    def new_absolute_zoom(self, factor):
        """Sets a new absolute zoom
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

            self.setTransform(QtGui.QTransform.fromScale(f, f))
            self.fit_to_view = False

            selected = self.scene().selectedItems()
            if selected:
                # Centre on selected items
                # self.ensureVisible(unite_rects([i.rect() for i in selected]))
                self.centerOn(unite_rects([i.rect() for i in selected]).center())

    def dragEnterEvent(self, event):
        """QWidget virtual
        """
        debug_print('BoxesView.dragEnterEvent')
        # This method overriden to allow file drag-drop. See
        # MainWindow.dragEnterEvent.
