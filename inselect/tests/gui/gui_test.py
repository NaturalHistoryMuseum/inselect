import unittest

from functools import partial
from mock import patch

from PySide import QtGui
from PySide.QtGui import QMessageBox

import inselect.settings

from inselect.gui.app import MainWindow


class GUITest(unittest.TestCase):
    """Base class for testing the GUI
    """

    @classmethod
    def setUpClass(cls):
        # Only one QApplication be constructed
        if QtGui.qApp == None:
            QtGui.QApplication([])
            inselect.settings.init()

    def setUp(self):
        assert(not hasattr(self, 'window'))
        self.window = MainWindow(QtGui.qApp)

    def tearDown(self):
        # Close open document, which might be modified
        if self.window.document:
            with patch.object(QMessageBox, 'question', return_value=QMessageBox.No):
                self.assertTrue(self.window.close_document())

        self.window.close()
        delattr(self, 'window')
