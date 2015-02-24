import unittest

from functools import partial
from mock import patch
from pathlib import Path

from PySide.QtCore import QPointF
from PySide.QtGui import QMessageBox

from gui_test import GUITest

TESTDATA = Path(__file__).parent.parent / 'test_data'


# TODO LH coverage does not detect code executed within a QThread


class TestSubsegment(GUITest):
    def test_subsegment(self):
        "Subsegment a single box with three seeds points"
        w = self.window

        # Open document for subsegmentation
        w.open_document(TESTDATA / 'test_subsegment.inselect')
        self.assertEqual(1, w.model.rowCount())

        # Select a box and add sub-segmentation seed points
        # TODO LH Selecting the box and adding points like this is nasty -
        # possible to use QTest.mouseClick?
        box = w.view_graphics_item.scene.box_items().next()
        box.setSelected(True)
        seeds = [QPointF(290.0, 145.0),
                 QPointF(586.0, 276.0),
                 QPointF(272.0, 453.0)]
        for pos in seeds:
            box.append_subsegmentation_seed_point(pos)

        # Sub-segment
        self.run_async_operation(partial(w.run_plugin, 1))

        # Should have three boxes
        self.assertEqual(3, w.model.rowCount())
        self.assertTrue(w.model.modified)

        # Close the document
        with patch.object(QMessageBox, 'question', return_value=QMessageBox.No):
            self.assertTrue(self.window.close_document())

    @patch.object(QMessageBox, 'warning', return_value=QMessageBox.Yes)
    def test_no_seeds(self, mock_warning):
        "Warning message if subsegment with no seeds"
        w = self.window

        # Open document for subsegmentation
        w.open_document(TESTDATA / 'test_subsegment.inselect')
        self.assertEqual(1, w.model.rowCount())

        # Attempt subsegment
        w.run_plugin(1)

        # Document should not have changed
        self.assertEqual(1, w.model.rowCount())
        self.assertFalse(w.model.modified)

        # User should have been warned
        self.assertTrue(mock_warning.called)
        expected = ('Please select exactly one box that contains at least two '
                    'seed points')
        self.assertTrue(expected in mock_warning.call_args[0])


if __name__=='__main__':
    unittest.main()
