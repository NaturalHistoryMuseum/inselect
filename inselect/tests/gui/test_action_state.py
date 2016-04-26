import unittest
from pathlib import Path

from gui_test import MainWindowTest


TESTDATA = Path(__file__).parent.parent / 'test_data'


class TestActionState(MainWindowTest):
    """Test the state of UI actions
    """
    def _test_no_document(self):
        "Enabled state for actions when no document is open"
        w = self.window
        self.assertEqual(0, w.model.rowCount())

        # File menu
        self.assertFalse(w.save_action.isEnabled())
        self.assertFalse(w.save_crops_action.isEnabled())
        self.assertFalse(w.export_csv_action.isEnabled())
        self.assertFalse(w.close_action.isEnabled())

        # Edit menu
        self.assertFalse(w.select_all_action.isEnabled())
        self.assertFalse(w.select_none_action.isEnabled())
        self.assertFalse(w.delete_action.isEnabled())
        self.assertFalse(w.next_box_action.isEnabled())
        self.assertFalse(w.previous_box_action.isEnabled())
        self.assertFalse(w.rotate_clockwise_action.isEnabled())
        self.assertFalse(w.rotate_counter_clockwise_action.isEnabled())
        self.assertTrue(w.sort_by_rows_action.isEnabled())
        self.assertTrue(w.sort_by_columns_action.isEnabled())
        self.assertFalse(w.plugin_actions[0].isEnabled())

        # View
        self.assertTrue(w.boxes_view_action.isEnabled())
        self.assertTrue(w.metadata_view_action.isEnabled())
        self.assertFalse(w.zoom_in_action.isEnabled())
        self.assertFalse(w.zoom_out_action.isEnabled())
        self.assertFalse(w.zoom_to_selection_action.isEnabled())
        self.assertFalse(w.zoom_home_action.isEnabled())

    def _test_document_open(self):
        "Enabled state for actions when a document is open"
        w = self.window

        # File menu
        self.assertTrue(w.save_action.isEnabled())
        self.assertTrue(w.save_crops_action.isEnabled())
        self.assertTrue(w.export_csv_action.isEnabled())
        self.assertTrue(w.close_action.isEnabled())

        # Edit menu
        self.assertTrue(w.select_all_action.isEnabled())
        self.assertTrue(w.select_none_action.isEnabled())
        self.assertFalse(w.delete_action.isEnabled())
        self.assertTrue(w.next_box_action.isEnabled())
        self.assertTrue(w.previous_box_action.isEnabled())
        self.assertFalse(w.rotate_clockwise_action.isEnabled())
        self.assertFalse(w.rotate_counter_clockwise_action.isEnabled())
        self.assertTrue(w.sort_by_rows_action.isEnabled())
        self.assertTrue(w.sort_by_columns_action.isEnabled())
        self.assertTrue(w.plugin_actions[0].isEnabled())

        # View
        self.assertTrue(w.boxes_view_action.isEnabled())
        self.assertTrue(w.metadata_view_action.isEnabled())
        self.assertTrue(w.zoom_in_action.isEnabled())
        self.assertTrue(w.zoom_out_action.isEnabled())
        self.assertTrue(w.zoom_to_selection_action.isEnabled())
        self.assertTrue(w.zoom_home_action.isEnabled())

    def test_open_and_closed(self):
        "Enabled state for actions as documents are opened and closed"
        w = self.window
        self.window.close_document()
        self._test_no_document()

        self.window.open_document(TESTDATA / 'test_segment.inselect')
        self.assertEqual(5, w.model.rowCount())
        self._test_document_open()

        self.window.close_document()
        self._test_no_document()

    def test_selection_dependent(self):
        "Enabled state for actions that depend upon what is selected"
        w = self.window

        w.open_document(TESTDATA / 'test_segment.inselect')

        # Select all boxes
        w.select_all()

        self.assertTrue(w.delete_action.isEnabled())
        self.assertTrue(w.rotate_clockwise_action.isEnabled())
        self.assertTrue(w.rotate_counter_clockwise_action.isEnabled())

        # Clear selection
        w.select_none()

        self.assertFalse(w.delete_action.isEnabled())
        self.assertFalse(w.rotate_clockwise_action.isEnabled())
        self.assertFalse(w.rotate_counter_clockwise_action.isEnabled())

    def test_boxes_view_active(self):
        "Checked state of view actions reflects the active view"
        w = self.window

        w.show_tab(0)
        self.assertTrue(w.boxes_view_action.isChecked())
        self.assertFalse(w.metadata_view_action.isChecked())

        w.show_tab(1)
        self.assertFalse(w.boxes_view_action.isChecked())
        self.assertTrue(w.metadata_view_action.isChecked())

        w.show_tab(0)


if __name__ == '__main__':
    unittest.main()
