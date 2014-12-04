from enum import Enum

from PySide import QtGui
from PySide.QtCore import Qt

from inselect.lib.utils import debug_print


class ZoomLevels(Enum):
    FitImage = 1
    Zoom1 = 2


class BoxesView(QtGui.QGraphicsView):
    """
    """

    def __init__(self, scene, parent=None):
        super(BoxesView, self).__init__(scene, parent)
        self.zoom = ZoomLevels.FitImage
        self.setCursor(Qt.CrossCursor)
        self.setDragMode(QtGui.QGraphicsView.RubberBandDrag)

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

    def toggle_zoom(self):
        """Sets a new zoom level
        """
        if ZoomLevels.FitImage == self.zoom:
            self.zoom = ZoomLevels.Zoom1

            selected = self.scene().selectedItems()
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
        else:
            self.zoom = ZoomLevels.FitImage
            self.fitInView(self.scene().sceneRect(), Qt.KeepAspectRatio)
