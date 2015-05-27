import unittest

from functools import partial
from mock import patch

from PySide import QtCore, QtGui
from PySide.QtGui import QMessageBox

from inselect.gui.main_window import MainWindow


class GUITest(unittest.TestCase):
    """Base class for GUI tests, which require a QApplication.
    """
    @classmethod
    def setUpClass(cls):
        # Only one QApplication can be constructed
        if not QtGui.qApp:
            QtGui.QApplication([])
  

class MainWindowTest(GUITest):
    """Base class for tests that require a MainWindow.
    """
    @classmethod
    def setUp(self):
        assert not hasattr(self, 'window')
        self.window = MainWindow(QtGui.qApp)

    @classmethod
    def tearDown(self):
        self.window.close()
        delattr(self, 'window')

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

        w = self.window
        receiver = TimeoutReceiver()
        timer = receiver.startTimer(timeout_ms)
        receiver.wait_for_timeout()
        receiver.killTimer(timer)
