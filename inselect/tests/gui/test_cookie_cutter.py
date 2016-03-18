import unittest

from functools import partial
from mock import patch
from pathlib import Path

from PySide.QtCore import QSettings
from PySide.QtGui import QFileDialog, QMessageBox

from gui_test import MainWindowTest

from inselect.lib.document import InselectDocument
from inselect.lib.cookie_cutter import CookieCutter
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
        self.assertEqual(
            '2x2 (4 boxes)',
            cookie_cutter_choice().current.name
        )

        self.window.cookie_cutter_widget.clear()

        self.assertEqual(None, cookie_cutter_choice().current)
        mock_setvalue.assert_called_with(cookie_cutter_choice().PATH_KEY, '')

    @patch.object(QSettings, 'setValue')
    def test_chooses_cookie_cutter(self, mock_setvalue):
        "User chooses cookie cutter"

        w = self.window
        w.cookie_cutter_widget.clear()

        path = TESTDATA / '2x2.inselect_cookie_cutter'
        retval = str(path), w.cookie_cutter_widget.FILE_FILTER
        with patch.object(QFileDialog, 'getOpenFileName', return_value=retval) as mock_gofn:
            w.cookie_cutter_widget.choose()
            self.assertEqual(1, mock_gofn.call_count)

        self.assertEqual(
            '2x2 (4 boxes)',
            cookie_cutter_choice().current.name
        )
        mock_setvalue.assert_any_call(cookie_cutter_choice().PATH_KEY, str(path))
        mock_setvalue.assert_any_call(
            cookie_cutter_choice().DIRECTORY_KEY,
            str(path.parent)
        )

    @patch.object(QFileDialog, 'getOpenFileName', return_value=(None, None))
    def test_cancels_choose_cookie_cutter(self, mock_gofn):
        "User cancels the 'choose cookie cutter' box"

        w = self.window
        w.cookie_cutter_widget.clear()
        w.cookie_cutter_widget.choose()
        self.assertEqual(None, cookie_cutter_choice().current)
        self.assertEqual(1, mock_gofn.call_count)

    @patch.object(QSettings, 'setValue')
    def test_save_to_cookie_cutter(self, mock_setvalue):
        "Create a new cookie cutter"
        w = self.window
        w.open_document(TESTDATA / 'test_segment.inselect')

        with temp_directory_with_files() as tempdir:
            path = tempdir / 'My new cookie cutter{0}'.format(
                CookieCutter.EXTENSION
            )
            retval = str(path), w.cookie_cutter_widget.FILE_FILTER
            with patch.object(QFileDialog, 'getSaveFileName', return_value=retval):
                w.save_to_cookie_cutter()

            cookie_cutter = CookieCutter.load(path)

        # The new cookie cutter should have been created with 5 boxes
        self.assertEqual(5, len(cookie_cutter.document_items))
        self.assertEqual(
            'My new cookie cutter (5 boxes)',
            cookie_cutter_choice().current.name
        )

    @patch.object(QSettings, 'setValue')
    def test_new_document(self, mock_setvalue):
        "Create a new document with cookie cutter applied"
        w = self.window
        w.cookie_cutter_widget.clear()

        path = TESTDATA / '2x2.inselect_cookie_cutter'
        retval = str(path), w.cookie_cutter_widget.FILE_FILTER
        with patch.object(QFileDialog, 'getOpenFileName', return_value=retval) as mock_gofn:
            w.cookie_cutter_widget.choose()
            self.assertEqual(1, mock_gofn.call_count)

        with temp_directory_with_files(TESTDATA / 'test_segment.png') as tempdir, \
                patch.object(QMessageBox, 'information', return_value=QMessageBox.Yes) as mock_information:
            self.run_async_operation(partial(w.new_document,
                                             tempdir / 'test_segment.png'))
            self.assertEqual(1, mock_information.call_count)
            doc = InselectDocument.load(tempdir / 'test_segment.inselect')

        # The new document should have been created with four boxes
        self.assertEqual(4, w.model.rowCount())
        self.assertEqual(4, len(doc.items))

    @patch.object(QSettings, 'setValue')
    def test_apply_cookie_cutter(self, mock_setvalue):
        "Applies the cookie cutter to the open document"
        w = self.window
        w.open_document(TESTDATA / 'test_segment.inselect')

        # Document has 5 boxes
        self.assertEqual(5, w.model.rowCount())

        path = TESTDATA / '2x2.inselect_cookie_cutter'
        retval = str(path), w.cookie_cutter_widget.FILE_FILTER
        with patch.object(QFileDialog, 'getOpenFileName', return_value=retval):
            w.cookie_cutter_widget.choose()

        with patch.object(QMessageBox, 'question', return_value=QMessageBox.Yes) as mock_question:
            w.apply_cookie_cutter()
            # User should have been prompted to replace existing boxes
            self.assertEqual(1, mock_question.call_count)

        # Document should now have the 4 boxes from the cookie cutter
        self.assertEqual(4, w.model.rowCount())

        # Clean up by closing the document
        with patch.object(QMessageBox, 'question', return_value=QMessageBox.No):
            self.assertTrue(w.close_document())


if __name__ == '__main__':
    unittest.main()
