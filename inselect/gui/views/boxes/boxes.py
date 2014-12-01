from itertools import izip
from enum import Enum

from PySide import QtCore, QtGui
from PySide.QtCore import Qt

from bidict import bidict

from inselect.lib.utils import debug_print
from inselect.gui.roles import ImageRole, RectRole
from inselect.gui.utils import unite_rects

from PySide import QtCore, QtGui


class GraphicsHookView(QtGui.QAbstractItemView):
    """Qt have used 'view' in two different contexts: the model-view
    architecture and the graphics/view framework, henceforth MV and GV
    respectively.

    This class is a MV view that acts as an interface between MV and GV.
    A limited number of events are passed between the two systems:
    * changes in selection
    * changes in boxes' position and size (RectRole)
    * addition of boxes (TODO)
    * deletion of boxes (TODO)
    """

    # Based on idea in:
    # http://stackoverflow.com/questions/3188584/how-to-use-qt-model-view-framework-with-the-graphics-view-framework

    def __init__(self, parent=None):
        super(GraphicsHookView, self).__init__(parent)
        self.scene = Scene(self, parent)
        self._mapping = bidict()

        self.handling_selection_update = False
        self.scene.selectionChanged.connect(self.scene_selection_changed)

    def reset(self):
        """QAbstractItemView virtual
        """
        debug_print('GraphicsHookView.reset')
        super(GraphicsHookView, self).reset()

        model = self.model()
        self.scene.new_document(model.index(0, 0).data(ImageRole))

        # Build up new mapping
        m = bidict()
        for row in xrange(0, model.rowCount()):
            index = model.index(row, 0)
            rect = index.data(RectRole)
            item = self.scene.add_box(rect)
            m[index] = item

        self._mapping = m

    def setModel(self, model):
        """QAbstractItemView virtual
        """
        debug_print('GraphicsHookView.setModel', model, model.rowCount(),
              model.columnCount())
        super(GraphicsHookView, self).setModel(model)

    def setCurrentIndex(self, index):
        """QAbstractItemView slot
        """
        debug_print('GraphicsHookView.setCurrentIndex', index)

    def update(self, index):
        """QAbstractItemView slot
        """
        debug_print('GraphicsHookView.update', index)

    def selectionChanged(self, selected, deselected):
        """QAbstractItemView virtual
        """
        # Tell the scene about the new selection
        if not self.handling_selection_update:
            # TODO Context for this
            debug_print('GraphicsHookView.selectionChanged')
            self.handling_selection_update = True
            try:
                # Tell the selected items
                selected_items = [self._mapping[i] for i in selected.indexes()]
                for item in selected_items:
                    item.setSelected(True)
                    item.update()

                # Tell the deselected items
                for item in [self._mapping[i] for i in deselected.indexes()]:
                    item.setSelected(False)
                    item.update()

                if selected_items:
                    # Ensure that the selected items are visible
                    rect = unite_rects([i.rect() for i in selected_items])
                    debug_print('GraphicsHookView will make visible', rect)
                    selected_items[0].ensureVisible(rect)

                msg = ('GraphicsHookView selectionChanged: [{0}] items added, '
                       '[{1}] items removed')
                debug_print(msg.format(len(selected.indexes()), len(deselected.indexes())))
            finally:
                self.handling_selection_update = False

    def currentChanged(self, current, previous):
        """QAbstractItemView virtual
        """
        debug_print('GraphicsHookView.currentChanged')

    def dataChanged(self, topLeft, bottomRight):
        """QAbstractItemView virtual
        """
        debug_print('GraphicsHookView.dataChanged')

    def scene_selection_changed(self):
        """scene.selectionChanged slot
        """
        if not self.handling_selection_update:
            debug_print('GraphicsHookView.scene_selection_changed')
            # TODO Context for this
            self.handling_selection_update = True
            try:
                selected = self.scene.selectedItems()
                s = self.selectionModel()

                # TODO LH Clear then add is clunky
                s.clear()
                for index in [self._mapping[:i] for i in selected]:
                    s.select(index, QtGui.QItemSelectionModel.Select)

                if selected:
                    s.setCurrentIndex(self._mapping[:selected[0]], s.Current)
            finally:
                self.handling_selection_update = False


    def item_rects_updated(self, items):
        """Function called by Scene
        """
        debug_print('GraphicsHookView.item_rects_updated')
        for index,item in izip([self._mapping[:i] for i in items], items):
            # item.sceneBoundingRect() is the items rects in the correct
            # coordinates system
            rect = item.sceneBoundingRect()
            # Cumbersome conversion to ints
            rect = QtCore.QRect(rect.left(), rect.top(), rect.width(), rect.height())
            self.model().setData(index, rect, RectRole)


class Scene(QtGui.QGraphicsScene):
    def __init__(self, source, parent=None):
        super(Scene, self).__init__(parent)
        self.source = source

        # A mapping from QGraphicsItem to QtCore.QRectF of selected items,
        # populated on mouseReleaseEvent()
        self._mouse_press_selection = {}

    def new_document(self, image):
        self.clear()  # Removes all items

        if image:
            debug_print('New scene [{0}] [{1}]'.format(image.width(), image.height()))
            self.setSceneRect(0, 0, image.width(), image.height())
            self.addItem(QtGui.QGraphicsPixmapItem(image))
            for v in self.views():
                v.updateSceneRect(self.sceneRect())
        else:
            debug_print('New empty scene')
            self.setSceneRect(0, 0, 0, 0)

    def add_box(self, rect):
        # Notification from source that a box has been added
        item = BoxItem(rect.left(), rect.top(), rect.width(), rect.height())
        self.addItem(item)
        return item

    def mousePressEvent(self, event):
        # QGraphicsRectItem virtual
        debug_print('Scene.mousePressEvent')
        super(Scene, self).mousePressEvent(event)

        if self._mouse_press_selection:
            debug_print('Unexpected _mouse_press_selection')
            self._mouse_press_selection = {}

        # Record the scene bounding rect of each selected items
        selected = self.selectedItems()
        self._mouse_press_selection = {i: i.sceneBoundingRect() for i in selected}

    def mouseReleaseEvent(self, event):
        # QGraphicsRectItem virtual
        debug_print('Scene.mouseReleaseEvent')
        super(Scene, self).mouseReleaseEvent(event)

        # Work out which items have had their scene bounding rects altered
        # in between mousePressEvent() and mouseReleaseEvent()
        original, self._mouse_press_selection = self._mouse_press_selection, {}

        selected = self.selectedItems()
        current = {i: i.sceneBoundingRect() for i in selected}

        # List of items with a scene bounding rects different from that when
        # mousePressEvent() ocurred
        changed = [i for i in current if current[i]!=original.get(i, current[i])]
        if changed:
            # This assumes that the order of items in self.selectedItems() has
            # not changed and that is one item's rect has altered then they all
            # have.
            self.source.item_rects_updated(selected)


class ZoomLevels(Enum):
    FitImage = 1
    Zoom1 = 2


class BoxesView(QtGui.QGraphicsView):
    def __init__(self, scene, parent=None):
        super(BoxesView, self).__init__(scene, parent)
        self.zoom = ZoomLevels.FitImage
        self.setCursor(Qt.CrossCursor)

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
        if event.oldSize() != event.size() and ZoomLevels.FitImage == self.zoom:
            self.fitInView(self.scene().sceneRect(), Qt.KeepAspectRatio)
        super(BoxesView, self).resizeEvent(event)

    def keyPressEvent(self, event):
        """QGraphicsView virtual
        """
        if QtCore.Qt.Key_Z==event.key():
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


class BoxItem(QtGui.QGraphicsRectItem):
    # Might be some relevant stuff here:
    # http://stackoverflow.com/questions/10590881/events-and-signals-in-qts-qgraphicsitem-how-is-this-supposed-to-work
    def __init__(self, x, y, w, h, parent=None, scene=None):
        super(BoxItem, self).__init__(x, y, w, h, parent, scene)
        self.setFlags(QtGui.QGraphicsItem.ItemIsFocusable |
                      QtGui.QGraphicsItem.ItemIsSelectable |
                      QtGui.QGraphicsItem.ItemSendsGeometryChanges |
                      QtGui.QGraphicsItem.ItemIsMovable)
        self.setCursor(Qt.ArrowCursor)

    def paint(self, painter, option, widget=None):
        """QGraphicsRectItem virtual
        """
        colour = QtCore.Qt.red if self.isSelected() else QtCore.Qt.blue
        thickness = 3 if self.isSelected() else 1
        painter.setPen(QtGui.QPen(colour, thickness, QtCore.Qt.SolidLine))
        painter.drawRect(self.rect())
