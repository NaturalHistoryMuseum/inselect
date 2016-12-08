import unittest

from mock import MagicMock, patch

from qtpy import QtCore, QtWidgets
from qtpy.QtWidgets import QMessageBox

from inselect.gui import shortcuts_help
from inselect.gui.app import qapplication
from inselect.gui.main_window import MainWindow


WINDOW = None

class GUITest(unittest.TestCase):
    """Base class for GUI tests, which require a MainWindow.

    Ensures that QtGui.qApp exists. Creates an instance of MainWindow in
    `cls.window`.

    Silently closes the open document (if any), discarding any changes, after
    each test completes.
    """
    @classmethod
    def setUpClass(cls):
        global WINDOW
        if not WINDOW:
            # A single window shared by all tests and destroyed when the process
            # exits
            WINDOW = MainWindow(qapplication())

        cls.window = WINDOW

        # Crude way of ensuring that the shortcuts help box is not shown at
        # startup
        shortcuts_help._show_shortcuts_at_startup = MagicMock(return_value=False)

    def tearDown(self):
        # Clean up by closing the document
        with patch.object(QMessageBox, 'question', return_value=QMessageBox.No):
            self.assertTrue(self.window.close_document())

    def run_async_operation(self, operation):
        """Runs an async operation in self.window's worker thread and waits for
        it to complete.
        """
        # Taken from SO thread http://stackoverflow.com/a/9712870

        # TODO LH coverage does not detect code executed within a QThread

        class SignalReceiver(QtCore.QObject):
            def __init__(self):
                super(self.__class__, self).__init__()
                self.eventLoop = QtCore.QEventLoop(self)

            def completed(self, user_cancelled, error_message):
                self.eventLoop.exit()

            def wait_for_input(self):
                self.eventLoop.exec_()

        w = self.window
        operation()
        receiver = SignalReceiver()
        w.running_operation[-1].completed.connect(receiver.completed)
        w.running_operation[-1].wait()
        receiver.wait_for_input()

    def run_event_loop(self, timeout_ms=100):
        """Runs the main window's event loop until timeout_ms have elapsed
        """
        class TimeoutReceiver(QtCore.QObject):
            def __init__(self):
                super(self.__class__, self).__init__()
                self.eventLoop = QtCore.QEventLoop(self)

            def timerEvent(self, event):
                self.eventLoop.exit()

            def wait_for_timeout(self):
                self.eventLoop.exec_()

        receiver = TimeoutReceiver()
        timer = receiver.startTimer(timeout_ms)
        receiver.wait_for_timeout()
        receiver.killTimer(timer)
