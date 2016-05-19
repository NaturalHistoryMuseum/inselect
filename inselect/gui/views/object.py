from PySide.QtCore import QRect, QSize, QPoint, Qt
from PySide.QtGui import (QColor, QListView, QBrush, QStyle, QTransform, QPen,
                          QAbstractItemView, QStyledItemDelegate,
                          QItemSelectionModel, QFont)

from inselect.lib.utils import debug_print
from inselect.gui.colours import colour_scheme_choice
from inselect.gui.utils import painter_state
from inselect.gui.roles import (MetadataValidRole, PixmapRole, RectRole,
                                RotationRole)


# TODO LH Delegate should respect stylesheet

def _blend_colour(first, second, amount=0.5):
    """Returns first + (second - first) * amount, without changing the alpha of
    first.
    """
    r1, g1, b1, a1 = first.getRgb()
    r2, g2, b2, a2 = second.getRgb()
    return QColor(
        r1 + (r2 - r1) * amount,
        g1 + (g2 - g1) * amount,
        b1 + (b2 - b1) * amount,
        a1
    )


class CropDelegate(QStyledItemDelegate):
    """Delegate that shows cropped object images with a grey box and
    provides editing of rotation and some flags.
    """

    # Brushes
    BLACK = QBrush(Qt.black)
    WHITE = QBrush(Qt.white)

    GRID_INVALID_COLOUR = QColor(0xfb, 0x9a, 0x99)
    INVALID = QBrush(GRID_INVALID_COLOUR)
    # Colour of selected invalid is the invalid colour lightened
    INVALID_SELECTED = QBrush(
        _blend_colour(GRID_INVALID_COLOUR,
                      QColor(0xff, 0xff, 0xff),
                      amount=0.3)
    )
    GREY = QBrush(Qt.gray)
    DARK_GREY = QBrush(Qt.darkGray)

    # Border around cropped image
    BORDER = 25

    @property
    def box_rect(self):
        "QRect of the complete box"
        expanded = self.parent().expanded
        return self.parent().viewport().rect() if expanded else QRect(0, 0, 250, 250)

    @property
    def title_rect(self):
        "Bounding QRect of the title"
        return QRect(QPoint(0, 0), self.box_rect.size()).adjusted(5, 5, -5, -5)

    @property
    def crop_rect(self):
        """QRect within which the cropped image will be drawn
        """
        b = self.BORDER
        return self.box_rect.adjusted(b, b, -b, -b)

    def _paint_box(self, painter, option, index):
        """Paints background
        """
        valid = index.data(MetadataValidRole)
        selected = QStyle.State_Selected & option.state
        with painter_state(painter):
            if not valid:
                painter.setBrush(self.INVALID_SELECTED if selected else self.INVALID)
            else:
                painter.setBrush(self.GREY if selected else self.DARK_GREY)
            painter.setPen(Qt.black)
            painter.drawRect(option.rect)

    def _paint_title(self, painter, option, index):
        """Paints the title of this crop
        """
        with painter_state(painter):
            font = painter.font()
            font.setPointSize(14)  # TODO LH Arbitrary font size
            font.setWeight(QFont.Black)
            painter.setFont(font)
            rect = self.title_rect.translated(option.rect.topLeft())

            # Textual title in black at top left
            painter.setPen(Qt.black)
            painter.drawText(rect, Qt.AlignTop | Qt.AlignLeft,
                             index.data(Qt.DisplayRole))

    def _paint_crop(self, painter, option, index):
        """Paints the crop
        """
        source_rect = index.data(RectRole)
        crop_rect = self.crop_rect.translated(option.rect.topLeft())
        angle = index.data(RotationRole)

        # Target rect with same aspect ratio as source
        source_aspect = float(source_rect.width()) / source_rect.height()
        crop_aspect = float(crop_rect.width()) / crop_rect.height()

        # True if the item has been rotated by a multiple of 90 degrees
        perpendicular = 1 == (angle / 90) % 2

        # Some nasty logic to compute the target rect
        if perpendicular:
            crop_aspect = 1.0 / crop_aspect

        if source_aspect > 1.0:
            # Crop is wider than is is tall
            if crop_aspect > source_aspect:
                fit_to = 'height'
                f = 1.0 / source_aspect
            else:
                fit_to = 'width'
                f = source_aspect
        else:
            # Crop is taller than is is wide
            if crop_aspect < source_aspect:
                fit_to = 'width'
                f = source_aspect
            else:
                fit_to = 'height'
                f = 1.0 / source_aspect

        if perpendicular:
            if 'width' == fit_to:
                size = QSize(crop_rect.height(),
                             crop_rect.height() / f)
            else:
                size = QSize(crop_rect.width() / f,
                             crop_rect.width())
        else:
            if 'width' == fit_to:
                size = QSize(crop_rect.width(),
                             crop_rect.width() / f)
            else:
                size = QSize(crop_rect.height() / f,
                             crop_rect.height())

        target_rect = QRect(crop_rect.topLeft(), size)
        target_rect.moveCenter(option.rect.center())

        # Draw rotated
        if angle:
            t = QTransform()
            t.translate(option.rect.width() / 2+option.rect.left(),
                        option.rect.height() / 2+option.rect.top())
            t.rotate(angle)
            t.translate(-option.rect.width() / 2-option.rect.left(),
                        -option.rect.height() / 2-option.rect.top())

        with painter_state(painter):
            if angle:
                painter.setTransform(t)
            painter.drawPixmap(target_rect, index.data(PixmapRole), source_rect)

            if QStyle.State_Selected & option.state:
                painter.setPen(QPen(Qt.white, 1, Qt.SolidLine))
                painter.drawRect(target_rect)

    def paint(self, painter, option, index):
        """QAbstractItemDelegate virtual
        """
        self._paint_box(painter, option, index)
        self._paint_title(painter, option, index)
        self._paint_crop(painter, option, index)

    def sizeHint(self, option, index):
        return self.box_rect.size()


class ObjectView(QListView):
    """Shows cropped object images either in a grid or expanded
    """
    def __init__(self, parent=None):
        super(ObjectView, self).__init__(parent)

        # Items are shown in a grid if False.
        # A single item is shown expanded if True.
        # When more than one item is selected, view changes to grid.
        self.expanded = False

        self.setItemDelegate(CropDelegate(self))
        self.setFlow(self.LeftToRight)
        self.setWrapping(True)
        self.setResizeMode(self.Adjust)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        # self.setStyleSheet("background-color: darkgray;")

        # Activating an item toggles the expanded state
        self.activated.connect(self.toggle_expanded)

        colour_scheme_choice().colour_scheme_changed.connect(self.colour_scheme_changed)

    def colour_scheme_changed(self):
        """Slot for colour_scheme_changed signal
        """
        self.update()

    def selectionChanged(self, selected, deselected):
        """QAbstractItemView slot
        """
        debug_print('ObjectView.selectionChanged')

        # Grid view unless exactly one item selected
        if self.expanded and 1 != len(self.selectionModel().selectedIndexes()):
            self.show_grid()

        super(ObjectView, self).selectionChanged(selected, deselected)

    def show_grid(self):
        """Shows the list as a grid of squares
        """
        debug_print('ObjectView.show_grid')
        self.expanded = False
        self._refresh()

    def show_expanded(self):
        """Shows the first item of the selection expanded to fill the viewport.
        If the selection is empty, the first item in the list is selected.
        """
        debug_print('ObjectView.show_expanded')
        self.expanded = True

        # Select a single item
        sm = self.selectionModel()
        selected = sm.selectedIndexes()
        if len(selected) > 1:
            sm.select(selected[0], QItemSelectionModel.ClearAndSelect)
        elif not selected:
            sm.select(self.model().index(0, 0), QItemSelectionModel.Select)

        self._refresh()

    def toggle_expanded(self, index):
        """Selects 'index' and toggles the expanded state
        """
        debug_print('ObjectView.toggle_expanded')
        self.selectionModel().select(index, QItemSelectionModel.Select)
        if self.expanded:
            self.show_grid()
        else:
            self.show_expanded()

    def _refresh(self):
        debug_print('ObjectView._refresh')
        self.scheduleDelayedItemsLayout()
        selected = self.selectionModel().selectedIndexes()
        if selected:
            self.scrollTo(selected[0])

    def keyPressEvent(self, event):
        """QAbstractItemView virtual
        """
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            # This logic reimplemented from QAbstractItemView::keyPressEvent,
            # in src/gui/itemviews/qabstractitemview.cpp - make 'Enter' and
            # 'Return' keys toggle the 'Expanded' / 'Grid' state on Mac OS X
            if self.state() != QListView.EditingState or self.hasFocus():
                if self.currentIndex().isValid():
                    self.activated.emit(self.currentIndex())
                event.ignore()
        else:
            super(ObjectView, self).keyPressEvent(event)
