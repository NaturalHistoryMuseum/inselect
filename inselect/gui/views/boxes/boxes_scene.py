from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsItem, QGraphicsPixmapItem

from inselect.lib.utils import debug_print

from .box_item import BoxItem


class BoxesScene(QGraphicsScene):
    """Boxes on an image of objects
    """
    def __init__(self, source, parent=None):
        super(BoxesScene, self).__init__(parent)
        self.source = source

        # A pixmap that is accessed by BoxItems during painting
        self.pixmap = None

        # A mapping from QGraphicsItem to QRectF of selected items,
        # populated on mouseReleaseEvent()
        self._mouse_press_selection = {}

    def new_document(self, pixmap):
        """A new document. pixmap should be a QPixmap or None.
        """
        self.clear()  # Removes all items

        if pixmap:
            debug_print('New scene [{0}] [{1}]'.format(pixmap.width(), pixmap.height()))
            self.setSceneRect(0, 0, pixmap.width(), pixmap.height())
            self.addItem(QGraphicsPixmapItem(pixmap))
            self.pixmap = pixmap
            for v in self.views():
                v.updateSceneRect(self.sceneRect())
        else:
            debug_print('Clear scene')
            self.setSceneRect(0, 0, 0, 0)
            self.pixmap = None

    @property
    def is_empty(self):
        """True if the scene does not contain a document
        """
        return 0 == self.sceneRect().width()

    @property
    def pixmap_item(self):
        """The single QGraphicsPixmapItem within this scene, or None if there is
        no open document
        """
        items = list(self.items())
        if not items:
            return None
        else:
            items = filter(lambda i: isinstance(i, QGraphicsPixmapItem), items)
            pixmap = next(items)

            # There should be only one pixmap item
            try:
                next(items)
            except StopIteration:
                return pixmap
            else:
                raise ValueError('Unexpected number of graphics pixmap items')

    def set_pixmap(self, pixmap):
        """Sets pixmap as the display image. pixmap should be a QPixmap with the
        same dimensions as self.width(), self.height().
        """
        pixmap_item = self.pixmap_item
        if pixmap_item:
            pw, ph = pixmap.width(), pixmap.height()
            sw, sh = self.width(), self.height()
            if not (pw == int(sw) and ph == int(sh)):
                raise ValueError('Unexpected pixmap dimension')
            else:
                pixmap_item.setPixmap(pixmap)
                self.pixmap = pixmap
                self.update()

    def box_items(self):
        "Iterable containin just BoxItems"
        return filter(lambda i: isinstance(i, BoxItem), list(self.items()))

    def add_box(self, rect, isvalid):
        """Notification from source that a box has been added.

        Adds a Box item at the given rect.
        """
        item = BoxItem(rect.left(), rect.top(), rect.width(), rect.height(),
                       isvalid)
        self.addItem(item)
        return item

    def user_add_box(self, rect):
        """Informs the source that the user has added a box
        """
        self.source.scene_box_added(rect)

    def keyPressEvent(self, event):
        """QGraphicsScene virtual
        """
        debug_print('BoxesScene.keyPressEvent')

        key = event.key()

        # Mapping from cursor key to adjustment (dx1, dy1, dx2, dy2)
        cursors = {
            Qt.Key_Up:    ( 0.0,-1.0, 0.0,-1.0),
            Qt.Key_Right: ( 1.0, 0.0, 1.0, 0.0),
            Qt.Key_Down:  ( 0.0, 1.0, 0.0, 1.0),
            Qt.Key_Left:  (-1.0, 0.0,-1.0, 0.0),
        }

        if key in cursors:
            event.accept()
            dx1, dy1, dx2, dy2 = cursors[key]
            modifiers = event.modifiers()

            if Qt.ShiftModifier & modifiers and not Qt.AltModifier & modifiers:
                # Adjust the bottom-right corner
                dx1 = dy1 = 0.0
            elif not Qt.ShiftModifier & modifiers and Qt.AltModifier & modifiers:
                # Adjust the top-left corner
                dx2 = dy2 = 0.0

            if event.isAutoRepeat():
                # Larger steps when key is being held down
                multiplier = 4
                dx1, dy1, dx2, dy2 = [v * multiplier for v in (dx1, dy1, dx2, dy2)]
            self.adjust_selected(dx1, dy1, dx2, dy2)
        else:
            super(BoxesScene, self).keyPressEvent(event)

    def mousePressEvent(self, event):
        """QGraphicsScene virtual
        """
        debug_print('BoxesScene.mousePressEvent')
        super(BoxesScene, self).mousePressEvent(event)

        if self._mouse_press_selection:
            debug_print('Unexpected _mouse_press_selection')
            self._mouse_press_selection = {}

        # Record the scene bounding rect of each selected items
        selected = self.selectedItems()
        self._mouse_press_selection = {i: i.sceneBoundingRect() for i in selected}

    def mouseReleaseEvent(self, event):
        """QGraphicsScene virtual
        """
        debug_print('BoxesScene.mouseReleaseEvent')
        super(BoxesScene, self).mouseReleaseEvent(event)

        # Work out which items have had their scene bounding rects altered
        # in between mousePressEvent() and mouseReleaseEvent()
        original, self._mouse_press_selection = self._mouse_press_selection, {}

        selected = self.selectedItems()
        current = {i: i.sceneBoundingRect() for i in selected}

        # List of items with a scene bounding rects different from that when
        # mousePressEvent() ocurred
        changed = [i for i in current if current[i] != original.get(i, current[i])]
        if changed:
            # This assumes that the order of items in self.selectedItems() has
            # not changed and that is one item's rect has altered then they all
            # have.
            self.source.scene_item_rects_updated(selected)

    def adjust_selected(self, dx1, dy1, dx2, dy2):
        """Adjusts the rects of the selected boxes
        """
        selected = self.selectedItems()
        for box in selected:
            box.adjust_rect(dx1, dy1, dx2, dy2)
        self.source.scene_item_rects_updated(selected)
