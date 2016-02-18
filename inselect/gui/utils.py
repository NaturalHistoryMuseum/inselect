from contextlib import contextmanager
from functools import wraps
from itertools import groupby

import cv2
import numpy as np

from PySide import QtGui
from PySide.QtGui import QItemSelection, QItemSelectionModel


def qimage_of_bgr(bgr):
    """ A QtGui.QImage representation of a BGR numpy array
    """
    bgr = cv2.cvtColor(bgr.astype('uint8'), cv2.COLOR_BGR2RGB)
    bgr = np.ascontiguousarray(bgr)
    qt_image = QtGui.QImage(bgr.data,
                            bgr.shape[1], bgr.shape[0],
                            bgr.strides[0], QtGui.QImage.Format_RGB888)

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
    for k, g in groupby(enumerate(values), lambda (i, x): i - x):
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


def report_to_user(f):
    """Decorator that reports exceptions to the user
    """
    @wraps(f)
    def wrapper(self, *args, **kwargs):
        try:
            return f(self, *args, **kwargs)
        except Exception as e:
            parent = self if isinstance(self, QtGui.QWidget) else None
            QtGui.QMessageBox.critical(parent, u'An error occurred',
                                       u'An error occurred:\n{0}'.format(e))
            raise
    return wrapper


def relayout_widget(widget, new_layout):
    """Replaces widget's existing layout with new_layout
    """
    # http://stackoverflow.com/a/10439207/1773758

    # Reparent the old layout to a temporary widget
    old_layout = widget.layout()
    QtGui.QWidget().setLayout(old_layout)
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
