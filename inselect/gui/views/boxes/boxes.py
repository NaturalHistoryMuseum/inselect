from functools import partial
from itertools import izip
from enum import Enum

from PySide import QtCore, QtGui
from PySide.QtCore import Qt, QRect, QRectF, QPointF, QSizeF

from inselect.lib.utils import debug_print
from inselect.gui.roles import PixmapRole, RectRole
from inselect.gui.utils import unite_rects, contiguous, PaintState

from .resize_handle import ResizeHandle


class GraphicsItemView(QtGui.QAbstractItemView):
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
        super(GraphicsItemView, self).__init__(parent)
        self.scene = Scene(self, parent)

        # List of QGraphicsRectItem
        self._rows = []

        self.handling_selection_update = False
        self.scene.selectionChanged.connect(self.scene_selection_changed)

    def reset(self):
        """QAbstractItemView virtual
        """
        debug_print('GraphicsItemView.reset')
        super(GraphicsItemView, self).reset()

        model = self.model()
        self.scene.new_document(model.data(QtCore.QModelIndex(), PixmapRole))

        # Build up new mapping
        r = [None] * model.rowCount()
        for row in xrange(0, model.rowCount()):
            rect = self.model().index(row, 0).data(RectRole)
            r[row] = self.scene.add_box(rect)

        self._rows = r

    def rowsInserted(self, parent, start, end):
        """QAbstractItemView slot
        """
        debug_print('GraphicsItemView.rowsInserted', start, end)

        # New boxes but are coming but their rects are not yet known.
        # Create new items with zero height and zero width rects - actual rects
        # will be set in dataChanged()
        n = 1 + end - start
        new = [None] * n
        rect = QRect(0, 0, 0, 0)
        for row in xrange(0, n):
            new[row] = self.scene.add_box(rect)
        self._rows[start:start] = new

    def dataChanged(self, topLeft, bottomRight):
        """QAbstractItemView virtual
        """
        debug_print('GraphicsItemView.dataChanged', topLeft.row(), bottomRight.row())

        for row in xrange(topLeft.row(), 1+bottomRight.row()):
            # new is a QRect - integer coordinates
            new = self.model().index(row, 0).data(RectRole)

            # Cumbersome conversion to ints
            item = self._rows[row]
            current = item.sceneBoundingRect()
            current = QRect(current.left(), current.top(),
                            current.width(), current.height())
            if current!=new:
                msg = 'Update rect for [{0}] from [{1}] to [{2}]'
                debug_print(msg.format(row, current, new))
                item.prepareGeometryChange()

                # setrect() expects floating point rect
                item.setRect(QRectF(new))

    def rowsAboutToBeRemoved(self, parent, start, end):
        """QAbstractItemView slot
        """
        debug_print('GraphicsItemView.rowsAboutToBeRemoved', start, end)

        map(self.scene.removeItem, self._rows[start:end])

        # Remove items
        self._rows[start:end] = []

    def selectionChanged(self, selected, deselected):
        """QAbstractItemView virtual
        """
        # Tell the scene about the new selection
        # TODO LH Use a timer to implement a delayed refresh
        if not self.handling_selection_update:
            # TODO Context for this
            debug_print('GraphicsItemView.selectionChanged')
            self.handling_selection_update = True
            try:
                current = set(self.scene.selectedItems())
                new = set(self._rows[i.row()] for i in self.selectionModel().selectedIndexes())

                for item in new.difference(current):
                    item.setSelected(True)
                    item.update()

                for item in current.difference(new):
                    item.setSelected(False)
                    item.update()

                if new:
                    # Ensure that the selected items are visible
                    rect = unite_rects([i.rect() for i in new])
                    debug_print('GraphicsItemView will make visible', rect)
                    new.pop().ensureVisible(rect)
            finally:
                self.handling_selection_update = False

    def _rows_of_items(self, items):
        """Returns a generator of row numbers of the list of QGraphicsItems
        """
        # TODO LH This is horrible
        # TODO LH Use a view to support changes to self._rows during iteration?
        return (self._rows.index(i) for i in items)

    def _indexes_of_items(self, items):
        """Returns a generator of indexes of the list of QGraphicsItems
        """
        # TODO LH Use a view to support changes to self._rows during iteration?
        return (self.model().index(row, 0) for row in self._rows_of_items(items))

    def scene_selection_changed(self):
        """scene.selectionChanged slot
        """
        # TODO LH Fix dreadful performance when selection changing as a result
        # of mouse drag
        if not self.handling_selection_update:
            debug_print('GraphicsItemView.scene_selection_changed')
            # TODO Context for this
            self.handling_selection_update = True
            try:
                model = self.model()
                sm = self.selectionModel()
                current = set(i.row() for i in sm.selectedIndexes())
                updated = set(self._rows_of_items(self.scene.selectedItems()))

                # Select contiguous blocks
                for row, count in contiguous(sorted(updated.difference(current))):
                    top_left = model.index(row, 0)
                    bottom_right = model.index(row+count-1, 0)
                    sm.select(QtGui.QItemSelection(top_left, bottom_right),
                              QtGui.QItemSelectionModel.Select)

                # Deselect contiguous blocks
                for row, count in contiguous(sorted(current.difference(updated))):
                    top_left = model.index(row, 0)
                    bottom_right = model.index(row+count-1, 0)
                    sm.select(QtGui.QItemSelection(top_left, bottom_right),
                              QtGui.QItemSelectionModel.Deselect)

                if updated:
                    # Set an arbitraty row as the current index
                    sm.setCurrentIndex(model.index(updated.pop(), 0),
                                       QtGui.QItemSelectionModel.Current)
            finally:
                self.handling_selection_update = False

    def scene_item_rects_updated(self, items):
        """The user moved or resized items in the scene
        """
        debug_print('GraphicsItemView.item_rects_updated')
        for index,item in izip(self._indexes_of_items(items), items):
            # item.sceneBoundingRect() is the items rects in the correct
            # coordinates system
            print('Row [{0}] updated'.format(index.row()))
            rect = item.sceneBoundingRect()
            # Cumbersome conversion to ints
            rect = QRect(rect.left(), rect.top(), rect.width(), rect.height())
            self.model().setData(index, rect, RectRole)

    def scene_items_deleted(self, items):
        """The user deleted items from the scene
        """
        # Inform the model of the indexes that have been deleted
        # The items will be deleted from the scene in this class's
        # rowsAboutToBeRemoved() implementation

        # Delete contiguous blocks of rows
        selected = sorted([i.row() for i in self.selectionModel().selectedIndexes()])

        # Clear selection before deleting
        self.clearSelection()

        # TODO LH We shouldn't need to remove blocks in reverse order - stems
        # from crummy GraphicsItemView
        # Remove blocks in reverse order so that row indices are not invalidated
        for row, count in reversed(list(contiguous(selected))):
            self.model().removeRows(row, count)


class Scene(QtGui.QGraphicsScene):
    """
    """
    def __init__(self, source, parent=None):
        super(Scene, self).__init__(parent)
        self.source = source

        # A mapping from QGraphicsItem to QRectF of selected items,
        # populated on mouseReleaseEvent()
        self._mouse_press_selection = {}

        self.setBackgroundBrush(QtGui.QBrush(Qt.darkGray))

    def new_document(self, pixmap):
        """A new document. pixmap should be a QPixmap or None.
        """
        self.clear()  # Removes all items

        if pixmap:
            debug_print('New scene [{0}] [{1}]'.format(pixmap.width(), pixmap.height()))
            self.setSceneRect(0, 0, pixmap.width(), pixmap.height())
            self.addItem(QtGui.QGraphicsPixmapItem(pixmap))
            for v in self.views():
                v.updateSceneRect(self.sceneRect())
        else:
            debug_print('Clear scene')
            self.setSceneRect(0, 0, 0, 0)

    def add_box(self, rect):
        # Notification from source that a box has been added
        item = BoxItem(rect.left(), rect.top(), rect.width(), rect.height())
        self.addItem(item)
        return item

    def keyPressEvent(self, event):
        """QGraphicsScene virtual
        """
        debug_print('Scene.keyPressEvent')
        if event.key() == Qt.Key_Delete:
            # Delete the selected items from source
            selected = self.selectedItems()
            self.source.scene_items_deleted(selected)
            event.accept()
        else:
            super(Scene, self).keyPressEvent(event)

    def mousePressEvent(self, event):
        """QGraphicsScene virtual
        """
        debug_print('Scene.mousePressEvent')
        super(Scene, self).mousePressEvent(event)

        if self._mouse_press_selection:
            debug_print('Unexpected _mouse_press_selection')
            self._mouse_press_selection = {}

        # Record the scene bounding rect of each selected items
        selected = self.selectedItems()
        self._mouse_press_selection = {i: i.sceneBoundingRect() for i in selected}

    def mouseReleaseEvent(self, event):
        """QGraphicsScene virtual
        """
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
            self.source.scene_item_rects_updated(selected)


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


class BoxItem(QtGui.QGraphicsRectItem):
    # Might be some relevant stuff here:
    # http://stackoverflow.com/questions/10590881/events-and-signals-in-qts-qgraphicsitem-how-is-this-supposed-to-work

    UNSELECTED = QtGui.QColor(0x00, 0x00, 0xff, 0xcc)
    SELECTED =   QtGui.QColor(0xff, 0x00, 0x00, 0xcc)
    RESIZING =   QtGui.QColor(0xff, 0x00, 0x00, 0x50)

    def __init__(self, x, y, w, h, parent=None, scene=None):
        super(BoxItem, self).__init__(x, y, w, h, parent, scene)
        self.setFlags(QtGui.QGraphicsItem.ItemIsFocusable |
                      QtGui.QGraphicsItem.ItemIsSelectable |
                      QtGui.QGraphicsItem.ItemSendsGeometryChanges |
                      QtGui.QGraphicsItem.ItemIsMovable)

        self.setCursor(Qt.ArrowCursor)
        self.setAcceptHoverEvents(True)

        self._handles_visible = False
        self._handles = []

        positions = (Qt.TopLeftCorner, Qt.TopRightCorner, Qt.BottomLeftCorner,
                     Qt.BottomRightCorner)
        self._handles = [self._create_handle(pos) for pos in positions]
        self._layout_handles()

    def paint(self, painter, option, widget=None):
        """QGraphicsRectItem virtual
        """
        # Thick red border is selected
        # Think blue border if not
        thickness = 3 if self.isSelected() else 1
        with PaintState(painter):
            painter.setPen(QtGui.QPen(self.colour, thickness, Qt.SolidLine))
            painter.drawRect(self.boundingRect())

    @property
    def colour(self):
        """QtGui.QColor
        """
        if self.scene().mouseGrabberItem() in self._handles:
            return self.RESIZING
        else:
            return self.SELECTED if self.isSelected() else self.UNSELECTED

    def hoverEnterEvent(self, event):
        """QGraphicsRectItem virtual
        """
        debug_print('BoxItem.hoverEnterEvent')
        super(BoxItem, self).hoverEnterEvent(event)
        self._set_handles_visible(True)

    def hoverLeaveEvent(self, event):
        """QGraphicsRectItem virtual
        """
        debug_print('BoxItem.hoverLeaveEvent')
        super(BoxItem, self).hoverLeaveEvent(event)
        self._set_handles_visible(False)

    def _set_handles_visible(self, visible):
        self._handles_visible = visible
        map(lambda i: i.setVisible(visible), self._handles)

    def _create_handle(self, corner):
        # Creates and returns a new ResizeHandle at the given Qt.Corner
        handle = ResizeHandle(corner, self)
        handle.setZValue(2.0)
        handle.setVisible(self._handles_visible)
        return handle

    def _layout_handles(self):
        """Moves handles to the appropriate positions
        """
        map(lambda i: i.relayout(self.boundingRect()), self._handles)

    def update_handles(self):
        """Updates handles
        """
        for item in self._handles + [self]:
            item.update()

    def setRect(self, rect):
        """QGraphicsRectItem function
        """
        debug_print('setRect')
        super(BoxItem, self).setRect(rect)
        self._layout_handles()

    def mousePressEvent(self, event):
        """QGraphicsRectItem virtual
        """
        debug_print('mousePressEvent')
        super(BoxItem, self).mousePressEvent(event)
        self.update_handles()
