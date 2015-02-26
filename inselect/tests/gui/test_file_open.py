import unittest

from functools import partial
from mock import patch
from pathlib import Path

from PySide.QtGui import QMessageBox, QFileDialog

from inselect.lib.inselect_error import InselectError

from gui_test import MainWindowTest

from inselect.gui.app import MainWindow

from inselect.tests.utils import temp_directory_with_files


TESTDATA = Path(__file__).parent.parent / 'test_data'


class TestFileOpen(MainWindowTest):
    """Tests the several routes to opening a file
    """
    def _load_and_modify(self, path):
        """ Helper that opens the inselect document in path and modifies it by
        deleting all existing boxes
        """
        w = self.window
        w.open_file(path)
        self.assertLess(0, w.model.rowCount())
        w.select_all()
        w.delete_selected()
        self.assertEqual(0, w.model.rowCount())

    def test_open_doc(self):
        "Open an inselect document"
        self.window.open_file(TESTDATA / 'test_segment.inselect')
        self.assertEqual(5, self.window.model.rowCount())
        self.assertEqual('test_segment.inselect[*]', self.window.windowTitle())

    def test_open_scanned_of_doc(self):
        """Open the scanned image file of an existing inselect document - the
        inselect document should be opened
        """
        self.window.open_file(TESTDATA / 'test_segment.png')
        self.assertEqual(5, self.window.model.rowCount())
        self.assertEqual('test_segment.inselect[*]', self.window.windowTitle())

    def test_open_thumbnail_of_doc(self):
        """Open the thumbnail image file of an existing inselect document - the
        inselect document should be opened
        """
        self.window.open_file(TESTDATA / 'test_segment_thumbnail.png')
        self.assertEqual(5, self.window.model.rowCount())
        self.assertEqual('test_segment.inselect[*]', self.window.windowTitle())

    @patch.object(MainWindow, 'new_document')
    def test_new_document(self, mock_new_document):
        """Open an image file for which no inselect document exists
        """
        # open_file delegates to new_document, which runs an operation runs in a
        # worker thread - I could not think of a way to test the complete
        # operation in a single test.
        # This test checks that new_document is called as expected.
        with temp_directory_with_files(TESTDATA / 'test_segment.png') as tempdir:
            self.window.open_file(tempdir / 'test_segment.png')
            self.assertTrue(mock_new_document.called)
            self.assertEqual(tempdir / 'test_segment.png',
                             mock_new_document.call_args[0][0])

    @patch.object(QMessageBox, 'information', return_value=QMessageBox.Yes)
    def test_new_document_thread(self, mock_information):
        """Open an image file for which no inselect document exists
        """
        # open_file delegates to new_document, which runs an operation runs in a
        # worker thread - I could not think of a way to test the complete
        # operation in a single test.
        # This test checks that new_document behaves as expected.
        with temp_directory_with_files(TESTDATA / 'test_segment.png') as tempdir:
            self.run_async_operation(partial(self.window.new_document,
                                             tempdir / 'test_segment.png'))

            # New document should have been created
            self.assertTrue((TESTDATA / 'test_segment.inselect').is_file())

            # User should have been told about the new document
            self.assertTrue(mock_information.called)
            expected = u'New Inselect document [test_segment] created in [{0}]'
            expected = expected.format(tempdir)
            self.assertTrue(expected in mock_information.call_args[0])

    @patch.object(QMessageBox, 'critical', return_value=QMessageBox.Yes)
    def test_open_non_existant_image(self, mock_critical):
        "Try to open a non-existant image file"
        self.assertRaises(InselectError, self.window.open_file,
                          'I do not exist.png')

        # User should have been told about the error
        self.assertTrue(mock_critical.called)
        expected = (u"An error occurred:\n"
                    u"Image file [I do not exist.png] does not exist")
        self.assertTrue(expected in mock_critical.call_args[0])

    @patch.object(QMessageBox, 'critical', return_value=QMessageBox.Yes)
    def test_open_non_existant_inselect(self, mock_critical):
        "Try to open a non-existant inselect file"
        self.assertRaises(IOError, self.window.open_file, 'I do not exist.inselect')
        self.assertTrue(mock_critical.called)
        expected = (u"An error occurred:\n"
                    u"[Errno 2] No such file or directory: 'I do not exist.inselect'")
        self.assertTrue(expected in mock_critical.call_args[0])

    @patch.object(QMessageBox, 'critical', return_value=QMessageBox.Yes)
    def test_open_non_existant_unrecognised(self, mock_critical):
        "Try to open a non-existant file with an unrecognised extension"
        self.assertRaises(InselectError, self.window.open_file, 'I do not exist')
        self.assertTrue(mock_critical.called)
        expected = u'An error occurred:\nUnknown file type [I do not exist]'
        self.assertTrue(expected in mock_critical.call_args[0])

    @patch.object(QMessageBox, 'question', return_value=QMessageBox.No)
    def test_open_do_not_save_existing_modified(self, mock_question):
        "User chooses not to save the existing modified document"
        w = self.window

        # Open and modify a document
        self._load_and_modify(TESTDATA / 'test_segment.inselect')

        # Open another doc - user says not to save
        w.open_file(TESTDATA / 'test_subsegment.inselect')
        self.assertTrue(mock_question.called)
        expected = "Save the document before closing?"
        self.assertTrue(expected in mock_question.call_args[0])

        self.assertEqual(1, w.model.rowCount())
        self.assertEqual('test_subsegment.inselect[*]', w.windowTitle())

        # Original document should not have changed
        w.open_file(TESTDATA / 'test_segment.inselect')
        self.assertEqual(5, w.model.rowCount())
        self.assertEqual('test_segment.inselect[*]', w.windowTitle())

    @patch.object(QMessageBox, 'question', return_value=QMessageBox.Yes)
    def test_open_save_existing_modified(self, mock_question):
        "User chooses to save the existing modified document"
        w = self.window

        # Create a temporary inselect document so that it can be modified
        with temp_directory_with_files(TESTDATA / 'test_segment.inselect', 
                                       TESTDATA / 'test_segment.png') as tempdir:

            # Oopen the temp doc and modify it
            self._load_and_modify(tempdir / 'test_segment.inselect')

            # Open another doc - user says not to save
            w.open_file(TESTDATA / 'test_subsegment.inselect')
            self.assertTrue(mock_question.called)
            expected = "Save the document before closing?"
            self.assertTrue(expected in mock_question.call_args[0])

            self.assertEqual(1, w.model.rowCount())
            self.assertEqual('test_subsegment.inselect[*]', w.windowTitle())

            # Original document should have changed - it should contain no boxes
            w.open_file(tempdir / 'test_segment.inselect')
            self.assertEqual(0, w.model.rowCount())
            self.assertEqual('test_segment.inselect[*]', w.windowTitle())

    @patch.object(QMessageBox, 'question', return_value=QMessageBox.Cancel)
    def test_open_cancel_existing_modified(self, mock_question):
        """User chooses to cancel open file when the existing document has been
        modified
        """
        w = self.window

        # Open and modify a document
        self._load_and_modify(TESTDATA / 'test_segment.inselect')

        # Open another document - user says not to save
        w.open_file(TESTDATA / 'test_subsegment.inselect')
        self.assertTrue(mock_question.called)
        expected = "Save the document before closing?"
        self.assertTrue(expected in mock_question.call_args[0])

        # Assert that the open document has not changed and has not been saved
        self.assertEqual(0, w.model.rowCount())
        self.assertEqual('test_segment.inselect[*]', w.windowTitle())
        self.assertTrue(w.model.is_modified)

        # Close the document
        with patch.object(QMessageBox, 'question', return_value=QMessageBox.No):
            self.assertTrue(self.window.close_document())

    @patch.object(QFileDialog, 'getOpenFileName', return_value=(None,None))
    def test_cancel_file_choose(self, mock_gofn):
        "User cancels the 'choose a file to open' box"
        # Load and modify a document
        self._load_and_modify(TESTDATA / 'test_segment.inselect')
        w = self.window
        w.open_file(None)

        self.assertEqual(0, w.model.rowCount())
        self.assertEqual('test_segment.inselect[*]', w.windowTitle())
        self.assertTrue(w.model.is_modified)

        # Close the document
        with patch.object(QMessageBox, 'question', return_value=QMessageBox.No):
            self.assertTrue(self.window.close_document())


if __name__=='__main__':
    unittest.main()
