from PySide.QtCore import QRect, QSize, QPoint, Qt, QCoreApplication
from PySide.QtGui import (QListView, QBrush, QStyle, QTransform, QPen,
                          QAbstractItemView, QAbstractItemDelegate,
                          QStyleOptionButton, QItemSelectionModel,
                          QColor, QFont)

from inselect.lib.utils import debug_print
from inselect.gui.colours import COLOURS
from inselect.gui.utils import painter_state
from inselect.gui.roles import (RectRole, PixmapRole, RotationRole,
                                MetadataValidRole)


class CropDelegate(QAbstractItemDelegate):
    """Delegate that shows cropped gecimen images with a grey box and
    provides editing of rotation and some flags.
    """

    # Brushes
    BLACK = QBrush(Qt.black)
    WHITE = QBrush(Qt.white)
    INVALID = QBrush(QColor(COLOURS['Invalid']))
    INVALID_SELECTED = QBrush(QColor(COLOURS['Invalid']))
    GREY = QBrush(Qt.gray)
    DARK_GREY = QBrush(Qt.darkGray)

    # Size of the rotation controls
    CONTROLS_SIZE = 23

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
        # Bounding rectangle within which the cropped image will be drawn
        b = self.BORDER
        return self.box_rect.adjusted(b, b, -b, -b)

    @property
    def rotate_counterclockwise_rect(self):
        r = QRect(0, 0, self.CONTROLS_SIZE, self.CONTROLS_SIZE)
        r.translate(QPoint(0, self.box_rect.height()-self.CONTROLS_SIZE))
        return r

    @property
    def rotate_clockwise_rect(self):
        r = QRect(0, 0, self.CONTROLS_SIZE, self.CONTROLS_SIZE)
        r.translate(QPoint(self.box_rect.width()-self.CONTROLS_SIZE,
                           self.box_rect.height()-self.CONTROLS_SIZE))
        return r

    def _paint_box(self, painter, option, index):
        """The grey box
        """
        valid = index.data(MetadataValidRole)
        selected = QStyle.State_Selected & option.state
        with painter_state(painter):
            if not valid:
                painter.setBrush(self.INVALID_SELECTED if selected else self.INVALID)
            else:
                painter.setBrush(self.GREY if selected else self.DARK_GREY)
            painter.drawRect(option.rect)
 
    def _paint_title(self, painter, option, index):
        """Title of this crop
        """
        with painter_state(painter):
            font = painter.font()
            font.setPointSize(13)  # TODO LH Arbitrary font size
            font.setWeight(QFont.Black)
            painter.setFont(font)
            title = index.data(Qt.DisplayRole)
            rect = self.title_rect.translated(option.rect.topLeft())
            painter.drawText(rect, Qt.AlignTop | Qt.AlignLeft, title)

    def _paint_crop(self, painter, option, index):
        """The cropped image
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

    def _paint_controls(self, painter, option, index):
        """Arrows to rotate crops
        """

        with painter_state(painter):
            selected = QStyle.State_Selected & option.state
            painter.setBrush(self.WHITE if selected else self.GREY)
            f = option.font
            f.setPointSize(19)  # TODO LH Arbitrary font size
            painter.setFont(f)

            # \u293e and \u293f are unicode characters for 'lower right
            # semicircular clockwise arrow' and 'lower right semicircular
            # anticlockwise arrow' respectively
            clockwise = self.rotate_clockwise_rect.translated(option.rect.topLeft())
            painter.drawRect(clockwise)
            painter.drawText(clockwise, Qt.AlignVCenter | Qt.AlignHCenter, u'\u293e')

            clockwise = self.rotate_counterclockwise_rect.translated(option.rect.topLeft())
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
        return self.box_rect.size()
 
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
            if self.rotate_clockwise_rect.contains(p):
                debug_print('CropDelegate.editorEvent rotate clockwise')
                current = index.data(RotationRole)
                model.setData(index, current+90, RotationRole)
            elif self.rotate_counterclockwise_rect.contains(p):
                debug_print('CropDelegate.editorEvent rotate counter-clockwise')
                current = index.data(RotationRole)
                model.setData(index, current-90, RotationRole)

        return super(CropDelegate, self).editorEvent(event, model, option, index)

    def setEditorData(self, editor, index):
        """QAbstractItemDelegate virtual
        """
        debug_print('CropDelegate.setEditorData')
        return super(CropDelegate, self).setEditorData(event, editor, index)


class SpecimenView(QListView):
    """Shows cropped specimen images either in a grid or expanded
    """
    def __init__(self, parent=None):
        super(SpecimenView, self).__init__(parent)

        # Items are shown in a grid if False.
        # A single item is shown expanded if True.
        # When more than one item is selected, view changes to grid.

        self.expanded = False

        self.setItemDelegate(CropDelegate(self))
        self.setFlow(self.LeftToRight)
        self.setWrapping(True)
        self.setResizeMode(self.Adjust)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setStyleSheet("background-color: darkgray;")

        # Activating an item toggles the expanded state
        self.activated.connect(self.toggle_expanded)

    def selectionChanged(self, selected, deselected):
        """QAbstractItemView slot
        """
        debug_print('SpecimenView.selectionChanged')

        # Grid view unless exactly one item selected
        if self.expanded and 1 != len(self.selectionModel().selectedIndexes()):
            self.show_grid()

        super(SpecimenView, self).selectionChanged(selected, deselected)

    def show_grid(self):
        debug_print('SpecimenView.show_grid')
        self.expanded = False
        self._refresh()

    def show_expanded(self):
        debug_print('SpecimenView.show_expanded')
        self.expanded = True

        # Select a single item
        sm = self.selectionModel()
        selected = sm.selectedIndexes()
        if len(selected)>1:
            sm.select(selected[0], QItemSelectionModel.ClearAndSelect)
        elif not selected:
            sm.select(self.model().index(0, 0), QItemSelectionModel.Select)

        self._refresh()

    def toggle_expanded(self, index):
        """Toggles the expanded state and selects index
        """
        self.selectionModel().select(index, QItemSelectionModel.Select)
        if self.expanded:
            self.show_grid()
        else:
            self.show_expanded()

    def _refresh(self):
        debug_print('SpecimenView.toggle_display_size')
        self.scheduleDelayedItemsLayout()
        selected = self.selectionModel().selectedIndexes()
        if selected:
            self.scrollTo(selected[0])
