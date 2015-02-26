import unittest

from mock import patch
from pathlib import Path

from PySide.QtGui import QMessageBox

from gui_test import GUITest


TESTDATA = Path(__file__).parent.parent / 'test_data'


class TestSelection(GUITest):
    """Tests selection
    """
    def test_select_all_none(self):
        "Select all and then none"
        w = self.window
        sm = w.view_specimen.selectionModel()

        # Open a document
        w.open_file(TESTDATA / 'test_segment.inselect')

        # Five boxes, none selected
        self.assertEqual(5, self.window.model.rowCount())
        self.assertFalse(sm.hasSelection())
        self.assertEqual(0, len(sm.selectedIndexes()))

        # Select all
        w.select_all()
        self.assertTrue(sm.hasSelection())
        self.assertEqual(5, len(sm.selectedIndexes()))

        # Select none
        w.select_none()
        self.assertFalse(sm.hasSelection())
        self.assertEqual(0, len(sm.selectedIndexes()))

    def test_next_previous(self):
        "Select the next box in the model, then the previous box"
        w = self.window
        sm = w.view_specimen.selectionModel()

        # Open a document
        w.open_file(TESTDATA / 'test_segment.inselect')

        # Select the first box
        w.select_next_prev(next=True)
        self.assertEqual(1, len(sm.selectedIndexes()))
        self.assertEqual(0, sm.selectedIndexes()[0].row())

        # Select the next box (the second)
        w.select_next_prev(next=True)
        self.assertEqual(1, len(sm.selectedIndexes()))
        self.assertEqual(1, sm.selectedIndexes()[0].row())

        # Select the previous box (the first)
        w.select_next_prev(next=False)
        self.assertEqual(1, len(sm.selectedIndexes()))
        self.assertEqual(0, sm.selectedIndexes()[0].row())

        # Select the previous box (the last)
        w.select_next_prev(next=False)
        self.assertEqual(1, len(sm.selectedIndexes()))
        self.assertEqual(4, sm.selectedIndexes()[0].row())

        # Select the next box (the first)
        w.select_next_prev(next=True)
        self.assertEqual(1, len(sm.selectedIndexes()))
        self.assertEqual(0, sm.selectedIndexes()[0].row())



if __name__=='__main__':
    unittest.main()
