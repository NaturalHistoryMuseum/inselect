from itertools import izip

from PySide import QtCore, QtGui
from PySide.QtCore import QRect

from inselect.lib.inselect_error import InselectError
from inselect.lib.utils import debug_print
from inselect.gui.roles import PixmapRole, RectRole, MetadataValidRole
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
    * addition of boxes
    * deletion of boxes
    * metadata valid status (MetadataValidRole)
    * TODO box verified status
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
        rows = [None] * model.rowCount()
        for row in xrange(0, model.rowCount()):
            index = model.index(row, 0)
            rows[row] = self.scene.add_box(index.data(RectRole),
                                           index.data(MetadataValidRole))
        self._rows = rows

    def show_alternative_pixmap(self, pixmap):
        """Show or clear an alternative pixmap in place of the document's usual
        pixmap. pixmaps should either be a QPixmap of the same dimensions as the
        documents pixmap (which is shown) or None (which clears any existing
        alternative pixmap)
        """
        debug_print('show_alternative_pixmap', pixmap)
        model = self.model()
        pixmap = pixmap if pixmap else model.data(QtCore.QModelIndex(), PixmapRole)
        self.scene.set_pixmap(pixmap)

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
            new[row] = self.scene.add_box(rect, False)
        self._rows[start:start] = new

    def dataChanged(self, topLeft, bottomRight):
        """QAbstractItemView virtual
        """
        debug_print('GraphicsItemView.dataChanged', topLeft.row(), bottomRight.row())

        for row in xrange(topLeft.row(), 1+bottomRight.row()):

            item = self._rows[row]
            # new is a QRect - integer coordinates
            index = self.model().index(row, 0)
            item.set_rect(index.data(RectRole))
            item.set_isvalid(index.data(MetadataValidRole))

    def rowsAboutToBeRemoved(self, parent, start, end):
        """QAbstractItemView slot
        """
        debug_print('GraphicsItemView.rowsAboutToBeRemoved', start, end)

        if self.handling_selection_update:
            debug_print('Unexpected handling_selection_update in '
                        'GraphicsItemView.rowsAboutToBeRemoved')

        # Ignore the selectionChanged() notifications that the scene will send
        # for every item that is about to be removed.
        self.handling_selection_update = True
        try:
            # TODO Context for this
            map(self.scene.removeItem, self._rows[start:end])
        finally:
            self.handling_selection_update = False

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

                if 1 == len(new):
                    rect = new.pop().rect()
                    for view in self.scene.views():
                        view.centerOn(rect.center())
                elif 1 < len(new):
                    # Ensure that the selected items are visible
                    rect = unite_rects([i.rect() for i in new])
                    debug_print('GraphicsItemView will make visible', rect)
                    new.pop().ensureVisible(rect)
            finally:
                self.handling_selection_update = False

    def rows_of_items(self, items):
        """Returns a generator of row numbers of the list of QGraphicsItems
        """
        # TODO LH This is horrible
        # TODO LH Use a view to support changes to self._rows during iteration?
        return (self._rows.index(i) for i in items)

    def indexes_of_items(self, items):
        """Returns a generator of indexes of the list of QGraphicsItems
        """
        # TODO LH Use a view to support changes to self._rows during iteration?
        return (self.model().index(row, 0) for row in self.rows_of_items(items))

    def items_of_rows(self, rows):
        """Returns an iterable of QGraphicsItems for the given rows
        """
        return (self._rows[r] for r in rows)

    def items_of_indexes(self, indexes):
        """Returns an iterable of QGraphicsItems for the given indexes
        """
        return (self._rows[i.row()] for i in indexes)

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
                updated = set(self.rows_of_items(self.scene.selectedItems()))

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
                    # Set an arbitrary row as the current index
                    sm.setCurrentIndex(model.index(updated.pop(), 0),
                                       QtGui.QItemSelectionModel.Current)
            finally:
                self.handling_selection_update = False

    def scene_item_rects_updated(self, items):
        """The user moved or resized items in the scene
        """
        debug_print('GraphicsItemView.item_rects_updated')
        for index,item in izip(self.indexes_of_items(items), items):
            # item.sceneBoundingRect() is the items rects in the correct
            # coordinates system
            debug_print('Row [{0}] updated'.format(index.row()))
            rect = item.sceneBoundingRect()
            # Cumbersome conversion to ints
            rect = QRect(rect.left(), rect.top(), rect.width(), rect.height())
            self.model().setData(index, rect, RectRole)

    def scene_box_added(self, rect):
        """The user added a box
        """
        m = self.model()
        row = len(self._rows)
        if not m.insertRow(row):
            raise InselectError('Could not insert row')
        else:
            # Cumbersome conversion to ints
            rect = QRect(rect.left(), rect.top(), rect.width(), rect.height())
            if not m.setData(m.index(row, 0), rect, RectRole):
                raise InselectError('Could not set rect')
            else:
                # Select the new box
                self.scene.clearSelection()
                item = self.items_of_rows([row]).next()
                item.setSelected(True)
                item.update()
