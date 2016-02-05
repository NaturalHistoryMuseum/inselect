import unittest

from mock import patch
from pathlib import Path

from PySide.QtCore import QSettings
from PySide.QtGui import QFileDialog

from gui_test import MainWindowTest

from inselect.gui.user_template_choice import user_template_choice

TESTDATA = Path(__file__).parent.parent / 'test_data'


class TestUserTemplateChoice(MainWindowTest):
    """Test the template choice
    """

    @patch.object(QSettings, 'setValue')
    def test_select_default(self, mock_setvalue):
        "User chooses the default template"

        # Set a non-default template before testing the default_user_template
        # method
        t = user_template_choice()
        t.load(TESTDATA / 'test.inselect_template')
        self.assertEqual('Test user template', t.current.name)

        self.window.default_user_template()

        self.assertEqual('Simple Darwin Core terms', user_template_choice().current.name)
        mock_setvalue.assert_called_with('user_template_path', '')

    @patch.object(QSettings, 'setValue')
    def test_chooses_template(self, mock_setvalue):
        "User chooses a template"

        w = self.window

        # Select default template before testing the choose_user_template method
        w.default_user_template()

        path = TESTDATA / 'test.inselect_template'
        retval = str(path), w.TEMPLATE_FILE_FILTER
        with patch.object(QFileDialog, 'getOpenFileName', return_value=retval) as mock_gofn:
            w.choose_user_template()
            self.assertEqual(1, mock_gofn.call_count)

        self.assertEqual('Test user template', user_template_choice().current.name)
        mock_setvalue.assert_any_call('user_template_path', str(path))
        mock_setvalue.assert_any_call('user_template_last_directory', str(path.parent))

    @patch.object(QFileDialog, 'getOpenFileName', return_value=(None, None))
    def test_cancels_choose_template(self, mock_gofn):
        "User cancels the 'choose template' box"

        w = self.window

        # Select default template before testing the choose_user_template method
        w.default_user_template()

        w.choose_user_template()

        self.assertEqual('Simple Darwin Core terms', user_template_choice().current.name)
        self.assertEqual(1, mock_gofn.call_count)


if __name__ == '__main__':
    unittest.main()
