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

    # Emitted when the operation has either finished or been cancelled, and
    # self.run() is about to exit. Arguments are user cancelled, error that
    # occurred.
    completed = QtCore.Signal(bool, str)

    # Emitted when the callable wants to set a new message- see progress()
    new_message = QtCore.Signal(str)

    def __init__(self, operation, box_title, parent=None):
        super(WorkerThread, self).__init__(parent)
        self._operation = operation
        self._box_title = box_title
        self._user_cancelled = False

        self.finished.connect(self._thread_finished)
        self.new_message.connect(self._set_message)

        # The current message
        self._message = None

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
        """Slot for self.finished
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
            self.completed.emit(False, 'An error occurred:\n{0}'.format(e))

    def user_cancelled(self):
        """Slot for the cancel button on the dialog
        """
        self._user_cancelled = True

    def progress(self, message=None):
        """Raises an OperationCancelledError if self._user_cancelled has been
        set.

        Should be called regularly by the operation.
        """
        if self._user_cancelled:
            debug_print('WorkerThread.progress: user cancelled')
            raise OperationCancelledError()
        elif message != self._message:
            # Only the main thread can call GUI methods. Emit a signal, the slot
            # for which will be executed in the main thread
            debug_print('WorkerThread.progress message [{0}]'.format(message))
            self.new_message.emit(message)

    def _set_message(self, message):
        """Slot for self.new_message
        """
        debug_print("WorkerThread._set_message [{0}]".format(message))
        # Must only be called from the main thread
        assert(self.thread() == QtCore.QThread.currentThread())
        self._progress_box.setLabelText(message)
