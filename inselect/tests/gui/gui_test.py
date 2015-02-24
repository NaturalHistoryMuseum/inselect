import unittest

from functools import partial
from mock import patch

from PySide import QtGui
from PySide.QtGui import QMessageBox

from inselect.gui.app import MainWindow


class GUITest(unittest.TestCase):
    """Base class for testing the GUI.
    """

    @classmethod
    def setUpClass(cls):
        # Only one QApplication be constructed
        if QtGui.qApp == None:
            QtGui.QApplication([])
        cls.window = MainWindow(QtGui.qApp)

    @classmethod
    def tearDownClass(cls):
        cls.window.close()
        delattr(cls, 'window')
