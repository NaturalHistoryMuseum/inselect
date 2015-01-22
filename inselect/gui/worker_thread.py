import traceback

import numpy as np

from PySide import QtCore, QtGui

from inselect.lib.utils import debug_print

from .progress_dialog import ProgressDialog


class OperationCancelledError(Exception):
    pass


class WorkerThread(QtCore.QThread):
    """Runs a callable in its own thread and shows a progress box to the user
    while the callable runs.
    """

    # Signalled when the operation has either finished or been cancelled, and 
    # self.run() is about to exit. Arguments are user cancelled, error that
    # occurred.
    completed = QtCore.Signal(bool, str)

    # Signalled when the callable wants to set new label text - see
    # self.progress.
    new_label_text = QtCore.Signal(str)

    def __init__(self, operation, box_title, parent=None):
        super(WorkerThread, self).__init__(parent)
        self._operation = operation
        self._box_title = box_title
        self._user_cancelled = False

        self.finished.connect(self._thread_finished)
        self.new_label_text.connect(self._set_label_text)

        # A progress box to show feedback while the operation runs and to allow
        # the user to cancel.
        self._progress_box = ProgressDialog(parent)
        # Connect the progress box's cancel signal to this object's
        # user_cancelled slot.
        self._progress_box.canceled.connect(self.user_cancelled)
        self._progress_box.setWindowModality(QtCore.Qt.WindowModal)
        self._progress_box.setWindowTitle(self._box_title)
        self._progress_box.setAutoClose(False)
        self._progress_box.setAutoReset(False)
        self._progress_box.setValue(0)
        self._progress_box.setMaximum(0)
        self._progress_box.setMinimum(0)
        self._progress_box.show()

    def _thread_finished(self):
        """Slot signalled by self.finished
        """
        debug_print('WorkerThread.finished')
        assert(self.thread() == QtCore.QThread.currentThread())
        self._progress_box.hide()

    def run(self):
        try:
            debug_print('WorkerThread.run enter')
            self._operation(self.progress)

            # Call progress in order to catch pending cancel request
            self.progress()

            self.completed.emit(False, '')
            debug_print('WorkerThread.run exit')
        except OperationCancelledError:
            debug_print('WorkerThread.run: user cancelled')
            self.completed.emit(True, '')
        except Exception as e:
            debug_print('Error in WorkerThread.run')
            traceback.print_exc()
            self.completed.emit(False, u'An error occurred:\n{0}'.format(e))

    def user_cancelled(self):
        """Slot that is signalled by the cancel button on the dialog
        """
        self._user_cancelled = True

    def progress(self, label=None):
        """Raises an OperationCancelledError if self._user_cancelled has been
        set.

        Should be called regularly by the operation.
        """
        debug_print('WorkerThread.progress [{0}]'.format(label))
        if self._user_cancelled:
            debug_print('WorkerThread.progress: user cancelled')
            raise OperationCancelledError()
        elif label:
            # Only the main thread can call GUI methods. Emit a signal, the slot
            # for which will be executed in the main thread
            self.new_label_text.emit(label)

    def _set_label_text(self, label):
        """Slot signalled by self.new_label_text
        """
        debug_print("WorkerThread._set_label_text")
        assert(self.thread() == QtCore.QThread.currentThread())
        self._progress_box.setLabelText(label)
