import platform
import subprocess
import sys
import traceback

from contextlib import contextmanager
from functools import wraps
from io import StringIO
from itertools import groupby

import sip

from PyQt5.QtCore import Qt, QItemSelection, QItemSelectionModel
from PyQt5.QtGui import QColor, QIcon, QImage, QPainter, QPixmap
from PyQt5.QtWidgets import QFrame, QLabel, QMessageBox, QWidget

from . import copy_box
from functools import reduce

# Warning: lazy load of cv2 and numpy via local imports

# Nasty hacks to get HTML links inside QLabels to appear in grey.
HTML_LINK_STYLE = """<style type=text/css>
   a:link {{ color: #dddddd; text-decoration: underline;}}
</style>
"""

HTML_LINK_TEMPLATE = """<html><head>{0}</head><body>
    {{0}}
</body></html>
""".format(HTML_LINK_STYLE)


def load_icon(path):
    """Returns a QIcon with the image at path as the Normal state and the image
    recoloured as the Disabled state.
    """

    pixmap = QPixmap(path)
    icon = QIcon()
    icon.addPixmap(pixmap)

    # Create disabled
    mask = pixmap.createMaskFromColor(QColor(0xff, 0xff, 0xff), Qt.MaskOutColor)
    p = QPainter(pixmap)
    p.setPen(QColor(0xaa, 0xaa, 0xaa))
    p.drawPixmap(pixmap.rect(), mask, mask.rect())
    p.end()

    icon.addPixmap(pixmap, QIcon.Disabled)

    return icon


def qimage_of_bgr(bgr):
    """ A QImage representation of a BGR numpy array
    """
    import cv2
    import numpy as np

    bgr = cv2.cvtColor(bgr.astype('uint8'), cv2.COLOR_BGR2RGB)
    bgr = np.ascontiguousarray(bgr)
    qt_image = QImage(
        bgr.data, bgr.shape[1], bgr.shape[0], bgr.strides[0],
        QImage.Format_RGB888
    )

    if qt_image.isNull():
        raise ValueError('Unable to create QImage')
    else:
        # QImage does not take a deep copy of np_arr.data so hold a reference
        # to it
        assert(not hasattr(qt_image, 'bgr_array'))
        qt_image.bgr_array = bgr
        return qt_image


def unite_rects(rects):
    """Returns united rect
    """
    return reduce(lambda x, y: x.united(y), rects)


def contiguous(values):
    """yields tuples (value, count) of contiguous blocks of integers in values

    >>> for value, count in contiguous([0, 15, 16, 17, 18, 22, 25, 26, 27, 28]):
        print(value, count)
    (0, 1)
    (15, 4)
    (22, 1)
    (25, 4)
    """
    # Taken from http://stackoverflow.com/a/2361991
    for k, g in groupby(enumerate(values), lambda i_x: i_x[0] - i_x[1]):
        g = list(g)
        lower, upper = g[0][1], g[-1][1]
        count = upper - lower + 1
        yield lower, count


@contextmanager
def painter_state(painter):
    """A context manager that saves and restores a QtGui.QPainter's state
    """
    painter.save()
    try:
        yield
    finally:
        painter.restore()


def report_exception_to_user(type, value, tb):
    "Shows the exception and traceback in a dialog"
    if False:
        # TODO Print if debug printing is enabled
        traceback.print_tb(tb)
        print(type, value)
    try:
        details = StringIO()
        traceback.print_tb(tb, file=details)
        copy_box.show_copy_details_box(
            icon=QMessageBox.Critical,
            title='An error occurred',
            text='An error occurred:\n{0}'.format(value),
            details='{0}\n{1}: {2}'.format(
                details.getvalue(), type.__name__, value
            )
        )
    except:
        # Wah! Exception showing the details box.
        QMessageBox.critical(
            None, 'An error occurred', 'An error occurred:\n{0}'.format(value)
        )


def relayout_widget(widget, new_layout):
    """Replaces widget's existing layout with new_layout
    """
    # http://stackoverflow.com/a/10439207/1773758

    # Reparent the old layout to a temporary widget
    if not sip.isdeleted(widget):
        old_layout = widget.layout()
        if old_layout:
            # Reparent the old layout to a temporary widget
            QWidget().setLayout(old_layout)
            del old_layout

        widget.setLayout(new_layout)


def update_selection_model(model, sm, new_selection):
    """Updates the selection model with new_selection
    """
    current = set(i.row() for i in sm.selectedIndexes())
    new_selection = set(new_selection)

    # Select contiguous blocks
    for row, count in contiguous(sorted(new_selection.difference(current))):
        top_left = model.index(row, 0)
        bottom_right = model.index(row + count - 1, 0)
        sm.select(QItemSelection(top_left, bottom_right),
                  QItemSelectionModel.Select)

    # Deselect contiguous blocks
    for row, count in contiguous(sorted(current.difference(new_selection))):
        top_left = model.index(row, 0)
        bottom_right = model.index(row + count - 1, 0)
        sm.select(QItemSelection(top_left, bottom_right),
                  QItemSelectionModel.Deselect)

    if new_selection:
        # Set an arbitrary row as the current index
        sm.setCurrentIndex(model.index(new_selection.pop(), 0),
                           QItemSelectionModel.Current)


class HorizontalLine(QFrame):
    """A horizontal line
    """
    def __init__(self, parent=None):
        super(HorizontalLine, self).__init__(parent)
        self.setFrameShape(QFrame.HLine)


class VerticalLine(QFrame):
    """A vertical line
    """
    def __init__(self, parent=None):
        super(VerticalLine, self).__init__(parent)
        self.setFrameShape(QFrame.VLine)


class BoldLabel(QLabel):
    """A label in a bold font
    """
    pass


def reveal_path(path):
    """Shows path in Finder (on Mac) or in Explorer (on Windows)
    """
    # http://stackoverflow.com/a/3546503
    path = path.resolve()
    if sys.platform.startswith("win"):
        res = subprocess.call("explorer.exe /select,{0}".format(path))
        if 1 != res:
            raise ValueError('Unexpected exit code [{0}]'.format(res))
    elif 'Darwin' == platform.system():
        reveal = 'tell application "Finder" to reveal POSIX file "{0}"'
        activate = 'tell application "Finder" to activate "{0}"'
        args = ['/usr/bin/osascript', '-e']
        subprocess.check_call(args + [reveal.format(path)])
        subprocess.check_call(args + [activate.format(path)])
    else:
        # What to do on Linux?
        pass
