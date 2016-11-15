import unittest

from mock import patch

from qtpy.QtWidgets import QDialog, QMessageBox

from inselect.gui import shortcuts_help

from gui_test import GUITest


class TestHelpBoxes(GUITest):
    """Help boxes are shown
    """
    @patch.object(QMessageBox, 'about', return_value=QMessageBox.Yes)
    def test_about(self, mock_about):
        "Help box is shown"
        self.window.about()
        self.assertEqual(1, mock_about.call_count)

    @patch.object(QDialog, 'exec_', return_value=QMessageBox.Ok)
    def test_show_shortcuts(self, mock_exec):
        self.window.show_shortcuts()
        self.assertEqual(1, mock_exec.call_count)

    @patch.object(shortcuts_help, '_show_shortcuts_at_startup', return_value=True)
    @patch.object(QDialog, 'exec_', return_value=QMessageBox.Ok)
    def test_show_shortcuts_post_startup(self, mock_exec, mock_show):
        self.window.show_shortcuts_post_startup()
        mock_exec.assert_called_once_with()
        mock_show.assert_called_with()

    @patch.object(shortcuts_help, '_show_shortcuts_at_startup', return_value=False)
    @patch.object(QDialog, 'exec_', return_value=QMessageBox.Ok)
    def test_do_not_show_shortcuts_post_startup(self, mock_exec, mock_show):
        self.window.show_shortcuts_post_startup()
        mock_exec.assert_not_called()
        mock_show.assert_called_with()


if __name__ == '__main__':
    unittest.main()
