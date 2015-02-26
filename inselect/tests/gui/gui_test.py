import unittest

from functools import partial
from mock import patch

from PySide import QtCore, QtGui
from PySide.QtGui import QMessageBox

from inselect.gui.app import MainWindow


class GUITest(unittest.TestCase):
    """Base class for testing the GUI. Creates QApplication and, as a class
    attribute, MainWindow.
    """

    @classmethod
    def setUpClass(cls):
        # Only one QApplication can be constructed
        if QtGui.qApp == None:
            QtGui.QApplication([])

    def setUp(self):
        assert not hasattr(self, 'window')
        self.window = MainWindow(QtGui.qApp)

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
