import unittest

from functools import partial
from mock import patch
from pathlib import Path

from qtpy.QtWidgets import QMessageBox

from .gui_test import GUITest

from inselect.gui.roles import RectRole
from inselect.gui.sort_document_items import SortDocumentItems


TESTDATA = Path(__file__).parent.parent / 'test_data'


# TODO LH coverage does not detect code executed within a QThread


class TestSegment(GUITest):
    @patch.object(QMessageBox, 'question', return_value=QMessageBox.Yes)
    def test_segment(self, mock_question):
        """Segment a document that already has boxes, making sure that the
        user is prompted and that the new boxes have the same rects as the
        existing boxes.
        """
        w = self.window

        # Clear any existing plugin image
        w.plugin_image = None

        # Load document with five boxes
        w.open_document(path=TESTDATA / 'shapes.inselect')
        self.assertEqual(5, w.model.rowCount())

        # Get the rects of the existing boxes
        indexes = [w.model.index(r, 0) for r in range(0, w.model.rowCount())]
        expected = [w.model.data(i, RectRole) for i in indexes]

        # Segment, sorting by rows
        with patch.object(SortDocumentItems, 'by_columns', False):
            self.run_async_operation(partial(w.run_plugin, 0))

        # Get the rects of the new boxes
        self.assertEqual(5, w.model.rowCount())
        indexes = [w.model.index(r, 0) for r in range(0, w.model.rowCount())]
        actual = [w.model.data(i, RectRole) for i in indexes]

        # Check that the display image was created
        self.assertIsNotNone(w.plugin_image)

        # Close the document
        with patch.object(QMessageBox, 'question', return_value=QMessageBox.No):
            self.assertTrue(self.window.close_document())

        # Check that the display image was cleared when the document was
        # closed
        self.assertIsNone(w.plugin_image)

        # Check that bounding boxes are the same as the original boxes
        self.assertEqual(expected, actual)

        # User should have been prompted
        self.assertTrue(mock_question.called)
        expected = ('Segmenting will cause all boxes and metadata to be '
                    'replaced.\n\nContinue and replace all existing '
                    'boxes and metadata')
        self.assertTrue(expected in mock_question.call_args[0])

    @patch.object(QMessageBox, 'question', return_value=QMessageBox.Yes)
    def test_segment_no_prompt(self, mock_question):
        """User is not prompted when segmenting a document with no existing
        boxes"""
        w = self.window

        # Open document and remove existing boxes
        w.open_document(path=TESTDATA / 'shapes.inselect')
        w.select_all()
        w.delete_selected()

        self.run_async_operation(partial(w.run_plugin, 0))

        # Close the document
        with patch.object(QMessageBox, 'question', return_value=QMessageBox.No):
            self.assertTrue(self.window.close_document())

        self.assertFalse(mock_question.called)

# TODO LH Assert that user can cancel


if __name__ == '__main__':
    unittest.main()
