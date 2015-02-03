from PySide.QtCore import QRect, QSize, QPoint, Qt, QCoreApplication
from PySide.QtGui import (QListView, QBrush, QStyle, QTransform, QPen,
                          QAbstractItemView, QAbstractItemDelegate,
                          QStyleOptionButton, QItemSelectionModel)

from inselect.lib.utils import debug_print
from inselect.gui.utils import PaintState
from inselect.gui.roles import RectRole, PixmapRole, RotationRole


class CropDelegate(QAbstractItemDelegate):
    """Delegate that shows cropped specimen images with a grey box and
    provides editing of rotation and some flags.
    """

    @property
    def BOX_RECT(self):
        "QRect of the complete box"
        expanded = self.parent().expanded
        return self.parent().viewport().rect() if expanded else QRect(0, 0, 250, 250)
 
    @property
    def TITLE_RECT(self):
        "Bounding QRect of the title"
        return QRect(QPoint(0, 0), self.BOX_RECT.size()).adjusted(5, 5, -5, -5)

    @property
    def BORDER(self):
        # Border around cropped image
        return 25

    @property
    def CROP_RECT(self):
        # Bounding rectangle within which the cropped image will be drawn
        b = self.BORDER
        return self.BOX_RECT.adjusted(b, b, -b, -b)

    @property
    def CONTROLS_SIZE(self):
        # Controls
        return 23

    @property
    def ROTATE_COUNTERCLOCKWISE_RECT(self):
        r = QRect(0, 0, self.CONTROLS_SIZE, self.CONTROLS_SIZE)
        r.translate(QPoint(0, self.BOX_RECT.height()-self.CONTROLS_SIZE))
        return r

    @property
    def ROTATE_CLOCKWISE_RECT(self):
        r = QRect(0, 0, self.CONTROLS_SIZE, self.CONTROLS_SIZE)
        r.translate(QPoint(self.BOX_RECT.width()-self.CONTROLS_SIZE,
                           self.BOX_RECT.height()-self.CONTROLS_SIZE))
        return r

    BLACK = QBrush(Qt.black)
    WHITE = QBrush(Qt.white)
    GREY = QBrush(Qt.gray)
    DARK_GREY = QBrush(Qt.darkGray)

    def _paint_box(self, painter, option, index):
        """The grey box
        """
        selected = QStyle.State_Selected & option.state
        with PaintState(painter):
            painter.setBrush(self.GREY if selected else self.DARK_GREY)
            painter.drawRect(option.rect)
 
    def _paint_title(self, painter, option, index):
        """Title of this crop
        """
        title = index.data(Qt.DisplayRole)
        rect = self.TITLE_RECT.translated(option.rect.topLeft())
        painter.drawText(rect, Qt.AlignTop | Qt.AlignLeft, title)

    def _paint_crop(self, painter, option, index):
        """The cropped image
        """
        source_rect = index.data(RectRole)
        crop_rect = self.CROP_RECT.translated(option.rect.topLeft())
        angle = index.data(RotationRole)

        # Target rect with same aspect ratio as source
        source_aspect = float(source_rect.width()) / source_rect.height()
        crop_aspect = float(crop_rect.width()) / crop_rect.height()

        # True is the item has been rotated by a multiple of 90 degrees
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

        with PaintState(painter):
            if angle:
                painter.setTransform(t)
            painter.drawPixmap(target_rect, index.data(PixmapRole), source_rect)

            painter.setPen(QPen(Qt.white, 1, Qt.SolidLine))
            painter.drawRect(target_rect)

    def _paint_controls(self, painter, option, index):
        """Arrows to rotate crops
        """

        with PaintState(painter):
            selected = QStyle.State_Selected & option.state
            painter.setBrush(self.WHITE if selected else self.GREY)
            f = option.font
            f.setPointSize(19)  # TODO LH Arbitrary font size
            painter.setFont(f)

            # \u293e and \u293f are unicode characters for 'lower right
            # semicircular clockwise arrow' and 'lower right semicircular
            # anticlockwise arrow' respectively
            clockwise = self.ROTATE_CLOCKWISE_RECT.translated(option.rect.topLeft())
            painter.drawRect(clockwise)
            painter.drawText(clockwise, Qt.AlignVCenter | Qt.AlignHCenter, u'\u293e')

            clockwise = self.ROTATE_COUNTERCLOCKWISE_RECT.translated(option.rect.topLeft())
            painter.drawRect(clockwise)
            painter.drawText(clockwise, Qt.AlignVCenter | Qt.AlignHCenter, u'\u293f')

    def paint(self, painter, option, index):
        """QAbstractItemDelegate virtual
        """
        self._paint_box(painter, option, index)
        self._paint_title(painter, option, index)
        self._paint_crop(painter, option, index)
        self._paint_controls(painter, option, index)

    def sizeHint(self, option, index):
        return self.BOX_RECT.size()
 
    def closeEditor(self, editor, hint):
        """QAbstractItemDelegate signal
        """
        debug_print('CropDelegate.closeEditor')
        return super(CropDelegate, self).closeEditor(editor, hint)

    def commitData(self, editor):
        """QAbstractItemDelegate signal
        """
        debug_print('CropDelegate.commitData')
        return super(CropDelegate, self).commitData(editor)

    def createEditor(self, parent, option, index):
        """QAbstractItemDelegate virtual
        """
        debug_print('CropDelegate.createEditor')
        return super(CropDelegate, self).createEditor(parent, option, index)

    def editorEvent(self, event, model, option, index):
        """QAbstractItemDelegate virtual
        """
        if event.type() in (event.MouseButtonPress,event.MouseButtonDblClick):
            p = event.pos() - option.rect.topLeft()
            # Not returning True here so that base handler will set selection
            # to index, if it is not already selected
            if self.ROTATE_CLOCKWISE_RECT.contains(p):
                debug_print('CropDelegate.editorEvent rotate clockwise')
                current = index.data(RotationRole)
                model.setData(index, current+90, RotationRole)
            elif self.ROTATE_COUNTERCLOCKWISE_RECT.contains(p):
                debug_print('CropDelegate.editorEvent rotate counter-clockwise')
                current = index.data(RotationRole)
                model.setData(index, current-90, RotationRole)

        return super(CropDelegate, self).editorEvent(event, model, option, index)

    def setEditorData(self, editor, index):
        """QAbstractItemDelegate virtual
        """
        debug_print('CropDelegate.setEditorData')
        return super(CropDelegate, self).setEditorData(event, editor, index)


class GridView(QListView):
    """Shows cropped images in a grid
    """
    def __init__(self, parent=None):
        super(GridView, self).__init__(parent)

        # Items are shown in a grid if False
        # A single item is shown expanded if True.

        # A serious problem with this approach is that multiple selections are
        # possible (despite setting SingleSelection in show_expanded):
        # Select All shortcut
        # Select None shortcut
        # Select none or multiple on Boxes view, then go to metadataview

        self.expanded = False

        self.setItemDelegate(CropDelegate(self))
        self.setFlow(self.LeftToRight)
        self.setWrapping(True)
        self.setResizeMode(self.Adjust)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setStyleSheet("background-color: darkgray;")

    def show_grid(self):
        debug_print('GridView.show_grid')
        self.expanded = False
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self._refresh()

    def show_expanded(self):
        debug_print('GridView.show_expanded')
        self.expanded = True
        self.setSelectionMode(QAbstractItemView.SingleSelection)

        # Select a single item
        sm = self.selectionModel()
        selected = self.selectionModel().selectedIndexes()
        if len(selected)>1:
            sm.select(selected[0], QItemSelectionModel.Select)
        elif not selected:
            sm.select(self.model().index(0, 0), QItemSelectionModel.Select)

        self._refresh()

    def _refresh(self):
        debug_print('GridView.toggle_display_size')
        self.scheduleDelayedItemsLayout()
        selected = self.selectionModel().selectedIndexes()
        if selected:
            self.scrollTo(selected[0])

    def toggle_zoom(self):
        debug_print('GridView.toggle_zoom')

        selected = self.selectionModel().selectedIndexes()
        self.toggle_item_display_size(selected[0])
