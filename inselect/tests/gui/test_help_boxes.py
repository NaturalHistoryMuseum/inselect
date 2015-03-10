import unittest

from mock import patch

from PySide.QtGui import QMessageBox, QDialog

from gui_test import MainWindowTest


class TestHelpBoxes(MainWindowTest):
    """Help boxes are shown
    """
    @patch.object(QMessageBox, 'about', return_value=QMessageBox.Yes)
    def test_about(self, mock_exec):
        "Help box is shown"
        self.window.about()


if __name__=='__main__':
    unittest.main()
