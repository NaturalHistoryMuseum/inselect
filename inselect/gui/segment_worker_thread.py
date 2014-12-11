import numpy as np

from PySide import QtCore

from inselect.lib.segment import segment_edges
from inselect.lib.utils import debug_print


class OperationCancelledError(Exception):
    pass


class SegmentWorkerThread(QtCore.QThread):
    """Runs segment_edges process in a thread
    """
    results = QtCore.Signal(list, np.ndarray, bool)

    def __init__(self, image, parent=None):
        super(SegmentWorkerThread, self).__init__(parent)
        self._image = image
        self._user_cancelled = False

    def run(self):
        debug_print('SegmentWorkerThread.run enter')
        try:
            rects, display = segment_edges(self._image,
                                           window=None,
                                           resize=(5000, 5000),
                                           variance_threshold=100,
                                           size_filter=1,
                                           callback=self.progress)
            self.results.emit(rects, display, False)
        except OperationCancelledError:
            debug_print('SegmentWorkerThread.run: user cancelled')
            self.results.emit([], np.empty(0), True)
        # TODO Catch other exceptions

        debug_print('SegmentWorkerThread.run exit')

    def user_cancelled(self):
        """Slot
        """
        self._user_cancelled = True

    def progress(self):
        """Raises an OperationCancelledError if the has user pressed
        self.progress_box's cancel button.
        """
        debug_print('SegmentWorkerThread.progress')
        if self._user_cancelled:
            debug_print('SegmentWorkerThread.progress: user cancelled')
            raise OperationCancelledError()
