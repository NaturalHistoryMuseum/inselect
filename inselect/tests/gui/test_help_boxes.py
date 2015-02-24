import unittest

from mock import patch

from PySide.QtGui import QMessageBox

from gui_test import GUITest

from inselect.gui.help_dialog import HelpDialog


class TestHelpBoxes(GUITest):
    """Help boxes are shown
    """
    @patch.object(HelpDialog, 'exec_', return_value=HelpDialog.Accepted)
    def test_help(self, mock_exec):
        "Help box is shown"
        HelpDialog(self.window).exec_()

    @patch.object(QMessageBox, 'about', return_value=QMessageBox.Yes)
    def test_about(self, mock_exec):
        "Help box is shown"
        self.window.about()


if __name__=='__main__':
    unittest.main()
