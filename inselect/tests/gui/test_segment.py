import unittest

from functools import partial
from mock import patch
from pathlib import Path

from PySide.QtGui import QMessageBox

from gui_test import GUITest

from inselect.gui.roles import RectRole


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

        # Load document with five boxes
        w.open_document(TESTDATA / 'test_segment.inselect')
        self.assertEqual(5, w.model.rowCount())

        # Get the rects of the existing boxes
        indexes = [w.model.index(r, 0) for r in xrange(0, w.model.rowCount())]
        expected = [w.model.data(i, RectRole) for i in indexes]

        # Segment
        self.run_async_operation(partial(w.run_plugin, 0))

        # Get the rects of the new boxes
        self.assertEqual(5, w.model.rowCount())
        indexes = [w.model.index(r, 0) for r in xrange(0, w.model.rowCount())]
        actual = [w.model.data(i, RectRole) for i in indexes]

        # Close the document
        with patch.object(QMessageBox, 'question', return_value=QMessageBox.No):
            self.assertTrue(self.window.close_document())

        # Check that bounding boxes are the same as the original boxes
        self.assertEqual(expected, actual)

        # Was the user prompted?
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
        w.open_document(TESTDATA / 'test_segment.inselect')
        w.select_all()
        w.delete_selected()

        self.run_async_operation(partial(w.run_plugin, 0))

        # Close the document
        with patch.object(QMessageBox, 'question', return_value=QMessageBox.No):
            self.assertTrue(self.window.close_document())

        self.assertFalse(mock_question.called)

# TODO LH Assert that user can cancel


if __name__=='__main__':
    unittest.main()
