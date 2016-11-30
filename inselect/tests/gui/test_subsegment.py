import unittest

from functools import partial
from mock import patch
from pathlib import Path

from qtpy.QtCore import QPointF, QRect
from qtpy.QtWidgets import QMessageBox

from inselect.gui.roles import MetadataRole, RectRole
from inselect.gui.sort_document_items import SortDocumentItems

from gui_test import GUITest

TESTDATA = Path(__file__).parent.parent / 'test_data'


# TODO LH coverage does not detect code executed within a QThread


class TestSubsegment(GUITest):
    def test_subsegment(self):
        "Subsegment a single box with three seeds points"
        w = self.window

        # Clear any existing plugin image
        w.plugin_image = None

        # Open document for subsegmentation
        w.open_document(path=TESTDATA / 'pinned.inselect')
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
            box.append_point_of_interest(pos)

        # Sub-segment, sorting by rows
        with patch.object(SortDocumentItems, 'by_columns', False):
            self.run_async_operation(partial(w.run_plugin, 1))

        # Should have three boxes with the same metadata
        self.assertEqual(3, w.model.rowCount())
        self.assertEqual({'Genus': 'Morganucodon'},
                         w.model.data(w.model.index(0, 0), MetadataRole))
        self.assertEqual(QRect(10, 31, 503, 278),
                         w.model.data(w.model.index(0, 0), RectRole))
        self.assertEqual({'Genus': 'Morganucodon'},
                         w.model.data(w.model.index(1, 0), MetadataRole))
        self.assertEqual(QRect(395, 157, 404, 253),
                         w.model.data(w.model.index(1, 0), RectRole))
        self.assertEqual({'Genus': 'Morganucodon'},
                         w.model.data(w.model.index(2, 0), MetadataRole))
        self.assertEqual(QRect(27, 370, 501, 209),
                         w.model.data(w.model.index(2, 0), RectRole))
        self.assertTrue(w.model.is_modified)

        # Check that the display image was created
        self.assertIsNotNone(w.plugin_image)

        # Close the document
        with patch.object(QMessageBox, 'question', return_value=QMessageBox.No):
            self.assertTrue(self.window.close_document())

        # Check that the display image was cleared when the document was
        # closed
        self.assertIsNone(w.plugin_image)

    @patch.object(QMessageBox, 'warning', return_value=QMessageBox.Yes)
    def test_subsegment_no_seeds(self, mock_warning):
        "Warning message if subsegment with no seeds"
        w = self.window

        # Open document for subsegmentation
        w.open_document(path=TESTDATA / 'pinned.inselect')
        self.assertEqual(1, w.model.rowCount())

        # Attempt subsegment
        w.run_plugin(1)

        # Document should not have changed
        self.assertEqual(1, w.model.rowCount())
        self.assertFalse(w.model.is_modified)

        # User should have been warned
        self.assertTrue(mock_warning.called)
        expected = ('Please select exactly one box that contains at least two '
                    'seed points')
        self.assertTrue(expected in mock_warning.call_args[0])


if __name__ == '__main__':
    unittest.main()
