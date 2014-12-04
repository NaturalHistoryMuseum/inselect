from itertools import izip

from PySide import QtCore, QtGui
from PySide.QtCore import Qt, QRect, QRectF

from inselect.lib.utils import debug_print
from inselect.gui.roles import PixmapRole, RectRole
from inselect.gui.utils import unite_rects, contiguous

from .boxes_scene import BoxesScene


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
        self.scene = BoxesScene(self, parent)

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
