import unittest
from pathlib import Path

from gui_test import GUITest


TESTDATA = Path(__file__).parent.parent / 'test_data'


class TestActionState(GUITest):
    """Test the enabled state of UI actions
    """
    def _test_closed(self):
        w = self.window
        self.assertEqual('Inselect', w.windowTitle())
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
        self.assertFalse(w.plugin_actions[0].isEnabled())

        # View
        self.assertFalse(w.zoom_in_action.isEnabled())
        self.assertFalse(w.zoom_out_action.isEnabled())
        self.assertFalse(w.toogle_zoom_action.isEnabled())
        self.assertFalse(w.zoom_home_action.isEnabled())

    def _test_open(self):
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
        self.assertTrue(w.plugin_actions[0].isEnabled())

        # View
        self.assertTrue(w.zoom_in_action.isEnabled())
        self.assertTrue(w.zoom_out_action.isEnabled())
        self.assertTrue(w.toogle_zoom_action.isEnabled())
        self.assertTrue(w.zoom_home_action.isEnabled())

    def test_open_and_closed(self):
        w = self.window
        self.window.close_document()
        self._test_closed()

        self.window.open_document(TESTDATA / 'test_segment.inselect')
        self.assertEqual(5, w.model.rowCount())
        self.assertEqual('Inselect [test_segment]', self.window.windowTitle())
        self._test_open()

        self.window.close_document()
        self._test_closed()

    def test_selection_dependent(self):
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


if __name__=='__main__':
    unittest.main()
