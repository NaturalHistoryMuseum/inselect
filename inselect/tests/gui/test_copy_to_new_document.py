import unittest

from mock import patch
from pathlib import Path

from qtpy.QtWidgets import QFileDialog

from gui_test import GUITest
from inselect.gui.main_window import MainWindow
from inselect.tests.utils import temp_directory_with_files


TESTDATA = Path(__file__).parent.parent / 'test_data'


class TestCopyToNewDocument(GUITest):
    "Tests the 'copy to new document' operation"

    @patch.object(MainWindow, 'new_document')
    def test_copy_to_new_document(self, mock_new_document):
        "User copies boxes to a new document"
        # open_file delegates to new_document, which runs an operation runs in a
        # worker thread - I could not think of a way to test the complete
        # operation in a single test.
        # This test checks that new_document is called as expected.
        w = self.window

        w.open_file(TESTDATA / 'shapes.inselect')

        # Take a copy of the metadata
        expected_metadata = w.document.items

        with temp_directory_with_files(TESTDATA / 'shapes.png') as tempdir:
            image = tempdir / 'other_image.png'
            (tempdir / 'shapes.png').rename(image)

            retval = str(image), w.IMAGE_FILE_FILTER

            with patch.object(QFileDialog, 'getOpenFileName', return_value=retval) as mock_gofn:
                w.copy_to_new_document()
                self.assertEqual(1, mock_gofn.call_count)

            # New document should have been called with the path to the image
            self.assertTrue(mock_new_document.called)
            mock_new_document.assert_called_once_with(
                image, default_metadata_items=expected_metadata
            )

            # Orignal document should have been closed
            self.assertIsNone(self.window.document)


if __name__ == '__main__':
    unittest.main()
