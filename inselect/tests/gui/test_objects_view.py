import unittest

from pathlib import Path

from .gui_test import GUITest

TESTDATA = Path(__file__).parent.parent / 'test_data'


class TestObjectsView(GUITest):
    """Basic tests of the objects views. Functions test as much of the
    view's paint methods as possible by loading a document, selecting the view
    under test and showing the main window full screen.
    """
    def _test_objects_view_grid_paint(self, expanded):
        "Test painting of objects view"
        w = self.window
        # Test using barcodes.inselect because it contains bounding boxes with
        # aspect ratios both > 1 and < 1
        w.open_file(path=TESTDATA / 'barcodes.inselect')
        w.show_tab(1)
        if expanded:
            w.view_object.show_expanded()
        else:
            w.view_object.show_grid()
        w.showFullScreen()
        #self.run_event_loop()

    def test_objects_view_grid_paint(self):
        "Objects expanded view is painted"
        self._test_objects_view_grid_paint(expanded=False)

    def test_objects_view_expanded_paint(self):
        "Objects expanded view is painted"
        self._test_objects_view_grid_paint(expanded=True)

        w = self.window

        # Paint first box (taller than it is wide) and then second box (wider
        # than it is tall) selected and at all rotations
        # all rotations
        w.sort_boxes(by_columns=False)
        for iteration in range(2):
            w.select_next_prev(next=True)
            self.run_event_loop()

            # Paint all rotations
            w.rotate90(clockwise=True)
            self.run_event_loop()

            # Paint all rotations
            w.rotate90(clockwise=True)
            self.run_event_loop()

            # Paint all rotations
            w.rotate90(clockwise=True)
            self.run_event_loop()


if __name__ == '__main__':
    unittest.main()
