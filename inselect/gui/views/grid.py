from PySide.QtCore import QRect, QPoint, Qt, QCoreApplication
from PySide.QtGui import (QListView, QBrush, QStyle, QTransform, QPen,
                          QAbstractItemView, QAbstractItemDelegate,
                          QStyleOptionButton)

from inselect.lib.utils import debug_print
from inselect.gui.utils import PaintState
from inselect.gui.roles import RectRole, PixmapRole, RotationRole

class CropDelegate(QAbstractItemDelegate):
    """Delegate that shows cropped specimen images with a grey box and
    provides editing of rotation and some flags.
    """

    BOX_RECT = QRect(0, 0, 250, 250)
 
    # Bounding rectangle for the title
    TITLE_RECT = QRect(QPoint(0, 0), BOX_RECT.size())
    TITLE_RECT.adjust(5, 5, -5, -5)

    BORDER = 25   # Border around cropped image

    # Bounding rectangle of cropped image
    CROP_RECT = BOX_RECT.adjusted(BORDER, BORDER, -BORDER, -BORDER)

    # Controls
    CONTROLS_SIZE = 23
    ROTATE_COUNTERCLOCKWISE_RECT = QRect(0, 0, CONTROLS_SIZE, CONTROLS_SIZE)
    ROTATE_COUNTERCLOCKWISE_RECT.translate(QPoint(0, BOX_RECT.height()-CONTROLS_SIZE))

    ROTATE_CLOCKWISE_RECT = QRect(0, 0, CONTROLS_SIZE, CONTROLS_SIZE)
    ROTATE_CLOCKWISE_RECT.translate(QPoint(BOX_RECT.width()-CONTROLS_SIZE,
                                    BOX_RECT.height()-CONTROLS_SIZE))

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
        target_rect = self.CROP_RECT.translated(option.rect.topLeft())

        # Adjust target rect to have the same aspect ratio as the source_rect
        aspect = float(source_rect.width()) / source_rect.height()
        if aspect>1.0:
            # Image is wider than it is tall => target_rect becomes shorter
            offset = target_rect.height() - target_rect.height() / aspect
            target_rect.adjust(0, offset/2, 0, -offset/2)
        else:
            # Image is taller than it is wide => target_rect becomes narrow
            offset = target_rect.width() - target_rect.width() * aspect
            target_rect.adjust(offset/2, 0, -offset/2, 0)

        # Draw rotated
        t = QTransform()
        t.translate(option.rect.width()/2+option.rect.left(),
                    option.rect.height()/2+option.rect.top())
        t.rotate(index.data(RotationRole))
        t.translate(-option.rect.width()/2-option.rect.left(),
                    -option.rect.height()/2-option.rect.top())

        with PaintState(painter):
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
        self.setItemDelegate(CropDelegate())
        self.setFlow(self.LeftToRight)
        self.setWrapping(True)
        self.setResizeMode(self.Adjust)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setStyleSheet("background-color: darkgray;")
