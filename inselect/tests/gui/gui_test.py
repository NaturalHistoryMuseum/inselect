import unittest

from functools import partial
from mock import patch

from PySide import QtCore, QtGui
from PySide.QtGui import QMessageBox

from inselect.gui.app import MainWindow


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
    def setUpClass(cls):
        "Creates a class attribute cls.window"
        super(MainWindowTest, cls).setUpClass()
        cls.window = MainWindow(QtGui.qApp)

    @classmethod
    def tearDownClass(cls):
        "Closes cls.window"
        cls.window.close()
        delattr(cls, 'window')

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
