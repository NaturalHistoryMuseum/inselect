import unittest

from functools import partial
from mock import patch
from pathlib import Path

from PySide.QtCore import QSettings
from PySide.QtGui import QFileDialog, QMessageBox

from gui_test import MainWindowTest

from inselect.lib.document import InselectDocument
from inselect.gui.cookie_cutter_choice import cookie_cutter_choice
from inselect.tests.utils import temp_directory_with_files

TESTDATA = Path(__file__).parent.parent / 'test_data'


class TestCookieCutterChoice(MainWindowTest):
    """Test the choices of initial boxes file
    """

    @patch.object(QSettings, 'setValue')
    def test_select_none(self, mock_setvalue):
        "User chooses to have no cookie cutter"

        cookie_cutter_choice().load(TESTDATA / '2x2.inselect_cookie_cutter')
        self.assertEqual('2x2', cookie_cutter_choice().current.name)

        self.window.clear_cookie_cutter()

        self.assertEqual(None, cookie_cutter_choice().current)
        mock_setvalue.assert_called_with('cookie_cutter_path', '')

    @patch.object(QSettings, 'setValue')
    def test_chooses_cookie_cutter(self, mock_setvalue):
        "User chooses cookie cutter"

        w = self.window
        w.clear_cookie_cutter()

        path = TESTDATA / '2x2.inselect_cookie_cutter'
        retval = str(path), w.cookie_cutter_FILE_FILTER
        with patch.object(QFileDialog, 'getOpenFileName', return_value=retval) as mock_gofn:
            w.choose_cookie_cutter()
            self.assertEqual(1, mock_gofn.call_count)

        self.assertEqual('2x2', cookie_cutter_choice().current.name)
        mock_setvalue.assert_any_call('cookie_cutter_path', str(path))
        mock_setvalue.assert_any_call('cookie_cutter_last_directory', str(path.parent))

    @patch.object(QFileDialog, 'getOpenFileName', return_value=(None, None))
    def test_cancels_choose_cookie_cutter(self, mock_gofn):
        "User cancels the 'choose cookie cutter' box"

        w = self.window
        w.clear_cookie_cutter()
        w.choose_cookie_cutter()
        self.assertEqual(None, cookie_cutter_choice().current)
        self.assertEqual(1, mock_gofn.call_count)

    @patch.object(QMessageBox, 'information', return_value=QMessageBox.Yes)
    def test_new_document(self, mock_information):
        "Create a new document with cookie cutter applied"
        w = self.window
        w.clear_cookie_cutter()

        path = TESTDATA / '2x2.inselect_cookie_cutter'
        retval = str(path), w.cookie_cutter_FILE_FILTER
        with patch.object(QFileDialog, 'getOpenFileName', return_value=retval):
            w.choose_cookie_cutter()

        with temp_directory_with_files(TESTDATA / 'test_segment.png') as tempdir:
            self.run_async_operation(partial(self.window.new_document,
                                             tempdir / 'test_segment.png'))
            doc = InselectDocument.load(tempdir / 'test_segment.inselect')

        # The new document should have been created with four boxes
        self.assertEqual(4, w.model.rowCount())
        self.assertEqual(4, len(doc.items))


if __name__ == '__main__':
    unittest.main()
