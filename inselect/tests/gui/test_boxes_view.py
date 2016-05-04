import unittest

from itertools import repeat
from pathlib import Path

from gui_test import MainWindowTest

TESTDATA = Path(__file__).parent.parent / 'test_data'


class TestBoxesView(MainWindowTest):
    """Activities in boxes view
    """
    def setUp(self):
        super(TestBoxesView, self).setUp()
        self.window.open_file(TESTDATA / 'test_segment.inselect')

    def tearDown(self):
        self.window.close()
        super(TestBoxesView, self).tearDown()

    def test_zoom_in(self):
        "User zooms in"
        w = self.window

        initial = w.boxes_view.absolute_zoom
        w.zoom_in()

        final = w.boxes_view.absolute_zoom
        self.assertGreater(final, initial)

    def test_maximum_zoom(self):
        "User zooms in until the maximum zoom limit is reached"
        w = self.window

        for _ in repeat(None, 20):
            w.zoom_in()

        self.assertEqual(w.boxes_view.MAXIMUM_ZOOM,
                         w.boxes_view.absolute_zoom)

        # Another zoom in makes no difference
        w.zoom_in()
        self.assertEqual(w.boxes_view.MAXIMUM_ZOOM,
                         w.boxes_view.absolute_zoom)

    def test_initial_zoom(self):
        "Newly loaded document is shown fully zoomed out"
        w = self.window

        initial = w.boxes_view.absolute_zoom
        w.zoom_out()
        final = w.boxes_view.absolute_zoom
        self.assertEqual(initial, final)

    def test_zoom_out(self):
        "Zoom in then out"
        w = self.window

        initial = w.boxes_view.absolute_zoom
        w.zoom_in()
        w.zoom_out()
        final = w.boxes_view.absolute_zoom
        self.assertEqual(initial, final)

    def test_zoom_home(self):
        "Zoom in the all the way out"
        w = self.window

        initial = w.boxes_view.absolute_zoom
        w.zoom_in()
        w.zoom_in()
        w.zoom_in()

        w.zoom_home()
        final = w.boxes_view.absolute_zoom
        self.assertEqual(initial, final)

    def test_toggle_zoom_to_selection(self):
        "Toggles between zooming in on the selected box and zooming out"
        w = self.window

        w.zoom_home()       # TODO LH This should not be necessary

        initial = w.boxes_view.absolute_zoom

        # Select the first box
        w.select_next_prev(next=True)

        # Zoom in on the selected item
        w.toggle_zoom_to_selection()
        self.assertGreater(w.boxes_view.absolute_zoom, initial)

        # Zoom all the way out
        w.zoom_home()

        final = w.boxes_view.absolute_zoom
        self.assertEqual(initial, final)


if __name__ == '__main__':
    unittest.main()
