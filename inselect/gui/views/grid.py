from PySide import QtCore, QtGui
from PySide.QtCore import Qt

from inselect.lib.utils import debug_print
from inselect.gui.utils import contiguous
from inselect.gui.roles import RectRole, ImageRole, RotationRole

class PaintState(object):
    """Context manager that saves and restores a QPainter's state
    """
    def __init__(self, painter):
        self._p = painter

    def __enter__(self):
        self._p.save()

    def __exit__(self, exc_type, exc_value, traceback):
        self._p.restore()


class CropDelegate(QtGui.QAbstractItemDelegate):
    """Delegate that shows cropped specimen images with a grey box and
    provides editing of rotation and some flags.
    """

    BOX_RECT = QtCore.QRect(0, 0, 250, 250)
 
    # Bounding rectangle for the title
    TITLE_RECT = QtCore.QRect(QtCore.QPoint(0, 0), BOX_RECT.size())
    TITLE_RECT.adjust(5, 5, -5, -5)

    BORDER = 25   # Border around cropped image

    # Bounding rectangle of cropped image
    CROP_RECT = BOX_RECT.adjusted(BORDER, BORDER, -BORDER, -BORDER)

    # Controls
    CONTROLS_SIZE = 23
    ROTATE_COUNTERCLOCKWISE_RECT = \
        QtCore.QRect(0, 0, CONTROLS_SIZE, CONTROLS_SIZE)
    ROTATE_COUNTERCLOCKWISE_RECT.translate(
        QtCore.QPoint(0, BOX_RECT.height()-CONTROLS_SIZE))

    ROTATE_CLOCKWISE_RECT = \
        QtCore.QRect(0, 0, CONTROLS_SIZE, CONTROLS_SIZE)
    ROTATE_CLOCKWISE_RECT.translate(
         QtCore.QPoint(BOX_RECT.width()-CONTROLS_SIZE,
                       BOX_RECT.height()-CONTROLS_SIZE))

    BLACK = QtGui.QBrush(Qt.black)
    WHITE = QtGui.QBrush(Qt.white)
    GREY = QtGui.QBrush(Qt.gray)
    DARK_GREY = QtGui.QBrush(Qt.darkGray)

    def _paint_box(self, painter, option, index):
        """The grey box
        """
        selected = QtGui.QStyle.State_Selected & option.state
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
        t = QtGui.QTransform()
        t.translate(option.rect.width()/2+option.rect.left(),
                    option.rect.height()/2+option.rect.top())
        t.rotate(index.data(RotationRole))
        t.translate(-option.rect.width()/2-option.rect.left(),
                    -option.rect.height()/2-option.rect.top())

        with PaintState(painter):
            painter.setTransform(t)
            painter.drawPixmap(target_rect, index.data(ImageRole), source_rect)
            painter.drawRect(target_rect)

    def _paint_controls(self, painter, option, index):
        """The controls
        """
        with PaintState(painter):
            painter.setBrush(self.WHITE)
            painter.drawRect(self.ROTATE_CLOCKWISE_RECT.translated(option.rect.topLeft()))
            painter.drawRect(self.ROTATE_COUNTERCLOCKWISE_RECT.translated(option.rect.topLeft()))

    def paint(self, painter, option, index):
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


class GridView(QtGui.QListView):
    """Shows cropped images in a grid
    """
    def __init__(self, parent=None):
        super(GridView, self).__init__(parent)
        self.setItemDelegate(CropDelegate())
        self.setFlow(self.LeftToRight)
        self.setWrapping(True)
        self.setResizeMode(self.Adjust)
        self.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)

    def keyPressEvent(self, event):
        """QListView protected
        """
        if event.key() == Qt.Key_Delete:
            # Delete contiguous blocks of rows
            selected = sorted([i.row() for i in self.selectedIndexes()])

            # Clear selection before deleting
            self.clearSelection()

            # TODO LH We shouldn't need to remove blocks in reverse order -
            # stems from crummy GraphicsItemView
            for row, count in reversed(list(contiguous(selected))):
                self.model().removeRows(row, count)

            return True
        else:
            return super(GridView, self).keyPressEvent(event)
