from enum import Enum

from PySide import QtGui
from PySide.QtCore import Qt, QRectF, QSizeF

from inselect.lib.utils import debug_print
from inselect.gui.utils import unite_rects


class ZoomLevels(Enum):
    FitImage = 1
    Zoom1 = 2
    FitSelection = 3


class BoxesView(QtGui.QGraphicsView):
    """
    """

    def __init__(self, scene, parent=None):
        super(BoxesView, self).__init__(scene, parent)
        self.zoom = ZoomLevels.FitImage
        self.setCursor(Qt.CrossCursor)
        self.setDragMode(QtGui.QGraphicsView.RubberBandDrag)

        # Will contain a temporary Rect object while the user drag-drop-creates
        # a box
        self._pending_box = None

    def updateSceneRect(self, rect):
        """QGraphicsView slot
        """
        debug_print('BoxesView.updateSceneRect')
        if ZoomLevels.FitImage == self.zoom:
            self.fitInView(self.scene().sceneRect(), Qt.KeepAspectRatio)

    def resizeEvent(self, event):
        """QGraphicsView virtual
        """
        debug_print('BoxesView.resizeEvent')

        # Check for change in size because many user-interface actions trigger
        # resizeEvent(), even though they do not cause a change in the view's
        # size
        if event.oldSize() != event.size() and ZoomLevels.FitImage == self.zoom:
            self.fitInView(self.scene().sceneRect(), Qt.KeepAspectRatio)
        super(BoxesView, self).resizeEvent(event)

    def keyPressEvent(self, event):
        """QGraphicsView virtual
        """
        if event.key() == Qt.Key_Z:
            event.accept()
            self.toggle_zoom()
        else:
            super(BoxesView, self).keyPressEvent(event)

    def mousePressEvent(self, event):
        """QGraphicsView virtual
        """
        debug_print('BoxesView.mousePressEvent')
        if Qt.RightButton == event.button():
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
            debug_print('Updating pending box')
            r = self._pending_box.rect()
            r.setBottomRight(self.mapToScene(event.pos()))
            self._pending_box.setRect(r)
            self._pending_box.update()

        super(BoxesView, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """QGraphicsView virtual
        """
        debug_print('BoxesView.mouseReleaseEvent')

        if Qt.RightButton == event.button():
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

                if r.width()>0 and r.height()>0:
                    debug_print('Creating a new box')
                    # Add the box
                    self.scene().user_add_box(r)
                else:
                    # Chances are that the user just click the right mouse - do
                    # nothing
                    pass
        else:
            super(BoxesView, self).mouseReleaseEvent(event)

    def toggle_zoom(self):
        """Sets a new zoom level
        """
        selected = self.scene().selectedItems()

        if ZoomLevels.FitImage == self.zoom:
            self.zoom = ZoomLevels.Zoom1
            if selected:
                # Centre on selected items
                self.scale(4, 4)
                self.ensureVisible(unite_rects([i.rect() for i in selected]))
            else:
                # Centre on mouse cursor, if mouse is within the scene
                p = self.mapToScene(self.mapFromGlobal(QtGui.QCursor.pos()))
                self.scale(4, 4)
                if self.scene().sceneRect().contains(p):
                    self.centerOn(p)
        elif ZoomLevels.Zoom1 == self.zoom and selected:
            self.zoom = ZoomLevels.FitSelection

            # Centre on selected item(s)
            r = unite_rects([i.rect() for i in selected])

            # Some space
            r.adjust(-20, -20, 40, 40)
            self.fitInView(r, Qt.KeepAspectRatio)
        else:
            # FitSelection
            self.zoom = ZoomLevels.FitImage
            self.fitInView(self.scene().sceneRect(), Qt.KeepAspectRatio)
