import unittest

from itertools import repeat
from mock import patch
from pathlib import Path

from PySide.QtCore import QSettings

from gui_test import MainWindowTest

from inselect.gui.user_template_choice import user_template_choice

TESTDATA = Path(__file__).parent.parent / 'test_data'


class TestUserTemplateChoice(MainWindowTest):
    """Test the template choice
    """
    @patch.object(QSettings, 'setValue')
    def test_select_default(self, mock_value):
        "User chooses the default template"
        t = user_template_choice()
        t.select_default()
        self.assertEqual('Simple Darwin Core terms', t.current.name)
        self.assertEqual('Simple Darwin Core terms',
                         self.window.view_metadata._template_label.text())  

    @patch.object(QSettings, 'setValue')
    def test_select_non_default(self, mock_value):
        "User chooses a non-default template"
        t = user_template_choice()
        t.load(TESTDATA / 'test.inselect_template')
        self.assertEqual('Test user template', t.current.name)
        self.assertEqual('Test user template',
                         self.window.view_metadata._template_label.text())  

if __name__=='__main__':
    unittest.main()
