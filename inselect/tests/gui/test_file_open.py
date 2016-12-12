import shutil
import unittest

from functools import partial
from mock import patch
from pathlib import Path

from qtpy.QtWidgets import QMessageBox, QFileDialog

from inselect.lib.inselect_error import InselectError
from inselect.lib.utils import make_readonly

from .gui_test import GUITest

from inselect.gui.main_window import MainWindow

from inselect.tests.utils import temp_directory_with_files


TESTDATA = Path(__file__).parent.parent / 'test_data'


class TestFileOpen(GUITest):
    """Tests the several routes to opening a file
    """
    def _load_and_modify(self, path):
        """ Helper that opens the inselect document in path and modifies it by
        deleting all existing boxes
        """
        w = self.window
        w.open_file(path=path)
        self.assertLess(0, w.model.rowCount())
        w.select_all()
        w.delete_selected()
        self.assertEqual(0, w.model.rowCount())

    def assertWindowTitleNoDocument(self):
        """Asserts that self.window.windowTitle is as expected
        """
        self.assertEqual('Inselect', self.window.windowTitle())

    def assertWindowTitleOpenDocument(self):
        """Asserts that self.window.windowTitle is as expected.
        """
        # Some OSes append ' \u2014 inselect' to the window title, so assert
        # using a regular expression rather than equality. Not possible to
        # check modified behaviour because MainWindow.modified_changed slot
        # is not called without event loop.
        self.assertRegex(self.window.windowTitle(),
                                 '^shapes\\.inselect.*')

    def test_open_doc(self):
        "Open an inselect document"
        self.window.open_file(path=TESTDATA / 'shapes.inselect')
        self.assertEqual(5, self.window.model.rowCount())
        self.assertWindowTitleOpenDocument()
        self.assertFalse(self.window.model.is_modified)

    @patch.object(QMessageBox, 'warning', return_value=QMessageBox.Ok)
    def test_open_readonly_doc(self, mock_warning):
        "User is warned when opening a read-only inselect document"
        with temp_directory_with_files(TESTDATA / 'shapes.inselect',
                                       TESTDATA / 'shapes.png',
                                       ) as tempdir:
            make_readonly(tempdir / 'shapes.inselect')
            self.window.open_file(path=tempdir / 'shapes.inselect')

            self.assertTrue(mock_warning.called)
            expected = ('The file [shapes.inselect] is read-only.\n\n'
                        'You will not be able to save any changes that you '
                        'make.')
            self.assertTrue(expected in mock_warning.call_args[0])

    def test_open_scanned_of_doc(self):
        """Open the scanned image file of an existing inselect document - the
        inselect document should be opened
        """
        self.window.open_file(path=TESTDATA / 'shapes.png')
        self.assertEqual(5, self.window.model.rowCount())
        self.assertFalse(self.window.model.is_modified)
        self.assertWindowTitleOpenDocument()

    def test_open_thumbnail_of_doc(self):
        """Open the thumbnail image file of an existing inselect document - the
        inselect document should be opened
        """
        with temp_directory_with_files(TESTDATA / 'shapes.inselect',
                                       TESTDATA / 'shapes.png',
                                       ) as tempdir:
            thumbnail = tempdir / 'shapes_thumbnail.jpg'

            # The test document contains no thumbnail file - create one now
            shutil.copy(str(tempdir / 'shapes.png'), str(thumbnail))

            self.window.open_file(path=thumbnail)
            self.assertEqual(5, self.window.model.rowCount())
            self.assertFalse(self.window.model.is_modified)
            self.assertWindowTitleOpenDocument()

    @patch.object(MainWindow, 'new_document')
    def test_new_document(self, mock_new_document):
        """Open an image file for which no inselect document exists
        """
        # open_file delegates to new_document, which runs an operation runs in a
        # worker thread - I could not think of a way to test the complete
        # operation in a single test.
        # This test checks that new_document is called as expected.
        with temp_directory_with_files() as tempdir:
            # Check that open_file accepts images with a file extension that is
            # not all lower case.
            shutil.copy(str(TESTDATA / 'shapes.png'),
                        str(tempdir / 'shapes.Png'))
            self.window.open_file(path=tempdir / 'shapes.Png')
            mock_new_document.assert_called_once_with(tempdir / 'shapes.Png')

    @patch.object(QMessageBox, 'information', return_value=QMessageBox.Yes)
    def test_new_document_thread(self, mock_information):
        """Open an image file for which no inselect document exists
        """
        # open_file delegates to new_document, which runs an operation runs in a
        # worker thread - I could not think of a way to test the complete
        # operation in a single test.
        # This test checks that new_document behaves as expected.
        with temp_directory_with_files(TESTDATA / 'shapes.png') as tempdir:
            self.run_async_operation(partial(self.window.new_document,
                                             tempdir / 'shapes.png'))

            # New document should have been created
            self.assertTrue((TESTDATA / 'shapes.inselect').is_file())

            # User should have been told about the new document
            self.assertTrue(mock_information.called)
            expected = 'New Inselect document [shapes] created in [{0}]'
            expected = expected.format(tempdir)
            self.assertTrue(expected in mock_information.call_args[0])

            self.assertFalse(self.window.model.is_modified)
            self.assertWindowTitleOpenDocument()

    def test_open_non_existant_image(self):
        "Try to open a non-existant image file"
        self.assertRaises(InselectError, self.window.open_file,
                          path='I do not exist.png')
        self.assertFalse(self.window.model.is_modified)
        self.assertWindowTitleNoDocument()

    def test_open_non_existant_inselect(self):
        "Try to open a non-existant inselect file"
        self.assertRaises(IOError, self.window.open_file, path='I do not exist.inselect')
        self.assertFalse(self.window.model.is_modified)
        self.assertWindowTitleNoDocument()

    def test_open_non_existant_unrecognised(self):
        "Try to open a non-existant file with an unrecognised extension"
        self.assertRaises(InselectError, self.window.open_file, path='I do not exist')
        self.assertFalse(self.window.model.is_modified)
        self.assertWindowTitleNoDocument()

    @patch.object(QMessageBox, 'question', return_value=QMessageBox.No)
    def test_open_do_not_save_existing_modified(self, mock_question):
        "User chooses not to save the existing modified document"
        w = self.window

        # Open and modify a document
        self._load_and_modify(TESTDATA / 'shapes.inselect')

        # Open another doc - user says not to save
        w.open_file(path=TESTDATA / 'pinned.inselect')
        self.assertTrue(mock_question.called)
        expected = "Save the document before closing?"
        self.assertTrue(expected in mock_question.call_args[0])

        self.assertEqual(1, w.model.rowCount())

        # Original document should not have changed
        w.open_file(path=TESTDATA / 'shapes.inselect')
        self.assertEqual(5, w.model.rowCount())
        self.assertFalse(w.model.is_modified)
        self.assertWindowTitleOpenDocument()

    @patch.object(QMessageBox, 'question', return_value=QMessageBox.Yes)
    def test_open_save_existing_modified(self, mock_question):
        "User chooses to save the existing modified document"
        w = self.window

        # Create a temporary inselect document so that it can be modified
        with temp_directory_with_files(TESTDATA / 'shapes.inselect',
                                       TESTDATA / 'shapes.png') as tempdir:

            # Oopen the temp doc and modify it
            self._load_and_modify(tempdir / 'shapes.inselect')

            # Open another doc - user says not to save
            w.open_file(path=TESTDATA / 'pinned.inselect')
            self.assertTrue(mock_question.called)
            expected = "Save the document before closing?"
            self.assertTrue(expected in mock_question.call_args[0])

            # Original document should have changed - it should contain no boxes
            w.open_file(path=tempdir / 'shapes.inselect')
            self.assertEqual(0, w.model.rowCount())
            self.assertFalse(w.model.is_modified)
            self.assertWindowTitleOpenDocument()

    @patch.object(QMessageBox, 'question', return_value=QMessageBox.Cancel)
    def test_open_cancel_existing_modified(self, mock_question):
        """User chooses to cancel open file when the existing document has been
        modified
        """
        w = self.window

        # Open and modify a document
        self._load_and_modify(TESTDATA / 'shapes.inselect')

        # Open another document - user says not to save
        w.open_file(path=TESTDATA / 'pinned.inselect')

        self.assertTrue(mock_question.called)
        expected = "Save the document before closing?"
        self.assertTrue(expected in mock_question.call_args[0])

        # Assert that the open document has not changed and has not been saved
        self.assertEqual(0, w.model.rowCount())
        self.assertTrue(self.window.model.is_modified)
        self.assertWindowTitleOpenDocument()

        # Clean up by closing the document
        with patch.object(QMessageBox, 'question', return_value=QMessageBox.No):
            self.assertTrue(self.window.close_document())

    @patch.object(QFileDialog, 'getOpenFileName', return_value=(None, None))
    def test_cancel_file_choose(self, mock_gofn):
        "User cancels the 'choose a file to open' box"
        w = self.window

        # Open a file
        w.open_file(path=None)

        self.assertEqual(1, mock_gofn.call_count)

        # No document should be open
        self.assertEqual(0, w.model.rowCount())
        self.assertFalse(w.model.is_modified)
        self.assertWindowTitleNoDocument()

    @patch.object(QMessageBox, 'question', return_value=QMessageBox.Yes)
    def test_reopen_replace_modified(self, mock_question):
        "User chooses to reopen a document that is already open and modified"
        w = self.window

        # Open and modify a document
        self._load_and_modify(TESTDATA / 'shapes.inselect')

        # Open the same document again
        w.open_file(path=TESTDATA / 'shapes.inselect')

        self.assertTrue(mock_question.called)
        self.assertTrue('Discard changes?' in mock_question.call_args[0])

        # Document should have been reopened
        self.assertEqual(5, w.model.rowCount())
        self.assertFalse(w.model.is_modified)
        self.assertWindowTitleOpenDocument()

    @patch.object(QMessageBox, 'question', return_value=QMessageBox.No)
    def test_reopen_do_notreplace_modified(self, mock_question):
        "User chooses not to reopen a document that is already open and modified"
        w = self.window

        # Open and modify a document
        self._load_and_modify(TESTDATA / 'shapes.inselect')

        # Open the same document again
        w.open_file(path=TESTDATA / 'shapes.inselect')

        self.assertTrue(mock_question.called)
        self.assertTrue('Discard changes?' in mock_question.call_args[0])

        # Document should not have been reopened
        self.assertEqual(0, w.model.rowCount())
        self.assertTrue(w.model.is_modified)
        self.assertWindowTitleOpenDocument()

        # Clean up by closing the document
        with patch.object(QMessageBox, 'question', return_value=QMessageBox.No):
            self.assertTrue(self.window.close_document())

    @patch.object(QMessageBox, 'information')
    def test_reopen(self, mock_information):
        "User tries to reopen a document that is already open and not modified"
        w = self.window

        # Open a document again
        w.open_file(path=TESTDATA / 'shapes.inselect')

        # Open the document again
        w.open_file(path=TESTDATA / 'shapes.inselect')

        self.assertTrue(mock_information.called)
        self.assertTrue('Document already open' in mock_information.call_args[0])

        self.assertFalse(w.model.is_modified)
        self.assertWindowTitleOpenDocument()


if __name__ == '__main__':
    unittest.main()
