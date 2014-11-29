from PySide import QtCore, QtGui

from inselect.lib.segment_scene import SegmentScene
from .graphics_scene import GraphicsScene
from .graphics_view import GraphicsView
from .sidebar import SegmentListWidget

class BoxesPage(QtGui.QSplitter):
    def __init__(self, app_window, parent=None):
        super(BoxesPage, self).__init__(parent)

        self.setSizes([1000, 100])

        self.segment_scene = SegmentScene()
        self.scene = GraphicsScene(self.segment_scene)
        self.view = GraphicsView(self.scene, app_window)
        self.view.setViewportUpdateMode(QtGui.QGraphicsView.FullViewportUpdate)
        self.view.setCursor(QtCore.Qt.CrossCursor)
        self.view.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
        self.view.setRenderHint(QtGui.QPainter.Antialiasing)
        self.view.setUpdatesEnabled(True)
        self.view.setMouseTracking(True)
        self.view.setCacheMode(QtGui.QGraphicsView.CacheBackground)
        self.addWidget(self.view)

        self.sidebar = SegmentListWidget(self.scene, app_window)
        self.addWidget(self.sidebar)
